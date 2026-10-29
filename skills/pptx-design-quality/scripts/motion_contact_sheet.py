#!/usr/bin/env python3
"""Render a deck's motion to video via PowerPoint and build a motion contact sheet.

`lint_pptx.py` and `preview_pptx.py` inspect resting frames, so a transition or a
build is invisible to both. This exports the deck through PowerPoint's own
`Presentation.CreateVideo`, samples the result, and tiles it — turning motion into
something a reviewer can actually look at.

Two environment facts this script exists to handle, both of which fail silently
otherwise:

1. **PowerPoint is a single-instance COM server.** `New-Object -ComObject
   PowerPoint.Application` attaches to an already-running PowerPoint rather than
   starting a clean one. If that instance is degraded — long-running, or showing
   "(Unlicensed Product)" — every automation call returns HRESULT 0x80048240 and
   the deck looks unautomatable when it is not. Preflight detects a running
   instance and says so instead of failing obscurely.
2. **PowerPoint cannot open a WSL path.** `\\\\wsl.localhost\\...` UNC paths fail, so
   a deck living under WSL is staged to a Windows-side temp directory first.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any

# ppMediaTaskStatus
STATUS_NONE, STATUS_IN_PROGRESS, STATUS_QUEUED, STATUS_DONE, STATUS_FAILED = range(5)

_EXPORT_PS1 = r"""
param([string]$In,[string]$Out,[int]$SlideSeconds,[int]$VertRes,[int]$Fps,[int]$TimeoutMin)
$app=$null;$pres=$null
try {
  $app = New-Object -ComObject PowerPoint.Application
  $pres = $app.Presentations.Open($In, [int]-1, [int]0, [int]-1)
  $pres.CreateVideo($Out, $true, $SlideSeconds, $VertRes, $Fps, 85)
  $st = 1
  $deadline = (Get-Date).AddMinutes($TimeoutMin)
  while ($st -eq 1 -or $st -eq 2) {
    Start-Sleep -Milliseconds 800
    $st = $pres.CreateVideoStatus
    if ((Get-Date) -gt $deadline) { break }
  }
  Write-Output ("STATUS=" + $st)
} catch {
  Write-Output ("ERROR=" + $_.Exception.Message)
} finally {
  if ($pres) { try { $pres.Close() } catch {} }
  if ($app)  { try { $app.Quit()  } catch {} }
}
"""

_PREFLIGHT_PS1 = r"""
$running = @(Get-Process POWERPNT -ErrorAction SilentlyContinue)
$titles = @($running | ForEach-Object { $_.MainWindowTitle })
$obj = [ordered]@{
  running_instances = $running.Count
  titles            = $titles
  com_ok            = $false
  version           = ''
  error             = ''
}
try {
  $app = New-Object -ComObject PowerPoint.Application
  $obj.version = $app.Version
  $obj.com_ok = $true
  if ($running.Count -eq 0) { try { $app.Quit() } catch {} }
} catch { $obj.error = $_.Exception.Message }
$obj | ConvertTo-Json -Compress
"""


def _run(argv: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, check=False, capture_output=True, text=True, timeout=timeout
    )


def _powershell() -> str | None:
    return shutil.which("powershell.exe") or shutil.which("pwsh.exe")


def _to_windows_path(path: Path) -> str | None:
    """Absolute Windows form of a path, or None when Windows cannot reach it.

    The path is resolved first on purpose. `wslpath -w` maps a relative path to a
    relative Windows path, which PowerPoint then resolves against its own working
    directory — under WSL that is a `\\\\wsl.localhost\\...` UNC path, and the call
    fails with an opaque E_FAIL instead of a path error.
    """
    path = path.resolve()
    if not shutil.which("wslpath"):
        return str(path)
    result = _run(["wslpath", "-w", str(path)], timeout=30)
    if result.returncode != 0:
        return None
    win = result.stdout.strip()
    return None if win.lower().startswith("\\\\wsl") else win


def _win_temp_dir() -> Path | None:
    """A directory PowerPoint can read, expressed as a WSL path."""
    for candidate in (Path("/mnt/c/Users") , ):
        if not candidate.is_dir():
            continue
        for user in candidate.iterdir():
            target = user / "AppData/Local/Temp"
            if target.is_dir():
                staged = target / f"pptx-motion-{uuid.uuid4().hex[:8]}"
                staged.mkdir(parents=True, exist_ok=True)
                return staged
    return None


def preflight(ps: str | None) -> dict[str, Any]:
    if ps is None:
        return {
            "ok": False,
            "reason": "powershell.exe not found; PowerPoint render QA needs Windows",
        }
    result = _run([ps, "-NoProfile", "-Command", _PREFLIGHT_PS1], timeout=180)
    payload: dict[str, Any] = {}
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                payload = json.loads(line)
                break
            except json.JSONDecodeError:
                continue
    if not payload:
        return {"ok": False, "reason": f"preflight produced no JSON: {result.stdout[:200]}"}

    running = payload.get("running_instances", 0)
    if not payload.get("com_ok"):
        hint = ""
        if running:
            hint = (
                " A PowerPoint instance is already running; COM attaches to it, so a "
                "degraded instance blocks automation. Close PowerPoint and retry."
            )
        return {
            "ok": False,
            "reason": f"PowerPoint COM unavailable: {payload.get('error', 'unknown')}.{hint}",
            "running_instances": running,
            "titles": payload.get("titles", []),
        }
    return {
        "ok": True,
        "version": payload.get("version", ""),
        "running_instances": running,
        "titles": payload.get("titles", []),
    }


def export_video(
    pptx: Path,
    out_video: Path,
    *,
    ps: str,
    slide_seconds: int,
    vert_res: int,
    fps: int,
    timeout_min: int,
) -> dict[str, Any]:
    staged_dir = None
    src_win = _to_windows_path(pptx)
    if src_win is None:
        staged_dir = _win_temp_dir()
        if staged_dir is None:
            return {"ok": False, "reason": "no Windows-visible directory to stage the deck"}
        staged = staged_dir / pptx.name
        shutil.copy2(pptx, staged)
        src_win = _to_windows_path(staged)
        target = staged_dir / (pptx.stem + ".mp4")
    else:
        target = out_video
    dst_win = _to_windows_path(target)
    if src_win is None or dst_win is None:
        return {"ok": False, "reason": "could not express paths in Windows form"}

    target.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "export.ps1"
        script.write_text(_EXPORT_PS1, encoding="utf-8")
        script_win = _to_windows_path(script)
        if script_win is None:
            hosted = (staged_dir or target.parent) / "export.ps1"
            hosted.write_text(_EXPORT_PS1, encoding="utf-8")
            script_win = _to_windows_path(hosted)
        result = _run(
            [
                ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_win),
                "-In", src_win, "-Out", dst_win,
                "-SlideSeconds", str(slide_seconds), "-VertRes", str(vert_res),
                "-Fps", str(fps), "-TimeoutMin", str(timeout_min),
            ],
            timeout=timeout_min * 60 + 120,
        )

    status = None
    error = ""
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("STATUS="):
            status = int(line.split("=", 1)[1])
        elif line.startswith("ERROR="):
            error = line.split("=", 1)[1]

    if status != STATUS_DONE or not target.is_file():
        return {
            "ok": False,
            "reason": error or f"CreateVideo returned status {status}",
            "status": status,
        }
    if target != out_video:
        out_video.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, out_video)
    if staged_dir is not None:
        shutil.rmtree(staged_dir, ignore_errors=True)
    return {"ok": True, "status": status, "bytes": out_video.stat().st_size}


def build_sheet(
    video: Path, out_dir: Path, *, sample_fps: float, columns: int, width: int
) -> dict[str, Any]:
    if not shutil.which("ffmpeg"):
        return {"ok": False, "reason": "ffmpeg not found"}
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for stale in frames_dir.glob("motion_*.png"):
        stale.unlink()

    extract = _run(
        [
            "ffmpeg", "-v", "error", "-i", str(video),
            "-vf", f"fps={sample_fps},scale={width}:-2",
            str(frames_dir / "motion_%03d.png"),
        ],
        timeout=900,
    )
    frames = sorted(frames_dir.glob("motion_*.png"))
    if not frames:
        return {"ok": False, "reason": f"no frames extracted: {extract.stderr[:200]}"}

    rows = (len(frames) + columns - 1) // columns
    sheet = out_dir / "motion-contact-sheet.png"
    tile = _run(
        [
            "ffmpeg", "-v", "error", "-y", "-i", str(video),
            "-vf",
            f"fps={sample_fps},scale={width}:-2,tile={columns}x{rows}:padding=6:margin=6:color=white",
            "-frames:v", "1", str(sheet),
        ],
        timeout=900,
    )
    if not sheet.is_file():
        return {"ok": False, "reason": f"tiling failed: {tile.stderr[:200]}"}
    return {
        "ok": True,
        "frames": len(frames),
        "grid": f"{columns}x{rows}",
        "frames_dir": str(frames_dir),
        "contact_sheet": str(sheet),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", nargs="?", help="deck to render")
    parser.add_argument("--out-dir", type=Path, default=Path("qa/motion"))
    parser.add_argument("--from-video", type=Path, help="skip export; sample this MP4")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--slide-seconds", type=int, default=2)
    parser.add_argument("--vert-res", type=int, default=720)
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--sample-fps", type=float, default=4.0)
    parser.add_argument("--columns", type=int, default=6)
    parser.add_argument("--frame-width", type=int, default=320)
    parser.add_argument("--timeout-min", type=int, default=6)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report: dict[str, Any] = {"contract_version": "1.0", "status": "blocked"}
    ps = _powershell()

    if args.from_video is None:
        report["preflight"] = preflight(ps)
        if args.preflight_only or not report["preflight"]["ok"]:
            report["status"] = "ready" if report["preflight"]["ok"] else "blocked"
            _emit(report, args.json)
            return 0 if report["preflight"]["ok"] else 3
    if args.preflight_only:
        _emit(report, args.json)
        return 0

    args.out_dir.mkdir(parents=True, exist_ok=True)

    if args.from_video is not None:
        video = args.from_video
        if not video.is_file():
            report["reason"] = f"missing video: {video}"
            _emit(report, args.json)
            return 1
    else:
        if not args.pptx:
            parser.error("pptx is required unless --from-video is given")
        pptx = Path(args.pptx)
        if not pptx.is_file():
            report["reason"] = f"missing deck: {pptx}"
            _emit(report, args.json)
            return 1
        video = args.out_dir / (pptx.stem + ".mp4")
        export = export_video(
            pptx, video, ps=ps, slide_seconds=args.slide_seconds,
            vert_res=args.vert_res, fps=args.fps, timeout_min=args.timeout_min,
        )
        report["export"] = export
        if not export["ok"]:
            _emit(report, args.json)
            return 3
        report["video"] = str(video)

    sheet = build_sheet(
        video, args.out_dir, sample_fps=args.sample_fps,
        columns=args.columns, width=args.frame_width,
    )
    report["contact_sheet"] = sheet
    report["status"] = "reviewed-input" if sheet["ok"] else "blocked"
    _emit(report, args.json)
    return 0 if sheet["ok"] else 3


def _emit(report: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    print(f"status: {report['status']}")
    pre = report.get("preflight")
    if pre:
        if pre["ok"]:
            print(f"- preflight OK (PowerPoint {pre.get('version','?')})")
            if pre.get("running_instances"):
                print(
                    f"  note: {pre['running_instances']} PowerPoint instance(s) already "
                    "running; COM will attach to one of them"
                )
        else:
            print(f"- preflight BLOCKED: {pre['reason']}")
    if "export" in report and not report["export"]["ok"]:
        print(f"- export BLOCKED: {report['export']['reason']}")
    sheet = report.get("contact_sheet")
    if isinstance(sheet, dict) and sheet.get("ok"):
        print(f"- {sheet['frames']} frames, grid {sheet['grid']}")
        print(f"- contact sheet: {sheet['contact_sheet']}")
    elif isinstance(sheet, dict):
        print(f"- contact sheet BLOCKED: {sheet['reason']}")
    if "reason" in report:
        print(f"- {report['reason']}")


if __name__ == "__main__":
    raise SystemExit(main())
