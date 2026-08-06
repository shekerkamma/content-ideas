#!/usr/bin/env python3
"""Build the evidence-led semiconductor investor dossier."""
import sys
from pathlib import Path
from pptx import Presentation

ROOT = Path('/home/sheke/content-ideas')
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'skills/branded-pptx-deck/scripts'))
from pptxkit import Brand, Deck, Inches, Pt, PP_ALIGN  # noqa: E402

b = Brand()
d = Deck(brand=b, footer='AI semiconductor startups · investor diligence')
d.prs = Presentation(str(ROOT / 'skills/branded-pptx-deck/resources/template.pptx'))
d._wipe(); d.W = Inches(13.333); d.H = Inches(7.5)
d.prs.slide_width = d.W; d.prs.slide_height = d.H
d.M = Inches(.58); d.CW = d.W - d.M * 2
OUT = RUN / 'semiconductor-startups-2026-investor-dossier-draft.pptx'
N = 30

def foot(s, i, dark=False, src=''):
    if src:
        d.text(s, src, d.M, Inches(6.73), Inches(9.7), Inches(.22), size=7.5,
               color=b.LIGHT_TEAL if dark else b.MUTED, shrink=True)
    d.footer(s, i, N, dark=dark)

def hdr(s, title, sub=None):
    d.header(s, title, sub)

def label(s, text, x, y, w, color=b.TEAL):
    d.text(s, text, x, y, w, Inches(.25), size=9, color=color, bold=True, shrink=True)

def body(s, text, x, y, w, h, size=15, color=None, bold=False, align=None):
    d.text(s, text, x, y, w, h, size=size, color=color or b.INK, bold=bold,
           align=align, shrink=True)

def card(s, x, y, w, h, title, text, accent=b.TEAL, dark=False):
    fill = b.NAVY_2 if dark else b.SOFT
    d.rect(s, x, y, w, h, fill, line=None if dark else b.GRID, radius=.035)
    d.rect(s, x, y, Inches(.07), h, accent)
    body(s, title, x+Inches(.22), y+Inches(.18), w-Inches(.38), Inches(.32), 12,
         accent, True)
    body(s, text, x+Inches(.22), y+Inches(.65), w-Inches(.4), h-Inches(.82),
         14, b.LIGHT_TEAL if dark else b.INK, False)

def profile(i, name, role, competitors, win, proof, gap, breaks, src):
    s=d.slide(fill=b.WHITE); hdr(s, f'{name}: {role}', f'Real competitors · {competitors}')
    card(s,d.M,Inches(1.52),Inches(5.95),Inches(1.72),'WHY IT CAN WIN',win,b.TEAL)
    card(s,Inches(6.82),Inches(1.52),Inches(5.92),Inches(1.72),'WHAT IS PROVEN',proof,b.ACCENT)
    card(s,d.M,Inches(3.52),Inches(5.95),Inches(1.72),'WHAT IS MISSING',gap,b.GOLD)
    card(s,Inches(6.82),Inches(3.52),Inches(5.92),Inches(1.72),'DISCONFIRMING SIGNAL',breaks,b.CORAL)
    d.rect(s,d.M,Inches(5.58),d.CW,Inches(.65),b.NAVY)
    body(s,'INVESTOR READ',d.M+Inches(.22),Inches(5.78),Inches(1.5),Inches(.22),10,b.TEAL,True)
    body(s,role,Inches(2.05),Inches(5.72),Inches(10.1),Inches(.35),15,b.WHITE,True)
    foot(s,i,False,src)

# 1 — cover
s=d.slide(fill=b.NAVY); d.rect(s,0,0,Inches(.16),d.H,b.GOLD)
body(s,'AI SEMICONDUCTOR STARTUPS · INVESTOR DOSSIER',d.M,Inches(.72),Inches(8.8),Inches(.35),13,b.TEAL,True)
body(s,'The cohort is not ten NVIDIA challengers',d.M,Inches(1.45),Inches(11.2),Inches(1.25),38,b.WHITE,True)
body(s,'It is five competitive games with radically different proof burdens, attachment breadth, and failure modes.',d.M,Inches(3.1),Inches(10.8),Inches(1.05),22,b.LIGHT_TEAL,True)
d.rect(s,d.M,Inches(4.65),Inches(8.4),Inches(.08),b.GOLD)
body(s,'Decision: where to diligence, where to wait, and what evidence changes the answer.',d.M,Inches(5.0),Inches(10.9),Inches(.7),19,b.WHITE,True)
foot(s,1,True,'CRN cohort · evidence current through 4 Aug 2026')

