---
name: presentation-source-bundle
description: Normalize cached slides, slide renders, extracted slide text, transcripts, and video-frame manifests into a validated presentation-evidence.json handoff for PPTX planning and semantic QA. Use when rebuilding an existing presentation, creating a deck from a video, or comparing source slides with a new PowerPoint.
metadata:
  category: Business Automation
---

# Presentation Source Bundle

Create the evidence layer that sits upstream of `slide-plan.json` and
`visual-spec.json`. This skill does not design slides or render PowerPoint. It records what
the supplied presentation sources contain so downstream builders can distinguish source
evidence from interpretation.

## Input layout

Point the builder at a run directory containing any of these cached artifacts:

```text
slides.pdf or slides.pptx
slide_images/slide_1.png
slide_ascii.md
outline.txt
transcript.txt
frames_manifest.md
```

The filenames match the Pamela Fox presentation-skill pipeline and are also usable by the
repo's `watch`, `video-to-deck`, PDF, and Office render workflows. Missing optional inputs
produce empty arrays or null fields; the builder never invents alignments.

When those cached artifacts do not yet exist, use the bundled intake adapters:

```bash
python3 scripts/fetch_slides.py <url> <run-dir>
python3 scripts/convert_slides_to_images.py <run-dir>/slides.pdf <run-dir>/slide_images
python3 scripts/extract_slide_text.py <run-dir>/slides.pdf <run-dir>/slide_ascii.md <run-dir>/slide_images
python3 scripts/thumbnail_of_pptx.py <onedrive-url> <run-dir>/thumbnail.png
python3 scripts/extract_transcript.py <youtube-url> <run-dir>/transcript.txt
```

The adapters are derived from Pamela Fox's MIT-licensed `presentation-skills` project; see
`references/upstream-presentation-skills.md`. They acquire and normalize evidence only.
They do not select a design, create a template, or render the final client deck.

## Outline slides (agent procedure)

`outline.txt` has no upstream script — the source project's `outline-slides` skill is a
vision-LLM procedure, not a deterministic parser, and every script in this skill stays a
pure parser/wrapper. Produce it directly:

1. For each `slide_images/slide_N.png`, read the matching `## Slide N` section of
   `slide_ascii.md` (if present) as ground truth for that slide's visible text.
2. Look at the image and write one plain-English sentence summarizing the slide, using the
   extracted text as the primary source and the image for visual context (diagrams,
   screenshots, embedded demos).
3. Write the summaries to `<run-dir>/outline.txt`, one per line, in the exact format
   `build_presentation_evidence.py`'s `OUTLINE_LINE` pattern expects:

```text
1. Title slide introducing the presentation on <topic>
2. Agenda slide listing the main sections to be covered
3. Diagram showing the architecture of <system>
```

For presentations over 50 slides, work through them in batches of 50. A malformed line
(missing the `N. ` prefix) is silently dropped by the builder — proofread the file before
running `build_presentation_evidence.py`.

## Build

```bash
python3 skills/presentation-source-bundle/scripts/build_presentation_evidence.py \
  --run <run-dir> \
  --title "<presentation title>"
```

The default output is `<run-dir>/presentation-evidence.json`. Repeat `--source` for an
original URL or a non-standard source filename. YouTube and Vimeo URLs are recognized as
video automatically; use repeatable `--video-source` for extensionless video URLs on other
hosts so captured frames retain the correct source provenance. If a bundle contains more
than one video, pass `--frame-source` and `--transcript-source` with the exact source values
that produced `frames_manifest.md` and `transcript.txt`; ambiguous provenance is rejected.
For a single video, both relationships are assigned automatically. Set `--rights` to the
supplied asset's known reuse status; the default explicitly requires verification before
client delivery.

The builder:

- hashes local source files and rendered slide images;
- parses deterministic `slide_ascii.md` sections as slide-text ground truth;
- reads numbered slide summaries from `outline.txt`;
- records timestamped transcript segments;
- imports timestamped frame descriptions and duplicate relationships from
  `frames_manifest.md`;
- leaves slide-to-transcript and slide-to-frame alignment empty until an analyst or
  alignment pass can support it.

## Plan and visual handoff

Greenfield deck with no source evidence: copy and tailor the shared slide-plan template:

```bash
cp skills/pptx-visual-spec/assets/slide-plan.template.json \
  <run-dir>/slide-plan.json
```

Reference-deck rebuild: draft `slide-plan.json` from `presentation-evidence.json` instead
of starting from the blank template:

```bash
python3 skills/pptx-visual-spec/scripts/draft_slide_plan.py \
  <run-dir>/presentation-evidence.json
cp <run-dir>/slide-plan.draft.json <run-dir>/slide-plan.json
```

The draft carries one `evidence_ids` link per slide and a `TODO:` placeholder
`action_title` for any slide `outline.txt` didn't summarize; it never writes `claims[]`
content — narrative and factual judgment stay with a human or agent. Tailor the draft
before continuing.

Create `visual-spec.json` through `pptx-visual-spec`, then validate the full chain:

```bash
python3 skills/pptx-visual-spec/scripts/validate_presentation_contracts.py \
  <run-dir>/presentation-evidence.json \
  <run-dir>/slide-plan.json \
  <run-dir>/visual-spec.json \
  --check-files
```

## Contract boundaries

- `presentation-evidence.json` records what the source contains.
- `slide-plan.json` records claims, audience purpose, speaker notes, accessibility, and
  the intended role of each slide.
- `visual-spec.json` records how each meaningful visual region is produced and QA'd.
- `deck-design.json` remains the deck-wide typography, color, layout, and lint contract.

Do not place slide design decisions in the evidence bundle. Do not place raw source facts
in the design contract.

## Relationships

| Skill | Pattern | Handoff |
|---|---|---|
| `watch` | Upstream source capture | transcript and frame manifest |
| `video-to-deck` | Downstream orchestrator | `presentation-evidence.json` |
| `pptx-visual-spec` | Mandatory contract owner | schemas and cross-contract validator |
| `pptx-design-quality` | Parallel design overlay | `deck-brief.md`, `deck-design.json` |
| `branded-pptx-deck` | Downstream native builder | evidence + slide plan + visual spec |

## Gotchas

- Deterministic extracted slide text is ground truth for visible source copy; image
  descriptions supply visual context, not replacement text.
- A checksum proves file identity, not factual correctness or reproduction rights.
- Never infer slide-to-transcript alignment from order alone.
- Frame manifest paths are relative to the run directory, even when the manifest itself is
  stored in a nested metadata directory. Timestamp cells may use `00:05` or `[00:05]`.
- An `extract` visual must reference source evidence through `evidence_ids`.
- Keep evidence paths relative to the run directory so bundles remain portable.
