// build_v7_deck.mjs — DeepGrid India ADAS competitor dossier, built on the v7 design authority.
//
// DESIGN: measured from the user-supplied `source-reference-v7.pptx`, not assumed.
//   The PPTX theme is stock Office (Calibri / #4F81BD) and carries none of the design —
//   every decision is applied through shape fills and run fonts, so the tokens below come
//   from counting all 80 slides and sampling rendered pixels. See v7-design-notes.md.
// CONTENT: the validated 73-slide Genspark model (slide-model.json), which the
//   export-coverage gate proved complete.
// GRAMMAR: this skill's Accenture analytical grammar — kicker, action title, cyan rule,
//   breadcrumb, status-coded evidence rows, falsifier on the page, closing decision band.
//
//   DECK_RUN=<dir> DECK_NAME=<slug> [DECK_RENDER=1] node src/build_v7_deck.mjs
import { readFile, writeFile, mkdir } from 'node:fs/promises';

const AT = process.env.ARTIFACT_TOOL_DIST || 'file:///home/sheke/.local/artifact-tool-linux/dist';
const { Presentation, PresentationFile, layers: composeLayers } = await import(`${AT}/artifact_tool.mjs`);
const { textStyle, stroke } = await import(`${AT}/presentation-jsx/index.mjs`);
const { jsx, jsxs } = await import(`${AT}/presentation-jsx/jsx-runtime.mjs`);

const RUN = process.env.DECK_RUN || '.';
const MODEL = JSON.parse(await readFile(`${RUN}/slide-model.json`, 'utf8'));

// ── measured v7 tokens ───────────────────────────────────────────────────
const V = {
  pageLight: '#FFFFFF', pageDark: '#081525',
  cardLight: '#F1F7F9', cardDark: '#10263A',
  band: '#101827', bandCyan: '#04B3C7',
  accent: '#04B3C7', accentDeep: '#176C80',
  ink: '#101827', white: '#FFFFFF',
  muted: '#65707E', mutedDark: '#8EA0B2',
  line: '#D8E2E7', lineDark: '#1A2F45',
  green: '#16835C', amber: '#C96A0A', red: '#C62828', amberTint: '#FFF7EC',
};
const SERIF = 'Georgia', SANS = 'Arial';
const PT = (pt) => pt / 0.75;                       // stage px per point

// v7 type scale (measured run sizes: title 19-22pt, body 8-12pt, caption 6-7pt)
const T = { title: PT(19), kicker: PT(6.5), crumb: PT(7.5), chip: PT(6),
            body: PT(9), lead: PT(10.5), band: PT(9.5), foot: PT(6.5), metric: PT(22) };

const M = 48, LIVE = 1184, GUT = 12;
const BODY_TOP = 126, BODY_BOT = 592;
const BAND_Y = 600, BAND_H = 46;
const FOOT_Y = 676;

const P = Presentation.create();
const C = P.compose;
const Text = ({ children = '', ...props }) => C.text(String(children), props);
const Shape = (props) => C.shape(props);
const Layers = ({ children = [], ...props }) =>
  composeLayers(props, Array.isArray(children) ? children : [children]);

const st = ({ size = T.body, face = SANS, color = V.ink, bold = false, align = 'left',
              anchor = 'top', caps = false }) =>
  textStyle(`font: ${bold ? 'bold ' : ''}${size}px ${face}; color: ${color}; align: ${align}; `
          + `anchor: ${anchor}; inset: 0px; autofit: shrink`);
const tx = (t, x, y, w, h, o = {}) => jsx(Text, {
  width: C.fixed(Math.max(4, w)), height: C.fixed(Math.max(6, h)),
  position: { left: x, top: y }, style: st(o),
  children: o.caps ? String(t).toUpperCase() : t });
