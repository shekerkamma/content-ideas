#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

BRANDED_SKILL = Path("/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(BRANDED_SKILL))

from pptxkit import Deck, Inches, PP_ALIGN, MSO_ANCHOR  # type: ignore

RUN_DIR = Path(__file__).resolve().parent
OUT = RUN_DIR / "real-estate-brokerage-automation-client-package-branded-draft.pptx"
FEED = json.loads((RUN_DIR / "feed-data.json").read_text(encoding="utf-8"))
UC = FEED["useCases"][0]
SLIDE3_TITLE = "Brokerage Lead Routing & Transaction Automation"
SLIDE3_CHALLENGE = [
    "Slow lead response and weak routing hurt conversion.",
    "Transaction work is split across CRM, docs, and finance tools.",
    "Agents reject tools that add admin without deal lift.",
]
SLIDE3_SOLUTION = [
    "Score and route inbound leads from Zillow, web, and campaigns.",
    "Automate follow-up, invites, document prep, and commission visibility.",
    "Keep the workflow inside the CRM and document stack.",
]
SLIDE3_STATS = [
    ("36%", "Cloze AI sales-lift claim"),
    ("30 sec", "Zillow routing timer"),
    ("$2K–4K/mo", "Source-PDF SMB revenue range"),
]
SLIDE3_HOW = [
    "Ingest leads from Zillow, forms, and brokerage campaigns.",
    "Score intent, assign agents, and draft the next action.",
    "Track response time, conversion, and task progress in CRM.",
]
SLIDE3_STACK = [
    ("EXPERIENCE", "CRM workspace + manager dashboard"),
    ("ORCHESTRATION", "OpenHands routing and workflow agents"),
    ("CONTEXT", "CRM, lead, listing, and milestone data"),
    ("ACTUATION", "Assignments, drafts, DocuSign, commissions"),
]
SLIDE3_ORGS = [
    ("Compass", "Large brokerage with expanding AI workflows."),
    ("Cloze", "Connected brokerage platform with AI assist."),
    ("Zillow", "Lead-routing marketplace and AI-assist surface."),
    ("Mid-market brokerage", "Buyer needing faster conversion without custom software."),
]


def header_slide(d: Deck, title: str, subtitle: str):
    s = d.slide(fill=d.b.WHITE)
    d.rect(s, 0, 0, d.W, Inches(0.16), d.b.TEAL)
    d.text(s, title, d.M, Inches(0.42), d.CW, Inches(0.78), size=20, color=d.b.NAVY, bold=True, shrink=True)
    d.rect(s, d.M, Inches(1.18), Inches(1.45), Inches(0.05), d.b.TEAL)
    d.text(s, subtitle, d.M, Inches(1.36), d.CW, Inches(0.26), size=10.8, color=d.b.MUTED, shrink=True)
    return s


def footer(d: Deck, s, page: int, total: int, dark: bool = False):
    d.footer(s, page, total, dark=dark)


def executive_summary(d: Deck, total: int):
    s = header_slide(
        d,
        "Brokerage AI works best when it captures leads faster and removes admin drag",
        "Executive summary built from the PDF brokerage use case, Compass, Zillow, Cloze, DocuSign, and verified OpenHands capabilities",
    )
    y = Inches(1.75)
    col_w = Inches(3.92)
    gap = Inches(0.22)
    xs = [d.M, d.M + col_w + gap, d.M + 2 * (col_w + gap)]
    titles = ["Situation", "Insight", "Recommendation"]
    bodies = [
        [
            "Brokerages lose revenue to slow response, bad routing, and fragmented transaction workflows.",
            "Zillow and Compass already treat routing and follow-up as productized workflows.",
            "The category is real, but agent adoption determines whether value sticks."
        ],
        [
            "The best wedge is speed-to-lead plus AI assignment and draft follow-up inside the CRM.",
            "The expansion path is document, marketing, and transaction workflow automation.",
            "OpenHands fits as the internal orchestration layer for reusable workflow agents."
        ],
        [
            "Lead with one team or office, one CRM workflow, and clear response/conversion metrics.",
            "Keep the workflow in the tools agents already use.",
            "Treat document and transaction automation as phase two after routing trust is earned."
        ],
    ]
    colors = [d.b.SOFT, d.b.SOFT, d.b.NAVY]
    for idx, x in enumerate(xs):
        d.rect(s, x, y, col_w, Inches(3.45), colors[idx], radius=0.05, shadow=True)
        d.text(s, titles[idx], x + Inches(0.22), y + Inches(0.18), col_w - Inches(0.4), Inches(0.25),
               size=16, color=d.b.TEAL if idx == 2 else d.b.NAVY, bold=True)
        d.text(
            s,
            [{"text": item, "bullet": True, "size": 12, "color": d.b.LIGHT_TEAL if idx == 2 else d.b.INK, "space_before": 7} for item in bodies[idx]],
            x + Inches(0.22), y + Inches(0.55), col_w - Inches(0.4), Inches(2.6), shrink=True
        )
    d.rect(s, d.M, Inches(5.55), d.CW, Inches(0.62), d.b.GOLD, radius=0.05)
    d.text(s, "THE ASK: approve a pilot for one office or team to improve speed-to-lead and routing quality inside the current CRM stack.",
           d.M + Inches(0.25), Inches(5.68), d.CW - Inches(0.5), Inches(0.28),
           size=11.0, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 2, total)


def use_case_realization(d: Deck, total: int):
    s = d.slide(fill=d.b.TEAL)
    panel_w = Inches(8.85)
    strip_x = panel_w
    strip_w = d.W - panel_w
    d.rect(s, strip_x, 0, strip_w, d.H, d.b.NAVY)
    d.rect(s, strip_x, 0, Inches(0.06), d.H, d.b.GOLD)
    d.text(s, UC["kicker"], d.M, Inches(0.28), panel_w - Inches(1.0), Inches(0.3), size=12, color=d.b.NAVY, bold=True)
    d.text(s, SLIDE3_TITLE, d.M, Inches(0.56), panel_w - Inches(1.0), Inches(0.68), size=20, color=d.b.WHITE, bold=True, shrink=True)

    card_y = Inches(1.25)
    card_h = Inches(1.64)
    gap = Inches(0.22)
    card_w = (panel_w - d.M * 2 - gap) / 2
    for idx, (title, items) in enumerate([("Challenge", SLIDE3_CHALLENGE), ("Solution", SLIDE3_SOLUTION)]):
        x = d.M + idx * (card_w + gap)
        d.rect(s, x, card_y, card_w, card_h, d.b.WHITE, radius=0.06, shadow=True)
        d.text(s, title.upper(), x + Inches(0.18), card_y + Inches(0.15), card_w - Inches(0.36), Inches(0.22), size=12, color=d.b.ACCENT, bold=True)
        d.text(s, [{"text": item, "bullet": True, "size": 8.8, "color": d.b.INK, "space_before": 2} for item in items],
               x + Inches(0.18), card_y + Inches(0.42), card_w - Inches(0.32), Inches(1.05), shrink=True, ls=0.98)

    sy = Inches(2.98)
    stat_gap = Inches(0.18)
    stat_w = (panel_w - d.M * 2 - stat_gap * 2) / 3
    for i, (num, label) in enumerate(SLIDE3_STATS):
        x = d.M + i * (stat_w + stat_gap)
        d.rect(s, x, sy, stat_w, Inches(0.86), d.b.GOLD, radius=0.05)
        d.text(s, num, x + Inches(0.12), sy + Inches(0.08), stat_w - Inches(0.24), Inches(0.28), size=18, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, label, x + Inches(0.12), sy + Inches(0.42), stat_w - Inches(0.24), Inches(0.22), size=9.2, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)

    how_y = Inches(4.0)
    d.text(s, "HOW IT WORKS", d.M, how_y, Inches(2.3), Inches(0.22), size=12, color=d.b.NAVY, bold=True)
    step_w = (panel_w - d.M * 2 - Inches(0.6)) / 3
    for i, step in enumerate(SLIDE3_HOW):
        x = d.M + i * (step_w + Inches(0.3))
        d.rect(s, x, how_y + Inches(0.28), step_w, Inches(0.92), d.b.WHITE, radius=0.05, shadow=True)
        d.text(s, f"{i+1:02d}", x + Inches(0.12), how_y + Inches(0.36), Inches(0.34), Inches(0.2), size=14, color=d.b.GOLD, bold=True)
        d.text(s, step, x + Inches(0.52), how_y + Inches(0.32), step_w - Inches(0.62), Inches(0.54), size=8.1, color=d.b.INK, shrink=True, ls=0.98)
        if i < 2:
            d.text(s, "→", x + step_w + Inches(0.05), how_y + Inches(0.54), Inches(0.24), Inches(0.24), size=14, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER)

    st_y = Inches(5.25)
    d.rect(s, d.M, st_y, panel_w - d.M * 2, Inches(0.95), d.b.NAVY, radius=0.05)
    d.text(s, "SOLUTION STACK", d.M + Inches(0.18), st_y + Inches(0.12), Inches(2), Inches(0.2), size=12, color=d.b.GOLD, bold=True)
    stack_w = (panel_w - d.M * 2 - Inches(0.72)) / 4
    for i, (layer, detail) in enumerate(SLIDE3_STACK):
        x = d.M + Inches(0.18) + i * stack_w
        d.text(s, layer, x, st_y + Inches(0.34), stack_w - Inches(0.08), Inches(0.18), size=8.8, color=d.b.TEAL, bold=True, shrink=True)
        d.text(s, detail, x, st_y + Inches(0.52), stack_w - Inches(0.08), Inches(0.32), size=7.7, color=d.b.WHITE, shrink=True, ls=0.98)

    by = Inches(6.45)
    bw = (panel_w - d.M * 2 - Inches(0.2)) / 2
    d.rect(s, d.M, by, bw, Inches(0.36), d.b.ACCENT, radius=0.04)
    d.text(s, "SYSTEMS: CRM · Zillow · DocuSign · QuickBooks · Marketing", d.M + Inches(0.15), by, bw - Inches(0.3), Inches(0.36), size=7.4, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.rect(s, d.M + bw + Inches(0.2), by, bw, Inches(0.36), d.b.DARK_TEAL, radius=0.04)
    d.text(s, "USERS: team lead · ops · agent · marketing", d.M + bw + Inches(0.35), by, bw - Inches(0.3), Inches(0.36), size=7.4, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)

    sx = strip_x + Inches(0.3)
    d.text(s, "ORGANIZATIONS", sx, Inches(0.45), strip_w - Inches(0.5), Inches(0.24), size=13, color=d.b.TEAL, bold=True)
    d.text(s, "DELIVERING / BUYING THIS", sx, Inches(0.72), strip_w - Inches(0.5), Inches(0.24), size=13, color=d.b.TEAL, bold=True)
    d.rect(s, sx, Inches(1.08), Inches(1.0), Inches(0.04), d.b.GOLD)
    oy = Inches(1.28)
    for name, desc in SLIDE3_ORGS:
        d.text(s, name, sx, oy, strip_w - Inches(0.5), Inches(0.24), size=13.0, color=d.b.WHITE, bold=True, shrink=True)
        d.text(s, desc, sx, oy + Inches(0.26), strip_w - Inches(0.55), Inches(0.58), size=9.0, color=d.b.LIGHT_TEAL, shrink=True, ls=0.98)
        oy += Inches(1.0)
    footer(d, s, 3, total, dark=True)


def market_landscape(d: Deck, total: int):
    s = header_slide(d, "The category is real because the lead-routing problem is already productized",
                     "Structured proof slide with market signals, operator proof, and revenue relevance")
    col_w = Inches(3.95)
    gap = Inches(0.22)
    xs = [d.M, d.M + col_w + gap, d.M + 2 * (col_w + gap)]
    blocks = [
        ("Operator proof", [
            "Compass is embedding AI into follow-up, contact management, marketing collateral, and invitations.",
            "Zillow already routes and reallocates leads based on agent capacity.",
            "Zillow AI Assist shows marketplace-level demand for automated engagement."
        ], d.b.SOFT, d.b.NAVY, d.b.INK),
        ("Revenue relevance", [
            "The source PDF estimates $2K–4K per month per brokerage client in SMB settings.",
            "Cloze claims AI can boost sales by 36%.",
            "The value path is faster response, better routing, and higher pipeline conversion."
        ], d.b.SOFT, d.b.NAVY, d.b.INK),
        ("Why now", [
            "Lead-routing and follow-up are visible enough for a clean ROI story.",
            "Document and transaction automation create a credible second phase.",
            "The market is crowded, so execution inside the current stack matters more than AI novelty."
        ], d.b.NAVY, d.b.TEAL, d.b.LIGHT_TEAL),
    ]
    for x, (title, items, fill, title_color, body_color) in zip(xs, blocks):
        d.rect(s, x, Inches(1.78), col_w, Inches(3.65), fill, radius=0.05, shadow=True)
        d.text(s, title, x + Inches(0.2), Inches(1.95), col_w - Inches(0.4), Inches(0.24), size=16, color=title_color, bold=True)
        d.text(s, [{"text": item, "bullet": True, "size": 11.4, "color": body_color, "space_before": 8} for item in items],
               x + Inches(0.22), Inches(2.28), col_w - Inches(0.42), Inches(2.75), shrink=True)
    footer(d, s, 4, total)


def architecture_stack(d: Deck, total: int):
    s = header_slide(d, "The reference architecture is CRM-native and OpenHands-orchestrated",
                     "Structured stack slide grounded in verified OpenHands, Compass, Zillow, and source-PDF capabilities")
    left_w = Inches(5.8)
    right_x = d.M + left_w + Inches(0.35)
    d.rect(s, d.M, Inches(1.75), left_w, Inches(4.4), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "ORCHESTRATION AND INTEGRATION STACK", d.M + Inches(0.22), Inches(1.95), left_w - Inches(0.4), Inches(0.24), size=15, color=d.b.TEAL, bold=True)
    stack_points = [
        "OpenHands SDK agents orchestrate lead scoring, assignment, and outreach drafting.",
        "OpenHands skills carry brokerage routing rules, follow-up policies, and workflow guardrails.",
        "CLI and headless execution support repeatable routing, reporting, and nightly task workflows.",
        "CRM, DocuSign, finance, and marketplace integrations feed actions back into the working stack.",
        "The brokerage CRM remains the system of action for agents and managers."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.2, "color": d.b.WHITE, "space_before": 8} for item in stack_points],
           d.M + Inches(0.22), Inches(2.28), left_w - Inches(0.44), Inches(3.35), shrink=True)
    cards = [
        ("Systems of record", "CRM, Zillow, DocuSign, QuickBooks, and marketing systems."),
        ("Deployment stance", "OpenHands is the internal execution layer; the CRM remains the user-facing surface."),
    ]
    cy = Inches(1.75)
    card_h = Inches(1.98)
    for title, body in cards:
        d.rect(s, right_x, cy, Inches(6.0), card_h, d.b.SOFT, radius=0.05, shadow=True)
        d.text(s, title, right_x + Inches(0.2), cy + Inches(0.16), Inches(5.6), Inches(0.28), size=14.0, color=d.b.NAVY, bold=True, shrink=True)
        d.text(s, body, right_x + Inches(0.2), cy + Inches(0.5), Inches(5.6), Inches(1.18), size=10.6, color=d.b.INK, shrink=True)
        cy += Inches(2.12)
    footer(d, s, 5, total)


