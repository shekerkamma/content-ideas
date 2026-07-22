---
name: branded-pptx-deck
description: Use when the user wants a new native .pptx (not HTML) slide deck built programmatically — executive summary, board deck, KPI/scorecard, use-case realization, or a material PowerPoint redesign. Triggers on "/branded-pptx-deck", "make a pptx deck", "executive deck", "board deck", "slide deck as pptx", "revamp this into slides", "adapt the Canva template", "presentation as PowerPoint". For controlled inspection, text/notes edits, or slide reordering in an existing .pptx, use `pptx-toolkit`. For HTML/CSS slide output use the `presentation` skill instead. For HTML/CSS slide output instead of .pptx, use `marp` instead.
trigger: /branded-pptx-deck
argument-hint: "[what deck — e.g. 'executive deck from analysis.json', 'revamp report.pdf into 25 slides']"
category: Business Automation
---

# branded-pptx-deck

Build **native, editable .pptx** decks programmatically with python-pptx. This is for
PowerPoint output. (For the HTML/CSS presentation system, use the `presentation` skill
instead — different tool, different output.)

The skill ships a reusable toolkit so you never re-derive layout mechanics or re-hit
the two classic failures: text overflowing between boxes, and the malformed-shadow XML
that makes PowerPoint show a **"repair"** prompt.

## Files

- `scripts/pptxkit.py` — the toolkit: `Brand` (palette), `Deck` (slide factory, `rect`,
  `text`, `header`, `footer`, `chart_barh`, `chart_matrix`, `picture_centered`,
  `save` with built-in validation), and `validate_pptx()`.
- `scripts/preview_pptx.py` — render any `.pptx` → per-slide PNGs + contact sheets, with
  red dashed boxes flagging likely text overflow. **Your eyes for QA.**
- `../../scripts/officecli_qa.py` — optional OfficeCLI QA gate: validates, checks
  issues, and renders the final `.pptx` to HTML/PNG when `officecli` is installed.
- `reference/brand.md` — palette, the Canva-Pro template location, slide-pattern recipes,
  and delivery steps.

## Upstream: chain skills for the content — do NOT hand-roll analysis

This skill is the **render stage only**. Its job is styled, validated `.pptx`. The findings,
charts, scores, and narrative should come from the existing skills — chaining them is the
default, not the exception. Hand-rolling the analysis is how unvalidated errors (e.g. citing
a wound-down company as live) reach an executive deck.

Pick the upstream chain that fits, then feed its outputs here:

