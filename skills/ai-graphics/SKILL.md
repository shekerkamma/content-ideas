---
name: ai-graphics
description: 'Use when someone wants a raster graphic, infographic, flyer, diagram, social card, visual insight, reference recreation, or design-token brief. Design-first: render structured or text-bearing graphics as deterministic HTML/SVG and route only eligible organic imagery to a host-native image tool or an explicitly selected provider adapter. For PPTX/deck work this skill is an execution dependency of pptx-visual-spec, not the deck builder.'
metadata:
  legacy-frontmatter:
    argument-hint: <what the graphic is about> [platform] [style]
    permissions:
      network:
      - http://localhost:20128
      - http://127.0.0.1:8317
      file_read:
      - ~/cliproxyapi/config.yaml
      file_write:
      - /mnt/c/Users/sheke/Pictures/
      - /mnt/c/Users/sheke/AppData/Local/Temp/
      shell:
        allowed_scripts:
        - scripts/omniroute_image.py
        - ~/content-ideas/skills/image-generation-router/scripts/generate_gemini.py
        - ~/content-ideas/skills/image-generation-router/scripts/generate_gemini_img2img.py
---

# ai-graphics — Design-First Raster Execution

Produce finished raster graphics (PNG/JPEG) for social posts, infographics, flyers,
and visual insights. The core method: **never send a raw prompt to an image model.**
Write a structured design spec first, then route it to the renderer that can honor it.

**Cost tier:** executor can be Sonnet-class. Codex built-in `image_gen` uses the signed-in
ChatGPT/Codex subscription and is separate from OmniRoute. Provider adapters have their own
quota/billing. Record the selected execution path rather than inferring cost from a model name.
The repo `image-generation-router` owns provider precedence: built-in OpenAI first, with
CLIProxyAPI Gemini only when explicitly requested or after disclosed built-in unavailability.

## Pipeline at a glance (each stage gates the next)

| # | Stage | Output | Gate — do not advance until |
|---|---|---|---|
| 1 | INTAKE | use case + format preset + track (A code / B image) | content type classified; reference image Read if supplied |
| 2 | DESIGN | design spec (B) or counted inventory + design plan (A) | every copy string quoted verbatim; A: counts stated; originals: `frontend-design` skill applied |
| 3 | RENDER | raw PNG (+ HTML template on track A) | script exits 0; expected dimensions |
| 4 | QA | reviewed PNG | Read the image; checklist/spec diff clean; Track B: ≤2 regenerations then switch strategy; Track A: no cap — edit the HTML and re-screenshot as many times as needed, it's free and deterministic |
| 5 | DELIVER | file in durable location, **opened** for the user | `code <abs-wsl-path>` ran; HTML template shipped beside PNG (track A); status stated: draft/reviewed |

**Supporting files:** [reference.md](reference.md) — API detail, provider matrix, catalog
recipe · [troubleshoot.md](troubleshoot.md) — every known error → fix ·
[examples/good.md](examples/good.md) — two verified worked specs ·
[examples/avoid.md](examples/avoid.md) — eight anti-patterns that actually failed ·
`assets/` — **visual calibration set, Read these** when judging quality:
reference→recreation pairs (`ref-editorial-diagram.png` → `recreation-editorial-diagram.png`,
`ref-dense-infographic.png` → `recreation-dense-infographic.png` — the target fidelity bar),
`fail-flux-typos.jpg` (what FLUX text failure looks like — plausible at a glance),
`success-gptimage-spec.png` (what a spec-driven gpt-image render achieves),
`fail-generic-original-design.png` vs `success-awwwards-grounded-original.png`
(prose-only original design vs the same content grounded in a real capture — read
both when calibrating "distinctive or generic") ·
`assets/references/<category>/` — **growing free design-reference library** (real
product captures, see Stage 0 above and [reference.md](reference.md) for the sourcing
strategy and the Mobbin build-vs-buy decision) ·
`templates/` — **proven HTML starters, adapt before writing from scratch**:
`editorial-diagram.html` (cream/serif node diagram, 1600×1000),
`dense-infographic.html` (7-section navy/purple infographic with icon library and
fixed-canvas flex layout, 1200×1800),
`card-grid-comparison.html` (blueprint-blue 2×3 numbered-card grid + 2-column
comparison table + footer CTA, mono-uppercase labels, crosshair corner-tick signature
element, 1200×1800 — verified 2026-07-13 pipeline test).

