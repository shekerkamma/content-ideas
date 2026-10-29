# L01–L16 Layout Library — canvas → profile → PPTX

An end-to-end exercise of `derive_template_profile.py --canvas`. The point is
that **no design value is written in the deck builder**: every type size,
margin, grid, radius and brand colour in the `.pptx` is read out of
`template-profile.json`, which was measured off the design canvas.

## Chain

```
build_canvas.py                → canvas/*.dc.html + canvas.json   (17 artboards, 1280×720)
derive_template_profile.py     → draft-template-profile.json      (--canvas)
  cp + validate_template_profile.py → template-profile.json
build_deck.py                  → L01-L16-Layout-Library-reviewed.pptx (16 slides)
lint_pptx.py                   → qa/lint-report.json              (clean: 0 errors, 0 warnings)
preview_pptx.py                → qa/preview/contact_*.png         (reviewed)
```

Re-run the whole thing:

```bash
python3 build_canvas.py
python3 ../../skills/pptx-design-quality/scripts/derive_template_profile.py --run . --canvas canvas
cp draft-template-profile.json template-profile.json
python3 ../../skills/pptx-design-quality/scripts/validate_template_profile.py template-profile.json
python3 build_deck.py
python3 ../../skills/pptx-design-quality/scripts/lint_pptx.py \
  L01-L16-Layout-Library-reviewed.pptx --config deck-design.json --out qa/lint-report.json
```

## Derived values, and what they came from

| Profile field | Value | Canvas source |
|---|---|---|
| `typography.title_pt` | 30.0 | 40px `.title` on `Main.dc.html` × 0.75 |
| `typography.body_pt` | 13.5 | 18px `.body` |
| `typography.caption_pt` | 7.5 | 10px `.foot` |
| `geometry.safe_margin_inches` | 0.5 | 48px `padding` on the 1280px `.root` |
| `geometry.grid_columns` | 12 | `grid-template-columns: repeat(12, 1fr)` |
| `geometry.gutter_inches` | 0.167 | `gap: 16px` |
| `composition.corner_radius` | 0.083 | `border-radius: 8px` |
| `brand.colors` | `#FFFFFF` / `#0A1628` / `#00B4D8` | declared palette, top 8 by frequency |
| `brand.heading_font` / `body_font` | Georgia / Aptos | family beside the largest / smallest size |

Every one lands inside the Client-Ready PPTX Design System's stated bands
(title 24–30pt, body 12–14pt, caption 7–8pt).

## Two findings this run produced

1. **A shared stylesheet defeated the reference-artboard scoping.** All 17
   artboards carry the same `<style>` block, so a `.cover { 64px }` rule that
   only the cover element uses put 48pt into `title_pt` on a body slide whose
   title is 40px. `derive_template_profile.py` now ignores CSS rules whose
   classes never appear in that artboard's markup; pinned by
   `test_unused_rules_in_a_shared_stylesheet_do_not_join_the_type_ramp`.

2. **The design system's own kicker fails WCAG AA.** "Kicker: 8–10 pt uppercase
   cyan" on white is 2.46:1 against a 4.5:1 floor, and cyan KPI numerals on
   `#F8FAFC` are 2.36:1. `build_deck.py` keeps `#00B4D8` exactly as specified on
   rules and accent bars — no text sits on those — and derives a darkened
   variant of the same hue for text, so a future palette recomputes rather than
   re-failing. 37 contrast warnings → 0. Worth fixing in the vault spec itself.

## Caveats

- `preview_pptx.py` approximates slides from shape geometry with matplotlib; it
  is not a PowerPoint render. Rounded corners and font substitution are not
  visible in the contact sheets. No PowerPoint-native render QA was run.
- Body font is Aptos (ships with M365). On a host without it PowerPoint will
  substitute; the design system says to apply a fallback deliberately rather
  than rely on silent substitution.
- Slide content is layout specification, not client evidence. This deck is a
  reference for the layout library — it carries no sourced claims, and a canvas
  must never be an evidence source.
