# Game Site Kit

A Claude Code plugin for building and maintaining a website for your game: from an empty folder to a live
GitHub Pages site, and then every new picture, story change and DevLog video after that.

## Skills
| Skill | Use it to |
|---|---|
| `setup-site-repo` | Start a site from the template, create the GitHub repository and turn on GitHub Pages. |
| `design-game-site` | Read your game design doc and first images, plan the pages, give the site its own look, write the texts. Uses the `design` plugin's skills when installed. |
| `plan-image-prompts` | Write an ordered list of image-generator prompts: references first, then the pictures that copy them. |
| `review-inbox-image` | Review a new image from the inbox against the current one and the canon; approve and file it, or give an exact fix. |
| `propagate-design-change` | Rename a place or character, or change a symbol, colour or look, everywhere at once. |
| `audit-site-images` | List every image the site shows, page by page, and find the ones that still show an old design. |
| `add-devlog-video` | Add a Loom, YouTube or Vimeo video to the DevLog in every language. |
| `publish-site` | Build, check locally, commit and push. |
| `key-art-assets` | Make splash screens, thumbnails and a share image from the key art and the logo. |
| `engine-handoff` | Write a handoff for your Unreal, Unity or Godot project about changed names and designs. |

Run a skill with `/game-site-kit:<skill>` or just ask in your own words ("I put the new knight portrait in the
inbox", "rename the castle to Greyhold").

## How a site is organised
See [reference/conventions.md](reference/conventions.md). In short: pages are small Python files in
`_builder/pages/`, images go in `_builder/images/` by ID, new versions wait in `_builder/images/inbox/`, and
everything private (design doc, canon of decisions, prompt list) lives in `_private/`, which is never published.
The **canon** (`_private/canon.md`) is the single place for names, symbols, colours and looks; every skill reads it.

## Needs
- Python 3.10+ with Pillow and numpy: `python -m pip install --user pillow numpy`
- Git and GitHub CLI (`gh auth login`) for the repository and publishing
- Optional: Anthropic's `design` plugin (design-critique, design-system, ux-copy, accessibility-review) and
  `frontend-design`, which the design and review skills use when present
