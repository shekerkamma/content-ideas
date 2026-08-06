---
name: "Impeccable 4.0 — Decision Flight Recorder"
description: "A dark operational decision system built from signal tracks, numbered states, instrument evidence, and explicit commitment gates."
colors:
  operational-navy: "#0B1020"
  instrument-panel: "#151C32"
  analysis-white: "#F4F7FF"
  evidence-cyan: "#46E6FF"
  commitment-lime: "#D8FF3E"
  comparison-violet: "#9B7CFF"
  escalation-coral: "#FF5A5F"
  telemetry-muted: "#A8B0C7"
  signal-rule: "#313A58"
  light-field-ink: "#111629"
  light-panel: "#E8ECF6"
typography:
  display:
    fontFamily: "Aptos Display, Aptos, sans-serif"
    fontSize: "48pt"
    fontWeight: 700
    lineHeight: 0.95
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
    fontSize: "15pt"
    fontWeight: 400
    lineHeight: 1.25
  label:
    fontFamily: "Aptos, sans-serif"
    fontSize: "10pt"
    fontWeight: 700
rounded:
  square: "0"
  tag: "0.12in"
spacing:
  slide-gutter: "0.55in"
  panel-inset: "0.3in"
  hairline: "1pt"
  signal: "4pt"
components:
  operational-slide:
    backgroundColor: "{colors.operational-navy}"
    textColor: "{colors.analysis-white}"
    rounded: "{rounded.square}"
  analysis-slide:
    backgroundColor: "{colors.analysis-white}"
    textColor: "{colors.light-field-ink}"
    rounded: "{rounded.square}"
  instrument-panel:
    backgroundColor: "{colors.instrument-panel}"
    textColor: "{colors.analysis-white}"
    rounded: "{rounded.square}"
    padding: "0.3in"
  state-tag:
    backgroundColor: "{colors.evidence-cyan}"
    textColor: "{colors.light-field-ink}"
    rounded: "{rounded.tag}"
    height: "0.34in"
---

# Design System: Impeccable 4.0 — Decision Flight Recorder

## Overview

**Creative North Star: "The Decision Flight Recorder"**

The built world is an executive operating console, not a report skin. A near-black navy canvas carries numbered states, signal rails, explicit boundaries, and oversized verdicts. Intermittent white analysis surfaces act as inspection plates where comparisons, ladders, and responsibility models require higher scanning speed. Authentic interface frames are treated as instrument readouts: dominant, unchanged, and paired with a single management interpretation.

The visual system converts a product demonstration into a governed adoption decision. It separates observed mechanisms from analyst models and unproven outcomes, then routes attention toward authorization, ownership, escalation, and measurement. The deck is 14 slides, uses six reusable archetypes, and does not fall back to product-tour or screenshot-recap pacing.

**Key Characteristics:**

- Operational Navy is the default field; Analysis White is an intentional analytical interruption.
- Four signal colors retain fixed state meanings across text, rails, tags, cells, and markers.
- Oversized verdicts bookend the narrative; dense middle slides use compact console chrome.
- Signal tracks express sequence, memory, and controlled movement without decorative charts.
- Every exact-state image remains authentic and subordinate only to the slide's visible decision claim.
- All six archetypes are authored natively in PowerPoint; the builder is the editable source.

## Colors

The palette behaves like operational telemetry: one dark canvas, one bright inspection surface, and four signals whose meaning never changes for decoration.

### Primary

- **Commitment Lime** (`#D8FF3E`): Authorization, commitment, accepted progress, demonstrated boundary, and the primary decision bar.

### Secondary

- **Evidence Cyan** (`#46E6FF`): Observed evidence, fixed inputs, chosen direction, section identifiers, and factual controls.
- **Comparison Violet** (`#9B7CFF`): Alternatives, bounded comparison, operator choice, and future constraints.

### Tertiary

- **Escalation Coral** (`#FF5A5F`): Risk, exception, reference reset, override, human ownership, unproven outcomes, and stop conditions.

### Neutral

