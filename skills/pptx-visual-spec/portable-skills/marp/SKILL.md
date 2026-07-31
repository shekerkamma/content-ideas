---
name: marp
description: >
  Use when someone says "make marp slides", "marp deck", "marp presentation", "marp slides about",
  or wants to write a MARP Markdown slide deck from a topic, synthesis file, or free-form content
  and export to HTML, PPTX, and/or PDF via the local Marp CLI. Supports three themes: neon
  (Aurora Glass dark, default), light, and corporate. Peer of branded-pptx-deck (.pptx output)
  and ikigai-gamma-slidedeck (Gamma browser-rendered output).
triggers:
  - marp
  - marp deck
  - make marp slides
  - marp slides
  - marp presentation
version: "1.0"
---

# marp

Write a MARP Markdown slide deck and export it to one or more formats.

## Narrative Frame

**This skill's job:** Turn research, analysis, or plans into a deck that someone would actually read — not a document with bullet points forced onto slides.

**Voice for slide writing:** Apply `~/.claude/skills/voice.md` in full. Every slide title is a verdict, not a topic label. Every number is exact. Every bullet is one idea in one sentence.

**Slide writing rules specific to this skill:**

- **Title slide:** The subtitle does the work — it should contain the single most important number or claim in the entire deck. If someone screenshots only the title slide, they should still know why this deck matters.
- **Chapter dividers:** Use them to signal a gear shift, not just navigation. The chapter title is a statement: "The tools that exist are built for agencies, not solos" — not "Market Analysis."
- **Data slides:** The table title pre-interprets the data. Not "Cost Comparison" → "Only 3 tools pass the replace test." Bold or color the cells that contain the decision.
- **Two-column slides:** Each column ends with a tag that gives a verdict. Not "OPTION A" → "FASTEST WIN · 7.1 MO PAYBACK."
- **Pull quotes:** Must be sharp enough to screenshot and share standalone. If a quote wouldn't work as a standalone tweet, rewrite it. The bar: "You don't have a SaaS problem. You have a build-vs-buy decision you never made."
- **Closing slide:** The last slide is the next action, not a summary. One bold claim. One sentence explaining the first move. Nothing else.

**Quality gate before export:** Read every slide title in sequence. If the titles alone tell the story of the deck, the deck is ready. If they don't, rewrite the weak titles before exporting.

## Inputs

| Input | Required | Notes |
|---|---|---|
| `topic` | Yes (or `--file`) | Free-form topic string |
| `--file <path>` | Alt to topic | Path to existing synthesis or research `.md` |
| `--style neon\|light\|corporate` | Optional | Visual theme. Default: `neon` |
| `--format html\|pptx\|pdf\|all` | Optional | Export format. Default: `html` |
| `--slug <slug>` | Optional | Output slug. Auto-derived if omitted |
| `--out <dir>` | Optional | Output directory. Default: `runs/YYYY-MM-DD-<slug>-marp/` |

## Outputs

All files land in the run directory:

| File | Description |
|---|---|
| `<slug>.md` | MARP Markdown source |
| `<slug>.html` | Self-contained HTML deck (always generated) |
| `<slug>.pptx` | PowerPoint export (if `--format pptx\|all`) |
| `<slug>.pdf` | PDF export (if `--format pdf\|all`) |

---

## Execution Instructions

### Pre-flight

1. Parse inputs: extract `topic`, `file`, `style`, `format`, `slug`, `out`.
2. Derive `slug` from topic (kebab-case, max 5 words) if not provided.
3. Derive `run_dir`:
   - If `--out` provided: use it.
   - Else: `runs/YYYY-MM-DD-<slug>-marp/` relative to cwd.
4. Create `run_dir`.
5. Resolve `PPTX_DESIGN_QUALITY_DIR` using `pptx-design-quality`'s Required artifacts
   block, then initialize `deck-brief.md` and `deck-design.json`. Set
   `deck.output_mode` to `image-per-slide`, tailor the context, and validate both files
   before writing slides.
6. Locate Marp binary — try in order:
   ```bash
   which marp 2>/dev/null \
     || ls ~/.local/node_modules/.bin/marp 2>/dev/null \
     || ls ~/.npm-global/bin/marp 2>/dev/null \
     || echo "NOT_FOUND"
   ```
   If `NOT_FOUND`: install to user prefix:
   ```bash
   npm install --prefix ~/.local @marp-team/marp-cli
   MARP=~/.local/node_modules/.bin/marp
   ```

