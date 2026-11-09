---
name: add-devlog-video
description: Add a development video (Loom, YouTube or Vimeo) to the website's DevLog with a title and a short description in every site language. Use when the user shares a video link for the DevLog or says "add this video".
argument-hint: "<video link> [what it shows]"
---

# Add a DevLog video

Input: $ARGUMENTS

1. Get the video's facts:
   ```
   python "${CLAUDE_PLUGIN_ROOT}/scripts/video_info.py" <link>
   ```
   It gives the provider, ID, title, length and aspect ratio.
2. Write the entry at the **top** of `VIDEOS` in `_builder/pages/devlog.py`: provider, id, ratio, minutes
   (e.g. "2 minutes"), month and year, a short title and two or three sentences, in every site language.
   - Build the text from what the user says the video shows, plus the video's own title. Say what the viewer
     sees and why it matters for the game; no hype. Keep internal tool names out unless the user wants them.
   - Use the game's names from `_private/canon.md`.
3. Build and check the DevLog page in every language (the video plays, the text fits).
4. Show the user the text, and push when they say so (`publish-site`).
