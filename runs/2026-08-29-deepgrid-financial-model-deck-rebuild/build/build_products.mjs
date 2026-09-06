import { P, C, K, SERIF, addSlide, tx, rect, roundRect, ellipse, sh,
         PresentationFile, OUT, PX, T, divider, SRC, barsNative,
         CY, TL, GR, PB, SL, GY, CYT, PBT, TLT,
         hdr, TH, CARD, CARDH, KPI, TBL, flow, VIOLATIONS } from './deck-lib.mjs';
import { PRODUCTS, BY_SEGMENT, FYS } from './data_products.mjs';


// Compact KPI for the product slides: numeral + label, no note row.
function KPI2(x, y, w, num, label, color = CY) {
  const lH = TH(label.toUpperCase(), w - 24, T.kpiLab);
  const H = 24 + 58 + 10 + lH + 18;
  const fits = Math.max(4, Math.floor((w - 16) / (0.612 * T.kpiNum)));
  const nSize = String(num).length <= fits ? T.kpiNum
              : Math.max(PX(20), Math.floor(T.kpiNum * fits / String(num).length));
  return [
    roundRect(x, y, w, H, K.surface, K.line, 1),
    tx(num, x, y + 24, w, 58, { size: nSize, face: SERIF, bold: true, color, align: 'center' }),
    tx(label.toUpperCase(), x + 12, y + 92, w - 24, lH, { size: T.kpiLab, bold: true, color: SL, align: 'center' }),
  ];
}

const S = [];
const add = (children, opts = {}) => S.push([children, opts]);
let pg = 0; const N = () => ++pg;
const cr = v => `₹${v >= 100 ? Math.round(v) : v.toFixed(v < 10 ? 2 : 1)} Cr`;

// Compact six-year unit ramp: label over count, one cell per year.
function rampStrip(x, y, w, units) {
  const n = units.length, gap = 10, cw = (w - (n - 1) * gap) / n;
  const e = [tx('UNITS SHIPPED', x, y - 22, 400, 18,
    { size: T.kicker, bold: true, color: CYT })];
  units.forEach((v, i) => {
    const cx = x + i * (cw + gap), hot = i === n - 1;
    e.push(roundRect(cx, y, cw, 50, hot ? K.softCyan : K.surface, hot ? CY : K.line, 1));
    e.push(tx(FYS[i], cx, y + 5, cw, 15, { size: T.kicker, bold: true, color: hot ? SL : GY, align: 'center' }));
    e.push(tx(v.toLocaleString('en-IN'), cx, y + 22, cw, 24,
      { size: T.cardH, bold: true, color: hot ? CYT : SL, align: 'center' }));
  });
  return e;
}

// ============================== 1. COVER =====================================
{
  const p = N();
  add([
    rect(0, 0, 1280, 720, K.midnight),
    ...Array.from({ length: 11 }, (_, i) => rect(864 + i * 38, 0, 1, 720, '#14263C')),
    rect(0, 0, 1280, 5, CY),
    ellipse(940, 150, 300, 300, '#0E1E33', '#16304C', 2),
    ellipse(1000, 210, 180, 180, '#101F36', CY, 1),
    tx('STRICTLY CONFIDENTIAL  ·  PRE-SERIES A', 80, 110, 700, 24, { size: T.kicker, bold: true, color: CY }),
    tx('Product Lines', 80, 168, 900, 86, { size: T.cover, face: SERIF, bold: true, color: K.white }),
    tx('Thirteen lines, one chip', 80, 268, 900, 56, { size: PX(26), face: SERIF, color: '#A9BACD' }),
    rect(80, 348, 150, 3, CY),
    tx('What each product is, who buys it, and the sized demand pool behind it.',
       80, 382, 760, 54, { size: PX(14), color: '#8FA2B7' }),
    roundRect(80, 470, 300, 96, '#0E1E33', '#1B3350', 1),
    tx('₹1,128 Cr', 104, 492, 260, 44, { size: PX(28), face: SERIF, bold: true, color: K.white }),
    tx('FY2032 REVENUE, ALL LINES', 104, 540, 260, 20, { size: T.kicker, bold: true, color: CY }),
    roundRect(400, 470, 300, 96, '#0E1E33', '#1B3350', 1),
    tx('13', 424, 492, 260, 44, { size: PX(28), face: SERIF, bold: true, color: K.white }),
    tx('PRODUCT LINES · 15 SKUs', 424, 540, 260, 20, { size: T.kicker, bold: true, color: CY }),
    tx('All figures are management projections prepared for fundraising purposes.',
       80, 616, 1000, 22, { size: T.foot, italic: true, color: '#6E8299' }),
    tx('August 2026', 80, 644, 400, 22, { size: T.foot, bold: true, color: '#8FA2B7' }),
  ], { background: K.midnight, notes:
    'Companion deck to the financial model walkthrough. Units and price from Revenue Build D44:J58; '+
    'demand pools, capture rates and sources from the Demand & TAM worksheet, section B (rows 22-33).' });
}

