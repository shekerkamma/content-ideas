# Hybrid-export traps

**Load this when:** building or debugging the hybrid-editable path
(`render_hybrid.mjs` → `build_editable_pptx.py`), or whenever the PPTX disagrees
with the PNG.

All three traps below corrupt the PowerPoint while the PNG render stays perfect —
the PNG is a real browser screenshot, so it can never reveal a capture bug. Two
of them are also invisible to OfficeCLI, because `issues: 0` only means no shape
crosses a slide edge.

| Trap | Symptom in PPTX | Caught by |
|---|---|---|
| Inline-only text dropped | Whole columns/labels missing | `check_export_coverage.mjs` |
| Inline tag as `display:block` | Text printed twice, overlapping | per-slide Office render |
| Tight bbox re-wrap | Last glyph pushed to a second line | per-slide Office render |
| Preformatted text collapsed | Code/file tree becomes one wrapped paragraph | per-slide Office render |
| CSS line-height passed as a ratio | Long blocks ~20% too tall, overflow their box | per-slide Office render |
| Wrong render stage width | Only the top-left of every slide captured | contact sheet |

## 1. Text that lives only inside inline tags gets DROPPED

```html
<div data-object-type="textbox"><b>Regulatory Compulsion</b><br><span>Is buying forced…</span></div>
```

This div has **no direct text node** — every character sits inside `<b>` and
`<span>`. A capture predicate of *"element must have a direct text node"* skips
the div, then skips `<b>` and `<span>` for having `display:inline`. The string is
lost from the export entirely.

The correct predicate is a **text leaf block**: the element holds text *and* has
no block-level child that itself holds text.

```js
if (!el.textContent.trim()) continue;
const hasBlockKid = [...el.children].some(c => {
  const d = getComputedStyle(c).display;
  return d !== "inline" && d !== "none" && c.textContent.trim();
});
if (hasBlockKid) continue;
```

Fixed in `render_hybrid.mjs`. **Do not reintroduce a `hasDirectText` gate.**
A live instance of this dropped 149 strings across 36 of 37 slides — entire table
columns — and shipped, because the PNG looked right and OfficeCLI said `0 issues`.

## 2. An inline tag styled `display:block` gets captured TWICE

```css
.bcap b { display: block }      /* <-- the bug */
```

The `<b>` now qualifies as its own box, *and* its text is still walked into the
parent's runs (because `walkLines` treats `B`/`SPAN`/`EM`/`I`/`A`/`SMALL`/`MARK`
as inline). PowerPoint then draws the string twice, overlapping itself.

Use `<br>` with a genuinely inline child instead — which is what well-formed
source decks already do:

```html
<div class="bcap"><b>FY27 gross margin</b><br>first silicon, low volume</div>
```

Audit any stylesheet you author or inherit:

```bash
grep -nE '^\s*\.[a-z0-9_. -]*\b(span|b|em|i|a|small|mark)\s*\{[^}]*display:\s*block' <css>
```

## 3. Tight bounding boxes re-wrap under PowerPoint's font metrics

An element sized to its own glyph run in HTML — a `%` inside a bar label, a unit
suffix — can lose its last character to a second line in PPTX, because the native
text box is rebuilt from the captured bbox and PowerPoint's metrics differ
slightly from the browser's.

Give such elements a full-width block box so the captured bbox has slack:

```css
.pct { display:block; width:100%; text-align:center }
```

## Verification order

1. `node scripts/check_export_coverage.mjs --deck <html> --pos build/pos` — must exit 0.
2. `node scripts/check_layout_overflow.mjs --deck <html> --min 20` — triage the report.
3. Build the PPTX, run `officecli_qa.py`.
4. **Open per-slide Office renders** for the densest slides:
   `officecli view <pptx> screenshot --page N -o <png>`.
   The 4-up `--grid` contact sheet is too low-resolution to judge legibility.

Steps 1 and 4 are the only ones that catch traps 1–3. Neither the PNG contact
sheet nor `issues: 0` can.

## 4. Preformatted text collapses into prose

A `<pre>` file tree, code block or ASCII diagram carries its meaning in **newlines
and runs of spaces**. Prose capture destroys both: it collapses `\s+` to a single
space and only breaks a line on `<br>`. The PNG stays perfect; the PPTX shows one
long wrapped paragraph.

`render_hybrid.mjs` now detects `white-space: pre*`, splits text on `\n`, and keeps
every space. It records `pre: true`, and `build_editable_pptx.py` sets
`word_wrap = False` on those boxes — wrapping a tree re-flows it even when the
lines were captured correctly.

If you author CSS for a code block, keep `white-space: pre` on the element that
holds the text; the detection reads the computed style of the captured box.

## 5. CSS line-height is not PowerPoint line spacing

CSS `line-height: 1.7` means **1.7 × font size**. python-pptx's float
`line_spacing = 1.7` means **1.7 × single line spacing**, and "single" is roughly
1.2 × font size. Passing the CSS ratio straight through over-spaces every
paragraph by about 20%, which quietly pushes long blocks out of their box.

Capture the absolute line box (`lhPx`) and set exact points instead:

```python
p.line_spacing = Pt(round(b["lhPx"] * pt_per_px, 2))
```

## 6. The render stage must match the deck

`render.mjs` and `render_hybrid.mjs` auto-detect the `#stage` width and derive
`deviceScaleFactor` so the export is always 2560×1440. Before that, a hardcoded
1280 viewport rendering a 1920 deck captured only the top-left **66.7%** of every
slide — correct file count, correct 2560×1440 dimensions, and a third of the
content silently gone. Override with `--stage <cssWidth>` only if detection fails.

## A note on reading the QA render

OfficeCLI's HTML preview renders the deck as HTML, so **leading whitespace
collapses** there even when it is correct in the file. Before calling an
indentation defect real, check the XML:

```python
for para in shape.text_frame.paragraphs:
    print(repr("".join(r.text for r in para.runs)))
```
If the spaces are in the runs, the PPTX is faithful and the preview is lossy.
