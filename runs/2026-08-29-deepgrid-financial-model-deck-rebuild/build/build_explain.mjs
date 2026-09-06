import { writeFileSync } from 'node:fs';
import { P, C, K, SERIF, addSlide, tx, rect, roundRect, ellipse, sh,
         PresentationFile, OUT, PX, T, divider, barsNative, rail, chain,
         CY, TL, GR, PB, SL, GY, CYT, PBT, TLT,
         hdr, TH, CARD, CARDH, KPI, TBL, flow, VIOLATIONS } from './deck-lib.mjs';
import { SKUS, SURFACES, DOMAINS, FYS } from './data_sku.mjs';
import { EXPLAIN } from './data_explain.mjs';
import { UNDERWRITE } from './data_products.mjs';

const S=[]; const add=(c,o={})=>S.push([c,o]);
const SEATS=[];   // {slide,x,y,w,h,video} -- where a clip is dropped later
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


// numbered step card, used by the signal-chain slide
function step(x,y,w,n,text,color){
  const h=TH(text,w-92,T.body)+72;
  return [roundRect(x,y,w,h,K.white,K.line,1), rect(x,y,w,4,color),
    ellipse(x+18,y+20,26,26,color,color,1),
    tx(String(n),x+18,y+25,26,18,{size:PX(10),bold:true,color:K.white,align:'center'}),
    tx(text,x+54,y+20,w-72,TH(text,w-92,T.body)+14,{size:T.body,color:SL})];
}
const stepH=(w,t)=>TH(t,w-92,T.body)+72;

// ============================== PART 0 · THE CASE ============================
{const p=N();add([rect(0,0,1280,720,K.midnight),
  ...Array.from({length:11},(_,i)=>rect(864+i*38,0,1,720,'#14263C')),rect(0,0,1280,5,CY),
  ellipse(940,150,300,300,'#0E1E33','#16304C',2),ellipse(1000,210,180,180,'#101F36',CY,1),
  tx('STRICTLY CONFIDENTIAL  ·  PRE-SERIES A',80,110,700,24,{size:T.kicker,bold:true,color:CY}),
  tx('Product Lines',80,168,900,86,{size:T.cover,face:SERIF,bold:true,color:K.white}),
  tx('Fifteen SKUs, explained',80,268,900,56,{size:PX(26),face:SERIF,color:'#A9BACD'}),
  rect(80,348,150,3,CY),
  tx('For each product: what it is, how it works on the shared silicon, who buys it, and what it contributes.',
     80,382,800,54,{size:PX(14),color:'#8FA2B7'}),
  roundRect(80,470,300,96,'#0E1E33','#1B3350',1),
  tx('15 SKUs',104,492,260,44,{size:PX(28),face:SERIF,bold:true,color:K.white}),
  tx('FOUR SLIDES EACH',104,540,260,20,{size:T.kicker,bold:true,color:CY}),
  roundRect(400,470,300,96,'#0E1E33','#1B3350',1),
  tx('One chip',424,492,260,44,{size:PX(28),face:SERIF,bold:true,color:K.white}),
  tx('SoC2 · 28 NM',424,540,260,20,{size:T.kicker,bold:true,color:CY}),
  tx('All figures are management projections prepared for fundraising purposes.',80,616,1000,22,{size:T.foot,italic:true,color:'#6E8299'}),
  tx('August 2026',80,644,400,22,{size:T.foot,bold:true,color:'#8FA2B7'}),
],{background:K.midnight,notes:'SKU explainer. Storyboard: storyboard-sku-explainer.md. Figures: Revenue Build rows 44-58 and 61-75; pools from Demand & TAM section B.'});}

