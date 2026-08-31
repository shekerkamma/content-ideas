import { P, C, K, SERIF, addSlide, tx, rect, roundRect, ellipse, sh,
         PresentationFile, OUT, PX, T, divider, barsNative, rail, chain,
         CY, TL, GR, PB, SL, GY, CYT, PBT, TLT,
         hdr, TH, CARD, CARDH, KPI, TBL, flow, VIOLATIONS } from './deck-lib.mjs';
import { SKUS, SURFACES, DOMAINS, FYS } from './data_sku.mjs';
import { UNDERWRITE } from './data_products.mjs';

const S=[]; const add=(c,o={})=>S.push([c,o]);
let pg=0; const N=()=>++pg;
const cr=v=>`₹${v>=100?Math.round(v):v.toFixed(v<10?2:1)} Cr`;
const byName=n=>SKUS.find(p=>p.name.startsWith(n));
const segCol=g=>g==='89%'?CY:g==='94%'?TL:g==='68%'?GR:PB;
const money2=v=>`₹${v>=100000?(v/100000).toFixed(2)+' L':v.toLocaleString('en-IN')}`;
const shortN=n=>n.replace(/\s*\(mandate retrofit\)/,'').replace(/\s*\(aftermarket\)/,'')
  .replace(/\s*\(port autonomy\)/,'').replace(/\s*\(SaaS\)/,'').replace(/\s*\(ASIC die\)/,'')
  .replace('driver-monitor wearable','driver monitor').replace(' +SDK','').replace('(M.2)','M.2').replace('(PCIe)','PCIe');
const money=v=>`₹${v>=100000?(v/100000).toFixed(2)+' L':v.toLocaleString('en-IN')}`;

function KPI2(x,y,w,num,label,color=CY){
  const lH=TH(label.toUpperCase(),w-24,T.kpiLab), H=24+58+10+lH+18;
  const fits=Math.max(4,Math.floor((w-16)/(0.612*T.kpiNum)));
  const nS=String(num).length<=fits?T.kpiNum:Math.max(PX(20),Math.floor(T.kpiNum*fits/String(num).length));
  return [roundRect(x,y,w,H,K.surface,K.line,1),
    tx(num,x,y+24,w,58,{size:nS,face:SERIF,bold:true,color,align:'center'}),
    tx(label.toUpperCase(),x+12,y+92,w-24,lH,{size:T.kpiLab,bold:true,color:SL,align:'center'})];
}
function ramp(x,y,w,h,units){
  const n=units.length,gap=14,bw=(w-(n-1)*gap)/n,max=Math.max(...units),e=[];
  units.forEach((v,i)=>{const bx=x+i*(bw+gap),hot=i===n-1,bh=Math.max(3,(v/max)*h);
    e.push(rect(bx,y+h-bh,bw,bh,hot?CY:'#CBD5E1'));
    e.push(tx(v.toLocaleString('en-IN'),bx-6,y+h-bh-24,bw+12,22,{size:T.body,bold:true,color:hot?CYT:SL,align:'center'}));
    e.push(tx(FYS[i],bx-6,y+h+8,bw+12,18,{size:T.kicker,bold:true,color:GY,align:'center'}));});
  return e;
}
// Height of a product column for width w — every box measured, none fixed.
function colH(w,p){
  const iw=w-36, fw=iw/3-4;
  return 20 + TH(shortN(p.name),iw,T.cardH) + 10
       + TH('FY32 UNITS',fw,PX(8)) + TH(p.units[5].toLocaleString('en-IN'),fw,T.body) + 14
       + TH(p.what,iw,PX(10.5)) + 12
       + TH('POOL · '+p.capture,iw,PX(8)) + TH(p.pool,iw,PX(9.5)) + 18;
}
function col(x,y,w,h,p){
  const iw=w-36, fw=iw/3-4;
  const nH=TH(shortN(p.name),iw,T.cardH);
  const lH=TH('FY32 UNITS',fw,PX(8)), vH=TH(p.units[5].toLocaleString('en-IN'),fw,T.body);
  const wH=TH(p.what,iw,PX(10.5));
  const pkH=TH('POOL · '+p.capture,iw,PX(8)), poH=TH(p.pool,iw,PX(9.5));
  const e=[roundRect(x,y,w,h,K.white,K.line,1),rect(x,y,w,5,segCol(p.gm)),
    tx(shortN(p.name),x+18,y+20,iw,nH,{size:T.cardH,bold:true,color:SL})];
  let fy=y+20+nH+10;
  [[p.units[5].toLocaleString('en-IN'),'FY32 UNITS'],[cr(p.fy32),'REVENUE'],[p.gm,'MARGIN']]
    .forEach(([v,l],i)=>{const fx=x+18+i*(iw/3);
      e.push(tx(v,fx,fy,fw,vH,{size:T.body,bold:true,color:CYT}));
      e.push(tx(l,fx,fy+vH,fw,lH,{size:PX(8),bold:true,color:GY}));});
  let cy=fy+vH+lH+10;
  e.push(rect(x+18,cy,iw,1,K.line));
  cy+=12;
  e.push(tx(p.what,x+18,cy,iw,wH,{size:PX(10.5),color:GY}));
  cy=y+h-18-poH-pkH;
  e.push(tx('POOL · '+p.capture,x+18,cy,iw,pkH,{size:PX(8),bold:true,color:TLT}));
  e.push(tx(p.pool,x+18,cy+pkH,iw,poH,{size:PX(9.5),color:GY}));
  return e;
}

