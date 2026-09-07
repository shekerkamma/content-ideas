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

const S=[]; // slide registry: [children, opts]
const add=(children,opts={})=>S.push([children,opts]);
let pg=0; const N=()=>++pg;

// ============================== 1. COVER =====================================
{
  const p=N();
  add([
    rect(0,0,1280,720,K.midnight),
    // geometric motif — deterministic, native, cannot mis-crop
    ...Array.from({length:11},(_,i)=>rect(864+i*38, 0, 2, 720, i%3===0?'#123css':'#14263C')).map(x=>x),
    rect(0,0,1280,5,CY),
    ellipse(940,150,300,300,'#0E1E33','#16304C',2),
    ellipse(1000,210,180,180,'#101F36',CY,1),
    tx('STRICTLY CONFIDENTIAL  ·  PRE-SERIES A',80,110,700,24,{size:T.kicker,bold:true,color:CY}),
    tx('DeepGrid Semi',80,168,900,86,{size:T.cover,face:SERIF,bold:true,color:K.white}),
    tx('Financial Model Walkthrough',80,268,900,56,{size:PX(26),face:SERIF,color:'#A9BACD'}),
    rect(80,348,150,3,CY),
    tx('India’s full-stack ADAS company, built on its own transformer silicon.',80,382,720,54,
       {size:PX(14),color:'#8FA2B7'}),
    roundRect(80,470,300,96,'#0E1E33','#1B3350',1),
    tx('₹45 Cr',104,492,260,44,{size:PX(28),face:SERIF,bold:true,color:K.white}),
    tx('EQUITY ROUND',104,540,260,20,{size:T.kicker,bold:true,color:CY}),
    roundRect(400,470,300,96,'#0E1E33','#1B3350',1),
    tx('₹10 Cr',424,492,260,44,{size:PX(28),face:SERIF,bold:true,color:K.white}),
    tx('CGTMSE DEBT FACILITY',424,540,260,20,{size:T.kicker,bold:true,color:CY}),
    tx('All figures in this document are management projections prepared for fundraising purposes.',
       80,616,1000,22,{size:T.foot,italic:true,color:'#6E8299'}),
    tx('August 2026',80,644,400,22,{size:T.foot,bold:true,color:'#8FA2B7'}),
  ],{background:K.midnight,notes:
    'Cover. Deal terms: equity ₹45 Cr, CGTMSE facility ₹10 Cr. Source: financial model Assumptions C11 and Use of Funds D8. '+
    'Basis of preparation: all figures are forward-looking management projections, not audited or reported results.'});
}

// ============================== 2. EXEC SUMMARY ==============================
{
  const p=N();
  add([
    ...hdr('Executive summary','A platform business that self-funds',
      'One 28 nm SoC serves four markets, turns EBITDA-positive in FY2028, and funds its successor from profit.',p),
    ...KPI(48,178,286,'₹1,128Cr','FY2032 revenue','Projected, from a bottom-up units × price build',CYT),
    ...KPI(348,178,286,'34.4%','FY2032 EBITDA margin','₹388 Cr projected EBITDA',TLT),
    ...KPI(648,178,286,'FY2028','EBITDA positive','One full year before the cash low point',GR),
    ...KPI(948,178,286,'₹10.1Cr','Projected cash low','FY2029, with no further equity assumed',CYT),
    ...(()=>{const f=flow(348,'s2');return [
      ...f.cards([
        [48,592,'A demand floor, not a demand forecast',
         'The AD2 kit answers a regulatory obligation on N2/N3 vehicles, not a discretionary purchase. At 18,000 units it captures 1.8% of the mandated pool.',CY],
        [656,576,'The round buys silicon, not runway',
         'Silicon absorbs 66.2% of the equity round, phased so the mask is committed only after working blocks are proven.',TL],
      ]),
      ...f.cards([
        [48,592,'Operating leverage is structural',
         'Gross margin rises from 39.7% to 87.4% as the ASIC replaces bought-in FPGA content, while overhead ratios decline.',GR],
        [656,576,'The next chip is self-funded',
         'About ₹300 Cr of cumulative R&D funds the 5 nm programme from operating profit, so the next wave needs no new silicon capital.',PB],
      ]),
    ];})(),
  ],{notes:'Sources: P&L C6:H26 (revenue, EBITDA, margins); Cash Flow & Runway C28 (low point); '+
    'Use of Funds C18 (silicon share of equity); Demand & TAM C16 (mandated capture).'});
}

// ============================== 3. THE ASK ===================================
{
  const p=N(); const d=D.DEAL;
  add([
    ...hdr('The ask','Equity funds only the silicon',
      'A ₹45 Cr equity round is paired with a ₹10 Cr collateral-free MSME facility that carries working capital.',p),
    ...TBL(48,180,1184,[
      {t:'Term',w:340},{t:'Basis',w:300},{t:'Value',w:272,a:'right'},{t:'Note',w:272}],
      [
        ['Pre-money valuation','Management basis',`₹${d.preMoney.toFixed(2)} Cr`,'Independent valuation report'],
        ['Equity raise','This round',`₹${d.raise.toFixed(2)} Cr`,'Pre-Series A'],
        ['Post-money valuation','Pre-money + raise',`₹${d.postMoney.toFixed(2)} Cr`,'Derived'],
        ['Investor ownership','Raise ÷ post-money',`${d.ownership}%`,`${d.newShares.toLocaleString('en-IN')} new shares`],
        ['Price per share','Round pricing',`₹${d.pricePerShare.toLocaleString('en-IN')}`,'Applied to the share register'],
        ['Debt facility','CGTMSE-backed','₹10.00 Cr','Collateral-free; non-dilutive'],
      ],{rowH:44,highlight:3}),
    ...CARD(48,510,388,'auto','Discount rate',
      `A ${d.wacc}% cost of capital and ${d.terminalG}% terminal growth are applied, reflecting an early-stage Indian hardware risk profile.`,CY),
    ...CARD(452,510,388,'auto','Tax',
      `${d.taxRate}% corporate rate, with the FY2027 loss carried forward and absorbed against FY2028 taxable income.`,TL),
    ...CARD(856,510,376,'auto','Currency',
      `Silicon costs are contracted in dollars and converted at ₹${d.usdInr}/USD throughout.`,PB),
    SRC('Ownership is calculated on a fully diluted basis at the stated price per share.'),
  ],{notes:'Source: Assumptions C6:C17. Investor ownership 18.07% = 45 / 249.03. '+
    'Diligence note: the share register totals 102,797 shares against 100,890 used in the pricing basis; '+
    'this 1,907-share difference is reconciled before definitive documents (see diligence readiness slide).'});
}

