// build_bound_deck.mjs — the content deck, generated AS BOUND BY the adapted
// prompt templates.
//
// Deliverable 2, stage 2. Nothing on a page is chosen by taste: each slide's
// body is the OUTPUT INCLUDES list of the template it was bound to in
// bound-envelopes.json, and its exhibit is the one that template names.
//
//   P1 ladder     rung width  = confidence
//   P2 heatmap    cell bar    = rating
//   P3 chain      numbered sequence, arrows, reversibility
//   P4 tristate   three stances at full strength
//   P5 rail       phase width = span in weeks
//   P6 waterfall  bar height  = magnitude
//   P7 register   filled dots = importance x evidence
//
// Design authority is the supplied v7 dossier (tokens in v7-design-notes.md).
// Structure authority is the template deck. Those are different jobs and this
// file keeps them apart.
//
//   DECK_RUN=<dir> DECK_NAME=<slug> [DECK_RENDER=1] node src/build_bound_deck.mjs
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { makeExhibits } from './exhibits.mjs';
import { makeStoryAssets } from './story_assets.mjs';

const AT = process.env.ARTIFACT_TOOL_DIST || 'file:///home/sheke/.local/artifact-tool-linux/dist';
const { Presentation, PresentationFile, layers: composeLayers } = await import(`${AT}/artifact_tool.mjs`);
const { textStyle, stroke } = await import(`${AT}/presentation-jsx/index.mjs`);
const { jsx, jsxs } = await import(`${AT}/presentation-jsx/jsx-runtime.mjs`);

const RUN = process.env.DECK_RUN || '.';
const BOUND = JSON.parse(await readFile(`${RUN}/bound-envelopes.json`, 'utf8')).slides;
const NAR = JSON.parse(await readFile(`${RUN}/narrative.json`, 'utf8'));
const DELTA = JSON.parse(await readFile(`${RUN}/research/evidence-delta.json`, 'utf8'));
// the primary artifact for the headline delta — exact-state evidence, extracted
let DELTA_IMG = null;
try {
  const png = await readFile(`${RUN}/research/primary/aptiv-gen6-india.png`);
  DELTA_IMG = `data:image/png;base64,${png.toString('base64')}`;
} catch { /* the page degrades to text-only when the capture is absent */ }

// measured v7 tokens (v7-design-notes.md)
const V = {
  pageLight: '#FFFFFF', pageDark: '#081525', cardLight: '#F1F7F9', cardDark: '#10263A',
  band: '#101827', accent: '#04B3C7', ink: '#101827', white: '#FFFFFF',
  muted: '#586270', mutedDark: '#8EA0B2', line: '#D8E2E7', lineDark: '#1A2F45',
  amberTint: '#FFF7EC',
};
const RAMP = {                       // AA-calibrated per ground; v7's single ramp fails on light
  light: { accent: '#037A87', verified: '#157F59', amber: '#AB5A08', red: '#C62828' },
  dark:  { accent: '#04B3C7', verified: '#1BA271', amber: '#D7720B', red: '#E06767' },
};
const SERIF = 'Georgia', SANS = 'Arial';
const PT = (v) => v / 0.75;
const T = { title: PT(20), kicker: PT(8), crumb: PT(9), lead: PT(12),
            label: PT(8), body: PT(10.5), band: PT(10), foot: PT(8) };
const M = 48, LIVE = 1184, GUT = 12, BAND_H = 80, FOOT_Y = 676;
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
  position: { left: x, top: y }, style: st(o), children: o.caps ? String(t).toUpperCase() : t });
const box = (x, y, w, h, fill, lc = 'none', lw = 0) => jsx(Shape, {
  geometry: 'rect', width: C.fixed(Math.max(1, w)), height: C.fixed(Math.max(1, h)), fill,
  line: lc === 'none' ? stroke('0px none') : stroke(`${lw}px solid ${lc}`), position: { left: x, top: y } });
