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

Copy and tailor the shared slide-plan template:

```bash
cp skills/pptx-visual-spec/assets/slide-plan.template.json \
  <run-dir>/slide-plan.json
```

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