# 2
s=d.slide(fill=b.WHITE); hdr(s,'Lead with interfaces and shipping systems; option the architecture bets')
items=[('CORE DILIGENCE','Lightmatter · Cornelis · Xsight · Tenstorrent','Broad attachment or multiple monetization paths; demand evidence is imperfect but the economic role survives heterogeneous compute.',b.TEAL),
('EXECUTION DILIGENCE','d-Matrix · Axelera · NextSilicon','Credible product or named validation; value depends on repeatable systems deployment, channel conversion, and software usability.',b.GOLD),
('MILESTONE OPTIONS','Etched · MatX · Fractile','Exceptional upside is inseparable from workload concentration, roadmap timing, and vendor-controlled benchmarks.',b.CORAL)]
for j,(h,n,t,c) in enumerate(items):
    y=Inches(1.68)+j*Inches(1.48); card(s,d.M,y,Inches(12.15),Inches(1.18),h,f'{n}\n{t}',c)
foot(s,2,False,'Investor judgment from evidence ledger; not investment advice')

# 3 storyboard
s=d.slide(fill=b.NAVY); body(s,'The storyboard resolves four investment questions',d.M,Inches(.62),d.CW,Inches(.65),30,b.WHITE,True)
qs=[('01','WHERE DOES VALUE ACCRUE?','Map bottlenecks and real competitive arenas.'),('02','WHAT IS ACTUALLY PROVEN?','Separate product, validation, production, and independent evidence.'),('03','WHO CAN WIN—AND WHY NOT?','Teardown each company against its true alternatives.'),('04','WHAT CHANGES THE DECISION?','Set proof gates, scenarios, kill criteria, and monitoring triggers.')]
for j,(n,h,t) in enumerate(qs):
    x=d.M+(j%2)*Inches(6.15); y=Inches(1.65)+(j//2)*Inches(2.25)
    card(s,x,y,Inches(5.75),Inches(1.8),f'{n}  {h}',t,b.TEAL if j<2 else b.GOLD,True)
foot(s,3,True)

# 4 market structure
s=d.slide(fill=b.WHITE); hdr(s,'Useful deployed throughput—not peak FLOPS—determines economic value')
stages=[('COMPUTE','Model execution','NVIDIA · AMD · hyperscaler ASICs'),('MEMORY','Keep data local','HBM · in-memory compute'),('FABRIC','Keep chips busy','InfiniBand · Ethernet · Omni-Path'),('SYSTEM','Deploy repeatedly','Racks · software · support')]
for j,(h,t,c) in enumerate(stages):
    x=d.M+j*Inches(3.05); d.rect(s,x,Inches(1.65),Inches(2.62),Inches(3.45),b.SOFT,line=b.GRID)
    label(s,h,x+Inches(.2),Inches(1.95),Inches(2.2),b.TEAL if j>1 else b.GOLD)
    body(s,t,x+Inches(.2),Inches(2.5),Inches(2.2),Inches(.65),20,b.NAVY,True,PP_ALIGN.CENTER)
    body(s,c,x+Inches(.2),Inches(3.55),Inches(2.2),Inches(.9),13,b.MUTED,False,PP_ALIGN.CENTER)
    if j<3: body(s,'→',x+Inches(2.7),Inches(2.75),Inches(.3),Inches(.4),20,b.MUTED,True,PP_ALIGN.CENTER)
body(s,'Investor implication',d.M,Inches(5.55),Inches(1.6),Inches(.25),10,b.TEAL,True)
body(s,'Interfaces can attach across winners; accelerator value is more sensitive to model, compiler, and incumbent roadmaps.',Inches(2.15),Inches(5.45),Inches(10.0),Inches(.5),17,b.NAVY,True)
foot(s,4,False,'NVIDIA FY2026 10-K; cohort product evidence')

# 5 arena map
s=d.slide(fill=b.WHITE); hdr(s,'The ten companies compete in five arenas—not one leaderboard')
arenas=[('INTERCONNECT','Lightmatter','Ayar Labs · Celestial AI · Broadcom/TSMC'),('FABRIC + DPU','Cornelis · Xsight','NVIDIA · Broadcom · Marvell · HPE Slingshot'),('OPEN / ADAPTIVE','Tenstorrent · NextSilicon','NVIDIA · AMD · Intel · Arm/RISC-V IP'),('INFERENCE SYSTEMS','d-Matrix · Axelera','Groq-class systems · Hailo · SiMa · Positron'),('SPECIALIST FRONTIER','Etched · MatX · Fractile','NVIDIA · TPU/Trainium/Maia · Broadcom ASICs')]
for j,(h,n,c) in enumerate(arenas):
    y=Inches(1.35)+j*Inches(1.03); label(s,h,d.M,y,Inches(1.8),b.TEAL)
    body(s,n,Inches(2.25),y-Inches(.05),Inches(2.7),Inches(.35),15,b.NAVY,True)
    body(s,c,Inches(5.1),y-Inches(.05),Inches(7.2),Inches(.45),14,b.INK,False)
    d.rect(s,d.M,y+Inches(.56),d.CW,Pt(1),b.GRID)
foot(s,5)

# 6 competitor universe
s=d.slide(fill=b.NAVY); body(s,'The most dangerous competitors are absent from the CRN cohort',d.M,Inches(.62),d.CW,Inches(.7),29,b.WHITE,True)
groups=[('VERTICALLY INTEGRATED','NVIDIA · Google TPU · AWS Trainium · Microsoft Maia','Bundle silicon, software, network, cloud demand, and financing.'),('AT-SCALE MERCHANT','AMD · Broadcom · Marvell · Qualcomm','Manufacturing leverage, channels, roadmaps, and customer trust.'),('STARTUP SURVIVORS','Cerebras · SambaNova · Rebellions · Furiosa · Positron · Hailo','Provide the closest commercialization and exit comparables.'),('STANDARDS + SYSTEMS','Ultra Ethernet · OIF · HPE Slingshot · Arista','Can commoditize a proprietary advantage or slow adoption.')]
for j,(h,n,t) in enumerate(groups):
    y=Inches(1.55)+j*Inches(1.25); label(s,h,d.M,y,Inches(2.1),b.GOLD if j<2 else b.TEAL)
    body(s,n,Inches(2.75),y-Inches(.05),Inches(4.2),Inches(.45),15,b.WHITE,True)
    body(s,t,Inches(7.15),y-Inches(.05),Inches(5.3),Inches(.55),14,b.LIGHT_TEAL)
foot(s,6,True,'NVIDIA 10-K; OIF; company and industry sources')

# 7 evidence rules
s=d.slide(fill=b.WHITE); hdr(s,'Product, validation, and production are different investment states')
gates=[('0','ROADMAP','Architecture and target disclosed','Question: can it be built?'),('1','SILICON','Working or sampled device','Question: can it yield?'),('2','VALIDATION','Named partner/customer evaluation','Question: does it reproduce?'),('3','PRODUCTION','Repeatable paid deployment','Question: can it scale?')]
for j,(n,h,t,q) in enumerate(gates):
    x=d.M+j*Inches(3.05); y=Inches(1.65)+j*Inches(.35)
    d.rect(s,x,y,Inches(2.65),Inches(3.35),b.SOFT,line=b.GRID)
    body(s,n,x+Inches(.2),y+Inches(.2),Inches(.6),Inches(.6),28,b.TEAL,True)
    body(s,h,x+Inches(.2),y+Inches(1.0),Inches(2.2),Inches(.35),14,b.NAVY,True)
    body(s,t,x+Inches(.2),y+Inches(1.58),Inches(2.15),Inches(.7),14,b.INK)
    body(s,q,x+Inches(.2),y+Inches(2.55),Inches(2.15),Inches(.5),12,b.CORAL,True)
foot(s,7,False,'Evidence-state definitions in metric-definitions.md')

# 8 maturity
s=d.slide(fill=b.WHITE); hdr(s,'Public evidence is concentrated in validation—not repeatable economics')
rows=[('PRODUCTION CLAIM','Tenstorrent · d-Matrix','Shipping language; customer economics remain mostly private',b.TEAL),('NAMED VALIDATION','Cornelis · NextSilicon · Axelera','DOE/partner evidence reduces—but does not eliminate—vendor bias',b.ACCENT),('EARLY ACCESS / SYSTEM TEST','Lightmatter · Xsight · Etched','Working systems or silicon; limited independent production proof',b.GOLD),('ROADMAP-DOMINANT','MatX · Fractile','Capital and architecture precede available product evidence',b.CORAL)]
for j,(h,n,t,c) in enumerate(rows):
    y=Inches(1.5)+j*Inches(1.18); d.rect(s,d.M,y,Inches(2.15),Inches(.83),c)
    body(s,h,d.M+Inches(.12),y+Inches(.24),Inches(1.9),Inches(.28),11,b.WHITE if c==b.CORAL else b.NAVY,True,PP_ALIGN.CENTER)
    body(s,n,Inches(3.0),y+Inches(.08),Inches(3.4),Inches(.35),15,b.NAVY,True)
    body(s,t,Inches(6.45),y+Inches(.05),Inches(5.8),Inches(.58),14,b.INK)
foot(s,8,False,'Company releases; Sandia; industry reporting')

# 9 funding vs proof
s=d.slide(fill=b.NAVY); body(s,'Capital has repriced possibility faster than public proof',d.M,Inches(.62),d.CW,Inches(.65),30,b.WHITE,True)
facts=[('$10.3B','Etched valuation','Working silicon + contracts claimed; production economics undisclosed'),('$4.4B','Lightmatter valuation','Strong technical partners; early-access/customer disclosure gap'),('$693M','Tenstorrent Series D','Broader shipping stack and IP model; revenue remains private'),('$500M','MatX Series B','Large-model processor targets 2027 shipment'),('$220M','Fractile Series B','Upcoming silicon; simulation-heavy proof')]
for j,(v,n,t) in enumerate(facts):
    y=Inches(1.48)+j*Inches(.98); body(s,v,d.M,y,Inches(1.65),Inches(.48),22,b.GOLD if j<2 else b.TEAL,True)
    body(s,n,Inches(2.35),y+Inches(.03),Inches(2.4),Inches(.32),14,b.WHITE,True)
    body(s,t,Inches(4.8),y,Inches(7.5),Inches(.5),13,b.LIGHT_TEAL)
foot(s,9,True,'Company releases; TechCrunch; values are financing signals, not operating proof')

# 10 framework
s=d.slide(fill=b.WHITE); hdr(s,'Compare companies on five questions—without manufacturing false precision')
dims=[('BOTTLENECK','Is buyer pain urgent and budgeted?'),('ATTACHMENT','Can the product monetize multiple winners?'),('COMMERCIAL PROOF','Roadmap, silicon, validation, or production?'),('EVIDENCE INDEPENDENCE','Who reproduced the claim?'),('FAILURE MODE','What single event breaks the thesis?')]
for j,(h,t) in enumerate(dims):
    y=Inches(1.35)+j*Inches(1.02); body(s,f'{j+1:02d}',d.M,y,Inches(.45),Inches(.35),12,b.TEAL,True)
    body(s,h,Inches(1.25),y-Inches(.03),Inches(2.35),Inches(.35),14,b.NAVY,True)
    body(s,t,Inches(3.9),y-Inches(.04),Inches(8.4),Inches(.48),16,b.INK)
    d.rect(s,d.M,y+Inches(.55),d.CW,Pt(1),b.GRID)
foot(s,10)

profile(11,'Lightmatter','Core diligence—broad attachment, but commercialization is the question','Ayar Labs · Celestial AI · Broadcom/TSMC · pluggable optics','3D-stacked photonic I/O addresses package-edge bandwidth and power across accelerator winners.','Rackable validation hardware; Qualcomm, Cadence, ASE and SENKO relationships; 1.6 Tbps/fiber company demonstration.','Named production customers, yield/cost, BER/thermals at volume, serviceability and revenue concentration.','CPO adoption slips; incumbent optics improve; hyperscalers internalize the interface; packaging economics fail.','Lightmatter technical/product releases; OIF')
profile(12,'Cornelis Networks','Core diligence—credible fabric proof in a standards war','NVIDIA InfiniBand · Ultra Ethernet · HPE Slingshot','Omni-Path offers a differentiated lossless fabric and an independent supply path for HPC/AI clusters.','Named DOE deployment and peer-reviewed architectural inheritance; CN5000 product family.','Commercial scale, Ethernet interoperability timing, gross margins, software/tooling and pipeline outside government HPC.','Ultra Ethernet closes the feature gap; NVIDIA bundles network with compute; roadmap slips at 800G/1.6T.','Cornelis; DOE/industry reporting; Journal of Supercomputing')
profile(13,'Xsight Labs','Core diligence—strategic silicon, limited public economic proof','Broadcom · NVIDIA · Marvell · custom hyperscaler networking','Programmable Ethernet switches and 800G DPU can monetize data movement without choosing the winning accelerator.','Concrete X2 and E-series specifications; company-reported Starlink selection.','Independent power/latency benchmarks, named data-center production deployments, revenue mix and software adoption.','Merchant networking incumbents bundle equivalent capabilities or customer concentration turns one design win into fragility.','Xsight product pages; company website')
profile(14,'Tenstorrent','Core diligence—broadest platform surface, highest execution breadth','NVIDIA · AMD · Cerebras · RISC-V/Arm IP · hyperscaler ASICs','Licensable IP, RISC-V CPUs, accelerators, systems and Ethernet create multiple monetization paths and strategic-exit options.','Blackhole systems and tooling ship; third-party Wormhole programming evidence; $693M Series D.','Recognized revenue by line, repeat customers, production workload TCO, developer retention and IP-license economics.','Breadth dilutes focus; software ecosystem never reaches escape velocity; customers prefer incumbent or internal silicon.','Tenstorrent; arXiv:2603.23343')
profile(15,'d-Matrix','Execution diligence—production claim with system-integration upside and risk','NVIDIA inference · Positron · FuriosaAI · Rebellions · SambaNova','Digital in-memory compute targets inference data movement; GigaIO assets extend the thesis toward rack-scale value.','Corsair production claim with TSMC/Alchip and named rack partners; GigaIO acquisition.','Named paid customers, reproducible end-to-end cost/token, availability, software migration effort and gross margin.','Heterogeneous system advantage disappears under fair batching; rack integration consumes capital and delays adoption.','d-Matrix production and acquisition releases')
profile(16,'Axelera AI','Execution diligence—edge focus lowers direct data-center collision','Hailo · SiMa.ai · Kneron · Qualcomm · NVIDIA Jetson','Edge inference has power, privacy and latency constraints where smaller accelerators can beat general-purpose GPUs.','Metis products; Advantech distribution/support relationship; reported business pipeline.','Pipeline conversion, fleet utilization, software/support cost, ASP/margin by vertical and repeat OEM design wins.','Fragmented edge channels lengthen sales cycles; incumbent SoCs bundle adequate AI at lower integration cost.','Axelera and Advantech releases')
profile(17,'NextSilicon','Execution diligence—rare independent HPC validation, software bridge incomplete','NVIDIA/AMD accelerators · Intel · FPGAs · national-lab incumbents','Runtime-reconfigurable dataflow targets scientific codes without wholesale rewrites; RISC-V host roadmap adds stack control.','Sandia Vanguard partnership; support for C/C++/Fortran/OpenMP/Kokkos; company says Maverick-2 is in production.','Commercial customers beyond labs, framework/CUDA/ROCm integration, repeat procurement, benchmark disclosure and Arbel timing.','Portability promise fails on real applications; market remains too narrow; 2028 CPU roadmap consumes runway.','Sandia; NextSilicon product pages')
profile(18,'Etched','Milestone option—demand signal is extraordinary; concentration risk is structural','NVIDIA · TPU/Trainium/Maia · Broadcom ASICs · specialist inference startups','Full-stack specialization can create step-change inference economics if frontier workloads remain compatible.','Working A0 N4P silicon; over $1B contracts claimed; customer system validation; substantial facilities and financing.','Independent workload/TCO results, contract terms, recognized revenue, yields, supply resilience and model compatibility boundaries.','Model architecture or batching changes compress the advantage; deployment slips; valuation leaves no room for normal execution.','Etched releases; TechCrunch; MLCommons')
profile(19,'MatX','Milestone option—ambitious frontier processor priced ahead of shipment','NVIDIA · Cerebras · Google TPU · custom frontier silicon','Large-model co-design could optimize training, RL, prefill and decode across a narrow but valuable customer set.','Published architecture/specifications and $500M financing indicate talent and investor conviction.','Working production silicon, independent benchmarks, named customers, compiler usability, manufacturing plan and 2027 schedule confidence.','Incumbents ship another generation before launch; target workloads change; software and systems work overwhelms chip advantage.','MatX; TechCrunch')
profile(20,'Fractile','Milestone option—memory thesis is plausible; evidence remains pre-product','d-Matrix · Positron · Taalas · NVIDIA inference','In-memory compute attacks the bandwidth and energy cost that increasingly dominates inference.','$220M Series B and a coherent memory-centric architecture thesis.','Manufactured silicon, benchmark methodology, named customer evaluation, software stack and credible time-to-volume.','Simulation advantage fails on silicon; schedule slips; competing memory-rich systems capture the window first.','Fractile financing release; independent reporting')

# 21 heatmap
s=d.slide(fill=b.WHITE); hdr(s,'The cross-company pattern is breadth versus proof—not a single winner')
cols=['COMPANY','ATTACHMENT','PROOF','INDEPENDENCE','PRIMARY FAILURE MODE']
xs=[.58,3.0,5.15,7.05,9.15]; ws=[2.25,1.9,1.65,1.85,3.58]
for x,w,h in zip(xs,ws,cols): label(s,h,Inches(x),Inches(1.33),Inches(w),b.TEAL)
rows=[('Lightmatter','Broad','Validation','Medium','CPO adoption / packaging'),('Cornelis','Broad','Validation','Medium','Standards + bundling'),('Xsight','Broad','Validation','Low–Med','Customer concentration'),('Tenstorrent','Broad','Production claim','Medium','Software ecosystem'),('d-Matrix','Moderate','Production claim','Low–Med','Rack execution'),('Axelera','Moderate','Validation','Medium','Channel conversion'),('NextSilicon','Moderate','Validation','Medium','Market breadth / timing'),('Etched','Narrow','System test','Low–Med','Model + valuation'),('MatX','Narrow','Roadmap','Low','Schedule + software'),('Fractile','Narrow','Roadmap','Low','Silicon reality')]
for r,row in enumerate(rows):
    y=Inches(1.72)+r*Inches(.45)
    if r%2==0: d.rect(s,d.M,y-Inches(.05),d.CW,Inches(.4),b.SOFT)
    for x,w,t in zip(xs,ws,row): body(s,t,Inches(x),y,Inches(w),Inches(.26),10.5,b.NAVY,True if x==.58 else False)
foot(s,21,False,'Evidence-state comparison; investor interpretation')

# 22 STORM
s=d.slide(fill=b.NAVY); body(s,'Five independent lenses converge on the proof gate—and disagree on timing',d.M,Inches(.58),d.CW,Inches(.78),28,b.WHITE,True)
lenses=[('PRACTITIONER','Named reproducible workload beats peak claims.'),('ACADEMIC','Independent silicon evidence is rare and decisive.'),('SKEPTIC','The cohort is more correlated than company count implies.'),('ECONOMIST','Evidence-adjusted valuation favors toll roads and shipping systems.'),('HISTORIAN','Interfaces retain strategic value; ecosystems defeat isolated chips.')]
for j,(h,t) in enumerate(lenses):
    y=Inches(1.5)+j*Inches(.92); label(s,h,d.M,y,Inches(1.75),b.GOLD if j in (2,3) else b.TEAL)
    body(s,t,Inches(2.55),y-Inches(.04),Inches(9.7),Inches(.4),16,b.WHITE,True)
body(s,'UNRESOLVED',d.M,Inches(6.15),Inches(1.35),Inches(.25),10,b.CORAL,True)
body(s,'How much credit should investors give shipping claims before workload economics and paid deployments are public?',Inches(2.05),Inches(6.05),Inches(10.2),Inches(.45),15,b.LIGHT_TEAL,True)
foot(s,22,True,'Author-constructed STORM panel; convergence is a hypothesis, not field consensus')

# 23 bull
s=d.slide(fill=b.WHITE); hdr(s,'Bull case: fragmentation creates more attach points than winners')
bulls=[('BOTTLENECKS MULTIPLY','Power, memory, fabric and packaging become independent budget lines.'),('CUSTOM SILICON NORMALIZES','Hyperscaler demand validates specialized architectures and acquisition paths.'),('INFERENCE EXPANDS','Serving economics create room for workload-specific hardware.'),('STANDARDS LOWER FRICTION','Ethernet, UCIe and RISC-V widen routes to distribution.'),('STRATEGIC M&A PERSISTS','Incumbents buy talent, IP, fabric and system capabilities before standalone scale.')]
for j,(h,t) in enumerate(bulls):
    y=Inches(1.38)+j*Inches(1.0); body(s,f'{j+1:02d}',d.M,y,Inches(.5),Inches(.3),11,b.TEAL,True)
    body(s,h,Inches(1.25),y-Inches(.03),Inches(2.7),Inches(.35),14,b.NAVY,True)
    body(s,t,Inches(4.1),y-Inches(.04),Inches(8.1),Inches(.48),15,b.INK)
foot(s,23,False,'OIF; AMD SeaMicro acquisition; cohort evidence')

# 24 bear
s=d.slide(fill=b.NAVY); body(s,'Bear case: ten names conceal six shared failure modes',d.M,Inches(.62),d.CW,Inches(.65),30,b.WHITE,True)
bears=[('INCUMBENT BUNDLING','NVIDIA grew compute and networking together.'),('SOFTWARE LOCK-IN','CUDA compounds across two decades of tools and habits.'),('SUPPLY CONCENTRATION','Foundry, HBM and packaging dependencies correlate outcomes.'),('CUSTOMER CONCENTRATION','One design win can validate technology and destroy pricing power.'),('ROADMAP DILUTION','Every slip burns runway while incumbents ship again.'),('MODEL DRIFT','Specialization can expire before volume deployment.')]
for j,(h,t) in enumerate(bears):
    x=d.M+(j%2)*Inches(6.1); y=Inches(1.55)+(j//2)*Inches(1.55)
    card(s,x,y,Inches(5.75),Inches(1.15),h,t,b.CORAL,True)
foot(s,24,True,'NVIDIA 10-K; CUDA docs; Cirrus Logic 10-K; AP')

# 25 valuation debate
s=d.slide(fill=b.WHITE); hdr(s,'Valuation should buy down uncertainty—not merely finance it')
vals=[('ETCHED','$10.3B','Contracts + silicon','Production economics, concentration, model durability'),('LIGHTMATTER','$4.4B','Technical ecosystem + optical scarcity','Customer/revenue visibility, packaging economics'),('TENSTORRENT','$2.0B pre-money','Shipping stack + IP optionality','Revenue mix, ecosystem conversion'),('MATX','$500M round','Talent + architecture','2027 silicon, customers, software'),('FRACTILE','$220M round','Memory thesis','First silicon and workload proof')]
for j,(n,v,p,g) in enumerate(vals):
    y=Inches(1.42)+j*Inches(1.0); body(s,n,d.M,y,Inches(1.55),Inches(.3),12,b.NAVY,True)
    body(s,v,Inches(2.0),y-Inches(.04),Inches(1.65),Inches(.38),17,b.TEAL if j>1 else b.GOLD,True)
    body(s,p,Inches(3.85),y-Inches(.03),Inches(3.0),Inches(.42),13,b.INK,True)
    body(s,g,Inches(7.0),y-Inches(.04),Inches(5.2),Inches(.48),13,b.CORAL,False)
    d.rect(s,d.M,y+Inches(.55),d.CW,Pt(1),b.GRID)
foot(s,25,False,'Financing values are not operating-value conclusions')

# 26 portfolio roles
s=d.slide(fill=b.WHITE); hdr(s,'Construct the portfolio by role, evidence burden, and reserve policy')
roles=[('FOUNDATIONAL INTERFACES','Lightmatter · Cornelis · Xsight','Diligence now','Reserve for customer/volume proof','Do not pay platform value without attach-rate evidence',b.TEAL),('PLATFORM + SYSTEMS','Tenstorrent · d-Matrix · Axelera · NextSilicon','Diligence selectively','Reserve against deployment milestones','Segment by software, customer and manufacturing proof',b.GOLD),('SPECIALIST OPTIONS','Etched · MatX · Fractile','Observe or price as options','Fund only against explicit gates','Assume correlated model and supply risk',b.CORAL)]
for j,(h,n,a,r,k,c) in enumerate(roles):
    y=Inches(1.42)+j*Inches(1.6); d.rect(s,d.M,y,Inches(2.15),Inches(1.27),c)
    body(s,h,d.M+Inches(.15),y+Inches(.25),Inches(1.85),Inches(.6),13,b.WHITE if c==b.CORAL else b.NAVY,True,PP_ALIGN.CENTER)
    body(s,n,Inches(3.0),y+Inches(.08),Inches(2.8),Inches(.4),14,b.NAVY,True)
    body(s,a,Inches(6.0),y+Inches(.08),Inches(1.55),Inches(.38),13,c,True)
    body(s,r,Inches(7.75),y+Inches(.08),Inches(2.05),Inches(.5),12,b.INK)
    body(s,k,Inches(10.0),y+Inches(.08),Inches(2.25),Inches(.7),12,b.MUTED)
foot(s,26,False,'Role framework; position sizing requires price, ownership and fund constraints')

# 27 diligence plan
s=d.slide(fill=b.NAVY); body(s,'The next diligence round should ask for evidence vendors cannot market around',d.M,Inches(.58),d.CW,Inches(.78),28,b.WHITE,True)
asks=[('WORKLOAD','Named model/application, precision, batch, context, compiler and baseline.'),('SYSTEM TCO','Power at wall, utilization, networking, memory, labor and support.'),('REPEATABILITY','90-day stability, second deployment and upgrade path.'),('COMMERCIAL','Paid status, contract terms, revenue recognition, renewals and concentration.'),('SUPPLY','Yield, packaging, HBM, second source, lead time and warranty exposure.'),('SOFTWARE','Migration effort, developer retention, release cadence and customer-owned code.')]
for j,(h,t) in enumerate(asks):
    x=d.M+(j%2)*Inches(6.1); y=Inches(1.55)+(j//2)*Inches(1.55); card(s,x,y,Inches(5.75),Inches(1.15),h,t,b.TEAL if j<2 else b.GOLD,True)
foot(s,27,True)

# 28 scenarios
s=d.slide(fill=b.WHITE); hdr(s,'Three scenarios produce different winners—and different follow-on rules')
sc=[('A · HETEROGENEOUS BOOM','Multiple accelerator architectures survive','Interfaces and open systems compound','Prioritize Lightmatter, fabric/DPU, Tenstorrent',b.TEAL),('B · INCUMBENT REBUNDLING','NVIDIA/hyperscalers absorb bottlenecks','Narrow merchant platforms compress','Favor strategic IP, standards and acquisition optionality',b.GOLD),('C · MODEL DISCONTINUITY','Workloads change faster than tape-outs','Fixed-function value decays','Favor adaptable compute; gate Etched/MatX/Fractile',b.CORAL)]
for j,(h,t,w,a,c) in enumerate(sc):
    y=Inches(1.45)+j*Inches(1.58); card(s,d.M,y,Inches(12.15),Inches(1.25),h,f'{t}  |  {w}  |  {a}',c)
foot(s,28)

# 29 kill triggers
s=d.slide(fill=b.WHITE); hdr(s,'Kill criteria turn narrative risk into observable triggers')
ks=[('BENCHMARK','Cannot reproduce under comparable workload conditions'),('SOFTWARE','Migration cost erases silicon advantage'),('SUPPLY','Yield, HBM or packaging blocks repeat delivery'),('CUSTOMER','Evaluation does not convert to paid production'),('TIMING','Roadmap misses the buyer deployment window'),('CONCENTRATION','One customer or supplier dominates economics'),('DRIFT','Model architecture invalidates specialization'),('VALUATION','Price assumes platform scale before evidence')]
for j,(h,t) in enumerate(ks):
    x=d.M+(j%2)*Inches(6.1); y=Inches(1.38)+(j//2)*Inches(1.22)
    body(s,f'{j+1:02d}',x,y,Inches(.45),Inches(.3),10,b.CORAL,True)
    body(s,h,x+Inches(.6),y-Inches(.03),Inches(1.45),Inches(.35),13,b.NAVY,True)
    body(s,t,x+Inches(2.15),y-Inches(.03),Inches(3.45),Inches(.5),13,b.INK)
    d.rect(s,x,y+Inches(.65),Inches(5.65),Pt(1),b.GRID)
foot(s,29)

# 30 close
s=d.slide(fill=b.NAVY); d.rect(s,0,0,Inches(.16),d.H,b.TEAL)
body(s,'Back interfaces that survive fragmentation.',d.M,Inches(1.0),Inches(11.0),Inches(.9),35,b.WHITE,True)
body(s,'Demand customer economics from systems.',d.M,Inches(2.25),Inches(11.0),Inches(.9),35,b.LIGHT_TEAL,True)
body(s,'Price specialist silicon as a milestone option.',d.M,Inches(3.5),Inches(11.0),Inches(.9),35,b.GOLD,True)
d.rect(s,d.M,Inches(5.15),d.CW,Inches(.06),b.TEAL)
body(s,'NEXT MOVE',d.M,Inches(5.55),Inches(1.4),Inches(.25),10,b.TEAL,True)
body(s,'Run six evidence requests against the seven diligence candidates; re-rank only after workload, commercial, and supply proof arrives.',Inches(2.1),Inches(5.43),Inches(10.1),Inches(.68),17,b.WHITE,True)
foot(s,30,True,'Evidence-led investor dossier · August 2026')

d.save(OUT)
print(OUT)
