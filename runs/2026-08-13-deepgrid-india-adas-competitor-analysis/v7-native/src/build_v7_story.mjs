// build_v7_story.mjs — DeepGrid India ADAS dossier: v7 design, Accenture grammar.
//
// The previous build rendered whatever blocks the source page happened to carry,
// which is why the storytelling read as fragments. This one renders the CONTENT
// ENVELOPE from `references/accenture-guide-content-envelope.md`, in the order the
// grammar requires, so every page argues rather than lists:
//
//   kicker -> action title -> cyan rule -> analytical question
//   -> EXECUTIVE ANSWER (the answer, stated first: BLUF)
//   -> status-coded evidence
//   -> WHY THIS FOLLOWS (the causal/comparative mechanism)
//   -> STRONGEST COUNTERARGUMENT + FALSIFIER (on the page, not in the notes)
//   -> DECISION band carrying owner, trigger and stop/escalate rule
//
//   DECK_RUN=<dir> DECK_NAME=<slug> [DECK_RENDER=1] node src/build_v7_story.mjs
import { readFile, writeFile, mkdir } from 'node:fs/promises';

const AT = process.env.ARTIFACT_TOOL_DIST || 'file:///home/sheke/.local/artifact-tool-linux/dist';
const { Presentation, PresentationFile, layers: composeLayers } = await import(`${AT}/artifact_tool.mjs`);
const { textStyle, stroke } = await import(`${AT}/presentation-jsx/index.mjs`);
const { jsx, jsxs } = await import(`${AT}/presentation-jsx/jsx-runtime.mjs`);

const RUN = process.env.DECK_RUN || '.';
const ENV = JSON.parse(await readFile(`${RUN}/slide-envelopes.json`, 'utf8')).slides;

// measured v7 tokens (see v7-design-notes.md)
const V = {
  pageLight: '#FFFFFF', pageDark: '#081525', cardLight: '#F1F7F9', cardDark: '#10263A',
  band: '#101827', accent: '#04B3C7', ink: '#101827', white: '#FFFFFF',
  muted: '#65707E', mutedDark: '#8EA0B2', line: '#D8E2E7', lineDark: '#1A2F45',
  amberTint: '#FFF7EC',
};
// AA-calibrated status ramps per ground (v7's single ramp fails 4.5:1 on light)
const RAMP = {
  light: { accent: '#037A87', verified: '#157F59', amber: '#AB5A08', red: '#C62828' },
  dark:  { accent: '#04B3C7', verified: '#1BA271', amber: '#D7720B', red: '#E06767' },
};
const SERIF = 'Georgia', SANS = 'Arial';
const PT = (pt) => pt / 0.75;
// label/foot sit at 8pt: the design system allows 7-8pt for captions and
// footers, and 8 is the floor the design-quality lint enforces.
const T = { title: PT(20), kicker: PT(8), crumb: PT(9), lead: PT(13),
            label: PT(8), body: PT(11), band: PT(10), foot: PT(8) };

const M = 48, LIVE = 1184, GUT = 12;
const BAND_H = 62, FOOT_Y = 676;
const BODY_BOT = 720 - 44 - BAND_H - 10;

const P = Presentation.create();
const C = P.compose;
const Text = ({ children = '', ...p }) => C.text(String(children), p);
const Shape = (p) => C.shape(p);
const Layers = ({ children = [], ...p }) => composeLayers(p, Array.isArray(children) ? children : [children]);

const st = (o) => textStyle(`font: ${o.bold ? 'bold ' : ''}${o.size}px ${o.face || SANS}; `
  + `color: ${o.color}; align: ${o.align || 'left'}; anchor: top; inset: 0px; autofit: shrink`);
const tx = (t, x, y, w, h, o) => jsx(Text, {
  width: C.fixed(Math.max(4, w)), height: C.fixed(Math.max(6, h)),
  position: { left: x, top: y }, style: st(o),
  children: o.caps ? String(t).toUpperCase() : t });
const box = (x, y, w, h, fill, lc = 'none', lw = 0) => jsx(Shape, {
  geometry: 'rect', width: C.fixed(Math.max(1, w)), height: C.fixed(Math.max(1, h)), fill,
  line: lc === 'none' ? stroke('0px none') : stroke(`${lw}px solid ${lc}`),
  position: { left: x, top: y } });

