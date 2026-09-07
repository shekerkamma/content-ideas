import { P, C, K, SERIF, addSlide, tx, rect, roundRect, ellipse, sh,
         PresentationFile, OUT, PX, T, divider, barsNative,
         CY, TL, GR, PB, SL, GY, CYT, PBT, TLT,
         hdr, TH, CARD, CARDH, KPI, TBL, flow, VIOLATIONS } from './deck-lib.mjs';
import { PRODUCTS, BY_SEGMENT, TIERS, UNDERWRITE, FYS } from './data_products.mjs';

const S = []; const add = (c, o = {}) => S.push([c, o]);
let pg = 0; const N = () => ++pg;
const cr = v => `₹${v >= 100 ? Math.round(v) : v.toFixed(v < 10 ? 2 : 1)} Cr`;
const byId = s => PRODUCTS.find(p => p.slug === s);
const segColour = g => g === '89%' ? CY : g === '94%' ? TL : g === '68%' ? GR : PB;
const shortName = n => n.replace(/\s*\([^)]*\)/g, '').replace('driver-monitor wearable', 'driver monitor');

// Compact KPI: numeral + label only.
function KPI2(x, y, w, num, label, color = CY) {
  const lH = TH(label.toUpperCase(), w - 24, T.kpiLab);
  const H = 24 + 58 + 10 + lH + 18;
  const fits = Math.max(4, Math.floor((w - 16) / (0.612 * T.kpiNum)));
  const nSize = String(num).length <= fits ? T.kpiNum
              : Math.max(PX(20), Math.floor(T.kpiNum * fits / String(num).length));
  return [ roundRect(x, y, w, H, K.surface, K.line, 1),
    tx(num, x, y + 24, w, 58, { size: nSize, face: SERIF, bold: true, color, align: 'center' }),
    tx(label.toUpperCase(), x + 12, y + 92, w - 24, lH, { size: T.kpiLab, bold: true, color: SL, align: 'center' }) ];
}

// Six-year unit ramp as columns with direct labels.
function ramp(x, y, w, h, units) {
  const n = units.length, gap = 14, bw = (w - (n - 1) * gap) / n;
  const max = Math.max(...units);
  const e = [];
  units.forEach((v, i) => {
    const bx = x + i * (bw + gap), hot = i === n - 1;
    const bh = Math.max(3, (v / max) * h);
    e.push(rect(bx, y + h - bh, bw, bh, hot ? CY : '#CBD5E1'));
    e.push(tx(v.toLocaleString('en-IN'), bx - 6, y + h - bh - 26, bw + 12, 24,
      { size: T.body, bold: true, color: hot ? CYT : SL, align: 'center' }));
    e.push(tx(FYS[i], bx - 6, y + h + 8, bw + 12, 20,
      { size: T.kicker, bold: true, color: GY, align: 'center' }));
  });
  return e;
}

// One product rendered as a column: name, three figures, description, pool.
function productColumn(x, y, w, p) {
  const e = [];
  e.push(roundRect(x, y, w, 300, K.white, K.line, 1));
  e.push(rect(x, y, w, 5, segColour(p.gm)));
  e.push(tx(shortName(p.name), x + 20, y + 22, w - 40, 48,
    { size: T.cardH, bold: true, color: SL }));
  const figs = [[p.units[5].toLocaleString('en-IN'), 'FY32 UNITS'],
                [cr(p.rev), 'REVENUE'], [p.gm, 'MARGIN']];
  figs.forEach(([v, l], i) => {
    const fx = x + 20 + i * ((w - 40) / 3);
    e.push(tx(v, fx, y + 78, (w - 40) / 3 - 6, 26, { size: T.body, bold: true, color: CYT }));
    e.push(tx(l, fx, y + 104, (w - 40) / 3 - 6, 16, { size: PX(8), bold: true, color: GY }));
  });
  e.push(rect(x + 20, y + 130, w - 40, 1, K.line));
  const bodyH = TH(p.what, w - 40, T.body);
  e.push(tx(p.what, x + 20, y + 144, w - 40, bodyH, { size: T.body, color: GY }));
  e.push(tx('DEMAND POOL · ' + p.capture, x + 20, y + 232, w - 40, 16,
    { size: PX(8), bold: true, color: TLT }));
  e.push(tx(p.pool, x + 20, y + 250, w - 40, TH(p.pool, w - 40, PX(10)),
    { size: PX(10), color: GY }));
  return e;
}

