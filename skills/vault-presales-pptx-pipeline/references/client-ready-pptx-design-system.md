---
title: Client-Ready PPTX Design System
date: 2026-07-16
tags:
  - presentation-design
  - pptx
  - pre-sales
  - design-system
status: active
aliases:
  - Default PPTX Design System
  - Custom PPTX Design Specification
---

# Client-Ready PPTX Design System

> [!important] Default
> Apply this design system whenever a request says “custom PPTX,” “client-ready deck,” “custom slide layout,” or “presentation design specification,” unless the current request supplies an approved client template or explicit visual direction.

This is a company-neutral design language derived from a 33-slide reference deck. Reuse its structural principles, not its identity or content.

## Precedence

1. Approved client template and brand kit.
2. Explicit instructions in the current request.
3. This design system.
4. Content-specific deviations required for readability or accessibility.

## Company-Neutral Rule

- Do not reuse the source company name, logo, product names, people, contact details, registration details, confidentiality labels, or proprietary imagery.
- Do not invent a replacement company identity or logo.
- Use neutral metadata such as `Client / Initiative / Date` when no client identity is provided.
- Adapt composition, typography, color roles, spacing, and information hierarchy. Do not reproduce branded pages as images.
- Replace source-specific claims and metrics with verified content from the current deck packet.

## Canvas and Grid

| Token | Specification |
|---|---|
| Aspect ratio | 16:9 widescreen |
| PowerPoint size | 13.333 × 7.5 in |
| Outer margins | 0.40 in left/right; 0.28–0.35 in top/bottom |
| Grid | 12 columns; 0.18 in gutters |
| Title zone | y = 0.30–1.25 in |
| Main content zone | y = 1.35–6.95 in |
| Footer zone | y = 7.08–7.30 in |
| Alignment | Hard alignment to shared vertical and horizontal guides |

Use white analytical slides for most of the narrative. Reserve dark navy slides for the cover, chapter transitions, technical deep dives, the ask, and the close. A typical deck should be roughly 70% light and 30% dark.

## Typography

| Role | Preferred | Safe fallback | Size |
|---|---|---|---|
| Cover headline | DM Serif Display Regular | Georgia Bold or Cambria Bold | 40–54 pt |
| Slide title | DM Serif Display Regular | Georgia Bold or Cambria Bold | 24–30 pt |
| Emphasized title phrase | DM Serif Display Italic | Georgia Italic or Cambria Italic | Match title |
| Body | Questrial Regular | Aptos or Arial | 12–14 pt |
| Card heading | Century Gothic Bold | Aptos Display SemiBold or Arial Bold | 12–16 pt |
| Section kicker | Century Gothic Bold, uppercase | Aptos Display SemiBold | 8–10 pt |
| Table and chart labels | Questrial Regular | Aptos or Arial | 9–11 pt |
| Footer and sources | Questrial Regular | Aptos or Arial | 7–8 pt |
| KPI number | DM Serif Display Regular or body bold | Georgia Bold or Aptos Display Bold | 28–40 pt |

Rules:

- Use a serif display face only for titles, large metrics, and short emphasis.
- Use a clean sans serif for all explanatory text, tables, diagrams, and annotations.
- Use uppercase, tracked labels sparingly for section numbers and categories.
- Keep titles to two lines. Highlight no more than one phrase in cyan italic.
- If preferred fonts are unavailable, apply the specified fallback intentionally and verify the rendered deck. Do not rely on silent font substitution.

## Color System

| Token | Hex | Use |
|---|---|---|
| Midnight | `#0A1628` | Dark slide background, title blocks, technical panels |
| Slate | `#1E293B` | Primary text on light slides |
| White | `#FFFFFF` | Light background and reversed text |
| Cyan | `#00B4D8` | Primary accent, rules, selected metric, italic title phrase |
| Teal | `#0A9396` | Process nodes, secondary accent, positive comparison |
| Pale blue | `#8DB4D4` | Secondary series and diagram support |
| Success green | `#12855B` | Verified status, completed milestone, positive KPI |
| Muted gray | `#6B7280` | Supporting text, captions, secondary labels |
| Surface | `#F8FAFC` | Card and table fill |
| Cool surface | `#F4F8FE` | Alternate band or evidence panel |
| Line | `#E2E8F0` | Dividers, card outlines, table rules |

