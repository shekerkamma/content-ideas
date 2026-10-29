#!/usr/bin/env python3
"""Run the existing Claude/Codex /watch skill from Codex Desktop.

This wrapper prefers a local WATCH_SKILL_DIR. On Windows it falls back to the
known WSL path reported by Claude Code.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import shlex
import subprocess
import sys


DEFAULT_WSL_WATCH_DIR = str(pathlib.Path(__file__).resolve().parents[2] / "watch")


def win_to_wsl(path: pathlib.Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    rest = str(resolved)[3:].replace("\\", "/")
    return f"/mnt/{drive}/{rest}"


def run(cmd: list[str], *, stdout=None) -> None:
    result = subprocess.run(cmd, stdout=stdout, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or f"Command failed: {' '.join(cmd)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="YouTube URL or local video path")
    parser.add_argument("--out-dir", required=True, help="Output directory for report and watch artifacts")
    parser.add_argument("--max-frames", type=int)
    parser.add_argument("--resolution", type=int)
    parser.add_argument("--fps", type=float)
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--no-whisper", action="store_true")
    parser.add_argument("--whisper", choices=["groq", "openai"])
    parser.add_argument("--watch-skill-dir", default=os.environ.get("WATCH_SKILL_DIR"))
    args = parser.parse_args()

    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report = out_dir / "report.md"
    watch_out = out_dir / "watch"
    watch_out.mkdir(parents=True, exist_ok=True)

    extra: list[str] = []
    for opt in ("max_frames", "resolution", "fps", "start", "end"):
        value = getattr(args, opt)
        if value is not None:
            extra.extend([f"--{opt.replace('_', '-')}", str(value)])
    if args.no_whisper:
        extra.append("--no-whisper")
    if args.whisper:
        extra.extend(["--whisper", args.whisper])

    local_skill = (
        pathlib.Path(args.watch_skill_dir).expanduser()
        if args.watch_skill_dir
        else pathlib.Path(DEFAULT_WSL_WATCH_DIR)
    )
    if local_skill and (local_skill / "scripts" / "watch.py").exists():
        cmd = [sys.executable, str(local_skill / "scripts" / "setup.py"), "--check"]
        run(cmd)
        watch_cmd = [
            sys.executable,
            str(local_skill / "scripts" / "watch.py"),
            args.source,
            "--out-dir",
            str(watch_out),
            *extra,
        ]
        with report.open("w", encoding="utf-8") as f:
            run(watch_cmd, stdout=f)
        print(report)
        return 0

    if os.name == "nt":
        wsl_check = f"test -f {shlex.quote(DEFAULT_WSL_WATCH_DIR)}/scripts/watch.py"
        run(["wsl", "bash", "-lc", wsl_check])
        wsl_out = win_to_wsl(watch_out)
        wsl_report = win_to_wsl(report)
        quoted_extra = " ".join(shlex.quote(x) for x in extra)
        source = shlex.quote(args.source)
        setup_py = f"{DEFAULT_WSL_WATCH_DIR}/scripts/setup.py"
        watch_py = f"{DEFAULT_WSL_WATCH_DIR}/scripts/watch.py"
        cmd = (
            f"python3 {shlex.quote(setup_py)} --check && "
            f"mkdir -p {shlex.quote(wsl_out)} && "
            f"python3 {shlex.quote(watch_py)} {source} "
            f"--out-dir {shlex.quote(wsl_out)} {quoted_extra} > {shlex.quote(wsl_report)}"
        )
        run(["wsl", "bash", "-lc", cmd])
        print(report)
        return 0

    raise SystemExit("Could not find /watch skill. Set WATCH_SKILL_DIR to the skill folder.")


if __name__ == "__main__":
    raise SystemExit(main())
