import { P, C, K, SERIF, addSlide, tx, rect, roundRect, ellipse, sh,
         PresentationFile, OUT, textH } from
  '/home/sheke/.claude/skills/vault-presales-pptx-pipeline/assets/deck-kit.mjs';
import { PX, T, header, headerDark, card, cardH, stack, kpi, table, chain, rail,
         divider, barsNative, SRC } from
  '/home/sheke/content-ideas/runs/2026-08-22-design-video-brief/kit-spec.mjs';
import * as D from './data.mjs';

const CY=K.cyan, TL=K.teal, GR=K.green, PB=K.paleBlue, SL=K.slate, GY=K.gray;
const money = (v) => `₹${v.toLocaleString('en-IN',{maximumFractionDigits:v<10?2:0})}`;

// ---- local composites -------------------------------------------------------
// Six-year column trajectory with direct labels. Native shapes, no chart object.
function trajectory(x, y, w, h, vals, labels, opts={}) {
  const { color=CY, dim='#CBD5E1', fmt=(v)=>String(v), hot=vals.length-1, baseline=false } = opts;
  y += 34; h -= 34;   // reserve headroom for the value label above the tallest bar
  const n = vals.length, gap = 18, bw = (w - (n-1)*gap)/n;
  const lo = Math.min(0, ...vals), hi = Math.max(...vals);
  const span = (hi-lo) || 1;
  const zeroY = y + h - ((0-lo)/span)*h;
  const e = [];
  if (baseline) e.push(rect(x, zeroY, w, 1, K.line));
  vals.forEach((v,i)=>{
    const bx = x + i*(bw+gap);
    const bh = Math.max(3, Math.abs(v)/span*h);
    const by = v >= 0 ? zeroY - bh : zeroY;
    e.push(rect(bx, by, bw, bh, i===hot ? color : dim));
    e.push(tx(fmt(v), bx-6, (v>=0? by-30 : by+bh+6), bw+12, 26,
      { size:T.cardH, bold:true, color: i===hot ? (color===CY?CYT:(color===TL?TLT:color)) : SL, align:'center' }));
    e.push(tx(labels[i], bx-6, y+h+34, bw+12, 22,
      { size:T.kicker, bold:true, color:GY, align:'center' }));
  });
  return e;
}

// Stacked 100% proportion strip with direct labels beneath.
function mixBar(x, y, w, h, rows) {
  const total = rows.reduce((s,r)=>s+r[1],0);
  const e=[]; let cx=x;
  const palette=[CY,TL,PB,'#B9C7D6'];
  rows.forEach((r,i)=>{
    const seg = (r[1]/total)*w;
    e.push(rect(cx, y, seg, h, palette[i%palette.length]));
    cx += seg;
  });
  let ly=y+h+22;
  rows.forEach((r,i)=>{
    e.push(rect(x, ly+4, 12, 12, palette[i%palette.length]));
    e.push(tx(r[0], x+22, ly, 260, 22, { size:T.body, bold:true, color:SL }));
    e.push(tx(`${money(r[1])} Cr`, x+292, ly, 120, 22, { size:T.body, color:GY, align:'right' }));
    e.push(tx(`${r[2].toFixed(1)}%`, x+420, ly, 70, 22, { size:T.body, bold:true, color:CYT, align:'right' }));
    ly += 28;
  });
  return e;
}

// Multi-series margin ramp as labelled endpoints — clearer than four crossing lines.
function rampRows(x,y,w,series,opts={}){
  const { rowH=54 } = opts;
  const e=[]; const labelW=200, trackW=w-labelW-150;
  Object.entries(series).forEach(([name,vals],i)=>{
    const ry=y+i*rowH;
    const a=vals[0], b=vals[vals.length-1];
    e.push(tx(name, x, ry+10, labelW-16, 24, { size:T.body, bold:true, color:SL }));
    e.push(rect(x+labelW, ry+20, trackW, 4, '#E8EDF2'));
    const ax = x+labelW + (a/100)*trackW, bx = x+labelW + (b/100)*trackW;
    e.push(rect(ax, ry+20, Math.max(2,bx-ax), 4, CY));
    e.push(ellipse(ax-7, ry+15, 14, 14, K.white, PB, 2));
    e.push(ellipse(bx-7, ry+15, 14, 14, CY, CY, 2));
    e.push(tx(`${a}%`, ax-40, ry-6, 36, 20, { size:T.kicker, bold:true, color:GY, align:'right' }));
    e.push(tx(`${b}%`, bx+12, ry+12, 120, 22, { size:T.cardH, bold:true, color:CYT }));
  });
  return e;
}


