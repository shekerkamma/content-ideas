# ai-graphics — reference

Deep detail the SKILL.md doesn't need inline. All findings verified live 2026-07-13.

## Design-reference sourcing: build-vs-buy decision (2026-07-13)

**Trigger:** user watched a video on Mobbin's MCP connector (621,500+ real UI screens,
searchable by Claude) and asked whether ai-graphics should integrate it.

**Decision: don't subscribe. Build the free equivalent instead — and it turned out
better for this skill's actual need.** Reasoning:

1. Mobbin costs $15/mo + requires OAuth-linking a personal account — a real spending
   and account-linking decision, not something to do silently mid-skill-build.
2. Mobbin's value is a *curated, cropped, tagged* database of UI *elements/screens*
   (buttons, modals, onboarding steps) — excellent for building actual app UI, but
   ai-graphics' domain is marketing graphics (infographics, flyers, social cards), where
   full-page live captures of real products are usually more useful than cropped
   element snippets.
3. The free alternative was already 90% built: `html_to_png.mjs` (built for Track A
   rendering) already accepted live `http://` URLs via Playwright — it just needed a
   `--full` (full-page) flag and a wrapper. Total new code: one flag + one ~70-line
   script (`capture_reference.py`).
4. Tried the "free" gallery aggregators first (Nicelydone, Page Flows, DivByZero,
   SaaSFrame, SaaSUI) — **every one of them gates the actual screenshots behind their
   own free signup.** Same friction as Mobbin, zero subscription fee, still a wall.
   Verdict: skip aggregators entirely, capture the real product's own live page instead.

**Result:** `capture_reference.py` — point it at any real product URL, it screenshots
the live page via Playwright (no login, no paywall, no rate limit beyond politeness),
crops to a bounded `Read`-able height, and catalogs it into
`assets/references/<category>/`. Verified same-session with three real captures (Linear
dark dashboard, Stripe gradient hero, Notion pricing) — all pixel-perfect, all free.

**When Mobbin would actually be worth it:** if ai-graphics' scope expands to building
real app UI (dashboards, in-product flows, not marketing graphics) at volume, Mobbin's
MCP surface would outperform hand-picking product URLs. Confirmed by watching the demo
video with actual video frames (not just transcript, 2026-07-13 — see below): its tool
is exactly three search granularities — `search_screens` (single screen by
plain-language description, iOS or web), `search_flows` (multi-screen sequences, e.g. a
full checkout or onboarding flow), `search_sections` (component/section level). That
`search_flows` tool is the specific piece nothing here replicates — it's the systematic
multi-screen-sequence capture that's structurally hard to get from one-off page
captures, whether via Exa+direct-capture or Awwwards. Revisit then — don't re-litigate
this decision for the current marketing-graphics scope.

## Watching the Mobbin demo video with frames, not just transcript (2026-07-13)

First pass (used to write the decision above) was transcript-only — yt-dlp's default
video download hit a 403. Fixed for future `/watch` runs on this machine: `yt-dlp -U`
(self-update; was 3 weeks stale) then retry — the stale version was the actual cause,
not a fundamental block. No special flags needed after updating; the skill's own flow
worked normally once yt-dlp was current.

Frames confirmed/refined the transcript in ways worth knowing if this decision is ever
revisited: the video's running example is the creator's own product ("Rivet", a
YouTube analytics co-pilot) reworked through all three Mobbin workflows — the "3
references" output was concretely named on-screen ("Electric Violet" from Lemon
Squeezy, "Night Sky" from Zapier, "Neo-Brutalist" from Gumroad); the missed-screens
demo really did produce a "Connect your channel" onboarding screen matching the
transcript's QuickBooks/Fiverr/Evernote claim. One validating aside: the creator hit
the identical viewport-vs-full-page screenshot problem this skill's `--full` flag
solves ("Confetti firing mid-screenshot is charming, but I only got the viewport") —
independent confirmation this is a real, common gotcha in AI-driven page capture, not
an artifact of this implementation specifically.

## Two discovery sources, two registers

The library has two distinct flavors, sourced differently:

