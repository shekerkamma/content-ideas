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

Do not start the branded rebuild until `validation.status=passed`. Require the
exact generation prompt, its SHA-256, the multimodal manifest, and
`genspark-content-validation.json`. Validation must cover every recovered slide
and every required audio/visual/temporal segment. If it fails, revise the same
Genspark project; do not locally summarize around missing content.

## Compound Genspark Contract

This skill is the required branded stage after `genspark-slides` whenever the
user asks to brand, reskin, contextualize, improve, or make a recovered Genspark
deck editable.

### Conversion completion invariant

Recovery is not delivery. The run is incomplete until a distinct branded
artifact has been built and QA'd. When Genspark expands or edits the project,
all earlier branded derivatives become stale immediately. Rebuild from the new
reference before reporting success. Record `delivery.slide_count` and require it
to be at least `recovery.captured_slide_count`; never leave a 14-slide branded
derivative attached to a newly recovered 38-slide project.

Accept `<run>/genspark-handoff.json` when present. Use it to resolve:

- validated story/content source
- Genspark project/viewer URL and recovered HTML/renders
- requested and recovered slide counts
- brand tokens or brand-source path
- requested editability: `image`, `hybrid`, or `native`
- blocked pages and hosted-generation status
- selected final builder

On the **re-author** route only (see Route 0), treat recovered layouts as visual
references rather than immutable templates: correct weak hierarchy, crowding,
repetition and unsupported claims instead of reproducing them. On the **verbatim**
route this does not apply — reproduce the slides as they are and fix only defects
that make text unreadable, saying what you changed.

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

Client-ready route: apply [`references/genspark-to-vault-native.md`](references/genspark-to-vault-native.md)
— preserve Genspark's storyline, semantic roles and useful archetypes, then translate
them into the Vault grid, layout library, typography and fully native object model;
never flatten Genspark styling into a background image for the final. The reusable
upstream prompt is [`assets/genspark-vault-concept-prompt.md`](assets/genspark-vault-concept-prompt.md).

If Genspark *generation* is blocked, continue from validated source content rather
than stopping: Codex/GPT-5.6-sol is the local authoring engine, preserving the frozen
prompt and multimodal IDs, authoring structured visual assets deterministically, and
routing fully native output through `branded-pptx-deck`.
Do not wait past the shared 600-second/two-no-progress ceiling. (Reading an existing
deck is never blocked — see the recovery lane under Execution.) Trigger examples:
`../pptx-visual-spec/portable-skills/genspark-slides/references/prompt-routing.md`.

## Why this skill exists (and when NOT to use it)

Genspark's own PPTX export is baked PNGs with no editable `theme.css`, so you
cannot reskin or edit its output. This skill inverts that: **you own the HTML/CSS**,
render it yourself, and get a deck with no Genspark dependency.

- **Use this** for design fidelity python-pptx can't reach — gradients, web type,
  custom diagrams — plus one-file rebranding and native click-and-retype text.
- **Use `branded-pptx-deck` instead** when the client must re-layout *shapes* or
  needs native charts. Hybrid text is editable; the design furniture is not.
- **Use `genspark-slides` first** for Genspark's own generator.

## Files

- `assets/theme.css` — **brand identity (tokens only)**. Swap this one file to
  reskin every slide. Colours, fonts, atmosphere.
- `assets/deck.css` — **structure**: 10 slide archetypes reading `theme.css`
  tokens. No hard-coded colours.
- `assets/deck.example.html` — complete 13-slide worked example; copy it to start.
- `scripts/render.mjs` — deck HTML → one 2560×1440 PNG per slide. `--deck <html> --out <png-dir>`; honours `CHROME_PATH`.
- `scripts/build_pptx.py` — PNGs → image-per-slide `.pptx` (WSL / python-pptx). *(image path)*
- `scripts/render_hybrid.mjs` — **editable path.** Captures every text block's bbox,
  runs, font family/size/line-height/align, and renders a **text-free background**
  PNG. `--deck <html> --out <dir>` → `bg/` + `pos/`.
- `scripts/build_editable_pptx.py` — background image + **native PowerPoint text
  boxes** at the captured coords. `--src <dir> --out <pptx> [--stage 1920]`.
- `scripts/contact_sheet.py` — PNGs → review grids. **Your eyes for QA.**
  Point it at `build/png`. `build/bg` is the text-free pass and will look blank.
- `scripts/build_verbatim_deck.py` — VERBATIM route: wraps recovered source slides
  into a renderable deck unchanged, plus a generic auto-fit. `--src slides --css chrome.css`.
