---
name: video-to-deck
description: >
  Use when someone says "turn this video into a deck", "video to slides", "video to presentation",
  pastes a video URL and wants a full deliverable, or asks for a presentation package from any
  video content. Runs a 4-stage pipeline: watch (transcript) → content-research (enrich) →
  visual route selection (excalidraw for conceptual/non-architecture visuals, explainer-graphic
  for infographic analogies, architecture-presentation for technical or solution architecture)
  → branded PPTX deck/package output.
  For a Markdown-first slide deck without video input, use `marp` instead.
---

# Video-to-Deck Skill System

Orchestrator that chains four child skills in sequence to turn any video into a
complete presentation package. The user provides a video URL (or local path) and
optionally a focus question. You deliver a full branded PPTX deck package — no
manual steps between stages. Markdown files are source/audit artifacts, not the
final deliverable.

## Canonical Genspark Contract

When Genspark participates in the pipeline, read and follow the installed sibling
contract at `../pptx-visual-spec/references/genspark-video-deck-contract.md` (repo
source: `skills/pptx-visual-spec/references/genspark-video-deck-contract.md`). It
governs scene-complete evidence, rich connector context, evidence-driven slide
count, same-project expansion, headed Playwright recovery, factual-integrity
scans, editability labels, handoff JSON, QA status, and cross-host behavior. This
skill may tighten those rules but may not weaken them.

Write and validate `<run>/genspark-handoff.json` whenever Genspark is requested,
attempted, or used as a reference—even when hosted generation is blocked and the
pipeline continues locally.

## Onboarding (first run only)

If `~/.claude/skills/video-to-deck/config.json` does not exist, ask these questions
before starting and save the answers:

1. **Deck theme**: "Enterprise Consulting (white)" or "Midnight Executive (dark)"? → default: Enterprise Consulting
2. **Include NotebookLM step?** Yes/No → default: Yes
3. **Auto-open outputs?** Yes/No → default: Yes
4. **Output directory**: Where to save deliverables → default: current working directory

Save as `config.json`:
```json
{
  "theme": "enterprise-consulting",
  "include_notebooklm": true,
  "auto_open": true,
  "output_dir": "."
}
```

On subsequent runs, load config silently. User can reconfigure with `/video-to-deck config`.

## Visual Routing Rule

Read and apply the mandatory `pptx-visual-spec` overlay before visualization:
`skills/pptx-visual-spec/references/visual-sourcing-rules.md`.

Video-specific interpretation:

- An exact application, IDE, terminal, browser, document, collaboration, or
  demonstrable product state is `exact-source-evidence` and routes to `extract`.
  Do not redraw it even when the pixels contain text or numbers.
- A reference frame used only for its underlying information routes to `native`
  or the appropriate deterministic `author-*` route.
- Use Excalidraw only when a hand-drawn editable source is intentionally desired;
  use Draw.io/architecture-presentation for explicit technical architecture.
- `image-model` is limited to new text-free organic/editorial regions and can
  never replace a missing hyperframe or product screen.

**Capture contract (source of truth):** the hyperframe set is produced by
`watch --detail scene-complete --resolution 1280` (dense sample + webcam-masked
perceptual-hash dedup, uncapped) so **every distinct screen** is captured. A
capped `efficient`/keyframe sample is discovery only and must NEVER drive the
storyboard — it drops docs pages, whiteboard panels, and demo screens.

Default reconstruction path:
`scene-complete capture -> screen-states.json -> visual-sourcing gate -> extracted/authored PNG asset -> native branded PPTX slide shell`.

Optional illustrative path:
`storyboard need -> text-free image-model prompt -> generated PNG -> fixed image slot inside native/HTML slide shell`.

Every meaningful hyperframe must produce a persistent visual asset. The PNG is
placed inside an otherwise-native slide whose title, callouts, captions,
citations, and footer remain live editable objects. A full-slide flattened image
is not allowed, but an image asset inside a native slide is the default contract.

The shared contract owns Codex-versus-provider execution rules. This skill's
Claude bridge remains `scripts/generate_with_codex_cli.py`; use it only for a
visual already classified as `image-model`.

## Non-Negotiable Delivery Gates

Do not call a video deck `reviewed` unless every gate below has passed and the
run contains the evidence artifacts.

0. **Deck-context gate:** `pptx-design-quality` produced and validated
   `<run>/deck-brief.md` plus `<run>/deck-design.json`. The brief records the audience,
   decision, narrative promise, anti-references, evidence standard, and editability mode.
1. **Story gate:** `ai-analyst` produced the upstream story spine when exposed.
   If it is unavailable, the run status must say `fallback`; do not silently
   treat fallback synthesis as equivalent.
