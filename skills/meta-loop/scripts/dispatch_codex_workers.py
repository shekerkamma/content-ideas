#!/usr/bin/env python3
"""Dispatch isolated Codex CLI workers from a validated JSON manifest."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

MAX_WORKERS = 20
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
SAFE_ENV_KEYS = {
    "PATH", "HOME", "USERPROFILE", "HOMEDRIVE", "HOMEPATH", "SYSTEMROOT",
    "WINDIR", "COMSPEC", "PATHEXT", "TEMP", "TMP", "APPDATA", "LOCALAPPDATA",
    "PROGRAMDATA", "PROGRAMFILES", "PROGRAMFILES(X86)", "LANG", "LC_ALL", "TERM",
    "TZ", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY",
    "CODEX_HOME",
}
SENSITIVE_MARKERS = ("API_KEY", "TOKEN", "PASSWORD", "PASSWD", "SECRET", "PRIVATE_KEY", "CREDENTIAL")


class ManifestError(ValueError):
    pass


def _resolve(base: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return (path if path.is_absolute() else base / path).resolve()


def _safe_env(worker_id: str) -> dict[str, str]:
    env = {
        key: value for key, value in os.environ.items()
        if key.upper() in SAFE_ENV_KEYS
        and not any(marker in key.upper() for marker in SENSITIVE_MARKERS)
    }
    env["META_LOOP_WORKER_ID"] = worker_id
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
    workers = data.get("workers")
    if not isinstance(workers, list) or not workers:
        raise ManifestError("workers must be a non-empty array")
    if len(workers) > MAX_WORKERS:
        raise ManifestError(f"workers exceeds hard cap {MAX_WORKERS}")
    concurrency = data.get("concurrency", min(3, len(workers)))
    timeout = data.get("timeout_seconds", 600)
    max_brief = data.get("max_brief_bytes", 100_000)
    default_model = data.get("default_model")
    if default_model is not None and (not isinstance(default_model, str) or not default_model.strip()):
        raise ManifestError("default_model must be omitted or a non-empty string")
    if not isinstance(concurrency, int) or not 1 <= concurrency <= MAX_WORKERS:
        raise ManifestError(f"concurrency must be from 1 to {MAX_WORKERS}")
    if not isinstance(timeout, int) or not 1 <= timeout <= 3600:
        raise ManifestError("timeout_seconds must be from 1 to 3600")
    if not isinstance(max_brief, int) or not 1 <= max_brief <= 1_000_000:
        raise ManifestError("max_brief_bytes must be from 1 to 1000000")

    base = path.parent.resolve()
    ids: set[str] = set()
    outputs: set[str] = set()
    normalized = []
    for index, worker in enumerate(workers):
        if not isinstance(worker, dict):
            raise ManifestError(f"workers[{index}] must be an object")
        worker_id = worker.get("id")
        if not isinstance(worker_id, str) or not ID_RE.fullmatch(worker_id):
            raise ManifestError(f"workers[{index}].id is invalid")
        if worker_id in ids:
            raise ManifestError(f"duplicate worker id: {worker_id}")
        ids.add(worker_id)
        brief_value, output_value = worker.get("brief_file"), worker.get("output_file")
        if not isinstance(brief_value, str) or not brief_value:
            raise ManifestError(f"{worker_id}.brief_file must be a non-empty string")
        if not isinstance(output_value, str) or not output_value:
            raise ManifestError(f"{worker_id}.output_file must be a non-empty string")
        brief, output = _resolve(base, brief_value), _resolve(base, output_value)
        if not brief.is_file() or brief.stat().st_size == 0:
            raise ManifestError(f"{worker_id} brief is missing or empty: {brief}")
        if brief.stat().st_size > max_brief:
            raise ManifestError(f"{worker_id} brief exceeds {max_brief} bytes")
        output_key = os.path.normcase(str(output))
        if output_key in outputs or os.path.normcase(str(brief)) == output_key:
            raise ManifestError(f"duplicate or unsafe output path: {output}")
        outputs.add(output_key)
        model = worker.get("model", default_model)
        if model is not None and (not isinstance(model, str) or not model.strip()):
            raise ManifestError(f"{worker_id}.model must be omitted or a non-empty string")
        normalized.append({"id": worker_id, "brief_file": brief, "output_file": output,
                           "brief_bytes": brief.stat().st_size, "model": model})
    return {"manifest": path.resolve(), "concurrency": concurrency, "timeout_seconds": timeout,
            "workers": normalized}


async def _terminate(proc: asyncio.subprocess.Process) -> None:
    if proc.returncode is not None:
        return
    proc.terminate()
    try:
        await asyncio.wait_for(proc.wait(), timeout=5)
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()


async def run_worker(worker: dict[str, Any], executable: str, timeout: int,
                     semaphore: asyncio.Semaphore) -> dict[str, Any]:
    worker_id = worker["id"]
    output: Path = worker["output_file"]
    log = Path(str(output) + ".log")
    error = Path(str(output) + ".stderr")
    output.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    stdout = stderr = b""
    exit_code: int | None = None
    status = "FAILED_DISPATCH"
    async with semaphore:
        try:
            with tempfile.TemporaryDirectory(prefix=f"meta-loop-{worker_id}-") as scratch:
                command = [executable, "exec", "--ignore-user-config", "--sandbox", "read-only", "--ephemeral",
                           "--skip-git-repo-check", "--color", "never", "--cd", scratch,
                           "--output-last-message", str(output)]
                if worker["model"]:
                    command.extend(["--model", worker["model"]])
                command.append("-")
                proc = await asyncio.create_subprocess_exec(
                    *command, cwd=scratch, env=_safe_env(worker_id),
                    stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                try:
                    stdout, stderr = await asyncio.wait_for(
                        proc.communicate(worker["brief_file"].read_bytes()), timeout=timeout
                    )
                    exit_code = proc.returncode
                    if exit_code == 0 and output.is_file() and output.stat().st_size:
                        status = "PASS_DISPATCH"
                except asyncio.TimeoutError:
                    status = "TIMEOUT"
                    await _terminate(proc)
                    exit_code = proc.returncode
                    stderr += f"\nmeta-loop: timeout after {timeout}s\n".encode()
        except Exception as exc:
            stderr += f"\nmeta-loop: {type(exc).__name__}: {exc}\n".encode()
    log.write_bytes(stdout)
    error.write_bytes(stderr)
    return {"id": worker_id, "model": worker["model"] or "codex-default", "status": status,
            "exit_code": exit_code, "output_file": str(output), "log_file": str(log),
            "stderr_file": str(error), "elapsed_seconds": round(time.monotonic() - started, 3)}


async def run_all(config: dict[str, Any], executable: str) -> list[dict[str, Any]]:
    semaphore = asyncio.Semaphore(config["concurrency"])
    return await asyncio.gather(*[
        run_worker(worker, executable, config["timeout_seconds"], semaphore)
        for worker in config["workers"]
    ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--codex", default="codex")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        config = load_manifest(args.manifest.expanduser().resolve())
        executable = shutil.which(args.codex)
        if not executable:
            raise ManifestError(f"codex executable not found: {args.codex}")
    except ManifestError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2
    plan = {"ok": True, "dry_run": args.dry_run, "codex": executable,
            "concurrency": config["concurrency"], "timeout_seconds": config["timeout_seconds"],
            "workers": [{"id": w["id"], "model": w["model"] or "codex-default",
                         "brief_file": str(w["brief_file"]), "brief_bytes": w["brief_bytes"],
                         "output_file": str(w["output_file"])} for w in config["workers"]]}
    if args.dry_run:
        print(json.dumps(plan, indent=2))
        return 0
    results = asyncio.run(run_all(config, executable))
    summary = dict(plan, dry_run=False, results=results,
                   ok=all(item["status"] == "PASS_DISPATCH" for item in results))
    print(json.dumps(summary, indent=2))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
