#!/usr/bin/env python3
"""Branded PPTX deck for the whole gamut of agentic opportunity work."""

import sys
from pathlib import Path

sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")

from pptxkit import Deck, Inches, PP_ALIGN

BASE = Path("/home/shekerk/content-ideas/runs/2026-06-26-agentic-opportunity-blueprints")
OUT = BASE / "agentic-opportunity-gamut-reviewed-draft.pptx"

d = Deck(footer="Agentic Opportunity Gamut · Skill-Spine Portfolio Deck · 2026-06-26")
b = d.b
C = PP_ALIGN.CENTER
TOTAL = 14


def card(s, x, y, w, h, title, lines, accent=None):
    accent = accent or b.TEAL
    d.rect(s, x, y, w, h, b.WHITE, radius=0.06, shadow=True)
    d.rect(s, x, y, Inches(0.08), h, accent)
    d.text(s, title, x + Inches(0.18), y + Inches(0.12), w - Inches(0.32), Inches(0.34), size=13.5, color=b.NAVY, bold=True, shrink=True)
    if lines:
        d.text(s, [{"text": t, "size": 10.5, "space_before": 3} for t in lines], x + Inches(0.18), y + Inches(0.50), w - Inches(0.3), h - Inches(0.58), color=b.INK, shrink=True)


def section_header(s, title, subtitle):
    d.rect(s, d.M, Inches(0.32), d.CW, Inches(0.05), b.TEAL)
    d.text(s, title, d.M, Inches(0.52), d.CW, Inches(0.34), size=18, color=b.NAVY, bold=True, shrink=True)
    d.text(s, subtitle, d.M, Inches(0.9), d.CW, Inches(0.22), size=10.5, color=b.MUTED, shrink=True)


def pill(s, x, y, w, h, text, fill, text_color=b.WHITE):
    d.rect(s, x, y, w, h, fill, radius=0.16, shadow=False)
    d.text(s, text, x, y + Inches(0.06), w, h - Inches(0.04), size=10.5, color=text_color, bold=True, align=C, shrink=True)


def stat(s, x, y, w, h, num, label, accent=b.TEAL):
    d.rect(s, x, y, w, h, b.NAVY, radius=0.06, shadow=True)
    d.rect(s, x, y, Inches(0.08), h, accent)
    d.text(s, num, x, y + Inches(0.18), w, Inches(0.45), size=27, color=b.GOLD, bold=True, align=C, shrink=True)
    d.text(s, label, x + Inches(0.12), y + Inches(0.72), w - Inches(0.24), h - Inches(0.82), size=10.5, color=b.WHITE, align=C, shrink=True)


def grid(n, gap=0.22, left=None, total_w=None):
    left = d.M if left is None else left
    total_w = d.CW if total_w is None else total_w
    g = Inches(gap)
    w = (total_w - g * (n - 1)) / n
    return [(left + int((w + g) * i), w) for i in range(n)]


# 1 — Cover
s = d.slide(fill=b.NAVY)
d.rect(s, Inches(11.55), 0, Inches(1.8), d.H, b.NAVY_2)
d.rect(s, Inches(11.49), 0, Inches(0.06), d.H, b.TEAL)
d.text(s, "REVIEWED PORTFOLIO DECK", d.M, Inches(1.25), Inches(9), Inches(0.35), size=13, color=b.TEAL, bold=True)
d.text(s, "The Whole Gamut of\nAgentic Opportunity", d.M, Inches(1.9), Inches(10.2), Inches(1.6), size=40, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(3.62), Inches(1.55), Inches(0.06), b.TEAL)
d.text(s, "A 10-skill operating system for turning market gaps into implementation-ready opportunity portfolios.", d.M, Inches(3.86), Inches(10.1), Inches(0.55), size=18, color=b.LIGHT_TEAL, bold=True, shrink=True)
for i, chip in enumerate(["52 reviewed opportunities", "10 skill prompts", "Whole-gamut portfolio"]):
    cw = Inches(3.3)
    pill(s, d.M + int((cw + Inches(0.2)) * i), Inches(5.72), cw, Inches(0.42), chip, b.NAVY_2, b.TEAL)
d.footer(s, 1, TOTAL, dark=True)

