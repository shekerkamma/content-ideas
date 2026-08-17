# DeepSeek Harness — multi-model provider contract

How `dsh` (DeepSeek Harness) is wired to every model provider available on this
machine, what each one actually costs, and which claims were verified rather
than assumed.

Companion files:
- `docs/dsh-cordis-patch.example.yml` — the provider config, secrets-free
  (`apiKeyEnv` references only). Live copy: `~/.dsh/profiles/{headless,web}/cordis.patch.yml`.
- `scripts/claude_code_bridge.py` — OpenAI-compatible shim over the Claude Code CLI.

## The one rule that governed this work

**A catalog entry is not a routable model.** Every model in the table below was
confirmed with a real `chat/completions` call returning a correct answer, then
re-confirmed end-to-end through `dsh` with tool use. This was not pedantry:

- OmniRoute listed **29** DeepSeek models. **28 fail** — zenmux 403, nvidia 410,
  ollama-cloud 401, cloudflare-ai 401, theoldllm 403. One works.
- OmniRoute's Cursor routes return **HTTP 200 with zero output tokens in 4 ms**.
  Any check that read only the status code would have called them healthy.
- NVIDIA lists 102 models; several return 404/`Gone` on invocation.

Trusting any of those listings would have produced a config that never worked.

## Providers

| Route | Endpoint | Auth | Cost |
|---|---|---|---|
| `claude-code-cli` | `127.0.0.1:8318/v1` (local bridge) | **Claude subscription** — no credential stored | none |
| `cliproxyapi` | `<win-host>:8317/v1` | AI Studio key + Antigravity OAuth | free tier |
| `zenmux` | `zenmux.ai/api/v1` | API key | **prepaid, per token** |
| `omniroute` | `<win-host>:20128/v1` | gateway key; ChatGPT sub for `cx/*` | mixed |
| `openrouter` | `openrouter.ai/api/v1` | API key | `:free` models only |

### Cost — zenmux is not a subscription

zenmux is a prepaid aggregator. It bills per token against a zenmux balance;
Claude Pro and ChatGPT Plus are **not** involved. Prices USD per million tokens,
read from its `/v1/models` `pricings` field on 2026-08-17:

| Model | Completion |
|---|---|
| `deepseek/deepseek-v4-flash-free` | **0** (prompt 0 too — genuinely free) |
| `openai/gpt-5.6-luna` | $1.20 → $1.80 |
| `deepseek/deepseek-v4-pro` | $1.98 → $3.96 |
| `google/gemini-3.7-flash` | $3.75 |
| `anthropic/claude-sonnet-5` | $10.00 |
| `anthropic/claude-opus-5` | **$25.00** |

zenmux exposes **no balance endpoint** (five paths tried, all 404) — remaining
credit can only be read from its dashboard. Treat an agent loop on
`claude-opus-5` as an unbounded spend with no local warning.

For Claude at zero cost use the `claude-code-cli` route instead; keep zenmux's
Claude entries only when real tool-calling is required (see the limitation
below).

## The Claude Code CLI bridge

Hermes reaches a Claude subscription through a provider it records as:

```json
{"auth_type": "external_process", "source": "manual:external_process",
 "base_url": "cli://claude-code"}
```

No access token, no refresh token, no API key — `cli://claude-code` means
*spawn the binary* and let the CLI authenticate itself. dsh cannot do this: its
`dsh-llm-pi-ai` adapter supports only `openai-completions`,
`openai-responses`, and `anthropic-messages` over HTTP, and its docs state that
OAuth-authenticated providers are deliberately excluded because a profile must
be fully describable by "a key, an endpoint, and headers."

`scripts/claude_code_bridge.py` is the missing adapter — HTTP in, subprocess
out. It serves `/v1/chat/completions` (JSON and SSE) plus `/v1/models`, and per
request runs `claude -p --output-format json`, returning the `result` field.

```bash
CLAUDE_BRIDGE_CWD=/path/to/workspace python3 scripts/claude_code_bridge.py --port 8318
dsh --profile headless --patch ~/.dsh/patches/claude-code-cli.yml "your task"
```

**Limitation, load-bearing:** `claude -p` is a complete agent, not a raw model.
It performs its own tool use internally and returns prose; it never emits
OpenAI `tool_calls`. Driving dsh through this route bypasses dsh's own
bash/fs/todo tools, permission prompts, sandbox policy, and trajectory log —
Claude Code does the work, nested inside dsh. A passing smoke test looks
identical to a real tool-calling route, so this cannot be detected by output
alone. Each call also re-sends Claude Code's own system prompt (~30k cache
tokens cold), so subscription rate limits arrive sooner than with a bare model.

## Host gotchas

Each of these cost real debugging time and is silent when wrong.

- **WSL cannot reach Windows-side services on `127.0.0.1`.** OmniRoute and
  CLIProxyAPI both run Windows-side; from WSL they are the default-gateway IP
  (`ip route show default | awk '{print $3}'`), which **changes on reboot**.
  Hermes' own config points `cliproxyapi` at `127.0.0.1:8317`, which therefore
  cannot work from the WSL side.
- **CLIProxyAPI binds `host:` literally.** Shipped as `127.0.0.1`, it is
  unreachable from WSL even when running; `0.0.0.0` is required. It also needs
  an explicit `-config <path>` — it will not resolve the path from a
  WSL-launched cwd.
- **OmniRoute connection updates take `PUT`, not `PATCH`.** `PATCH` returns 405,
  and the bundled `omniroute api providers patch-api-providers-id-` wrapper
  reports success while changing nothing. An imported OAuth connection also
  stays `isActive: false` and serves **0 models** until flipped.
- **`omniroute providers available` lists only api-key providers** — it prints
  "Categories: api-key". OAuth providers live in `omniroute oauth providers`.
  Reading the first and concluding a provider does not exist is wrong.
- **The same provider can work in one host and be broken in another.**
  OmniRoute's zenmux connection 403s on every model including non-DeepSeek ones,
  while Hermes' zenmux key works on all of them. A 403 from one host's copy is
  not evidence the provider is unavailable.

## Reproducing

Provider credentials already on this machine are the starting point, not new
signups. `~/.hermes/config.yaml` is the authoritative record of what works —
its `custom_providers` entries of `type: openai_compatible` map 1:1 onto dsh's
`api: openai-completions`, so porting is a copy rather than an integration.

Secrets live in `~/.dsh/.credentials.yaml` (mode 0600) as `apiKeyEnv`
references; no literal key belongs in the profile config or in this repo.
