---
name: "Impeccable 4.0 — Taste as an Operating System"
description: "A warm-paper editorial field manual that turns transcript evidence into disciplined visual argument."
colors:
  paper: "#F2EDE3"
  ink: "#202220"
  signal-red: "#E33D2E"
  moss: "#315C4A"
  archive-tan: "#C8A46B"
  soft-rule: "#DED6C8"
  muted-copy: "#6E6A63"
  paper-on-ink: "#F6F0E7"
  white: "#FFFFFF"
typography:
  display:
    fontFamily: "Aptos Display, Aptos, sans-serif"
    fontSize: "48pt"
    fontWeight: 700
    lineHeight: 0.98
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
    fontSize: "12pt"
    fontWeight: 700
    letterSpacing: "normal"
rounded:
  square: "0"
  pill: "50%"
spacing:
  hairline: "1pt"
  rule: "2pt"
  slide-gutter: "0.7in"
  section-gap: "0.4in"
components:
  slide-paper:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.square}"
  slide-ink:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper-on-ink}"
    rounded: "{rounded.square}"
  proof-note:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper-on-ink}"
    rounded: "{rounded.square}"
    padding: "0.3in"
  numbered-marker:
    backgroundColor: "{colors.signal-red}"
    textColor: "{colors.white}"
    rounded: "{rounded.pill}"
    size: "0.48in"
---

# Design System: Impeccable 4.0 — Taste as an Operating System

## Overview

**Creative North Star: "The Editorial Field Manual"**

The built deck reads like a practical dossier: warm uncoated paper, near-black ink, hard-edged annotation bars, small folios, and a restrained archive palette. Its layouts favor argument, comparison, and procedural clarity over ornamental polish. Dark chapter-like slides punctuate the paper sequence and give the narrative a deliberate reading rhythm.

The visual system is native PowerPoint synthesis with source imagery reserved for proof. Three screenshot slides use three visibly different evidence treatments—image with a right-hand note, panoramic image with a bottom annotation band, and left-hand note with a mirrored image—so evidence feels authored without being redrawn or disguised.

**Key Characteristics:**

- Warm paper and dense ink alternate as the two principal reading surfaces.
- Signal red marks commitment, friction, iteration, and key conclusions.
- Moss carries constructive guidance; archive tan carries taxonomy, sequencing, and secondary structure.
- Slides are flat, rectilinear, and built from type, rules, bars, and a small number of circular markers.
- Evidence remains visibly photographic while interpretation stays editable and native.

## Colors

The palette combines publication neutrals with three controlled editorial inks; color is semantic and sparse rather than atmospheric.

### Primary

- **Signal Red** (`#E33D2E`): Used for the cover spine, active steps, directional arrows, critical labels, emphasis rules, micro-change bands, and concluding claims.

### Secondary

- **Moss** (`#315C4A`): Used for positive operating guidance, macro-change bands, accepted or stable states, and constructive conclusions.

### Tertiary

- **Archive Tan** (`#C8A46B`): Used for world taxonomies, process connectors, secondary stage rules, and the closing proposition on ink.

### Neutral

- **Warm Paper** (`#F2EDE3`): Default slide field and the background surrounding source evidence.
- **Editorial Ink** (`#202220`): Default text, dark-slide field, proof annotation panel, and terminal process bar.
- **Soft Rule** (`#DED6C8`): Structural dividers and quiet connectors on paper.
- **Muted Copy** (`#6E6A63`): Supporting descriptions, captions, and paper-slide folios.
- **Paper on Ink** (`#F6F0E7`): Primary display text on dark slides.
- **White** (`#FFFFFF`): Text inside strong red and moss markers or bands.

### Named Rules

**The Signal Rule.** Red identifies a decision, warning, or narrative turn; it is not a general-purpose fill.

**The Paper-and-Ink Rule.** Use warm paper for explanation and ink for thesis, tension, or conclusion. Do not introduce a third full-slide background.

## Typography

**Display Font:** Aptos Display, with Aptos and sans-serif fallback  
**Body Font:** Aptos, with sans-serif fallback

**Character:** The deck uses one restrained sans-serif family with weight, scale, case, and spacing doing the expressive work. Large bold statements behave like editorial headlines; small uppercase labels behave like marginalia and section markers.

### Hierarchy

- **Display** (700, 37–48pt, approximately 0.98 line-height): Cover and closing theses; usually one or two short lines.
- **Headline** (700, 28–34pt): Slide titles and major paired concepts such as “WORLDS” and “LIVE MODE.”
- **Title** (700, 17–22pt): Claims, proof annotations, stage names, and prominent conclusions.
- **Body** (400, 12–18pt, up to 1.38 line-height): Explanations and supporting argument. Source-proof detail is 12pt; major explanatory copy rises to 18pt.
- **Label** (700, 8–15pt, usually uppercase): Eyebrows, taxonomy labels, metadata, stage labels, and folios. Eight- to nine-point type is confined to provenance and navigation metadata.

