#!/usr/bin/env python3
"""Client-ready AI Use-Case CATALOG (8 detailed use cases) for the DFW boutique-
brokerage vertical. Grounded on DFW-Brokerage-Prospects.xlsx + audience research.
Applies the ai-use-cases-consultant worldview: vertical scoping, realization-
pattern selection, KPI baselines, AWS scoping matrix, RAI Identify->Operate.
Pilot discipline = 3 of the 8 run in the first 90 days; the rest are the roadmap."""
import sys, csv
sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, Inches, Pt, PP_ALIGN, MSO_ANCHOR

DOCS = "/home/shekerk/content-ideas/docs/solo-agent-agency"
OUT = f"{DOCS}/DFW-Brokerage-AI-UseCases-draft.pptx"
prospects = list(csv.reader(open(f"{DOCS}/re-brokerage-prospects.csv", newline="", encoding="utf-8")))[1:]

d = Deck(footer="AI Use-Case Catalog · DFW Boutique Brokerage Vertical · Confidential | 2026")
b = d.b
MF, CWF = 0.6, 12.133
_pages = []
def page(fill=b.WHITE, dark=False):
    s = d.slide(fill=fill); _pages.append((s, dark)); return s
def H(s, t, sub=None): d.header(s, t, sub)

def card(s, x, y, w, h, title, body, *, accent=None, idx=None, fill=None):
    accent = accent or b.TEAL
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(h), fill or b.SOFT, radius=0.06, shadow=True)
    d.rect(s, Inches(x), Inches(y), Inches(0.08), Inches(h), accent)
    if idx is not None:
        d.rect(s, Inches(x+0.22), Inches(y+0.22), Inches(0.42), Inches(0.42), b.NAVY, radius=0.2)
        d.text(s, str(idx), Inches(x+0.22), Inches(y+0.27), Inches(0.42), Inches(0.34), size=15,
               color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        tx = x + 0.8
    else:
        tx = x + 0.28
    d.text(s, title, Inches(tx), Inches(y+0.22), Inches(w-(tx-x)-0.2), Inches(0.45), size=14,
           color=b.NAVY, bold=True, shrink=True)
    if body:
        d.text(s, body, Inches(x+0.28), Inches(y+0.74), Inches(w-0.5), Inches(h-0.9), size=11.3,
               color=b.INK, shrink=True)

def divider(num, title, sub):
    s = page(fill=b.NAVY, dark=True)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.text(s, f"SECTION {num}", Inches(MF), Inches(2.6), Inches(6), Inches(0.4), size=15, color=b.TEAL, bold=True)
    d.text(s, title, Inches(MF), Inches(3.1), Inches(11.2), Inches(1.2), size=38, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(MF), Inches(4.4), Inches(1.6), Inches(0.05), b.TEAL)
    d.text(s, sub, Inches(MF), Inches(4.6), Inches(10.8), Inches(0.7), size=15, color=b.LIGHT_TEAL, shrink=True)
    return s

def kpi_grid(s, kpis, y=1.95, h=2.5):
    n = len(kpis); gap = 0.3; cw = (CWF - gap*(n-1)) / n
    for i, (num, lab, note) in enumerate(kpis):
        x = MF + i*(cw+gap)
        d.rect(s, Inches(x), Inches(y), Inches(cw), Inches(h), b.NAVY, radius=0.05, shadow=True)
        d.text(s, num, Inches(x+0.1), Inches(y+0.26), Inches(cw-0.2), Inches(0.82), size=28, color=b.GOLD,
               bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, lab, Inches(x+0.12), Inches(y+1.12), Inches(cw-0.24), Inches(0.5), size=12, color=b.WHITE,
               bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, note, Inches(x+0.18), Inches(y+1.66), Inches(cw-0.36), Inches(h-1.76), size=10.3,
               color=b.LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)

def takeaway(s, label, txt, y=5.6, h=0.95, fill=None, accent=None, tcol=None):
    d.rect(s, Inches(MF), Inches(y), Inches(CWF), Inches(h), fill or b.LIGHT_TEAL, radius=0.04)
    d.rect(s, Inches(MF), Inches(y), Inches(0.08), Inches(h), accent or b.TEAL)
    d.text(s, label, Inches(MF+0.3), Inches(y+0.15), Inches(7), Inches(0.32), size=12, color=tcol or b.DARK_TEAL, bold=True)
    d.text(s, txt, Inches(MF+0.3), Inches(y+0.5), Inches(CWF-0.6), Inches(h-0.6), size=12.5, color=tcol or b.INK, shrink=True)

def scorecard(s, heads, widths, rows, y=1.9, rh=0.8, hh=0.5, fs=10.6):
    xs = [MF]
    for w in widths[:-1]: xs.append(xs[-1] + w)
    d.rect(s, Inches(MF), Inches(y), Inches(CWF), Inches(hh), b.NAVY)
    for hx_, hw, ht in zip(xs, widths, heads):
        d.text(s, ht, Inches(hx_+0.12), Inches(y+0.08), Inches(hw-0.2), Inches(hh-0.14), size=11,
               color=b.WHITE, bold=True, shrink=True, anchor=MSO_ANCHOR.MIDDLE)
    ry = y + hh
    for row in rows:
        ac = row[-1]; cells = row[:-1]
        d.rect(s, Inches(MF), Inches(ry), Inches(CWF), Inches(rh), b.SOFT)
        d.rect(s, Inches(MF), Inches(ry), Inches(0.07), Inches(rh), ac)
        for cx, cw, val, i in zip(xs, widths, cells, range(len(cells))):
            d.text(s, val, Inches(cx+0.1), Inches(ry+0.08), Inches(cw-0.16), Inches(rh-0.14), size=fs,
                   color=b.NAVY if i == 0 else b.INK, bold=(i == 0), shrink=True, anchor=MSO_ANCHOR.MIDDLE)
        ry += rh + 0.03
    return ry

def cards_grid(s, items, cols=2, y0=1.95, ch=1.8, idx=False):
    cw = (CWF - 0.3*(cols-1)) / cols
    for i, (h, body) in enumerate(items):
        x = MF + (i % cols)*(cw+0.3); y = y0 + (i // cols)*(ch+0.25)
        card(s, x, y, cw, ch, h, body, idx=(i+1) if idx else None, accent=b.TEAL if i % 2 == 0 else b.ACCENT)

def realization(s, no, total, name, tagline, challenge, solution, stats, steps, stack, systems, users, panel, pilot):
    d.rect(s, 0, 0, Inches(3.5), d.H, panel)
    tag = b.NAVY if panel in (b.TEAL, b.GOLD) else b.WHITE
    d.text(s, f"USE CASE {no} OF {total}", Inches(0.35), Inches(0.5), Inches(2.9), Inches(0.35), size=12, color=tag, bold=True)
    d.text(s, name, Inches(0.35), Inches(0.95), Inches(2.95), Inches(1.4), size=21, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(0.35), Inches(2.4), Inches(1.1), Inches(0.05), tag)
    d.text(s, tagline, Inches(0.35), Inches(2.6), Inches(2.95), Inches(2.7), size=12, color=tag, shrink=True)
    badge = "PILOT (90-DAY)" if pilot else "ROADMAP"
    d.rect(s, Inches(0.35), Inches(6.45), Inches(2.4), Inches(0.5), b.NAVY if panel != b.NAVY_2 else b.GOLD, radius=0.1)
    d.text(s, badge, Inches(0.35), Inches(6.57), Inches(2.4), Inches(0.3), size=11,
           color=b.GOLD if panel != b.NAVY_2 else b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    rx = 3.9
    d.text(s, "How It’s Realized", Inches(rx), Inches(0.5), Inches(9), Inches(0.5), size=21, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, Inches(rx), Inches(1.15), Inches(4.4), Inches(1.45), b.SOFT, radius=0.05, shadow=True)
    d.text(s, "CHALLENGE", Inches(rx+0.2), Inches(1.27), Inches(4), Inches(0.3), size=11, color=b.CORAL, bold=True)
    d.text(s, challenge, Inches(rx+0.2), Inches(1.6), Inches(4.0), Inches(0.92), size=11.3, color=b.INK, shrink=True)
    d.rect(s, Inches(rx+4.6), Inches(1.15), Inches(4.4), Inches(1.45), b.SOFT, radius=0.05, shadow=True)
    d.text(s, "SOLUTION", Inches(rx+4.8), Inches(1.27), Inches(4), Inches(0.3), size=11, color=b.DARK_TEAL, bold=True)
    d.text(s, solution, Inches(rx+4.8), Inches(1.6), Inches(4.0), Inches(0.92), size=11.3, color=b.INK, shrink=True)
    for i, (n, l) in enumerate(stats):
        x = rx + i*3.07
        d.rect(s, Inches(x), Inches(2.78), Inches(2.85), Inches(0.92), b.NAVY, radius=0.06)
        d.text(s, n, Inches(x+0.1), Inches(2.88), Inches(1.25), Inches(0.6), size=18, color=b.GOLD, bold=True,
               align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, l, Inches(x+1.35), Inches(2.96), Inches(1.4), Inches(0.55), size=10.5, color=b.WHITE, bold=True,
               anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.text(s, "HOW IT WORKS", Inches(rx), Inches(3.9), Inches(9), Inches(0.3), size=11, color=b.MUTED, bold=True)
    sx = rx; w = (9.0 - 0.22*(len(steps)-1)) / len(steps)
    for i, st in enumerate(steps):
        d.rect(s, Inches(sx), Inches(4.25), Inches(w), Inches(0.55), b.LIGHT_TEAL, radius=0.1)
        d.text(s, st, Inches(sx+0.03), Inches(4.37), Inches(w-0.06), Inches(0.34), size=9.5, color=b.DARK_TEAL,
               bold=True, align=PP_ALIGN.CENTER, shrink=True)
        if i < len(steps)-1:
            d.text(s, "→", Inches(sx+w-0.04), Inches(4.31), Inches(0.24), Inches(0.4), size=12, color=b.TEAL,
                   bold=True, align=PP_ALIGN.CENTER)
        sx += w + 0.22
    d.rect(s, Inches(rx), Inches(5.05), Inches(9.0), Inches(0.55), b.NAVY, radius=0.06)
    d.text(s, "STACK:  " + stack, Inches(rx+0.2), Inches(5.16), Inches(8.7), Inches(0.36), size=10.4,
           color=b.LIGHT_TEAL, bold=True, shrink=True)
    d.rect(s, Inches(rx), Inches(5.72), Inches(4.4), Inches(0.5), b.SOFT, radius=0.06)
    d.text(s, "SYSTEMS:  " + systems, Inches(rx+0.2), Inches(5.82), Inches(4.0), Inches(0.32), size=10,
           color=b.INK, bold=True, shrink=True)
    d.rect(s, Inches(rx+4.6), Inches(5.72), Inches(4.4), Inches(0.5), b.SOFT, radius=0.06)
    d.text(s, "USERS:  " + users, Inches(rx+4.8), Inches(5.82), Inches(4.0), Inches(0.32), size=10,
           color=b.INK, bold=True, shrink=True)

# ── the 8 use cases ─────────────────────────────────────────────────────────
PANELS = [b.TEAL, b.ACCENT, b.GOLD, b.NAVY_2, b.TEAL, b.ACCENT, b.GOLD, b.NAVY_2]
UCS = [
 dict(no=1, name="Lead Response\n& Nurture", short="Lead Response & Nurture", pilot=True,
   pattern="Conversational agent + structured CRM tool-calls (KG/MCP, not RAG)", roi="1–4mo", scope="1",
   challenge="Leads leak in the 24h after arrival; 48% of agents never follow up; the fastest agent wins, not the best.",
   solution="A conversational agent replies in <60s across text/email, qualifies, books, and runs the 8–12 touch nurture.",
   owner="Owner: broker / team lead. Guardrails: TCPA consent, Fair-Housing-safe language, human-in-loop on offers.",
   tagline="Always-on first responder that turns inbound leads into booked appointments while the team sells.",
   rchallenge="A Zillow lead lands at 9pm. The broker is at dinner. Three faster agents call back first.",
   rsolution="Replies <60s, qualifies on intent, books the showing/callback, and logs it to the CRM.",
   stats=[("<60s","response"),("24/7","coverage"),("8–12","nurture")],
   steps=["Lead in","Reply <60s","Qualify+book","CRM tool-call","Nurture"],
   stack="Hermes · Composio (SMS/Gmail/Calendar/CRM) · Agent Mail · Obsidian (voice) · GPT-5.5",
   systems="FUB/kvCORE · Zillow · Calendar", users="Broker · Agents · Leads",
   kpi=[("Median response","hours → <60s"),("<5-min contact rate","~20% → 90%+")],
   rai="TCPA consent · Fair-Housing language test · human-in-loop on offers"),
 dict(no=2, name="Transaction\nCoordination", short="Transaction Coordination", pilot=True,
   pattern="Document AI extraction + deterministic deadline rule engine", roi="2–6mo", scope="3",
   challenge="450–900 open tasks across 15–30 files; 34% of failures are lender-doc delays; 18% are date-calc errors. E&O exposure.",
   solution="Auto-open each file at contract, extract dates/parties, calculate deadlines, fire 3-tier alerts, escalate exceptions.",
   owner="Owner: transaction coordinator. Guardrails: human sign-off on filings; full E&O documentation trail.",
   tagline="Tracks every contract-relative deadline across every file so nothing slips and no client loses earnest money.",
   rchallenge="A lender-doc deadline slips while the TC is heads-down on three other files. Earnest money at risk.",
   rsolution="Extracts dates at contract, holds every deadline, alerts in 3 tiers, escalates only exceptions.",
   stats=[("0","silent misses"),("90–99%","extract recall"),("35–45","files / TC")],
   steps=["Contract in","Doc AI extract","Dates calc’d","3-tier alerts","Escalate"],
   stack="Document AI (GCP Doc AI / AWS Textract) · deadline rule engine · Composio (DocuSign/email) · GPT-5.5",
   systems="TX mgmt · DocuSign · Calendar", users="Coordinator · Agents · Clients",
   kpi=[("Silent missed deadlines","some → 0"),("Date-calc errors","18% → <1%")],
   rai="Human sign-off on filings · immutable audit log · E&O retention"),
 dict(no=3, name="Listing &\nMarketing Ops", short="Listing & Marketing Ops", pilot=True,
   pattern="Multi-agent orchestration (4 specialist agents)", roi="1–4mo", scope="1/2",
   challenge="The owner is the unpaid marketing director; social is ad-hoc; the CRM goes stale; the sphere isn’t nurtured.",
   solution="An orchestrator dispatches specialists: listing-copy, social scheduler, market-report, and sphere-nurture agents.",
   owner="Owner: broker / marketing lead. Guardrails: Fair-Housing copy filter, MLS rules, brand-voice review.",
   tagline="A team of specialist agents that markets every new listing within 24 hours and keeps the brand on.",
   rchallenge="A new listing goes live but copy, social, and a market report take days the broker doesn’t have.",
   rsolution="An orchestrator dispatches specialist agents — copy, social, report, sphere — on the brand voice.",
   stats=[("24h","to marketed"),("4","specialist agents"),("5/wk","posts")],
   steps=["Listing in","Orchestrate","Copy+social","Market report","Sphere"],
   stack="Orchestrator (ADK/LangGraph or Hermes sub-agents) · GPT-5.5 + image · Composio (social/MLS/email) · Obsidian",
   systems="MLS · Social · Email/CRM", users="Broker · Agents · Sphere",
   kpi=[("Listings marketed ≤24h","X% → 100%"),("Owner hours saved","8–10 / wk")],
   rai="Fair-Housing copy classifier · MLS-rule check · brand review"),
 dict(no=4, name="Agent Recruiting\n& Retention", short="Agent Recruiting & Retention", pilot=False,
   pattern="Conversational agent + ATS/CRM tool-calls + outreach (light RAG on value-prop)", roi="1–4mo", scope="1",
   challenge="A brokerage grows by recruiting — but the owner has no time to source, nurture, and onboard candidates. Recruiting is ad-hoc.",
   solution="A recruiting agent sources candidate signals, runs personalized outreach, books interviews, and drives onboarding checklists.",
   owner="Owner: broker. Guardrails: EEO-compliant outreach (no protected-class targeting), CAN-SPAM, platform ToS.",
   tagline="The brokerage growth engine — sources, nurtures, and onboards agents while the owner sells.",
   rchallenge="The owner wants to grow headcount but recruiting always loses to today’s deals.",
   rsolution="Sources candidates, personalizes outreach, books interviews, and runs the onboarding checklist.",
   stats=[("weekly","outreach"),("↑","interviews / mo"),("days→hrs","onboarding")],
   steps=["Source","Personalize","Outreach","Book interview","Onboard"],
   stack="Hermes · Composio (LinkedIn/email/calendar/ATS) · Agent Mail · Obsidian (recruiting pitch) · GPT-5.5",
   systems="ATS/CRM · LinkedIn · Calendar", users="Broker · Recruits · Ops",
   kpi=[("Interviews booked / mo","ad-hoc → steady"),("Onboarding time","days → hours")],
   rai="EEO-compliant targeting · CAN-SPAM · platform ToS · opt-out"),
 dict(no=5, name="CMA & Pricing\nIntelligence", short="CMA & Pricing Intelligence", pilot=False,
   pattern="Structured MLS-data tool-calls (KG/MCP, not RAG) + report generation", roi="1–4mo", scope="3",
   challenge="Producing CMAs and market reports for listing appointments is slow and manual; pricing is gut-feel.",
   solution="The agent pulls comps from MLS (structured), computes pricing ranges, and generates a branded CMA on demand.",
   owner="Owner: listing agent. Guardrails: pricing fairness, no steering, MLS data-licensing compliance.",
   tagline="On-demand, data-grounded CMAs that win the listing appointment — minutes, not hours.",
   rchallenge="A listing appointment is tomorrow; the CMA takes 2–3 hours of manual comp pulling.",
   rsolution="Queries MLS comps via structured tool-calls, computes a defensible range, and renders a branded CMA.",
   stats=[("<15min","CMA turnaround"),("93–97%","grounding acc."),("↑","win rate")],
   steps=["Address in","MLS tool-call","Comp analysis","Pricing range","Branded CMA"],
   stack="Hermes · Composio (MLS/BigQuery) · GPT-5.5 · Obsidian (pricing rules) · chart gen",
   systems="MLS · BigQuery · Slides", users="Listing agents · Sellers",
   kpi=[("CMA prep time","2–3h → <15min"),("Listing-appt win rate","+ lift")],
   rai="Pricing fairness · no steering · MLS data licensing"),
 dict(no=6, name="Database\nReactivation", short="Database Reactivation / ‘Likely to Move’", pilot=False,
   pattern="Propensity scoring over structured CRM (KG/MCP) + conversational outreach", roi="1–4mo", scope="1/2",
   challenge="70%+ of future business is in the database — but it sits cold. No one works past clients and sphere.",
   solution="The agent scores the database for ‘likely to move’ signals and runs personalized reactivation outreach.",
   owner="Owner: broker / agents. Guardrails: TCPA, honored opt-outs, Fair-Housing-safe messaging.",
   tagline="Mines the gold already in the CRM — surfacing listing conversations from people you already know.",
   rchallenge="The database has thousands of contacts and zero systematic follow-up.",
   rsolution="Scores contacts for move-propensity and runs tailored, opt-out-respecting reactivation.",
   stats=[("4–6","listing convos/mo"),("monthly","DB touch"),("↑","reactivation")],
   steps=["Enrich DB","Score propensity","Segment","Personalize","Outreach"],
   stack="Hermes · Composio (CRM/enrichment/email/SMS) · GPT-5.5 · Obsidian",
   systems="CRM · Enrichment · Email/SMS", users="Broker · Agents · Past clients",
   kpi=[("Extra listing convos / mo","0 → 4–6"),("Database touch rate","quarterly → monthly")],
   rai="TCPA · opt-out honoring · Fair-Housing messaging"),
 dict(no=7, name="Inbound Voice\n& Scheduling", short="Inbound Voice Receptionist & Scheduler", pilot=False,
   pattern="Voice/conversational agent + calendar & CRM tool-calls", roi="1–4mo", scope="1",
   challenge="Calls go to voicemail; showing requests and buyer/seller questions stall; after-hours calls are lost.",
   solution="A voice agent answers 24/7, qualifies, books showings, and routes urgent items to the right agent.",
   owner="Owner: broker / front desk. Guardrails: call-recording disclosure, TCPA, escalation paths.",
   tagline="A 24/7 voice receptionist that never sends a caller to voicemail and books the showing live.",
   rchallenge="A buyer calls about a listing at 7pm; it goes to voicemail and they call the next sign instead.",
   rsolution="Answers live, qualifies, books the showing on the right agent’s calendar, and logs the call.",
   stats=[("24/7","answered"),("~0%","missed-call rate"),("live","booking")],
   steps=["Call in","Answer live","Qualify","Book showing","Route/log"],
   stack="Hermes · voice (STT/TTS) · Composio (Calendar/CRM/telephony) · GPT-5.5",
   systems="Phone · Calendar · CRM", users="Callers · Agents · Front desk",
   kpi=[("Missed-call rate","X% → ~0"),("After-hours bookings","0 → captured")],
   rai="Call-recording disclosure · TCPA · escalation paths"),
 dict(no=8, name="Compliance\n& File Audit", short="Compliance & File Audit", pilot=False,
   pattern="Document AI extraction + deterministic compliance rules engine", roi="2–6mo", scope="3",
   challenge="The broker is liable for every file’s compliance; missing signatures/disclosures = E&O and license risk. Manual review doesn’t scale.",
   solution="Document AI reviews each file against a required-docs checklist and flags gaps before closing.",
   owner="Owner: broker / compliance. Guardrails: Fair-Housing disclosure checks, E&O documentation, retention.",
   tagline="A second set of eyes on every file — catching the missing disclosure before it becomes a claim.",
   rchallenge="A file closes missing a required disclosure; the gap surfaces only when a complaint arrives.",
   rsolution="Extracts and checks every required doc/signature against the rules, flagging gaps pre-close.",
   stats=[("100%","files audited"),("90–99%","catch recall"),("hrs→min","review")],
   steps=["File in","Doc AI extract","Rule check","Flag gaps","Broker review"],
   stack="Document AI (GCP/Textract) · compliance rules engine · Composio (TX mgmt/DocuSign) · GPT-5.5",
   systems="TX mgmt · DocuSign · Drive", users="Broker · Compliance · Agents",
   kpi=[("Compliance gaps caught pre-close","X → all"),("Broker review time","hours → minutes")],
   rai="Fair-Housing disclosure check · E&O documentation · retention"),
]
TOTAL_UC = len(UCS)

# ════════════════════════════════════════════════════════════════════════════
# FRONT MATTER
# ════════════════════════════════════════════════════════════════════════════
s = page(fill=b.NAVY, dark=True)
d.rect(s, Inches(11.6), 0, Inches(1.733), d.H, b.NAVY_2); d.rect(s, Inches(11.54), 0, Inches(0.06), d.H, b.TEAL)
d.text(s, "AI USE-CASE CATALOG", Inches(MF), Inches(1.3), Inches(9), Inches(0.4), size=15, color=b.TEAL, bold=True)
d.text(s, "8 AI Use Cases for the DFW\nBoutique Brokerage", Inches(MF), Inches(2.0), Inches(10.4), Inches(2.0),
       size=40, color=b.WHITE, bold=True, shrink=True)
d.rect(s, Inches(MF), Inches(4.25), Inches(1.6), Inches(0.05), b.TEAL)
d.text(s, "Eight detailed, pattern-selected agent use cases — KPI-baselined and mapped to 12 named prospects. "
          "Three run as the 90-day pilot.", Inches(MF), Inches(4.45), Inches(10.2), Inches(0.9), size=16,
       color=b.LIGHT_TEAL, shrink=True)
for i, chip in enumerate(["8 detailed use cases", "3 = the pilot", "Grounded on 12 prospects"]):
    d.rect(s, Inches(MF + i*3.3), Inches(5.7), Inches(3.0), Inches(0.6), b.NAVY_2, radius=0.3)
    d.text(s, chip, Inches(MF + i*3.3), Inches(5.83), Inches(3.0), Inches(0.36), size=12.5, color=b.TEAL,
           bold=True, align=PP_ALIGN.CENTER)
d.text(s, "Vertical: residential real estate (cross-industry) · DFW, TX", Inches(MF), Inches(6.65), Inches(10),
       Inches(0.4), size=12, color=b.MUTED)

# Exec summary
s = page()
H(s, "Eight Use Cases, Four Patterns, Three In The Pilot", "Executive summary")
d.rect(s, Inches(MF), Inches(1.75), Inches(CWF), Inches(0.85), b.NAVY, radius=0.04)
d.text(s, "BLUF: This is the full agent opportunity for a boutique brokerage — eight detailed use cases across "
          "lead, transaction, marketing, recruiting, pricing, database, voice, and compliance. We pilot exactly "
          "three in 90 days (each KPI-gated), then expand down the roadmap.", Inches(MF+0.3), Inches(1.88),
       Inches(CWF-0.6), Inches(0.65), size=13, color=b.WHITE, bold=True, shrink=True)
cols = [
    ("THE CATALOG", "8 use cases spanning all four realization patterns — conversational tool-calling, Document "
     "AI, multi-agent orchestration, and structured-data grounding.", b.TEAL),
    ("THE PILOT (3)", "Lead Response, Transaction Coordination, Listing/Marketing Ops — the highest-frequency, "
     "fastest-ROI trio, each with a before/after KPI.", b.ACCENT),
    ("THE ROADMAP (5)", "Recruiting, CMA/Pricing, Database Reactivation, Voice Receptionist, Compliance Audit — "
     "sequenced after the pilot clears its gates.", b.GOLD),
]
cw = (CWF - 0.6) / 3
for i, (h, body, ac) in enumerate(cols):
    x = MF + i*(cw+0.3)
    d.rect(s, Inches(x), Inches(2.8), Inches(cw), Inches(2.55), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, Inches(x), Inches(2.8), Inches(cw), Inches(0.5), ac, radius=0.05)
    d.text(s, h, Inches(x), Inches(2.9), Inches(cw), Inches(0.34), size=12.5, color=b.NAVY if ac == b.GOLD else b.WHITE,
           bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, body, Inches(x+0.25), Inches(3.5), Inches(cw-0.5), Inches(1.75), size=12, color=b.INK, shrink=True)
takeaway(s, "THE ASK", "Start the pilot with UC1 on one prospect’s live lead flow; expand by KPI gate through the "
         "eight-use-case roadmap.", y=5.6, h=0.85, fill=b.GOLD, accent=b.NAVY, tcol=b.NAVY)

# Agenda
s = page()
H(s, "How This Deck Is Organized", "Agenda")
cards_grid(s, [
    ("01  The Opportunity", "The DFW boutique vertical and what the 12 prospects signal"),
    ("02  Catalog & Patterns", "All 8 use cases at a glance + pattern-selection logic"),
    ("03  The 8 Use Cases", "Detailed card + realization for each — pilot and roadmap"),
    ("04  Architecture & Patterns", "The managed stack, hyperscaler options, defense-in-depth"),
    ("05  Governance & Activation", "Responsible AI, KPI matrix, 90-day plan, prospect mapping"),
    ("Appendix", "Consolidated KPI baseline + RAI/scope matrices"),
], cols=2, y0=1.95, ch=0.95)

# ════════════════════════════════════════════════════════════════════════════
# SECTION 01 — OPPORTUNITY
# ════════════════════════════════════════════════════════════════════════════
divider("01", "The Opportunity", "The DFW boutique vertical — grounded on 12 named prospects.")

s = page()
H(s, "The Vertical: Under-Served, People-Heavy, AI-Curious", "Where we play")
kpi_grid(s, [
    ("12", "named prospects", "scored & mapped in the worksheet"),
    ("5–40", "agents each", "the sweet-spot boutique band"),
    ("8", "agent use cases", "the full opportunity surface"),
    ("$92B+", "back-office market", "the spend AI redirects, SMB-fastest"),
])
takeaway(s, "Why now", "Falling model costs make a managed ‘digital employee’ viable for a sub-50-agent brokerage "
         "for the first time — and national BPOs won’t serve them. The opportunity is structural.")

s = page()
H(s, "What The 12 Prospects Signal", "Grounded on the prospect worksheet")
rows = []
for r in prospects[:6]:
    name, seg, signal, fit = r[0], r[3], r[4], r[6]
    ac = b.TEAL if int(fit) >= 88 else (b.AMBER if int(fit) >= 80 else b.CORAL)
    rows.append((name, fit, seg.split(" - ")[-1], (signal[:48] + "…") if len(signal) > 48 else signal, ac))
scorecard(s, ["Brokerage", "Fit", "Segment", "Signal that points to a use case"], [3.0, 1.0, 3.0, 5.13], rows, y=1.82, rh=0.48)
takeaway(s, "The read", "Tech-forward boutiques lead with Lead Response & Marketing; shops advertising a TC "
         "bottleneck lead with Transaction Coordination; design-led shops with Marketing Ops. The signal picks the "
         "use case — and the entry point.", y=5.75, h=1.05)

s = page()
H(s, "We Catalog Eight — But Pilot Only Three", "The pilot discipline")
cards_grid(s, [
    ("Catalog all 8", "Map the full agent opportunity so the brokerage sees the destination, not just step one."),
    ("Pilot max 3 / 90 days", "More than three at once is the #1 pilot-failure pattern. Focus beats breadth."),
    ("Before/after KPI each", "Every use case has a baseline captured in week one (e.g. response: 6h → <60s)."),
    ("Expand by KPI gate", "Each pilot use case must beat its gate before the next roadmap use case turns on."),
], cols=2, idx=True)
takeaway(s, "Evidence", "McKinsey 2025: <10% of gen-AI use cases pass pilot — the gap is missing value criteria "
         "and vertical specificity. The catalog sets the vision; the 3-use-case gate closes the value gap.")

# ════════════════════════════════════════════════════════════════════════════
# SECTION 02 — CATALOG & PATTERNS
# ════════════════════════════════════════════════════════════════════════════
divider("02", "The Catalog & The Patterns", "All eight use cases — and why each pattern was chosen.")

s = page()
H(s, "The Full Catalog At A Glance", "Eight use cases, four patterns")
rows = []
for uc in UCS:
    ac = b.TEAL if uc["pilot"] else b.AMBER
    tag = "PILOT" if uc["pilot"] else "Roadmap"
    rows.append((f"UC{uc['no']} {uc['short']}", uc["pattern"].split(" (")[0], uc["roi"], uc["scope"], tag, ac))
scorecard(s, ["Use case", "Realization pattern", "ROI", "Scope", "Phase"],
          [3.5, 4.6, 1.0, 1.0, 2.03], rows, y=1.68, rh=0.5, hh=0.46, fs=10.2)
d.text(s, "All four realization patterns are represented; pattern follows data shape, not hype.", Inches(MF),
       Inches(6.66), Inches(CWF), Inches(0.34), size=12, color=b.DARK_TEAL, bold=True, shrink=True)

s = page()
H(s, "Why These Patterns — Not Just ‘RAG Everything’", "Realization-pattern selection")
scorecard(s, ["If the work is…", "Use", "Not", "Because"], [3.3, 2.7, 1.7, 4.43], [
    ("Querying structured CRM/MLS data", "Knowledge-Graph / MCP tool-calls", "RAG", "RAG can’t answer ‘which fields exist’; tool-calls hit 93–97% vs ~60%", b.TEAL),
    ("Extracting dates/parties from contracts", "Document AI", "Prompted LLM", "90–99% recall vs 70–85%; 10–50× cheaper per page", b.TEAL),
    ("A workflow with 3+ decision points", "Multi-agent orchestration", "Single prompt", "Clean tool boundaries, distributed context, isolated failures", b.TEAL),
    ("Answering over brand/FAQ docs", "RAG (narrow)", "Fine-tune", "Unstructured text is RAG’s job — used sparingly here", b.AMBER),
], y=1.9, rh=0.78, hh=0.5, fs=10.4)
takeaway(s, "The discipline", "Most brokerage value is structured (CRM, MLS, contracts) — so most of this catalog is "
         "tool-calling + Document AI, with RAG used only where it actually fits.", y=5.95, h=1.0)

# ════════════════════════════════════════════════════════════════════════════
# SECTION 03 — THE 8 USE CASES (card + realization each)
# ════════════════════════════════════════════════════════════════════════════
divider("03", "The Eight Use Cases", "Detailed card + realization for each — pilot (1–3) and roadmap (4–8).")

for uc in UCS:
    # detail card slide
    s = page()
    badge = "PILOT · 90-DAY" if uc["pilot"] else "ROADMAP"
    H(s, f"UC{uc['no']} — {uc['short']}", f"{badge}  ·  Pattern: {uc['pattern']}")
    cards_grid(s, [
        ("Challenge", uc["challenge"]),
        ("Solution", uc["solution"]),
        ("Realization pattern", uc["pattern"] + "."),
        ("Owner & guardrails", uc["owner"]),
    ], cols=2, idx=True)
    takeaway(s, "ROI & scope", f"ROI timeline: {uc['roi']}.  AWS Gen-AI scope: {uc['scope']}.  "
             f"KPI gate: {uc['kpi'][0][0]} ({uc['kpi'][0][1]}).")
    # realization slide
    s = page()
    realization(s, uc["no"], TOTAL_UC, uc["name"], uc["tagline"], uc["rchallenge"], uc["rsolution"],
                uc["stats"], uc["steps"], uc["stack"], uc["systems"], uc["users"],
                PANELS[uc["no"]-1], uc["pilot"])

# Consolidated KPI matrix
s = page()
H(s, "Consolidated KPI Baseline Worksheet", "Measure all eight before/after")
rows = []
for uc in UCS:
    ac = b.TEAL if uc["pilot"] else b.AMBER
    k1, k2 = uc["kpi"][0], uc["kpi"][1]
    rows.append((f"UC{uc['no']} {uc['short']}", f"{k1[0]}: {k1[1]}", f"{k2[0]}: {k2[1]}", ac))
scorecard(s, ["Use case", "Primary KPI (before → after)", "Secondary KPI (before → after)"],
          [3.3, 4.4, 4.43], rows, y=1.68, rh=0.5, hh=0.46, fs=10.0)
d.text(s, "Rule: no use case turns on without its baseline captured in week one — the before/after is the go/no-go evidence.",
       Inches(MF), Inches(6.66), Inches(CWF), Inches(0.34), size=12, color=b.DARK_TEAL, bold=True, shrink=True)

# Consolidated RAI / scope matrix
s = page()
H(s, "Consolidated Scope & Responsible-AI Matrix", "Governance per use case")
rows = []
for uc in UCS:
    ac = b.TEAL if uc["pilot"] else b.AMBER
    rows.append((f"UC{uc['no']} {uc['short']}", uc["scope"], uc["rai"], ac))
scorecard(s, ["Use case", "Scope", "Key Responsible-AI controls"], [3.3, 1.2, 7.63], rows, y=1.68, rh=0.5, hh=0.46, fs=10.0)
d.text(s, "Scope per AWS Gen-AI Security Scoping Matrix: Scope 1 → guardrails + DLP + consent; Scope 3 → isolation + audit log.",
       Inches(MF), Inches(6.66), Inches(CWF), Inches(0.34), size=12, color=b.DARK_TEAL, bold=True, shrink=True)

# ════════════════════════════════════════════════════════════════════════════
# SECTION 04 — ARCHITECTURE & PATTERNS
# ════════════════════════════════════════════════════════════════════════════
divider("04", "Architecture & Patterns", "One managed stack runs all eight; cloud options where wanted.")

s = page()
H(s, "One Managed Stack Runs Every Agent", "Delivery architecture")
cards_grid(s, [
    ("Harness", "Hermes (model-agnostic, self-evolving) per agent, on an isolated Orgo cloud VM per client."),
    ("Tools & auth", "Composio brokers 1,000s of apps with managed auth — no shared credentials on your machine."),
    ("Context", "Obsidian vault holds brand voice + rules; structured CRM/MLS accessed via tool-calls, not RAG."),
    ("Reliability", "Watchdog auto-restart + failure alerts to us; per-client sandbox, deletable in <1s."),
], cols=2)
takeaway(s, "Why this stack", "Fully managed — the broker approves outcomes and never monitors, updates, or "
         "debugs an agent. The same stack scales from one use case to all eight.")

s = page()
H(s, "If A Cloud-Native Build Is Preferred", "Hyperscaler options (real estate = cross-industry)")
scorecard(s, ["Capability", "GCP", "AWS", "Azure"], [3.6, 2.9, 2.9, 2.73], [
    ("Document AI (UC2/UC8)", "Document AI", "Textract", "Doc Intelligence", b.TEAL),
    ("Structured CRM/MLS grounding (UC1/5/6)", "Native MCP server", "Lambda + Glue", "Purview (preview)", b.TEAL),
    ("Unstructured listing/FAQ search", "Vertex AI Search", "Kendra/Bedrock KB", "Azure AI Search", b.TEAL),
    ("Office/Teams integration", "—", "—", "Copilot Studio", b.AMBER),
], y=1.9, rh=0.78, hh=0.5, fs=10.6)
takeaway(s, "Recommendation", "No heavy regulatory driver in real estate, so choose on footprint: GCP if Document "
         "AI + native CRM/MLS-grounding MCP matter most; AWS on data maturity; Azure only if the brokerage lives in "
         "Microsoft 365. Default: stay on the managed micro-agency stack.", y=5.95, h=1.05)

s = page()
H(s, "Defense-In-Depth Around Every Agent", "Security architecture")
cards_grid(s, [
    ("Input", "Prompt-injection detection, PII scrub, TCPA-consent check before any outbound message."),
    ("Model", "System-prompt hardening, per-client context isolation, model-agnostic routing."),
    ("Output", "Fair-Housing + grounding checks, hallucination scoring, content classification before send."),
    ("Observability", "Mandatory audit log: session ID, role, model version, input/output hash, latency, RAI flags."),
], cols=2, idx=True)

# ════════════════════════════════════════════════════════════════════════════
# SECTION 05 — GOVERNANCE & ACTIVATION
# ════════════════════════════════════════════════════════════════════════════
divider("05", "Governance & Activation", "Responsible AI, the 90-day plan, and who to start with.")

s = page()
H(s, "Responsible AI Is Built In — Not Bolted On", "Identify → Measure → Mitigate → Operate")
cards_grid(s, [
    ("Identify", "Map risks per use case: TCPA consent, Fair-Housing language, contract/PII sensitivity, MLS & EEO rules."),
    ("Measure", "Test-set checks at build time — discriminatory-language classifier, extraction recall, pricing fairness."),
    ("Mitigate", "Blocked-term filters, human-in-the-loop on offers/filings, brand & compliance review on outputs."),
    ("Operate", "Immutable audit log on every action; weekly RAI flag review; retention for E&O defense."),
], cols=2, idx=True)
takeaway(s, "Standard", "Maps to NIST AI RMF (Map→Measure→Manage→Govern) and the Microsoft Responsible AI Standard — "
         "RAI sits at the Measure stage, before production, not as a post-hoc audit.")

s = page()
H(s, "The 90-Day Pilot Plan, With KPI Gates", "Activation — 3 of 8")
scorecard(s, ["Phase", "What ships", "KPI gate to advance"], [2.2, 5.6, 4.33], [
    ("Days 0–2", "UC1 Lead Response live on one prospect; baseline captured", "First lead answered <60s", b.TEAL),
    ("Days 1–30", "UC1 nurture running; weekly Loom updates", "Response time + <5-min rate beaten", b.TEAL),
    ("Days 31–60", "UC2 Transaction Coordination added", "Zero silent misses on live files", b.TEAL),
    ("Days 61–90", "UC3 Marketing Ops added; go/no-go on roadmap", "Listings ≤24h + hours saved shown", b.GOLD),
], y=1.9, rh=0.78, hh=0.5)
takeaway(s, "Then the roadmap", "After the pilot clears its gates, sequence UC4–UC8 (recruiting, CMA, database, "
         "voice, compliance) by the brokerage’s biggest remaining bottleneck.", y=5.95, h=0.95)

s = page()
H(s, "Who To Start With — Grounded On The Worksheet", "Prospect → use-case mapping")
scorecard(s, ["Prospect", "Fit", "Lead use case", "Why (from their signal)"], [3.0, 1.0, 3.0, 5.13], [
    ("Momentus Real Estate", "92", "UC1 Lead Response", "Tech-forward, ‘intelligence layer’, growth mode", b.TEAL),
    ("Fort Worth Focused", "88", "UC2 / UC3", "Has a Director of Ops — admin overload signal", b.TEAL),
    ("Arbrook Realty", "86", "UC2 Transaction Coord.", "Advertises a TC bottleneck explicitly", b.TEAL),
    ("Nitra Realty", "80", "UC1 / UC6", "Relocation niche = high follow-up + DB value", b.AMBER),
    ("MOXY Real Estate+Design", "78", "UC3 Marketing Ops", "Design/brand identity — marketing-led fit", b.AMBER),
], y=1.9, rh=0.62, hh=0.5)
takeaway(s, "Sequencing", "Start with Momentus on UC1 (warmest + cleanest fit), prove it, then expand across use "
         "cases and down the fit-ranked prospect list.", y=5.9, h=0.9)

s = page()
H(s, "Expected Return", "The business case")
kpi_grid(s, [
    ("1–4 mo", "to first value", "UC1, UC3–7 (consumer-facing)"),
    ("2–6 mo", "to doc-AI value", "UC2 & UC8 (back-office)"),
    ("1 deal", "to break even", "per quarter covers the engagement"),
    ("8", "use-case roadmap", "compounding value per brokerage"),
])
takeaway(s, "The asymmetry", "Eight measured use cases on one managed stack; a single saved deal per quarter pays "
         "for the engagement — and the owner gets the hours back to grow the brokerage.")

# Close
s = page(fill=b.NAVY, dark=True)
d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
d.text(s, "THE NEXT STEP", Inches(MF), Inches(1.3), Inches(8), Inches(0.4), size=15, color=b.TEAL, bold=True)
d.text(s, "Catalog set. Pilot three.", Inches(MF), Inches(1.95), Inches(11), Inches(1.0), size=40, color=b.WHITE,
       bold=True, shrink=True)
d.rect(s, Inches(MF), Inches(3.1), Inches(1.6), Inches(0.05), b.TEAL)
d.text(s, "Start UC1 on one prospect’s live lead flow in 48 hours, beat the baseline, then expand through the "
          "eight-use-case roadmap by KPI gate.", Inches(MF), Inches(3.3), Inches(10.5), Inches(0.8), size=16,
       color=b.LIGHT_TEAL, shrink=True)
steps = [("1", "Choose prospect", "Momentus is warmest (fit 92)"),
         ("2", "Pilot 3 in 90 days", "Lead · Transaction · Marketing"),
         ("3", "Expand the catalog", "UC4–UC8 by KPI gate")]
cw = (CWF - 0.8) / 3
for i, (n, h, body) in enumerate(steps):
    x = MF + i*(cw+0.4)
    d.rect(s, Inches(x), Inches(4.35), Inches(cw), Inches(1.7), b.NAVY_2, radius=0.06)
    d.rect(s, Inches(x), Inches(4.35), Inches(cw), Inches(0.5), b.TEAL, radius=0.06)
    d.text(s, f"STEP {n}", Inches(x), Inches(4.45), Inches(cw), Inches(0.32), size=12, color=b.NAVY, bold=True,
           align=PP_ALIGN.CENTER)
    d.text(s, h, Inches(x+0.2), Inches(4.95), Inches(cw-0.4), Inches(0.45), size=15, color=b.WHITE, bold=True, shrink=True)
    d.text(s, body, Inches(x+0.2), Inches(5.4), Inches(cw-0.4), Inches(0.6), size=12, color=b.LIGHT_TEAL, shrink=True)
d.text(s, "Contact: shekerkamma@gmail.com", Inches(MF), Inches(6.45), Inches(10), Inches(0.4), size=13,
       color=b.GOLD, bold=True)

TOTAL = len(_pages)
for i, (s, dark) in enumerate(_pages, start=1):
    d.footer(s, i, TOTAL, dark=dark)
d.save(OUT)
print("SLIDES:", d.n)