const box = (x, y, w, h, fill, lc = 'none', lw = 0) => jsx(Shape, {
  geometry: 'rect', width: C.fixed(Math.max(1, w)), height: C.fixed(Math.max(1, h)),
  fill, line: lc === 'none' ? stroke('0px none') : stroke(`${lw}px solid ${lc}`),
  position: { left: x, top: y } });

// crude but stable text measurement — Arial at ~0.52em average advance
const textH = (s, w, size, lh = 1.34) => {
  const cpl = Math.max(8, Math.floor(w / (size * 0.50)));
  const lines = String(s).split('\n')
    .reduce((n, p) => n + Math.max(1, Math.ceil(p.length / cpl)), 0);
  return Math.ceil(lines * size * lh);
};

// ── evidence status → colour (v7 reserves colour for status, never decoration)
// v7 uses one status hue on both grounds, which measures 2.35:1 for cyan on the
// light card and 2.75:1 for red on the dark card — well under the 4.5:1 the
// quality gate enforces. Same hues, two calibrated ramps: darkened for the light
// ground, lightened for the dark one. Identity is preserved; legibility is not
// left to chance.
const STATUS_KEYS = [
  ['verified', /verified|confirmed|proven/i],
  ['red',      /insufficient|unverified|gap|contested|not proven|missing/i],
  ['amber',    /qualified|attributed|company claim|issuer|partial|pending|monitor|watchlist/i],
];
const RAMP = {
  light: { accent: '#037A87', verified: '#157F59', amber: '#AB5A08', red: '#C62828' },
  dark:  { accent: '#04B3C7', verified: '#1BA271', amber: '#D7720B', red: '#E06767' },
};
const statusOf = (s, dark) => {
  const ramp = dark ? RAMP.dark : RAMP.light;
  for (const [k, re] of STATUS_KEYS) if (re.test(s)) return ramp[k];
  return ramp.accent;
};

const ENTITIES = ['Starkenn', 'Gahan', 'drivebuddyAI', 'STRADVISION', 'Netrasemi', 'bitsensing',
                  'Sterling', 'MINIEYE', 'Aptiv', 'ZF', 'Bosch', 'Continental', 'Valeo'];

function kickerOf(s) {
  const t = s.title;
  const e = ENTITIES.find((x) => t.toLowerCase().includes(x.toLowerCase()));
  if (/falsifi/i.test(t))              return e ? `${e} · falsifier` : 'Falsifier';
  if (/heatmap|threat .*arena|by arena/i.test(t)) return e ? `${e} · threat by arena` : 'Threat by arena';
  if (/counter-?move|battlecard|response/i.test(t)) return e ? `${e} · counter-move` : 'Counter-move';
  if (/profile|dossier|anatomy|evidence assessment/i.test(t)) return e ? `${e} · competitor anatomy` : 'Competitor anatomy';
  if (e)                               return `${e} · evidence`;
  if (/pricing|cost|economic|asic|fpga/i.test(t)) return 'Economics';
  if (/decision|fund|stop|board|message|next 90|roadmap/i.test(t)) return 'Decision';
  if (/rubric|scorecard|confidence|method|evidence ladder/i.test(t)) return 'Method';
  return 'Position';
}
// v7 runs roughly half dark: mechanism, threat and decision pages carry the dark ground.
const isDark = (t) => /falsifi|threat|counter-?move|mechanism|decision|verdict|stop|fund |pause |board|message/i.test(t);

// ── content shaping ──────────────────────────────────────────────────────
const CLOSER = /^(strategic implication|implication|decision|next steps?|so what|bounded verdict|verdict|recommendation|action items?|next actions?)$/i;

function shape(sl) {
  const blocks = sl.blocks.map((b) => ({ ...b }));
  // the closing band takes the decision/implication block
  let closer = null;
  const body = [];
  for (const b of blocks) {
    if (!closer && b.heading && CLOSER.test(b.heading.trim())) { closer = b; continue; }
    body.push(b);
  }
  if (!closer && body.length) closer = body.pop();
  return { body, closer };
}

