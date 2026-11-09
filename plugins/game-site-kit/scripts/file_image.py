"""File an approved image: archive the old version and put the new one in its place, under the image's ID.

    python file_image.py <site root> <ID> [source file] [--folder=sheets/props] [--cutout]

- Without a source file it takes the newest image in <site>/_builder/images/inbox/ and removes it from there.
- The new file goes where the old one is (any folder under _builder/images except inbox and archive), saved as <ID>.png.
- The old one, whatever its extension, moves to _builder/images/archive/; a name that is taken gets a date and time.
- A new ID with no old file needs --folder (relative to _builder/images).
- --cutout (or a file in site.json "cutout_folder") also makes a transparent copy in originals/ with cutout.py,
  so a portrait sits on a dark page without a white box.
"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image

EXTS = (".png", ".jpg", ".jpeg", ".webp")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = {a.split("=", 1)[0]: (a.split("=", 1)[1] if "=" in a else True) for a in sys.argv[1:] if a.startswith("--")}
    if len(args) < 2:
        sys.exit(__doc__)
    site, img_id = Path(args[0]).resolve(), args[1].upper()
    img = site / "_builder" / "images"
    inbox, archive = img / "inbox", img / "archive"
    cfg = json.loads((site / "site.json").read_text(encoding="utf-8")) if (site / "site.json").exists() else {}
    if len(args) > 2:
        src = Path(args[2])
    else:
        new = sorted((f for f in inbox.glob("*.*") if f.suffix.lower() in EXTS), key=lambda f: f.stat().st_mtime)
        if not new:
            sys.exit(f"no image in {inbox}")
        src = new[-1]
    old = [f for f in img.rglob("*.*") if f.suffix.lower() in EXTS and inbox not in f.parents and archive not in f.parents
           and f.stem.strip().strip(",").upper() == img_id]
    # an image filed into the cut-out folder also has a transparent copy of the same ID in originals/: only the
    # source is replaced (the copy is remade below), so the copy must never be taken for the image's home
    in_cutout = [f for f in old if f.parent.name == cfg.get("cutout_folder", "\0")]
    if in_cutout:
        old = in_cutout
    if old:
        dest_dir = old[0].parent
    elif "--folder" in opts:
        dest_dir = img / opts["--folder"]
    else:
        sys.exit(f"{img_id} has no current file: give --folder=<folder under _builder/images>")
    dest_dir.mkdir(parents=True, exist_ok=True)
    archive.mkdir(parents=True, exist_ok=True)
    for f in old:
        target = archive / f.name
        if target.exists():
            target = archive / f"{f.stem}-{time.strftime('%Y%m%d-%H%M%S')}{f.suffix}"
        shutil.move(str(f), str(target))
        print("archived", f.relative_to(img), "->", target.relative_to(img))
    dest = dest_dir / f"{img_id}.png"
    with Image.open(src) as im:
        im.load()
        im.save(dest)
        size = im.size
    print("placed", src.name, "->", dest.relative_to(img), size)
    if src.parent == inbox:
        src.unlink()
    if opts.get("--cutout") or dest_dir.name == cfg.get("cutout_folder", "\0"):
        out = img / "originals" / f"{img_id}.png"
        subprocess.run([sys.executable, str(Path(__file__).with_name("cutout.py")), str(dest), str(out)], check=True)


main()
