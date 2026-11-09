---
name: review-inbox-image
description: Review a new image the user put in the site's inbox (or pasted), compare it with the current version, approve it and file it into place, or give an exact fix. Use when the user says "I put X in the inbox", "review this image", "here is the new version of X", or sends a generated picture for the website.
argument-hint: "<image ID> [what to look at]"
---

# Review an inbox image

Request: $ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/reference/conventions.md` and `_private/canon.md` first. The prompt the image was made
from is in `_private/prompts.md` (search for its ID).

## 1. Find the files
- New version: the newest file in `_builder/images/inbox/` (names may have stray spaces or commas; that's fine).
  If the user pasted the image instead, use the pasted copy and say that a full-quality file in the inbox is better
  for later edits.
- Current version: search `_builder/images/` (not inbox/archive) for the ID.

## 2. Look closely
```
python "${CLAUDE_PLUGIN_ROOT}/scripts/compare_images.py" <new> <current> --out=<scratch>/<ID>_review.jpg --zoom=x0,y0,x1,y1
```
Read the side-by-side and the zoom (zoom into whatever the edit was about: a face, a symbol, a building). Check:
- **The asked change** happened, fully and everywhere it appears.
- **Nothing else changed**: faces, poses, clothes, composition, light.
- **Canon**: names, symbols, colours, the character's look (all images of a character or class must match).
- **Physical sense**: how people stand, hold things and touch surfaces; walls, roads and buildings that connect;
  how many arms, hands and weapons; sizes against people.
- **Leftovers** from the old design (old symbols, old colours) anywhere in the picture.
Listen to what the user says looks off; check it first and say plainly whether they're right.

## 3. Write the critique
If the `design:design-critique` skill is available, follow its structure; otherwise use: overall impression
(approved or not, in one sentence), a table of points with ✅ / 🟡 / 🔴 and a note each, then the fix.
Mention small things (🟢) without asking for a fix when they don't matter.

## 4a. Not approved
Give **one** edit prompt to paste into the image generator, in a quote block, that:
- says what to keep ("Keep everything exactly the same and change only…"),
- describes the target precisely (where, what it touches, how it's made, what must not appear),
- lists what to attach (usually only this image; plus a reference when copying a look),
- ends with "No text anywhere."
Then fix the cause at the source: update the entry in `_private/prompts.md` (and the canon if a rule was missing),
so every later prompt avoids the same mistake. Leave the image in the inbox.

## 4b. Approved
File it, then rebuild:
```
python "${CLAUDE_PLUGIN_ROOT}/scripts/file_image.py" <site root> <ID> [--folder=<folder>] [--cutout]
python _builder/build.py
```
`--cutout` makes a transparent copy for portraits shown on a dark page. Delete older tries of the same ID left in
the inbox. Tell the user: approved, where the old and new files are, which pages now show it, and what's next in
the prompt list. Push when the user says so (`publish-site`), including every newer image.