- `scripts/install_fonts.sh` — installs the deck's own families. `--from <css>` / `--check`.
- `scripts/check_export_coverage.mjs` — **mandatory hybrid gate.** Diffs every
  visible DOM string against the captured text boxes. Catches silent content
  loss that the PNG and OfficeCLI both miss. `--deck <html> --pos build/pos`.
- `scripts/check_layout_overflow.mjs` — overflow + collision report. `--deck <html> [--min 20]`.
- `../../scripts/officecli_qa.py` — final `.pptx` gate: validate / issues / html /
  screenshot. Use `--required`. **`issues: 0` only means nothing crosses a slide
  edge** — it is blind to wrapped, doubled or missing text that stays in-bounds.
- `references/archetypes.md` — the content contract: every archetype + density budget.

## Upstream: chain skills for the content — do NOT hand-roll analysis

This skill is the **render/brand stage only**. Findings, scores and narrative come
from the skills below; feed their outputs into `deck.html`.

| Need | Use first |
|------|-----------|
| Ingest sites / repos / videos / docs | `content-research` (or `competitive-intel-sprint`) |
| Market / vertical / competitive analysis | `ai-strategy-researcher` or `ai-strategy-brief` |
| Quant findings + validated charts | `ai-analyst` (`/analyze`) — its validation catches bad facts |
| Scored lanes / verticals | `vertical-scorer` |
| Brand tokens (colours/fonts) | `mkt-visual-identity` → map `tokens.json` into `theme.css` |

Always run a **validation pass** before rendering: every named entity, count,
status and claim checked against source.

## Route 0 — decide FIRST: reproduce verbatim, or re-author?

Answer before authoring: **does the user want *this* deck, or a new deck informed
by it?** Guessing wrong wastes the entire build.

| The user says | Route |
|---|---|
| "make a PPTX of this deck", "convert", "make it editable", "faithful" | **Verbatim** — recover the source slides, use them unchanged. No re-titling, re-layout or re-theming. |
| "upgrade", "improve", "fix the claims", "rebuild on our brand" | **Re-author** — steps 1–12. Extract the reference's storyline *and* its design tokens first: [`references/design-template-from-source.md`](references/design-template-from-source.md). |

**Default to Verbatim when a deck URL is supplied.** Do not scrape the agent-chat
page — it yields the generation *prompt*, not the slides, and the viewer
virtualises to ~10 mounted iframes. The deck is served as data:
`GET /api/project/slide_data?project_id=<id>&deck=<deck>` returns every slide's
HTML plus its `chrome.css` design system. Full procedure, the 1920-stage retarget
table and font handling: [`references/verbatim-recovery.md`](references/verbatim-recovery.md).

## Workflow (do these in order)

1. **Resolve the compound handoff.** Read `genspark-handoff.json` when present,
   then get any missing validated content from the upstream skills above.
   (JSON/markdown). Verify `genspark-prompt.txt`,
   `genspark-multimodal-context.json`, and
   `genspark-content-validation.json`. Never invent metrics; confirm entity
   statuses.
   **Read `references/archetypes.md`, `assets/deck.example.html` and
   `assets/deck.css` before writing a single slide.** The archetypes are a
   closed set and `deck.css` is the only class inventory that exists; inventing
   class names produces slides that render as empty panels.
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

   **Point it at `build/png`, never `build/bg`.** `bg/` is the text-free
   background pass — it is *supposed* to look empty. Running the contact sheet
   over `bg/` and declaring QA green is a fabricated pass. Sanity check: a real
   sheet is hundreds of KB; a `bg/` sheet is ~20KB.

   Overlap hides at thumbnail size — measure it:
   `node scripts/check_layout_overflow.mjs --deck <deck.html> --min 20`. Fixed-height
   title boxes are the usual culprit: a two-line title prints over its subtitle.

7b. **Export-fidelity gate (hybrid path) — run after `render_hybrid.mjs`:**
   `node scripts/check_export_coverage.mjs --deck <deck.html> --pos build/pos`

   Not optional, and covered by nothing else. It diffs every visible DOM string
   against the capture. A predicate bug deletes content while the PNG looks perfect
   (real screenshot) and OfficeCLI reports `issues: 0` (survivors are in-bounds) —
   one instance dropped whole table columns across 36 of 37 slides and shipped.
   Exit 0 or do not build the PPTX.
