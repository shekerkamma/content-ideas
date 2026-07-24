#!/usr/bin/env python3
"""Comprehensive (50+ slide) client-facing deck for Momentus Real Estate Group.
Content validated against this session's scorecard / GTM brief / audience research.
Mechanics live in pptxkit; content lives here. Footers are deferred so page totals
are always correct regardless of slide count."""
import sys
sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, Inches, Pt, PP_ALIGN, MSO_ANCHOR

DOCS = "/home/shekerk/content-ideas/docs/solo-agent-agency"
ARCH_PNG = f"{DOCS}/solo-agent-agency-architecture.png"
OUT = f"{DOCS}/Momentus-AI-Digital-Employee-Proposal-draft.pptx"

d = Deck(footer="Prepared for Momentus Real Estate Group · Confidential | 2026")
b = d.b
MF, CWF = 0.6, 12.133

# ── footer-deferral registry ────────────────────────────────────────────────
_pages = []          # list of (slide, dark)
def page(fill=b.WHITE, dark=False):
    s = d.slide(fill=fill)
    _pages.append((s, dark))
    return s

# ── reusable helpers ────────────────────────────────────────────────────────
def H(s, title, sub=None):
    d.header(s, title, sub)

def card(s, x, y, w, h, title, body, *, accent=None, idx=None, fill=None, tcol=None):
    accent = accent or b.TEAL
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(h), fill or b.SOFT, radius=0.06, shadow=True)
    d.rect(s, Inches(x), Inches(y), Inches(0.08), Inches(h), accent)
    if idx is not None:
        d.rect(s, Inches(x+0.22), Inches(y+0.22), Inches(0.42), Inches(0.42), b.NAVY, radius=0.2)
        d.text(s, str(idx), Inches(x+0.22), Inches(y+0.27), Inches(0.42), Inches(0.34),
               size=15, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        tx = x + 0.8
    else:
        tx = x + 0.28
    d.text(s, title, Inches(tx), Inches(y+0.22), Inches(w-(tx-x)-0.2), Inches(0.45),
           size=14.5, color=tcol or b.NAVY, bold=True, shrink=True)
    if body:
        d.text(s, body, Inches(x+0.28), Inches(y+0.78), Inches(w-0.5), Inches(h-0.95),
               size=11.5, color=b.INK, shrink=True)

def divider(num, title, sub):
    s = page(fill=b.NAVY, dark=True)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.text(s, f"SECTION {num}", Inches(MF), Inches(2.6), Inches(6), Inches(0.4),
           size=15, color=b.TEAL, bold=True)
    d.text(s, title, Inches(MF), Inches(3.1), Inches(11.2), Inches(1.2),
           size=40, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(MF), Inches(4.4), Inches(1.6), Inches(0.05), b.TEAL)
    d.text(s, sub, Inches(MF), Inches(4.6), Inches(10.8), Inches(0.7),
           size=15, color=b.LIGHT_TEAL, shrink=True)
    return s

def kpi_grid(s, kpis, y=1.95, h=2.55):
    n = len(kpis); gap = 0.3
    cw = (CWF - gap*(n-1)) / n
    for i, (num, lab, note) in enumerate(kpis):
        x = MF + i*(cw+gap)
        d.rect(s, Inches(x), Inches(y), Inches(cw), Inches(h), b.NAVY, radius=0.05, shadow=True)
        d.text(s, num, Inches(x+0.1), Inches(y+0.28), Inches(cw-0.2), Inches(0.85), size=32,
               color=b.GOLD, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, lab, Inches(x+0.12), Inches(y+1.18), Inches(cw-0.24), Inches(0.55), size=12.5,
               color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, note, Inches(x+0.18), Inches(y+1.75), Inches(cw-0.36), Inches(h-1.85), size=10.5,
               color=b.LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)

def takeaway(s, label, txt, y=5.6, h=0.95, fill=None, accent=None):
    d.rect(s, Inches(MF), Inches(y), Inches(CWF), Inches(h), fill or b.LIGHT_TEAL, radius=0.04)
    d.rect(s, Inches(MF), Inches(y), Inches(0.08), Inches(h), accent or b.TEAL)
    d.text(s, label, Inches(MF+0.3), Inches(y+0.15), Inches(5), Inches(0.32), size=12,
           color=b.DARK_TEAL, bold=True)
    d.text(s, txt, Inches(MF+0.3), Inches(y+0.5), Inches(CWF-0.6), Inches(h-0.6), size=13,
           color=b.INK, shrink=True)

def bullets(s, items, x=MF, y=1.95, w=CWF, size=14, space=12):
    d.text(s, [{"text": t, "bullet": True, "space_before": space, "size": size} for t in items],
           Inches(x), Inches(y), Inches(w), Inches(d.H.inches-y-0.7), shrink=True)

def quotes_grid(s, quotes, y=1.9):
    cw = (CWF - 0.6) / 3
    for i, (q, src) in enumerate(quotes):
        x = MF + (i % 3)*(cw+0.3); yy = y + (i // 3)*1.95
        d.rect(s, Inches(x), Inches(yy), Inches(cw), Inches(1.75), b.SOFT, radius=0.05, shadow=True)
        d.rect(s, Inches(x), Inches(yy), Inches(0.08), Inches(1.75), b.TEAL)
        d.text(s, f"“{q}”", Inches(x+0.25), Inches(yy+0.2), Inches(cw-0.45), Inches(1.1),
               size=11.5, color=b.INK, italic=True, shrink=True)
        d.text(s, f"— {src}", Inches(x+0.25), Inches(yy+1.38), Inches(cw-0.45), Inches(0.3),
               size=10, color=b.MUTED, bold=True, shrink=True)

def scorecard(s, heads, widths, rows, y=1.9, rh=0.84):
    xs = [MF]
    for w in widths[:-1]:
        xs.append(xs[-1] + w)
    d.rect(s, Inches(MF), Inches(y), Inches(CWF), Inches(0.5), b.NAVY)
    for hx_, hw, ht in zip(xs, widths, heads):
        d.text(s, ht, Inches(hx_+0.12), Inches(y+0.1), Inches(hw-0.2), Inches(0.32),
               size=12, color=b.WHITE, bold=True, shrink=True)
    ry = y + 0.5
    for row in rows:
        ac = row[-1]; cells = row[:-1]
        d.rect(s, Inches(MF), Inches(ry), Inches(CWF), Inches(rh), b.SOFT)
        d.rect(s, Inches(MF), Inches(ry), Inches(0.07), Inches(rh), ac)
        for cx, cw, val, i in zip(xs, widths, cells, range(len(cells))):
            d.text(s, val, Inches(cx+0.12), Inches(ry+0.14), Inches(cw-0.2), Inches(rh-0.24),
                   size=11, color=b.NAVY if i == 0 else b.INK, bold=(i == 0),
                   italic=(i == len(cells)-1), shrink=True, anchor=MSO_ANCHOR.MIDDLE)
        ry += rh + 0.04
    return ry

def cards_grid(s, items, *, cols=2, y0=1.95, ch=1.8, idx=False):
    cw = (CWF - 0.3*(cols-1)) / cols
    for i, (h, body) in enumerate(items):
        x = MF + (i % cols)*(cw+0.3); y = y0 + (i // cols)*(ch+0.25)
        card(s, x, y, cw, ch, h, body, idx=(i+1) if idx else None,
             accent=b.TEAL if i % 2 == 0 else b.ACCENT)

def two_panel(s, left, right, y=1.9, h=3.9):
    lw = 5.8; rw = CWF - lw - 0.35
    return (MF, lw, MF+lw+0.35, rw, y, h)

# ════════════════════════════════════════════════════════════════════════════
# FRONT MATTER
# ════════════════════════════════════════════════════════════════════════════
# 1 COVER
s = page(fill=b.NAVY, dark=True)
d.rect(s, Inches(11.6), 0, Inches(1.733), d.H, b.NAVY_2)
d.rect(s, Inches(11.54), 0, Inches(0.06), d.H, b.TEAL)
d.text(s, "PROPOSAL · DONE-FOR-YOU AI", Inches(MF), Inches(1.3), Inches(9), Inches(0.4),
       size=15, color=b.TEAL, bold=True)
d.text(s, "An AI Digital Employee\nfor Momentus Real Estate Group", Inches(MF), Inches(2.0),
       Inches(10.4), Inches(2.0), size=40, color=b.WHITE, bold=True, shrink=True)
d.rect(s, Inches(MF), Inches(4.25), Inches(1.6), Inches(0.05), b.TEAL)
d.text(s, "Answer every lead in under 60 seconds. Never miss a transaction deadline. You manage nothing.",
       Inches(MF), Inches(4.45), Inches(10.2), Inches(0.8), size=16, color=b.LIGHT_TEAL, shrink=True)
for i, chip in enumerate(["Live in 48 hours", "$5K / month, flat", "Fully managed"]):
    d.rect(s, Inches(MF + i*3.3), Inches(5.6), Inches(3.0), Inches(0.6), b.NAVY_2, radius=0.3)
    d.text(s, chip, Inches(MF + i*3.3), Inches(5.73), Inches(3.0), Inches(0.36),
           size=13, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "Prepared for Maureen Cappallo, Broker/Founder · Grapevine, DFW", Inches(MF),
       Inches(6.6), Inches(10), Inches(0.4), size=12, color=b.MUTED)

# 2 AGENDA
s = page()
H(s, "What’s Inside", "A complete proposal — problem, solution, proof, and the path to yes")
agenda = [
    ("01  The Situation", "Where boutique brokerages lose deals today"),
    ("02  The Cost", "What the status quo actually costs you"),
    ("03  Why The Usual Fixes Fail", "ISAs, CRMs, VAs, and DIY AI"),
    ("04  The Solution", "A managed digital employee, three jobs done"),
    ("05  Architecture & How It Works", "What runs under the hood — you touch none of it"),
    ("06  Reliability, Security & Trust", "The moat: fixed before anyone notices"),
    ("07  Engagement & Onboarding", "Live in 48 hours; 30/60/90 plan"),
    ("08  Proof & Differentiation", "It already runs; why us"),
    ("09  Commercials", "Pricing, ROI, and the pilot"),
    ("10  Fit & The Ask", "Why Momentus, and the next step"),
]
cw = (CWF - 0.3) / 2
for i, (h, sub) in enumerate(agenda):
    x = MF + (i % 2)*(cw+0.3); y = 1.85 + (i // 2)*1.02
    d.rect(s, Inches(x), Inches(y), Inches(cw), Inches(0.9), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, Inches(x), Inches(y), Inches(0.08), Inches(0.9), b.TEAL)
    d.text(s, h, Inches(x+0.25), Inches(y+0.13), Inches(cw-0.4), Inches(0.36), size=14,
           color=b.NAVY, bold=True, shrink=True)
    d.text(s, sub, Inches(x+0.25), Inches(y+0.5), Inches(cw-0.4), Inches(0.32), size=11.5,
           color=b.MUTED, shrink=True)

# 3 EXECUTIVE SUMMARY
s = page()
H(s, "The Leads You Already Pay For Are Leaking — We Stop The Leak", "Executive summary")
d.rect(s, Inches(MF), Inches(1.75), Inches(CWF), Inches(0.8), b.NAVY, radius=0.04)
d.text(s, "BLUF: A managed AI “digital employee” responds to every lead in <60s and tracks every "
          "deadline — reclaiming Maureen’s capacity to recruit and sell, for less than half the cost of one ISA.",
       Inches(MF+0.3), Inches(1.9), Inches(CWF-0.6), Inches(0.55), size=14.5, color=b.WHITE, bold=True, shrink=True)
cols = [
    ("SITUATION", "Boutique brokerages lose deals in the 24h after a lead arrives — not from bad leads, "
     "from slow follow-up. 48% of agents never follow up at all.", b.CORAL),
    ("INSIGHT", "ISAs cost $65–120K, turn over every 8–24 months, and only pencil above ~350 leads/mo. "
     "CRMs go unused. DIY AI just moves the work to ‘managing the bot’.", b.AMBER),
    ("RECOMMENDATION", "Install a fully-managed digital employee — lead follow-up + transaction "
     "coordination + listing ops. Live in 48h. You approve outcomes; we run it.", b.TEAL),
]
cw = (CWF - 0.6) / 3
for i, (h, body, ac) in enumerate(cols):
    x = MF + i*(cw+0.3)
    d.rect(s, Inches(x), Inches(2.75), Inches(cw), Inches(2.7), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, Inches(x), Inches(2.75), Inches(cw), Inches(0.5), ac, radius=0.05)
    d.text(s, h, Inches(x), Inches(2.85), Inches(cw), Inches(0.34), size=13.5, color=b.WHITE,
           bold=True, align=PP_ALIGN.CENTER)
    d.text(s, body, Inches(x+0.25), Inches(3.45), Inches(cw-0.5), Inches(1.85), size=12.5,
           color=b.INK, shrink=True)
d.rect(s, Inches(MF), Inches(5.7), Inches(CWF), Inches(0.85), b.GOLD, radius=0.04)
d.text(s, "THE ASK:  A 2-week paid pilot — one live agent, one workflow, measured against your current "
          "follow-up. Decide on the proof, not the promise.", Inches(MF+0.3), Inches(5.92),
       Inches(CWF-0.6), Inches(0.5), size=14, color=b.NAVY, bold=True, shrink=True)

# ════════════════════════════════════════════════════════════════════════════
# SECTION 01 — THE SITUATION
# ════════════════════════════════════════════════════════════════════════════
divider("01", "The Situation", "Where DFW boutique brokerages lose deals right now.")

# Market context
s = page()
H(s, "Boutique Brokerages Are Caught Between Growth And Capacity", "Market context")
cards_grid(s, [
    ("The market is huge and underserved", "BPO/back-office is a $92B+ market; 52% of real-estate teams "
     "now use a virtual assistant. Demand for ‘someone to handle the ops’ is mainstream — supply is broken."),
    ("Enterprise help skips the small shop", "National BPOs (Accenture, Teleperformance) won’t economically "
     "serve a sub-50-agent brokerage. The boutique is structurally abandoned."),
    ("AI made serving SMBs viable", "Falling model costs put a ‘digital employee’ within reach of a "
     "boutique for the first time — the economics finally work for both sides."),
    ("But the broker is the constraint", "Growth adds admin, follow-up, and tools faster than hours in the "
     "day. Capacity — not leads — is what caps a boutique’s growth."),
], cols=2)

# Silent killer
s = page()
H(s, "The Problem Isn’t Lead-Gen — It’s The 24 Hours After A Lead Arrives", "The silent killer")
card(s, MF, 1.85, 3.78, 3.0, "No instant response",
     "Leads arrive while you’re showing homes or at a closing. By the time you circle back, they’ve "
     "already talked to a faster agent.", idx=1)
card(s, MF+3.98, 1.85, 3.78, 3.0, "No follow-up system",
     "80% of deals need 5+ touches; 48% of agents never follow up once. Attempts 5–12 are where deals close.",
     idx=2, accent=b.AMBER)
card(s, MF+7.96, 1.85, 3.77, 3.0, "No single source of truth",
     "Leads scattered across Zillow, IG, forms, email. The hand-raisers get the same (no) attention as "
     "the tire-kickers.", idx=3, accent=b.CORAL)
takeaway(s, "What brokers actually say",
         "“Leads are coming in… but deals are still falling through. Not because of bad leads — because of "
         "follow-up.”  — BiggerPockets, May 2026", y=5.15, h=1.2, fill=b.NAVY, accent=b.TEAL)
# recolor takeaway text to light on navy
d.text(s, "“Leads are coming in… but deals are still falling through — because of follow-up.”  "
          "— BiggerPockets, 2026", Inches(MF+0.3), Inches(5.65), Inches(CWF-0.6), Inches(0.6),
       size=13, color=b.LIGHT_TEAL, italic=True, shrink=True)

# Speed-to-lead data
s = page()
H(s, "Speed Is The Whole Game — And It’s Measured In Minutes", "Speed-to-lead")
kpi_grid(s, [
    ("21×", "more likely to convert", "lead contacted <5 min vs >30 min"),
    ("7×", "more meaningful talks", "contacting within 1 hour (HubSpot)"),
    ("48%", "never follow up once", "of agents, after the first attempt (NAR)"),
    ("5–12", "touches to close", "most conversions happen after attempt 5"),
])
takeaway(s, "Implication",
         "A human can’t answer in 5 minutes while showing a house. An always-on agent can — every time, "
         "day or night. This single capability is the difference between a pipeline and a revolving door.")

# Follow-up gap
s = page()
H(s, "The Follow-Up Gap Is Where Commission Quietly Disappears", "The conversion leak")
bullets(s, [
    "The lead comes in Thursday afternoon. You see it Friday morning. By Friday afternoon, someone else has talked to them.",
    "Calling once and giving up is the most common mistake — yet 80% of sales need 5+ follow-up touches.",
    "It isn’t lead quality. You’re getting good leads; you’re just not talking to them fast enough, in the right way.",
    "A solo agent juggling response time, scoring, nurture, and data quality will always lose to a team with a dedicated follow-up function.",
], size=15)
takeaway(s, "The reframe",
         "You don’t need more leads. You need to stop leaking the ones you’ve already paid for — and that’s "
         "a systems problem, not an effort problem.")

# TC overload
s = page()
H(s, "Behind The Sale: Transaction Coordination Buries The Team", "Operational load")
kpi_grid(s, [
    ("30–60", "admin tasks / file", "between contract and keys"),
    ("450–900", "open tasks at once", "across a 15–30 file pipeline"),
    ("15–20", "files = the wall", "where quality starts to slip"),
    ("34%", "of failures", "are lender-doc delays not caught in time"),
])
takeaway(s, "Why it breaks",
         "No human reliably tracks hundreds of contract-relative deadlines across parallel files. A missed "
         "contingency can cost a client earnest money — and cost you the relationship and referral.")

# Tech Frankenstein / every hat
s = page()
H(s, "The Owner Becomes The Bottleneck — Wearing Every Hat", "The broker-owner trap")
left = ("The ‘tech Frankenstein’", "Brokers duct-tape a CRM, a transaction tool, a website builder, and a "
        "dozen tools that won’t talk to each other — spending thousands/month and becoming an unpaid IT "
        "consultant, marketing director, and compliance officer.")
right = ("The human glue", "When no tool owns the whole journey, the broker becomes the brain connecting "
         "them — checking if things went out, moving data between systems, the bottleneck when it gets busy.")
d.rect(s, Inches(MF), Inches(1.95), Inches(5.85), Inches(2.6), b.SOFT, radius=0.05, shadow=True)
d.rect(s, Inches(MF), Inches(1.95), Inches(0.08), Inches(2.6), b.CORAL)
d.text(s, left[0], Inches(MF+0.25), Inches(2.15), Inches(5.4), Inches(0.4), size=15, color=b.NAVY, bold=True)
d.text(s, left[1], Inches(MF+0.25), Inches(2.6), Inches(5.4), Inches(1.8), size=12.5, color=b.INK, shrink=True)
d.rect(s, Inches(MF+6.05), Inches(1.95), Inches(5.78), Inches(2.6), b.SOFT, radius=0.05, shadow=True)
d.rect(s, Inches(MF+6.05), Inches(1.95), Inches(0.08), Inches(2.6), b.AMBER)
d.text(s, right[0], Inches(MF+6.3), Inches(2.15), Inches(5.3), Inches(0.4), size=15, color=b.NAVY, bold=True)
d.text(s, right[1], Inches(MF+6.3), Inches(2.6), Inches(5.3), Inches(1.8), size=12.5, color=b.INK, shrink=True)
takeaway(s, "The quiet cost",
         "“You end up spending more time managing your tools than the tools spend managing your business.” "
         "The growth you fought for becomes the thing drowning you.", y=4.8, h=1.45)

# Psychographic
s = page()
H(s, "The Pattern: A Systems Problem Disguised As Dedication", "The owner’s reality")
bullets(s, [
    "The broker equates doing everything with caring — so the business runs entirely on their attention.",
    "Leaked deals get explained as ‘bad leads’ because the alternative — ‘I was too slow’ — indicts them.",
    "The honest version, from a 32-agent broker: broker + admin + trainer + tech support + therapist, all at once.",
    "The belief that keeps them stuck: ‘If I want it done right, I have to do it myself.’",
], size=15)
takeaway(s, "The unlock",
         "You’re not wearing every hat because you care. You’re wearing them because nothing has a hook to "
         "hang on yet. We build the hooks.")

# Voice of customer
s = page()
H(s, "In Their Own Words", "Voice of the market — verbatim, last 12 months")
quotes_grid(s, [
    ("The silent killer is what happens in the 24 hours after a lead arrives.", "BiggerPockets, 2026"),
    ("I still don’t know what half the buttons do, and I’ve been on it for a year.", "Agent on kvCORE, HACK/re 2026"),
    ("It’s 11pm and you’re on Indeed scrolling ISA listings because nobody follows up fast enough.", "RobinFlow, 2026"),
    ("Agents are now drowning in tools AND paperwork, not one or the other.", "Signed to Keys, 2026"),
    ("An OpenClaw agent might handle tasks — but now you manage the system that does the admin.", "REdelegate, 2026"),
    ("On a pipeline of 15–30 files, the aggregate load is crushing — the #1 reason agents burn out.", "Signed to Keys, 2026"),
])

# ════════════════════════════════════════════════════════════════════════════
# SECTION 02 — THE COST
# ════════════════════════════════════════════════════════════════════════════
divider("02", "The Cost", "What the status quo actually costs — in lost deals and wasted salary.")

s = page()
H(s, "The Status Quo Has A Price, Paid Every Month", "Quantifying the cost")
kpi_grid(s, [
    ("21×", "conversion lost", "when response slips past 30 minutes"),
    ("$65–120K", "loaded ISA cost", "per year, before turnover"),
    ("~350", "leads/mo to break even", "on an ISA — most boutiques never hit it"),
    ("450+", "tasks in flight", "across 15–30 files, where deadlines slip"),
])
takeaway(s, "Takeaway",
         "You already pay for the leads. The choice is whether to keep leaking them — or convert them with an "
         "always-on employee that costs less than half an ISA and never quits, trains, or takes a day off.")

s = page()
H(s, "The ISA Math Rarely Pencils For A Boutique", "Cost deep-dive: the human ISA")
scorecard(s, ["Cost line", "Amount / year", "Note"], [3.6, 3.5, 5.03], [
    ("Base salary", "$40–60K", "competent ISA, 2026", b.CORAL),
    ("Benefits + tools + mgmt", "+40–60%", "the hidden load on top of salary", b.AMBER),
    ("Ramp (30–50% productivity)", "$15–25K lost", "3–6 month ramp at full pay", b.AMBER),
    ("Turnover (every 8–24 mo)", "$15–30K / cycle", "many cycle through 2–3 before one sticks", b.CORAL),
    ("Fully loaded", "$65–120K", "and it only pencils above ~350 leads/mo", b.CORAL),
], rh=0.78)
takeaway(s, "Verdict", "For a sub-50-agent boutique below the ~350-lead threshold, an ISA is a fixed cost "
         "against unpredictable lead flow — overpaying for coverage you don’t fully use.", y=5.85, h=1.0)

s = page()
H(s, "And The CRM You Bought Is Mostly Unused", "Cost deep-dive: tool waste")
cards_grid(s, [
    ("30–40% feature use", "Most users engage a third of what they pay for; advanced CRMs take weeks to learn."),
    ("‘Built for brokers, not agents’", "Agent-level adoption is uneven — the tool nobody opens doesn’t convert leads."),
    ("Migration is dangerous", "One documented CRM switch cost $340K in lost transactions, turnover, and re-training."),
    ("Support is thin", "‘Second account manager in 9 months and can’t reach him’ — a few thousand/month for friction."),
], cols=2)
takeaway(s, "The pattern", "Tooling promised efficiency and delivered overhead. The trusted message now is "
         "outcome + zero-management — not another dashboard.")

s = page()
H(s, "Annualized, The Leak Dwarfs The Fix", "The compounding cost")
two = [
    ("Lost deals", "Even a handful of leaked leads per quarter at DFW commission levels is tens of thousands "
     "in GCI walking out the door — silently, every year."),
    ("Wasted salary & tools", "An underutilized ISA + an unused CRM can run $80–130K/year combined, with the "
     "broker still doing the glue work."),
    ("Owner opportunity cost", "Every hour on admin is an hour not recruiting agents or winning listings — the "
     "actual growth levers of a brokerage."),
    ("Burnout & turnover risk", "The owner-as-bottleneck model caps growth and risks the founder’s health — the "
     "least-insured asset in the business."),
]
cards_grid(s, two, cols=2, idx=True)

# ════════════════════════════════════════════════════════════════════════════
# SECTION 03 — WHY THE USUAL FIXES FAIL
# ════════════════════════════════════════════════════════════════════════════
divider("03", "Why The Usual Fixes Fail", "Every option you’ve been sold leaves the work on you.")

s = page()
H(s, "Every Fix Leaves The Work On You", "Solution landscape")
scorecard(s, ["Tried", "Why they tried", "Why it fails", "#1 complaint"], [2.5, 2.3, 3.5, 3.83], [
    ("Do it yourself", "Control", "Mental load exceeds capacity at 15–30 files", "You become the bottleneck", b.CORAL),
    ("Hire an ISA", "Speed-to-lead", "8–24mo turnover; pencils only >350 leads/mo", "$65–120K + you manage them", b.CORAL),
    ("Hire a VA", "Cheaper, flexible", "Trust/quality; still needs managing", "Drowning in tools AND paperwork", b.AMBER),
    ("Buy kvCORE", "All-in-one platform", "Weeks of training; 30–40% feature use", "“Don’t know half the buttons”", b.AMBER),
    ("DIY AI (OpenClaw)", "Cheap autonomy", "Maintenance lands on you", "You manage the bot that does the admin", b.CORAL),
])
d.text(s, "The gap nobody fills: a fully-managed employee where the broker does nothing but approve outcomes.",
       Inches(MF), Inches(6.45), Inches(CWF), Inches(0.4), size=12.5, color=b.DARK_TEAL, bold=True, shrink=True)

s = page()
H(s, "Human ISA vs. VA vs. Managed AI — Side By Side", "Option comparison")
scorecard(s, ["Dimension", "Human ISA", "Virtual Assistant", "Managed AI Employee"],
          [3.0, 3.0, 3.0, 3.13], [
    ("Response time", "Business hours", "Business hours / TZ", "<60s, 24/7", b.TEAL),
    ("Ramp to value", "3–6 months", "2–6 weeks", "48 hours", b.TEAL),
    ("Turnover risk", "Every 8–24 months", "High", "None", b.TEAL),
    ("Monthly cost", "$5.5–10K loaded", "$1.2–2.4K + mgmt", "$5K, fully managed", b.TEAL),
    ("Who manages it", "You", "You", "We do", b.TEAL),
])
takeaway(s, "Net", "The managed AI employee wins on speed, ramp, reliability, and — crucially — removes the "
         "management burden entirely.", y=5.85, h=1.0)

s = page()
H(s, "The DIY-AI Trap: You Just Trade One Job For Another", "Why ‘build it yourself’ backfires")
bullets(s, [
    "Spinning up an OpenClaw / DIY agent looks cheap — until it becomes a second job.",
    "“Once configured, an OpenClaw agent might handle tasks automatically. But the mental load of monitoring, "
    "updating, and fixing it when it breaks doesn’t go away.”",
    "“It moves from doing the admin to managing the system that does the admin.” — REdelegate, 2026",
    "For a busy broker, that invisible, ongoing overhead is harder to offload than the admin itself.",
], size=14.5)
takeaway(s, "Our wedge", "This is exactly the burden a *managed* service removes. We run the system; you never "
         "monitor, update, or debug an agent. You approve outcomes.")

s = page()
H(s, "The Unmet Need", "Where we play")
d.rect(s, Inches(MF), Inches(2.1), Inches(CWF), Inches(2.2), b.NAVY, radius=0.05, shadow=True)
d.text(s, "“I want every lead answered and every deadline tracked —\nwithout hiring, training, or babysitting "
          "anything.”", Inches(MF+0.5), Inches(2.5), Inches(CWF-1.0), Inches(1.4), size=22, color=b.WHITE,
       bold=True, align=PP_ALIGN.CENTER, shrink=True)
takeaway(s, "The category we occupy",
         "Not software (you’d configure it). Not staffing (you’d manage it). Not DIY AI (you’d maintain it). "
         "A managed outcome — a digital employee, run for you.", y=4.7, h=1.5)

# ════════════════════════════════════════════════════════════════════════════
# SECTION 04 — THE SOLUTION
# ════════════════════════════════════════════════════════════════════════════
divider("04", "The Solution", "A managed digital employee — sold as an outcome, not a tool.")

s = page()
H(s, "Our Thesis: Sell A Digital Employee, Not A Tool", "The core idea")
cards_grid(s, [
    ("An employee, not an app", "You don’t learn it, configure it, or log into it. It has a name, an inbox, "
     "and a job — like a hire, minus the hiring."),
    ("Outcomes, not features", "We talk in deals saved and hours returned, never tokens or dashboards. The "
     "measure is your business result."),
    ("Abundance, simply priced", "Unlimited requests, one flat fee, no usage anxiety. Simplicity is what makes "
     "the ‘yes’ fast and the relationship calm."),
    ("Fully managed", "Infrastructure, models, monitoring, security, and fixes are ours. Your only job is to "
     "approve the work."),
], cols=2)

s = page()
H(s, "One Digital Employee, Three Jobs Done — End To End", "What we deliver")
ws = [
    ("Lead Follow-Up", "Answers every inbound lead in <60s, 24/7, across phone, text, email. Runs the 8–12 "
     "touch nurture so no hand-raiser goes cold.", "Sub-60s response"),
    ("Transaction Coordination", "Auto-creates each file at contract, calculates all deadlines, fires "
     "5-day / 2-day / day-of alerts so nothing slips.", "Zero missed deadlines"),
    ("Listing & Marketing Ops", "Drafts listing copy, schedules social, builds market reports, and keeps "
     "your CRM actually updated — on your brand voice.", "Hours back per week"),
]
cw = (CWF - 0.6) / 3
for i, (h, body, stat) in enumerate(ws):
    x = MF + i*(cw+0.3)
    d.rect(s, Inches(x), Inches(1.9), Inches(cw), Inches(3.6), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, Inches(x), Inches(1.9), Inches(cw), Inches(0.7), b.NAVY, radius=0.05)
    d.text(s, h, Inches(x+0.2), Inches(2.08), Inches(cw-0.4), Inches(0.4), size=15, color=b.WHITE, bold=True, shrink=True)
    d.text(s, body, Inches(x+0.25), Inches(2.85), Inches(cw-0.5), Inches(1.7), size=12.5, color=b.INK, shrink=True)
    d.rect(s, Inches(x+0.25), Inches(4.7), Inches(cw-0.5), Inches(0.6), b.LIGHT_TEAL, radius=0.1)
    d.text(s, stat, Inches(x+0.25), Inches(4.82), Inches(cw-0.5), Inches(0.36), size=12.5,
           color=b.DARK_TEAL, bold=True, align=PP_ALIGN.CENTER)
takeaway(s, "Tailored to Momentus", "Veteran & first-time-buyer workflows and your ‘Care, Clarity, "
         "Confidence’ voice — baked in from day one.", y=5.7, h=0.7)

# Workstream details
for title, sub, items in [
    ("Workstream 1 — Lead Follow-Up, In Detail", "Speed + persistence, automated",
     [("Instant first touch", "Replies in <60s by text + email the moment a lead lands, any hour."),
      ("Qualify & route", "Asks the right questions, scores intent, books a showing or callback."),
      ("Persistent nurture", "Runs the 8–12 touch sequence over weeks so slow-to-decide leads stay warm."),
      ("Clean CRM, always", "Logs every interaction into FUB/kvCORE so the pipeline is finally trustworthy.")]),
    ("Workstream 2 — Transaction Coordination, In Detail", "Deadlines that never slip",
     [("Auto file open", "Creates the file at contract execution and populates all party data."),
      ("Deadline engine", "Calculates every contract-relative date — no manual math, no 18% date errors."),
      ("Three-tier alerts", "Advisory at 5 days, warning at 2, critical day-of — to the TC and the agent."),
      ("Document chase", "Requests and tracks signatures and disclosures, escalating only exceptions.")]),
    ("Workstream 3 — Listing & Marketing Ops, In Detail", "On your brand, on schedule",
     [("Listing content", "Drafts MLS copy, descriptions, and email blasts in the Momentus voice."),
      ("Social cadence", "Schedules and posts consistently so the brand stays visible without your time."),
      ("Market reports", "Generates farm-area and seller reports on demand for listing appointments."),
      ("Sphere nurture", "Keeps past clients and the database warm for repeat and referral business.")]),
]:
    s = page(); H(s, title, sub); cards_grid(s, items, cols=2, idx=True)

# Use-case realization 1 — Mia
s = page()
d.rect(s, 0, 0, Inches(3.5), d.H, b.TEAL)
d.text(s, "USE CASE 01", Inches(0.35), Inches(0.6), Inches(2.9), Inches(0.4), size=13, color=b.NAVY, bold=True)
d.text(s, "“Mia” — Your Lead\nResponse Agent", Inches(0.35), Inches(1.1), Inches(2.95), Inches(1.3),
       size=23, color=b.WHITE, bold=True, shrink=True)
d.rect(s, Inches(0.35), Inches(2.5), Inches(1.1), Inches(0.05), b.NAVY)
d.text(s, "A named digital employee with her own inbox, living on a secure cloud computer — she works your "
          "leads while you sleep.", Inches(0.35), Inches(2.7), Inches(2.95), Inches(2.0), size=12.5,
       color=b.NAVY, shrink=True)
d.text(s, "DEPLOYS IN 48 HOURS", Inches(0.35), Inches(6.5), Inches(3), Inches(0.4), size=12, color=b.NAVY, bold=True)
rx = 3.9
d.text(s, "How Mia Realizes The Outcome", Inches(rx), Inches(0.55), Inches(9), Inches(0.5), size=22,
       color=b.NAVY, bold=True, shrink=True)
d.rect(s, Inches(rx), Inches(1.25), Inches(4.4), Inches(1.5), b.SOFT, radius=0.05, shadow=True)
d.text(s, "CHALLENGE", Inches(rx+0.2), Inches(1.38), Inches(4), Inches(0.3), size=11, color=b.CORAL, bold=True)
d.text(s, "A Zillow lead lands at 9pm. The broker is at dinner. Three other agents call back first.",
       Inches(rx+0.2), Inches(1.72), Inches(4.0), Inches(0.95), size=12, color=b.INK, shrink=True)
d.rect(s, Inches(rx+4.6), Inches(1.25), Inches(4.4), Inches(1.5), b.SOFT, radius=0.05, shadow=True)
d.text(s, "SOLUTION", Inches(rx+4.8), Inches(1.38), Inches(4), Inches(0.3), size=11, color=b.DARK_TEAL, bold=True)
d.text(s, "Mia replies in <60s, qualifies, books the showing or callback, and logs it — before a competitor "
          "even sees the lead.", Inches(rx+4.8), Inches(1.72), Inches(4.0), Inches(0.95), size=12, color=b.INK, shrink=True)
for i, (n, l) in enumerate([("<60s", "response"), ("24/7", "coverage"), ("8–12", "nurture touches")]):
    x = rx + i*3.07
    d.rect(s, Inches(x), Inches(2.95), Inches(2.85), Inches(0.95), b.NAVY, radius=0.06)
    d.text(s, n, Inches(x+0.1), Inches(3.05), Inches(1.2), Inches(0.6), size=22, color=b.GOLD, bold=True,
           align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, l, Inches(x+1.3), Inches(3.18), Inches(1.45), Inches(0.5), size=12, color=b.WHITE, bold=True,
           anchor=MSO_ANCHOR.MIDDLE, shrink=True)
d.text(s, "HOW IT WORKS", Inches(rx), Inches(4.1), Inches(9), Inches(0.3), size=11, color=b.MUTED, bold=True)
sx = rx
for i, st in enumerate(["Lead in", "Reply <60s", "Qualify+book", "Log to CRM", "Nurture"]):
    w = 1.6
    d.rect(s, Inches(sx), Inches(4.45), Inches(w), Inches(0.55), b.LIGHT_TEAL, radius=0.1)
    d.text(s, st, Inches(sx), Inches(4.57), Inches(w), Inches(0.34), size=10.5, color=b.DARK_TEAL,
           bold=True, align=PP_ALIGN.CENTER, shrink=True)
    if i < 4:
        d.text(s, "→", Inches(sx+w), Inches(4.5), Inches(0.25), Inches(0.4), size=14, color=b.TEAL,
               bold=True, align=PP_ALIGN.CENTER)
    sx += w + 0.25
d.rect(s, Inches(rx), Inches(5.25), Inches(9.0), Inches(0.55), b.NAVY, radius=0.06)
d.text(s, "STACK:  Hermes harness · Composio (auth+tools) · Agent Mail · Obsidian context · GPT-5.5",
       Inches(rx+0.2), Inches(5.37), Inches(8.7), Inches(0.34), size=11.5, color=b.LIGHT_TEAL, bold=True, shrink=True)
d.rect(s, Inches(rx), Inches(5.95), Inches(4.4), Inches(0.5), b.SOFT, radius=0.06)
d.text(s, "SYSTEMS:  FUB/kvCORE · Zillow · Calendar", Inches(rx+0.2), Inches(6.05), Inches(4.0), Inches(0.32),
       size=10.5, color=b.INK, bold=True, shrink=True)
d.rect(s, Inches(rx+4.6), Inches(5.95), Inches(4.4), Inches(0.5), b.SOFT, radius=0.06)
d.text(s, "USERS:  Broker · Agents · Coordinator", Inches(rx+4.8), Inches(6.05), Inches(4.0), Inches(0.32),
       size=10.5, color=b.INK, bold=True, shrink=True)

# Use-case realization 2 — TC agent
s = page()
d.rect(s, 0, 0, Inches(3.5), d.H, b.ACCENT)
d.text(s, "USE CASE 02", Inches(0.35), Inches(0.6), Inches(2.9), Inches(0.4), size=13, color=b.WHITE, bold=True)
d.text(s, "“Theo” — Your\nDeadline Guardian", Inches(0.35), Inches(1.1), Inches(2.95), Inches(1.3),
       size=23, color=b.WHITE, bold=True, shrink=True)
d.rect(s, Inches(0.35), Inches(2.5), Inches(1.1), Inches(0.05), b.WHITE)
d.text(s, "A transaction-coordination agent that holds every deadline across every open file — so nothing "
          "slips and no client loses earnest money.", Inches(0.35), Inches(2.7), Inches(2.95), Inches(2.2),
       size=12.5, color=b.WHITE, shrink=True)
d.text(s, "E&O RISK ↓", Inches(0.35), Inches(6.5), Inches(3), Inches(0.4), size=12, color=b.WHITE, bold=True)
d.text(s, "How Theo Realizes The Outcome", Inches(rx), Inches(0.55), Inches(9), Inches(0.5), size=22,
       color=b.NAVY, bold=True, shrink=True)
d.rect(s, Inches(rx), Inches(1.25), Inches(4.4), Inches(1.5), b.SOFT, radius=0.05, shadow=True)
d.text(s, "CHALLENGE", Inches(rx+0.2), Inches(1.38), Inches(4), Inches(0.3), size=11, color=b.CORAL, bold=True)
d.text(s, "A lender-doc deadline slips on one file while the TC is heads-down on three others. The buyer’s "
          "earnest money is at risk.", Inches(rx+0.2), Inches(1.72), Inches(4.0), Inches(0.95), size=12,
       color=b.INK, shrink=True)
d.rect(s, Inches(rx+4.6), Inches(1.25), Inches(4.4), Inches(1.5), b.SOFT, radius=0.05, shadow=True)
d.text(s, "SOLUTION", Inches(rx+4.8), Inches(1.38), Inches(4), Inches(0.3), size=11, color=b.DARK_TEAL, bold=True)
d.text(s, "Theo tracks all contract-relative dates across every file and escalates the exception — the human "
          "only handles what truly needs judgment.", Inches(rx+4.8), Inches(1.72), Inches(4.0), Inches(0.95),
       size=12, color=b.INK, shrink=True)
for i, (n, l) in enumerate([("0", "missed deadlines"), ("3-tier", "alerts"), ("35–45", "files / TC")]):
    x = rx + i*3.07
    d.rect(s, Inches(x), Inches(2.95), Inches(2.85), Inches(0.95), b.NAVY, radius=0.06)
    d.text(s, n, Inches(x+0.1), Inches(3.05), Inches(1.25), Inches(0.6), size=20, color=b.GOLD, bold=True,
           align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, l, Inches(x+1.35), Inches(3.18), Inches(1.4), Inches(0.5), size=11.5, color=b.WHITE, bold=True,
           anchor=MSO_ANCHOR.MIDDLE, shrink=True)
d.text(s, "HOW IT WORKS", Inches(rx), Inches(4.1), Inches(9), Inches(0.3), size=11, color=b.MUTED, bold=True)
sx = rx
for i, st in enumerate(["Contract in", "Dates calc’d", "Tasks set", "Tiered alerts", "Escalate"]):
    w = 1.6
    d.rect(s, Inches(sx), Inches(4.45), Inches(w), Inches(0.55), b.LIGHT_TEAL, radius=0.1)
    d.text(s, st, Inches(sx), Inches(4.57), Inches(w), Inches(0.34), size=10.5, color=b.DARK_TEAL,
           bold=True, align=PP_ALIGN.CENTER, shrink=True)
    if i < 4:
        d.text(s, "→", Inches(sx+w), Inches(4.5), Inches(0.25), Inches(0.4), size=14, color=b.TEAL,
               bold=True, align=PP_ALIGN.CENTER)
    sx += w + 0.25
d.rect(s, Inches(rx), Inches(5.25), Inches(9.0), Inches(0.55), b.NAVY, radius=0.06)
d.text(s, "STACK:  Hermes harness · Composio · Obsidian (deadline rules) · GPT-5.5 · scheduled crons",
       Inches(rx+0.2), Inches(5.37), Inches(8.7), Inches(0.34), size=11.5, color=b.LIGHT_TEAL, bold=True, shrink=True)
d.rect(s, Inches(rx), Inches(5.95), Inches(4.4), Inches(0.5), b.SOFT, radius=0.06)
d.text(s, "SYSTEMS:  TX mgmt · DocuSign · Calendar · Email", Inches(rx+0.2), Inches(6.05), Inches(4.0),
       Inches(0.32), size=10.5, color=b.INK, bold=True, shrink=True)
d.rect(s, Inches(rx+4.6), Inches(5.95), Inches(4.4), Inches(0.5), b.SOFT, radius=0.06)
d.text(s, "USERS:  Coordinator · Agents · Clients", Inches(rx+4.8), Inches(6.05), Inches(4.0), Inches(0.32),
       size=10.5, color=b.INK, bold=True, shrink=True)

# Product principles
s = page()
H(s, "The Principles That Keep This Working", "Product principles")
cards_grid(s, [
    ("Remove friction", "The client never thinks about tokens, infra, or security. It just works."),
    ("Create abundance", "Unlimited requests; we control cost behind the scenes so you never ration."),
    ("Go vertical", "Generic agents lose. Yours is tuned to real-estate and the Momentus brand."),
    ("Talk outcomes", "Revenue and hours, not ‘time saved’ — the metric the business actually feels."),
    ("Stay model-agnostic", "We swap to the best/cheapest model as the market moves; you never re-platform."),
    ("Improve weekly", "The agent gets better every week — a relationship, not a one-time setup."),
], cols=3, y0=2.0, ch=1.95)

# ════════════════════════════════════════════════════════════════════════════
# SECTION 05 — ARCHITECTURE & HOW IT WORKS
# ════════════════════════════════════════════════════════════════════════════
divider("05", "Architecture & How It Works", "What runs under the hood — you touch none of it.")

s = page()
H(s, "Under The Hood: A Managed, Layered Architecture", "Solution architecture")
try:
    d.picture_centered(s, ARCH_PNG, top=Inches(1.55), width=Inches(8.7), max_bottom=Inches(6.2))
except Exception as e:
    d.text(s, f"[architecture diagram] {e}", Inches(MF), Inches(3), Inches(CWF), Inches(1), size=12, color=b.MUTED)
d.text(s, "Seven layers — channels → ops → control plane → per-client runtime → capabilities → model router "
          "→ reliability. You touch none of it.", Inches(MF), Inches(6.35), Inches(CWF), Inches(0.5),
       size=12, color=b.MUTED, italic=True, align=PP_ALIGN.CENTER, shrink=True)

s = page()
H(s, "Architecture, Top Half: From Client To Control", "Layer walkthrough (1 of 2)")
cards_grid(s, [
    ("① Clients & Channels", "Your team and leads reach the agent where they already are — text, email, web, voice."),
    ("② Delivery & Client Ops", "A simple board (Trello), meeting notes (Granola), and Loom updates — your window in."),
    ("③ Control Plane", "A meta-agent provisions, configures, and repairs your agents via one connector. The leverage point."),
    ("④ Per-Client Runtime", "Your dedicated agent(s) live on an isolated, secure cloud computer — yours alone."),
], cols=2)

s = page()
H(s, "Architecture, Bottom Half: Capabilities To Reliability", "Layer walkthrough (2 of 2)")
cards_grid(s, [
    ("⑤ Capabilities & Context", "Composio connects 1,000s of apps with managed auth; Obsidian holds your brand context."),
    ("⑥ Model Router", "GPT-5.5 by default, swappable to cheaper/stronger models — your cost lever, invisible to you."),
    ("⑦ Reliability & Observability", "Watchdog + failure alerts keep it running; we’re paged, not you."),
    ("Security boundary", "Per-client sandbox, no shared credentials, deletable in <1s — isolation by design."),
], cols=2)

s = page()
H(s, "You Approve Outcomes. We Run Everything Else.", "The operating model")
panels = [
    ("1 · Request", "You drop a request in one place — or a lead just arrives."),
    ("2 · We provision", "Our control-plane agent configures your agent on a secure cloud computer."),
    ("3 · Agent works", "It uses your tools, CRM, and brand context to do the work."),
    ("4 · We watch", "Watchdog auto-restarts breaks; failures alert us, not you."),
    ("5 · You get the win", "Faster responses, closed deadlines, hours back — improved weekly."),
]
pw = (CWF - 4*0.35) / 5
for i, (h, body) in enumerate(panels):
    x = MF + i*(pw+0.35)
    d.rect(s, Inches(x), Inches(2.1), Inches(pw), Inches(3.0), b.SOFT, radius=0.06, shadow=True)
    d.rect(s, Inches(x), Inches(2.1), Inches(pw), Inches(0.55), b.TEAL if i < 4 else b.GOLD, radius=0.06)
    d.text(s, h, Inches(x+0.1), Inches(2.2), Inches(pw-0.2), Inches(0.36), size=11.5, color=b.NAVY,
           bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, body, Inches(x+0.18), Inches(2.85), Inches(pw-0.36), Inches(2.1), size=11, color=b.INK, shrink=True)
    if i < 4:
        d.text(s, "→", Inches(x+pw+0.02), Inches(3.3), Inches(0.33), Inches(0.5), size=18, color=b.TEAL,
               bold=True, align=PP_ALIGN.CENTER)
takeaway(s, "The principle", "More agents is the answer — an agent builds and repairs your agents, which is why "
         "one operator runs this without it becoming your second job.", y=5.4, h=0.95, fill=b.NAVY, accent=b.GOLD)
d.text(s, "More agents is the answer — an agent builds and repairs your agents, so one operator runs this "
          "without it becoming your second job.", Inches(MF+0.3), Inches(5.9), Inches(CWF-0.6), Inches(0.5),
       size=13, color=b.LIGHT_TEAL, shrink=True)

s = page()
H(s, "The Leverage: An Agent That Builds Your Agents", "The control-plane advantage")
bullets(s, [
    "Setup is the historic time-sink — auth, configuration, connecting tools. We automate it with a control agent.",
    "One connector manages every client computer, so fixes and upgrades happen from anywhere, in seconds.",
    "That’s why a boutique-grade service can be delivered reliably without a 20-person ops team behind it.",
    "For you it means: faster onboarding, faster fixes, and a service that scales with you, not against you.",
], size=14.5)
takeaway(s, "Why you care", "Lower delivery cost and faster response on our side translate directly into your "
         "48-hour go-live and same-day fixes.")

# ════════════════════════════════════════════════════════════════════════════
# SECTION 06 — RELIABILITY, SECURITY & TRUST
# ════════════════════════════════════════════════════════════════════════════
divider("06", "Reliability, Security & Trust", "The moat: we fix it before you — or your client — notices.")

s = page()
H(s, "We Fix It Before You — Or Your Client — Notices", "Reliability & observability")
cards_grid(s, [
    ("Watchdog", "Auto-restarts crashed chat gateways so the agent never goes silent mid-conversation."),
    ("Failure alerts", "If a task or schedule fails, the agent emails US — we fix it before it reaches a client."),
    ("Weekly improvement", "Every week the agent’s skills and context get sharper — reliability compounds."),
    ("Always-on coverage", "24/7/365 — no sick days, no vacations, no Monday-morning ramp."),
], cols=2)
takeaway(s, "Why it matters", "Your clients become dependent on the agent fast. The reliability layer is what "
         "keeps that dependence a delight, not a risk.")

s = page()
H(s, "Security & Isolation By Design", "Trust")
cards_grid(s, [
    ("Per-client sandbox", "Your agent runs in a dedicated, isolated cloud VM — never shared with another client."),
    ("Managed auth", "Tool access is brokered through Composio — no passwords emailed, no credentials on your machine."),
    ("Small blast radius", "A compromised or misbehaving agent is contained and deletable in under a second."),
    ("Your data stays yours", "Context lives in your vault; you own it, and it’s portable if you ever leave."),
], cols=2)

s = page()
H(s, "Human-In-The-Loop Where Judgment Matters", "How we keep it safe with clients")
bullets(s, [
    "The agent drafts; a human signs off on anything client-facing that requires judgment.",
    "High-stakes verticals (legal-style language, sensitive negotiations) stay copilot, by design — not a limitation.",
    "A documented industry lesson: clients pay MORE for assurance — a legal AI pivoted to human-in-loop at a higher price.",
    "You always control the boundary between ‘agent decides’ and ‘human decides.’",
], size=14.5)
takeaway(s, "The balance", "Full automation on the repetitive 90%; human judgment on the 10% that protects "
         "your brand and your client relationships.")

s = page()
H(s, "Our Service Commitments", "What you can hold us to")
scorecard(s, ["Commitment", "Standard", "How we back it"], [4.0, 3.6, 4.53], [
    ("Lead response time", "Under 60 seconds", "Always-on agent + monitoring", b.TEAL),
    ("Time to first agent", "48 hours", "Automated, control-plane provisioning", b.TEAL),
    ("Deadline tracking", "Zero silent misses", "3-tier alerts + escalation", b.TEAL),
    ("Issue detection", "Before the client", "Failure alerts route to us", b.TEAL),
    ("Improvement cadence", "Weekly", "Loom updates + iteration", b.TEAL),
])

# ════════════════════════════════════════════════════════════════════════════
# SECTION 07 — ENGAGEMENT & ONBOARDING
# ════════════════════════════════════════════════════════════════════════════
divider("07", "Engagement & Onboarding", "Live in 48 hours; compounding from week one.")

s = page()
H(s, "Live In 48 Hours. Compounding From Week One.", "Onboarding & roadmap")
d.rect(s, Inches(MF), Inches(1.9), Inches(CWF), Inches(1.25), b.NAVY, radius=0.05)
d.text(s, "FIRST 48 HOURS", Inches(MF+0.3), Inches(2.05), Inches(4), Inches(0.35), size=12, color=b.TEAL, bold=True)
d.text(s, "Kickoff call → connect CRM + lead sources → stand up your agent on a secure VM → load Momentus "
          "brand voice → first live lead answered.", Inches(MF+0.3), Inches(2.45), Inches(CWF-0.6), Inches(0.6),
       size=13.5, color=b.WHITE, bold=True, shrink=True)
phases = [
    ("DAYS 1–30", "Lead follow-up live; nurture running; weekly Loom updates; baseline metrics set."),
    ("DAYS 31–60", "Add the transaction-coordination agent; deadline alerts active; first case-study numbers."),
    ("DAYS 61–90", "Listing/marketing ops + vertical (veteran/first-time) skills; review, expand, or hold."),
]
cw = (CWF - 0.6) / 3
for i, (h, body) in enumerate(phases):
    x = MF + i*(cw+0.3)
    d.rect(s, Inches(x), Inches(3.4), Inches(cw), Inches(2.3), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, Inches(x), Inches(3.4), Inches(cw), Inches(0.55), b.TEAL, radius=0.05)
    d.text(s, h, Inches(x+0.1), Inches(3.5), Inches(cw-0.2), Inches(0.36), size=13, color=b.NAVY,
           bold=True, align=PP_ALIGN.CENTER)
    d.text(s, body, Inches(x+0.25), Inches(4.1), Inches(cw-0.5), Inches(1.45), size=12.5, color=b.INK, shrink=True)
d.text(s, "No 90-day ramp. No training plan. No replacement search when someone quits.", Inches(MF),
       Inches(5.95), Inches(CWF), Inches(0.4), size=12.5, color=b.DARK_TEAL, bold=True, align=PP_ALIGN.CENTER)

s = page()
H(s, "How We’ll Work Together", "Ways of working")
cards_grid(s, [
    ("Single intake", "One place to request work (board or chat). We cap to 1–2 requests / 48h to keep quality high."),
    ("Async updates", "Loom walkthroughs whenever we ship a change — watch on your time, not in a meeting."),
    ("Light cadence", "A short weekly check-in; otherwise the agent runs and you get your time back."),
    ("A human on call", "When something needs judgment or a fix, a real person responds — fast."),
], cols=2)

s = page()
H(s, "Who Does What", "Roles & responsibilities (RACI)")
scorecard(s, ["Activity", "You / Momentus", "Us"], [4.5, 3.8, 3.83], [
    ("Define priorities & brand voice", "Accountable", "Support", b.TEAL),
    ("Build, deploy & maintain agents", "Inform", "Responsible", b.TEAL),
    ("Connect CRM & lead sources", "Consulted", "Responsible", b.TEAL),
    ("Approve client-facing outputs", "Accountable", "Recommend", b.TEAL),
    ("Monitoring, fixes & upgrades", "Inform", "Responsible", b.TEAL),
    ("Measure results & iterate", "Consulted", "Responsible", b.TEAL),
], rh=0.66)

s = page()
H(s, "How We’ll Measure Success", "KPIs & success metrics")
kpi_grid(s, [
    ("Response time", "median, per lead", "target: under 60 seconds"),
    ("Speed-to-lead %", "<5 min contact rate", "target: 90%+ of inbound"),
    ("Deadline misses", "per month", "target: zero silent misses"),
    ("Owner hours saved", "per week", "tracked and reported monthly"),
])
takeaway(s, "Baseline first", "We capture your current numbers in week one, so every improvement is measured "
         "against your real starting point — not a generic benchmark.")

# ════════════════════════════════════════════════════════════════════════════
# SECTION 08 — PROOF & DIFFERENTIATION
# ════════════════════════════════════════════════════════════════════════════
divider("08", "Proof & Differentiation", "It already runs. Here’s why us.")

s = page()
H(s, "This Already Runs — Proof, Not A Promise", "Demonstrated capability")
d.rect(s, Inches(MF), Inches(1.95), Inches(6.0), Inches(3.9), b.NAVY, radius=0.05, shadow=True)
d.text(s, "LIVE DEMO", Inches(MF+0.35), Inches(2.2), Inches(5), Inches(0.4), size=13, color=b.TEAL, bold=True)
d.text(s, "Summit Realty Group — DFW", Inches(MF+0.35), Inches(2.6), Inches(5.3), Inches(0.6), size=20,
       color=b.WHITE, bold=True, shrink=True)
d.text(s, "A working AI dashboard agent built for a DFW brokerage — the same pattern we deploy for your agent:",
       Inches(MF+0.35), Inches(3.3), Inches(5.3), Inches(0.7), size=13, color=b.LIGHT_TEAL, shrink=True)
for i, t in enumerate(["Agent operates a real computer — visible, demoable",
                       "Connects to live data + tools via one connector",
                       "Does real research and real work on screen"]):
    d.text(s, {"text": t, "bullet": True, "size": 12.5, "color": b.LIGHT_TEAL},
           Inches(MF+0.5), Inches(4.05 + i*0.55), Inches(5.1), Inches(0.5), shrink=True)
d.rect(s, Inches(MF+6.4), Inches(1.95), Inches(5.13), Inches(3.9), b.SOFT, radius=0.05, shadow=True)
d.rect(s, Inches(MF+6.4), Inches(1.95), Inches(0.08), Inches(3.9), b.TEAL)
d.text(s, "Why a live demo wins the room", Inches(MF+6.7), Inches(2.2), Inches(4.6), Inches(0.4), size=14.5,
       color=b.NAVY, bold=True)
d.text(s, "Brokers struggle to picture ‘an AI that does work.’ When they watch an agent operate a computer — "
          "search, qualify, book — it stops being abstract. The screen sells the trust a slide never can.",
       Inches(MF+6.7), Inches(2.75), Inches(4.5), Inches(2.0), size=13, color=b.INK, shrink=True)
d.rect(s, Inches(MF+6.7), Inches(4.85), Inches(4.5), Inches(0.7), b.LIGHT_TEAL, radius=0.1)
d.text(s, "We can run a live demo on your real lead flow in the pilot.", Inches(MF+6.85), Inches(4.98),
       Inches(4.2), Inches(0.5), size=12.5, color=b.DARK_TEAL, bold=True, shrink=True)

s = page()
H(s, "Why Us, Specifically", "Differentiation")
cards_grid(s, [
    ("Managed, not DIY", "We remove the operator role — you never monitor, update, or debug an agent."),
    ("Real-estate native", "Built around lead follow-up, TC, and listing ops — not a generic chatbot."),
    ("Proof in hand", "A working DFW brokerage demo today — we show, we don’t just tell."),
    ("Outcome-priced", "Flat fee, abundance offer, no usage anxiety — aligned to your result, not our usage."),
], cols=2)

s = page()
H(s, "Risks — Named, And How We Handle Them", "Risk & mitigation")
scorecard(s, ["Risk", "Mitigation"], [5.0, 7.13], [
    ("Agent breaks / goes silent", "Watchdog auto-restart + failure alerts to us; same-day fixes", b.TEAL),
    ("Client data / security", "Per-client sandbox, managed auth, no shared credentials", b.TEAL),
    ("Agent embarrasses you", "Human-in-the-loop on client-facing judgment calls", b.TEAL),
    ("Model price / availability shifts", "Model-agnostic router; we swap without re-platforming", b.TEAL),
    ("‘Another tool to manage’", "Fully managed — you approve outcomes, we run the system", b.TEAL),
    ("Lock-in worry", "You own the context and workflows; portable if you leave", b.TEAL),
], rh=0.66)

# ════════════════════════════════════════════════════════════════════════════
# SECTION 09 — COMMERCIALS
# ════════════════════════════════════════════════════════════════════════════
divider("09", "Commercials", "Simple, flat, all-inclusive — and proven before you commit.")

s = page()
H(s, "Simple, Flat, All-Inclusive — No Tokens, No Surprises", "Pricing & packaging")
d.rect(s, Inches(MF), Inches(1.95), Inches(5.3), Inches(4.0), b.NAVY, radius=0.05, shadow=True)
d.text(s, "MANAGED DIGITAL EMPLOYEE", Inches(MF+0.35), Inches(2.2), Inches(4.6), Inches(0.4), size=12.5,
       color=b.TEAL, bold=True)
d.text(s, "$5,000", Inches(MF+0.35), Inches(2.65), Inches(4.6), Inches(1.0), size=52, color=b.GOLD,
       bold=True, shrink=True)
d.text(s, "per month · flat · cancel anytime", Inches(MF+0.35), Inches(3.7), Inches(4.6), Inches(0.4),
       size=14, color=b.LIGHT_TEAL)
for i, t in enumerate(["Unlimited requests (scoped 1–2 / 48h)", "All infrastructure, models & tools included",
                       "Monitoring, security & weekly improvements", "Loom updates + a human on call"]):
    d.text(s, {"text": t, "bullet": True, "size": 12.5, "color": b.WHITE},
           Inches(MF+0.45), Inches(4.25 + i*0.4), Inches(4.6), Inches(0.4), shrink=True)
d.rect(s, Inches(MF+5.6), Inches(1.95), Inches(5.93), Inches(1.85), b.SOFT, radius=0.05, shadow=True)
d.text(s, "You never pay for, or manage:", Inches(MF+5.85), Inches(2.15), Inches(5.4), Inches(0.4), size=14,
       color=b.NAVY, bold=True)
for i, t in enumerate(["Tokens, usage, or credits", "Servers, VMs, or model subscriptions",
                       "An ISA salary, benefits, or turnover"]):
    d.text(s, {"text": t, "bullet": True, "size": 12, "color": b.INK},
           Inches(MF+6.0), Inches(2.6 + i*0.38), Inches(5.2), Inches(0.36), shrink=True)
d.rect(s, Inches(MF+5.6), Inches(4.0), Inches(5.93), Inches(1.95), b.LIGHT_TEAL, radius=0.05, shadow=True)
d.rect(s, Inches(MF+5.6), Inches(4.0), Inches(0.08), Inches(1.95), b.TEAL)
d.text(s, "Start with a 2-week paid pilot", Inches(MF+5.9), Inches(4.2), Inches(5.4), Inches(0.4), size=14.5,
       color=b.NAVY, bold=True)
d.text(s, "One agent, one workflow, measured against your current follow-up. Roll into the monthly only if "
          "the numbers land. The risk is ours to prove.", Inches(MF+5.9), Inches(4.65), Inches(5.3),
       Inches(1.2), size=12.5, color=b.INK, shrink=True)

s = page()
H(s, "What’s Included — And What You’ll Never Touch", "Scope clarity")
left = ["Lead follow-up agent (24/7, <60s)", "Transaction-coordination agent", "Listing & marketing ops",
        "CRM integration & clean-up", "Brand-voice tuning (Momentus)", "Monitoring, security & fixes",
        "Weekly improvements + Loom updates"]
right = ["Buying / managing model subscriptions", "Standing up servers or VMs", "Paying per token or per credit",
         "Hiring, training, or replacing an ISA", "Configuring or learning a new CRM", "Debugging a broken automation",
         "Being the ‘glue’ between tools"]
d.text(s, "INCLUDED", Inches(MF), Inches(1.85), Inches(5.8), Inches(0.4), size=14, color=b.DARK_TEAL, bold=True)
d.text(s, [{"text": t, "bullet": True, "size": 12.5, "space_before": 7} for t in left],
       Inches(MF), Inches(2.3), Inches(5.7), Inches(4.0), shrink=True)
d.text(s, "YOU’LL NEVER TOUCH", Inches(MF+6.2), Inches(1.85), Inches(5.6), Inches(0.4), size=14,
       color=b.CORAL, bold=True)
d.text(s, [{"text": t, "bullet": True, "size": 12.5, "space_before": 7, "color": b.MUTED} for t in right],
       Inches(MF+6.2), Inches(2.3), Inches(5.6), Inches(4.0), shrink=True)

s = page()
H(s, "The Math Works On A Single Saved Deal", "Business case")
kpi_grid(s, [
    ("$5K / mo", "your investment", "less than half a loaded ISA"),
    ("1 deal", "to break even", "one extra closing per quarter pays the year"),
    ("21×", "conversion lift", "leads answered <5 min vs >30 min"),
    ("0", "to manage", "no hiring, training, turnover, or upkeep"),
])
takeaway(s, "The asymmetry", "Recovering even one leaked lead per quarter covers the entire annual cost — and "
         "you keep every closing after that, plus the hours to recruit agents and grow Momentus.",
         y=4.7, h=1.2)

s = page()
H(s, "Start With Proof: The 2-Week Pilot", "De-risked entry")
cards_grid(s, [
    ("Scope", "One agent, one workflow (lead follow-up) on your real lead flow."),
    ("Measure", "Response time and contact rate vs your current baseline — captured day one."),
    ("Decide", "Roll into the monthly only if the numbers land. No long contract to start."),
    ("Risk", "Ours. We prove the outcome before you commit to the relationship."),
], cols=2, idx=True)

# ════════════════════════════════════════════════════════════════════════════
# SECTION 10 — FIT & THE ASK
# ════════════════════════════════════════════════════════════════════════════
divider("10", "Fit & The Ask", "Why Momentus — and the next step.")

s = page()
H(s, "Why This Fits Momentus Specifically", "The fit")
cards_grid(s, [
    ("You already think in systems", "Momentus markets a ‘proprietary intelligence layer’ and an ecosystem — "
     "a digital employee extends that thesis, it doesn’t fight it."),
    ("Growth mode, boutique feel", "Founded 2024 and scaling without losing the boutique touch. The agent "
     "absorbs the operational load that usually forces a trade-off."),
    ("High-context niches", "Veteran & first-time-buyer journeys are follow-up- and education-heavy — exactly "
     "where instant response and patient nurture convert."),
    ("Owner-led, time-starved", "When the founder is broker, trainer, and ops, reclaiming hours is the highest- "
     "leverage move you can make."),
], cols=2, idx=True)

s = page()
H(s, "Where This Goes Next For Momentus", "Vertical roadmap")
cards_grid(s, [
    ("Quarter 1", "Lead-response + TC agents live across the team; baseline beaten on speed-to-lead."),
    ("Quarter 2", "Veteran & first-time-buyer ‘Ready or Not?’ education flows automated end-to-end."),
    ("Quarter 3", "Recruiting agent — Momentus’ growth engine, working candidates while you sell."),
    ("Beyond", "A Momentus ‘intelligence layer’ that is real, running, and a recruiting differentiator."),
], cols=2)

s = page()
H(s, "Objections, Answered Plainly", "Anticipated questions")
scorecard(s, ["You might think…", "The reality"], [5.2, 6.93], [
    ("“Is it secure with client data?”", "Per-client sandbox, managed auth, no shared credentials", b.TEAL),
    ("“Another tool I’ll manage?”", "Fully managed — you approve outcomes, we run it", b.TEAL),
    ("“Will it embarrass me?”", "Human-in-the-loop on judgment; watchdog catches breaks", b.TEAL),
    ("“I already pay for kvCORE.”", "We sit on top and make the tool you abandoned get used", b.TEAL),
    ("“$5K is a lot.”", "Less than half an ISA; one saved deal/quarter pays the year", b.TEAL),
], rh=0.7)

# CLOSE
s = page(fill=b.NAVY, dark=True)
d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
d.text(s, "THE NEXT STEP", Inches(MF), Inches(1.3), Inches(8), Inches(0.4), size=15, color=b.TEAL, bold=True)
d.text(s, "Let’s run a 2-week pilot.", Inches(MF), Inches(1.9), Inches(11), Inches(1.0), size=42,
       color=b.WHITE, bold=True, shrink=True)
d.rect(s, Inches(MF), Inches(3.05), Inches(1.6), Inches(0.05), b.TEAL)
d.text(s, "One live agent on your real lead flow, measured against how you follow up today. You decide on the proof.",
       Inches(MF), Inches(3.3), Inches(10.5), Inches(0.8), size=16, color=b.LIGHT_TEAL, shrink=True)
steps = [("1", "30-min kickoff", "scope the first workflow + connect sources"),
         ("2", "48h to live", "your agent answering real leads"),
         ("3", "2-week readout", "metrics vs your baseline → go / no-go")]
cw = (CWF - 0.8) / 3
for i, (n, h, body) in enumerate(steps):
    x = MF + i*(cw+0.4)
    d.rect(s, Inches(x), Inches(4.35), Inches(cw), Inches(1.7), b.NAVY_2, radius=0.06)
    d.rect(s, Inches(x), Inches(4.35), Inches(cw), Inches(0.5), b.TEAL, radius=0.06)
    d.text(s, f"STEP {n}", Inches(x), Inches(4.45), Inches(cw), Inches(0.32), size=12, color=b.NAVY,
           bold=True, align=PP_ALIGN.CENTER)
    d.text(s, h, Inches(x+0.2), Inches(4.95), Inches(cw-0.4), Inches(0.45), size=15, color=b.WHITE, bold=True, shrink=True)
    d.text(s, body, Inches(x+0.2), Inches(5.4), Inches(cw-0.4), Inches(0.6), size=12, color=b.LIGHT_TEAL, shrink=True)
d.text(s, "Contact: shekerkamma@gmail.com", Inches(MF), Inches(6.45), Inches(10), Inches(0.4), size=13,
       color=b.GOLD, bold=True)

# ── draw deferred footers with correct total ────────────────────────────────
TOTAL = len(_pages)
for i, (s, dark) in enumerate(_pages, start=1):
    d.footer(s, i, TOTAL, dark=dark)

d.save(OUT)
print("SLIDES:", d.n)
