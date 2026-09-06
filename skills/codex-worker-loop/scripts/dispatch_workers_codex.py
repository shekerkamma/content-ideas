#!/usr/bin/env python3
"""Dispatch isolated Codex CLI (GPT-5.6 Sol) workers from a validated JSON manifest.

Adapted for Codex CLI from the agy-based dispatch discipline in a Hermes-agent
adaptation of Shubham Saboo's Apache-2.0 advisor-orchestrator-worker skill.
See references/attribution.md. Unlike that ancestor, workers here write
directly into the real target repo under `-C <repo_dir>` (codex exec -s
workspace-write) rather than into an isolated empty scratch directory --
this is a build tool, not a text generator.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Any

MAX_WORKERS = 20
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
VALID_SANDBOXES = {"read-only", "workspace-write", "danger-full-access"}
SAFE_ENV_KEYS = {
    # POSIX (Linux/macOS)
    "PATH", "HOME", "USER", "LOGNAME", "SHELL",
    "TEMP", "TMP", "TMPDIR",
    "LANG", "LC_ALL", "TERM", "TZ", "SSL_CERT_FILE", "SSL_CERT_DIR",
    "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY",
    # Windows -- codex.exe needs these to resolve its own config/auth at all;
    # harmless no-ops on Linux/macOS since they're simply absent from os.environ there.
    "USERPROFILE", "HOMEDRIVE", "HOMEPATH", "APPDATA", "LOCALAPPDATA",
    "PROGRAMDATA", "PROGRAMFILES", "PROGRAMFILES(X86)",
    "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT",
    "PROCESSOR_ARCHITECTURE", "NUMBER_OF_PROCESSORS",
}
SENSITIVE_MARKERS = ("API_KEY", "TOKEN", "PASSWORD", "PASSWD", "SECRET", "PRIVATE_KEY", "CREDENTIAL")


class ManifestError(ValueError):
    pass


def _resolve(base: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = base / path
    return path.resolve()


def _safe_env(worker_id: str) -> dict[str, str]:
    env: dict[str, str] = {}
    for key, value in os.environ.items():
        upper = key.upper()
        if upper in SAFE_ENV_KEYS and not any(marker in upper for marker in SENSITIVE_MARKERS):
            env[key] = value
    env["CODEX_WORKER_ID"] = worker_id
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ManifestError(f"manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ManifestError(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc

    if not isinstance(data, dict):
        raise ManifestError("manifest root must be an object")

    model = data.get("model", "gpt-5.6-sol")
    if not isinstance(model, str) or not model.strip():
        raise ManifestError("model must be a non-empty string")

    effort = data.get("reasoning_effort", "max")
    if not isinstance(effort, str) or not effort.strip():
        raise ManifestError("reasoning_effort must be a non-empty string")

    repo_dir_value = data.get("repo_dir")
    if not isinstance(repo_dir_value, str) or not repo_dir_value:
        raise ManifestError("repo_dir is required and must be a non-empty string")
    base = path.parent.resolve()
    repo_dir = _resolve(base, repo_dir_value)
    if not repo_dir.is_dir():
        raise ManifestError(f"repo_dir is not a directory: {repo_dir}")

    workers = data.get("workers")
    if not isinstance(workers, list) or not workers:
        raise ManifestError("workers must be a non-empty array")
    if len(workers) > MAX_WORKERS:
        raise ManifestError(f"workers exceeds hard cap {MAX_WORKERS}")

    concurrency = data.get("concurrency", min(3, len(workers)))
    timeout = data.get("timeout_seconds", 1800)
    max_brief = data.get("max_brief_bytes", 100_000)
    if not isinstance(concurrency, int) or not 1 <= concurrency <= MAX_WORKERS:
        raise ManifestError(f"concurrency must be an integer from 1 to {MAX_WORKERS}")
    if not isinstance(timeout, int) or not 1 <= timeout <= 21600:
        raise ManifestError("timeout_seconds must be an integer from 1 to 21600")
    if not isinstance(max_brief, int) or not 1 <= max_brief <= 1_000_000:
        raise ManifestError("max_brief_bytes must be an integer from 1 to 1000000")

    normalized: list[dict[str, Any]] = []
    ids: set[str] = set()
    outputs: set[str] = set()
    for index, worker in enumerate(workers):
        if not isinstance(worker, dict):
            raise ManifestError(f"workers[{index}] must be an object")
        worker_id = worker.get("id")
        if not isinstance(worker_id, str) or not ID_RE.fullmatch(worker_id):
            raise ManifestError(f"workers[{index}].id must match {ID_RE.pattern}")
        if worker_id in ids:
            raise ManifestError(f"duplicate worker id: {worker_id}")
        ids.add(worker_id)

        brief_value = worker.get("brief_file")
        output_value = worker.get("output_file")
        if not isinstance(brief_value, str) or not brief_value:
            raise ManifestError(f"{worker_id}.brief_file must be a non-empty string")
        if not isinstance(output_value, str) or not output_value:
            raise ManifestError(f"{worker_id}.output_file must be a non-empty string")
        brief = _resolve(base, brief_value)
        output = _resolve(base, output_value)
        if not brief.is_file():
            raise ManifestError(f"{worker_id} brief not found: {brief}")
        brief_bytes = brief.stat().st_size
        if brief_bytes == 0:
            raise ManifestError(f"{worker_id} brief is empty")
        if brief_bytes > max_brief:
            raise ManifestError(f"{worker_id} brief is {brief_bytes} bytes; cap is {max_brief}")
        output_key = os.path.normcase(str(output))
        if output_key in outputs:
            raise ManifestError(f"duplicate output path: {output}")
        outputs.add(output_key)
        if os.path.normcase(str(brief)) == output_key:
            raise ManifestError(f"{worker_id} output_file cannot overwrite its brief")

        worker_cwd_value = worker.get("cwd")
        worker_cwd = _resolve(base, worker_cwd_value) if worker_cwd_value else repo_dir
        if not worker_cwd.is_dir():
            raise ManifestError(f"{worker_id} cwd is not a directory: {worker_cwd}")

        sandbox = worker.get("sandbox", "workspace-write")
        if sandbox not in VALID_SANDBOXES:
            raise ManifestError(f"{worker_id}.sandbox must be one of {sorted(VALID_SANDBOXES)}")

        normalized.append({
            "id": worker_id,
            "brief_file": brief,
            "output_file": output,
            "brief_bytes": brief_bytes,
            "cwd": worker_cwd,
            "sandbox": sandbox,
        })

    return {
        "manifest": path.resolve(),
        "model": model.strip(),
        "reasoning_effort": effort.strip(),
        "repo_dir": repo_dir,
        "concurrency": concurrency,
        "timeout_seconds": timeout,
        "max_brief_bytes": max_brief,
        "workers": normalized,
    }


async def _terminate(proc: asyncio.subprocess.Process) -> None:
    if proc.returncode is not None:
        return
    proc.terminate()
    try:
        await asyncio.wait_for(proc.wait(), timeout=5)
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()


async def run_worker(
    worker: dict[str, Any],
    *,
    executable: str,
    model: str,
    reasoning_effort: str,
    timeout_seconds: int,
    semaphore: asyncio.Semaphore,
) -> dict[str, Any]:
    worker_id = worker["id"]
    brief_path: Path = worker["brief_file"]
    output_path: Path = worker["output_file"]
    worker_cwd: Path = worker["cwd"]
    sandbox: str = worker["sandbox"]
    stderr_path = Path(str(output_path) + ".stderr")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    proc: asyncio.subprocess.Process | None = None
    status = "FAILED_DISPATCH"
    exit_code: int | None = None
    stdout = b""
    stderr = b""

    async with semaphore:
        try:
            brief = brief_path.read_bytes()
            command = [
                executable,
                "exec",
                "-s", sandbox,
                "-m", model,
                "-c", f'model_reasoning_effort="{reasoning_effort}"',
                "-C", str(worker_cwd),
                "-",  # read prompt from stdin, never as a CLI argument
            ]
            proc = await asyncio.create_subprocess_exec(
                *command,
                cwd=str(worker_cwd),
                env=_safe_env(worker_id),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            try:
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(input=brief), timeout=timeout_seconds + 10
                )
                exit_code = proc.returncode
                if exit_code == 0 and stdout.strip():
                    status = "PASS_DISPATCH"
            except asyncio.TimeoutError:
                status = "TIMEOUT"
                await _terminate(proc)
                exit_code = proc.returncode
                stderr += f"\ncodex-worker-loop: timeout after {timeout_seconds}s\n".encode()
            except asyncio.CancelledError:
                await _terminate(proc)
                raise
        except Exception as exc:  # Process/setup failures must become ledger evidence.
            stderr += f"\ncodex-worker-loop: {type(exc).__name__}: {exc}\n".encode()
            status = "FAILED_DISPATCH"

    output_path.write_text(stdout.decode("utf-8", errors="replace"), encoding="utf-8")
    stderr_path.write_text(stderr.decode("utf-8", errors="replace"), encoding="utf-8")
    elapsed = round(time.monotonic() - started, 3)
    return {
        "id": worker_id,
        "status": status,
        "exit_code": exit_code,
        "output_bytes": len(stdout),
        "elapsed_seconds": elapsed,
        "output_file": str(output_path),
        "stderr_file": str(stderr_path),
        "cwd": str(worker_cwd),
        "sandbox": sandbox,
    }


async def run_all(config: dict[str, Any], executable: str) -> list[dict[str, Any]]:
    semaphore = asyncio.Semaphore(config["concurrency"])
    tasks = [
        asyncio.create_task(run_worker(
            worker,
            executable=executable,
            model=config["model"],
            reasoning_effort=config["reasoning_effort"],
            timeout_seconds=config["timeout_seconds"],
            semaphore=semaphore,
        ))
        for worker in config["workers"]
    ]
    return await asyncio.gather(*tasks)


def _check_subscription_auth(codex_home: Path) -> tuple[bool, str]:
    auth_file = codex_home / "auth.json"
    if not auth_file.is_file():
        return False, f"no auth.json found at {auth_file} -- run `codex login` first"
    try:
        auth = json.loads(auth_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"could not read/parse {auth_file}: {exc}"
    mode = auth.get("auth_mode")
    if mode != "chatgpt":
        return False, (
            f"auth_mode is '{mode}', not 'chatgpt' -- this looks like API-key auth. "
            "Run `codex login` (interactive OAuth) instead of `codex login --with-api-key` "
            "before dispatching, or every worker call will bill per-token instead of "
            "drawing on the subscription."
        )
    return True, "subscription auth confirmed"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--codex", default="codex", help="codex executable name or absolute path")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--skip-auth-check", action="store_true",
        help="Skip the subscription-auth-mode check (not recommended)",
    )
    args = parser.parse_args()

    try:
        config = load_manifest(args.manifest.expanduser().resolve())
        executable = shutil.which(args.codex)
        if not executable:
            raise ManifestError(f"codex executable not found: {args.codex}")
    except ManifestError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2

    auth_ok, auth_message = (True, "skipped") if args.skip_auth_check else _check_subscription_auth(
        Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    )
    if not auth_ok and not args.dry_run:
        print(json.dumps({"ok": False, "error": auth_message}, indent=2), file=sys.stderr)
        return 3

    plan = {
        "ok": True,
        "dry_run": args.dry_run,
        "manifest": str(config["manifest"]),
        "codex": executable,
        "model": config["model"],
        "reasoning_effort": config["reasoning_effort"],
        "repo_dir": str(config["repo_dir"]),
        "concurrency": config["concurrency"],
        "timeout_seconds": config["timeout_seconds"],
        "auth_check": auth_message,
        "workers": [
            {
                "id": w["id"],
                "brief_file": str(w["brief_file"]),
                "brief_bytes": w["brief_bytes"],
                "output_file": str(w["output_file"]),
                "cwd": str(w["cwd"]),
                "sandbox": w["sandbox"],
            }
            for w in config["workers"]
        ],
    }
    if args.dry_run:
        print(json.dumps(plan, indent=2))
        return 0

    try:
        results = asyncio.run(run_all(config, executable))
    except KeyboardInterrupt:
        print(json.dumps({"ok": False, "error": "interrupted"}, indent=2), file=sys.stderr)
        return 130

    summary = dict(plan)
    summary["dry_run"] = False
    summary["results"] = results
    summary["ok"] = all(result["status"] == "PASS_DISPATCH" for result in results)
    print(json.dumps(summary, indent=2))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
