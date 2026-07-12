# Fable 5 Comprehensive Deck Run Report

Status: reviewed

Final deck: `runs/2026-07-03-video-to-deck-watch-efficient-test/fable-5-comprehensive-deck-reviewed.pptx`

## Pipeline Summary

- Watch extraction: completed with updated watch efficient mode.
- Story spine: completed with an ai-analyst-style storyboard pack.
- Visual coverage: completed with meaningful screen changes grouped and mapped to slide treatments.
- Validation: completed with slide-by-slide skeptical challenge against captions and visual coverage.
- PPTX build: completed with `pptxkit`.
- Editability mode: PPT-native editable diagrams.

## QA Evidence

- XML validation: passed during `Deck.save()`.
- Visible text scan: passed in the builder.
- Lightweight preview: passed after layout corrections.
- Real render: passed via LibreOffice PDF export.
- Render contact sheets:
  - `runs/2026-07-03-video-to-deck-watch-efficient-test/render-qa/real-render-contact-01.png`
  - `runs/2026-07-03-video-to-deck-watch-efficient-test/render-qa/real-render-contact-02.png`

## Visual Handling

- No raw video screenshots are used as primary slide visuals.
- Presenter-only frames were excluded.
- Demo, terminal, article, and diagnostic screens were recreated as native workflow diagrams, tables, and decision panels.
- The deck uses editable PowerPoint shapes rather than embedded screen captures.

## Deliverables

- Story pack: `fable-5-story-pack.md`
- Visual coverage map: `fable-5-visual-coverage.md`
- Validation notes: `fable-5-grill-me-validation.md`
- Builder script: `build_fable5_comprehensive_deck.py`
- Reviewed deck: `fable-5-comprehensive-deck-reviewed.pptx`

