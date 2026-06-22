#!/usr/bin/env python3
"""Builder v5: Agentic AI vs. SaaS — adds Top-25 use cases derived from Google's 1,302 real
deployments (graphed) fused with the SaaS replace/enrich verdict. Auto page-numbering."""
import sys
sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, Inches as In, Pt, PP_ALIGN
from pptx.enum.text import MSO_ANCHOR as VA
CENTER, LEFT = PP_ALIGN.CENTER, PP_ALIGN.LEFT

OUT = "/home/shekerk/content-ideas/runs/2026-06-22-agentic-ai-vs-saas-reddit-strategy/agentic-ai-vs-saas-usecases-v5-draft.pptx"
d = Deck(footer="Agentic AI vs. SaaS · Use-Case Strategy | 2026-06-22")
b = d.b
W = d.W
TOTAL = 20
_pgc = [1]
def PG():
    _pgc[0] += 1
    return _pgc[0]

def card(s, x, y, w, h, fill, line=None):
    d.rect(s, x, y, w, h, fill, line=line, radius=0.06, shadow=True)

def head(s, title, subtitle=None):
    d.text(s, title, d.M, In(0.42), d.CW, In(0.66), size=30, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, d.M, In(1.12), In(1.45), In(0.05), b.TEAL)
    if subtitle:
        d.text(s, subtitle, d.M, In(1.26), d.CW, In(0.4), size=14.5, color=b.MUTED, shrink=True)

def pill(s, x, y, w, h, text, fill, txt=None, size=11):
    d.rect(s, x, y, w, h, fill, radius=0.5)
    d.text(s, text, x, y + (h - In(0.24)) / 2, w, In(0.24), size=size, color=txt or b.WHITE, bold=True, align=CENTER)

V = {"REPLACE": b.CORAL, "ENRICH": b.TEAL, "HYBRID": b.AMBER}

def top25_slide(title, subtitle, groups):
    s = d.slide(fill=b.WHITE)
    head(s, title, subtitle)
    cx_num, w_num = In(0.6), In(0.4)
    cx_uc, w_uc = In(1.05), In(2.45)
    cx_pr, w_pr = In(3.55), In(4.25)
    cx_sa, w_sa = In(7.9), In(2.7)
    cx_vd, w_vd = In(10.7), In(2.0)
    hy = In(1.72)
    d.rect(s, d.M, hy, d.CW, In(0.4), b.NAVY, radius=0.04)
    for cx, w, t, al in [(cx_num, w_num, "#", CENTER), (cx_uc, w_uc, "USE CASE", LEFT),
                         (cx_pr, w_pr, "PROOF — REAL DEPLOYMENTS", LEFT),
                         (cx_sa, w_sa, "SAAS DISPLACED / ENRICHED", LEFT), (cx_vd, w_vd, "VERDICT", CENTER)]:
        d.text(s, t, cx + In(0.06), hy + In(0.08), w - In(0.1), In(0.26), size=9.5, color=b.TEAL, bold=True, align=al)
    y = hy + In(0.4)
    for gname, rows in groups:
        d.rect(s, d.M, y, d.CW, In(0.28), b.ACCENT)
        d.text(s, gname, d.M + In(0.12), y + In(0.04), In(9), In(0.22), size=9.5, color=b.WHITE, bold=True)
        y += In(0.28)
        for num, uc, proof, saas, verd in rows:
            d.rect(s, d.M, y, d.CW, In(0.4), b.SOFT if num % 2 == 0 else b.WHITE)
            d.rect(s, d.M, y, In(0.05), In(0.4), V[verd])
            d.text(s, str(num), cx_num, y + In(0.09), w_num, In(0.24), size=10, color=b.INK, bold=True, align=CENTER)
            d.text(s, uc, cx_uc + In(0.05), y + In(0.05), w_uc - In(0.22), In(0.32), size=9.5, color=b.INK, bold=True, shrink=True)
            d.text(s, proof, cx_pr + In(0.12), y + In(0.05), w_pr - In(0.24), In(0.32), size=8.7, color=b.MUTED, shrink=True)
            d.text(s, saas, cx_sa + In(0.05), y + In(0.05), w_sa - In(0.12), In(0.32), size=8.7, color=b.INK, shrink=True)
            pill(s, cx_vd + In(0.18), y + In(0.07), w_vd - In(0.36), In(0.26), verd, V[verd], size=9)
            y += In(0.4)
    d.footer(s, PG(), TOTAL)

# ── 1. Cover ──────────────────────────────────────────────────────────────────
s = d.slide(fill=b.NAVY)
d.rect(s, W - In(2.4), 0, In(2.4), In(7.5), b.NAVY_2)
d.rect(s, W - In(2.4), 0, In(0.06), In(7.5), b.TEAL)
d.text(s, "USE-CASE STRATEGY · MARKET INTELLIGENCE", d.M, In(0.95), In(8), In(0.4), size=15, color=b.TEAL, bold=True)
d.text(s, "Agentic AI vs. SaaS: The Top 25 Use Cases", d.M, In(1.55), In(9.6), In(1.9),
       size=44, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, In(3.7), In(1.6), In(0.05), b.TEAL)
d.text(s, "The 25 agentic use cases proven across 1,302 real deployments — and the SaaS each "
          "displaces or enriches, with a scorecard to grade your stack.", d.M, In(3.95), In(9.4), In(0.9),
       size=16, color=b.LIGHT_TEAL, shrink=True)
for i, chip in enumerate(["Top 25 use cases", "1,302 deployments", "23 cited sources"]):
    cx = d.M + In(i * 3.15)
    d.rect(s, cx, In(5.4), In(2.95), In(0.62), b.NAVY_2, line=b.TEAL, radius=0.12)
    d.text(s, chip, cx, In(5.55), In(2.95), In(0.36), size=13, color=b.WHITE, bold=True, align=CENTER)
