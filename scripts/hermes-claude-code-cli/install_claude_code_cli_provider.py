#!/usr/bin/env python3
"""Install the `claude-code-cli` provider into a hermes-agent tree.

Idempotent: every edit is guarded by a marker check, so re-running after a
Hermes upgrade re-applies only what the upgrade removed.

Usage:  python3 install_claude_code_cli_provider.py <hermes-agent-dir> [--dry-run]
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

CLIENT_SRC = Path(__file__).with_name("claude_code_cli_client.py")

DRY = "--dry-run" in sys.argv
ROOT = Path([a for a in sys.argv[1:] if not a.startswith("--")][0]).resolve()

changes: list[str] = []
skipped: list[str] = []


def patch(rel: str, anchor: str, insert: str, marker: str, *, before: bool = False) -> None:
    """Insert `insert` relative to `anchor` in `rel`, unless `marker` is present."""
    path = ROOT / rel
    if not path.exists():
        skipped.append(f"{rel}: FILE MISSING")
        return
    text = path.read_text(encoding="utf-8")
    if marker in text:
        skipped.append(f"{rel}: already patched ({marker[:40]}...)")
        return
    if anchor not in text:
        skipped.append(f"{rel}: ANCHOR NOT FOUND -- {anchor[:60]!r}")
        return
    if text.count(anchor) != 1:
        skipped.append(f"{rel}: anchor appears {text.count(anchor)}x, expected 1")
        return
    new = text.replace(anchor, (insert + anchor) if before else (anchor + insert), 1)
    if not DRY:
        path.write_text(new, encoding="utf-8")
    changes.append(f"{rel}: inserted {marker[:50]}")


def replace_block(rel: str, anchor: str, replacement: str, marker: str) -> None:
    """Replace `anchor` outright with `replacement`, unless `marker` is present."""
    path = ROOT / rel
    if not path.exists():
        skipped.append(f"{rel}: FILE MISSING")
        return
    text = path.read_text(encoding="utf-8")
    if marker in text:
        skipped.append(f"{rel}: already patched ({marker[:40]}...)")
        return
    if anchor not in text:
        skipped.append(f"{rel}: ANCHOR NOT FOUND -- {anchor[:60]!r}")
        return
    if text.count(anchor) != 1:
        skipped.append(f"{rel}: anchor appears {text.count(anchor)}x, expected 1")
        return
    if not DRY:
        path.write_text(text.replace(anchor, replacement, 1), encoding="utf-8")
    changes.append(f"{rel}: replaced block for {marker[:50]}")


# ── 1. the client module ────────────────────────────────────────────────────
dst = ROOT / "agent" / "claude_code_cli_client.py"
if not CLIENT_SRC.exists():
    skipped.append("agent/claude_code_cli_client.py: SOURCE MISSING")
elif dst.exists() and dst.read_text(encoding="utf-8") == CLIENT_SRC.read_text(encoding="utf-8"):
    skipped.append("agent/claude_code_cli_client.py: already current")
else:
    if not DRY:
        shutil.copyfile(CLIENT_SRC, dst)
    changes.append("agent/claude_code_cli_client.py: installed")

# ── 2. auth.py: base-url constant ───────────────────────────────────────────
patch(
    "hermes_cli/auth.py",
    anchor='DEFAULT_COPILOT_ACP_BASE_URL = "acp://copilot"',
    insert='\nDEFAULT_CLAUDE_CODE_CLI_BASE_URL = "cli://claude-code"',
    marker="DEFAULT_CLAUDE_CODE_CLI_BASE_URL",
)

# ── 3. auth.py: ProviderConfig ──────────────────────────────────────────────
patch(
    "hermes_cli/auth.py",
    anchor='''    "copilot-acp": ProviderConfig(
        id="copilot-acp",
        name="GitHub Copilot ACP",
        auth_type="external_process",
        inference_base_url=DEFAULT_COPILOT_ACP_BASE_URL,
        base_url_env_var="COPILOT_ACP_BASE_URL",
    ),
''',
    insert='''    "claude-code-cli": ProviderConfig(
        id="claude-code-cli",
        name="Claude Code CLI (subscription)",
        auth_type="external_process",
        inference_base_url=DEFAULT_CLAUDE_CODE_CLI_BASE_URL,
        base_url_env_var="CLAUDE_CODE_CLI_BASE_URL",
    ),
''',
    marker='"claude-code-cli": ProviderConfig(',
)

# ── 4. auth.py: credential resolver branch ──────────────────────────────────
_RESOLVER_ANCHOR = '''    base_url = os.getenv(pconfig.base_url_env_var, "").strip() if pconfig.base_url_env_var else ""
    if not base_url:
        base_url = pconfig.inference_base_url

    command = (
        os.getenv("HERMES_COPILOT_ACP_COMMAND", "").strip()
        or os.getenv("COPILOT_CLI_PATH", "").strip()
        or "copilot"
    )
    raw_args = os.getenv("HERMES_COPILOT_ACP_ARGS", "").strip()
    args = shlex.split(raw_args) if raw_args else ["--acp", "--stdio"]
    resolved_command = shutil.which(command) if command else None
    if not resolved_command and not base_url.startswith("acp+tcp://"):'''

_RESOLVER_BRANCH = '''    base_url = os.getenv(pconfig.base_url_env_var, "").strip() if pconfig.base_url_env_var else ""
    if not base_url:
        base_url = pconfig.inference_base_url

    if provider_id == "claude-code-cli":
        # Drives the locally installed Claude Code CLI, which performs its own
        # subscription auth. That is what keeps traffic on the plan's included
        # quota instead of the extra-usage / API-credit bucket the direct
        # `anthropic` OAuth transport is billed against.
        cc_command = (
            os.getenv("HERMES_CLAUDE_CLI_COMMAND", "").strip()
            or os.getenv("CLAUDE_CLI_PATH", "").strip()
            or "claude"
        )
        cc_raw_args = os.getenv("HERMES_CLAUDE_CLI_ARGS", "").strip()
        cc_args = shlex.split(cc_raw_args) if cc_raw_args else [
            "-p",
            "--output-format", "json",
            "--tools", "",
            "--safe-mode",
            "--no-session-persistence",
            "--strict-mcp-config",
        ]
        cc_resolved = shutil.which(cc_command) if cc_command else None
        if not cc_resolved and not Path(cc_command).exists():
            raise AuthError(
                f"Could not find the Claude Code CLI command '{cc_command}'. "
                "Install it with `npm install -g @anthropic-ai/claude-code`, or set "
                "HERMES_CLAUDE_CLI_COMMAND/CLAUDE_CLI_PATH.",
                provider=provider_id,
                code="missing_claude_cli",
            )
        return {
            "provider": provider_id,
            "api_key": "claude-code-cli",
            "base_url": base_url.rstrip("/"),
            "command": cc_resolved or cc_command,
            "args": cc_args,
            "source": "process",
        }

    command = (
        os.getenv("HERMES_COPILOT_ACP_COMMAND", "").strip()
        or os.getenv("COPILOT_CLI_PATH", "").strip()
        or "copilot"
    )
    raw_args = os.getenv("HERMES_COPILOT_ACP_ARGS", "").strip()
    args = shlex.split(raw_args) if raw_args else ["--acp", "--stdio"]
    resolved_command = shutil.which(command) if command else None
    if not resolved_command and not base_url.startswith("acp+tcp://"):'''

replace_block(
    "hermes_cli/auth.py",
    anchor=_RESOLVER_ANCHOR,
    replacement=_RESOLVER_BRANCH,
    marker='if provider_id == "claude-code-cli":',
)

# ── 4b. auth.py: status snapshot branch (drives the model selector) ─────────
patch(
    "hermes_cli/auth.py",
    anchor='''    pconfig = PROVIDER_REGISTRY.get(provider_id)
    if not pconfig or pconfig.auth_type != "external_process":
        return {"configured": False}
''',
    insert='''
    if provider_id == "claude-code-cli":
        cc_command = (
            os.getenv("HERMES_CLAUDE_CLI_COMMAND", "").strip()
            or os.getenv("CLAUDE_CLI_PATH", "").strip()
            or "claude"
        )
        cc_resolved = shutil.which(cc_command) if cc_command else None
        cc_base_url = (
            os.getenv(pconfig.base_url_env_var, "").strip()
            if pconfig.base_url_env_var else ""
        ) or pconfig.inference_base_url
        return {
            "configured": bool(cc_resolved),
            "provider": provider_id,
            "name": pconfig.name,
            "command": cc_command,
            "args": [],
            "resolved_command": cc_resolved,
            "base_url": cc_base_url,
            "logged_in": bool(cc_resolved),
            "source_label": "Managed by the Claude Code CLI (subscription)",
        }
''',
    marker='if provider_id == "claude-code-cli":\n        cc_command',
)

# ── 4c. auth.py: get_auth_status dispatcher ────────────────────────────────
patch(
    "hermes_cli/auth.py",
    anchor='''    if target == "copilot-acp":''',
    insert='''    if target == "claude-code-cli":
        return get_external_process_provider_status(target)
''',
    marker='if target == "claude-code-cli":',
    before=True,
)

# ── 5. providers.py: Hermes overlay ─────────────────────────────────────────
patch(
    "hermes_cli/providers.py",
    anchor='''    "copilot-acp": HermesOverlay(
        transport="codex_responses",
        auth_type="external_process",
        base_url_override="acp://copilot",
        base_url_env_var="COPILOT_ACP_BASE_URL",
    ),
''',
    insert='''    "claude-code-cli": HermesOverlay(
        transport="openai_chat",
        auth_type="external_process",
        base_url_override="cli://claude-code",
        base_url_env_var="CLAUDE_CODE_CLI_BASE_URL",
    ),
''',
    marker='"claude-code-cli": HermesOverlay(',
)

# ── 6. auxiliary_client.py: dispatch branch ─────────────────────────────────
patch(
    "agent/auxiliary_client.py",
    anchor='        if provider == "copilot-acp":',
    insert='''        if provider == "claude-code-cli":
            if not final_model:
                logger.warning(
                    "resolve_provider_client: claude-code-cli requested but no "
                    "model was provided or configured"
                )
                return None, None
            from agent.claude_code_cli_client import ClaudeCodeCLIClient

            client = ClaudeCodeCLIClient(
                api_key=str(creds.get("api_key", "")).strip() or "claude-code-cli",
                base_url=str(creds.get("base_url", "")).strip(),
                command=str(creds.get("command", "")).strip() or None,
                args=list(creds.get("args") or []),
            )
            logger.debug("resolve_provider_client: %s (%s)", provider, final_model)
            return (_to_async_client(client, final_model, is_vision=is_vision) if async_mode
                    else (client, final_model))
''',
    marker='if provider == "claude-code-cli":',
    before=True,
)

# ── 7. auxiliary_client.py: don't re-wrap as an Anthropic-wire client ───────
patch(
    "agent/auxiliary_client.py",
    anchor='''    try:
        from agent.copilot_acp_client import CopilotACPClient
        if _safe_isinstance(client_obj, CopilotACPClient):
            return client_obj
    except ImportError:
        pass
''',
    insert='''    try:
        from agent.claude_code_cli_client import ClaudeCodeCLIClient
        if _safe_isinstance(client_obj, ClaudeCodeCLIClient):
            return client_obj
    except ImportError:
        pass
''',
    marker="_safe_isinstance(client_obj, ClaudeCodeCLIClient)",
)

# ── 8. auxiliary_client.py: async passthrough ───────────────────────────────
patch(
    "agent/auxiliary_client.py",
    anchor='''    try:
        from agent.copilot_acp_client import CopilotACPClient
        if isinstance(sync_client, CopilotACPClient):
            return sync_client, model
    except ImportError:
        pass
''',
    insert='''    try:
        from agent.claude_code_cli_client import ClaudeCodeCLIClient
        if isinstance(sync_client, ClaudeCodeCLIClient):
            return sync_client, model
    except ImportError:
        pass
''',
    marker="isinstance(sync_client, ClaudeCodeCLIClient)",
)

# ── 9. agent_runtime_helpers.py: main-loop client factory ───────────────────
patch(
    "agent/agent_runtime_helpers.py",
    anchor='    if agent.provider == "copilot-acp" or str(client_kwargs.get("base_url", "")).startswith("acp://copilot"):',
    insert='''    if agent.provider == "claude-code-cli" or str(client_kwargs.get("base_url", "")).startswith("cli://claude-code"):
        from agent.claude_code_cli_client import ClaudeCodeCLIClient

        client = ClaudeCodeCLIClient(**client_kwargs)
        _ra().logger.info(
            "Claude Code CLI client created (%s, shared=%s) %s",
            reason,
            shared,
            agent._client_log_context(),
        )
        return client
''',
    marker='agent.provider == "claude-code-cli"',
    before=True,
)

# ── 9b. runtime_provider.py: runtime resolution branch ──────────────────────
# Without this the configured provider falls through the generic path and
# silently resolves to openrouter, which then 400s on the bare model id.
patch(
    "hermes_cli/runtime_provider.py",
    anchor='''    if provider == "copilot-acp":
        creds = resolve_external_process_provider_credentials(provider)''',
    insert='''    if provider == "claude-code-cli":
        creds = resolve_external_process_provider_credentials(provider)
        return {
            "provider": "claude-code-cli",
            "api_mode": "chat_completions",
            "base_url": creds.get("base_url", "").rstrip("/"),
            "api_key": creds.get("api_key", ""),
            "command": creds.get("command", ""),
            "args": list(creds.get("args") or []),
            "source": creds.get("source", "process"),
            "requested_provider": requested_provider,
        }

''',
    marker='if provider == "claude-code-cli":',
    before=True,
)

# ── 9c. models.py: curated model list for the picker ────────────────────────
patch(
    "hermes_cli/models.py",
    anchor='''    "anthropic": [
        "claude-fable-5",''',
    insert='''    "claude-code-cli": [
        "claude-opus-5",
        "claude-sonnet-5",
        "claude-fable-5",
        "claude-opus-4-8",
        "claude-opus-4-7",
        "claude-opus-4-6",
        "claude-sonnet-4-6",
        "claude-opus-4-5-20251101",
        "claude-sonnet-4-5-20250929",
        "claude-haiku-4-5-20251001",
    ],
''',
    marker='"claude-code-cli": [',
    before=True,
)

# ── 9d. models.py: show it in the `hermes model` provider picker ────────────
patch(
    "hermes_cli/models.py",
    anchor='    ProviderEntry("anthropic",      "Anthropic",                "Anthropic (Claude models via API key or Claude Code)"),',
    insert='\n    ProviderEntry("claude-code-cli", "Claude Code CLI",         "Claude Code CLI subscription (spawns claude -p; no API credits)"),',
    marker='ProviderEntry("claude-code-cli"',
)

# ── 9e/9f. register the provider's env keys so they load from .env ──────────
_ENV_KEYS = '''    "HERMES_CLAUDE_CLI_COMMAND",
    "HERMES_CLAUDE_CLI_ARGS",
    "HERMES_CLAUDE_CLI_CWD",
    "CLAUDE_CLI_PATH",
    "CLAUDE_CODE_CLI_BASE_URL",
'''
for _rel in ("hermes_cli/config.py", "hermes_cli/env_loader.py"):
    patch(
        _rel,
        anchor='''    "HERMES_COPILOT_ACP_COMMAND",
    "HERMES_COPILOT_ACP_ARGS",
    "COPILOT_CLI_PATH",
    "COPILOT_ACP_BASE_URL",
''',
        insert=_ENV_KEYS,
        marker='"HERMES_CLAUDE_CLI_COMMAND",',
    )

# ── 10. provider plugin (profile registration) ──────────────────────────────
plugdir = ROOT / "plugins" / "model-providers" / "claude-code-cli"
plugin_init = '''"""Claude Code CLI provider profile.

