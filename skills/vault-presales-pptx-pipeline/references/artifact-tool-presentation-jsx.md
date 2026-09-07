# artifact-tool presentation JSX — the client-ready PPTX build method

This is the **mandated builder** for final client-ready decks (`## PowerPoint Rule` in
`SKILL.md`). It produces **native, editable PowerPoint objects** — the thing
`Client-Ready PPTX Design System` requires ("Do not flatten full slides into images").

Validated: `Decks/_work/design-system-test/build_test_deck.mjs` (2026-07-16, 7 slides)
and `runs/2026-07-16-deepgrid-client-ready-pptx/build_deck.mjs` (20 slides, OfficeCLI
`passed` / 0 issues, 690 shapes, 442 text boxes, **0 pictures**).

---

## 1. Where the library lives, and how to run it from WSL

The tool ships inside the **Codex runtime cache**, as a Windows-native install:

```
C:/Users/sheke/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool
```

`@oai/artifact-tool@2.8.24` · deps: `skia-canvas@^3.0.6`, `@oai/walnut`

### The blocker

Importing it directly from WSL fails:

```
Error: .../skia-canvas/lib/skia.node: invalid ELF header  (ERR_DLOPEN_FAILED)
```

`skia-canvas` is a **native addon compiled for Windows**. Linux node cannot `dlopen` it.
Everything else in the package is portable JS — only this one dep is the problem.

### The fix — a one-time Linux port (verified 2026-07-16)

```bash
SRC="/mnt/c/Users/sheke/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool"
DST="$HOME/.local/artifact-tool-linux"
rm -rf "$DST" && mkdir -p "$DST" && cp -r "$SRC"/. "$DST"/
rm -rf "$DST/node_modules/skia-canvas"
cd "$DST" && npm install skia-canvas@3.0.8 --no-save     # pulls the Linux prebuild
file node_modules/skia-canvas/lib/skia.node                # => ELF 64-bit LSB, x86-64
```

**Port location: `~/.local/artifact-tool-linux`.** Re-run the above if the Codex runtime
upgrades and you want the newer artifact-tool. Match the `skia-canvas` version to the
one in the source package's `node_modules/skia-canvas/package.json`.

### Import block (WSL)

```js
const AT = 'file:///home/sheke/.local/artifact-tool-linux/dist';
const { Presentation, PresentationFile, layers: composeLayers } = await import(`${AT}/artifact_tool.mjs`);
const { textStyle, stroke, paint, Fragment, createRef }        = await import(`${AT}/presentation-jsx/index.mjs`);
const { jsx, jsxs }                                            = await import(`${AT}/presentation-jsx/jsx-runtime.mjs`);
```

Use **dynamic `await import()` with absolute `file://` URLs**. Static `import ... from
'file:///...'` also works (the reference builder does this) but hard-codes Windows paths
— prefer the constant + dynamic import so the path is swappable.

Windows original (for reference builders): same three paths under
`file:///C:/Users/sheke/.cache/codex-runtimes/.../@oai/artifact-tool/dist`.

---

## 1b. Use the kit — do not rewrite these helpers

`assets/deck-kit.mjs` is a proven, import-and-go library (card / kpi / table / barsV /
barsH / proportion / rail / chain / header / addSlide). It carries the design-system tokens,
the content-fitting card, and every gotcha below already solved.

```bash
DECK_RUN=<run-dir> DECK_NAME=<slug> DECK_FOOTER='CLIENT · INITIATIVE · DATE' node build.mjs
```

Proven: Deepgrid IM rebuild — 18 slides, 867 shapes, 547 text boxes, 0 pictures, OfficeCLI
`passed`. Start from the kit; write only slide content.

## 2. Minimum viable builder

