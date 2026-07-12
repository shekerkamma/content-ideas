#!/usr/bin/env python3
"""Build the branded client-facing PPTX for manufacturing predictive maintenance.

Uses the branded-pptx-deck workflow (`pptxkit`) and includes a detailed
use-case realization slide with structured content on every slide.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

BRANDED_SKILL = Path("/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(BRANDED_SKILL))

from pptxkit import Deck, Inches, Pt, PP_ALIGN, RGBColor, MSO_ANCHOR  # type: ignore

RUN_DIR = Path(__file__).resolve().parent
OUT = RUN_DIR / "manufacturing-predictive-maintenance-client-package-branded.pptx"
FEED = json.loads((RUN_DIR / "feed-data.json").read_text(encoding="utf-8"))
UC = FEED["useCases"][0]


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
        "Predictive maintenance is a credible wedge for AI engineering services",
        "Executive summary built from the PDF use case, Hyundai deployment proof, SAP workflow signals, and verified OpenHands capabilities",
    )
    y = Inches(1.75)
    col_w = Inches(3.92)
    gap = Inches(0.22)
    xs = [d.M, d.M + col_w + gap, d.M + 2 * (col_w + gap)]
    titles = ["Situation", "Insight", "Recommendation"]
    bodies = [
        [
            "Unplanned downtime remains expensive and visible in discrete manufacturing.",
            "Hyundai is already scaling predictive robotics maintenance in production.",
            "Maintenance is still under-mature despite broader smart-manufacturing investment."
        ],
        [
            "The value is not generic AI experimentation; it is maintenance action inside SAP PM.",
            "The strongest beachhead is one downtime-critical asset family.",
            "OpenHands fits as the internal orchestration layer for repeatable agent delivery."
        ],
        [
            "Run a 90-day pilot tied to one asset family and one planner workflow.",
            "Use OpenHands agents + MCP-style integrations behind the scenes, not as the customer-facing pitch.",
            "Measure downtime reduction, false positives, and maintenance response quality."
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
    d.text(s, "THE ASK: approve a discovery sprint for one asset family and leave behind reusable OpenHands delivery patterns.",
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
    d.text(s, UC["title"], d.M, Inches(0.56), panel_w - Inches(1.0), Inches(0.62), size=25, color=d.b.WHITE, bold=True, shrink=True)

    # Challenge and solution cards
    card_y = Inches(1.25)
    card_h = Inches(1.55)
    gap = Inches(0.22)
    card_w = (panel_w - d.M * 2 - gap) / 2
    for idx, (title, items) in enumerate([("Challenge", UC["challenge"]), ("Solution", UC["solution"])]):
        x = d.M + idx * (card_w + gap)
        d.rect(s, x, card_y, card_w, card_h, d.b.WHITE, radius=0.06, shadow=True)
        d.text(s, title.upper(), x + Inches(0.18), card_y + Inches(0.15), card_w - Inches(0.36), Inches(0.22),
               size=12, color=d.b.ACCENT, bold=True)
        d.text(
            s,
            [{"text": item, "bullet": True, "size": 10.3, "color": d.b.INK, "space_before": 4} for item in items],
            x + Inches(0.18), card_y + Inches(0.42), card_w - Inches(0.32), Inches(0.95), shrink=True, ls=1.0
        )

    # Stats
    sy = Inches(2.98)
    stat_gap = Inches(0.18)
    stat_w = (panel_w - d.M * 2 - stat_gap * 2) / 3
    for i, (num, label) in enumerate(UC["stats"]):
        x = d.M + i * (stat_w + stat_gap)
        d.rect(s, x, sy, stat_w, Inches(0.86), d.b.GOLD, radius=0.05)
        d.text(s, num, x + Inches(0.12), sy + Inches(0.08), stat_w - Inches(0.24), Inches(0.28),
               size=18, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, label, x + Inches(0.12), sy + Inches(0.44), stat_w - Inches(0.24), Inches(0.18),
               size=10.2, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)

    # How it works
    how_y = Inches(4.0)
    d.text(s, "HOW IT WORKS", d.M, how_y, Inches(2.3), Inches(0.22), size=12, color=d.b.NAVY, bold=True)
    step_w = (panel_w - d.M * 2 - Inches(0.6)) / 3
    for i, step in enumerate(UC["how"]):
        x = d.M + i * (step_w + Inches(0.3))
        d.rect(s, x, how_y + Inches(0.28), step_w, Inches(0.92), d.b.WHITE, radius=0.05, shadow=True)
        d.text(s, f"{i+1:02d}", x + Inches(0.12), how_y + Inches(0.36), Inches(0.34), Inches(0.2),
               size=14, color=d.b.GOLD, bold=True)
        d.text(s, step, x + Inches(0.52), how_y + Inches(0.34), step_w - Inches(0.62), Inches(0.48),
               size=9.6, color=d.b.INK, shrink=True, ls=1.0)
        if i < 2:
            d.text(s, "→", x + step_w + Inches(0.05), how_y + Inches(0.55), Inches(0.2), Inches(0.2),
                   size=16, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER)

    # Stack
    st_y = Inches(5.25)
    d.rect(s, d.M, st_y, panel_w - d.M * 2, Inches(0.95), d.b.NAVY, radius=0.05)
    d.text(s, "SOLUTION STACK", d.M + Inches(0.18), st_y + Inches(0.12), Inches(2), Inches(0.2),
           size=12, color=d.b.GOLD, bold=True)
    stack_w = (panel_w - d.M * 2 - Inches(0.72)) / 4
    for i, (layer, detail) in enumerate(UC["stack"][:4]):
        x = d.M + Inches(0.18) + i * stack_w
        d.text(s, layer, x, st_y + Inches(0.34), stack_w - Inches(0.08), Inches(0.18),
               size=9.5, color=d.b.TEAL, bold=True, shrink=True)
        d.text(s, detail, x, st_y + Inches(0.54), stack_w - Inches(0.08), Inches(0.28),
               size=8.4, color=d.b.WHITE, shrink=True, ls=1.0)

    # Systems / users
    by = Inches(6.45)
    bw = (panel_w - d.M * 2 - Inches(0.2)) / 2
    d.rect(s, d.M, by, bw, Inches(0.36), d.b.ACCENT, radius=0.04)
    d.text(s, "SYSTEMS: " + " · ".join(UC["systems"][:5]), d.M + Inches(0.15), by, bw - Inches(0.3), Inches(0.36),
           size=8.3, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.rect(s, d.M + bw + Inches(0.2), by, bw, Inches(0.36), d.b.DARK_TEAL, radius=0.04)
    d.text(s, "USERS: " + UC["users"], d.M + bw + Inches(0.35), by, bw - Inches(0.3), Inches(0.36),
           size=8.3, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)

    # Right strip organizations
    sx = strip_x + Inches(0.3)
    d.text(s, "ORGANIZATIONS", sx, Inches(0.45), strip_w - Inches(0.5), Inches(0.24), size=13, color=d.b.TEAL, bold=True)
    d.text(s, "DELIVERING / BUYING THIS", sx, Inches(0.72), strip_w - Inches(0.5), Inches(0.24), size=13, color=d.b.TEAL, bold=True)
    d.rect(s, sx, Inches(1.08), Inches(1.0), Inches(0.04), d.b.GOLD)
    oy = Inches(1.28)
    for name, desc in UC["orgs"]:
        d.text(s, name, sx, oy, strip_w - Inches(0.5), Inches(0.24), size=14.2, color=d.b.WHITE, bold=True, shrink=True)
        d.text(s, desc, sx, oy + Inches(0.26), strip_w - Inches(0.55), Inches(0.58), size=10.2, color=d.b.LIGHT_TEAL, shrink=True, ls=1.0)
        oy += Inches(1.0)
    footer(d, s, 3, total, dark=True)


def market_landscape(d: Deck, total: int):
    s = header_slide(d, "The business case is strong because downtime is costly",
                     "Structured proof slide with cost of inaction, observed upside, and buyer readiness")
    col_w = Inches(3.95)
    gap = Inches(0.22)
    xs = [d.M, d.M + col_w + gap, d.M + 2 * (col_w + gap)]
    blocks = [
        ("Cost of inaction", [
            "NIST: downtime is 8.3% of planned production time in discrete manufacturing.",
            "NIST: downtime cost reaches $245B across discrete manufacturing.",
            "Deloitte: industrial manufacturers face a $50B annual unplanned-downtime problem."
        ], d.b.SOFT, d.b.NAVY, d.b.INK),
        ("Observed upside", [
            "Deloitte: smart-manufacturing adopters report 10% to 20% production-output improvement.",
            "Predictive maintenance benchmarks point to 53% less unplanned downtime and 79% fewer defects.",
            "Maintenance is one of the least mature but most investment-ready functions."
        ], d.b.SOFT, d.b.NAVY, d.b.INK),
        ("Buyer readiness", [
            "65% to 70% of manufacturers outsource AI, automation, data, and cybersecurity roles.",
            "This supports a services-led entry model for implementation-heavy workflows.",
            "The beachhead is a narrow pilot, not enterprise-wide autonomous maintenance on day one."
        ], d.b.NAVY, d.b.TEAL, d.b.LIGHT_TEAL),
    ]
    for x, (title, items, fill, title_color, body_color) in zip(xs, blocks):
        d.rect(s, x, Inches(1.78), col_w, Inches(3.65), fill, radius=0.05, shadow=True)
        d.text(s, title, x + Inches(0.2), Inches(1.95), col_w - Inches(0.4), Inches(0.24),
               size=16, color=title_color, bold=True)
        d.text(s, [{"text": item, "bullet": True, "size": 11.6, "color": body_color, "space_before": 8} for item in items],
               x + Inches(0.22), Inches(2.28), col_w - Inches(0.42), Inches(2.75), shrink=True)
    footer(d, s, 4, total)


def architecture_stack(d: Deck, total: int):
    s = header_slide(d, "The reference architecture is SAP-native and OpenHands-orchestrated",
                     "Structured stack slide grounded in verified OpenHands, SAP, and source-PDF capabilities")
    left_w = Inches(5.8)
    right_x = d.M + left_w + Inches(0.35)
    d.rect(s, d.M, Inches(1.75), left_w, Inches(4.4), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "ORCHESTRATION AND INTEGRATION STACK", d.M + Inches(0.22), Inches(1.95), left_w - Inches(0.4), Inches(0.24),
           size=15, color=d.b.TEAL, bold=True)
    stack_points = [
        "OpenHands SDK agents orchestrate anomaly analysis, summarization, and operator decision support.",
        "OpenHands skills / repository agents carry manufacturing-specific workflow and guardrail logic.",
        "CLI and headless execution support scheduled jobs, incident runs, and repeatable delivery operations.",
        "MCP-compatible integrations connect enterprise tools and external servers where needed.",
        "SAP PM / APM remains the action system for work orders, planners, and technicians."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.5, "color": d.b.WHITE, "space_before": 8} for item in stack_points],
           d.M + Inches(0.22), Inches(2.28), left_w - Inches(0.44), Inches(3.35), shrink=True)
    # right cards
    cards = [
        ("Systems of record", "SAP PM, SAP APM, MES, historians, gateways, and asset data."),
        ("Deployment stance and fit", "OpenHands is the reusable execution layer; SAP remains the system of action."),
    ]
    cy = Inches(1.75)
    card_h = Inches(1.98)
    for title, body in cards:
        d.rect(s, right_x, cy, Inches(6.0), card_h, d.b.SOFT, radius=0.05, shadow=True)
        d.text(s, title, right_x + Inches(0.2), cy + Inches(0.16), Inches(5.6), Inches(0.28), size=14.0, color=d.b.NAVY, bold=True, shrink=True)
        d.text(s, body, right_x + Inches(0.2), cy + Inches(0.5), Inches(5.6), Inches(1.18), size=10.8, color=d.b.INK, shrink=True)
        cy += Inches(2.12)
    footer(d, s, 5, total)


def score_risks(d: Deck, total: int):
    s = header_slide(d, "The use case is attractive, but rollout discipline matters more than novelty",
                     "Structured score-and-risk slide")
    d.rect(s, d.M, Inches(1.75), Inches(4.1), Inches(4.4), d.b.SOFT, radius=0.05, shadow=True)
    d.text(s, "VERTICAL SCORECARD", d.M + Inches(0.22), Inches(1.95), Inches(3.7), Inches(0.22), size=15, color=d.b.NAVY, bold=True)
    scores = [
        "Intelligence Ratio: 4/5",
        "Outsourcing Readiness: 4/5",
        "TAM Accessibility: 4/5",
        "Data Moat Potential: 4/5",
        "Regulatory Friction: 3/5",
        "Incumbent Vulnerability: 3/5",
        "Mirage PMF Risk: 3/5",
        "Composite: 25/35 — GO",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.8, "color": d.b.INK, "space_before": 6} for item in scores],
           d.M + Inches(0.22), Inches(2.28), Inches(3.6), Inches(2.7), shrink=True)
    d.rect(s, Inches(5.0), Inches(1.75), Inches(7.7), Inches(4.4), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "RISKS AND CONTROLS", Inches(5.22), Inches(1.95), Inches(3.2), Inches(0.22), size=15, color=d.b.TEAL, bold=True)
    risks = [
        "False positives erode technician trust — start with assisted triage and conservative thresholds.",
        "Weak maintenance history limits value — begin with a well-instrumented asset family.",
        "OT security slows access to plant data — use edge-first or read-only integration where needed.",
        "IT/OT/maintenance ownership is unclear — require an executive sponsor and named maintenance lead."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.6, "color": d.b.LIGHT_TEAL, "space_before": 8} for item in risks],
           Inches(5.22), Inches(2.28), Inches(7.1), Inches(2.85), shrink=True)
    footer(d, s, 6, total)


def roadmap_and_account(d: Deck, total: int):
    s = header_slide(d, "A 90-day pilot and Hyundai-specific expansion path make the offer concrete",
                     "Structured execution and account slide")
    d.rect(s, d.M, Inches(1.75), Inches(6.1), Inches(4.55), d.b.SOFT, radius=0.05, shadow=True)
    d.text(s, "90-DAY ROADMAP", d.M + Inches(0.22), Inches(1.95), Inches(2.5), Inches(0.22), size=15, color=d.b.NAVY, bold=True)
    roadmap = [
        "Days 1-15: select one asset family, review failure modes, map telemetry and SAP PM workflow, complete OT/security review.",
        "Days 16-45: ingest telemetry, establish baseline analytics, configure OpenHands orchestration and integration adapters.",
        "Days 46-75: launch pilot alerts, technician workflow, and false-positive tuning loop.",
        "Days 76-90: measure downtime, response quality, and operational fit; package the expansion template for the next plant or asset family."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.5, "color": d.b.INK, "space_before": 8} for item in roadmap],
           d.M + Inches(0.22), Inches(2.28), Inches(5.6), Inches(3.4), shrink=True)
    rx = Inches(6.95)
    d.rect(s, rx, Inches(1.75), Inches(5.75), Inches(4.55), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "HYUNDAI ACCOUNT ANGLE", rx + Inches(0.22), Inches(1.95), Inches(3.0), Inches(0.22), size=15, color=d.b.TEAL, bold=True)
    account = [
        "Hyundai already proved predictive maintenance on robotics at production scale.",
        "The next value is cross-asset and cross-plant standardization, not proving the concept again.",
        "Pitch the offer as rollout acceleration around SAP PM workflow integration with reusable OpenHands-based orchestration behind the scenes.",
        "Recommended next step: run a discovery sprint on one asset family beyond robotics and quantify the gap to broader manufacturing standardization."
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.4, "color": d.b.LIGHT_TEAL, "space_before": 8} for item in account],
           rx + Inches(0.22), Inches(2.28), Inches(5.25), Inches(3.4), shrink=True)
    footer(d, s, 7, total)


def closing(d: Deck, total: int):
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.16), d.b.TEAL)
    d.text(s, "BOTTOM LINE", d.M, Inches(1.15), Inches(3), Inches(0.25), size=16, color=d.b.TEAL, bold=True)
    d.text(s, "Predictive maintenance is a client-ready AI engineering offer when it is sold as operational reliability and delivered through a reusable branded orchestration layer.", d.M, Inches(1.6), Inches(11.6), Inches(1.3), size=22, color=d.b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(3.15), Inches(11.9), Inches(0.06), d.b.GOLD)
    final_points = [
        "Use SAP PM as the system of action.",
        "Use OpenHands internally for agent orchestration, skills, and repeatable delivery patterns.",
        "Start with one asset family, one workflow, and one measurable operational outcome.",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 16, "color": d.b.LIGHT_TEAL, "space_before": 10} for item in final_points],
           d.M, Inches(3.45), Inches(10.9), Inches(1.8), shrink=True)
    d.rect(s, d.M, Inches(5.85), Inches(6.3), Inches(0.72), d.b.GOLD, radius=0.05)
    d.text(s, "Suggested next step: approve a discovery sprint for the selected asset family.",
           d.M + Inches(0.3), Inches(6.04), Inches(11.3), Inches(0.42), size=11.5, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 8, total, dark=True)


def main():
    total = 8
    d = Deck(footer="Manufacturing Predictive Maintenance | Client Package | June 2026")

    # cover
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, d.W - Inches(3.0), 0, Inches(3.0), d.H, d.b.NAVY_2)
    d.rect(s, d.W - Inches(3.0), 0, Inches(0.06), d.H, d.b.TEAL)
    d.text(s, "CLIENT PACKAGE", d.M, Inches(0.95), Inches(3), Inches(0.25), size=15, color=d.b.TEAL, bold=True)
    d.text(s, "Manufacturing Predictive Maintenance", d.M, Inches(1.45), Inches(8.2), Inches(1.2), size=40, color=d.b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.75), Inches(1.6), Inches(0.06), d.b.TEAL)
    d.text(s, "A branded strategy and presales package built from UC06 in the AI Engineering Use Cases Framework, validated with current Hyundai, SAP, Deloitte, NIST, and OpenHands signals.",
           d.M, Inches(3.05), Inches(7.8), Inches(1.2), size=16, color=d.b.WHITE, shrink=True)
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
