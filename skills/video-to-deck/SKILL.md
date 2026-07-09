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
user_invocable: true
---

# Video-to-Deck Skill System

Orchestrator that chains four child skills in sequence to turn any video into a
complete presentation package. The user provides a video URL (or local path) and
optionally a focus question. You deliver a full branded PPTX deck package — no
manual steps between stages. Markdown files are source/audit artifacts, not the
final deliverable.

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

Retain the existing workflow, but choose the visual target based on the video's
content:

- Use `svg` as the preferred reconstruction intermediate when the frame contains
  precise boxes, arrows, labels, tables, scorecards, architecture-like diagrams,
  or any layout where coordinates and alignment matter. SVG is for QA and
  reconstruction, not the final deck asset.
- Use `html/css` as the preferred reconstruction intermediate when the frame is
  slide-like, text-heavy, web-like, dashboard-like, or needs typography/layout
  fidelity. HTML is for QA and reconstruction, not the final deck asset.
- Use `excalidraw` when the video contains conceptual models, frameworks,
  whiteboard-style explanations, business workflows, mental models, process
  maps, teaching diagrams, or visuals that should be recreated in an editable
  hand-drawn style.
- Use `architecture-presentation` / `.drawio` when the video is primarily a
  technical architecture, solution architecture, system design, integration map,
  cloud topology, data flow, deployment model, or component-level engineering
  diagram.
- Use `explainer-graphic` when the deck needs a polished infographic or analogy
  visual rather than an editable diagram.

Default reconstruction path:
`hyperframe -> visual-spec.json -> svg/html/excalidraw reconstruction -> QA preview -> editable branded PPTX shapes`.

Default to `svg` or `html/css` for precise slide recreation. Use Excalidraw
only when a hand-drawn editable source is actually the desired style.

## Non-Negotiable Delivery Gates

Do not call a video deck `reviewed` unless every gate below has passed and the
run contains the evidence artifacts.

1. **Story gate:** `ai-analyst` produced the upstream story spine when exposed.
   If it is unavailable, the run status must say `fallback`; do not silently
   treat fallback synthesis as equivalent.
2. **Evidence gate:** `grill-me` or the manual fallback challenged every
   slide-level claim against the transcript/research and recorded rebuild
   decisions.
3. **Visual coverage gate:** every meaningful screen-change / hyperframe maps
   to a slide, recreated visual, grouped duplicate, or explicit skip reason.
   Presenter-only frames may be excluded, but they must be accounted for.
4. **Client-language gate:** extracted visible slide text has no internal terms:
   `transcript`, `hyperframe`, `Excalidraw`, `YouTube`, `source`,
   `validation`, `synthesis`, `audit`, `Codex`, `Claude`, file paths, or
   timestamps.
5. **Render gate:** PPTX XML validation passes and a real render pass confirms
   embedded diagrams appear, are readable, and are not cropped. Prefer the shared
   OfficeCLI QA gate:
   `python3 scripts/officecli_qa.py <deck.pptx> --out <run>/qa/officecli`.
   If OfficeCLI is skipped or fails, use PowerPoint, LibreOffice PDF, Google
   Slides import, or equivalent. The lightweight preview alone is insufficient
   for decks with embedded visuals.
6. **Editability gate:** declare one editability mode in the run report and
   final response: `PPT-native editable diagrams`, `Excalidraw-source editable
   diagrams`, or `non-editable visual render`. If the user asks for editable
   slides and does not accept source-layer editability, rebuild diagrams as
   native PPT shapes.
7. **Proof gate:** named examples in the source, such as companies/products,
   must survive synthesis as named proof cards unless excluded for a stated
   reason.

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
- For the first full-video visual pass, invoke watch with `--detail efficient`
  unless the user explicitly requests a higher-fidelity scan. Efficient mode is
  the default hyperframe extraction pass for video-to-deck because it uses the
  updated watch keyframe path, caps the run at 50 frames, drops near-duplicates,
  and gives enough coverage to build the initial hyperframe manifest.
- For long videos or visually dense sections, use the efficient pass to find
  candidate sections, then re-run watch on those exact ranges with
  `--start`/`--end`, `--timestamps`, or a higher detail mode only where needed.
  Do not jump directly to `token-burner` for the whole video unless the user
  explicitly accepts the cost.

**Pass forward:** structured summary + transcript + topic name

Also create a hyperframe manifest before visualization:
- List every extracted frame/hyperframe with timestamp, path, classification,
  and disposition.
- Classify as `diagram`, `text-slide`, `demo-screen`, `talking-head`, or
  `duplicate/low-value`.
- Recreate every `diagram`, `text-slide`, and meaningful `demo-screen` in the
  deck unless it is explicitly marked duplicate.
- Exclude YouTuber/talking-head frames by default. Do not use presenter face
  screenshots in the branded deck unless the user explicitly asks for source
  evidence or a thumbnail-style appendix.
- If any meaningful hyperframe is skipped, state why in the manifest and final
  report.

Then create a `visual-spec.json` before rendering:
- One record per meaningful hyperframe or grouped duplicate set.
- Capture title, layout type, text blocks, cards, table rows, connectors,
  visual hierarchy, colors, and source frame paths.
- Route each record to `svg`, `html/css`, `excalidraw`, or `pptx-native`.
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

**Pass forward:** storyboard, slide spine, evidence map, visual-spec inputs

### Stage 2.6: Grill-Me Validation → Self-Correction
Before the final PPTX build, run a skeptical validation pass against the
transcript and any research artifacts. This is mandatory for client-facing video
decks.

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

