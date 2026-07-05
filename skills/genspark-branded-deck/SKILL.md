---
name: genspark-branded-deck
description: Use when the user wants a client-ready, branded slide deck from the HTML/CSS design template — as either a Genspark-format image-per-slide .pptx (2560×1440) OR an EDITABLE .pptx with native click-and-retype text boxes over the design (built-in hybrid). Triggers on "/genspark-branded-deck", "branded genspark deck", "editable genspark deck", "genspark-style pptx", "design-template deck", "make a branded deck from the template", "editable branded slides", "client-ready deck without genspark credits". Peer of branded-pptx-deck (fully native shapes/charts) and genspark-slides (drives genspark.ai itself). Use branded-pptx-deck instead when the client must re-layout shapes or needs native charts. Use genspark-slides instead when the user specifically wants Genspark's own generator.
trigger: /genspark-branded-deck
argument-hint: "[what deck — e.g. 'branded teardown from memo.md', 'reskin the servicenow deck to Aurora Glass']"
category: Business Automation
---

# genspark-branded-deck

Produce a **client-ready, branded deck** from the repo's HTML/CSS **design
template**, rendered to the same **image-per-slide 2560×1440 .pptx** format
Genspark exports — but the design is 100% yours, editable at source, and
**credit-free**.

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
- **Use `genspark-slides` instead** when the user specifically wants Genspark's
  own generator (needs credits; output stays image-only).

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

1. **Get validated content** by chaining the skills above into structured source
   (JSON/markdown). Never invent metrics; confirm entity statuses.
2. **Decide the spine.** Lead with the verdict (BLUF); write **action titles**
   (every `<h2>` is a so-what assertion). Honor slide-count minimums.
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
   equals the requested slide count.
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
9. **Declare editability honestly.** State which build you shipped: `image-based`
   (source-editable in `deck.html`/`theme.css` only) or `hybrid-editable` (native
   text boxes over a design background — headings/cards/stats are click-and-retype;
   vector-diagram shapes stay in the background). If the client must re-layout
   shapes or wants native charts, use `branded-pptx-deck` instead.
10. **Set status honestly.** `*-draft.pptx` before QA; rename to `*-reviewed.pptx`
    only after the contact-sheet review + visible-text scan pass; `*-blocked.txt`
    if a required path (Chrome, render) is unavailable. Keep `render.mjs` +
    `deck.html` in the run folder so QA fixes are reproducible.