### Stage 1 — Write MARP Markdown

**If `--file` provided:** read the file and use its content as the narrative
source. Derive slide structure from section headings and bullet points.

**If topic provided:** write a 8–12 slide deck from scratch covering the topic.
Structure: cover → 2–3 content slides → optional chapter break → 3–4 content
slides → quote or data slide → closing.

Write the MARP `.md` file to `<run_dir>/<slug>.md`.

**Always include** at the top of the file:

```markdown
---
marp: true
theme: default
paginate: true
style: |
  <THEME_CSS>
---
```

Where `<THEME_CSS>` comes from the theme block below matching `--style`.

#### Theme: neon (Aurora Glass dark — default)

```css
  :root {
    --bg: #080b11; --bg-elev: #0f141d; --ink: #eef2f7;
    --soft: #aeb8c7; --muted: #69748a;
    --teal: #2dd4bf; --sky: #38bdf8; --magenta: #e879f9; --amber: #f6b94b;
    --line: rgba(255,255,255,.09); --glass: rgba(255,255,255,.04);
  }
  section {
    background: #080b11; color: #eef2f7;
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    padding: 60px 80px 80px;
    border-bottom: 4px solid transparent;
    border-image: linear-gradient(90deg,#2dd4bf,#38bdf8,#e879f9) 1;
    font-size: 22px;
  }
  section::after { color: #69748a; font-size: 12px; letter-spacing:.2em; text-transform:uppercase; font-family:monospace; }
  h1 { font-size: 3.2rem; font-weight: 800; letter-spacing: -.02em; line-height: 1.05;
       background: linear-gradient(135deg,#2dd4bf 0%,#38bdf8 50%,#e879f9 100%);
       -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
  h2 { font-size: 2rem; font-weight: 800; letter-spacing:-.02em; color:#eef2f7; }
  h3 { font-family:monospace; font-size:.72rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; font-weight:400; }
  p  { color:#eef2f7; line-height:1.6; }
  ul { list-style:none; padding-left:0; }
  ul li { padding-left:1.4em; position:relative; color:#eef2f7; line-height:1.6; margin-bottom:.35em; }
  ul li::before { content:'→'; position:absolute; left:0; color:#2dd4bf; font-family:monospace; }
  blockquote { border-left:4px solid #2dd4bf; box-shadow:-4px 0 12px rgba(45,212,191,.4);
               padding:1em 2em; margin:0; font-size:1.5rem; font-style:italic; color:#aeb8c7; }
  .cols { display:grid; grid-template-columns:1fr 1px 1fr; gap:0; align-items:stretch; margin-top:1em; }
  .col  { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.09);
          padding:24px 28px; display:flex; flex-direction:column; gap:10px; }
  .col:first-child { border-radius:12px 0 0 12px; border-right:none; }
  .col:last-child  { border-radius:0 12px 12px 0; border-left:none; }
  .col-rule { background:linear-gradient(180deg,transparent,#2dd4bf 20%,#2dd4bf 80%,transparent); box-shadow:0 0 10px #2dd4bf; }
  .col-head { font-family:monospace; font-size:.68rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; }
  .col-title { font-size:1.3rem; font-weight:700; color:#eef2f7; margin:0; }
  .col ul li::before { color:#2dd4bf; }
  .col-tag { font-family:monospace; font-size:.68rem; letter-spacing:.14em; text-transform:uppercase;
             padding-top:12px; border-top:1px solid rgba(255,255,255,.09); margin-top:auto; }
  .col-tag.t { color:#2dd4bf; } .col-tag.m { color:#e879f9; } .col-tag.s { color:#38bdf8; }
  .kicker { font-family:monospace; font-size:.8rem; letter-spacing:.22em; text-transform:uppercase; color:#2dd4bf; }
  .subtitle { color:#aeb8c7; line-height:1.6; font-size:1.1rem; max-width:52ch; }
  .pill { display:inline-block; font-family:monospace; font-size:.68rem; letter-spacing:.14em;
          text-transform:uppercase; padding:5px 14px; border:1px solid rgba(255,255,255,.09);
          border-radius:999px; color:#aeb8c7; margin:4px 6px 4px 0; }
  .pill.t{border-color:#2dd4bf;color:#2dd4bf;} .pill.s{border-color:#38bdf8;color:#38bdf8;} .pill.m{border-color:#e879f9;color:#e879f9;}
  .chip { display:inline-block; font-family:monospace; font-size:.68rem; letter-spacing:.14em;
          text-transform:uppercase; padding:5px 14px; border:1px solid #2dd4bf;
          border-radius:999px; color:#2dd4bf; margin:4px 6px 4px 0; }
  .stat-num { font-size:8rem; font-weight:800; letter-spacing:-.04em; line-height:1; text-align:center; color:#2dd4bf; }
  .stat-label { font-family:monospace; font-size:.72rem; letter-spacing:.22em; text-transform:uppercase;
                color:#69748a; text-align:center; }
  .chapter-num { font-family:monospace; font-size:7rem; font-weight:800; line-height:1;
                 letter-spacing:-.04em; color:#2dd4bf; }
```

