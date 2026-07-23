---
name: genspark-branded-deck
description: Rebuild validated content or recovered Genspark slides into an owned, branded HTML/CSS deck and either an image-based or hybrid-editable PPTX. Use when `genspark-slides` produces a handoff, when a Genspark deck must be branded/reskinned or made hybrid-editable, or when hosted Genspark needs a local credit-free fallback. Route fully native or client-ready PowerPoint onward to `branded-pptx-deck` or `vault-presales-pptx-pipeline`.
---

# genspark-branded-deck

Produce an owned, branded deck from the repo's HTML/CSS design template. Build
either an image-per-slide 2560×1440 PPTX or a hybrid with native text over a
rendered design background. The source is editable and credit-free; the output
is not fully native PowerPoint unless it is rebuilt by a native downstream
builder.

## Canonical Genspark Contract

Read and follow the installed sibling contract at
`../pptx-visual-spec/references/genspark-video-deck-contract.md` (repo source:
`skills/pptx-visual-spec/references/genspark-video-deck-contract.md`). Accept the
canonical nested v1.2 `genspark-handoff.json`; tolerate older flat handoffs only
as migration input and rewrite them to v1.2 before delivery. Never weaken its
factual-integrity, editability-label, slide-count, or reviewed-status gates.

## Compound Genspark Contract

This skill is the required branded stage after `genspark-slides` whenever the
user asks to brand, reskin, contextualize, improve, or make a recovered Genspark
deck editable.

Accept `<run>/genspark-handoff.json` when present. Use it to resolve:

- validated story/content source
- Genspark project/viewer URL and recovered HTML/renders
- requested and recovered slide counts
- brand tokens or brand-source path
- requested editability: `image`, `hybrid`, or `native`
- blocked pages and hosted-generation status
- selected final builder

Treat recovered Genspark layouts as visual references, not immutable templates.
Re-author the deck in owned `deck.html` and `theme.css`; correct weak hierarchy,
crowding, repetition, and unsupported claims rather than reproducing them.

Before rebuilding, scan every Genspark-created number, URL, provider/model name,
price, machine specification, performance metric, completion percentage, and
status against the allowed evidence. A simulated interface is not proof that the
source product exposes the displayed values.

Route outcomes as follows:

| Requested outcome | This skill's output | Required downstream |
|---|---|---|
| Fast branded visual deck | Image PPTX | Contact-sheet and OfficeCLI QA |
| Hybrid-editable deck | Native text over rendered background | OfficeCLI QA |
| Fully native/editable deck | Branded HTML/render reference | `branded-pptx-deck` |
| Client-ready presales deck | Branded HTML/render reference | `vault-presales-pptx-pipeline` |

For the client-ready route, apply
[`references/genspark-to-vault-native.md`](references/genspark-to-vault-native.md).
This is the “best of both worlds” contract: preserve Genspark's storyline,
semantic roles, and useful archetypes, then translate them into the Vault grid,
layout library, typography, and fully native object model. Do not flatten the
Genspark styling into a background image for the final.
Use [`assets/genspark-vault-concept-prompt.md`](assets/genspark-vault-concept-prompt.md)
as the reusable upstream Genspark prompt when the intended final route is Vault-native.

If Genspark generation or capture is blocked, continue from validated source
content. Do not stop merely because a hosted Genspark artifact is unavailable.
The shared trigger examples are in
`../pptx-visual-spec/portable-skills/genspark-slides/references/prompt-routing.md`.

## Why this skill exists (and when NOT to use it)

Genspark returns **flattened images** at every exit (its viewer endpoints *and*
its PPTX export are baked PNGs — no editable `theme.css`), so you cannot reskin
or brand Genspark's own output. This skill inverts that: **you own the HTML/CSS**,
render it yourself, and get a branded, on-brand deck with no Genspark dependency.

- **Use this** for pixel-perfect design fidelity python-pptx can't easily do —
  gradients, web typography, custom diagrams (tower/ground-floor, gap bars),
  glassmorphism — plus one-file rebranding, matching Genspark's format.