const SURFCOL={'Road autonomy':CY,'Silicon & compute':TL,'Fleet & mobility':PB,'Sensors & robotics':GR};
const scol=s=>SURFCOL[s]||CY;

// 1 COVER
{const p=N();add([rect(0,0,1280,720,K.midnight),
  ...Array.from({length:11},(_,i)=>rect(864+i*38,0,1,720,'#14263C')),rect(0,0,1280,5,CY),
  ellipse(940,150,300,300,'#0E1E33','#16304C',2),ellipse(1000,210,180,180,'#101F36',CY,1),
  tx('STRICTLY CONFIDENTIAL  ·  PRE-SERIES A',80,110,700,24,{size:T.kicker,bold:true,color:CY}),
  tx('Product Lines',80,168,900,86,{size:T.cover,face:SERIF,bold:true,color:K.white}),
  tx('Fifteen SKUs. One chip.',80,268,900,56,{size:PX(26),face:SERIF,color:'#A9BACD'}),
  rect(80,348,150,3,CY),
  tx('A mandate creates the demand. One 28 nm chip serves it. Every SKU here runs the same silicon.',
     80,382,780,54,{size:PX(14),color:'#8FA2B7'}),
  roundRect(80,470,300,96,'#0E1E33','#1B3350',1),
  tx('₹1,128 Cr',104,492,260,44,{size:PX(28),face:SERIF,bold:true,color:K.white}),
  tx('FY2032 REVENUE, ALL SKUs',104,540,260,20,{size:T.kicker,bold:true,color:CY}),
  roundRect(400,470,300,96,'#0E1E33','#1B3350',1),
  tx('$3.88',424,492,260,44,{size:PX(28),face:SERIF,bold:true,color:K.white}),
  tx('COST PER DIE AT VOLUME',424,540,260,20,{size:T.kicker,bold:true,color:CY}),
  tx('All figures are management projections prepared for fundraising purposes.',80,616,1000,22,{size:T.foot,italic:true,color:'#6E8299'}),
  tx('August 2026',80,644,400,22,{size:T.foot,bold:true,color:'#8FA2B7'}),
],{background:K.midnight,notes:'Fifteen SKUs from Revenue Build rows 44-58 and 61-75. Surfaces from the section-A sum formulas. Pools from Demand & TAM section B.'});}

