---
name: key-art-assets
description: Make splash screens, square project thumbnails and a social share image from the game's key art and its transparent logo, and put them where the game engine and the website use them. Use when there is new key art or a new logo, or the user asks for a splash screen, launcher thumbnail, icon or share image.
argument-hint: "[key art ID] [logo file]"
---

# Key art assets

Input: $ARGUMENTS

1. Find the key art (usually `_builder/images/originals/KEYART.*`, without any logo) and the logo (a transparent
   PNG or WebP). Look at the key art: where is calm space for the logo (sky, upper middle)? Which part makes a good
   square close-up (the main clash or hero)?
2. Make the files:
   ```
   python "${CLAUDE_PLUGIN_ROOT}/scripts/make_key_art.py" <key art> <logo> _private/engine --name=<Game> --focus=<x,y> --logo-top=0.015 --logo-width=0.40
   ```
   It writes splash screens (1440×740, 720×370), thumbnails (512, 192) and a share image (1200×630), and moves older
   versions to `Old/` with a date.
3. Look at every result. The logo must sit on calm space, not cover a face; at 192 px the logo must still read.
   Adjust `--focus`, `--logo-top`, `--logo-width` and run again until it does.
4. Put them to use, after asking:
   - **Unreal Engine**: the 720×370 splash goes to `<project>/Content/Splash/Splash.png` and `EdSplash.png`
     (keep a copy of the old ones), the 192 thumbnail to `<project>/<Project>.png` next to the `.uproject`. Restart
     the editor to see them.
   - **Other engines**: tell the user the sizes and where their engine expects them.
   - **Website**: copy the share image to `_builder/images/originals/SHARE.png` and set `og="SHARE"` on the home
     page entry.