// ============================== 4. OPPORTUNITY ===============================
{
  const p=N();
  add([
    ...hdr('Market','Regulation makes the safety buy compulsory',
      'ADAS obligations on commercial vehicles create a recurring, addressable unit pool.',p),
    ...KPI(48,178,286,'$53.2B','India commercial vehicles','Market size, 2025',PBT),
    ...KPI(348,178,286,'$2.29B','India ADAS market','2024, growing at 20.6% a year',CYT),
    ...KPI(648,178,286,'1.0M','Addressable units a year','0.5 M new build plus 0.5 M retrofit',TLT),
    ...KPI(948,178,286,'1.8%','Planned FY2032 capture','18,000 of the mandated pool',GR),
    ...rail(48,392,1184,[
      ['MAR 2025','Rule notified','GSR 184(E) sets the ADAS obligation for N2/N3 vehicles',CYT,true],
      ['APR 2026','New models','Driver-drowsiness, blind-spot and lane-departure systems required',CYT,true],
      ['OCT 2026','Existing models','Obligation extends to the in-service fleet, opening retrofit','#0A6E70',true],
      ['OCT 2027','Braking systems','Advanced emergency braking follows on a separate schedule',PBT,false],
    ]),
    SRC('Market sizes are third-party published estimates. Capture rates are management assumptions.'),
  ],{notes:'Sources: Demand & TAM C7:C12 and B40. Regulatory basis: MoRTH GSR 184(E) dated 20 March 2025. '+
    'The 2026 dates cover the DDAWS / blind-spot / lane-departure suite that AD2 demand rests on. '+
    'The AEBS braking requirement (AIS-162 / IS-11852) sits on a later schedule confirmed to 1 October 2027. '+
    'These are two different obligations on two timetables — not a discrepancy.'});
}

// ============================== 5. PLATFORM ==================================
{
  const p=N();
  add([
    ...hdr('Platform','One chip and one stack, four markets',
      'The same SoC2 silicon ships under different firmware, so engineering effort compounds instead of forking.',p),
    ...chain(48,196,1184,[
      ['SoC2 · 28 nm','Transformer-native ASIC replacing bought-in FPGA content',CY],
      ['Common stack','Perception, planning and diagnostics shared across products',TL],
      ['Four surfaces','Road autonomy · silicon & compute · fleet · sensors and robotics',PB],
      ['Four revenue lines','Kits, dies and licences priced independently by market',GR],
    ],{nodeH:118}),
    ...CARD(48,368,286,'auto','Road autonomy',
      'Smart Mirror and Smart Truck kits — the mandated and near-mandated volume core.',CY),
    ...CARD(348,368,286,'auto','Silicon & compute',
      'ASIC die sold to OEMs, A100 compute boxes and the T100 licence.',TL),
    ...CARD(648,368,286,'auto','Fleet & mobility',
      'Autonomous transport-as-a-service and port automation vehicles.',PB),
    ...CARD(948,368,284,'auto','Sensors & robotics',
      'Thermal, radar and wearable sensing, defence and drone platforms.',GR),
    ...(()=>{const f=flow(528,'s5');return [
      ...f.cards([[48,1184,'Why this matters to the financial plan',
        'Every surface runs the same silicon, so the tapeout is costed once and amortised across all four revenue lines — one ₹29.8 Cr investment supporting a ₹1,128 Cr projected base.',CY,K.cool]]),
    ];})(),
  ],{notes:'Source: Revenue Build A section (platform surfaces, rows 7–11) and B12 platform note.'});
}

// ============================== 6. DIVIDER 1 =================================
{ const p=N(); add(divider('Part one','The revenue plan',
    'How volume, price and customer count build to the FY2032 projection',p),{background:K.midnight,
    notes:'Section divider. Native geometry only — no raster asset.'}); }

// ============================== 7. REVENUE TRAJECTORY ========================
{
  const p=N();
  add([
    ...hdr('Revenue','₹1.7 Cr to ₹1,128 Cr in six years',
      'Every year is built bottom-up as units multiplied by price; no total is set as a target and back-solved.',p),
    ...trajectory(80,194,1120,212,D.PL.revenue,D.FYS,{fmt:(v)=>`₹${v>=100?Math.round(v):v.toFixed(v<10?1:0)}`}),
    ...(()=>{const f=flow(474,'s7');return [
      ...f.cards([
        [48,388,'The inflection is FY2028',
         'Revenue rises 15.4× as ASIC-era products reach the market and systems ship at scale.',CY],
        [452,388,'Growth decelerates by design',
         'Year-on-year growth steps down from 15.4× to 90% as the base compounds.',TL],
        [856,376,'No contracted backlog assumed',
         'The build reflects planned volumes; signed order cover is shown in diligence.',PB],
      ]),
    ];})(),
  ],{notes:'Source: Revenue Build E76:J76 and growth row E77:J77. Figures ₹ Cr. '+
    'FY2027 reflects FPGA-based products and robot sales only; ASIC-derived revenue begins FY2028.'});
}