// ============================== COVER ========================================
{
  const p = N();
  add([
    rect(0,0,1280,720,K.midnight),
    ...Array.from({length:11},(_,i)=>rect(864+i*38,0,1,720,'#14263C')),
    rect(0,0,1280,5,CY),
    ellipse(940,150,300,300,'#0E1E33','#16304C',2),
    ellipse(1000,210,180,180,'#101F36',CY,1),
    tx('STRICTLY CONFIDENTIAL  ·  PRE-SERIES A',80,110,700,24,{size:T.kicker,bold:true,color:CY}),
    tx('Product Lines',80,168,900,86,{size:T.cover,face:SERIF,bold:true,color:K.white}),
    tx('Where the ₹1,128 Cr comes from',80,268,900,56,{size:PX(26),face:SERIF,color:'#A9BACD'}),
    rect(80,348,150,3,CY),
    tx('Thirteen lines on one chip. Two carry 64% of the plan, and this deck weights them accordingly.',
       80,382,760,54,{size:PX(14),color:'#8FA2B7'}),
    roundRect(80,470,300,96,'#0E1E33','#1B3350',1),
    tx('64%',104,492,260,44,{size:PX(28),face:SERIF,bold:true,color:K.white}),
    tx('CARRIED BY TWO LINES',104,540,260,20,{size:T.kicker,bold:true,color:CY}),
    roundRect(400,470,300,96,'#0E1E33','#1B3350',1),
    tx('Under 2%',424,492,260,44,{size:PX(28),face:SERIF,bold:true,color:K.white}),
    tx('SHARE OF EVERY DEMAND POOL',424,540,260,20,{size:T.kicker,bold:true,color:CY}),
    tx('All figures are management projections prepared for fundraising purposes.',
       80,616,1000,22,{size:T.foot,italic:true,color:'#6E8299'}),
    tx('August 2026',80,644,400,22,{size:T.foot,bold:true,color:'#8FA2B7'}),
  ],{background:K.midnight,notes:'Companion to the financial model walkthrough. Units and price from Revenue Build D44:J58; demand pools, capture and sources from the Demand & TAM worksheet, section B.'});
}

// ============================== PORTFOLIO ====================================
{
  const p = N();
  add([
    ...hdr('Portfolio','Thirteen lines, and two carry 64%',
      'AD2 and AD0 carry ₹720 Cr; the other eleven share ₹408 Cr. Prices hold flat.',p),
    ...(()=>{const f=flow(170,'portfolio');return [
      ...f.tbl(48,1184,[
        {t:'Product line',w:330},{t:'Unit price',w:150,a:'right'},
        {t:'FY2032 units',w:170,a:'right'},{t:'FY2032 revenue',w:180,a:'right'},
        {t:'Share',w:130,a:'right'},{t:'Gross margin',w:224,a:'right'}],
        [...PRODUCTS].sort((a,b)=>b.rev-a.rev).map(x=>[x.name,x.asp,
          x.units[5].toLocaleString('en-IN'),cr(x.rev),`${x.share.toFixed(1)}%`,x.gm]),
        {headH:34,highlight:0}),
    ];})(),
  ],{notes:'Source: Revenue Build D44:J58 and E61:J75; Assumptions C25:H28. Shares of ₹1,128.45 Cr.'});
}

