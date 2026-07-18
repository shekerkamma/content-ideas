# WSL execution blockers (verified 2026-07-16)

Read this **before** attempting Genspark generation from Claude Code on WSL.
Every row below was tried and failed on 2026-07-16. Do not re-litigate them.

## What actually blocks generation

| Path | Outcome |
|---|---|
| Headless Playwright Chromium → `genspark.ai/ai_slides` | **Cloudflare bot-check** interstitial: "Performing security verification… protect against malicious bots". The homepage loads fine; `/ai_slides` does not. |
| Headed Playwright Chromium (WSLg; `DISPLAY=:0` works) | Passes Cloudflare, but the page renders **"Sign in / Sign up"** — not authenticated. |
| Copy Windows profile `C:/Users/sheke/.codex/genspark-browser-profile-9333` → WSL | **Cookies do not decrypt.** Chrome binds its cookie store to an OS key (Windows DPAPI); a Linux Chromium cannot read it. Structural, not a bug. |
| Fresh Google sign-in inside an automated browser | **Google blocks it** — "this browser or app may not be secure". This is a deliberate anti-automation security control. **Do not attempt to defeat it.** |
| Windows toolkit `C:/Users/sheke/.codex/genspark-gen/generate.mjs` | **Blocked when WSL interop is off** (see below). |

## The root cause: WSL interop

Check first — it explains most failures in one command:

```bash
ls /proc/sys/fs/binfmt_misc/WSLInterop   # missing => interop is OFF
```

When it's missing, **no Windows binary can execute from WSL at all** — not
`cmd.exe`, `powershell.exe`, `explorer.exe`, nor Windows `node`. That kills the
Windows Genspark toolkit *and* things like `powershell.exe Start-Process <file>`.

**Unlock:** add to `/etc/wsl.conf`:

```ini
[interop]
enabled=true
```

then `wsl --shutdown` from Windows PowerShell and reopen. After that, the existing
Windows toolkit (`generate.mjs` + `capture.mjs`, Windows node + Windows Chrome +
the authenticated persistent profile) runs as designed — that setup worked on
2026-07-03.

## Traps that waste time

- **The genspark.ai homepage looks logged-in when it isn't.** It renders a
  workspace-style sidebar (New / Home / Skills / Workflows / Drive) to logged-out
  visitors too. **Never** treat that nav as proof of auth. Check `/ai_slides` for
  "Sign in / Sign up" instead.
- **A copied profile "succeeds" misleadingly** — it copies ~217MB, launches without
  error, and renders pages. The cookies are simply undecryptable ciphertext. Auth
  silently isn't there.
- **The stale selector.** `generate.mjs` targets `textarea, input[type="text"]`.
  Genspark's UI is now "AI Slides 5.0" / "Workspace 4.0" and that selector matches
  nothing (it finds only a hidden input). Re-probe selectors before assuming the
  driver is current.

## Working alternatives when generation is blocked

1. **Sheker generates in his own normal Windows browser** and hands over the
   project/viewer URL. Capture + editable rebuild then run locally with no auth
   problem. This is the fastest unblock.
2. **Skip Genspark entirely** — author `deck.html` against `genspark-branded-deck`'s
   archetypes and render locally with WSL Playwright Chromium. Credit-free, no auth,
   no Cloudflare. Correct choice whenever the content is already written and there's
   nothing for Genspark's AI to add.

## Capture returns HTML, not pixels

Contrary to an older note: `https://public.gensparkspace.com/api/files/s/<id>?pageIndex=N&scale=1`
returns **real HTML** (~15KB/slide, real CSS, zero `<img>` tags, extractable text) —
verified across 25/25 slides in `runs/2026-07-16-genspark-branded-deck/capture/`.
Genspark's *own PPTX export* is image-only; the **recovered HTML is not**. Those are
different exits — don't conflate them.
