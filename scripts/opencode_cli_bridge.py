#!/usr/bin/env python3
"""OpenAI-compatible HTTP shim over the OpenCode CLI.

OpenCode Zen's free models (deepseek-v4.1-flash-free and friends) refuse every
direct API call with `FreeTierError: OpenCode's free tier can only be used from
within OpenCode`. So instead of calling Zen, this bridge spawns the real
`opencode run` client per request — HTTP in, subprocess out, the same shape as
claude_code_bridge.py.

    POST /v1/chat/completions   (stream=true -> SSE, else JSON)
    GET  /v1/models

KNOWN LIMITATION — same as the Claude Code bridge: `opencode run` is a complete
agent, not a raw model. It does its own tool use and returns prose; it never
emits OpenAI `tool_calls`. Driving dsh through this route bypasses dsh's own
tools, permission prompts, sandbox policy and trajectory log. Each call also
re-sends OpenCode's system prompt (~76k input tokens cold on the free models).

Usage:
    python3 opencode_cli_bridge.py [--port 8320] [--host 127.0.0.1]
Env:
    OPENCODE_BRIDGE_TOKEN    required bearer token (default: local-opencode-bridge)
    OPENCODE_BRIDGE_CWD      working directory for spawned opencode (default: $HOME)
    OPENCODE_BRIDGE_TIMEOUT  seconds per request (default: 600)
    OPENCODE_BRIDGE_AUTO     "1" adds --auto (auto-approve permissions not
                             explicitly denied). Off by default: `opencode run`
                             has no TTY, so gated tools are rejected instead.

OPENCODE_BRIDGE_CWD is the project the nested agent sees — point it at the
repository the work is in, not a scratch directory.

If every request fails with "database disk image is malformed", the culprit is
~/.local/share/opencode/opencode.db, not this bridge or the model.
"""
import argparse
import json
import os
import re
import subprocess
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOKEN = os.environ.get("OPENCODE_BRIDGE_TOKEN", "local-opencode-bridge")
WORKDIR = os.environ.get("OPENCODE_BRIDGE_CWD", os.path.expanduser("~"))
TIMEOUT = int(os.environ.get("OPENCODE_BRIDGE_TIMEOUT", "600"))
AUTO = os.environ.get("OPENCODE_BRIDGE_AUTO", "") == "1"

# Bridge model id -> value for `opencode run -m`. Free Zen models listed at
# https://opencode.ai/zen/v1/models on 2026-10-18; only the first was smoke-tested.
MODEL_MAP = {
    "deepseek-v4.1-flash-free": "opencode/deepseek-v4.1-flash-free",
    "glm-5.3-flash-free": "opencode/glm-5.3-flash-free",
    "mimo-v2.6-flash-free": "opencode/mimo-v2.6-flash-free",
    "nemotron-3.5-super-vl-free": "opencode/nemotron-3.5-super-vl-free",
    "big-pickle": "opencode/big-pickle",
}
DEFAULT_MODEL = "deepseek-v4.1-flash-free"
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def flatten(messages):
    """Collapse an OpenAI message array into one prompt string."""
    system, turns = [], []
    for m in messages or []:
        role = m.get("role", "user")
        content = m.get("content", "")
        if isinstance(content, list):  # OpenAI content-parts form
            content = "".join(
                p.get("text", "") for p in content if isinstance(p, dict) and p.get("type") == "text"
            )
        if not content:
            continue
        if role == "system":
            system.append(content)
        elif role == "assistant":
            turns.append(f"Assistant: {content}")
        else:
            turns.append(f"User: {content}")
    parts = []
    if system:
        parts.append("\n\n".join(system))
    parts.extend(turns)
    return "\n\n".join(parts).strip()


