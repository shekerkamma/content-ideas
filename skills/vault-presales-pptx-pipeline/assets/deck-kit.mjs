// deck-kit.mjs — Client-Ready PPTX Design System kit for artifact-tool presentation JSX
//
// Import-and-go helper library. Proven on:
//   Deepgrid IM rebuild (18 slides, 867 shapes, 547 text boxes, 0 pictures, OfficeCLI passed)
//
// USAGE:  DECK_RUN=<dir> DECK_NAME=<slug> DECK_FOOTER='...' node build.mjs
//   import everything below, then compose slides with addSlide([...]).
//
// PREREQ (WSL): the Linux port of @oai/artifact-tool at ~/.local/artifact-tool-linux
//   see references/artifact-tool-presentation-jsx.md §1
//
// PRIMITIVES
//   tx / sh / rect / roundRect / ellipse ...... raw
//   header / headerDark / footer ............... slide chrome (L-series compliant)
//   card(x,y,w,'auto',title,body,accent) ....... CONTENT-FITTING card — pass 'auto', never a number
//   kpi(x,y,w,num,label,note,color) ............ KPI tile
//   table(x,y,w,cols,rows,{highlight}) ......... flat table, one highlighted row
//   barsV(x,y,w,h,series,{max,barW}) ........... vertical shape-chart, direct labels
//   barsH(x,y,w,rows,{max}) .................... ranked horizontal bars
//   proportion(x,y,w,h,segs) ................... to-scale share bar  <- use for any "X is N% of Y"
//   rail(x,y,w,nodes,{dark}) ................... milestone timeline
//   chain(x,y,w,nodes,{nodeW,nodeH}) ........... L04 process chain w/ arrows
//
// HARD RULES
//   1. addSlide() calls setViewportSize(1280,720) -> exactly 13.333 x 7.5in. Never change.
//   2. card heights are 'auto'. A fixed height = dead space = the deck reads as junk.
//   3. Charts are SHAPES with direct labels (design system). Do not reach for C.chart.
//   4. On dark slides pass {dark:true} to rail() or labels fail the 4.5:1 contrast rule.
//   5. flowChartTerminator renders as a bare rule — use flowChartAlternateProcess instead.
//   6. Fonts: DM Serif Display/Questrial are absent on Linux. SERIF/SANS below are the
//      design system's documented fallbacks, set deliberately. Local renders show sans
//      titles; Windows PowerPoint resolves Georgia. That is a render artifact, not a defect.

import { writeFile, mkdir } from 'node:fs/promises';

const AT = 'file:///C:/Users/sheke/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist';
const { Presentation, PresentationFile, layers: composeLayers } = await import(`${AT}/artifact_tool.mjs`);
const { textStyle, stroke } = await import(`${AT}/presentation-jsx/index.mjs`);
const { jsx, jsxs } = await import(`${AT}/presentation-jsx/jsx-runtime.mjs`);

// ── configure per deck ───────────────────────────────────────────────
const RUN = process.env.DECK_RUN || '.';
const OUT = `${RUN}/${process.env.DECK_NAME || 'deck'}-draft.pptx`;
const PREVIEW_DIR = `${RUN}/qa/renders`;
const MONTAGE = `${RUN}/qa/montage.png`;
await mkdir(PREVIEW_DIR, { recursive: true });

const P = Presentation.create();
const C = P.compose;

// ── Client-Ready PPTX Design System tokens ────────────────────────────────
const K = {
  midnight: '#0A1628', slate: '#1E293B', white: '#FFFFFF',
  cyan: '#00B4D8', teal: '#0A9396', paleBlue: '#8DB4D4',
  green: '#12855B', gray: '#6B7280', surface: '#F8FAFC',
  cool: '#F4F8FE', line: '#E2E8F0', softCyan: '#E8F8FC', softTeal: '#E8F6F5',
  amber: '#B45309', red: '#B42318',
};
// Fonts: DM Serif Display / Questrial unavailable → documented fallbacks,
// applied intentionally (Georgia for display, Arial for body).
const SERIF = 'Georgia', SANS = 'Arial';