2. **Evidence gate:** `grill-me` or the manual fallback challenged every
   slide-level claim against the transcript/research and recorded rebuild
   decisions.
3. **Capture-completeness + coverage gate:** the hyperframe manifest MUST come
   from a `watch --detail scene-complete` pass (dense sample + webcam-masked dHash
   dedup, uncapped) — **never** a capped `efficient`/keyframe sample. Record the
   distinct-screen count **and `meta.max_gap_seconds`** in the run report. A large
   `max_gap_seconds` on a screencast is a flag to eyeball (a section may have been
   over-collapsed by the dedup); on a talking-head stretch it is expected. Then
   every distinct screen maps to a slide, a recreated visual, a grouped duplicate,
   or an explicit skip reason; presenter-only frames may be excluded but must be
   accounted for. **Slide count is not a constraint — one slide per distinct
   captured screen is acceptable and always preferred over dropping a screen.**
   Building the storyboard from a sparse/capped sample is a **blocking defect** —
   it silently drops docs pages, whiteboard panels, and demo screens and guts the
   storyline.
   **Slide count is never a ceiling.** Derive the count from the evidence map,
   narrative density, and meaningful screen coverage. A count supplied by the
   user or an upstream generator is a minimum or planning estimate unless the
   user explicitly requests a hard maximum. Add slides whenever combining
   distinct screens would make the evidence illegible or omit an operating step.
4. **Client-language gate:** native/authored visible slide text has no internal terms:
   `transcript`, `hyperframe`, `Excalidraw`, `YouTube`, `source`,
   `validation`, `synthesis`, `audit`, `Codex`, `Claude`, file paths, or
   timestamps.
5. **Render gate:** PPTX XML validation and the deterministic
   `pptx-design-quality` lint pass, then a real render pass confirms
   embedded diagrams appear, are readable, and are not cropped. Prefer the shared
   OfficeCLI QA gate:
   `python3 scripts/officecli_qa.py <deck.pptx> --out <run>/qa/officecli`.
   If OfficeCLI is skipped or fails, use PowerPoint, LibreOffice PDF, Google
   Slides import, or equivalent. The lightweight preview alone is insufficient
   for decks with embedded visuals.
6. **Editability gate:** declare one editability mode in the run report and
   final response: `PPT-native editable diagrams`, `Excalidraw-source editable
   diagrams`, `hybrid editable`, or `non-editable visual render`. `Hybrid
   editable` means native slide structure/text plus source-backed PNG evidence
   and editable HTML/SVG source for authored diagrams.
7. **Proof gate:** named examples in the source, such as companies/products,
   must survive synthesis as named proof cards unless excluded for a stated
   reason.
8. **Generated-asset gate:** every image-model asset is text-free, labeled
   `generated` in provenance, stores its final prompt and resolved engine, and
   is not presented as evidence. Any generated glyph, logo, UI, person, result,
   facility, or certification is a blocking defect.

Status rules:
- Use `*-draft.pptx` before all gates pass.
- Use `*-reviewed.pptx` only after all gates pass.
- Use `blocked` when a required dependency, render path, or editability mode is
  unavailable.
- Use `fallback` when the deck is usable but a required upstream skill was
  unavailable and a manual equivalent was used.

## Pipeline

### Stage 1: Watch → Extract
Invoke the `/watch` skill on the provided video URL.
- Extract the full transcript and key visual frames
- Identify the core topic, thesis, and structure
- Produce a structured summary: title, sections, key insights, notable visuals
- **Primary hyperframe capture: invoke watch with `--detail scene-complete
  --resolution 1280`.** This is the screencast-optimized coverage pass — watch
  densely samples (1 fps), masks the presenter-webcam corner, and keeps every
  DISTINCT screen via a perceptual-hash + stability dedup (uncapped). The
  storyboard is then built from ALL scene changes, not a sparse sample. A
  50-keyframe `efficient` pass is discovery ONLY and is **not** sufficient: it
  drops docs pages, whiteboard panels, and demo screens, gutting the storyline.
  Use `efficient` only for a fast topical scan, never as the manifest source of
  truth. (`scene-complete` supersedes the older two-step efficient +
  `extract_screen_states.py` coverage pass.)
- For long videos or visually dense sections, use the efficient pass to find
  candidate sections, then re-run watch on those exact ranges with
  `--start`/`--end`, `--timestamps`, or a higher detail mode only where needed.
  Do not jump directly to `token-burner` for the whole video unless the user
  explicitly accepts the cost.

**Pass forward:** structured summary + transcript + topic name

