# Ghostty, WSL, Hermes, Codex, Claude Code, OpenClaw, and GBrain Runbook

Date captured: 2026-06-29

## What This Setup Is

Ghostty/winghostty is installed as a Windows terminal application. It is not
installed inside WSL.

The working model is:

```text
Windows winghostty.exe
  -> starts wsl.exe
    -> opens Ubuntu
      -> runs shell tools such as claude, codex, and hermes
        -> those clients connect to shared GBrain over HTTP MCP
```

## Installed Components

- Windows terminal app: `winghostty 1.3.116`
- Windows executable: `C:\Program Files\winghostty\winghostty.exe`
- Start Menu shortcut: `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\winghostty\winghostty.lnk`
- WSL distro: `Ubuntu`
- Project path: `/home/shekerk/content-ideas`
- Claude Code: installed in WSL, verified as `2.1.195`
- Codex CLI: installed in WSL, verified as `0.141.0`
- Hermes: installed in WSL under `/home/shekerk/hermes-agent`
- OpenClaw: running via Docker container `openclaw-openclaw-gateway-1`
- GBrain shared MCP service: systemd user service on port `3131`

## Important Distinction

This command launches a new Windows Ghostty window from WSL:

```bash
"/mnt/c/Program Files/winghostty/winghostty.exe"
```

It does not render Ghostty inside the current VS Code terminal pane. It opens a
separate GUI terminal window.

## Open Ghostty Into This WSL Project

From any WSL terminal:

```bash
"/mnt/c/Program Files/winghostty/winghostty.exe" -e wsl.exe -d Ubuntu --cd /home/shekerk/content-ideas
```

Meaning:

- `winghostty.exe`: launch Windows Ghostty/winghostty
- `-e`: run the following command inside Ghostty
- `wsl.exe -d Ubuntu`: start the Ubuntu WSL distro
- `--cd /home/shekerk/content-ideas`: open directly in this repo

## Optional WSL Alias

Add this to `~/.bashrc` if it is not already present:

```bash
ghostty-here() {
  "/mnt/c/Program Files/winghostty/winghostty.exe" -e wsl.exe -d Ubuntu --cd "$(pwd)"
}
```

Then reload the shell:

```bash
source ~/.bashrc
```

Usage:

```bash
cd ~/content-ideas
ghostty-here
```

## Shared GBrain MCP

All agent clients should use the same GBrain HTTP MCP server:

```text
http://127.0.0.1:3131/mcp
```

Why this matters:

- GBrain uses a local PGLite database.
- Multiple direct stdio writers can conflict with each other.
- The intended setup is one GBrain HTTP service as the single writer, and all
  agents as MCP clients.

The shared client token lives at:

```text
~/.gbrain/shared-clients.token
```

Do not commit or paste this token.

The WSL shell exports it dynamically from `~/.bashrc`:

```bash
if [ -r "$HOME/.gbrain/shared-clients.token" ]; then
  export MCP_GBRAIN_API_KEY="$(cat "$HOME/.gbrain/shared-clients.token")"
fi
```

### Client Topology Rule

Codex, Claude Code, Hermes, Antigravity/Gemini, and OpenClaw should use the
shared HTTP service, not direct stdio.

Codex:

```toml
[mcp_servers.gbrain]
url = "http://127.0.0.1:3131/mcp"
bearer_token_env_var = "MCP_GBRAIN_API_KEY"
startup_timeout_sec = 60
```

Claude Code:

```json
{
  "mcpServers": {
    "gbrain": {
      "type": "http",
      "url": "http://127.0.0.1:3131/mcp",
      "headers": {
        "Authorization": "Bearer <shared client token>"
      }
    }
  }
}
```

The older stdio wrapper (`scripts/gbrain_stdio_local.sh`) is only for
intentional single-client local mode. It opens the PGLite database directly and
can conflict with the shared HTTP service.

Hermes:

- Uses `http://127.0.0.1:3131/mcp`.
- Stores its bearer via Hermes' MCP environment handling.
- Existing Hermes config does not need to change for this Codex recovery path.

Antigravity/Gemini:

- Windows-native config uses `serverUrl: "http://127.0.0.1:3131/mcp"`.
- Auth is an HTTP `Authorization` header with the shared client token.
- Existing Antigravity/Gemini config does not need to change for this Codex
  recovery path.

## GBrain MCP Recovery

Symptom:

```text
MCP client for `gbrain` failed to start
handshaking with MCP server failed
error sending request for url (http://127.0.0.1:3131/mcp)
```

First check the shared service:

```bash
scripts/gbrain-recover.sh --check
```

If the service is down and no live process owns `~/.gbrain/brain.pglite`, repair
stale PGLite lock artifacts and restart the service:

```bash
scripts/gbrain-recover.sh --fix
```

