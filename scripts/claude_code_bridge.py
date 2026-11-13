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
    CLAUDE_BRIDGE_PERMISSION_MODE  --permission-mode for the spawned CLI
                          (default: acceptEdits)
    CLAUDE_BRIDGE_LEAN_CWD  empty folder used by the lean (default) models
                          (default: ~/.dsh/bridges/work)
    CLAUDE_BRIDGE_RETRIES extra tries for transient failures (default: 1)

LEAN MODE (default since 2026-11-13). Every model except `claude-code-agent`
runs `claude -p` as a plain model: no MCP servers (--strict-mcp-config), no
user/project/local settings, hooks, plugins or mods (--setting-sources ""),
no skill list (--disable-slash-commands), no tools of its own (--tools ""),
no session file, in an empty folder. A PONG went from 62-184 s to ~3.5 s.
`--bare` is deliberately NOT used: it ignores the subscription OAuth login and
only accepts ANTHROPIC_API_KEY (billed). `claude-code-agent` keeps the old
full-session behaviour (tools, MCP, hooks) in CLAUDE_BRIDGE_CWD.
Calls are serialized (one claude process at a time) so dsh's parallel title
call cannot double the load, and a subscription usage limit is returned as
HTTP 429 with the CLI's reset message instead of a generic 502.

CLAUDE_BRIDGE_CWD IS THE SANDBOX ROOT the nested agent sees. `claude -p` can
only read and write beneath its own cwd, so pointing this at a throwaway temp
directory makes every path outside it look "blocked by policy" to whatever is
driving the bridge — which reads like a dsh sandbox setting and is not one.
Point it at the repository the agent is meant to work in.

