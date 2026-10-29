import { P, C, K, SERIF, addSlide, tx, rect, roundRect, ellipse, sh,
         PresentationFile, OUT, PX, T, divider, barsNative, rail, chain,
         CY, TL, GR, PB, SL, GY, CYT, PBT, TLT,
         hdr, TH, CARD, CARDH, KPI, TBL, flow, VIOLATIONS } from './deck-lib.mjs';
import { PRODUCTS, BY_SEGMENT, TIERS, UNDERWRITE, FYS } from './data_products.mjs';

const S=[]; const add=(c,o={})=>S.push([c,o]);
let pg=0; const N=()=>++pg;
const cr=v=>`₹${v>=100?Math.round(v):v.toFixed(v<10?2:1)} Cr`;
const byId=s=>PRODUCTS.find(p=>p.slug===s);
const segCol=g=>g==='89%'?CY:g==='94%'?TL:g==='68%'?GR:PB;
const shortN=n=>n.replace(/\s*\([^)]*\)/g,'').replace('driver-monitor wearable','driver monitor');

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
  [[p.units[5].toLocaleString('en-IN'),'FY32 UNITS'],[cr(p.rev),'REVENUE'],[p.gm,'MARGIN']]
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

// 1 COVER
{const p=N();add([rect(0,0,1280,720,K.midnight),
  ...Array.from({length:11},(_,i)=>rect(864+i*38,0,1,720,'#14263C')),rect(0,0,1280,5,CY),
  ellipse(940,150,300,300,'#0E1E33','#16304C',2),ellipse(1000,210,180,180,'#101F36',CY,1),
  tx('STRICTLY CONFIDENTIAL  ·  PRE-SERIES A',80,110,700,24,{size:T.kicker,bold:true,color:CY}),
  tx('Product Lines',80,168,900,86,{size:T.cover,face:SERIF,bold:true,color:K.white}),
  tx('One chip. Thirteen products.',80,268,900,56,{size:PX(26),face:SERIF,color:'#A9BACD'}),
  rect(80,348,150,3,CY),
  tx('A mandate creates the demand. One 28 nm chip serves it. The portfolio follows from the silicon.',
     80,382,780,54,{size:PX(14),color:'#8FA2B7'}),
  roundRect(80,470,300,96,'#0E1E33','#1B3350',1),
  tx('₹1,128 Cr',104,492,260,44,{size:PX(28),face:SERIF,bold:true,color:K.white}),
  tx('FY2032 REVENUE, ALL LINES',104,540,260,20,{size:T.kicker,bold:true,color:CY}),
  roundRect(400,470,300,96,'#0E1E33','#1B3350',1),
  tx('$3.88',424,492,260,44,{size:PX(28),face:SERIF,bold:true,color:K.white}),
  tx('COST PER DIE AT VOLUME',424,540,260,20,{size:T.kicker,bold:true,color:CY}),
  tx('All figures are management projections prepared for fundraising purposes.',80,616,1000,22,{size:T.foot,italic:true,color:'#6E8299'}),
  tx('August 2026',80,644,400,22,{size:T.foot,bold:true,color:'#8FA2B7'}),
],{background:K.midnight,notes:'Product-line pitch. Story spine in story-pack-product-lines.md. Units and price from Revenue Build; pools and sources from Demand & TAM section B.'});}

// 2 EXEC SUMMARY
{const p=N();add([
  ...hdr('The case','One chip, thirteen products, one decision',
    'The portfolio is a consequence of the silicon — judge the round on the chip.',p),
  ...KPI2(48,178,286,'₹1,128 Cr','FY2032 revenue',CYT),
  ...KPI2(348,178,286,'13','Product lines',TLT),
  ...KPI2(648,178,286,'64%','Carried by two lines',GR),
  ...KPI2(948,178,284,'Under 2%','Share of every pool',PBT),
  ...(()=>{const f=flow(326,'exec',646);return [
    ...f.cards([
      [48,592,'The demand is legislated, not forecast',
       'India requires driver-drowsiness, blind-spot and lane-departure systems on N2/N3 vehicles from April and October 2026. That is a pool of one million trucks a year that must comply.',CYT],
      [656,576,'The portfolio is downstream of one tapeout',
       'Every line here runs the same SoC2 silicon under different firmware. Thirteen products, one engineering programme, one certification path.',TLT]]),
    ...f.cards([[48,1184,'What this deck asks you to underwrite',
      'Not thirteen businesses. Two mandate-adjacent lines carry 64%, the silicon lines carry the margin, and every line sits under 2% of its own pool. The risk that matters is whether the chip lands.',CY,K.cool]]),
  ];})(),
],{notes:'Executive summary. Beats 1-3 of the argument arc compressed for a reader who stops here.'});}

