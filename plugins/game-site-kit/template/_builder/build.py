"""Static site builder for a game website: Python pages, any number of languages, and an image pipeline.

    python _builder/build.py            # builds into the repository root (what GitHub Pages serves)

- site.json (repo root) holds the title, languages, navigation and image folders.
- Every module in _builder/pages/ defines PAGES = {"path/name.html": dict(title=(...), lede=(...), body=function)}.
  body(ctx) returns HTML. Texts are tuples with one entry per language, in the order of site.json "languages";
  ctx.t("English", "Deutsch") picks the current one.
- Images: put sources in _builder/images/<folder>/ (folders listed in site.json "image_folders"; a later folder wins
  when two files share a name). Each becomes assets/img/full/<ID>.webp and assets/img/thumb/<ID>.webp, where <ID> is
  the file name without extension, upper-cased. ctx.figure("KEYART") shows one; a missing image becomes a labelled
  placeholder, so pages can be written before the art exists.
- The first language is built at the root, every other one under /<lang>/.
- Sections: a nav entry in site.json may list "pages" (each {"path", "title", optional "short"}). Every page of such a
  section gets a tab strip under its title, showing all the section's pages and "Page 2 of 4", which stays in view
  while scrolling, and Previous / Next links at the bottom. "short" is a shorter tab name when the titles don't fit.
"""
import html
import importlib
import json
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONFIG = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
LANGS = CONFIG["languages"]
IMG_IN = HERE / "images"
IMG_OUT = ROOT / "assets" / "img"
FULL_MAX, THUMB_MAX = 1920, 640
IMAGES = {}  # ID -> dict(w, h, tw, th)