d.text(s, "Evidence base: Google Cloud's 1,302 gen-AI deployments (graphed). Authentic strategy — no astroturfing.",
       d.M, In(6.55), In(11), In(0.4), size=12, color=b.MUTED, italic=True)

# ── 2. Executive summary (BLUF) ───────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "Agents Replace Workflows, Not Software In General", "BLUF · Situation → Insight → Recommendation")
d.rect(s, d.M, In(1.75), d.CW, In(0.9), b.NAVY, radius=0.05)
d.text(s, "Per-seat software is being repriced where the seat wraps a repetitive workflow: ~$300B of vendor "
          "value erased in 2026. We isolate the 25 use cases that are proven at scale — and grade the SaaS each hits.",
       d.M + In(0.25), In(1.92), d.CW - In(0.5), In(0.6), size=14.5, color=b.WHITE, anchor=VA.MIDDLE, shrink=True)
cols = [
    ("SITUATION", b.MUTED, ["Per-seat = one login per human worker", "Reddit: 790+ r/SaaS founder threads",
                            "Google lists 1,302 live deployments"]),
    ("INSIGHT", b.TEAL, ["6 agent archetypes recur across 11 industries", "Workflow-heavy + logic-light flips first",
                         "Systems of record compound (data moat)"]),
    ("RECOMMENDATION", b.GOLD, ["Rank the top 25, map each to a SaaS verdict", "Keep / renegotiate / replace, with math",
                                "Publish it as a pre-sales magnet"]),
]
cw = (d.CW - In(0.6)) / 3
for i, (h, col, items) in enumerate(cols):
    x = d.M + i * (cw + In(0.3))
    card(s, x, In(2.85), cw, In(2.95), b.SOFT)
    d.rect(s, x, In(2.85), cw, In(0.5), b.NAVY, radius=0.06)
    d.text(s, h, x, In(2.95), cw, In(0.32), size=13, color=col, bold=True, align=CENTER)
    d.text(s, [{"text": t, "bullet": True, "size": 12.5, "space_before": 8} for t in items],
           x + In(0.22), In(3.55), cw - In(0.44), In(2.1), shrink=True)
d.rect(s, d.M, In(6.05), d.CW, In(0.62), b.GOLD, radius=0.05)
d.text(s, "THE ASK:  Build the \"Agent Replacement Scorecard\" around the Top 25 use cases that follow.",
       d.M + In(0.25), In(6.18), d.CW - In(0.5), In(0.4), size=13.5, color=b.NAVY, bold=True, anchor=VA.MIDDLE, shrink=True)
d.footer(s, PG(), TOTAL)

# ── 3. Storyboard narrative ───────────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "The Argument In Five Beats", "Situation → Complication → Question → Answer → Action")
beats = [
    ("SITUATION", b.MUTED, "Buyers pay per seat for software that wraps a workflow."),
    ("COMPLICATION", b.CORAL, "Agents now do the workflow — no seat needed. ~$300B repriced in 2026."),
    ("QUESTION", b.AMBER, "Which use cases flip to agents now, and which stay?"),
    ("ANSWER", b.TEAL, "25 archetypes are proven across 1,302 deployments; records compound."),
    ("ACTION", b.GOLD, "Grade every use case: keep / renegotiate / replace."),
]
n = len(beats); gap = In(0.28); pw = (d.CW - gap * (n - 1)) / n
for i, (h, col, body) in enumerate(beats):
    x = d.M + i * (pw + gap)
    card(s, x, In(2.1), pw, In(3.7), b.SOFT)
    d.rect(s, x, In(2.1), pw, In(0.55), b.NAVY, radius=0.06)
    d.rect(s, x, In(2.1), pw, In(0.06), col)
    d.text(s, h, x, In(2.24), pw, In(0.32), size=12.5, color=col, bold=True, align=CENTER)
    d.text(s, body, x + In(0.16), In(2.9), pw - In(0.32), In(2.7), size=13, color=b.INK, shrink=True)
    if i < n - 1:
        d.text(s, "→", x + pw - In(0.04), In(3.5), gap + In(0.1), In(0.4), size=20, color=b.TEAL, bold=True, align=CENTER)
d.footer(s, PG(), TOTAL)

# ── 4. Top-25 methodology ─────────────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "How The Top 25 Were Chosen", "From 1,302 real deployments → graphed → ranked → mapped to a SaaS verdict")
steps = [
    ("1", "EVIDENCE BASE", "Google Cloud's 1,302 real-world gen-AI deployments, split into 11 industries and "
     "built into a 77-node knowledge graph (this run)."),
    ("2", "ARCHETYPES", "The corpus collapses to 6 agent types — Customer, Employee, Creative, Code, Data, "
     "Security — recurring across every industry. We ranked the 25 most prevalent."),
    ("3", "SAAS VERDICT", "Each archetype mapped to the SaaS category it displaces or enriches, using the "
     "Agent Replacement Index + ITOps research."),
]
cw = (d.CW - In(0.6)) / 3
for i, (num, h, body) in enumerate(steps):
    x = d.M + i * (cw + In(0.3))
    card(s, x, In(2.0), cw, In(3.0), b.SOFT)
    d.rect(s, x, In(2.0), In(0.8), In(0.65), b.NAVY, radius=0.08)
    d.text(s, num, x, In(2.1), In(0.8), In(0.45), size=22, color=b.GOLD, bold=True, align=CENTER)
    d.text(s, h, x + In(0.95), In(2.18), cw - In(1.1), In(0.4), size=14, color=b.INK, bold=True, shrink=True)
    d.text(s, body, x + In(0.25), In(2.9), cw - In(0.5), In(1.9), size=12.5, color=b.MUTED, shrink=True)
    if i < 2:
        d.text(s, "→", x + cw - In(0.02), In(3.3), In(0.3), In(0.4), size=20, color=b.TEAL, bold=True, align=CENTER)
