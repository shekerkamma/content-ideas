# Trend Brief — Fintech Gradient Hero (from stripe.com, captured 2026-07-13)

> Extracted from a real, current live capture, not invented. Sampled colors via
> `extract_palette.py`; typography/component read visually from the capture.
> Format matches this repo's `DESIGN.md` (Google Stitch) shape — drop straight into
> a project's `docs/design.md`, hand to `marp`/`branded-pptx-deck`, or use directly
> for one Track A graphic.

## 1. Visual Theme & Atmosphere

**Aurora Fintech.** A clean white canvas broken by one large diagonal aurora-mesh
gradient sweep (blue → violet → magenta → orange) confined to the hero band only —
everything below the fold reverts to plain white/gray. The mood is precise and
confident, not playful: dense product-screenshot content (phone mockup, checkout
form) sits directly on the gradient with no card container, so the gradient reads as
atmosphere, not decoration.

- **Density:** Low in the hero (one headline, one CTA), high below the fold (data
  tables, real UI mockups).
- **Philosophy:** One gradient sweep does all the color work; the rest of the page is
  grayscale. Never repeat the gradient elsewhere on the page.
- **Signature element:** the gradient is diagonal and asymmetric (heavier top-right),
  not a centered radial blob — that asymmetry is what keeps it from reading generic.

## 2. Color Palette & Roles

Sampled from the actual hero capture (`extract_palette.py --crop 0,0,1440,900`):

| Token | Hex | Role |
|---|---|---|
| `--bg` | `#f8f8f8` | Base canvas below the fold (68% of sampled pixels) |
| `--ink` | `#1a1a2e` (visually read; darkest headline text) | Primary headline text |
| `--muted` | `#888888` | Secondary/supporting text |
| `--gradient-blue` | `#bbc7f9` | Gradient stop 1 (top-left) |
| `--gradient-violet` | `#d6a9e4` | Gradient stop 2 |
| `--gradient-orange` | `#fe9617` | Gradient stop 3 |
| `--gradient-coral` | `#fe82aa` | Gradient stop 4 |
| `--gradient-navy` | `#2d4870` | Gradient shadow/depth tone |

**Rule (observed):** the gradient never touches body text — headline sits in the
plain-white left column, gradient occupies the right ~55% of the hero only.

## 3. Typography Rules

- Sans-serif throughout (system/product sans, not a display serif) — headline is
  large, tight line-height, mixed-weight within one heading (bold black + lighter
  blue-gray on the second/third lines) to de-emphasize supporting clauses without a
  separate font size.
- Small mono-ish uppercase label above the headline ("Global GDP running on
  Stripe:") — same restrained-eyebrow pattern as this repo's own DESIGN.md.

## 4. Component Stylings

- **CTA button:** solid indigo/violet fill, white text, small corner radius, no
  gradient border — deliberately flat and quiet against the loud hero background.
- **Logo strip:** plain black/brand-color wordmarks on white, directly below the
  hero, no cards or dividers — restraint after the loud gradient.
- **Below-fold cards:** two-column white cards with a real product screenshot
  (phone mockup) bleeding out of the card boundary at the bottom edge.

## Hand-off

This brief is a design-token INPUT, not a finished deliverable. Three consumers:
1. **Single graphic** — feed directly into a Track A HTML/SVG spec's `Style:` line.
2. **Slide deck** — drop into a project's `docs/design.md` (or hand to `marp`'s theme
   `:root` block / `branded-pptx-deck`'s color scheme) so slides share this identity.
3. **Full design system** — hand to the `design-system` skill as calibration input
   alongside the source screenshot.

ai-graphics does not build the deck itself — see SKILL.md's "NOT for editable decks"
boundary. This brief is the hand-off artifact, not a replacement for those skills.