// ============================== 8. SURFACES ==================================
{
  const p=N();
  add([
    ...hdr('Revenue mix','Road autonomy carries two-thirds',
      'The four surfaces contribute unevenly; mandated demand is deliberately the largest pool.',p),
    ...mixBar(48,182,600,38,D.SURF_FY32),
    ...(()=>{const f=flow(182,'s8-right',392);return [
      ...f.cards([[684,548,'Concentration is the main exposure',
        'Road autonomy at ₹762 Cr is 67.5% of FY2032 revenue, so the AD0 and AD2 ramps are the two assumptions that most affect the outcome. Silicon and compute reach ₹194 Cr, easing that reliance over time.',CY]]),
    ];})(),
    ...(()=>{const f=flow(410,'s8-table');return [
      ...f.tbl(48,1184,[
        {t:'Surface',w:340},{t:'FY2029',w:200,a:'right'},{t:'FY2031',w:200,a:'right'},
        {t:'FY2032',w:222,a:'right'},{t:'Share of FY2032',w:222,a:'right'}],
        [
          ['Road autonomy','₹79.0 Cr','₹417.0 Cr','₹762.0 Cr','67.5%'],
          ['Silicon & compute','₹16.4 Cr','₹90.2 Cr','₹194.3 Cr','17.2%'],
          ['Fleet & mobility','₹8.9 Cr','₹39.8 Cr','₹88.7 Cr','7.9%'],
          ['Sensors & robotics','₹11.1 Cr','₹47.4 Cr','₹83.5 Cr','7.4%'],
        ],{rowH:38,headH:34,highlight:0}),
    ];})(),
  ],{notes:'Source: Revenue Build E7:J11 (platform surfaces). Shares calculated on the FY2032 total of ₹1,128.45 Cr.'});
}

// ============================== 9. SEGMENT MIX ===============================
{
  const p=N();
  add([
    ...hdr('Business mix','Systems are the economic engine',
      'Silicon creates the cost advantage; revenue is realised by selling complete systems.',p),
    ...mixBar(48,182,660,38,D.SEG_FY32),
    ...KPI(760,178,228,'83.4%','Systems share','₹941 Cr of FY2032 revenue',CYT,146),
    ...KPI(1004,178,228,'9.2%','Semiconductors','₹104 Cr of FY2032 revenue',TLT,146),
    ...(()=>{const f=flow(534,'s9-card');return [
      ...f.cards([[48,1184,'What diligence must evidence',
        'System-level pricing, installation capacity and channel access — not chip performance alone.',CY,K.cool]]),
    ];})(),
    ...(()=>{const f=flow(348,'s9-table');return [
      ...f.tbl(48,1184,[
        {t:'Segment',w:300},{t:'FY2027',w:170,a:'right'},{t:'FY2029',w:170,a:'right'},
        {t:'FY2032',w:180,a:'right'},{t:'Gross margin FY2032',w:364,a:'right'}],
        [
          ['Systems','₹0.13 Cr','₹99.2 Cr','₹941.0 Cr','89%'],
          ['Semiconductors','—','₹5.2 Cr','₹104.0 Cr','94%'],
          ['Robotics','₹1.20 Cr','₹7.1 Cr','₹50.0 Cr','68%'],
          ['Sensors','₹0.38 Cr','₹4.0 Cr','₹33.5 Cr','50%'],
        ],{rowH:36,headH:34,highlight:0}),
    ];})(),
  ],{notes:'Source: Revenue Build E16:J21 (segment revenue) and Assumptions C25:H28 (segment gross margin).'});
}

// ============================== 10. UNIT RAMPS ===============================
{
  const p=N();
  add([
    ...hdr('Unit economics','Eleven product lines build the plan',
      'Prices are held flat across the plan; growth comes from volume rather than from price increases.',p),
    ...(()=>{const f=flow(178,'s10');return [
      ...f.tbl(48,1184,[
        {t:'Business line',w:340},{t:'Unit price',w:180,a:'right'},{t:'FY2027 units',w:180,a:'right'},
        {t:'FY2032 units',w:200,a:'right'},{t:'FY2032 revenue',w:284,a:'right'}],
        D.LINES.map(l=>[l[0],l[1],l[2]?l[2].toLocaleString('en-IN'):'—',
          l[3].toLocaleString('en-IN'),`₹${l[4].toFixed(l[4]<100?2:0)} Cr`]),
        {headH:34,highlight:0}),
      ...f.note('Prices are held constant — no erosion or volume-discount curve is modelled. The AD2 truck kit and AD0 mirror together represent ₹720 Cr, or 63.8% of the FY2032 projection.'),
    ];})(),
  ],{notes:'Source: Revenue Build D44:J58 (units and price) and E61:J75 (derived revenue). '+
    'Sensor suite aggregates thermal camera, 4D radar pod and H100 wearable lines.'});
}

// ============================== 11. CUSTOMERS ================================
{
  const p=N();
  add([
    ...hdr('Customers','Accounts grow from 5 to 650',
      'Revenue per account peaks in FY2029, then falls as the base broadens into retrofit and fleet.',p),
    tx('DISTINCT ACCOUNTS',80,176,540,20,{size:T.kicker,bold:true,color:CYT}),
    tx('AVERAGE REVENUE PER ACCOUNT (₹ CR)',680,176,520,20,{size:T.kicker,bold:true,color:'#0A6E70'}),
    ...trajectory(80,200,540,242,D.CUSTOMERS,D.FYS,{fmt:(v)=>String(v),color:CY}),
    ...trajectory(680,200,520,242,D.ARPC,D.FYS,{fmt:(v)=>`₹${v.toFixed(2)}`,color:TL,hot:2}),
    ...(()=>{const f=flow(506,'s11');return [
      ...f.cards([
        [48,592,'Concentration falls as the base widens',
         'Early years depend on a handful of accounts. By FY2032 no single account is structurally required for the plan to hold.',CY],
        [656,576,'What diligence should test',
         'Repeat-purchase behaviour, pilot-to-volume conversion, and the installation throughput needed to serve 650 accounts.',TL],
      ]),
    ];})(),
  ],{notes:'Source: Revenue Build E34:J35. Average revenue per account is total revenue ÷ distinct accounts.'});
}