{const p=N();add([
  ...hdr('How to read this deck','Every SKU gets the same four slides',
    'Learn the pattern once and you can navigate all fifteen products.',p),
  ...chain(48,196,1184,[
    ['A · What it is','If you held one, what would you be holding',CYT],
    ['B · How it works','What the silicon actually does in this product',TLT],
    ['C · Who buys it','Buyer, channel and the trigger to purchase',PBT],
    ['D · How it fits','What it contributes and what it depends on',GR]],{nodeH:104}),
  ...(()=>{const f=flow(328,'read',646);return [
    ...f.tbl(48,1184,[{t:'Part',w:300},{t:'SKUs',w:120,a:'right'},{t:'FY2032 revenue',w:220,a:'right'},
      {t:'Share',w:150,a:'right'},{t:'Role in the portfolio',w:394}],
      SURFACES.map(s=>[s.name,String(SKUS.filter(x=>x.surface===s.name).length),cr(s.rev),
        s.share+'%',s.title]),{headH:34,highlight:0}),
    ...f.cards([[48,1184,'The one thing to carry through',
      'Every SKU here runs the same SoC2 silicon under different firmware — one tapeout, not fifteen independent product bets.',CYT,K.cool]]),
  ];})(),
],{notes:'Reading key. The four-slide unit is the deck grammar.'});}

{const p=N();add([
  ...hdr('Why now','The mandate is a demand floor, not a forecast',
    'Compliance dates are set. The buying decision is when, not whether.',p),
  ...KPI2(48,178,286,'1.0 M','Trucks a year in scope',CYT),
  ...KPI2(348,178,286,'0.5 M','New build, annually',TLT),
  ...KPI2(648,178,286,'0.5 M','Existing fleet retrofit',GR),
  ...KPI2(948,178,284,'18,000','Our FY2032 AD2 units',PBT),
  ...rail(48,356,1184,[
    ['MAR 2025','Rule notified','Sets the ADAS obligation for N2/N3 vehicles',CYT,true],
    ['APR 2026','New models','Drowsiness, blind-spot and lane-departure required',CYT,true],
    ['OCT 2026','Existing models','Obligation reaches the in-service fleet',TLT,true],
    ['OCT 2027','Braking','Advanced emergency braking on a separate schedule',PBT,false]]),
  ...(()=>{const f=flow(512,'mandate',646);return [
    ...f.cards([[48,1184,'What a floor means for an investor',
      'A mandated purchase removes the hardest question in hardware — whether the buyer will pay for safety. Execution risk stays ours: certification and installation throughput.',CYT,K.cool]]),
  ];})(),
],{notes:'Mandate framing per the demand schedule.'});}

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
      'Silicon absorbs 66.2% of the equity round, and every SKU in this deck is downstream of it. Sign-off and the mask are committed only after working silicon exists.',CY,K.cool]]),
  ];})(),
],{notes:'Tapeout economics from the unit-economics schedule.'});}

{const p=N();add([
  ...hdr('The silicon','What the part actually is',
    'One 28 nm die under every SKU in this deck. Configuration changes; the compute does not.',p),
  ...(()=>{const f=flow(172,'soc2',646);return [
    ...f.tbl(48,1184,[{t:'Parameter',w:210},{t:'Specification',w:430},{t:'Why an investor should care',w:544}],[
      ['Process','TSMC 28 nm · single die, ~57 mm²','Monolithic, not chiplet — less cost and less risk.'],
      ['Compute','32,768 MACs at 600 MHz · 39.3 TOPS','64 compute cubes of 512 MACs. Derived, not rounded up.'],
      ['Memory','102.4 GB/s dual-channel LPDDR5','Bandwidth, not TOPS, binds multi-camera fusion.'],
      ['Transformer','Hardware softmax · weight-stationary attention','The operation an FPGA cannot do at frame rate.'],
      ['Safety','Lockstep cores plus a hardware root of trust','The path to an automotive safety rating.'],
      ['Throughput','Eleven sensor channels fused in 8.6 ms','Of a 33.3 ms frame budget — 74% left unused.'],
    ],{headH:34,highlight:5}),
    ...f.cards([[48,1184,'The one number that explains the portfolio',
      'A part that clears eleven channels in a quarter of its frame budget configures downward into a one-channel module, a mirror unit, a radar pod or a forklift kit without redesigning the compute. That headroom is why fifteen SKUs are one tapeout, not fifteen programmes.',CYT,K.cool]]),
  ];})(),
],{notes:'SoC2 specification. Headroom is what permits the SKU fan-out; every configuration below eleven channels is a firmware and front-end change, not a new die.'});}