const Text = ({ children = '', ...props }) => C.text(String(children), props);
const Shape = (props) => C.shape(props);
const Layers = ({ children = [], ...props }) => composeLayers(props, Array.isArray(children) ? children : [children]);

function style({ size = 14, face = SANS, color = K.slate, bold = false, italic = false, align = 'left', anchor = 'top', inset = 0 }) {
  return textStyle(`font: ${italic ? 'italic ' : ''}${bold ? 'bold ' : ''}${size}px ${face}; color: ${color}; align: ${align}; anchor: ${anchor}; inset: ${inset}px; autofit: shrink`);
}
const tx = (text, x, y, w, h, o = {}) => jsx(Text, {
  width: C.fixed(w), height: C.fixed(h), position: { left: x, top: y }, style: style(o), children: text,
});
const sh = (geometry, x, y, w, h, fill, lineColor = 'none', lineWidth = 0) => jsx(Shape, {
  geometry, width: C.fixed(w), height: C.fixed(h), fill,
  line: lineColor === 'none' ? stroke('0px none') : stroke(`${lineWidth}px solid ${lineColor}`),
  position: { left: x, top: y },
});
const rect = (x, y, w, h, f, lc = 'none', lw = 0) => sh('rect', x, y, w, h, f, lc, lw);
const roundRect = (x, y, w, h, f, lc = 'none', lw = 0) => sh('roundRect', x, y, w, h, f, lc, lw);
const ellipse = (x, y, w, h, f, lc = 'none', lw = 0) => sh('ellipse', x, y, w, h, f, lc, lw);

