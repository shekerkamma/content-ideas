"""Claude Code CLI provider client.

``claude-code-cli`` drives the locally installed Claude Code CLI as an external
subprocess instead of calling ``api.anthropic.com`` directly.  That distinction
is the entire point of the provider:

* The ``anthropic`` provider sends a Claude subscription OAuth token to the
  public Messages API.  Anthropic bills that traffic to the *extra usage*
  (pay-as-you-go) bucket, so it fails with ``HTTP 400: You're out of extra
  usage`` on a plan that has no overage balance.
* This provider shells out to ``claude -p``.  The CLI performs its own
  subscription auth, so the request is billed against the plan's included
  quota — no API credits, no extra-usage balance required.

Structurally this mirrors ``agent/copilot_acp_client.py``: a minimal
OpenAI-client-compatible facade exposing ``client.chat.completions.create``.
Hermes keeps ownership of tool execution — the CLI runs with ``--tools ""`` so
it never acts on its own; tool calls come back as ``<tool_call>{...}</tool_call>``
text blocks which are parsed into OpenAI-shaped tool calls.

The prompt is written to the child's **stdin**, never argv: Hermes system
prompts routinely exceed the 32767-character Windows command-line limit.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import threading
from pathlib import Path
from types import SimpleNamespace
from typing import Any

logger = logging.getLogger(__name__)

# Marker base_url — identifies the provider without being a reachable endpoint.
CLI_MARKER_BASE_URL = "cli://claude-code"

_DEFAULT_TIMEOUT_SECONDS = 900.0

# Reuse the transport-agnostic helpers already proven by the copilot-acp
# provider rather than duplicating ~150 lines of tool-call parsing.
try:  # pragma: no cover - import shape varies across Hermes versions
    from agent.copilot_acp_client import (
        _completion_to_stream_chunks,
        _extract_tool_calls_from_text,
        _render_message_content,
    )
except ImportError:  # pragma: no cover
    _completion_to_stream_chunks = None  # type: ignore[assignment]
    _extract_tool_calls_from_text = None  # type: ignore[assignment]
    _render_message_content = None  # type: ignore[assignment]


def _resolve_command() -> str:
    """Locate the Claude Code CLI binary."""
    candidate = (
        os.getenv("HERMES_CLAUDE_CLI_COMMAND", "").strip()
        or os.getenv("CLAUDE_CLI_PATH", "").strip()
        or "claude"
    )
    return shutil.which(candidate) or candidate


def _resolve_args() -> list[str]:
    """Default argv for a non-interactive, tool-free, single-shot run.

    ``--tools ""``            Hermes owns tool execution; the CLI must not act.
    ``--safe-mode``           Ignore CLAUDE.md, skills, plugins, hooks and MCP
                              servers so the user's local setup cannot leak into
                              Hermes turns.  Auth still resolves normally, which
                              is what keeps this on the subscription.
    ``--no-session-persistence``  Don't write Hermes turns into the user's own
                              Claude Code session history.
    ``--strict-mcp-config``   Belt-and-braces against ambient MCP servers.

    Deliberately NOT used: ``--bare``, which forces ANTHROPIC_API_KEY/apiKeyHelper
    auth and never reads OAuth — the exact API-credit path this provider exists
    to avoid.
    """
    import shlex

    raw = os.getenv("HERMES_CLAUDE_CLI_ARGS", "").strip()
    if raw:
        return shlex.split(raw)
    return [
        "-p",
        "--output-format", "json",
        "--tools", "",
        "--safe-mode",
        "--no-session-persistence",
        "--strict-mcp-config",
    ]


def _resolve_cwd(explicit: str | None = None) -> str:
    override = os.getenv("HERMES_CLAUDE_CLI_CWD", "").strip()
    target = explicit or override or os.getcwd()
    try:
        return str(Path(target).resolve())
    except Exception:
        return os.getcwd()


def _build_subprocess_env() -> dict[str, str]:
    """Environment for the child CLI.

    Strips ``ANTHROPIC_API_KEY`` / ``ANTHROPIC_AUTH_TOKEN``: if either is set,
    Claude Code authenticates as an API-key user and bills API credits, which
    defeats the purpose of this provider.  ``CLAUDE_CODE_OAUTH_TOKEN`` is
    deliberately preserved — a setup-token is a subscription credential.

    Nested-session markers are cleared so a Hermes process that itself runs
    inside Claude Code doesn't confuse the child.
    """
    env = dict(os.environ)
    for key in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"):
        env.pop(key, None)
    for key in (
        "CLAUDECODE",
        "CLAUDE_CODE_ENTRYPOINT",
        "CLAUDE_CODE_SESSION_ID",
        "CLAUDE_CODE_CHILD_SESSION",
        "CLAUDE_CODE_SSE_PORT",
    ):
        env.pop(key, None)
    return env


def _strip_provider_prefix(model: str | None) -> str:
    """``claude-code-cli/claude-sonnet-4-6`` -> ``claude-sonnet-4-6``."""
    text = str(model or "").strip()
    if not text:
        return ""
    for prefix in ("claude-code-cli/", "claude-code/", "anthropic/"):
        if text.startswith(prefix):
            return text[len(prefix):]
    return text


def _fallback_render_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                text = block.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(p for p in parts if p)
    if content is None:
        return ""
    return str(content)


def _format_messages_as_prompt(
    messages: list[dict[str, Any]],
    model: str | None = None,
    tools: list[dict[str, Any]] | None = None,
    tool_choice: Any = None,
) -> str:
    """Flatten an OpenAI-shaped message list into a single Claude Code prompt.

    System messages are folded into the transcript rather than passed via
    ``--system-prompt`` so the payload travels on stdin and stays clear of the
    Windows argv length limit.
    """
    render = _render_message_content or _fallback_render_content

    sections: list[str] = [
        "You are the model backend for Hermes, an external agent runtime.",
        "Answer the conversation below. Hermes executes all tools — you must not "
        "attempt to act on the system yourself.",
        "IMPORTANT: To call a tool, output one or more <tool_call>{...}</tool_call> "
        "blocks containing JSON in OpenAI function-call shape "
        "(id/type/function{name,arguments}); arguments must be a JSON string. "
        "If no tool is needed, answer normally.",
    ]

    if isinstance(tools, list) and tools:
        tool_specs: list[dict[str, Any]] = []
        for t in tools:
            if not isinstance(t, dict):
                continue
            fn = t.get("function") or {}
            if not isinstance(fn, dict):
                continue
            name = fn.get("name")
            if not isinstance(name, str) or not name.strip():
                continue
            tool_specs.append(
                {
                    "name": name.strip(),
                    "description": fn.get("description", ""),
                    "parameters": fn.get("parameters", {}),
                }
            )
        if tool_specs:
            sections.append(
                "Available tools (OpenAI function schema). When using a tool, emit "
                "ONLY <tool_call>{...}</tool_call> blocks.\n"
                + json.dumps(tool_specs, ensure_ascii=False)
            )

    if tool_choice is not None:
        sections.append(
            f"Tool choice hint: {json.dumps(tool_choice, ensure_ascii=False)}"
        )

    transcript: list[str] = []
    for message in messages or []:
        if not isinstance(message, dict):
            continue
        role = str(message.get("role") or "unknown").strip().lower()
        if role not in {"system", "user", "assistant", "tool"}:
            role = "context"
        rendered = render(message.get("content"))
        if not rendered:
            continue
        label = {
            "system": "System",
            "user": "User",
            "assistant": "Assistant",
            "tool": "Tool",
            "context": "Context",
        }.get(role, role.title())
        transcript.append(f"{label}:\n{rendered}")

    if transcript:
        sections.append("Conversation transcript:\n\n" + "\n\n".join(transcript))

    sections.append("Continue the conversation from the latest user request.")
    return "\n\n".join(s.strip() for s in sections if s and s.strip())


def _parse_cli_result(stdout_text: str) -> tuple[str, str]:
    """Extract ``(result_text, error_text)`` from ``--output-format json`` output.

    The CLI prints a single JSON object; tolerate leading noise by scanning for
    the last parseable line so a stray warning doesn't break the run.
    """
    text = (stdout_text or "").strip()
    if not text:
        return "", "Claude Code CLI produced no output"

    payload: dict[str, Any] | None = None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        for line in reversed(text.splitlines()):
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                payload = json.loads(line)
                break
            except json.JSONDecodeError:
                continue

    if not isinstance(payload, dict):
        # Not JSON at all — treat the raw text as the answer (``--output-format
        # text`` via HERMES_CLAUDE_CLI_ARGS lands here).
        return text, ""

    if payload.get("is_error"):
        detail = (
            payload.get("result")
            or payload.get("api_error_status")
            or payload.get("subtype")
            or "unknown error"
        )
        return "", f"Claude Code CLI reported an error: {detail}"

    result = payload.get("result")
    if isinstance(result, str):
        return result, ""
    if result is not None:
        return json.dumps(result, ensure_ascii=False), ""
    return "", "Claude Code CLI returned no 'result' field"


class _CLIChatCompletions:
    def __init__(self, client: "ClaudeCodeCLIClient"):
        self._client = client

    def create(self, **kwargs: Any) -> Any:
        return self._client._create_chat_completion(**kwargs)


class _CLIChatNamespace:
    def __init__(self, client: "ClaudeCodeCLIClient"):
        self.completions = _CLIChatCompletions(client)


class ClaudeCodeCLIClient:
    """Minimal OpenAI-client-compatible facade over the Claude Code CLI."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        default_headers: dict[str, str] | None = None,
        command: str | None = None,
        args: list[str] | None = None,
        cwd: str | None = None,
        **_: Any,
    ):
        self.api_key = api_key or "claude-code-cli"
        self.base_url = base_url or CLI_MARKER_BASE_URL
        self._default_headers = dict(default_headers or {})
        self._command = command or _resolve_command()
        self._args = list(args or _resolve_args())
        self._cwd = _resolve_cwd(cwd)
        self.chat = _CLIChatNamespace(self)
        self.is_closed = False
        self._active_process: subprocess.Popen[str] | None = None
        self._active_process_lock = threading.Lock()

    def close(self) -> None:
        with self._active_process_lock:
            proc = self._active_process
            self._active_process = None
        self.is_closed = True
        if proc is None:
            return
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass

    @staticmethod
    def _normalize_timeout(timeout: Any) -> float:
        if timeout is None:
            return _DEFAULT_TIMEOUT_SECONDS
        if isinstance(timeout, (int, float)):
            return float(timeout)
        candidates = [
            getattr(timeout, attr, None)
            for attr in ("read", "write", "connect", "pool", "timeout")
        ]
        numeric = [float(v) for v in candidates if isinstance(v, (int, float))]
        return max(numeric) if numeric else _DEFAULT_TIMEOUT_SECONDS

    def _create_chat_completion(
        self,
        *,
        model: str | None = None,
        messages: list[dict[str, Any]] | None = None,
        timeout: float | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: Any = None,
        stream: bool = False,
        **_: Any,
    ) -> Any:
        resolved_model = _strip_provider_prefix(model)
        prompt_text = _format_messages_as_prompt(
            messages or [],
            model=resolved_model,
            tools=tools,
            tool_choice=tool_choice,
        )
        response_text = self._run_prompt(
            prompt_text,
            model=resolved_model,
            timeout_seconds=self._normalize_timeout(timeout),
        )

        if _extract_tool_calls_from_text is not None:
            tool_calls, cleaned_text = _extract_tool_calls_from_text(response_text)
        else:  # pragma: no cover - only when the copilot module is absent
            tool_calls, cleaned_text = [], response_text

        usage = SimpleNamespace(
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
            prompt_tokens_details=SimpleNamespace(cached_tokens=0),
        )
        assistant_message = SimpleNamespace(
            content=cleaned_text,
            tool_calls=tool_calls,
            reasoning=None,
            reasoning_content=None,
            reasoning_details=None,
        )
        choice = SimpleNamespace(
            message=assistant_message,
            finish_reason="tool_calls" if tool_calls else "stop",
        )
        completion = SimpleNamespace(
            choices=[choice],
            usage=usage,
            model=resolved_model or "claude-code-cli",
        )
        if stream:
            if _completion_to_stream_chunks is None:  # pragma: no cover
                raise RuntimeError(
                    "streaming requires agent.copilot_acp_client helpers"
                )
            return _completion_to_stream_chunks(completion)
        return completion

    def _build_argv(self, model: str) -> list[str]:
        argv = [self._command, *self._args]
        if model and "--model" not in argv:
            argv += ["--model", model]
        return argv

    def _run_prompt(
        self,
        prompt_text: str,
        *,
        model: str,
        timeout_seconds: float,
    ) -> str:
        if not shutil.which(self._command) and not Path(self._command).exists():
            raise RuntimeError(
                f"Could not find the Claude Code CLI command '{self._command}'. "
                "Install it with `npm install -g @anthropic-ai/claude-code`, or set "
                "HERMES_CLAUDE_CLI_COMMAND / CLAUDE_CLI_PATH."
            )

        argv = self._build_argv(model)
        popen_kwargs: dict[str, Any] = {}
        try:
            # Hide the console window the CLI child would flash on Windows.
            from hermes_cli._subprocess_compat import windows_hide_flags

            popen_kwargs.update(windows_hide_flags())
        except Exception:
            pass

        logger.debug("claude-code-cli: spawning %s (cwd=%s)", argv, self._cwd)
        try:
            proc = subprocess.Popen(
                argv,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                cwd=self._cwd,
                env=_build_subprocess_env(),
                **popen_kwargs,
            )
        except FileNotFoundError as exc:
            raise RuntimeError(
                f"Could not launch the Claude Code CLI ('{self._command}'): {exc}"
            ) from exc

        with self._active_process_lock:
            self._active_process = proc

        try:
            stdout_text, stderr_text = proc.communicate(
                input=prompt_text, timeout=timeout_seconds
            )
        except subprocess.TimeoutExpired:
            proc.kill()
            try:
                proc.communicate(timeout=5)
            except Exception:
                pass
            raise RuntimeError(
                f"Claude Code CLI timed out after {timeout_seconds:.0f}s"
            )
        finally:
            with self._active_process_lock:
                self._active_process = None

        result_text, error_text = _parse_cli_result(stdout_text)
        if error_text:
            detail = (stderr_text or "").strip()
            suffix = f" (stderr: {detail[:400]})" if detail else ""
            raise RuntimeError(f"{error_text}{suffix}")
        if proc.returncode not in (0, None) and not result_text:
            detail = (stderr_text or "").strip()
            raise RuntimeError(
                f"Claude Code CLI exited with code {proc.returncode}"
                + (f": {detail[:400]}" if detail else "")
            )
        return result_text