```js
const P = Presentation.create();
const C = P.compose;

const Text   = ({ children = '', ...props }) => C.text(String(children), props);
const Shape  = (props) => C.shape(props);
const Layers = ({ children = [], ...props }) =>
  composeLayers(props, Array.isArray(children) ? children : [children]);

function addSlide(children, { background = '#FFFFFF', notes = '' } = {}) {
  const s = P.slides.add();
  s.setViewportSize(1280, 720);            // → 13.333 × 7.5 in. ALWAYS set this.
  s.compose(jsxs(Layers, {
    width: C.fixed(1280), height: C.fixed(720),
    children: [rect(0, 0, 1280, 720, background), ...children],
  }));
  s.speakerNotes.text = notes;             // notes are cheap; add them
  return s;
}

await (await PresentationFile.exportPptx(P)).save(OUT);
```

**`setViewportSize(1280, 720)` is the whole geometry contract.** 1280×720 px maps exactly
to the design system's 13.333 × 7.5 in canvas. All coordinates below are px in that space.

---

## 3. API surface (introspected, not guessed)

### `presentation-jsx` exports — only five
`Fragment` · `createRef` · `paint` · `stroke` · `textStyle`

### `P.compose` primitives
`auto` · `card` · `chart` · `column` · `fill` · `fixed` · `fr` · `grow` · `grid` ·
`hug` · `image` · `panel` · `repeat` · `row` · `rule` · `shape` · `table` · `text` · `wrap`

Sizing: `C.fixed(px)` (absolute) · `C.fr(n)` (fraction) · `C.hug()` (shrink-to-content) ·
`C.grow()` · `C.auto()`. Layout containers: `C.row` / `C.column` / `C.grid` / `C.panel`.
Use absolute positioning (`position: {left, top}`) for design-system layouts — it maps
1:1 to the spec's pixel grid and is far easier to QA than flow layout.

### Slide methods (prototype)
`compose` · `setViewportSize` · `setLayout` · `speakerNotes` · `background` · `shapes` ·
`tables` · `charts` · `images` · `elements` · `export` · `duplicate` · `moveTo` ·
`delete` · `fromMermaid` · `gridLayout` · `stackVertical` · `stackHorizontal` · `autoLayout`

### Useful top-level helpers
`addMermaidDiagramToSlide` · `addCodeBlockToSlide` · `SHAPE_GEOMETRY_NAME_TO_PROTO`

---

## 4. The style grammar (CSS-like strings — get these exactly right)

```js
textStyle('font: italic bold 16px Georgia; color: #1E293B; align: left; anchor: top; inset: 0px; autofit: shrink')
stroke('1px solid #E2E8F0')     // stroke('0px none') = no line
```

`textStyle` keys: `font` (`[italic] [bold] <size>px <family>`) · `color` · `align`
(`left|center|right`) · `anchor` (`top|middle|bottom`) · `inset` · `autofit`
(`shrink` = shrink-to-fit; **always set it** on data-driven text).

Helper pattern:

```js
function style({ size = 14, face = 'Arial', color = '#1E293B', bold = false,
                 italic = false, align = 'left', anchor = 'top', inset = 0 }) {
  return textStyle(`font: ${italic ? 'italic ' : ''}${bold ? 'bold ' : ''}${size}px ${face}; ` +
                   `color: ${color}; align: ${align}; anchor: ${anchor}; inset: ${inset}px; autofit: shrink`);
}
const tx = (t, x, y, w, h, o = {}) => jsx(Text, {
  width: C.fixed(w), height: C.fixed(h), position: { left: x, top: y },
  style: style(o), children: t,
});
const sh = (geometry, x, y, w, h, fill, lineColor = 'none', lineWidth = 0) => jsx(Shape, {
  geometry, width: C.fixed(w), height: C.fixed(h), fill,
  line: lineColor === 'none' ? stroke('0px none') : stroke(`${lineWidth}px solid ${lineColor}`),
  position: { left: x, top: y },
});
const rect      = (x,y,w,h,f,lc='none',lw=0) => sh('rect',      x,y,w,h,f,lc,lw);
const roundRect = (x,y,w,h,f,lc='none',lw=0) => sh('roundRect', x,y,w,h,f,lc,lw);
const ellipse   = (x,y,w,h,f,lc='none',lw=0) => sh('ellipse',   x,y,w,h,f,lc,lw);
```

---

## 5. Geometry names — 190 available (full OOXML preset set)

