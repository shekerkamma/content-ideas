#!/usr/bin/env python3
"""Serve a page with a token slider panel, then bake the chosen values back into its source CSS.

usage: python3 tweak.py <site-root> --bake-into <file.css> [<file.css> ...] [--config tweak.json] [--port 8791]
                        [--page index.html]

  <site-root>    directory served as-is (a static site or a build's output folder)
  --bake-into    the SOURCE stylesheet(s) that declare the tokens (`:root { --x: ... }`); for a built site
                 these are the source files, not the hashed bundle. Only these files are ever written.
  --config       optional tweak.json: the few controls to show, with labels, ranges, colour swatches and
                 section names (see SKILL.md). Without it every :root token is listed by raw name.
Open the printed URL, adjust, press Bake. Every bake first writes <file>.bak-tweak-<timestamp>.

Stdlib only. Binds 127.0.0.1, and a bake needs the per-run token injected into the served page, so no
other site open in the browser can post to it.
"""
import argparse
import json
import os
import re
import secrets
import shutil
import sys
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.realpath(__file__))
HIDDEN_START = '/* tweak: hidden sections (baked) */'
HIDDEN_END = '/* tweak: end hidden sections */'


def root_blocks(css: str) -> list[tuple[int, int]]:
    """(start, end) of the body of every top-level `:root { ... }` rule, skipping comments and anything
    nested in an at-rule (a dark-mode or media override is a different value on purpose)."""
    out, i, n, depth, at_depth, sel_start = [], 0, len(css), 0, [], 0
    while i < n:
        if css.startswith('/*', i):
            j = css.find('*/', i + 2)
            i = n if j < 0 else j + 2
            continue
        c = css[i]
        if c in '"\'':
            j = i + 1
            while j < n and css[j] != c:
                j += 2 if css[j] == '\\' else 1
            i = j + 1
            continue
        if c == '{':
            selector = re.sub(r'/\*.*?\*/', '', css[sel_start:i], flags=re.S).strip()
            if selector.startswith('@'):
                at_depth.append(depth)
            elif depth == 0 and selector == ':root':
                out.append((i + 1, None))
            depth += 1
            sel_start = i + 1
        elif c == '}':
            depth -= 1
            if at_depth and at_depth[-1] == depth:
                at_depth.pop()
            if out and out[-1][1] is None and depth == 0:
                out[-1] = (out[-1][0], i)
            sel_start = i + 1
        elif c == ';' and depth == 0:
            sel_start = i + 1
        i += 1
    return [(a, b) for a, b in out if b is not None]


DECL = re.compile(r'(--[\w-]+)\s*:\s*([^;{}]*?)\s*(;|(?=\}))')


def declarations(css: str) -> dict[str, list[tuple[int, int, str]]]:
    """Token name -> [(value_start, value_end, value)] across the file's top-level :root blocks."""
    found: dict[str, list] = {}
    for a, b in root_blocks(css):
        body = css[a:b]
        for m in DECL.finditer(body):
            found.setdefault(m.group(1), []).append((a + m.start(2), a + m.end(2), m.group(2)))
    return found


def read_tokens(files: list[str]) -> dict[str, dict]:
    """The value the cascade would use: the last top-level :root declaration, later files winning."""
    tokens: dict[str, dict] = {}
    for f in files:
        for name, occ in declarations(open(f, encoding='utf-8').read()).items():
            tokens[name] = {'value': occ[-1][2], 'file': f, 'count': len(occ) + tokens.get(name, {}).get('count', 0)}
    return tokens


def bake(files: list[str], values: dict[str, str], hidden: list[str]) -> dict:
    """Write each changed token into the file whose declaration wins; append the hidden-sections block."""
    stamp = time.strftime('%Y%m%d-%H%M%S')
    report = {'changed': [], 'skipped': [], 'backups': [], 'hidden': []}
    winners = read_tokens(files)
    edits: dict[str, list] = {}
    for name, value in values.items():
        value = str(value).strip()
        if not re.fullmatch(r'--[\w-]+', name) or any(ch in value for ch in ';{}') or not value:
            report['skipped'].append({'name': name, 'reason': 'not a token, or the value would break the rule'})
            continue
        w = winners.get(name)
        if not w:
            report['skipped'].append({'name': name, 'reason': 'not declared in a top-level :root of the bake files'})
            continue
        if w['value'] == value:
            continue
        edits.setdefault(w['file'], []).append((name, value, w['value']))
    hidden = [h for h in hidden if re.fullmatch(r'[#.\w\-\s>:()\[\]="\']+', h or '')]
    targets = set(edits) | ({files[0]} if hidden is not None and (hidden or HIDDEN_START in open(files[0]).read()) else set())
    for f in sorted(targets):
        css = open(f, encoding='utf-8').read()
        backup = f'{f}.bak-tweak-{stamp}'
        shutil.copy2(f, backup)
        report['backups'].append(backup)
        for name, value, old in edits.get(f, []):
            start, end, _ = declarations(css)[name][-1]  # re-read offsets after each edit
            css = css[:start] + value + css[end:]
            report['changed'].append({'name': name, 'from': old, 'to': value, 'file': f})
        if f == files[0]:
            css = re.sub(re.escape(HIDDEN_START) + r'.*?' + re.escape(HIDDEN_END) + r'\n?', '', css, flags=re.S)
            if hidden:
                css = css.rstrip('\n') + '\n\n' + HIDDEN_START + '\n' + ''.join(f'{h} {{ display: none !important; }}\n' for h in hidden) + HIDDEN_END + '\n'
                report['hidden'] = hidden
        open(f, 'w', encoding='utf-8').write(css)
    return report


