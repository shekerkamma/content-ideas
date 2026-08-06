#!/usr/bin/env python3
"""Build the investor-oriented semiconductor startup deck."""
import sys
from pathlib import Path
from pptx import Presentation

ROOT = Path('/home/sheke/content-ideas')
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'skills/branded-pptx-deck/scripts'))
from pptxkit import Brand, Deck, Inches, Pt, PP_ALIGN  # noqa: E402

b = Brand()
d = Deck(brand=b, footer='AI semiconductor startups · investor lens')
d.prs = Presentation(str(ROOT / 'skills/branded-pptx-deck/resources/template.pptx'))
d._wipe(); d.W = Inches(13.333); d.H = Inches(7.5)
d.prs.slide_width = d.W; d.prs.slide_height = d.H
d.M = Inches(.6); d.CW = d.W - d.M * 2
OUT = RUN / 'semiconductor-startups-2026-investor-deck-draft.pptx'
N = 12

scores = [
    ('Lightmatter',41,'Core'),('Tenstorrent',41,'Core'),('Xsight Labs',41,'Core'),
    ('Cornelis',39,'Core'),('d-Matrix',38,'Growth'),('Axelera AI',35,'Growth'),
    ('NextSilicon',35,'Option'),('Etched',31,'Moonshot'),('MatX',28,'Moonshot'),('Fractile',28,'Moonshot')]

def footer(s, i, dark=False): d.footer(s, i, N, dark=dark)
def header(s, text, sub=None): d.header(s, text, sub)
def pill(s, text, x, y, w, fill, color=None):
    d.rect(s,x,y,w,Inches(.38),fill,radius=.5)
    d.text(s,text,x,y+Inches(.07),w,Inches(.22),size=10,color=color or b.WHITE,bold=True,align=PP_ALIGN.CENTER)
def note(s, text, y=6.25, dark=False):
    d.text(s,text,d.M,Inches(y),d.CW,Inches(.34),size=10,color=b.LIGHT_TEAL if dark else b.MUTED,italic=True,shrink=True)

# 1
s=d.slide(fill=b.NAVY); d.rect(s,0,0,Inches(.16),d.H,b.GOLD)
d.text(s,'The picks-and-shovels portfolio\nbeats the accelerator lottery',d.M,Inches(1.15),Inches(10.7),Inches(2.0),size=43,color=b.WHITE,bold=True,shrink=True)
d.text(s,'Ten semiconductor startups · one investable hierarchy',d.M,Inches(3.65),Inches(8),Inches(.5),size=19,color=b.TEAL,bold=True)
d.rect(s,d.M,Inches(4.45),Inches(7.7),Inches(.08),b.GOLD)
d.text(s,'Anchor in horizontal infrastructure. Buy specialist compute as options, not certainty.',d.M,Inches(4.82),Inches(10.4),Inches(.9),size=22,color=b.LIGHT_TEAL,bold=True,shrink=True)
footer(s,1,True)

# 2
s=d.slide(fill=b.WHITE); header(s,'The investable asymmetry sits between bottleneck urgency and proof')
d.text(s,'HIGH URGENCY',d.M,Inches(1.62),Inches(1.3),Inches(.3),size=10,color=b.TEAL,bold=True)
d.text(s,'LOW PROOF',Inches(11.2),Inches(5.87),Inches(1.2),Inches(.3),size=10,color=b.CORAL,bold=True,align=PP_ALIGN.RIGHT)
d.rect(s,Inches(1.25),Inches(2.05),Inches(10.8),Inches(3.45),b.SOFT,line=b.GRID)
d.rect(s,Inches(1.25),Inches(2.05),Inches(5.4),Inches(1.72),b.LIGHT_TEAL)
d.rect(s,Inches(6.65),Inches(3.77),Inches(5.4),Inches(1.73),b.SOFT)
quads=[('CORE COMPOUNDERS','Lightmatter · Xsight · Cornelis · Tenstorrent',1.55,2.35,b.NAVY),('EXECUTION BETS','d-Matrix · Axelera',6.95,2.35,b.NAVY),('WATCHLIST','NextSilicon',1.55,4.1,b.NAVY),('MOONSHOTS','Etched · MatX · Fractile',6.95,4.1,b.CORAL)]
for h,body,x,y,c in quads:
    d.text(s,h,Inches(x),Inches(y),Inches(4.6),Inches(.35),size=12,color=c,bold=True)
    d.text(s,body,Inches(x),Inches(y+.48),Inches(4.6),Inches(.5),size=17,color=b.NAVY,bold=True,shrink=True)