# 2 — Executive summary
s = d.slide(fill=b.WHITE)
section_header(s, "52 opportunities now form a portfolio", "Executive summary")
d.rect(s, d.M, Inches(1.45), d.CW, Inches(0.68), b.NAVY, radius=0.05)
d.text(s, "BLUF: the market is not buying isolated ideas. It is buying a repeatable operating system for deciding whether an opportunity is real, scoping it, architecting it, pricing it, validating it, and shipping it in 30 days.", d.M + Inches(0.22), Inches(1.57), d.CW - Inches(0.44), Inches(0.45), size=13.5, color=b.WHITE, bold=True, shrink=True)
cols = grid(3)
cards = [
    ("What changed", ["We no longer have sketches.", "We have 52 reviewed opportunities.", "Every one maps to the same 10-skill spine."], b.CORAL),
    ("What the buyer gets", ["A decision flow they can show internally.", "A scope that can survive delivery.", "A portfolio that spans the whole gamut."], b.TEAL),
    ("Why it matters", ["The skill prompts replace expensive discovery.", "The deck proves the operating model.", "The appendix proves coverage."], b.GOLD),
]
for (x, w), (title, body, ac) in zip(cols, cards):
    card(s, x, Inches(2.3), w, Inches(2.95), title, body, accent=ac)
stat(s, d.M, Inches(5.45), Inches(4.05), Inches(0.9), "52", "opportunities", accent=b.TEAL)
stat(s, d.M + Inches(4.25), Inches(5.45), Inches(4.05), Inches(0.9), "10", "skill prompts", accent=b.GOLD)
stat(s, d.M + Inches(8.55), Inches(5.45), Inches(2.9), Inches(0.9), "0", "draft-level", accent=b.CORAL)
d.footer(s, 2, TOTAL)

