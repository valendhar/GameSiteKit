"""Put the current image and a new version side by side, and optionally zoom into a region of the new one, for review.

    python compare_images.py <new> [old] --out=<review.jpg> [--zoom=x0,y0,x1,y1] [--height=760]

The zoom region is given as shares of the image (0 to 1), e.g. --zoom=0.25,0,0.75,0.4 for the head of a full body.
The zoom is written next to --out as <name>_zoom.jpg. Read both files to look at them.
"""
import sys
from pathlib import Path

from PIL import Image


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    if not args or "out" not in opts:
        sys.exit(__doc__)
    h = int(opts.get("height", 760))
    new = Image.open(args[0]).convert("RGB")
    ims = [Image.open(args[1]).convert("RGB")] if len(args) > 1 and Path(args[1]).exists() else []
    ims.append(new)
    ims = [i.resize((round(i.width * h / i.height), h)) for i in ims]
    sheet = Image.new("RGB", (sum(i.width for i in ims) + 20 * (len(ims) - 1), h), "white")
    x = 0
    for i in ims:
        sheet.paste(i, (x, 0)); x += i.width + 20
    out = Path(opts["out"])
    sheet.save(out, quality=88)
    print("side by side:", out, "(old left, new right)" if len(ims) == 2 else "(new only)")
    if "zoom" in opts:
        x0, y0, x1, y1 = (float(v) for v in opts["zoom"].split(","))
        W, H = new.size
        z = new.crop((int(W * x0), int(H * y0), int(W * x1), int(H * y1)))
        z = z.resize((900, round(900 * z.height / z.width)))
        zp = out.with_name(out.stem + "_zoom.jpg")
        z.save(zp, quality=90)
        print("zoom:", zp)


main()
