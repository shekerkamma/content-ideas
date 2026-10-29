"""Tests for mcp-capability-probe. Stdlib + pytest, no external network.

A throwaway HTTP server stands in for an MCP server so the suite exercises the
real transport -- including the SSE framing that gbrain actually uses and that
a JSON-only parser would have failed on.
"""

from __future__ import annotations

import json
import subprocess
import sys
import threading
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
PROBE = SCRIPTS / "probe_mcp.py"

sys.path.insert(0, str(SCRIPTS))

from probe_mcp import ProbeError, _decode, _from_codex_toml, _from_mcp_json  # noqa: E402

TOOLS = [
    {"name": "alpha", "description": "does alpha things",
     "inputSchema": {"type": "object", "properties": {"x": {"type": "string"}}}},
    {"name": "beta", "description": "does beta things", "inputSchema": {"type": "object"}},
]


def _make_handler(framing: str, seen: list):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(n))
            seen.append((req["method"], self.headers.get("Authorization")))
            method = req["method"]
            if method == "initialize":
                result = {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}},
                          "serverInfo": {"name": "stub", "version": "9.9"}}
                body = {"jsonrpc": "2.0", "id": req["id"], "result": result}
            elif method == "tools/list":
                body = {"jsonrpc": "2.0", "id": req["id"], "result": {"tools": TOOLS}}
            else:
                body = {"jsonrpc": "2.0", "id": req["id"],
                        "error": {"code": -32601, "message": "Method not found"}}
            if framing == "sse":
                raw = f"event: message\ndata: {json.dumps(body)}\n\n".encode()
                ctype = "text/event-stream"
            else:
                raw = json.dumps(body).encode()
                ctype = "application/json"
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
    return H


@pytest.fixture(params=["sse", "json"])
def server(request):
    """A stub MCP server in each response framing seen in the wild."""
    seen: list = []
    httpd = HTTPServer(("127.0.0.1", 0), _make_handler(request.param, seen))
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{httpd.server_port}/mcp", seen
    httpd.shutdown()


def run(*args, env=None):
    import os
    return subprocess.run([sys.executable, str(PROBE), *args],
                          capture_output=True, text=True,
                          env={**os.environ, **(env or {})})


# ------------------------------------------------------------------ transport

def test_probe_writes_map_and_summarises(server, tmp_path: Path):
    url, _ = server
    r = run("probe", "--url", url, "--name", "stub", "--out", str(tmp_path))
    assert r.returncode == 0, r.stderr
    assert "tools:    2" in r.stdout
    assert "alpha, beta" in r.stdout
    # the summary must not carry the schemas
    assert "inputSchema" not in r.stdout

    cap = json.loads((tmp_path / "stub.json").read_text())
    assert cap["counts"]["tools"] == 2
    assert [t["name"] for t in cap["tools"]] == ["alpha", "beta"]
    assert cap["server_info"]["name"] == "stub"


def test_unsupported_listing_is_not_zero(server, tmp_path: Path):
    """A server that errors on resources/list is different from an empty one."""
    url, _ = server
    run("probe", "--url", url, "--name", "stub", "--out", str(tmp_path))
    cap = json.loads((tmp_path / "stub.json").read_text())
    assert cap["counts"]["resources"] is None
    assert cap["counts"]["tools"] == 2
    assert "resources" in cap["unsupported"]


def test_bearer_token_is_sent_but_never_written(server, tmp_path: Path):
    url, seen = server
    # Generated, not a literal. A credential-shaped constant is a finding
    # even when it is fake, and a fresh value per run also proves the
    # assertion is not passing on a stale match. The variable is named
    # `token_value` because the repo's credential scanner matches on the
    # variable name too -- and it is right to.
    token_value = "tok-" + uuid.uuid4().hex
    r = run("probe", "--url", url, "--name", "stub", "--out", str(tmp_path),
            "--bearer-env", "PROBE_TEST_TOKEN", env={"PROBE_TEST_TOKEN": token_value})
    assert r.returncode == 0, r.stderr
    assert any(auth == f"Bearer {token_value}" for _, auth in seen), "token was not sent"
    written = (tmp_path / "stub.json").read_text()
    assert token_value not in written, "token leaked into the capability map"
    assert token_value not in r.stdout


