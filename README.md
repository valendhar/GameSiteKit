# Game Site Kit — plugin marketplace

This folder is a Claude Code plugin marketplace with one plugin, **game-site-kit**
([plugins/game-site-kit](plugins/game-site-kit/README.md)).

## Install from this folder
In Claude Code (an interactive `claude` terminal):
```
/plugin marketplace add E:/Data/GameSiteKit
/plugin install game-site-kit@game-site-kit-marketplace
```

## Share it
Push this folder to a GitHub repository, then anyone can install it with:
```
/plugin marketplace add <github-user>/<repo>
/plugin install game-site-kit@game-site-kit-marketplace
```

## Change it
Edit the skills in `plugins/game-site-kit/skills/<name>/SKILL.md`, the scripts in `plugins/game-site-kit/scripts/`
and the starter site in `plugins/game-site-kit/template/`. Raise `version` in
`plugins/game-site-kit/.claude-plugin/plugin.json` and run `/plugin marketplace update game-site-kit-marketplace`.