// ============================== CONCENTRATION ================================
{
  const p = N();
  add([
    ...hdr('Concentration','Two lines carry 64%, eleven carry the rest',
      'FY2032 revenue by line. Colour shows segment: systems, silicon, robotics, sensors.',p),
    ...barsNative(48,186,1184,[...PRODUCTS].sort((a,b)=>b.rev-a.rev)
      .map(x=>[shortName(x.name),x.rev,segColour(x.gm),cr(x.rev)]),
      {rowH:29,labelW:320,valW:120,max:460}),
    ...(()=>{const f=flow(578,'conc',646);return [
      ...f.note('AD2 and AD0 are both road-autonomy systems sold to overlapping buyers, so a certification or installation delay hits ₹720 Cr at once — not two independent lines.'),
    ];})(),
  ],{notes:'Source: Revenue Build E61:J75. Bars are FY2032 revenue in ₹ Cr on a 460 Cr axis.'});
}

// ============================== HEADROOM =====================================
{
  const p = N();
  const sized = PRODUCTS.filter(x=>x.capture!=='—');
  add([
    ...hdr('Headroom','No line assumes we win its market',
      'FY2032 share of each line\'s own sized demand pool. Axis runs to 2%.',p),
    ...barsNative(48,190,1184,sized.map(x=>[shortName(x.name),parseFloat(x.capture),
      parseFloat(x.capture)>1?CY:PB,x.capture]),{rowH:38,labelW:320,valW:110,max:2.0}),
    ...(()=>{const f=flow(490,'head',640);return [
      ...f.cards([
        [48,592,'Why the shares look small',
         'Most pools are global while our serviceable market is the India slice, so the real share is higher. Five lines have no sized pool and are excluded.',CYT],
        [656,576,'The one to read differently',
         'Seaport AGV shows 0.02% against a pool that is total port automation, cranes and software included. We sell only the vehicle layer.',TLT],
      ]),
    ];})(),
    tx('Demand pool sources are shown against each line. Capture rates are management assumptions.',
       48,652,1184,20,{size:T.foot,italic:true,color:GY}),
  ],{notes:'Source: Demand & TAM section B, capture column E22:E33. Eight of thirteen lines carry a numeric capture rate; AD1, H100, D-HUMR, D100 and T100 have no separately sized pool.'});
}

// ============================== TIERS ========================================
for (const t of TIERS) {
  { const p = N();
    add(divider(t.part, t.label, `${cr(t.rev)} · ${t.share}% of FY2032 revenue — ${t.beat}`, p),
      { background: K.midnight, notes: `Tier: ${t.label}. Members: ${t.slugs.join(', ')}. ${cr(t.rev)} of FY2032 revenue.` });
  }

  if (t.id === 'core') {
    // The two material lines get a full slide each, with what must be true.
    for (const slug of t.slugs) {
      const x = byId(slug), u = UNDERWRITE[slug], p = N();
      add([
        ...hdr(x.kicker, x.title, x.tag, p),
        ...KPI2(48,178,286,x.units[5].toLocaleString('en-IN'),'FY2032 units',CYT),
        ...KPI2(348,178,286,x.asp,'Unit price',TLT),
        ...KPI2(648,178,286,cr(x.rev),'FY2032 revenue',GR),
        ...KPI2(948,178,284,x.share.toFixed(1)+'%','Share of FY2032',PBT),
        tx('UNITS SHIPPED',48,330,400,18,{size:T.kicker,bold:true,color:CYT}),
        ...ramp(48,382,560,86,x.units),
        ...(()=>{const f=flow(330,'core-'+slug,646);return [
          ...f.at(330),
          ...f.cards([[656,576,'What it is, and who buys it',x.what+' '+x.buyer,CYT]]),
          ...f.cards([[656,576,'Demand pool · '+x.capture+' capture',x.pool,TLT,K.cool]]),
        ];})(),
        ...(()=>{const f=flow(500,'core2-'+slug,646);return [
          ...f.cards(u.must.map((m,i)=>[48+i*0,560,'','',CY]).length?[]:[]),
        ];})(),
        ...u.must.map((m,i)=>{
          const cx = 48 + i*196, cw = 184;
          return [ roundRect(cx,500,cw,124,K.white,K.line,1),
            rect(cx,500,cw,4,CY),
            tx(m[0],cx+14,514,cw-28,34,{size:PX(11),bold:true,color:SL}),
            tx(m[1],cx+14,552,cw-28,64,{size:PX(9.5),color:GY}) ];
        }).flat(),
        tx('WHAT MUST BE TRUE',48,478,400,16,{size:T.kicker,bold:true,color:CYT}),
        tx(u.evidence,48,634,1184,20,{size:T.foot,italic:true,color:GY}),
      ],{notes:`${x.name}. Units ${x.units.join(' / ')} at ${x.asp} giving ${cr(x.rev)} (${x.share.toFixed(1)}% of ₹1,128.45 Cr) at ${x.gm} segment margin. Demand pool source: ${x.source}.`});
    }
  } else {
    // Smaller lines share a slide, three columns at a time.
    const members = t.slugs.map(byId);
    for (let i = 0; i < members.length; i += 3) {
      const grp = members.slice(i, i + 3), p = N();
      const w = grp.length === 3 ? 384 : grp.length === 2 ? 584 : 1184;
      const gap = grp.length === 3 ? 16 : 16;
      add([
        ...hdr(t.label, grp.length === 1 ? grp[0].title
             : grp.map(g => shortName(g.name)).join(' · '),
          grp.map(g => `${shortName(g.name)} ${cr(g.rev)}`).join('  ·  ') + '  ·  ' +
          cr(grp.reduce((s,g)=>s+g.rev,0)) + ' combined', p),
        ...grp.map((g, j) => productColumn(48 + j * (w + gap), 186, w, g)).flat(),
        ...(()=>{const f=flow(506,'grp-'+t.id+'-'+i,646);return [
          ...f.note(grp.map(g => `${shortName(g.name)}: ${g.why}`).join('  ')),
        ];})(),
        tx('Demand pool sources: ' + grp.map(g => `${shortName(g.name)} — ${g.source}`).join('; ') + '.',
           48, 652, 1184, 20, { size: T.foot, italic: true, color: GY }),
      ],{notes: grp.map(g=>`${g.name}: units ${g.units.join('/')} at ${g.asp} = ${cr(g.rev)} (${g.share.toFixed(1)}%), ${g.gm} margin. Pool source: ${g.source}.`).join(' ')});
    }
  }
}

