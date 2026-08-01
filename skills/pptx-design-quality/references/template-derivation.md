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
  inspection. Either input works alone; both together cover more fields.

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
| `geometry.grid_columns`, `geometry.gutter_inches`, all of `composition.*` | Not derived — no reliable signal exists in either input | Always kept at the shipped template's default; the script prints `defaulted:` for each |
| `archetypes[]` | Union of archetype ids whose `max_words` (from `slide-archetypes.json`) is at or above at least one evidence slide's word count, plus `cover`/`executive-summary`/`section-divider` always included as structural defaults | Deliberately permissive (a candidate list, not a final selection) — tailor it down before build |

Every derived or defaulted field is printed to stdout as `derived: ...` or
`defaulted: ...` so the draft's provenance is auditable without diffing JSON.

## Non-goals

- No logo detection or extraction from slide images.
- No icon-style classification — stays the fixed template placeholder string.
- No numpy/scikit-learn dependency for color clustering; Pillow-only.
- Never auto-writes the canonical `template-profile.json`.