## Preconditions

Run the preflight — it verifies the entire chain in one free command (bogus-model probes;
generates nothing) and names any broken layer:

```bash
python3 ~/.claude/skills/ai-graphics/scripts/preflight.py   # --skip-server for Track A only
```

Checks: Windows temp bridge, server + images route, each image driver (codex/nvidia/comfyui),
playwright + chromium for Track A, Pillow. On FAIL → [troubleshoot.md](troubleshoot.md).
**Cadence:** once per session, before the first render — not before every render. Re-run
only after an environment change or an unexplained transport failure.

> **`OmniRoute server + images route` FAIL from WSL is very often not a down server.**
> WSL2's `localhost`→Windows port-forwarding can silently fail to reach this specific
> server even while it's genuinely running (`powershell.exe -NoProfile -Command
> "omniroute doctor"` reports it reachable). Diagnose with `omniroute doctor` first; if it
> says reachable, get the WSL gateway IP (`ip route show | grep default`) and
> `export OMNIROUTE_BASE_URL="http://<gateway-ip>:20128"` before re-running preflight —
> do not assume a restart is needed. Full recipe: [troubleshoot.md](troubleshoot.md).

> **Preflight tests reachability, not quota.** It probes each driver with a **bogus model**,
> so a driver that is rate-limited (429) or returning upstream 404 still reports **PASS** —
> preflight proves the wire is up, not that a real render will succeed. For Track B / hybrid,
> gate on the live status table in **[deck-image-routing.md](deck-image-routing.md)** and
> confirm with one real render before promising a generated asset. Track A (HTML/SVG) has no
> quota, so a green preflight is sufficient there.

For an explicit Gemini/Nano Banana request or disclosed built-in fallback, probe the separate
CLIProxyAPI route instead of OmniRoute:

```bash
python3 ~/content-ideas/skills/image-generation-router/scripts/generate_gemini.py --probe
```

- This is a **machine-specific skill** (this WSL2 + Windows box). Paths assume
  `/mnt/c/Users/sheke/...`; override via `OMNIROUTE_WIN_TEMP`, `OMNIROUTE_BASE_URL`,
  `PLAYWRIGHT_ROOT` env vars.

## Workflow

### 0. Reference sourcing (when no reference image is supplied)

If the user wants a specific look ("dashboard-y", "like a fintech landing page", "clean
SaaS onboarding") but hasn't pasted a reference image, don't guess from vibes and don't
reach for a paid design-reference MCP (Mobbin etc. — $15/mo, OAuth account-link,
evaluated 2026-07-13 and deliberately not installed). Source a real one for free instead:

1. **Check `assets/references/<category>/` first** — the library grows every time this
   step runs (see lifecycle below); a matching capture may already exist.
2. **Find a real live page — two discovery sources depending on register:**
   - **Product/SaaS register** (dashboards, pricing, onboarding, empty states) — Exa
     search (`web_search_exa`) for the category/style, picking an actual product URL.
     **Gallery aggregators are a trap:** Nicelydone, Page Flows, DivByZero, SaaSFrame
     all gate the real screenshots behind their own free signup — same friction as
     Mobbin, no fee, still a wall. Skip them.
   - **Creative/bold/award-winning register** (the `frontend-design` overlay's
     "signature element" and "one aesthetic risk" calls for this) —
     **awwwards.com is NOT a trap**, unlike the SaaS aggregators: its listing pages
     (homepage, `/websites/`, category pages) are freely browsable with no signup, and
     each entry's `awwwards.com/sites/<slug>` page links to the **real live winning
     site** (fetch the page, find the outbound site URL — often mid-page near the
     title, sometimes only visible as a footer/element link). Capture that real URL
     directly, never an Awwwards page itself.
3. **Capture it directly — free, no signup, no paywall:**
   ```bash
   python3 ~/.claude/skills/ai-graphics/scripts/capture_reference.py \
     --url https://example.com --category dashboard-dark --brand example \
     --note "what makes this useful as a reference" [--max-height 2800]
   ```
   Saves a bounded-height PNG + JSON metadata into `assets/references/<category>/` and
   upserts one line in `assets/references/catalog.md` (keyed by category/brand — a
   re-capture replaces its line, never duplicates). `--max-height` bounds the crop
   (full pages run 7,000–16,000px tall) so the result stays `Read`-able — 1600–2800px
   is a good hero/first-fold default; raise it if the pattern you need is further down.
   Add `--settle 1500`–`2500` for motion-heavy sites (common on Awwwards) to let
   entrance animations finish before the shot — but know its limit: a continuously
   looping element (marquee ticker text, infinite carousels) has no resting frame, so
   `--settle` won't fix it. Treat that as expected, not a bug: judge whether the
   "oddity" is actually the site's real design device (oversized, edge-cropped display
   type is a genuine, common Awwwards pattern, not always a capture glitch) before
   assuming the capture failed.
4. **Read the capture**, then feed it into the Reference Reproduction Protocol (below)
   exactly like a user-pasted reference image.

### Three named workflows (mirrors Mobbin's demonstrated pattern — tested against
Awwwards specifically, 2026-07-13; fit varies per workflow, don't assume uniform coverage)

- **A — Rework a generic-looking design.** ("find 3 great references for this app,
  build a sample page for each") Browse Awwwards whole sites (homepage, `/websites/`,
  category pages — freely browsable) for 2-3 real sites in the target register, fetch
  each `/sites/<slug>` page for its outbound live-site URL (reliably present as plain
  text there), capture each with `capture_reference.py`, then build one Track A variant
  per reference. **Verified good fit.**
- **B — Generate standout components to seed a design system.** ("5 UI components that
  are useful and visually arresting") **This is Awwwards' best-fit workflow, arguably
  better than A.** `awwwards.com/elements/<category>/` (footer, pricing_page, menu,
  ui_components, forms, ...) and `awwwards.com/elements/?text=<query>` are real,
  filterable, unwalled browsers built exactly for "give me N great examples of X
  component." **Two-hop capture required** — unlike `/sites/` pages, individual
  `/inspiration/<slug>` element pages render their outbound link as a DOM button, not
  crawlable text, so: read the element page for the brand/project name → Exa-search
  "`<brand>` official website" → capture that URL. Verified end-to-end: Awwwards
  "Raven Health Pricing Page" element → `ravenhealth.com/pricing/` →
  `assets/references/components-pricing/ravenhealth.png`.
- **C — Find UI patterns builders forget** (onboarding, empty states, delete-confirm
  modals, upgrade/payroll pages). **Weak, uneven fit — verified, don't oversell it.**
  Free-text search on visually-substantial patterns works: `?text=onboarding` returned
  strong, well-tagged real results (full-screen onboarding forms, onboarding modals,
  carousels). But `?text=empty%20state` returned mostly noise (hover/idle/error states,
  one loose "Empty Bag" match) — Awwwards' selection is inherently biased toward
  visual-craft award submissions, not systematic full-app-flow completeness. Mobbin's
  actual advantage here is real: it screenshots *every* screen of real shipped apps
  regardless of visual glamour, so the boring delete-confirm modal is present because
  it's part of the real product, not because someone submitted it for an award. **This
  gap is genuinely not closed** for mundane utility screens — if that specific need
  becomes frequent, that's the strongest case for reconsidering Mobbin, not A or B.

### 0.5. Trend-grounded design brief (optional — for "make this stand out" / "cutting-edge" requests, or slide-deck design grounding)

Most requests skip this — it's for when a graphic or deck needs to feel current and
deliberately non-generic, not for routine single-image asks (adds a research
round-trip; don't pay that cost when it isn't wanted).

**What it produces:** a design-token brief in this repo's `DESIGN.md` (Google Stitch)
shape — the same 4-section format already used at `content-ideas/DESIGN.md` and
consumed by `marp`'s theme `:root` block. This is deliberately an INPUT artifact, not
a finished deliverable — see Hand-off below. **ai-graphics still does not build decks
itself** (see frontmatter); this stage produces grounding that deck skills consume.

1. **Identify the vertical/register** (e.g., "fintech SaaS", "developer tool",
   "creative portfolio").
2. **Discover 2-3 real, current references** — Awwwards (whole-site or
   `/elements/<category>/`, per Stage 0) for creative/bold register, Exa-search +
   direct capture for product/SaaS register. Capture each with `capture_reference.py`.
3. **Extract real colors, don't eyeball them:**
   ```bash
   python3 ~/.claude/skills/ai-graphics/scripts/extract_palette.py <capture.png> --crop X,Y,W,H
   ```
   Two passes: neutral/background ramp (always produces output) and accent colors
   (gated on brightness — see Gotchas; an empty accent result on a near-monochrome
   source is a real finding, report "restrained/no color accent," don't force one).
4. **Read the capture(s)** for typography and component treatment — this part stays
   qualitative (font pairing, spacing philosophy, signature element), the script only
   grounds the color table.
5. **Assemble the brief** in the 4-section shape: Visual Theme & Atmosphere (prose) →
   Color Palette & Roles (table, real sampled hex) → Typography Rules → Component
   Stylings. Worked example: `assets/references/landing-hero/stripe-trend-brief.md`.

**Hand-off — three consumers, pick per request:**
- Single graphic → feed the brief into a Track A HTML/SVG spec's `Style:` line.
- Slide deck → write into the project's `docs/design.md`, or hand to `marp`/
  `branded-pptx-deck` directly. Sequential downstream relationship, not a merge.
- Full design system → hand to the `design-system` skill alongside the source capture.

### 1. Classify the request → format preset

| Use case | Size to request | Final canvas |
|---|---|---|
| LinkedIn/IG portrait post | `1024x1536` | 1080×1350 (4:5) |
| Twitter/X / LinkedIn landscape card | `1536x1024` | 1600×900 or 1200×627 |
| Instagram square / avatar-adjacent | `1024x1024` | 1080×1080 |
| Flyer / poster (print-ish) | `1024x1536` | keep 2:3 |
| Whiteboard explainer | `1024x1536` or square | per platform |

### 2. Write the DESIGN SPEC (the step that makes text come out right)

Build the prompt as a structured spec, not prose. Template:

```
Render this design specification exactly as a <style> image.