- **Product/SaaS register** — Exa search for the pattern (e.g. "dark mode SaaS
  dashboard"), pick a real product URL, capture directly. Aggregators
  (Nicelydone/PageFlows/DivByZero/SaaSFrame) gate behind free signup — skip them.
- **Creative/bold/award-winning register** — **awwwards.com is not a trap, unlike the
  SaaS aggregators.** Its listing/category pages are freely browsable (verified
  2026-07-13, no signup wall), and each `/sites/<slug>` detail page links to the real
  live site (e.g. Longbow's Awwwards page → `https://db-longbow.webflow.io/`, found in
  the page's "Elements" section / footer link). Fetch the Awwwards detail page first to
  extract the outbound URL, then capture that URL — never the Awwwards page itself
  (it's just scores and metadata, no useful screenshot). Verified with one real capture:
  `assets/references/creative-bold/longbow.png` — bold display type, cinematic product
  photography, dark editorial tone.

## Awwwards structure — three surfaces, not one (verified 2026-07-13)

Prompted by: does Awwwards support the same 3 workflows the Mobbin video demonstrated
(rework a design / find missed screens / generate standout components)? Tested each:

1. **Whole sites** (`/sites/<slug>`) — outbound live-site URL is plain crawlable text on
   the page (proven: Longbow → `db-longbow.webflow.io`). Powers workflow A (rework).
2. **Category-browsable elements** (`awwwards.com/elements/<category>/` — real
   categories seen: `footer`, `pricing_page`, `menu`, `ui_components`, `forms`, and
   more) plus **free-text search** (`awwwards.com/elements/?text=<query>`) — both real,
   unwalled, no signup. This is the strongest match to Mobbin's per-element model and
   powers workflow B (standout components) well.
3. **Individual element pages** (`/inspiration/<slug>`) — do **not** reliably expose
   the outbound URL as text (tested on a pricing-page element: no plain-text link in
   the extracted content, unlike `/sites/` pages). The "visit site" link is DOM/button-
   rendered. **Two-hop workaround, verified:** read the element page for the
   brand/project name (e.g. "Raven Health Pricing Page") → Exa-search
   `"<brand> official website"` → capture the resulting real URL. Confirmed end-to-end:
   Raven Health → `ravenhealth.com/pricing/`.

**Workflow C (find missed/forgotten screens) is a real, unclosed gap.** Free-text
search quality varies sharply by pattern glamour: `?text=onboarding` returned strong
tagged hits (full-screen onboarding forms, modals, carousels — visually substantial,
agencies submit these for awards); `?text=empty%20state` returned mostly unrelated
noise (hover/idle/error states) because empty states are rarely visually impressive
enough to be *award-submitted*. Mobbin's actual moat is systematic per-app screen
coverage regardless of visual glamour — it captures the boring delete-confirm modal
because it's really in the app, not because it won an award. Don't claim Awwwards
replicates this; it doesn't, structurally, and no amount of clever searching fixes a
corpus that's selection-biased toward craft over completeness.

**Motion-heavy site gotcha (Awwwards sites especially):** a static screenshot freezes
whatever animation state was showing. `--settle 1500-2500` on `capture_reference.py`
fixes one-shot entrance animations (fades, reveals) but **not** continuously-looping
elements (marquee ticker text, infinite carousels) — there is no resting frame to wait
for. Tested live: Longbow's giant "LONGBO" headline stayed identically clipped before
and after a 2.5s settle, confirming it's a loop, not a transition. Two honest options
when this happens: accept the clip (the photography/type/color/layout signal is still
valid), or recognize that oversized edge-cropped display type is itself a real,
common Awwwards-style design device — not necessarily a capture failure at all.

## A 4th generic default — prose guidance alone isn't enough (verified 2026-07-13)

**Finding:** `frontend-design`'s calibration section names three "generic AI design"
defaults to avoid (cream+serif+terracotta; near-black+neon; broadsheet columns). A
Track A original design (no reference, no capture — pure written-guidance-only) was
built for a 6-card "AI Agent Patterns" infographic, deliberately avoiding all three
named defaults. User feedback: "this does not look good at all." Correct — it had
landed on a **4th, unnamed default**: pale blue-gray background + white cards + one
saturated blue accent + system sans. This is arguably the single most common
AI-generated / Tailwind-default-shadcn SaaS look in 2026, just not one frontend-design
named explicitly. Self-critique confirmed the failure: the "signature element" (9px
crosshair corner-ticks) was invisible at delivery size — a signature element that
can't be seen in a normal glance isn't functioning as one.

**Fix, and the real lesson:** rebuilt the identical content grounded in one real
Awwwards capture (`assets/references/creative-bold/kriss-ai.png` — Kriss.ai, SOTD
7.45, an actual AI healthcare product) instead of prose alone. Result was immediately,
visibly more distinctive: warm greige-mauve gradient (`#c9bec0`→`#b8a7aa`, confirmed by
direct RGB sampling — see channel-bias note below) instead of cold blue-gray; large
bold ghost-numeral watermarks + corner brackets as the signature device (visible, not
9px); a restrained rust accent instead of saturated blue. Side-by-side pair:
`assets/fail-generic-original-design.png` (the rejected v4) vs
`assets/success-awwwards-grounded-original.png` (the fix) — read both when calibrating
"does this look distinctive or generic."

**The generalizable rule:** for original (no-reference) requests, prefer grounding the
`frontend-design` plan in one real Stage-0 capture over prose-guidance alone. A real
capture forces concrete, specific choices (actual sampled hex, actual scale of a real
signature device) that pure description tends to default back toward safe/common
patterns. Prose-only guidance is a fallback for when a quick capture genuinely isn't
feasible, not the default path.

**Signature-element sizing rule (concrete, checkable):** if you can't spot the
signature element in a quick glance at final delivery size, it isn't one. Kriss.ai's
brackets are ~18px at 1440px viewport width (~1.25% of width) and immediately legible;
the failed attempt's crosshair ticks were 9px (~0.6%) and invisible. Scale signature
devices boldly, not subtly.

**Near-neutral ≠ truly flat — channel-bias check.** `extract_palette.py`'s
saturation-gated accent pass correctly reported "none found" for Kriss.ai's background
(true at its 0.20 threshold — the warmth is subtle). But direct RGB sampling at 4
points showed a consistent R−B bias of 8–14 (e.g. `#c9bec0`: R201 G190 B192) — a real,
consistent warm grade, not noise. This is genuinely different from Linear's dashboard
(0 channel bias, truly flat gray) and was visually perceptible as "warm mauve" before
the numbers confirmed it. When the saturation pass returns empty on a background
that reads as warm/cool by eye, sample raw RGB at a few points and check for a
consistent R vs B (or R vs G) offset before concluding "truly neutral" — subtle
temperature is real design signal the saturation gate alone won't catch.

## Reference-sourcing recipe

```bash
# 1. find a real product URL (Exa search, not a gallery aggregator)
# 2. capture it
python3 ~/.claude/skills/ai-graphics/scripts/capture_reference.py \
  --url https://linear.app --category dashboard-dark --brand linear \
  --note "dark SaaS product UI, sidebar nav + issue detail + AI panel" \
  --size 1440x900 --max-height 2800
```

Notes:
- Full-page captures run 7,000–15,000px tall (a real homepage scroll) — always crop
  with `--max-height`, or the saved PNG won't `Read` legibly. 1600–2800px covers
  hero + first fold; go higher only for a specific lower-page pattern (pricing tables,
  footers).
- `html_to_png.mjs` sends a real desktop Chrome user-agent (added alongside `--full` —
  some sites serve degraded markup to obvious headless-browser UAs).
- Bot-defended sites may still fail (timeout or block) — same failure class as the
  YouTube-video-download 403 hit earlier this session. Not every URL will capture;
  that's fine, try a different real product with a similar look.
- `assets/references/catalog.md` is append-only, one line per capture — grep it before
  a new capture to check for an existing match.

## OmniRoute image API

- Endpoint: `POST http://localhost:20128/api/v1/providers/{provider}/images/generations`
- No auth needed from localhost for generation. Body (OpenAI images shape):

```json
{"model":"codex/gpt-5.5","prompt":"<design spec>","n":1,"size":"1024x1536","quality":"medium"}
```

- Response: `{"created": ..., "data": [{...}]}` where the image is either
  `data[0].b64_json` (nvidia, JPEG) or `data[0].url` as a `data:image/png;base64,...`
  URL plus `data[0].revised_prompt` (codex, PNG with C2PA metadata).

## Provider status matrix (probed 2026-07-13)

| Provider | Image driver | Models | Notes |
|---|---|---|---|
| codex | ✅ | `codex/gpt-5.5` (`type:image` in catalog) | ChatGPT subscription; honors size (3 options); strong typography. `gpt-5.6` REJECTED upstream: "not supported when using Codex with a ChatGPT account" |
| nvidia | ✅ | `flux.1-dev` ✅, `flux.1-schnell` ❌ (upstream error on test), `flux.1-kontext-dev` (edit, untested), `flux.2-klein-4b` (untested) | clamps to 1024×1024 |
| comfyui | ✅ driver | `flux-dev`, `sdxl` | "fetch failed" until local ComfyUI app runs |
| zenmux | ❌ | catalog lists `openai/gpt-image-2`, `gpt-image-1.5` | "Unknown image provider: zenmux" — unreachable |
| command-code | ❌ | chat only (Claude/GPT) | |
| cloudflare-ai, ollama-cloud, cursor | ❌ | — | |

## Checking for new models (do this instead of assuming)

Catalog and providers endpoints need auth. Read the key inside PowerShell — never echo it:

```bash
powershell.exe -NoProfile -Command "
\$key = (Get-Content 'C:\Users\sheke\OmniRoute\.env' | Where-Object { \$_ -match '^OMNIROUTE_API_KEY=' }) -replace '^OMNIROUTE_API_KEY=',''
Invoke-RestMethod -Uri 'http://localhost:20128/api/models/catalog' -Headers @{ Authorization = ('Bearer ' + \$key.Trim()) } |
  ConvertTo-Json -Depth 8 -Compress | Set-Content -Encoding utf8 'C:\Users\sheke\AppData\Local\Temp\or-catalog.json'"
```

Then parse `/mnt/c/Users/sheke/AppData/Local/Temp/or-catalog.json` (`utf-8-sig`!):
`catalog.<provider>.models[*]` — image models have `"type": "image"` (but zenmux's
gpt-image entries are mistagged `"chat"`, and driver support is separate from catalog
presence — always end with a live 1-image probe).

The MCP tool `omniroute_list_models_catalog` returns 401 (needs the same auth the MCP
client doesn't send). The CLI (`omniroute api models ...`) renders `[object Object]`
tables. Hence the PowerShell recipe.

## Design-spec worked example (produced a zero-typo render first try)

```
Render this design specification exactly as a whiteboard-style infographic image.

DESIGN SPEC
Canvas: vertical portrait poster, clean white dry-erase whiteboard background, subtle marker texture.
Style: hand-drawn dry-erase marker illustration; black, red and blue marker ink; neat legible
marker handwriting; every word spelled exactly as specified.

LAYOUT (top to bottom):
1. HEADER — bold black marker lettering, two lines, centered:
   Line 1: "3 REASONS TO REPLACE SaaS"
   Line 2: "WITH AI-BUILT TOOLS"
   A single hand-drawn blue underline beneath the header.
2. ROW 1 — a black hand-drawn circle containing the numeral "1"; beside it a red dollar-sign
   doodle with a small downward-trending curve; label in red marker: "CUT RECURRING COSTS"
3. ROW 2 — ... numeral "2"; blue padlock doodle; label in blue marker: "OWN YOUR SOFTWARE"
4. ROW 3 — ... numeral "3"; red puzzle-piece doodle; label in red marker: "BUILT EXACTLY FOR YOU"
5. FOOTER — small black marker arrow pointing right with the words "START SMALL. BUILD ONE TOOL."

RULES: exactly three numbered rows, no extra rows, no extra text, no logos, no watermark;
all spelling must match the spec exactly.
```

Contrast: three raw-prompt FLUX attempts each produced typos ("AI-BULT", "RECURENCE")
or phantom rows. The spec structure + gpt-image is what fixed it, not prompt luck.

## Platform size cheat sheet

| Platform | Post type | Canvas |
|---|---|---|
| LinkedIn | portrait post | 1080×1350 |
| LinkedIn | link/landscape card | 1200×627 |
| Twitter/X | in-stream image | 1600×900 |
| Instagram | portrait | 1080×1350 |
| Instagram | square | 1080×1080 |
| Stories/Reels cover | vertical | 1080×1920 (pad from 1024×1536) |

gpt-image renders only 1024×1024 / 1024×1536 / 1536×1024 — always render the nearest
orientation, then `--canvas WxH` pads with the sampled background color.
