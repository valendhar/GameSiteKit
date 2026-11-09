"""Make a transparent copy of a character image on a plain light background, without a white halo.

    python cutout.py <source> <destination.png> [--tol=14] [--band=14] [--shadow]

How it works (see cutout() below): a smooth background gradient is fitted to the image's top and upper sides; background
is what is reachable from the border and close to it, plus enclosed smooth colourless pockets (between hair strands,
inside staff rings); warm or tinted pixels (cream cloth, blond highlights) always count as the figure. Along the edge,
alpha follows the distance from the background and half-transparent pixels take their colour from the figure next to
them, so no white bleeds into hair. --shadow keeps a soft ground shadow (full bodies and line-ups). Needs numpy and Pillow.
"""
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


def background_surface(a, mask):
    """A smooth colour gradient fitted to the pixels in mask (the backgrounds have soft gradients)."""
    h, w, _ = a.shape
    yy, xx = np.mgrid[0:h, 0:w]
    x, y = xx / w - .5, yy / h - .5
    # a flat gradient: a curved surface fitted to the top drifts far off towards the bottom of a portrait
    terms = np.stack([np.ones_like(x), x, y], -1)
    out = np.zeros_like(a)
    t = terms[::3, ::3][mask[::3, ::3]]
    for c in range(3):
        coef, *_ = np.linalg.lstsq(t, a[::3, ::3, c][mask[::3, ::3]], rcond=None)
        out[..., c] = terms @ coef
    return out


def box(m, r):
    """Mean over a (2r+1) square around each pixel."""
    p = np.pad(m, r + 1, mode="edge").cumsum(0).cumsum(1)
    k = 2 * r + 1
    return (p[k:, k:] - p[:-k, k:] - p[k:, :-k] + p[:-k, :-k])[:m.shape[0], :m.shape[1]] / (k * k)


def shift(m, dy, dx):
    return np.roll(np.roll(m, dy, 0), dx, 1)


def flood(near):
    """Background reachable from the image border through 'near' pixels."""
    h, w = near.shape
    seen = np.zeros((h, w), bool)
    # from the top and both sides (not the bottom row, where portraits are cut off); it only enters background-like pixels
    q = deque([(0, x) for x in range(w)] + [(y, 0) for y in range(h)] + [(y, w - 1) for y in range(h)]
              + [(h - 1, x) for x in range(w) if near[h - 1, x] and near[h - 2, x] and near[h - 6, x]])
    while q:
        y, x = q.popleft()
        if y < 0 or x < 0 or y >= h or x >= w or seen[y, x] or not near[y, x]:
            continue
        seen[y, x] = True
        q.extend([(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)])
    return seen


def components(m, min_size):
    """Connected regions of m with at least min_size pixels."""
    h, w = m.shape
    done = np.zeros((h, w), bool)
    keep = np.zeros((h, w), bool)
    for y0, x0 in zip(*np.nonzero(m)):
        if done[y0, x0]:
            continue
        region, q = [], deque([(y0, x0)])
        done[y0, x0] = True
        while q:
            y, x = q.popleft()
            region.append((y, x))
            for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= ny < h and 0 <= nx < w and m[ny, nx] and not done[ny, nx]:
                    done[ny, nx] = True
                    q.append((ny, nx))
        if len(region) >= min_size:
            ys, xs = zip(*region)
            keep[ys, xs] = True
    return keep