Not a short list. Everything PowerPoint has, by its OOXML preset name:

- **Basic:** `rect` `roundRect` `ellipse` `line` `triangle` `rtTriangle` `diamond`
  `parallelogram` `trapezoid` `pentagon` `hexagon` `heptagon` `octagon` `plaque`
  `teardrop` `homePlate` `chevron` `cube` `can` `frame` `halfFrame` `corner` `bevel`
- **Rounded/snipped:** `round1Rect` `round2SameRect` `round2DiagRect` `snipRoundRect`
  `snip1Rect` `snip2SameRect` `snip2DiagRect`
- **Arrows:** `rightArrow` `leftArrow` `upArrow` `downArrow` `leftRightArrow`
  `upDownArrow` `quadArrow` `bentArrow` `uturnArrow` `circularArrow` `curvedRightArrow`
  `swooshArrow` `stripedRightArrow` `notchedRightArrow` …
- **Callouts:** `wedgeRectCallout` `wedgeRoundRectCallout` `wedgeEllipseCallout`
  `cloudCallout` `callout1..3` `rightArrowCallout` …
- **Flowchart (use for architecture/process — L04/L07/L08):** `flowChartProcess`
  `flowChartDecision` `flowChartInputOutput` `flowChartTerminator` `flowChartDatabase`
  `flowChartDocument` `flowChartPreparation` `flowChartConnector` `flowChartDelay`
  `flowChartMagneticDisk` `flowChartOffpageConnector` … (~30 more)
- **Pie/arc:** `pie` `pieWedge` `blockArc` `donut` `chord` `arc` `noSmoking`
- **Stars/misc:** `star4..star32` `heart` `sun` `moon` `lightningBolt` `cloud`
  `smileyFace` `foldedCorner` `diagStripe` `bracketPair` `bracePair` `ellipseRibbon`

Full list: `Object.keys(SHAPE_GEOMETRY_NAME_TO_PROTO)`.

---

## 5b. Visual primitives — the difference between a deck and a wall of boxes

The design system says *"flat 2D charts with direct labels; remove legends when direct
labels are possible."* So **charts are shapes**, not `C.chart`. The validated reference
builder does exactly this. All of these are in `assets/deck-kit.mjs`:

| Helper | Use for | Why it beats prose |
|---|---|---|
| `proportion(x,y,w,h,segs)` | any "**X is N% of Y**" claim | draws the share **to scale** — the argument becomes visible. The single highest-value primitive. |
| `barsV(...)` | a series (prices, revenue by year) | shows the trend; direct value labels, no legend |
| `barsH(...)` | rankings / scorecards | the gap between #1 and #6 is *seen*, not read |
| `rail(x,y,w,nodes,{dark})` | milestones, mandate timelines | mirrors the reference decks' proof-of-execution strip |
| `chain(x,y,w,nodes)` | L04 process / sequenced steps | `flowChart*` nodes + `rightArrow`, native |

**Density is a correctness issue, not taste.** A card sized by grid math and filled with
three lines of text is 40–50% dead air, and a deck of those reads — correctly — as junk.
`card()` takes `'auto'` and measures its own body via `textH()`. **Never pass a fixed
height.** If a slide still looks empty, the content is too thin for the slide, not the
other way round — merge it.

Layout variety is also a correctness issue: one build shipped **L12 ×10 of 20 slides**
(the same "table + two cards"). Vary the layout per the design system's L01–L16, or the
deck flatlines regardless of how good the words are.

## 6. Export + QA

```js
// PPTX — auto-writes a sibling <name>.pptx.inspect.ndjson (move it to qa/)
await (await PresentationFile.exportPptx(P)).save(OUT);

// per-slide PNG
for (let i = 0; i < P.slides.count; i += 1) {
  const blob = await P.export({ format: 'png', slide: P.slides.getItem(i), scale: 1 });
  await writeFile(`${DIR}/slide-${String(i+1).padStart(2,'0')}.png`, Buffer.from(await blob.arrayBuffer()));
}

// montage — NOTE: in the WSL port this emitted only page 1. Build a contact sheet
// from the per-slide PNGs with PIL instead; do not trust montage for QA.
const montage = await P.export({ format: 'png', montage: true, scale: 0.45 });
```

