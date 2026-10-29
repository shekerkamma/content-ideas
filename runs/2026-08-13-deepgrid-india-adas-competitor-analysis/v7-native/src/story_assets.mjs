// story_assets.mjs — the visual story layer the deck was missing.
//
// 73 argued pages with no spine above them is a reference document, not a
// presentation. These are the assets that make it a story:
//
//   storyboardPage  the whole arc on one page — acts as bands, pages to scale
//   pyramidPage     governing thought over three supports (Pyramid Principle)
//   deltaPage       what live research changed since the dossier was written
//   actDivider      the act's question, and what it settles
//   hostilePage     the six questions a skeptical board actually asks
//
// Geometry encodes meaning here too: on the storyboard, band width is page
// count, so the reader sees that Act III is 60% of the deck before reading a
// word of it.
export function makeStoryAssets({ jsx, C, Text, Shape, textStyle, stroke, V, RAMP, T, SERIF, textH }) {
  const st = (o) => textStyle(`font: ${o.bold ? 'bold ' : ''}${o.size}px ${o.face || 'Arial'}; `
    + `color: ${o.color}; align: ${o.align || 'left'}; anchor: top; inset: 0px; autofit: shrink`);
  const tx = (t, x, y, w, h, o) => jsx(Text, {
    width: C.fixed(Math.max(4, w)), height: C.fixed(Math.max(6, h)),
    position: { left: x, top: y }, style: st(o), children: o.caps ? String(t).toUpperCase() : t });
  const box = (x, y, w, h, fill, lc = 'none', lw = 0) => jsx(Shape, {
    geometry: 'rect', width: C.fixed(Math.max(1, w)), height: C.fixed(Math.max(1, h)), fill,
    line: lc === 'none' ? stroke('0px none') : stroke(`${lw}px solid ${lc}`), position: { left: x, top: y } });
  const cap = (s, n) => (String(s).length > n ? `${String(s).slice(0, n - 1).trimEnd()}…` : String(s));
  const M = 48, LIVE = 1184;
  const ACT_COL = ['#04B3C7', '#D7720B', '#E06767', '#1BA271', '#8B7BE0'];   // bars/fills
  const ACT_TX  = ['#04B3C7', '#E88A2C', '#EE8585', '#2FBF87', '#A99DF0'];   // text on dark

  // ── the whole deck on one page; band width = page count ──────────────────
  function storyboardPage(nar, startPage) {
    const el = [box(0, 0, 1280, 720, V.pageDark), box(0, 0, 1280, 4, V.accent)];
    el.push(tx('The storyboard', M, 34, 700, 34, { size: T.title, face: SERIF, bold: true, color: V.white }));
    el.push(tx('Five acts, 73 argued pages. Band width is page count — Act III is the deck.',
               M, 74, 900, 16, { size: T.crumb, color: V.mutedDark }));
    el.push(box(M, 100, LIVE, 2, V.accent));

    // SCQA strip
    const sc = [['S', nar.scqa.situation], ['C', nar.scqa.complication],
                ['Q', nar.scqa.question], ['A', nar.scqa.answer]];
    const cw = (LIVE - 3 * 10) / 4;
    let scH = 0;
    sc.forEach(([k, v], i) => { scH = Math.max(scH, 30 + textH(v, cw - 24, T.foot + 1)); });
    sc.forEach(([k, v], i) => {
      const x = M + i * (cw + 10);
      el.push(box(x, 116, cw, scH, V.cardDark, V.lineDark, 1));
      el.push(box(x, 116, cw, 3, i === 3 ? RAMP.dark.verified : RAMP.dark.accent));
      el.push(tx({ S: 'Situation', C: 'Complication', Q: 'Question', A: 'Answer' }[k],
                 x + 12, 124, cw - 20, 12, { size: T.label, bold: true,
                 color: i === 3 ? RAMP.dark.verified : RAMP.dark.accent, caps: true }));
      el.push(tx(v, x + 12, 140, cw - 24, scH - 26, { size: T.foot + 1, color: '#C9D6E2' }));
    });

    // act bands, to scale
    let y = 116 + scH + 22;
    el.push(tx('The arc', M, y, 400, 13, { size: T.label, bold: true, color: V.mutedDark, caps: true }));
    y += 20;
    const total = nar.acts.reduce((a, k) => a + k.slides.length, 0);
    let x = M;
    nar.acts.forEach((a, i) => {
      const w = (a.slides.length / total) * LIVE;
      el.push(box(x, y, Math.max(4, w - 4), 34, ACT_COL[i]));
      el.push(tx(a.no, x + 8, y + 6, w - 16, 12, { size: T.label, bold: true, color: '#06121F', caps: true }));
      el.push(tx(`${a.slides.length}`, x + 8, y + 18, w - 16, 12,
                 { size: T.label, bold: true, color: '#06121F' }));
      x += w;
    });
    y += 44;

    // act rows: question + what it settles
    nar.acts.forEach((a, i) => {
      const h = 60;
      el.push(box(M, y, LIVE, h, V.cardDark, V.lineDark, 1));
      el.push(box(M, y, 3, h, ACT_COL[i]));
      el.push(tx(`${a.no} · ${a.name}`, M + 14, y + 8, 260, 14,
                 { size: T.body - 1, bold: true, color: ACT_TX[i] }));
      el.push(tx(`pp. ${startPage + nar.acts.slice(0, i).reduce((s, k) => s + k.slides.length + 1, 0) + 1}`
                 + `–${startPage + nar.acts.slice(0, i + 1).reduce((s, k) => s + k.slides.length + 1, 0)}`,
                 M + 14, y + 26, 260, 12, { size: T.foot, color: V.mutedDark, caps: true }));
      el.push(tx(a.question, M + 288, y + 8, 560, 26, { size: T.foot + 1, color: V.white }));
      el.push(tx(a.settles, M + 288, y + 34, 560, 22, { size: T.foot, color: V.mutedDark }));
      el.push(tx(`${a.slides.length}`, M + LIVE - 74, y + 14, 60, 32,
                 { size: 26, face: SERIF, bold: true, color: ACT_TX[i], align: 'right' }));
      y += h + 6;
    });
    return el;
  }

  // ── Pyramid Principle: one governing thought over three supports ─────────
  function pyramidPage(nar) {
    const p = nar.pyramid;
    const el = [box(0, 0, 1280, 720, V.pageLight)];
    const r = RAMP.light;
    el.push(tx('The argument in one shape', M, 30, 900, 30,
               { size: T.title, face: SERIF, bold: true, color: V.ink }));
    el.push(tx('If the board reads one page, this is the page.', M, 68, 900, 14,
               { size: T.crumb, color: V.muted }));
    el.push(box(M, 92, LIVE, 2, V.accent));

    const gh = 16 + textH(p.governing_thought, LIVE - 60, T.lead) + 26;
    el.push(box(M, 108, LIVE, gh, V.pageDark));
    el.push(box(M, 108, 4, gh, r.accent));
    el.push(tx('Governing thought', M + 20, 118, 400, 13,
               { size: T.label, bold: true, color: V.accent, caps: true }));
    el.push(tx(p.governing_thought, M + 20, 136, LIVE - 60, gh - 40,
               { size: T.lead, color: V.white }));

    // three supports, each: claim / because / where it is proved
    const y0 = 108 + gh + 14;
    el.push(box(M + LIVE / 2 - 1, y0 - 12, 2, 12, V.line));
    const w = (LIVE - 2 * 12) / 3;
    const bodyH = Math.max(...p.supports.map((s) =>
      70 + textH(s.claim, w - 26, T.body) + textH(s.because, w - 26, T.foot + 1)));
    p.supports.forEach((s, i) => {
      const x = M + i * (w + 12);
      const col = [r.accent, r.red, r.amber][i];
      el.push(box(x, y0, w, bodyH, V.cardLight, V.line, 1));
      el.push(box(x, y0, w, 4, col));
      el.push(tx(`Support ${i + 1}`, x + 14, y0 + 12, w - 26, 12,
                 { size: T.label, bold: true, color: col, caps: true }));
      const ch = textH(s.claim, w - 26, T.body);
      el.push(tx(s.claim, x + 14, y0 + 30, w - 26, ch + 4,
                 { size: T.body, bold: true, color: V.ink }));
      el.push(tx(s.because, x + 14, y0 + 36 + ch, w - 26,
                 textH(s.because, w - 26, T.foot + 1) + 4, { size: T.foot + 1, color: '#3E4A57' }));
      el.push(box(x + 14, y0 + bodyH - 24, w - 28, 1, V.line));
      el.push(tx(s.proof, x + 14, y0 + bodyH - 18, w - 26, 12,
                 { size: T.foot, bold: true, color: V.muted, caps: true }));
    });
    return el;
  }

  // ── what live research changed since the dossier was written ─────────────
  function deltaPage(delta, imgDataUrl) {
    const el = [box(0, 0, 1280, 720, V.pageLight)];
    const r = RAMP.light;
    el.push(tx('Live research moves four ratings — and finds our thesis already occupied',
               M, 30, LIVE, 34, { size: T.title, face: SERIF, bold: true, color: V.ink }));
    el.push(box(M, 74, LIVE, 2, V.accent));
    el.push(tx(delta.method, M, 84, LIVE, 14, { size: T.crumb, color: V.muted }));

    // the headline finding, with the primary artifact beside it
    const d1 = delta.deltas[0];
    const nowH = textH(d1.now, 700, T.lead);
    const whyH = textH(d1.so_what, 700, T.foot + 1);
    const H = Math.max(176, 46 + nowH + 10 + whyH + 26);
    el.push(box(M, 108, LIVE, H, V.pageDark));
    el.push(box(M, 108, 4, H, r.red));
    el.push(tx('The finding that changes the map', M + 20, 120, 600, 13,
               { size: T.label, bold: true, color: RAMP.dark.red, caps: true }));
    el.push(tx(d1.now, M + 20, 140, 700, nowH + 4, { size: T.lead, bold: true, color: V.white }));
    el.push(tx(d1.so_what, M + 20, 150 + nowH, 700, whyH + 4,
               { size: T.foot + 1, color: '#C9D6E2' }));
    el.push(tx(`Verified fact · ${d1.source}`, M + 20, H + 108 - 24, 700, 12,
               { size: T.foot, color: RAMP.dark.verified, caps: true }));
    if (imgDataUrl) {
      el.push(C.image({ dataUrl: imgDataUrl, width: C.fixed(388), height: C.fixed(H - 32),
                        position: { left: M + LIVE - 404, top: 124 } }));
    }

    // the rest as a status-move register
    let y = 108 + H + 14;
    el.push(tx('Every other gap, retested', M, y, 500, 13,
               { size: T.label, bold: true, color: V.muted, caps: true }));
    y += 18;
    const rows = delta.deltas.slice(1);
    const rh = Math.floor((604 - y) / rows.length) - 4;
    rows.forEach((d) => {
      const col = d.status === 'verified fact' ? r.verified
        : d.status === 'insufficient evidence' ? r.red : r.amber;
      el.push(box(M, y, LIVE, rh, V.cardLight, V.line, 1));
      el.push(box(M, y, 3, rh, col));
      el.push(tx(d.entity, M + 14, y + 7, 170, 14, { size: T.body - 1, bold: true, color: V.ink }));
      el.push(tx(d.status, M + 14, y + rh - 16, 170, 12, { size: T.foot, bold: true, color: col, caps: true }));
      el.push(tx(cap(d.rating_move, 86), M + 196, y + 7, 300, rh - 12, { size: T.foot + 1, color: V.ink }));
      el.push(tx(cap(d.so_what, 176), M + 508, y + 7, LIVE - 522, rh - 12,
                 { size: T.foot + 1, color: '#3E4A57' }));
      y += rh + 4;
    });
    return el;
  }

  // ── act divider ──────────────────────────────────────────────────────────
  function actDivider(act, i, firstPage, lastPage) {
    const col = ACT_COL[i];
    return [
      box(0, 0, 1280, 720, V.pageDark), box(0, 0, 1280, 4, col),
      box(M, 214, 120, 4, col),
      tx(act.no, M, 240, 500, 22, { size: T.crumb, bold: true, color: ACT_TX[i], caps: true }),
      tx(act.name, M, 268, 900, 68, { size: 46, face: SERIF, bold: true, color: V.white }),
      tx(act.question, M, 356, 820, 52, { size: T.lead + 2, color: '#C9D6E2' }),
      box(M, 428, 820, 1, V.lineDark),
      tx('What this act settles', M, 442, 400, 13,
         { size: T.label, bold: true, color: ACT_TX[i], caps: true }),
      tx(act.settles, M, 462, 820, 44, { size: T.crumb, color: V.mutedDark }),
      tx(`${act.slides.length}`, M + 940, 262, 200, 74,
         { size: 62, face: SERIF, bold: true, color: ACT_TX[i] }),
      tx('pages', M + 940, 340, 200, 14, { size: T.foot, bold: true, color: V.mutedDark, caps: true }),
      tx(`pp. ${firstPage}–${lastPage}`, M + 940, 360, 200, 14, { size: T.foot, color: V.mutedDark }),
    ];
  }

  // ── the questions a skeptical board actually asks ────────────────────────
  function hostilePage(qs) {
    const el = [box(0, 0, 1280, 720, V.pageLight)];
    const r = RAMP.light;
    el.push(tx('Six questions this deck must survive', M, 30, LIVE, 34,
               { size: T.title, face: SERIF, bold: true, color: V.ink }));
    el.push(box(M, 74, LIVE, 2, V.accent));
    el.push(tx('Answers are on the page, not in the appendix. Each one names the evidence it rests on.',
               M, 84, LIVE, 14, { size: T.crumb, color: V.muted }));
    const w = (LIVE - 12) / 2, rows = Math.ceil(qs.length / 2);
    const h = Math.floor((596 - 108) / rows) - 8;
    qs.forEach(([q, a], i) => {
      const x = M + (i % 2) * (w + 12), y = 108 + Math.floor(i / 2) * (h + 8);
      el.push(box(x, y, w, h, V.cardLight, V.line, 1));
      el.push(box(x, y, 3, h, r.amber));
      el.push(tx(q, x + 14, y + 9, w - 26, 30, { size: T.body - 1, bold: true, color: V.ink }));
      el.push(tx(a, x + 14, y + 42, w - 26, h - 50, { size: T.foot + 1, color: '#3E4A57' }));
    });
    return el;
  }

  return { storyboardPage, pyramidPage, deltaPage, actDivider, hostilePage };
}
