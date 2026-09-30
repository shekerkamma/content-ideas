"""Contract tests for skills/e2e-qa-review: the skill's gates must fail closed, and the Pages server must
resolve paths the way GitHub Pages does (the local mismatch cost 79 false nav failures on dr-silicon-v3)."""
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
SKILL = ROOT / 'skills' / 'e2e-qa-review'
SCRIPTS = SKILL / 'scripts'


def test_frontmatter_name_and_policy_sections():
    text = (SKILL / 'SKILL.md').read_text()
    assert re.search(r'^name: e2e-qa-review$', text, re.M)
    assert re.search(r'^description: .{40,}', text, re.M)
    assert '## Judgment rules' in text
    assert 'cost-tier' in text
    for ref in ('false-greens.md', 'report-template.md', 'design-bans.md', 'cross-family.md', 'config.md'):
        assert (SKILL / 'references' / ref).is_file(), ref
        assert ref in text, f'{ref} is orphaned: SKILL.md never points at it'


def test_every_script_named_in_skill_exists():
    text = (SKILL / 'SKILL.md').read_text()
    names = set(re.findall(r'\$SKILL_DIR/scripts/([\w.]+\.(?:py|mjs))', text))
    assert len(names) == 6, names  # an empty population passes every check
    for name in names:
        assert (SCRIPTS / name).is_file(), name


@pytest.mark.parametrize('name', ['sweep.mjs', 'nav_gate.mjs'])
def test_node_scripts_parse(name):
    if not shutil.which('node'):
        pytest.skip('node not installed')
    subprocess.run(['node', '--check', str(SCRIPTS / name)], check=True)


@pytest.mark.parametrize('name', ['sweep.mjs', 'nav_gate.mjs'])
def test_gates_never_exit_clean_before_measuring(name):
    """A gate that skips must not look like a gate that passed: no exit(0) before the browser opens,
    and a missing dependency is exit 1 (BLOCKED), never 0."""
    src = (SCRIPTS / name).read_text()
    before_launch = src.split('chromium.launch(')[0]
    assert 'process.exit(0)' not in before_launch
    assert "console.error('BLOCKED: '" in src and 'process.exit(1)' in src
    assert re.search(r'process\.exit\(\w+.*\? 2 : 0\)', src), 'findings must exit 2'


def test_gates_block_without_config(tmp_path):
    if not shutil.which('node'):
        pytest.skip('node not installed')
    for name in ('sweep.mjs', 'nav_gate.mjs'):
        r = subprocess.run(['node', str(SCRIPTS / name), str(tmp_path / 'missing.json')],
                           cwd=tmp_path, capture_output=True, text=True)
        assert r.returncode == 1 and 'BLOCKED' in r.stderr, (name, r.returncode, r.stderr)


@pytest.mark.parametrize('name', ['serve_pages.py', 'summarize.py', 'contact_sheet.py', 'lanes.py'])
def test_python_scripts_compile(name):
    import py_compile
    py_compile.compile(str(SCRIPTS / name), doraise=True)


