"""Splash screens, thumbnails and share images from the key art and a transparent title logo.

    python make_key_art.py <key art> <logo.png> <out folder> [--name=Game] [--logo-top=0.015] [--logo-width=0.40] [--focus=0.6,0.62]

Writes (and moves any older file of the same name to <out>/Old/ with a date first):
  Splash_<name>_1440x740.png, Splash_<name>_720x370.png    engine splash screens (Unreal uses 720x370 / larger)
  Thumbnail_<name>_512.png, Thumbnail_<name>_192.png      square project thumbnails, logo large so it reads small
  Share_<name>_1200x630.png                               social / Open Graph image
--focus is the point of the key art the square thumbnail centres on, as shares of its width and height.
"""
import shutil
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


def opts():
    return dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)


def trimmed(p):
    im = Image.open(p).convert("RGBA")
    return im.crop(im.split()[3].point(lambda v: 255 if v > 10 else 0).getbbox())


def gradient(size, a0, a1, start, end):
    w, h = size
    g = Image.new("L", (1, h))
    for y in range(h):
        t = min(max((y / h - start) / max(end - start, 1e-6), 0), 1)
        g.putpixel((0, y), int(255 * (a0 + (a1 - a0) * t)))
    layer = Image.new("RGBA", size, (8, 8, 14, 255))
    layer.putalpha(g.resize(size))
    return layer


def cover(img, w, h, cx=0.5, cy=0.5):
    s = max(w / img.width, h / img.height)
    im = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = min(max(round(im.width * cx - w / 2), 0), im.width - w)
    y = min(max(round(im.height * cy - h / 2), 0), im.height - h)
    return im.crop((x, y, x + w, y + h))


def place_logo(canvas, logo, share, top):
    w = round(canvas.width * share)
    l = logo.resize((w, round(logo.height * w / logo.width)), Image.LANCZOS)
    x, y = (canvas.width - w) // 2, round(canvas.height * top)
    halo = Image.new("RGBA", l.size, (0, 0, 0, 0))
    halo.putalpha(l.split()[3].filter(ImageFilter.GaussianBlur(max(2, w // 60))).point(lambda v: int(v * .55)))
    canvas.alpha_composite(halo, (x, y))
    canvas.alpha_composite(l, (x, y))


def save(img, out, name):
    p = out / name
    if p.exists():
        (out / "Old").mkdir(exist_ok=True)
        shutil.move(str(p), str(out / "Old" / f"{time.strftime('%Y%m%d')}_{name}"))
    img.convert("RGB").save(p)
    print("wrote", p)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 3:
        sys.exit(__doc__)
    o = opts()
    art, logo, out = Image.open(args[0]).convert("RGBA"), trimmed(args[1]), Path(args[2])
    out.mkdir(parents=True, exist_ok=True)
    name = o.get("name", "Game")
    lw, lt = float(o.get("logo-width", 0.40)), float(o.get("logo-top", 0.015))
    fx, fy = (float(v) for v in o.get("focus", "0.6,0.62").split(","))

    wide = cover(art, 1440, 740)
    wide.alpha_composite(gradient(wide.size, 0, .55, .78, 1))
    place_logo(wide, logo, lw, lt)
    for w, h in ((1440, 740), (720, 370)):
        save(wide.resize((w, h), Image.LANCZOS), out, f"Splash_{name}_{w}x{h}.png")

    share = cover(art, 1200, 630)
    share.alpha_composite(gradient(share.size, 0, .5, .75, 1))
    place_logo(share, logo, lw + .05, lt + .01)
    save(share, out, f"Share_{name}_1200x630.png")

    sq = cover(art, 1024, 1024, fx, fy)
    sq = ImageEnhance.Contrast(ImageEnhance.Color(sq.convert("RGB")).enhance(1.08)).enhance(1.06).convert("RGBA")
    sq.alpha_composite(gradient(sq.size, .78, 0, 0, .42))
    sq.alpha_composite(gradient(sq.size, 0, .45, .82, 1))
    v = Image.new("L", sq.size, 0)
    ImageDraw.Draw(v).ellipse((-200, -160, sq.width + 200, sq.height + 220), fill=255)
    edge = Image.new("RGBA", sq.size, (8, 8, 14, 255))
    edge.putalpha(v.filter(ImageFilter.GaussianBlur(120)).point(lambda p: int((255 - p) * .7)))
    sq.alpha_composite(edge)
    place_logo(sq, logo, .94, .03)
    for s in (512, 192):
        save(sq.resize((s, s), Image.LANCZOS), out, f"Thumbnail_{name}_{s}.png")


main()