DESIGN SPEC
Canvas: <orientation, background, texture>
Style: <visual language, palette, lettering style>; every word spelled exactly as specified.

LAYOUT (top to bottom):
1. HEADER — <treatment>: "<exact copy>"
2. <ZONE> — <icon/doodle description>; label: "<exact copy>"
3. ...
N. FOOTER — <treatment>: "<exact copy>"

RULES: exactly <N> <rows/zones>, no extra rows, no extra text, no logos,
no watermark; all spelling must match the spec exactly.
```

Every piece of copy is quoted verbatim. If the user gave brand tokens (or a repo
`DESIGN.md` exists and they want brand-consistent output), fold its colors/typography
words into `Style:`. Apply `~/.claude/skills/voice.md` to the copy itself — titles are
verdicts, numbers beat adjectives.

**Reference file as design input:** when the user supplies a reference image (screenshot,
existing graphic, competitor visual), Read it and extract its design language —
background color/texture, typography family and weights, box/border treatment, accent
color and where it's used, arrow/connector style, annotation style. Then choose the track:

- **Track A — reference → CODE (default for structured graphics).** Reproduce the design
  system as self-contained HTML/SVG (sampled hex colors, system serif/sans stacks,
  explicit geometry), then screenshot at exact pixel dimensions. This is the superior
  path for diagrams, cards, flat infographics, and quote cards: pixel-exact colors,
  perfect text, any canvas size, and the HTML/SVG file is a **reusable editable
  template** — change copy, re-screenshot, done. **Follow the Reference Reproduction
  Protocol below** — the failure mode of this track is silently dropping content, and
  the protocol exists because a first attempt did exactly that (6 elements rendered
  from a 15-element reference).
- **Track B — reference → spec words → image model.** Fold the extracted style into the
  spec's `Style:` line and render via OmniRoute. Use only for styles code can't produce:
  hand-drawn marker, photographic scenes, painterly/organic texture. Note OmniRoute has
  **no `/images/edits` endpoint** (verified) — the reference file itself can't be sent
  to the model; for true image-to-image use `nano-banana edit_image` or `higgsfield`.
- **Hybrid — Track A shell + Track B slots.** A and B are not either/or. For a rich graphic,
  let **code own all structure and every glyph** and use the image model only for **text-free
  illustrative regions** (a hero texture, a scenic backdrop), composited into the HTML before
  the screenshot. Declare the route per element in the spec (`ROUTE: image|code`). Three
  constraints: assets are **text-free by construction**; **slot size is fixed** (gpt-image
  does only 1024², 1024×1536, 1536×1024 — plan the crop with `object-fit: cover`);
  **backgrounds aren't reliably transparent** — match the shell bg in the prompt or composite
  deliberately. The shell keeps unlimited free re-renders; only the slots are quota-bound.

> **Route status is execution-path specific.** Before promising Track B / hybrid, read
> [deck-image-routing.md](deck-image-routing.md) and confirm the selected route with a real
> render. Built-in Codex `image_gen` is independent of OmniRoute adapter quotas. Track A is
> deterministic and unaffected by image-provider status.

**Reference Reproduction Protocol (Track A, mandatory):**

1. **Inventory pass.** Before writing any code, enumerate from the reference:
   (a) every text string VERBATIM — title, headings, sublabels, captions, edge/arrow
   labels, annotations, footnotes; (b) every visual element — each node/box (fill,
   border style, corner treatment), each connector (direction, solid/dashed, curvature,
   single/bidirectional, self-loops), groupings, legends, accent usage. Write the
   inventory down as a numbered checklist and **state the counts** (e.g. "15 text
   strings, 13 connectors").
2. **Fidelity contract.** The code must contain every inventoried item; nothing may be
   summarized, merged, or invented. If the user wants a *simplified* version, that is a
   decision they make — never a silent default.
3. **Write the code data-first.** Define nodes/edges/labels as explicit lists (SVG
   elements or JS arrays), then lay out — this makes a dropped item visible as a
   missing list entry, not an invisible omission.
4. **QA diff.** Screenshot, Read the image, and tick off every checklist item against
   the render. Missing or overlapping items are coordinate/code fixes (cheap and
   deterministic) — fix and re-screenshot until the checklist is clean.
5. **Declared substitutions** — some reference elements must NOT be copied; substitute
   and say so in the verification report, never silently:
   - **Photos / real-person likenesses** → flat initials disc or neutral avatar. Never
     recreate a person's face.
   - **Brand logos** → typographic chip or placement block, not a counterfeit mark.
   - **Exact icon glyphs** → stylized SVG equivalents are acceptable; log as substitution.
   - **Proprietary fonts** → nearest system stack by default; offer webfont embedding
     if the user needs exact letterforms.
6. **Verification report** (delivered with the image): sections checked ✓, string count
   verified, declared substitutions listed, deviations listed, status (draft/reviewed),
   and render count **split by type** — Track A edit/re-screenshot passes (free, no
   cap) vs Track B image-model generations (costs credits, ≤2 per the retry budget).
   Don't report one combined number; it hides whether the budget was actually respected.
   Verified at scale: a ~60-string, 7-section, 35-icon infographic passed with 3 Track A
   renders and 2 one-line template fixes; a 6-card/comparison-table infographic passed
   with 4 Track A renders (0 Track B generations) fixing a layout defect.

**Original designs (no reference):** before writing Track A code, read and apply the
`frontend-design` skill (official plugin, installed) for the design plan — token system
(4–6 named hex values), deliberate type pairing, layout concept, one signature element —
then run steps 3–4 above. **Prose guidance alone is not enough — verified live, it
produced a 4th generic default** (see [examples/avoid.md](examples/avoid.md) #9 and
[reference.md](reference.md) "A 4th generic default"). **Prefer grounding the plan in
one real capture** (Stage 0's Awwwards/Exa sourcing) even for "original" requests —
treat pure-prose-only as a fallback for when a quick capture isn't feasible, not the
default path.

### 3. Route to a renderer (see Judgment rules to tune)

| Content | Renderer | Why |
|---|---|---|
| Structured/flat design: diagrams, cards, quote cards, data callouts, brand-token work, reference-matched layouts | **CODE: HTML/SVG → `scripts/html_to_png.mjs`** | deterministic, pixel-exact, any size, editable template |
| Organic style WITH text (whiteboard marker, sketch, painterly + typography) | `codex` / `codex/gpt-5.5` | gpt-image follows specs; spelling survives |
| Pure illustration, texture, scene, ≤4 short labels | `nvidia` / `nvidia/black-forest-labs/flux.1-dev` | look exploration |
| Edit an existing image (fix a word, restyle a region) | `nvidia` / `flux.1-kontext-dev`, or `nano-banana edit_image` MCP | targeted repair beats regeneration |
| Explicit Gemini/Nano Banana generation | `image-generation-router` → CLIProxyAPI live image model | user-selected Gemini route; runtime catalog is authoritative |

For the CODE track: **check `templates/` first** — if a starter matches the style family
(editorial diagram, dense infographic), copy and adapt it; its layout bugs are already
fixed and its icon library is reusable. Otherwise write a self-contained `.html` (inline
CSS/SVG, system font stacks, body sized to the target canvas), then:

```bash
node ~/.claude/skills/ai-graphics/scripts/html_to_png.mjs <file.html> <out.png> 1080x1350
```

Save the `.html` next to the `.png` — it IS the editable design artifact. The script
resolves Playwright from `$PLAYWRIGHT_ROOT` (default `~/content-ideas`) and falls back
across cached/system chromium builds.

Do NOT hardcode newer model names (verified: `gpt-5.6` does not exist upstream —
"not supported when using Codex with a ChatGPT account"). When checking for newer
models, list the live catalog (recipe in [reference.md](reference.md)).

### 4. Generate

```bash
python3 ~/.claude/skills/ai-graphics/scripts/omniroute_image.py \
  --provider codex --model codex/gpt-5.5 \
  --prompt-file /path/to/spec.txt --size 1024x1536 \
  --out <durable-path>/<name>.png [--canvas 1080x1350] [--quality low|medium|high]
