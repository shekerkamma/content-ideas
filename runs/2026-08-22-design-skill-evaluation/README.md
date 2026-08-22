# Claude /design — evaluation deck

12 slides, 740 words. Content is the 2026-08-22 evaluation of Claude Code's
built-in `/design` skill; every figure is something verified in that session
against the installed 2.1.238 binary, this repo's contracts, or a command whose
output is quoted here or in the sibling run folder. Nothing is illustrative.

**The design system is not written in this builder.** `template-profile.json` is
copied unchanged from `../2026-08-22-l01-l16-layout-library/`, where
`derive_template_profile.py --canvas` measured it off the L01–L16 design canvas.
One profile, two decks.

## Status: reviewed

| Gate | Result |
|---|---|
| `pptxkit` save validation | passed |
| `lint_pptx.py` | clean — 0 errors, 0 warnings |
| `preview_pptx.py` contact sheets | reviewed — no red overflow boxes, no collisions |

## What the QA pass cost

Real content is denser than layout placeholders, and the first build showed it:
**6 errors, 28 warnings.** Three rounds fixed it.

1. `SHAPE_OUT_OF_BOUNDS` ×6 — a 2×2 KPI grid placed at column 5 with span 4
   ran past column 12. Re-laid to 4+4+4.
2. `SLIDE_WORD_COUNT` — three slides between 87 and 143 words against an 80 cap.
   Card notes went from three sentences to one. This is the linter enforcing
   `voice.md`'s "one idea in one sentence", and it was right.
3. `TEXT_OVERFLOW_RISK` — the title box was `Inches(0.95)`, which at 30pt allows
   exactly one line (`line_height = 30/72 × 1.2 = 0.5in`). Raised to 1.05in.

## The gates disagreed, and the contact sheet won

After lint reported **clean**, the contact sheet still drew red overflow boxes on
slides 4 and 6. The rules differ:

- `preview_pptx.py`: `overflow = total_h > h + 0.03` — a direct height comparison.
- `lint_pptx.py`: `available_lines = max(1, int(height / line_height))`.

That `max(1, ...)` floors the available height at one line, so **a box too short
for even one line is treated as having room for one**. Four shapes needing
0.22in in a 0.11in box passed lint and were plainly broken on the render.

`scripts/overflow_scan.py` in this folder replicates the preview rule headlessly,
so the discrepancy is findable without reading images. Worth deciding whether
`lint_pptx.py` should adopt the same comparison — it would newly flag existing
decks, so it is a gate-semantics change, not a bug fix.

## Caveats

- `preview_pptx.py` approximates with matplotlib; it is not a PowerPoint render.
  Rounded corners and font substitution are invisible. No PowerPoint-native
  render QA ran.
- Body font is Aptos (ships with M365); heading font is Georgia.