claude-code-cli drives the local Claude Code CLI as a subprocess rather than
calling api.anthropic.com. The CLI performs its own subscription auth, so
requests are billed against the plan's included quota instead of the
extra-usage bucket the direct OAuth transport requires.

The subprocess facade lives in agent/claude_code_cli_client.py.
"""

from providers import register_provider
from providers.base import ProviderProfile


class ClaudeCodeCLIProfile(ProviderProfile):
    """Claude Code CLI — external process, no REST models endpoint."""

    def fetch_models(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 8.0,
    ) -> list[str] | None:
        """Model listing is owned by the CLI; expose the subscription catalog."""
        return [
            "claude-opus-5",
            "claude-sonnet-5",
            "claude-fable-5",
            "claude-opus-4-6",
            "claude-sonnet-4-6",
            "claude-haiku-4-5-20251001",
        ]


claude_code_cli = ClaudeCodeCLIProfile(
    name="claude-code-cli",
    aliases=("claude-cli", "claude-subscription"),
    api_mode="chat_completions",
    env_vars=(),  # credentials are owned by the Claude Code CLI
    base_url="cli://claude-code",
    auth_type="external_process",
)

register_provider(claude_code_cli)
'''
plugin_yaml = """name: claude-code-cli-provider
kind: model-provider
version: 1.0.0
description: Claude Code CLI subscription via local subprocess
"""
for name, body in (("__init__.py", plugin_init), ("plugin.yaml", plugin_yaml)):
    target = plugdir / name
    if target.exists() and target.read_text(encoding="utf-8") == body:
        skipped.append(f"plugins/model-providers/claude-code-cli/{name}: already current")
        continue
    if not DRY:
        plugdir.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    changes.append(f"plugins/model-providers/claude-code-cli/{name}: written")

print(f"=== {'DRY RUN ' if DRY else ''}{ROOT} ===")
for c in changes:
    print("  [CHANGED] " + c)
for s in skipped:
    tag = "[!!]" if ("NOT FOUND" in s or "MISSING" in s or "expected 1" in s) else "[ ok ]"
    print(f"  {tag} {s}")
print(f"  -> {len(changes)} change(s), {len(skipped)} skipped")
