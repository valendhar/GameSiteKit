# Game Site Kit — conventions every skill follows

## Folders of a game site
```
site.json                      title, languages, navigation, image folders, dev port
_builder/build.py, dev.py      the builder (copied from the kit's template); pages in _builder/pages/*.py
_builder/images/
  originals/                   pictures: key art, scenes, action shots, transparent cut-outs
  characters/                  people: portraits and full bodies on plain backgrounds
  sheets/<group>/              concept and asset sheets, one sub-folder per Concept Art group
  inbox/                       new versions waiting for review (ignored by git)
  archive/                     replaced versions (ignored by git)
assets/                        built images and CSS (published)
_private/                      never published: game design doc, canon, prompt lists, research, handoffs
  canon.md                     names, symbols, colours, looks and rules decided so far (the source of truth)
  prompts.md                   the ordered image prompt list
```
Image IDs are file names without extension, upper-case (`KEYART`, `HERO-KNIGHT-F`, `BL-02`). The same ID is the
prompt's ID, the file name and what the pages call. A missing image shows as a labelled placeholder.

## The canon
`_private/canon.md` holds every decision about the game's world that pictures or text depend on: place and
character names (in each site language), coats of arms and symbols, colours per faction or class, what a
character looks like, materials and architecture, and things that must never appear. Every skill reads it first
and writes new decisions into it the moment the user makes them, with the date. When the canon and an older text
disagree, the canon wins.

## Working with the user
- **Commit and push only when the user says so.** Build and check locally first. Pattern: short branch, commit,
  fast-forward merge into the default branch, push, delete the branch.
- **Publish every newer image** that a build picks up; don't hold images back unless the user asks.
- **Approved means filed:** when you approve an image as final, file it yourself (archive the old, place the new,
  make cut-outs) with `scripts/file_image.py`, rebuild, and say what changed.
- **One look per character or class:** every image of the same character or class (portrait, full body, scenes,
  both genders) shares the same clothes, colours and symbols. A change to one goes to all of them.
- **Never invent a recreation of an existing game.** Original designs only; real history and real places are fine
  and can be required to be accurate when the user says so.
- **Keep private things private:** budgets, grant plans, internal tooling, build phases and unreleased business
  details stay off the public site unless the user explicitly wants them shown.
- Write player-facing copy: plain, specific, no marketing filler, sentence case, one job per sentence.

## Reviewing an image (summary, see review-inbox-image)
Compare with the current version side by side, zoom into the parts that changed, check against the canon and the
approved references, then: approve and file it, or give one exact edit prompt for the image generator and fix the
source prompt so the mistake doesn't come back.

## Image generation habits that worked
- Edits of an approved image keep its composition, faces and light; ask for **one to three changes** per edit.
- Attach references in a fixed order: the image being edited first, then the people (their approved full body),
  then the buildings or sheets, then symbol sheets (coats of arms) last.
- Say where things are and what they touch ("he stands on the wall-walk, his hand on the sill of a gap in the
  parapet"); generators invent geometry when only the material is described.
- Name the exception when a style line would mislead ("the chapel is all stone, with no half-timbering, unlike
  the town's houses").
- Carved, stitched or painted symbols: say how they are made ("cut into the stone, the same colour as the stone";
  "gold thread embroidered into the cloth, following its folds and light").
- Ask for "no text anywhere" in every prompt.
