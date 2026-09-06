# Deriving a draft template profile

`scripts/derive_template_profile.py` produces a **draft** `template-profile.json`
from a reference deck so a rebuild starts from a real design instead of the blank
template. It never writes the canonical `template-profile.json` — only a
`draft-template-profile.json` that must be reviewed, copied over, and validated
with `validate_template_profile.py`.

## Inputs

- `--evidence <presentation-evidence.json>` — a bundle built by
  `presentation-source-bundle`. Supplies rendered `slide_images/*.png` for color
  sampling and `extracted_text` word counts for archetype candidates.
- `--pptx <reference.pptx>` — the original PowerPoint file, when available.
  Supplies aspect ratio, fonts, and placeholder geometry via `python-pptx`
  inspection.
- `--canvas <canvas-dir>` — a `/design` canvas working tree: the directory
  holding `canvas.json` and the `*.dc.html` artboards (the `canvas.json` path
  itself is also accepted). Stdlib-only — needs neither `python-pptx` nor
  Pillow. Supplies the fields below, including the three the other two inputs
  document as underivable.

Any input works alone; together they cover more fields. When `--canvas` is
combined with `--pptx`, **the canvas wins** every field it derives: a canvas is
the design you intend, a reference deck is the design you have.

## Why a canvas measures better than it looks

A `/design` artboard is authored in CSS px; a slide renders on a fixed-inch
stage. The reference artboard's frame width in `canvas.json` fixes the scale
for the whole profile:

```
inches_per_px = slide_width_inches / frame_width_px     # 16:9 -> 13.333in, 4:3 -> 10in
pt = px * inches_per_px * 72
```

At the vault pipeline's own stage (`deck-kit.mjs`: `setViewportSize(1280, 720)`
= exactly 13.333 x 7.5in) that resolves to 0.75pt/px — the familiar 96dpi CSS
constant. **It is derived, never assumed.** Draw the same design at 1920px wide
and the scale is 0.5pt/px; hardcoding 0.75 would report every size a third too
large. That reading error is what this input exists to prevent, so
`test_derive_from_canvas.py` pins both frame widths.

The scale is only derived when the reference artboard has a 16:9 or 4:3 frame
in `canvas.json`. Without one, every pt and inch field stays at the template
default and the script prints `defaulted: px scale`; fonts, colors, grid
columns and archetypes still land, since those are unitless.

### The reference artboard

Typography is read from **one** artboard, picked in this order: `Main.dc.html`,
then `launch.file`, then the first entry in `canvas.json`. Colors, font
families, grid columns and corner radius are read from the whole canvas.
The split is deliberate: an L01 cover hero at 64px would otherwise set
`title_pt` for every slide in the deck.

## Heuristics and their limits

| Field | Method | Caveat |
|---|---|---|
| `template.source` | Literal passthrough of the input path | The one field the shipped template ships as `null` and nothing else populates |
| `template.aspect_ratio` | `slide_width / slide_height` compared to 16:9 and 4:3 within 2% tolerance | Falls back to `custom` outside tolerance |
| `brand.colors` | Downsample each slide image to 48×27, quantize to 8 color clusters, classify by luminance: lightest cluster → `page`, darkest → `ink`, most-saturated remaining cluster → `accent` | A Pillow-only heuristic, not perceptual color science; always eyeball the result against the actual brand palette before treating it as final |
| `brand.heading_font` / `body_font` | Distinct `run.font.name` values across all text runs, alphabetically first/last | Alphabetical selection is arbitrary when a deck uses exactly two fonts inconsistently; verify manually |
| `typography.title_pt` / `body_pt` | Max font size seen in title placeholders / min font size seen in body placeholders | Skipped if the derived value would fall below the schema's own minimum (18pt title, 8pt body) rather than writing an invalid draft |
| `typography.max_font_families` | Count of distinct font names found | — |
| `geometry.title_zone_inches` | Bottom edge (top + height) of the lowest title placeholder found | Assumes the title sits at the top of the slide |
| `geometry.safe_margin_inches` | Smallest gap between any placeholder edge and the corresponding slide edge, across every placeholder in the deck | This is the tightest inset actually used, not a design recommendation |
| `geometry.footer_zone_inches` | Height of any non-title placeholder within 0.6in of the bottom edge | Only fires when such a placeholder exists |
| `geometry.grid_columns`, `geometry.gutter_inches`, all of `composition.*` | Not derived from `--evidence` or `--pptx` — no reliable signal exists in either | Kept at the shipped template's default and printed as `defaulted:`, unless `--canvas` supplies them (below) |