- **Use `branded-pptx-deck` instead** when the client needs **PowerPoint-native
  editable shapes/charts** (they'll re-type numbers, restyle boxes in PowerPoint).
  This skill's slides are **images** (source-editable in HTML, not in PPT).
- **Use `genspark-slides` first** when the user wants Genspark's own generator or
  supplies a Genspark URL. Return here automatically for branding or editability.

## Files

- `assets/theme.css` — **brand identity (tokens only)**. Swap this one file to
  reskin every slide. Colours, fonts, atmosphere.
- `assets/deck.css` — **structure**: 10 slide archetypes reading `theme.css`
  tokens. No hard-coded colours.
- `assets/deck.example.html` — a complete 13-slide worked example (ServiceNow
  teardown). Copy it as the starting point for a new deck.
- `scripts/render.mjs` — deck HTML → one 2560×1440 PNG per slide (Windows node +
  Chrome). `--deck <html> --out <png-dir>`; honours `CHROME_PATH`. *(image path)*
- `scripts/build_pptx.py` — PNGs → image-per-slide `.pptx` (WSL / python-pptx). *(image path)*
- `scripts/render_hybrid.mjs` — **editable path.** Per slide, captures every text
  block's bbox + runs (colour/bold) + font/line-height/align, and renders a
  **text-free background** PNG. `--deck <html> --out <dir>` → `bg/` + `pos/`.
- `scripts/build_editable_pptx.py` — **editable path.** Background image +
  **native PowerPoint text boxes** at the captured coords (shrink-to-fit so text
  can't overflow its slot). `--src <dir> --out <pptx>`.
- `scripts/contact_sheet.py` — PNGs → review grids. **Your eyes for QA.**
- `../../scripts/officecli_qa.py` — optional final `.pptx` QA gate: validates,
  checks issues, and renders the built PowerPoint to HTML/PNG when `officecli` is
  installed.
- `references/archetypes.md` — the content contract: every archetype + density budget.

## Upstream: chain skills for the content — do NOT hand-roll analysis

This skill is the **render/brand stage only**. Findings, scores, and narrative
should come from the existing skills; chaining is the default. Feed their outputs
into `deck.html`.

| Need | Use first |
|------|-----------|
| Ingest sites / repos / videos / docs | `content-research` (or `competitive-intel-sprint`) |
| Market / vertical / competitive analysis | `ai-strategy-researcher` or `ai-strategy-brief` |
| Quant findings + validated charts | `ai-analyst` (`/analyze`) — its validation catches bad facts |
| Scored lanes / verticals | `vertical-scorer` |
| Brand tokens (colours/fonts) | `mkt-visual-identity` → map `tokens.json` into `theme.css` |

Always run content through a **validation pass** before rendering — every named
entity, count, status, and claim checked against source.

## Workflow (do these in order)

1. **Resolve the compound handoff.** Read `genspark-handoff.json` when present,
   then get any missing validated content from the upstream skills above.
   (JSON/markdown). Never invent metrics; confirm entity statuses.
2. **Decide the spine.** Lead with the verdict (BLUF); write **action titles**
   (every `<h2>` is a so-what assertion). Derive slide count from evidence
   coverage and density; honor minimums but never treat them as ceilings.
3. **Author `deck.html`.** Copy `assets/deck.example.html`; for each point pick an
   archetype from `references/archetypes.md` and refill the text. Use the semantic
   token classes (`a` = subject/competitor, `b` = our wedge, `alert` =
   kill-criteria) — never raw colours. Respect the density budget (overflow is
   clipped, not scrolled).
4. **Sanitize client-facing text.** No internal production language on slides —
   scan for tool names, file paths, timestamps, `transcript`, `synthesis`,
   `Codex`, `Claude`, `Genspark`, `audit`, `validation`. Use client labels
   (`Business implication`, `Decision`, `Next move`).
5. **Brand it.** Confirm `theme.css` carries the client's identity. To reskin,
   edit **only** `theme.css` (or `<link>` a `theme.<brand>.css`); if
   `mkt-visual-identity` ran, map its `tokens.json` into the `--ground` / `--ink`
   / `--accent-*` / `--font-*` tokens. Never edit `deck.css` to rebrand.
6. **Render.** Stage into a Windows-accessible workdir (see Execution), then:
   `node render.mjs --deck <deck.html> --out build/png`. Confirm the PNG count
   equals the content-driven slide manifest and every evidence row is mapped.
7. **QA — this is a delivery gate, not optional.**
   `python3 scripts/contact_sheet.py --png build/png --out build/qa` and **actually
   look** at every sheet: no clipped stat bars, no title/body collisions, no
   overflow, an eyebrow/label present on each slide. Because slides are rendered
   HTML, the PNGs are faithful — no placeholder problem. Fix `deck.html`/`theme.css`
   and re-render until clean.
8. **Build the PPTX — pick the output** (see "Two outputs" below):
   - *image/fast:* `python3 scripts/build_pptx.py --png build/png --out build/<name>-draft.pptx`
   - *editable (default when they want to edit in PowerPoint):*
     `node scripts/render_hybrid.mjs --deck <deck.html> --out build` then
     `python3 scripts/build_editable_pptx.py --src build --out build/<name>-editable-draft.pptx`
9. **QA the final PPTX.** From the repo root, run
   `python3 ../../scripts/officecli_qa.py <built.pptx> --out <run>/qa/officecli`.
   Compare the OfficeCLI-rendered final PPTX screenshots with the source HTML
   contact sheet, especially for the hybrid-editable path where PowerPoint text
   boxes can reflow differently from HTML. If OfficeCLI is skipped, use
   LibreOffice/PDF, PowerPoint, Google Slides import, or equivalent.
10. **Declare editability honestly.** State which build you shipped: `image-based`
   (source-editable in `deck.html`/`theme.css` only) or `hybrid-editable` (native
   text boxes over a design background — headings/cards/stats are click-and-retype;
   vector-diagram shapes stay in the background). If the client must re-layout
    shapes or wants native charts, continue into `branded-pptx-deck`; use
    `vault-presales-pptx-pipeline` for client-ready presales delivery.
    When routing to Vault, retain this skill's HTML/PPTX as a labeled visual
    prototype and pass the design spec plus recovered references through the
    Genspark-to-Vault native handoff contract.
11. **Set status honestly.** `*-draft.pptx` before QA; rename to `*-reviewed.pptx`
    only after the contact-sheet review + visible-text scan pass; `*-blocked.txt`
    if a required path (Chrome, render) is unavailable. Keep `render.mjs` +
    `deck.html` in the run folder so QA fixes are reproducible.
12. **Deliver.** Copy the **reviewed** deck to `CLIENT_DELIVERY_DIR` (or, for this
    user, `/mnt/c/Users/<user>/OneDrive/Desktop/`), and open with
    `powershell.exe -NoProfile -Command "Start-Process '<C:\...>'"`. A deck open in
    PowerPoint is **locked** — on "Permission denied", write a **new filename**.

## Two outputs: image (fast) vs editable (built-in hybrid)

Full CSS can't *become* PPT shapes, so this skill offers two builds from the
**same `deck.html`**:

**A) Image deck (fast/visual)** — `render.mjs` → `build_pptx.py`. Pixel-perfect,
non-editable. Use when the client only receives the file.

**B) Editable deck (built-in hybrid)** — the default when the user wants editable:
```
node render_hybrid.mjs --deck deck.html --out build      # bg/ (text-free design) + pos/ (text boxes)
python3 build_editable_pptx.py --src build --out build/<name>-editable.pptx
```
It renders the **design as a text-free background**, then lays **native
PowerPoint text boxes** (real, click-and-retype) at the captured coordinates with
matching colour/weight/line-height, shrink-to-fit so nothing overflows. Result:
the exact design **and** editable headings, cards, and stats. This is the
"wire both" path — design fidelity + editability in one pipeline, credit-free.

