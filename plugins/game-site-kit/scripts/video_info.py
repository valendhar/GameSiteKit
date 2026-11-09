"""Title, length, aspect ratio and ID of a Loom, YouTube or Vimeo video, from the provider's public oEmbed endpoint.

    python video_info.py <share link>

Prints JSON: provider, id, title, minutes (rounded to a half), ratio ("16 / 9" style), width, height.
"""
import json
import math
import re
import sys
import urllib.parse
import urllib.request

ENDPOINTS = {
    "loom": ("https://www.loom.com/v1/oembed?url={u}", r"loom\.com/(?:share|embed)/([0-9a-f]{32})"),
    "youtube": ("https://www.youtube.com/oembed?format=json&url={u}", r"(?:youtu\.be/|v=|/shorts/|/embed/)([\w-]{11})"),
    "vimeo": ("https://vimeo.com/api/oembed.json?url={u}", r"vimeo\.com/(?:video/)?(\d+)"),
}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    url = sys.argv[1]
    provider = next((p for p in ENDPOINTS if p in url or (p == "youtube" and "youtu.be" in url)), None)
    if not provider:
        sys.exit("not a Loom, YouTube or Vimeo link")
    endpoint, pattern = ENDPOINTS[provider]
    m = re.search(pattern, url)
    req = urllib.request.Request(endpoint.format(u=urllib.parse.quote(url, safe="")), headers={"User-Agent": "game-site-kit"})
    data = json.load(urllib.request.urlopen(req, timeout=20))
    w, h = int(data.get("width") or 16), int(data.get("height") or 9)
    g = math.gcd(w, h)
    ratio = f"{w // g} / {h // g}"
    if (w // g) > 50:  # odd sizes: fall back to the nearest common ratio
        ratio = min(("16 / 9", 16 / 9), ("4 / 3", 4 / 3), ("21 / 9", 21 / 9), key=lambda r: abs(r[1] - w / h))[0]
    dur = data.get("duration")
    minutes = round(dur / 30) / 2 if dur else None
    print(json.dumps(dict(provider=provider, id=m[1] if m else None, title=data.get("title"), minutes=minutes, ratio=ratio,
                          width=w, height=h), ensure_ascii=False, indent=1))


main()