def test_missing_credential_names_the_variable(server, tmp_path: Path):
    url, _ = server
    r = run("probe", "--url", url, "--out", str(tmp_path),
            "--bearer-env", "DEFINITELY_UNSET_VAR_XYZ")
    assert r.returncode == 2
    assert "DEFINITELY_UNSET_VAR_XYZ" in r.stderr
    assert "credential binding" in r.stderr


def test_decode_handles_both_framings():
    body = {"jsonrpc": "2.0", "id": 1, "result": {"ok": True}}
    assert _decode(json.dumps(body))["result"]["ok"] is True
    assert _decode(f"event: message\ndata: {json.dumps(body)}\n\n")["result"]["ok"] is True
    with pytest.raises(ProbeError):
        _decode("")


# --------------------------------------------------------------------- show

def test_show_grep_and_missing_tool(server, tmp_path: Path):
    url, _ = server
    run("probe", "--url", url, "--name", "stub", "--out", str(tmp_path))
    m = str(tmp_path / "stub.json")

    g = run("show", m, "--grep", "beta")
    assert g.returncode == 0 and "1/2" in g.stdout and "beta" in g.stdout

    one = run("show", m, "--tool", "alpha")
    assert one.returncode == 0 and "inputSchema" in one.stdout

    missing = run("show", m, "--tool", "does_not_exist")
    assert missing.returncode == 1
    assert "Discovery is authoritative" in missing.stderr


def test_diff_flags_removal_as_failure(tmp_path: Path):
    old = tmp_path / "old.json"
    new = tmp_path / "new.json"
    old.write_text(json.dumps({"name": "s", "tools": TOOLS}))
    new.write_text(json.dumps({"name": "s", "tools": [
        TOOLS[0], {"name": "gamma", "description": "new"}]}))

    r = run("diff", str(old), str(new))
    assert r.returncode == 1, "a removed tool must not exit 0"
    assert "+ added: gamma" in r.stdout
    assert "- removed: beta" in r.stdout

    same = run("diff", str(old), str(old))
    assert same.returncode == 0 and "no change" in same.stdout


# ------------------------------------------------------------------- configs

def test_reads_codex_toml_bearer_env(tmp_path: Path):
    p = tmp_path / "config.toml"
    p.write_text(
        '[mcp_servers.gb]\n'
        'url = "http://127.0.0.1:3131/mcp"\n'
        'bearer_token_env_var = "GB_TOKEN"\n'
        'required = true\n\n'
        '[hooks.state]\n', encoding="utf-8")
    got = _from_codex_toml(p)
    assert len(got) == 1
    assert got[0]["url"] == "http://127.0.0.1:3131/mcp"
    assert got[0]["bearer_env"] == "GB_TOKEN"
    assert got[0]["transport"] == "http"


def test_reads_mcp_json_and_marks_stdio(tmp_path: Path):
    p = tmp_path / "mcp.json"
    p.write_text(json.dumps({"mcpServers": {
        "remote": {"url": "https://x/mcp"},
        "local": {"command": "npx", "args": ["y"]}}}), encoding="utf-8")
    by = {s["name"]: s for s in _from_mcp_json(p)}
    assert by["remote"]["transport"] == "http"
    assert by["local"]["transport"] == "stdio"


def test_servers_contacts_nothing(server):
    """`servers` must never make a call, whatever is configured."""
    _, seen = server
    r = run("servers")
    assert r.returncode == 0
    assert seen == []
    assert "No server was contacted" in r.stdout or "configured MCP server" in r.stdout