const textH = (s, w, size, lh = 1.34) => {
  const cpl = Math.max(8, Math.floor(w / (size * 0.50)));
  return Math.ceil(String(s).split('\n')
    .reduce((n, p) => n + Math.max(1, Math.ceil(p.length / cpl)), 0) * size * lh);
};
function panel(x, y, w, label, body, colour, size, dark, fill) {
  const bh = textH(body, w - 26, size);
  const H = 8 + T.label + 5 + bh + 9;
  const lab = String(label).length > 46 ? `${String(label).slice(0, 44).trimEnd()}…` : label;
  return { h: H, out: [
    box(x, y, w, H, fill, dark ? V.lineDark : V.line, 1),
    box(x, y, 3, H, colour),
    tx(lab, x + 13, y + 7, w - 22, T.label + 4, { size: T.label, bold: true, color: colour, caps: true }),
    tx(body, x + 13, y + 7 + T.label + 5, w - 26, bh + 3, { size, color: dark ? '#C9D6E2' : V.ink }),
  ] };
}
const EX = makeExhibits({ jsx, C, Text, Shape, textStyle, stroke, V, RAMP, T, SERIF, textH });
const cap = (s, n) => (String(s).length > n ? `${String(s).slice(0, n - 1).trimEnd()}…` : String(s));
const SA = makeStoryAssets({ jsx, C, Text, Shape, textStyle, stroke, V, RAMP, T, SERIF, textH });

const STATUS_COLOUR = (s, r) =>
  /verified fact/i.test(s) ? r.verified : /insufficient/i.test(s) ? r.red
  : /attributed|qualified/i.test(s) ? r.amber : r.accent;

const PATTERN = {
  P1: { name: 'Evidence ladder', exhibitLabel: 'Rung width = confidence' },
  P2: { name: 'Threat × arena', exhibitLabel: 'Bar length = rating' },
  P3: { name: 'Staged move', exhibitLabel: 'Sequence · reversibility marked' },
  P4: { name: 'Bounded argument', exhibitLabel: 'Three stances, none softened' },
  P5: { name: 'Dated plan', exhibitLabel: 'Phase width = span in weeks' },
  P6: { name: 'Cost bridge', exhibitLabel: 'Bar height = magnitude' },
  P7: { name: 'Confidence register', exhibitLabel: 'Dots = importance × evidence' },
};
// An object literal would evaluate every branch, so a P4 envelope (no `rungs`)
// threw on the P1 entry. Each arm must stay lazy.
const EX_ROWS = (o) => {
  const t = o.typed;
  switch (o.pattern_id) {
    case 'P1': return t.rungs.length;
    case 'P2': return t.matrix.rows.length;
    case 'P7': return t.claims.length;
    default: return 1;
  }
};
const DARK_PATTERNS = new Set(['P3', 'P5']);
const isDark = (o) => DARK_PATTERNS.has(o.pattern_id)
  || /falsifi|threat|counter-?move|verdict|stop|fund /i.test(o.spine.action_title);

