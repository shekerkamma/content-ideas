---
name: "Impeccable 4.0 Executive Decision System"
description: "A proof-led executive field manual for allocating judgment, governing iteration, and testing adoption."
colors:
  proof-paper: "#F2EDE3"
  charcoal: "#202220"
  vermilion: "#E33D2E"
  moss: "#315C4A"
  archive-tan: "#C8A46B"
  soft-rule: "#DED6C8"
  muted-copy: "#6E6A63"
  warm-white: "#F8F3EA"
  pale-paper: "#EAE4DA"
  evidence-gray: "#A7A199"
typography:
  display:
    fontFamily: "Aptos Display, Aptos, sans-serif"
    fontSize: "44pt"
    fontWeight: 700
    lineHeight: 1.02
  headline:
    fontFamily: "Aptos Display, Aptos, sans-serif"
    fontSize: "28pt"
    fontWeight: 700
  title:
    fontFamily: "Aptos, sans-serif"
    fontSize: "18pt"
    fontWeight: 700
  body:
    fontFamily: "Aptos, sans-serif"
    fontSize: "12pt"
    fontWeight: 400
    lineHeight: 1.18
  label:
    fontFamily: "Aptos, sans-serif"
    fontSize: "10pt"
    fontWeight: 700
rounded:
  square: "0"
  tag: "0.15in"
  circle: "50%"
spacing:
  slide-gutter: "0.72in"
  evidence-inset: "0.3in"
  hairline: "1pt"
  rule: "2pt"
components:
  paper-slide:
    backgroundColor: "{colors.proof-paper}"
    textColor: "{colors.charcoal}"
    rounded: "{rounded.square}"
  charcoal-slide:
    backgroundColor: "{colors.charcoal}"
    textColor: "{colors.warm-white}"
    rounded: "{rounded.square}"
  proof-panel:
    backgroundColor: "{colors.charcoal}"
    textColor: "{colors.warm-white}"
    rounded: "{rounded.square}"
    padding: "0.3in"
  decision-marker:
    backgroundColor: "{colors.vermilion}"
    textColor: "{colors.warm-white}"
    rounded: "{rounded.circle}"
    size: "0.55in"
---

# Design System: Impeccable 4.0 Executive Decision System

## Overview

**Creative North Star: "The Conservation Proof Table"**

The deck translates a source-conservation test into an executive decision system. It feels like a proof paper crossed with an operating brief: warm stock, charcoal fields, compact evidence labels, hard-edged matrices, and explicit gates. The visual language distinguishes what was observed, what the presenter asserted, and what the analyst recommends without changing or decorating the underlying evidence.

Fifteen analytical slides are fully native and editable. Three exact-state proof slides retain authentic product frames and pair them with native interpretation. The system is designed for reading and adjudication: every slide should help an executive locate the decision, owner, control, risk, or measurement implication.

**Key Characteristics:**

- Proof Paper and Charcoal alternate as the primary reading surfaces.
- Vermilion identifies decisions, risk, escalation, and active intervention.
- Moss identifies governed support, confidence, and constructive control.
- Archive Tan identifies context, continuity, fixed conditions, and secondary structure.
- Evidence provenance is visible at the slide edge and never merged into analyst claims.
- Visual assets remain conserved; design improves framing, priority, annotation, and sequence.

## Colors

The palette behaves like editorial ink on an archival proof sheet, with three semantic accents rather than decorative brand color.

### Primary

- **Vermilion** (`#E33D2E`): Decision gates, risk states, escalation, active workflow labels, critical arrows, and recommendation emphasis.

### Secondary

- **Moss** (`#315C4A`): High-confidence routes, system support, constructive controls, and governed or stable states.

### Tertiary

- **Archive Tan** (`#C8A46B`): Fixed conditions, context labels, intermediate states, decision-brief metadata, and continuity across steps.

### Neutral

- **Proof Paper** (`#F2EDE3`): Default analytical slide surface and background around authentic source frames.
- **Charcoal** (`#202220`): Thesis and decision slides, strong endpoint blocks, and proof annotation panels.
- **Warm White** (`#F8F3EA`): Primary text on Charcoal and strong accent fields.
- **Soft Rule** (`#DED6C8`): Dividers, matrix structure, and quiet sequencing.
- **Muted Copy** (`#6E6A63`): Supporting explanation and metadata on Proof Paper.
- **Evidence Gray** (`#A7A199`): Low-emphasis labels and provenance on Charcoal.

### Named Rules

**The Semantic Ink Rule.** Vermilion means decide or intervene; Moss means support or proceed; Archive Tan means context or continuity. Do not swap these roles for variety.

**The Conservation Rule.** Exact-state evidence keeps its source colors. Deck colors frame and annotate it; they do not recolor it.

## Typography

**Display Font:** Aptos Display, with Aptos and sans-serif fallback  
**Body Font:** Aptos, with sans-serif fallback

**Character:** A single corporate sans-serif is made editorial through decisive scale, bold weights, uppercase evidence labels, and disciplined spacing. Type is direct and analytical, with complete-thought headlines rather than topic-only titles.

