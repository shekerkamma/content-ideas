"""skills/tweak: the bake must change exactly the declaration the page used, and nothing it should not."""
import json
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'tweak'
sys.path.insert(0, str(SKILL / 'scripts'))
import tweak  # noqa: E402


@pytest.fixture
def demo(tmp_path):
    d = tmp_path / 'site'
    shutil.copytree(SKILL / 'assets' / 'demo', d)
    return d


def test_frontmatter_and_policy():
    text = (SKILL / 'SKILL.md').read_text()
    assert re.search(r'^name: tweak$', text, re.M) and '## Judgment rules' in text and 'cost-tier' in text


def test_parser_skips_at_rule_overrides_and_comments(demo):
    css = (demo / 'styles.css').read_text()
    toks = tweak.read_tokens([str(demo / 'styles.css')])
    assert toks['--bg']['value'] == '#f7f5f0' and toks['--bg']['count'] == 1   # the dark override is not a candidate
    assert toks['--font-text']['value'] == 'Inter, system-ui, sans-serif'      # commas stay inside one value
    assert '/* a stack' in css


def test_bake_edits_only_the_winning_declaration(demo):
    f = str(demo / 'styles.css')
    before = open(f).read()
    r = tweak.bake([f], {'--space': '32px', '--bg': '#ffffff', '--nope': '1px', '--radius': '6px'}, [])
    after = open(f).read()
    assert {c['name'] for c in r['changed']} == {'--space', '--bg'}                 # --radius unchanged: no edit
    assert [s['name'] for s in r['skipped']] == ['--nope']
    assert '--space: 32px;' in after and '--bg: #ffffff;' in after
    assert '--bg: #111313' in after                                              # dark block untouched
    assert len(r['backups']) == 1 and open(r['backups'][0]).read() == before
    diff = [(a, b) for a, b in zip(before.splitlines(), after.splitlines()) if a != b]
    assert len(diff) == 2, diff                                                  # nothing else moved


def test_bake_refuses_values_that_break_the_rule(demo):
    f = str(demo / 'styles.css')
    r = tweak.bake([f], {'--space': '1px; } body { display:none'}, [])
    assert not r['changed'] and r['skipped'] and 'display:none' not in open(f).read()


def test_hidden_sections_are_a_reversible_block(demo):
    f = str(demo / 'styles.css')
    tweak.bake([f], {}, ['#faq'])
    assert '#faq { display: none !important; }' in open(f).read()
    tweak.bake([f], {}, [])                                                      # un-hide removes the block
    s = open(f).read()
    assert tweak.HIDDEN_START not in s and '#faq' not in s


def _serve(demo, port):
    p = subprocess.Popen([sys.executable, str(SKILL / 'scripts' / 'tweak.py'), str(demo), '--bake-into',
                          str(demo / 'styles.css'), '--port', str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for _ in range(50):
        try:
            urllib.request.urlopen(f'http://127.0.0.1:{port}/__tweak/tokens')
            return p
        except OSError:
            time.sleep(0.1)
    p.terminate()
    raise RuntimeError(p.stderr.read().decode())


def _port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def test_server_injects_panel_and_requires_the_token(demo):
    port = _port()
    p = _serve(demo, port)
    try:
        html = urllib.request.urlopen(f'http://127.0.0.1:{port}/').read().decode()
        m = re.search(r'data-token="([^"]+)"', html)
        assert '/__tweak/panel.js' in html and m
        req = lambda tok: urllib.request.Request(f'http://127.0.0.1:{port}/__tweak/bake', method='POST',
                                                 data=json.dumps({'values': {'--space': '40px'}}).encode(),
                                                 headers={'Content-Type': 'application/json', **({'X-Tweak-Token': tok} if tok else {})})
        with pytest.raises(urllib.error.HTTPError) as e:
            urllib.request.urlopen(req(None))
        assert e.value.code == 403 and '--space: 24px' in (demo / 'styles.css').read_text()
        assert json.loads(urllib.request.urlopen(req(m.group(1))).read())['changed'][0]['to'] == '40px'
        assert '--space: 40px' in (demo / 'styles.css').read_text()
    finally:
        p.terminate()
        p.wait(5)


def test_server_blocks_when_no_tokens(tmp_path):
    (tmp_path / 'a.css').write_text('body { color: red; }')
    r = subprocess.run([sys.executable, str(SKILL / 'scripts' / 'tweak.py'), str(tmp_path), '--bake-into',
                        str(tmp_path / 'a.css')], capture_output=True, text=True, timeout=30)
    assert r.returncode == 1 and 'BLOCKED' in r.stderr


def test_browser_slider_then_bake(demo):
    """End to end in Chromium: the panel lists the tokens, a slider restyles the page live, Bake writes it."""
    if not shutil.which('node') or subprocess.run(['node', '-e', "require('playwright')"], cwd=ROOT).returncode:
        pytest.skip('node + playwright not available')
    port = _port()
    p = _serve(demo, port)
    js = f"""
    const {{chromium}} = require('playwright');
    (async () => {{
      const b = await chromium.launch(); const pg = await b.newPage();
      await pg.goto('http://127.0.0.1:{port}/', {{waitUntil: 'networkidle'}});
      await pg.waitForFunction(() => document.getElementById('tweak-panel-host')?.shadowRoot?.querySelector('.row'));
      const res = await pg.evaluate(async () => {{
        const sh = document.getElementById('tweak-panel-host').shadowRoot;
        const rows = [...sh.querySelectorAll('.row')];
        const row = rows.find((r) => r.querySelector('label').textContent.startsWith('--space'));
        const range = row.querySelector('input[type=range]');
        range.value = 36; range.dispatchEvent(new Event('input'));
        const live = getComputedStyle(document.querySelector('section')).paddingTop;
        const faq = [...sh.querySelectorAll('.sec input')].find((i) => i.nextElementSibling.textContent === '#faq');
        faq.checked = false; faq.dispatchEvent(new Event('change'));
        sh.querySelector('.bake').click();
        await new Promise((r) => setTimeout(r, 800));
        return {{ rows: rows.length, live, out: sh.querySelector('.out').textContent }};
      }});
      console.log(JSON.stringify(res)); await b.close();
    }})();"""
    try:
        r = subprocess.run(['node', '-e', js], cwd=ROOT, capture_output=True, text=True, timeout=120)
        res = json.loads(r.stdout.strip().splitlines()[-1])
        assert res['rows'] == 8 and res['live'] == '36px', res
        assert '--space: 24px → 36px' in res['out'], res
        css = (demo / 'styles.css').read_text()
        assert '--space: 36px;' in css and '#faq { display: none !important; }' in css
    finally:
        p.terminate()
        p.wait(5)