CLAUDE_BRIDGE_PERMISSION_MODE matters just as much. `claude -p` has no TTY, so
anything that would raise an approval prompt is auto-rejected with no prompt
for a human to answer. Without an explicit mode the nested agent reports tools
as "not granted" and confirmation dialogs as unanswerable. Modes: `default`
(prompt-driven; auto-rejects here), `acceptEdits` (file edits proceed, other
gated tools still auto-reject), `bypassPermissions` (nothing is gated — only
for a bridge you trust every local caller of, since the default bearer token
is a well-known string).
"""
import argparse
import json
import os
import subprocess
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOKEN = os.environ.get("CLAUDE_BRIDGE_TOKEN", "local-claude-bridge")
WORKDIR = os.environ.get("CLAUDE_BRIDGE_CWD", os.path.expanduser("~"))
TIMEOUT = int(os.environ.get("CLAUDE_BRIDGE_TIMEOUT", "180"))
LEAN_CWD = os.environ.get("CLAUDE_BRIDGE_LEAN_CWD", os.path.expanduser("~/.dsh/bridges/work"))
LEAN_FLAGS = ["--strict-mcp-config", "--setting-sources", "", "--disable-slash-commands",
              "--tools", "", "--no-session-persistence"]
AGENT_MODELS = {"claude-code-agent"}
RATE_LIMIT_MARKERS = ("hit your", "usage limit", "rate limit", "rate_limit")
_ONE_AT_A_TIME = threading.Semaphore(1)
PERMISSION_MODE = os.environ.get("CLAUDE_BRIDGE_PERMISSION_MODE", "acceptEdits")

MODELS = ["claude-code-opus", "claude-code-sonnet", "claude-code-haiku", "claude-code-default",
          "claude-code-agent"]
# Bridge model id -> value for `claude --model`. "default" means omit the flag
# and let the CLI use whatever the user's session is configured for.
MODEL_MAP = {
    "claude-code-opus": "opus",
    "claude-code-sonnet": "sonnet",
    "claude-code-haiku": "haiku",
    "claude-code-default": None,
    "claude-code-agent": None,   # full Claude Code session (tools, MCP, hooks)
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
    agent = model_id in AGENT_MODELS
    workdir = WORKDIR if agent else LEAN_CWD
    if agent:
        if PERMISSION_MODE:
            cmd += ["--permission-mode", PERMISSION_MODE]
    else:
        os.makedirs(LEAN_CWD, exist_ok=True)
        cmd += LEAN_FLAGS
    # A missing cwd raises the same FileNotFoundError as a missing binary, so
    # check it first — otherwise a deleted working directory is reported as
    # "claude CLI not found on PATH", which sends debugging at the wrong thing.
    if not os.path.isdir(workdir):
        return None, (
            f"bridge working directory does not exist: {workdir}. The claude binary is "
            f"probably fine — this is the bridge's working directory."
        )
    try:
        proc = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            cwd=workdir,
        )
    except subprocess.TimeoutExpired:
        return None, f"claude CLI timed out after {TIMEOUT}s"
    except FileNotFoundError:
        return None, "claude CLI not found on PATH"

    # Claude Code reports WHY it failed on stdout as JSON and leaves stderr
    # empty, so a non-zero exit must still parse stdout. Returning stderr here
    # collapsed rate limits, aborted streams and bad flags into one opaque
    # "claude CLI failed".
    text, detail = None, None
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        data = None
        # Non-JSON stdout still carries usable text in plain print mode.
        text = proc.stdout.strip() or None
    else:
        if data.get("is_error"):
            detail = str(
                data.get("result")
                or data.get("api_error_status")
                or data.get("subtype")
                or (data.get("errors") or [None])[0]
                or ""
            ).strip() or None
            reason = data.get("terminal_reason")
            if reason:
                detail = f"{detail} (terminal_reason={reason})" if detail else f"terminal_reason={reason}"
        else:
            text = data.get("result", "")

    if proc.returncode != 0 or detail:
        why = detail or (proc.stderr or "").strip() or "no detail on stdout or stderr"
        return None, f"claude CLI failed (exit {proc.returncode}): {why}"[:500]
    return text if text is not None else "", None


# `claude -p` sometimes exits 1 with "No messages returned from query" for a
# prompt that succeeds on the next try (seen under load). Retry those; log
# every failure so intermittent ones can be diagnosed afterwards.
TRANSIENT_ERRORS = ("No messages returned from query",)
RETRIES = int(os.environ.get("CLAUDE_BRIDGE_RETRIES", "1"))
FAIL_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "claude_bridge_failures.log")


def _log_failure(model_id, prompt, err, attempt):
    try:
        with open(FAIL_LOG, "a") as fh:
            tail = prompt[-300:].replace("\n", "\\n")
            fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} model={model_id} attempt={attempt} "
                     f"prompt_chars={len(prompt)} err={err!r} prompt_tail={tail!r}\n")
    except OSError:
        pass


def run_claude_retrying(prompt, model_id):
    for attempt in range(1, RETRIES + 2):
        with _ONE_AT_A_TIME:
            text, err = run_claude(prompt, model_id)
        if not err:
            return text, None
        _log_failure(model_id, prompt, err, attempt)
        if not any(t in err for t in TRANSIENT_ERRORS):
            break
        time.sleep(2)
    return text, err


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

        text, err = run_claude_retrying(prompt, model)
        if err:
            if any(m in err.lower() for m in RATE_LIMIT_MARKERS):
                return self._send(429, {"error": {"message": err, "type": "rate_limit_error",
                                                  "code": "rate_limit_exceeded"}})
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
    print(
        f"claude-code bridge on http://{args.host}:{args.port}/v1\n"
        f"  cwd             = {WORKDIR}"
        f"{'' if os.path.isdir(WORKDIR) else '   *** DOES NOT EXIST ***'}\n"
        f"  lean cwd        = {LEAN_CWD} (all models except claude-code-agent)\n"
        f"  timeout         = {TIMEOUT}s, retries = {RETRIES}, one call at a time\n"
        f"  permission-mode = {PERMISSION_MODE or '(cli default — gated tools auto-reject)'}",
        flush=True,
    )
    srv.serve_forever()


if __name__ == "__main__":
    main()