### Named Rules

**The Weight-First Rule.** Establish hierarchy with bold weight and size before adding color. Red labels are compact; red paragraphs are not part of the system.

**The Read-Mode Rule.** Headlines state a complete thought. Supporting copy explains it; it does not repeat it as a second slogan.

## Layout

The deck is 16:9 and follows a loose 12-column structure with a consistent outer gutter of roughly 0.7–0.85 inches. Titles occupy a shallow band at the top; folios sit at the lower right. Most slides use one dominant composition: a bilateral comparison, a horizontal process, a two-row operating grid, or a source image paired with a dark annotation field.

Vertical rules split conceptual comparisons. Horizontal rules join sequences, separate list rows, or underline labels. Rectangular color fields create hierarchy without card stacks. Density stays moderate: one proposition per slide, generous negative space around major statements, and smaller copy clustered near the evidence it interprets.

The three evidence-proof archetypes are fixed patterns:

1. **Image + right note:** wide source frame on the left, full-height ink annotation panel on the right.
2. **Panorama + bottom band:** wide source frame above, full-width ink annotation band below with claim and detail in separate columns.
3. **Left note + image:** narrow ink annotation panel on the left, source frame on the right.

## Elevation & Depth

The system is flat. It uses no shadows, bevels, glow, translucency, or simulated material depth. Hierarchy comes from tonal inversion, strong rectangular fields, image-to-annotation adjacency, and 1–2pt rules. Embedded source frames retain their original interface depth, but the deck adds no decorative elevation around them.

### Named Rules

**The Flat Evidence Rule.** Source images sit flush to their editorial frame. Do not turn screenshots into floating cards or device mockups.

## Shapes

The dominant form language is square and architectural: full-bleed fields, hard-edged bands, narrow rules, rectangular labels, and simple columns. Circles appear only as small numbered or stage markers, implemented as fully rounded 0.38–0.50 inch shapes. No rounded card containers are used. The cover and closing slide share a narrow red vertical spine, while the central slides rely on rules and bands rather than framing chrome.

## Components

### Editorial Slides

- **Paper slide:** Warm Paper field, Editorial Ink headline, muted supporting copy, and a small lower-right folio.
- **Ink slide:** Editorial Ink field, Paper-on-Ink headline, muted warm-gray support text, and selective Signal Red or Archive Tan emphasis.
- **Spine slide:** Ink slide with a 0.16-inch Signal Red bar on the left; used only for the cover and conclusion.

### Evidence Proofs

- **Shape:** Source image and annotation field are square-cornered and flush.
- **Annotation:** Ink field with a 2pt Signal Red rule, bold warm-white claim, and quieter warm-gray detail.
- **Behavior:** Keep source evidence uncropped where practical and keep interpretive language outside the screenshot. Rotate among the three established archetypes to avoid repetition.

### Process Markers

- **Numbered marker:** Signal Red circle with centered white bold numeral; approximately 0.38–0.48 inches.
- **State marker:** Moss indicates stable or macro states; Signal Red indicates selection, live iteration, or risk.
- **Connector:** Archive Tan 2pt horizontal rule; Soft Rule for low-emphasis transitions.

### Bars and Labels

- **Strong band:** Solid Moss, Signal Red, or Editorial Ink rectangle with white text; square corners and no outline.
- **Taxonomy strip:** Archive Tan or Soft Rule fill with Editorial Ink text.
- **Micro-label:** Uppercase, bold, compact, and aligned directly to the object or rule it names.

### Folios and Provenance

- **Folio:** `current / total` at lower right in 8pt Muted Copy on paper or a lighter muted gray on ink.
- **Provenance:** Small, low-contrast metadata is allowed only at the deck edge and never carries the main argument.

## Do's and Don'ts

- **Do** begin with Warm Paper, Editorial Ink, and one semantic accent.
- **Do** use red for decisions, warnings, active steps, and decisive conclusions.
- **Do** preserve the three evidence archetypes and keep commentary native and editable.
- **Do** build hierarchy from typography, alignment, tonal fields, and rules.
- **Do** keep slides to one legible argument and reserve the smallest type for metadata.
- **Don't** add gradients, glow, shadows, glass effects, or decorative texture.
- **Don't** introduce rounded card grids; circles are reserved for compact markers.
- **Don't** recolor, redraw, or visually imitate source evidence when an exact frame is available.
- **Don't** use all three accent colors at equal strength on the same slide.
- **Don't** treat screenshots as decoration; each one must prove a specific interface state.
