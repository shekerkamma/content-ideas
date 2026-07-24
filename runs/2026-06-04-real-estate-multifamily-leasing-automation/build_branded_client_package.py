#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

BRANDED_SKILL = Path("/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(BRANDED_SKILL))

from pptxkit import Deck, Inches, PP_ALIGN, MSO_ANCHOR  # type: ignore

RUN_DIR = Path(__file__).resolve().parent
OUT = RUN_DIR / "real-estate-multifamily-leasing-automation-client-package-branded-draft.pptx"
FEED = json.loads((RUN_DIR / "feed-data.json").read_text(encoding="utf-8"))
UC = FEED["useCases"][0]

SLIDE3_TITLE = "Multifamily Leasing & Resident Communication Automation"
SLIDE3_CHALLENGE = [
    "Slow response and weak follow-up lose prospects.",
    "Leasing and renewal work is split across inboxes and systems.",
    "Site teams want less admin, not another tool to manage.",
]
SLIDE3_SOLUTION = [
    "Triage leasing inquiries and route the next action.",
    "Draft replies, renewals, and document steps in workflow.",
    "Keep humans in control inside the PMS and CRM stack.",
]
SLIDE3_STATS = [
    ("24/7", "AppFolio always-on AI angle"),
    ("Faster", "Yardi response-time focus"),
    ("$2K–5K/mo", "Practical retainer range"),
]
SLIDE3_HOW = [
    "Ingest prospect and resident messages from core channels.",
    "Classify intent, draft replies, and trigger next steps.",
    "Track response, occupancy pipeline, and renewal progress.",
]
SLIDE3_STACK = [
    ("EXPERIENCE", "Leasing inbox + manager view"),
    ("ORCHESTRATION", "OpenHands workflow agents"),
    ("CONTEXT", "PMS, CRM, resident, and doc data"),
    ("ACTUATION", "Replies, tours, renewals, packets"),
]
SLIDE3_ORGS = [
    ("AppFolio", "Incumbent pushing AI leasing workflows."),
    ("Yardi", "Enterprise platform with leasing automation."),
    ("Greystar", "Scaled operator with strong workflow leverage."),
    ("Mid-market operator", "Buyer needing occupancy lift without custom builds."),
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
        "Leasing AI works best when it protects occupancy and removes workflow drag",
        "Executive summary built from the source PDF, AppFolio, Yardi, Docusign, Greystar context, and verified OpenHands capabilities",
    )
    y = Inches(1.75)
    col_w = Inches(3.92)
    gap = Inches(0.22)
    xs = [d.M, d.M + col_w + gap, d.M + 2 * (col_w + gap)]
    titles = ["Situation", "Insight", "Recommendation"]
    bodies = [
        [
            "Operators still lose prospects through slow response and fragmented handoffs.",
            "Incumbents now package AI inside leasing workflows rather than as generic chat.",
            "Document and renewal steps create a credible phase-two expansion path."
        ],
        [
            "The best wedge is inquiry triage, follow-up, and next-step routing.",
            "The offer should live inside PMS and CRM workflows, not beside them.",
            "OpenHands fits as the internal orchestration layer for reusable agent delivery."
        ],
        [
            "Start with one centralized team or regional portfolio.",
            "Measure response time, tour progression, and application or renewal completion.",
            "Expand into lease packets and resident-document workflows after trust is earned."
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
    d.text(s, "THE ASK: approve a pilot for one leasing team or portfolio to improve response speed inside the current stack.",
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
    d.text(s, "SYSTEMS: PMS · CRM · DocuSign · Email/SMS · Listings", d.M + Inches(0.15), by, bw - Inches(0.3), Inches(0.36), size=7.3, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.rect(s, d.M + bw + Inches(0.2), by, bw, Inches(0.36), d.b.DARK_TEAL, radius=0.04)
    d.text(s, "USERS: leasing · manager · resident svc · regional ops", d.M + bw + Inches(0.35), by, bw - Inches(0.3), Inches(0.36), size=7.2, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)

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
    s = header_slide(d, "The category is real because incumbents already package AI into leasing workflows",
                     "Structured proof slide with incumbent evidence, workflow value, and timing")
    col_w = Inches(3.95)
    gap = Inches(0.22)
    xs = [d.M, d.M + col_w + gap, d.M + 2 * (col_w + gap)]
    blocks = [
        ("Incumbent proof", [
            "AppFolio positions Realm-X for always-on leasing workflow support.",
            "Yardi already sells leasing and CRM workflow tooling into the market.",
            "Docusign extends the lane into lease and renewal document execution."
        ], d.b.SOFT, d.b.NAVY, d.b.INK),
        ("Business value", [
            "The core value is faster response, fewer dropped prospects, and cleaner renewals.",
            "Operators can tie success to occupancy pipeline and workflow completion.",
            "Document-heavy tasks create a practical upsell path after phase one."
        ], d.b.SOFT, d.b.NAVY, d.b.INK),
        ("Why now", [
            "The market already expects AI assistance inside workflow tools.",
            "Many teams still operate across inboxes, site teams, and disconnected systems.",
            "That creates room for implementation-led workflow packaging."
        ], d.b.NAVY, d.b.TEAL, d.b.LIGHT_TEAL),
    ]
    for x, (title, items, fill, title_color, body_color) in zip(xs, blocks):
        d.rect(s, x, Inches(1.78), col_w, Inches(3.65), fill, radius=0.05, shadow=True)
        d.text(s, title, x + Inches(0.2), Inches(1.95), col_w - Inches(0.4), Inches(0.24), size=16, color=title_color, bold=True)
        d.text(s, [{"text": item, "bullet": True, "size": 11.2, "color": body_color, "space_before": 8} for item in items],
               x + Inches(0.22), Inches(2.28), col_w - Inches(0.42), Inches(2.75), shrink=True)
    footer(d, s, 4, total)


def architecture_stack(d: Deck, total: int):
    s = header_slide(d, "The reference architecture is PMS-native and OpenHands-orchestrated",
                     "Structured stack slide grounded in AppFolio, Yardi, Docusign, and verified OpenHands capabilities")
    left_w = Inches(5.8)
    right_x = d.M + left_w + Inches(0.35)
    d.rect(s, d.M, Inches(1.75), left_w, Inches(4.4), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "ORCHESTRATION AND INTEGRATION STACK", d.M + Inches(0.22), Inches(1.95), left_w - Inches(0.4), Inches(0.24), size=15, color=d.b.TEAL, bold=True)
    stack_points = [
        "OpenHands SDK agents orchestrate inquiry triage, renewals, and resident workflow support.",
        "OpenHands skills hold leasing rules, response policies, and escalation logic.",
        "CLI and headless execution support repeatable nightly or batch workflow runs.",
        "PMS, CRM, document, and messaging systems feed the workflow layer.",
        "The PMS remains the system of action for site teams and managers."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.0, "color": d.b.WHITE, "space_before": 8} for item in stack_points],
           d.M + Inches(0.22), Inches(2.28), left_w - Inches(0.44), Inches(3.35), shrink=True)
    cards = [
        ("Systems of record", "PMS, CRM, listings, messaging systems, and Docusign-style document tooling."),
        ("Deployment stance", "OpenHands is the internal execution layer; leasing staff stay inside the existing stack."),
    ]
    cy = Inches(1.75)
    card_h = Inches(1.98)
    for title, body in cards:
        d.rect(s, right_x, cy, Inches(6.0), card_h, d.b.SOFT, radius=0.05, shadow=True)
        d.text(s, title, right_x + Inches(0.2), cy + Inches(0.16), Inches(5.6), Inches(0.28), size=14.0, color=d.b.NAVY, bold=True, shrink=True)
        d.text(s, body, right_x + Inches(0.2), cy + Inches(0.5), Inches(5.6), Inches(1.18), size=10.4, color=d.b.INK, shrink=True)
        cy += Inches(2.12)
    footer(d, s, 5, total)


def score_risks(d: Deck, total: int):
    s = header_slide(d, "The lane is attractive, but resident-experience guardrails matter",
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
        "Poor resident experience if automation overreaches — keep sensitive actions assistive.",
        "Policy and fair-housing concerns — encode workflow rules and human approvals.",
        "Tool fragmentation by operator — begin with one stack and one portfolio.",
        "Site-team adoption risk — prove less admin and faster service first."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.1, "color": d.b.LIGHT_TEAL, "space_before": 8} for item in risks],
           Inches(5.22), Inches(2.28), Inches(7.1), Inches(2.85), shrink=True)
    footer(d, s, 6, total)


def roadmap_and_account(d: Deck, total: int):
    s = header_slide(d, "A focused pilot and a Greystar-style account angle make the offer concrete",
                     "Structured execution and account slide")
    d.rect(s, d.M, Inches(1.75), Inches(6.1), Inches(4.55), d.b.SOFT, radius=0.05, shadow=True)
    d.text(s, "90-DAY ROADMAP", d.M + Inches(0.22), Inches(1.95), Inches(2.5), Inches(0.22), size=15, color=d.b.NAVY, bold=True)
    roadmap = [
        "Days 1-15: map inquiry channels, PMS workflow, renewal steps, and service escalation rules.",
        "Days 16-35: configure ingestion, OpenHands workflow logic, and reporting views.",
        "Days 36-60: launch assistive triage and follow-up for one team or portfolio.",
        "Days 61-90: measure lift, refine rules, and scope document or renewal expansion."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.1, "color": d.b.INK, "space_before": 8} for item in roadmap],
           d.M + Inches(0.22), Inches(2.28), Inches(5.6), Inches(3.4), shrink=True)
    rx = Inches(6.95)
    d.rect(s, rx, Inches(1.75), Inches(5.75), Inches(4.55), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "GREYSTAR ACCOUNT ANGLE", rx + Inches(0.22), Inches(1.95), Inches(3.2), Inches(0.22), size=15, color=d.b.TEAL, bold=True)
    account = [
        "Scaled operators gain more from centralized workflow automation than small sites do.",
        "The next value is operational packaging, not another resident-facing bot.",
        "Pitch OpenHands as the internal layer for reusable leasing and renewal workflow skills.",
        "Recommended next step: choose one regional portfolio and one measurable leasing-response objective."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 10.8, "color": d.b.LIGHT_TEAL, "space_before": 8} for item in account],
           rx + Inches(0.22), Inches(2.28), Inches(5.25), Inches(3.4), shrink=True)
    footer(d, s, 7, total)


