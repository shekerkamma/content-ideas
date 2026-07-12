#!/usr/bin/env python3
"""
RetailCo — Solution Blueprint
2 slides: Capability Map + Phased Delivery Plan
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".claude/skills/branded-pptx-deck/scripts"))
from pptxkit import Deck, Inches, Pt, PP_ALIGN, MSO_ANCHOR

RUN_DIR = Path(__file__).parent
OUT = RUN_DIR / "retailco-solution-blueprint-draft.pptx"
TOTAL = 3   # cover + 2 content slides
FOOTER = "AI Consulting Toolkit  ·  RetailCo  ·  June 2026  ·  CONFIDENTIAL"

d = Deck(footer=FOOTER)
b = d.b

# ─────────────────────────────────────────────────────────────
# COVER
# ─────────────────────────────────────────────────────────────
s = d.slide(fill=b.NAVY)

# right dark strip
d.rect(s, Inches(10.5), 0, Inches(2.833), Inches(7.5), b.NAVY_2)
# teal left edge
d.rect(s, 0, 0, Inches(0.18), Inches(7.5), b.TEAL)
# teal top band
d.rect(s, 0, 0, Inches(13.333), Inches(0.18), b.TEAL)

d.text(s, "SOLUTION DELIVERY", Inches(0.6), Inches(1.1), Inches(9.6), Inches(0.45),
       size=13, color=b.TEAL, bold=True)
d.text(s, "RetailCo", Inches(0.6), Inches(1.65), Inches(9.6), Inches(0.65),
       size=36, color=b.WHITE, bold=True, shrink=True)
d.text(s, "Solution Blueprint", Inches(0.6), Inches(2.4), Inches(9.6), Inches(1.2),
       size=52, color=b.GOLD, bold=True, shrink=True)

# teal rule
d.rect(s, Inches(0.6), Inches(3.75), Inches(2.2), Inches(0.055), b.TEAL)

d.text(s, "AI-Powered Customer Service Automation", Inches(0.6), Inches(3.9),
       Inches(9.6), Inches(0.45), size=17, color=b.LIGHT_TEAL)
d.text(s, "Capability Map  ·  Phased Delivery Plan  ·  Integration Constraints",
       Inches(0.6), Inches(4.45), Inches(9.6), Inches(0.4), size=13, color=b.MUTED)

# chips
chip_data = [("60% Deflection Target", b.TEAL), ("3-Wave Delivery", b.ACCENT),
             ("SAP + Salesforce", b.NAVY_2)]
x = Inches(0.6)
for label, fill in chip_data:
    w = Inches(2.1)
    d.rect(s, x, Inches(5.2), w, Inches(0.42), fill, radius=0.08)
    d.text(s, label, x + Inches(0.12), Inches(5.21), w - Inches(0.22), Inches(0.4),
           size=11, color=b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    x += w + Inches(0.18)

d.text(s, "June 2026", Inches(0.6), Inches(6.8), Inches(4), Inches(0.35),
       size=11, color=b.MUTED)

# ─────────────────────────────────────────────────────────────
# SLIDE 1 — CAPABILITY MAP
# ─────────────────────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
d.rect(s, 0, 0, Inches(13.333), Inches(0.16), b.TEAL)
d.header(s, "Capability Map — Build / Buy / Partner Decision",
         "AI customer service: full capability stack for Wave 1–3 delivery", band=False)

# Table definition
# Columns: Outcome | Capability | Component | Technology | Build/Buy/Partner
COL_W  = [Inches(2.05), Inches(2.05), Inches(2.8), Inches(3.5), Inches(1.7)]
COL_X  = [Inches(0.6)]
for w in COL_W[:-1]:
    COL_X.append(COL_X[-1] + w + Inches(0.06))

ROW_H  = Inches(0.52)
HDR_Y  = Inches(1.65)
ROW_Y0 = Inches(2.22)

HEADERS = ["Outcome", "Capability", "Component", "Technology", "Build / Buy"]
ROWS = [
    ("60% contact deflection", "Intent classification",     "LLM classifier",           "Azure OpenAI GPT-4o",          "Buy"),
    ("",                        "Conversation orchestration","LangGraph agent loop",      "LangGraph + Python 3.11",      "Build"),
    ("",                        "Knowledge retrieval",       "RAG pipeline",              "Azure AI Search + GPT-4o",     "Build"),
    ("Order status self-serve", "Order data access",         "SAP OData integration",     "SAP S/4HANA OData API",        "Build (integration)"),
    ("Returns initiation",      "Returns workflow",          "Returns API connector",     "Internal REST API v2",         "Build (integration)"),
    ("Escalation to human",     "Handoff with context",      "CRM screen-pop",            "Salesforce Service Cloud CTI",  "Build (integration)"),
    ("Quality & safety",        "Guardrails",                "Content safety + validation","Azure Content Safety + Pydantic","Buy"),
]

# header row
for i, (hdr, x, w) in enumerate(zip(HEADERS, COL_X, COL_W)):
    d.rect(s, x, HDR_Y, w, ROW_H, b.NAVY)
    d.text(s, hdr, x + Inches(0.1), HDR_Y + Inches(0.06), w - Inches(0.18), ROW_H - Inches(0.1),
           size=11, color=b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

# data rows
for ri, row in enumerate(ROWS):
    y = ROW_Y0 + ri * (ROW_H + Inches(0.04))
    fill = b.SOFT if ri % 2 == 0 else b.WHITE
    for ci, (cell, x, w) in enumerate(zip(row, COL_X, COL_W)):
        d.rect(s, x, y, w, ROW_H, fill)
        if cell:
            # Build/Buy column: color-coded
            if ci == 4:
                if cell.startswith("Buy"):
                    tc = b.TEAL
                elif cell.startswith("Build ("):
                    tc = b.AMBER
                else:
                    tc = b.ACCENT
                bold = True
            else:
                tc = b.INK
                bold = (ci == 0 and cell != "")
            d.text(s, cell, x + Inches(0.1), y + Inches(0.05),
                   w - Inches(0.18), ROW_H - Inches(0.08),
                   size=10.5, color=tc, bold=bold, anchor=MSO_ANCHOR.MIDDLE, shrink=True)

# legend
lx = Inches(0.6)
ly = Inches(6.62)
for label, col in [("Buy = vendor platform", b.TEAL),
                   ("Build = internal / custom", b.ACCENT),
                   ("Build (integration) = API wrapper", b.AMBER)]:
    d.rect(s, lx, ly, Inches(0.18), Inches(0.18), col, radius=0.1)
    d.text(s, label, lx + Inches(0.24), ly, Inches(3.1), Inches(0.22),
           size=9.5, color=b.MUTED, shrink=True)
    lx += Inches(3.4)

d.footer(s, 1, TOTAL)

# ─────────────────────────────────────────────────────────────
# SLIDE 2 — PHASED DELIVERY PLAN
# ─────────────────────────────────────────────────────────────
s = d.slide(fill=b.WHITE)
d.rect(s, 0, 0, Inches(13.333), Inches(0.16), b.TEAL)
d.header(s, "Phased Delivery — Gate-Controlled Wave Approach",
         "Wave 1 = order status only · Wave 2 = returns + escalation · Wave 3 = optimise & scale",
         band=False)

WAVE_W = Inches(3.8)
WAVE_GAP = Inches(0.17)
WAVE_Y = Inches(1.65)
WAVE_H = Inches(4.6)

waves = [
    {
        "label": "WAVE 1",
        "period": "Months 1–3",
        "goal": "Order status self-serve",
        "color": b.NAVY,
        "items": [
            "Azure OpenAI + Content Safety provisioning",
            "RAG pipeline (4,200 SKUs + 800 FAQ articles)",
            "SAP OData integration — read-only order status",
            "Agent orchestration: classify → lookup → respond",
            "Guardrails + output validation layer",
            "Shadow mode UAT on 5% live traffic",
        ],
        "gate": "≥85% accuracy on order status intents in UAT",
        "gate_col": b.GOLD,
    },
    {
        "label": "WAVE 2",
        "period": "Months 4–6",
        "goal": "Returns + escalation",
        "color": b.ACCENT,
        "items": [
            "Returns API v2 integration",
            "Salesforce CTI screen-pop on escalation",
            "Expand intents: product Q&A, store locator, loyalty",
            "A/B test: AI-first vs IVR-first routing",
            "Target: 45% deflection",
        ],
        "gate": "Deflection ≥45% · CSAT ≥4.1/5.0",
        "gate_col": b.TEAL,
    },
    {
        "label": "WAVE 3",
        "period": "Months 7–9",
        "goal": "Optimise & scale",
        "color": b.DARK_TEAL,
        "items": [
            "Fine-tune classifier on 90 days of production data",
            "Redis cache layer for SAP (↓60% OData calls)",
            "Proactive order delay push notifications",
            "Scale to 100% inbound traffic",
        ],
        "gate": "Deflection ≥60% · Handle time for escalations ≤6 min",
        "gate_col": b.TEAL,
    },
]

for wi, wv in enumerate(waves):
    x = Inches(0.6) + wi * (WAVE_W + WAVE_GAP)

    # wave card background
    d.rect(s, x, WAVE_Y, WAVE_W, WAVE_H, b.SOFT, radius=0.06)
    # coloured top band
    d.rect(s, x, WAVE_Y, WAVE_W, Inches(0.68), wv["color"], radius=0.06)
    # square off bottom corners of top band
    d.rect(s, x, WAVE_Y + Inches(0.44), WAVE_W, Inches(0.24), wv["color"])

    # wave label + period
    d.text(s, wv["label"], x + Inches(0.18), WAVE_Y + Inches(0.06),
           WAVE_W - Inches(0.3), Inches(0.32),
           size=13, color=b.WHITE, bold=True)
    d.text(s, wv["period"], x + Inches(0.18), WAVE_Y + Inches(0.36),
           WAVE_W - Inches(0.3), Inches(0.28),
           size=10, color=b.LIGHT_TEAL)

    # goal line
    d.text(s, wv["goal"], x + Inches(0.18), WAVE_Y + Inches(0.78),
           WAVE_W - Inches(0.3), Inches(0.32),
           size=12, color=b.NAVY, bold=True)

    # deliverables
    item_y = WAVE_Y + Inches(1.18)
    for item in wv["items"]:
        d.text(s, "•  " + item, x + Inches(0.18), item_y,
               WAVE_W - Inches(0.3), Inches(0.46),
               size=10, color=b.INK, shrink=True)
        item_y += Inches(0.47)

    # gate strip
    gate_y = WAVE_Y + WAVE_H - Inches(0.65)
    d.rect(s, x, gate_y, WAVE_W, Inches(0.62), wv["gate_col"], radius=0.06)
    d.rect(s, x, gate_y, WAVE_W, Inches(0.24), wv["gate_col"])  # flatten top corners
    d.text(s, "GATE  " + wv["gate"],
           x + Inches(0.14), gate_y + Inches(0.08),
           WAVE_W - Inches(0.22), Inches(0.5),
           size=9.5, color=b.NAVY if wv["gate_col"] == b.GOLD else b.WHITE,
           bold=True, shrink=True, anchor=MSO_ANCHOR.MIDDLE)

# arrow connectors between waves
for wi in range(2):
    ax = Inches(0.6) + (wi + 1) * (WAVE_W + WAVE_GAP) - Inches(0.22)
    ay = WAVE_Y + WAVE_H / 2 - Inches(0.15)
    d.text(s, "→", ax, ay, Inches(0.22), Inches(0.3),
           size=18, color=b.MUTED, bold=True, align=PP_ALIGN.CENTER)

d.footer(s, 2, TOTAL)

# ─────────────────────────────────────────────────────────────
# SAVE + VALIDATE
# ─────────────────────────────────────────────────────────────
d.save(OUT)
print(f"Output: {OUT}")