d.rect(s, d.M, In(5.3), d.CW, In(1.25), b.NAVY, radius=0.05)
d.text(s, "Honesty line", d.M + In(0.3), In(5.45), In(6), In(0.4), size=13, color=b.TEAL, bold=True)
d.text(s, "Deployments are real and named (Google's list). The ranking and the replace/enrich verdicts are "
          "structured judgment — directional guidance, not measured counts.", d.M + In(0.3), In(5.85), d.CW - In(0.6),
       In(0.6), size=13, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, PG(), TOTAL)

# ── 5–7. Top-25 matrices ──────────────────────────────────────────────────────
top25_slide("The Top 25 — Customer & Employee Agents", "Proof from Google's 1,302 deployments · verdict from SaaS-disruption research", [
    ("CUSTOMER AGENTS", [
        (1, "Conversational support", "Mercedes MBUX, Wendy's FreshAI, Home Depot Magic Apron, Macy's", "Per-seat help desks (Zendesk)", "REPLACE"),
        (2, "In-product owner assistant", "Volkswagen myVW, GM OnStar", "Manuals / FAQ / deflection tools", "ENRICH"),
        (3, "AI shopping / sales consultant", "Mercedes smart sales, Mobiauto, Best Buy", "Guided-selling SaaS", "REPLACE"),
        (4, "Travel & booking planner", "Agoda, Priceline, LATAM Cosmos, Virgin Voyages", "Booking / itinerary tools", "REPLACE"),
        (5, "Messaging-channel chatbot", "LUXGEN (LINE), Banglalink REN, DT MINDR", "Chatbot / CCaaS bots", "REPLACE"),
    ]),
    ("EMPLOYEE AGENTS", [
        (6, "Enterprise knowledge search", "Geotab, Bosch AskBosch, Glean", "Enterprise search SaaS", "REPLACE"),
        (7, "Doc summarization & drafting", "KPMG, PwC, Deloitte", "Doc / productivity add-ons", "ENRICH"),
        (8, "Contact-center agent assist", "Humana Agent Assist, Vodafone", "CCaaS agent-assist", "ENRICH"),
        (9, "Legal research & drafting", "Harvey, Thomson Reuters, Deutsche Bank DB Lumina", "Westlaw, LexisNexis, CLM", "REPLACE"),
        (10, "HR / onboarding agent", "Grupo Ruiz, employee-agent deployments", "HR workflow SaaS", "REPLACE"),
    ]),
])
top25_slide("The Top 25 — Creative & Code Agents", "Proof from Google's 1,302 deployments · verdict from SaaS-disruption research", [
    ("CREATIVE AGENTS", [
        (11, "Ad & creative generation at scale", "WPP, Authentic Brands Group, PODS billboard", "Creative production seats", "REPLACE"),
        (12, "Video generation", "Veo deployments, Adobe", "Video editing SaaS", "HYBRID"),
        (13, "Personalized marketing content", "Adobe, ElevenLabs (voice)", "Marketing content tools", "REPLACE"),
        (14, "Brand / 3D asset generation", "BMW Group SORDI.ai", "Asset / DAM tooling", "ENRICH"),
    ]),
    ("CODE AGENTS", [
        (15, "AI code assistant", "Valeo, Broadcom (Gemini Code Assist)", "IDE / code-review add-ons", "ENRICH"),
        (16, "Legacy-IT modernization (NL→SAP)", "Suzano, Deutsche Telekom", "Modernization consulting / tools", "ENRICH"),
        (17, "App build / migration automation", "Code-agent deployments", "Low-code & migration tooling", "HYBRID"),
    ]),
])
top25_slide("The Top 25 — Data & Security Agents", "Proof from Google's 1,302 deployments · verdict from SaaS-disruption research", [
    ("DATA AGENTS", [
        (18, "NL analytics (text-to-SQL)", "Spotify, Etsy (BigQuery)", "BI dashboards (Looker-class)", "HYBRID"),
        (19, "Document AI extraction", "Document AI deployments", "IDP / OCR SaaS", "REPLACE"),
        (20, "Forecasting / predictive ops", "Honeywell, Geotab", "Predictive-analytics SaaS", "ENRICH"),
        (21, "Research & insight agent", "MLB Scout Insights, NotebookLM", "Market-research tooling", "ENRICH"),
    ]),
    ("SECURITY AGENTS", [
        (22, "Threat detection / SecOps", "Google Security Operations deployments", "SIEM tier-1", "ENRICH"),
        (23, "Agentic auto-remediation", "Security-agent deployments", "SOAR / runbooks", "REPLACE"),
        (24, "Fraud & risk detection", "Citi, Wells Fargo, Commerzbank Bene", "Fraud / risk add-ons", "ENRICH"),
        (25, "Compliance & audit agent", "U.S. FDA, regulated deployments", "GRC tooling", "ENRICH"),
    ]),
])