// 3 THE MANDATE
{const p=N();add([
  ...hdr('Why now','The mandate is a demand floor, not a forecast',
    'Compliance dates are set. The buying decision is when, not whether.',p),
  ...KPI2(48,178,286,'1.0 M','Trucks a year in scope',CYT),
  ...KPI2(348,178,286,'0.5 M','New build, annually',TLT),
  ...KPI2(648,178,286,'0.5 M','Existing fleet retrofit',GR),
  ...KPI2(948,178,284,'18,000','Our FY2032 units',PBT),
  ...rail(48,356,1184,[
    ['MAR 2025','Rule notified','GSR 184(E) sets the obligation for N2/N3 vehicles',CYT,true],
    ['APR 2026','New models','Drowsiness, blind-spot and lane-departure required',CYT,true],
    ['OCT 2026','Existing models','Obligation reaches the in-service fleet',TLT,true],
    ['OCT 2027','Braking','Advanced emergency braking on a separate schedule',PBT,false]]),
  ...(()=>{const f=flow(512,'mandate',646);return [
    ...f.cards([[48,1184,'What a floor means for an investor',
      'A mandated purchase removes the hardest question in hardware — whether the buyer will pay for safety. Execution risk stays ours: certification and installation throughput.',CYT,K.cool]]),
  ];})(),
  tx('Source: MoRTH GSR 184(E), 20 March 2025. Pool sizing from the demand schedule.',48,652,1184,20,{size:T.foot,italic:true,color:GY}),
],{notes:'Beat 1. The 2026 dates cover the DDAWS/blind-spot/LDWS suite. AEBS (AIS-162/IS-11852) sits on a separate 2027 schedule — two obligations, two timetables.'});}

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
       'Mature-node design, an India-tuned perception stack and domestic supply are what make a locally priced system possible. Without an Indian part, the mandate is met at foreign margins.',TLT]]),
    ...f.note('Die cost is derived from a 57 mm² die, 94.5% yield and a $2,400 wafer, plus $1.50 assembly, test and packaging — not quoted as a target.'),
  ];})(),
],{notes:'Beat 2. Deliberately does NOT present the 774x multiple the workbook computes: it compares a bare die to a complete module.'});}

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
      'Silicon absorbs 66.2% of the equity round, and every line in this deck is downstream of it: no die, no kit, no box, no licence. Sign-off and the mask are committed only after working silicon exists.',CY,K.cool]]),
  ];})(),
],{notes:'Beat 3. Tapeout economics from the unit-economics schedule; use-of-funds share from the funding schedule.'});}

// 6 PORTFOLIO AS CONSEQUENCE
{const p=N();add([
  ...hdr('The portfolio','Thirteen products are a consequence of one chip',
    'Same silicon, same stack, different firmware and different buyer.',p),
  ...chain(48,190,1184,[
    ['SoC2 · 28 nm','One transformer-native ASIC',CYT],
    ['Common stack','Perception, planning, diagnostics',TLT],
    ['Four surfaces','Road · silicon · fleet · sensing',PBT],
    ['Thirteen lines','Priced independently by market',GR]],{nodeH:104}),
  ...(()=>{const f=flow(322,'portfolio',646);return [
    ...f.tbl(48,1184,[{t:'Tier',w:300},{t:'Lines',w:120,a:'right'},
      {t:'FY2032 revenue',w:240,a:'right'},{t:'Share',w:180,a:'right'},{t:'What it contributes',w:344}],
      [['Core volume — AD2, AD0','2',cr(720),'63.8%','The mandated and near-mandated volume core'],
       ['Silicon monetisation','3',cr(194.30),'17.2%','The margin: die, compute boxes and licence'],
       ['Adjacent platforms','5',cr(180.65),'16.0%','Option value on new procurement cycles'],
       ['Sensor attach','3',cr(33.50),'3.0%','Capability and channel access']],
      {headH:34,highlight:0}),
  ];})(),
],{notes:'Beat 4. Tier totals reconcile to ₹1,128.45 Cr; verified against per-line revenue.'});}

// 7 CONCENTRATION
{const p=N();add([
  ...hdr('Concentration','Two lines carry 64% — by design',
    'FY2032 revenue by line. Colour shows segment: systems, silicon, robotics, sensors.',p),
  ...barsNative(48,186,1184,[...PRODUCTS].sort((a,b)=>b.rev-a.rev)
    .map(x=>[shortN(x.name),x.rev,segCol(x.gm),cr(x.rev)]),{rowH:29,labelW:320,valW:120,max:460}),
  ...(()=>{const f=flow(578,'conc',646);return [
    ...f.note('AD2 and AD0 are the same product family sold to overlapping buyers, so a certification or installation delay hits ₹720 Cr at once. That single exposure is larger than the rest of the portfolio combined.'),
  ];})(),
],{notes:'Beat 5. Source: revenue build, FY2032 column.'});}

