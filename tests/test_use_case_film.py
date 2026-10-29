"""Static guards for the use-case-film skill.

Each assertion pins a property whose absence has previously produced a green
run over a broken artifact. They are static so they run without ffmpeg,
Kokoro, or a browser.
"""
import ast
import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "use-case-film"
SCRIPTS = SKILL / "scripts"


def _src(name):
    return (SCRIPTS / name).read_text()


def test_skill_exists_with_closed_frontmatter():
    text = (SKILL / "SKILL.md").read_text()
    assert text.startswith("---\n")
    assert "\n---\n" in text[4:], "frontmatter block is not closed"
    assert "\nname: use-case-film\n" in text


def test_every_script_parses():
    for p in sorted(SCRIPTS.glob("*.py")):
        ast.parse(p.read_text(), filename=str(p))


def test_volumedetect_is_not_silenced():
    """`-v error` suppresses ffmpeg's volumedetect/silencedetect output, so a
    check that passes it measures nothing and reports clean."""
    src = _src("verify_films.py")
    fn = src.split("def mean_volume(")[1].split("\ndef ")[0]
    assert '"-v", "error"' not in fn, "mean_volume must not suppress ffmpeg output"
    assert "volumedetect" in fn


def test_silence_threshold_is_derived_not_hardcoded():
    """The floor comes from a generated silent file, not a guessed dB number."""
    src = _src("verify_films.py")
    assert "def silence_floor" in src
    assert "anullsrc" in src, "must generate a silence control to compare against"
    assert "floor +" in src, "audio level must be compared against the measured floor"


def test_gate_exit_codes_are_distinct():
    """0 clean, 1 blocked, 2 findings — blocked must never look like clean."""
    src = _src("verify_films.py")
    assert "return 1" in src and "return 2" in src and "return 0" in src
    for marker in ("BLOCKED: ffprobe not found", "BLOCKED: no films found"):
        assert marker in src


def test_duration_is_checked_against_the_manifest():
    src = _src("verify_films.py")
    assert "drift" in src and "manifest" in src


def test_truncated_model_is_refused():
    """A partially downloaded ONNX fails opaquely deep in the runtime."""
    src = _src("tts_beats.py")
    assert "MODEL_BYTES" in src
    assert "expected" in src and "BLOCKED" in src


def test_measure_is_the_only_place_durations_are_decided():
    """build_film must read the manifest, never compute a duration from words."""
    src = _src("build_film.py")
    assert "manifest" in src
    assert 'e["start"]' in src and 'e["dur"]' in src
    assert "len(vo.split())" not in src, "durations must not be estimated from text"


def test_missing_audio_blocks_rather_than_defaults():
    src = _src("measure_beats.py")
    assert "BLOCKED" in src and "have no audio" in src


def test_skill_states_its_judgment_rules():
    text = (SKILL / "SKILL.md").read_text()
    assert "## Judgment rules" in text
    assert "## Verification discipline" in text
    for rule in ("REQUIRES VERIFICATION", "Runtime is an output", "pgrep -f"):
        assert rule in text, f"missing judgment rule: {rule}"
