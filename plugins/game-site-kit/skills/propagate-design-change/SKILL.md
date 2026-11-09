---
name: propagate-design-change
description: Apply a story or design decision (a renamed place or character, a new symbol, a changed colour or look) everywhere - canon, every page in every language, the image prompt list, and edits for finished images that show the old version. Use when the user says "rename X to Y", "X should now look like…", "change the colour of…", or decides something new about the world.
argument-hint: "<the decision>"
---

# Propagate a design change

Decision: $ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/reference/conventions.md` and `_private/canon.md` first.

## 1. Settle it
If the decision has open parts, give a recommendation with reasons (one option, then alternatives briefly) and
let the user choose. Think about the knock-on effects and name them:
- Does it clash with something else (two factions sharing a colour, a symbol that now means two things)?
- Names in every site language: a direct translation, a native name, or the same word? Articles and plurals?
- Real-world sensitivities: protected coats of arms, brand look-alikes, real religious or political symbols.
Write the result into the canon with today's date.

## 2. Find every occurrence
Search the page sources (`_builder/pages/`, `site.json`, any translation tables), `_private/prompts.md`, and
handoff documents for the old name or look, in every language and spelling (plural, possessive, compound words).
Text in other languages is often written separately, not translated at build time, so search each language.

## 3. Change it
- Pages: every language. Keep IDs, file names and URLs stable unless the user wants them changed.
- Prompts: every entry not made yet, and the descriptions people and places are built from.
- Finished images that show the old version: add edit entries to the prompt list (after the references they need,
  in website order), and tell the user which ones are on the live site.
- Handoffs to other projects (game engine docs): update their name map (see `engine-handoff`).

## 4. Verify
Build, then search the built HTML of every language and the prompt list for the old terms; there must be none
left except where the old term is intended. Report what changed, where, and which images still need new versions.
Commit and push only when the user says so.
