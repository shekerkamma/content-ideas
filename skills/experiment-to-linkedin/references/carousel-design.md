# Carousel design: editorial report

`assets/template.html` is the design. Fill it with `scripts/fill_template.py` (skeleton → values
→ fill; see SKILL.md step 5), chart numbers included. Don't restyle per post. The user picked this direction from three mockups after
rejecting two others (see `examples/code-mode.md`), so changing it is the user's call.

## Tokens

| Token | Hex | Use |
|---|---|---|
| paper | `#FFFFFF` | background |
| ink | `#111111` | headlines, masthead rules, values |
| body | `#3A3A3A` | standfirst and table text |
| muted | `#6B6B6B` | labels, axis ticks, source lines, footers |
| hair | `#D9D9D9` | table rules, footer rule, chart gridlines |
| accent | `#A4161A` | the change arm, the "Changed" row, one `<em>` per headline |
| base | `#9AA3AD` | the baseline arm's bar |
| wash | `#F4F4F2` | code block background |

Type: **DM Serif Display** (headlines, masthead title, key figures, callout) and **Inter**
(everything else, tabular numerals). IBM Plex Mono for code. All three are installed locally;
the stacks fall back to Georgia, Helvetica and DejaVu Sans Mono.

## Slide plan (6)

| # | Archetype | Focal point |
|---|---|---|
| 1 | Verdict | headline "gain. <em>cost.</em>", standfirst, three key figures in a ruled strip |
| 2 | Method | headline + ruled method table (task, answer key, held constant, changed, measured) |
| 3 | Metric A | finding as headline, horizontal bar chart with axis, source line |
| 4 | Metric B | same chart; a red-ruled callout carries the correctness result |
| 5 | The catch | headline + feature table, limits in the accent |
| 6 | Rule | headline, "use it for / keep it off for" columns, optional code block |

Only one metric? Delete slide 4 and renumber the masthead pages `n / 5`.

## Headlines

Every headline is the finding, not a topic ("Code Mode cut conversation tokens by 48%", not
"Token usage"). Put `<em>` on exactly one span (the number or the turn), which colours it red.

## Bar charts

- Set `--max` on `.plot` to a round number just above the largest value (34.4 → 40, 67 → 80).
- Set `--v` on each `.bar` to the raw value in the same unit. Length is `v / max × 640px`.
- Tick labels go at 0 / 25 / 50 / 75 / 100 % of `--max` (40 → 10k, 20k, 30k, 40k).
- Baseline bar is `.bar` (grey), the change is `.bar b` (red), with its value in `.val acc`.
- The source line under every chart is required. It names where the number was read.

## Review checklist (each slide, full size)

- no `[[placeholder]]` left (render.mjs refuses anyway)
- no one-word last line (headlines and the callout use `text-wrap: balance`)
- bar values stay on one line, and both bars start at the same x
- bar lengths match the numbers (34.4 of 40 = 86 % of the axis)
- every number matches `claims.md`
- slide order matches the post
- code-block lines are broken by hand, not wrapped by the browser