Color discipline:

- Use one dominant accent per slide: cyan or teal.
- Use green only for verified positive states.
- Keep large data tables neutral; highlight one row, column, or metric.
- Avoid gradients, shadows, glow, glass effects, and decorative color noise.
- Maintain at least 4.5:1 contrast for body text.

## Composition Rules

- Give every slide one claim and one primary proof object.
- Use a small uppercase kicker above the title: `SECTION · TOPIC` or `01 · TOPIC`.
- Place a thin cyan rule below or beside the title area when structure needs reinforcement.
- Use 2–5 columns. Avoid more than six major objects on one slide.
- Use square or nearly square cards with thin outlines and minimal corner radius.
- Prefer structured whitespace over decoration.
- Use arrows only to show sequence, causality, or flow.
- Keep recurring footer information small and quiet.

## Reusable Components

### Section header

- Kicker: 8–10 pt uppercase cyan.
- Title: 24–30 pt serif, dark navy.
- Optional emphasis: one short italic cyan phrase.
- Optional divider: 1–2 pt navy or cyan rule.

### KPI tile

- One number, one short label, one evidence note.
- Number: 28–40 pt.
- Label: 10–12 pt uppercase or semi-bold.
- Note: 8–10 pt muted gray.
- Use 3–5 tiles in a row; do not mix unrelated metrics.

### Evidence card

- 12–16 pt heading.
- 25–45 words maximum.
- One small proof marker: source, date, status, or quantified result.
- Use thin `#E2E8F0` borders and white or `#F8FAFC` fill.

### Comparison table

- Put the decision criteria in the first column.
- Use a neutral header and one cyan/teal highlighted option.
- Prefer words, checks, and short values over paragraphs.
- Use direct annotations to explain why a difference matters.

### Architecture diagram

- Flow left to right.
- Use dark navy for system boundaries, cyan for the primary path, teal for services or decisions, and gray for external dependencies.
- Keep connector crossings to zero where possible.
- Label interfaces and data movement directly.
- Add a short outcome statement above or below the diagram.

### Chart

- Use flat 2D charts with direct labels.
- Use gray for context, blue families for comparison, and cyan or teal for the focus series.
- Remove legends when direct labels are possible.
- Include units, timeframe, source, and whether values are actual, target, or forecast.

## Layout Library

| ID | Layout | Build formula |
|---|---|---|
| L01 | Cover | Full-bleed evidence image or midnight field; small metadata; 40–54 pt headline; thin cyan accent |
| L02 | Executive thesis | 55/45 split; dark headline panel left; 2×2 KPI grid right |
| L03 | Positioning | Title + one-sentence thesis + 3–4 evidence cards + narrow proof strip |
| L04 | Process chain | 4–6 nodes left to right; one outcome endpoint; concise annotation below |
| L05 | Reasons or pillars | 4–5 equal columns; numbered labels; one evidence image strip or proof row |
| L06 | Opportunity or KPI landscape | 3–5 metric tiles on top; evidence cards or assumptions below |
| L07 | Solution architecture | Hero visual or diagram at left; three capability columns or layers at right/bottom |
| L08 | Technical deep dive | Midnight background; centered system diagram; cyan dimensions and annotations |
| L09 | Product or service matrix | 4–6 columns; common-platform bar; one highlighted recommended option |
| L10 | Competitive comparison | Criteria table or quadrant; grouped competitors; one clear win and one honest limitation |
| L11 | Roadmap and validation | Horizontal phases; status strip; evidence and risk blocks below |
| L12 | Financial or performance evidence | Table plus 2–4 callout metrics, or three small charts with aligned scales |
| L13 | Cost or concept clarity | Three large-number cards linked by arrows; bottom-line implication below |
| L14 | Ask or next step | Midnight 40% panel with the ask; 60% light panel with use of resources, owners, and milestones |
| L15 | Team or governance | 2–4 leader cards above; capability or advisor grid below; role evidence over biography |
| L16 | Closing proof montage | Midnight field; one-line close; 4–8 evidence thumbnails with short captions |

