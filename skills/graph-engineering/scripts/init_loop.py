#!/usr/bin/env python3
"""Scaffold the state layer for a graph-engineering contract loop.

Writes the four persistent artifacts a cold run needs to pick up work, plus the
adversarial auditor subagent, and initializes a git repo.

Stdlib only. No network. Idempotent: existing files are left alone unless
--force is passed.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS = SKILL_DIR / "assets"

PROGRESS_HEADER = """\
# {project}
# Progress log. Newest entries at the bottom.
#
# One line per run. Record what was tried, what failed, and what the next run
# should know. The "note for next run" lines are the ones that make the loop
# get smarter without anyone retraining anything.
#
# Format: <timestamp> | <item id> | <what happened>

{stamp} | -- | Loop initialized. No items attempted yet.
"""

INIT_SH = """\
#!/usr/bin/env bash
# Boot script for: {project}
#
# Every run calls this instead of rediscovering how to launch the thing.
# Keep it fast and idempotent. Exit non-zero if the environment is not usable.

set -euo pipefail

echo "[init] project: {project}"
echo "[init] pwd: $(pwd)"

# --- Add environment setup below. Examples:
# python3 -m venv .venv && source .venv/bin/activate
# npm install --silent
# docker compose up -d

echo "[init] ready"
"""

SAMPLE_ITEMS = [
    {
        "id": 1,
        "name": "REPLACE ME: one thing you can watch succeed or fail",
        "status": "failing",
        "verified_by": "REPLACE ME: the exact command that decides",
        "notes": "",
    }
]


def _stamp() -> str:
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d %H:%M")


def _write(path: Path, content: str, force: bool, executable: bool = False) -> str:
    """Write content to path. Returns one of: created, skipped, overwritten."""
    existed = path.exists()
    if existed and not force:
        return "skipped"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if executable:
        path.chmod(path.stat().st_mode | 0o111)
    return "overwritten" if existed else "created"


def _render_asset(name: str, **subs: str) -> str:
    src = ASSETS / name
    if not src.is_file():
        raise SystemExit(f"ERROR: missing bundled asset: {src}")
    text = src.read_text(encoding="utf-8")
    for key, value in subs.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )


def init_git(root: Path, quiet: bool) -> str:
    if not shutil.which("git"):
        return "git not found on PATH — skipped"
    if (root / ".git").is_dir():
        return "already a git repo"
    res = _git(root, "init", "-q")
    if res.returncode != 0:
        return f"git init failed: {res.stderr.strip()}"
    _git(root, "add", "-A")
    commit = _git(
        root, "-c", "user.name=graph-engineering", "-c",
        "user.email=graph-engineering@localhost",
        "commit", "-q", "-m", "Initialize contract loop state layer",
    )
    if commit.returncode != 0:
        return "git init ok, initial commit skipped (nothing to commit or hooks blocked it)"
    return "git initialized with an initial commit"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Scaffold a graph-engineering contract loop state layer.",
    )
    ap.add_argument("--project", required=True, help="Project name, used in headers")
    ap.add_argument("--dir", default=".", help="Target directory (default: cwd)")
    ap.add_argument(
        "--force", action="store_true",
        help="Overwrite existing artifacts instead of leaving them alone",
    )
    ap.add_argument(
        "--no-git", action="store_true", help="Skip git initialization",
    )
    ap.add_argument("--quiet", action="store_true", help="Only print errors")
    args = ap.parse_args(argv)

    root = Path(args.dir).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()

    results: list[tuple[str, str]] = []

    feature_list = {
        "project": args.project,
        "created": today,
        "items": SAMPLE_ITEMS,
    }
    results.append((
        "feature_list.json",
        _write(
            root / "feature_list.json",
            json.dumps(feature_list, indent=2) + "\n",
            args.force,
        ),
    ))

    results.append((
        "claude-progress.txt",
        _write(
            root / "claude-progress.txt",
            PROGRESS_HEADER.format(project=args.project, stamp=_stamp()),
            args.force,
        ),
    ))

    results.append((
        "init.sh",
        _write(
            root / "init.sh",
            INIT_SH.format(project=args.project),
            args.force,
            executable=True,
        ),
    ))

    results.append((
        "contract.md",
        _write(
            root / "contract.md",
            _render_asset("contract-template.md", PROJECT=args.project, DATE=today),
            args.force,
        ),
    ))

    results.append((
        ".claude/agents/auditor.md",
        _write(
            root / ".claude" / "agents" / "auditor.md",
            _render_asset("auditor.md"),
            args.force,
        ),
    ))

    (root / "traces").mkdir(exist_ok=True)
    results.append(("traces/", "created" if not args.quiet else "created"))

    git_note = "skipped (--no-git)" if args.no_git else init_git(root, args.quiet)

    if not args.quiet:
        print(f"Contract loop scaffolded in {root}\n")
        width = max(len(name) for name, _ in results)
        for name, status in results:
            print(f"  {name.ljust(width)}  {status}")
        print(f"\n  git: {git_note}\n")
        skipped = [n for n, s in results if s == "skipped"]
        if skipped:
            print("Existing files were left alone. Re-run with --force to replace them.\n")
        print("Next:")
        print("  1. Edit feature_list.json — replace the sample item. Every item needs")
        print("     a verified_by command. If you cannot write one, rewrite the item.")
        print("  2. Read .claude/agents/auditor.md and tune the rubric to your work.")
        print("  3. Negotiate contract.md with the auditor, then set Status: AGREED.")
        print("  4. Gate on it:  python3 scripts/check_contract.py --dir .")

    return 0


if __name__ == "__main__":
    sys.exit(main())