def closing(d: Deck, total: int):
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.16), d.b.TEAL)
    d.text(s, "BOTTOM LINE", d.M, Inches(1.15), Inches(3), Inches(0.25), size=16, color=d.b.TEAL, bold=True)
    d.text(s, "Leasing and resident workflow automation is a client-ready AI engineering offer when it improves response speed and workflow reliability inside the current PMS and CRM stack.", d.M, Inches(1.6), Inches(11.6), Inches(1.3), size=22, color=d.b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(3.15), Inches(11.9), Inches(0.06), d.b.GOLD)
    final_points = [
        "Use the PMS as the system of action.",
        "Use OpenHands internally for orchestration, skills, and repeatable workflow patterns.",
        "Start with one team, one portfolio, and one measurable occupancy outcome.",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 15.2, "color": d.b.LIGHT_TEAL, "space_before": 10} for item in final_points],
           d.M, Inches(3.45), Inches(10.9), Inches(1.8), shrink=True)
    d.rect(s, d.M, Inches(5.85), Inches(6.2), Inches(0.72), d.b.GOLD, radius=0.05)
    d.text(s, "Suggested next step: approve a pilot for one centralized leasing team or regional portfolio.",
           d.M + Inches(0.3), Inches(6.03), Inches(11.3), Inches(0.42), size=11.2, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 8, total, dark=True)


def main():
    total = 8
    d = Deck(footer="Real Estate Multifamily Leasing Automation | Client Package | June 2026")
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, d.W - Inches(3.0), 0, Inches(3.0), d.H, d.b.NAVY_2)
    d.rect(s, d.W - Inches(3.0), 0, Inches(0.06), d.H, d.b.TEAL)
    d.text(s, "CLIENT PACKAGE", d.M, Inches(0.95), Inches(3), Inches(0.25), size=15, color=d.b.TEAL, bold=True)
    d.text(s, "Multifamily Leasing\nAutomation", d.M, Inches(1.45), Inches(7.6), Inches(1.28), size=31, color=d.b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.75), Inches(1.6), Inches(0.06), d.b.TEAL)
    d.text(s, "A branded strategy and presales package built from the real-estate use case in the framework document and validated with current AppFolio, Yardi, Docusign, Greystar, and OpenHands signals.",
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