// ── the exhibit for a bound envelope ─────────────────────────────────────
function exhibitFor(o, x, y, w, dark, size, grow = 0) {
  const r = dark ? RAMP.dark : RAMP.light, t = o.typed;
  switch (o.pattern_id) {
    case 'P1':
      return EX.ladder(x, y, w, t.rungs.map((g) => ({ ...g, colour: STATUS_COLOUR(g.status, r) })), dark, size, grow);
    case 'P2':
      return EX.heatmap(x, y, w, t.matrix.arenas, t.matrix.rows, dark, size, grow);
    case 'P3':
      return EX.chain(x, y, w, t.stages.map((s2) => ({
        label: s2.label, text: s2.text,
        colour: s2.reversible ? r.accent : r.red })), dark, size, grow);
    case 'P4': {
      const lab = { taken: 'Position taken', opposing: 'Strongest opposing', bounded: 'Bounded middle' };
      return EX.tristate(x, y, w, t.positions.map((p2) => ({
        label: `${lab[p2.stance]}${p2.supported ? ' · evidence supports' : ''}`,
        text: p2.claim })), dark, size, grow);
    }
    case 'P5':
      return EX.rail(x, y, w, t.phases.map((p2, i) => ({
        when: p2.when, span: p2.span_weeks, label: p2.label, note: p2.artifact,
        colour: [r.accent, r.amber, r.verified, r.red][i % 4] })), dark, size, grow);
    case 'P6':
      return EX.waterfall(x, y, w, 168, t.steps.map((s2) => ({
        ...s2, colour: s2.kind === 'base' ? r.accent : s2.kind === 'target' ? r.verified : r.amber })),
        dark, size, grow);
    case 'P7':
      return EX.register(x, y, w, t.claims.map((c) => ({
        ...c, colour: c.band === 'high' ? r.verified : c.band === 'medium' ? r.amber : r.red })),
        dark, size, grow);
    default:
      return { out: [], h: 0 };
  }
}

// the closing rows each template's OUTPUT INCLUDES actually requires
function closingRows(o) {
  const t = o.typed, s = o.spine;
  switch (o.pattern_id) {
    case 'P1': return [['Evidence gap holding the rating', t.gap, 'red']];
    case 'P2': return [['Why the rating moves between arenas', t.variance_mechanism, 'accent'],
                       ['Signal that would invert the ranking', t.inversion_signal, 'amber']];
    case 'P3': return [['Why they currently win', t.their_mechanism, 'accent'],
                       ['Abandon the move when', t.abandon_when, 'red']];
    case 'P4': return [['What would overturn the chosen stance', t.overturned_by, 'red']];
    case 'P5': return [['The plan stops if', t.stops_if, 'red']];
    case 'P6': return [['Comparability rule', t.comparability_rule, 'amber'],
                       ['Capital gate', t.capital_gate, 'accent']];
    case 'P7': return [['May not appear in client-facing material',
                        t.purge_list.length ? t.purge_list.join(' · ') : '—', 'red'],
                       ['Publication rule', t.publication_rule, 'accent']];
    default: return [['Falsifier', s.falsifier, 'red']];
  }
}

let page = 0;
const stats = [];

// ── cover ────────────────────────────────────────────────────────────────
page += 1;
{
  const s = P.slides.add(); s.setViewportSize(1280, 720);
  s.compose(jsxs(Layers, { width: C.fixed(1280), height: C.fixed(720), children: [
    box(0, 0, 1280, 720, V.pageDark), box(0, 0, 1280, 4, V.accent),
    tx('India ADAS · competitor dossier · bound to the adapted templates', M, 200, 900, 16,
       { size: T.kicker, bold: true, color: V.accent, caps: true }),
    box(M, 226, 88, 2, V.accent),
    tx('Perception-layer acceptance is the strategic gate', M, 248, 1040, 116,
       { size: PT(34), face: SERIF, bold: true, color: V.white }),
    tx('Every page is generated under one of seven prompt templates. The template names the exhibit; '
     + 'the exhibit’s geometry carries the finding. Nothing here is prose arranged into cards.',
       M, 384, 980, 44, { size: T.crumb, color: V.mutedDark }),
    ...[['73', 'Slides bound'], ['7', 'Templates'], ['0', 'Unbound slides'], ['2027', 'AEBS mandate']]
      .flatMap(([n, l], i) => [
        tx(n, M + i * 210, 462, 190, 38, { size: PT(22), face: SERIF, bold: true, color: V.accent }),
        tx(l, M + i * 210, 502, 190, 13, { size: T.foot, bold: true, color: V.mutedDark, caps: true })]),
    box(M, FOOT_Y - 10, LIVE, 1, V.lineDark),
    tx('DeepGrid Semi · India ADAS competitor dossier · Confidential', M, FOOT_Y, 820, 12,
       { size: T.foot, color: V.mutedDark, caps: true }),
  ] }));
  s.speakerNotes.text = 'Cover. Design authority: supplied v7 dossier. Structure authority: the adapted prompt-template deck.';
  stats.push({ page, kind: 'cover', dark: true });
}