// 8-9 THE TWO MATERIAL LINES
for (const slug of ['ad2','ad0']) {
  const x=byId(slug),u=UNDERWRITE[slug],p=N();
  add([
    ...hdr(x.kicker,x.title,x.tag,p),
    ...KPI2(48,178,286,x.units[5].toLocaleString('en-IN'),'FY2032 units',CYT),
    ...KPI2(348,178,286,x.asp,'Unit price',TLT),
    ...KPI2(648,178,286,cr(x.rev),'FY2032 revenue',GR),
    ...KPI2(948,178,284,x.share.toFixed(1)+'%','Share of FY2032',PBT),
    tx('UNITS SHIPPED',48,326,400,16,{size:T.kicker,bold:true,color:CYT}),
    ...ramp(48,374,540,74,x.units),
    ...CARD(636,326,596,'auto','What it is, and who buys it',x.what+' '+x.buyer,CYT),
    tx('WHAT MUST BE TRUE',48,486,400,16,{size:T.kicker,bold:true,color:CYT}),
    ...u.must.map((m,i)=>{const cx=48+i*396,cw=384;
      return [roundRect(cx,508,cw,116,K.white,K.line,1),rect(cx,508,cw,4,CY),
        tx(m[0],cx+16,520,cw-32,22,{size:PX(11.5),bold:true,color:SL}),
        tx(m[1],cx+16,546,cw-32,68,{size:PX(9.5),color:GY})];}).flat(),
    tx(u.evidence+'  Demand pool: '+x.pool+' · '+x.capture+' capture · source: '+x.source+'.',
       48,634,1184,32,{size:T.foot,italic:true,color:GY}),
  ],{notes:`${x.name}. Units ${x.units.join(' / ')} at ${x.asp} = ${cr(x.rev)} (${x.share.toFixed(1)}% of ₹1,128.45 Cr) at ${x.gm} segment margin. Pool source: ${x.source}.`});
}

// 10-12 TIER SLIDES
const tierSlides=[
 {id:'silicon',title:'Three ways to sell the chip without a vehicle',
  sub:'₹194.3 Cr at 94% gross margin — the most profitable revenue in the plan.',
  note:'These lines need no installation capacity, no homologation and no channel build. They are pure downstream value from the tapeout, and they are why the silicon is the thing to fund.'},
 {id:'adjacent',title:'Same silicon, a different buyer',
  sub:'₹180.65 Cr across five lines on procurement cycles unlike automotive.',
  note:'Indoor autonomy ships level-4 behaviour years before it is legal on a road; defence has already paid ₹1 Cr on FPGA hardware. Each opens a buyer that does not depend on the vehicle mandate.'},
 {id:'sensors',title:'Sensors are carried for capability, not profit',
  sub:'₹33.5 Cr at 50% gross margin — the lowest in the portfolio, and stated plainly.',
  note:'Indian night and fog are exactly where camera-only systems fail, so thermal and radar earn their place on capability. The radar block is already on the die, so the incremental cost is low.'},
];
for (const ts of tierSlides) {
  const t=TIERS.find(z=>z.id===ts.id), all=t.slugs.map(byId);
  for (let i=0;i<all.length;i+=3){
    const members=all.slice(i,i+3), p=N();
    const n=members.length, gap=14, w=(1184-(n-1)*gap)/n;
    const h=Math.max(...members.map(g=>colH(w,g)));
    const cont=all.length>3 ? ` (${i/3+1} of ${Math.ceil(all.length/3)})` : '';
    add([
      ...hdr(t.label,ts.title+cont,ts.sub,p),
      ...members.map((g,j)=>col(48+j*(w+gap),186,w,h,g)).flat(),
      ...(()=>{const f=flow(186+h+18,'tier-'+ts.id+i,646);return [ ...f.note(ts.note) ];})(),
      (()=>{const t='Demand pool sources: '+members.map(g=>`${shortN(g.name)} — ${g.source}`).join('; ')+'.';
            const h=TH(t,1184,T.foot); return tx(t,48,676-h,1184,h,{size:T.foot,italic:true,color:GY});})(),
    ],{notes:members.map(g=>`${g.name}: ${g.units.join('/')} units at ${g.asp} = ${cr(g.rev)} (${g.share.toFixed(1)}%), ${g.gm} margin. ${g.why}`).join(' ')});
  }
}