const FOOT = process.env.DECK_FOOTER || 'CLIENT  ·  INITIATIVE  ·  DATE';
function footer(page, dark = false) {
  const color = dark ? '#8FA2B7' : K.gray;
  const line = dark ? '#23364C' : K.line;
  return [
    rect(48, 683, 1184, 1, line),
    tx(FOOT, 48, 690, 760, 16, { size: 9, bold: true, color }),
    tx(String(page).padStart(2, '0'), 1175, 689, 57, 16, { size: 9, bold: true, color, align: 'right' }),
  ];
}
function header(kicker, title, subtitle, page) {
  return [
    tx(kicker.toUpperCase(), 48, 26, 800, 18, { size: 10, bold: true, color: K.cyan }),
    tx(title, 48, 50, 1160, 46, { size: 30, face: SERIF, bold: true, color: K.slate }),
    subtitle ? tx(subtitle, 50, 102, 1135, 30, { size: 14, color: K.gray }) : rect(0, 0, 1, 1, K.white),
    rect(48, 142, 1184, 2, K.slate),
    ...footer(page),
  ];
}
function headerDark(kicker, title, subtitle, page) {
  return [
    tx(kicker.toUpperCase(), 48, 26, 800, 18, { size: 10, bold: true, color: K.cyan }),
    tx(title, 48, 50, 1160, 46, { size: 30, face: SERIF, bold: true, color: K.white }),
    subtitle ? tx(subtitle, 50, 102, 1135, 30, { size: 14, color: '#A9BACD' }) : rect(0, 0, 1, 1, K.midnight),
    rect(48, 142, 1184, 2, K.cyan),
    ...footer(page, true),
  ];
}
function addSlide(children, { background = K.white, notes = '' } = {}) {
  const s = P.slides.add();
  s.setViewportSize(1280, 720);
  s.compose(jsxs(Layers, { width: C.fixed(1280), height: C.fixed(720), children: [rect(0, 0, 1280, 720, background), ...children] }));
  s.speakerNotes.text = notes;
  return s;
}
// components
// measure: how tall does `body` need to be at this width/size?
function textH(body, w, size = 13, lh = 1.45) {
  const cpl = Math.max(8, Math.floor(w / (size * 0.50)));   // chars per line
  const lines = String(body).split('\n').reduce((n, para) =>
    n + Math.max(1, Math.ceil(para.length / cpl)), 0);
  const paras = String(body).split('\n').length - 1;
  return Math.ceil(lines * size * lh + paras * 8);
}
// card that FITS ITS CONTENT. Pass h = 'auto' (default) or a number to force.
function card(x, y, w, h, title, body, accent = K.cyan, fill = K.white) {
  const S = 13;
  const bodyH = textH(body, w - 40, S);
  const auto = 16 + 22 + 10 + bodyH + 18;          // padTop + title + gap + body + padBottom
  const H = (h === 'auto' || h == null) ? auto : Math.max(h, auto);
  return [
    roundRect(x, y, w, H, fill, K.line, 1),
    rect(x, y, 5, H, accent),
    tx(title, x + 20, y + 16, w - 36, 22, { size: 15, bold: true, color: K.slate }),
    tx(body, x + 20, y + 48, w - 40, bodyH + 6, { size: S, color: K.gray }),
  ];
}
function kpi(x, y, w, num, label, note, color = K.cyan) {
  return [
    roundRect(x, y, w, 150, K.surface, K.line, 1),
    tx(num, x, y + 22, w, 52, { size: 40, face: SERIF, bold: true, color, align: 'center' }),
    tx(label.toUpperCase(), x + 12, y + 82, w - 24, 20, { size: 10, bold: true, color: K.slate, align: 'center' }),
    tx(note, x + 12, y + 104, w - 24, 36, { size: 9, color: K.gray, align: 'center' }),
  ];
}
// simple table
function table(x, y, w, cols, rows, opts = {}) {
  const { rowH = 30, headH = 32, highlight = -1, colColor = null } = opts;
  const e = [rect(x, y, w, headH, K.midnight)];
  let cx = x;
  cols.forEach((c, i) => {
    e.push(tx(c.t.toUpperCase(), cx + 10, y + 9, c.w - 14, 18, { size: 9, bold: true, color: K.white, align: c.a || 'left' }));
    cx += c.w;
  });
  rows.forEach((r, ri) => {
    const ry = y + headH + ri * rowH;
    const hot = ri === highlight;
    e.push(rect(x, ry, w, rowH, hot ? K.softCyan : (ri % 2 ? K.surface : K.white), K.line, 1));
    if (hot) e.push(rect(x, ry, 4, rowH, K.cyan));
    let rx = x;
    r.forEach((cell, ci) => {
      const col = cols[ci];
      const c = colColor ? colColor(ri, ci, hot) : (hot ? K.slate : (ci === 0 ? K.slate : K.gray));
      e.push(tx(String(cell), rx + 10, ry + 8, col.w - 14, rowH - 12, { size: 11, bold: hot || ci === 0, color: c, align: col.a || 'left' }));
      rx += col.w;
    });
  });
  return e;
}

// ── VISUAL PRIMITIVES (design system: flat 2D, direct labels, no legends) ──

// vertical shape-bars with direct labels (the validated reference pattern)
function barsV(x, y, w, h, series, opts = {}) {
  const { max = Math.max(...series.map(s => s[1])), barW = 92, gap = null, note = null } = opts;
  const n = series.length;
  const step = gap ?? (w / n);
  const e = [rect(x, y + h, w, 1, K.line)];
  series.forEach(([label, val, color, sub], i) => {
    const bh = Math.max(6, (val / max) * h);
    const bx = x + i * step + (step - barW) / 2;
    e.push(roundRect(bx, y + h - bh, barW, bh, color, color, 1));
    e.push(tx(sub ?? String(val), bx - 20, y + h - bh - 34, barW + 40, 28,
      { size: 18, face: SERIF, bold: true, color: K.slate, align: 'center' }));
    e.push(tx(label, bx - 24, y + h + 10, barW + 48, 18,
      { size: 10, bold: true, color: K.gray, align: 'center' }));
  });
  if (note) e.push(tx(note, x, y + h + 34, w, 18, { size: 11, italic: true, color: K.gray }));
  return e;
}