// ── one page per bound envelope ──────────────────────────────────────────
function renderContent(o) {
  page += 1;
  const e = o.spine, dark = isDark(o);
  const r = dark ? RAMP.dark : RAMP.light;
  const cardBg = dark ? V.cardDark : V.cardLight;
  const el = [box(0, 0, 1280, 720, dark ? V.pageDark : V.pageLight)];
  const meta = PATTERN[o.pattern_id];

  // header: the template it was generated under is stated on the page
  el.push(box(M, 22, 3, 13, r.accent));
  el.push(tx(`${o.pattern_id} · ${meta.name}`, M + 10, 23, 420, 13,
             { size: T.kicker, bold: true, color: r.accent, caps: true }));
  el.push(tx(meta.exhibitLabel, M + 430, 23, 754, 13,
             { size: T.kicker, color: dark ? V.mutedDark : V.muted, caps: true, align: 'right' }));
  const tl = Math.min(2, Math.max(1, Math.ceil(e.action_title.length / 76)));
  el.push(tx(e.action_title, M, 40, LIVE, tl * (T.title + 6),
             { size: T.title, face: SERIF, bold: true, color: dark ? V.white : V.ink }));
  let top = 40 + tl * (T.title + 6) + 6;
  el.push(box(M, top, LIVE, 2, V.accent)); top += 8;
  if (e.analytical_question) {
    el.push(tx(e.analytical_question, M, top, LIVE, 13,
               { size: T.crumb, color: dark ? V.mutedDark : V.muted }));
    top += 19;
  }

  const answer = o.typed.observable_position || o.typed.target_outcome || e.executive_answer;
  const rows = closingRows(o).filter(([, t2]) => t2 && String(t2).trim());

  const lay = (size, grow = 0) => {
    const out = []; let y = top;
    const a = panel(M, y, LIVE, o.pattern_id === 'P1' ? 'Observable position' : 'Executive answer',
                    answer, r.accent, T.lead, dark, cardBg);
    out.push(...a.out); y += a.h + GUT;
    const ex = exhibitFor(o, M, y, LIVE, dark, size, grow);
    out.push(...ex.out); y += ex.h + 4;
    if (o.pattern_id === 'P6' && o.typed.steps.some((s3) => !s3.verified)) {
      out.push(tx('Directional only — illustrative magnitudes, not verified quotations or BOM costs.',
                  M, y, LIVE, 14, { size: T.foot, bold: true, color: r.amber, caps: true }));
      y += 18;
    }
    y += GUT - 4;
    if (rows.length === 2) {
      const w = (LIVE - GUT) / 2;
      const hs = rows.map(([l, t2, c]) => panel(M, y, w, l, t2, r[c], size, dark,
        dark ? V.cardDark : (c === 'amber' ? V.amberTint : V.cardLight)));
      const H = Math.max(hs[0].h, hs[1].h);
      rows.forEach(([l, t2, c], i) => {
        const p2 = panel(M + i * (w + GUT), y, w, l, t2, r[c], size, dark,
          dark ? V.cardDark : (c === 'amber' ? V.amberTint : V.cardLight));
        out.push(...p2.out);
      });
      y += H + GUT;
    } else if (rows.length === 1) {
      const [l, t2, c] = rows[0];
      const p2 = panel(M, y, LIVE, l, t2, r[c], size, dark,
        dark ? V.cardDark : (c === 'amber' ? V.amberTint : V.cardLight));
      out.push(...p2.out); y += p2.h + GUT;
    }
    return { out, bottom: y - GUT };
  };

  let laid = null, chosen = PT(8);
  for (const size of [T.body, PT(10), PT(9.5), PT(9), PT(8.5), PT(8)]) {
    const t2 = lay(size, 0);
    if (t2.bottom <= BODY_BOT) { laid = t2; chosen = size; break; }
  }
  if (!laid) { laid = lay(PT(8), 0); stats.push({ overflow: page, src: o.slide_id }); }
  else {
    // Leftover height grows the exhibit rows. Distributing it as gaps instead
    // just moves the empty space around, which is what the previous build did.
    const slack = BODY_BOT - laid.bottom;
    if (slack > 20) {
      const grow = Math.min(160, Math.floor(slack / EX_ROWS(o)));
      const g2 = lay(chosen, grow);
      if (g2.bottom <= BODY_BOT) laid = g2;
    }
  }
  el.push(...laid.out);

  // decision band — decision · owner · trigger · stop rule
  const by = 720 - 44 - BAND_H;
  el.push(box(M, by, LIVE, BAND_H, dark ? V.band : V.pageDark));
  el.push(box(M, by, 3, BAND_H, V.accent));
  // Three columns, not two. Owner+trigger+stop crammed into one 438px column
  // wrapped to two lines that printed past the band — invisible in the HTML
  // render, obvious in the native PowerPoint one.
  const bandCols = [
    ['Decision', e.decision || e.implication || '', V.accent, M + 16, 516, T.band],
    ['Owner · trigger', [e.owner && `Owner · ${e.owner}`, e.trigger && `Trigger · ${e.trigger}`]
      .filter(Boolean).join('\n'), V.mutedDark, M + 552, 300, T.foot],
    ['Stop / escalate', e.stop_or_escalate_rule || '—', RAMP.dark.amber, M + 872, LIVE - 888, T.foot],
  ];
  bandCols.forEach(([label, body, col, x, w, size]) => {
    el.push(tx(label, x, by + 8, w, 11, { size: T.label, bold: true, color: col, caps: true }));
    el.push(tx(cap(body, 168), x, by + 22, w, BAND_H - 28,
               { size, color: label === 'Decision' ? V.white : col }));
  });

  el.push(box(M, FOOT_Y - 10, LIVE, 1, dark ? V.lineDark : V.line));
  el.push(tx('DeepGrid Semi · India ADAS competitor dossier · Confidential', M, FOOT_Y, 820, 12,
             { size: T.foot, color: dark ? V.mutedDark : V.muted, caps: true }));
  el.push(tx(String(page), 1152, FOOT_Y, 40, 12,
             { size: T.foot, bold: true, color: dark ? V.mutedDark : V.muted, align: 'right' }));

  const s = P.slides.add(); s.setViewportSize(1280, 720);
  s.compose(jsxs(Layers, { width: C.fixed(1280), height: C.fixed(720), children: el }));
  s.speakerNotes.text =
    `Generated under ${o.pattern_id} · ${meta.name} (exhibit: ${o.exhibit}).\n`
  + `Bind status: ${o.bind.status}${o.bind.reason ? ` — ${o.bind.reason}` : ''}\n\n`
  + `Q: ${e.analytical_question}\nA: ${e.executive_answer}\n\n`
  + `Mechanism: ${(e.logic || {}).mechanism || ''}\n`
  + `Counterargument: ${e.counterargument || ''}\nFalsifier: ${e.falsifier || ''}\n`
  + `Implication: ${e.implication || ''}\nDecision: ${e.decision || ''}\n`
  + `Owner: ${e.owner || ''} · Trigger: ${e.trigger || ''}\n`
  + `Stop/escalate: ${e.stop_or_escalate_rule || ''}\n\n`
  + `Evidence: ${(e.evidence_ids || []).join(', ')}\n${e.source_note || ''}`;
  stats.push({ page, src: o.slide_id, pattern: o.pattern_id, exhibit: o.exhibit, dark });
}