// 2 EXEC SUMMARY
{const p=N();add([
  ...hdr('The case','One chip, fifteen SKUs, one decision',
    'The portfolio is a consequence of the silicon — judge the round on the chip.',p),
  ...KPI2(48,178,286,'₹1,128 Cr','FY2032 revenue',CYT),
  ...KPI2(348,178,286,'15','SKUs on one chip',TLT),
  ...KPI2(648,178,286,'64%','Carried by two SKUs',GR),
  ...KPI2(948,178,284,'Under 2%','Share of every pool',PBT),
  ...(()=>{const f=flow(326,'exec',646);return [
    ...f.cards([
      [48,592,'The demand is legislated, not forecast',
       'India requires drowsiness, blind-spot and lane-departure systems on N2/N3 vehicles from April and October 2026 — a pool of one million trucks a year that must comply.',CYT],
      [656,576,'Fifteen SKUs, one engineering programme',
       'Every SKU runs the same SoC2 silicon under different firmware, across four platform surfaces. One tapeout, one certification path.',TLT]]),
    ...f.cards([[48,1184,'What this deck asks you to underwrite',
      'Not fifteen businesses. Two SKUs carry 64%, the silicon SKUs carry the margin, and every line sits under 2% of its own pool. The risk that matters is whether the chip lands.',CY,K.cool]]),
  ];})(),
],{notes:'Executive summary.'});}

// 3 MANDATE
{const p=N();add([
  ...hdr('Why now','The mandate is a demand floor, not a forecast',
    'Compliance dates are set. The buying decision is when, not whether.',p),
  ...KPI2(48,178,286,'1.0 M','Trucks a year in scope',CYT),
  ...KPI2(348,178,286,'0.5 M','New build, annually',TLT),
  ...KPI2(648,178,286,'0.5 M','Existing fleet retrofit',GR),
  ...KPI2(948,178,284,'18,000','Our FY2032 AD2 units',PBT),
  ...rail(48,356,1184,[
    ['MAR 2025','Rule notified','GSR 184(E) sets the obligation for N2/N3 vehicles',CYT,true],
    ['APR 2026','New models','Drowsiness, blind-spot and lane-departure required',CYT,true],
    ['OCT 2026','Existing models','Obligation reaches the in-service fleet',TLT,true],
    ['OCT 2027','Braking','Advanced emergency braking on a separate schedule',PBT,false]]),
  ...(()=>{const f=flow(512,'mandate',646);return [
    ...f.cards([[48,1184,'What a floor means for an investor',
      'A mandated purchase removes the hardest question in hardware — whether the buyer will pay for safety. Execution risk stays ours: certification and installation throughput.',CYT,K.cool]]),
  ];})(),
  tx('Source: MoRTH GSR 184(E), 20 March 2025.',48,652,1184,20,{size:T.foot,italic:true,color:GY}),
],{notes:'The 2026 dates cover the DDAWS/blind-spot/LDWS suite; AEBS sits on a separate 2027 schedule.'});}

// 4 THE GAP
{const p=N();add([
  ...hdr('The gap','Today that mandate is met with imported silicon',
    'The compute is available. It is not made here, and it is not priced for here.',p),
  ...barsNative(48,206,1184,[
    ['Incumbent ADAS module',3000,'#B9C7D6','$3,000 – 8,000'],
    ['DeepGrid SoC2 die at volume',3.88,CY,'$3.88']],
    {rowH:72,labelW:360,valW:220,max:3200}),
  ...(()=>{const f=flow(392,'gap',646);return [
    ...f.cards([
      [48,592,'Read the comparison honestly',
       'A bare die is not a finished module. The incumbent price includes packaging, board, software and support; ours is silicon only. The like-for-like system comparison is provided in diligence.',CYT],
      [656,576,'Why the gap is the opening',
       'Mature-node design, an India-tuned perception stack and domestic supply are what make a locally priced system possible.',TLT]]),
    ...f.note('Die cost is derived from a 57 mm² die, 94.5% yield and a $2,400 wafer, plus $1.50 assembly, test and packaging — not quoted as a target.'),
  ];})(),
],{notes:'Deliberately omits the 774x multiple: it compares a bare die to a complete module.'});}

