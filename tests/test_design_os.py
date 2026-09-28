"""skills/design-os: index incrementally, stop cleanly on quota, search by content, serve only indexed files."""
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'design-os'
SCRIPT = SKILL / 'scripts' / 'design_os.py'


def png(path, rgb, w=16, h=10):
    """A solid-colour PNG from the standard library, so these tests need no Pillow."""
    import struct
    import zlib
    raw = b''.join(b'\x00' + bytes(rgb) * w for _ in range(h))
    chunk = lambda t, d: struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
                     + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))


def run(home, *args, **env):
    e = {**os.environ, 'DESIGN_OS_HOME': str(home), 'DESIGN_OS_FAKE_EMBED': '1', **env}
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, env=e, timeout=120)


@pytest.fixture
def lib(tmp_path):
    d = tmp_path / 'lib'
    d.mkdir()
    img = lambda name, colour: png(d / name, colour)
    img('orange-a.png', (230, 120, 20))
    img('orange-b.png', (231, 121, 21))   # near-identical twin of orange-a
    img('blue.png', (20, 60, 220))
    img('green.png', (30, 170, 60))
    (d / 'landing.html').write_text('<!doctype html><title>Pricing page</title><h1>Three tiers</h1>')
    (d / 'notes.txt').write_text('not indexed')
    return d


def test_frontmatter_and_policy():
    text = (SKILL / 'SKILL.md').read_text()
    assert re.search(r'^name: design-os$', text, re.M) and '## Judgment rules' in text and 'cost-tier' in text


def test_index_is_incremental_and_forgets_deleted_files(lib, tmp_path):
    home = tmp_path / 'home'
    r = run(home, 'index', str(lib))
    assert r.returncode == 0 and '5 items' in r.stdout and '5 embedded this run' in r.stdout, r.stdout + r.stderr
    r = run(home, 'index', str(lib))
    assert '0 new or changed' in r.stdout and '0 embedded this run' in r.stdout      # nothing re-embedded
    (lib / 'green.png').unlink()
    r = run(home, 'index', str(lib))
    assert '4 items' in r.stdout
    items = json.load(open(home / 'index.json'))['items'].values()
    design = next(v for v in items if v['kind'] == 'design')
    assert design['title'] == 'Pricing page' and 'Three tiers' in design['text']


def test_quota_stops_cleanly_and_resumes(lib, tmp_path):
    home = tmp_path / 'home'
    r = run(home, 'index', str(lib), DESIGN_OS_FAKE_FAIL_AFTER='2')
    assert r.returncode == 0 and '2 embedded this run' in r.stdout and '3 pending' in r.stdout, r.stdout
    assert 'RESOURCE_EXHAUSTED' in r.stderr
    r = run(home, 'index', str(lib))                                                   # quota back: finishes
    assert '3 embedded this run' in r.stdout and '5/5 searchable' in r.stdout


def test_limit_caps_new_embeddings(lib, tmp_path):
    r = run(tmp_path / 'home', 'index', str(lib), '--limit', '1')
    assert '1 embedded this run' in r.stdout and '4 pending' in r.stdout


def test_no_key_still_indexes_names(lib, tmp_path):
    home = tmp_path / 'home'
    r = run(home, 'index', str(lib), '--no-embed')
    assert '0 embedded this run' in r.stdout and '0/5 searchable' in r.stdout
    items = json.load(open(home / 'index.json'))['items'].values()
    assert sum(1 for v in items if v['thumb']) == 4 and '0 pending' not in r.stdout      # images get a thumb, html none


def _serve(home, port):
    e = {**os.environ, 'DESIGN_OS_HOME': str(home), 'DESIGN_OS_FAKE_EMBED': '1'}
    p = subprocess.Popen([sys.executable, str(SCRIPT), 'serve', '--port', str(port)], env=e,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        try:
            urllib.request.urlopen(f'http://127.0.0.1:{port}/api/items')
            return p
        except OSError:
            time.sleep(0.1)
    p.terminate()
    raise RuntimeError('server did not start')


def test_more_like_this_and_file_serving(lib, tmp_path):
    home = tmp_path / 'home'
    run(home, 'index', str(lib))
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
    p = _serve(home, port)
    try:
        base = f'http://127.0.0.1:{port}'
        items = json.loads(urllib.request.urlopen(base + '/api/items').read())['items']
        a = next(i for i in items if i['name'] == 'orange-a.png')
        like = json.loads(urllib.request.urlopen(f"{base}/api/items?like={a['id']}").read())['items']
        assert like[0]['name'] == 'orange-b.png', [i['name'] for i in like]             # the twin ranks first
        assert all(i['id'] != a['id'] for i in like)
        imgs = json.loads(urllib.request.urlopen(base + '/api/items?kind=image').read())['items']
        assert {i['kind'] for i in imgs} == {'image'}
        assert urllib.request.urlopen(f"{base}/file/{a['id']}").read()[:4] == b'\x89PNG'
        for bad in ('/file/0000000000000000', '/file/../index.json', '/thumb/zz'):
            with pytest.raises(urllib.error.HTTPError) as e:
                urllib.request.urlopen(base + bad)
            assert e.value.code == 404
    finally:
        p.terminate()
        p.wait(5)


def test_serve_blocks_on_empty_index(tmp_path):
    r = run(tmp_path / 'empty', 'serve', '--port', '1')
    assert r.returncode == 1 and 'BLOCKED' in r.stderr
