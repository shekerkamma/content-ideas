# Slide archetypes & content contract

Every slide is a `<section class="slide" data-title="…">` inside `#stage`. Fill
one with the archetype that fits the point. Copy the block, swap the text.
`assets/deck.example.html` is a complete 13-slide worked example.

## Semantic colour tokens (never use raw colours)

Classes carry meaning, so a `theme.css` swap recolours the whole argument
consistently:

| class | meaning | in the ServiceNow deck |
|-------|---------|------------------------|
| `a` / `a-l` / `a-eye` / `a-v` | **Accent A** — the subject / competitor / their strength | amber |
| `b` / `b-l` / `b-eye` / `b-v` | **Accent B** — our wedge / "what has to be true" | teal |
| `alert` / `alert-eye` | **Alert** — kill-criteria / risk | red |

Apply the semantic class to `<span>`/`<strong>` inside titles and to the
`-l` / `-eye` / `-v` modifiers on cards, eyebrows, and verdicts.

## Common parts

- **Eyebrow:** `<div class="eyebrow"><span class="num">01</span> Section label</div>`
  (add `a-eye` / `b-eye` / `alert-eye` to tint). The leading `.dot` is only for
  the cover.
- **Action title:** `<h2>` — a so-what assertion, not a topic. Wrap the pivot
  words in a semantic span.
- **Numbers/labels** render in mono automatically; wrap data in `<b>` inside body
  copy so it picks up tabular mono figures.

## The ten archetypes

1. **thesis** (cover) — `.mega` headline (two lines, second line semantic), `.lede`
   subtitle, `.memo-meta` 3-up key/value grid (last item spans full width).
2. **moves-row** — `.moves-row` of 3 `.move-card` (each `.move-tag` + `<p>`). Left teal rail.
3. **grid-5** — five `.fact` cards, each `a-l` or `b-l` (top rule colour) + `<h3>` + `<p>`.
   Use for "5 reasons / forces / weaknesses".
4. **stat-band + pull** — `.stat-band` of 4 `.stat` (`.stat-n` big number + `.stat-l`),
   optional `.pull` blockquote with `<cite>`. Use for evidence dumps.
5. **stack-diagram** — vertical `.layer-tower` (accent A) / `.layer-divider` (alert
   chip) / `.layer-ground` (accent B). Use for any "two-layer, they-own-top /
   we-own-bottom" spatial argument.
6. **gap-visual** — two `.gap-bar` with `.gap-fill` (`fill-a` / `fill-b`, inline
   `height:NN%`), a `.gap-arrow` delta chip, and a `.gap-note`. Use for a stark
   two-number comparison.
7. **recon** — `.recon-row`s (layer label | `.recon-verdict` `a-v`/`b-v` | why).
   Use to reconcile competing cases.
8. **move-detail** — `.md-spec` (key/value `.spec-item`s) beside a `.truth-block`
   of `.truth.true` ("what has to be true") + `.truth.kill` ("what proves it
   wrong"). Use `.truth-block.wide` (2-up) when there's no spec column. Use for a
   recommendation with kill-criteria.
9. **killbox** — `.killbox` with `.killcond` (the if), `.killthen` (the consequence),
   `.killnot` (the discipline line). Use for a single decisive rule.
10. **src-list** — 2-column `.src-list` of sources.

## Density budget (fits 1280×720 canvas)

- grid-5: ≤ ~34 words per card.
- stat-band: number ≤ 9 chars, label ≤ ~14 words.
- move-detail truth blocks: ≤ ~40 words each.
- Action titles: ≤ 20 characters over the width — the `<h2>` `max-width:20ch`
  keeps them to ~2–3 lines; longer titles wrap to 4+ lines and crowd the body.

If content exceeds the budget, split into two slides rather than shrinking type.
The renderer captures a fixed canvas — overflow is clipped, not scrolled, so QA
the contact sheet.

## Adding a genuinely new layout

Add the component CSS to `deck.css` using `var(--…)` tokens only (never raw
colours), then document it here. Keep `theme.css` limited to tokens so a reskin
never touches structure.
