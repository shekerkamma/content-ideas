#!/usr/bin/env python3
"""Builder: Agentic AI vs. SaaS — content strategy deck. Branded pptxkit."""
import sys
sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, Inches, Pt, PP_ALIGN
from pptx.enum.text import MSO_ANCHOR

OUT = "/home/shekerk/content-ideas/runs/2026-06-22-agentic-ai-vs-saas-reddit-strategy/agentic-ai-vs-saas-strategy-draft.pptx"
d = Deck(footer="Agentic AI vs. SaaS · Reddit + Market Intelligence | 2026-06-22")
b = d.b
W = d.W
TOTAL = 10

def card(s, x, y, w, h, fill, line=None):
    d.rect(s, x, y, w, h, fill, line=line, radius=0.06, shadow=True)

def head(s, title, subtitle=None):
    # shrink-enabled header: long titles auto-fit the band (no overflow flag)
    d.text(s, title, d.M, Inches(0.42), d.CW, Inches(0.66), size=30, color=b.NAVY,
           bold=True, shrink=True)
    d.rect(s, d.M, Inches(1.12), Inches(1.45), Inches(0.05), b.TEAL)
    if subtitle:
        d.text(s, subtitle, d.M, Inches(1.26), d.CW, Inches(0.4), size=14.5, color=b.MUTED, shrink=True)

# ── 1. Cover ────────────────────────────────────────────────────────────────
s = d.slide(fill=b.NAVY)
d.rect(s, W - Inches(2.4), 0, Inches(2.4), Inches(7.5), b.NAVY_2)
d.rect(s, W - Inches(2.4), 0, Inches(0.06), Inches(7.5), b.TEAL)
d.text(s, "MARKET INTELLIGENCE · CONTENT STRATEGY", d.M, Inches(0.95), Inches(8), Inches(0.4),
       size=15, color=b.TEAL, bold=True)
d.text(s, "Agentic AI vs. SaaS: The Content Opportunity in the SaaSpocalypse", d.M, Inches(1.55),
       Inches(9.6), Inches(1.9), size=42, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(3.7), Inches(1.6), Inches(0.05), b.TEAL)
d.text(s, "What Reddit builders and the market are saying about AI agents replacing SaaS — "
          "and the honest content angles that win buyer trust.", d.M, Inches(3.95), Inches(9.4),
       Inches(0.9), size=16, color=b.LIGHT_TEAL, shrink=True)
for i, chip in enumerate(["r/SaaS + r/artificial", "Bain · Gartner · L.E.K.", "15 cited sources"]):
    cx = d.M + Inches(i * 3.15)
    d.rect(s, cx, Inches(5.4), Inches(2.95), Inches(0.62), b.NAVY_2, line=b.TEAL, radius=0.12)
    d.text(s, chip, cx, Inches(5.55), Inches(2.95), Inches(0.36), size=13, color=b.WHITE,
           bold=True, align=PP_ALIGN.CENTER)
d.text(s, "Note: authentic strategy — no covert Reddit insertions / astroturfing.", d.M,
       Inches(6.55), Inches(10), Inches(0.4), size=12, color=b.MUTED, italic=True)

# ── 2. Executive summary (BLUF) ───────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "SaaSpocalypse: Real And Repriced",
         "BLUF · Situation → Insight → Recommendation")
