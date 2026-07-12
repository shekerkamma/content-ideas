#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

BRANDED_SKILL = Path("/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(BRANDED_SKILL))

from pptxkit import Deck, Inches, PP_ALIGN, MSO_ANCHOR  # type: ignore

RUN_DIR = Path(__file__).resolve().parent
OUT = RUN_DIR / "real-estate-commission-automation-client-package-branded-draft.pptx"
FEED = json.loads((RUN_DIR / "feed-data.json").read_text(encoding="utf-8"))
UC = FEED["useCases"][0]

SLIDE3_TITLE = "Brokerage Commission & Deal Payout Automation"
SLIDE3_CHALLENGE = [
    "Manual splits, caps, and fees slow payouts.",
    "Transaction, accounting, and documents drift across systems.",
    "Ops teams need auditability and speed, not AI theater.",
]
SLIDE3_SOLUTION = [
    "Validate deal state and apply payout rules in workflow.",
    "Route exceptions, approvals, and accounting handoffs automatically.",
    "Keep finance and brokerage ops in control of release steps.",
]
SLIDE3_STATS = [
    ("1,500+", "Brokerages on Brokermint"),
    ("65,000+", "Agents supported"),
    ("400,000+", "Transactions per year"),
]
SLIDE3_HOW = [
    "Ingest transaction data and commission-plan rules.",
    "Validate payouts, detect exceptions, and prep next steps.",
    "Track readiness, approvals, and transaction-to-cash flow.",
]
SLIDE3_STACK = [
    ("EXPERIENCE", "Ops dashboard + payout queue"),
    ("ORCHESTRATION", "OpenHands payout workflow agents"),
    ("CONTEXT", "Deals, plans, ledgers, and docs"),
    ("ACTUATION", "Approvals, packets, updates, alerts"),
]
SLIDE3_ORGS = [
    ("Brokermint", "Official proof point for commission automation."),
    ("Inside Real Estate", "Platform context across the brokerage lifecycle."),
    ("RE/MAX-style network", "Scaled buyer where payout flow matters."),
    ("Mid-market brokerage", "Buyer needing fewer errors and faster payouts."),
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
        "Back-office AI works best when it speeds payouts and reduces brokerage exceptions",
        "Executive summary built from the source PDF, Brokermint, Docusign, and verified OpenHands capabilities",
    )
    y = Inches(1.75)
    col_w = Inches(3.92)
    gap = Inches(0.22)
    xs = [d.M, d.M + col_w + gap, d.M + 2 * (col_w + gap)]
    titles = ["Situation", "Insight", "Recommendation"]
    bodies = [
        [
            "Brokerages still run slow, error-prone payout workflows across spreadsheets and systems.",
            "Commission logic is structured enough for automation but painful enough to justify spend.",
            "Back-office buyers care about accuracy, approvals, and throughput."
        ],
        [
            "The best wedge is payout validation plus exception handling.",
            "The workflow becomes stronger when transaction, accounting, and document state stay synchronized.",
            "OpenHands fits as the internal orchestration layer for reusable back-office agents."
        ],
        [
            "Start with one ops team or payout queue.",
            "Measure payout cycle time, exception rate, and approval latency.",
            "Expand into broader transaction and accounting workflows after trust is earned."
        ],
    ]
    colors = [d.b.SOFT, d.b.SOFT, d.b.NAVY]
    for idx, x in enumerate(xs):
        d.rect(s, x, y, col_w, Inches(3.45), colors[idx], radius=0.05, shadow=True)
        d.text(s, titles[idx], x + Inches(0.22), y + Inches(0.18), col_w - Inches(0.4), Inches(0.25),
               size=16, color=d.b.TEAL if idx == 2 else d.b.NAVY, bold=True)
        d.text(s, [{"text": item, "bullet": True, "size": 12, "color": d.b.LIGHT_TEAL if idx == 2 else d.b.INK, "space_before": 7} for item in bodies[idx]],
               x + Inches(0.22), y + Inches(0.55), col_w - Inches(0.4), Inches(2.6), shrink=True)
    d.rect(s, d.M, Inches(5.55), d.CW, Inches(0.62), d.b.GOLD, radius=0.05)
    d.text(s, "THE ASK: approve a pilot for one payout workflow to improve speed and reduce commission exceptions.",
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
    d.text(s, "SYSTEMS: Back Office · Accounting · DocuSign · QuickBooks · Tx Mgmt", d.M + Inches(0.15), by, bw - Inches(0.3), Inches(0.36), size=7.0, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.rect(s, d.M + bw + Inches(0.2), by, bw, Inches(0.36), d.b.DARK_TEAL, radius=0.04)
    d.text(s, "USERS: ops · finance · tx coord · broker-owner", d.M + bw + Inches(0.35), by, bw - Inches(0.3), Inches(0.36), size=7.1, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)

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
    s = header_slide(d, "The category is real because commission automation is already a scaled brokerage workflow",
                     "Structured proof slide with operator evidence, workflow value, and timing")
    col_w = Inches(3.95)
    gap = Inches(0.22)
    xs = [d.M, d.M + col_w + gap, d.M + 2 * (col_w + gap)]
    blocks = [
        ("Operator proof", [
            "Brokermint says it supports 1,500+ brokerages, 65,000+ agents, and 400,000+ transactions per year.",
            "Its official platform includes commission automation, transaction management, accounting, and reporting.",
            "Docusign supports real-estate transaction and agreement workflows that connect to payout state."
        ], d.b.SOFT, d.b.NAVY, d.b.INK),
        ("Business value", [
            "The core value is fewer errors, faster payouts, and cleaner approval flow.",
            "This lane creates a finance-friendly ROI story instead of a generic AI story.",
            "Exception handling and reconciliation are the highest-friction steps to attack first."
        ], d.b.SOFT, d.b.NAVY, d.b.INK),
        ("Why now", [
            "Brokerages already buy software for this workflow but still bridge gaps manually.",
            "That leaves room for orchestration and exception automation across systems.",
            "The buyer is operationally mature and measurable."
        ], d.b.NAVY, d.b.TEAL, d.b.LIGHT_TEAL),
    ]
    for x, (title, items, fill, title_color, body_color) in zip(xs, blocks):
        d.rect(s, x, Inches(1.78), col_w, Inches(3.65), fill, radius=0.05, shadow=True)
        d.text(s, title, x + Inches(0.2), Inches(1.95), col_w - Inches(0.4), Inches(0.24), size=16, color=title_color, bold=True)
        d.text(s, [{"text": item, "bullet": True, "size": 11.0, "color": body_color, "space_before": 8} for item in items],
               x + Inches(0.22), Inches(2.28), col_w - Inches(0.42), Inches(2.75), shrink=True)
    footer(d, s, 4, total)


def architecture_stack(d: Deck, total: int):
    s = header_slide(d, "The reference architecture is back-office-native and OpenHands-orchestrated",
                     "Structured stack slide grounded in Brokermint, Docusign, and verified OpenHands capabilities")
    left_w = Inches(5.8)
    right_x = d.M + left_w + Inches(0.35)
    d.rect(s, d.M, Inches(1.75), left_w, Inches(4.4), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "ORCHESTRATION AND INTEGRATION STACK", d.M + Inches(0.22), Inches(1.95), left_w - Inches(0.4), Inches(0.24), size=15, color=d.b.TEAL, bold=True)
    stack_points = [
        "OpenHands SDK agents orchestrate payout validation, exception handling, and task routing.",
        "OpenHands skills hold plan logic, approval policies, and escalation rules.",
        "CLI and headless execution support repeatable back-office runs and queue processing.",
        "Back-office, accounting, and document systems feed the workflow layer.",
        "The brokerage ops and finance stack remains the system of action."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.0, "color": d.b.WHITE, "space_before": 8} for item in stack_points],
           d.M + Inches(0.22), Inches(2.28), left_w - Inches(0.44), Inches(3.35), shrink=True)
    cards = [
        ("Systems of record", "Back-office software, accounting ledgers, transaction tools, and document workflows."),
        ("Deployment stance", "OpenHands is the internal execution layer; finance and ops remain in control."),
    ]
    cy = Inches(1.75)
    card_h = Inches(1.98)
    for title, body in cards:
        d.rect(s, right_x, cy, Inches(6.0), card_h, d.b.SOFT, radius=0.05, shadow=True)
        d.text(s, title, right_x + Inches(0.2), cy + Inches(0.16), Inches(5.6), Inches(0.28), size=14.0, color=d.b.NAVY, bold=True, shrink=True)
        d.text(s, body, right_x + Inches(0.2), cy + Inches(0.5), Inches(5.6), Inches(1.18), size=10.3, color=d.b.INK, shrink=True)
        cy += Inches(2.12)
    footer(d, s, 5, total)


def score_risks(d: Deck, total: int):
    s = header_slide(d, "The lane is attractive, but payout-control discipline matters",
                     "Structured score-and-risk slide")
    d.rect(s, d.M, Inches(1.75), Inches(4.1), Inches(4.4), d.b.SOFT, radius=0.05, shadow=True)
    d.text(s, "VERTICAL SCORECARD", d.M + Inches(0.22), Inches(1.95), Inches(3.7), Inches(0.22), size=15, color=d.b.NAVY, bold=True)
    scores = [
        "Intelligence Ratio: 4/5",
        "Outsourcing Readiness: 4/5",
        "TAM Accessibility: 4/5",
        "Data Moat Potential: 3/5",
        "Regulatory Friction: 3/5",
        "Incumbent Vulnerability: 4/5",
        "Mirage PMF Risk: 4/5",
        "Composite: 26/35 — GO",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.4, "color": d.b.INK, "space_before": 6} for item in scores],
           d.M + Inches(0.22), Inches(2.28), Inches(3.6), Inches(2.7), shrink=True)
    d.rect(s, Inches(5.0), Inches(1.75), Inches(7.7), Inches(4.4), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "RISKS AND CONTROLS", Inches(5.22), Inches(1.95), Inches(3.2), Inches(0.22), size=15, color=d.b.TEAL, bold=True)
    risks = [
        "Bad payout logic damages trust fast — keep release authority human-controlled.",
        "Plan exceptions can sprawl — encode explicit rules and escalation policy.",
        "System fragmentation slows rollout — begin with one stack and one queue.",
        "Finance skepticism is rational — keep auditability visible at each step."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.0, "color": d.b.LIGHT_TEAL, "space_before": 8} for item in risks],
           Inches(5.22), Inches(2.28), Inches(7.1), Inches(2.85), shrink=True)
    footer(d, s, 6, total)