{const p=N();add([
  ...hdr('The portfolio','Fifteen SKUs across four platform surfaces',
    'Sorted by FY2032 revenue. Same silicon, priced independently by market.',p),
  ...(()=>{
    const ranked=[...SKUS].sort((a,b)=>b.fy32-a.fy32);
    const row=x=>[shortN(x.name),money2(x.asp),cr(x.fy32),x.share.toFixed(1)+'%',x.gm,x.launch];
    const cols=[{t:'SKU',w:200},{t:'Price',w:84,a:'right'},{t:'FY32 rev.',w:96,a:'right'},
      {t:'Share',w:68,a:'right'},{t:'GM',w:56,a:'right'},{t:'First',w:72,a:'right'}];
    const L=flow(178,'mapL',646), R=flow(178,'mapR',646);
    return [...L.tbl(48,576,cols,ranked.slice(0,8).map(row),{headH:32,highlight:0}),
            ...R.tbl(656,576,cols,ranked.slice(8).map(row),{headH:32})];
  })(),
],{notes:'All fifteen SKUs; totals reconcile to ₹1,128.45 Cr.'});}

// ============ PARTS 1-4 · ONE DIVIDER PER SURFACE, FOUR SLIDES PER SKU ============
const PARTNAME=['Part one','Part two','Part three','Part four'];
SURFACES.forEach((surf,si)=>{
  const members=SKUS.filter(x=>x.surface===surf.name);
  { const p=N();
    add(divider(PARTNAME[si],surf.name,
      `${cr(surf.rev)} · ${surf.share}% of FY2032 · ${members.length} SKUs · ${surf.title}`,p),
      {background:K.midnight,notes:`${surf.name}: ${members.map(m=>m.name).join(', ')}.`}); }

  for(const x of members){
    const e=EXPLAIN[x.name];

    // A · WHAT IT IS
    { const p=N();
      add([
        ...hdr(shortN(x.name)+' · A','What it is',e.form,p),
        ...KPI2(48,178,286,money2(x.asp),'Unit price',CYT),
        ...KPI2(348,178,286,x.segment,'Segment',TLT),
        ...KPI2(648,178,286,x.domain,'Operating domain',GR),
        ...KPI2(948,178,284,x.launch,'First revenue',PBT),
        tx('WHAT IS IN IT',48,326,400,16,{size:T.kicker,bold:true,color:CYT}),
        ...e.contents.map((c,i)=>{
          const cw=(1184-3*14)/4, cx=48+i*(cw+14);
          return [roundRect(cx,346,cw,126,K.white,K.line,1),rect(cx,346,cw,4,scol(x.surface)),
            tx(String(i+1).padStart(2,'0'),cx+16,360,cw-32,18,{size:PX(9),bold:true,color:GY}),
            tx(c,cx+16,382,cw-32,TH(c,cw-32,T.body),{size:T.body,color:SL})];}).flat(),
        ...(()=>{const f=flow(492,'A-'+x.name,646);return [
          ...f.cards([[48,1184,'How it is positioned',
            `${x.name} sells at ${money2(x.asp)} into the ${surf.name.toLowerCase()} surface. `+e.fit,scol(x.surface),K.cool]]),
        ];})(),
      ],{notes:`${x.name} — what it is. Price ${money2(x.asp)}, segment ${x.segment}, domain ${x.domain}, first revenue ${x.launch}.`});}

    // B · HOW IT WORKS
    { const p=N();
      const cw=(1184-3*14)/4;
      const h=Math.max(...e.chain.map(t=>stepH(cw,t)));
      add([
        ...hdr(shortN(x.name)+' · B','How it works',
          'Sense, compute on SoC2, decide, act — the same four stages in every product.',p),
        tx('SIGNAL CHAIN',48,182,400,16,{size:T.kicker,bold:true,color:CYT}),
        ...e.chain.map((t,i)=>step(48+i*(cw+14),206,cw,i+1,t,[CYT,TLT,PBT,GR][i])).flat(),
        ...e.chain.map((_,i)=> i<3 ? [sh('rightArrow',48+i*(cw+14)+cw+1,206+h/2-9,12,18,scol(x.surface),scol(x.surface),1)] : []).flat(),
        ...(()=>{const f=flow(206+h+22,'B-'+x.name,646);return [
          ...f.cards([
            [48,592,'What the silicon does here', e.proof ||
             `The SoC2 stage is common to every SKU: it is the same perception compute under different firmware. For ${shortN(x.name)} it runs stage two of the chain above.`,CYT],
            [656,576,'What this product depends on',e.depends,TLT],
          ]),
        ];})(),
      ],{notes:`${x.name} — signal chain: ${e.chain.join(' -> ')}. Depends on: ${e.depends}`});}

    // C · WHO BUYS IT, AND WHY NOW
    { const p=N();
      add([
        ...hdr(shortN(x.name)+' · C','Who buys it, and why now',e.trigger,p),
        ...(()=>{const f=flow(178,'C-'+x.name,646);return [
          ...f.cards([
            [48,592,'The buyer',e.buyer,CYT],
            [656,576,'The channel',e.channel,TLT],
          ]),
          ...f.cards([[48,1184,
            x.pool ? `Demand pool · ${x.capture} capture at FY2032` : 'Demand pool · none separately sized',
            x.pool ? `${x.pool}. Our FY2032 volume of ${x.units[5].toLocaleString('en-IN')} units is ${x.capture} of that pool.`
                   : 'No separately sized demand pool is modelled for this line. Treat its revenue as optionality rather than base case.',
            x.pool?PBT:GY,K.cool]]),
          ...f.note('Source: '+(x.source||'no sized pool in the demand schedule')+'. Capture rates are management assumptions; pool sizes are third-party published estimates.'),
        ];})(),
      ],{notes:`${x.name} — buyer: ${e.buyer} Channel: ${e.channel} Trigger: ${e.trigger} Pool: ${x.pool||'none sized'} (${x.capture}). Source: ${x.source||'n/a'}.`});}

    // D · HOW IT FITS
    { const p=N();
      add([
        ...hdr(shortN(x.name)+' · D','How it fits the overall picture',
          `${cr(x.fy32)} at FY2032 — ${x.share.toFixed(1)}% of group revenue, at ${x.gm} gross margin.`,p),
        ...KPI2(48,178,286,x.units[5].toLocaleString('en-IN'),'FY2032 units',CYT),
        ...KPI2(348,178,286,cr(x.fy32),'FY2032 revenue',TLT),
        ...KPI2(648,178,286,x.share.toFixed(1)+'%','Share of group',GR),
        ...KPI2(948,178,284,x.gm,'Gross margin',PBT),
        tx('UNITS SHIPPED',48,326,300,16,{size:T.kicker,bold:true,color:CYT}),
        ...ramp(48,374,540,74,x.units),
        tx('REVENUE, ₹ CR',636,326,300,16,{size:T.kicker,bold:true,color:CYT}),
        ...ramp(636,374,596,74,x.rev.map(v=>Math.round(v))),
        ...(()=>{const f=flow(472,'D-'+x.name,646);return [
          ...f.cards([
            [48,592,'Its role in the portfolio',e.fit,scol(x.surface)],
            [656,576,'What it depends on',e.depends,TLT],
          ]),
        ];})(),
      ],{notes:`${x.name} — units ${x.units.join(' / ')}, revenue ${x.rev.join(' / ')} ₹Cr. FY2032 ${cr(x.fy32)} = ${x.share}% at ${x.gm}. Role: ${e.fit}`});}

    // E · PROVEN IN A WORKING SIMULATOR (only where a demonstrator exists)
    if(e.demo){ const p=N(); const d=e.demo;
      add([
        ...hdr(shortN(x.name)+' · E','Proven in a working simulator',d.sub,p),
        roundRect(48,178,1184,62,K.cool,scol(x.surface),1),
        rect(48,178,5,62,scol(x.surface)),
        tx('LIVE DEMONSTRATOR',72,192,400,16,{size:T.kicker,bold:true,color:CYT}),
        tx(d.name,72,212,900,24,{size:PX(15),bold:true,face:SERIF,color:K.midnight}),
        ...(()=>{const f=flow(262,'E-'+x.name,640);return [
          ...f.cards([[48,592,d.pts[0][0],d.pts[0][1],CYT],[656,576,d.pts[1][0],d.pts[1][1],TLT]]),
          ...f.cards([[48,592,d.pts[2][0],d.pts[2][1],PBT],[656,576,d.pts[3][0],d.pts[3][1],GR]]),
        ];})(),
        tx('The demonstrator runs the production perception stack against a simulated environment. It is evidence of the decision layer, not of a fielded deployment.',
           48,652,1184,20,{size:T.foot,italic:true,color:GY}),
      ],{notes:`${x.name} — demonstrator ${d.name}. ${d.pts.map(q=>q[0]+': '+q[1]).join(' ')}`});}

    // F · THE SIMULATOR ITSELF, EMBEDDED AND PLAYABLE
    // The dark plate below is the video's seat: attach_media.py drops the clip
    // at exactly these coordinates, so the frame is authored here and the media
    // is placed against it rather than floated somewhere plausible.
    if(e.demo && e.demo.video){ const p=N(); const d=e.demo;
      const VX=48, VY=168, VW=800, VH=450;
      const RX=864, RW=368;
      SEATS.push({slide:p,x:VX,y:VY,w:VW,h:VH,video:d.video,frame:{x:VX-4,y:VY-4,w:VW+8,h:VH+8}});
      add([
        ...hdr(shortN(x.name)+' · F','The simulator, running',d.cap,p),
        roundRect(VX-4,VY-4,VW+8,VH+8,K.midnight,scol(x.surface),1),
        ...(()=>{
          // Measured, not fixed: a rail card sized to a guessed height clips its
          // last line silently, and the frame beside it hides the symptom.
          const bw=RW-40;
          const hs=d.watch.map(w=>32+TH(w[1],bw,T.body)+10);
          const gap=6, tot=hs.reduce((a,b)=>a+b,0)+gap*3, top=VY;
          if(top+tot>646) VIOLATIONS.push(`F-${x.name}: rail ${Math.round(top+tot)} > 646`);
          let yy=top;
          return d.watch.map((w,i)=>{
            const h=hs[i], y0=yy; yy+=h+gap;
            return [roundRect(RX,y0,RW,h,K.cool,K.line,1),rect(RX,y0,4,h,[CYT,TLT,PBT,GR][i]),
              tx(w[0],RX+20,y0+9,bw,22,{size:T.cardH,bold:true,color:K.midnight}),
              tx(w[1],RX+20,y0+33,bw,TH(w[1],bw,T.body)+8,{size:T.body,color:SL})];}).flat();
        })(),
        tx('Recorded from the simulator itself; the clip plays in the deck. Simulation, not a fielded deployment.',
           48,652,1184,20,{size:T.foot,italic:true,color:GY}),
      ],{notes:`${x.name} — embedded clip of ${d.name}. ${d.watch.map(w=>w[0]+': '+w[1]).join(' ')}`});}

    // ANIMATION SLIDE — a product-line animation that exists in the source
    // material. Same seat contract as F, so attach_media fills it and
    // plan_motion excludes it.
    if(e.anim){ const p=N(); const a=e.anim;
      const VX=48, VY=168, VW=800, VH=450;
      const RX=864, RW=368;
      SEATS.push({slide:p,x:VX,y:VY,w:VW,h:VH,video:a.video,frame:{x:VX-4,y:VY-4,w:VW+8,h:VH+8}});
      add([
        ...hdr(shortN(x.name)+' · '+a.letter, a.title, a.cap, p),
        roundRect(VX-4,VY-4,VW+8,VH+8,K.midnight,scol(x.surface),1),
        ...(()=>{
          const bw=RW-40;
          const hs=a.watch.map(w=>32+TH(w[1],bw,T.body)+10);
          const gap=6, tot=hs.reduce((q,r)=>q+r,0)+gap*3, top=VY;
          if(top+tot>646) VIOLATIONS.push(`ANIM-${x.name}: rail ${Math.round(top+tot)} > 646`);
          let yy=top;
          return a.watch.map((w,i)=>{
            const h=hs[i], y0=yy; yy+=h+gap;
            return [roundRect(RX,y0,RW,h,K.cool,K.line,1),rect(RX,y0,4,h,[CYT,TLT,PBT,GR][i]),
              tx(w[0],RX+20,y0+9,bw,22,{size:T.cardH,bold:true,color:K.midnight}),
              tx(w[1],RX+20,y0+33,bw,TH(w[1],bw,T.body)+8,{size:T.body,color:SL})];}).flat();
        })(),
        tx('Recorded from the source animation; the clip plays in the deck. Illustrative of the architecture, not a measurement.',
           48,652,1184,20,{size:T.foot,italic:true,color:GY}),
      ],{notes:`${x.name} — ${a.title}. ${a.watch.map(w=>w[0]+': '+w[1]).join(' ')}`});}
  }
});