// ============================== 2. PORTFOLIO TABLE ===========================
{
  const p = N();
  const rows = PRODUCTS.map(x => [x.name, x.asp,
    x.units[5].toLocaleString('en-IN'), cr(x.rev), `${x.share.toFixed(1)}%`, x.gm]);
  add([
    ...hdr('Portfolio', 'Thirteen lines, and two carry 64%',
      'AD2 and AD0 carry ₹720 Cr; the other eleven share ₹408 Cr. Prices hold flat.', p),
    ...(() => { const f = flow(170, 'p2'); return [
      ...f.tbl(48, 1184, [
        { t: 'Product line', w: 330 }, { t: 'Unit price', w: 150, a: 'right' },
        { t: 'FY2032 units', w: 170, a: 'right' }, { t: 'FY2032 revenue', w: 180, a: 'right' },
        { t: 'Share', w: 130, a: 'right' }, { t: 'Gross margin', w: 224, a: 'right' }],
        rows, { headH: 34, highlight: 0 }),
    ]; })(),
  ], { notes: 'Source: Revenue Build D44:J58 (units, price) and E61:J75 (derived revenue); '+
    'Assumptions C25:H28 (segment gross margin). Shares of ₹1,128.45 Cr.' });
}

// ============================== 3. SEGMENT SPLIT =============================
{
  const p = N();
  add([
    ...hdr('Where the margin sits', 'Systems carry revenue, silicon carries margin',
      'Four segments, each with its own margin path to FY2032.', p),
    ...KPI(48, 178, 286, '83.4%', 'Systems share', '₹941 Cr at 89% margin', CYT),
    ...KPI(348, 178, 286, '94%', 'Semiconductor margin', 'Highest in the portfolio', TLT),
    ...KPI(648, 178, 286, '50%', 'Sensor margin', 'Lowest — a capability line', PBT),
    ...KPI(948, 178, 284, '68%', 'Robotics margin', 'Defence and drone platforms', GR),
    ...(() => { const f = flow(344, 'p3'); return [
      ...f.tbl(48, 1184, [
        { t: 'Segment', w: 330 }, { t: 'FY2032 revenue', w: 250, a: 'right' },
        { t: 'Share of revenue', w: 250, a: 'right' }, { t: 'FY2032 gross margin', w: 354, a: 'right' }],
        BY_SEGMENT.map(s => [s[0], cr(s[1]), `${s[2]}%`, s[3]]), { headH: 34, highlight: 0 }),
      ...f.cards([[48, 1184, 'Read the two together',
        'Systems are 83.4% of revenue at 89% margin, so group economics track that line. Semiconductors are 9.2% of revenue at 94% margin — the most profitable revenue we can add.',
        CYT, K.cool]]),
    ]; })(),
  ], { notes: 'Source: Revenue Build E16:J21; Assumptions C25:H28.' });
}

// ============================== 4. REVENUE CONCENTRATION ====================
{
  const p = N();
  const segColour = g => g === '89%' ? CY : g === '94%' ? TL : g === '68%' ? GR : PB;
  const short = n => n.replace(/\s*\([^)]*\)/g, '').replace('driver-monitor wearable', 'driver monitor');
  const rows = [...PRODUCTS].sort((a, b) => b.rev - a.rev)
    .map(x => [short(x.name), x.rev, segColour(x.gm), cr(x.rev)]);
  add([
    ...hdr('Concentration', 'Two lines carry 64%, eleven carry the rest',
      'FY2032 revenue by product line. Colour shows segment: systems, silicon, robotics, sensors.', p),
    ...barsNative(48, 186, 1184, rows, { rowH: 29, labelW: 320, valW: 120, max: 460 }),
    ...(() => { const f = flow(578, 'p4', 646); return [
      ...f.note('AD2 and AD0 are both road-autonomy systems sold to overlapping buyers, so a certification or installation delay hits ₹720 Cr at once — not two independent lines.'),
    ]; })(),
  ], { notes: 'Source: Revenue Build E61:J75. Bars are FY2032 revenue in ₹ Cr against a 460 Cr axis.' });
}

