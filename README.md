# Game Site Kit — plugin marketplace

This folder is a Claude Code plugin marketplace with one plugin, **game-site-kit**
([plugins/game-site-kit](plugins/game-site-kit/README.md)).

## Install
In Claude Code (an interactive `claude` terminal):
```
/plugin install game-site-kit --marketplace valendhar/GameSiteKit
```
On older Claude Code versions:
```
/plugin marketplace add valendhar/GameSiteKit
/plugin install game-site-kit@game-site-kit-marketplace
```

Licensed under the MIT License (see `LICENSE`).

## Change it
Edit the skills in `plugins/game-site-kit/skills/<name>/SKILL.md`, the scripts in `plugins/game-site-kit/scripts/`
and the starter site in `plugins/game-site-kit/template/`. Raise `version` in
`plugins/game-site-kit/.claude-plugin/plugin.json` and run `/plugin marketplace update game-site-kit-marketplace`.