Also create `screen-states.json` and a human-readable hyperframe manifest before visualization:
- List every extracted frame/hyperframe with timestamp, path, classification,
  and disposition.
- Classify as `diagram`, `text-slide`, `demo-screen`, `terminal-result`,
  `collaboration-screen`, `talking-head`, or `duplicate/low-value`.
- Recreate every `diagram`, `text-slide`, and meaningful `demo-screen` in the
  deck unless it is explicitly marked duplicate.
- Exclude YouTuber/talking-head frames by default. Do not use presenter face
  screenshots in the branded deck unless the user explicitly asks for source
  evidence or a thumbnail-style appendix.
- If any meaningful hyperframe is skipped, state why in the manifest and final
  report.
- Save the timestamped transcript as `<run>/transcript.txt` using one
  `[MM:SS] text` segment per line.
- Save a machine-readable `<run>/frames_manifest.md` with `File`, `Timestamp`, and
  `Description` columns and paths relative to the run. Keep the richer
  `<topic>-hyperframes.md` for classification and disposition; it does not replace the
  machine manifest.

Normalize the Stage 1 artifacts with `presentation-source-bundle`:

```bash
python3 skills/presentation-source-bundle/scripts/build_presentation_evidence.py \
  --run <run> --title "<topic>"
```

This produces `<run>/presentation-evidence.json`, the durable source inventory for
transcript segments, frames, source slides when present, checksums, and rights status. Do
not infer slide-to-transcript or slide-to-frame alignment from ordering alone.

Then create a `visual-spec.json` before rendering:
- One record per meaningful hyperframe or grouped duplicate set.
- Capture title, layout type, text blocks, cards, table rows, connectors,
  visual hierarchy, colors, and source frame paths.
- Route each meaningful visual region using the shared vocabulary: `extract`,
  `place-asset`, `native`, `author-html`, `author-svg`, `author-react`,
  `image-model`, or `none`.
- Record source location, evidence status, reason, editable source/asset paths,
  placement, execution metadata, and QA as required by
  `skills/pptx-visual-spec/references/visual-spec-schema.json`.
- Validate with `skills/pptx-visual-spec/scripts/validate_visual_spec.py`.
- Validate the complete evidence → slide plan → visual chain with
  `skills/pptx-visual-spec/scripts/validate_presentation_contracts.py`; an extract visual
  without a valid evidence ID is a blocking defect.
- Treat this spec as the source of truth for both reconstruction QA and final
  PPTX rendering.

### Stage 2: Research → Enrich
Invoke the `/content-research` skill on the extracted content, enriched with deeper tools:
- Use **Exa** (`web_search_exa`) to find related sources, papers, and expert commentary on the video's topic
- Use **`/wikipedia`** for baseline context if the topic involves established concepts
- Use **`/firecrawl`** if the video references specific websites or products worth scraping
- Do NOT fall back to basic WebSearch — always prefer Exa and Firecrawl for richer results
- Create a research note in second-brain format (if in a project with second-brain/)
- Otherwise create a standalone `<topic>-research.md`
- Extract deck-usable facts, figures, quotes
- Separate internal-only insights from customer-facing content

**Pass forward:** enriched research note + deck-usable content

### Stage 2.5: Story Architect + Analyst Synthesis → Storyboard
Before visualization or PPTX rendering, run a synthesis/storyboard step so the
deck has a narrative spine instead of becoming a pile of recreated frames.
After the story spine is resolved, initialize and tailor `deck-brief.md` plus
`deck-design.json` with `pptx-design-quality`; validate both before Stage 3.

Preferred path:
- Use `story-architect` as the concrete upstream storyboard stage whenever it is
  installed/exposed or present in the repo. This stage must produce BLUF,
  audience decision, tension, argument arc, slide spine, evidence map, content
  cuts, and rebuild instructions. Feed this artifact into the visual spec and
  PPTX builder.
- Use `ai-analyst` as the required upstream synthesis step whenever it is
  installed/exposed. Do not skip it for convenience. Without this stage, the
  deck tends to become a pile of frames or notes instead of an executive
  storyboard.
- Use `ai-analyst` especially for quantitative claims, market sizing, metrics,
  scorecards, trend claims, and any story that depends on data interpretation.
- Use its story-architect/storytelling output to produce BLUF, argument arc,
  slide sequence, evidence map, confidence notes, and chart/table needs.
- Feed the `ai-analyst` output into both the visual spec and the branded PPTX
  builder. Slide titles, business implication panels, executive summary, and
  conclusion should come from the analyst story spine, not from raw transcript
  snippets alone.

Fallback path when `ai-analyst` is not available:
- Use `strategy-consulting` / consulting synthesis to produce a senior-partner
  storyboard: Context -> Tension -> Resolution -> Proof -> Decision/Ask.
