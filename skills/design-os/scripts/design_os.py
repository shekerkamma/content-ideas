#!/usr/bin/env python3
"""Design OS: index your finished designs, generated images and videos, and search them by what is in them.

usage:
  python3 design_os.py index <folder> [<folder> ...] [--limit 200] [--no-embed] [--screenshots]
  python3 design_os.py serve [--port 8793]
  python3 design_os.py search "<words>" [--top 10]

Index: images (png jpg jpeg webp gif), videos (mp4 webm mov, poster frame via ffmpeg) and HTML designs
(title + visible text; `--screenshots` adds a rendered thumbnail through Playwright). Every item is embedded
once with Gemini Embedding 2 (text and images share one 3072-d space, so words find pictures), cached by
content hash; `--limit` caps new embeds per run and a quota error stops cleanly with the rest reported as
pending. Serve: a local gallery with semantic search, "more like this", filters, and a copy-path button.

State lives in $DESIGN_OS_HOME (default ~/.local/share/design-os, %LOCALAPPDATA%\\design-os on Windows).
Stdlib only; Pillow is used for thumbnails when installed. Binds 127.0.0.1 and serves only indexed files.
"""
import argparse
import array
import hashlib
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

HERE = os.path.dirname(os.path.realpath(__file__))
IMAGES = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
VIDEOS = {'.mp4', '.webm', '.mov', '.m4v'}
DESIGNS = {'.html', '.htm'}
SKIP_DIRS = {'node_modules', '.git', '__pycache__', '.venv', 'dist-ssr', '.next', '.cache'}
DIM = 3072


def home() -> str:
    base = os.environ.get('DESIGN_OS_HOME')
    if not base:
        base = os.path.join(os.environ['LOCALAPPDATA'], 'design-os') if os.name == 'nt' and os.environ.get('LOCALAPPDATA') \
            else os.path.join(os.path.expanduser('~'), '.local', 'share', 'design-os')
    os.makedirs(os.path.join(base, 'thumbs'), exist_ok=True)
    return base


# ---------------------------------------------------------------- embedding (real or deterministic fake)

def _fake_vec(seed: bytes) -> list[float]:
    """Deterministic stand-in for tests: similar bytes give similar vectors only by accident, so tests that
    need real similarity use images whose colour histogram is encoded in the seed (see _image_seed)."""
    out, h = [], seed
    while len(out) < DIM:
        h = hashlib.sha256(h).digest()
        out.extend((b - 127.5) / 127.5 for b in h)
    return out[:DIM]


def _image_seed(path: str) -> bytes | None:
    try:
        from PIL import Image
        im = Image.open(path).convert('RGB').resize((8, 8))
        return bytes(v // 64 for px in im.getdata() for v in px)  # coarse colour layout: near-identical images match
    except Exception:
        return None


_CALLS = [0]


def embed(text: str | None = None, image: str | None = None) -> list[float]:
    _CALLS[0] += 1
    fail_after = os.environ.get('DESIGN_OS_FAKE_FAIL_AFTER')  # test hook: simulate the free tier running out
    if fail_after and _CALLS[0] > int(fail_after):
        raise RuntimeError('HTTP 429 RESOURCE_EXHAUSTED (simulated)')
    if os.environ.get('DESIGN_OS_FAKE_EMBED'):
        if image:
            # coarse colour layout when Pillow exists; otherwise the filename's first word, so test twins
            # ("orange-a", "orange-b") still share a vector family. The fake proves plumbing, not vision.
            seed = _image_seed(image) or os.path.basename(image).split('-')[0].split('.')[0].encode()
            return _fake_vec(b'img' + seed)
        return _fake_vec(b'txt' + (text or '').lower().encode())
    sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'scripts'))  # content-ideas/scripts/gemini_embed.py
    try:
        import gemini_embed
    except ImportError:
        raise RuntimeError('gemini_embed.py not found (set PYTHONPATH to the content-ideas scripts/ folder)')
    return gemini_embed.embed(text=text, image_path=image)


def cosine(a, b) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


# ---------------------------------------------------------------- store: index.json + vectors.bin

class Store:
    def __init__(self, base: str):
        self.base = base
        self.index_path = os.path.join(base, 'index.json')
        self.vec_path = os.path.join(base, 'vectors.bin')
        self.items: dict[str, dict] = {}
        self.vectors: dict[str, array.array] = {}  # content sha -> vector
        if os.path.isfile(self.index_path):
            data = json.load(open(self.index_path, encoding='utf-8'))
            self.items = data.get('items', {})
            order = data.get('vector_order', [])
            if order and os.path.isfile(self.vec_path):
                buf = array.array('f')
                with open(self.vec_path, 'rb') as f:
                    buf.fromfile(f, len(order) * DIM)
                for i, sha in enumerate(order):
                    self.vectors[sha] = buf[i * DIM:(i + 1) * DIM]

    def save(self) -> None:
        order = list(self.vectors)
        buf = array.array('f')
        for sha in order:
            buf.extend(self.vectors[sha])
        tmp = self.vec_path + '.tmp'
        with open(tmp, 'wb') as f:
            buf.tofile(f)
        os.replace(tmp, self.vec_path)
        tmp = self.index_path + '.tmp'
        json.dump({'items': self.items, 'vector_order': order, 'saved': time.strftime('%Y-%m-%dT%H:%M:%S')},
                  open(tmp, 'w', encoding='utf-8'))
        os.replace(tmp, self.index_path)


