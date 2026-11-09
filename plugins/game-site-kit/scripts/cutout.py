"""Make a transparent copy of a character image on a plain light background, keeping hair strands and soft edges.

    python cutout.py <source> <destination.png> [--tol=13] [--band=4] [--shadow]

The background is found by flooding from the image edges with colours close to the edge colour. Along its boundary,
pixels are 'un-mixed' from the background colour, so there is no white halo. --shadow also removes soft neutral
ground shadows in the bottom tenth (for full-body images). Needs numpy and Pillow.
"""
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageFilter


def cutout(src, dst, tol=13, band=4, shadow=False):
    a = np.asarray(Image.open(src).convert("RGB"), float)
    h, w, _ = a.shape
    edge = np.concatenate([a[:6].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)] + ([] if shadow else [a[-6:].reshape(-1, 3)]))
    bg = np.median(edge, 0)
    near = np.abs(a - bg).max(-1) < tol
    if shadow:
        sat = a.max(-1) - a.min(-1)
        ground = np.zeros((h, w), bool)
        ground[int(h * .9):] = True
        near |= (sat < 18) & (a.mean(-1) > bg.mean() * .42) & ground
    seen = np.zeros((h, w), bool)
    q = deque([(0, x) for x in range(w)] + [(h - 1, x) for x in range(w)] + [(y, 0) for y in range(h)] + [(y, w - 1) for y in range(h)])
    while q:
        y, x = q.popleft()
        if y < 0 or x < 0 or y >= h or x >= w or seen[y, x] or not near[y, x]:
            continue
        seen[y, x] = True
        q.extend(((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)))
    alpha = (~seen).astype(float)
    # soften the boundary: within `band` pixels of the background, estimate how much background is mixed in
    m = Image.fromarray((seen * 255).astype("uint8")).filter(ImageFilter.MaxFilter(band * 2 + 1))
    border = (np.asarray(m) > 0) & ~seen
    d = np.abs(a - bg).max(-1)
    alpha[border] = np.clip(d[border] / 60.0, 0, 1)
    rgb = a.copy()
    k = border & (alpha > 0.02)
    rgb[k] = (a[k] - bg * (1 - alpha[k, None])) / alpha[k, None]
    rgb[seen] = 0
    out = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype("uint8")
    Image.fromarray(out, "RGBA").save(dst)
    print(dst, "transparent share", round(float((alpha < .05).mean()), 3))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = {a.split("=", 1)[0]: (a.split("=", 1)[1] if "=" in a else True) for a in sys.argv[1:] if a.startswith("--")}
    if len(args) != 2:
        sys.exit(__doc__)
    cutout(args[0], args[1], tol=int(opts.get("--tol", 13)), band=int(opts.get("--band", 4)), shadow=bool(opts.get("--shadow")))