def run_opencode(prompt, model_id):
    """Spawn the CLI. Returns (text, error_or_None)."""
    if model_id not in MODEL_MAP:
        return None, f"unknown OpenCode bridge model: {model_id}"
    # A missing cwd raises the same FileNotFoundError as a missing binary.
    if not os.path.isdir(WORKDIR):
        return None, f"OPENCODE_BRIDGE_CWD does not exist: {WORKDIR}"
    cmd = ["opencode", "run", "-m", MODEL_MAP[model_id], "--format", "json"]
    if AUTO:
        cmd.append("--auto")
    # The prompt goes in argv; stdin is DEVNULL so the CLI never blocks on it.
    cmd += ["--", prompt]
    # OpenCode git-snapshots the whole worktree before each run so it can undo
    # edits. On a 29 GB repo with a large untracked tree that never finishes —
    # a "Reply with pong" request sat past 200 s. Turn snapshots off for the
    # bridge only; the user's own opencode config is untouched.
    env = dict(os.environ)
    env.setdefault("OPENCODE_CONFIG_CONTENT", json.dumps({"snapshot": False}))
    env.setdefault("OPENCODE_DISABLE_AUTOUPDATE", "1")
    try:
        proc = subprocess.run(
            cmd,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            cwd=WORKDIR,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return None, f"opencode CLI timed out after {TIMEOUT}s"
    except FileNotFoundError:
        return None, "opencode CLI not found on PATH"

    texts, errors = [], []
    for line in proc.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "text":
            texts.append(event.get("part", {}).get("text", ""))
        elif event.get("type") == "error":
            err = event.get("error") or event.get("part") or event
            errors.append(json.dumps(err) if not isinstance(err, str) else err)

    if proc.returncode != 0 or (errors and not texts):
        why = "; ".join(errors) or ANSI.sub("", proc.stderr or "").strip() or "no detail"
        return None, f"opencode CLI failed (exit {proc.returncode}): {why}"[:500]
    return "\n\n".join(t for t in texts if t), None


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):  # keep the console quiet
        pass

    def _send(self, code, payload, ctype="application/json"):
        body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _authorized(self):
        got = self.headers.get("Authorization", "")
        return got.replace("Bearer ", "").strip() == TOKEN

    def do_GET(self):
        if not self._authorized():
            return self._send(401, {"error": {"message": "unauthorized"}})
        if self.path.rstrip("/").endswith("/models"):
            now = int(time.time())
            return self._send(200, {
                "object": "list",
                "data": [
                    {"id": m, "object": "model", "created": now, "owned_by": "opencode-cli"}
                    for m in MODEL_MAP
                ],
            })
        self._send(404, {"error": {"message": "not found"}})

    def do_POST(self):
        if not self._authorized():
            return self._send(401, {"error": {"message": "unauthorized"}})
        if "chat/completions" not in self.path:
            return self._send(404, {"error": {"message": "not found"}})

        try:
            raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            req = json.loads(raw or b"{}")
        except (ValueError, TypeError):
            return self._send(400, {"error": {"message": "invalid JSON body"}})

        model = req.get("model", DEFAULT_MODEL)
        prompt = flatten(req.get("messages"))
        if not prompt:
            return self._send(400, {"error": {"message": "no message content"}})

        text, err = run_opencode(prompt, model)
        if err:
            return self._send(502, {"error": {"message": err, "type": "upstream_error"}})

        cid = "chatcmpl-opencode-" + uuid.uuid4().hex[:12]
        created = int(time.time())
        if req.get("stream"):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "close")
            self.end_headers()

            def chunk(delta, finish=None):
                payload = {
                    "id": cid, "object": "chat.completion.chunk", "created": created,
                    "model": model,
                    "choices": [{"index": 0, "delta": delta, "finish_reason": finish}],
                }
                self.wfile.write(b"data: " + json.dumps(payload).encode() + b"\n\n")
                self.wfile.flush()

            chunk({"role": "assistant", "content": ""})
            chunk({"content": text})
            chunk({}, finish="stop")
            self.wfile.write(b"data: [DONE]\n\n")
            self.wfile.flush()
            self.close_connection = True
            return

        self._send(200, {
            "id": cid, "object": "chat.completion", "created": created, "model": model,
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": text},
                "finish_reason": "stop",
            }],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8320)
    args = ap.parse_args()
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(
        f"opencode bridge on http://{args.host}:{args.port}/v1\n"
        f"  cwd  = {WORKDIR}{'' if os.path.isdir(WORKDIR) else '   *** DOES NOT EXIST ***'}\n"
        f"  auto = {AUTO}",
        flush=True,
    )
    srv.serve_forever()


if __name__ == "__main__":
    main()