*Editable-hybrid caveats:* text reflows if a client heavily rewrites a block
(shrink-to-fit keeps it inside its slot). Complex vector diagrams remain part of
the background image (their *labels* are editable, the shapes are not).

**This hybrid is NOT "client-ready" under the `Client-Ready PPTX Design System`**, whose
rule is explicit: *"Do not flatten full slides into images for the client-ready output."*
The hybrid's layouts ARE flattened (design background + text boxes on top). It is the
right tool for fast, pixel-perfect, credit-free visual decks — not for a deck governed by
that design system.

Route out when the client must re-layout shapes or needs native charts:
- **`/vault-presales-pptx-pipeline`** — the client-ready path. Builds via **artifact-tool
  presentation JSX** into 100% native objects (zero pictures), on the design system's
  L01–L16 layouts, gated by OfficeCLI QA. Globally available. Read that skill's
  artifact-tool presentation JSX reference first.
- **`/branded-pptx-deck`** (pptxkit) — native shapes/charts on the branded template, for
  decks outside the vault design system.

**QA the editable build** by rendering it back. Prefer
`python3 ../../scripts/officecli_qa.py <pptx> --out <run>/qa/officecli`; if OfficeCLI
is skipped, use `soffice --headless --convert-to pdf` then PyMuPDF (`fitz`) to
PNG, and inspect for overlap/clipping — the shapes are real text, so the render
is faithful.

## Execution: where render.mjs runs

`render.mjs` needs **Playwright + a Chromium-family browser**. It does *not* care
which OS supplies them.

