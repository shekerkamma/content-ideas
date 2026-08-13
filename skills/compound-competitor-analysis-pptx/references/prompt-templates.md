# Prompt templates

## Content-envelope prompt

```text
You are writing one slide in a decision-grade Accenture-style strategy deck.

Audience: {audience}
Decision: {deck_decision}
Section role: {section_role}
Source evidence: {evidence_records}
Prior slide: {prior_slide_title}
Next slide: {next_slide_title}

Produce JSON only with:
- assertion_title: one complete answer-led sentence, max 18 words;
- analytical_question: one executive decision question;
- executive_answer: bounded answer, max 40 words;
- evidence_blocks: 2–4 blocks, each with label, scoped claim, evidence_ids, evidence_status;
- comparison_logic: explicit compare/segment/decompose/qualify operation;
- counterargument: strongest credible alternative explanation;
- implication: business consequence;
- decision: one action or choice;
- owner: accountable role;
- trigger: observable escalation/stop event and timing;
- exhibit: analytical archetype and required elements;
- source_note: evidence IDs, attribution, caveats.

Rules:
1. Do not introduce facts absent from evidence.
2. Attribute company claims explicitly.
3. Do not hide caveats in notes.
4. Do not repeat the title as body copy.
5. The slide must perform analysis, not catalogue facts.
```

## Design-envelope prompt

```text
Design one editable 16:9 Accenture-style strategy slide.

Content contract: {slide_content_contract}
Template profile: {template_profile}
Sequence context: {prior_and_next_slides}

The slide must visually prove: {executive_answer}

Return JSON only with:
- family/archetype;
- visual_thesis;
- design_prompt;
- layout_contract: grid, focal point, reading flow, title/exhibit/decision/footer zones,
  whitespace, alignment, hierarchy;
- graphic_contract: marks, encodings, axes or stages, comparison logic, evidence-status encoding,
  counterargument treatment, source treatment;
- typography_contract: title, verdict, body, annotation and source sizes;
- content_limits: visible blocks, max words, max lines per region;
- evidence_regions with visual roles;
- visual_routes with native/extract/place-asset/author/image-model/none routing;
- prohibited patterns;
- five QA questions.

Rules:
1. Use one dominant exhibit; do not arrange prose into cards.
2. Geometry must encode comparison, causality, sequence, qualification, or magnitude.
3. Keep evidence status separate from threat/magnitude encoding.
4. Preserve at least 20% negative space.
5. Keep complete evidence in notes/appendix; show only decision-changing content.
6. No nested cards, decorative pills, pseudo-charts, or text below the contract minimum.
```

## Slide critique prompt

```text
Review the rendered slide against its content and design contracts.

Score 0–2 on:
1. five-second answer clarity;
2. visible analytical operation;
3. evidence boundary clarity;
4. geometry-to-meaning fit;
5. hierarchy and whitespace;
6. typography and legibility;
7. decision/owner/trigger specificity;
8. counterargument visibility;
9. consistency with sequence and template;
10. absence of generic AI-slide patterns.

For every score below 2, prescribe one concrete layout or copy change. Reject the slide if the
exhibit is merely prose in containers, if a conclusion outruns evidence, or if any required claim is
available only in speaker notes.
```

## Full-deck council prompt

```text
Audit the deck as an executive argument. Read titles first, then exhibits, then notes.
Identify: broken narrative transitions, duplicated claims, missing counterarguments, unsupported
rankings, inconsistent competitor scope, non-parallel dossier pages, repeated renderer patterns,
decision gaps, and appendix material left in the core story. Return slide-specific rewrites and an
ordered promotion/blocker list. Do not reward invocation logs; judge visible output only.
```