def score_risks(d: Deck, total: int):
    s = header_slide(d, "The lane is attractive, but agent adoption risk is real",
                     "Structured score-and-risk slide")
    d.rect(s, d.M, Inches(1.75), Inches(4.1), Inches(4.4), d.b.SOFT, radius=0.05, shadow=True)
    d.text(s, "VERTICAL SCORECARD", d.M + Inches(0.22), Inches(1.95), Inches(3.7), Inches(0.22), size=15, color=d.b.NAVY, bold=True)
    scores = [
        "Intelligence Ratio: 4/5",
        "Outsourcing Readiness: 4/5",
        "TAM Accessibility: 4/5",
        "Data Moat Potential: 3/5",
        "Regulatory Friction: 3/5",
        "Incumbent Vulnerability: 3/5",
        "Mirage PMF Risk: 4/5",
        "Composite: 25/35 — GO",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.6, "color": d.b.INK, "space_before": 6} for item in scores],
           d.M + Inches(0.22), Inches(2.28), Inches(3.6), Inches(2.7), shrink=True)
    d.rect(s, Inches(5.0), Inches(1.75), Inches(7.7), Inches(4.4), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "RISKS AND CONTROLS", Inches(5.22), Inches(1.95), Inches(3.2), Inches(0.22), size=15, color=d.b.TEAL, bold=True)
    risks = [
        "Agents ignore AI suggestions — keep the workflow in the current CRM and start assistive.",
        "Lead noise reduces routing quality — maintain source-specific logic and human override.",
        "Fair-housing or disclosure concerns — constrain autonomous customer-facing actions.",
        "Tool fragmentation across offices — begin with one brokerage stack before broadening support."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.4, "color": d.b.LIGHT_TEAL, "space_before": 8} for item in risks],
           Inches(5.22), Inches(2.28), Inches(7.1), Inches(2.85), shrink=True)
    footer(d, s, 6, total)