```

The script handles the WSL→Windows transport, BOM parsing, both response shapes
(`b64_json` and `data:` URL), and `--canvas` scale-and-pad with sampled background color.

For explicit Gemini generation, keep the same design spec in a prompt file and run:

```bash
python3 ~/content-ideas/skills/image-generation-router/scripts/generate_gemini.py \
  --prompt-file <spec.txt> --out <durable-path>/<name>.png [--model <live-model-id>]
```

Never fall through from a missing Nano Banana Pro model to a Flash image model. The router
checks authenticated `/v1/models`, writes a provenance sidecar, and stops on absent models.

### 5. QA — read the image before delivering

Open the output with the Read tool and check, against the spec: every word spelled
correctly, zone count matches, no phantom rows, no watermark. If it fails: one targeted
retry (tighten the RULES line, shorten copy), then prefer an edit-model repair over a
third regeneration. Never deliver unreviewed.

### 6. Deliver

- Save to a durable location: `/mnt/c/Users/sheke/Pictures/<topic>/` or the repo run
  folder — never only the session scratchpad.
- **Open it for the user**: `code <absolute-wsl-path>` (and/or `explorer.exe`). Print
  only absolute WSL paths. Never print relative or `C:\` paths as links.
- State status: `draft` (unreviewed variants) vs `reviewed` (QA-passed deliverable).

## Asset & template lifecycle (self-compounding)

- **Promote wins.** When a run produces a first-of-its-kind result — a new style family
  (dark-mode card, brand-specific layout), or a reference→recreation pair that sets a
  new fidelity bar — copy the HTML into `templates/<style-family>.html` and the image
  pair into `assets/`, and add one line to the supporting-files list. The skill's
  quality compounds through these files, not through SKILL.md edits.
- **`assets/references/` grows differently — no cap.** Every `capture_reference.py` run
  is a free, real, permanent addition to the library, cataloged in
  `assets/references/catalog.md`. Unlike the fidelity-bar assets above, don't prune
  these; more real references is strictly more useful for future style-matching. Do
  keep captures purposeful — capture because a task needs that category, not
  speculatively.
- **Cap growth (fidelity-bar assets only).** One template + one recreation-pair per
  style family; replace, don't accumulate (keep the non-`references/` part of `assets/`
  under ~10 files). Prefer updating an existing template over adding a near-duplicate.
- **Third-party boundary.** `ref-*` images copied from user-supplied references are
  private calibration material for this machine only. If this skill is ever published
  or vendored into a shared repo, strip `assets/ref-*` (and review recreations of
  third-party designs) first. Own-output templates and renders are fine to ship.

## Judgment rules

Editable policy — tune here, not in the steps above.

- **Retry budget: 2 generations max per deliverable — applies to Track B (OmniRoute
  image-model calls) only.** Those cost API credits/quota and are nondeterministic, so
  capping them and switching strategy (edit-model repair, or the HTML/CSS deterministic
  path) after 2 misses is the right call. **Track A code-edit-and-rescreenshot cycles
  are NOT capped by this rule** — they're free, deterministic, and iterating them IS
  the point of the code track (verified live: the card-grid-comparison test took 4
  edit/re-screenshot passes to fix a layout defect — correct behavior, not a budget
  overrun). If ever unsure which applies: ask "does this cost an API call or quota?" —
  if no, keep editing.
- **Executor tier by step:** inventory + code articulation is the reasoning-heavy step —
  Sonnet-class minimum; escalate to Opus/Fable for dense references (15+ elements) or
  original designs where taste matters. Transport/decode/screenshot steps are
  script-driven and tier-agnostic.
- **Typography threshold:** more than ~4 words of visible text → gpt-image, no exceptions.
- **Draft cheaply:** style exploration on `flux.1-dev`; final render on the routed model.
  (`flux.1-schnell` is catalogued but returned "Image generation provider error" on live
  test 2026-07-13 — re-probe before relying on it.)
- **Don't upgrade renderers silently.** comfyui (`flux-dev`, `sdxl`) is wired but its local
  app is usually off; ask before requiring it.
- **quality flag:** default `medium` for gpt-image finals; `low` for probes.

## PPTX And Deck Visual Contract

When this skill is called by a deck workflow, the mandatory `pptx-visual-spec` overlay takes
precedence over standalone social-graphic routing. Read
`skills/pptx-visual-spec/references/visual-sourcing-rules.md` and consume the selected visual
record from `<run>/visual-spec.json`. In deck contexts, every glyph/claim is native or
deterministic code; `image-model` is text-free and non-evidentiary without exception.
Execute any selected image-model record through `skills/image-generation-router/SKILL.md`.

## Gotchas

- **CLI/MCP dead ends:** the OmniRoute MCP has NO image tool; the `omniroute api images ...`
  CLI prints `[object Object]` tables. Only the direct HTTP POST works — that's why the
  script exists. Don't rediscover this.
- **Image-driver whitelist:** only `codex`, `nvidia`, `comfyui` work. `zenmux` lists
  gpt-image models in its catalog but has **no image driver** ("Unknown image provider").
  `command-code`, `cloudflare-ai`, `ollama-cloud` are chat-only.
- **nvidia clamps to 1024×1024** regardless of `size`/`width`/`height`. codex honors
  `1024x1024 | 1024x1536 | 1536x1024` only.
- **Response shape differs by provider:** nvidia → `data[0].b64_json` (JPEG);
  codex → `data[0].url` as `data:image/png;base64,...` + `revised_prompt`. Script handles both.
- **PowerShell writes UTF-8 BOM** — always parse response JSON with `utf-8-sig`.
- **Never echo `OMNIROUTE_API_KEY`** (needed only for catalog introspection; the images
  endpoint needs no auth from localhost). Read it inside PowerShell (reference.md).
- **FLUX text failure looks plausible** — "AI-BULT", phantom rows. QA against the spec
  word-by-word, not by glance.
- **Playwright version drift:** bare `npx playwright screenshot` may demand a browser
  build (`chromium_headless_shell-12xx`) that isn't in `~/.cache/ms-playwright`.
  `scripts/html_to_png.mjs` sidesteps this by launching a cached full-chromium build
  (note: binary lives under `chrome-linux64/`, not `chrome-linux/`) or system chromium.
- **HSV saturation is numerically unstable near black** — tiny absolute RGB
  differences (e.g. `#090a0b`) produce inflated saturation ratios that look like real
  color but aren't. `extract_palette.py` gates accent detection on a brightness floor
  (`--min-value`, default 0.15) specifically to avoid this; don't loosen it chasing
  color where a source is genuinely near-monochrome (verified live: Linear's dashboard
  hero has 0 pixels above the threshold — a real finding, not a bug).
