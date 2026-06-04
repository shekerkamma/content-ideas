"""Helpers for using gbrain as a repo-local content-research stage."""

from __future__ import annotations

import os
import pwd
import subprocess
from pathlib import Path


def real_home():
    """Return the user's real home directory, ignoring sandboxed HOME values."""
    return Path(pwd.getpwuid(os.getuid()).pw_dir)


def gbrain_env(base_env=None):
    """Build an env that lets gbrain find the real ~/.gbrain state."""
    env = dict(base_env or os.environ)
    home = str(real_home())
    env["HOME"] = home
    env.setdefault("MCP_STDIO", "1")
    bun_bin = str(real_home() / ".bun" / "bin")
    env["PATH"] = bun_bin + os.pathsep + env.get("PATH", "")
    return env


def resolve_gbrain_command():
    """Resolve the preferred gbrain command for this host."""
    home = real_home()
    bun = home / ".bun" / "bin" / "bun"
    repo_cli = home / "gbrain" / "src" / "cli.ts"
    if bun.exists() and repo_cli.exists():
        return [str(bun), "run", str(repo_cli)]
    gbrain_bin = home / ".bun" / "bin" / "gbrain"
    if gbrain_bin.exists():
        return [str(gbrain_bin)]
    return ["gbrain"]


def run_gbrain(args, input_text=None, timeout=180):
    """Run gbrain with the corrected env and return stdout."""
    proc = subprocess.run(
        [*resolve_gbrain_command(), *args],
        input=input_text,
        text=True,
        capture_output=True,
        timeout=timeout,
        env=gbrain_env(),
        check=False,
    )
    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        stdout = (proc.stdout or "").strip()
        detail = stderr or stdout or f"exit {proc.returncode}"
        raise RuntimeError(f"gbrain {' '.join(args)} failed: {detail}")
    return proc.stdout


def gbrain_available():
    """Return True when the repo-local gbrain CLI is callable."""
    try:
        run_gbrain(["version"], timeout=30)
        return True
    except Exception:  # noqa: BLE001
        return False


def recall(query_text, mode="query", timeout=180):
    """Run a recall query through gbrain."""
    if mode not in {"query", "search"}:
        raise ValueError(f"unsupported gbrain recall mode: {mode}")
    return run_gbrain([mode, query_text], timeout=timeout).strip()


def write_page(slug, body):
    """Write a durable page back into gbrain."""
    return run_gbrain(["put", slug], input_text=body)


def render_recall_note(title, query_text, response_text, slug=None):
    """Render a markdown note for the Stage 1 GBrain recall artifact."""
    frontmatter = [
        "---",
        f"title: {title}",
        "source_type: gbrain_page",
    ]
    if slug:
        frontmatter.append(f"source_slug: {slug}")
    frontmatter.extend(
        [
            "---",
            "",
            f"# {title}",
            "",
            f"Query: `{query_text}`",
            "",
            response_text.strip(),
            "",
        ]
    )
    return "\n".join(frontmatter)


def write_recall_note(path, title, query_text, response_text, slug=None):
    """Write the standardized GBrain recall note to disk."""
    note = render_recall_note(title, query_text, response_text, slug=slug)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(note, encoding="utf-8")
    return path