| Need | Use first |
|------|-----------|
| Ingest sites / repos / videos / docs into a knowledge base | `content-research` (or `competitive-intel-sprint` for a competitor) |
| Market / VC thesis / vertical / competitive / unit-economics analysis | `ai-strategy-researcher` (full) or `ai-strategy-brief` (1-pager) |
| Quant findings + publication-quality charts + **validation** | `ai-analyst` (`/analyze`) — its validation step is what catches bad facts |
| Score lanes / verticals (attractiveness, priority) | `vertical-scorer` (don't invent H/M/L by hand) |
| Narrative arc (BLUF, storyboard, story beats) | `ai-analyst`'s story-architect / storytelling |
| Quantify a single opportunity | `ai-analyst` (`/analyze` → size-opportunity) |

Only build inputs by hand when no skill covers them. **Always run the content through a
validation pass before rendering** — every named entity, count, status, and claim checked
against source. If a skill produced the data, reuse its validation; if you assembled it
yourself, validate explicitly.

## Workflow (do these in order)

1. **Get the content by chaining the skills above** into a structured source
   (JSON/markdown/outline). Decks are *generated from validated data*, not typed
   slide-by-slide. Never invent metrics; if a number isn't in the source, use a qualitative
   label and say so. Confirm entity statuses (is the company still operating? right batch?).
2. **Decide the spine.** For executives: lead with the answer (BLUF), an executive-summary
   one-pager, a storyboard of the argument, then proof, then the ask. Write **action
   titles** (every title is a so-what assertion). Honor explicit slide-count minimums.
3. **Write and validate the visual specification.** Read
   `skills/pptx-visual-spec/references/visual-sourcing-rules.md`, classify every meaningful
   visual region, write `<run>/visual-spec.json`, and validate it with
   `skills/pptx-visual-spec/scripts/validate_visual_spec.py`. Exact-state evidence is
   extracted; ordinary data and claims remain native; image models are text-free and
   non-evidentiary.
4. **Build with `pptxkit`.** Write a builder script that imports `pptxkit` and composes
   slides. Keep brand/mechanics in the kit; keep content in your script. Use
   `shrink=True` on any text box whose length is data-driven.
5. **Sanitize client-facing text.** Visible slide text must not expose internal production
   language unless the user explicitly asks for an audit appendix. Keep tool names, source
   filenames, timestamps, "synthesis" labels, implementation notes, and validation notes in
   source/run files rather than on client slides. Use client-facing labels such as
   `Business implication`, `Decision`, `Operating model`, or `Next move`. Also scan for
   internal/source terms such as `transcript`, `hyperframe`, `Excalidraw`, `YouTube`,
   `source`, `audit`, `validation`, `synthesis`, `Codex`, `Claude`, file paths, and raw
   timestamps before delivery.
6. **Validate + preview.** `Deck.save()` auto-validates and raises on malformed XML.
   Then run `python3 scripts/preview_pptx.py <out.pptx>` and actually *look* at the
   contact sheets; fix any overflow before delivering. After that, run the shared
   OfficeCLI QA gate from the repo root:
   `python3 scripts/officecli_qa.py <out.pptx> --out <run>/qa/officecli`.
   When `officecli` is installed, use its HTML/PNG render as the preferred real
   render evidence. If OfficeCLI is skipped or fails, use PowerPoint, LibreOffice
   PDF, Google Slides import, or equivalent because `preview_pptx.py` shows
   pictures as placeholders.
7. **Declare editability.** For decks with diagrams, record one of these in the run report
   and final response: `PPT-native editable diagrams`, `Excalidraw-source editable
   diagrams`, or `non-editable visual render`. If the user asked for editable slides,
   source-layer editability is not enough unless they explicitly accept it.
8. **Set status honestly.** Use `*-draft.pptx` before QA, `*-reviewed.pptx` only after
   XML validation, real render QA, visible-text scan, and slide-by-slide content/design
   validation pass, and `blocked` when a required render/editability path is unavailable.
9. **Deliver.** This user opens decks in Windows PowerPoint from WSL. Copy to
   `/mnt/c/Users/<user>/OneDrive/Desktop/` and open with
   `powershell.exe -NoProfile -Command "Start-Process '<C:\...>'"`. A file open in
   PowerPoint is **locked** — if a re-copy fails with "Permission denied", write the
   corrected file under a **new name** instead of overwriting.

## Minimal example

```python
import sys; sys.path.insert(0, "<skill>/scripts")
from pptxkit import Deck, Inches, Pt, PP_ALIGN

d = Deck(footer="Acme · Executive Briefing | 2026")
b = d.b

# cover
s = d.slide(fill=b.NAVY)
d.text(s, "EXECUTIVE BRIEFING", d.M, Inches(0.95), Inches(7), Inches(0.4), size=15, color=b.TEAL, bold=True)
d.text(s, "Winning In Agentic AI", d.M, Inches(1.5), Inches(8), Inches(1.1), size=46, color=b.WHITE, bold=True, shrink=True)

# a content slide with header + bullets
s = d.slide(fill=b.WHITE)
d.header(s, "The Value Concentrates In A Few Lanes", "Action title = the takeaway")
d.text(s, [{"text": t, "bullet": True, "space_before": 10, "size": 14} for t in
           ["First point", "Second point", "Third point"]],
       d.M, Inches(1.8), d.CW, Inches(3.5), shrink=True)
d.footer(s, 2, 2)

d.save("docs/reports/acme-exec.pptx")   # validates; raises if it would need repair
```

## Practical OfficeCLI QA Run

For any branded PPTX build, keep the builder, PPTX, and QA evidence in the same
run folder. This is the repeatable path:

```bash
RUN=runs/<date>-<topic>-branded-pptx
python3 "$RUN/build_deck.py"                         # writes *-draft.pptx
python3 skills/branded-pptx-deck/scripts/preview_pptx.py "$RUN/<name>-draft.pptx"
python3 scripts/officecli_qa.py "$RUN/<name>-draft.pptx" --out "$RUN/qa/officecli"
```

If `qa/officecli/qa-summary.md` reports `Status: partial`, the deck's XML,
issue scan, and HTML render passed, but the managed sandbox blocked Chromium
screenshot rendering. For client-facing `*-reviewed.pptx`, rerun the exact
OfficeCLI command with `--required` outside the sandbox or with approved
escalation:

```bash
python3 scripts/officecli_qa.py "$RUN/<name>-draft.pptx" --out "$RUN/qa/officecli" --required
```

Only rename/copy to `*-reviewed.pptx` after:
- `Deck.save()` validation passed.
- `preview_pptx.py` contact sheets were inspected.
- OfficeCLI QA is `passed`, or a documented equivalent real-render fallback was
  inspected.
- Visible client-facing text has no internal process terms.

## Hard rules (learned the hard way)

- **Never** append a second `<a:effectLst>` after `shape.shadow.inherit = False`. The kit's
  `rect(shadow=True)` already reuses the single one. If you write raw OOXML, do the same,
  then run `validate_pptx()`.
- A clean python-pptx round-trip is **not** proof of validity — only `validate_pptx()` /
  PowerPoint catches the effectLst + child-order issues.
- Re-skin by passing a different `Brand(...)`; don't fork the kit.

## Reference deck builders

Worked examples (chained from one analysis pack) live in the `ticketforge` repo:
`scripts/build_yc_deck_v2.py` (analyst), `build_yc_usecase_deck.py` (Canva-adapted
use-case/realization, org-named), `build_yc_exec_deck.py` (executive: summary, five-beat
storyboard, decision scorecard, where-to-play, decision/ask). Read these for slide-pattern
recipes (KPI grid, cards, comparison, scorecard, use-case realization, storyboard).

---

## Shared Visual Contract

`pptx-visual-spec` is mandatory and overrides duplicated or dated visual-routing prose.
Read `skills/pptx-visual-spec/references/visual-sourcing-rules.md`; emit and validate
`<run>/visual-spec.json`. This skill's output mode is `native`: image assets may occupy
regions inside otherwise-native slides, but titles, claims, data, diagrams that are feasible
in PowerPoint, captions, and citations remain editable objects.

## Skill Relationships

### Category
Business Automation

### Dependencies
- `pptxkit.py` — required; lives in `scripts/pptxkit.py` within this skill directory
- `preview_pptx.py` — required for QA; lives in `scripts/preview_pptx.py`
- `officecli-qa` — optional preferred real-render QA; uses repo root
  `scripts/officecli_qa.py` when `officecli` is installed
- `pptx-visual-spec` — mandatory visual-routing overlay and schema

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `content-research` | Sequential upstream | when ingesting sites/repos/docs first | `$CONTENT_HOME/research/*.md` or summary files |
| `competitive-intel-sprint` | Sequential upstream | when competitor content is needed | research output files |
| `ai-strategy-researcher` | Sequential upstream | when market/vertical analysis needed | strategy report (Word doc or markdown) |
| `ai-strategy-brief` | Sequential upstream | for 1-page exec brief as input | brief markdown |
| `ai-analyst` | Sequential upstream | for quant findings + validated charts | analysis JSON / chart PNGs |
| `vertical-scorer` | Sequential upstream | for scored lane/vertical tables | scorer output markdown |
| `mkt-visual-identity` | Sequential upstream | when on-brand visuals required | `{brand_context}/visual-identity/tokens.json` |
| `pptx-visual-spec` | Behavioral overlay | every deck build | `<run>/visual-spec.json` |
| `presentation-accessibility` | Amplifier downstream | optional post-QA pass | output `.pptx` |
| `marp` | Alternative / Peer | if markdown slides preferred over .pptx | — |
| `mcp__claude_ai_Gamma__generate` | Alternative / Peer | if browser-rendered slides preferred | — |

### Runtime Preamble

At invocation, surface this to the user:

> "Before I build the deck, have you run any upstream skills to generate the content?
> - `/content-research` or `/competitive-intel-sprint` → for ingested research
> - `/ai-strategy-researcher` or `/ai-strategy-brief` → for market/vertical analysis
> - `/ai-analyst` → for validated quant findings and charts
> - `/vertical-scorer` → for scored lanes
> - `/mkt-visual-identity` → for tokens.json (brand colors/fonts)
>
> If content is already ready, tell me the file path and I'll build from it.
> Alternatives if you want a different format: `/marp` (markdown slides), Gamma (browser-rendered)."

---

## Gotchas

- **Never render unvalidated content:** Every named entity, metric, and claim must be verified before it lands on a slide. If you assembled the data yourself (not from an upstream skill), run a validation pass first. Wrong facts in an executive deck are a delivery failure.
- **No internal process language on client slides:** Don't show tool names, source paths,
  timestamps, audit labels, `transcript`, `hyperframe`, "synthesis" labels, or validation
  notes as visible slide text. Those belong in the run report, speaker notes only when
  requested, or source artifacts.
- **Embedded images need real render QA:** The built-in preview is useful for text and
  geometry, but it does not show embedded pictures. Prefer OfficeCLI screenshots via
  `python3 scripts/officecli_qa.py`; if skipped, render to PDF or inspect in
  PowerPoint before delivering decks that include diagrams, canvases, screenshots,
  or previews.
- **Reviewed requires evidence:** Do not name a deck `*-reviewed.pptx` unless the run
  contains the validation evidence: XML validation result, OfficeCLI QA summary
  when available, real render/contact sheet or PowerPoint inspection, visible-text
  internal-term scan, and slide-by-slide content/design validation notes.
- **Readable diagrams are mandatory:** If a deck embeds diagram images, the labels must be
  readable in the real render. If not, enlarge the visual, split the slide, or rebuild the
  labels/diagram as native PPT shapes.
- **Editability must be explicit:** If diagrams are rendered images with editable source
  files elsewhere, say so. Do not imply PowerPoint-native editability when the deck only
  embeds image previews.
- **Never re-derive the effectLst:** Appending a second `<a:effectLst>` after `shape.shadow.inherit = False` corrupts the file and triggers PowerPoint's repair prompt. Use `rect(shadow=True)` from the kit — it manages this correctly.
- **A clean python-pptx round-trip is not proof of validity:** Only `validate_pptx()` or PowerPoint itself catches effectLst and child-order issues. Always call `Deck.save()` (which auto-validates) — do not bypass it.
- **File locked in PowerPoint:** If re-copy fails with "Permission denied", the deck is open in PowerPoint. Write the corrected file under a new filename — do not attempt to overwrite.
- **Status before delivery:** Label all decks explicitly as `draft`, `reviewed`, or `blocked`. Use filename suffixes that match: `*-draft.pptx`, `*-reviewed.pptx`. Never present an unreviewed deck as final.
- **tokens.json is required for branded output:** If `/mkt-visual-identity` has not been run, the deck will fall back to hardcoded Brand() defaults. Warn the user and proceed with defaults rather than blocking — but note the deck is not on-brand.
- **Never fork pptxkit.py for re-skinning:** Pass a different `Brand(...)` object instead. Forking creates maintenance drift.

## Images And Visuals

Follow `pptx-visual-spec`; route raster execution through `ai-graphics`. In Codex hosts,
built-in `image_gen` is the primary subscription-backed route for eligible text-free organic
imagery. OmniRoute/provider state applies only when that adapter is explicitly selected.
Confirm image availability with an actual render and inspect the placed crop in OfficeCLI.
