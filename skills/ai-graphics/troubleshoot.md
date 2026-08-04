# ai-graphics — troubleshooting

Every error below was hit and solved live on 2026-07-13. Match the symptom, apply the fix.

## Server / transport

| Symptom | Cause | Fix |
|---|---|---|
| Connection refused on :20128 from **WSL** (`curl localhost:20128`, `omniroute_get_health` MCP tool), but `omniroute doctor` on the **Windows** side reports the server reachable | **Not actually down.** WSL2's `localhost`→Windows port-forwarding silently doesn't reach this server (binding/interface gap, not a WSL-wide outage — plain `curl https://google.com` still works). The server is genuinely up. | Find the WSL gateway IP: `ip route show \| grep default` (e.g. `172.20.112.1`). Then `export OMNIROUTE_BASE_URL="http://<gateway-ip>:20128"` before `preflight.py` / `omniroute_image.py` / any direct curl. Verified 2026-07-23: preflight went FAIL→ALL PASS purely by swapping the base URL, no server restart needed. **Diagnose first**, always: run `powershell.exe -NoProfile -Command "omniroute doctor"` — if it says "Server reachable", the server is fine and this is the fix; only chase an actual restart if doctor also reports the server down. |
| `omniroute doctor` itself also reports the server down/unreachable | OmniRoute server genuinely not running | restart the Windows-side server; re-run `omniroute doctor` to confirm before touching the WSL gateway-IP workaround above |
| `codex` image driver: `Codex credentials missing accessToken - reconnect the Codex provider` | OmniRoute's codex/gpt-image adapter has a stale/disconnected OAuth token — separate from the ChatGPT/Codex CLI subscription's own usage limit (see below) | Fall back to `--provider nvidia --model nvidia/black-forest-labs/flux.1-dev` for the same request; only reconnect the codex provider if the user specifically needs gpt-image's typography/spec-following strength |
| `codex exec` (the direct CLI image_gen bridge, not OmniRoute) returns `ERROR: You've hit your usage limit... try again at <date>` | ChatGPT/Codex account-level usage cap exhausted — this is a hard quota, not a transport bug; every retry fails identically until reset | Do not retry this path. Switch providers entirely: OmniRoute `nvidia` driver, or the CLIProxyAPI Gemini route below. Report the reset date to the user rather than silently downgrading output quality by retrying. |
| `AUTH_001 Authentication required` (401) | catalog/providers endpoints need auth (generation does not) | Bearer-key recipe in [reference.md](reference.md) — read `OMNIROUTE_API_KEY` inside PowerShell, never echo it |
| CLI prints `[object Object]` tables | CLI renderer flattens JSON; no `--json` flag exists | never use the CLI for payloads — direct `Invoke-RestMethod` POST (the script does this) |
| `json.decoder.JSONDecodeError` on response | PowerShell `Set-Content -Encoding utf8` writes a BOM | open with `encoding='utf-8-sig'` |

## CLIProxyAPI Gemini route (separate service, port 8317)