d.rect(s, d.M, Inches(1.75), d.CW, Inches(0.9), b.NAVY, radius=0.05)
d.text(s, "In 5 months of 2026 the market repriced seat-based software: Salesforce & ServiceNow each "
          "−~30% YTD, ~$300B vendor market cap erased. The builder community has a plain-language thesis; "
          "analysts have the framework. The gap is a trustworthy operator voice.",
       d.M + Inches(0.25), Inches(1.92), d.CW - Inches(0.5), Inches(0.6), size=14.5,
       color=b.WHITE, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
cols = [
    ("SITUATION", b.MUTED, ["\"SaaSpocalypse\" coined by investors", "Reddit: 790+ r/SaaS founder threads",
                            "\"The End of Software\": 88 upvotes"]),
    ("INSIGHT", b.TEAL, ["Disruption = selective unbundling, not death", "Gartner: 35% of point SaaS gone by 2030 (65% survives)",
                         "Per-seat breaks; system-of-record compounds"]),
    ("RECOMMENDATION", b.GOLD, ["Publish the buyer-side \"keep/replace/renegotiate\" framework",
                                "Lead with nuance, not hype or denial", "Distribute on owned channels; cite real quotes"]),
]
cw = (d.CW - Inches(0.6)) / 3
for i, (h, col, items) in enumerate(cols):
    x = d.M + i * (cw + Inches(0.3))
    card(s, x, Inches(2.85), cw, Inches(2.95), b.SOFT)
    d.rect(s, x, Inches(2.85), cw, Inches(0.5), b.NAVY, radius=0.06)
    d.text(s, h, x, Inches(2.95), cw, Inches(0.32), size=13, color=col, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, [{"text": t, "bullet": True, "size": 12.5, "space_before": 8} for t in items],
           x + Inches(0.22), Inches(3.55), cw - Inches(0.44), Inches(2.1), shrink=True)
d.rect(s, d.M, Inches(6.05), d.CW, Inches(0.62), b.GOLD, radius=0.05)
d.text(s, "THE ASK:  Build the \"Agent Replacement Scorecard\" as the flagship asset — a pre-sales magnet "
          "for build-vs-buy conversations.", d.M + Inches(0.25), Inches(6.18), d.CW - Inches(0.5),
       Inches(0.4), size=13.5, color=b.NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
d.footer(s, 2, TOTAL)

# ── 3. Demand landscape (KPI grid) ───────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "Operators Are Already Swapping Stacks",
         "What the conversation looks like right now")
kpis = [
    ("$300B", "vendor market cap erased", "SaaSpocalypse, 2026 YTD"),
    ("98%", "cost cut in one Reddit case", "$15k/mo ops+mktg → $271/mo"),
    ("790+", "r/SaaS founder threads", "indexed on AI-vs-SaaS impact"),
    ("35%", "point SaaS replaced by 2030", "Gartner — 65% survives, evolved"),
]
gw = (d.CW - Inches(0.9)) / 4
for i, (n, lab, note) in enumerate(kpis):
    x = d.M + i * (gw + Inches(0.3))
    card(s, x, Inches(1.95), gw, Inches(2.3), b.NAVY)
    d.text(s, n, x, Inches(2.25), gw, Inches(0.8), size=38, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, lab, x + Inches(0.12), Inches(3.15), gw - Inches(0.24), Inches(0.6), size=13.5,
           color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, note, x + Inches(0.12), Inches(3.72), gw - Inches(0.24), Inches(0.45), size=11,
           color=b.LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)
d.rect(s, d.M, Inches(4.6), d.CW, Inches(2.0), b.SOFT, radius=0.05)
d.text(s, "The pattern operators describe", d.M + Inches(0.3), Inches(4.78), Inches(8), Inches(0.4),
       size=15, color=b.INK, bold=True)
pts = [
    "Sweet spot = workflow-heavy, logic-light SaaS: support triage, social monitoring, lead routing, scheduling, basic reporting.",
    "Klarna AI ≈ 700 support reps; Salesforce Agentforce 5,000+ deals in 6 months; seat reductions 30–40% (up to 80–90% in support).",
    "Reality check from the same threads: maintenance, security patching, variable API cost, and the builder's own time are underestimated.",
]
d.text(s, [{"text": t, "bullet": True, "size": 13, "space_before": 9} for t in pts],
       d.M + Inches(0.3), Inches(5.2), d.CW - Inches(0.6), Inches(1.3), shrink=True)
d.footer(s, 3, TOTAL)

# ── 4. Verbatim Reddit sentiment ─────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "The Builder Thesis, In Their Words", "Verbatim, attributed — cited, never planted")
quotes = [
    ("\"Classic SaaS is fundamentally a workaround. Nobody wants a dashboard. Nobody wants to "
     "'manage their pipeline.'\"", "u/Lyassou · r/SaaS"),
    ("\"Your customers are going to start sending AI agents to do tasks in your product… your SaaS "
     "is probably broken for agents.\"", "u/yolosollo · r/SaaS"),
    ("\"Analysts ask about our AI strategy on every earnings call — how AI agents will disrupt our "
     "business model.\"  (23% revenue growth, stock −45%)", "u/Stock-Parking-411 · r/SaaS"),
]
qy = Inches(1.95)
for q, who in quotes:
    card(s, d.M, qy, d.CW, Inches(1.45), b.SOFT)
    d.rect(s, d.M, qy, Inches(0.08), Inches(1.45), b.TEAL)
    d.text(s, q, d.M + Inches(0.35), qy + Inches(0.18), d.CW - Inches(0.7), Inches(0.78),
           size=16, color=b.INK, italic=True, shrink=True)
    d.text(s, who, d.M + Inches(0.35), qy + Inches(1.02), d.CW - Inches(0.7), Inches(0.32),
           size=12.5, color=b.ACCENT, bold=True)
    qy += Inches(1.62)
d.footer(s, 4, TOTAL)

# ── 5. Category exposure scorecard ───────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "UI-Over-Data Loses; Records Compound",
         "Agent Replacement Index: 189 categories; 44 scored ≥8; only 3 scored 0")
