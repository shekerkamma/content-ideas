---
name: pptx-toolkit
description: Inspect and perform explicitly constrained surgical operations on existing PowerPoint (.pptx) files while preserving their package structure and current layout. Use for slide inventories, shape and text discovery, a named whole-shape text correction, a specified native speaker-note update, explicit slide reordering or removal, OOXML unpack/repack, and structural validation. Do not use for broad requests to update, modify, contextualize, customize, adapt, refresh, improve, enhance, rebrand, upgrade, or fix a deck; route those requests to vault-presales-pptx-pipeline for a full native rebuild.
---

# PPTX Toolkit

Use this skill as the **existing-file surgery layer**. It complements the deck-building
skills; it does not replace them.

## Route the request

- Existing `.pptx`, inspect or perform explicitly named surgical operations while preserving
  its current layout: use this skill.
- Broad requests to update, modify, contextualize, customize, adapt, refresh, improve,
  enhance, rebrand, upgrade, or fix a deck: use `vault-presales-pptx-pipeline`; rebuild it.
- New client-facing deck or material redesign: use `vault-presales-pptx-pipeline`, unless the
  user explicitly requires the separate branded-template workflow.
- Visual assets are added or materially changed: apply `pptx-visual-spec` before editing.
- Any deliverable: finish with `officecli-qa`; do not call it reviewed without real render QA.

## Safe workflow

1. Keep the source file unchanged. Write edits to a new `*-draft.pptx` path.
2. Inspect the source and save the JSON inventory.
3. Address shapes by `shape_id` whenever possible; names can repeat.
4. Apply replacements, notes, or slide ordering with the bundled CLI.
5. Validate the output structurally.
6. Run the existing preview and OfficeCLI gates. Promote to `*-reviewed.pptx` only after
   those gates pass.

```bash
TOOL=skills/pptx-toolkit/scripts/pptx_toolkit.py

python3 "$TOOL" inspect source.pptx --out inventory.json
python3 "$TOOL" edit source.pptx edited-draft.pptx --spec edits.json
python3 "$TOOL" reorder source.pptx reordered-draft.pptx --order 3,1,2
python3 "$TOOL" validate edited-draft.pptx
```

Read [references/operations.md](references/operations.md) before writing an edit spec,
reordering with omissions, or unpacking OOXML.

## Handoffs to existing skills

- `vault-presales-pptx-pipeline`: rebuild when the request is broad or affects narrative,
  branding, charts, layout, visuals, contextualization, or client-ready quality.
- `branded-pptx-deck`: use instead only when the user explicitly requires that separate
  branded-template workflow.
- `pptx-visual-spec`: classify any new or replaced visual region and preserve provenance.
- `officecli-qa`: validate, inspect issues, render, and screenshot the final PowerPoint.
- `presentation-speaker-notes`: use for HTML-deck notes; this toolkit manages native PPTX
  notes.

## Guardrails

- Never overwrite the source by default. `--force` only permits replacing the output path;
  input and output still cannot be the same file.
- Never interpret a broad deck-change request as permission for in-place surgery. If the user
  did not name the exact surgical operation and ask to preserve the layout, hand off to
  `vault-presales-pptx-pipeline` for a full rebuild.
- Slide numbers in CLI arguments and JSON specs are one-based.
- Reordering accepts each source slide at most once. Omitting a slide deletes it from the
  output; duplication is deliberately unsupported.
- Whole-shape text replacement preserves the first existing run's formatting and clears
  other runs. It does not preserve mixed formatting within the replaced shape.
- Inspect comments but do not edit them. Do not claim support for animations, SmartArt,
  embedded objects, macros, or chart-data mutation.
- After raw OOXML edits, always repack, validate, and real-render the result.
