"""skills/roast-room + skills/newroaster: the port from github.com/nateherkai/roast-room.

Every bundled seat must resolve to a seat file and a full brain, no file may still point at the
upstream `.claude/` layout, the quote checker must pass the shipped examples, and the room must
read user state from ROAST_HOME instead of the skill folder (a plugin cache is replaced on upgrade).
"""
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
ROAST = ROOT / 'skills' / 'roast-room'
NEWROASTER = ROOT / 'skills' / 'newroaster'
BRAIN_FILES = ['_hot.md', 'books.md', 'frameworks.md', 'positions.md',
               'principles.md', 'sources.md', 'stories.md', 'voice.md']
ROSTER = json.loads((ROAST / 'roster.json').read_text())


def test_every_seat_has_a_seat_file_and_full_brain():
    keys = [s['key'] for s in ROSTER['seats']]
    assert len(keys) == len(set(keys)) == 13
    for s in ROSTER['seats']:
        assert (ROAST / 'seats' / f"council-{s['key']}.md").is_file(), s['key']
        for f in BRAIN_FILES:
            assert (ROAST / 'brains' / s['slug'] / f).is_file(), f"{s['slug']}/{f}"
    assert set(ROSTER['default']) <= set(keys) and 1 <= len(ROSTER['default']) <= 9
    assert ROSTER['board'] in {'ask', 'auto', 'default'}


def test_no_upstream_layout_paths_remain():
    # $HOME/.claude/skills/ is the linked-skill lookup, not the upstream repo layout. Brains and
    # examples keep upstream provenance (sources.md build paths), which is history, not a path to use.
    pattern = re.compile(r'(?<!\$HOME/)\.claude/(skills|agents)/|projects/founder-council|npm start')
    hits = [str(p.relative_to(ROOT))
            for base in (ROAST, NEWROASTER)
            for p in base.rglob('*')
            if p.is_file() and p.suffix in {'.md', '.mjs', '.py', '.json'}
            and not {'examples', 'brains'} & set(p.parts) and pattern.search(p.read_text(errors='replace'))]
    assert hits == []


def test_seat_files_take_their_brain_from_the_chair():
    for f in (ROAST / 'seats').glob('council-*.md'):
        text = f.read_text()
        assert 'the brain folder the Chair names in your prompt' in text, f.name
    prompts = (ROAST / 'references' / 'round-prompts.md').read_text()
    assert 'Your brain folder is [brain folder]' in prompts and 'Repo root' not in prompts


def test_user_state_goes_to_roast_home():
    skill = (ROAST / 'SKILL.md').read_text()
    assert '$ROAST_HOME/sessions/YYYY-MM-DD-<decision-slug>/' in skill
    assert 'never edit the bundled one' in skill
    builder = (NEWROASTER / 'SKILL.md').read_text()
    assert 'Build folder (`<build>` below): `$ROAST_HOME/build/<slug>/`' in builder
    assert '--out $ROAST_HOME/portraits' in builder


@pytest.mark.parametrize('session', sorted(p.name for p in (ROAST / 'examples').iterdir()))
def test_shipped_examples_pass_the_quote_check(session, tmp_path):
    res = subprocess.run([sys.executable, str(ROAST / 'scripts' / 'check_quotes.py'),
                          str(ROAST / 'examples' / session)],
                         capture_output=True, text=True, env={'ROAST_HOME': str(tmp_path)})
    assert res.returncode == 0, res.stdout


def test_quote_check_verifies_elided_quotes_part_by_part(tmp_path):
    s = tmp_path / 'session'
    s.mkdir()
    good = '"The biggest mistakes... they\'re the mistakes of omission rather than commission" (S028)'
    bad = '"The biggest mistakes... are the mistakes of omission rather than commission" (S028)'
    for text, code in ((good, 0), (bad, 1)):
        (s / 'round-1.md').write_text(f'## Buffett\n\n{text}\n')
        res = subprocess.run([sys.executable, str(ROAST / 'scripts' / 'check_quotes.py'), str(s)],
                             capture_output=True, text=True, env={'ROAST_HOME': str(tmp_path / 'home')})
        assert res.returncode == code, res.stdout


def _free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


@pytest.mark.skipif(shutil.which('node') is None, reason='node not installed')
def test_room_reads_roast_home_before_the_bundle(tmp_path):
    home = tmp_path / 'home'
    (home / 'portraits').mkdir(parents=True)
    roster = dict(ROSTER, default=['buffett'], board='default')
    (home / 'roster.json').write_text(json.dumps(roster))
    (home / 'portraits' / 'buffett-base.webp').write_bytes(b'custom')
    port = _free_port()
    proc = subprocess.Popen(['node', str(ROAST / 'app' / 'server.mjs')],
                            env={'ROAST_HOME': str(home), 'PORT': str(port), 'PATH': '/usr/bin:/bin:/usr/local/bin'},
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    base = f'http://127.0.0.1:{port}'
    try:
        for _ in range(50):
            try:
                seats = json.load(urllib.request.urlopen(base + '/api/seats'))
                break
            except OSError:
                time.sleep(0.1)
        else:
            pytest.fail('room did not start')
        assert len(seats['seats']) == 13 and seats['board']['default'] == ['buffett']
        assert urllib.request.urlopen(base + '/portraits/buffett-base.webp').read() == b'custom'
        sessions = json.load(urllib.request.urlopen(base + '/api/sessions'))['sessions']
        assert len(sessions) == 3   # the bundled examples
        with pytest.raises(urllib.error.HTTPError):
            urllib.request.urlopen(base + '/portraits/..%2f..%2fserver.mjs')
    finally:
        proc.terminate()
        proc.wait(timeout=5)


@pytest.mark.skipif(shutil.which('node') is None, reason='node not installed')
def test_add_seat_writes_roast_home_not_the_bundle(tmp_path):
    before = (ROAST / 'roster.json').read_bytes()
    res = subprocess.run(['node', str(NEWROASTER / 'scripts' / 'add_seat.mjs'), '--key', 'naval',
                          '--name', 'Naval Ravikant', '--short', 'Naval', '--slug', 'naval-ravikant',
                          '--pillar', 'Leverage', '--question', 'Q?', '--dimension', 'D', '--default'],
                         capture_output=True, text=True, env={'ROAST_HOME': str(tmp_path), 'PATH': '/usr/bin:/bin:/usr/local/bin'})
    assert res.returncode == 0, res.stderr
    assert 'naval' in json.loads((tmp_path / 'roster.json').read_text())['default']
    assert (ROAST / 'roster.json').read_bytes() == before


@pytest.mark.skipif(shutil.which('node') is None, reason='node not installed')
def test_portrait_falls_back_to_gemini_without_a_kie_key(tmp_path):
    script = str(NEWROASTER / 'scripts' / 'portrait.mjs')
    base = {'HOME': str(tmp_path), 'PATH': '/usr/bin:/bin:/usr/local/bin'}
    res = subprocess.run(['node', script, 'probe'], capture_output=True, text=True, cwd=tmp_path,
                         env=dict(base, GEMINI_API_KEY='x'))
    assert res.returncode == 0 and 'engine: gemini (gemini-nano-banana-2.1)' in res.stdout
    res = subprocess.run(['node', script, 'probe'], capture_output=True, text=True, cwd=tmp_path, env=base)
    assert res.returncode == 3 and 'GEMINI_API_KEY' in res.stderr