// ============================== PART 5 · PORTFOLIO ECONOMICS ================
{const p=N();add(divider('Part five','Portfolio economics',
  'Concentration, sequencing, operating domains, the margin ladder and demand headroom',p),
  {background:K.midnight,notes:'Economics section.'});}

{const p=N();add([
  ...hdr('Concentration','Two SKUs carry 64%, thirteen carry the rest',
    'FY2032 revenue by SKU. Colour shows platform surface.',p),
  ...barsNative(48,180,1184,[...SKUS].sort((a,b)=>b.fy32-a.fy32)
    .map(x=>[shortN(x.name),x.fy32,scol(x.surface),cr(x.fy32)]),{rowH:26,labelW:330,valW:120,max:460}),
  ...(()=>{const f=flow(586,'conc',646);return [
    ...f.note('AD2 and AD0 are the same product family sold to overlapping buyers, so a certification or installation delay hits ₹720 Cr at once — larger than the other thirteen SKUs combined.'),
  ];})(),
],{notes:'Revenue Build FY2032 column.'});}

{const p=N();
 const byYear=FYS.map(y=>[y,SKUS.filter(s=>s.launch==='FY20'+y.slice(2)).map(s=>shortN(s.name))]);
 add([
  ...hdr('Sequencing','Six SKUs earn in FY2027, nine more in FY2028',
    'First revenue year per SKU. FY2027 is FPGA-based product only.',p),
  ...(()=>{const f=flow(178,'seq');return [
    ...f.tbl(48,1184,[{t:'First revenue',w:180},{t:'SKUs',w:110,a:'right'},{t:'What switches on',w:894}],
      byYear.filter(r=>r[1].length).map(r=>[r[0].replace('FY','FY20'),String(r[1].length),r[1].join(' · ')]),
      {headH:34,highlight:0}),
    ...f.cards([[48,1184,'Why the shape matters',
      'FY2027 revenue is FPGA-based product and robot sales only — ₹1.7 Cr across six SKUs. Nine more begin earning in FY2028 as ASIC-era product reaches market, and the licence line starts in FY2029. The ramp is gated by silicon, which is what the round funds.',CY,K.cool]]),
  ];})(),
],{notes:'Launch year = first non-zero revenue year per SKU.'});}

