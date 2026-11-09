"""Concept Art: every image in _builder/images/sheets/<group>/ appears under its group, newest work first in the folder order.
Group names come from GROUPS; a folder that isn't listed still shows, under its own name."""
from pathlib import Path

SHEETS = Path(__file__).resolve().parent.parent / "images" / "sheets"
GROUPS = {
    "characters": ("Characters", "Figuren"),
    "creatures": ("Creatures", "Kreaturen"),
    "buildings": ("Buildings", "Gebäude"),
    "props": ("Props", "Requisiten"),
    "environment": ("Environment", "Umgebung"),
}


def concept(ctx):
    t = ctx.t
    out = []
    folders = sorted(p for p in SHEETS.iterdir() if p.is_dir()) if SHEETS.exists() else []
    for folder in folders:
        ids = [f.stem.strip().upper() for f in sorted(folder.iterdir()) if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
        if ids:
            name = t(*GROUPS.get(folder.name, (folder.name.title(),)))
            out.append(f'<section class="section"><h2>{name}</h2>{ctx.gallery([(i, None) for i in ids])}</section>')
    if not out:
        out.append(f'<p>{t("The first concept art is on its way.", "Die erste Konzeptkunst ist unterwegs.")}</p>')
    return f'<div class="wrap">{"".join(out)}</div>'


PAGES = {"concept/index.html": dict(title=("Concept Art", "Konzeptkunst"),
                                    lede=("Design sheets for the world, its people and its places.", "Designblätter für die Welt, ihre Leute und ihre Orte."),
                                    body=concept)}
