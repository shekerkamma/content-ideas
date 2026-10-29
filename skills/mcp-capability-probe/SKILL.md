---
name: mcp-capability-probe
description: Use before building against an MCP server, when a tool call fails with "no such tool", or when a server's surface may have shifted under you — "what does this MCP server actually expose", "which tools do I have", "did the server change", "the docs mention an endpoint I can't call". Writes the full tool/resource/prompt map to disk and prints a summary, so a 96-tool server costs a few lines of context instead of 85 KiB of schemas. Not an MCP client and not a way to call tools.
license: MIT
metadata:
  category: Agent Engineering
  version: '1.0'
  compatibility: Python 3 stdlib only. HTTP/Streamable-HTTP MCP servers. Claude Code, Codex, DeepSeek Harness, or any host with a shell.
  derived-from-video: https://www.youtube.com/watch?v=nI0Mhzcl2Fk
  derived-on: '2026-08-25'
  source-upload-date: '2026-08-24'
---

# MCP Capability Probe

Asks a server what it exposes, writes the answer to a file, and prints a
summary. It does not call the server's tools, and it is not a replacement for
your host's own MCP client.

The demonstration this came from opens by asking an assistant "show me what
endpoints are available" and building only on what came back. That instinct is
right and the transcript's version of it is expensive: a real server's tool list
does not belong in a conversation. The local `gbrain` server answers with **96
tools and 85.5 KiB of schemas** — more than most of the work they will ever do.

**Source:** derived from a video demonstration, then executed here. See
`references/source-video.md`.

## When to invoke

- Before writing anything against an unfamiliar MCP server.
- When a call fails with an unknown-tool error and you need to settle whether
  the tool exists, rather than re-reading the docs.
- When documentation and behaviour disagree.
- On a schedule or before a release, to catch a server whose surface moved.

Do not invoke it to *use* a tool. Your host already has an MCP client; this
answers "what is there", not "do the thing".

## Procedure

1. **List what is configured.** Route: `Bash`. Reads config files only —
   contacts nothing, costs nothing, needs no credential.

   ```bash
   python3 scripts/probe_mcp.py servers
   ```

   Reads `~/.claude.json`, `~/.claude/mcp.json`, `~/.cursor/mcp.json`,
   `./.mcp.json`, and `~/.codex/config.toml`, including each server's
   `bearer_token_env_var`. A server absent here is "not configured in a file
   this tool reads" — hosts also inject servers at runtime, so absence is not
   proof.

2. **Probe one server.** Route: `Bash`. Runs `initialize`, then `tools/list`,
   `resources/list`, `prompts/list`.

   ```bash
   python3 scripts/probe_mcp.py probe --server gbrain --out ./capability-maps
   python3 scripts/probe_mcp.py probe --url https://example.com/mcp \
           --bearer-env MY_TOKEN_VAR --out ./capability-maps
   ```

   `--bearer-env` names an environment variable. The token is never accepted as
   an argument and never written into a map. A server that does not implement
   `resources/list` or `prompts/list` is recorded as `unsupported` rather than
   as empty — those are different facts.

3. **Search the map instead of reading it.** Route: `Bash`. This is the step
   that keeps the probe cheap.

   ```bash
   python3 scripts/probe_mcp.py show capability-maps/gbrain.json --grep search
   python3 scripts/probe_mcp.py show capability-maps/gbrain.json --tool put_page
   ```

   `--grep` matches names and descriptions and prints one line each; `--tool`
   prints one full schema. Pull a schema when you are about to call that tool,
   not before.

4. **Diff after anything upgrades.** Route: `Bash`. Exit 1 when a tool
   disappeared, because that is the change that breaks callers.

   ```bash
   python3 scripts/probe_mcp.py diff old.json new.json
   ```

5. **Record what you relied on.** Route: `Read/Write`. Keep the map beside the
   code that depends on it and cite the probe date. A capability map is a
   measurement with a timestamp, not a permanent fact.

## Judgment rules

Editable policy. Tune these; do not hardcode them into the steps.

- **Discovery outranks documentation.** In the source video the assistant
  reports that the vendor's docs reference an endpoint that the discovery
  response did not list (video 02:18, on screen). When the two disagree,
  believe the server. `show --tool <name>` exits 1 with that reminder.
- **Never print a tool list you have not been asked for.** Summary by default,
  schema on demand. A 96-tool dump costs roughly 20k tokens and answers a
  question nobody asked.
