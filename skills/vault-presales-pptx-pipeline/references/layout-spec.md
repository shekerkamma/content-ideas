# Layout Specification — the mechanism that replaces hand-typed coordinates

**Why this exists.** Placing every object with a literal `left/top/width` means layout is
*hard-coded, not specified*: one label grows and every downstream coordinate is wrong, and
"faithful layout" becomes trial-and-error. This spec makes layout a first-class part of the
design system — a grid and a template catalog — so coordinates are **derived**, never typed.

Proven on: `DeepGrid-IM-Recreation-v2` (7 slides, grid-driven native + HTML/CSS graphics,
OfficeCLI passed / 0 issues, 0 out-of-bounds).

---

## 1. Two authoring layers, one rule each

| Layer | Rule | Tool |
|---|---|---|
| **Native slide objects** (titles, KPIs, tables, cards, citations) | Place from the **grid**, never from raw pixels | `deck-grid.mjs` + templates |
| **Graphics** (flows, comparison panels, diagrams) | Lay out with a **real layout engine**, not hand coordinates | HTML/CSS (flexbox/grid) → PNG; SVG only for true geometry |

The dividing line for graphics: **if it is boxes-and-labels, it is CSS.** Reserve raw SVG
for genuine vector geometry (the 3D tensor cube's isometric math). I used SVG for the
cascade in v1 — wrong tool; v2 rebuilt it as 32 lines of flexbox with **zero coordinates**
(vs 67 lines of hand-placed SVG).

---

## 2. The grid (`deck-grid.mjs`)

```
Canvas 1280 × 720 · margin 48 · 12 columns · gutter 20 · inner width 1184 · colW ≈ 80.3
```

**Vertical bands** (the horizontal rules of the page):

| Band | Top | Height | Holds |
|---|---|---|---|
| KICKER | 26 | 18 | section eyebrow |
| TITLE | 50 | 46 | slide assertion (Georgia 29) |
| SUB | 100 | 28 | one-line subtitle |
| RULE | 140 | 2 | divider |
| BODY | 168 | 468 | all content |
| FOOTER | 683 | 34 | rule + footer + page no. |

**Accessors** — you say *where in the grid*, the function returns pixels:

- `cx(i)` — left edge of column *i* (1-based)
- `span(a,b)` — width of columns *a..b* inclusive
- `bandTop(name)` / `bandH(name)` — vertical band position
- `cols(n)` — **N equal columns across the body** (this is CSS `fr(1) fr(1) …`, computed)
- `rows(n, {top,height})` — N stacked rows
- `cellGrid(r,c,region)` — an r×c cell matrix

Example — a 4-tile KPI row never types a coordinate:

```js
const boxes = cols(4);            // [{x,w}×4], gutters handled
boxes.forEach(({x,w}) => kpiTile(x, bandTop('BODY'), w, …));
```

Split a slide 7/5: table on `span(1,7)`, KPI column on `cx(8)…margin`. Change the grid
constants once and every slide re-flows.

---

## 3. Template catalog (compose from the grid)

Each template takes content and places it via the grid — the L-series layouts made real:

| Template | Fills |
|---|---|
| `tHeader(kicker,title,subtitle,page)` | KICKER+TITLE+SUB+RULE+footer bands |
| `tFooter(page,{dark})` | rule + footer + page number |
| `tKpiRow(items,{top,left,right})` | N KPI tiles auto-spanned via `cols(N)` |
| `tCardRow(cards,{top})` | N content-fitting cards via `cols(N)` |
| `tTable(x,y,w,colspec,rows)` | header + zebra rows + one highlight |
| `tCaption(text,{dark})` | graphic caption band pinned above footer |

A slide becomes: pick templates, pour in content. No pixel appears in slide code.

---

## 4. Graphics: HTML/CSS is the default, SVG is the exception

- **`assets/cascade-flex.html`** — flow of nodes as flexbox; branch pairs auto-stack; even
  spacing free. 32 lines, no coordinates.
- **`assets/fullstack.html`** — three equal-height columns; spec bars pinned to the bottom
  with `margin-top:auto` (a flexbox idiom that is painful in hand-SVG).
- **`assets/cube.svg`** — the 3D systolic cube: genuine isometric geometry, so SVG is
  correct here. Parameterised in `cube.svg.py`, not hand-drawn.

All render via `~/.claude/skills/ai-graphics/scripts/html_to_png.mjs` (headless browser,
free, deterministic). The `.html`/`.svg` ships beside the `.png` as the editable source.
Placed as pictures **under native live text** — no slide is flattened.

---

## 5. Why not the tool's native flow containers?

artifact-tool exposes `C.row` / `C.grid` / `C.fr`, but in testing they exported without
error and **rendered blank** — the composition semantics of the minified engine did not
behave as documented, and the tool's own reference recommends absolute positioning because
it "maps 1:1 to the pixel grid and is far easier to QA." So the grid is computed in JS on
top of the reliable absolute primitives: the same declarative benefit (derived coordinates,
change-once-reflow) without depending on a finicky engine, and native objects stay editable.

---

## 6. Adoption checklist

1. `import { GRID, cx, span, bandTop, cols, rows } from './deck-grid.mjs'`.
2. Native slides: `tHeader(...)` + templates; positions from `cols()/span()/cx()/band*()`.
3. Graphics: HTML/CSS flexbox by default; SVG only for true geometry; render via
   `html_to_png.mjs`; keep the source file beside the PNG.
4. QA unchanged: OfficeCLI issues = 0, 0 out-of-bounds, 0 flattened slides, visual review.
5. Promote `-draft` → `-reviewed` only after all four pass.

> Next step to make this durable: fold §2–§4 into the canonical
> `Client-Ready PPTX Design System` and ship `deck-grid.mjs` in the skill's `assets/`
> beside `deck-kit.mjs`, so every future deck inherits the grid instead of re-deriving it.

---

## 7. Fix log — graphic/slide background must match

**Symptom (v2 slide 3):** the dark cube graphic on a white slide rendered as a hard-edged
dark rectangle floating in white — reads as broken.

**Cause:** a placed graphic whose background colour differs from the slide's. `contain` fit
letterboxes the image, exposing the mismatch as a framed island.

**Rule:** *a placed graphic's background must equal the slide background.* Either set the
graphic's canvas fill to the slide colour, or make the slide match the graphic (a dark
glowing diagram belongs on a dark slide). Transparency is **not** a reliable route —
`html_to_png` flattens alpha to opaque, so color-match explicitly.