- Label the run report clearly: `ai-analyst unavailable; strategy-consulting
  synthesis fallback used`.
- If prior `ai-analyst` packs exist in the repo, reuse their schema and record
  that the current run used an `ai-analyst`-style fallback because the callable
  skill/tool was unavailable.

Output:
- `<topic>-storyboard.md`
- `<topic>-story-architect-pack.md/json`
- `<topic>-analyst-story-pack.md/json` when `ai-analyst` or an
  `ai-analyst`-style fallback is used
- Optional `<topic>-findings.json` when data-backed findings or chart inputs are
  available
- `<run>/deck-brief.md`
- `<run>/deck-design.json`
- `<run>/slide-plan.json` — one semantic plan record per intended slide, including claims,
  evidence IDs, audience job, visual IDs, speaker notes, and accessibility intent

**Pass forward:** storyboard, slide spine, evidence map, visual-spec inputs

### Stage 2.6: Grill-Me Validation → Self-Correction
Before the final PPTX build, run a skeptical validation pass against the
transcript and any research artifacts. This is mandatory for client-facing video
decks.

If `slide-plan.json` has claims with `evidence_ids`, run
`pptx-design-quality`'s `check_claim_evidence.py` first as a fast mechanical
pre-pass (regex number matching against cited evidence text) — it catches
unsourced numbers cheaply before the richer semantic Grill-Me pass below, which
it does not replace.

Preferred path:
- Use `grill-me` when it is installed/exposed.
- Challenge each slide-level claim against the transcript: "Is this directly
  supported, a fair synthesis, or an unsupported interpretation?"
- Self-answer each challenge with timestamped transcript evidence or a clear
  correction.

Fallback path when `grill-me` is not available:
- Create a `<topic>-grill-me-validation.md` file manually using the same pattern:
  claim, challenge, transcript evidence, self-answer, rebuild decision.
- If a claim is more consultant interpretation than transcript-supported, either
  soften it or replace it with transcript-backed language.
- If a visual contains unsupported wording, regenerate the visual source and
  preview before rebuilding the deck. Do not fix only the slide text while
  leaving the old claim embedded inside the visual.

Output:
- `<topic>-grill-me-validation.md`
- Optional `<topic>-transcript-excerpts.md` with the relevant timestamped
  transcript passages used for validation
- The validation must include both content and slide-design questions: claim
  support, client-facing wording, visual readability, layout hierarchy,
  missing/over-generalized proof, and whether each visual is editable at the
  declared layer.

**Pass forward:** corrected slide spine, validated claims, visual corrections

### Stage 3: Visualize
Choose one visual route using the Visual Routing Rule.

**Route 0 — Persistent hyperframe assets (default for slide recreation):**
Use this before final PPTX rendering when the frame is a diagram, table,
scorecard, slide, or layout-heavy visual.
- **Extract is the correct route for a specific screen in a video** — exact-state
  evidence is placed, never redrawn into native shapes or HTML "to claim
  editability" (`pptx-visual-spec` gate). Native redraw of an exact UI screen is a
  route violation; keep native only for titles, captions, callouts, and structured
  so-what content.
- **Webcam-mask the extract before placing it.** Screencasts carry a presenter
  bubble (usually a fixed bottom-right corner). Fill that corner with a
  locally-sampled background color (PIL: sample a clean patch just left of the
  bubble, paint the corner rect) so the placed frame reads as clean UI, not a
  pasted-on screenshot. `scene-complete` already masks the webcam for *dedup*; the
  saved frame is unmasked, so masking for *display* is a separate prep step.
- Extract exact UI/application frames into cropped PNG assets.
- Generate SVG for authored diagrams, boxes, arrows, and geometric figures.
- Generate HTML/CSS for authored text-heavy diagrams and whiteboards.
- Render authored SVG/HTML to PNG and preserve the editable source file.
- Insert the PNG as the primary evidence visual inside a native slide shell.
- Keep data summaries, titles, callouts, captions, and citations native.

**Route 0B — Generated illustrative raster (optional; never hyperframe evidence):**
- Invoke the installed `imagegen` skill and built-in `image_gen` tool for a new text-free photo,
  illustration, texture, or metaphor only when the storyboard materially needs
  it and no exact approved asset exists.
- Codex writes the prompt and constraints; the image tool generates the PNG.
  Treat the image tool's returned/logged engine as authoritative.
- Use the signed-in Codex/ChatGPT subscription path by default. Do not require
  an API key, OmniRoute, or a separate paid provider for this normal path.