#### Theme: light

```css
  section { background:#f8f9fa; color:#1a1a2e; font-family:ui-sans-serif,system-ui,sans-serif;
             padding:60px 80px 80px; border-bottom:4px solid #4361ee; font-size:22px; }
  h1 { font-size:3.2rem; font-weight:800; color:#1a1a2e; letter-spacing:-.02em; }
  h2 { font-size:2rem; font-weight:800; color:#1a1a2e; }
  h3 { font-family:monospace; font-size:.72rem; letter-spacing:.22em; text-transform:uppercase; color:#4361ee; font-weight:400; }
  p  { color:#1a1a2e; line-height:1.6; }
  ul { list-style:none; padding-left:0; }
  ul li { padding-left:1.4em; position:relative; color:#1a1a2e; line-height:1.6; margin-bottom:.35em; }
  ul li::before { content:'→'; position:absolute; left:0; color:#4361ee; font-family:monospace; }
  blockquote { border-left:4px solid #4361ee; padding:1em 2em; margin:0; font-size:1.5rem; font-style:italic; color:#555; }
  section::after { color:#999; font-size:12px; letter-spacing:.2em; text-transform:uppercase; font-family:monospace; }
```

#### Theme: corporate

```css
  section { background:#1b2838; color:#ecf0f1; font-family:ui-sans-serif,system-ui,sans-serif;
             padding:60px 80px 80px; border-bottom:4px solid #3498db; font-size:22px; }
  h1 { font-size:3.2rem; font-weight:800; color:#ffffff; letter-spacing:-.02em; }
  h2 { font-size:2rem; font-weight:800; color:#ffffff; }
  h3 { font-family:monospace; font-size:.72rem; letter-spacing:.22em; text-transform:uppercase; color:#3498db; font-weight:400; }
  p  { color:#ecf0f1; line-height:1.6; }
  ul { list-style:none; padding-left:0; }
  ul li { padding-left:1.4em; position:relative; color:#ecf0f1; line-height:1.6; margin-bottom:.35em; }
  ul li::before { content:'→'; position:absolute; left:0; color:#3498db; font-family:monospace; }
  blockquote { border-left:4px solid #3498db; padding:1em 2em; margin:0; font-size:1.5rem; font-style:italic; color:#bdc3c7; }
  section::after { color:#7f8c8d; font-size:12px; letter-spacing:.2em; text-transform:uppercase; font-family:monospace; }
```

#### MARP slide conventions

```markdown
---             ← slide separator (always 3 dashes on own line)

<!-- _class: lead -->   ← cover / closing (centers content)

### CHAPTER 01 · SECTION NAME    ← h3 = monospace label at top of slide
## Slide Title                    ← h2 = main slide title
Normal paragraph body text.

- bullet one
- bullet two

> "Pull quote text."
> <cite>Attribution</cite>

<div class="cols">
  <div class="col">
    <div class="col-head">LEFT LABEL</div>
    <div class="col-title">Left Title</div>
    <ul><li>item A</li><li>item B</li></ul>
    <div class="col-tag t">TAG TEXT</div>
  </div>
  <div class="col-rule"></div>
  <div class="col">
    <div class="col-head">RIGHT LABEL</div>
    <div class="col-title">Right Title</div>
    <ul><li>item C</li><li>item D</li></ul>
    <div class="col-tag m">TAG TEXT</div>
  </div>
</div>

<!-- Use explicit <ul><li> inside .col — NOT markdown "- " bullets. Markdown
     lists interleaved with HTML <div> blocks mis-nest (markdown-it merges the
     second column's items into the first column's <ul>), which drops the
     custom arrow marker on one column. HTML lists render identically. -->

<div class="stat-label">METRIC LABEL</div>
<div class="stat-num">42%</div>
```