8. **Build the PPTX — pick the output** (see "Two outputs" below):
   - *image/fast:* `python3 scripts/build_pptx.py --png build/png --out build/<name>-draft.pptx`
   - *editable (default when they want to edit in PowerPoint):*
     `node scripts/render_hybrid.mjs --deck <deck.html> --out build` then
     `python3 scripts/build_editable_pptx.py --src build --out build/<name>-editable-draft.pptx`
9. **QA the final PPTX.** From the repo root, run
   `python3 ../../scripts/officecli_qa.py <built.pptx> --out <run>/qa/officecli --required`.
   **`--required` is mandatory for anything client-facing:** without it the helper
   exits 0 and writes `Status: skipped` when OfficeCLI is absent, so a silent skip
   reads exactly like a pass. Confirm `Status: passed` plus all three artifacts
   (`qa-summary.md`, `render/<name>.png`, `<name>.html`).
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
Renders the **design as a text-free background**, then lays **native PowerPoint
text boxes** at the captured coordinates with matching family/colour/weight/
line-height, shrink-to-fit. Design fidelity *and* click-and-retype text, credit-free.
Add `--stage 1920` for a recovered deck. *Caveats:* heavy client rewrites reflow
within the slot; vector diagrams stay in the background (labels editable, shapes not).

**Not "client-ready" under the `Client-Ready PPTX Design System`** — its rule is
*"do not flatten full slides into images"*, and hybrid layouts are flattened.
Route out when the client must re-layout shapes or needs native charts:
- **`/vault-presales-pptx-pipeline`** — the client-ready path. Builds via **artifact-tool
  presentation JSX** into 100% native objects (zero pictures), on the design system's
  L01–L16 layouts, gated by OfficeCLI QA. Globally available. Read that skill's
  artifact-tool presentation JSX reference first.
- **`/branded-pptx-deck`** (pptxkit) — native shapes/charts on the branded template, for
  decks outside the vault design system.

**QA the editable build** per step 9. If OfficeCLI is unavailable, fall back to
`soffice --headless --convert-to pdf` plus PyMuPDF (`fitz`) and inspect for
overlap and clipping.

## Execution: two different browser lanes

Do not conflate these. Picking the wrong one is why a build stalls.

| Lane | Purpose | Use |
|---|---|---|
| **Recovery** | Drive a *live, logged-in* Genspark deck | `mcp__chrome-devtools-windows__*` (Windows Chrome) |
| **Render** | Screenshot *your own local* `deck.html` | WSL Playwright Chromium, headless |

### Recovery lane — authenticated browsing

**There is no Genspark connector tool.** Do not wait for one, and never ask the
user to export or screenshot the deck by hand. To read a Genspark URL, use the
Windows-side Chrome DevTools MCP — it carries the authenticated session that WSL
Chromium lacks. A WSL sign-in/cookie wall is **not** a blocker to report; it is
the signal to switch lanes. Drive it with `list_network_requests` +
`evaluate_script`, passing `filePath` for large payloads so they never cross context.

### Render lane — WSL Playwright Chromium (re-verified 2026-07-22)

**No Windows staging, no `GENSPARK_DECK_WORKDIR`, no `cmd.exe`.** Run everything in
WSL from the run folder, passing WSL's own Playwright Chromium via `--chrome`:

```bash
CHROME=$(node -e "console.log(require('playwright').chromium.executablePath())")
node render.mjs        --deck deck.html --out build/png    --chrome "$CHROME"
node render_hybrid.mjs --deck deck.html --out build        --chrome "$CHROME"
python3 build_editable_pptx.py --src build --out build/<name>-draft.pptx
```

Playwright resolves from the active repository root (`<repo>/node_modules`), so run
from there or a subdirectory. Headless is correct here — the render is deterministic
and needs no session. Flip `headless:false` **only** to debug a blank or short render
(missing `window.__deck`, a bad `<section>`), then put it back.

### Fallback: Windows node + Windows Chrome (only if WSL Chromium is missing)

WSL2 cannot reach a Windows Chrome *debug port*, and Windows node cannot run from a
`\\wsl$` UNC path, so this path needs Windows-filesystem staging: copy the CSS,
`deck.html` and `render.mjs` into `GENSPARK_DECK_WORKDIR` (default
`C:/Users/<user>/genspark-design-template`), `npm i playwright@1.49.1` there with
`PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1` (reuses system Chrome), run `render.mjs` via
`cmd.exe /c`, then run the Python steps in WSL against the PNGs.