// 5 THE CHIP
{const p=N();add([
  ...hdr('The move','One chip, priced for the mandate',
    'A phased 28 nm programme: prove the blocks, then the die, then commit the mask.',p),
  ...KPI2(48,178,286,'$3.17 M','Programme cost',CYT),
  ...KPI2(348,178,286,'$3.88','Cost per die',TLT),
  ...KPI2(648,178,286,'175k','Dies to repay it',GR),
  ...KPI2(948,178,284,'4','Gated stages',PBT),
  ...chain(48,368,1184,[
    ['Block prototypes','Compute and radar blocks on a shared wafer',CYT],
    ['Full-die prototype','57 mm² device, shared wafer',TLT],
    ['Backend to GDSII','Physical design and sign-off',PBT],
    ['Production mask','Committed only once silicon works',GR]],{nodeH:104}),
  ...(()=>{const f=flow(500,'chip',646);return [
    ...f.cards([[48,1184,'Why this is the thing to fund',
      'Silicon absorbs 66.2% of the equity round, and every SKU in this deck is downstream of it: no die, no kit, no box, no licence. Sign-off and the mask are committed only after working silicon exists.',CY,K.cool]]),
  ];})(),
],{notes:'Tapeout economics from the unit-economics schedule.'});}

// 6 THE PORTFOLIO TABLE — all 15, two columns
{const p=N();
 const sorted=[...SKUS].sort((a,b)=>b.fy32-a.fy32);
 const mk=arr=>arr.map(x=>[shortN(x.name),money(x.asp),x.units[5].toLocaleString('en-IN'),cr(x.fy32),x.share.toFixed(1)+'%']);
 const cols=[{t:'SKU',w:210},{t:'Price',w:96,a:'right'},{t:'FY32 units',w:104,a:'right'},
             {t:'Revenue',w:98,a:'right'},{t:'Share',w:76,a:'right'}];
 add([
  ...hdr('The portfolio','Fifteen SKUs across four platform surfaces',
    'Same silicon, different firmware, priced independently by market.',p),
  ...TBL(48,180,584,cols,mk(sorted.slice(0,8)),{headH:32,highlight:0}),
  ...TBL(648,180,584,cols,mk(sorted.slice(8)),{headH:32}),
  tx('Sorted by FY2032 revenue. Shares of ₹1,128.45 Cr; the fifteen SKUs reconcile to the total exactly.',
     48,652,1184,20,{size:T.foot,italic:true,color:GY}),
],{notes:'Source: Revenue Build rows 44-58 (units, price) and 61-75 (revenue).'});}

// 7 CONCENTRATION — 15 bars
{const p=N();add([
  ...hdr('Concentration','Two SKUs carry 64%, thirteen carry the rest',
    'FY2032 revenue by SKU. Colour shows platform surface.',p),
  ...barsNative(48,180,1184,[...SKUS].sort((a,b)=>b.fy32-a.fy32)
    .map(x=>[shortN(x.name),x.fy32,scol(x.surface),cr(x.fy32)]),{rowH:26,labelW:330,valW:120,max:460}),
  ...(()=>{const f=flow(586,'conc',646);return [
    ...f.note('AD2 and AD0 are the same product family sold to overlapping buyers, so a certification or installation delay hits ₹720 Cr at once — larger than the other thirteen SKUs combined.'),
  ];})(),
],{notes:'Source: Revenue Build FY2032 column, rows 61-75.'});}

