"""The game overview: pillars of the design, each with a picture. Add more pages in this folder the same way."""

PILLARS = [
    ("PILLAR-1", ("First pillar", "Erste Säule"), ("What makes the game special, in two sentences.", "Was das Spiel besonders macht, in zwei Sätzen.")),
    ("PILLAR-2", ("Second pillar", "Zweite Säule"), ("Another core idea of the game.", "Eine weitere Kernidee des Spiels.")),
]


def game(ctx):
    t = ctx.t
    rows = "".join(f'<article class="feature">{ctx.figure(img, alt=t(*name))}<div><h2>{t(*name)}</h2><p>{t(*text)}</p></div></article>'
                   for img, name, text in PILLARS)
    return f'<section class="wrap section">{rows}</section>'


def how_it_plays(ctx):
    t = ctx.t
    return (f'<section class="wrap section"><div class="prose"><p>{t("Describe a session from the player's side: what they do first, what they "
            "learn, and what pulls them back.", "Beschreibe eine Spielsitzung aus Sicht der Spielenden: was sie zuerst tun, was "
            "sie lernen und was sie zurückholt.")}</p></div></section>')


# Both pages belong to the "The Game" section in site.json ("pages"), so each shows the section's tab strip.
PAGES = {
    "game/index.html": dict(title=("The Game", "Das Spiel"), lede=("What it is and how it plays.", "Was es ist und wie es sich spielt."), body=game),
    "game/how-it-plays.html": dict(title=("How It Plays", "So spielt es sich"), lede=("A session, start to finish.", "Eine Spielsitzung von Anfang bis Ende."),
                                   body=how_it_plays),
}