// ============================== 12. DIVIDER 2 ================================
{ const p=N(); add(divider('Part two','Margin and profitability',
    'How gross margin expands and overhead ratios decline into operating leverage',p),{background:K.midnight,
    notes:'Section divider.'}); }

// ============================== 13. MARGIN ARCHITECTURE ======================
{
  const p=N();
  add([
    ...hdr('Margin architecture','Each segment has its own margin path',
      'The blended gross margin is an output of the mix, not an assumption applied to the top line.',p),
    ...rampRows(48,206,1184,D.GM_SEG,{rowH:64}),
    tx('FY2027',232,180,60,20,{size:T.kicker,bold:true,color:GY}),
    tx('FY2032',1140,180,92,20,{size:T.kicker,bold:true,color:CYT,align:'right'}),
    ...CARD(48,486,388,'auto','What drives the expansion',
      'The ASIC displaces a bought-in FPGA module inside each kit, removing the largest single line in the bill of materials.',CY),
    ...CARD(452,486,388,'auto','Blended outcome',
      'Group gross margin rises from 39.7% in FY2027 to 87.4% in FY2032 as the mix shifts toward higher-margin segments.',TL),
    ...CARD(856,486,376,'auto','The assumption to test',
      'Systems margin reaching 89% is the single most consequential input, because systems are 83.4% of revenue.',PB),
    SRC('Segment margins are management assumptions; supplier quotations are provided in diligence.'),
  ],{notes:'Source: Assumptions C25:H28 (segment gross margin) and P&L C24:H24 (blended gross margin).'});
}

// ============================== 14. P&L ======================================
{
  const p=N(); const f=(a)=>a.map(v=>v<0?`(₹${Math.abs(v).toFixed(2)})`:`₹${v.toFixed(v<100?2:0)}`);
  const R=(label,arr,pct=false)=>[label,...(pct?arr.map(v=>`${v.toFixed(1)}%`):f(arr))];
  add([
    ...hdr('Profit and loss','Operating leverage arrives in FY2028',
      'Every line is derived from the same units-and-price build. All values ₹ Cr.',p),
    ...(()=>{const f=flow(178,'s14');return [
      ...f.tbl(48,1184,[
        {t:'Line item',w:280},{t:'FY2027',w:150,a:'right'},{t:'FY2028',w:150,a:'right'},
        {t:'FY2029',w:150,a:'right'},{t:'FY2030',w:150,a:'right'},{t:'FY2031',w:150,a:'right'},
        {t:'FY2032',w:154,a:'right'}],
        [
          R('Revenue',D.PL.revenue),
          R('Gross profit',D.PL.gp),
          R('Gross margin',D.PL.gmPct,true),
          R('Research & development',D.PL.rndTot),
          R('Sales & marketing',D.PL.sm),
          R('General & administrative',D.PL.ga),
          R('EBITDA',D.PL.ebitda),
          R('EBITDA margin',D.PL.ebitdaPct,true),
          R('Net income',D.PL.ni),
        ],{headH:36,highlight:6}),
      ...f.note('EBITDA turns positive in FY2028 — one year before the projected cash low point, because silicon and working capital keep absorbing cash after profitability arrives. The ₹0.43 Cr FY2027 loss carries forward against FY2028 taxable income.'),
    ];})(),
  ],{notes:'Source: P&L C6:H26 in full. R&D total splits into run-rate and the SoC4 programme (rows 10–11). '+
    'Operating expense includes the scenario opex delta, which is nil in the base case.'});
}

// ============================== 15. OPERATING LEVERAGE =======================
{
  const p=N();
  add([
    ...hdr('Operating leverage','EBITDA reaches ₹388 Cr at a 34.4% margin by FY2032',
      'The step from loss to structural profitability happens once revenue clears the fixed engineering base.',p),
    ...trajectory(80,190,1120,258,D.PL.ebitda,D.FYS,
      {fmt:(v)=>v<0?`(₹${Math.abs(v).toFixed(2)})`:`₹${v.toFixed(v<10?2:0)}`,baseline:true}),
    ...KPI(48,512,286,'FY2028','First positive year','₹2.25 Cr EBITDA',GR,148),
    ...KPI(348,512,286,'34.4%','FY2032 margin','₹387.88 Cr projected EBITDA',CYT,148),
    ...KPI(648,512,286,'24.3%','FY2032 net margin','₹273.98 Cr projected net income',TLT,148),
    ...KPI(948,512,284,'87.4%','FY2032 gross margin','Up from 39.7% in FY2027',PBT,148),
  ],{notes:'Source: P&L C15:H15 (EBITDA), C25:H25 (EBITDA margin), C22:H22 (net income), C24:H24 (gross margin).'});
}

// ============================== 16. OPEX DISCIPLINE ==========================
{
  const p=N();
  add([
    ...hdr('Cost discipline','All three overhead ratios decline',
      'Expenses are planned as a declining percentage of revenue rather than as fixed absolute budgets.',p),
    ...rampRows(48,206,1184,D.OPEX_RATIO,{rowH:64}),
    tx('FY2027',232,180,60,20,{size:T.kicker,bold:true,color:GY}),
    tx('FY2032',1140,180,92,20,{size:T.kicker,bold:true,color:CYT,align:'right'}),
    ...(()=>{const f=flow(408,'s16');return [
      ...f.cards([
        [48,592,'R&D stays deliberately high',
         'Held at 33% of revenue in FY2032 — above a typical hardware business — because it carries the next silicon generation, not only the current one.',CY],
        [656,576,'Sales and administration compress',
         'Sales and marketing falls from 15% to 12.5% of revenue and administration from 10% to 7.5%, as direct pilots give way to channel distribution.',TL],
      ]),
      ...f.note('Diligence item: these ratios are reconciled with the hiring schedule into a single operating bridge before close, so hiring pace and payroll timing can be tested independently.'),
    ];})(),
  ],{notes:'Source: Assumptions C32:H35 (opex ratios) and P&L C9:H13 (applied expense). '+
    'The linked hiring schedule is a diligence deliverable; see the operating plan and diligence readiness slides.'});
}