note(s,'Placement is analyst judgment from the verified research bundle—not an investment recommendation.')
footer(s,2)

# 3
s=d.slide(fill=b.NAVY)
d.text(s,'The market rewards whoever keeps expensive compute busy',d.M,Inches(.62),d.CW,Inches(1.0),size=31,color=b.WHITE,bold=True,shrink=True)
stages=[('COMPUTE','Accelerators',b.CORAL),('MEMORY','Movement',b.GOLD),('FABRIC','Utilization',b.TEAL),('SYSTEM','Deployment',b.ACCENT)]
for i,(h,sub,c) in enumerate(stages):
    x=d.M+i*Inches(3.03)
    d.rect(s,x,Inches(2.05),Inches(2.45),Inches(2.15),b.NAVY_2,radius=.05)
    d.rect(s,x,Inches(2.05),Inches(2.45),Inches(.12),c)
    d.text(s,h,x+Inches(.2),Inches(2.5),Inches(2.05),Inches(.4),size=14,color=c,bold=True,align=PP_ALIGN.CENTER)
    d.text(s,sub,x+Inches(.2),Inches(3.13),Inches(2.05),Inches(.45),size=20,color=b.WHITE,bold=True,align=PP_ALIGN.CENTER)
    if i<3:d.text(s,'→',x+Inches(2.55),Inches(2.8),Inches(.4),Inches(.5),size=22,color=b.MUTED,bold=True,align=PP_ALIGN.CENTER)
d.text(s,'Investor implication',d.M,Inches(4.82),Inches(2),Inches(.35),size=12,color=b.TEAL,bold=True)
d.text(s,'Infrastructure vendors can monetize heterogeneity; narrow accelerators must correctly predict the winning workload.',Inches(2.65),Inches(4.7),Inches(9.7),Inches(.8),size=21,color=b.LIGHT_TEAL,bold=True,shrink=True)
footer(s,3,True)

# 4 ranking
s=d.slide(fill=b.WHITE); header(s,'Three companies tie for the strongest risk-adjusted profile','Ten dimensions · 1–5 analyst score per dimension')
for i,(name,total,cluster) in enumerate(scores):
    y=Inches(1.80)+i*Inches(.44); col=b.TEAL if total>=39 else (b.GOLD if total>=35 else b.CORAL)
    d.text(s,f'{i+1:02d}',d.M,y,Inches(.38),Inches(.25),size=9,color=col,bold=True)
    d.text(s,name,Inches(1.15),y-Inches(.02),Inches(1.65),Inches(.3),size=13,color=b.NAVY,bold=True)
    d.rect(s,Inches(3.0),y+Inches(.04),Inches(total/50*7.6),Inches(.18),col)
    d.text(s,str(total),Inches(10.85),y-Inches(.03),Inches(.45),Inches(.3),size=12,color=b.NAVY,bold=True,align=PP_ALIGN.RIGHT)
    pill(s,cluster,Inches(11.5),y-Inches(.06),Inches(.82),col,b.NAVY if col!=b.CORAL else b.WHITE)
note(s,'Dimensions: urgency, TAM adjacency, maturity, differentiation, proof, ecosystem, optionality, capital efficiency, timing, exits.')
footer(s,4)

