#!/usr/bin/env python3
"""Run optional OfficeCLI QA for Office deliverables.

The script records validation, issue, HTML, and screenshot attempts in one
artifact folder, and exits cleanly when OfficeCLI is unavailable so existing
skill fallbacks can continue.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


OFFICE_EXTS = {".docx", ".xlsx", ".pptx"}


def run_command(cmd: list[str], out_dir: Path, name: str) -> dict:
    result = subprocess.run(cmd, capture_output=True, text=True)
    record = {
        "name": name,
        "command": cmd,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    (out_dir / f"{name}.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record


def write_summary(out_dir: Path, status: str, records: list[dict], reason: str | None = None) -> None:
    lines = [
        "# OfficeCLI QA Summary",
        "",
        f"- Status: `{status}`",
        f"- Checked at: `{datetime.now(timezone.utc).isoformat()}`",
    ]
    if reason:
        lines.append(f"- Reason: {reason}")
    for record in records:
        result = "failed" if command_failed(record) else "passed"
        lines.append(f"- `{record['name']}`: `{result}` (exit `{record.get('returncode')}`)")
    (out_dir / "qa-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def is_screenshot_sandbox_block(record: dict) -> bool:
    if record.get("name") != "screenshot" or record.get("returncode") == 0:
        return False
    stderr = (record.get("stderr") or "").lower()
    markers = [
        "no headless browser available",
        "operation canceled",
        "operation not permitted",
        "setsockopt",
        "crashpad",
    ]
    return any(marker in stderr for marker in markers)


def command_failed(record: dict) -> bool:
    """Treat semantic validation failures as failures even when the CLI exits 0."""
    if record.get("returncode") != 0:
        return True
    if record.get("name") not in {"validate", "issues"}:
        return False
    try:
        payload = json.loads(record.get("stdout") or "{}")
    except json.JSONDecodeError:
        return True
    if payload.get("success") is not True:
        return True
    if record.get("name") == "issues":
        return int((payload.get("data") or {}).get("count", 0)) > 0
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Run OfficeCLI QA for .docx/.xlsx/.pptx files.")
    parser.add_argument("file", help="Office file to inspect")
    parser.add_argument("--out", default=None, help="QA artifact directory")
    parser.add_argument(
        "--required",
        action="store_true",
        help="Return non-zero when OfficeCLI is missing or QA commands fail",
    )
    args = parser.parse_args()

    target = Path(args.file).resolve()
    out_dir = Path(args.out).resolve() if args.out else target.with_suffix("").parent / "qa" / "officecli"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not target.exists():
        write_summary(out_dir, "failed", [], f"File not found: {target}")
        return 2

    if target.suffix.lower() not in OFFICE_EXTS:
        write_summary(out_dir, "skipped", [], f"Unsupported extension: {target.suffix}")
        return 1 if args.required else 0

    officecli = shutil.which("officecli")
    if not officecli:
        write_summary(out_dir, "skipped", [], "officecli is not installed or not on PATH")
        return 1 if args.required else 0

    render_dir = out_dir / "render"
    render_dir.mkdir(exist_ok=True)
    html_path = out_dir / f"{target.stem}.html"
    screenshot_path = render_dir / f"{target.stem}.png"

    screenshot_cmd = [officecli, "view", str(target), "screenshot", "-o", str(screenshot_path)]
    if target.suffix.lower() == ".pptx":
        screenshot_cmd.extend(["--grid", "4"])

    commands = [
        ("validate", [officecli, "validate", str(target), "--json"]),
        ("issues", [officecli, "view", str(target), "issues", "--json"]),
        ("html", [officecli, "view", str(target), "html", "-o", str(html_path)]),
        ("screenshot", screenshot_cmd),
    ]

    records = [run_command(cmd, out_dir, name) for name, cmd in commands]
    failed = [record for record in records if command_failed(record)]
    screenshot_blocked = len(failed) == 1 and is_screenshot_sandbox_block(failed[0])
    if not failed:
        status = "passed"
        reason = None
    elif screenshot_blocked:
        status = "partial"
        reason = (
            "OfficeCLI validate/issues/html passed, but screenshot rendering was blocked "
            "by managed sandbox browser permissions."
        )
    else:
        status = "failed"
        reason = None
    write_summary(out_dir, status, records, reason)
    return 1 if failed and args.required else 0


if __name__ == "__main__":
    sys.exit(main())
