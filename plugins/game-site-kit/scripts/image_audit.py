"""List every image each built page shows, page by page, starting at the home page, with where its source file is.

    python image_audit.py <site root> [--since=YYYY-MM-DD] [--json]

Pages are read from the built HTML of the first language (navigation order from site.json, then the rest).
With --since, images whose source was not changed since that date are marked "old": the candidates to check
after a design change. Each image is listed once, under the first page that shows it.
"""
import json
import re
import sys
import time
from pathlib import Path

EXTS = (".png", ".jpg", ".jpeg", ".webp")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = {a.split("=", 1)[0]: (a.split("=", 1)[1] if "=" in a else True) for a in sys.argv[1:] if a.startswith("--")}
    if not args:
        sys.exit(__doc__)
    site = Path(args[0]).resolve()
    cfg = json.loads((site / "site.json").read_text(encoding="utf-8"))
    langs = cfg["languages"]
    since = time.mktime(time.strptime(opts["--since"], "%Y-%m-%d")) if "--since" in opts else None
    sources = {}
    for d in cfg.get("image_folders", ["originals"]):
        for f in (site / "_builder" / "images" / d).rglob("*"):
            if f.suffix.lower() in EXTS:
                sources[f.stem.strip().strip(",").upper()] = f
    others = [p for p in site.rglob("*.html") if not any(part in ("_builder", "_private", ".git") for part in p.parts)
              and not (len(langs) > 1 and p.relative_to(site).parts[0] in langs[1:])]
    order = [site / n["path"] for n in cfg["nav"]] + sorted(set(others) - {site / n["path"] for n in cfg["nav"]})
    seen, report = set(), []
    for page in order:
        if not page.exists():
            continue
        ids = []
        for m in re.finditer(r"assets/img/(?:full|thumb)/([A-Za-z0-9_\-]+)\.webp", page.read_text(encoding="utf-8")):
            if m[1] not in seen:
                seen.add(m[1]); ids.append(m[1])
        rows = []
        for i in ids:
            src = sources.get(i)
            state = "no source" if not src else ("old" if since and src.stat().st_mtime < since else "ok")
            rows.append(dict(id=i, source=str(src.relative_to(site)) if src else None, state=state))
        if rows:
            report.append(dict(page=str(page.relative_to(site)).replace("\\", "/"), images=rows))
    if "--json" in opts:
        print(json.dumps(report, indent=1))
        return
    for p in report:
        print(p["page"])
        for r in p["images"]:
            print(f"   {r['state']:9} {r['id']:30} {r['source'] or ''}")


main()