// ---- measured vertical flow --------------------------------------------------
// Every lower-half block is PLACED BY MEASUREMENT, never by a hand-typed y.
// SAFE_BOTTOM keeps content clear of the footer rule at y=681.
const SAFE_BOTTOM = 664;
const VIOLATIONS = [];
function flow(startY, tag, limit = SAFE_BOTTOM) {
  let y = startY;
  const api = {
    get y(){ return y; },
    skip(px){ y += px; return []; },
    at(v){ y = v; return []; },
    // specs: [x, w, title, body, accent?, fill?] — all cards share the tallest height
    cards(specs, gap = 14) {
      const h = Math.max(...specs.map(s => CARDH(s[3], s[1], s[2])));
      const el = specs.flatMap(s => CARD(s[0], y, s[1], h, s[2], s[3], s[4], s[5]));
      y += h + gap;
      if (y - gap > limit) VIOLATIONS.push(`${tag}: cards bottom ${Math.round(y-gap)} > ${limit}`);
      return el;
    },
    tbl(x, w, cols, rows, opts = {}) {
      const headH = opts.headH ?? 38;
      const el = TBL(x, y, w, cols, rows, { ...opts, headH });
      y += TBLH(cols, rows, headH) + 16;
      if (y - 16 > limit) VIOLATIONS.push(`${tag}: table bottom ${Math.round(y-16)} > ${limit}`);
      return el;
    },
    src(text, x = 48, w = 1184) {
      const hh = TH(text, w, T.foot);
      const el = [tx(text, x, y, w, hh, { size: T.foot, italic: true, color: GY })];
      y += hh + 8;
      if (y - 8 > limit) VIOLATIONS.push(`${tag}: source bottom ${Math.round(y)} > ${limit}`);
      return el;
    },
    note(text, x = 48, w = 1184) {
      const hh = TH(text, w, T.body);
      const el = [tx(text, x, y, w, hh, { size: T.body, color: GY })];
      y += hh + 14;
      if (y - 42 > limit) VIOLATIONS.push(`${tag}: note bottom ${Math.round(y)} > ${limit}`);
      return el;
    },
  };
  return api;
}


// Text-safe accents. #00B4D8 cyan is 2.46:1 on white — compliant as a FILL or RULE,
// non-compliant as TYPE. These darker tones carry the same accent role for glyphs.
const CYT = '#00758F';   // 5.33:1 on white · 5.16:1 on surface
const PBT = '#3D6E96';   // 5.02:1 on white
const TLT = '#0A6E70';   // 6.04:1 on white — safe at any size

// Local header: identical geometry to the kit, accessible kicker colour.
function hdr(kicker, title, subtitle, page, dark = false) {
  if (String(title).length > 48)
    VIOLATIONS.push(`p${page}: title ${String(title).length} chars > 48 (wraps; drops below the 24pt floor)`);
  const base = header(kicker, title, subtitle, page, dark);
  if (!dark) base[0] = tx(String(kicker).toUpperCase(), 48, 24, 800, 22,
                          { size: T.kicker, bold: true, color: CYT });
  // Kit sizes the subtitle box at a flat 30px; the gate needs its real wrapped height.
  // The band between the subtitle and the rule at y=146 holds ONE line, so a subtitle
  // that wraps prints its second line straight through the rule. Guard it.
  if (subtitle) {
    if (String(subtitle).length > 105)
      VIOLATIONS.push(`p${page}: subtitle ${String(subtitle).length} chars > 105 (wraps into the rule)`);
    base[2] = tx(subtitle, 48, 106, 1140, TH(subtitle, 1140, T.sub),
                 { size: T.sub, color: dark ? '#A9BACD' : GY });
  }
  return base;
}


