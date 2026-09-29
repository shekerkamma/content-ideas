"""graphify-pro must fail closed: no proxy, no run, and never the billed Gemini key."""
import os
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "graphify-pro"

pytestmark = pytest.mark.skipif(shutil.which("bash") is None, reason="needs bash")


def run(args, tmp_path, **env):
    creds = tmp_path / "creds.yaml"
    creds.write_text("CLIPROXY_API_KEY: fake-proxy-key\n")
    base = {"PATH": os.environ["PATH"], "HOME": str(tmp_path), "CLIPROXY_CREDS": str(creds),
            "GEMINI_API_KEY": "billed-key-must-not-leak"}
    return subprocess.run(["bash", str(SCRIPT), *args], capture_output=True, text=True,
                          env={**base, **env}, timeout=30)


def test_script_parses():
    assert subprocess.run(["bash", "-n", str(SCRIPT)]).returncode == 0


def test_dead_proxy_fails_closed(tmp_path):
    # Port 1 on localhost refuses at once: the negative control for the probe.
    r = run(["--env"], tmp_path, CLIPROXY_HOST="127.0.0.1", CLIPROXY_PORT="1",
            GRAPHIFY_PRO_MODEL="gemini-3.8-flash-high")
    assert r.returncode == 1
    assert "refusing to fall back" in r.stderr
    assert r.stdout == ""  # nothing to eval, so no half-configured environment


def test_dead_proxy_never_runs_the_command(tmp_path):
    marker = tmp_path / "ran"
    r = run(["touch", str(marker)], tmp_path, CLIPROXY_HOST="127.0.0.1", CLIPROXY_PORT="1",
            GRAPHIFY_PRO_MODEL="gemini-3.8-flash-high")
    assert r.returncode == 1 and not marker.exists()


def test_missing_key_is_an_error(tmp_path):
    r = subprocess.run(["bash", str(SCRIPT), "--check"], capture_output=True, text=True, timeout=30,
                       env={"PATH": os.environ["PATH"], "HOME": str(tmp_path), "USER": "nobody-here",
                            "CLIPROXY_CREDS": str(tmp_path / "absent.yaml"), "CLIPROXY_HOST": "127.0.0.1",
                            "GRAPHIFY_PRO_MODEL": "gemini-3.8-flash-high"})
    assert r.returncode == 1 and "no CLIProxyAPI key" in r.stderr


def fake_claude_path(tmp_path):
    bindir = tmp_path / "bin"
    bindir.mkdir()
    claude = bindir / "claude"
    claude.write_text("#!/bin/sh\necho '9.9.9 (Claude Code)'\n")
    claude.chmod(0o755)
    return f"{bindir}:{os.environ['PATH']}"


def test_default_is_sonnet_via_claude_cli_and_drops_the_billed_key(tmp_path):
    r = run(["--env"], tmp_path, PATH=fake_claude_path(tmp_path))
    assert r.returncode == 0, r.stderr
    assert "unset GEMINI_API_KEY GOOGLE_API_KEY" in r.stdout
    assert "export GRAPHIFY_PRO_BACKEND=claude-cli" in r.stdout
    assert "export GRAPHIFY_CLAUDE_CLI_MODEL=claude-sonnet-5-5" in r.stdout
    assert "export CLAUDE_MEMORY_WORKER=1" in r.stdout
    assert "billed-key-must-not-leak" not in r.stdout


def test_claude_cli_mode_needs_claude_on_path(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    r = run(["--env"], tmp_path, PATH=f"{empty}:/usr/bin:/bin")
    if subprocess.run(["bash", "-c", "PATH=/usr/bin:/bin command -v claude"]).returncode == 0:
        pytest.skip("a system-wide claude would satisfy the check")
    assert r.returncode == 1 and "'claude' CLI not on PATH" in r.stderr and r.stdout == ""
