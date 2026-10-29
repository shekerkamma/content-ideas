"""Offline gates for the reference-mode verification harness.

These never render anything — rendering costs subscription quota and needs the
network. What is checkable offline is that the harness cannot silently measure
nothing: that its fixtures and reference assets exist, and that the palette
metric actually discriminates rather than returning a number for any input.
"""
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / "scripts"))


def _solid(path, rgb, size=(120, 120)):
    Image = pytest.importorskip("PIL.Image", reason="Pillow not installed")
    Image.new("RGB", size, rgb).save(path)
    return str(path)


@pytest.fixture
def metric():
    pytest.importorskip("PIL", reason="Pillow not installed")
    import palette_distance
    return palette_distance


def test_identical_palettes_score_zero(metric, tmp_path):
    a = _solid(tmp_path / "a.png", (7, 28, 72))
    assert metric.distance(metric.palette(a), metric.palette(a)) == pytest.approx(0, abs=0.5)


def test_metric_discriminates_opposites(metric, tmp_path):
    """The negative control: a metric that cannot separate navy from cream is
    not measuring colour, and would pass a style test that transferred nothing."""
    navy = _solid(tmp_path / "navy.png", (7, 28, 72))
    cream = _solid(tmp_path / "cream.png", (241, 234, 228))
    ref = metric.palette(navy)
    near = metric.distance(metric.palette(navy), ref)
    far = metric.distance(metric.palette(cream), ref)
    assert far > near + 50, f"metric failed to separate opposites: {near} vs {far}"


def test_style_arm_is_comparative_not_thresholded():
    """Guards the design decision: no absolute pass mark may creep in, because a
    style render legitimately shifts the histogram when the subject changes."""
    src = (SKILL / "scripts" / "verify_reference_modes.py").read_text()
    assert "must be LOWER" in src
    for banned in ("THRESHOLD", "< 5.0", "<= 5.0", "MAX_DISTANCE"):
        assert banned not in src, f"absolute threshold crept in: {banned}"


@pytest.mark.parametrize("mode", ["edit", "style", "variation"])
def test_every_mode_has_its_reference_and_spec(mode):
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "vrm", SKILL / "scripts" / "verify_reference_modes.py")
    vrm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vrm)
    ref_name, spec_name = vrm.ARMS[mode]
    assert (SKILL / "assets" / ref_name).is_file(), f"missing reference {ref_name}"
    assert (SKILL / "tests" / "fixtures" / spec_name).is_file(), f"missing spec {spec_name}"


def test_specs_do_not_leak_what_only_the_reference_knows():
    """The discriminator. If a spec enumerates the model captions, the control can
    reproduce them from the prompt alone and a pass proves nothing."""
    leaks = ("Gemini 3.5 Flash", "GPT-5.6", "Fable 5", "Labor Layer", "hot path")
    for name in ("spec-edit.txt", "spec-variation.txt"):
        text = (SKILL / "tests" / "fixtures" / name).read_text()
        for leak in leaks:
            assert leak not in text, f"{name} leaks reference-only string: {leak!r}"


def test_harness_runs_and_refuses_a_bad_mode():
    proc = subprocess.run(
        [sys.executable, str(SKILL / "scripts" / "verify_reference_modes.py"),
         "--mode", "nonsense", "--out-dir", "/tmp/x"],
        capture_output=True, text=True)
    assert proc.returncode != 0 and "invalid choice" in proc.stderr