{const p=N();add([
  ...hdr('Where autonomy runs','Outdoor carries it; indoor ships L4 sooner',
    'The same chip across three operating domains, with different regulatory exposure.',p),
  ...KPI2(48,178,286,'86.3%','Outdoor autonomy',CYT),
  ...KPI2(348,178,286,'8.0%','General compute',TLT),
  ...KPI2(648,178,286,'5.7%','Indoor autonomy',GR),
  ...KPI2(948,178,284,'15','SKUs in total',PBT),
  ...(()=>{const f=flow(306,'domain',646);return [
    ...f.tbl(48,1184,[{t:'Domain',w:260},{t:'SKUs',w:110,a:'right'},{t:'FY2032 revenue',w:200,a:'right'},
      {t:'Share',w:140,a:'right'},{t:'What it covers',w:474}],
      DOMAINS.map(d=>[d[0],String(d[3]),cr(d[1]),d[2].toFixed(1)+'%',d[4]]),{headH:34,highlight:0}),
    ...f.cards([[48,1184,'The regulatory asymmetry',
      'Outdoor revenue depends on homologation and public-road rules. Indoor is geofenced, so level-4 ships years earlier on the same chip. Compute carries no vehicle exposure at all.',CYT,K.cool]]),
  ];})(),
],{notes:'Revenue Build section C.'});}