| Symptom | Cause | Fix |
|---|---|---|
| `Cannot reach CLIProxyAPI at http://127.0.0.1:8317/v1/models: [Errno 111] Connection refused` | The CLIProxyAPI binary is installed but **not started** — it doesn't run as a persistent service by default | Start it: `cd ~/cliproxyapi && nohup ./cli-proxy-api --config config.yaml > /tmp/cliproxyapi.log 2>&1 &`. Config/binary live at `~/cliproxyapi/config.yaml` and `~/cliproxyapi/cli-proxy-api` (symlink to the versioned build, e.g. `~/cliproxyapi/7.2.86/`). Confirm with `python3 ~/content-ideas/skills/image-generation-router/scripts/generate_gemini.py --probe` → `CLIProxyAPI ready; selected image model: gemini-3.1-flash-image`. Unlike OmniRoute, this one genuinely is just "not running," not a networking gap — plain `127.0.0.1` works fine once started (it's a native WSL process, not a Windows-side service). |
| `HTTP 429: You have exhausted your capacity on this model. Your quota will reset after <Nh Nm>` | Free/OAuth-tier per-model quota on gemini-3.1-flash-image | No alternate image model on this proxy (`--list-models` returns only the one). Wait for reset, or switch to OmniRoute `nvidia` driver for the remaining images in the batch — don't block the whole deliverable on one exhausted route. |
| Need **image-conditioned** generation (recreate a reference image's composition, not just describe it in words) | Neither `omniroute_image.py` (OmniRoute) nor the stock `generate_gemini.py` (CLIProxyAPI) accept a reference image — both are text-prompt-only | Use `skills/image-generation-router/scripts/generate_gemini_img2img.py --ref <img> --prompt-file <spec.txt> --out <out.png>` (content-ideas repo). Same auth/model-selection as `generate_gemini.py`, but POSTs a multimodal `content: [{type:"text",...},{type:"image_url",image_url:{url:"data:image/png;base64,..."}}]` array — the OpenAI-compatible vision message format CLIProxyAPI accepts. Verified working against gemini-3.1-flash-image, 2026-07-23. Always instruct explicitly to omit every word/label/number visible in the reference; text-heavy references (data-labeled diagrams) still came out clean with a strongly worded "ignore all text" instruction. |

## Generation errors (read the error body — it names the layer)

| Error message | Meaning | Fix |
|---|---|---|
| `Unknown image provider: <p>` | provider has NO image driver (zenmux, command-code, cloudflare-ai, ollama-cloud) | route to codex / nvidia / comfyui |
| `The '<m>' model is not supported when using Codex with a ChatGPT account` | model doesn't exist upstream — this is how `gpt-5.6` was disproven | list catalog for real ids; probe, don't assume |
| `Image generation provider error` (upstream_error) | model catalogued but upstream rejects it (`flux.1-schnell` on test day) | switch model (`flux.1-dev`); re-probe occasionally |
| `Image provider error: fetch failed` (comfyui) | driver is wired but local ComfyUI app not running | start ComfyUI or route elsewhere |
| Output is 1024×1024 despite requested size | nvidia driver clamps; ignores `size`/`width`/`height` | generate square, fix aspect with `--canvas` |

## Screenshot track

| Symptom | Cause | Fix |
|---|---|---|
| `Executable doesn't exist at .../chromium_headless_shell-12xx` | bare `npx playwright` resolved a newer version than the cached browsers | use `scripts/html_to_png.mjs` (finds cached full chromium; note binary is under `chrome-linux64/`, not `chrome-linux/`) |
| `ERR_MODULE_NOT_FOUND: playwright` | playwright isn't global | script resolves it from `$PLAYWRIGHT_ROOT` (default `~/content-ideas`); point it at any repo with playwright installed |
| Labels overlap arrows/boxes in render | coordinate collision | edit the HTML coordinates and re-screenshot — never regenerate; this is the point of the code track |
| Bare call to `html_to_png.mjs` (no `--full`/`--settle`) fails with usage error | regression from `--settle` support: when `--settle` is absent, `indexOf` returns -1, and `-1 + 1 = 0` collided with a real arg index, silently dropping the first positional arg | fixed 2026-07-13 (guard the exclusion on `settleIdx >= 0`) — if this resurfaces, check that guard first |
| Grid-of-cards has large dead space between description and stat/divider | `flex:1` (or an oversized grid track) gives the card far more height than its 1-2 line content needs | don't just center-pad it — first check if the grid itself is oversized (too few rows / too much `flex:1` area), fix row count first, THEN scale up type/icon size to genuinely fill the corrected card size. Centering alone (`justify-content:center`) redistributes but doesn't remove excess dead space. |

## Quality failures

| Symptom | Cause | Fix |
|---|---|---|
| Typos / phantom rows in rendered text | text sent through FLUX, or spec not structured | wrong track: structured graphic → code; organic + text → gpt-image with a RULES line |
| Render "looks right" but content missing vs reference | lossy spec-writing (the 6-of-15 failure) | run the Reference Reproduction Protocol — counted inventory + QA diff |
| Output looks like generic AI design | no design plan for an original piece | read the `frontend-design` skill first; pick a signature element; avoid the three default looks it names |

## Reference capture (capture_reference.py)

| Symptom | Cause | Fix |
|---|---|---|
| Captured PNG is huge / `Read` truncates or looks wrong | full-page capture wasn't cropped | always pass `--max-height` (1600-2800 covers hero+first fold; the script bounds by default at 2800 but confirm it matches what you need) |
| `page.goto` timeout / capture fails on a specific site | bot defense, geofencing, or a slow SPA | try a different real product with a similar look; not every URL will capture — same failure class as the YouTube 403 hit earlier this session |
| Capture looks like a stripped-down/mobile layout | site serves degraded markup to headless-browser UAs | already mitigated by the desktop Chrome UA in `html_to_png.mjs`; if still degraded, the site may require JS interaction (scroll, click) beyond a plain page load |
| Gallery aggregator (Nicelydone/PageFlows/DivByZero/SaaSFrame) shows names but no real images | those sites gate screenshots behind their own free signup | don't fight it — go straight to the real product's own live URL instead |
| Capture shows oversized/clipped text mid-transition (e.g. giant headline cut off at frame edge) | motion-heavy site (GSAP/scroll-jacked), common on Awwwards — could be a genuinely looping element (marquee/ticker) with no resting frame | try `--settle 1500-2500` first (fixes one-shot entrance animations); if unchanged after settle, it's likely continuous motion — accept it, or judge whether it's actually an intentional design device (oversized edge-cropped type is a real Awwwards pattern) rather than a bug |
| Awwwards page itself has no real screenshot, just names/scores | you fetched an `awwwards.com/sites/<slug>` page directly instead of the linked live site | read that page's content for the outbound URL (near the title, or in an "elements" link) and capture THAT URL, never awwwards.com itself |
| `/inspiration/<slug>` element page has no crawlable outbound URL (unlike `/sites/` pages) | the "visit site" link is DOM/button-rendered, not plain text, on individual element pages | two-hop it: read the element page for the brand/project name, Exa-search `"<brand> official website"`, capture that result |
| Free-text `/elements/?text=<query>` search returns noisy/unrelated results for a pattern | Awwwards' corpus is selection-biased toward visual-craft award submissions, not systematic app-screen completeness — mundane utility patterns (empty states, delete-confirm modals) are thin | don't force it; this is a real, unclosed gap (Mobbin's actual advantage) — accept partial coverage or note the gap explicitly rather than presenting noisy results as good matches |

## Palette extraction (extract_palette.py)

| Symptom | Cause | Fix |
|---|---|---|
| "Accent colors: none found" on a UI screenshot you visually remember as colorful | either the crop region really is monochrome, or the region sampled doesn't include the colorful part | first check if it's a real finding (verified: Linear's dashboard hero genuinely has 0 pixels above the saturation+brightness gate); if not, narrow `--crop` to the specific colorful area |
| Naive saturation extraction (no brightness gate) reports "accent colors" that are actually near-black | HSV saturation is mathematically unstable at low brightness — `(max-min)/max` blows up for tiny RGB values like `#090a0b` | always gate on `--min-value` (default 0.15); never drop this filter chasing color in a dark UI |
| Dominant-color quantize on the WHOLE hero returns only near-black/near-white | background pixels vastly outnumber small accent icons/badges by area — naive by-pixel-count quantize drowns them | this is why the script does two separate passes (neutral ramp + saturation-gated accent) instead of one quantize call |

## Delivery failures

| Symptom | Cause | Fix |
|---|---|---|
| User can't open the file links | relative or `C:\` paths printed in chat (Remote-WSL treats them as external URLs) | copy out of scratchpad to a durable location, `code <absolute-wsl-path>`, print absolute WSL paths only |
