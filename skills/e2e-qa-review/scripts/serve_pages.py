#!/usr/bin/env python3
"""Serve a static build the way GitHub Pages does, under a base path, for the QA gates.

usage: python3 serve_pages.py <dist-dir> <base-slug> <port>
  e.g. python3 serve_pages.py dist/pages my-site 8768   ->  http://127.0.0.1:8768/my-site/

What Pages does and `python3 -m http.server` does not:
  - /x resolves to x.html before x/ (a directory with no index.html is never listed);
  - a missing path returns the site's own 404.html with status 404;
  - it serves many connections at once (a single-threaded server stalls a page's parallel chunk requests,
    so `networkidle` never fires and a fine page fails the gate).
Stdlib only.
"""
import os
import sys
import tempfile
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


def main() -> None:
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    dist, slug, port = os.path.abspath(sys.argv[1]), sys.argv[2].strip('/'), int(sys.argv[3])
    if not os.path.isfile(os.path.join(dist, 'index.html')):
        sys.exit(f'BLOCKED: {dist}/index.html not found; build first')
    root = tempfile.mkdtemp(prefix='qa-srv-')
    os.symlink(dist, os.path.join(root, slug))

    class Handler(SimpleHTTPRequestHandler):
        def send_head(self):
            clean = self.path.split('?')[0].split('#')[0]
            path = self.translate_path(clean)
            if not os.path.exists(path) and os.path.isfile(path.rstrip('/') + '.html'):
                self.path = clean.rstrip('/') + '.html'
            elif os.path.isdir(path) and not os.path.isfile(os.path.join(path, 'index.html')):
                if not clean.endswith('/') and os.path.isfile(path.rstrip('/') + '.html'):
                    self.path = clean + '.html'
                else:
                    self.send_error(404)
                    return None
            return super().send_head()

        def send_error(self, code, message=None, explain=None):
            page = os.path.join(dist, '404.html')
            if code == 404 and os.path.isfile(page):
                body = open(page, 'rb').read()
                self.send_response(404)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                if self.command != 'HEAD':
                    self.wfile.write(body)
                return
            super().send_error(code, message, explain)

        def log_message(self, *args):
            pass

    ThreadingHTTPServer.daemon_threads = True
    print(f'serving {dist} at http://127.0.0.1:{port}/{slug}/', flush=True)
    ThreadingHTTPServer(('127.0.0.1', port), partial(Handler, directory=root)).serve_forever()


if __name__ == '__main__':
    main()