rows = [
    ("HIGHEST RISK 8–10", b.CORAL, "Sales outreach, cold email, funnel builders, time tracking, scheduling, task lists, support tickets",
     "Visual UI over a task models now do natively"),
    ("REPRICING", b.AMBER, "CRM (~$100B), ITSM (~$15–20B), HCM (~$30–40B)",
     "Per-seat for reps doing data entry/triage; 65% of rep time is non-selling"),
    ("LIVE REPLACEMENT", b.GOLD, "Support, outreach, recruiting, legal, marketing ops, IT helpdesk, finance/AP, CS health",
     "Well-defined outputs + deterministic workflows"),
    ("RESILIENT", b.TEAL, "ERP, payroll, compliance, regulated vertical SaaS, backup/archival, systems of record",
     "Data moats, auditability, write access — agents need them"),
]
ry = Inches(1.9)
for lab, col, cats, why in rows:
    h = Inches(1.13)
    card(s, d.M, ry, d.CW, h, b.SOFT)
    d.rect(s, d.M, ry, Inches(2.5), h, b.NAVY, radius=0.06)
    d.rect(s, d.M, ry, Inches(0.08), h, col)
    d.text(s, lab, d.M + Inches(0.2), ry, Inches(2.2), h, size=13.5, color=col, bold=True,
           anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.text(s, cats, d.M + Inches(2.75), ry + Inches(0.13), d.CW - Inches(3.0), Inches(0.6),
           size=13, color=b.INK, bold=True, shrink=True)
    d.text(s, why, d.M + Inches(2.75), ry + Inches(0.7), d.CW - Inches(3.0), Inches(0.35),
           size=11.5, color=b.MUTED, italic=True, shrink=True)
    ry += Inches(1.25)
d.footer(s, 5, TOTAL)

# ── 6. The nuance that wins trust ────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "Win Trust With The Nuance",
         "The hybrid model is what operators actually adopt")
panels = [
    ("THE HYPE SAYS", b.CORAL, ["\"Replace all your SaaS with one agent\"",
                                "Per-seat is dead overnight", "$19/mo agent beats every $300 tool"]),
    ("THE DATA SAYS", b.TEAL, ["Selective unbundling, not destruction (65% survives)",
                               "Agent does the work; dashboard becomes the audit/verification layer",
                               "Hallucination risk gates autonomy — the \"cockpit\" stays"]),
]
pw = (d.CW - Inches(0.4)) / 2
for i, (h, col, items) in enumerate(panels):
    x = d.M + i * (pw + Inches(0.4))
    card(s, x, Inches(1.95), pw, Inches(3.0), b.SOFT)
    d.rect(s, x, Inches(1.95), pw, Inches(0.55), col, radius=0.06)
    d.text(s, h, x, Inches(2.06), pw, Inches(0.34), size=15, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, [{"text": t, "bullet": True, "size": 13.5, "space_before": 11} for t in items],
           x + Inches(0.25), Inches(2.7), pw - Inches(0.5), Inches(2.1), shrink=True)