# 5 core
s=d.slide(fill=b.WHITE); header(s,'Core exposure should monetize multiple accelerator winners')
core=[('LIGHTMATTER','Optical interconnect','Bandwidth scarcity','Strategic fit across compute stacks'),('XSIGHT LABS','Programmable Ethernet + DPU','Network throughput','Open, standard deployment surface'),('CORNELIS','Lossless scale-out fabric','Cluster utilization','Named HPC/AI deployment signals'),('TENSTORRENT','Open compute + licensable IP','Lock-in + customization','Multiple monetization paths')]
for i,(name,product,why,edge) in enumerate(core):
    y=Inches(1.5)+i*Inches(1.15)
    d.rect(s,d.M,y,Inches(2.25),Inches(.86),b.NAVY)
    d.text(s,name,d.M+Inches(.15),y+Inches(.22),Inches(1.95),Inches(.35),size=13,color=b.WHITE,bold=True,align=PP_ALIGN.CENTER,shrink=True)
    d.text(s,product,Inches(3.05),y+Inches(.18),Inches(2.65),Inches(.48),size=15,color=b.NAVY,bold=True,shrink=True)
    d.text(s,why,Inches(6.05),y+Inches(.18),Inches(2.25),Inches(.48),size=14,color=b.TEAL,bold=True,shrink=True)
    d.text(s,edge,Inches(8.75),y+Inches(.18),Inches(3.55),Inches(.48),size=14,color=b.INK,shrink=True)
d.text(s,'PORTFOLIO ROLE',d.M,Inches(6.18),Inches(1.4),Inches(.3),size=10,color=b.TEAL,bold=True)
d.text(s,'Anchor positions',Inches(2.0),Inches(6.12),Inches(2.2),Inches(.4),size=17,color=b.NAVY,bold=True)
d.text(s,'Revenue paths survive a fragmented accelerator market.',Inches(4.35),Inches(6.14),Inches(7.7),Inches(.36),size=15,color=b.MUTED)
footer(s,5)

# 6 proof ladder
s=d.slide(fill=b.NAVY)
d.text(s,'Capital must climb four proof gates before it earns conviction',d.M,Inches(.6),d.CW,Inches(1.0),size=30,color=b.WHITE,bold=True,shrink=True)
gates=[('01','ARCHITECTURE','Plausible advantage'),('02','SILICON','Working chip + yield'),('03','CUSTOMER','Reproducible workload'),('04','SYSTEM','Repeatable deployment')]
for i,(n,h,body) in enumerate(gates):
    x=d.M+i*Inches(3.03); y=Inches(1.75)+i*Inches(.45)
    d.rect(s,x,y,Inches(2.5),Inches(2.6),b.NAVY_2,radius=.04)
    d.text(s,n,x+Inches(.2),y+Inches(.2),Inches(.5),Inches(.35),size=11,color=b.TEAL,bold=True)
    d.text(s,h,x+Inches(.2),y+Inches(.82),Inches(2.05),Inches(.38),size=14,color=b.WHITE,bold=True,align=PP_ALIGN.CENTER)
    d.text(s,body,x+Inches(.25),y+Inches(1.45),Inches(2.0),Inches(.7),size=15,color=b.LIGHT_TEAL,bold=True,align=PP_ALIGN.CENTER,shrink=True)
d.text(s,'Funding is not a fifth gate.',d.M,Inches(5.75),d.CW,Inches(.5),size=22,color=b.GOLD,bold=True,align=PP_ALIGN.CENTER)
footer(s,6,True)

# 7 execution bets
s=d.slide(fill=b.WHITE); header(s,'d-Matrix and Axelera become investable through execution—not architecture alone')
for i,(name,thesis,proof,risk,c) in enumerate([
    ('d-Matrix','Rack-scale inference integration','Production claims + GigaIO assets','System complexity',b.TEAL),
    ('Axelera AI','Edge inference economics','Metis products + 2026 financing','Workload-dependent vendor claims',b.GOLD)]):
    x=d.M+i*Inches(6.05)
    d.text(s,name,x,Inches(1.62),Inches(5.55),Inches(.55),size=25,color=b.NAVY,bold=True)
    d.rect(s,x,Inches(2.32),Inches(5.55),Inches(.08),c)
    for j,(lab,txt) in enumerate([('THESIS',thesis),('PROOF TO BUY',proof),('RISK',risk)]):
        y=Inches(2.75)+j*Inches(1.05)
        d.text(s,lab,x,y,Inches(1.25),Inches(.3),size=10,color=c if lab!='RISK' else b.CORAL,bold=True)
        d.text(s,txt,x+Inches(1.45),y-Inches(.03),Inches(3.9),Inches(.55),size=15,color=b.NAVY,bold=True,shrink=True)