// ============================== 17. R&D / SoC4 ===============================
{
  const p=N();
  add([
    ...hdr('Research investment','R&D funds the next chip from profit',
      'The next silicon generation is an internally financed option, not a future funding round.',p),
    ...(()=>{const f=flow(178,'s17');return [
      ...f.tbl(48,1184,[
        {t:'Research allocation',w:340},{t:'FY2028',w:170,a:'right'},{t:'FY2029',w:170,a:'right'},
        {t:'FY2030',w:170,a:'right'},{t:'FY2031',w:170,a:'right'},{t:'FY2032',w:164,a:'right'}],
        [
          ['Run-rate R&D (current silicon + software)','₹7.23','₹25.38','₹54.08','₹106.97','₹203.12'],
          ['Next-generation 5 nm programme','₹3.06','₹16.15','₹45.54','₹95.09','₹169.27'],
          ['Total research & development','₹10.29','₹41.54','₹99.63','₹202.06','₹372.39'],
        ],{highlight:1}),
      ...f.cards([
        [48,388,'Why R&D looks high',
         'A conventional read treats 33% of revenue as overspending. Here about half of it is a discrete programme building the next product.',CY],
        [452,388,'What it buys',
         'A 5 nm part aimed at level-4 autonomy and datacentre-class inference — markets that open after this plan horizon.',TL],
        [856,376,'The financing consequence',
         'Funded from profit, so the plan does not depend on raising silicon capital again after this round.',GR],
      ]),
      ...f.note('How to read this in the base case: the programme is an expense inside these projections, not an addition to them — the ₹388 Cr FY2032 EBITDA is stated after absorbing ₹169 Cr of that spend.'),
    ];})(),
  ],{notes:'Source: P&L C10:H11 (run-rate versus programme split) and Assumptions C33:H33. '+
    'Cumulative programme spend FY2028–FY2032 is approximately ₹329 Cr; the narrative rounds to ₹300 Cr per the plan note at P&L B29.'});
}

// ============================== 18. DIVIDER 3 ================================
{ const p=N(); add(divider('Part three','Silicon and capital',
    'What the round funds, what the chip costs, and when it pays back',p),{background:K.midnight,
    notes:'Section divider.'}); }

// ============================== 19. USE OF FUNDS =============================
{
  const p=N();
  add([
    ...hdr('Use of funds','₹55 Cr: silicon first, cycle on debt',
      'Equity is directed almost entirely at the tapeout; the facility funds inventory and receivables.',p),
    ...mixBar(48,182,660,38,D.FUNDS.uses.map(u=>[u[0],u[1],u[2]])),
    ...KPI(760,178,228,'₹45Cr','Equity','Funds silicon and engineering',CYT,146),
    ...KPI(1004,178,228,'₹10Cr','Debt facility','Collateral-free, non-dilutive',TLT,146),
    ...(()=>{const f=flow(528,'s19-card');return [
      ...f.cards([[48,1184,'Silicon is 66.2% of the equity round',
        'The equity raise buys one outcome: working 28 nm silicon; the facility absorbs the working-capital cycle.',CY,K.cool]]),
    ];})(),
    ...(()=>{const f=flow(348,'s19-table');return [
      ...f.tbl(48,1184,[
        {t:'Allocation',w:330},{t:'Amount',w:170,a:'right'},{t:'Share',w:140,a:'right'},{t:'What it covers',w:544}],
        D.FUNDS.uses.map(u=>[u[0],`₹${u[1].toFixed(2)} Cr`,`${u[2]}%`,u[3]]),{rowH:36,headH:34,highlight:0}),
    ];})(),
  ],{notes:'Source: Use of Funds C7:E18. Facility terms are set out on the capital structure slide. '+
    'Draw timing and repayment are integrated into the cash schedule as a diligence deliverable.'});
}

// ============================== 20. TAPEOUT PROGRAMME ========================
{
  const p=N();
  add([
    ...hdr('Silicon programme','The largest commitment comes last',
      'Shared-wafer prototypes prove the blocks before the dedicated production mask is ordered.',p),
    ...chain(48,190,1184,[
      ['Block prototypes','Compute and radar blocks on a shared wafer · $138 k',CY],
      ['Full-die prototype','57 mm² device on a shared wafer · $232 k',TL],
      ['Backend to GDSII','Physical design and sign-off · $1.00 M',PB],
      ['Production mask','Dedicated 28 nm mask set · $1.00 M',GR],
    ],{nodeH:112}),
    ...TBL(48,330,760,[
      {t:'Programme item',w:300},{t:'Cost',w:150,a:'right'},{t:'Purpose',w:310}],
      D.TAPEOUT.phases.map(f=>[f[0],f[1],f[2]]),{rowH:34,headH:32}),
    ...KPI(830,330,190,'$3.17M','Total programme','₹29.80 Cr at ₹94/USD',CYT,146),
    ...KPI(1042,330,190,'4','Gated stages','Each gated on the stage before it',TLT,146),
    ...(()=>{const f=flow(486,'s20');return [
      ...f.cards([[830,402,'Why phasing limits capital risk',
        'The mask and backend sign-off are committed only after working silicon is proven.',CY,K.cool]]),
    ];})(),
  ],{notes:'Source: Tapeout Unit Economics C7:D14. Conversion at ₹94/USD per Assumptions C6.'});
}