Unavailable whenever WSL interop is off — check `/proc/sys/fs/binfmt_misc/WSLInterop`;
if absent, no Windows binary can execute from WSL and the WSL-Chromium path is the
only one. If **both** render paths are gone, set status `blocked`; do not ship an
unrendered deck. (Note this constrains only *rendering* — the recovery lane above
runs through the DevTools MCP, not through WSL.)

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
When that lane stalls or under-generates, Codex/GPT-5.6-sol becomes the authoring
engine; Genspark is no longer a delivery dependency.

## Hard rules (learned the hard way)

- **A reference deck is the design system, not just the storyline.** If a deck
  URL is supplied, open the *rendered slides* and extract their real tokens
  (palette, type roles, scale, chrome) before choosing anything. Scraping the
  agent-chat page gets you the generation prompt and none of the design.
  Substituting this skill's default theme for the client's is a rebuild, not a
  reskin, and will be rejected.
- **Never re-author content the user asked you to reproduce.** Re-titling,
  re-laying-out, or "improving" a 37-slide source into your own 43-slide arc
  destroys work they chose. Verbatim is the default for a supplied deck.
- **Never claim a gate passed without opening the artifact it produces.**
  Checking `build/bg` instead of `build/png`, or reporting `issues: 0` without
  looking at the render, is a fabricated pass. Every gate in this skill has a
  specific artifact to *look at*; a green exit code is not the evidence.
- **Match effort to the ask.** When the source is already well-designed HTML,
  the job is recover → wrap → render → export. Building a template system and a
  generator to reproduce a deck that already exists is the expensive wrong turn.
- **Declare the actual build.** Image path = `non-editable visual render`.
  Hybrid path = `hybrid-editable text over rendered design background`. Do not
  imply fully native PowerPoint shapes/charts unless you used `branded-pptx-deck`.
- **Reskin via `theme.css` only.** Never edit `deck.css` or fork it to rebrand —
  that's maintenance drift. Structure reads tokens; identity lives in tokens.
- **Overflow is clipped, not scrolled.** The canvas is a fixed 1280×720 (→2560×1440).
  If content doesn't fit the density budget, split the slide — never shrink type
  past legibility. QA the contact sheet every time.
- **Never render unvalidated content.** Wrong facts in a client deck are a delivery
  failure. Validate every entity/number/status against source first and require a
  passed exact-prompt/multimodal validation before branding.
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

### Dependencies — preflight before rendering

| Need | Check | If missing |
|---|---|---|
| Playwright + Chromium | `node -e "console.log(require('playwright').chromium.executablePath())"` | run from the repo root; `npm run test:e2e:install` |
| python-pptx | `python3 -c "import pptx"` | both PPTX builders need it |
| Pillow | `python3 -c "import PIL"` | `contact_sheet.py` needs it |
| officecli | `which officecli` | final QA gate degrades to LibreOffice/PDF |
| **The deck's fonts** | `scripts/install_fonts.sh --check --from <chrome.css\|deck.html>` | `scripts/install_fonts.sh --from <css>` |

**Fonts are not optional on the hybrid path.** `render_hybrid.mjs` captures each
box's *real* family and the builder writes it into the PPTX; uninstalled means the
PNG substitutes silently, OfficeCLI misrepresents what the client sees, and
PowerPoint substitutes again on their machine. Install first, **ship the `.ttf`s
beside the deck**, and say a machine without them will substitute.

**Stage width:** `build_editable_pptx.py --stage` defaults to 1280 (this skill's
template); pass `--stage 1920` for a recovered Genspark deck or every coordinate
and font size is halved. Also required: the `theme.css`+`deck.css`+`deck.html`
triplet, and `pptx-visual-spec`.

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

### Hybrid-export traps — read before debugging a PPTX/PNG mismatch

Three traps corrupt the PowerPoint while the PNG stays perfect, and two are
invisible to OfficeCLI: **inline-only text silently dropped**, **inline tags
styled `display:block` captured twice**, and **tight bboxes re-wrapping** under
PowerPoint's font metrics. Full symptoms, the correct capture predicate, the
stylesheet audit command and the verification order are in
[`references/hybrid-export-traps.md`](references/hybrid-export-traps.md).

## Images And Visuals

Follow `pptx-visual-spec` and execute raster work through `ai-graphics`. HTML/CSS owns the
design background and all glyphs. Built-in Codex `image_gen` may fill only declared
text-free organic slots; it never renders slide copy. Record its prompt and provenance in
`visual-spec.json`, then inspect the composited background and final PPTX render.
