# `claude-code-cli` provider for Hermes Agent

Adds a first-class `claude-code-cli` model provider to a [Hermes
Agent](https://github.com/NousResearch/hermes-agent) install. It drives the
locally installed Claude Code CLI as a subprocess instead of calling
`api.anthropic.com` directly, so inference is billed against the Claude
**subscription** rather than API credits.

## Why this exists

Hermes ships two Anthropic paths, and neither spends a plain subscription:

| Path | What it does | Result on a Pro plan |
|---|---|---|
| `anthropic` + API key | `x-api-key` against the Messages API | Bills API credits |
| `anthropic` + OAuth token | Subscription OAuth token against the Messages API | `HTTP 400: You're out of extra usage` |

The second is the trap. Anthropic bills third-party OAuth traffic to the
**extra usage** (pay-as-you-go) bucket, not the plan's included quota. Hermes'
own provider card says so verbatim — `_OAUTH_PROVIDER_CATALOG` in
`hermes_cli/web_server.py` names it *"Anthropic OAuth: Required Extra Usage
Credits to Use Subscription"*, with a source comment noting it "only works with
extra usage credits on top of a Claude Max plan."

This is the structural difference from `openai-codex`, which *does* work on a
bare ChatGPT subscription: OpenAI permits third-party clients to spend a
subscription against its Codex endpoint. Anthropic does not.

`claude-code-cli` sidesteps it by shelling out to `claude -p`. The CLI performs
its own subscription auth, so the request is indistinguishable from ordinary
Claude Code usage and lands on the included quota.

## Install

The installer is idempotent — every edit is guarded by a marker check, so it is
safe to re-run.

```bash
# Hermes CLI (typically ~/hermes-agent)
python3 install_claude_code_cli_provider.py ~/hermes-agent

# Hermes Desktop — the Windows profile mounted into WSL
python3 install_claude_code_cli_provider.py \
  "/mnt/c/Users/$USER/AppData/Local/hermes/hermes-agent"
```

Preview without writing:

```bash
python3 install_claude_code_cli_provider.py <tree> --dry-run
```

Every edit is **additive**. The installer refuses to touch a file whose anchor
is missing or ambiguous and reports it as `[!!]` rather than guessing — so a
Hermes version it doesn't understand fails loudly instead of corrupting a core
file.

**Re-run after every Hermes upgrade.** Upgrades overwrite core files; the
marker checks mean a re-run restores only what the upgrade removed.

## Configure

```yaml
model:
  default: claude-sonnet-4-6
  provider: claude-code-cli
```

`hermes model` lists the provider as "Claude Code CLI" with the subscription
model catalog (`claude-opus-5`, `claude-sonnet-5`, `claude-fable-5`,
`claude-sonnet-4-6`, …). `hermes -m <model> --provider claude-code-cli` works
for one-off overrides.

Optional environment overrides, resolved in this order:

| Variable | Purpose |
|---|---|
| `HERMES_CLAUDE_CLI_COMMAND` / `CLAUDE_CLI_PATH` | Absolute path to the CLI |
| `HERMES_CLAUDE_CLI_ARGS` | Replace the default argv wholesale |
| `HERMES_CLAUDE_CLI_CWD` | Working directory for the child process |
| `CLAUDE_CODE_CLI_BASE_URL` | Override the `cli://claude-code` marker |

On Hermes Desktop, pin the absolute path in the Hermes `.env` — the Windows
process resolves `claude.exe` from its own `PATH`, not WSL's:

```
HERMES_CLAUDE_CLI_COMMAND=C:\Users\<you>\.local\bin\claude.exe
```

## How it works

`agent/claude_code_cli_client.py` is a minimal OpenAI-client-compatible facade
(`client.chat.completions.create`) that spawns:

```
claude -p --output-format json --model <model> \
       --tools "" --safe-mode --no-session-persistence --strict-mcp-config
```

Four decisions worth knowing before editing it:

- **The prompt travels on stdin, never argv.** Hermes system prompts routinely
  exceed the 32767-character Windows command-line limit. System messages are
  folded into the transcript rather than passed via `--system-prompt` for the
  same reason.
- **`--tools ""` disables the CLI's own tools.** Hermes keeps ownership of tool
  execution. Tool calls come back as `<tool_call>{...}</tool_call>` text blocks
  and are parsed into OpenAI-shaped calls by the helpers in
  `agent/copilot_acp_client.py`, which this module reuses rather than
  duplicating.
- **`ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN` are stripped from the child
  environment.** If either is set, Claude Code authenticates as an API-key user
  and bills credits — defeating the entire point. `CLAUDE_CODE_OAUTH_TOKEN` is
  preserved, since a setup-token is a subscription credential.
- **`--bare` is deliberately avoided.** It forces `ANTHROPIC_API_KEY`/
  `apiKeyHelper` auth and never reads OAuth. `--safe-mode` is used instead: it
  disables CLAUDE.md, skills, plugins, hooks and MCP servers so the user's local
  setup can't leak into Hermes turns, while auth still resolves normally.

## What the installer patches

`copilot-acp` is the only other `external_process` provider in Hermes and was
the working template for all of this.

| File | Change |
|---|---|
| `agent/claude_code_cli_client.py` | **new** — the subprocess client |
| `plugins/model-providers/claude-code-cli/` | **new** — provider profile + `plugin.yaml` |
| `hermes_cli/auth.py` | `ProviderConfig`, credential resolver, status snapshot, `get_auth_status` dispatch |
| `hermes_cli/providers.py` | `HermesOverlay` entry |
| `hermes_cli/runtime_provider.py` | runtime resolution branch |
| `hermes_cli/models.py` | curated model list + `hermes model` picker entry |
| `hermes_cli/config.py`, `hermes_cli/env_loader.py` | register the `HERMES_CLAUDE_CLI_*` env keys so they load from `.env` |
| `agent/auxiliary_client.py` | client dispatch + guards against re-wrapping as an Anthropic-wire client |
| `agent/agent_runtime_helpers.py` | main-loop client factory branch |

The `runtime_provider.py` branch is the non-obvious one. Without it the
configured provider falls through the generic resolution path and silently
resolves to **OpenRouter**, which then 400s with `<model> is not a valid model
ID` — an error that looks nothing like a provider-routing bug.

## Verify

```bash
# provider registers and reports the CLI as available
python3 -c "
from hermes_cli.auth import PROVIDER_REGISTRY, get_external_process_provider_status
print(PROVIDER_REGISTRY['claude-code-cli'].name)
print(get_external_process_provider_status('claude-code-cli'))"

# end-to-end through Hermes' own dispatch
python3 -c "
from agent.auxiliary_client import resolve_provider_client
c, m = resolve_provider_client(provider='claude-code-cli', model='claude-sonnet-4-6')
r = c.chat.completions.create(model=m,
    messages=[{'role':'user','content':'Reply with exactly: OK'}], timeout=300)
print(r.choices[0].message.content)"

# full agent turn
hermes -z "Reply with exactly: OK"
```

Run these with each host's own interpreter — Hermes Desktop uses
`hermes-agent/venv/`, not `.venv/`.