def load_config(path: str, tokens: dict) -> dict:
    """Validate tweak.json against the tokens actually declared; a typo must fail loudly, not vanish."""
    cfg = json.load(open(path, encoding='utf-8'))
    problems = []
    for i, c in enumerate(cfg.get('controls', [])):
        if c.get('token') not in tokens:
            problems.append(f"controls[{i}]: {c.get('token')!r} is not declared in a top-level :root")
        for sw in c.get('swatches', []):
            val = sw.get('value') if isinstance(sw, dict) else sw
            if isinstance(val, str) and val.startswith('--') and val not in tokens:
                problems.append(f"controls[{i}] swatch {val!r} is not a declared token")
    for sel in cfg.get('sections', {}):
        if not re.fullmatch(r'[#.\w\-\s>:()\[\]="\']+', sel):
            problems.append(f'sections: {sel!r} is not a plain selector')
    if problems:
        sys.exit('BLOCKED: ' + path + ':\n  ' + '\n  '.join(problems))
    # resolve token-reference swatches to their values once, server-side
    for c in cfg.get('controls', []):
        out = []
        for sw in c.get('swatches', []):
            label, val = (sw.get('label'), sw.get('value')) if isinstance(sw, dict) else (None, sw)
            out.append({'label': label or (val if not val.startswith('--') else val[2:]),
                        'value': tokens[val]['value'] if val.startswith('--') else val})
        if out:
            c['swatches'] = out
    return cfg


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('root')
    ap.add_argument('--bake-into', nargs='+', required=True)
    ap.add_argument('--port', type=int, default=8791)
    ap.add_argument('--page', default='')
    ap.add_argument('--config')
    a = ap.parse_args()
    root = os.path.realpath(a.root)
    files = [os.path.realpath(f) for f in a.bake_into]
    missing = [f for f in files if not os.path.isfile(f)]
    if not os.path.isdir(root) or missing:
        sys.exit(f'BLOCKED: {root if not os.path.isdir(root) else missing} not found')
    if not read_tokens(files):
        sys.exit('BLOCKED: no `--token: value` declarations in a top-level :root of ' + ', '.join(files))
    config = load_config(a.config, read_tokens(files)) if a.config else None
    token = secrets.token_urlsafe(16)
    panel = open(os.path.join(HERE, 'panel.js'), encoding='utf-8').read()

    class Handler(SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _json(self, code, obj):
            body = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = self.path.split('?')[0]
            if path == '/__tweak/panel.js':
                body = panel.encode()
                self.send_response(200)
                self.send_header('Content-Type', 'text/javascript')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            if path == '/__tweak/tokens':
                self._json(200, read_tokens(files))
                return
            if path == '/__tweak/config':
                self._json(200, config or {})
                return
            fs = self.translate_path(path)
            if os.path.isdir(fs):
                fs = os.path.join(fs, 'index.html')
            elif not os.path.exists(fs) and os.path.isfile(fs + '.html'):
                fs += '.html'
            if fs.endswith('.html') and os.path.isfile(fs) and os.path.realpath(fs).startswith(root + os.sep):
                html = open(fs, encoding='utf-8', errors='replace').read()
                tag = f'<script src="/__tweak/panel.js" data-token="{token}"></script>'
                html = html.replace('</body>', tag + '</body>') if '</body>' in html else html + tag
                body = html.encode()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Cache-Control', 'no-store')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            super().do_GET()

        def do_POST(self):
            if self.path.split('?')[0] != '/__tweak/bake':
                self._json(404, {'error': 'not found'})
                return
            if self.headers.get('X-Tweak-Token') != token:
                self._json(403, {'error': 'missing or wrong token'})
                return
            try:
                req = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))) or b'{}')
                self._json(200, bake(files, req.get('values', {}), req.get('hidden', [])))
            except (ValueError, OSError) as e:
                self._json(400, {'error': str(e)})

    url = f'http://127.0.0.1:{a.port}/{a.page}'
    print(f'tweak: {len(read_tokens(files))} tokens from {", ".join(os.path.relpath(f) for f in files)}')
    print(f'open {url}  (Ctrl+C to stop)', flush=True)
    ThreadingHTTPServer(('127.0.0.1', a.port), partial(Handler, directory=root)).serve_forever()


if __name__ == '__main__':
    main()