# ── Realization slide factory ─────────────────────────────────────────────────
def uc_slide(title, subtitle, challenge, solution, stats, steps, stack, displaces, proof,
             left_label="DISPLACES", left_color=None):
    left_color = left_color or b.CORAL
    s = d.slide(fill=b.WHITE)
    head(s, title, subtitle)
    top = In(1.8)
    LPx, LPw = d.M, In(4.25)
    d.rect(s, LPx, top, LPw, In(4.75), b.NAVY, radius=0.05)
    d.rect(s, LPx, top, LPw, In(0.06), b.TEAL)
    d.text(s, "CHALLENGE", LPx + In(0.25), top + In(0.2), LPw - In(0.5), In(0.3), size=13, color=b.TEAL, bold=True)
    d.text(s, challenge, LPx + In(0.25), top + In(0.58), LPw - In(0.5), In(1.5), size=13, color=b.LIGHT_TEAL, shrink=True)
    d.text(s, "SOLUTION", LPx + In(0.25), top + In(2.2), LPw - In(0.5), In(0.3), size=13, color=b.GOLD, bold=True)
    d.text(s, solution, LPx + In(0.25), top + In(2.58), LPw - In(0.5), In(2.0), size=13, color=b.WHITE, shrink=True)
    RX = d.M + In(4.55); RW = d.W - In(0.6) - RX
    sw = (RW - In(0.6)) / 3
    for i, (num, lab) in enumerate(stats):
        x = RX + i * (sw + In(0.3))
        d.rect(s, x, top, sw, In(1.05), b.SOFT, radius=0.06)
        d.text(s, num, x, top + In(0.1), sw, In(0.55), size=26, color=b.NAVY, bold=True, align=CENTER)
        d.text(s, lab, x + In(0.08), top + In(0.66), sw - In(0.16), In(0.34), size=10.5, color=b.MUTED, align=CENTER, shrink=True)
    hwy = top + In(1.3)
    d.text(s, "HOW IT WORKS", RX, hwy, RW, In(0.3), size=12.5, color=b.ACCENT, bold=True)
    nstep = len(steps); sgap = In(0.32); stw = (RW - sgap * (nstep - 1)) / nstep
    for i, st in enumerate(steps):
        x = RX + i * (stw + sgap)
        d.rect(s, x, hwy + In(0.4), stw, In(0.9), b.NAVY, radius=0.06)
        d.text(s, f"{i+1}", x + In(0.1), hwy + In(0.48), stw - In(0.2), In(0.28), size=12, color=b.GOLD, bold=True)
        d.text(s, st, x + In(0.1), hwy + In(0.74), stw - In(0.2), In(0.5), size=10.5, color=b.WHITE, shrink=True)
        if i < nstep - 1:
            d.text(s, "→", x + stw - In(0.02), hwy + In(0.62), sgap, In(0.4), size=15, color=b.TEAL, bold=True, align=CENTER)
    sby = hwy + In(1.55)
    d.text(s, "STACK", RX, sby, In(2), In(0.28), size=12.5, color=b.ACCENT, bold=True)
    d.text(s, "  ·  ".join(stack), RX + In(0.9), sby - In(0.01), RW - In(0.9), In(0.32), size=11, color=b.INK, bold=True, shrink=True)
    dy = sby + In(0.5); half = (RW - In(0.3)) / 2
    d.rect(s, RX, dy, half, In(1.62), b.SOFT, radius=0.06)
    d.text(s, left_label, RX + In(0.18), dy + In(0.12), half - In(0.36), In(0.3), size=12, color=left_color, bold=True)
    d.text(s, [{"text": t, "bullet": True, "size": 11, "space_before": 5} for t in displaces],
           RX + In(0.18), dy + In(0.46), half - In(0.36), In(1.1), shrink=True)
    d.rect(s, RX + half + In(0.3), dy, half, In(1.62), b.SOFT, radius=0.06)
    d.text(s, "PROOF", RX + half + In(0.48), dy + In(0.12), half - In(0.36), In(0.3), size=12, color=b.TEAL, bold=True)
    d.text(s, [{"text": t, "bullet": True, "size": 11, "space_before": 5} for t in proof],
           RX + half + In(0.48), dy + In(0.46), half - In(0.36), In(1.1), shrink=True)
    d.footer(s, PG(), TOTAL)

# ── 8–10. Deep dives ──────────────────────────────────────────────────────────
uc_slide(
    "Deep Dive — Customer Support (#1)", "Tier-1 ticket resolution · displaces per-seat help desks",
    "A 100-agent support team, each on a per-seat help-desk license. Ticket volume scales cost "
    "linearly, yet Tier-1 work is repetitive and well-defined.",
    "Deploy an AI support agent that autonomously resolves ~80% of ticket volume and escalates the "
    "rest. Humans move from first-line response to escalation management.",
    [("~80%", "tickets auto-resolved"), ("~700", "reps-equiv (Klarna)"), ("80–90%", "seat cut, wave 1")],
    ["Ingest ticket + context", "Classify & draft", "Resolve or escalate", "Write to record"],
    ["LLM agent", "RAG", "MCP tools", "Escalation"],
    ["Per-seat help desks (Zendesk-style)", "QA scoring tools", "Lower-tier BPO contracts"],
    ["Klarna AI ≈ 700 reps", "Mercedes MBUX, Wendy's FreshAI (Google list)", "Support: 80–90% seat cuts"],
)
uc_slide(
    "Deep Dive — Sales Outreach (#3-class)", "Prospecting + sequencing · displaces per-rep engagement tools",
    "SDR teams are the heaviest users of sales-engagement software — one seat per rep for "
    "prospecting, enrichment, and multi-channel sequencing.",
    "One coordinated agent infrastructure runs research, personalization, and outreach end-to-end. "
    "No per-rep seats; the team supervises outcomes instead of operating tools.",
    [("1", "agent infra vs. N seats"), ("9/10", "Replacement Index"), ("65%", "rep time non-selling")],
    ["Find buying signals", "Enrich & personalize", "Run sequence", "Route replies"],
    ["LLM agent", "Data APIs", "Email/LinkedIn", "CRM write"],
    ["Outreach / Salesloft seats", "Enrichment (ZoomInfo/Apollo)", "Per-seat sequencers"],
    ["11x, Artisan, AISDR live", "Agentic wins SMB outbound", "Hybrid still wins enterprise"],
)
uc_slide(
    "Deep Dive — IT Helpdesk (#6-class)", "Tier-1 tickets & requests · displaces per-seat ITSM",
    "IT staff on per-seat ITSM licenses spend hours on password resets, ticket triage, and status "
    "updates — repetitive, well-documented work.",
    "An AI service agent resolves common requests end-to-end and routes the rest, working inside the "
    "existing ITSM as the system of record.",
    [("30–40%+", "tickets no-touch"), ("L1", "role absorbed"), ("24/7", "coverage, no seats")],
    ["Classify request", "Pull KB/runbook", "Resolve or route", "Update ticket"],
    ["LLM agent", "Runbooks", "ITSM API", "Routing"],
    ["ITSM tier-1 seats (ServiceNow)", "Internal KB products", "The L1 helpdesk role"],
    ["Moveworks, Aisera, Glean live", "ServiceNow: 30–40% resolvable", "Password resets fully auto"],
)