### `--canvas` only

Every value below is parsed out of CSS declaration blocks and inline `style`
attributes with regexes — flat CSS, no browser, no layout engine. It reads what
the markup *declares*, never what the browser would *compute*: a cascade, a
CSS variable, or a media query can move a number this table will not follow.

| Field | Method | Caveat |
|---|---|---|
| `template.aspect_ratio` | Reference artboard's `w`/`h` in `canvas.json`, 16:9 and 4:3 within 2% | `custom` outside tolerance, which also disables the px scale |
| `brand.heading_font` / `body_font` | The family declared alongside the largest `font-size`; body is the smallest-sized family that is not the heading | Replaces the `.pptx` path's alphabetical guess. A block that sets `font-family` without `font-size` contributes to the family count only |
| `typography.title_pt` | Largest `font-size` on the reference artboard | A KPI number larger than the title will win — check the printed artboard name against what you drew |
| `typography.body_pt` | Median of the reference artboard's sizes below the title size | — |
| `typography.caption_pt` | Smallest `font-size` on the reference artboard | — |
| `typography.metric_pt` | **Not derived** | A KPI number and a heading are the same thing in markup; nothing distinguishes them without layout |
| `brand.colors` | Every `#rgb`, `#rrggbb` and `rgb()/rgba()` across all artboards, top 8 by frequency, then the same luminance/saturation classification the image path uses | One heuristic shared with `--evidence`, not a second one. `currentColor`, gradients and CSS variables are invisible to it |
| `geometry.grid_columns` | Most common track count in `grid-template-columns` (`repeat(N, …)`, else whitespace-separated track count) | The first field `--pptx` cannot reach |
| `geometry.gutter_inches` | Most common `gap` / `column-gap` / `grid-gap`, converted at the derived scale | The second |
| `composition.corner_radius` | Most common `border-radius`, converted at the derived scale | The third. Shorthand with four values takes the first |
| `geometry.safe_margin_inches` | Smallest `padding` on a block whose `width` matches the frame width within 2px | Only fires when a frame-width root declares its padding; a flex/grid-centred root will not match |
| `archetypes[]` | Artboard file stems slugified and matched against `slide-archetypes.json`, plus the structural defaults | Name-driven and deterministic: `Comparison.dc.html` → `comparison`, anything unrecognized is ignored. Wins over the `--evidence` word-count guess when present |
| `geometry.title_zone_inches`, `geometry.footer_zone_inches` | **Not derived** | Both need computed layout, which regex parsing does not have |
| `archetypes[]` | Union of archetype ids whose `max_words` (from `slide-archetypes.json`) is at or above at least one evidence slide's word count, plus `cover`/`executive-summary`/`section-divider` always included as structural defaults | Deliberately permissive (a candidate list, not a final selection) — tailor it down before build |

Every derived or defaulted field is printed to stdout as `derived: ...` or
`defaulted: ...` so the draft's provenance is auditable without diffing JSON.

## Non-goals

- No logo detection or extraction from slide images.
- No icon-style classification — stays the fixed template placeholder string.
- No numpy/scikit-learn dependency for color clustering; Pillow-only.
- No browser, headless or otherwise, for the `--canvas` path — declared CSS
  only, never computed style.
- **A canvas never sources evidence.** It may set geometry, type and brand and
  nothing else; claims and numbers stay with `presentation-evidence.json` and
  `check_claim_evidence.py`. A profile derived from a canvas you drew is
  already a measurement of your own intent — letting it carry evidence too
  would make it a check derived from the artifact it is meant to check.
- Never auto-writes the canonical `template-profile.json`.