// ============================== CLOSE ========================================
{
  const p = N();
  add([
    ...hdr('What the portfolio implies','Underwrite two lines, and the rest is optionality',
      'Where the revenue sits, where the margin sits, and what has to be evidenced.',p),
    ...KPI2(48,178,286,'64%','Carried by AD2 + AD0',CYT),
    ...KPI2(348,178,286,'94%','Best segment margin',TLT),
    ...KPI2(648,178,286,'Under 2%','Share of every pool',GR),
    ...KPI2(948,178,284,'1','Line with revenue today',PBT),
    ...(()=>{const f=flow(326,'close',646);return [
      ...f.cards([
        [48,592,'Concentration is the exposure',
         'AD2 and AD0 are the same product family sold to overlapping buyers. A certification or installation delay hits ₹720 Cr at once. Everything else in the portfolio is smaller than that single risk.',CYT],
        [656,576,'Margin sits where revenue does not',
         'Semiconductors are 9.2% of revenue at 94% margin and need no installation capacity. Sensors are 3.0% at 50% and are carried for capability, not profit.',TLT],
      ]),
      ...f.cards([[48,1184,'What moves these lines from projection to backlog',
        'Customer nominations and pilot conversion history behind AD2 and AD0 · certification status through ARAI or ICAT · channel agreements evidencing the aftermarket ramp · the existing defence revenue reconciled to a paid order.',CY,K.cool]]),
    ];})(),
  ],{notes:'Close. The four figures are computed from the tables in this deck; the diligence list matches the walkthrough deck.'});
}

for (const [c,o] of S) addSlide(c,o);
if (VIOLATIONS.length) { console.log('LAYOUT VIOLATIONS:'); VIOLATIONS.forEach(v=>console.log('  '+v)); }
else console.log('layout guard: clean');
await (await PresentationFile.exportPptx(P)).save(OUT);
console.log(`OK slides=${S.length} -> ${OUT}`);