d.rect(s, d.M, Inches(5.25), d.CW, Inches(1.3), b.NAVY, radius=0.05)
d.text(s, "Position to own", d.M + Inches(0.3), Inches(5.4), Inches(6), Inches(0.4), size=14,
       color=b.TEAL, bold=True)
d.text(s, "Be the operator who tells buyers exactly which line items to keep, renegotiate, or replace — "
          "and proves it with the build-vs-buy math the \"just build it\" crowd skips.",
       d.M + Inches(0.3), Inches(5.8), d.CW - Inches(0.6), Inches(0.65), size=14, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, 6, TOTAL)

# ── 7. Content angles to own ─────────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "Five Angles That Convert To Pipeline",
         "Each maps to a real buyer question from the threads")
angles = [
    ("01", "Agent Replacement Scorecard", "Buyer-side keep/renegotiate/replace framework on the Bain 2×2 + Replacement Index. Flagship magnet."),
    ("02", "Renewal Leverage 2026", "Turn the SaaSpocalypse into a procurement playbook — vendors under margin pressure negotiate."),
    ("03", "What Actually Survives", "Contrarian: system-of-record + data moats compound. Counter-programs the hype."),
    ("04", "Operator Teardown", "Annotate the $15k→$271/mo Reddit story: what's real, what's underestimated."),
    ("05", "Is Your SaaS Broken For Agents?", "Agent-readiness checklist for founders (the u/yolosollo angle)."),
]
cw3 = (d.CW - Inches(0.6)) / 3
for i, (n, t, desc) in enumerate(angles):
    col = i % 3; row = i // 3
    x = d.M + col * (cw3 + Inches(0.3))
    y = Inches(1.95) + row * Inches(2.3)
    card(s, x, y, cw3, Inches(2.1), b.SOFT)
    d.rect(s, x, y, Inches(0.85), Inches(0.6), b.NAVY, radius=0.08)
    d.text(s, n, x, y + Inches(0.1), Inches(0.85), Inches(0.4), size=20, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, t, x + Inches(0.95), y + Inches(0.12), cw3 - Inches(1.1), Inches(0.7), size=14.5,
           color=b.INK, bold=True, shrink=True)
    d.text(s, desc, x + Inches(0.2), y + Inches(0.95), cw3 - Inches(0.4), Inches(1.0), size=12,
           color=b.MUTED, shrink=True)
d.footer(s, 7, TOTAL)

# ── 8. Distribution — the honest way ─────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "Earn Citation — Don't Plant It",
         "The line this strategy will not cross")
do = ["Publish long-form on OWN channels (blog / newsletter / LinkedIn) so it ranks and is cited on merit.",
      "Engage Reddit threads transparently, with disclosure when you have a stake — lead with genuine help.",
      "Pull 3–5 attributed verbatim quotes (with links) into the long-form — credit the authors.",
      "Let LLM citation happen because the content is the best answer available."]
dont = ["No covert, disguised-as-organic comments engineered to be lifted by scrapers.",
        "No targeting specific threads with planted brand mentions (\"injection points\").",
        "No coordinated inauthentic behavior — it violates Reddit TOS and breaks trust.",
        "No headless scraping to \"bypass API restrictions\" as a growth tactic."]
pw = (d.CW - Inches(0.4)) / 2
for i, (h, col, items) in enumerate([("DO — EARN IT", b.TEAL, do), ("DON'T — ASTROTURF", b.CORAL, dont)]):
    x = d.M + i * (pw + Inches(0.4))
    card(s, x, Inches(1.95), pw, Inches(4.4), b.SOFT)
    d.rect(s, x, Inches(1.95), pw, Inches(0.55), col, radius=0.06)
    d.text(s, h, x, Inches(2.06), pw, Inches(0.34), size=15, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, [{"text": t, "bullet": True, "size": 13, "space_before": 13} for t in items],
           x + Inches(0.25), Inches(2.72), pw - Inches(0.5), Inches(3.4), shrink=True)
d.footer(s, 8, TOTAL)