{const p=N();
 const segs=['Systems','Semiconductors','Robotics','Sensors'];
 const rows=segs.map(s=>{const m=SKUS.filter(x=>x.segment===s);const t=m.reduce((a,x)=>a+x.fy32,0);
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
],{notes:'Segment totals computed from the fifteen SKUs.'});}

{const p=N();
 const seen=new Set();
 const sized=SKUS.filter(x=>{ if(x.capture==='—') return false;
   if(seen.has(x.pool)) return false; seen.add(x.pool); return true;});
 add([
  ...hdr('Headroom','No SKU assumes we win its market',
    'FY2032 share of each SKU\'s own sized demand pool. Axis runs to 2%.',p),
  ...barsNative(48,190,1184,sized.map(x=>[x.name.startsWith('A100')?'A100 compute box (3 SKUs)':shortN(x.name),
    parseFloat(x.capture),parseFloat(x.capture)>1?CY:PB,x.capture]),{rowH:34,labelW:330,valW:110,max:2.0}),
  ...(()=>{const f=flow(468,'head',640);return [
    ...f.cards([
      [48,592,'Why the shares look small',
       'Most pools are global while our serviceable market is the India slice, so the real share is higher. The three A100 SKUs share one pool row; T100 has none.',CYT],
      [656,576,'The one to read differently',
       'Seaport AGV shows 0.02% against a pool that is total port automation, cranes and software included. We sell only the vehicle layer.',TLT]]),
  ];})(),
  tx('Capture rates are management assumptions; pool sizes are third-party published estimates.',48,652,1184,20,{size:T.foot,italic:true,color:GY}),
],{notes:'Demand & TAM section B capture column; A100 collapsed to its single pool row.'});}