// ---- preview-compatible text metrics ----------------------------------------
// preview_pptx.py (the delivery gate) wraps at  chars = w_in / (pt * 0.0085)  and
// stacks lines at 1.18x. In pixel terms that is  chars = w_px / (0.612 * size_px).
// deck-kit's textH assumes a 0.50 char-width, which under-counts lines and yields
// boxes ~1.5x too short. Every box below is sized to the gate's metric instead.
function TH(text, w, size, pad = 10) {
  const maxc = Math.max(4, Math.floor((w / (0.612 * size)) * 0.94));
  const lines = String(text).split('\n')
    .reduce((n, p) => n + Math.max(1, Math.ceil(p.length / maxc)), 0);
  return Math.ceil(lines * size * 1.18) + pad;
}
// Card sized to the gate. Same geometry grammar as the kit's card().
function CARD(x, y, w, h, title, body, accent = CY, fill = K.white) {
  const tH = TH(title, w - 44, T.cardH);
  const bH = TH(body,  w - 48, T.body);
  const H  = (h === 'auto' || h == null) ? (18 + tH + 10 + bH + 18) : h;
  return [
    roundRect(x, y, w, H, fill, K.line, 1),
    rect(x, y, 6, H, accent),
    tx(title, x + 24, y + 18, w - 44, tH, { size: T.cardH, bold: true, color: SL }),
    tx(body,  x + 24, y + 18 + tH + 10, w - 48, bH, { size: T.body, color: GY }),
  ];
}
const CARDH = (body, w, title = 'X') =>
  18 + TH(title, w - 44, T.cardH) + 10 + TH(body, w - 48, T.body) + 18;

// KPI sized to the gate: label and note boxes grow to their real wrapped height.
function KPI(x, y, w, num, label, note, color = CY) {
  const lH = TH(label.toUpperCase(), w - 24, T.kpiLab);
  const nH = TH(note, w - 28, T.kpiNote);
  const H  = 24 + 58 + 10 + lH + 6 + nH + 18;
  // A 38.25pt numeral fits ~6 chars in a 190px tile; step down rather than wrap.
  const fits = Math.max(4, Math.floor((w - 16) / (0.612 * T.kpiNum)));
  const nSize = String(num).length <= fits ? T.kpiNum
              : Math.max(PX(20), Math.floor(T.kpiNum * fits / String(num).length));
  return [
    roundRect(x, y, w, H, K.surface, K.line, 1),
    tx(num, x, y + 24, w, 58, { size: nSize, face: SERIF, bold: true, color, align: 'center' }),
    tx(label.toUpperCase(), x + 12, y + 92, w - 24, lH, { size: T.kpiLab, bold: true, color: SL, align: 'center' }),
    tx(note, x + 14, y + 92 + lH + 6, w - 28, nH, { size: T.kpiNote, color: GY, align: 'center' }),
  ];
}
const KPIH = (label, note, w) =>
  24 + 58 + 10 + TH(label.toUpperCase(), w - 24, T.kpiLab) + 6 + TH(note, w - 28, T.kpiNote) + 18;

// Table whose row height is derived from the tallest wrapped cell in that row.
function TBL(x, y, w, colspec, rows, opts = {}) {
  const { headH = 38, highlight = -1 } = opts;
  const e = [rect(x, y, w, headH, K.midnight)];
  let hx = x;
  colspec.forEach((c) => {
    e.push(tx(c.t.toUpperCase(), hx + 14, y + 11, c.w - 20, headH - 16,
      { size: T.thead, bold: true, color: K.white, align: c.a || 'left' }));
    hx += c.w;
  });
  let ry = y + headH;
  rows.forEach((r, ri) => {
    const rowH = Math.max(32, ...r.map((cell, ci) => TH(String(cell), colspec[ci].w - 22, T.tcell, 2) + 14));
    const hot = ri === highlight;
    e.push(rect(x, ry, w, rowH, hot ? K.softCyan : (ri % 2 ? K.surface : K.white), K.line, 1));
    if (hot) e.push(rect(x, ry, 5, rowH, CY));
    let rx = x;
    r.forEach((cell, ci) => {
      const col = colspec[ci];
      e.push(tx(String(cell), rx + 14, ry + 7, col.w - 22, rowH - 12,
        { size: T.tcell, bold: hot || ci === 0, color: hot ? SL : (ci === 0 ? SL : GY), align: col.a || 'left' }));
      rx += col.w;
    });
    ry += rowH;
  });
  return e;
}
const TBLH = (colspec, rows, headH = 38) => headH + rows.reduce((s, r) =>
  s + Math.max(32, ...r.map((c, ci) => TH(String(c), colspec[ci].w - 22, T.tcell, 2) + 14)), 0);

export { CY, TL, GR, PB, SL, GY, money, trajectory, mixBar, rampRows,
         SAFE_BOTTOM, VIOLATIONS, flow, CYT, PBT, TLT, hdr,
         TH, CARD, CARDH, KPI, KPIH, TBL, TBLH };
export { P, C, K, SERIF, addSlide, tx, rect, roundRect, ellipse, sh,
         PresentationFile, OUT, textH, PX, T, header, headerDark, card, cardH,
         stack, kpi, table, chain, rail, divider, barsNative, SRC };
