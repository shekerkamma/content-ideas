#!/usr/bin/env python3
"""5 Executive Summary slides — one per industry.

Each slide condenses 2 use cases into: headline stat, UC1/UC2 cards with
key metrics + implementation gist, buyer profile, and revenue model.
"""
from __future__ import annotations

import sys
from pathlib import Path

BRANDED_SKILL = Path("/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(BRANDED_SKILL))

from pptxkit import Deck, Inches, PP_ALIGN, MSO_ANCHOR  # type: ignore

RUN_DIR = Path(__file__).resolve().parent
OUT = RUN_DIR / "executive-industry-summaries-draft.pptx"

INDUSTRIES = [
    {
        "num": "01",
        "name": "Manufacturing",
        "score": "32/35 GO",
        "revenue": "$5-10K/mo per client",
        "headline": "From Reactive to Predictive — Two AI Wedges That Ship in Weeks",
        "subtitle": "Predictive maintenance + visual quality inspection — production-proven, MCP-connected, SAP-integrated",
        "uc1": {
            "id": "UC-01",
            "title": "Predictive Maintenance",
            "company": "Unilever (Brazil)",
            "stats": [
                ("$2.3M", "saved annually"),
                ("92%", "prediction accuracy"),
                ("6.5mo", "payback period"),
            ],
            "gist": [
                "Sensor data (MQTT/OPC-UA) → anomaly detection → SAP PM work orders",
                "52-endpoint MCP server bridges PdM models to planner workflows",
                "Started with 1 asset family at Indaiatuba, expanded to 7+ sites",
            ],
        },
        "uc2": {
            "id": "UC-02",
            "title": "Visual Quality Inspection",
            "company": "Hyundai Framework",
            "stats": [
                ("99.2%", "detection accuracy"),
                ("85%", "false positive ↓"),
                ("1.2ms", "edge inference"),
            ],
            "gist": [
                "YOLOv8 on Jetson Orin NX — real-time line-speed defect detection",
                "Active learning: human corrections feed model retraining pipeline",
                "SAP MES integration for quality holds + disposition routing",
            ],
        },
        "buyer": "VP Manufacturing · Plant Manager · VP Quality",
        "market": "PdM market: $2.6B → $19.3B by 2032 (39.5% CAGR). BMW AIQX deployed across all plants worldwide.",
    },
    {
        "num": "02",
        "name": "Healthcare",
        "score": "Viable",
        "revenue": "$3-5K/mo per client",
        "headline": "Automate the Bureaucracy, Augment the Clinician",
        "subtitle": "Patient intake automation + clinical AI sepsis detection — HIPAA-compliant, FHIR-native, clinician-in-the-loop",
        "uc1": {
            "id": "UC-03",
            "title": "Patient Intake Automation",
            "company": "Reference Architecture",
            "stats": [
                ("80%", "staff time saved"),
                ("<30s", "insurance verification"),
                ("3", "agent pipeline"),
            ],
            "gist": [
                "3-agent pipeline: intake → insurance verification → scheduling",
                "FHIR R4 APIs + Twilio SMS + Calendly booking — all MCP-connected",
                "PHI stays inside customer boundary; failed verifications escalate to humans",
            ],
        },
        "uc2": {
            "id": "UC-04",
            "title": "Clinical AI — Sepsis Detection",
            "company": "Tampa General Hospital",
            "stats": [
                ("700+", "lives saved"),
                ("61K", "care gap orders"),
                ("5%", "mortality ↓"),
            ],
            "gist": [
                "TGH + Palantir: real-time EHR vitals → ML detects deterioration → alerts care team",
                "CommonSpirit Health: 61K care gap orders closed across 142 hospitals",
                "Clinician-in-the-loop: AI recommends, clinician reviews and acts",
            ],
        },
        "buyer": "Practice Manager · CMO · VP Clinical Operations",
        "market": "Healthcare AI verification market accelerating. Mastercard proved same <50ms decisioning pattern at 143B txns/year.",
    },
    {
        "num": "03",
        "name": "Legal",
        "score": "30/35 GO",
        "revenue": "$3-5K/mo per client",
        "headline": "67 Review Agents + Source-Grounded Research = Lawyer Time Recaptured",
        "subtitle": "Contract generation & review + LexisNexis AI research — auditable, source-cited, no hallucinated case law",
        "uc1": {
            "id": "UC-05",
            "title": "Contract Gen & Review",
            "company": "Top-100 Global Law Firm",
            "stats": [
                ("70%", "review time ↓"),
                ("$2.4M", "recaptured value"),
                ("99.1%", "clause accuracy"),
            ],
            "gist": [
                "3 agents: generation + 67-agent debate review + legal research",
                "40+ templates as MCP server endpoints; DocuSign signature routing",
                "22-week build, production by week 10; 45K-contract training corpus",
            ],
        },
        "uc2": {
            "id": "UC-10",
            "title": "LexisNexis Lexis+ AI",
            "company": "Forrester TEI Study",
            "stats": [
                ("284%", "3-year ROI"),
                ("$1.2M", "total benefits"),
                ("13%", "outside counsel ↓"),
            ],
            "gist": [
                "Gen AI grounded in verified LexisNexis primary law corpus — zero fabricated citations",
                "Research time reduced up to 80%; payback under 6 months",
                "Practice-area scoped: jurisdiction + domain boundaries enforced",
            ],
        },
        "buyer": "Legal Ops · Managing Partner · General Counsel",
        "market": "Harvey AI: $300M ARR, $11B valuation, 142K lawyers. Legal AI adoption doubled 14% → 26% in 12 months.",
    },
    {
        "num": "04",
        "name": "Financial Services",
        "score": "Production",
        "revenue": "$5-10K/mo per client",
        "headline": "Two Banks, Two Eras of AI — Both Ship, Both Save Millions",
        "subtitle": "TD Bank agentic mortgage processing + JPMorgan COIN contract extraction — deterministic math, LLM reading, human gates",
        "uc1": {
            "id": "UC-06",
            "title": "TD Bank Mortgage Agent",
            "company": "TD Bank (Jan 2026)",
            "stats": [
                ("15hr→min", "processing time"),
                ("$826M", "origination volume"),
                ("Day 1", "compliance ready"),
            ],
            "gist": [
                "Agentic AI reads entire borrower packages — purchase agreements, IDs, bank stmts",
                "Deterministic tools for arithmetic; LLM for document reading — sharp task boundaries",
                "Human adjudicator signs off every credit decision; AI recommends only",
            ],
        },
        "uc2": {
            "id": "UC-07",
            "title": "JPMorgan COIN",
            "company": "JPMorgan Chase (2016→now)",
            "stats": [
                ("360K", "attorney-hours saved/yr"),
                ("12K", "contracts/year"),
                ("9+yr", "in production"),
            ],
            "gist": [
                "Purpose-built ML extracts 150 attributes from commercial credit agreements",
                "Not an LLM — narrow domain, closed text, static rules; precision extraction",
                "9+ years running proves staying power; human corrections feed retraining",
            ],
        },
        "buyer": "VP Mortgage Ops · CTO · VP Legal Operations",
        "market": "Mastercard Decision Intelligence: 143B txns/year, 20-300% fraud detection lift, <50ms decisioning.",
    },
    {
        "num": "05",
        "name": "Construction",
        "score": "Production",
        "revenue": "$3-8K/mo per client",
        "headline": "The Superintendent Now Acts on Data, Not Memory",
        "subtitle": "Autonomous site capture + CV risk detection — 34M annotations, 48% injury reduction, 6x ROI validated",
        "uc1": {
            "id": "UC-08",
            "title": "DroneDeploy",
            "company": "DroneDeploy + Barton Malow",
            "stats": [
                ("34M", "training annotations"),
                ("+340%", "progress tracking ↑"),
                ("48%", "injury reduction"),
            ],
            "gist": [
                "4 AI agents: Progress AI, Safety AI, Inspection AI, Embodied AI",
                "Overnight autonomous capture → structured morning reports by trade",
                "13-year corpus across 180 countries — 770M images; break-even Sep 2025",
            ],
        },
        "uc2": {
            "id": "UC-09",
            "title": "BCG AI Site Assistant",
            "company": "German DevCo (BCG pilot)",
            "stats": [
                ("6x", "ROI validated"),
                ("12%", "productivity ↑"),
                ("48%", "injury ↓"),
            ],
            "gist": [
                "CV risk detection from continuous site imagery → smart notifications in minutes",
                "Automated documentation replaces memory-based superintendent decisions",
                "Pilot on 2 live projects; BCG 2026 Executive Perspectives report",
            ],
        },
        "buyer": "VP Construction · Project Director · COO",
        "market": "C.H. Robinson: 30+ AI agents, 3M+ tasks automated, 35% productivity gain. Same agentic pattern works in field ops.",
    },
]


def exec_slide(d: Deck, ind: dict, page: int, total: int):
    """One executive summary slide per industry — two UC cards side by side."""
    s = d.slide(fill=d.b.WHITE)

    # ── Top bar ──
    d.rect(s, 0, 0, d.W, Inches(0.12), d.b.TEAL)

    # ── Industry header ──
    d.text(s, f"INDUSTRY {ind['num']}  ·  {ind['name'].upper()}",
           d.M, Inches(0.26), Inches(5), Inches(0.24),
           size=11, color=d.b.MUTED, bold=True)

    # Score + revenue badges
    badge_x = d.W - d.M - Inches(3.6)
    d.rect(s, badge_x, Inches(0.22), Inches(1.5), Inches(0.3), d.b.TEAL, radius=0.04)
    d.text(s, f"SCORE: {ind['score']}", badge_x + Inches(0.1), Inches(0.22),
           Inches(1.3), Inches(0.3), size=9.5, color=d.b.WHITE, bold=True,
           anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    d.rect(s, badge_x + Inches(1.7), Inches(0.22), Inches(1.9), Inches(0.3), d.b.GOLD, radius=0.04)
    d.text(s, ind["revenue"], badge_x + Inches(1.8), Inches(0.22),
           Inches(1.7), Inches(0.3), size=9.5, color=d.b.NAVY, bold=True,
           anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    # ── Headline + subtitle ──
    d.text(s, ind["headline"], d.M, Inches(0.58), d.CW, Inches(0.56),
           size=21, color=d.b.NAVY, bold=True, shrink=True)
    d.rect(s, d.M, Inches(1.08), Inches(1.2), Inches(0.04), d.b.TEAL)
    d.text(s, ind["subtitle"], d.M, Inches(1.18), d.CW, Inches(0.24),
           size=10.5, color=d.b.MUTED, shrink=True)

    # ── Two UC cards side by side ──
    card_y = Inches(1.58)
    card_h = Inches(4.0)
    card_gap = Inches(0.3)
    card_w = (d.CW - card_gap) / 2

    for i, uc in enumerate([ind["uc1"], ind["uc2"]]):
        x = d.M + i * (card_w + card_gap)
        d.rect(s, x, card_y, card_w, card_h, d.b.NAVY, radius=0.06, shadow=True)

        # UC ID + title
        d.text(s, uc["id"], x + Inches(0.2), card_y + Inches(0.15),
               Inches(1.0), Inches(0.2), size=10, color=d.b.GOLD, bold=True)
        d.text(s, uc["title"], x + Inches(0.2), card_y + Inches(0.36),
               card_w - Inches(0.4), Inches(0.36),
               size=16, color=d.b.WHITE, bold=True, shrink=True)

        # Company tag
        d.rect(s, x + Inches(0.2), card_y + Inches(0.78),
               card_w - Inches(0.4), Inches(0.24), d.b.ACCENT, radius=0.03)
        d.text(s, uc["company"], x + Inches(0.3), card_y + Inches(0.78),
               card_w - Inches(0.6), Inches(0.24),
               size=8.5, color=d.b.WHITE, bold=True,
               anchor=MSO_ANCHOR.MIDDLE, shrink=True)

        # 3 stat pills
        stat_y = card_y + Inches(1.15)
        stat_gap = Inches(0.12)
        stat_w = (card_w - Inches(0.4) - stat_gap * 2) / 3
        for j, (num, label) in enumerate(uc["stats"]):
            sx = x + Inches(0.2) + j * (stat_w + stat_gap)
            d.rect(s, sx, stat_y, stat_w, Inches(0.72), d.b.GOLD, radius=0.04)
            d.text(s, num, sx + Inches(0.06), stat_y + Inches(0.06),
                   stat_w - Inches(0.12), Inches(0.3),
                   size=16, color=d.b.NAVY, bold=True,
                   align=PP_ALIGN.CENTER, shrink=True)
            d.text(s, label, sx + Inches(0.06), stat_y + Inches(0.4),
                   stat_w - Inches(0.12), Inches(0.26),
                   size=7.5, color=d.b.NAVY, bold=True,
                   align=PP_ALIGN.CENTER, shrink=True)

        # Divider
        d.rect(s, x + Inches(0.2), stat_y + Inches(0.85),
               card_w - Inches(0.4), Inches(0.03), d.b.TEAL)

        # Implementation gist (3 bullets)
        d.text(s, "IMPLEMENTATION", x + Inches(0.2), stat_y + Inches(0.96),
               Inches(2.5), Inches(0.2), size=9, color=d.b.TEAL, bold=True)
        d.text(s, [{"text": g, "bullet": True, "size": 8.8, "color": d.b.WHITE, "space_before": 3}
                   for g in uc["gist"]],
               x + Inches(0.2), stat_y + Inches(1.18),
               card_w - Inches(0.4), Inches(1.6), shrink=True, ls=1.0)

    # ── Bottom strip: buyer + market context ──
    strip_y = Inches(5.78)
    strip_h = Inches(0.95)
    buyer_w = d.CW * 0.35
    market_w = d.CW * 0.65 - Inches(0.2)

    d.rect(s, d.M, strip_y, buyer_w, strip_h, d.b.TEAL, radius=0.05)
    d.text(s, "BUYER PROFILE", d.M + Inches(0.18), strip_y + Inches(0.1),
           buyer_w - Inches(0.36), Inches(0.2), size=10, color=d.b.NAVY, bold=True)
    d.text(s, ind["buyer"], d.M + Inches(0.18), strip_y + Inches(0.35),
           buyer_w - Inches(0.36), Inches(0.45),
           size=10.5, color=d.b.WHITE, bold=True, shrink=True)

    d.rect(s, d.M + buyer_w + Inches(0.2), strip_y, market_w, strip_h, d.b.SOFT, radius=0.05)
    d.text(s, "MARKET SIGNAL", d.M + buyer_w + Inches(0.38), strip_y + Inches(0.1),
           market_w - Inches(0.36), Inches(0.2), size=10, color=d.b.NAVY, bold=True)
    d.text(s, ind["market"], d.M + buyer_w + Inches(0.38), strip_y + Inches(0.35),
           market_w - Inches(0.36), Inches(0.45),
           size=9.5, color=d.b.INK, shrink=True, ls=1.0)

    d.footer(s, page, total)


def build():
    total = 5
    d = Deck()
    for i, ind in enumerate(INDUSTRIES):
        exec_slide(d, ind, i + 1, total)
    d.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