# ── 11. IT OPERATIONS framing ─────────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "IT Operations: Enrich First, Replace Second", "The agent rides on top of your data-rich platforms via MCP — not around them")
d.rect(s, d.M, In(1.75), d.CW, In(0.86), b.NAVY, radius=0.05)
d.text(s, "In ITOps the winning pattern is augmentation: an AI SRE agent connects (read-only, via MCP) to the "
          "telemetry platforms you already run, investigates autonomously, and remediates within policy. Only "
          "workflow-over-data layers get replaced.", d.M + In(0.25), In(1.9), d.CW - In(0.5), In(0.58),
       size=13.5, color=b.WHITE, anchor=VA.MIDDLE, shrink=True)
panels = [
    ("ENRICH — the data-rich layer", b.TEAL,
     ["Datadog, Dynatrace, Splunk, ServiceNow, New Relic, Grafana, Elastic",
      "Agents consume telemetry via MCP; correlate, draft RCA",
      "The platform's data moat grows MORE valuable, not less"]),
    ("REPLACE — workflow-over-data", b.CORAL,
     ["PagerDuty alert routing, BigPanda correlation, L1 NOC triage",
      "The agent becomes the first responder on every page",
      "Routing / correlation seats erode as agents reason natively"]),
]
pw = (d.CW - In(0.4)) / 2
for i, (h, col, items) in enumerate(panels):
    x = d.M + i * (pw + In(0.4))
    card(s, x, In(2.8), pw, In(2.5), b.SOFT)
    d.rect(s, x, In(2.8), pw, In(0.5), col, radius=0.06)
    d.text(s, h, x, In(2.9), pw, In(0.32), size=13.5, color=b.WHITE, bold=True, align=CENTER)
    d.text(s, [{"text": t, "bullet": True, "size": 12.5, "space_before": 9} for t in items],
           x + In(0.22), In(3.45), pw - In(0.44), In(1.7), shrink=True)
stat = [("up to 35%", "ITOps cost cut (IBM)"), ("hrs → min", "MTTR with AI SRE"), ("MCP", "the agent–telemetry bridge (GA)")]
sw = (d.CW - In(0.6)) / 3
for i, (n_, lab) in enumerate(stat):
    x = d.M + i * (sw + In(0.3))
    d.rect(s, x, In(5.5), sw, In(1.0), b.NAVY, radius=0.06)
    d.text(s, n_, x, In(5.62), sw, In(0.5), size=24, color=b.GOLD, bold=True, align=CENTER)
    d.text(s, lab, x + In(0.1), In(6.12), sw - In(0.2), In(0.32), size=11.5, color=b.LIGHT_TEAL, align=CENTER, shrink=True)
d.footer(s, PG(), TOTAL)

# ── 12. Top 10 ITOps products ─────────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "Top 10 ITOps Products: Replace Or Enrich", "Sourced from ISG, IDC, Gartner & PeerSpot 2026 AIOps / observability rankings")
ix = [d.M, d.M + In(1.95), d.M + In(5.2), d.M + In(10.55)]
iw = [In(1.9), In(3.2), In(5.3), In(2.0)]
ihy = In(1.72)
d.rect(s, d.M, ihy, d.CW, In(0.42), b.NAVY, radius=0.04)
for cx, cwd, ht in zip(ix, iw, ["PRODUCT", "WHAT IT DOES", "AGENTIC USE CASE", "VERDICT"]):
    al = CENTER if ht == "VERDICT" else LEFT
    d.text(s, ht, cx + In(0.1), ihy + In(0.08), cwd - In(0.15), In(0.28), size=10.5, color=b.TEAL, bold=True, align=al)
itops = [
    ("Datadog", "Full-stack observability + AIOps", "Agent rides on top via Datadog MCP for autonomous RCA", "ENRICH"),
    ("Dynatrace", "Causal AI (Davis), explainable RCA", "Davis feeds agents deterministic root cause", "ENRICH"),
    ("Splunk (Cisco)", "Observability + SIEM convergence", "Agent queries SPL; AI Assistant; SecOps triage", "ENRICH"),
    ("ServiceNow ITOM", "CMDB-coupled event correlation", "Now Assist + CMDB = the context layer agents need", "ENRICH"),
    ("New Relic", "Consumption-priced APM / AIOps", "Applied Intelligence + NRDB feed agent RCA", "ENRICH"),
    ("Grafana Cloud", "OTel-native dashboards", "SRE Agent on open telemetry; dashboards = audit layer", "ENRICH"),
    ("Elastic Observ.", "Search-powered observability", "Vector search + agent retrieval over logs", "ENRICH"),
    ("PagerDuty", "Incident response / on-call routing", "Agent becomes first responder; routing compresses", "REPLACE"),
    ("BigPanda", "Event correlation / noise reduction", "Agents reason causally natively; correlation erodes", "REPLACE"),
    ("L1 NOC / runbooks", "Tier-1 triage & manual runbooks", "Agent auto-investigates & remediates within policy", "REPLACE"),
]
ry = ihy + In(0.42); rh = In(0.46)
for j, (prod, does, uc, verd) in enumerate(itops):
    vc = V[verd]
    d.rect(s, d.M, ry, d.CW, rh, b.SOFT if j % 2 == 0 else b.WHITE)
    d.rect(s, d.M, ry, In(0.06), rh, vc)
    d.text(s, prod, ix[0] + In(0.12), ry + In(0.11), iw[0] - In(0.18), In(0.26), size=10.5, color=b.INK, bold=True, shrink=True)
    d.text(s, does, ix[1] + In(0.1), ry + In(0.12), iw[1] - In(0.18), In(0.24), size=9.5, color=b.MUTED, shrink=True)
    d.text(s, uc, ix[2] + In(0.1), ry + In(0.12), iw[2] - In(0.18), In(0.24), size=9.5, color=b.INK, shrink=True)
    pill(s, ix[3] + In(0.15), ry + In(0.09), iw[3] - In(0.4), In(0.28), verd, vc, size=10)
    ry += rh
