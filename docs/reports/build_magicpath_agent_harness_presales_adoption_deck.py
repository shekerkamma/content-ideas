#!/usr/bin/env python3
"""Build MagicPath vs agent harness pre-sales adoption deck."""
import sys
sys.path.insert(0, "/home/sheke/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, Inches, PP_ALIGN, MSO_ANCHOR

TOTAL = 24
OUT = "docs/reports/magicpath-agent-harness-presales-adoption-reviewed.pptx"

d = Deck(footer="MagicPath Adoption Brief · Pre-Sales Demo Acceleration | June 2026")
b = d.b


def footer(s, n, dark=False):
    d.footer(s, n, TOTAL, dark=dark)


def chip(s, text, left, top, width, fill=None, color=None):
    d.rect(s, left, top, width, Inches(0.4), fill or b.NAVY_2, radius=0.08)
    d.text(s, text, left + Inches(0.08), top + Inches(0.04), width - Inches(0.16), Inches(0.32),
           size=10.2, color=color or b.TEAL, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shrink=True)


def callout(s, text, top, fill=None, color=None, height=0.62):
    d.rect(s, d.M, Inches(top), d.CW, Inches(height), fill or b.NAVY, radius=0.035)
    d.text(s, text, Inches(0.85), Inches(top + 0.08), Inches(11.5), Inches(height - 0.12),
           size=12.6, color=color or b.TEAL, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)


def small_card(s, left, top, w, h, title, body, accent=b.TEAL, title_size=13, body_size=10.7):
    d.rect(s, left, top, w, h, b.SOFT, radius=0.05, shadow=True)
    d.rect(s, left, top, w, Inches(0.08), accent)
    d.text(s, title, left + Inches(0.18), top + Inches(0.18), w - Inches(0.36), Inches(0.38),
           size=title_size, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, left + Inches(0.18), top + Inches(0.67), w - Inches(0.36), h - Inches(0.82),
           size=body_size, color=b.INK, shrink=True)


def numbered_row(s, n, title, body, top, accent=b.TEAL):
    d.rect(s, d.M, Inches(top), Inches(0.52), Inches(0.52), b.NAVY, radius=0.08)
    d.text(s, str(n), d.M + Inches(0.05), Inches(top + 0.03), Inches(0.42), Inches(0.44),
           size=15, color=accent, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, title, Inches(1.28), Inches(top - 0.01), Inches(3.6), Inches(0.34),
           size=13.7, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, Inches(4.75), Inches(top - 0.01), Inches(7.65), Inches(0.5),
           size=11.3, color=b.INK, shrink=True)


def scenario_slide(num, title, buyer, direct_agent, magicpath_role, demo_moment, poc_bridge, guardrail, accent):
    s = d.slide(fill=b.WHITE)
    d.header(s, title, buyer)
    small_card(s, d.M, Inches(1.82), Inches(3.75), Inches(1.85), "If using agents directly", direct_agent, b.CORAL, 12.6, 10.5)
    small_card(s, Inches(4.72), Inches(1.82), Inches(3.75), Inches(1.85), "What MagicPath adds", magicpath_role, accent, 12.6, 10.5)
    small_card(s, Inches(8.82), Inches(1.82), Inches(3.45), Inches(1.85), "Buyer-visible moment", demo_moment, b.GOLD, 12.6, 10.2)
    d.text(s, "POC bridge", d.M, Inches(4.25), Inches(2.2), Inches(0.32), size=11.5, color=b.MUTED, bold=True)
    d.rect(s, d.M, Inches(4.65), d.CW, Inches(0.72), b.LIGHT_TEAL, radius=0.035)
    d.text(s, poc_bridge, Inches(0.85), Inches(4.73), Inches(11.5), Inches(0.54), size=12.4, color=b.NAVY, bold=True, shrink=True)
    d.text(s, "Sales guardrail", d.M, Inches(5.82), Inches(2.2), Inches(0.32), size=11.5, color=b.MUTED, bold=True)
    d.text(s, guardrail, d.M, Inches(6.18), d.CW, Inches(0.5), size=11.6, color=b.INK, shrink=True)
    footer(s, num)


# 1 Cover
s = d.slide(fill=b.NAVY)
d.rect(s, Inches(11.35), 0, Inches(1.98), d.H, b.NAVY_2)
d.rect(s, Inches(11.35), 0, Inches(0.08), d.H, b.TEAL)
d.text(s, "EXECUTIVE / SALES ENABLEMENT", d.M, Inches(0.88), Inches(7.5), Inches(0.35), size=13, color=b.TEAL, bold=True)
d.text(s, "Why MagicPath\nWhen We Already\nHave Agents?", d.M, Inches(1.42), Inches(9.7), Inches(2.35), size=43, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
d.rect(s, d.M, Inches(4.08), Inches(1.35), Inches(0.06), b.TEAL)
d.text(s, "A practical pre-sales adoption brief: where MagicPath adds value, where it does not, and how to use it across six buyer scenarios.",
       d.M, Inches(4.38), Inches(8.8), Inches(0.82), size=16, color=b.MUTED, shrink=True)
x=d.M
for label in ["Agent Harness", "Visual Spec", "Buyer Workflow", "POC Bridge"]:
    chip(s, label, x, Inches(5.45), Inches(2.15)); x += Inches(2.35)
footer(s, 1, dark=True)

# 2 BLUF
s=d.slide(fill=b.WHITE)
d.header(s, "The Answer First", "MagicPath is not valuable because it adds another agent")
callout(s, "Agents are good at building from instructions. MagicPath is useful when the missing layer is a visual, collaborative, prospect-specific spec that humans and agents can both work from.", 1.72, b.NAVY, b.WHITE, 0.88)
small_card(s, d.M, Inches(3.05), Inches(3.65), Inches(1.85), "What you already have", "Claude Code, Codex, Cursor, and your agent harness can build, refactor, test, and deploy from a clear instruction set.", b.CORAL)
small_card(s, Inches(4.65), Inches(3.05), Inches(3.65), Inches(1.85), "What is often missing", "The buyer-specific workflow: screens, roles, decisions, exception states, approvals, integrations, and demo storyline.", b.GOLD)
small_card(s, Inches(8.7), Inches(3.05), Inches(3.65), Inches(1.85), "MagicPath's job", "Create the shared visual surface where sales, pre-sales, design, buyer context, and coding agents align before code is built.", b.TEAL)
callout(s, "If your harness already creates great buyer-specific visual specs, MagicPath may be optional. If prototypes are generic or slow to scope, MagicPath can be useful.", 5.82, b.LIGHT_TEAL, b.NAVY, 0.58)
footer(s,2)

# 3 Objection
s=d.slide(fill=b.WHITE)
d.header(s, "The Core Objection", "Why integrate with Claude Code or Codex when we can use them directly?")
small_card(s, d.M, Inches(1.85), Inches(5.6), Inches(2.25), "Direct agent workflow", "Prompt → code → app\n\nThis works when the requirement is clear, the UI pattern is obvious, and the buyer does not need a highly tailored experience to move forward.", b.CORAL, 15, 12)
small_card(s, Inches(6.75), Inches(1.85), Inches(5.6), Inches(2.25), "Pre-sales reality", "Discovery notes are ambiguous. Buyers speak in operational terms. The demo must show their workflow, not just a functional app.", b.GOLD, 15, 12)
callout(s, "The integration point is not 'MagicPath replaces Claude Code/Codex.' It is 'MagicPath gives Claude Code/Codex a better visual spec to build from.'", 5.05, b.NAVY, b.TEAL, 0.7)
footer(s,3)

# 4 Layer model
s=d.slide(fill=b.WHITE)
d.header(s, "Layer Model", "Separate the business problem, visual spec, code agent, and deployment layer")
layers=[("Business problem", "Discovery call, buyer pain, economics, stakeholder goals", b.CORAL), ("Workflow/spec/design", "MagicPath canvas, scenario storyboard, screens, states, integration placeholders", b.TEAL), ("Implementation", "Claude Code, Codex, Cursor, internal agent harness", b.GOLD), ("Deployment", "Vercel, Netlify, internal sandbox, demo URL", b.ACCENT), ("Commercial next step", "POC package, data access, owners, success metric", b.NAVY)]
for i,(title,body,color) in enumerate(layers):
    left=d.M+i*Inches(2.48)
    d.rect(s,left,Inches(2.05),Inches(2.22),Inches(2.05),b.SOFT,radius=0.05,shadow=True)
    d.rect(s,left,Inches(2.05),Inches(2.22),Inches(0.08),color)
    d.text(s,title,left+Inches(0.14),Inches(2.36),Inches(1.94),Inches(0.45),size=12.6,color=b.NAVY,bold=True,shrink=True)
    d.text(s,body,left+Inches(0.14),Inches(2.95),Inches(1.94),Inches(1.05),size=9.8,color=b.INK,shrink=True)
    if i<4:
        d.text(s,"→",left+Inches(2.27),Inches(2.78),Inches(0.22),Inches(0.45),size=16,color=b.MUTED,align=PP_ALIGN.CENTER)
callout(s,"The sales value sits in the workflow/spec/design layer. That is where the buyer decides whether the proposed AI feels real for their business.",5.35,b.LIGHT_TEAL,b.NAVY,0.6)
footer(s,4)

# 5 Comparison table
s=d.slide(fill=b.WHITE)
d.header(s, "Direct Agent vs MagicPath-Assisted Agent", "Use the right workflow for the right kind of problem")
headers=["Question","Use Claude Code/Codex directly","Use MagicPath + agent"]
lefts=[d.M,Inches(4.05),Inches(8.15)]; widths=[Inches(3.25),Inches(3.8),Inches(4.15)]
for j,h in enumerate(headers):
    d.rect(s,lefts[j],Inches(1.72),widths[j],Inches(0.45),b.NAVY)
    d.text(s,h,lefts[j]+Inches(0.08),Inches(1.78),widths[j]-Inches(0.16),Inches(0.32),size=10.2,color=b.WHITE,bold=True,align=PP_ALIGN.CENTER,shrink=True)
rows=[
("Requirement clarity","Clear written spec exists","Workflow needs visual alignment"),
("Buyer involvement","Low; internal build task","High; buyer must see their process"),
("UI specificity","Generic/functional is enough","Industry-specific UI matters"),
("Iteration mode","Prompt/code/test loop","Canvas + agent build loop"),
("Best output","Working code","Sales-ready prototype + POC scope"),
("When to avoid","When design ambiguity is high","When backend logic is the real work"),
]
for i,row in enumerate(rows):
    top=Inches(2.22)+i*Inches(0.68)
    fill=b.SOFT if i%2==0 else b.WHITE
    for j,val in enumerate(row):
        d.rect(s,lefts[j],top,widths[j],Inches(0.58),fill,line=b.GRID)
        d.text(s,val,lefts[j]+Inches(0.08),top+Inches(0.06),widths[j]-Inches(0.16),Inches(0.46),size=9.5,color=b.NAVY if j==0 else b.INK,bold=(j==0),shrink=True)
footer(s,5)

# 6 What MagicPath actually does
s=d.slide(fill=b.WHITE)
d.header(s,"The Real Job MagicPath Does", "It is a visual alignment layer, not a replacement for the build agent")
items=[
("Visual requirements canvas","Align sales, pre-sales, design, buyer language, screens, states, and integrations before code."),
("Demo storyboard builder","Define the buyer journey: dashboard → exception → decision → approval → next action."),
("Agent-readable design spec","Give Claude Code/Codex a concrete visual target instead of a long ambiguous prompt."),
("Prospect-specific generator","Make the demo feel like the buyer's workflow, not a generic AI SaaS screen."),
("Iteration surface","Change the canvas when the buyer asks for approval, audit trail, role change, or system detail."),
]
for i,(t,body) in enumerate(items):
    numbered_row(s,i+1,t,body,1.82+i*0.92,b.TEAL)
footer(s,6)

# 7 When useful / not
s=d.slide(fill=b.WHITE)
d.header(s,"Adoption Rule", "Do not force MagicPath into every agent workflow")
small_card(s,d.M,Inches(1.8),Inches(5.75),Inches(3.65),"Use MagicPath when", "- Demo is visual and workflow-heavy\n- Buyer-specific relevance matters\n- Multiple stakeholders need to align\n- Prospect asks 'show me our workflow'\n- UI polish affects credibility\n- POC scope is still ambiguous\n- Sales needs a repeatable demo artifact", b.TEAL, 16, 12)
small_card(s,Inches(6.75),Inches(1.8),Inches(5.75),Inches(3.65),"Skip MagicPath when", "- Clear written spec already exists\n- Work is backend-heavy\n- Internal tool does not need visual polish\n- Harness already handles screenshots, design context, and iterations\n- Buyer does not need a clickable workflow\n- Time is better spent integrating real data", b.CORAL, 16, 12)
callout(s,"The practical rule: use MagicPath when the sales risk is unclear workflow fit. Use agents directly when the engineering task is already clear.",6.05,b.NAVY,b.TEAL,0.55)
footer(s,7)

# 8 Sales impact
s=d.slide(fill=b.WHITE)
d.header(s,"Why Sales And Pre-Sales Should Care", "The tool is only useful if it changes deal behavior")
impacts=[("Faster relevance","Move from generic demo to prospect-specific workflow while momentum is live.",b.TEAL), ("Better qualification","The prototype exposes missing data, integration risk, role confusion, and buying objections early.",b.GOLD), ("Cleaner POC scope","Buyer feedback becomes backlog, success metric, data request, and implementation boundary.",b.CORAL), ("Higher executive confidence","Leaders see the operating model, controls, and ROI path instead of abstract AI capability.",b.ACCENT)]
for i,(t,body,color) in enumerate(impacts):
    left=d.M+(i%2)*Inches(6.15); top=Inches(1.9)+(i//2)*Inches(1.8)
    small_card(s,left,top,Inches(5.75),Inches(1.35),t,body,color,14,11.2)
callout(s,"Sales should not sell MagicPath. Sales should use MagicPath to make the prospect's desired future workflow visible.",5.95,b.LIGHT_TEAL,b.NAVY,0.6)
footer(s,8)

# 9 Six scenarios summary
s=d.slide(fill=b.WHITE)
d.header(s,"How It Addresses The Six Scenarios", "Same pattern, different buyer workflow")
scenarios=[("Manufacturing","Alert → asset context → SAP work order","Downtime or scrap workflow feels real"),("Legal","Upload → clause risk → partner approval","Trust barrier drops through human review"),("Healthcare","Patient mobile intake → staff verification","ROI is visible through time saved"),("Financial Services","Document extraction → checklist → sign-off","Regulatory fear reduced by source traceability"),("Construction","Site map → violation → morning report","Weekly reporting becomes daily control"),("AI Readiness","Assessment → ranked use cases → ROI cards","Vague AI interest becomes funded roadmap")]
for i,(name,flow,value) in enumerate(scenarios):
    left=d.M+(i%3)*Inches(4.1); top=Inches(1.82)+(i//3)*Inches(2.05)
    small_card(s,left,top,Inches(3.75),Inches(1.55),name,flow+"\n\n"+value,[b.TEAL,b.GOLD,b.CORAL,b.ACCENT,b.TEAL,b.GOLD][i],13.5,10.2)
callout(s,"The common move: turn the prospect's business scenario into a clickable decision workflow, then convert that workflow into POC scope.",6.08,b.NAVY,b.TEAL,0.62)
footer(s,9)

# 10-15 scenario slides
scenario_slide(10,"Scenario 1: Manufacturing", "Buyer: VP Manufacturing, Plant VP, VP Quality", "Claude Code/Codex can build a dashboard if given a clear spec, but may default to generic charts and synthetic alerts.", "Creates plant-specific visual language: lines, assets, OEE, severity, maintenance status, SAP PM placeholder.", "Buyer clicks a high-severity asset alert and sees root cause, downtime risk, and create-work-order flow.", "Ask for historian sample, asset taxonomy, downtime/scrap metric, SAP PM/QM owner, and one line/station for POC.", "Do not claim live SAP integration in the demo unless it exists. Label it as integration placeholder and scope it as POC work.", b.TEAL)
scenario_slide(11,"Scenario 2: Legal", "Buyer: Managing Partner, Legal Ops, GC", "Agents can build a contract analyzer UI, but legal buyers need workflow trust, auditability, and human approval modeled visually.", "Defines the review journey: upload, highlighted clause, risk rationale, confidence, precedent/citation placeholder, partner approval.", "Buyer sees a risky clause flagged and routes it to a partner instead of accepting AI output blindly.", "Ask for document types, clause playbook, review authority matrix, risk taxonomy, and pilot template set.", "Never position AI as autonomous legal judgment. The demo should show AI assistance, source/rationale, and human override.", b.GOLD)
scenario_slide(12,"Scenario 3: Healthcare", "Buyer: Practice Manager, COO, Front Desk Lead", "Agents can build a form and dashboard, but may miss the operational handoff between patient, staff, insurance, and EHR.", "Creates a dual-view workflow: patient mobile intake plus staff queue with verification, exception, and EHR sync status.", "Buyer submits intake on mobile and immediately sees the record in the staff queue with status badges.", "Ask for intake steps, top exception reasons, insurance workflow, EHR constraints, HIPAA/security path, and baseline intake time.", "Do not imply production HIPAA readiness from a prototype. Use it to scope compliance, hosting, audit, and integration requirements.", b.CORAL)
scenario_slide(13,"Scenario 4: Financial Services", "Buyer: VP Mortgage Ops, Underwriting, Risk", "Agents can build document extraction screens, but finance buyers need traceability, controls, and exception handling before they trust automation.", "Shapes the workspace around source documents, extracted fields, confidence, page references, checklist status, and adjudicator sign-off.", "Buyer clicks an extracted income field and sees the source document location before approving the checklist.", "Ask for sample package, LOS system, underwriting checklist, exception taxonomy, compliance constraints, and target cycle-time metric.", "Frame as AI-assisted review. The underwriter remains accountable; the prototype demonstrates review compression, not automatic approval.", b.ACCENT)
scenario_slide(14,"Scenario 5: Construction", "Buyer: Project Director, Safety Lead, Operations Director", "Agents can build a map or report UI, but may miss how field teams consume site risk, progress, assignments, and morning reporting.", "Creates a command center: portfolio map, site drilldown, visual exception, owner assignment, and generated morning report.", "Buyer opens a site, sees a safety/progress issue, assigns it, and reviews an auto-generated daily report.", "Ask for active site list, reporting cadence, image/drone source, safety categories, trade schedule, and superintendent workflow.", "Avoid implying real computer vision accuracy without data. Use visual detections as storyboard placeholders for a POC validation plan.", b.TEAL)
scenario_slide(15,"Scenario 6: AI Readiness", "Buyer: CTO, COO, Transformation Lead", "Agents can generate a questionnaire or dashboard, but the value is in turning vague AI ambition into prioritized initiatives.", "Creates an executive portal: intake wizard, maturity radar, ranked use cases, ROI bands, timeline, and next-step CTA.", "Buyer answers questions and sees three ranked projects with payback logic and implementation path.", "Ask for strategic priorities, data maturity, systems, team capability, risk tolerance, and executive sponsor for first use case.", "Do not make ROI look falsely precise. Use ranges, assumptions, and confidence levels; convert interest into paid discovery.", b.GOLD)

# 16 POC conversion
s=d.slide(fill=b.WHITE)
d.header(s,"Convert Prototype Feedback Into POC Scope", "MagicPath is valuable when it changes what happens after the demo")
steps=[("Buyer asks for change","Capture as canvas update or backlog item"),("Buyer questions data","Convert into data access request"),("Buyer asks about systems","Convert into integration scope"),("Buyer worries about trust","Add approval, audit, and exception states"),("Buyer asks ROI","Define baseline metric and success threshold")]
for i,(event,action) in enumerate(steps):
    numbered_row(s,i+1,event,action,1.8+i*0.86,b.TEAL)
callout(s,"The prototype is not the destination. It is a structured way to turn buyer reactions into POC design decisions.",6.15,b.LIGHT_TEAL,b.NAVY,0.55)
footer(s,16)

# 17 Adoption playbook
s=d.slide(fill=b.WHITE)
d.header(s,"Pre-Sales Adoption Playbook", "How sales teams should actually use the tool")
plays=[("Before discovery","Prepare vertical prompt library and example workflows."),("During discovery","Listen for roles, systems, approvals, metrics, and exceptions."),("After discovery","Create MagicPath canvas from brief; hand off to agent for prototype."),("Before demo","QA assumptions, labels, integration placeholders, and talk track."),("During demo","Let buyer interact; capture changes live."),("After demo","Send POC scope: data, systems, owners, success metric, timeline.")]
for i,(t,body) in enumerate(plays):
    left=d.M+(i%3)*Inches(4.1); top=Inches(1.82)+(i//3)*Inches(2.05)
    small_card(s,left,top,Inches(3.75),Inches(1.45),t,body,[b.CORAL,b.GOLD,b.TEAL,b.ACCENT,b.TEAL,b.GOLD][i],13.2,10.5)
footer(s,17)

# 18 Team roles
s=d.slide(fill=b.WHITE)
d.header(s,"Who Does What", "Adoption fails if everyone thinks someone else owns the demo artifact")
roles=[("Account Executive","Owns buyer problem, commercial urgency, stakeholder map, and next step."),("Solution Consultant","Translates discovery into workflow, demo story, controls, and POC assumptions."),("MagicPath Operator","Builds visual canvas, imports context, applies design system, refines screens."),("Agent Harness Lead","Uses Claude Code/Codex/Cursor to build clickable app from canvas/spec."),("Delivery Lead","Validates POC feasibility, integration effort, compliance, and rollout path.")]
for i,(role,body) in enumerate(roles):
    numbered_row(s,i+1,role,body,1.78+i*0.9,[b.CORAL,b.GOLD,b.TEAL,b.ACCENT,b.NAVY][i])
footer(s,18)

# 19 Demo quality checklist
s=d.slide(fill=b.WHITE)
d.header(s,"Demo Quality Checklist", "What makes a MagicPath-assisted demo credible")
checks=["Uses buyer's industry language and roles", "Shows at least one exception state", "Includes human approval where risk is high", "Labels mock data and placeholder integrations", "Links every screen to a POC question", "Has a 90-second story before product tour", "Makes next step obvious: data, system, owner, metric"]
for i,c in enumerate(checks):
    top=Inches(1.75)+i*Inches(0.68)
    d.rect(s,d.M,top,Inches(0.38),Inches(0.38),b.TEAL,radius=0.08)
    d.text(s,"✓",d.M+Inches(0.05),top+Inches(0.01),Inches(0.28),Inches(0.32),size=13,color=b.NAVY,bold=True,align=PP_ALIGN.CENTER)
    d.text(s,c,Inches(1.18),top-Inches(0.01),Inches(11.0),Inches(0.42),size=12.2,color=b.INK,shrink=True)
callout(s,"If the prototype cannot answer 'what would this look like for us?', it is just another generic demo.",6.45,b.NAVY,b.TEAL,0.42)
footer(s,19)

# 20 Commercial packaging
s=d.slide(fill=b.WHITE)
d.header(s,"Commercial Packaging", "Use MagicPath to make the next purchase smaller and easier")
packages=[("Discovery Sprint","$10K-$25K","Validate workflow, data availability, and business case."),("Focused POC","$40K-$75K","One workflow, one dataset, one success metric, one decision owner."),("Production Pilot","$100K-$250K","Security, integration, user testing, deployment, adoption workflow."),("Managed Service","$3K-$10K/mo","Monitoring, iteration, retraining, reporting, and enablement.")]
for i,(name,price,body) in enumerate(packages):
    left=d.M+(i%2)*Inches(6.15); top=Inches(1.8)+(i//2)*Inches(1.85)
    small_card(s,left,top,Inches(5.75),Inches(1.42),name,price+"\n"+body,[b.TEAL,b.GOLD,b.CORAL,b.ACCENT][i],14,10.8)
callout(s,"MagicPath helps sell the POC by making scope concrete; it does not remove the need to validate data, security, integration, and adoption.",5.9,b.LIGHT_TEAL,b.NAVY,0.62)
footer(s,20)

# 21 Metrics
s=d.slide(fill=b.WHITE)
d.header(s,"How To Measure Whether MagicPath Is Worth It", "Adopt it only if it improves sales outcomes")
metrics=[("Discovery-to-demo elapsed time","Can we produce a tailored prototype faster?"),("Demo-to-POC conversion","Does the clickable workflow increase next-step commitment?"),("Solution architect hours","Does it reduce expensive custom demo effort?"),("POC scope clarity","Are data/system/owner/success metric clearer after demo?"),("Stakeholder expansion","Does the demo get forwarded to more decision makers?"),("Win/loss notes","Do buyers cite relevance and workflow fit?")]
for i,(m,why) in enumerate(metrics):
    left=d.M+(i%2)*Inches(6.15); top=Inches(1.75)+(i//2)*Inches(1.42)
    small_card(s,left,top,Inches(5.75),Inches(1.02),m,why,[b.TEAL,b.GOLD,b.CORAL,b.ACCENT,b.TEAL,b.GOLD][i],12.5,10.1)
footer(s,21)

# 22 Risks
s=d.slide(fill=b.WHITE)
d.header(s,"Risks And Anti-Patterns", "Where MagicPath can hurt more than help")
risks=[("Pretty but fake","Prototype looks good but cannot connect to real systems or data."),("Over-automation story","Sales implies AI will decide in legal, healthcare, finance, or safety workflows."),("No POC bridge","Demo ends with applause but no data request, owner, metric, or timeline."),("Tool-first selling","Sales pitches MagicPath instead of the buyer's workflow and business outcome."),("Harness duplication","Team adds MagicPath even when agent harness already solves visual context well.")]
for i,(r,body) in enumerate(risks):
    numbered_row(s,i+1,r,body,1.8+i*0.9,b.CORAL)
footer(s,22)

# 23 Recommendation
s=d.slide(fill=b.WHITE)
d.header(s,"Recommended Position", "Adopt selectively as a pre-sales workflow layer")
callout(s,"Use MagicPath only where the sales risk is unclear workflow fit, buyer-specific visualization, or slow custom demo creation.",1.75,b.NAVY,b.WHITE,0.78)
small_card(s,d.M,Inches(3.05),Inches(3.75),Inches(1.7),"Do now","Pilot it on 3 live opportunities across different verticals; measure demo speed, buyer engagement, and POC conversion.",b.TEAL,14,11)
small_card(s,Inches(4.72),Inches(3.05),Inches(3.75),Inches(1.7),"Do not do","Do not mandate it for every agent project or backend-heavy build. That will create process drag.",b.CORAL,14,11)
small_card(s,Inches(8.82),Inches(3.05),Inches(3.45),Inches(1.7),"Decision gate","Keep it if it improves conversion or reduces solution effort. Drop it if direct agents perform equally well.",b.GOLD,14,10.5)
callout(s,"The winning motion is not MagicPath vs agents. It is MagicPath before agents when humans need to agree on what the agent should build.",5.8,b.LIGHT_TEAL,b.NAVY,0.62)
footer(s,23)

# 24 Sources / status
s=d.slide(fill=b.WHITE)
d.header(s,"Sources And Deck Status", "Evidence base and QA status")
sources=[("MagicPath documentation","https://www.magicpath.ai/documentation","Shared canvas, external agents, code export, Figma and product workflows."),("MagicPath external agents","https://www.magicpath.ai/documentation/features/external-agents","Claude Code, Codex, Cursor, and external agent positioning."),("MagicPath Figma Connect","https://www.magicpath.ai/documentation/features/figma-connect","Figma-to-MagicPath workflow for existing design context."),("Anthropic Claude Design","https://www.anthropic.com/news/claude-design-anthropic-labs","Comparable Claude-native design-to-Claude-Code handoff pattern."),("Claude Design Help Center","https://support.claude.com/en/articles/14604416-get-started-with-claude-design","Claude Design capabilities and handoff to Claude Code.")]
for i,(name,url,note) in enumerate(sources):
    top=Inches(1.65)+i*Inches(0.78)
    d.text(s,name,d.M,top,Inches(2.75),Inches(0.28),size=10.8,color=b.NAVY,bold=True,shrink=True)
    d.text(s,url,Inches(3.2),top,Inches(4.55),Inches(0.28),size=8.4,color=b.ACCENT,shrink=True)
    d.text(s,note,Inches(7.95),top,Inches(4.45),Inches(0.36),size=9.2,color=b.INK,shrink=True)
callout(s,"Deck status: reviewed after PPTX structural validation and preview-render text overflow QA.",6.32,b.SOFT,b.NAVY,0.42)
footer(s,24)

d.save(OUT)