// row banding keeps matrices reading as matrices (threat x arena pages)
function rows(bs) {
  const s = [...bs].sort((a, b) => (a.y - b.y) || (a.x - b.x));
  const out = [];
  for (const b of s) {
    const last = out[out.length - 1];
    if (last && b.y - last.y0 < 46) last.items.push(b);
    else out.push({ y0: b.y, items: [b] });
  }
  out.forEach((r) => r.items.sort((a, b) => a.x - b.x));
  const wrapped = [];
  for (const r of out) for (let i = 0; i < r.items.length; i += 4) wrapped.push(r.items.slice(i, i + 4));
  return wrapped;
}

const cardOf = (b) => {
  const rest = [...b.body];
  const label = b.heading || rest.shift() || '';
  // Ordered-list markers were captured as their own tags/blocks, so cards were
  // rendering with a claim of "1 · 2 · 3" or a bare "1". They carry no meaning.
  const NUMERIC = /^[\d\s·.,:;()-]*$/;
  const tags = b.tags.filter((t) => t && t !== label && !NUMERIC.test(t));
  let claim = rest.join(' ').trim();
  // A card with a label and nothing else renders as an empty box. The status
  // tag IS the claim in that case — that is how v7 shows a bare status row.
  if (!claim) claim = tags.join('  ·  ');
  return { label, claim, status: tags[0] || '', key: [label, ...tags].join(' ') };
};
// Drop blocks that carry no content at all; they were producing empty cards and
// one fully blank row on the Aptiv page.
const hasContent = (b) => {
  const c = cardOf(b);
  const NUMERIC = /^[\d\s·.,:;()-]*$/;
  if (NUMERIC.test(c.label) && NUMERIC.test(c.claim)) return false;
  return !!(c.label.trim() || c.claim.trim());
};

let page = 0;
const stats = [];

// ── cover ────────────────────────────────────────────────────────────────
page += 1;
{
  const s = P.slides.add(); s.setViewportSize(1280, 720);
  s.compose(jsxs(Layers, { width: C.fixed(1280), height: C.fixed(720), children: [
    box(0, 0, 1280, 720, V.pageDark),
    box(0, 0, 1280, 4, V.accent),
    tx('India ADAS · competitor dossier', M, 214, 900, 16, { size: T.kicker, bold: true, color: V.accent, caps: true }),
    box(M, 240, 88, 2, V.accent),
    tx('Perception-layer acceptance is the strategic gate',
       M, 262, 1050, 120, { size: PT(34), face: SERIF, bold: true, color: V.white }),
    tx('Who occupies each buying arena, what the evidence actually supports, and the four gates worth funding',
       M, 400, 900, 40, { size: T.crumb, color: V.mutedDark }),
    ...[['10', 'Competitors assessed'], ['4', 'Evidence gates'], ['3', 'Priority threats'], ['2027', 'AEBS mandate']]
      .flatMap(([n, l], i) => [
        tx(n, M + i * 210, 470, 190, 40, { size: T.metric, face: SERIF, bold: true, color: V.accent }),
        tx(l, M + i * 210, 512, 190, 14, { size: T.foot, bold: true, color: V.mutedDark, caps: true })]),
    box(M, FOOT_Y - 10, LIVE, 1, V.lineDark),
    tx('DeepGrid Semi · India ADAS competitor dossier · Confidential', M, FOOT_Y, 800, 12,
       { size: T.foot, color: V.mutedDark, caps: true }),
  ] }));
  s.speakerNotes.text = 'Cover. Design derived from the supplied v7 dossier; content from the validated India ADAS evidence base.';
  stats.push({ page, kind: 'cover', dark: true });
}