// ============================== 21. DIE ECONOMICS ============================
{
  const p=N(); const t=D.TAPEOUT;
  add([
    ...hdr('Chip economics','At volume the die costs $3.88',
      'Cost is derived from die size, wafer price and yield rather than quoted as a target.',p),
    ...TBL(48,180,700,[
      {t:'Derivation',w:400},{t:'Value',w:300,a:'right'}],
      [
        ['Die area','57 mm²'],
        ['Gross die per 300 mm wafer','1,069'],
        ['Yield at mature 28 nm','94.5%'],
        ['Good die per wafer','1,010'],
        ['Wafer cost','$2,400'],
        ['Wafer cost per good die','$2.38'],
        ['Assembly, test and packaging','$1.50'],
        ['Cost per die at volume','$3.88'],
      ],{rowH:38,headH:34,highlight:7}),
    ...KPI(772,180,224,'$18.12','Margin per chip','Against $22 contribution in a kit',CYT,146),
    ...KPI(1008,180,224,'175k','Chips to recover NRE','Breakeven on the programme',TLT,146),
    ...(()=>{const f=flow(352,'s21');return [
      ...f.cards([[772,460,'Volume context',
        'About 217,000 dies ship through FY2032, passing breakeven inside the horizon. The $2,400 wafer price assumes a lifetime commitment near 500,000 dies.',CY]]),
      ...f.note('Reading the cost advantage: a $3.88 bare die is not comparable with a $3,000–8,000 incumbent module. Diligence presents a like-for-like system comparison.',772,460),
    ];})(),
    tx('Yield modelled on a Murphy distribution at approximately 0.1 defects/cm². Supplier quotations provided in diligence.',
       48,620,700,32,{size:T.foot,italic:true,color:GY}),
  ],{notes:'Source: Tapeout Unit Economics C18:C34. '+
    'Deliberate presentation choice: the workbook records a 774× advantage versus a $3,000 incumbent, '+
    'but that compares a bare die to a complete module. The like-for-like framing is used on the slide instead.'});
}

// ============================== 22. SCHEDULE SENSITIVITY =====================
{
  const p=N(); const t=D.TAPEOUT;
  add([
    ...hdr('Schedule risk','A silicon slip costs ₹58 Cr, core intact',
      'Exposure is contained to silicon and compute; road autonomy runs on current-generation parts.',p),
    ...barsNative(48,202,1184,[
      ['Silicon & compute · on plan', 194.30, CY, '₹194.3 Cr'],
      ['Silicon & compute · slip case', 136.01, '#B9C7D6', '₹136.0 Cr'],
    ],{rowH:56,labelW:340,valW:200,max:200}),
    ...KPI(48,340,286,'30%','Revenue haircut','Applied to the affected lines',CYT),
    ...KPI(348,340,286,'₹58.3Cr','FY2032 impact','5.2% of projected group revenue',TLT),
    ...KPI(648,340,286,'Intact','Road autonomy','₹762 Cr runs on current silicon',GR),
    ...KPI(948,340,284,'None','New capital needed','Programme is funded from profit',PBT),
    ...(()=>{const f=flow(510,'s22');return [
      ...f.cards([[48,1184,'Why the core is insulated',
        'Mandated truck and mirror products ship on current-generation silicon. A next-generation delay defers the silicon and compute ramp by a year; it does not interrupt the revenue carrying two-thirds of the plan.',CY,K.cool]]),
    ];})(),
  ],{notes:'Source: Tapeout Unit Economics C42:C45. Group impact calculated against FY2032 revenue of ₹1,128.45 Cr.'});
}

// ============================== 23. CASH & RUNWAY ============================
{
  const p=N();
  add([
    ...hdr('Cash and runway','A ₹10.1 Cr low point, then recovery',
      'Cash recovers once tapeout capital is complete and operating profit outpaces working-capital growth.',p),
    tx('CLOSING CASH BALANCE (₹ CR)',80,172,600,20,{size:T.kicker,bold:true,color:CYT}),
    ...trajectory(80,178,1120,158,D.CASH.closing,D.FYS,
      {fmt:(v)=>`₹${v.toFixed(v<100?1:0)}`,hot:2,color:CY}),
    ...(()=>{const f=flow(398,'s23');return [
      ...f.tbl(48,1184,[
        {t:'Cash movement',w:280},{t:'FY2027',w:150,a:'right'},{t:'FY2028',w:150,a:'right'},
        {t:'FY2029',w:150,a:'right'},{t:'FY2030',w:150,a:'right'},{t:'FY2031',w:150,a:'right'},
        {t:'FY2032',w:154,a:'right'}],
        [
          ['Operating cash flow','(₹0.40)','₹1.93','₹16.78','₹53.07','₹133.57','₹296.55'],
          ['Silicon capital','(₹18.00)','(₹10.00)','(₹2.00)','—','—','—'],
          ['Working capital movement','(₹0.26)','(₹3.92)','(₹13.13)','(₹25.39)','(₹46.45)','(₹80.12)'],
          ['Net cash flow','(₹19.74)','(₹13.93)','(₹1.25)','₹22.43','₹78.62','₹202.43'],
          ['Closing cash','₹25.28','₹11.35','₹10.10','₹32.53','₹111.16','₹313.58'],
        ],{rowH:36,headH:34,highlight:4}),
    ];})(),
  ],{notes:'Source: Cash Flow & Runway C6:H29. Low point ₹10.098 Cr at FY2029 close (C28). '+
    'Fleet vehicles for the transport service are asset-financed against the vehicles, so that capital is not an equity draw. '+
    'Diligence deliverable: monthly runway to the trough and integration of facility draw and repayment into this schedule.'});
}