- Do not send diagrams, labels, KPIs, tables, product screens, terminal output,
  logos, or factual proof to an image model.
- Place the generated PNG in a fixed slot owned by a native or HTML/CSS shell.
  Keep every word and claim outside the generated bitmap.
- Save the final prompt beside the asset, add `generated` provenance, and record
  `execution_path`, `auth_mode`, the active orchestration model, and any
  image-engine identifier actually returned by the tool. Inspect the PNG at full resolution;
  any glyph-like mark or false product detail requires regeneration or removal.
- A successful built-in `image_gen` call is the availability check. Consult
  `~/.claude/skills/ai-graphics/deck-image-routing.md` only for an explicitly
  requested OmniRoute/provider path; its status does not govern the built-in
  subscription route.
- Claude Code invocation:
  `python3 scripts/generate_with_codex_cli.py --prompt-file <prompt.txt> --out <asset.png> --workdir <run-dir>`.
  The output must be inside the declared workdir. Preserve the generated
  `<asset.png>.provenance.json` sidecar and feed its fields into
  `visual-spec.json`.

**Route A — Excalidraw conceptual recreation (NOT the default; opt-in only):**
Route 0 is the default for every screencast, product demo, IDE/terminal, browser,
docs, or dashboard video — recreate each screen as an extracted/authored PNG asset
on a native slide. Use Route A **only** when the user explicitly wants a hand-drawn
whiteboard aesthetic for genuinely conceptual/framework content, and never for
product/UI/demo screens (those are `exact-source-evidence` → Route 0 extract).
Invoke the `/excalidraw` skill using the key frames and transcript from
`/watch`.
- Recreate every meaningful diagram/text hyperframe as one or more editable
  Excalidraw diagrams. Do not collapse multiple distinct hyperframes into a
  generic text slide unless the manifest marks them as duplicates.
- Use the captured frames as reference, but redraw the concept in an original
  style rather than copying copyrighted visuals exactly
- When building the branded PPTX for a conceptual/whiteboard-style video, keep
  the rendered Excalidraw recreation visible as the primary visual evidence on
  the relevant story slides. Do not overcorrect into a native-only consulting
  deck that hides the recreated drawings.
- Use branded PPTX elements around the drawing: action title, business
  implication panel, concise takeaway, and page number. The drawing should feel
  intentionally framed inside a professional client deck, not dumped as a full
  slide screenshot.
- Save each source as `<topic>-<frame-id>-concept.excalidraw`.
- Export each Excalidraw drawing to `<topic>-<frame-id>-concept.png` or `.svg`
  for PPTX insertion. The inserted deck visual may be a rendered Excalidraw
  preview, but the editable `.excalidraw` source must be delivered alongside it.

**Route B — Explainer Graphic infographic:**
Invoke the `/explainer-graphic` skill on the core concept.
- Find the killer analogy for the video's main topic
- Map all components to the analogy
- Generate a self-contained HTML infographic
- Save as `<topic>-explainer.html`

**Route C — Architecture Presentation / Draw.io:**
Use this route only when the video is technical architecture or solution
architecture.
- Produce a `.drawio` component-flow diagram based on the video's
  architecture/concept
- Produce the architecture explanation and deck package

**Pass forward:** selected visual artifact + visual brief

### Stage 4: Package
Package based on the selected visual route, but always finish with a branded
native `.pptx` unless the user explicitly asks for Markdown-only output.

Mandatory deck assembly:
- Invoke `branded-pptx-deck` / `pptxkit` as the final render stage.
- Treat Markdown files as source notes, storyboard, speaker notes, citations,
  and audit trail. Do not stop at Markdown when the request is "video to deck."
- Build from the Stage 2.5 storyboard and Stage 2.6 validation, not directly
  from raw frames. Every slide should have an action title and a role in the
  narrative.
- Build a branded deck with action titles, a clear storyline, an executive
  summary near the front, and a conclusion / next-action slide at the end.
  Do not target a generic slide-count range. Compute the count after mapping all
  transcript-supported beats and meaningful screen states. Add evidence slides
  whenever combining states would reduce legibility, traceability, or operating
  detail; one slide per distinct captured screen is acceptable.
