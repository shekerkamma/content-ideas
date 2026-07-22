# WSL and Windows browser boundary

Read this before attempting Genspark generation or recovery from WSL. Treat
historical outcomes as evidence, not permanent configuration. Re-run the short
checks before choosing a browser lane.

## Current verified state (2026-07-22)

- Windows interop works: `powershell.exe` can run from WSL.
- `genspark.ai` resolves in both WSL and Windows.
- WSL HTTPS reaches Genspark successfully.
- Windows Chrome listens on CDP port `9222`.
- WSL cannot reach Windows Chrome through `127.0.0.1:9222`.

This is currently a Windows/WSL browser-boundary problem, not a DNS failure. A
Windows process can connect to Windows loopback; a WSL process cannot assume it
can.

## Diagnose before choosing a lane

```bash
test -e /proc/sys/fs/binfmt_misc/WSLInterop && echo interop-on || echo interop-off
getent ahosts genspark.ai
curl -I --max-time 20 https://genspark.ai/
curl --max-time 3 http://127.0.0.1:9222/json/version
```

Interpret the results separately:

| Check | Meaning |
|---|---|
| DNS lookup fails | Resolver/network problem; browser configuration is not the fix |
| HTTPS returns a status | DNS and routing worked; `403` may be bot/auth/method policy |
| Interop is off | WSL cannot start Windows browser tooling |
| Windows CDP listens but WSL loopback fails | Run the MCP process on Windows or expose a deliberate bridge |
| Viewer shows sign-in | Authentication/profile problem, not DNS |

If interop is disabled, add this to `/etc/wsl.conf`:

```ini
[interop]
enabled=true
```

Then run `wsl --shutdown` from Windows PowerShell and reopen WSL.

## Authentication constraints

- Headless Chromium may trigger Genspark/Cloudflare verification even when the
  homepage loads.
- A copied Windows Chrome profile does not provide Linux authentication because
  Windows cookies are encrypted with Windows credentials.
- Google may reject sign-in from an automated browser. Do not attempt to bypass
  that control.
- A normal Windows Chrome profile can retain Genspark authentication when the
  browser and cookie store stay on Windows.

## Preferred routing

1. Use the Genspark AI Slides connector for generation.
2. Use Windows-authenticated Chrome for gated viewer recovery. Connect through
   Chrome DevTools MCP or Playwright extension mode running on Windows.
3. Use WSL Playwright Chromium for public viewers and local HTML rendering.
4. If the connector or authenticated viewer is unavailable, continue from
   validated source content with `genspark-branded-deck`.

Do not repeatedly launch local headed/headless browsers after the diagnosis has
identified an OS/profile boundary.

## Capture semantics

`https://public.gensparkspace.com/api/files/s/<id>?pageIndex=N&scale=1` can
return complete slide HTML rather than pixels. Genspark's own PowerPoint export
may still be image-based. Treat recovered HTML as a reference/source surface and
rebuild branded or native deliverables through the compound pipeline.