**Rules:**
- Cover slide: `<!-- _class: lead -->` + `# Big Title` + `<div class="kicker">` + `<div class="subtitle">`
- Closing slide: same as cover
- Chapter divider: `<div class="chapter-num">02</div>` then `## Chapter Title`
- Never exceed 80 words per slide body
- Use `---` between every slide
- Vary slide types — no run of 3+ same layout

### Stage 2 — Export

```bash
MARP=<resolved marp binary path>

# Always export HTML
$MARP <run_dir>/<slug>.md --html --output <run_dir>/<slug>.html

# If format includes pptx or all (requires Chrome/Chromium)
$MARP <run_dir>/<slug>.md --pptx --output <run_dir>/<slug>.pptx

# If format includes pdf or all (requires Chrome/Chromium)
$MARP <run_dir>/<slug>.md --pdf --output <run_dir>/<slug>.pdf
```

**If pptx/pdf export fails (no browser):** report the error, fall back to
`python-pptx` builder (same approach as `research-to-deck`), and note the
fallback in the delivery summary.

### Stage 2.5 — Design QA gate (deterministic, required for HTML)

Before delivering, lint the exported HTML with the version-pinned Impeccable detector —
deterministic slop rules, no LLM, no API key. Catches purple gradients, overused
fonts (Inter/Roboto/Geist…), bounce easing, cramped padding, dark glows, low
contrast.

```bash
GATE="${CONTENT_IDEAS_DIR:-$HOME/content-ideas}/scripts/design-qa-detect.sh"
[ -x "$GATE" ] && "$GATE" <run_dir>/<slug>.html \
  || npx -y impeccable@3.4.0 detect <run_dir>/<slug>.html   # fallback: ensure `nvm use 24` first
# exit 0 = clean · exit 2 = anti-patterns found (printed) · exit 1 = blocked (Node<24)
```

- **neon theme:** drop a `DESIGN.md` (Aurora Glass) beside the HTML or run from a
  dir that has one, so intentional teal/glow/gradient is not flagged — only
  deviations are. The `dark-glow` rule may still fire on signature neon glow;
  waive it with an inline `<!-- impeccable-disable dark-glow -- intentional neon -->`
  or note it as accepted, don't restyle.
- **light / corporate themes:** treat any finding as a real defect and fix it.
- If the gate exits 2, report the findings and fix the deck (or waive with reason)
  before marking it delivered. If it exits 1 (no Node 24), say the deck is
  **unreviewed for design QA** rather than presenting it as final.

### Stage 2.6 — PPTX artifact gate

When PPTX output was requested, lint the exported artifact from the repo root even though its slides are
flattened. The `image-per-slide` context disables native-title and layout-repetition rules
while retaining aspect-ratio, slide-boundary, image-resolution, and package checks:

```bash
python3 "$PPTX_DESIGN_QUALITY_DIR/scripts/lint_pptx.py" \
  <run_dir>/<slug>.pptx --config <run_dir>/deck-design.json \
  --json --out <run_dir>/qa/pptx-design-lint.json
```

### Stage 3 — Deliver

Print delivery summary:

```
Marp deck: <slug>
Theme:     <neon|light|corporate>
Slides:    <N>

Deliverables:
  Source:  <run_dir>/<slug>.md
  HTML:    <run_dir>/<slug>.html
  PPTX:    <run_dir>/<slug>.pptx   (if generated)
  PDF:     <run_dir>/<slug>.pdf    (if generated)

To re-export:  ~/.local/node_modules/.bin/marp <slug>.md --pptx
To edit:       open <slug>.md in any Markdown editor
```

---

## Error Handling

| Failure | Action |
|---|---|
| Marp not found + npm not available | Report blocked; deliver `.md` only |
| pptx/pdf export fails (no Chrome) | Fall back to python-pptx builder; note in summary |
| `--file` path not found | Ask user to confirm path |
| Slide count < 5 | Warn; offer to expand |

## Marp Binary Path

Primary: `~/.local/node_modules/.bin/marp`
Fallback install: `npm install --prefix ~/.local @marp-team/marp-cli`
PATH shortcut: `export PATH="$HOME/.local/node_modules/.bin:$PATH"`

---

## Shared Visual Contract

When output includes PPTX, read `pptx-visual-spec`, create and validate
`<run>/visual-spec.json`, and set deck output mode to `image-per-slide`. Marp is explicitly
flattened by design, but its source regions still obey the contract: exact references remain
exact, structured/text content stays in Markdown/HTML, and image-model regions are text-free
and non-evidentiary.