const textH = (s, w, size, lh = 1.34) => {
  const cpl = Math.max(8, Math.floor(w / (size * 0.50)));
  return Math.ceil(String(s).split('\n')
    .reduce((n, p) => n + Math.max(1, Math.ceil(p.length / cpl)), 0) * size * lh);
};

// one labelled panel: colour bar + caps label + body
function panel(x, y, w, h, label, body, colour, size, dark, fill, pad = 0) {
  const bh = textH(body, w - 26, size);
  const H = Math.max(h, 8 + T.label + 5 + bh + 9 + pad);
  // A few source labels are whole sentences. Uppercased at label size they wrap
  // into a paragraph and stop reading as a label, so they are clamped.
  const lab = String(label).length > 46 ? String(label).slice(0, 44).trimEnd() + '…' : label;
  return [
    box(x, y, w, H, fill, dark ? V.lineDark : V.line, 1),
    box(x, y, 3, H, colour),
    tx(lab, x + 13, y + 7, w - 22, T.label + 4, { size: T.label, bold: true, color: colour, caps: true }),
    tx(body, x + 13, y + 7 + T.label + 5, w - 26, bh + 3,
       { size, color: dark ? '#C9D6E2' : V.ink }),
  ];
}
const panelH = (body, w, size, pad = 0) => 8 + T.label + 5 + textH(body, w - 26, size) + 9 + pad;

const ENTITIES = ['Starkenn', 'Gahan', 'drivebuddyAI', 'STRADVISION', 'Netrasemi', 'bitsensing',
                  'Sterling', 'MINIEYE', 'Aptiv', 'ZF', 'Bosch', 'Continental', 'Valeo'];
function kickerOf(e) {
  const t = e.action_title, ent = ENTITIES.find((x) => t.toLowerCase().includes(x.toLowerCase()));
  const a = e.archetype || '';
  if (/falsifi/i.test(t)) return ent ? `${ent} · falsifier` : 'Falsifier';
  if (a === 'decision-scorecard') return 'Method';
  if (a === 'recommendation-ask') return 'Decision';
  if (a === 'risk-mitigation') return ent ? `${ent} · risk control` : 'Risk control';
  if (ent) return `${ent} · evidence`;
  return 'Position';
}
const isDark = (e) => ['recommendation-ask', 'risk-mitigation'].includes(e.archetype)
  || /falsifi|threat|counter-?move|decision|verdict|stop|fund |pause /i.test(e.action_title);

const STATUS_COLOUR = (s, ramp) =>
  /verified fact/i.test(s) ? ramp.verified
  : /insufficient/i.test(s) ? ramp.red
  : /attributed|qualified/i.test(s) ? ramp.amber : ramp.accent;

let page = 0;
const stats = [];

// ── cover ────────────────────────────────────────────────────────────────
page += 1;
{
  const s = P.slides.add(); s.setViewportSize(1280, 720);
  s.compose(jsxs(Layers, { width: C.fixed(1280), height: C.fixed(720), children: [
    box(0, 0, 1280, 720, V.pageDark), box(0, 0, 1280, 4, V.accent),
    tx('India ADAS · competitor dossier', M, 208, 900, 16, { size: T.kicker, bold: true, color: V.accent, caps: true }),
    box(M, 234, 88, 2, V.accent),
    tx('Perception-layer acceptance is the strategic gate', M, 256, 1040, 116,
       { size: PT(34), face: SERIF, bold: true, color: V.white }),
    tx('Who occupies each buying arena, what the evidence actually supports, and the four gates worth funding before the 2027 AEBS dates.',
       M, 392, 920, 40, { size: T.crumb, color: V.mutedDark }),
    ...[['10', 'Competitors assessed'], ['4', 'Evidence gates'], ['3', 'Priority threats'], ['2027', 'AEBS mandate']]
      .flatMap(([n, l], i) => [
        tx(n, M + i * 210, 462, 190, 38, { size: PT(22), face: SERIF, bold: true, color: V.accent }),
        tx(l, M + i * 210, 502, 190, 13, { size: T.foot, bold: true, color: V.mutedDark, caps: true })]),
    box(M, FOOT_Y - 10, LIVE, 1, V.lineDark),
    tx('DeepGrid Semi · India ADAS competitor dossier · Confidential', M, FOOT_Y, 820, 12,
       { size: T.foot, color: V.mutedDark, caps: true }),
  ] }));
  s.speakerNotes.text = 'Cover. Design authority: supplied v7 dossier. Content: validated India ADAS evidence base.';
  stats.push({ page, kind: 'cover', dark: true });
}