// ── the story layer, then the acts ───────────────────────────────────────
const BY_ID = new Map(BOUND.map((o) => [o.slide_id, o]));
const chrome = (dark, label) => {
  const el = [box(M, FOOT_Y - 10, LIVE, 1, dark ? V.lineDark : V.line)];
  el.push(tx(label, M, FOOT_Y, 820, 12,
             { size: T.foot, color: dark ? V.mutedDark : V.muted, caps: true }));
  el.push(tx(String(page), 1152, FOOT_Y, 40, 12,
             { size: T.foot, bold: true, color: dark ? V.mutedDark : V.muted, align: 'right' }));
  return el;
};
const FOOT = 'DeepGrid Semi · India ADAS competitor dossier · Confidential';
function addPage(children, notes, dark, kind) {
  page += 1;
  const s = P.slides.add(); s.setViewportSize(1280, 720);
  s.compose(jsxs(Layers, { width: C.fixed(1280), height: C.fixed(720),
                           children: [...children, ...chrome(dark, FOOT)] }));
  s.speakerNotes.text = notes;
  stats.push({ page, kind, dark });
}

// front matter: storyboard, pyramid, what live research changed
const STORY_FRONT = 4;                 // cover + these three, before Act I opens
addPage(SA.storyboardPage(NAR, STORY_FRONT), `Storyboard.\n\n${NAR.core_message}`, true, 'storyboard');
addPage(SA.pyramidPage(NAR), `Pyramid.\n\nGoverning thought: ${NAR.pyramid.governing_thought}`,
        false, 'pyramid');