// ============================== 5. CAPTURE HEADROOM =========================
{
  const p = N();
  const sized = PRODUCTS.filter(x => x.capture !== '—');
  const short = n => n.replace(/\s*\([^)]*\)/g, '').replace('driver-monitor wearable', 'driver monitor');
  const rows = sized.map(x => [short(x.name), parseFloat(x.capture),
    parseFloat(x.capture) > 1 ? CY : PB, x.capture]);
  add([
    ...hdr('Headroom', 'No line assumes we win its market',
      'FY2032 share of each product\'s own sized demand pool. Axis runs to 2%.', p),
    ...barsNative(48, 190, 1184, rows, { rowH: 38, labelW: 320, valW: 110, max: 2.0 }),
    ...(() => { const f = flow(490, 'p5', 646); return [
      ...f.cards([
        [48, 592, 'Why the shares look small',
         'Most pools are global while our serviceable market is the India slice, so the real share is higher. Five lines have no sized pool and are excluded.', CYT],
        [656, 576, 'The one to read differently',
         'Seaport AGV shows 0.02% against a pool that is total port automation, cranes and software included. We sell only the vehicle layer.', TLT],
      ]),
    ]; })(),
    tx('Demand pool sources per line are shown on each product slide. Capture rates are management assumptions.',
       48, 652, 1184, 20, { size: T.foot, italic: true, color: GY }),
  ], { notes: 'Source: Demand & TAM section B, capture column E22:E33. Eight of thirteen lines carry a '+
    'numeric capture rate; AD1, H100, D-HUMR, D100 and T100 have no separately sized pool.' });
}

// ============================== 4..16 PRODUCT SLIDES =========================
for (const x of PRODUCTS) {
  const p = N();
  add([
    ...hdr(x.kicker, x.title, x.tag, p),
    ...KPI2(48, 178, 286, x.units[5].toLocaleString('en-IN'), 'FY2032 units', CYT),
    ...KPI2(348, 178, 286, x.asp, 'Unit price', TLT),
    ...KPI2(648, 178, 286, cr(x.rev), 'FY2032 revenue', GR),
    ...KPI2(948, 178, 284, x.share.toFixed(1) + '%', 'Share of FY2032', PBT),
    ...(() => { const f = flow(326, 'p-' + x.slug, 646); return [
      ...f.cards([[48, 1184, 'What it is, and who buys it', x.what + ' ' + x.buyer, CYT]]),
      ...f.cards([[48, 1184, 'Demand pool · ' + x.capture + ' capture at FY2032',
                   x.pool + '. ' + x.why, TLT, K.cool]]),
    ]; })(),
    tx('Units ' + x.units[0].toLocaleString('en-IN') + ' in FY2027 to ' +
       x.units[5].toLocaleString('en-IN') + ' in FY2032 at ' + x.asp + ' held flat · ' +
       x.gm + ' segment gross margin · demand pool source: ' + x.source + '.',
       48, 652, 1184, 20, { size: T.foot, italic: true, color: GY }),
  ], { notes:
    `${x.name}. Units ${x.units.join(' / ')} across FY2027-FY2032 at ${x.asp}, giving ${cr(x.rev)} in FY2032 `+
    `(${x.share.toFixed(1)}% of ₹1,128.45 Cr) at ${x.gm} segment gross margin. `+
    `Demand pool and capture from Demand & TAM section B; source: ${x.source}. Units and price are from the revenue build; capture rates are management assumptions.` });
}

for (const [children, opts] of S) addSlide(children, opts);
if (VIOLATIONS.length) { console.log('LAYOUT VIOLATIONS:'); VIOLATIONS.forEach(v => console.log('  ' + v)); }
else console.log('layout guard: clean');
await (await PresentationFile.exportPptx(P)).save(OUT);
console.log(`OK slides=${S.length} -> ${OUT}`);