ENV.forEach((e) => {
  page += 1;
  const dark = isDark(e);
  const ramp = dark ? RAMP.dark : RAMP.light;
  const pg = dark ? V.pageDark : V.pageLight;
  const cardBg = dark ? V.cardDark : V.cardLight;
  const el = [box(0, 0, 1280, 720, pg)];

  // header
  el.push(tx(kickerOf(e), M, 24, 800, 13, { size: T.kicker, bold: true, color: ramp.accent, caps: true }));
  const tl = Math.min(2, Math.max(1, Math.ceil(e.action_title.length / 76)));
  el.push(tx(e.action_title, M, 40, LIVE, tl * (T.title + 6),
             { size: T.title, face: SERIF, bold: true, color: dark ? V.white : V.ink }));
  let y = 40 + tl * (T.title + 6) + 6;
  el.push(box(M, y, LIVE, 2, V.accent)); y += 8;
  if (e.analytical_question) {
    el.push(tx(e.analytical_question, M, y, LIVE, 13, { size: T.crumb, color: dark ? V.mutedDark : V.muted }));
    y += 19;
  }

  // ---- the argument, in grammar order
  const ev = (e.supporting_blocks || []).filter((b) => (b.label || '').trim() && (b.text || '').trim());
  const evStatus = (b) => STATUS_COLOUR((b.tags || []).join(' '), ramp);

  const trySize = (size, pad = 0) => {
    // rowCount tracks LAYOUT rows, not elements. Counting distinct element tops
    // inflated it about fourfold (each panel emits box, bar, label, body), which
    // made the computed padding negligible and left the band empty.
    const out = []; let yy = y, rowCount = 0;
    const add = (items) => { items.forEach((i) => out.push(i)); };

    // 1. executive answer — the answer first
    const aH = panelH(e.executive_answer, LIVE, T.lead, pad);
    add(panel(M, yy, LIVE, aH, 'Executive answer', e.executive_answer, ramp.accent, T.lead, dark,
              dark ? V.cardDark : V.cardLight, pad)); yy += aH + GUT; rowCount += 1;

    // 2. evidence, status-coded — up to six across two rows of three
    const picks = ev.slice(0, 6);
    for (let r = 0; r < Math.ceil(picks.length / 3); r += 1) {
      const row = picks.slice(r * 3, r * 3 + 3);
      const w = (LIVE - GUT * (row.length - 1)) / row.length;
      const h = Math.max(...row.map((b) => panelH(b.text, w, size, pad)));
      row.forEach((b, i) => add(panel(M + i * (w + GUT), yy, w, h,
        b.label, b.text, evStatus(b), size, dark, cardBg, pad)));
      yy += h + GUT; rowCount += 1;
    }

    // 3. mechanism
    if (e.logic && e.logic.mechanism) {
      const h = panelH(e.logic.mechanism, LIVE, size, pad);
      add(panel(M, yy, LIVE, h, 'Why this follows', e.logic.mechanism, ramp.accent, size, dark, cardBg, pad));
      yy += h + GUT; rowCount += 1;
    }

    // 4. counterargument + falsifier, side by side
    const pair = [
      e.counterargument && ['Strongest counterargument', e.counterargument, ramp.amber],
      e.falsifier && ['Falsifier', e.falsifier, ramp.red],
    ].filter(Boolean);
    if (pair.length) {
      const w = (LIVE - GUT * (pair.length - 1)) / pair.length;
      const h = Math.max(...pair.map(([, t]) => panelH(t, w, size, pad)));
      pair.forEach(([l, t, c], i) => add(panel(M + i * (w + GUT), yy, w, h, l, t, c, size, dark,
        dark ? V.cardDark : (c === ramp.amber ? V.amberTint : V.cardLight), pad)));
      yy += h + GUT; rowCount += 1;
    }
    return { out, bottom: yy - GUT, rows: rowCount };
  };

  // Fit at the largest type that works, then RE-LAY OUT with per-panel padding so
  // the leftover height grows the panels instead of opening a gap above the
  // decision band. The first version distributed slack between rows, which just
  // moved the empty space around.
  let laid = null, chosen = null;
  for (const size of [T.body, PT(10), PT(9), PT(8), PT(7.5)]) {
    const r = trySize(size, 0);
    if (r.bottom <= BODY_BOT) { laid = r; chosen = size; break; }
  }
  if (!laid) { chosen = PT(7.5); laid = trySize(chosen, 0); stats.push({ overflow: page }); }
  else {
    const slack = BODY_BOT - laid.bottom;
    if (slack > 24 && laid.rows > 0) {
      const padded = trySize(chosen, Math.min(34, slack / laid.rows));
      if (padded.bottom <= BODY_BOT) laid = padded;
    }
  }
  el.push(...laid.out);

  // 5. decision band — decision, owner, trigger, stop rule
  const by = 720 - 44 - BAND_H;
  el.push(box(M, by, LIVE, BAND_H, dark ? V.band : V.pageDark));
  el.push(box(M, by, 3, BAND_H, V.accent));
  el.push(tx('Decision', M + 16, by + 9, 150, 11, { size: T.label, bold: true, color: V.accent, caps: true }));
  el.push(tx(e.decision || e.implication || '', M + 16, by + 23, 700, 30, { size: T.band, color: V.white }));
  const meta = [e.owner && `Owner · ${e.owner}`, e.trigger && `Trigger · ${e.trigger}`]
    .filter(Boolean).join('     ');
  el.push(tx(meta, M + 730, by + 9, LIVE - 746, 24, { size: T.foot, color: V.mutedDark }));
  // The band is dark on every page, so it always takes the DARK ramp. Using the
  // page's ramp put light-ramp amber (#AB5A08) on #081525 at 3.67:1.
  el.push(tx(e.stop_or_escalate_rule ? `Stop / escalate · ${e.stop_or_escalate_rule}` : '',
             M + 730, by + 36, LIVE - 746, 20, { size: T.foot, color: RAMP.dark.amber }));

  // footer
  el.push(box(M, FOOT_Y - 10, LIVE, 1, dark ? V.lineDark : V.line));
  el.push(tx('DeepGrid Semi · India ADAS competitor dossier · Confidential', M, FOOT_Y, 820, 12,
             { size: T.foot, color: dark ? V.mutedDark : V.muted, caps: true }));
  el.push(tx(String(page), 1232 - 40, FOOT_Y, 40, 12,
             { size: T.foot, bold: true, color: dark ? V.mutedDark : V.muted, align: 'right' }));

  const s = P.slides.add(); s.setViewportSize(1280, 720);
  s.compose(jsxs(Layers, { width: C.fixed(1280), height: C.fixed(720), children: el }));
  s.speakerNotes.text =
    `Q: ${e.analytical_question}\nA: ${e.executive_answer}\n\n`
  + `Mechanism: ${(e.logic || {}).mechanism || ''}\n`
  + `Counterargument: ${e.counterargument || ''}\nFalsifier: ${e.falsifier || ''}\n`
  + `Implication: ${e.implication || ''}\nDecision: ${e.decision || ''}\n`
  + `Owner: ${e.owner || ''} · Trigger: ${e.trigger || ''}\n`
  + `Stop/escalate: ${e.stop_or_escalate_rule || ''}\n\n${e.source_note || ''}`;
  stats.push({ page, src: e.slide_id, archetype: e.archetype, dark, evidence: ev.length });
});

const OUT = `${RUN}/${process.env.DECK_NAME || 'deck'}-draft.pptx`;
await (await PresentationFile.exportPptx(P)).save(OUT);
await mkdir(`${RUN}/qa`, { recursive: true });
await writeFile(`${RUN}/qa/layout-stats.json`, JSON.stringify(stats, null, 1));
const d = stats.filter((s) => s.dark).length, n = stats.filter((s) => s.page).length;
console.log(`DONE: ${P.slides.count} slides -> ${OUT}`);
console.log(`  dark ${d} of ${n} (${Math.round(d / n * 100)}%) · overflow ${stats.filter((s) => s.overflow).length}`);

if (process.env.DECK_RENDER) {
  const dir = `${RUN}/qa/renders`;
  await mkdir(dir, { recursive: true });
  for (let i = 0; i < P.slides.count; i += 1) {
    const b = await P.export({ format: 'png', slide: P.slides.getItem(i), scale: 1 });
    await writeFile(`${dir}/slide-${String(i + 1).padStart(3, '0')}.png`, Buffer.from(await b.arrayBuffer()));
  }
  console.log(`  rendered ${P.slides.count} PNGs -> ${dir}`);
}
