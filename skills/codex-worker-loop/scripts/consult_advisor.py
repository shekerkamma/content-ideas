#!/usr/bin/env python3
"""Run a tool-disabled Claude Code advisor consult with timeout and audit files.

Adapted from a Hermes-agent adaptation of Shubham Saboo's Apache-2.0
advisor-orchestrator-worker skill. See references/attribution.md. Default
model is claude-opus-5, not claude-fable-5: Opus 5 is priced at half of
Fable 5 per token and is Anthropic's stated default for agentic-coding and
enterprise-judgment work, which is exactly the shape of a plan review or
taste-pass consult -- there's no capability reason to pay Fable-5 rates here.
"""

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
    parser.add_argument("--consult-file", required=True, type=Path)
    parser.add_argument("--output-file", required=True, type=Path)
    parser.add_argument("--model", default=os.getenv("CODEX_LOOP_ADVISOR_MODEL", "claude-opus-5"))
    parser.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--claude", default="claude", help="Claude executable name or absolute path")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    consult = args.consult_file.expanduser().resolve()
    output = args.output_file.expanduser().resolve()
    stderr_path = Path(str(output) + ".stderr")
    executable = shutil.which(args.claude)

    errors: list[str] = []
    if not consult.is_file():
        errors.append(f"consult file not found: {consult}")
    elif consult.stat().st_size == 0:
        errors.append(f"consult file is empty: {consult}")
    if output == consult:
        errors.append("output file cannot overwrite consult file")
    if not executable:
        errors.append(f"claude executable not found: {args.claude}")
    if not 1 <= args.timeout_seconds <= 3600:
        errors.append("timeout-seconds must be from 1 to 3600")
    if not args.model.strip():
        errors.append("model must be non-empty")
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, indent=2), file=sys.stderr)
        return 2

    plan = {
        "ok": True,
        "dry_run": args.dry_run,
        "claude": executable,
        "model": args.model,
        "effort": args.effort,
        "consult_file": str(consult),
        "consult_bytes": consult.stat().st_size,
        "output_file": str(output),
        "stderr_file": str(stderr_path),
        "timeout_seconds": args.timeout_seconds,
        "tools_enabled": False,
        "mcp_enabled": False,
        "session_persistence": False,
    }
    if args.dry_run:
        print(json.dumps(plan, indent=2))
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    stdout = b""
    stderr = b""
    status = "FAILED_CONSULT"
    exit_code: int | None = None

    with tempfile.TemporaryDirectory(prefix="codex-worker-loop-advisor-") as scratch:
        empty_mcp = Path(scratch) / "mcp.json"
        empty_mcp.write_text('{"mcpServers": {}}\n', encoding="utf-8")
        command = [
            executable,
            "--model", args.model,
            "--effort", args.effort,
            "--tools", "",
            "--disable-slash-commands",
            "--no-session-persistence",
            "--mcp-config", str(empty_mcp),
            "--strict-mcp-config",
            "--output-format", "text",
            "-p",
        ]
        try:
            completed = subprocess.run(
                command,
                input=consult.read_bytes(),
                cwd=scratch,
                env=os.environ.copy(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=args.timeout_seconds,
                check=False,
            )
            stdout = completed.stdout
            stderr = completed.stderr
            exit_code = completed.returncode
            if exit_code == 0 and stdout.strip():
                status = "PASS_CONSULT"
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout or b""
            stderr = (exc.stderr or b"") + f"\ncodex-worker-loop: timeout after {args.timeout_seconds}s\n".encode()
            status = "TIMEOUT"
            exit_code = 124
        except Exception as exc:
            stderr = f"codex-worker-loop: {type(exc).__name__}: {exc}\n".encode()

    output.write_text(stdout.decode("utf-8", errors="replace"), encoding="utf-8")
    stderr_path.write_text(stderr.decode("utf-8", errors="replace"), encoding="utf-8")
    summary = dict(plan)
    summary.update({
        "dry_run": False,
        "status": status,
        "exit_code": exit_code,
        "output_bytes": len(stdout),
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "ok": status == "PASS_CONSULT",
    })
    print(json.dumps(summary, indent=2))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