def roadmap_and_account(d: Deck, total: int):
    s = header_slide(d, "A focused payout pilot and a network-brokerage angle make the offer concrete",
                     "Structured execution and account slide")
    d.rect(s, d.M, Inches(1.75), Inches(6.1), Inches(4.55), d.b.SOFT, radius=0.05, shadow=True)
    d.text(s, "90-DAY ROADMAP", d.M + Inches(0.22), Inches(1.95), Inches(2.5), Inches(0.22), size=15, color=d.b.NAVY, bold=True)
    roadmap = [
        "Days 1-15: map transaction sources, payout logic, exception queues, and approval controls.",
        "Days 16-35: configure OpenHands workflow logic, integrations, and audit views.",
        "Days 36-60: launch validation and exception routing for one ops team or queue.",
        "Days 61-90: measure cycle time, refine rules, and scope accounting or document expansion."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.0, "color": d.b.INK, "space_before": 8} for item in roadmap],
           d.M + Inches(0.22), Inches(2.28), Inches(5.6), Inches(3.4), shrink=True)
    rx = Inches(6.95)
    d.rect(s, rx, Inches(1.75), Inches(5.75), Inches(4.55), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "NETWORK BROKERAGE ANGLE", rx + Inches(0.22), Inches(1.95), Inches(3.2), Inches(0.22), size=15, color=d.b.TEAL, bold=True)
    account = [
        "Scaled brokerage networks feel payout delays and exceptions more acutely.",
        "The next value is workflow orchestration across systems, not another dashboard.",
        "Pitch OpenHands as the internal layer for reusable payout and approval skills.",
        "Recommended next step: choose one payout queue and one measurable latency goal."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 10.8, "color": d.b.LIGHT_TEAL, "space_before": 8} for item in account],
           rx + Inches(0.22), Inches(2.28), Inches(5.25), Inches(3.4), shrink=True)
    footer(d, s, 7, total)