- Package captured video diagrams as branded visual story slides:
  - Treat captured frames and hyperframes as reference inputs that must route to
    persistent assets.
  - Insert exact application/IDE/terminal/collaboration screenshots as primary
    evidence visuals after cropping and background matching. Do not redraw them.
  - For Route A, insert rendered Excalidraw drawings, not original frame
    screenshots. Keep the `.excalidraw` source files as the editable diagram
    layer. Do not replace visible recreated drawings with native-only PPTX
    approximations unless the user explicitly asks for fully native editability.
  - If the user explicitly requires PowerPoint-native editability too, rebuild
    the diagrams with editable PowerPoint shapes, text boxes, connectors,
    tables, and charts through `pptxkit` / `python-pptx`.
  - Account for all meaningful hyperframes from the manifest. The deck can
    combine related hyperframes into one synthesized editable slide, but it
    must not silently miss a captured diagram.
  - If an SVG/HTML reconstruction was generated, preserve its source, render it
    to PNG, and embed that PNG as the slide visual.
  - Route A: include all `<topic>-<frame-id>-concept.excalidraw` files as
    editable source. Insert only their rendered PNG/SVG previews into the deck,
    never the original hyperframe screenshots.
  - Route B: include the infographic HTML as source and export a deck-ready PNG
    for placement inside the native slide shell.
  - Route C: include the `.drawio` source and export/screenshot the architecture
    diagram only as a fallback; prefer editable PPTX shapes.
- Client-facing slide hygiene:
  - Do not show internal workflow/tool terms on slides: `Excalidraw`, `YouTube`,
    `transcript`, `hyperframe`, `source`, `audit`, `validation`, `synthesis`,
    `internal`, `recreated`, `Codex`, `Claude`, file paths, or skill names.
    Those belong in run reports and source packages, not client-facing slide
    text.
  - Do not label panels with process terms like `Synthesis`. Use client-facing
    labels such as `Business implication`, `Decision`, `Operating model`, or
    `Next move`.
  - Do not show timestamps on slides. Timestamps belong in validation and audit
    artifacts only.
  - Do not show source-file footers such as `.excalidraw` filenames on slides.
    Keep those references in the run report or artifact index.
  - Speaker notes may contain internal traceability only when the user wants
    source/audit context preserved in the deck file; otherwise keep notes clean
    too.
- Run branded PPTX validation and preview QA. Use `*-draft.pptx` until all
  delivery gates pass; use `*-reviewed.pptx` only after slide-by-slide
  validation and real render QA pass.
- Run `pptx-design-quality` against the draft and store
  `<run>/qa/pptx-design-lint.json`; fix or explicitly waive every finding before
  reviewed promotion.
- For decks with embedded visuals, run a real render QA pass, not only the
  lightweight `preview_pptx.py` placeholder render. Prefer
  `python3 scripts/officecli_qa.py <deck.pptx> --out <run>/qa/officecli`; if
  skipped, use LibreOffice/PDF or another renderer to confirm the actual drawing
  images appear, are legible, and are not cropped.
- Extract visible PPTX text and scan for forbidden internal terms before
  delivery. If any are found, rebuild before opening the deck.
- Preserve named proof examples from the source. Do not collapse specific
  companies/products into generic categories unless the run report states why.
- If editable diagram recreation is unavailable, mark the deck `blocked`; do
  not silently substitute screenshots as the main deliverable.

Route-specific source package:
- If Route A was selected, preserve the Excalidraw source and generated preview.
- If Route B was selected, preserve the HTML infographic and generated preview.
- If Route C was selected, preserve the `.drawio` diagram and architecture
  explanation, then render the branded PPTX deck.

**Output files:**
```
<topic>-research.md
<topic>-storyboard.md               # source/audit, not final delivery
<topic>-analyst-story-pack.md/json  # ai-analyst synthesis/story spine
<topic>-grill-me-validation.md      # challenge/self-answer validation against transcript
<topic>-transcript-excerpts.md      # timestamped evidence used by validation
transcript.txt                      # complete timestamped Stage 1 transcript
frames_manifest.md                 # machine-readable persistent frame inventory
<topic>-findings.json               # optional analyst/strategy synthesis payload
<topic>-hyperframes.md              # every frame classified and accounted for
<topic>-screen-change-coverage.md   # every meaningful visual mapped or skipped with reason
presentation-evidence.json          # normalized source slides, transcript, and frames
slide-plan.json                     # per-slide semantic intent and evidence map
<topic>-visual-spec.json            # source of truth for visual reconstruction
<topic>-reconstruction.svg          # optional QA intermediate, not final deck asset
<topic>-reconstruction.html         # optional QA intermediate, not final deck asset
<topic>-concept.excalidraw          # Route A
<topic>-concept.png or .svg         # Route A preview/export, when available
<topic>-<frame-id>-concept.excalidraw
<topic>-<frame-id>-concept.png or .svg
<topic>-editable-diagram.pptx       # optional standalone editable diagram deck
<topic>-explainer.html              # Route B
<topic>-architecture.drawio         # Route C
<topic>-architecture.md             # Route C
<topic>-video-deck-draft.pptx       # mandatory branded PPTX output
<topic>-video-deck-reviewed.pptx    # only after all delivery gates pass
<topic>-slide-validation.md         # slide-by-slide content/design validation
deck-brief.md                       # audience, decision, narrative and anti-references
deck-design.json                    # deterministic deck-design and lint contract
qa/pptx-design-lint.json            # native PPTX design-quality findings
qa/officecli/qa-summary.md          # OfficeCLI QA status when available
qa/officecli/render/                # OfficeCLI final-PPTX screenshots when available
```

