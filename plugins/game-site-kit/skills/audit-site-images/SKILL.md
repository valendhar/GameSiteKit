---
name: audit-site-images
description: List every image the website shows, page by page from the home page, and find which ones still show an old design, so the image work can be ordered by what visitors see. Use after a design change, or when the user asks "which images need fixing", "what's left on the site", or wants the prompt list in website order.
argument-hint: "[--since=YYYY-MM-DD]"
---

# Audit the site's images

Read `${CLAUDE_PLUGIN_ROOT}/reference/conventions.md` and `_private/canon.md` first.

1. Build the site, then list the images per page:
   ```
   python "${CLAUDE_PLUGIN_ROOT}/scripts/image_audit.py" <site root> --since=<date of the design change>
   ```
   Each image appears once, under the first page that shows it. "old" means its source wasn't changed since that
   date; "no source" means only the published web copy exists.
2. Look at every "old" image (make a contact sheet with PIL, 9 per sheet, and zoom into suspicious areas) and
   check it against the canon: names, symbols, colours, looks, buildings. Note exactly what's wrong in each.
3. Images that are fine stay as they are. For the rest, add edit entries to `_private/prompts.md` in this order:
   page by page from the home page; within a page, the references a picture copies (portrait → full body →
   scene) come right before it. Things the site doesn't show come after.
4. Report: per page, which images need an edit and why, which are fine, and the new order of the prompt list.
