#!/usr/bin/env python3
"""Run Claude Code Opus as the Meta LOOP plan or final aggregator."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True, choices=("plan", "final"))
    parser.add_argument("--input-file", required=True, type=Path)
    parser.add_argument("--output-file", required=True, type=Path)
    parser.add_argument("--model", default=os.getenv("META_LOOP_AGGREGATOR_MODEL", "opus"))
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--claude", default="claude")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    source = args.input_file.expanduser().resolve()
    output = args.output_file.expanduser().resolve()
    error = Path(str(output) + ".stderr")
    executable = shutil.which(args.claude)
    errors = []
    if not source.is_file() or source.stat().st_size == 0:
        errors.append(f"input file is missing or empty: {source}")
    if source == output:
        errors.append("output file cannot overwrite input file")
    if not executable:
        errors.append(f"claude executable not found: {args.claude}")
    if not args.model.strip():
        errors.append("model must be non-empty")
    if not 1 <= args.timeout_seconds <= 3600:
        errors.append("timeout-seconds must be from 1 to 3600")
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, indent=2), file=sys.stderr)
        return 2
    plan = {"ok": True, "dry_run": args.dry_run, "stage": args.stage,
            "claude": executable, "model": args.model, "input_file": str(source),
            "input_bytes": source.stat().st_size, "output_file": str(output),
            "stderr_file": str(error), "timeout_seconds": args.timeout_seconds}
    if args.dry_run:
        print(json.dumps(plan, indent=2))
        return 0
    verdicts = "PROCEED, REVISE, or BLOCK" if args.stage == "plan" else "SHIP, CONDITIONAL, or BLOCK"
    system = (
        "You are Claude Code Opus, the sole orchestrator and aggregator for a bounded Meta LOOP. "
        "Codex models are independent workers; never invent missing worker evidence. Review every "
        "success criterion, resolve contradictions explicitly, cite worker IDs when present, and "
        f"begin with exactly one verdict: {verdicts}. You have no tools and must return only the "
        "decision, rationale, required corrections, and approved synthesis."
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="meta-loop-opus-") as scratch:
        mcp = Path(scratch) / "mcp.json"
        mcp.write_text('{"mcpServers": {}}\n', encoding="utf-8")
        command = [executable, "--model", args.model, "--tools", "", "--disable-slash-commands",
                   "--no-session-persistence", "--mcp-config", str(mcp), "--strict-mcp-config",
                   "--system-prompt", system, "--output-format", "text", "-p"]
        try:
            completed = subprocess.run(command, input=source.read_bytes(), cwd=scratch,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       timeout=args.timeout_seconds, check=False)
            stdout, stderr, exit_code = completed.stdout, completed.stderr, completed.returncode
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout or b""
            stderr = (exc.stderr or b"") + f"\nmeta-loop: timeout after {args.timeout_seconds}s\n".encode()
            exit_code = 124
    output.write_bytes(stdout)
    error.write_bytes(stderr)
    first_line = stdout.decode("utf-8", errors="replace").lstrip().splitlines()[:1]
    expected = ("PROCEED", "REVISE", "BLOCK") if args.stage == "plan" else ("SHIP", "CONDITIONAL", "BLOCK")
    normalized_verdict = first_line[0].strip().lstrip("#>*- ").strip("*_` ").upper() if first_line else ""
    valid_verdict = normalized_verdict in expected
    summary = dict(plan, dry_run=False, exit_code=exit_code, verdict_valid=valid_verdict,
                   output_bytes=len(stdout), elapsed_seconds=round(time.monotonic() - started, 3),
                   ok=exit_code == 0 and bool(stdout.strip()) and valid_verdict)
    print(json.dumps(summary, indent=2))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