## Completion

After all stages complete:
1. List all output files with paths
2. Open the branded `.pptx` if auto_open is enabled
3. Provide NotebookLM manual steps if enabled
4. Report total pipeline status

## Error handling

- If `/watch` fails (download error, no transcript): stop and report. Don't proceed with empty content.
- If any stage produces weak output: flag it, continue, and note the quality gap in the final report.
- If the video is >15 minutes: warn the user and suggest focusing on a specific section with `--start`/`--end`.

---

## Skill Relationships

### Category
Business Automation

### Dependencies
- `watch` — required (Stage 1); downloads video and extracts transcript
- `presentation-source-bundle` — required after Stage 1; normalizes source evidence
- `content-research` — required (Stage 2); enriches with Exa + firecrawl
- `ai-analyst` — required for Stage 2.5 synthesis when installed/exposed; produces story spine, BLUF, evidence map, and validation-ready claims
- `excalidraw` — default visual route for conceptual/non-architecture diagrams
- `explainer-graphic` — optional visual route for HTML infographics
- `architecture-presentation` — required only for technical/solution architecture packages; produces drawio + md + pptx
- `branded-pptx-deck` — required final render stage for native branded PPTX output
- `officecli-qa` — optional preferred final-PPTX render gate; uses repo root
  `scripts/officecli_qa.py` when `officecli` is installed
- `pptx-visual-spec` — mandatory visual-routing overlay and shared schema
- `pptx-design-quality` — mandatory deck-context, critique, and native-PPTX lint overlay

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `presentation-source-bundle` | Sequential upstream | after watch capture | `<run>/presentation-evidence.json` |
| `pptx-design-quality` | Behavioral overlay | every video-derived deck | `<run>/deck-brief.md`, `<run>/deck-design.json`, `<run>/qa/pptx-design-lint.json` |
| `watch` | Sequential upstream | always — watch provides transcript and frames | structured summary + transcript |
| `content-research` | Sequential upstream | always — enriches transcript with Exa research | `<topic>-research.md` |
| `ai-analyst` | Sequential upstream | required when exposed before visualization/PPTX rendering | `<topic>-analyst-story-pack.md/json`, BLUF, evidence map, slide spine |
| `pptx-visual-spec` | Behavioral overlay | every visualization and PPTX build | `<topic>-visual-spec.json` |
| `excalidraw` | Sequential downstream | **opt-in only** — hand-drawn whiteboard aesthetic for genuinely conceptual content; NEVER for product/UI/demo screens (those are Route 0 extract) | `<topic>-concept.excalidraw` + preview |
| `explainer-graphic` | Alternative / Peer | when a polished infographic or analogy is better than an editable diagram | `<topic>-explainer.html` |
| `architecture-presentation` | Alternative / Peer | when the video is technical architecture or solution architecture | `<topic>-architecture.drawio`, `.md`, `.pptx` |
| `marp` | Alternative / Peer | marp for markdown-first decks; video-to-deck chains architecture-presentation for .pptx | `<topic>-architecture.pptx` |
| `branded-pptx-deck` | Required downstream | always for video-to-deck unless user asks for Markdown-only | `<topic>-storyboard.md` + visual previews + captured frames |
| `second-brain` | Sequential downstream | if project has second-brain/, research notes land there automatically | `second-brain/wiki/<topic>.md` |

### Runtime Preamble

At invocation, say:
- "Running /video-to-deck — 4-stage pipeline: watch → research → visual route selection → branded PPTX deck/package."
- "Capture is `watch --detail scene-complete` (every distinct screen, deduped) — the manifest source of truth; a capped efficient sample is discovery only."
- "Visuals route per asset: exact evidence → extract; structured/textual → native or HTML/SVG; text-free organic illustration → built-in image generation. Each screen becomes a recreated PNG asset on a native editable slide — never a raw talking-head screenshot, never redraw-and-discard."
- If video is >15 minutes: "This video is long — consider passing a `--start`/`--end` range to focus the deck."
- Config file at `~/.claude/skills/video-to-deck/config.json` — if missing, onboarding questions will run first.

---

## Gotchas