## Imagery

- Prefer real product, workflow, facility, architecture, or prototype evidence over generic stock imagery.
- Use a dark overlay only on cover or chapter imagery to protect title contrast.
- Crop images tightly around the proof object.
- Use a thin white, navy, or cyan frame; avoid soft shadows.
- Add 7–9 pt captions when the image is evidence.
- Do not reuse photographs or illustrations from the source deck unless the user owns and explicitly provides usage rights.

## Visual Tool Routing

- Route by artifact requirement rather than defaulting to one design platform.
- Prefer authentic evidence and approved connected assets before public search or generation.
- Use native Presentations objects for slide structure, diagrams, charts, tables, and annotations.
- Use purpose-built tools for their strongest context: Framer for web, Figma for high-craft design, Paper or MagicPath for agent-native product design, Stitch for design systems, UX Pilot for rapid journeys, and Canva or Genspark for presentation exploration.
- Use image generation for clearly illustrative raster assets, not for business proof, technical diagrams, quantitative evidence, logos, or real people and facilities.
- Treat external design output as an intermediate source and rebuild the final client-ready PPTX as editable slide objects unless the asset is authentic visual evidence.
- The full requirement and availability matrix lives in `.agents/skills/vault-presales-pptx-pipeline/references/visual-tool-routing.md`.

## Content Density

| Element | Target |
|---|---|
| Title | 6–12 words; two lines maximum |
| Subtitle or thesis | One sentence |
| Standard body copy | 45–90 words per slide |
| Dense analytical slide | Up to 120 words outside tables |
| Card body | 12–30 words |
| Major objects | 3–6 |
| Columns | 2–5 |

Use dense slides only for comparisons, architecture, roadmaps, evidence, or financial detail. Follow a dense slide with a synthesis or decision slide when the audience needs a clear takeaway.

## Editable PPTX Rules

- Build titles, body text, cards, tables, diagrams, and charts as editable PowerPoint objects.
- Use screenshots only for real evidence such as application UI, documents, or photographs.
- Do not flatten full slides into images for the client-ready output.
- Apply color and typography through reusable theme tokens.
- Put citations or source URLs in speaker notes or a 7–8 pt source footer.
- Keep source labels visually subordinate to the claim.
- Follow the vault’s pre-sales PPTX skill for final deck creation; do not use direct OOXML editing for final decks.

## Quality Gate

- [ ] No source company name, logo, people, products, contact details, legal identifiers, or proprietary imagery remains.
- [ ] The current client’s approved identity is used when supplied; otherwise the deck stays neutral.
- [ ] Every slide has one clear claim and one primary proof object.
- [ ] Titles, body, charts, and diagrams use the correct type hierarchy.
- [ ] Accent color is controlled and contrast is accessible.
- [ ] Text, charts, diagrams, and tables are editable.
- [ ] No text overflow, clipped labels, misaligned cards, or accidental font substitution.
- [ ] Forecasts, targets, and actuals are clearly distinguished.
- [ ] Sources are present for externally derived claims.
- [ ] The deck renders cleanly and opens in Microsoft PowerPoint.

## Validated Test

- [[Client-Ready PPTX Design System Test]]
- [[Client-Ready-PPTX-Design-System-Test.pptx]]
- [[2026-07-16 - Test client-ready PPTX design system]]

The initial validation passed on 2026-07-16: seven editable slides, seven distinct layout patterns, correct 16:9 geometry, zero source-company identifiers, clean rendered-slide QA, and successful Microsoft PowerPoint opening.