d.footer(s, PG(), TOTAL)

# ── 13. AI SRE deep dive ──────────────────────────────────────────────────────
uc_slide(
    "Autonomous Incident Response (AI SRE)", "Use Case 22-class · enriches your observability + on-call stack",
    "An SRE paged at 2 AM manually correlates telemetry scattered across logs, deploys, and third-party "
    "monitors. RCA routinely takes hours, and on-call can't scale with system complexity.",
    "An AI SRE agent watches the existing stack read-only via MCP, investigates autonomously on every alert, "
    "produces a root-cause analysis before the human arrives, and remediates within a bounded policy envelope.",
    [("hrs → min", "MTTR reduction"), ("50%+", "incidents auto-resolved"), ("up to 35%", "ITOps cost cut")],
    ["Alert fires (PD/Datadog)", "Correlate telemetry", "Causal RCA", "Remediate / escalate"],
    ["AI SRE agent", "MCP to obs tools", "Read-only", "Policy guardrails"],
    ["Datadog, Dynatrace, Splunk", "PagerDuty, ServiceNow", "GitHub / GitLab via MCP"],
    ["AWS DevOps Agent + Datadog MCP", "OpsAI: 50%+ auto-resolved", "NeuBird, Traversal: AI SRE"],
    left_label="ENRICHES", left_color=b.TEAL,
)

# ── 14. Exposure tiers ────────────────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "Exposure Concentrates By Use Case, Not By Vendor", "Agent Replacement Index: 189 categories; 44 scored ≥8; only 3 scored 0")
rows = [
    ("HIGHEST RISK 8–10", b.CORAL, "Sales outreach, cold email, funnel builders, time tracking, scheduling, support tickets", "Visual UI over a task models now do natively"),
    ("REPRICING", b.AMBER, "CRM (~$100B), ITSM (~$15–20B), HCM (~$30–40B)", "Per-seat for reps doing data entry/triage"),
    ("LIVE REPLACEMENT", b.GOLD, "Support, outreach, recruiting, legal, marketing ops, finance/AP, CS", "Well-defined outputs + deterministic workflows"),
    ("RESILIENT", b.TEAL, "ERP, payroll, compliance, regulated vertical SaaS, systems of record", "Data moats, auditability, write access"),
]
ry = In(1.9)
for lab, col, cats, why in rows:
    h = In(1.13)
    card(s, d.M, ry, d.CW, h, b.SOFT)
    d.rect(s, d.M, ry, In(2.5), h, b.NAVY, radius=0.06)
    d.rect(s, d.M, ry, In(0.08), h, col)
    d.text(s, lab, d.M + In(0.2), ry, In(2.2), h, size=13.5, color=col, bold=True, anchor=VA.MIDDLE, shrink=True)
    d.text(s, cats, d.M + In(2.75), ry + In(0.13), d.CW - In(3.0), In(0.6), size=13, color=b.INK, bold=True, shrink=True)
    d.text(s, why, d.M + In(2.75), ry + In(0.7), d.CW - In(3.0), In(0.35), size=11.5, color=b.MUTED, italic=True, shrink=True)
    ry += In(1.25)
d.footer(s, PG(), TOTAL)

# ── 15. The nuance ────────────────────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "Win Trust With The Nuance", "The hybrid model is what operators actually adopt")
panels = [
    ("THE HYPE SAYS", b.CORAL, ["\"Replace all your SaaS with one agent\"", "Per-seat is dead overnight",
                                "$19/mo agent beats every $300 tool"]),
    ("THE DATA SAYS", b.TEAL, ["Selective unbundling — ~65% of SaaS survives", "Agent does the work; dashboard = audit layer",
                               "Hallucination risk gates full autonomy"]),
]
pw = (d.CW - In(0.4)) / 2
for i, (h, col, items) in enumerate(panels):
    x = d.M + i * (pw + In(0.4))
    card(s, x, In(1.95), pw, In(3.0), b.SOFT)
    d.rect(s, x, In(1.95), pw, In(0.55), col, radius=0.06)
    d.text(s, h, x, In(2.06), pw, In(0.34), size=15, color=b.WHITE, bold=True, align=CENTER)
    d.text(s, [{"text": t, "bullet": True, "size": 13.5, "space_before": 11} for t in items],
           x + In(0.25), In(2.7), pw - In(0.5), In(2.1), shrink=True)
d.rect(s, d.M, In(5.25), d.CW, In(1.3), b.NAVY, radius=0.05)
d.text(s, "Position to own", d.M + In(0.3), In(5.4), In(6), In(0.4), size=14, color=b.TEAL, bold=True)
d.text(s, "Tell buyers exactly which use cases to keep, renegotiate, or replace — and prove it with the "
          "build-vs-buy math the \"just build it\" crowd skips.", d.M + In(0.3), In(5.8), d.CW - In(0.6), In(0.65),
       size=14, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, PG(), TOTAL)