// ── interior ─────────────────────────────────────────────────────────────
MODEL.slides.forEach((sl) => {
  page += 1;
  const dark = isDark(sl.title);
  const pg = dark ? V.pageDark : V.pageLight;
  const cardBg = dark ? V.cardDark : V.cardLight;
  const cardLn = dark ? V.lineDark : V.line;
  const titleC = dark ? V.white : V.ink;
  const crumbC = dark ? V.mutedDark : V.muted;
  const bodyC = dark ? '#C9D6E2' : V.ink;

  const { body, closer } = shape(sl);
  const banded = rows(body.filter(hasContent));

  const el = [box(0, 0, 1280, 720, pg)];
  // header
  el.push(tx(kickerOf(sl), M, 26, 800, 14, { size: T.kicker, bold: true, color: dark ? V.accent : RAMP.light.accent, caps: true }));
  const tLines = Math.min(2, Math.max(1, Math.ceil(sl.title.length / 74)));
  el.push(tx(sl.title, M, 44, LIVE, tLines * (T.title + 6),
             { size: T.title, face: SERIF, bold: true, color: titleC }));
  let y = 44 + tLines * (T.title + 6) + 8;
  el.push(box(M, y, LIVE, 2, V.accent)); y += 10;
  if (sl.subtitle) { el.push(tx(sl.subtitle, M, y, LIVE, 14, { size: T.crumb, color: crumbC })); y += 20; }

  // evidence rows — search type size down until the band fits
  const top = Math.max(y, BODY_TOP);
  const avail = BODY_BOT - top;
  let placed = null;
  for (const size of [T.body, PT(8.5), PT(8)]) {
    const out = []; let yy = top;
    for (const row of banded) {
      const n = row.length;
      const w = (LIVE - GUT * (n - 1)) / n;
      const cards = row.map(cardOf).map((c) => ({ ...c, color: statusOf(c.key, dark) }));
      const h = Math.max(...cards.map((c) => 10 + (size + 3) + 4 + (c.claim ? textH(c.claim, w - 26, size) : 0) + 10));
      cards.forEach((c, i) => out.push({ ...c, x: M + i * (w + GUT), y: yy, w, h, size }));
      yy += h + GUT;
    }
    const used = yy - top - GUT;
    if (used <= avail) {
      // spread the slack so the page reads full, the way v7's pages do
      const nRows = banded.length;
      if (nRows > 1 && avail - used > 24) {
        const extra = Math.min(18, (avail - used) / nRows);
        let shift = 0, lastY = null;
        for (const c of out) {
          if (lastY !== null && c.y !== lastY) shift += extra;
          lastY = c.y; c.y += shift; c.h += extra;
        }
      }
      placed = out; break;
    }
  }
  if (!placed) {
    // Dense pages exhaust the size ladder. The old fallback laid out at 8pt
    // *unconditionally* and ran straight through the body band into the closing
    // decision band — that was every TEXT_BOX_OVERLAP error. Lay out, then
    // compress proportionally so the band boundary is never crossed; the 8pt
    // floor is preserved and autofit:shrink absorbs the text.
    const size = PT(8); const out = []; let yy = top;
    for (const row of banded) {
      const n = row.length; const w = (LIVE - GUT * (n - 1)) / n;
      const cards = row.map(cardOf).map((c) => ({ ...c, color: statusOf(c.key, dark) }));
      const h = Math.max(...cards.map((c) => 10 + (size + 3) + 4 + (c.claim ? textH(c.claim, w - 26, size) : 0) + 10));
      cards.forEach((c, i) => out.push({ ...c, x: M + i * (w + GUT), y: yy, w, h, size }));
      yy += h + GUT;
    }
    const used = yy - top - GUT;
    if (used > avail) {
      const k = avail / used;
      out.forEach((c) => { c.y = top + (c.y - top) * k; c.h = c.h * k; });
    }
    placed = out;
  }

  // Hard bound: nothing may cross into the closing band. Cheap to assert, and it
  // is the exact failure the linter caught.
  placed.forEach((c) => {
    if (c.y + c.h > BODY_BOT) c.h = Math.max(18, BODY_BOT - c.y);
  });

  placed.forEach((c) => {
    el.push(box(c.x, c.y, c.w, c.h, cardBg, cardLn, 1));
    el.push(box(c.x, c.y, 3, c.h, c.color));                       // status accent bar
    el.push(tx(c.label, c.x + 14, c.y + 9, c.w - 24, c.size + 5,
               { size: c.size - 1, bold: true, color: c.color, caps: true }));
    if (c.claim) {
      // Height is the card's remaining space, NOT the estimated text height.
      // textH under-estimates Arial's real advance, so an estimate-sized box
      // spilled past the card into the row beneath it — that was every one of
      // the 29 TEXT_BOX_OVERLAP errors. autofit:shrink absorbs the difference.
      const claimTop = c.y + 9 + c.size + 7;
      el.push(tx(c.claim, c.x + 14, claimTop, c.w - 26,
                 Math.max(10, c.y + c.h - 8 - claimTop), { size: c.size, color: bodyC }));
    }
  });

  // closing decision band — v7 always states the so-what on the page
  if (closer) {
    const c = cardOf(closer);
    el.push(box(M, BAND_Y, LIVE, BAND_H, dark ? V.band : V.pageDark));
    el.push(box(M, BAND_Y, 3, BAND_H, V.accent));
    el.push(tx(c.label || 'Decision', M + 16, BAND_Y + 9, 168, 12,
               { size: T.chip, bold: true, color: V.accent, caps: true }));
    el.push(tx(c.claim || c.status || '', M + 196, BAND_Y + 8, LIVE - 212, BAND_H - 14,
               { size: T.band, color: V.white }));
  }

  // footer
  el.push(box(M, FOOT_Y - 10, LIVE, 1, dark ? V.lineDark : V.line));
  el.push(tx('DeepGrid Semi · India ADAS competitor dossier · Confidential', M, FOOT_Y, 820, 12,
             { size: T.foot, color: dark ? V.mutedDark : V.muted, caps: true }));
  el.push(tx(String(page), 1232 - 40, FOOT_Y, 40, 12,
             { size: T.foot, bold: true, color: dark ? V.mutedDark : V.muted, align: 'right' }));

  const s = P.slides.add(); s.setViewportSize(1280, 720);
  s.compose(jsxs(Layers, { width: C.fixed(1280), height: C.fixed(720), children: el }));
  s.speakerNotes.text = `${sl.title}\n${sl.subtitle}\n\nSource: validated India ADAS evidence base, slide ${sl.n}. `
    + `Design: v7 dossier authority (measured tokens). ${placed.length} evidence rows.`;
  stats.push({ page, src: sl.n, kind: 'evidence-rows', dark, cards: placed.length,
               size: +(placed[0]?.size || 0).toFixed(1) });
});

const OUT = `${RUN}/${process.env.DECK_NAME || 'deck'}-draft.pptx`;
await (await PresentationFile.exportPptx(P)).save(OUT);
await mkdir(`${RUN}/qa`, { recursive: true });
await writeFile(`${RUN}/qa/layout-stats.json`, JSON.stringify(stats, null, 1));
const d = stats.filter((s) => s.dark).length;
console.log(`DONE: ${P.slides.count} slides -> ${OUT}`);
console.log(`  dark ${d} (${Math.round(d / P.slides.count * 100)}%) · evidence rows ${stats.reduce((a, s) => a + (s.cards || 0), 0)}`);

if (process.env.DECK_RENDER) {
  const dir = `${RUN}/qa/renders`;
  await mkdir(dir, { recursive: true });
  for (let i = 0; i < P.slides.count; i += 1) {
    const blob = await P.export({ format: 'png', slide: P.slides.getItem(i), scale: 1 });
    await writeFile(`${dir}/slide-${String(i + 1).padStart(3, '0')}.png`, Buffer.from(await blob.arrayBuffer()));
  }
  console.log(`  rendered ${P.slides.count} PNGs -> ${dir}`);
}
