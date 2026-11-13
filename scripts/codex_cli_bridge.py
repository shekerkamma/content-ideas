#!/usr/bin/env python3
"""OpenAI-compatible HTTP shim over an authenticated Codex CLI."""

import argparse
import queue
import signal
import tempfile
import threading
import json
import os
import subprocess
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


TOKEN = os.environ.get("CODEX_BRIDGE_TOKEN", "local-codex-bridge")
WORKDIR = os.environ.get("CODEX_BRIDGE_CWD", os.path.expanduser("~"))
TIMEOUT = int(os.environ.get("CODEX_BRIDGE_TIMEOUT", "900"))

# Only models the signed-in ChatGPT account can actually route. gpt-5.5,
# gpt-5.4, and gpt-5.4-mini were listed here but return
# "not supported when using Codex with a ChatGPT account" (model_not_found).
MODEL_MAP = {
    "codex-cli-default": None,
    "codex-cli-gpt-6.1-sol": "gpt-6.1-sol",
    "codex-cli-gpt-6.1-terra": "gpt-6.1-terra",
    "codex-cli-gpt-6-sol": "gpt-6-sol",
    "codex-cli-gpt-6-astra": "gpt-6-astra",
    "codex-cli-gpt-6-luna": "gpt-6-luna",
    "codex-cli-gpt-5.6-sol": "gpt-5.6-sol",
    "codex-cli-gpt-5.6-terra": "gpt-5.6-terra",
    "codex-cli-gpt-5.6-luna": "gpt-5.6-luna",
}


def flatten(messages):
    parts = []
    for message in messages or []:
        role = message.get("role", "user")
        content = message.get("content", "")
        if isinstance(content, list):
            content = "".join(
                part.get("text", "")
                for part in content
                if isinstance(part, dict) and part.get("type") == "text"
            )
        if content:
            parts.append(f"{role.title()}: {content}")
    return "\n\n".join(parts).strip()


