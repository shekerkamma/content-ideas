"""Static and behavioural guards for scroll-story-gate."""
import ast
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "scroll-story-gate"
GATE = SKILL / "scripts" / "check_story.py"
FIX = SKILL / "fixtures"


def run(fixture):
    r = subprocess.run([sys.executable, str(GATE), str(FIX / fixture)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def test_script_parses():
    ast.parse(GATE.read_text(), filename=str(GATE))


def test_clean_plan_passes():
    code, out, _ = run("clean.json")
    assert code == 0, out
    assert "UNVERIFIED" in out, "a clean plan must still disclaim pacing"


def test_broken_plan_is_caught():
    code, _, err = run("broken.json")
    assert code == 2
    for expect in ("duplicate id", "never read", "credibility claim",
                   "no copy and no copy_waived", "that seam is a cut",
                   "points at its own clip"):
        assert expect in err, f"gate missed: {expect}"


def test_duration_coupling_fires_alone():
    """The source insight: vh must not be inherited from clip length."""
    code, _, err = run("coupled.json")
    assert code == 2
    assert "inherited from footage length" in err
    assert err.count(" - ") == 1, "coupled fixture must isolate exactly one defect"


def test_missing_file_blocks_rather_than_passes():
    r = subprocess.run([sys.executable, str(GATE), str(FIX / "nope.json")],
                       capture_output=True, text=True)
    assert r.returncode == 1, "a missing plan must block (1), never read as clean (0)"


def test_exit_codes_are_distinct():
    src = GATE.read_text()
    assert "return 0" in src and "return 2" in src and "sys.exit(1)" in src


def test_thresholds_are_named_policy():
    src = GATE.read_text()
    for k in ("MIN_COPY_VH", "MIN_BEAT_VH", "MAX_BEAT_VH", "DURATION_COUPLING"):
        assert k in src, f"threshold {k} must be a named constant, not inline"


def test_gate_names_no_vendor():
    """Provider independence is the whole point of this gate."""
    blob = (GATE.read_text() + (SKILL / "SKILL.md").read_text()
            + (SKILL / "references" / "plan-format.md").read_text()).lower()
    for vendor in ("higgsfield", "kie.ai", "runway", "veo", "sora", "api_key"):
        assert vendor not in blob, f"gate must stay provider-agnostic, found {vendor!r}"


def test_stdout_flushed_before_findings():
    src = GATE.read_text()
    assert "sys.stdout.flush()" in src, "findings must not print before the summary"