**Contact sheet that actually works:**

```python
from PIL import Image; import glob
fs = sorted(glob.glob('qa/renders/*.png')); cols, W, H = 4, 320, 180
rows = (len(fs)+cols-1)//cols
sheet = Image.new('RGB',(cols*W, rows*H),'white')
for i,f in enumerate(fs): sheet.paste(Image.open(f).resize((W,H)), ((i%cols)*W,(i//cols)*H))
sheet.save('qa/contact-sheet.png')
```

---

## 7. Mandatory gates before `*-reviewed.pptx`

Run all of these. Evidence goes in the run folder.

| Gate | Command / check | Bar |
|---|---|---|
| Canvas | `p.slide_width/914400` | **13.333 × 7.5** |
| **No flattened slides** | count `sh.shape_type == 13` | **0 pictures** (except real photo/UI evidence) |
| Native objects | count shapes + text frames | every title/card/table/diagram is a shape |
| Speaker notes | `s.has_notes_slide` | present |
| OfficeCLI | `python3 scripts/officecli_qa.py <pptx> --out <run>/qa/officecli` | `Status: passed`, `count: 0` |
| Real render | `soffice --headless --convert-to pdf` + PyMuPDF | all pages open |
| Contact sheet | inspect it with your eyes | no overflow/clipping/collision |
| Internal-term scan | regex visible text | no tool names, paths, `EV-####`, `synthesis`, `audit` |
| Banned-number scan | regex visible text | **context-check hits** — see trap below |

---

## 8. Traps (each one cost real time)

- **`skia.node: invalid ELF header`** → you imported the Windows package from WSL. Use the
  Linux port (§1). This is *the* blocker; everything else is downstream of it.
- **Do not reach for `pptxkit` / python-pptx for final client decks.** It works and it
  validates, but the mandated method is this one, and the design system's editability rule
  is what's actually at stake. `pptxkit` remains correct for `branded-pptx-deck` decks.
- **Fonts.** `DM Serif Display` / `Questrial` / `Georgia` are **absent on Linux**. Set the
  design system's documented fallbacks *deliberately* — Georgia (display) / Arial (body) —
  because Windows PowerPoint has them. Local renders will show sans titles; that is a
  render artifact, **not** the delivered file. Say so; never let a font substitute silently.
- **Banned-number false positives.** A scan for `Q3 2024` / `Q4 2024` / `₹50K` will hit
  legitimate text — Mobileye's *real filed ASP quarters*, and the "Removed as unsupported"
  disavowal row. Scan for banned figures **asserted as fact**, not mere presence. Always
  print the surrounding text before calling it a defect.
- **Montage export is unreliable in the port** — emitted page 1 only. Use the PIL contact
  sheet.
- **`.inspect.ndjson`** is written automatically next to the PPTX. Move it into `qa/` so
  the delivery folder stays clean.
- **`flowChartTerminator` renders as a bare rule** (no filled box) — use
  `flowChartAlternateProcess` for start/end nodes.
- **Dark slides need `{dark:true}` on `rail()`** or the labels come out slate-on-midnight
  and fail the design system's 4.5:1 contrast rule. Caught only by *looking* at the render.
- **Slide count follows density, not the outline.** The design system's budget (45–90 words
  a slide) beats hitting a requested number. Consolidating 28 script beats → 20 slides is
  correct; padding to 28 is not. State the deviation.

---

## 9. Where finals go

- Vault convention: `Decks/outputs/<Name>-Client-Ready-reviewed.pptx`
- Builder + QA evidence stay together in the run folder so fixes are reproducible.
- Windows delivery: copy to `/mnt/c/Users/sheke/OneDrive/Desktop/`. Opening it from WSL
  via `powershell.exe` requires WSL interop — check
  `/proc/sys/fs/binfmt_misc/WSLInterop`; if missing, hand over the `C:\...` path instead.