// 8 LAUNCH SEQUENCING
{const p=N();
 const byYear=FYS.map((y,i)=>[y,SKUS.filter(s=>s.launch==='FY20'+y.slice(2)).map(s=>shortN(s.name))]);
 add([
  ...hdr('Sequencing','Six SKUs earn in FY2027, nine more in FY2028',
    'First revenue year per SKU. FY2027 is FPGA-based products only.',p),
  ...(()=>{const f=flow(178,'seq');return [
    ...f.tbl(48,1184,[{t:'First revenue',w:180},{t:'SKUs',w:110,a:'right'},
      {t:'What switches on',w:894}],
      byYear.filter(r=>r[1].length).map(r=>[r[0].replace('FY','FY20'),String(r[1].length),r[1].join(' · ')]),
      {headH:34,highlight:0}),
    ...f.cards([[48,1184,'Why the shape matters',
      'FY2027 revenue is FPGA-based product and robot sales only — ₹1.7 Cr across six SKUs. Nine more SKUs begin earning in FY2028 as ASIC-era product reaches market, and the licence line starts in FY2029. The ramp is gated by silicon, which is what the round funds.',CY,K.cool]]),
  ];})(),
],{notes:'Launch year derived as the first year with non-zero revenue per SKU, rows 61-75.'});}

// 9 DOMAIN SPLIT
{const p=N();add([
  ...hdr('Where autonomy runs','Outdoor carries it; indoor ships L4 sooner',
    'The same silicon across three operating domains, with different regulatory exposure.',p),
  ...KPI2(48,178,286,'86.3%','Outdoor autonomy',CYT),
  ...KPI2(348,178,286,'8.0%','General compute',TLT),
  ...KPI2(648,178,286,'5.7%','Indoor autonomy',GR),
  ...KPI2(948,178,284,'15','SKUs in total',PBT),
  ...(()=>{const f=flow(306,'domain',646);return [
    ...f.tbl(48,1184,[{t:'Domain',w:260},{t:'SKUs',w:110,a:'right'},
      {t:'FY2032 revenue',w:200,a:'right'},{t:'Share',w:140,a:'right'},{t:'What it covers',w:474}],
      DOMAINS.map(d=>[d[0],String(d[3]),cr(d[1]),d[2].toFixed(1)+'%',d[4]]),{headH:34,highlight:0}),
    ...f.cards([[48,1184,'The regulatory asymmetry',
      'Outdoor revenue depends on homologation and public-road rules. Indoor is geofenced, so level-4 ships years earlier on the same chip. Compute carries no vehicle exposure at all.',CYT,K.cool]]),
  ];})(),
],{notes:'Source: Revenue Build section C, indoor/outdoor/compute totals rows 25-29.'});}

