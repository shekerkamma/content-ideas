#!/usr/bin/env python3
"""OpenAI-compatible HTTP shim over the Claude Code CLI.

Reproduces the pattern Hermes records as:
    providers.claude-code-cli = {auth_type: external_process,
                                 base_url: "cli://claude-code"}

Hermes stores no Claude credential — it spawns the `claude` binary and lets the
CLI authenticate itself against the user's own subscription. dsh cannot do that
directly: its LLM adapter speaks HTTP to a key+endpoint and has no `cli://`
transport. This server is the missing adapter — HTTP in, subprocess out.

    POST /v1/chat/completions   (stream=true -> SSE, else JSON)
    GET  /v1/models

KNOWN LIMITATION — read before relying on this for agent work:
`claude -p` is a complete agent, not a raw model. It performs its own tool use
internally and returns final prose; it never emits OpenAI `tool_calls`. So when
dsh drives this route, dsh's own bash/fs/todo tools, permission prompts,
sandbox policy, and trajectory log are bypassed — you get Claude Code nested
inside dsh rather than Claude acting as dsh's model. Fine for text generation
and for tasks Claude Code can complete alone; not equivalent to a real
tool-calling model.

Each request also re-sends Claude Code's own system prompt, so token usage per
call is far higher than a bare model call and subscription rate limits arrive
sooner.

Usage:
    python3 claude_code_bridge.py [--port 8318] [--host 127.0.0.1]
Env:
    CLAUDE_BRIDGE_TOKEN   required bearer token (default: local-claude-bridge)
    CLAUDE_BRIDGE_CWD     working directory for spawned claude (default: $HOME)
    CLAUDE_BRIDGE_TIMEOUT seconds per request (default: 600)
"""
import argparse
import json
import os
import subprocess
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOKEN = os.environ.get("CLAUDE_BRIDGE_TOKEN", "local-claude-bridge")
WORKDIR = os.environ.get("CLAUDE_BRIDGE_CWD", os.path.expanduser("~"))
TIMEOUT = int(os.environ.get("CLAUDE_BRIDGE_TIMEOUT", "600"))

MODELS = ["claude-code-opus", "claude-code-sonnet", "claude-code-haiku", "claude-code-default"]
# Bridge model id -> value for `claude --model`. "default" means omit the flag
# and let the CLI use whatever the user's session is configured for.
MODEL_MAP = {
    "claude-code-opus": "opus",
    "claude-code-sonnet": "sonnet",
    "claude-code-haiku": "haiku",
    "claude-code-default": None,
}


def flatten(messages):
    """Collapse an OpenAI message array into one prompt string.

    Claude Code takes a single prompt, so multi-turn context is rendered as
    labelled blocks. System messages lead, preserving their priority.
    """
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


def run_claude(prompt, model_id):
    """Spawn the CLI. Returns (text, error_or_None)."""
    cmd = ["claude", "-p", "--output-format", "json"]
    mapped = MODEL_MAP.get(model_id, None)
    if mapped:
        cmd += ["--model", mapped]
    try:
        proc = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            cwd=WORKDIR,
        )
    except subprocess.TimeoutExpired:
        return None, f"claude CLI timed out after {TIMEOUT}s"
    except FileNotFoundError:
        return None, "claude CLI not found on PATH"
    if proc.returncode != 0:
        return None, (proc.stderr or "claude CLI failed").strip()[:500]
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        # Non-JSON stdout still carries usable text in plain print mode.
        return proc.stdout.strip(), None
    if data.get("is_error"):
        return None, str(data.get("result") or data.get("api_error_status"))[:500]
    return data.get("result", ""), None


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
                    {"id": m, "object": "model", "created": now, "owned_by": "claude-code-cli"}
                    for m in MODELS
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

        model = req.get("model", "claude-code-default")
        prompt = flatten(req.get("messages"))
        if not prompt:
            return self._send(400, {"error": {"message": "no message content"}})

        text, err = run_claude(prompt, model)
        if err:
            return self._send(502, {"error": {"message": err, "type": "upstream_error"}})

        cid = "chatcmpl-claudecode-" + uuid.uuid4().hex[:12]
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
    ap.add_argument("--port", type=int, default=8318)
    args = ap.parse_args()
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"claude-code bridge on http://{args.host}:{args.port}/v1  (cwd={WORKDIR})", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