- **Operational Navy** (`#0B1020`): Default slide field and the darkest endpoint in analytical models.
- **Instrument Panel** (`#151C32`): Cards, readout panels, route cells, and experiment arms on Navy.
- **Analysis White** (`#F4F7FF`): High-contrast analytical slide field and primary type on Navy.
- **Light Field Ink** (`#111629`): Primary type and dark comparison fields on Analysis White.
- **Telemetry Muted** (`#A8B0C7`): Explanations, status, folios, axes, and secondary labels on Navy.
- **Signal Rule** (`#313A58`): Structural rules and quiet separators.
- **Light Panel** (`#E8ECF6`): Secondary comparison surface on white slides.

### Named Rules

**The Four-Signal Rule.** Cyan means evidence or fixed input; Lime means commitment or controlled progress; Violet means comparison or choice; Coral means risk, escalation, or unproven status. Never exchange meanings to balance a composition.

**The Signal-to-Noise Rule.** A signal color identifies a state, rail, or verdict. Large fields remain Navy, Panel, White, or Ink unless the whole field is itself the decision.

## Typography

**Display Font:** Aptos Display, with Aptos and sans-serif fallback  
**Body Font:** Aptos, with sans-serif fallback

**Character:** Typography is terse, instrument-like, and assertive. Uppercase labels mimic console readouts; complete-sentence headlines and large verdicts keep the executive argument legible without requiring the presenter to decode the interface.

### Hierarchy

- **Display** (700, 44–48pt, 0.95–0.98 line-height): Opening and closing verdicts; short, uppercase, and usually two lines.
- **Headline** (700, 24–28pt): Slide-level decision statements and major trade-off labels.
- **Title** (700, 17–22pt): State names, proof implications, and analytical conclusions.
- **Body** (400 or 700, 14–20pt, 1.1–1.4 line-height): Explanations inside panels, matrices, and comparison fields.
- **Label** (700, 8–12pt, usually uppercase): Section chrome, evidence status, axes, tags, field names, and folios. Eight-point type is restricted to provenance and navigation.

### Named Rules

**The Verdict Rule.** Display type makes an authorization or boundary explicit; it does not announce a topic.

**The Readout Rule.** Uppercase labels are short state identifiers. Longer reasoning stays in sentence case.

## Layout

The deck uses a 16:9 canvas and a loose 12-column grid. Operational slides use approximately 0.55–0.75-inch outer gutters. Standard chrome places a cyan section label at the upper left, a 28pt title below it, a 1pt Signal Rule across the page, evidence status at lower left, and a zero-padded folio at lower right.

Rhythm alternates dark operational fields with white inspection plates. Consecutive slides do not repeat the same archetype more than twice. Each slide has one dominant reasoning structure—readout, ledger, track, proof, matrix, or ladder—and one visible management conclusion. Panels align to shared top and bottom rails rather than floating independently.

Signal rails are built from 4pt colored segments separated by small gaps. They indicate movement or state coverage, not quantitative magnitude. Arrows are reserved for real sequence or escalation. Numbered states use zero-padded labels (`01`, `02`, `03`) to reinforce the recorder metaphor.

## Elevation & Depth

The world is flat and luminous rather than dimensional. It uses no shadows, gradients, glow, glass, bevels, or device mockups. Depth comes from Navy/Panel layering, dark/light field inversion, colored edge rails, and the contrast between authentic screen imagery and native interpretation. Panels sit on the same plane; their meaning comes from alignment and signal state.

### Named Rules

**The One-Plane Rule.** Keep panels flush and shadowless. Use color rails and tonal contrast to establish hierarchy.

## Shapes

Geometry is rectilinear: hard-edged panels, bars, matrix cells, staircase blocks, rules, and segmented tracks. Square corners are the default. Only compact status tags receive a slight 0.12-inch radius. A narrow 0.18-inch Lime spine appears on the opening verdict as a flight-recorder index mark. Signal rails use uniform thickness and deliberately uneven segment lengths; they should never be mistaken for progress bars or measured charts.

## Components

The six archetypes below are the complete reusable set. Extensions should compose from them before introducing another slide grammar.

### 1. Decision Readout