// ============================== 24. CAPITAL STRUCTURE ========================
{
  const p=N(); const d=D.DEBT;
  add([
    ...hdr('Capital structure','Equity funds the asset, debt the cycle',
      'Separating the two keeps dilution on silicon and working capital non-dilutive.',p),
    ...CARD(48,180,592,'auto','Equity — ₹45 Cr',
      'Directed at the tapeout, engineering and certification. This is the capital that creates a durable asset: a working, '+
      'certified 28 nm device that every product line depends on.',CY),
    ...CARD(656,180,576,'auto','Debt — ₹10 Cr CGTMSE facility',
      'A collateral-free MSME-backed overdraft sized against working capital. It is non-dilutive and scales with the '+
      'receivables cycle rather than with the capital programme.',TL),
    ...TBL(48,340,760,[
      {t:'Facility term',w:380},{t:'Basis',w:380,a:'right'}],
      [
        ['Sanctioned limit','₹10.00 Cr'],
        ['Interest rate','15.0%'],
        ['Assumed utilisation','25% — ₹2.50 Cr average draw'],
        ['Annual finance cost at that utilisation','₹0.375 Cr'],
      ],{rowH:44,headH:38}),
    ...CARD(830,340,402,'auto','Why working capital needs a facility',
      'Indian commercial-vehicle customers typically settle in 60–90 days. Working capital is planned at 15% of revenue and '+
      'absorbs ₹80.1 Cr in FY2032 alone — a cycle cost that should not consume equity.',PB),
    ...CARD(48,560,1184,'auto','What is finalised before close',
      'Draw timing, principal repayment, fees, guarantee coverage and covenants are integrated into the cash schedule, '+
      'together with facility availability under the constrained-capital case.',CY,K.cool),
  ],{notes:'Source: facility terms — limit ₹10 Cr, 15% rate, 25% utilisation, ₹0.375 Cr finance cost. '+
    'Working-capital intensity from Cash Flow & Runway C18 (15% of revenue).'});
}

// ============================== 25. OWNERSHIP ================================
{
  const p=N();
  const totalShares = D.CAP.reduce((s,c)=>s+c[2],0);
  add([
    ...hdr('Ownership and prior capital','Founder-controlled, ₹2.48 Cr deployed',
      'Governance rights, not dispersed ownership, protect an incoming investor.',p),
    ...TBL(48,180,700,[
      {t:'Shareholder',w:340},{t:'Type',w:140},{t:'Shares',w:120,a:'right'},{t:'Holding',w:100,a:'right'}],
      D.CAP.map(c=>[c[0],c[1],c[2].toLocaleString('en-IN'),`${c[3]}%`]),{rowH:46,headH:38,highlight:0}),
    ...KPI(772,180,220,'18.07%','Investor holding','Post-round, this raise',CYT,150),
    ...KPI(1012,180,220,'₹2.48Cr','Capital deployed','Grants and angel funding to date',TLT,150),
    ...TBL(48,376,700,[
      {t:'Capital received to date',w:340},{t:'Amount',w:140,a:'right'},{t:'Status',w:220}],
      D.PRIOR.map(r=>[r[0],`₹${r[1].toFixed(2)} Cr`,r[2]]),{rowH:42,headH:36}),
    ...CARD(772,350,460,'auto','What this establishes',
      'Grants and angel capital carried certification, FPGA development and operations to this point. A further ₹1 Cr of defence revenue was earned.',CY),
    ...CARD(772,516,460,'auto','Governance is the live term',
      'With founder holdings above 95%, reserved matters, board composition and information rights carry more weight '+
      'than the ownership percentage alone.',PB,K.cool),
  ],{notes:'Sources: share register (102,797 shares) and prior-capital schedule. '+
    'Diligence item: the pricing basis uses 100,890 existing shares; the 1,907-share difference is reconciled before definitive documents. '+
    'Grant and angel amounts: ARAI ₹0.36 Cr, HDFC Parivartan ₹0.12 Cr, angel ₹2.00 Cr.'});
}

// ============================== 26. OPERATING PLAN ===========================
{
  const p=N();
  add([
    ...hdr('Operating plan','Headcount grows from 34 to 541',
      'The hiring shape follows the product plan: silicon and software first, commercial scale later.',p),
    tx('TOTAL HEADCOUNT',80,172,560,20,{size:T.kicker,bold:true,color:CYT}),
    tx('FY2032 BY FUNCTION',700,172,520,20,{size:T.kicker,bold:true,color:'#0A7A7D'}),
    ...trajectory(80,186,560,190,D.HEADCOUNT,D.FYS,{fmt:(v)=>String(v),color:CY}),
    ...barsNative(700,208,532,D.DEPTS.slice(0,7).map(d=>[d[0],d[1],
      ['Software','Hardware','AI'].includes(d[0])?TL:'#C6D2DE',String(d[1])]),
      {rowH:32,labelW:190,valW:60,max:110}),
    ...(()=>{const f=flow(446,'s26');return [
      ...f.cards([
        [48,592,'Engineering is two-thirds of the FY2032 organisation',
         'Software, hardware, AI, firmware, design and testing account for 357 of 541 planned roles — a business whose differentiation is silicon and the stack on it.',CY],
        [656,576,'Presented separately, and why',
         'Overhead is planned as a share of revenue. Headcount is shown as the operating shape and is not spliced into the profit projection until both are reconciled into one linked bridge.',TL],
      ]),
    ];})(),
  ],{notes:'Source: hiring schedule — headcount 34 → 541 across FY2027–FY2032, by department. '+
    'Editorial rule applied: payroll values from the hiring schedule are NOT combined with the profit projection, '+
    'because the two are calibrated to different revenue bases. Reconciliation is a stated diligence deliverable.'});
}

// ============================== 27. DIVIDER 4 ================================
{ const p=N(); add(divider('Part four','Risk and decision',
    'Downside cases, the assumptions that matter most, and what happens next',p),{background:K.midnight,
    notes:'Section divider.'}); }