def cutout(src, dst, tol=14, band=14, shadow=False, **_):
    """Transparent copy of a figure on a plain light background.

    1. A smooth background surface is fitted to the image border, then refined on everything that looks like background.
    2. Background = what is reachable from the border and close to that surface, plus enclosed pockets (between hair
       strands, inside staff rings) that are just as close to it and colourless.
    3. In a soft zone of `band` pixels around the background, alpha follows the distance from the background colour,
       and the colour of half-transparent pixels is taken from the figure next to them, so no white bleeds into hair.
    """
    a = np.asarray(Image.open(src).convert("RGB"), float)
    h, w, _ = a.shape
    border = np.zeros((h, w), bool)
    border[:12] = True
    border[:int(h * .7), :12] = border[:int(h * .7), -12:] = True  # the upper sides: the lower ones may hold a cut-off figure
    bg = background_surface(a, border)
    for _ in range(2):
        d = np.abs(a - bg).max(-1)
        seen = flood(d < tol)
        bg = background_surface(a, seen & (d < tol * .6))
    # colour beyond the background's own tint: pale cream cloth has it, white haze and grey background don't
    tint = np.clip((a.max(-1) - a.min(-1)) - (bg.max(-1) - bg.min(-1)) - 4, 0, None)
    # warmth beyond the background's: cream cloth and blond hair are warmer than the cool white or grey background,
    # even where a highlight makes them almost as bright
    warm = np.abs((a[..., 0] - a[..., 2]) - (bg[..., 0] - bg[..., 2]))
    d = np.maximum(np.maximum(np.abs(a - bg).max(-1), tint * 2.5), np.clip(warm - 3, 0, None) * 2.5)
    sat = tint
    seen = flood(d < tol)
    # enclosed pockets of background: as close to the surface as the open background, and without colour
    # ... and as smooth as background: reflections on steel are just as pale but streaked, and must stay
    lum = a.mean(-1)
    blur, blur2 = box(lum, 3), box(lum * lum, 3)
    smooth = np.sqrt(np.clip(blur2 - blur * blur, 0, None)) < 1.2
    same_light = np.abs(lum - bg.mean(-1)) < 4
    pockets = components((d < tol * .5) & (sat < 2) & smooth & same_light & ~seen, 30)
    seen |= pockets
    if shadow:  # soft neutral ground shadows also count as background
        ground = np.zeros((h, w), bool)
        ground[int(h * .9):] = True
        seen |= flood((d < tol) | ((sat < 18) & (a.mean(-1) > bg.mean() * .42) & ground))
    # close narrow fingers of "background" that crept along a pale outline into the cloth; gaps that really are background
    # are still found by the colour check in the soft zone below
    S = Image.fromarray((seen * 255).astype("uint8"))
    seen = np.asarray(S.filter(ImageFilter.MinFilter(7)).filter(ImageFilter.MaxFilter(7)), bool) | (seen & (d < tol * .35))
    # soft zone around the background
    zone = np.asarray(Image.fromarray((seen * 255).astype("uint8")).filter(ImageFilter.MaxFilter(band * 2 + 1)), bool) & ~seen
    alpha = np.ones((h, w))
    alpha[seen] = 0
    # shading on pale cloth is darker than the background and must stay solid; leftover haze is lighter
    shade = np.clip(bg.mean(-1) - a.mean(-1), 0, None) * .8
    dz = np.maximum(d, shade)
    alpha[zone] = np.clip((dz[zone] - 8) / 46, 0, 1) ** 1.5  # pulled in a little, so no pale rim is left
    # pull the outer edge in by about a pixel, where the last light rim of the old background sits
    alpha = np.minimum(alpha, np.clip(box(alpha, 1) * 1.2, 0, 1))
    # colour of the figure next to each half-transparent pixel, spread outwards from the solid inside
    solid = alpha >= .97
    col = np.where(solid[..., None], a, 0.0)
    filled = solid.copy()
    for _ in range(band + 4):
        acc = np.zeros_like(a); n = np.zeros((h, w))
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
            f = shift(filled, dy, dx)
            acc += shift(col, dy, dx) * f[..., None]
            n += f
        new = ~filled & (n > 0)
        col[new] = acc[new] / n[new, None]
        filled |= new
    al = alpha[..., None]
    unmixed = np.clip((a - (1 - al) * bg) / np.maximum(al, .05), 0, 255)
    # the fainter a pixel, the more its colour comes from the figure beside it instead of the un-mixed estimate
    trust = np.clip(al * 1.6 - .6, 0, 1)
    rgb = np.where(filled[..., None], unmixed * trust + col * (1 - trust), unmixed)
    rgb[alpha <= 0] = 0
    if shadow:
        darkness = np.clip((bg.mean(-1) - a.mean(-1)) / np.maximum(bg.mean(-1), 1), 0, 1)
        ground_shadow = seen & (np.arange(h)[:, None] > h * .85)
        alpha[ground_shadow] = np.clip(darkness[ground_shadow] * 1.1, 0, .75)
        rgb[ground_shadow] = 0
    out = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype("uint8")
    Image.fromarray(out, "RGBA").save(dst)
    print(Path(dst).name, "transparent", round(float((alpha < .05).mean()), 3))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = {a.split("=", 1)[0]: (a.split("=", 1)[1] if "=" in a else True) for a in sys.argv[1:] if a.startswith("--")}
    if len(args) != 2:
        sys.exit(__doc__)
    cutout(args[0], args[1], tol=int(opts.get("--tol", 13)), band=int(opts.get("--band", 4)), shadow=bool(opts.get("--shadow")))