## Skill Relationships

### Category
Scaffolding & Templates

### Dependencies
- `@marp-team/marp-cli` — installed automatically to `~/.local/node_modules/.bin/marp` on first run
- Chrome/Chromium — required for pptx/pdf export only (HTML export works without it)
- `pptx-design-quality` — required context, critique vocabulary, and PPTX artifact lint

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `pptx-design-quality` | Behavioral overlay | every deck; artifact lint when PPTX is exported | `<run>/deck-brief.md`, `<run>/deck-design.json`, `<run>/qa/pptx-design-lint.json` |
| `branded-pptx-deck` | Alternative / Peer | use branded-pptx-deck when output must be a branded .pptx; use marp for markdown-source slides | `<run_dir>/<slug>.pptx` |
| `content-research` | Sequential upstream | optional — content-research produces a synthesis .md that marp uses as `--file` input | `<topic>-research.md` or synthesis .md |
| `research-to-deck` | Orchestrator | research-to-deck can invoke marp as its deck generation stage | `<slug>.md` + exports |
| `video-to-deck` | Sequential upstream | video-to-deck produces a research note that marp can consume as `--file` | `<topic>-research.md` |
| `presentation-accessibility` | Amplifier | run after marp export to audit the HTML output for WCAG compliance | `<run_dir>/<slug>.html` |
| `ikigai-gamma-slidedeck` | Alternative / Peer | ikigai uses Gamma (browser-rendered); marp is the local markdown-first alternative | — |

### Runtime Preamble

At invocation, say:
- "Running /marp — local Markdown slide deck. Themes: neon (default), light, corporate. Formats: html (default), pptx, pdf, all."
- If user wants a branded .pptx with the corporate template: "For a fully branded .pptx file, /branded-pptx-deck is the right tool."
- If user has a research file: "Pass it as `--file <path>` and I will derive the slides from it."

---

## Design-system sync (DESIGN.md)

Each theme's `style:` block is a CSS-variable design system (see the `:root` in the
neon theme). Those tokens are portable: export them to a project-root `DESIGN.md`
(Google Stitch format) so a slide deck and an app UI share one identity — edit tokens
in both to keep them in step. The reverse works too: distill a `DESIGN.md` into a new
fourth theme block and pass it with `--style`. The neon `:root` is the canonical
"Aurora Glass" token set; `~/content-ideas/DESIGN.md` mirrors it. For the
research → distill → build workflow, resource libraries (getdesign.md, Refero), and
the `refero-design` methodology skill, see
`~/content-ideas/references/design-md-resources.md`.

## Gotchas

- **PPTX/PDF export requires Chrome.** If Chrome is not installed, these formats fail silently or with a cryptic error. Fall back to python-pptx builder and note the fallback. If only Chromium is present, point Marp at it: `CHROME_PATH=$(command -v chromium-browser) marp deck.md --pptx --allow-local-files --output deck.pptx`.
- **Marp PPTX is image-based, not editable.** Each slide exports as a full-bleed PNG of the rendered HTML — pixel-perfect but no editable text boxes. If the user needs an editable/branded `.pptx`, use `branded-pptx-deck` instead.
- **Open a deck on a WSL/Windows host:** `cmd.exe /c start "" "$(wslpath -w deck.pptx)"` launches it in the Windows default app.
- **Two-column `.col` blocks must use explicit `<ul><li>`, never markdown `- ` bullets.** Markdown lists interleaved with HTML `<div>` blocks mis-nest — markdown-it merges the second column's items into the first column's `<ul>`, dropping the arrow marker on one column. See the conventions block above.
- **Never exceed 80 words per slide body.** Slides that exceed this are documents, not slides.
- **Quality gate is mandatory before export.** Read all slide titles in sequence — if they do not tell the story alone, rewrite before exporting.
- **`--` must appear on its own line as the slide separator.** Three dashes (`---`) in a MARP file always means a new slide — do not use them inside a slide for visual rules.
- **neon theme uses gradient text on h1.** If the heading is very short (one word), the gradient may look bad — add a subtitle or kicker to balance the slide.

## Images And Visuals

Markdown images reference assets selected by `visual-spec.json` and executed through
`ai-graphics`. HTML/SVG remains deterministic for structured/text-bearing visuals. Built-in
Codex `image_gen` is the primary subscription-backed path for eligible text-free organic
imagery; provider-adapter status applies only when explicitly selected. Inspect the exported
PPTX because Marp flattens each slide.