// ============================== 28. SCENARIOS ================================
{
  const p=N();
  add([
    ...hdr('Scenarios','Self-funding even on a 70% miss',
      'One revenue multiplier and one overhead adjustment drive each case, so the downside is testable.',p),
    ...(()=>{const f=flow(178,'s28');return [
      ...f.tbl(48,1184,[
        {t:'Case',w:200},{t:'Revenue multiplier',w:220,a:'right'},{t:'Overhead adjustment',w:220,a:'right'},
        {t:'FY2032 revenue',w:220,a:'right'},{t:'What it represents',w:324}],
        D.SCENARIOS.map(s=>[s[0],s[1],s[2],s[3],s[4]]),{headH:38,highlight:1}),
      ...f.cards([
        [48,592,'The downside case is the important one',
         'At 0.3× revenue and eight points of extra overhead, FY2032 revenue is about ₹339 Cr — reached without assuming a further equity round.',CY],
        [656,576,'What the cases do not yet cover',
         'Each case moves revenue uniformly. Diligence separates a mandate delay, a silicon delay and margin compression, which have different cash timing.',TL],
      ]),
      ...f.note('Decision outputs requested from every case: cash low point and its date · the next funding requirement, if any · the EBITDA breakeven year · facility headroom under covenants.'),
    ];})(),
  ],{notes:'Source: scenario switch — Bull 1.2×, Bear 0.75×, Downside 0.3× revenue multiplier; '+
    'overhead delta Bull −3 pts, Bear +5 pts, Downside +8 pts. Downside revenue 0.3 × ₹1,128.45 Cr ≈ ₹339 Cr. '+
    'Bull and Bear FY2032 revenue shown are the multiplier applied to the base; full case P&Ls are a diligence deliverable.'});
}

// ============================== 29. DRIVERS + DILIGENCE ======================
{
  const p=N();
  add([
    ...hdr('What determines the outcome','Five assumptions carry the projection',
      'The inputs where a modest change moves the result materially.',p),
    ...TBL(48,180,1184,[
      {t:'Driver',w:300},{t:'Base assumption',w:270},{t:'Why it is decisive',w:614}],
      D.DRIVERS.map(d=>[d[0],d[1],d[2]]),{rowH:44,headH:36,highlight:0}),
    ...(()=>{const f=flow(436,'s29');return [
      ...f.cards([[48,1184,'Evidence provided in diligence',
        'Customer nominations and conversion history behind the volume ramps · supplier quotations and bill-of-materials build-ups supporting the margin path · monthly cash to the low point with facility terms integrated · share register reconciled to the pricing basis · hiring schedule linked to the overhead ratios.',CY,K.cool]]),
      ...f.note('Capital is proposed to release against gates rather than against the forecast: working silicon on shared wafers, certification achieved, and pilots converted to paying customers — each a verifiable event with a date.'),
    ];})(),
  ],{notes:'Sensitivity drivers derived from the plan structure: AD0+AD2 = ₹720 Cr of ₹1,128.45 Cr (63.8%); '+
    'systems 83.4% of revenue at 89% margin; die cost from 94.5% yield at $2,400/wafer; working capital 15% of revenue '+
    '= ₹80.12 Cr FY2032 movement; SoC4 slip = ₹58.3 Cr. Diligence list reflects the open reconciliation items.'});
}

// ============================== 30. CLOSE ====================================
{
  const p=N();
  add([
    rect(0,0,1280,720,K.midnight),
    rect(0,0,1280,5,CY),
    ...Array.from({length:9},(_,i)=>rect(940+i*38,0,1,720,'#14263C')),
    tx('THE ASK',80,96,700,24,{size:T.kicker,bold:true,color:CY}),
    tx('₹45 Cr equity to fund working silicon',80,142,1000,60,
       {size:PX(30),face:SERIF,bold:true,color:K.white}),
    tx('Paired with a ₹10 Cr non-dilutive facility for working capital, against a plan that reaches self-funding without a further round.',
       80,214,1040,48,{size:PX(14),color:'#A9BACD'}),
    rect(80,282,140,3,CY),
    ...[['Mandated demand','Regulation sets a recurring unit pool, not a discretionary market'],
        ['One chip, four markets','A single tapeout amortised across every revenue line'],
        ['Self-funding','EBITDA positive in FY2028; the next chip financed from profit'],
        ['Gated capital','Released against silicon, certification and paying customers']]
      .map(([t2,b],i)=>{
        const x=80+i*292;
        return [
          roundRect(x,324,272,150,'#0E1E33','#1B3350',1),
          rect(x,324,272,4,[CY,TL,GR,PB][i]),
          tx(t2,x+20,348,232,48,{size:T.cardH,bold:true,color:K.white}),
          tx(b,x+20,400,232,78,{size:PX(11),color:'#8FA2B7'}),
        ];
      }).flat(),
    roundRect(80,512,1120,92,'#0E1E33',CY,1),
    tx('A credible plan is not the one with the highest terminal year — it is the one whose assumptions can be verified.',
       112,536,1056,52,{size:PX(15),italic:true,face:SERIF,color:K.white}),
    tx('All figures are management projections prepared for fundraising purposes and are not audited or reported results.',
       80,634,1000,20,{size:T.foot,italic:true,color:'#6E8299'}),
    tx('DEEPGRID SEMI  ·  PRE-SERIES A  ·  AUGUST 2026',80,662,700,20,{size:T.foot,bold:true,color:'#8FA2B7'}),
    tx(String(p).padStart(2,'0'),1160,662,72,20,{size:T.foot,bold:true,color:'#8FA2B7',align:'right'}),
  ],{background:K.midnight,notes:'Close. Restates the ask and the four structural arguments. '+
    'Basis of preparation repeated for the reader who starts at the back.'});
}

// ---- emit -------------------------------------------------------------------
for (const [children,opts] of S) addSlide(children,opts);
await (await PresentationFile.exportPptx(P)).save(OUT);
if (VIOLATIONS.length) { console.log('LAYOUT VIOLATIONS:'); VIOLATIONS.forEach(v=>console.log('  '+v)); }
else console.log('layout guard: clean');
console.log(`OK slides=${S.length} -> ${OUT}`);
