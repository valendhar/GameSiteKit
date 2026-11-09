---
name: setup-site-repo
description: Create a new game website project from the kit's template, put it in a new GitHub repository and turn on GitHub Pages so it is live. Use when someone wants to start a website for their game, "set up the site", "create the repo", or "publish the page on GitHub".
argument-hint: "[game name] [folder]"
---

# Set up a game website repository

What the user typed: $ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/reference/conventions.md` first.

## 1. Gather (ask only what you can't infer)
- Game title and a one-line tagline.
- Languages of the site (first = default, others get `/<lang>/`). Default: English only.
- Where the folder goes (default: a new folder named after the game, next to the current directory).
- GitHub account and repository name (default: the game's name in kebab-case), public or private.
  GitHub Pages on a free account needs a **public** repository; say so if they choose private.

## 2. Check the tools
Run `git --version`, `gh --version`, `gh auth status`, and `python -c "import PIL, numpy"`.
- `gh` missing or not signed in: tell the user to install GitHub CLI and run `gh auth login` themselves. Never
  ask for or type a token or password.
- Pillow or numpy missing: offer `python -m pip install --user pillow numpy`.

## 3. Create the project
1. Copy `${CLAUDE_PLUGIN_ROOT}/template/` into the new folder. Rename `gitignore.txt` to `.gitignore` and add an
   empty `.nojekyll` file, so GitHub Pages serves the files as they are instead of running Jekyll over them.
2. Fill `site.json`: title, tagline, languages, `base_url` = `https://<user>.github.io/<repo>/`, navigation titles in
   every language. Remove `"de"` titles if the site is English only (they're ignored anyway).
3. Create `_builder/images/{originals,characters,sheets,inbox,archive}` and `_private/` with an empty
   `_private/canon.md` that starts with the game's name and today's date.
4. Run `python _builder/build.py`. It must report the pages it built.

## 4. GitHub
Ask before creating anything on GitHub (it publishes the project). Then:
```
git init -b main
git add -A
git commit -m "Start the <Game> website"
gh repo create <user>/<repo> --public --source . --push
gh api -X POST repos/<user>/<repo>/pages -f "source[branch]=main" -f "source[path]=/"
```
If the Pages call says it already exists, use `-X PUT` with the same fields. Then poll
`gh api repos/<user>/<repo>/pages --jq .status` a few times (not in a tight loop) until it is `built`, and open the
URL in the browser to confirm the home page shows.

## 5. Hand over
Tell the user the live URL, the folder, how to preview (`python _builder/dev.py`), and that the next step is
`design-game-site` (look, pages and texts from their game design doc). Record the repository and URL in
`_private/canon.md` under "Project".
