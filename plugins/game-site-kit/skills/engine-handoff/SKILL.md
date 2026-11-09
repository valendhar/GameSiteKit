---
name: engine-handoff
description: Write a handoff document for the game engine project (Unreal, Unity, Godot) that tells another Claude session or developer which names and designs changed on the website side and what to update in the game, safely. Use when the user says the game project "still uses the old names", or asks for a handoff of design or story changes.
argument-hint: "<path to the game project>"
---

# Hand design changes over to the game project

Target: $ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/reference/conventions.md` and `_private/canon.md` first.

## 1. Survey the game project (read only)
- Its own instructions (`CLAUDE.md`, README, a step log) and where its docs live.
- Where the old names appear: docs, data tables and quest text, generators and scripts, asset folders and
  prefixes, map names. Count files per kind (`grep -rIl`), skipping build output and third-party content.

## 2. Write the handoff
Put it in the game project's docs folder (next to similar handoffs), numbered like its neighbours, with:
1. **Why and when**: which decisions, decided by whom, on which dates; "this file wins over older docs".
2. **Name map**: old name → new name in every language, with notes (articles, plurals, IDs that stay).
3. **Design decisions** the game must follow: architecture and materials with sizes, symbols and where they're
   used, colours per faction or class, characters' looks, what changed about places and the story's end.
4. **What to change, in a safe order**: docs → player-facing text (keep row names, IDs and map IDs stable) →
   generators (never their outputs, then regenerate) → assets whose design changed (one row per asset).
5. **Asset and folder renames: ask the user first.** List paths and prefixes that still carry the old name, warn
   about prefixes that clash with other meanings, recommend leaving them or doing one planned rename with
   redirects, and name the things that must never be renamed (third-party assets, map and zone IDs).
6. **Open points** and **where the source of truth is** (the canon, the approved images).

## 3. Tell the next session
Add a dated entry to the game project's step log or notes pointing to the handoff. Change nothing else in the game
project. Keep the handoff updated when later decisions come in.