def roadmap_and_account(d: Deck, total: int):
    s = header_slide(d, "A focused pilot and a Compass-specific angle make the offer commercially concrete",
                     "Structured execution and account slide")
    d.rect(s, d.M, Inches(1.75), Inches(6.1), Inches(4.55), d.b.SOFT, radius=0.05, shadow=True)
    d.text(s, "90-DAY ROADMAP", d.M + Inches(0.22), Inches(1.95), Inches(2.5), Inches(0.22), size=15, color=d.b.NAVY, bold=True)
    roadmap = [
        "Days 1-15: map lead sources, CRM flow, routing rules, and follow-up expectations.",
        "Days 16-35: configure ingestion, OpenHands routing logic, and manager reporting.",
        "Days 36-60: launch pilot routing and AI-assisted follow-up for one team.",
        "Days 61-90: measure lift, refine rules, and scope document/transaction automation."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.4, "color": d.b.INK, "space_before": 8} for item in roadmap],
           d.M + Inches(0.22), Inches(2.28), Inches(5.6), Inches(3.4), shrink=True)
    rx = Inches(6.95)
    d.rect(s, rx, Inches(1.75), Inches(5.75), Inches(4.55), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "COMPASS ACCOUNT ANGLE", rx + Inches(0.22), Inches(1.95), Inches(3.0), Inches(0.22), size=15, color=d.b.TEAL, bold=True)
    account = [
        "Compass already embeds AI into agent workflows such as follow-up, contact management, and invitations.",
        "The next value is deeper workflow packaging, not generic AI assistance.",
        "Pitch OpenHands as an internal orchestration layer for reusable brokerage skills and workflows.",
        "Recommended next step: pick one post-lead workflow and package it as a reusable internal automation pattern."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.0, "color": d.b.LIGHT_TEAL, "space_before": 8} for item in account],
           rx + Inches(0.22), Inches(2.28), Inches(5.25), Inches(3.4), shrink=True)
    footer(d, s, 7, total)