// horizontal shape-bars — for rankings/scorecards
function barsH(x, y, w, rows, opts = {}) {
  const { max = 5, rowH = 46, labelW = 200, valW = 70 } = opts;
  const trackX = x + labelW, trackW = w - labelW - valW;
  const e = [];
  rows.forEach(([label, val, color, dark], i) => {
    const ry = y + i * rowH;
    e.push(tx(label, x, ry + 8, labelW - 12, 22, { size: 14, bold: true, color: dark ? K.white : K.slate }));
    e.push(rect(trackX, ry + 10, trackW, 18, dark ? '#1B2E44' : K.surface));
    e.push(rect(trackX, ry + 10, Math.max(4, (val / max) * trackW), 18, color));
    e.push(tx(val.toFixed(2), trackX + trackW + 8, ry + 6, valW - 10, 24,
      { size: 16, face: SERIF, bold: true, color, align: 'left' }));
  });
  return e;
}

// proportion bar — one whole, one highlighted segment
function proportion(x, y, w, h, segs) {
  const total = segs.reduce((a, s) => a + s[1], 0);
  let cx = x; const e = [];
  segs.forEach(([label, val, color, txtColor]) => {
    const sw = (val / total) * w;
    e.push(rect(cx, y, sw, h, color));
    if (sw > 70) {
      e.push(tx(label, cx + 10, y + h / 2 - 16, sw - 20, 22,
        { size: 13, bold: true, color: txtColor || K.white }));
    }
    cx += sw;
  });
  e.push(rect(x, y, w, h, 'none', K.line, 1));
  return e;
}

// milestone rail — L11 timeline (mirrors the source deck's proof-of-execution strip)
function rail(x, y, w, nodes, opts = {}) {
  const { dark = false } = opts;
  const titleC = dark ? K.white : K.slate;
  const subC   = dark ? '#8FA2B7' : K.gray;
  const chipBg = dark ? '#12243A' : K.surface;
  const step = w / nodes.length;
  const e = [rect(x + 20, y + 46, w - 40, 2, dark ? '#23364C' : K.line)];
  nodes.forEach(([chip, title, sub, color, filled], i) => {
    const cx = x + i * step;
    e.push(rect(cx, y, step - 16, 26, filled ? color : chipBg, color, 1));
    e.push(tx(chip.toUpperCase(), cx, y + 6, step - 16, 16,
      { size: 9, bold: true, color: filled ? K.white : color, align: 'center' }));
    e.push(ellipse(cx + (step - 16) / 2 - 7, y + 40, 14, 14, filled ? color : (dark ? K.midnight : K.white), color, 2));
    e.push(tx(title, cx - 6, y + 66, step - 4, 22, { size: 13, bold: true, color: titleC, align: 'center' }));
    e.push(tx(sub, cx - 6, y + 88, step - 4, 34, { size: 10, color: subC, align: 'center' }));
  });
  return e;
}

// process chain — L04, flowChart nodes + arrows
function chain(x, y, w, nodes, opts = {}) {
  const { nodeW = 196, nodeH = 96, geom = 'flowChartProcess' } = opts;
  const gap = (w - nodes.length * nodeW) / (nodes.length - 1);
  const e = [];
  nodes.forEach(([title, body, color, g], i) => {
    const nx = x + i * (nodeW + gap);
    e.push(sh(g || geom, nx, y, nodeW, nodeH, K.white, color, 2));
    e.push(rect(nx, y, nodeW, 4, color));
    e.push(tx(title, nx + 12, y + 16, nodeW - 24, 22, { size: 14, bold: true, color: K.slate, align: 'center' }));
    e.push(tx(body, nx + 12, y + 42, nodeW - 24, 46, { size: 11, color: K.gray, align: 'center' }));
    if (i < nodes.length - 1) {
      e.push(sh('rightArrow', nx + nodeW + gap / 2 - 15, y + nodeH / 2 - 10, 30, 20, K.cyan, K.cyan, 1));
    }
  });
  return e;
}

const SRC = (t, x = 48, y = 660) => tx(t, x, y, 1000, 14, { size: 8, color: K.gray, italic: true });