**Route 0 — SVG/HTML reconstruction QA (preferred for slide recreation):**
Use this before final PPTX rendering when the frame is a diagram, table,
scorecard, slide, or layout-heavy visual.
- Generate SVG for diagrams, tables, boxes, arrows, and scorecards.
- Generate HTML/CSS for text-heavy slide-like layouts or dashboard/web screens.
- Render or screenshot the SVG/HTML only for QA comparison.
- Do not insert the SVG/HTML screenshot as the final deck visual unless the user
  explicitly accepts non-editable output.
- Rebuild the same visual with native PowerPoint shapes in Stage 4.

**Route A — Excalidraw conceptual recreation (default):**
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
  Typical length is 10-15 slides for a long-form video; use fewer only when the
  content is genuinely simple.
- Package captured video diagrams as branded visual story slides:
  - Use captured frames and hyperframes only as reference inputs.
  - Do not insert screenshots as the primary slide visual. Screenshots are
    acceptable only in a clearly labeled appendix/evidence slide when the user
    asks for source evidence.
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
  - If an SVG/HTML reconstruction was generated, use its structure and
    coordinates to drive native PPTX layout; do not embed it as a flat image.
  - Route A: include all `<topic>-<frame-id>-concept.excalidraw` files as
    editable source. Insert only their rendered PNG/SVG previews into the deck,
    never the original hyperframe screenshots.
  - Route B: include the infographic HTML as source and export/screenshot a
    deck-ready PNG only when an editable recreation is not feasible; otherwise
    recreate the visual natively in PPTX.
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
<topic>-findings.json               # optional analyst/strategy synthesis payload
<topic>-hyperframes.md              # every frame classified and accounted for
<topic>-screen-change-coverage.md   # every meaningful visual mapped or skipped with reason
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
- `content-research` — required (Stage 2); enriches with Exa + firecrawl
- `ai-analyst` — required for Stage 2.5 synthesis when installed/exposed; produces story spine, BLUF, evidence map, and validation-ready claims
- `excalidraw` — default visual route for conceptual/non-architecture diagrams
- `explainer-graphic` — optional visual route for HTML infographics
- `architecture-presentation` — required only for technical/solution architecture packages; produces drawio + md + pptx
- `branded-pptx-deck` — required final render stage for native branded PPTX output
- `officecli-qa` — optional preferred final-PPTX render gate; uses repo root
  `scripts/officecli_qa.py` when `officecli` is installed

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `watch` | Sequential upstream | always — watch provides transcript and frames | structured summary + transcript |
| `content-research` | Sequential upstream | always — enriches transcript with Exa research | `<topic>-research.md` |
| `ai-analyst` | Sequential upstream | required when exposed before visualization/PPTX rendering | `<topic>-analyst-story-pack.md/json`, BLUF, evidence map, slide spine |
| `excalidraw` | Sequential downstream | default for conceptual models, frameworks, workflows, and non-technical visuals | `<topic>-concept.excalidraw` + preview |
| `explainer-graphic` | Alternative / Peer | when a polished infographic or analogy is better than an editable diagram | `<topic>-explainer.html` |
| `architecture-presentation` | Alternative / Peer | when the video is technical architecture or solution architecture | `<topic>-architecture.drawio`, `.md`, `.pptx` |
| `marp` | Alternative / Peer | marp for markdown-first decks; video-to-deck chains architecture-presentation for .pptx | `<topic>-architecture.pptx` |
| `branded-pptx-deck` | Required downstream | always for video-to-deck unless user asks for Markdown-only | `<topic>-storyboard.md` + visual previews + captured frames |
| `second-brain` | Sequential downstream | if project has second-brain/, research notes land there automatically | `second-brain/wiki/<topic>.md` |

### Runtime Preamble

At invocation, say:
- "Running /video-to-deck — 4-stage pipeline: watch → research → visual route selection → branded PPTX deck/package."
- "Default visual route is Excalidraw unless this is a technical or solution architecture video."
- If video is >15 minutes: "This video is long — consider passing a `--start`/`--end` range to focus the deck."
- Config file at `~/.claude/skills/video-to-deck/config.json` — if missing, onboarding questions will run first.

---

## Gotchas

- **Never proceed past Stage 1 with empty transcript.** If `/watch` fails, stop and report. An empty transcript produces a fabricated deck.
- **Always use Exa for Stage 2 research, not basic WebSearch.** Exa + Firecrawl produce richer grounding than generic search.
- **Always wire `ai-analyst` upstream when exposed.** The analyst story pack is
  what turns transcript notes and frames into a client-ready storyboard. Use a
  clearly labeled `ai-analyst`-style fallback only when the callable skill/tool
  is genuinely unavailable.
- **Default to Excalidraw for conceptual visuals.** Use Draw.io/architecture-presentation only when the content is explicitly technical architecture or solution architecture.
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
  slide-embeddable recreated diagram preview. Do not use captured video frames
  as the main visual fallback unless the user explicitly asks for source
  evidence.
- **Rendered Excalidraw must be readable.** If Excalidraw previews are inserted
  into PPTX, label text must be readable in the exported PDF/contact sheet. If
  labels are not readable, enlarge the drawing, split the slide, or rebuild the
  labels/diagram as native PPT text and shapes.
- **Reviewed is a real QA status, not a filename preference.** Never create or
  deliver `*-reviewed.pptx` until XML validation, OfficeCLI QA when available,
  real render QA, internal-term scan, visual coverage, editability declaration,
  and slide-by-slide grill validation all pass.
- **Do not copy copyrighted frames exactly.** Use `/watch` frames as reference and redraw the idea in an original editable style unless the user owns the source material or has rights.
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