def run_codex(prompt, model_id, emit=None):
    if model_id not in MODEL_MAP:
        return None, f"unknown Codex bridge model: {model_id}"
    if not os.path.isdir(WORKDIR):
        return None, f"CODEX_BRIDGE_CWD does not exist: {WORKDIR}"

    cmd = [
        "codex", "exec", "--json", "--ephemeral", "--skip-git-repo-check",
        # Plain-model use: read-only sandbox in an empty folder (CODEX_BRIDGE_CWD,
        # ~/.dsh/bridges/work since 2026-11-13), not full access to the repo.
        "-s", "read-only", "-C", WORKDIR,
    ]
    model = MODEL_MAP[model_id]
    if model:
        cmd += ["--model", model]
    # Harness can send a multi-megabyte system/tool context. Passing that as
    # argv exceeds Linux ARG_MAX and drops the HTTP connection. `codex exec -`
    # reads the prompt from stdin and has no such command-line size limit.
    cmd.append("-")

    text = None
    errors = []
    events = queue.Queue()
    proc = None
    try:
        # A file avoids blocking on a full stderr pipe. The writer thread also
        # prevents a large incoming conversation from delaying HTTP heartbeats.
        with tempfile.TemporaryFile(mode="w+t") as stderr:
            proc = subprocess.Popen(
                cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=stderr,
                text=True, cwd=WORKDIR, start_new_session=True,
            )
            def feed():
                try:
                    proc.stdin.write(prompt)
                    proc.stdin.close()
                except (BrokenPipeError, OSError):
                    pass
            def read_events():
                try:
                    for line in proc.stdout:
                        events.put(line)
                finally:
                    events.put(None)
            threading.Thread(target=feed, daemon=True).start()
            threading.Thread(target=read_events, daemon=True).start()
            deadline = time.monotonic() + TIMEOUT
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    return None, f"codex CLI timed out after {TIMEOUT}s"
                try:
                    line = events.get(timeout=min(5, remaining))
                except queue.Empty:
                    if emit:
                        emit(None)
                    continue
                if line is None:
                    break
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                item = event.get("item", {})
                if event.get("type") == "item.completed" and item.get("type") == "agent_message":
                    text = item.get("text", "")
                    if emit and text:
                        emit(text)
                elif event.get("type") in {"error", "turn.failed"}:
                    errors.append(str(event.get("message") or event.get("error") or event))
            proc.wait(timeout=max(0.01, deadline - time.monotonic()))
            stderr.seek(0)
            stderr_text = stderr.read()
    except subprocess.TimeoutExpired:
        return None, f"codex CLI timed out after {TIMEOUT}s"
    except FileNotFoundError:
        return None, "codex CLI not found on PATH"
    except (BrokenPipeError, ConnectionResetError):
        raise
    except OSError as exc:
        return None, f"could not start codex CLI: {exc}"
    finally:
        if proc is not None:
            if proc.poll() is None:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            proc.wait()

    if proc.returncode != 0 or text is None:
        detail = "; ".join(errors) or stderr_text.strip() or "no final agent message"
        return None, f"codex CLI failed (exit {proc.returncode}): {detail}"[:1000]
    return text, None


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass

    def send_json(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def authorized(self):
        return self.headers.get("Authorization", "").removeprefix("Bearer ").strip() == TOKEN

    def do_GET(self):
        if not self.authorized():
            return self.send_json(401, {"error": {"message": "unauthorized"}})
        if self.path.rstrip("/").endswith("/models"):
            now = int(time.time())
            return self.send_json(200, {
                "object": "list",
                "data": [
                    {"id": model, "object": "model", "created": now, "owned_by": "codex-cli"}
                    for model in MODEL_MAP
                ],
            })
        self.send_json(404, {"error": {"message": "not found"}})

    def do_POST(self):
        if not self.authorized():
            return self.send_json(401, {"error": {"message": "unauthorized"}})
        if "chat/completions" not in self.path:
            return self.send_json(404, {"error": {"message": "not found"}})
        try:
            raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            request = json.loads(raw or b"{}")
        except (ValueError, TypeError):
            return self.send_json(400, {"error": {"message": "invalid JSON body"}})

        model = request.get("model", "codex-cli-default")
        prompt = flatten(request.get("messages"))
        if not prompt:
            return self.send_json(400, {"error": {"message": "no message content"}})
        if model not in MODEL_MAP:
            return self.send_json(400, {"error": {"message": "unknown Codex bridge model"}})
        completion_id = "chatcmpl-codexcli-" + uuid.uuid4().hex[:12]
        created = int(time.time())
        if request.get("stream"):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "close")
            self.end_headers()
            self.close_connection = True
            def chunk(delta, finish=None):
                payload = {
                    "id": completion_id, "object": "chat.completion.chunk",
                    "created": created, "model": model,
                    "choices": [{"index": 0, "delta": delta, "finish_reason": finish}],
                }
                self.wfile.write(b"data: " + json.dumps(payload).encode() + b"\n\n")
                self.wfile.flush()
            sent = False
            def emit(content):
                nonlocal sent
                if content is None:
                    self.wfile.write(b": keep-alive\n\n")
                    self.wfile.flush()
                else:
                    chunk({"content": ("\n\n" if sent else "") + content})
                    sent = True
            try:
                chunk({"role": "assistant", "content": ""})
                _, error = run_codex(prompt, model, emit)
                if error:
                    self.wfile.write(b"data: " + json.dumps({"error": {
                        "message": error, "type": "upstream_error"
                    }}).encode() + b"\n\n")
                else:
                    chunk({}, "stop")
                self.wfile.write(b"data: [DONE]\n\n")
                self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass
            return

        text, error = run_codex(prompt, model)
        if error:
            return self.send_json(502, {"error": {"message": error, "type": "upstream_error"}})
        self.send_json(200, {
            "id": completion_id, "object": "chat.completion", "created": created,
            "model": model,
            "choices": [{"index": 0, "message": {"role": "assistant", "content": text},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8319)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(
        f"codex-cli bridge on http://{args.host}:{args.port}/v1\n"
        f"  cwd = {WORKDIR}{'' if os.path.isdir(WORKDIR) else ' *** DOES NOT EXIST ***'}",
        flush=True,
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