# ── 16. Flagship Scorecard ────────────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "Flagship Asset: The Agent Replacement Scorecard", "Grade each use case → keep / renegotiate / replace, with build-vs-buy math")
sx = [d.M, d.M + In(2.7), d.M + In(3.8), d.M + In(5.1), d.M + In(6.3), d.M + In(8.7)]
swid = [In(2.6), In(1.0), In(1.2), In(1.1), In(2.3), In(4.0)]
shead = ["USE CASE", "VOLUME", "DETERMIN.", "DATA MOAT", "VERDICT", "BUILD-VS-BUY"]
hy = In(1.85)
d.rect(s, d.M, hy, d.CW, In(0.46), b.NAVY, radius=0.04)
for cx, cwd, ht in zip(sx, swid, shead):
    d.text(s, ht, cx + In(0.1), hy + In(0.09), cwd - In(0.15), In(0.3), size=11, color=b.TEAL, bold=True,
           align=(CENTER if ht in ("VOLUME", "DETERMIN.", "DATA MOAT", "VERDICT") else LEFT))
SR = [
    ("Support tickets", "H", "H", "L", "REPLACE", b.CORAL, "80 seats → 1 agent + KB"),
    ("Sales outreach", "H", "M", "L", "REPLACE", b.CORAL, "Per-rep seats → 1 agent infra"),
    ("CRM data entry", "H", "M", "M", "RENEGOTIATE", b.AMBER, "Drop seats; keep the system"),
    ("Financial close", "M", "M", "H", "RENEGOTIATE", b.AMBER, "Agent assists; human signs off"),
    ("Backup / archival", "L", "H", "H", "KEEP", b.TEAL, "Not a workflow — infrastructure"),
]
def hml_color(v):
    return {"H": b.TEAL, "M": b.AMBER, "L": b.GRID}[v]
ry = hy + In(0.46); rh = In(0.66)
for j, (uc, vol, det, moat, verd, vc, note) in enumerate(SR):
    d.rect(s, d.M, ry, d.CW, rh, b.SOFT if j % 2 == 0 else b.WHITE)
    d.text(s, uc, sx[0] + In(0.1), ry + In(0.2), swid[0] - In(0.15), In(0.34), size=12.5, color=b.INK, bold=True, shrink=True)
    for ci, val in ((1, vol), (2, det), (3, moat)):
        txtcol = b.NAVY if val != "L" else b.MUTED
        pill(s, sx[ci] + (swid[ci] - In(0.5)) / 2, ry + In(0.18), In(0.5), In(0.3), val, hml_color(val), txt=txtcol, size=12)
    pill(s, sx[4] + In(0.1), ry + In(0.18), swid[4] - In(0.3), In(0.3), verd, vc, size=10.5)
    d.text(s, note, sx[5] + In(0.1), ry + In(0.2), swid[5] - In(0.15), In(0.34), size=11.5, color=b.INK, shrink=True)
    ry += rh
d.text(s, "H / M / L = intensity of each factor; the verdict weighs all three. Illustrative judgment, not measured data. "
          "Low data moat + high volume + high determinism → replace.",
       d.M, ry + In(0.12), d.CW, In(0.5), size=10.5, color=b.MUTED, italic=True, shrink=True)
d.footer(s, PG(), TOTAL)

# ── 17. Content angles ────────────────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "Five Angles That Convert Use Cases To Pipeline", "Each maps to a real buyer question from the threads")
angles = [
    ("01", "Agent Replacement Scorecard", "Grade a buyer's stack use case by use case (keep/renegotiate/replace). Flagship magnet."),
    ("02", "Renewal Leverage 2026", "Turn repricing into a procurement playbook — vendors under margin pressure negotiate."),
    ("03", "What Actually Survives", "Contrarian: system-of-record + data moats compound. Counter-programs the hype."),
    ("04", "Operator Teardown", "Annotate the $15k→$271/mo Reddit swap: what's real, what's underestimated."),
    ("05", "Is Your SaaS Broken For Agents?", "Agent-readiness checklist for founders (the u/yolosollo angle)."),
]
cw3 = (d.CW - In(0.6)) / 3
for i, (num, t, desc) in enumerate(angles):
    col = i % 3; row = i // 3
    x = d.M + col * (cw3 + In(0.3)); y = In(1.95) + row * In(2.3)
    card(s, x, y, cw3, In(2.1), b.SOFT)
    d.rect(s, x, y, In(0.85), In(0.6), b.NAVY, radius=0.08)
    d.text(s, num, x, y + In(0.1), In(0.85), In(0.4), size=20, color=b.GOLD, bold=True, align=CENTER)
    d.text(s, t, x + In(0.95), y + In(0.12), cw3 - In(1.1), In(0.7), size=14.5, color=b.INK, bold=True, shrink=True)
    d.text(s, desc, x + In(0.2), y + In(0.95), cw3 - In(0.4), In(1.0), size=12, color=b.MUTED, shrink=True)
d.footer(s, PG(), TOTAL)

# ── 18. Distribution ──────────────────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "Earn Citation — Don't Plant It", "The line this strategy will not cross")
do = ["Publish long-form on OWN channels (blog / newsletter / LinkedIn) so it ranks and is cited on merit.",
      "Engage Reddit threads transparently, with disclosure when you have a stake — lead with genuine help.",
      "Pull 3–5 attributed verbatim quotes (with links) into the long-form — credit the authors.",
      "Let LLM citation happen because the content is the best answer available."]