// 13 MARGIN LADDER
{const p=N();add([
  ...hdr('Margin','Volume and margin sit in different places',
    'Systems carry the revenue; semiconductors carry the profit per rupee.',p),
  ...(()=>{const f=flow(178,'ladder',646);return [
    ...f.tbl(48,1184,[{t:'Segment',w:300},{t:'FY2032 revenue',w:220,a:'right'},
      {t:'Share of revenue',w:220,a:'right'},{t:'FY2032 gross margin',w:220,a:'right'},{t:'Role',w:224}],
      [['Systems',cr(940.95),'83.4%','89%','Volume and the mandate'],
       ['Semiconductors',cr(104.00),'9.2%','94%','Profit per rupee of revenue'],
       ['Robotics',cr(50.00),'4.4%','68%','Defence and drone optionality'],
       ['Sensors',cr(33.50),'3.0%','50%','Capability and channel']],{headH:34,highlight:1}),
    ...f.cards([[48,1184,'How to read the two together',
      'Group economics track systems, because systems are 83.4% of revenue. But the marginal rupee is worth most in semiconductors at 94%, and that line needs no installation capacity. Growth in the silicon lines improves group margin without adding operational load.',CYT,K.cool]]),
  ];})(),
],{notes:'Beat 6. Segment revenue from the revenue build; margins from the assumptions schedule.'});}

// 14 HEADROOM
{const p=N();const sized=PRODUCTS.filter(x=>x.capture!=='—');add([
  ...hdr('Headroom','No line assumes we win its market',
    'FY2032 share of each line\'s own sized demand pool. Axis runs to 2%.',p),
  ...barsNative(48,190,1184,sized.map(x=>[shortN(x.name),parseFloat(x.capture),
    parseFloat(x.capture)>1?CY:PB,x.capture]),{rowH:34,labelW:320,valW:110,max:2.0}),
  ...(()=>{const f=flow(478,'head',640);return [
    ...f.cards([
      [48,592,'Why the shares look small',
       'Most pools are global while our serviceable market is the India slice, so the real share is higher. Five lines have no sized pool and are excluded.',CYT],
      [656,576,'The one to read differently',
       'Seaport AGV shows 0.02% against a pool that is total port automation, cranes and software included. We sell only the vehicle layer.',TLT]]),
  ];})(),
  tx('Capture rates are management assumptions; pool sizes are third-party published estimates.',48,652,1184,20,{size:T.foot,italic:true,color:GY}),
],{notes:'Beat 7. Source: demand schedule, capture column.'});}

// 15 THE ASK
{const p=N();add([
  rect(0,0,1280,720,K.midnight),rect(0,0,1280,5,CY),
  ...Array.from({length:9},(_,i)=>rect(940+i*38,0,1,720,'#14263C')),
  tx('THE ASK',80,96,700,24,{size:T.kicker,bold:true,color:CY}),
  tx('Fund the silicon; the portfolio follows',80,142,1000,60,{size:PX(30),face:SERIF,bold:true,color:K.white}),
  tx('Thirteen lines, one tapeout. Release capital against silicon, certification and paying customers — not against the forecast.',
     80,214,1040,48,{size:PX(14),color:'#A9BACD'}),
  rect(80,282,140,3,CY),
  ...[['Legislated demand','A million trucks a year must comply from 2026'],
      ['One tapeout','Every line downstream of a single 28 nm chip'],
      ['Margin where it counts','94% on silicon, needing no installation capacity'],
      ['A floor, not a stretch','Under 2% of every sized pool, prices flat six years']]
    .map(([t2,b],i)=>{const x=80+i*292;return [
      roundRect(x,324,272,150,'#0E1E33','#1B3350',1),rect(x,324,272,4,[CY,TL,GR,PB][i]),
      tx(t2,x+20,348,232,48,{size:T.cardH,bold:true,color:K.white}),
      tx(b,x+20,400,232,78,{size:PX(11),color:'#8FA2B7'})];}).flat(),
  roundRect(80,512,1120,92,'#0E1E33',CY,1),
  tx('The portfolio is not thirteen bets. It is one bet, thirteen times over.',
     112,536,1056,52,{size:PX(15),italic:true,face:SERIF,color:K.white}),
  tx('All figures are management projections prepared for fundraising purposes and are not audited or reported results.',
     80,634,1000,20,{size:T.foot,italic:true,color:'#6E8299'}),
  tx('DEEPGRID SEMI  ·  PRE-SERIES A  ·  AUGUST 2026',80,662,700,20,{size:T.foot,bold:true,color:'#8FA2B7'}),
  tx(String(p).padStart(2,'0'),1160,662,72,20,{size:T.foot,bold:true,color:'#8FA2B7',align:'right'}),
],{background:K.midnight,notes:'Beat 8. Decision slide; gate language matches the walkthrough deck.'});}

for (const [c,o] of S) addSlide(c,o);
if (VIOLATIONS.length){console.log('LAYOUT VIOLATIONS:');VIOLATIONS.forEach(v=>console.log('  '+v));}
else console.log('layout guard: clean');
await (await PresentationFile.exportPptx(P)).save(OUT);
console.log(`OK slides=${S.length} -> ${OUT}`);
