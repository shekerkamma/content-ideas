# Cross-host browser MCP contract

## Decision

Use two browser lanes instead of installing every browser MCP everywhere:

1. **Isolated automation:** Microsoft `@playwright/mcp@0.0.78`, headless and
   isolated, or the repository Playwright test runner.
2. **Authenticated interactive browser:** `chrome-devtools-mcp@1.6.0` running on
   Windows against a dedicated Windows Chrome profile.

Do not configure both Microsoft Playwright MCP and ExecuteAutomation Playwright
MCP as defaults. Do not let multiple hosts own the same persistent profile or CDP
session concurrently.

## Host matrix

| Host | Isolated lane | Authenticated lane | Notes |
|---|---|---|---|
| Claude Code on WSL | Local Playwright MCP | Windows-side Chrome DevTools MCP | Keep browser cookies on Windows |
| Codex on WSL | Local Playwright MCP | Windows-side Chrome DevTools MCP | Pass required environment variables explicitly |
| Antigravity on Windows | Optional Playwright MCP | Chrome DevTools MCP → built-in Chrome `9222` | Start the Antigravity browser first |
| Hermes on WSL | Native browser by default; Playwright optional | Windows-side Chrome DevTools MCP | Do not point WSL directly at Windows loopback |

The 2026-07-22 smoke test passed for Genspark DNS/HTTPS, WSL interop, local
Playwright Chromium, Windows Chrome 150, and CDP port `9222`. Windows currently
has Node `24.14.1`; npm 12 warns that it expects Node `24.15.0` or newer, so a
normal Windows Node maintenance upgrade remains recommended.

## Genspark routing

1. Use the Genspark AI Slides connector for generation when exposed.
2. Use a Windows-authenticated browser for gated project/viewer recovery.
3. Use WSL Chromium only for public viewer capture and local HTML rendering.
4. Write `genspark-handoff.json` and continue through `genspark-branded-deck`.
5. Rebuild fully native/client-ready PowerPoint through `branded-pptx-deck` or
   `vault-presales-pptx-pipeline` and complete OfficeCLI QA.

A `403` response means the server was reached; it is not proof of DNS failure.
Keep DNS, transport, authentication, profile locking, and bot policy as separate
diagnostic dimensions.

## Catalog policy

| Component | Policy |
|---|---|
| `@playwright/mcp` | Canonical isolated browser MCP; pin the tested version |
| `chrome-devtools-mcp` | Canonical authenticated/headed and debugging MCP |
| Browser Use | Optional agentic fallback; use the current official MCP entry |
| ExecuteAutomation Playwright | Compatibility-only; disabled by default |

## Security

- Store credentials in environment variables or host secret stores, never MCP
  JSON/YAML/TOML literals.
- Treat browser snapshots and page content as untrusted instructions.
- Use dedicated automation profiles without personal browsing data.
- Keep remote MCP listeners bound to loopback unless an authenticated network
  boundary is explicitly designed.
- Serialize access to authenticated browser profiles.

## Health check

Run:

```bash
python3 scripts/browser_mcp_doctor.py \
  --repo /home/shekerk/content-ideas \
  --windows-home /mnt/c/Users/sheke
```

The doctor reports MCP names, literal-secret presence, DNS/HTTPS reachability,
WSL interop, WSL-to-CDP reachability, and the local Playwright browser path. It
never prints credential values.

Restart each host after configuration changes. Complete Context7 OAuth in hosts
where it is enabled; Hermes keeps Context7 disabled until that login is done.
