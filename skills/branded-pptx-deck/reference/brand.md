# Brand & patterns reference

## Default palette (the user's Canva-Pro look)

| Token | Hex | Use |
|-------|-----|-----|
| NAVY | `#0A1628` | backgrounds, dividers, dark bars |
| NAVY_2 | `#12243A` | secondary panels on navy |
| TEAL | `#00C9A7` | primary accent, top band, "high"/good |
| ACCENT | `#009B82` | secondary teal, card spines |
| DARK_TEAL | `#008F75` | bars, lower-rank bars |
| LIGHT_TEAL | `#E0F7F1` | body text on navy |
| GOLD | `#FFB800` | stat numbers, the "ask", priority |
| AMBER | `#F2A83B` | "mixed"/medium in scorecards |
| CORAL | `#E05A6B` | "expected/negative" column |
| SOFT | `#F4F7F8` | light card fill |
| INK | `#1B2B3C` | body text on light |
| MUTED | `#5B6B7C` | subtitles, footers |
| Font | **Calibri** | headings + body |

Re-skin by constructing `Brand(NAVY=hx("..."), TEAL=hx("..."), FONT="Inter", ...)` and
passing it to `Deck(brand=...)`. Everything inherits.

## The Canva-Pro template (source of this palette)

Not in every repo — it lives in `~/projects/hyundai-peopletech-deck/`:
- `AI-Engineering-Business-Use-Cases-Canva-Pro.pptx` (36-slide template, 16:9)
- `build_canva_style_deck.py` (the `build_uc_slide` layout: teal left panel + Challenge/
  Solution + gold stat boxes + How-it-works + Solution-stack bar + Systems/Users bars)

The Canva **MCP** has no usable brand templates for this account (template search is empty;
one unnamed brand kit). So "adapt the Canva template" = build locally with `pptxkit` using
this palette — not Canva autofill.

## Slide-pattern recipes (compose from `Deck` primitives)

- **Cover** — `slide(fill=NAVY)`, right strip `NAVY_2` + 6px `TEAL` edge, kicker (TEAL),
  big title (WHITE, shrink), teal rule, subtitle, chips row.
- **Section divider** — `slide(fill=NAVY)`, 0.18" TEAL left edge, "SECTION 0X" (TEAL),
  large title, rule, subtitle.
- **Header content** — `header(title, subtitle)` then bullets/cards starting ~`Inches(1.8)`.
- **KPI grid** — N navy rounded boxes; big GOLD/TEAL number + WHITE label + note; takeaway band.
- **Cards / conclusions** — white rounded cards (shadow=True) with a navy index chip.
- **Comparison** — two columns: CORAL header "expected" vs TEAL header "observed".
- **Executive summary one-pager** — BLUF navy banner + 3 columns (Situation/Insight/
  Recommendation) + a GOLD "THE ASK" strip.
- **Storyboard** — 5 panels (Situation→Complication→Question→Answer→Action) with → arrows.
- **Decision scorecard** — rows = options/lanes, cols = factors; cells colored H=TEAL,
  M=AMBER, L=grey; a Priority pill per row. Label scoring as judgment, not measured data.
- **Use-case "realization"** — teal panel: Challenge / How-it's-realized cards, gold stat
  boxes, How-it-works (→ steps), Solution-stack navy bar, Systems/Users bars; navy right
  strip lists the named organizations.

## Delivery (WSL → Windows PowerPoint)

```bash
cp out.pptx "/mnt/c/Users/<user>/OneDrive/Desktop/Name.pptx"
powershell.exe -NoProfile -Command "Start-Process 'C:\\Users\\<user>\\OneDrive\\Desktop\\Name.pptx'"
```
If the copy hits "Permission denied", the file is open in PowerPoint (locked) — write a new
filename (e.g. `Name-FIXED.pptx`) rather than overwriting.

## Pre-flight checklist

1. `Deck.save()` returned without raising (built-in `validate_pptx`).
2. `preview_pptx.py` contact sheets reviewed — no overflow, no collisions.
3. Slide count meets any stated minimum.
4. No invented numbers; qualitative labels where the source lacks data.

## Learned gotchas (codified from the DataStaqAI book build)

- **Colors must be `RGBColor`** — pass `b.NAVY`/`hx("RRGGBB")`, never a `"#RRGGBB"` string (raises `ValueError: assigned value must be type RGBColor`).
- **`d.M` / `d.CW` are EMU ints** — `d.CW - Inches(x)*2` returns a plain int with no `.inches`. Compute derived geometry (grids/quadrants) from float-inch constants instead.
- **Speaker notes:** `slide.notes_slide.notes_text_frame.text = "..."` on the slide returned by `d.slide()`.
- **`preview_pptx.py` is matplotlib-only — no LibreOffice/soffice needed.** It approximates (ignores auto-shrink) and draws pictures as grey "[image]" placeholders. Visual QA works with zero install.
- **Merging decks into a master:** deepcopy each `shape._element` into a blank layout, remap image `r:embed`/`r:link` rIds, and create image parts via `master.part.package.get_or_add_image_part(BytesIO(blob))` — using `relate_to(target_part)` causes duplicate `imageN.png` zip entries → PowerPoint repair.
- **Optional companion pipeline:** `scripts/compile.py` + `resources/template.pptx` build dark-teal slides from a `findings.json` Universal Schema (table/split/bullets/quotes_grid); also wired into the `strategy-consulting` skill's "Automated Deck Pipeline".