# 3 — Skill spine
s = d.slide(fill=b.WHITE)
section_header(s, "The 10 skills are the operating system", "The deck flow follows this spine")
rows = [
    ("1", "Problem-solution fit", "Is the problem real?"),
    ("2", "30-day scope", "What proves the hypothesis?"),
    ("3", "Architecture", "What stack actually ships?"),
    ("4", "Build vs buy", "What should be custom?"),
    ("5", "ROI", "Why does the buyer pay now?"),
    ("6", "Competitors", "Who blocks the sale?"),
    ("7", "Acceptance criteria", "What counts as done?"),
    ("8", "Data architecture", "Where is the source of truth?"),
    ("9", "Deployment", "How do we launch safely?"),
    ("10", "Iteration", "What improves after launch?"),
]
for i, (idx, title, body) in enumerate(rows):
    x, w = grid(2)[i % 2]
    y = Inches(1.55 + (i // 2) * 0.82)
    d.rect(s, x, y, w, Inches(0.68), b.SOFT, radius=0.06)
    d.rect(s, x, y, Inches(0.09), Inches(0.68), b.TEAL if i % 2 == 0 else b.GOLD)
    pill(s, x + Inches(0.16), y + Inches(0.12), Inches(0.34), Inches(0.24), idx, b.NAVY, b.WHITE)
    d.text(s, title, x + Inches(0.58), y + Inches(0.1), Inches(1.9), Inches(0.24), size=12.4, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, x + Inches(2.3), y + Inches(0.12), w - Inches(2.45), Inches(0.22), size=10.5, color=b.INK, shrink=True)
d.footer(s, 3, TOTAL)

skills = [
    ("Skill #1 · Problem-Solution Fit Validation", "This replaces the diagnostic phase.", ["Who specifically has this problem?", "When did they last face it and what did it cost?", "What are they doing today to work around it?", "Why would they switch?", "Would they pay, and can we reach 100 in 30 days?"], b.TEAL),
    ("Skill #2 · 30-Day Scope Definition", "This replaces the scope doc phase.", ["What is the validated problem?", "What is the one thing the MVP must prove?", "What stays out of scope?", "What realistic time budget exists?", "What are the 4 weekly milestones?"], b.GOLD),
    ("Skill #3 · Tech Stack + Architecture Design", "This replaces the architecture phase.", ["What stack is boring and shippable?", "What is the database schema?", "What APIs and env vars are required?", "What auth and integration choices are locked in?", "What forces reconsideration?"], b.CORAL),
    ("Skill #4 · Build vs Buy Decision Matrix", "This replaces the hidden SOW analysis.", ["For each feature: build, buy, or hybrid?", "What is the 3-year cost?", "Where does lock-in matter?", "What SaaS spend is avoidable?", "What is core to the moat?"], b.AMBER),
    ("Skill #5 · MVP ROI Business Case", "This is the buyer's payback logic.", ["What is the current-state cost?", "What is the monthly agent cost?", "What payback case is downside / base / upside?", "What price can the buyer stomach?", "If breakeven is too far out, kill it."], b.TEAL),
    ("Skill #6 · Competitor Product Teardown", "This is the market map.", ["Who are the 5-10 incumbents?", "What do they sell?", "Where are they strong and weak?", "Which 2 are direct threats?", "What must we deliberately not build?"], b.GOLD),
    ("Skill #7 · Acceptance Criteria + Test Plan", "This defines shipped.", ["What are the user stories?", "What are the testable criteria?", "What are the edge cases?", "What is out of scope for each feature?", "How does QA verify it fast?"], b.CORAL),
    ("Skill #8 · Data Architecture Lite", "This is the data contract.", ["What are the sources?", "Where does each data domain live?", "What is the source of truth?", "What analytics events exist from day 1?", "What are the guardrails?"], b.AMBER),
    ("Skill #9 · Deployment Sequencing", "This is the launch plan.", ["What must be true before deploy?", "What does staging look like?", "What is the smoke test?", "What is the rollback path?", "What cannot fail silently?"], b.TEAL),
    ("Skill #10 · Post-Launch Iteration Plan", "This is the 30-day operating loop.", ["What are the 3 metrics?", "What counts as bugs vs quick wins?", "What gets built in week 2 and week 3?", "What are the pivot signals?", "What must not be added in week 1?"], b.GOLD),
]

for i, (title, subtitle, body, ac) in enumerate(skills):
    s = d.slide(fill=b.WHITE)
    section_header(s, title, subtitle)
    card(s, d.M, Inches(1.65), Inches(4.0), Inches(3.25), "The prompt does", body[:3], accent=ac)
    card(s, d.M + Inches(4.2), Inches(1.65), Inches(4.0), Inches(3.25), "Where the operator is sharper", body[3:], accent=b.NAVY_2 if ac != b.NAVY_2 else b.TEAL)
    card(s, d.M + Inches(8.4), Inches(1.65), Inches(3.15), Inches(3.25), "What to expect", ["A decision memo.", "A scope artifact.", "A build-ready input."], accent=b.CORAL)
    d.rect(s, d.M, Inches(5.15), d.CW, Inches(0.9), b.NAVY, radius=0.05)
    d.text(s, "Use this skill before moving to the next one; each prompt tightens the build contract.", d.M + Inches(0.25), Inches(5.31), d.CW - Inches(0.5), Inches(0.45), size=14, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 4 + i, TOTAL)

# 14 — Portfolio gamut
s = d.slide(fill=b.WHITE)
section_header(s, "All 52 reviewed opportunities are represented", "Portfolio gamut")
cluster_cards = [
    ("Customer ops", ["Conversational Support", "Contact Center Agent Assist", "Messaging Channel Chatbot", "In-Product Owner Assistant"], b.TEAL),
    ("Risk / compliance", ["KYC/AML Onboarding", "Prior Authorization", "Compliance and Audit", "Fraud and Risk Detection", "Agentic Auto-remediation"], b.GOLD),
    ("Finance / revops", ["Deal Desk Pricing", "Commission Dispute Resolution", "Financial Report Reconciliation", "Forecasting / Predictive Ops"], b.CORAL),
    ("Docs / extraction", ["Lease Abstraction", "Bill of Lading Extraction", "Document AI", "Summarization / Drafting", "Legal / Tax Synthesis"], b.AMBER),
    ("Commercial growth", ["AI Shopping", "Ad / Creative Generation", "Personalized Marketing", "Influencer Orchestration", "CRM Hygiene"], b.TEAL),
    ("Operations / supply chain", ["Freight Routing", "Inventory Rerouting", "Supplier Disputes", "Retail Reconciliation", "Maintenance Orchestration"], b.GOLD),
]
for i, (title, items, ac) in enumerate(cluster_cards):
    x, w = grid(3, gap=0.22)[i % 3]
    y = Inches(1.55 + (i // 3) * 2.2)
    card(s, x, y, w, Inches(1.9), title, items[:4], accent=ac)
d.footer(s, 14, TOTAL)

d.save(str(OUT))
print(OUT)
