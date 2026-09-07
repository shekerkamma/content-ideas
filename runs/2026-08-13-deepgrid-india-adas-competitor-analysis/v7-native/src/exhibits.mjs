// exhibits.mjs — twelve exhibit families, one per method.
//
// The previous deck rendered every OUTPUT INCLUDES as the same stack of bordered
// text boxes. The guide's whole mechanism is that each method yields a DIFFERENT
// artifact — a Fact Base table, a Driver Tree, a scored Register, a Size Estimate
// by two methods. The schema is the exhibit. These draw them.
//
// Geometry encodes meaning in every one: bar length is share, cell colour is
// rating, rung width is confidence, step height is cost. Nothing here is a box
// that merely contains a sentence.

export function makeExhibits({ jsx, C, Text, Shape, textStyle, stroke, V, RAMP, T, SERIF, textH }) {
  const st = (o) => textStyle(`font: ${o.bold ? 'bold ' : ''}${o.size}px ${o.face || 'Arial'}; `
    + `color: ${o.color}; align: ${o.align || 'left'}; anchor: ${o.anchor || 'top'}; inset: 0px; autofit: shrink`);
  const tx = (t, x, y, w, h, o) => jsx(Text, {
    width: C.fixed(Math.max(4, w)), height: C.fixed(Math.max(6, h)),
    position: { left: x, top: y }, style: st(o),
    children: o.caps ? String(t).toUpperCase() : t });
  const box = (x, y, w, h, fill, lc = 'none', lw = 0) => jsx(Shape, {
    geometry: 'rect', width: C.fixed(Math.max(1, w)), height: C.fixed(Math.max(1, h)), fill,
    line: lc === 'none' ? stroke('0px none') : stroke(`${lw}px solid ${lc}`),
    position: { left: x, top: y } });
  const dot = (x, y, d, fill) => jsx(Shape, {
    geometry: 'ellipse', width: C.fixed(d), height: C.fixed(d), fill,
    line: stroke('0px none'), position: { left: x, top: y } });
  const arrow = (x, y, w, h, fill) => jsx(Shape, {
    geometry: 'rightArrow', width: C.fixed(w), height: C.fixed(h), fill,
    line: stroke('0px none'), position: { left: x, top: y } });

  const G = (dark) => ({
    ramp: dark ? RAMP.dark : RAMP.light,
    card: dark ? V.cardDark : V.cardLight,
    line: dark ? V.lineDark : V.line,
    ink: dark ? '#C9D6E2' : V.ink,
    head: dark ? V.white : V.ink,
    muted: dark ? V.mutedDark : V.muted,
  });
  const cap = (s, n) => (String(s).length > n ? String(s).slice(0, n - 1).trimEnd() + '…' : String(s));

  // ── M01 · EVIDENCE LADDER — four rungs, width encodes confidence ────────
  function ladder(x, y, w, rungs, dark, size, grow = 0) {
    const g = G(dark), out = [], rh = 46 + grow, gap = 7;
    rungs.forEach((r, i) => {
      const yy = y + i * (rh + gap);
      const share = Math.max(0.24, r.confidence);
      out.push(box(x, yy, w, rh, g.card, g.line, 1));
      out.push(box(x, yy, Math.max(6, w * share), 3, r.colour));   // confidence bar, to scale
      out.push(box(x, yy, 3, rh, r.colour));
      out.push(tx(cap(r.label, 40), x + 12, yy + 9, w * 0.30, T.label + 3,
        { size: T.label, bold: true, color: r.colour, caps: true }));
      out.push(tx(cap(r.text, 150), x + 12 + w * 0.31, yy + 8, w * 0.50, rh - 14,
        { size, color: g.ink }));
      out.push(tx(r.status, x + w - w * 0.16 - 12, yy + 9, w * 0.16, T.label + 3,
        { size: T.label, bold: true, color: r.colour, align: 'right', caps: true }));
    });
    return { out, h: rungs.length * (rh + gap) - gap };
  }

  // ── M02 · THREAT HEATMAP — arenas × dimensions, colour IS the rating ────
  const RATE = { HIGHEST: 1, HIGH: 0.82, 'MEDIUM-HIGH': 0.66, MEDIUM: 0.5,
                 'LOW-MEDIUM': 0.34, LOW: 0.2, NONE: 0.08 };
  function heatmap(x, y, w, cols, rows, dark, size, grow = 0) {
    const g = G(dark), out = [], labW = w * 0.20, cw = (w - labW) / cols.length;
    const hh = 26, rh = 44 + grow;
    out.push(box(x + labW, y, w - labW, hh, dark ? '#0C1D2E' : '#E8F0F3'));
    cols.forEach((c, i) => out.push(tx(cap(c, 22), x + labW + i * cw + 10, y + 8, cw - 16, 13,
      { size: T.label, bold: true, color: g.muted, caps: true })));
    rows.forEach((r, ri) => {
      const yy = y + hh + ri * rh;
      out.push(box(x, yy, labW, rh, g.card, g.line, 1));
      out.push(tx(cap(r.label, 26), x + 10, yy + 12, labW - 16, rh - 18,
        { size: T.label, bold: true, color: g.head, caps: true }));
      r.cells.forEach((cell, ci) => {
        const lvl = RATE[(cell.rating || '').toUpperCase()] ?? 0.4;
        const col = lvl >= 0.8 ? g.ramp.red : lvl >= 0.6 ? g.ramp.amber
                  : lvl >= 0.35 ? g.ramp.accent : g.ramp.verified;
        const cx0 = x + labW + ci * cw;
        out.push(box(cx0 + 3, yy + 3, cw - 6, rh - 6, g.card, g.line, 1));
        out.push(box(cx0 + 3, yy + 3, (cw - 6) * lvl, 4, col));    // rating, to scale
        out.push(tx(cell.rating, cx0 + 11, yy + 12, cw - 22, 12,
          { size: T.label, bold: true, color: col, caps: true }));
        out.push(tx(cap(cell.note, 46), cx0 + 11, yy + 25, cw - 22, rh - 30,
          { size: size - 1, color: g.ink }));
      });
    });
    return { out, h: hh + rows.length * rh };
  }

  // ── M03 · FALSIFIER TRI-STATE — raise · hold · lower ────────────────────
  function tristate(x, y, w, states, dark, size, grow = 0) {
    const g = G(dark), out = [], cw = (w - 2 * 10) / 3;
    const cols = [g.ramp.red, g.ramp.accent, g.ramp.verified];
    const H = Math.max(...states.map((s) => 34 + textH(s.text, cw - 26, size))) + 12 + grow;
    states.forEach((s, i) => {
      const xx = x + i * (cw + 10);
      out.push(box(xx, y, cw, H, g.card, g.line, 1));
      out.push(box(xx, y, cw, 4, cols[i]));
      out.push(tx(s.label, xx + 12, y + 12, cw - 24, T.label + 3,
        { size: T.label, bold: true, color: cols[i], caps: true }));
      out.push(tx(s.text, xx + 12, y + 28, cw - 26, H - 36, { size, color: g.ink }));
    });
    return { out, h: H };
  }

  // ── M04 · PROPORTION BAR — control-point ownership, to scale ────────────
  function proportion(x, y, w, segs, dark, size) {
    const g = G(dark), out = [], h = 52, total = segs.reduce((a, s) => a + s.share, 0);
    let cx = x;
    segs.forEach((s) => {
      const sw = (s.share / total) * w;
      out.push(box(cx, y, sw, h, s.colour));
      if (sw > 76) {
        out.push(tx(cap(s.label, 22), cx + 10, y + 10, sw - 18, 12,
          { size: T.label, bold: true, color: V.white, caps: true }));
        out.push(tx(cap(s.note, 40), cx + 10, y + 26, sw - 18, 18, { size: size - 1, color: '#DCE7EE' }));
      }
      cx += sw;
    });
    out.push(box(x, y, w, h, 'none', g.line, 1));
    segs.forEach((s, i) => {
      const sw = (s.share / total) * w;
      out.push(tx(`${Math.round((s.share / total) * 100)}%`,
        x + segs.slice(0, i).reduce((a, q) => a + (q.share / total) * w, 0), y + h + 6, sw, 13,
        { size: T.label, bold: true, color: g.muted }));
    });
    return { out, h: h + 20 };
  }

  // ── M05/M12 · SCORED TABLE — rows with a status column ──────────────────
  function scoredTable(x, y, w, cols, rows, dark, size) {
    const g = G(dark), out = [], hh = 26;
    const ws = cols.map((c) => (c.w || 1));
    const tot = ws.reduce((a, b) => a + b, 0);
    const cw = ws.map((v) => (v / tot) * w);
    out.push(box(x, y, w, hh, dark ? '#0C1D2E' : V.pageDark));
    let cx = x;
    cols.forEach((c, i) => { out.push(tx(c.t, cx + 10, y + 8, cw[i] - 14, 12,
      { size: T.label, bold: true, color: dark ? g.muted : V.white, caps: true })); cx += cw[i]; });
    let yy = y + hh;
    rows.forEach((r, ri) => {
      const rh = Math.max(34, ...r.cells.map((c, i) => 16 + textH(c.t, cw[i] - 20, size)));
      out.push(box(x, yy, w, rh, ri % 2 ? g.card : (dark ? V.pageDark : V.white), g.line, 1));
      if (r.colour) out.push(box(x, yy, 3, rh, r.colour));
      let rx = x;
      r.cells.forEach((c, i) => {
        out.push(tx(c.t, rx + 10, yy + 8, cw[i] - 18, rh - 12,
          { size, bold: !!c.bold, color: c.colour || (i === 0 ? g.head : g.ink) }));
        rx += cw[i];
      });
      yy += rh;
    });
    return { out, h: yy - y };
  }

  // ── M06 · SCORED REGISTER — importance × evidence, as filled dots ───────
  function register(x, y, w, items, dark, size, grow = 0) {
    const g = G(dark), out = [], rh = 40 + grow;
    out.push(box(x, y, w, 24, dark ? '#0C1D2E' : '#E8F0F3'));
    out.push(tx('Claim', x + 12, y + 7, w * 0.52, 12, { size: T.label, bold: true, color: g.muted, caps: true }));
    out.push(tx('Load-bearing', x + w * 0.56, y + 7, 100, 12, { size: T.label, bold: true, color: g.muted, caps: true }));
    out.push(tx('Evidence', x + w * 0.76, y + 7, 100, 12, { size: T.label, bold: true, color: g.muted, caps: true }));
    items.forEach((it, i) => {
      const yy = y + 24 + i * rh;
      out.push(box(x, yy, w, rh, i % 2 ? g.card : (dark ? V.pageDark : V.white), g.line, 1));
      out.push(box(x, yy, 3, rh, it.colour));
      out.push(tx(cap(it.claim, 120), x + 12, yy + 9, w * 0.52 - 16, rh - 14, { size, color: g.ink }));
      for (let d = 0; d < 3; d += 1)
        out.push(dot(x + w * 0.56 + d * 15, yy + rh / 2 - 5, 10,
          d < it.importance ? it.colour : (dark ? '#20344A' : '#D8E2E7')));
      for (let d = 0; d < 3; d += 1)
        out.push(dot(x + w * 0.76 + d * 15, yy + rh / 2 - 5, 10,
          d < it.evidence ? g.ramp.verified : (dark ? '#20344A' : '#D8E2E7')));
    });
    return { out, h: 24 + items.length * rh };
  }

  // ── M07/M10 · TIMELINE RAIL — phases to scale on a dated axis ───────────
  function rail(x, y, w, nodes, dark, size, grow = 0) {
    const g = G(dark), out = [], railY = y + 30;
    out.push(box(x, railY, w, 3, dark ? '#23364C' : V.line));
    const tot = nodes.reduce((a, n) => a + (n.span || 1), 0);
    let cx = x;
    nodes.forEach((n) => {
      const nw = ((n.span || 1) / tot) * w;
      out.push(box(cx, railY, Math.max(4, nw - 6), 3, n.colour));
      out.push(dot(cx - 1, railY - 5, 13, n.colour));
      out.push(tx(n.when, cx + 16, y + 6, nw - 20, 12,
        { size: T.label, bold: true, color: n.colour, caps: true }));
      out.push(tx(cap(n.label, 34), cx + 16, railY + 14, nw - 22, 15,
        { size: size + 1, bold: true, color: g.head }));
      out.push(tx(cap(n.note, 150), cx + 16, railY + 34, nw - 24, 46 + grow, { size, color: g.ink }));
      cx += nw;
    });
    return { out, h: 106 + grow };
  }

  // ── M08 · COST WATERFALL — step heights are the magnitudes ──────────────
  function waterfall(x, y, w, h, steps, dark, size, grow = 0) {
    h += grow;
    const g = G(dark), out = [], n = steps.length, bw = (w - (n - 1) * 14) / n;
    const max = Math.max(...steps.map((s) => Math.abs(s.value)));
    out.push(box(x, y + h, w, 1, g.line));
    steps.forEach((s, i) => {
      const bh = Math.max(8, (Math.abs(s.value) / max) * (h - 30));
      const bx = x + i * (bw + 14);
      out.push(box(bx, y + h - bh, bw, bh, s.colour));
      out.push(tx(s.amount, bx - 6, y + h - bh - 20, bw + 12, 16,
        { size: size + 2, face: SERIF, bold: true, color: g.head, align: 'center' }));
      out.push(tx(cap(s.label, 20), bx - 8, y + h + 7, bw + 16, 24,
        { size: T.label, bold: true, color: g.muted, align: 'center', caps: true }));
    });
    return { out, h: h + 34 };
  }

  // ── M09/M11 · NUMBERED CHAIN — sequence with arrows ─────────────────────
  function chain(x, y, w, nodes, dark, size, grow = 0) {
    const g = G(dark), out = [], n = nodes.length;
    const nw = (w - (n - 1) * 30) / n;
    const H = Math.max(...nodes.map((d) => 40 + textH(d.text, nw - 26, size))) + 12 + grow;
    nodes.forEach((d, i) => {
      const nx = x + i * (nw + 30);
      out.push(box(nx, y, nw, H, g.card, d.colour, 1));
      out.push(box(nx, y, nw, 4, d.colour));
      out.push(tx(String(i + 1).padStart(2, '0'), nx + 12, y + 11, 24, 16,
        { size: size + 3, face: SERIF, bold: true, color: d.colour }));
      out.push(tx(cap(d.label, 30), nx + 38, y + 13, nw - 48, 13,
        { size: T.label, bold: true, color: g.head, caps: true }));
      out.push(tx(d.text, nx + 12, y + 34, nw - 26, H - 42, { size, color: g.ink }));
      if (i < n - 1) out.push(arrow(nx + nw + 6, y + H / 2 - 8, 18, 16, g.ramp.accent));
    });
    return { out, h: H };
  }

  return { ladder, heatmap, tristate, proportion, scoredTable, register, rail, waterfall, chain,
           helpers: { tx, box, dot, arrow, G, cap } };
}
