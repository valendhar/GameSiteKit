"""Build the site, then serve it at http://127.0.0.1:<dev_port> (site.json) for a local check.

    python _builder/dev.py
"""
import functools
import http.server
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
port = json.loads((ROOT / "site.json").read_text(encoding="utf-8")).get("dev_port", 8766)
subprocess.run([sys.executable, str(ROOT / "_builder" / "build.py")], check=True)
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
print(f"Serving http://127.0.0.1:{port}/  (Ctrl+C to stop)")
http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()
