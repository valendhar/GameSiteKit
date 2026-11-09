"""Home page: key art with the title, a short pitch, and the main facts. Replace the texts with the game's own."""


def home(ctx):
    t = ctx.t
    facts = [
        (t("Genre", "Genre"), t("Write the genre here", "Genre hier eintragen")),
        (t("Platform", "Plattform"), t("PC", "PC")),
        (t("Status", "Status"), t("In development", "In Entwicklung")),
    ]
    dl = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in facts)
    return f"""
<section class="hero">{ctx.figure("KEYART", alt=t("Key art", "Key Art"), eager=True, link=False)}
  <div class="hero-copy wrap"><h1>{ctx.site["title"]}</h1>
  <p class="hook">{t("One sentence that makes someone want to play.", "Ein Satz, der Lust aufs Spielen macht.")}</p></div>
</section>
<section class="wrap section intro">
  <div class="prose"><p class="big">{t("Two or three sentences about the world, the player and what they do.",
                                        "Zwei oder drei Sätze über die Welt, die Spielfigur und was sie tut.")}</p></div>
  <dl class="facts">{dl}</dl>
</section>
"""


PAGES = {"index.html": dict(title=("Home", "Start"), body=home, bare=True, og="KEYART")}