dont = ["No covert, disguised-as-organic comments engineered to be lifted by scrapers.",
        "No targeting specific threads with planted brand mentions (\"injection points\").",
        "No coordinated inauthentic behavior — it violates Reddit TOS and breaks trust.",
        "No headless scraping to \"bypass API restrictions\" as a growth tactic."]
pw = (d.CW - In(0.4)) / 2
for i, (h, col, items) in enumerate([("DO — EARN IT", b.TEAL, do), ("DON'T — ASTROTURF", b.CORAL, dont)]):
    x = d.M + i * (pw + In(0.4))
    card(s, x, In(1.95), pw, In(4.4), b.SOFT)
    d.rect(s, x, In(1.95), pw, In(0.55), col, radius=0.06)
    d.text(s, h, x, In(2.06), pw, In(0.34), size=15, color=b.WHITE, bold=True, align=CENTER)
    d.text(s, [{"text": t, "bullet": True, "size": 13, "space_before": 13} for t in items],
           x + In(0.25), In(2.72), pw - In(0.5), In(3.4), shrink=True)
d.footer(s, PG(), TOTAL)

# ── 19. References ────────────────────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "References & Sources", "Current web discovery via Exa · GBrain recall attempted (PGLite lock, unavailable)")
refs = [
    "1. Bain & Company — \"Will Agentic AI Disrupt SaaS?\" (2025-09-23)",
    "2. L.E.K. — \"Revolution or Extinction?\" (2025-06-24)",
    "3. Value Add VC — \"AI Agents Replacing Entire Workflows\" (2026-05-30)",
    "4. every.rocks — \"The SaaSpocalypse Is Here\" (2026-05-25)",
    "5. AgentMarketCap — \"$300B Erased\" (2026-04-06)",
    "6. WhatAreTheBest — \"Agent Replacement Index: 189 cats\" (2026-04-13)",
    "7. MindStudio — \"SaaS Pricing Is Breaking\" (2026-04-15)",
    "8. Coommit — \"Service-as-Software: 8 Categories\" (2026-05-12)",
]
refs2 = [
    "9. DeepSignal — \"AI Is Repricing Software\" (2026-04-06)",
    "10. Built In — \"AI Agents Are Disrupting SaaS\" (2026-03-18)",
    "11. TheAgentTimes — \"Reddit Debate: Builder Economics\" (2026-04-19)",
    "12. Lobster Pack — \"SMBs replacing $500–$20K/mo stacks\" (2026-03-23)",
    "13. Discury — r/SaaS founder-thread digests (790+)",
    "14. Intellectia — \"Will AI Disrupt SaaS? 2026\" (Gartner 35%)",
    "15. inmydata — \"Business Software in the Agentic Era\" (2026-03-06)",
    "Communities: r/SaaS, r/artificial (quotes attributed).",
]
refs3 = [
    "IT OPERATIONS + EVIDENCE BASE",
    "16. ISG Buyers Guide — AIOps Platforms 2026",
    "17. ISG Buyers Guide — IT Observability Platforms 2026",
    "18. IDC MarketScape — Worldwide AIOps 2026",
    "19. Gartner — MQ for Observability Platforms",
    "20. IBM — \"Observability in the Agentic Era\" (2026-04-17)",
    "21. AWS — \"DevOps Agent + Datadog MCP, GA\" (2026-06-18)",
    "22. Guideflow Top-10 AIOps; PeerSpot; OpsAI; NeuBird; Traversal",
    "23. Google Cloud — \"1,302 Real-World Gen AI Use Cases\" (2026-04-22) — Top-25 evidence base",
]
colw = (d.CW - In(0.8)) / 3
def refcol(items, x, lead=False):
    runs = []
    for i, t in enumerate(items):
        if lead and i == 0:
            runs.append({"text": t, "size": 10.5, "space_before": 0, "color": b.ACCENT, "bold": True})
        else:
            runs.append({"text": t, "size": 10.5, "space_before": 6})
    d.text(s, runs, x, In(1.95), colw, In(4.8), shrink=True)
refcol(refs, d.M)
refcol(refs2, d.M + colw + In(0.4))
refcol(refs3, d.M + 2 * (colw + In(0.4)), lead=True)
d.footer(s, PG(), TOTAL)

# ── 20. Next steps ────────────────────────────────────────────────────────────
s = d.slide(fill=b.NAVY)
d.text(s, "NEXT STEPS", d.M, In(0.7), In(6), In(0.4), size=15, color=b.TEAL, bold=True)
d.text(s, "From the Top 25 to a published asset", d.M, In(1.2), In(11), In(0.8), size=32, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, In(2.1), In(1.6), In(0.05), b.TEAL)
steps = [
    ("1", "Build the Scorecard", "Grade the Top 25 (keep/renegotiate/replace) with build-vs-buy math."),
    ("2", "Add positioning (optional)", "Name a real brand/offer and fold in honest positioning + a CTA."),
    ("3", "Embed the proof", "Drop the named Google deployments + Reddit quotes into the long-form."),
    ("4", "Ship on owned channels", "Publish, then engage relevant threads transparently. No planted comments."),
]
sy = In(2.5)
for num, t, desc in steps:
    d.rect(s, d.M, sy, In(0.6), In(0.6), b.TEAL, radius=0.5)
    d.text(s, num, d.M, sy + In(0.08), In(0.6), In(0.44), size=20, color=b.NAVY, bold=True, align=CENTER)
    d.text(s, t, d.M + In(0.85), sy + In(0.02), In(4.5), In(0.5), size=16, color=b.WHITE, bold=True, shrink=True)
    d.text(s, desc, d.M + In(0.85), sy + In(0.5), In(11), In(0.4), size=13, color=b.LIGHT_TEAL, shrink=True)
    sy += In(1.05)
d.footer(s, PG(), TOTAL, dark=True)

d.save(OUT)
print("SAVED", OUT, "· pages used:", _pgc[0])