def esc(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- images
def process_images():
    for k in ("full", "thumb"):
        (IMG_OUT / k).mkdir(parents=True, exist_ok=True)
    chosen = {}
    for folder in CONFIG.get("image_folders", ["originals"]):
        for src in sorted((IMG_IN / folder).rglob("*")):
            if src.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
                chosen[src.stem.strip().strip(",").upper()] = src  # stray spaces and commas happen when saving
    for img_id, src in chosen.items():
        full, thumb = IMG_OUT / "full" / f"{img_id}.webp", IMG_OUT / "thumb" / f"{img_id}.webp"
        if not (full.exists() and full.stat().st_mtime >= src.stat().st_mtime):
            with Image.open(src) as im:
                im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
                f = im.copy(); f.thumbnail((FULL_MAX, FULL_MAX), Image.LANCZOS); f.save(full, "WEBP", quality=82, method=6)
                t = im.copy(); t.thumbnail((THUMB_MAX, THUMB_MAX), Image.LANCZOS); t.save(thumb, "WEBP", quality=80, method=6)
        with Image.open(full) as f, Image.open(thumb) as t:
            IMAGES[img_id] = dict(w=f.width, h=f.height, tw=t.width, th=t.height)
    # web copies whose sources are not in the repository (private or archived originals) still count
    for full in (IMG_OUT / "full").glob("*.webp"):
        i = full.stem.upper()
        if i not in IMAGES and (IMG_OUT / "thumb" / full.name).exists():
            with Image.open(full) as f:
                IMAGES[i] = dict(w=f.width, h=f.height, tw=f.width, th=f.height)


# ---------------------------------------------------------------- page context
class Ctx:
    def __init__(self, lang, path):
        self.lang, self.path = lang, path
        self.site = CONFIG  # site.json, e.g. ctx.site['title']
        self.li = LANGS.index(lang)
        depth = path.count("/") + (0 if lang == LANGS[0] else 1)
        self.root = "../" * depth

    def t(self, *texts):
        """One text per language, in site.json order; falls back to the first."""
        return texts[self.li] if self.li < len(texts) else texts[0]

    def url(self, target):
        return self.root + ("" if self.lang == LANGS[0] else self.lang + "/") + target

    def asset(self, target):
        return self.root + target

    def lang_url(self, lang):
        return self.root + ("" if lang == LANGS[0] else lang + "/") + self.path

    def has(self, img_id):
        return img_id.upper() in IMAGES

    def img_src(self, img_id, kind="thumb"):
        return f"{self.root}assets/img/{kind}/{img_id.upper()}.webp"

    def figure(self, img_id, caption=None, alt=None, eager=False, link=True):
        img_id = img_id.upper()
        alt = esc(alt or caption or img_id)
        cap = f"<figcaption>{caption}</figcaption>" if caption else ""
        if img_id not in IMAGES:
            return f'<figure class="ph" role="img" aria-label="{alt}"><span>{esc(caption or img_id)}</span>{cap}</figure>'
        m = IMAGES[img_id]
        load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
        img = f'<img src="{self.img_src(img_id)}" alt="{alt}" width="{m["tw"]}" height="{m["th"]}" {load}>'
        if link:
            img = f'<a href="{self.img_src(img_id, "full")}" class="zoom">{img}</a>'
        return f"<figure>{img}{cap}</figure>"

    def gallery(self, items, cls="gallery"):
        """A grid of pictures. A picture not made yet is left out rather than shown as an empty box among finished art,
        unless none is made. Add "square" to cls for square tiles that fill (materials, textures)."""
        made = [(i, c) for i, c in items if self.has(i)]
        return f'<div class="{cls}">' + "".join(self.figure(i, c) for i, c in (made or items)) + "</div>"


# ---------------------------------------------------------------- sections
def title_of(entry, lang, short=False):
    names = entry.get("short") if short and entry.get("short") else entry["title"]
    return names.get(lang, names[LANGS[0]])


def section_of(path):
    """The nav entry whose "pages" include this page, when it has more than one page."""
    for n in CONFIG["nav"]:
        if len(n.get("pages", [])) > 1 and any(p["path"] == path for p in n["pages"]):
            return n
    return None


def section_tabs(ctx):
    sec = section_of(ctx.path)
    if not sec:
        return ""
    pages = sec["pages"]
    tabs = "".join(f'<li><a href="{ctx.url(p["path"])}"{" aria-current=\"page\"" if p["path"] == ctx.path else ""}>'
                   f'{esc(title_of(p, ctx.lang, short=True))}</a></li>' for p in pages)
    pos = [p["path"] for p in pages].index(ctx.path) + 1
    name = title_of(sec, ctx.lang)
    return (f'<nav class="section-tabs" aria-label="{esc(name)}"><div class="wrap st-inner">'
            f'<a class="st-name" href="{ctx.url(pages[0]["path"])}">{esc(name)}</a><ol class="st-list">{tabs}</ol>'
            f'<span class="st-count">{ctx.t(f"Page {pos} of {len(pages)}", f"Seite {pos} von {len(pages)}")}</span></div></nav>')


def pager(ctx):
    sec = section_of(ctx.path)
    if not sec:
        return ""
    pages = sec["pages"]
    i = [p["path"] for p in pages].index(ctx.path)
    prev_ = (f'<a class="prev" href="{ctx.url(pages[i - 1]["path"])}"><small>{ctx.t("Previous", "Zurück")}</small>'
             f'{esc(title_of(pages[i - 1], ctx.lang))}</a>') if i > 0 else "<span></span>"
    next_ = (f'<a class="next" href="{ctx.url(pages[i + 1]["path"])}"><small>{ctx.t("Next", "Weiter")}</small>'
             f'{esc(title_of(pages[i + 1], ctx.lang))}</a>') if i + 1 < len(pages) else "<span></span>"
    return f'<nav class="pager wrap" aria-label="{ctx.t("Pages", "Seiten")}">{prev_}{next_}</nav>'


# ---------------------------------------------------------------- layout
def layout(ctx, page, body):
    t = ctx.t
    title = t(*page["title"])
    cur_page, cur_lang = ' aria-current="page"', ' aria-current="true"'
    def nav_link(n):
        here = n["path"] == ctx.path or any(p["path"] == ctx.path for p in n.get("pages", []))
        return f'<a href="{ctx.url(n["path"])}"{cur_page if here else ""}>{esc(title_of(n, ctx.lang))}</a>'
    nav = "".join(nav_link(n) for n in CONFIG["nav"])
    names = CONFIG.get("language_names", {})
    langs = "".join(f'<a href="{ctx.lang_url(l)}" hreflang="{l}"{cur_lang if l == ctx.lang else ""}>{esc(names.get(l, l))}</a>'
                    for l in LANGS) if len(LANGS) > 1 else ""
    lede = f'<p class="lede">{t(*page["lede"])}</p>' if page.get("lede") else ""
    head_title = esc(CONFIG["title"] if ctx.path == "index.html" else f'{title} · {CONFIG["title"]}')
    desc = esc(t(*page["description"]) if page.get("description") else CONFIG["tagline"])
    og = page.get("og")
    og_tag = f'<meta property="og:image" content="{CONFIG["base_url"]}assets/img/full/{og}.webp">' if og and og.upper() in IMAGES else ""
    hero = "" if page.get("bare") else f'<header class="page-head wrap"><h1>{title}</h1>{lede}</header>'
    return f"""<!doctype html>
<html lang="{ctx.lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{head_title}</title><meta name="description" content="{desc}">
<meta property="og:title" content="{head_title}"><meta property="og:description" content="{desc}">{og_tag}
<link rel="stylesheet" href="{ctx.asset('assets/css/site.css')}">
</head>
<body>
<a class="skip" href="#main">{t("Skip to content", "Zum Inhalt springen")}</a>
<header class="site-head"><div class="wrap">
  <a class="brand" href="{ctx.url('index.html')}">{esc(CONFIG["title"])}</a>
  <nav aria-label="{t('Main', 'Hauptmenü')}">{nav}</nav>
  <div class="langs">{langs}</div>
</div></header>
<main id="main">{hero}{"" if page.get("bare") else section_tabs(ctx)}{body}{pager(ctx)}</main>
<footer class="site-foot"><div class="wrap"><p>{esc(CONFIG["title"])} · {esc(CONFIG["tagline"])}</p></div></footer>
<script src="{ctx.asset('assets/js/site.js')}" defer></script>
</body>
</html>
"""


def main():
    process_images()
    sys.path.insert(0, str(HERE))
    pages = {}
    for f in sorted(f for f in (HERE / "pages").glob("*.py") if not f.name.startswith("_")):
        pages.update(importlib.import_module(f"pages.{f.stem}").PAGES)
    n = 0
    for lang in LANGS:
        for path, page in pages.items():
            ctx = Ctx(lang, path)
            out = ROOT / ("" if lang == LANGS[0] else lang) / path
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(layout(ctx, page, page["body"](ctx)), encoding="utf-8")
            n += 1
    print(f"Built {n} pages, {len(IMAGES)} images -> {ROOT}")


if __name__ == "__main__":
    main()
