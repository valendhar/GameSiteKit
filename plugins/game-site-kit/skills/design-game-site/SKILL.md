---
name: design-game-site
description: Design and write the first version of a game's website from its game design document and first images - site map, visual identity, page texts in every language - using the design plugin's skills. Use after setup-site-repo, or when someone says "design the website", "make the pages from my GDD", or "give the site its own look".
argument-hint: "<path to game design doc> [image folder]"
---

# Design the game website

Input: $ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/reference/conventions.md` and the site's `_private/canon.md` first.

## 1. Read the material
- The game design document (any format: read PDFs with the pdf skill, Word with docx). Copy it to `_private/`.
- The images the user gives. Put pictures in `_builder/images/originals/`, people in `characters/`, sheets in
  `sheets/<group>/`, named by a short ID (`KEYART`, `HERO-…`). Look at each one.
- Write what you learn into `_private/canon.md`: world, factions, names (in every site language), symbols,
  colours, characters' looks, the player's role, the core loop, what is public and what stays private.
  Ask the user about anything the site would state that the document doesn't settle.

## 2. Plan the site (show the plan before building)
Propose a site map from the content, usually:
- **Home**: key art with the title, one-line hook, short pitch, key facts, links into the rest.
- **The Game**: pillars of the design, the core loop, classes/jobs/roles, combat, progression.
- **World**: regions and places, each with a picture.
- **Characters**: the people the player meets; creatures and enemies.
- **Journey** (if the game has a story or a vertical slice): acts or steps in order.
- **Art**: picture galleries. **Concept Art**: sheets by group (the template page does this automatically).
- **DevLog**: development videos. **Media/Press**: logo, key art, contact.
Mark each page's images by ID; missing ones show as placeholders until they exist.

## 3. Visual identity
Use the design plugin's skills when they are available (they are named `design:...`):
- `design:design-system` to define tokens: 4–6 named colours, type roles, spacing, the one memorable device.
  Take colours from the key art and the game's factions, not from generic defaults.
- `frontend-design:frontend-design` (if installed) for direction: avoid the templated looks it lists.
- `design:ux-copy` for headings, buttons and short texts.
- `design:accessibility-review` on the built pages: contrast, focus, alt texts, reduced motion.
Put the tokens in `assets/css/site.css` (`:root` variables) and adjust the layout CSS. Fonts from Google Fonts are
fine; load them in `build.py`'s `<head>`.

## 4. Build the pages
Edit or add modules in `_builder/pages/` (each defines `PAGES`; texts are tuples, one per language in `site.json`
order). Add each new page to `site.json` `nav` if it belongs in the menu. When a menu entry has more than one
page, list them under its `pages` (each `{"path", "title"}`, plus a shorter `"short"` tab name if the titles are
long): every page of that section then shows a tab strip with all its pages and "Page 2 of 4", which stays in view
while scrolling, and Previous / Next links at the bottom, so visitors see that a section has more pages. Galleries
leave out pictures that aren't made yet; use `ctx.gallery(items, "gallery square")` for square textures. Write player-facing copy: concrete,
plain, no hype, consistent names from the canon. Give every image an alt text.

## 5. Check
Run `python _builder/dev.py` and check every page in the browser (desktop and ~400 px phone width, every
language): layout, overflow, placeholders, links, the language switch, and on every section page that the tab
strip shows all the section's pages (on a phone it scrolls sideways, with the current page in the middle). Fix, then ask the user whether to commit
and push (see `publish-site`).

## 6. Next steps to offer
- `plan-image-prompts` to make the missing pictures and sheets in a consistent style.
- `key-art-assets` once there is key art and a logo.