// 10..n SURFACE SLIDES + the two deep dives
const DEEP = { 'Smart Truck (AD2 kit)':'ad2', 'AD0 Smart Mirror (mandate retrofit)':'ad0' };
for (const surf of SURFACES) {
  const members = SKUS.filter(x => x.surface === surf.name);
  // surface overview: every SKU in the surface, three to a slide
  for (let i = 0; i < members.length; i += 3) {
    const grp = members.slice(i, i + 3), p = N();
    const n = grp.length, gap = 14, w = (1184 - (n - 1) * gap) / n;
    const h = Math.max(...grp.map(g => colH(w, g)));
    const cont = members.length > 3 ? ` (${i / 3 + 1} of ${Math.ceil(members.length / 3)})` : '';
    add([
      ...hdr(surf.name, surf.title + cont,
        `${cr(surf.rev)} · ${surf.share}% of FY2032 · ${members.length} SKUs · ${surf.gm} gross margin`, p),
      ...grp.map((g, j) => col(48 + j * (w + gap), 186, w, h, g)).flat(),
      ...(() => { const f = flow(186 + h + 18, 'surf-' + surf.name + i, 646); return [
        ...f.note(grp.map(g => `${shortN(g.name)}: ${g.why}`).join('  ')),
      ]; })(),
      (() => { const t = 'Demand pool sources: ' + grp.map(g => `${shortN(g.name)} — ${g.source || 'no separately sized pool'}`).join('; ') + '.';
               const th = TH(t, 1184, T.foot); return tx(t, 48, 676 - th, 1184, th, { size: T.foot, italic: true, color: GY }); })(),
    ], { notes: grp.map(g => `${g.name}: ${g.units.join('/')} units at ${money(g.asp)}, revenue ${g.rev.join('/')} ₹Cr, FY2032 ${cr(g.fy32)} (${g.share}%), ${g.gm} margin, first revenue ${g.launch}. Domain ${g.domain}. Pool: ${g.pool || 'none sized'}.`).join(' ') });
  }
  // deep dives immediately after their surface
  for (const g of members) {
    const slug = DEEP[g.name]; if (!slug) continue;
    const u = UNDERWRITE[slug], p = N();
    add([
      ...hdr(g.surface + ' · deep dive', slug === 'ad2' ? 'AD2 sells against a legal obligation'
                                                        : 'AD0 already sells without a mandate',
        slug === 'ad2' ? 'The largest SKU in the plan, and the only one whose buyer must comply.'
                       : 'Voluntary demand in a market that already exists.', p),
      ...KPI2(48,178,286,g.units[5].toLocaleString('en-IN'),'FY2032 units',CYT),
      ...KPI2(348,178,286,money(g.asp),'Unit price',TLT),
      ...KPI2(648,178,286,cr(g.fy32),'FY2032 revenue',GR),
      ...KPI2(948,178,284,g.share.toFixed(1)+'%','Share of FY2032',PBT),
      tx('UNITS SHIPPED',48,326,300,16,{size:T.kicker,bold:true,color:CYT}),
      ...ramp(48,374,540,74,g.units),
      tx('REVENUE, ₹ CR',636,326,300,16,{size:T.kicker,bold:true,color:CYT}),
      ...ramp(636,374,596,74,g.rev.map(v=>Math.round(v))),
      tx('WHAT MUST BE TRUE',48,486,400,16,{size:T.kicker,bold:true,color:CYT}),
      ...u.must.map((m,i)=>{const cx=48+i*396,cw=384;
        return [roundRect(cx,508,cw,116,K.white,K.line,1),rect(cx,508,cw,4,CY),
          tx(m[0],cx+16,520,cw-32,22,{size:PX(11.5),bold:true,color:SL}),
          tx(m[1],cx+16,546,cw-32,68,{size:PX(9.5),color:GY})];}).flat(),
      tx(u.evidence+'  Demand pool: '+g.pool+' · '+g.capture+' capture · source: '+g.source+'.',
         48,634,1184,32,{size:T.foot,italic:true,color:GY}),
    ],{notes:`${g.name}. Units ${g.units.join(' / ')} at ${money(g.asp)}; revenue ${g.rev.join(' / ')} ₹Cr. FY2032 ${cr(g.fy32)} = ${g.share}% of ₹1,128.45 Cr at ${g.gm}. Pool source: ${g.source}.`});
  }
}

// MARGIN LADDER
{const p=N();
 const segs=['Systems','Semiconductors','Robotics','Sensors'];
 const rows=segs.map(s=>{const m=SKUS.filter(x=>x.segment===s);
   const t=m.reduce((a,x)=>a+x.fy32,0);
   return [s,String(m.length),cr(t),(t/1128.45*100).toFixed(1)+'%',m[0].gm];});
 add([
  ...hdr('Margin','Volume and margin sit in different places',
    'Systems carry the revenue; semiconductors carry the profit per rupee.',p),
  ...(()=>{const f=flow(178,'ladder',646);return [
    ...f.tbl(48,1184,[{t:'Segment',w:280},{t:'SKUs',w:110,a:'right'},{t:'FY2032 revenue',w:210,a:'right'},
      {t:'Share of revenue',w:210,a:'right'},{t:'FY2032 gross margin',w:374,a:'right'}],rows,{headH:34,highlight:1}),
    ...f.cards([[48,1184,'How to read the two together',
      'Group economics track systems, because systems are 83.4% of revenue. But the marginal rupee is worth most in semiconductors at 94%, and those SKUs need no installation capacity. Growth in the silicon SKUs improves group margin without adding operational load.',CYT,K.cool]]),
  ];})(),
],{notes:'Segment revenue computed from the 15 SKUs; margins from the assumptions schedule.'});}

