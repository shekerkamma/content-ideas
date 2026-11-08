"""scripts/detox: patches for Ben AI's /detox skill, which this public repo does not carry.

The original is a free download with no licence, so only our patches, a hash manifest and a
self-test are committed. The patched skill is built per machine into vendor/detox/ (gitignored)
and linked into ~/.claude/skills by dual-host. These tests keep that split honest: no copy of
the original may be tracked, the manifest must pin both ends, and the builder must refuse a zip
it was not made for or one that writes outside detox/.

The full behaviour check runs only where the original is available: set DETOX_ZIP to Ben AI's
detox.zip, or build vendor/detox first.
"""
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'scripts' / 'detox'
MANIFEST = json.loads((HERE / 'manifest.json').read_text(encoding='utf-8'))
APPLY = HERE / 'apply_patches.py'


def _apply(*args):
    return subprocess.run([sys.executable, '-I', str(APPLY), *map(str, args)],
                          capture_output=True, text=True, timeout=120)


def test_manifest_pins_the_original_and_every_patched_file():
    assert len(MANIFEST['original_zip_sha256']) == 64
    files = MANIFEST['patched_files_sha256']
    assert {'SKILL.md', 'PATCHES.md', 'scripts/gather_local.py', 'scripts/build_page.py'} <= set(files)
    assert all(len(h) == 64 for h in files.values())


def test_no_copy_of_the_original_is_tracked():
    tracked = subprocess.run(['git', 'ls-files'], cwd=ROOT, capture_output=True, text=True, check=True)
    bad = [p for p in tracked.stdout.splitlines()
           if p.startswith('vendor/') or p.endswith(('detox/assets/page.html', 'detox/assets/logo.svg'))
           or p.startswith('skills/detox/')]
    assert bad == []


def test_vendor_is_gitignored():
    r = subprocess.run(['git', 'check-ignore', '-q', 'vendor/detox/SKILL.md'], cwd=ROOT)
    assert r.returncode == 0, 'vendor/ must be in .gitignore'


def test_patches_md_is_the_one_the_manifest_expects():
    import hashlib
    got = hashlib.sha256((HERE / 'PATCHES.md').read_bytes()).hexdigest()
    assert got == MANIFEST['patched_files_sha256']['PATCHES.md']


def test_refuses_a_zip_it_was_not_made_for(tmp_path):
    z = tmp_path / 'detox.zip'
    with zipfile.ZipFile(z, 'w') as f:
        f.writestr('detox/SKILL.md', '---\nname: detox\n---\n')
    r = _apply('--zip', z, '--out', tmp_path / 'out')
    assert r.returncode == 1 and 'is not the detox.zip' in r.stderr
    assert not (tmp_path / 'out').exists()


def test_refuses_entries_outside_detox(tmp_path, monkeypatch):
    sys.path.insert(0, str(HERE))
    try:
        import apply_patches as ap
    finally:
        sys.path.pop(0)
    z = tmp_path / 'evil.zip'
    with zipfile.ZipFile(z, 'w') as f:
        f.writestr('detox/SKILL.md', 'x')
        f.writestr('../escape.txt', 'x')
    fake = dict(MANIFEST, original_zip_sha256=ap.sha256(z))
    with pytest.raises(ap.PatchError, match='unexpected zip entry'):
        ap.build(z, fake)
    assert not (tmp_path.parent / 'escape.txt').exists()


def test_missing_zip_is_a_usage_error(tmp_path, monkeypatch):
    r = subprocess.run([sys.executable, '-I', str(APPLY), '--zip', str(tmp_path / 'nope.zip')],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 2


@pytest.mark.skipif(not os.environ.get('DETOX_ZIP') and not (ROOT / 'vendor/detox/SKILL.md').is_file(),
                    reason='needs Ben AI detox.zip (DETOX_ZIP) or a built vendor/detox')
def test_built_skill_matches_manifest_and_passes_selftest(tmp_path):
    if os.environ.get('DETOX_ZIP'):
        r = _apply('--zip', os.environ['DETOX_ZIP'], '--out', tmp_path / 'detox')
        assert r.returncode == 0, r.stderr
        skill = tmp_path / 'detox'
    else:
        skill = ROOT / 'vendor/detox'
        sys.path.insert(0, str(HERE))
        try:
            import apply_patches as ap
        finally:
            sys.path.pop(0)
        have = {p.relative_to(skill).as_posix(): ap.sha256(p) for p in skill.rglob('*')
                if p.is_file() and '__pycache__' not in p.parts}
        assert have == MANIFEST['patched_files_sha256']
    r = subprocess.run([sys.executable, '-I', str(HERE / 'selftest.py'), str(skill)],
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-2000:]