### Hierarchy

- **Display** (700, 34–44pt, 1.02 line-height): Opening thesis and final recommendation.
- **Headline** (700, 27–28pt): Slide propositions, management implications, and pilot outcomes.
- **Title** (700, 17–22pt): Claims, matrix choices, stage names, and proof annotations.
- **Body** (400, 12–20pt, approximately 1.18–1.38 line-height): Explanations, implications, and decision rationale.
- **Label** (700, 8–12pt, usually uppercase): Evidence classes, owners, exit criteria, state labels, rubrics, and folios. Eight-point type is reserved for provenance and navigation.

### Named Rules

**The Executive Sentence Rule.** A headline states the implication or decision, not merely the subject.

**The Evidence Label Rule.** Provenance and epistemic status use compact uppercase labels and remain visually subordinate to the claim.

## Layout

The deck uses a governed 16:9 canvas with roughly 0.72–0.85-inch outer gutters. A consistent title band occupies the upper 1.2 inches; evidence status and folio sit along the bottom edge. The central field uses matrices, paired columns, horizontal decision sequences, operating-model grids, and risk-to-control tables.

Most analytical slides contain one dominant reasoning structure rather than collections of interchangeable cards. Rectangular blocks represent states or decisions; arrows show movement; thin rules establish scales and separations. Negative space isolates the management implication.

The three proof slides share one exact-state component with purposeful orientation changes:

- Source frame left with Charcoal interpretation panel right.
- Charcoal interpretation panel left with source frame right.
- A repeated proof pattern is permitted only because each slide proves a different interface state; orientation follows reading order and the important region of the image.

## Elevation & Depth

The system is flat. There are no shadows, gradients, glows, bevels, glass effects, or floating-device treatments. Depth comes from full-field tonal inversion, adjacent evidence and interpretation planes, and 1–2pt rules. Source screenshots retain their native UI depth but receive no added chrome.

### Named Rules

**The Flat Proof Rule.** Exact-state frames sit flush beside analysis. Never convert them into decorative cards or device mockups.

## Shapes

The form language is rectilinear and table-like: square fields, horizontal rules, axis lines, grids, and direct side-by-side comparisons. Compact labels may use a slight 0.15-inch rounding. Fully rounded geometry is reserved for numbered decision markers and question gates, typically 0.55–0.68 inches. The opening thesis uses a narrow 0.16-inch Vermilion spine as a report-binding motif.

## Components

### Analytical Slide

- **Paper variant:** Proof Paper field, Charcoal headline, Muted Copy support, and semantic accent blocks.
- **Charcoal variant:** Charcoal field, Warm White headline, warm-gray supporting text, and restrained Vermilion or Archive Tan emphasis.
- **Footer:** Evidence status at lower left and `current / total` folio at lower right, both at 8pt.

### Exact-State Proof

- **Image:** Authentic extracted frame, centered and contained without synthetic replacement.
- **Panel:** Charcoal rectangle, square corners, 0.3-inch inset, and a 2pt Vermilion rule.
- **Claim:** Warm White, bold, 19pt; states what the frame demonstrates.
- **Implication:** Warm gray, 12pt; explains the executive consequence.
- **Provenance:** “Observed demonstration” in the footer.

### Decision Matrix

- **Cells:** Solid Vermilion, Moss, Archive Tan, or Charcoal rectangles with centered high-contrast text.
- **Axes:** Compact uppercase labels; Vermilion denotes low confidence or escalation and Moss denotes high confidence or controlled progress.
- **Use:** Route change altitude, confidence, ownership, or go/no-go conditions—not general feature comparison.

### Gates and Markers

- **Decision marker:** Vermilion circle with centered Warm White numeral.
- **Question gate:** Archive Tan circle with Charcoal question mark.
- **Exit condition:** Short explicit instruction adjacent to the owning role or gate.

### Evidence Tags

- **Shape:** Short, slightly rounded strip approximately 0.36 inches high.
- **Type:** 9pt bold, centered.
- **Role:** Label epistemic class or workflow state; never substitute for a full explanation.

### Risk-to-Control Row

- **Structure:** Vermilion gate label, bold Charcoal risk, Archive Tan arrow, and bold Moss control.
- **Closing bar:** Charcoal band with a white accountability principle.

## Do's and Don'ts

- **Do** conserve the exact copy, claim, frame, and sequence when comparing treatments.
- **Do** expose whether a statement is observed evidence, presenter assertion, or analyst assessment.
- **Do** use one dominant decision structure per slide.
- **Do** keep the management implication visually stronger than its supporting detail.
- **Do** use Vermilion, Moss, and Archive Tan according to their fixed semantic roles.
- **Don't** recolor, redraw, crop away, or replace authentic product evidence.
- **Don't** introduce decorative gradients, shadows, glass, rounded card grids, or ornamental icons.
- **Don't** imply measured performance where the slide presents a conceptual relationship or pilot hypothesis.
- **Don't** allow provenance text to carry the argument; it identifies the evidence class only.
- **Don't** scale the workflow visually or rhetorically past the bounded-pilot recommendation encoded in the deck.