- **Don't image-gen what code can render.** If the design is flat boxes, text, and
  arrows, an image model adds nondeterminism for zero benefit — Track A first.
- **Capability truth comes from live probes.** The catalog listed models that fail
  (`flux.1-schnell`), a provider with no driver (zenmux), and upstream rejected a
  plausible-sounding model (`gpt-5.6`). Before promising a model/provider, probe it
  with one cheap request; on error, read the error body — it names the failing layer
  (see [troubleshoot.md](troubleshoot.md)).
- **Two Nano Banana paths exist:** the old OmniRoute adapter may remain blocked by prepaid
  billing while CLIProxyAPI Gemini is healthy through provider OAuth. Treat them as separate
  execution paths and probe the one actually selected.
- **Fixed-canvas HTML pattern:** size the `body` to exact px (`width:1200px;
  height:1800px`), sections as a flex column with `justify-content:space-between` to
  fill the canvas. **Trap:** `margin-top:auto` on the last child silently swallows all
  distributed space — space-between appears broken until it's removed (hit live).
- **Icons: inline SVG only, 1–3 stroke shapes each.** No emoji in Track A — headless
  chromium's emoji fonts are unreliable and the style clashes; a tiny hand-rolled SVG
  glyph reads consistently at 22–34px.

## Skill Relationships