addPage(SA.deltaPage(DELTA, DELTA_IMG),
        `Evidence delta, ${DELTA.generated}.\n${DELTA.method}\n\n`
        + DELTA.deltas.map((d) => `${d.id} ${d.entity}: ${d.rating_move}\n  source: ${d.source}`).join('\n'),
        false, 'delta');

NAR.acts.forEach((act, i) => {
  const first = page + 2, last = page + 1 + act.slides.length;
  addPage(SA.actDivider(act, i, first, last),
          `${act.no} · ${act.name}\n\nQ: ${act.question}\nSettles: ${act.settles}`, true, 'divider');
  act.slides.forEach((sid) => renderContent(BY_ID.get(sid)));
});

addPage(SA.hostilePage(NAR.hostile_questions),
        'Hostile questions.\n\n'
        + NAR.hostile_questions.map(([q, a]) => `Q: ${q}\nA: ${a}`).join('\n\n'), false, 'hostile');

const OUT = `${RUN}/${process.env.DECK_NAME || 'deck'}-draft.pptx`;
await (await PresentationFile.exportPptx(P)).save(OUT);
await mkdir(`${RUN}/qa`, { recursive: true });
await writeFile(`${RUN}/qa/bound-layout-stats.json`, JSON.stringify(stats, null, 1));
const byPat = {};
stats.filter((s) => s.pattern).forEach((s) => { byPat[s.pattern] = (byPat[s.pattern] || 0) + 1; });
console.log(`DONE: ${P.slides.count} slides -> ${OUT}`);
console.log(`  exhibits: ${JSON.stringify(byPat)}`);
console.log(`  dark ${stats.filter((s) => s.dark).length} · overflow ${stats.filter((s) => s.overflow).length}`);

if (process.env.DECK_RENDER) {
  const dir = `${RUN}/qa/renders-bound`;
  await mkdir(dir, { recursive: true });
  for (let i = 0; i < P.slides.count; i += 1) {
    const b = await P.export({ format: 'png', slide: P.slides.getItem(i), scale: 1 });
    await writeFile(`${dir}/slide-${String(i + 1).padStart(3, '0')}.png`, Buffer.from(await b.arrayBuffer()));
  }
  console.log(`  rendered ${P.slides.count} PNGs -> ${dir}`);
}
