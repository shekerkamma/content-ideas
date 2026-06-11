# Reference — "SOP: Board-Ready Strategic Plan Deck via GenSpark.ai" (Jo Lambadjieva, captured 2026-06-09)

Source PDF: `SOP_ Building a Board-Ready Strategic Plan Deck via GenSpark.ai.pdf`
(owner's Desktop; the embedded master prompt is truncated in the capture —
output-spec sections 1.1–1.5 recovered, citation rules partially cut).

Contextual input to CIOS-SPEC v1.0 Part 8 (Output Engine). **We do not adopt
GenSpark** — deck generation stays on the branded-pptx-deck workflow per
CIOS-OUT-002. What we adopt is the *contract shape*: a parameterized intake
schema plus hard slide-layout rules, which make board-deck output repeatable
and reviewable.

## Extracted contract → CIOS-OUT-005

**Intake placeholders** (their `{{...}}` set, generalized):
company name, industry, HQ, primary market, mission, product lines,
revenue/EBITDA, 3 named competitors, time horizon (years), optional ESG
priorities + constraints, brand color/logo, report currency.

**Output spec** (their §1.1–1.5):
- Editable deck, 20–30 slides max excluding appendix
- ≤5 bullets per slide, ≤12 words per bullet
- Speaker notes 100–150 words per slide
- High-resolution visuals (vector or 16:9 PNG)
- Brand accent color + logo on title slide
- Citations required (their rule partially truncated; CIOS applies its own
  stricter CIOS-GOV-002 citation rule instead)

## Fit notes

- The intake schema slots in as the `board-deck` deliverable's required
  inputs — collected from pack + GBrain + engagement context first, asked of
  the user only for the gaps (layered load order, CIOS-CTX-001).
- Slide-density rules *augment* the repo slide contract (action title +
  structured support + evidence/implication); they do not replace it.
- Their single-prompt approach trades control for speed; CIOS keeps the
  multi-stage pipeline (context → narrative → branded build → QA gate) but
  the placeholder discipline removes the "what do I need to know before
  building a board deck" ambiguity.
