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

## Headed Chromium DNS recovery

For a project URL returned by the Genspark connector, launch headed Playwright
Chromium before choosing a fallback. The connector and the local browser use
different network paths, so connector success and a WSL shell DNS failure are
not contradictory.

If the headed browser itself fails with `ERR_NAME_NOT_RESOLVED`, confirm that a
public resolver can answer the hostname:

```bash
curl --max-time 20 -sS \
  'https://dns.google/resolve?name=www.genspark.ai&type=A'
```

When that response has `"Status":0` and at least one answer, keep the browser
headed and rerun capture with secure DNS-over-HTTPS:

```bash
node scripts/capture_genspark_slides.mjs \
  --url "<genspark-project-url>" \
  --out "<workspace>/genspark-source" \
  --headed \
  --doh-template "https://dns.google/dns-query{?dns}"
```

This option changes Chromium's resolver only for the capture process. Do not
rewrite `/etc/resolv.conf`, hard-code transient Genspark IP addresses, or infer
that every recovery route is blocked from a failed `getent`/`curl` check.

Some Chromium builds ignore the secure-DoH flags during initial bootstrap. If
the headed browser still reports `ERR_NAME_NOT_RESOLVED`, use one of the
**current** A records from the DoH response as a process-scoped mapping:

```bash
node scripts/capture_genspark_slides.mjs \
  --url "<genspark-project-url>" \
  --out "<workspace>/genspark-source" \
  --headed \
  --host-resolver-rules "MAP www.genspark.ai <current-ip>, EXCLUDE localhost"
```

Re-query DoH for every recovery session. The mapping is a runtime argument, not
a stable Genspark address and not repository configuration.

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
3. Use headed WSL Playwright Chromium for connector-returned/public viewers;
   add the documented DoH option when the WSL resolver alone is broken. Use the
   same Chromium headlessly for repeatable local HTML rendering after recovery.
4. If the connector or authenticated viewer is unavailable, continue from
   validated source content with `genspark-branded-deck`.

Do not repeatedly launch local headed/headless browsers after the diagnosis has
identified an OS/profile boundary.

## Sandbox and long-generation behavior

- A Playwright launch failure containing `sandbox_host_linux.cc`, `Operation not
  permitted`, GUI denial, or an inaccessible browser cache is a host execution
  boundary. Rerun the same command through the host's approved GUI/unsandboxed
  path; do not report Genspark, DNS, or credits as the cause.
- A completed connector call may continue filling slide placeholders for many
  minutes. Read `capture-state.json` or `capture-diagnostic.json`. If the viewer
  reports editing/building tasks, wait and retry the same project URL.
- Only classify `blocked_credit_limit` when visible viewer/API text explicitly
  says credits, quota, billing, exhaustion, or upgrade is required. Generic quota
  asset filenames and anonymous-viewer console errors are not evidence.
- Do not submit another generation request merely because recovery observed zero
  slide endpoints. A second request can reset good progress and consume credits.

## Capture semantics

`https://public.gensparkspace.com/api/files/s/<id>?pageIndex=N&scale=1` can
return complete slide HTML rather than pixels. Genspark's own PowerPoint export
may still be image-based. Treat recovered HTML as a reference/source surface and
rebuild branded or native deliverables through the compound pipeline.