11. **Deliver.** Copy the **reviewed** deck to `CLIENT_DELIVERY_DIR` (or, for this
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
the background image (their *labels* are editable, the shapes are not). For a
deck the client must fully re-layout (move/restyle shapes, native charts), use
**`branded-pptx-deck`** (pptxkit) instead — or, in Sheker's vault, the
`presentations:Presentations` chain (`/ce-doc-review` → `vault-presales-pptx-pipeline`).

**QA the editable build** by rendering it back: `soffice --headless --convert-to
pdf` then PyMuPDF (`fitz`) to PNG, and inspect for overlap/clipping — the shapes
are real text, so the render is faithful.

## Execution: where render.mjs runs

`render.mjs` needs **Playwright + a Chromium-family browser**. In this WSL setup
that means **Windows node + Windows Chrome** — WSL2 cannot reach a Windows Chrome
debug port. Windows node also **cannot run scripts from a `\\wsl$` UNC path**, so
**stage the deck on the Windows filesystem** first:

1. Resolve the workdir from `GENSPARK_DECK_WORKDIR` (default
   `C:/Users/<user>/genspark-design-template`).
2. Copy `assets/theme.css`, `assets/deck.css`, your `deck.html`, and
   `scripts/render.mjs` into it (once; `npm i playwright@1.49.1` there with
   `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1` — it reuses system Chrome).
3. Run `render.mjs` with **Windows node** (via `cmd.exe /c`).
4. Run `build_pptx.py` and `contact_sheet.py` with **WSL python** against the
   PNGs (both filesystems see `/mnt/c/...`).

If Windows Chrome/node is unavailable, set status `blocked` and say the render
path is missing — do not ship an unrendered deck.

## Portable paths

- `CHROME_PATH` — Chrome executable (default `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`).
- `GENSPARK_DECK_WORKDIR` — Windows staging/render dir.
- `CLIENT_DELIVERY_DIR` — copy-out location for the reviewed deck.

If an env var is unset, use the documented default; don't invent a machine path.

## Host Compatibility

### Target Hosts

- Claude Code: yes. The original source was ported from `/home/shekerk/.claude/skills/genspark-branded-deck/`.
- Codex/OpenAI: yes. Canonical project source is `skills/genspark-branded-deck/`.
- OpenHands: yes. Use the same repo-local skill folder and scripts.

### Discovery Path

Use `skills/genspark-branded-deck/SKILL.md` as the canonical source of truth.
If a host needs a discovery wrapper, point it here rather than duplicating the
skill body.

### Tool Mapping

- Read/search files with shell reads and `rg`.
- Edit files with `apply_patch`.
- Run scripts with shell commands from `/home/shekerk/content-ideas`.
- If Chrome, Windows node, or package install steps are blocked by sandboxing,
  request approval rather than bypassing the render path.

### Codex Notes

This skill is a local render pipeline, not the Genspark connector. In Codex,
use the bundled scripts under `skills/genspark-branded-deck/scripts/`; use the
Genspark AI Slides app only when the user explicitly wants Genspark's hosted
generator instead of this branded HTML/CSS template pipeline.

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
  contact-sheet review and a visible-text internal-term scan.
- **Semantic classes, not raw colours.** `a`/`b`/`alert` keep the argument
  colour-coded through any reskin. A hard-coded colour breaks on theme swap.

---

## Skill Relationships

### Category
Business Automation

### Dependencies
- `render.mjs` — required; needs Windows node + Chrome (Playwright).
- `build_pptx.py` — required; needs WSL python-pptx.
- `contact_sheet.py` — required for QA; needs PIL.
- `assets/theme.css` + `assets/deck.css` + a `deck.html` — the template triplet.

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `content-research` | Sequential upstream | ingest sites/repos/docs first | `$CONTENT_HOME/research/*.md` |
| `competitive-intel-sprint` | Sequential upstream | competitor teardown content | research output files |
| `ai-strategy-researcher` / `ai-strategy-brief` | Sequential upstream | market/vertical analysis | strategy report / brief md |
| `ai-analyst` | Sequential upstream | validated quant findings + charts | analysis JSON / chart PNGs |
| `vertical-scorer` | Sequential upstream | scored lanes | scorer output md |
| `mkt-visual-identity` | Sequential upstream | brand tokens for `theme.css` | `tokens.json` |
| `presentations:Presentations` | Sequential downstream (editable rebuild) | user needs native-editable slides; where installed (vault/Codex) | `deck.html` text + `build/png/*` references → editable `.pptx` |
| `branded-pptx-deck` | Sequential downstream (editable rebuild) | native-editable slides on this machine | `deck.html` text + PNG refs → editable `.pptx` |
| `genspark-slides` | Alternative / Peer | want Genspark's own generator (credits) | genspark project URL |
| `marp` | Alternative / Peer | markdown → HTML/PPTX preferred | — |
| `presentation-accessibility` | Amplifier downstream | optional post-QA a11y pass | output `.pptx` |

### Runtime Preamble

At invocation, surface this to the user:

> "This produces an **image-per-slide branded .pptx** from the HTML design template
> (pixel-perfect, one-file rebrandable, credit-free) — but slides are **images**,
> editable at source in `deck.html`/`theme.css`, not as PowerPoint shapes. If you
> need **native-editable** PowerPoint, I'll use `/branded-pptx-deck` instead.
>
> Have you run upstream skills for the content (`/content-research`,
> `/ai-strategy-brief`, `/ai-analyst`, `/vertical-scorer`)? And should I use the
> default 'operations console' theme or your Aurora Glass / `DESIGN.md` identity?"

---

## Gotchas

- **WSL can't render:** `render.mjs` must run on **Windows node + Chrome**, from a
  **Windows-filesystem** workdir (UNC `\\wsl$` paths fail). Stage first.
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