def closing(d: Deck, total: int):
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.16), d.b.TEAL)
    d.text(s, "BOTTOM LINE", d.M, Inches(1.15), Inches(3), Inches(0.25), size=16, color=d.b.TEAL, bold=True)
    d.text(s, "Brokerage lead routing and transaction automation is a client-ready AI engineering offer when it improves conversion inside the current CRM and document stack.", d.M, Inches(1.6), Inches(11.6), Inches(1.3), size=22, color=d.b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(3.15), Inches(11.9), Inches(0.06), d.b.GOLD)
    final_points = [
        "Use the CRM as the system of action.",
        "Use OpenHands internally for orchestration, skills, and reusable workflow patterns.",
        "Start with one team, one routing workflow, and one measurable revenue outcome.",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 15.5, "color": d.b.LIGHT_TEAL, "space_before": 10} for item in final_points],
           d.M, Inches(3.45), Inches(10.9), Inches(1.8), shrink=True)
    d.rect(s, d.M, Inches(5.85), Inches(6.0), Inches(0.72), d.b.GOLD, radius=0.05)
    d.text(s, "Suggested next step: approve a pilot for one office or team and review the workflow expansion path.",
           d.M + Inches(0.3), Inches(6.03), Inches(11.3), Inches(0.42), size=11.2, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 8, total, dark=True)