def _get(url):
    try:
        with urllib.request.urlopen(url) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def test_serve_pages_resolves_like_github_pages(tmp_path):
    dist = tmp_path / 'dist'
    (dist / 'about').mkdir(parents=True)
    (dist / 'index.html').write_text('HOME')
    (dist / '404.html').write_text('NOTFOUND')
    (dist / 'about.html').write_text('ABOUT')          # /about -> about.html, never the about/ listing
    (dist / 'about' / 'team.html').write_text('TEAM')
    (dist / 'bare').mkdir()                             # a directory with no index.html and no bare.html
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
    proc = subprocess.Popen([sys.executable, str(SCRIPTS / 'serve_pages.py'), str(dist), 'site', str(port)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        base = f'http://127.0.0.1:{port}/site/'
        for _ in range(50):
            try:
                urllib.request.urlopen(base)
                break
            except OSError:
                time.sleep(0.1)
        assert _get(base) == (200, 'HOME')
        assert _get(base + 'about') == (200, 'ABOUT')
        assert _get(base + 'about/team') == (200, 'TEAM')
        assert _get(base + 'bare') == (404, 'NOTFOUND')
        assert _get(base + 'bare/') == (404, 'NOTFOUND')
        assert _get(base + 'no-such-page') == (404, 'NOTFOUND')
        root = f'http://127.0.0.1:{port}/'
        assert _get(root)[0] == 404 and _get(root + 'about')[0] == 404       # outside the base path
        (tmp_path / 'secret.html').write_text('SECRET')
        assert _get(base + '../secret')[1] != 'SECRET'                        # no escape from dist
        assert _get(base + '%2e%2e/secret')[1] != 'SECRET'
    finally:
        proc.terminate()
        proc.wait(5)


def test_summarize_groups_findings_and_flags_suspects(tmp_path):
    row = {'width': 'desktop', 'route': 'x', 'status': 200, 'statusOk': True, 'errs': [], 'failed': [], 'h1': 1,
           'skips': [], 'overflowX': 0, 'broken': [], 'noBox': [], 'noBoxN': 0, 'small': 0, 'smallSample': [],
           'unrevealed': 0, 'title': 't',
           'axe': [{'id': 'target-size', 'impact': 'serious', 'n': 1, 'sample': ['a | partially obscured']}],
           'design': {'emDash': 1, 'emDashAt': ['a — b'], 'counters': 0, 'italicHeads': [], 'monoLabels': 0,
                      'pills': 0, 'eyebrowsPerH2': 0}}
    f = tmp_path / 'r.json'
    import json
    f.write_text(json.dumps({'base': 'b', 'loads': 1, 'dupTitles': [], 'rows': [row]}))
    out = subprocess.run([sys.executable, str(SCRIPTS / 'summarize.py'), str(f)], capture_output=True, text=True,
                         check=True).stdout
    assert '## axe target-size (serious) (1)' in out and 'test WCAG 2.4.11 directly' in out
    assert '## Design: em dashes (1)' in out
    row['deadLinks'] = ['404 /demonstrations']
    row['design'].update(straightQuotes=2, straightQuotesAt=["don't"])
    f.write_text(json.dumps({'base': 'b', 'loads': 1, 'dupTitles': [], 'rows': [row]}))
    out = subprocess.run([sys.executable, str(SCRIPTS / 'summarize.py'), str(f)], capture_output=True, text=True,
                         check=True).stdout
    assert '## Dead links in page content (1)' in out and '## Design: straight quotes (1)' in out


FIXTURE = SKILL / 'assets' / 'fixtures' / 'broken'


@pytest.fixture
def broken_site(tmp_path):
    """Serve the negative-control fixture; skip (not pass) where a browser is unavailable."""
    if not shutil.which('node'):
        pytest.skip('node not installed')
    probe = subprocess.run(['node', '-e', "require('playwright').chromium.executablePath()"], cwd=ROOT,
                           capture_output=True)
    if probe.returncode:
        pytest.skip('playwright not installed in the repo')
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
    proc = subprocess.Popen([sys.executable, str(SCRIPTS / 'serve_pages.py'), str(FIXTURE), 'fx', str(port)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    base = f'http://127.0.0.1:{port}/fx/'
    for _ in range(50):
        try:
            urllib.request.urlopen(base)
            break
        except OSError:
            time.sleep(0.1)
    yield base
    proc.terminate()
    proc.wait(5)


def test_sweep_fires_on_every_planted_defect_and_not_on_the_clean_page(broken_site, tmp_path):
    import json
    cfg = tmp_path / 'sweep.json'
    cfg.write_text(json.dumps({'base': broken_site, 'routes': ['', 'a', 'no-such-page'], 'widths': [[1280, 800, 'desktop']],
                               'out': str(tmp_path / 'r.json'), 'shots': str(tmp_path / 'shots'), 'webgl': False}))
    r = subprocess.run(['node', str(SCRIPTS / 'sweep.mjs'), str(cfg)], cwd=ROOT, capture_output=True, text=True,
                       timeout=300)
    if r.returncode == 1 and 'BLOCKED' in r.stderr:
        pytest.skip(r.stderr.strip())
    assert r.returncode == 2, r.stdout + r.stderr
    rows = {x['route']: x for x in json.loads((tmp_path / 'r.json').read_text())['rows']}
    bad = rows['/']
    assert bad['errs'] and bad['failed'] and bad['skips'] and bad['overflowX'] > 0 and bad['broken'] and bad['small']
    assert 'button-name' in {v['id'] for v in bad['axe']} and bad['design']['emDash']
    assert bad['lordiconNoCredit'] and bad['design']['rasterIcons']
    # in-page link crawl: the never-built route fires, and page a's own links (./ and a#top) do not
    assert any(h.endswith('/demonstrations') for h in bad['deadLinks']), bad['deadLinks']
    assert bad['design']['straightQuotes'] >= 2
    assert rows['a']['deadLinks'] == [] and rows['a']['linksN'] >= 2 and not rows['a']['design']['straightQuotes']
    for clean in ('a', 'no-such-page'):   # the 404 route's own 404 is the right answer, not an error
        x = rows[clean]
        assert x['statusOk'] and not (x['errs'] or x['failed'] or x['skips'] or x['axe']), (clean, x)
    # controls: a credited Lordicon and an SVG icon on page a must not be flagged
    assert not rows['a']['lordiconNoCredit'] and not rows['a']['design']['rasterIcons']
    # minTarget: the 32px control passes the WCAG 24px floor and fails the HIG 44px floor
    cfg.write_text(json.dumps({**json.loads(cfg.read_text()), 'routes': [''], 'minTarget': 44,
                               'out': str(tmp_path / 'r44.json')}))
    subprocess.run(['node', str(SCRIPTS / 'sweep.mjs'), str(cfg)], cwd=ROOT, capture_output=True, timeout=300)
    at44 = json.loads((tmp_path / 'r44.json').read_text())['rows'][0]
    assert at44['small'] > bad['small'], (bad['small'], at44['small'])


def test_nav_gate_fires_on_every_planted_defect(broken_site, tmp_path):
    import json
    cfg = tmp_path / 'nav.json'
    cfg.write_text(json.dumps({'base': broken_site, 'start': '', 'typed': ['a']}))
    r = subprocess.run(['node', str(SCRIPTS / 'nav_gate.mjs'), str(cfg)], cwd=ROOT, capture_output=True, text=True,
                       timeout=300)
    assert r.returncode == 2, r.stdout + r.stderr
    for planted in ('panel closed before the pointer reached', 'Tab from the open button', 'Escape left it open',
                    'not open after a click', 'phone: no', 'typed /A'):
        assert planted in r.stdout, planted
    assert 'top link' not in r.stdout, 'the top link works; a finding there is the gate misreading a relative href'


def _lanes(tmp_path, cfg):
    import json
    p = tmp_path / 'lanes.json'
    cfg = {'out': str(tmp_path / 'lanes-results.json'), **cfg}
    p.write_text(json.dumps(cfg))
    r = subprocess.run([sys.executable, str(SCRIPTS / 'lanes.py'), str(p)], capture_output=True, text=True, timeout=900)
    out = json.loads((tmp_path / 'lanes-results.json').read_text()) if (tmp_path / 'lanes-results.json').exists() else None
    return r, out


def test_lanes_block_without_config(tmp_path):
    r = subprocess.run([sys.executable, str(SCRIPTS / 'lanes.py'), str(tmp_path / 'none.json')], capture_output=True, text=True)
    assert r.returncode == 1 and 'BLOCKED' in r.stderr


def test_guidelines_lane_scanning_nothing_is_blocked_not_clean(tmp_path):
    if not shutil.which('node'):
        pytest.skip('node not installed')
    (tmp_path / 'empty').mkdir()
    r, out = _lanes(tmp_path, {'src': str(tmp_path / 'empty'), 'lanes': ['guidelines']})
    assert r.returncode == 1 and out['guidelines']['status'] == 'blocked' and 'empty population' in out['guidelines']['reason']


def test_guidelines_lane_finds_the_fixture_img_and_scrollcraft_says_why_it_did_not_run(tmp_path):
    if not shutil.which('node'):
        pytest.skip('node not installed')
    r, out = _lanes(tmp_path, {'src': str(FIXTURE), 'dist': str(FIXTURE), 'lanes': ['guidelines', 'scrollcraft']})
    assert r.returncode == 2, r.stdout + r.stderr
    g = out['guidelines']
    assert g['status'] == 'ran' and any(f['rule'] == 'Images' and f['file'].endswith('index.html') for f in g['findings'])
    s = out['scrollcraft']
    assert s['status'] == 'not-applicable' and 'data-sc-act' in s['reason']   # recorded, never silently dropped


def test_scrollcraft_lane_becomes_applicable_on_an_engine_page(tmp_path):
    """Negative control for the applicability test: the same lane must NOT say not-applicable once the page
    uses the engine (it then runs, or is BLOCKED if the skill or Chrome is missing, never quietly skipped)."""
    site = tmp_path / 'site'
    site.mkdir()
    (site / 'index.html').write_text('<!doctype html><section data-sc-act="hero"></section>')
    _, out = _lanes(tmp_path, {'dist': str(site), 'base': 'http://127.0.0.1:9/', 'lanes': ['scrollcraft'],
                               'skillDirs': {'scroll-craft': str(tmp_path / 'nope')}})
    assert out['scrollcraft']['status'] in ('ran', 'blocked')


def test_parse_shoot_reads_sectioned_output():
    sys.path.insert(0, str(SCRIPTS))
    try:
        import lanes
    finally:
        sys.path.pop(0)
    sample = ('page: 7.0 viewport-heights, acts: a > b\n\nDEAD SCROLL between: 03, 04\n\n'
              'FROZEN CLIP (still image while the page moves):\n  hero 00-02 t=0.00\n\n'
              'CONTRAST FAIL (worst frame < 3:1):\n  2.1 "Build it"\n  2.8 "Ship it"\n\ncontrast over media: ok\n')
    rules = [f['rule'] for f in lanes.parse_shoot(sample, 'desktop')]
    assert rules == ['DEAD SCROLL', 'FROZEN CLIP', 'CONTRAST FAIL', 'CONTRAST FAIL']
    assert lanes.parse_shoot('all 3 scrub clip(s) keep moving whenever they are on screen\n', 'd') == []


def test_impeccable_lane_gates_warnings_and_routes_advisory(tmp_path):
    sys.path.insert(0, str(SCRIPTS))
    try:
        import lanes
    finally:
        sys.path.pop(0)
    if not lanes.node_at_least(24):
        pytest.skip('Node >= 24 not available')
    r, out = _lanes(tmp_path, {'src': str(FIXTURE), 'lanes': ['impeccable']})
    imp = out['impeccable']
    if imp['status'] == 'blocked' and 'exited' in imp['reason']:
        pytest.skip('impeccable not fetchable here: ' + imp['reason'])
    assert imp['status'] == 'ran' and r.returncode == 2
    assert 'skipped-heading' in {f['rule'] for f in imp['findings']}
    assert all(f['severity'] != 'advisory' for f in imp['findings']) and 'improve-ui' in imp['advisory']['route']


# --- cross-host contract: the compound skill must work from a fresh clone on any host -----------------------

PORTED = ['e2e-qa-review', 'web-design-guidelines', 'improve-ui', 'impeccable', 'hig', 'tweak', 'design-os', 'tip-card-film']


@pytest.mark.parametrize('name', PORTED)
def test_lane_skill_is_flat_and_mirrored_for_every_host(name):
    """Claude and Codex read skills/, DeepSeek Harness and OpenHands read .agents/skills/ (single level only)."""
    import filecmp
    for tree in ('skills', '.agents/skills'):
        skill = ROOT / tree / name / 'SKILL.md'
        assert skill.is_file(), f'{tree}/{name} missing: that host cannot see this lane'
        head = skill.read_text().split('\n---\n', 1)[0]
        assert re.search(rf'^name: {name}$', head, re.M) and re.search(r'^description: \S', head, re.M)
    if name != 'impeccable':  # impeccable's harness copies differ by design (cross-tree-variants.json)
        cmp = filecmp.dircmp(ROOT / 'skills' / name, ROOT / '.agents/skills' / name, ignore=['__pycache__'])
        stack = [cmp]
        while stack:
            c = stack.pop()
            assert not (c.left_only or c.right_only or c.diff_files), (name, c.left_only, c.right_only, c.diff_files)
            stack += c.subdirs.values()


@pytest.mark.parametrize('name', ['web-design-guidelines', 'improve-ui'])
def test_vendored_lane_skills_carry_their_license(name):
    d = ROOT / 'skills' / name
    assert (d / 'PROVENANCE.md').is_file() and any(p.name.startswith('LICENSE') for p in d.iterdir())


def test_lanes_resolve_peer_skills_from_the_repo_alone(tmp_path):
    """A fresh machine has no ~/.claude/skills: the lane skills must resolve from this repo's own tree."""
    code = ('import sys; sys.path.insert(0, sys.argv[1]); import lanes; '
            'print(lanes.find_skill("web-design-guidelines", {})); print(lanes.find_skill("improve-ui", {}))')
    env = {**__import__('os').environ, 'HOME': str(tmp_path), 'USERPROFILE': str(tmp_path)}
    r = subprocess.run([sys.executable, '-c', code, str(SCRIPTS)], cwd=tmp_path, env=env, capture_output=True, text=True)
    got = r.stdout.split()
    assert len(got) == 2 and all(str(ROOT) in g for g in got), r.stdout + r.stderr


def test_scripts_avoid_posix_only_calls():
    """Windows hosts: no symlinks, no hard-coded python3 or bare npx inside the scripts themselves."""
    for p in SCRIPTS.glob('*.py'):
        src = p.read_text()
        assert 'os.symlink' not in src, p.name
        assert "'npx'" not in src or 'npx.cmd' in src, p.name