The script only removes:

```text
~/.gbrain/brain.pglite/.gbrain-lock
~/.gbrain/brain.pglite/postmaster.pid
```

It refuses to remove them when `lsof +D ~/.gbrain/brain.pglite` reports a live
owner.

Manual equivalent:

```bash
systemctl --user status gbrain-http.service --no-pager
curl -i http://127.0.0.1:3131/health
lsof +D ~/.gbrain/brain.pglite
rm -rf ~/.gbrain/brain.pglite/.gbrain-lock ~/.gbrain/brain.pglite/postmaster.pid
systemctl --user restart gbrain-http.service
curl -i http://127.0.0.1:3131/health
```

After changing any client MCP config or recovering the service, restart the
affected client so it reloads MCP configuration.

## Configured Clients

Claude Code:

- Config files updated:
  - `~/.claude.json`
  - `~/.claude/settings.json`
- `gbrain` points to HTTP MCP, not the direct DB stdio wrapper.
- Relaunch Claude Code after config changes.

Codex:

- Config file: `~/.codex/config.toml`
- `gbrain` is configured as `streamable_http`
- URL: `http://127.0.0.1:3131/mcp`
- Bearer token env var: `MCP_GBRAIN_API_KEY`

Hermes:

- Config file: `~/.hermes/config.yaml`
- `gbrain` points to `http://127.0.0.1:3131/mcp`
- Token is stored via Hermes environment handling.

OpenClaw:

- Container: `openclaw-openclaw-gateway-1`
- GBrain URL from container: `http://host.docker.internal:3131/mcp`

## Verification Commands

Run these from WSL.

Check the GBrain HTTP service:

```bash
curl -fsS http://127.0.0.1:3131/health
```

Expected shape:

```json
{"status":"ok","version":"0.42.25.0","engine":"pglite"}
```

Check Hermes MCP:

```bash
hermes mcp test gbrain
```

Expected:

```text
Transport: HTTP -> http://127.0.0.1:3131/mcp
Connected
Tools discovered: 81
```

Check Codex MCP:

```bash
codex mcp get gbrain
```

Expected:

```text
transport: streamable_http
url: http://127.0.0.1:3131/mcp
bearer_token_env_var: MCP_GBRAIN_API_KEY
```

Check OpenClaw MCP:

```bash
docker exec openclaw-openclaw-gateway-1 openclaw mcp probe | grep -i gbrain
```

Expected:

```text
- gbrain: 81 tools
```

## Test Hermes Inside Ghostty

From WSL:

```bash
"/mnt/c/Program Files/winghostty/winghostty.exe" \
  -e wsl.exe -d Ubuntu --cd /home/shekerk/content-ideas -- \
  bash -lc 'source ~/.bashrc; hermes mcp test gbrain; echo; echo "Hermes-in-Ghostty test complete. Press Enter to close."; read'
```

Expected in the new Ghostty window:

```text
Transport: HTTP -> http://127.0.0.1:3131/mcp
Connected
Tools discovered: 81
Hermes-in-Ghostty test complete. Press Enter to close.
```

## Test Hermes Writes To Shared Memory

```bash
hermes chat -q "Use the gbrain MCP tool to write a page with slug 'hermes-ghostty-demo-2026-06-29'. Body exactly: '# Hermes Ghostty Demo\n\nHermes successfully used the shared GBrain HTTP MCP server from Ghostty setup on 2026-06-29.' Then reply with only the slug you wrote." --yolo
```

Then verify:

```bash
TOKEN="$(cat ~/.gbrain/shared-clients.token)"
curl -sS -X POST http://127.0.0.1:3131/mcp \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_page","arguments":{"slug":"hermes-ghostty-demo-2026-06-29"}}}'
```

## Hermes Web Dashboard

Hermes dashboard is separate from Ghostty. Ghostty is a terminal app; the Hermes
dashboard is a browser UI.

Check dashboard:

```bash
hermes dashboard --status
```

Known running endpoint:

```text
http://127.0.0.1:9119
```

The dashboard should use the same Hermes config and therefore the same GBrain MCP
server. In the browser, ask:

```text
Use gbrain get_page to read hermes-ghostty-demo-2026-06-29.
```

## Recovery

If a client cannot reach GBrain:

1. Verify the GBrain service:

   ```bash
   systemctl --user status gbrain-http.service --no-pager
   curl -fsS http://127.0.0.1:3131/health
   ```

2. Verify token export in a new shell:

   ```bash
   test -n "$MCP_GBRAIN_API_KEY" && echo token-loaded
   ```

3. Re-run the cutover script if needed:

   ```bash
   cd ~/content-ideas
   bash scripts/gbrain-shared-cutover.sh
   ```

4. Relaunch Claude Code, Codex, Hermes, or OpenClaw after config changes.