d.rect(s,d.M,Inches(6.02),d.CW,Inches(.58),b.NAVY)
d.text(s,'Advance only when customer economics reproduce at rack level.',d.M+Inches(.2),Inches(6.17),d.CW-Inches(.4),Inches(.3),size=14,color=b.WHITE,bold=True,align=PP_ALIGN.CENTER)
footer(s,7)

# 8 moonshots
s=d.slide(fill=b.WHITE); header(s,'Specialist compute is a call option on workload stability')
moon=[('ETCHED','Transformer-only ASIC','Highest specialization','Model architecture drift'),('MATX','Large-model processor','Frontier throughput','2027 shipping + limited proof'),('FRACTILE','In-memory inference','Memory bottleneck','Hardware availability + benchmarks')]
for i,(name,bet,up,risk) in enumerate(moon):
    x=d.M+i*Inches(4.05)
    d.rect(s,x,Inches(1.62),Inches(3.72),Inches(3.95),b.SOFT,line=b.GRID,radius=.03)
    d.text(s,name,x+Inches(.22),Inches(1.92),Inches(3.25),Inches(.45),size=20,color=b.NAVY,bold=True,align=PP_ALIGN.CENTER)
    pill(s,'MOONSHOT',x+Inches(1.15),Inches(2.52),Inches(1.42),b.CORAL)
    for j,(lab,txt) in enumerate([('BET',bet),('UPSIDE',up),('BREAKS IF',risk)]):
        y=Inches(3.12)+j*Inches(.72)
        d.text(s,lab,x+Inches(.22),y,Inches(.82),Inches(.28),size=9,color=b.CORAL if lab=='BREAKS IF' else b.TEAL,bold=True)
        d.text(s,txt,x+Inches(1.08),y-Inches(.02),Inches(2.35),Inches(.4),size=12,color=b.NAVY,bold=True,shrink=True)
note(s,'Underwrite as staged options with technical milestones—not as scaled platform companies.')
footer(s,8)

# 9 duration
s=d.slide(fill=b.NAVY)
d.text(s,'Roadmap duration is hidden dilution',d.M,Inches(.72),d.CW,Inches(.7),size=32,color=b.WHITE,bold=True)
d.rect(s,Inches(1.1),Inches(3.55),Inches(11.05),Inches(.08),b.MUTED)
years=[('NOW','Products / deployments',1.1,b.TEAL),('LATE 2026','Lightmatter sampling',4.15,b.GOLD),('2027','MatX target',7.25,b.CORAL),('Q1 2028','NextSilicon Arbel',10.0,b.CORAL)]
for label,body,x,c in years:
    d.rect(s,Inches(x),Inches(3.32),Inches(.52),Inches(.52),c,radius=.5)
    d.text(s,label,Inches(x)-Inches(.45),Inches(2.25),Inches(1.4),Inches(.38),size=12,color=c,bold=True,align=PP_ALIGN.CENTER)
    d.text(s,body,Inches(x)-Inches(.8),Inches(4.05),Inches(2.1),Inches(.62),size=14,color=b.WHITE,bold=True,align=PP_ALIGN.CENTER,shrink=True)
d.text(s,'Every slip consumes runway while incumbents ship another generation.',d.M,Inches(5.4),d.CW,Inches(.55),size=20,color=b.LIGHT_TEAL,bold=True,align=PP_ALIGN.CENTER)
footer(s,9,True)

