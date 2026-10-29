"""skills/tip-card-film: the builder must refuse bad specs and emit a composition HyperFrames accepts."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'tip-card-film'
BUILD = SKILL / 'scripts' / 'build_tip_film.py'
needs_ffmpeg = pytest.mark.skipif(not (shutil.which('ffmpeg') and shutil.which('ffprobe')), reason='ffmpeg not installed')


@pytest.fixture
def project(tmp_path):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc2=size=640x360:rate=30',
                    '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000', '-t', '8', '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', str(tmp_path / 'talk.mp4')], check=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=0x3355ff:s=320x200',
                    '-frames:v', '1', str(tmp_path / 'shot.png')], check=True)
    spec = {'camera': 'talk.mp4', 'width': 640, 'height': 360, 'cards': [
        {'start': 1.0, 'end': 3.5, 'title': 'Grab a font', 'subtitle': 'one that fits', 'image': 'shot.png'},
        {'start': 4.5, 'end': 7.0, 'title': 'Ask for SVG', 'prompt': 'Make the icons SVG.'}]}
    (tmp_path / 'spec.json').write_text(json.dumps(spec))
    return tmp_path


def build(d, spec=None):
    if spec is not None:
        (d / 'spec.json').write_text(json.dumps(spec))
    return subprocess.run([sys.executable, str(BUILD), str(d / 'spec.json'), str(d / 'out')], capture_output=True, text=True)


def test_frontmatter_and_policy():
    text = (SKILL / 'SKILL.md').read_text()
    assert re.search(r'^name: tip-card-film$', text, re.M) and '## Judgment rules' in text and 'cost-tier' in text


@needs_ffmpeg
def test_builds_a_composition_that_follows_the_contract(project):
    r = build(project)
    assert r.returncode == 0, r.stderr
    doc = (project / 'out' / 'index.html').read_text()
    assert 'data-composition-id="tipfilm"' in doc and 'window.__timelines["tipfilm"] = tl' in doc
    assert doc.count('gsap.timeline(') == 1
    assert re.search(r'<video id="cam"[^>]*\bmuted\b', doc) and '<audio id="cam-audio"' in doc     # sound lives on <audio>
    assert 'crossorigin' not in doc
    assert not re.search(r'id="camwrap"[^>]*data-start', doc)                                    # the animated wrapper is untimed
    assert re.search(r'data-duration="8(\.0+)?"', doc)
    assert (project / 'out' / 'assets' / 'talk.mp4').is_file() and (project / 'out' / 'assets' / 'shot.png').is_file()
    assert doc.count('class="clip card"') == 2 and 'Make the icons SVG.' in doc
    assert 'tl.fromTo("#camfx"' not in doc and 'tl.set("#camfx"' in doc                            # one baseline, no fromTo race


@needs_ffmpeg
@pytest.mark.parametrize('cards,needle', [
    ([{'start': 1, 'end': 3, 'title': 'a'}, {'start': 2.5, 'end': 5, 'title': 'b'}], 'overlapping'),
    ([{'start': 1, 'end': 1.8, 'title': 'a'}], 'too short'),
    ([{'start': 6, 'end': 9, 'title': 'a'}], 'after the camera video'),
    ([{'start': 1, 'end': 3, 'title': 'a', 'image': 'nope.png'}], 'not found'),
    ([{'start': 1, 'end': 3}], 'title is required'),
])
def test_bad_specs_are_blocked(project, cards, needle):
    r = build(project, {'camera': 'talk.mp4', 'cards': cards})
    assert r.returncode == 1 and 'BLOCKED' in r.stderr and needle in r.stderr, r.stderr


@needs_ffmpeg
def test_named_font_without_a_file_is_blocked(project):
    r = build(project, {'camera': 'talk.mp4', 'tokens': {'font_display': 'Newsreader, serif'},
                        'cards': [{'start': 1, 'end': 3, 'title': 'a'}]})
    assert r.returncode == 1 and '"Newsreader" needs a local file' in r.stderr


@needs_ffmpeg
def test_hyperframes_check_passes(project):
    hf = shutil.which('hyperframes') or next(iter(sorted(Path.home().glob('.nvm/versions/node/v2*/bin/hyperframes'))), None)
    if not hf:
        pytest.skip('hyperframes CLI not installed')
    assert build(project).returncode == 0
    r = subprocess.run([str(hf), 'check'], cwd=project / 'out', capture_output=True, text=True, timeout=600,
                       env={**__import__('os').environ, 'PATH': str(Path(hf).parent) + ':' + __import__('os').environ['PATH']})
    out = r.stdout + r.stderr
    assert r.returncode == 0, out[-2000:]
    assert re.search(r'0 error\(s\)', out) and not re.search(r'across 0 sample', out), out[-2000:]   # audits actually ran