### Preferred: WSL Playwright Chromium (re-verified 2026-07-22)

**No Windows staging, no `GENSPARK_DECK_WORKDIR`, no `cmd.exe`.** Run everything in
WSL from the run folder, passing WSL's own Playwright Chromium via `--chrome`:

```bash
CHROME=$(node -e "console.log(require('playwright').chromium.executablePath())")
node render.mjs        --deck deck.html --out build/png    --chrome "$CHROME"
node render_hybrid.mjs --deck deck.html --out build        --chrome "$CHROME"
python3 build_editable_pptx.py --src build --out build/<name>-draft.pptx
```

Playwright resolves from the active repository root (`<repo>/node_modules`), so
run from there or a subdirectory of it. Proven end-to-end: 28 slides → 2560×1440 PNGs →
358 native text boxes → OfficeCLI QA 0 issues.

### Fallback: Windows node + Windows Chrome (only if WSL Chromium is missing)

WSL2 cannot reach a Windows Chrome *debug port*, and Windows node cannot run scripts
from a `\\wsl$` UNC path — so this path requires staging on the Windows filesystem:

1. Resolve the workdir from `GENSPARK_DECK_WORKDIR` (default
   `C:/Users/<user>/genspark-design-template`).
2. Copy `assets/theme.css`, `assets/deck.css`, your `deck.html`, and
   `scripts/render.mjs` into it (once; `npm i playwright@1.49.1` there with
   `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1` — it reuses system Chrome).
3. Run `render.mjs` with **Windows node** (via `cmd.exe /c`).
4. Run `build_pptx.py` and `contact_sheet.py` with **WSL python** against the PNGs.

**This fallback is unavailable whenever WSL interop is off** — check
`/proc/sys/fs/binfmt_misc/WSLInterop`. If it doesn't exist, no Windows binary
(`cmd.exe`, `powershell.exe`, Windows node) can execute from WSL at all, and the
WSL-Chromium path above is the *only* one that works. That was the state on
2026-07-16.

Only if **both** paths are unavailable: set status `blocked` and say the render path
is missing — do not ship an unrendered deck.

## Portable paths

- `CHROME_PATH` — Chrome executable (default `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`).
- `GENSPARK_DECK_WORKDIR` — Windows staging/render dir.
- `CLIENT_DELIVERY_DIR` — copy-out location for the reviewed deck.

If an env var is unset, use the documented default; don't invent a machine path.

## Host Compatibility

### Target Hosts

- Claude Code: yes. Install from the canonical repo source through the cross-host registry.
- Codex/OpenAI: yes. Canonical project source is `skills/genspark-branded-deck/`.
- OpenHands: yes. Use the same repo-local skill folder and scripts.

### Discovery Path

Use `skills/genspark-branded-deck/SKILL.md` as the canonical source of truth.
If a host needs a discovery wrapper, point it here rather than duplicating the
skill body.

### Tool Mapping

- Read/search files with shell reads and `rg`.
- Edit files with `apply_patch`.
- Run scripts with shell commands from the repository root or the run directory.
- If Chrome, Windows node, or package install steps are blocked by sandboxing,
  request approval rather than bypassing the render path.

### Codex Notes

This skill is the local branded stage, not the hosted generator. When the user
wants Genspark generation, run `genspark-slides` first through the Genspark AI
Slides app, write `genspark-handoff.json`, and return here for the owned rebuild.

## Hard rules (learned the hard way)

- **Declare the actual build.** Image path = `non-editable visual render`.
  Hybrid path = `hybrid-editable text over rendered design background`. Do not
  imply fully native PowerPoint shapes/charts unless you used `branded-pptx-deck`.
- **Reskin via `theme.css` only.** Never edit `deck.css` or fork it to rebrand —
  that's maintenance drift. Structure reads tokens; identity lives in tokens.
- **Overflow is clipped, not scrolled.** The canvas is a fixed 1280×720 (→2560×1440).
  If content doesn't fit the density budget, split the slide — never shrink type
  past legibility. QA the contact sheet every time.
- **Never render unvalidated content.** Wrong facts in a client deck are a delivery
  failure. Validate every entity/number/status against source first.
- **No internal language on client slides.** Especially scrub `Genspark`, tool
  names, paths, and `synthesis`/`validation` labels — they belong in run files.
- **Reviewed requires evidence.** Only name a deck `*-reviewed.pptx` after a real
  contact-sheet review, OfficeCLI final-PPTX QA when available, and a visible-text
  internal-term scan.