def closing(d: Deck, total: int):
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.16), d.b.TEAL)
    d.text(s, "BOTTOM LINE", d.M, Inches(1.15), Inches(3), Inches(0.25), size=16, color=d.b.TEAL, bold=True)
    d.text(s, "Commission and payout automation is a client-ready AI engineering offer when it improves accuracy and throughput inside the brokerage back-office stack.", d.M, Inches(1.6), Inches(11.6), Inches(1.3), size=22, color=d.b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(3.15), Inches(11.9), Inches(0.06), d.b.GOLD)
    final_points = [
        "Use back-office and accounting systems as the systems of action.",
        "Use OpenHands internally for orchestration, skills, and repeatable payout workflows.",
        "Start with one queue, one ops team, and one measurable cycle-time outcome.",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 15.0, "color": d.b.LIGHT_TEAL, "space_before": 10} for item in final_points],
           d.M, Inches(3.45), Inches(10.9), Inches(1.8), shrink=True)
    d.rect(s, d.M, Inches(5.85), Inches(6.1), Inches(0.72), d.b.GOLD, radius=0.05)
    d.text(s, "Suggested next step: approve a pilot for one payout workflow and exception queue.",
           d.M + Inches(0.3), Inches(6.03), Inches(11.3), Inches(0.42), size=11.2, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 8, total, dark=True)


def main():
    total = 8
    d = Deck(footer="Real Estate Commission Automation | Client Package | June 2026")
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, d.W - Inches(3.0), 0, Inches(3.0), d.H, d.b.NAVY_2)
    d.rect(s, d.W - Inches(3.0), 0, Inches(0.06), d.H, d.b.TEAL)
    d.text(s, "CLIENT PACKAGE", d.M, Inches(0.95), Inches(3), Inches(0.25), size=15, color=d.b.TEAL, bold=True)
    d.text(s, "Brokerage Commission\nAutomation", d.M, Inches(1.45), Inches(7.6), Inches(1.28), size=31, color=d.b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.75), Inches(1.6), Inches(0.06), d.b.TEAL)
    d.text(s, "A branded strategy and presales package built from the real-estate use case in the framework document and validated with current Brokermint, Docusign, and OpenHands signals.",
           d.M, Inches(3.05), Inches(7.8), Inches(1.2), size=15.2, color=d.b.WHITE, shrink=True)
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