- **Purpose:** Open or close with an explicit authorization, boundary, or scale decision.
- **Structure:** Oversized verdict on Navy; Lime qualifier; optional Instrument Panel authorization block; narrow Lime spine or multicolor signal rail.
- **Use:** One decision, one constraint, one bounded next action.

### 2. Signal Ledger

- **Purpose:** Summarize observed mechanisms or decision inputs without feature-tour framing.
- **Structure:** Numbered rows, compact state label, complete-sentence finding, colored status tag, 1pt row rule, and a full-width decision bar.
- **Use:** Cyan, Violet, and Coral identify distinct evidence mechanisms; the resulting commitment bar is Lime.

### 3. State Track

- **Purpose:** Show governed sequence, accumulated cost, or memory across operational states.
- **Structure:** Three to four aligned nodes joined by arrows or a segmented signal rail. Each node has one state name, one operational action, and one semantic top or side edge.
- **Variants:** Horizontal mechanism track, rising cost staircase, and organizational-memory loop.
- **Constraint:** Rails show sequence, not measured performance.

### 4. Instrument Proof

- **Purpose:** Prove an exact interface state while exposing its management implication.
- **Structure:** Dominant authentic screen, adjacent Instrument Panel, one semantic tag, one 21–22pt finding, and one 15pt implication or control.
- **Orientations:** Image left/panel right for Worlds and reference reset; panel left/image right for Live Mode.
- **Evidence treatment:** Contain the source frame, preserve its pixels and original aspect ratio, and avoid decorative crop, recoloring, redraw, masking, or device chrome. The status line must read `OBSERVED DEMONSTRATION`.

### 5. Decision Matrix

- **Purpose:** Allocate ownership or route work across explicit operational states.
- **Structure:** Two-by-two route matrix or four-column responsibility board; Navy/Panel cells, colored side rails, compact axes, and clear human/system or low/high distinctions.
- **Use:** Coral for escalation and human accountability, Lime for controlled local work, Cyan for structural or fixed-input work, Violet for unresolved comparison.

### 6. Boundary Ladder

- **Purpose:** Separate demonstrated structure from unproven outcomes or compare operating conditions.
- **Structure:** Ordered colored levels or paired fields followed by a full-width boundary rail and a plain-language caveat.
- **Use:** Lime marks demonstrated or controlled territory; Coral marks unproven outcomes and stop conditions.
- **Constraint:** The ladder is categorical, not a maturity score derived from measurement.

### Native Construction

- All titles, labels, panels, rails, tables, matrices, arrows, and analytical graphics remain editable PowerPoint objects generated by `build_deck.py`.
- Exact source screens are the only raster evidence. Generated imagery is not part of the world.
- Speaker notes may supplement the talk track but may not carry a required claim, caveat, or evidence boundary; all fourteen key messages remain visible on-slide.
- New slides must use the governed branded template, 16:9 canvas, and existing native helpers before adding custom geometry.

## Do's and Don'ts

- **Do** begin every extension by selecting one of the six established archetypes.
- **Do** keep the slide's decision, evidence status, and boundary visible without speaker notes.
- **Do** use the four signal colors according to their semantic roles across every component.
- **Do** alternate Navy operational surfaces with White inspection surfaces when the analytical rhythm needs relief.
- **Do** keep exact-state frames dominant and unchanged, with native interpretation beside them.
- **Do** preserve editability for all non-evidence content and verify the real PowerPoint render at 1920 × 1080.
- **Do** introduce a new state by composing existing rails, panels, tags, and numbered readouts first.
- **Don't** redesign the world as a product tour, screenshot recap, conventional consulting card grid, or feature-count showcase.
- **Don't** invent ROI, productivity, usability, quality, or business-outcome proof; label these as pilot hypotheses.
- **Don't** use signal rails as unlabeled decoration or imply that segment length is a metric.
- **Don't** add gradients, shadows, glass effects, ornamental icons, rounded card stacks, or generated imagery.
- **Don't** let a new archetype appear for one slide only; extend the system only when an existing archetype cannot express a recurring decision structure.
- **Don't** lower body text below 11pt or captions below 8pt; keep primary claims at presentation scale and validate contrast in the final render.