- **Semantic classes, not raw colours.** `a`/`b`/`alert` keep the argument
  colour-coded through any reskin. A hard-coded colour breaks on theme swap.

---

## Shared Visual Contract

Read `../pptx-visual-spec/references/visual-sourcing-rules.md`, then emit and validate
`<run>/visual-spec.json`. The contract applies to source regions even when this skill's final
output mode explicitly permits flattened design backgrounds. Exact references remain exact;
slide text and claims are never image-model output; generated regions are text-free and
non-evidentiary.

## Skill Relationships

### Category
Business Automation

### Dependencies
- `render.mjs` — required; needs Windows node + Chrome (Playwright).
- `build_pptx.py` — required; needs WSL python-pptx.
- `contact_sheet.py` — required for QA; needs PIL.
- `officecli-qa` — optional final PowerPoint QA gate; uses the repository QA
  script when `officecli` is installed.
- `assets/theme.css` + `assets/deck.css` + a `deck.html` — the template triplet.
- `pptx-visual-spec` — mandatory visual-routing overlay and schema.

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `content-research` | Sequential upstream | ingest sites/repos/docs first | `$CONTENT_HOME/research/*.md` |
| `competitive-intel-sprint` | Sequential upstream | competitor teardown content | research output files |
| `ai-strategy-researcher` / `ai-strategy-brief` | Sequential upstream | market/vertical analysis | strategy report / brief md |
| `ai-analyst` | Sequential upstream | validated quant findings + charts | analysis JSON / chart PNGs |
| `vertical-scorer` | Sequential upstream | scored lanes | scorer output md |
| `mkt-visual-identity` | Sequential upstream | brand tokens for `theme.css` | `tokens.json` |
| `pptx-visual-spec` | Behavioral overlay | every image or hybrid deck build | `<run>/visual-spec.json` |
| `vault-presales-pptx-pipeline` | Sequential downstream (client-ready rebuild) | deliverable must be client-ready / fully native (design system forbids flattened slides); globally available | `deck.html` text + `build/png/*` as reference → native `.pptx` via artifact-tool JSX |
| `branded-pptx-deck` | Sequential downstream (editable rebuild) | native-editable slides on this machine | `deck.html` text + PNG refs → editable `.pptx` |
| `genspark-slides` | Sequential upstream | hosted generation or a Genspark URL supplies reference slides | `genspark-handoff.json`, recovered HTML/renders |
| `marp` | Alternative / Peer | markdown → HTML/PPTX preferred | — |
| `presentation-accessibility` | Amplifier downstream | optional post-QA a11y pass | output `.pptx` |

### Runtime Preamble

At invocation, disclose the selected output class:

> "This produces an **image-per-slide branded .pptx** from the HTML design template
> (pixel-perfect, one-file rebrandable, credit-free) — but slides are **images**,
> editable at source in `deck.html`/`theme.css`, not as PowerPoint shapes. If you
> need **native-editable** PowerPoint, I'll use `/branded-pptx-deck` instead.
>
> If fully native/client-ready PowerPoint is required, this branded build becomes
> the reference input to `/branded-pptx-deck` or
> `/vault-presales-pptx-pipeline`."

---

## Gotchas

- **Choose the current render lane:** prefer the verified WSL Playwright Chromium
  path. Use Windows node + Chrome only when WSL Chromium is missing or broken;
  stage on the Windows filesystem because Windows node cannot run from a UNC
  `\\wsl$` working directory.
- **PNG count ≠ slide count:** if the render drops slides, the deck HTML likely
  errored (missing `window.__deck` hook or a bad `<section>`); check the browser
  console via a headed run before building the PPTX.
- **Blurry slides:** confirm `deviceScaleFactor: 2` in `render.mjs` and that the
  stage is at `--fit:1` during export (`window.__deck.fitOne()`), giving true 2560×1440.
- **Reskin looks half-applied:** a raw colour leaked into `deck.html` or `deck.css`.
  All colour must come from `var(--…)`; audit for hex literals.
- **File locked in PowerPoint:** on "Permission denied" re-copy, the deck is open —
  write a new filename, don't overwrite.
- **Status before delivery:** label `draft` / `reviewed` / `blocked` with matching
  filename suffixes. Never present an unreviewed deck as final.

## Images And Visuals

Follow `pptx-visual-spec` and execute raster work through `ai-graphics`. HTML/CSS owns the
design background and all glyphs. Built-in Codex `image_gen` may fill only declared
text-free organic slots; it never renders slide copy. Record its prompt and provenance in
`visual-spec.json`, then inspect the composited background and final PPTX render.