def main():
    total = 8
    d = Deck(footer="Real Estate Brokerage Automation | Client Package | June 2026")
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, d.W - Inches(3.0), 0, Inches(3.0), d.H, d.b.NAVY_2)
    d.rect(s, d.W - Inches(3.0), 0, Inches(0.06), d.H, d.b.TEAL)
    d.text(s, "CLIENT PACKAGE", d.M, Inches(0.95), Inches(3), Inches(0.25), size=15, color=d.b.TEAL, bold=True)
    d.text(s, "Real Estate Brokerage\nAutomation", d.M, Inches(1.45), Inches(7.6), Inches(1.28), size=32, color=d.b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.75), Inches(1.6), Inches(0.06), d.b.TEAL)
    d.text(s, "A branded strategy and presales package built from the brokerage use case in the framework document and validated with current Compass, Zillow, Cloze, DocuSign, and OpenHands signals.",
           d.M, Inches(3.05), Inches(7.8), Inches(1.2), size=15.5, color=d.b.WHITE, shrink=True)
    d.text(s, "DETAILED USE CASE · EXECUTIVE SUMMARY · ARCHITECTURE · SCORECARD · ROADMAP · ACCOUNT ANGLE",
           d.M, Inches(5.75), Inches(8.6), Inches(0.28), size=11, color=d.b.GOLD, bold=True)
    footer(d, s, 1, total, dark=True)
    executive_summary(d, total)
    use_case_realization(d, total)
    market_landscape(d, total)
    architecture_stack(d, total)
    score_risks(d, total)
    roadmap_and_account(d, total)
    closing(d, total)
    d.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