### Category
Business Automation

### Dependencies
- `image-generation-router` — required whenever Track B chooses a generated raster.
- OmniRoute server — required only for the explicit OmniRoute adapter.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `design-system` / repo `DESIGN.md` | Sequential upstream | when brand-consistent output wanted | `docs/design.md` tokens → Style line |
| `frontend-design` (official plugin) | Behavioral overlay | Track A original designs (no reference) | design plan → HTML/SVG code |
| `design-system`, `marp`, `branded-pptx-deck` | Sequential downstream | trend-grounded design brief (Stage 0.5) produced | brief in DESIGN.md 4-section shape → `docs/design.md` / theme tokens |
| `pptx-visual-spec` | Behavioral overlay | any raster asset for a PowerPoint or deck workflow | `<run>/visual-spec.json` visual record |
| `image-generation-router` | Behavioral overlay | any generated raster | prompt + generated image + provenance JSON |
| `marp` / HyperFrames HTML path | Alternative / Peer | pixel-perfect text or brand tokens required | — |
| `nano-banana` MCP (`edit_image`) | Fallback / Amplifier | typo or region repair after generation | generated PNG |
| `higgsfield` MCP | Alternative / Peer | upscale/outpaint/video needed | generated PNG |
| `explainer-graphic` | Alternative / Peer | different graphic pipeline; prefer ai-graphics for OmniRoute-rendered rasters | — |
| `social-media-team` | Sequential downstream | post copy to pair with the graphic | final PNG path |
| `genspark-branded-deck`, `branded-pptx-deck` | Alternative / Peer | when the ask is a deck, not a single graphic | — |