# ── 9. References & Sources ──────────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
head(s, "References & Sources", "Current web discovery via Exa · GBrain recall attempted (PGLite lock, unavailable)")
refs = [
    "1. Bain & Company — \"Will Agentic AI Disrupt SaaS?\" (2025-09-23)",
    "2. L.E.K. — \"Revolution or Extinction? Rethinking SaaS in the Age of Agentic AI\" (2025-06-24)",
    "3. Value Add VC (T. Cohen) — \"How AI Agents Are Replacing Entire Workflows\" (2026-05-30)",
    "4. every.rocks — \"The SaaSpocalypse Is Here\" (2026-05-25)",
    "5. AgentMarketCap — \"The Agent Layer Eating SaaS: $300B Erased\" (2026-04-06)",
    "6. WhatAreTheBest — \"Agent Replacement Index: 189 categories\" (2026-04-13)",
    "7. MindStudio — \"SaaS Pricing Is Breaking: Per-Seat in the AI Agent Era\" (2026-04-15)",
    "8. Coommit — \"Service-as-Software: 8 SaaS Categories AI Agents Replace\" (2026-05-12)",
]
refs2 = [
    "9. DeepSignal — \"AI Is Repricing Software: Which Moats Survive\" (2026-04-06)",
    "10. Built In — \"AI Agents Are Disrupting SaaS\" (2026-03-18)",
    "11. TheAgentTimes — \"Reddit Debate: Builder Economics of Replacing SaaS\" (2026-04-19)",
    "12. Lobster Pack — \"SMBs replacing $500–$20K/mo SaaS stacks\" (2026-03-23)",
    "13. Discury — r/SaaS founder-thread digests (790+ indexed)",
    "14. Intellectia — \"Will AI Disrupt SaaS? 2026\" (Gartner 35%-by-2030) (2026-02-25)",
    "15. inmydata — \"How Business Software Survives the Agentic Era\" (2026-03-06)",
    "Communities: r/SaaS, r/artificial (quotes attributed to public usernames).",
]
colw = (d.CW - Inches(0.4)) / 2
d.text(s, [{"text": t, "size": 12.5, "space_before": 9} for t in refs], d.M, Inches(1.95),
       colw, Inches(4.6), shrink=True)
d.text(s, [{"text": t, "size": 12.5, "space_before": 9} for t in refs2], d.M + colw + Inches(0.4),
       Inches(1.95), colw, Inches(4.6), shrink=True)
d.footer(s, 9, TOTAL)

# ── 10. Next steps ───────────────────────────────────────────────────────────
s = d.slide(fill=b.NAVY)
d.text(s, "NEXT STEPS", d.M, Inches(0.7), Inches(6), Inches(0.4), size=15, color=b.TEAL, bold=True)
d.text(s, "From intelligence to published asset", d.M, Inches(1.2), Inches(11), Inches(0.8),
       size=32, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(2.1), Inches(1.6), Inches(0.05), b.TEAL)
steps = [
    ("1", "Draft the flagship", "Build the Agent Replacement Scorecard (keep/renegotiate/replace) as the lead asset."),
    ("2", "Add positioning (optional)", "Name a real brand/offer and fold in honest positioning + a CTA."),
    ("3", "Embed the proof", "Drop the 3–5 attributed Reddit quotes (with links) into the long-form."),
    ("4", "Ship on owned channels", "Publish, then engage relevant threads transparently. No planted comments."),
]
sy = Inches(2.5)
for n, t, desc in steps:
    d.rect(s, d.M, sy, Inches(0.6), Inches(0.6), b.TEAL, radius=0.5)
    d.text(s, n, d.M, sy + Inches(0.08), Inches(0.6), Inches(0.44), size=20, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, t, d.M + Inches(0.85), sy + Inches(0.02), Inches(4), Inches(0.5), size=16, color=b.WHITE, bold=True, shrink=True)
    d.text(s, desc, d.M + Inches(0.85), sy + Inches(0.5), Inches(11), Inches(0.4), size=13, color=b.LIGHT_TEAL, shrink=True)
    sy += Inches(1.05)
d.footer(s, 10, TOTAL, dark=True)

d.save(OUT)
print("SAVED", OUT)
