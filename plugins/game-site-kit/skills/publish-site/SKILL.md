---
name: publish-site
description: Build the game website, check it locally in a browser, and commit and push it to GitHub Pages. Use when the user says "push it", "publish", "commit and push", "update the site", or approves changes for the live site.
argument-hint: "[what this update contains]"
---

# Publish the site

Read `${CLAUDE_PLUGIN_ROOT}/reference/conventions.md` first. Publish only when the user has said so in this turn
or the request clearly asks for it.

1. **Build**: `python _builder/build.py`. It must finish without errors.
2. **Check what will go out**: `git status --short`. Every newer image goes out with the push (don't hold images
   back unless the user asked). Nothing from `_private/`, the inbox or the archive may be staged; `.gitignore`
   keeps them out — if one shows up, stop and fix the ignore rule.
3. **Check it locally** if pages or layout changed: `python _builder/dev.py`, open the changed pages in the
   browser at desktop and ~400 px width, in every language; look for placeholders, overflow, broken images and
   old names. Stop the server afterwards.
4. **Commit and push**:
   ```
   git checkout -b <short-topic>
   git add -A
   git commit -m "<what visitors will notice, in one line>" -m "<a short paragraph>"
   git checkout <main branch>
   git merge --ff-only <short-topic>
   git push origin <main branch>
   git branch -d <short-topic>
   ```
   Follow any commit attribution rules of the environment.
5. **Report**: the commit, what's live (GitHub Pages usually updates within a minute or two; a hard reload clears
   the browser cache), and what's next.
