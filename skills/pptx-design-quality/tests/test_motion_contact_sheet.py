from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts/motion_contact_sheet.py"

_spec = importlib.util.spec_from_file_location("motion_contact_sheet", SCRIPT)
mcs = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(mcs)

needs_ffmpeg = pytest.mark.skipif(
    shutil.which("ffmpeg") is None, reason="ffmpeg not installed"
)


def run_script(*argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *argv],
        check=False,
        capture_output=True,
        text=True,
    )


@pytest.fixture
def moving_video(tmp_path: Path) -> Path:
    """A clip whose content changes over time, standing in for a rendered deck."""
    out = tmp_path / "clip.mp4"
    subprocess.run(
        [
            "ffmpeg", "-v", "error", "-y", "-f", "lavfi",
            "-i", "testsrc=size=320x240:rate=12", "-t", "3",
            "-pix_fmt", "yuv420p", str(out),
        ],
        check=True,
        capture_output=True,
    )
    return out


def test_relative_path_is_resolved_to_absolute(tmp_path: Path, monkeypatch) -> None:
    """A relative path handed to PowerPoint resolves against its own cwd, which
    under WSL is a UNC path — the call then fails with an opaque E_FAIL."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "deck.pptx").write_bytes(b"x")
    monkeypatch.setattr(mcs.shutil, "which", lambda name: None)
    resolved = mcs._to_windows_path(Path("deck.pptx"))
    assert resolved is not None
    assert Path(resolved).is_absolute()


def test_wsl_unc_path_is_rejected(monkeypatch) -> None:
    """PowerPoint cannot open \\\\wsl.localhost paths; the deck must be staged."""
    monkeypatch.setattr(mcs.shutil, "which", lambda name: "/usr/bin/wslpath")
    monkeypatch.setattr(
        mcs,
        "_run",
        lambda argv, timeout: subprocess.CompletedProcess(
            argv, 0, "\\\\wsl.localhost\\Ubuntu\\home\\u\\deck.pptx\n", ""
        ),
    )
    assert mcs._to_windows_path(Path("/home/u/deck.pptx")) is None


def test_preflight_blocked_without_powershell() -> None:
    result = mcs.preflight(None)
    assert result["ok"] is False
    assert "powershell" in result["reason"].lower()


def test_running_instance_is_named_in_the_failure(monkeypatch) -> None:
    """PowerPoint is a single-instance COM server: a degraded running instance
    blocks automation, and the message has to say so or the cause is invisible."""
    payload = json.dumps(
        {
            "running_instances": 1,
            "titles": ["deck.pptx - PowerPoint (Unlicensed Product)"],
            "com_ok": False,
            "version": "",
            "error": "Exception from HRESULT: 0x80048240",
        }
    )
    monkeypatch.setattr(
        mcs,
        "_run",
        lambda argv, timeout: subprocess.CompletedProcess(argv, 0, payload, ""),
    )
    result = mcs.preflight("powershell.exe")
    assert result["ok"] is False
    assert "Close PowerPoint" in result["reason"]
    assert result["running_instances"] == 1


def test_missing_video_reports_cleanly(tmp_path: Path) -> None:
    result = run_script(
        "--from-video", str(tmp_path / "nope.mp4"), "--out-dir", str(tmp_path / "o")
    )
    assert result.returncode == 1
    assert "missing video" in result.stdout


@needs_ffmpeg
def test_contact_sheet_from_video(tmp_path: Path, moving_video: Path) -> None:
    out = tmp_path / "qa"
    result = run_script(
        "--from-video", str(moving_video), "--out-dir", str(out),
        "--sample-fps", "4", "--columns", "4", "--json",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    sheet = report["contact_sheet"]
    assert sheet["ok"] is True
    assert sheet["frames"] > 1
    assert Path(sheet["contact_sheet"]).is_file()
    assert len(list((out / "frames").glob("motion_*.png"))) == sheet["frames"]


@needs_ffmpeg
def test_rerun_clears_stale_frames(tmp_path: Path, moving_video: Path) -> None:
    out = tmp_path / "qa"
    frames = out / "frames"
    frames.mkdir(parents=True)
    stale = frames / "motion_999.png"
    stale.write_bytes(b"stale")
    mcs.build_sheet(moving_video, out, sample_fps=2, columns=3, width=160)
    assert not stale.exists()


@needs_ffmpeg
def test_sheet_grid_covers_every_frame(tmp_path: Path, moving_video: Path) -> None:
    out = tmp_path / "qa"
    sheet = mcs.build_sheet(moving_video, out, sample_fps=3, columns=4, width=160)
    assert sheet["ok"] is True
    columns, rows = (int(n) for n in sheet["grid"].split("x"))
    assert columns * rows >= sheet["frames"]
