# Environment bindings

Every row was true on the demonstrator's machine and had to be resolved before
this skill could run here. Resolutions are `confirm`, `substitute`, `drop`, or
`BLOCKED-ON-USER`. None was resolved by assuming.

| # | Binding | In the video | Resolution | Notes |
|---|---|---|---|---|
| 1 | MCP server | AnySite hosted at `https://mcp.anysite.io/mcp` | **substitute** | Any HTTP MCP server. Verified against `gbrain` 0.42.67.0 at `http://127.0.0.1:3131/mcp`. |
| 2 | Server credential | AnySite JWT, pasted into `~/.cursor/mcp.json` (visible on screen at 01:51) | **substitute** | `--bearer-env` names an environment variable; the token is never a CLI argument and never written into a map. Verified: the written map does not contain the token. |
| 3 | An HTTP MCP server to test against | — | **confirm** | `gbrain` runs as a systemd user service on this machine and `GBRAIN_REMOTE_TOKEN` is set in both `~/.bashrc` and Codex's config. This is why the verification is executed rather than hypothetical. |
| 4 | Client | Cursor, via its "Add MCP" button | **drop** | The probe speaks JSON-RPC directly. No editor, no host client. |
| 5 | Config location | `~/.cursor/mcp.json` | **substitute** | Reads Claude Code (`~/.claude.json`, `~/.claude/mcp.json`), Cursor, project `./.mcp.json`, and Codex (`~/.codex/config.toml`). Cursor's path is still read, so the video's own setup works unchanged. |
| 6 | Transport | Streamable HTTP | **confirm** | Implemented. Both response framings are handled — gbrain replies with SSE `data:` frames, and a plain JSON body is equally accepted. |
| 7 | OAuth | Dashboard offered an OAuth URL as the recommended option | **drop** | Not implemented. Bearer-token only; recorded in Limits rather than half-built. |
| 8 | stdio servers | not shown | **BLOCKED-ON-USER** | Out of scope. `servers` lists them and `probe` refuses with a message naming the transport, rather than failing obscurely. |

## What execution established

- **The SSE framing matters.** gbrain answers `initialize` with
  `event: message\ndata: {...}` rather than a JSON body. A probe that only
  parsed JSON would have failed against a perfectly healthy server. Both
  framings are handled and the `Accept` header asks for both, so a server that
  only speaks one does not reject the request.
- **`resources/list` and `prompts/list` are genuinely optional.** gbrain
  implements neither and returns an error for both. Recording that as
  `unsupported` rather than `0` keeps "wrong assumption" distinguishable from
  "empty".
- **Codex stores auth differently from Claude Code.** `~/.codex/config.toml`
  uses `bearer_token_env_var` — a variable *name*, not a value. The config
  reader picks that up, which is why `probe --server gbrain` needs no `--bearer-env`
  flag on this machine.

## Credentials

No token is ever accepted as a command-line argument, written into a capability
map, or echoed. Maps are scrubbed before writing as a second line of defence.
An unset variable produces a message naming the variable and exits — it is a
binding to resolve, not a server that is down.

Per this repo's two-layer convention, a token needs to exist in **both**
`~/.bashrc` (the cross-host baseline Codex and DSH read) and
`.claude/settings.local.json`'s `env` block (which Claude Code injects into
non-interactive Bash calls). `GBRAIN_REMOTE_TOKEN` satisfies both, which is why
the probe works from a Bash tool call that never sources `~/.bashrc`.