def sha_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def thumb_for(path: str, kind: str, sha: str, base: str, screenshots: bool) -> str | None:
    out = os.path.join(base, 'thumbs', sha[:24] + '.jpg')
    if os.path.isfile(out):
        return out
    src = path
    if kind == 'video':
        if not shutil.which('ffmpeg'):
            return None
        r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', '1', '-i', path, '-frames:v', '1',
                            '-vf', 'scale=640:-2', out], capture_output=True)
        if r.returncode or not os.path.isfile(out):
            subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', path, '-frames:v', '1', '-vf', 'scale=640:-2', out],
                           capture_output=True)
        return out if os.path.isfile(out) else None
    if kind == 'design':
        if not screenshots or not shutil.which('node'):
            return None
        js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage("
              "{viewport:{width:1280,height:800}});await p.goto(process.argv[1],{waitUntil:'load',timeout:20000}).catch(()=>{});"
              "await p.screenshot({path:process.argv[2],type:'jpeg',quality:70});await b.close()})()")
        subprocess.run(['node', '-e', js, 'file://' + os.path.abspath(path), out], capture_output=True, timeout=60)
        return out if os.path.isfile(out) else None
    try:
        from PIL import Image
        im = Image.open(src)
        im.seek(0)
        im = im.convert('RGB')
        im.thumbnail((640, 640))
        im.save(out, 'JPEG', quality=80)
        return out
    except Exception:
        return src if os.path.getsize(src) < 4_000_000 else None  # no Pillow: small originals serve as their own thumb


def html_text(path: str) -> tuple[str, str]:
    raw = open(path, encoding='utf-8', errors='replace').read()
    title = re.search(r'<title[^>]*>(.*?)</title>', raw, re.S | re.I)
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', raw, flags=re.S | re.I)
    text = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', body))).strip()
    return (html.unescape(title.group(1).strip()) if title else os.path.basename(path)), text[:2000]


def cmd_index(a) -> int:
    base = home()
    st = Store(base)
    seen, added, embedded, pending, errors = set(), 0, 0, 0, []
    stop_embedding = a.no_embed
    for folder in a.folders:
        folder = os.path.realpath(folder)
        if not os.path.isdir(folder):
            print(f'BLOCKED: {folder} is not a folder', file=sys.stderr)
            return 1
        for dirpath, dirnames, files in os.walk(folder):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]
            for name in sorted(files):
                ext = os.path.splitext(name)[1].lower()
                kind = 'image' if ext in IMAGES else 'video' if ext in VIDEOS else 'design' if ext in DESIGNS else None
                if not kind:
                    continue
                path = os.path.join(dirpath, name)
                key = hashlib.sha1(path.encode()).hexdigest()[:16]
                seen.add(key)
                stat = os.stat(path)
                item = st.items.get(key)
                if not item or item['mtime'] != stat.st_mtime or item['size'] != stat.st_size:
                    sha = sha_file(path)
                    item = {'id': key, 'path': path, 'name': name, 'kind': kind, 'folder': folder,
                            'size': stat.st_size, 'mtime': stat.st_mtime, 'sha': sha,
                            'thumb': thumb_for(path, kind, sha, base, a.screenshots)}
                    if kind == 'design':
                        item['title'], item['text'] = html_text(path)
                    st.items[key] = item
                    added += 1
                if item['sha'] in st.vectors:
                    continue
                if stop_embedding or (a.limit is not None and embedded >= a.limit):
                    pending += 1
                    continue
                try:
                    if kind == 'design' and not item.get('thumb'):
                        vec = embed(text=f"{item.get('title', '')}. {item.get('text', '')}")
                    else:
                        if not item.get('thumb'):
                            pending += 1
                            continue
                        vec = embed(image=item['thumb'])
                    st.vectors[item['sha']] = array.array('f', vec)
                    embedded += 1
                except Exception as e:  # quota, network or key: keep what we have, report the rest
                    msg = str(e)[:200]
                    errors.append(f'{name}: {msg}')
                    pending += 1
                    if re.search(r'429|quota|RESOURCE_EXHAUSTED|API key|not found in environment', msg, re.I):
                        stop_embedding = True
    # forget files that vanished from the indexed folders
    roots = {os.path.realpath(f) for f in a.folders}
    for key in [k for k, v in st.items.items() if v['folder'] in roots and k not in seen]:
        del st.items[key]
    st.save()
    total = len(st.items)
    ready = sum(1 for v in st.items.values() if v['sha'] in st.vectors)
    print(f'design-os: {total} items ({added} new or changed), {embedded} embedded this run, '
          f'{ready}/{total} searchable, {pending} pending -> {st.index_path}')
    if errors:
        print('embedding stopped or failed on: ' + '; '.join(errors[:3]), file=sys.stderr)
    return 0


