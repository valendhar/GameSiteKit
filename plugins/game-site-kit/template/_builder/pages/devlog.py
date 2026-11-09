"""DevLog: development videos, newest first. Add an entry at the top of VIDEOS (the add-devlog-video skill does it).
provider is "loom", "youtube" or "vimeo"; id is the video's ID from its share link; ratio comes from its oEmbed width and height."""

EMBED = {"loom": "https://www.loom.com/embed/{id}", "youtube": "https://www.youtube-nocookie.com/embed/{id}", "vimeo": "https://player.vimeo.com/video/{id}"}
LINK = {"loom": "https://www.loom.com/share/{id}", "youtube": "https://www.youtube.com/watch?v={id}", "vimeo": "https://vimeo.com/{id}"}

VIDEOS = [
    # dict(provider="loom", id="...", ratio="16 / 9", minutes=("2 minutes", "2 Minuten"), when=("January 2027", "Januar 2027"),
    #      title=("First greybox", "Erste Greybox"), text=("What the video shows.", "Was das Video zeigt.")),
]


def devlog(ctx):
    t = ctx.t
    if not VIDEOS:
        return f'<div class="wrap section"><p>{t("The first video is coming soon.", "Das erste Video kommt bald.")}</p></div>'
    items = []
    for n, v in enumerate(VIDEOS):
        title = t(*v["title"])
        items.append(f"""<article class="devlog-entry">
  <div class="devlog-video" style="aspect-ratio:{v['ratio']}"><iframe src="{EMBED[v['provider']].format(id=v['id'])}" title="{title}"
    loading="{'eager' if n == 0 else 'lazy'}" allow="fullscreen; picture-in-picture" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div>
  <div><p class="kicker">{t(*v['when'])} · {t(*v['minutes'])}</p><h2>{title}</h2><p>{t(*v['text'])}</p>
  <p><a href="{LINK[v['provider']].format(id=v['id'])}" target="_blank" rel="noopener">{t("Watch on the video site", "Auf der Videoseite ansehen")}</a></p></div>
</article>""")
    return f'<div class="wrap section">{"".join(items)}</div>'


PAGES = {"devlog/index.html": dict(title=("DevLog", "DevLog"), lede=("The game as it is being built.", "Das Spiel, während es entsteht."), body=devlog)}
