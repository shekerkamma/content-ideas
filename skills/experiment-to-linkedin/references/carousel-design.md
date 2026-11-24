# Carousel design

`assets/template.html` is the design. Copy it, fill the `EDIT` regions, set the `data-n` counts.
Don't restyle per post; consistency across posts is the point.

## Tokens

| Token | Hex | Use |
|---|---|---|
| canvas | `#F2F1EB` | background (bone, not white) |
| ink | `#1A1A17` | punchline line, baseline numbers |
| greige | `#8F8A7E` | context lines (3.04:1 on canvas; large text only) |
| muted | `#77736A` | mono labels (4.18:1) |
| rule | `#D9D6CC` | header/footer hairlines |
| signal | `#F04E23` | the change arm, one punchline per slide, pixel squares |
| steel | `#3B3A36` | the baseline arm's squares |

Type: Inter 300/400/500 for display and body; IBM Plex Mono uppercase for labels. Both are
installed locally; the stack falls back to Helvetica/DejaVu.

## Slide plan (6)

| # | Archetype | Focal point |
|---|---|---|
| 1 | Hook statement | three lines: context (greige), gain (ink), cost (orange) |
| 2 | Setup statement | held-constant lines in greige, the one change in ink |
| 3 | Metric A | 270px hero number + two unit grids |
| 4 | Metric B | hero number + grids; correctness in the caption |
| 5 | The catch | what you lose (greige list), the sharpest limit (ink) |
| 6 | Verdict | the rule you now follow + optional code block |

Only one metric? Delete slide 4 and renumber the `0N / 06` labels to `/ 05`.

## Unit grids (the signature element)

`<div class="grid b" data-n="18">` draws 18 squares, 22 per row. Pick a unit so each arm is
roughly 10–90 squares, and say the unit in the slide footer ("1 square = 1k tokens"). Round
to the nearest unit; the exact value sits beside the label.

## Decoration squares

The `.px` squares are absolutely positioned. After copy edits, check that none sits on text or
on the code block. Move them; don't delete them all (they carry the reference's look).

## Review checklist (each slide, full size)

- no `[[placeholder]]` left (render.mjs refuses anyway)
- no one-word last line (headings use `text-wrap: balance`)
- no decoration square touching text or the code box
- hero numbers match `claims.md` exactly
- slide order matches the post
- the code block's lines are broken by hand, not wrapped by the browser