def search(st: Store, q: str = '', like: str | None = None, kind: str = '', top: int = 60) -> list[dict]:
    items = [v for v in st.items.values() if not kind or v['kind'] == kind]
    if like:
        ref = st.items.get(like)
        qv = st.vectors.get(ref['sha']) if ref else None
        if qv is None:
            return []
    elif q:
        words = q.lower().split()
        text_hits = {v['id'] for v in items if all(w in (v['path'] + ' ' + v.get('title', '')).lower() for w in words)}
        try:
            qv = embed(text=q)
        except Exception:
            qv = None  # no key or offline: fall back to names only
        if qv is None:
            return [dict(v, score=1.0) for v in items if v['id'] in text_hits][:top]
    else:
        return sorted(items, key=lambda v: -v['mtime'])[:top]
    scored = []
    for v in items:
        vec = st.vectors.get(v['sha'])
        s = cosine(qv, vec) if vec is not None else -1.0
        if not like and q and v['id'] in text_hits:
            s += 0.15  # a name match is strong evidence too
        if like and v['id'] == like:
            continue
        scored.append(dict(v, score=round(s, 4)))
    scored.sort(key=lambda v: -v['score'])
    return [v for v in scored if v['score'] > -1][:top]


def public(v: dict) -> dict:
    return {k: v.get(k) for k in ('id', 'name', 'path', 'kind', 'folder', 'size', 'mtime', 'title', 'score')} | \
        {'thumb': bool(v.get('thumb'))}


def cmd_serve(a) -> int:
    st = Store(home())
    if not st.items:
        print('BLOCKED: the index is empty; run `design_os.py index <folder>` first', file=sys.stderr)
        return 1
    page = open(os.path.join(HERE, 'gallery.html'), encoding='utf-8').read()
    types = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.gif': 'image/gif',
             '.mp4': 'video/mp4', '.webm': 'video/webm', '.mov': 'video/quicktime', '.m4v': 'video/mp4',
             '.html': 'text/html; charset=utf-8', '.htm': 'text/html; charset=utf-8'}

    class H(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send(self, code, body, ctype):
            self.send_response(code)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            u = urlparse(self.path)
            qs = {k: v[0] for k, v in parse_qs(u.query).items()}
            if u.path == '/':
                return self.send(200, page.encode(), 'text/html; charset=utf-8')
            if u.path == '/api/items':
                res = search(st, qs.get('q', ''), qs.get('like'), qs.get('kind', ''), int(qs.get('top', 120)))
                ready = sum(1 for v in st.items.values() if v['sha'] in st.vectors)
                return self.send(200, json.dumps({'items': [public(v) for v in res], 'total': len(st.items),
                                                  'searchable': ready}).encode(), 'application/json')
            m = re.fullmatch(r'/(thumb|file)/([0-9a-f]{16})', u.path)
            if m and m.group(2) in st.items:  # only indexed ids, never a path from the request
                v = st.items[m.group(2)]
                p = v['thumb'] if m.group(1) == 'thumb' else v['path']
                if p and os.path.isfile(p):
                    return self.send(200, open(p, 'rb').read(), types.get(os.path.splitext(p)[1].lower(), 'application/octet-stream'))
            self.send(404, b'not found', 'text/plain')

    print(f'design-os: {len(st.items)} items -> http://127.0.0.1:{a.port}/  (Ctrl+C to stop)', flush=True)
    ThreadingHTTPServer(('127.0.0.1', a.port), H).serve_forever()
    return 0


def cmd_search(a) -> int:
    st = Store(home())
    for v in search(st, a.query, top=a.top):
        print(f"{v.get('score', 0):.3f}  {v['kind']:6}  {v['path']}")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description='Index and search your designs, images and videos by content.')
    sub = ap.add_subparsers(dest='cmd', required=True)
    i = sub.add_parser('index')
    i.add_argument('folders', nargs='+')
    i.add_argument('--limit', type=int, default=200, help='max new embeddings this run (free-tier friendly)')
    i.add_argument('--no-embed', action='store_true', help='index and thumbnail only; names stay searchable')
    i.add_argument('--screenshots', action='store_true', help='render HTML designs to thumbnails via Playwright')
    s = sub.add_parser('serve')
    s.add_argument('--port', type=int, default=8793)
    q = sub.add_parser('search')
    q.add_argument('query')
    q.add_argument('--top', type=int, default=10)
    a = ap.parse_args()
    sys.exit({'index': cmd_index, 'serve': cmd_serve, 'search': cmd_search}[a.cmd](a))


if __name__ == '__main__':
    main()
