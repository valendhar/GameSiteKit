---
name: plan-image-prompts
description: Write an ordered list of image-generator prompts (ChatGPT, Midjourney, etc.) for a game's website and concept art, so every picture matches the canon and builds on approved references. Use when the user needs pictures, character sheets, asset sheets or key art made, or asks "what should I generate next" or "write the prompts".
argument-hint: "[what to make: e.g. heroes, town, key art]"
---

# Plan the image prompts

Scope: $ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/reference/conventions.md` and `_private/canon.md` first. The list lives in
`_private/prompts.md`; keep it the single place the user works from.

## Order: references before the pictures that copy them
1. **Symbols**: coats of arms, faction signs, logo (everything later copies these).
2. **Landmarks**: the buildings and places that appear in many pictures.
3. **People**: for each character or class, a portrait first, then the full body (which copies the portrait).
   Both genders and every image of a class share one look.
4. **Pictures** for the website, in the order of the pages (home first), each after the references it uses.
5. **Sheets** that aren't needed for the website yet (asset sheets, turnarounds), last.
When the user's priority is "fix what the website shows", run `image_audit.py` (see `audit-site-images`) and put
those first, page by page.

## Each entry
```
#### <number> · <ID> · <name>
**New picture** or **Edit**, save as `_builder/images/<folder>/<ID>.png`.
**Attach:** <IDs in order: the image being edited, people, buildings/sheets, symbols>
> Review stop: <what to check before anything copies this>   (for references others depend on)
<prompt in a text block>
```
- **New picture**: subject, who is in it (each person described exactly as in the canon), place, light and time,
  the moment, composition (where the logo or text will go, if any), style line, "Exactly N people", "No text".
- **Edit**: "Edit the first attached image. Keep everything else exactly as it is… Change only these things:"
  then 1–3 numbered changes, each naming where it is in the picture.
- **Sheets**: plain background, views needed (turnarounds only for characters and their gear; asset sets get one
  three-quarter view per item so more items fit), true scale, no ground or plants unless they are the subject.
- One shared style block for the whole game, written once in the canon and pasted into every prompt.

## Keep the list consistent
When a decision changes (name, symbol, colour, look), change it in the canon and in every entry not made yet,
and add edit entries for finished images that show the old version (see `propagate-design-change`). Number new
entries after the existing ones so numbers never shift. Move finished entries to a "Done" section.
