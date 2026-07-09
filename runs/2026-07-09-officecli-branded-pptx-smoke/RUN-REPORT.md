# Branded PPTX OfficeCLI Smoke Run

Status: reviewed

Decks:

- Draft: `officecli-branded-pptx-smoke-draft.pptx`
- Reviewed: `officecli-branded-pptx-smoke-reviewed.pptx`

Editability:

- PPT-native editable diagrams and text.
- No primary slide visual is a flat screenshot.

QA Evidence:

- `Deck.save()` passed built-in `validate_pptx()` with 3 slides.
- Lightweight preview/contact sheet:
  `docs/reports/_preview/contact_1.png`
- OfficeCLI QA summary:
  `qa/officecli/qa-summary.md`
- OfficeCLI final screenshot render:
  `qa/officecli/render/officecli-branded-pptx-smoke-draft.png`
- OfficeCLI HTML render:
  `qa/officecli/officecli-branded-pptx-smoke-draft.html`

OfficeCLI result:

```text
Status: passed
validate: 0
issues: 0
html: 0
screenshot: 0
```

Notes:

- The managed sandbox can block Chromium screenshot rendering. The final QA run
  used the codified escalated path with `--required`.
- The contact sheet was inspected after reducing slide 2 text density; no red
  overflow boxes remained.