// ============================== CLOSE ========================================
{const p=N();add([
  rect(0,0,1280,720,K.midnight),rect(0,0,1280,5,CY),
  ...Array.from({length:9},(_,i)=>rect(940+i*38,0,1,720,'#14263C')),
  tx('THE ASK',80,96,700,24,{size:T.kicker,bold:true,color:CY}),
  tx('Fund the silicon; the portfolio follows',80,142,1000,60,{size:PX(30),face:SERIF,bold:true,color:K.white}),
  tx('Fifteen SKUs, one tapeout. Release capital against silicon, certification and paying customers — not against the forecast.',
     80,214,1040,48,{size:PX(14),color:'#A9BACD'}),
  rect(80,282,140,3,CY),
  ...[['Legislated demand','A million trucks a year in scope'],
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
],{background:K.midnight,notes:'Close.'});}

for(const [c,o] of S) addSlide(c,o);
console.log('DARK_SLIDES='+S.map((e,i)=>e[1].background?i+1:0).filter(Boolean).join(','));
if(VIOLATIONS.length){console.log('LAYOUT VIOLATIONS:',VIOLATIONS.length);VIOLATIONS.slice(0,14).forEach(v=>console.log('  '+v));}
else console.log('layout guard: clean');
writeFileSync(OUT.replace(/\.pptx$/,'')+'-video-seats.json',JSON.stringify({seats:SEATS},null,1));
console.log('video seats:',SEATS.map(s=>s.slide+':'+s.video).join(' '));
await (await PresentationFile.exportPptx(P)).save(OUT);
console.log(`OK slides=${S.length} -> ${OUT}`);
