# Slide Validation

Status: reviewed after PPTX XML validation, preview render, visible-text scan, and section-based visual coverage update.

## Validation Scope

- Story gate: completed with `claude-code-course-storyboard.md`.
- Evidence gate: completed with `claude-code-course-grill-me-validation.md`.
- Visual coverage gate: completed with section-based `/watch` scene extraction: Section 1 = 94 frames, Section 2 = 117 frames, Section 3 = 230 frames, Section 4 = 23 frames; plus interrupted full-video scene scan = 461 frames.
- Client-language gate: to be checked after PPTX build by extracting visible text.
- Render gate: to be checked after PPTX build.
- Editability gate: declared as `PPT-native editable diagrams`.
- Proof gate: specific demos are preserved as named proof cards: website, invoice automation, support inbox, lead enricher, pricing.


## Final Render QA

- PPTX output: `claude-code-course-video-deck-reviewed.pptx`
- Slide count: 46
- PPTX XML validation: clean
- Preview render: completed to `docs/reports/_preview/contact_1.png` through `contact_6.png`
- Visible internal-term scan: clean
- Editability mode: PPT-native editable diagrams