// HEADROOM
{const p=N();
 // Demand & TAM lists one pool row per product family: the three A100 SKUs share a
 // single row at 0.20%. Collapse them so the chart matches the source, not the SKU list.
 const seen=new Set();
 const sized=SKUS.filter(x=>{
   if(x.capture==='—') return false;
   const key=x.pool; if(seen.has(key)) return false; seen.add(key); return true;});
 add([
  ...hdr('Headroom','No SKU assumes we win its market',
    'FY2032 share of each SKU\'s own sized demand pool. Axis runs to 2%.',p),
  ...barsNative(48,190,1184,sized.map(x=>[x.name.startsWith('A100')?'A100 compute box (3 SKUs)':shortN(x.name),parseFloat(x.capture),
    parseFloat(x.capture)>1?CY:PB,x.capture]),{rowH:34,labelW:330,valW:110,max:2.0}),
  ...(()=>{const f=flow(468,'head',640);return [
    ...f.cards([
      [48,592,'Why the shares look small',
       'Most pools are global while our serviceable market is the India slice, so the real share is higher. The three A100 SKUs share one pool row; T100 has none.',CYT],
      [656,576,'The one to read differently',
       'Seaport AGV shows 0.02% against a pool that is total port automation, cranes and software included. We sell only the vehicle layer.',TLT]]),
  ];})(),
  tx('Capture rates are management assumptions; pool sizes are third-party published estimates.',48,652,1184,20,{size:T.foot,italic:true,color:GY}),
],{notes:'Source: Demand & TAM section B, capture column.'});}

// THE ASK
{const p=N();add([
  rect(0,0,1280,720,K.midnight),rect(0,0,1280,5,CY),
  ...Array.from({length:9},(_,i)=>rect(940+i*38,0,1,720,'#14263C')),
  tx('THE ASK',80,96,700,24,{size:T.kicker,bold:true,color:CY}),
  tx('Fund the silicon; the portfolio follows',80,142,1000,60,{size:PX(30),face:SERIF,bold:true,color:K.white}),
  tx('Fifteen SKUs, one tapeout. Release capital against silicon, certification and paying customers — not against the forecast.',
     80,214,1040,48,{size:PX(14),color:'#A9BACD'}),
  rect(80,282,140,3,CY),
  ...[['Legislated demand','A million trucks a year must comply from 2026'],
      ['One tapeout','All fifteen SKUs downstream of a single 28 nm chip'],
      ['Margin where it counts','94% on silicon, needing no installation capacity'],
      ['A floor, not a stretch','Under 2% of every sized pool, prices flat six years']]
    .map(([t2,b],i)=>{const x=80+i*292;return [
      roundRect(x,324,272,150,'#0E1E33','#1B3350',1),rect(x,324,272,4,[CY,TL,GR,PB][i]),
      tx(t2,x+20,348,232,48,{size:T.cardH,bold:true,color:K.white}),
      tx(b,x+20,400,232,78,{size:PX(11),color:'#8FA2B7'})];}).flat(),
  roundRect(80,512,1120,92,'#0E1E33',CY,1),
  tx('The portfolio is not fifteen bets. It is one bet, fifteen times over.',
     112,536,1056,52,{size:PX(15),italic:true,face:SERIF,color:K.white}),
  tx('All figures are management projections prepared for fundraising purposes and are not audited or reported results.',
     80,634,1000,20,{size:T.foot,italic:true,color:'#6E8299'}),
  tx('DEEPGRID SEMI  ·  PRODUCT LINES  ·  AUGUST 2026',80,662,700,20,{size:T.foot,bold:true,color:'#8FA2B7'}),
  tx(String(p).padStart(2,'0'),1160,662,72,20,{size:T.foot,bold:true,color:'#8FA2B7',align:'right'}),
],{background:K.midnight,notes:'Decision slide.'});}

for (const [c,o] of S) addSlide(c,o);
if (VIOLATIONS.length){console.log('LAYOUT VIOLATIONS:');VIOLATIONS.forEach(v=>console.log('  '+v));}
else console.log('layout guard: clean');
await (await PresentationFile.exportPptx(P)).save(OUT);
console.log(`OK slides=${S.length} -> ${OUT}`);