### Runtime Preamble
"I will classify the visual first: deterministic HTML/SVG for structured or text-bearing
graphics; host-native image generation or an explicitly selected provider only for eligible
organic imagery. Deck requests also enforce the shared pptx-visual-spec contract."

## Host Compatibility

### Target Hosts
- Claude Code: yes — `~/.claude/skills/ai-graphics/SKILL.md` (canonical).
- Codex/OpenAI: **yes, ported 2026-07-13** — symlinks `~/.codex/skills/ai-graphics` and
  `~/.agents/skills/ai-graphics` → master; discovery verified via `codex debug prompt-input`.
  Scripts are host-neutral (python3/node/powershell.exe). Codex notes: its system
  built-in `image_gen` tool is the primary subscription-backed Track B path for eligible
  text-free imagery; CLIProxyAPI Gemini is explicit or fallback through the shared router;
  OmniRoute remains a separate explicit provider-adapter path. Never skip QA.
- Gemini CLI: **yes, ported 2026-07-24** — symlink `~/.gemini/skills/ai-graphics` → master,
  same pattern as the 11 other skills already symlinked there. Scripts are host-neutral;
  discovery not live-verified on this machine (`gemini` binary not on PATH here) — same
  confidence level as the other pre-existing `.gemini/skills/` symlinks, not independently
  re-checked.
- OpenHands: no (depends on this machine's Windows-side server).

### Canonical Source
`~/.claude/skills/ai-graphics/` is the source of truth; other roots are symlinks, so
edits propagate automatically — never break the links into diverged copies (that is the
Codex dual-root drift risk `skill_evals` flags).

### Source / Tool Order
1. This SKILL.md, then [reference.md](reference.md) for catalog introspection and API detail.
2. Memory `reference_omniroute_imagegen.md` (project memory) for provenance.
3. Live probes against `localhost:20128` — never assume model availability from memory.