# 10 portfolio
s=d.slide(fill=b.WHITE); header(s,'A barbell captures infrastructure compounding and specialist convexity')
d.rect(s,d.M,Inches(1.65),Inches(7.35),Inches(3.7),b.NAVY,radius=.03)
d.text(s,'70%',d.M+Inches(.35),Inches(2.0),Inches(2.0),Inches(.9),size=48,color=b.TEAL,bold=True)
d.text(s,'CORE + EXECUTION',d.M+Inches(.35),Inches(3.05),Inches(3.0),Inches(.35),size=13,color=b.WHITE,bold=True)
d.text(s,'Lightmatter · Xsight · Cornelis · Tenstorrent · d-Matrix · Axelera',d.M+Inches(.35),Inches(3.67),Inches(6.55),Inches(.8),size=18,color=b.LIGHT_TEAL,bold=True,shrink=True)
d.rect(s,Inches(8.25),Inches(1.65),Inches(4.48),Inches(3.7),b.CORAL,radius=.03)
d.text(s,'30%',Inches(8.6),Inches(2.0),Inches(2.0),Inches(.9),size=48,color=b.WHITE,bold=True)
d.text(s,'OPTIONS',Inches(8.6),Inches(3.05),Inches(2.0),Inches(.35),size=13,color=b.WHITE,bold=True)
d.text(s,'NextSilicon · Etched · MatX · Fractile',Inches(8.6),Inches(3.67),Inches(3.55),Inches(.8),size=18,color=b.WHITE,bold=True,shrink=True)
note(s,'Illustrative construction, not a recommendation; size positions by stage, valuation, ownership, and follow-on reserves.')
footer(s,10)

# 11 diligence
s=d.slide(fill=b.WHITE); header(s,'Six kill criteria prevent conviction from becoming narrative lock-in')
criteria=[('01','BENCHMARK','Fails comparable precision, batch, latency, or power'),('02','SOFTWARE','Migration friction erases silicon advantage'),('03','SUPPLY','Yield or packaging blocks repeatable delivery'),('04','CUSTOMER','Design wins do not convert to production revenue'),('05','TIMING','Roadmap slips beyond buyer deployment windows'),('06','DRIFT','Model architecture invalidates specialization')]
for i,(n,h,body) in enumerate(criteria):
    col,row=i%2,i//2; x=d.M+col*Inches(6.05); y=Inches(1.5)+row*Inches(1.42)
    d.text(s,n,x,y,Inches(.45),Inches(.3),size=10,color=b.CORAL,bold=True)
    d.text(s,h,x+Inches(.62),y-Inches(.03),Inches(1.25),Inches(.34),size=13,color=b.NAVY,bold=True)
    d.text(s,body,x+Inches(2.0),y-Inches(.03),Inches(3.55),Inches(.58),size=14,color=b.INK,bold=True,shrink=True)
    d.rect(s,x,y+Inches(.72),Inches(5.55),Pt(1),b.GRID)
d.rect(s,d.M,Inches(5.95),d.CW,Inches(.62),b.CORAL)
d.text(s,'If a company fails two gates, stop funding the story and reprice the option.',d.M+Inches(.2),Inches(6.11),d.CW-Inches(.4),Inches(.32),size=14,color=b.WHITE,bold=True,align=PP_ALIGN.CENTER)
footer(s,11)

# 12
s=d.slide(fill=b.NAVY); d.rect(s,0,0,Inches(.16),d.H,b.TEAL)
d.text(s,'Back the toll roads.\nOption the rockets.',d.M,Inches(1.25),Inches(9.5),Inches(1.75),size=48,color=b.WHITE,bold=True,shrink=True)
d.text(s,'Core thesis',d.M,Inches(3.65),Inches(1.4),Inches(.3),size=11,color=b.TEAL,bold=True)
d.text(s,'Interconnect, open IP, and rack infrastructure compound across winners.',Inches(2.2),Inches(3.55),Inches(9.4),Inches(.7),size=22,color=b.LIGHT_TEAL,bold=True,shrink=True)
d.text(s,'Discipline',d.M,Inches(4.72),Inches(1.4),Inches(.3),size=11,color=b.CORAL,bold=True)
d.text(s,'Specialist compute earns follow-on capital only by clearing proof gates.',Inches(2.2),Inches(4.62),Inches(9.4),Inches(.7),size=22,color=b.WHITE,bold=True,shrink=True)
note(s,'CRN list; company releases; You.com Livecrawl Level 2 research · August 2026',6.34,True)
footer(s,12,True)

d.save(OUT)
print(OUT)