- **Never build the storyboard from a capped sample.** Capture with `watch --detail scene-complete` (dense sample + webcam-masked dHash dedup, uncapped) — the manifest source of truth. A 50-keyframe `efficient` pass silently drops docs pages, whiteboard panels, and demo screens and guts the storyline; it is discovery only. Record the distinct-screen count in the run report (Gate 3).
- **Never compress to a predetermined slide count.** First map every meaningful
  screen and transcript beat; then let the content determine the deck length.
  Treat requested/generated counts as minimums or estimates unless the user
  explicitly sets a hard maximum.
- **Recreate screens; never scrape-and-paste, never redraw-and-discard.** Each hyperframe is a *reference image*: extract exact UI/app frames as cropped PNGs, author diagrams/whiteboards/screens as HTML/SVG → PNG (keep the source), then place the PNG as the primary visual on an otherwise-native slide (live title/callouts/captions). Do not paste raw talking-head-laden frames, and do not redraw a screen as native shapes only to throw the recreated image away (that is what guts the visuals). Excalidraw/native-redraw is opt-in for conceptual content only.
- **Never proceed past Stage 1 with empty transcript.** If `/watch` fails, stop and report. An empty transcript produces a fabricated deck.
- **Always use Exa for Stage 2 research, not basic WebSearch.** Exa + Firecrawl produce richer grounding than generic search.
- **Always wire `ai-analyst` upstream when exposed.** The analyst story pack is
  what turns transcript notes and frames into a client-ready storyboard. Use a
  clearly labeled `ai-analyst`-style fallback only when the callable skill/tool
  is genuinely unavailable.
- **Route per visual; there is no universal Excalidraw default.** Use
  Excalidraw only for an intentionally hand-drawn conceptual style. Use
  HTML/CSS for structured boxes and text, SVG for geometry, and
  Draw.io/architecture-presentation for explicit technical architecture.
- **Visible drawings and branded deck quality are both required.** For Route A,
  do not choose between "professional deck" and "visible recreated drawings."
  The correct output is a branded PPTX slide system that frames the recreated
  drawings with action titles, concise business implication text, and takeaway
  bands.
- **Client slides must not expose the production process.** Keep tool names,
  timestamps, source filenames, `transcript`, hyperframe/audit language,
  synthesis labels, and validation notes out of visible slide text.
- **Validate against the transcript before delivery.** Run `grill-me` or the
  fallback self-question validation. Unsupported consultant interpretations must
  be softened, removed, or marked as interpretation in source notes. If the
  unsupported language appears inside a visual, regenerate the visual.
- **Always include executive summary and conclusion slides** for client-facing
  decks unless the user explicitly asks for a tiny excerpt deck.
- **Markdown is intermediate, not final.** Use `.md` files for research notes,
  storyboard, speaker notes, citations, and QA. The user-facing deck output is
  the branded `.pptx`.
- **Capture diagrams into the deck.** Every selected visual route must produce a
  slide-embeddable persistent asset. Use exact captured video frames for real
  UI/application/IDE/terminal/collaboration evidence; use authored previews for
  diagrams that require reconstruction. Do not substitute generated imagery for
  missing evidence.
- **Rendered Excalidraw must be readable.** If Excalidraw previews are inserted
  into PPTX, label text must be readable in the exported PDF/contact sheet. If
  labels are not readable, enlarge the drawing, split the slide, or rebuild the
  labels/diagram as native PPT text and shapes.
- **Reviewed is a real QA status, not a filename preference.** Never create or
  deliver `*-reviewed.pptx` until XML validation, OfficeCLI QA when available,
  real render QA, internal-term scan, visual coverage, editability declaration,
  and slide-by-slide grill validation all pass.
- **Treat rights and provenance explicitly.** Exact UI/application frames may
  be placed as attributed evidence from the reviewed video; do not present them
  as original artwork. Do not extract third-party artwork, logos, people, or
  certifications to imply ownership or endorsement. For an authored conceptual
  diagram, preserve the idea and evidence while creating an original visual
  treatment unless the user owns or is licensed to reproduce the source.
- **Config is persistent across runs.** User answers (theme, NotebookLM, output dir) are saved to config.json and reused silently. Reconfigure with `/video-to-deck config`.
- **Stage 4 must produce a branded .pptx.** Use `branded-pptx-deck` after Stage
  3 for all routes. `architecture-presentation` may provide source architecture
  content, but the final deck should still pass the branded PPTX QA gate.

## Example usage

```
/video-to-deck https://youtube.com/watch?v=abc123
/video-to-deck https://youtube.com/watch?v=abc123 focus on the architecture section
/video-to-deck ./recording.mp4
/video-to-deck config
```
