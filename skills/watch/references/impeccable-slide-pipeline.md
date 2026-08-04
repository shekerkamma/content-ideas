# Impeccable visual-asset branch for Watch

## Purpose

Test and apply whether a committed design template or visual world improves the presentation of
assets recovered from a watched video. The output should feel like the video's presentation was
professionally recreated—not like a report written about the video.

## Inputs from Watch

Use the existing watch work directory. Do not redownload or resample when the needed frames and
transcript are already present.

Create `transcript-map.json` first. Segment the complete transcript into sections and record each
section's thesis, supporting claims, demonstration, caveat, implication, and timestamp window.
Turn those sections into a narrative spine and slide claims before choosing frames.

Then create `visual-context-map.json` with one record per meaningful screen: frame path and
timestamp, surrounding transcript window, visible labels and proof, visual role, recoverable
assets, disposition, and reconstruction route. Talking-head-only frames are context, not assets.

## Impeccable handoff

Use the repo-local Impeccable skill at `.agents/skills/impeccable/`.

1. Run its context loader once from the project root.
2. Read `reference/new-work.md` and `reference/craft-floor.md`.
3. Use **Read** mode for explanatory decks and **Persuade** only for an explicitly requested pitch.
4. Treat the deck as a whole surface. If no established presentation world exists, run the
   mandatory direction assignment and world tournament from `new-work.md`.
5. Keep content, sequence, labels, numbers, named examples, and recovered assets fixed across
   directions. Only the presentation system may change.

External galleries may inform typography, composition, material, pacing, and asset framing. They
are not template or artwork sources.

## Transcript-led template/world experiment

The deck must communicate the video's argument without requiring playback. Native slide content
is the default: diagrams, process maps, comparisons, matrices, timelines, and concise explanatory
copy. A source frame is used only when the exact interface state is evidence. Do not turn each
transcript section into a screenshot-plus-caption page.

Create representative slides in two treatments before building the complete deck.

### Baseline

Source-faithful reconstruction using the incumbent branded slide system without Impeccable art
direction.

### Impeccable treatment

Use the same visual/context pairs and recovered assets in the selected world. Change only asset
scale, crop, focal point, framing, typography, hierarchy, spacing, rhythm, compatible color,
annotations, connectors, and meaning-preserving sequence.

Never improve an asset by replacing it with generic generated imagery. Image generation is allowed
only for a new text-free supporting texture or metaphor—never evidence, UI, diagrams, logos,
people, results, or certifications.

## Asset benchmark

Write `visual-asset-benchmark.json`. Score baseline and each treatment from 1–5 on:

- `asset_prominence`
- `crop_and_focus`
- `context_binding`
- `hierarchy`
- `legibility`
- `visual_distinctiveness`
- `source_fidelity`
- `cross_slide_coherence`
- `editability`
- `asset_authenticity`

Every score includes a reason and affected slide IDs. Record the winner and why. Impeccable wins
only when it improves the total without lowering `source_fidelity`, `legibility`, or
`asset_authenticity` below baseline.

Run the bundled deterministic scorer after the human/visual review records its scores:

```bash
python3 scripts/benchmark_visual_assets.py benchmark-input.json \
  --out visual-asset-benchmark.json
```

The scorer rejects incomplete records, enforces the fidelity/legibility/authenticity guardrails,
and chooses only among eligible treatments. It does not invent scores; those come from inspecting
the rendered representative slides.

## Slide construction

### Content expansion gate

After `story-architect` approves the slide spine, run `presentation-content-writer` before
finalizing `slide-plan.json`. It consumes the story pack and writes `slide-content.md` with a
key message, substantial slide copy, concrete support, native speaker notes, and a transition for
every slide. This stage may deepen articulation but may not add claims outside Watch evidence.

### Signature explainer gate

Use `explainer-graphic` to brief one or two concepts whose mechanism is difficult to understand
with ordinary slide primitives. Route those briefs through `ai-graphics` Track A so all text and
geometry are deterministic HTML/SVG; keep the editable source beside each PNG. Never use this
gate to redraw exact interface evidence or produce decorative model imagery.

### Native notes gate

After the branded deck is constructed, use `pptx-toolkit` for one constrained operation: embed
the approved `slide-content.md` speaker notes into native PowerPoint notes without changing slide
geometry. Validate and real-render the notes-enabled output before reviewed promotion.

For every slide, make the transcript-derived claim dominant. Use native structure to explain the
claim. When a chosen source state materially proves it, make that recovered or faithfully
recreated visual readable and prominent; retain named examples, values, diagrams, and product
states; split states when combining them would shrink assets; preserve editable source for authored
SVG/HTML/native reconstructions.

A screenshot sequence fails this branch even when polished. So does a small screenshot beside a
large generic text panel. The target is a coherent standalone presentation with selective proof.

## Required outputs

- `visual-context-map.json`
- `transcript-map.json`
- `narrative-spine.md`
- `slide-content.md`
- `asset-inventory.json`
- `baseline-treatment/`
- `impeccable-treatment/`
- `impeccable-direction.md`
- `visual-asset-benchmark.json`
- `slide-plan.json`
- `visual-spec.json`
- reproducible deck builder
- editable HTML/SVG sources and PNG renders for any authored signature graphics
- native speaker-note edit specification and notes-enabled PPTX
- draft or reviewed PPTX
- render and lint QA artifacts

## Promotion gate

Read `skills/present/references/visible-skill-application-contract.md`, write
`skill-application-manifest.json`, and run its validator. Content-writer output must affect visible
slides; Impeccable must materially change the visual world; graphics must form a reusable system;
native notes count only as notes; and OfficeCLI proves technical cleanliness rather than design
quality. Invocation alone never earns stage credit.

Call the deck `reviewed` only when every meaningful screen has a disposition; the benchmark is
complete; chosen assets are readable in a real Office-compatible render; contracts and lint pass;
no asset misrepresents the source; and visible client text contains no production terms or
timestamps. Otherwise retain `draft` or report `blocked`.
