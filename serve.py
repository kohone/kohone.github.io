"""Локальный просмотр как на GitHub Pages: /nardy/verify → nardy/verify.html.  python3 serve.py [порт]"""
import http.server, os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = super().translate_path(path)
        if not os.path.exists(p) and os.path.exists(p + ".html"):
            return p + ".html"
        return p


http.server.ThreadingHTTPServer(("", int(sys.argv[1]) if len(sys.argv) > 1 else 8765), Handler).serve_forever()