- **`unsupported` is not `0`.** A server that does not implement
  `resources/list` is different from one that implements it and has none.
  Collapsing them loses the ability to tell "wrong assumption" from "empty".
- **Absence in a config file is not absence.** `servers` reads disk. Hosts
  inject servers at runtime; say "not configured here", never "does not exist".
  (This repo has been burned by exactly that inference — see the
  `prove-absence-before-blocking` and `one-blocked-path-is-not-a-blocked-lane`
  notes.)
- **A missing credential is a binding, not an outage.** Unset env var → a
  message naming the variable, never a retry loop against a server that is fine.
- **Re-probe on a version change, not on a schedule you picked arbitrarily.**
  The map is only stale when the server moved.

## Environment bindings

| Binding | In the video | On this machine |
|---|---|---|
| MCP server | AnySite hosted MCP at `mcp.anysite.io/mcp` | **substitute** — any HTTP MCP server; `gbrain` at `127.0.0.1:3131/mcp` used for verification |
| Auth | `Authorization: Bearer <jwt>` pasted into `~/.cursor/mcp.json` | **substitute** — `--bearer-env` names a variable; the token never enters a file or an argument |
| Client | Cursor's "Add MCP" button | **drop** — this speaks JSON-RPC directly; no editor needed |
| Discovery | asking the assistant in chat | **substitute** — a script, so the result lands on disk instead of in the transcript |
| Transport | Streamable HTTP | **confirm** — implemented, with SSE-framed and plain-JSON bodies both handled |
| stdio servers | not shown | **BLOCKED-ON-USER** — out of scope; probe those through their own host |

## Verification

```bash
cd skills/mcp-capability-probe
python3 scripts/probe_mcp.py servers
python3 scripts/probe_mcp.py probe --server gbrain --out /tmp/capmaps
python3 scripts/probe_mcp.py show /tmp/capmaps/gbrain.json --grep schema
python3 -m pytest tests/ -q
```

**Executed 2026-08-25** against `gbrain` 0.42.67.0 (PGLite engine) over
Streamable HTTP, protocol `2025-06-18`, Python 3.12.3.

Independently confirmed, not self-reported:

- `servers` found 7 configured servers across `~/.claude.json` and
  `~/.codex/config.toml`, correctly reading gbrain's
  `bearer_token_env_var = "GBRAIN_REMOTE_TOKEN"` out of TOML, and contacted
  none of them.
- `probe --server gbrain` returned **96 tools**, wrote an **85.5 KiB** map, and
  printed 12 tool names. `resources` and `prompts` came back `unsupported`,
  which is what gbrain actually does — not zero.
- `grep -c "$GBRAIN_REMOTE_TOKEN"` against the written map returned **0**: the
  bearer token is not in the artifact.
- `show --tool company_employees` (a name from the *video's* server, absent
  here) exited 1 with the discovery-outranks-docs message.
- `diff` on a mutated copy correctly reported 1 added, 1 removed, 1 changed and
  exited 1 on the removal.

- **Cross-host discovery was measured, not assumed.** DeepSeek Harness's own
  `@deepseek-ai/dsh-skill-filesystem` provider was driven directly against this
  repo: it resolves `<projectRoot>/.agents/skills` at rank 200, and `list()`
  returned this skill by name with its description parsed and zero warnings.
  The frontmatter was re-parsed with the same `yaml` package DSH ships.

## Limits

- **HTTP/Streamable-HTTP only.** stdio servers are not probed; they need a host
  that can spawn them.
- No OAuth flow. The source video's dashboard offered an OAuth URL alongside
  the direct-key URL; only bearer-token auth is implemented here.
- `initialize` is sent but no `notifications/initialized` follow-up. Every
  server tested accepted `tools/list` regardless; a stricter server may not.
- A capability map is a measurement at a timestamp. It says nothing about
  whether a tool *works*, only that the server lists it.
- Derived from a demonstration dated 2026-08-24. The vendor UI shown there is
  expiring evidence; the MCP protocol behaviour is not vendor-specific and was
  verified independently.

## Host compatibility

| Host | Status |
|---|---|
| Claude Code | Full. Reads `~/.claude.json` and project `.mcp.json`. |
| Codex CLI / Desktop | Full. Reads `~/.codex/config.toml`, including `bearer_token_env_var`. |
| DeepSeek Harness | Full. Discovered from `<projectRoot>/.agents/skills` (rank 200) or `~/.dsh/skills`. |
| Any host with a shell | Full — pass `--url` and `--bearer-env` directly. |
