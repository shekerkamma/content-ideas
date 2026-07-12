#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

BRANDED_SKILL = Path("/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(BRANDED_SKILL))

from pptxkit import Deck, Inches, PP_ALIGN  # type: ignore

RUN_DIR = Path(__file__).resolve().parent
OUT = RUN_DIR / "real-estate-portfolio-index-client-package-branded-draft.pptx"

LANES = [
    {
        "title": "Brokerage Lead Routing & Transaction Automation",
        "score": "25/35 — GO",
        "buyer": "Brokerage revenue and ops teams",
        "proof": "Compass, Zillow, Cloze",
        "outcome": "Faster speed-to-lead, better follow-up, cleaner transaction handoffs",
    },
    {
        "title": "Multifamily Leasing & Resident Communication Automation",
        "score": "26/35 — GO",
        "buyer": "Leasing, community, and regional ops",
        "proof": "AppFolio, Yardi, Greystar",
        "outcome": "Better prospect response, renewal flow, and resident communication",
    },
    {
        "title": "Brokerage Commission & Deal Payout Automation",
        "score": "26/35 — GO",
        "buyer": "Brokerage ops and finance",
        "proof": "Brokermint, BoldTrail BackOffice, Docusign",
        "outcome": "Faster payouts, fewer exceptions, cleaner accounting handoffs",
    },
    {
        "title": "Service Request & Maintenance Automation",
        "score": "26/35 — GO",
        "buyer": "Property ops and maintenance teams",
        "proof": "AppFolio, Buildium, Yardi",
        "outcome": "Faster routing, better queue visibility, stronger resident updates",
    },
    {
        "title": "Title, Escrow & Closing Workflow Automation",
        "score": "26/35 — GO",
        "buyer": "Title, escrow, and closing teams",
        "proof": "Qualia, SoftPro, Docusign",
        "outcome": "Cleaner file setup, fewer missing items, better closing readiness",
    },
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
        "Five reviewed lanes show a coherent real-estate AI engineering portfolio",
        "Portfolio summary built from five reviewed client decks completed on June 4, 2026",
    )
    y = Inches(1.75)
    col_w = Inches(3.92)
    gap = Inches(0.22)
    xs = [d.M, d.M + col_w + gap, d.M + 2 * (col_w + gap)]
    titles = ["Where to play", "Why it works", "What to do"]
    bodies = [
        [
            "Brokerage revenue workflows",
            "Leasing and resident operations",
            "Back-office, maintenance, and closing coordination",
        ],
        [
            "All five lanes are operational, measurable, and already budget-adjacent.",
            "Incumbent software proves buyer awareness while leaving room for workflow orchestration.",
            "OpenHands creates a reusable internal execution layer across the whole portfolio.",
        ],
        [
            "Package the portfolio as a workflow-automation thesis, not isolated chatbot ideas.",
            "Lead with one narrow pilot per buyer group and one measurable operational outcome.",
            "Reuse branded decks, OpenHands patterns, and QA gates across lanes.",
        ],
    ]
    colors = [d.b.SOFT, d.b.SOFT, d.b.NAVY]
    for idx, x in enumerate(xs):
        d.rect(s, x, y, col_w, Inches(3.45), colors[idx], radius=0.05, shadow=True)
        d.text(s, titles[idx], x + Inches(0.22), y + Inches(0.18), col_w - Inches(0.4), Inches(0.25),
               size=16, color=d.b.TEAL if idx == 2 else d.b.NAVY, bold=True)
        d.text(s, [{"text": item, "bullet": True, "size": 11.6, "color": d.b.LIGHT_TEAL if idx == 2 else d.b.INK, "space_before": 7} for item in bodies[idx]],
               x + Inches(0.22), y + Inches(0.55), col_w - Inches(0.4), Inches(2.6), shrink=True)
    d.rect(s, d.M, Inches(5.55), d.CW, Inches(0.62), d.b.GOLD, radius=0.05)
    d.text(s, "THE ASK: use this index deck to choose the first real-estate wedge, then pair it with the matching reviewed lane deck.",
           d.M + Inches(0.25), Inches(5.68), d.CW - Inches(0.5), Inches(0.28), size=10.8, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 2, total)


def portfolio_map(d: Deck, total: int):
    s = header_slide(
        d,
        "The portfolio spans five lanes across revenue, operations, back office, and closing",
        "Each lane is a reviewed client-ready artifact with a distinct buyer and a clear operational wedge",
    )
    left_w = Inches(6.2)
    right_x = d.M + left_w + Inches(0.35)
    d.rect(s, d.M, Inches(1.75), left_w, Inches(4.45), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "PORTFOLIO MAP", d.M + Inches(0.22), Inches(1.95), Inches(2.0), Inches(0.22), size=15, color=d.b.TEAL, bold=True)
    map_points = [
        "1. Brokerage lead routing and transaction follow-up",
        "2. Multifamily leasing and resident communication",
        "3. Brokerage commission and payout automation",
        "4. Property service-request and maintenance operations",
        "5. Title, escrow, and closing workflow automation",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.2, "color": d.b.WHITE, "space_before": 8} for item in map_points],
           d.M + Inches(0.22), Inches(2.28), left_w - Inches(0.44), Inches(3.3), shrink=True)
    cards = [
        ("Score pattern", "Four lanes scored 26/35 GO; one lane scored 25/35 GO."),
        ("Shared posture", "Use incumbent systems as systems of action and OpenHands internally for orchestration."),
    ]
    cy = Inches(1.75)
    for title, body in cards:
        d.rect(s, right_x, cy, Inches(5.75), Inches(2.05), d.b.SOFT, radius=0.05, shadow=True)
        d.text(s, title, right_x + Inches(0.2), cy + Inches(0.16), Inches(5.35), Inches(0.28), size=14.0, color=d.b.NAVY, bold=True, shrink=True)
        d.text(s, body, right_x + Inches(0.2), cy + Inches(0.5), Inches(5.35), Inches(1.05), size=10.5, color=d.b.INK, shrink=True)
        cy += Inches(2.25)
    footer(d, s, 3, total)


def lane_matrix(d: Deck, total: int):
    s = header_slide(
        d,
        "The five lanes can be compared directly by buyer, proof point, and outcome",
        "Matrix view for selecting the best first wedge by account or operating pain",
    )
    x0 = d.M
    widths = [Inches(3.05), Inches(1.45), Inches(2.6), Inches(2.8), Inches(3.0)]
    headers = ["Lane", "Score", "Primary Buyer", "Proof", "Outcome"]
    xs = [x0]
    for w in widths[:-1]:
        xs.append(xs[-1] + w)
    y = Inches(1.85)
    for x, w, h in zip(xs, widths, headers):
        d.rect(s, x, y, w, Inches(0.45), d.b.NAVY)
        d.text(s, h, x + Inches(0.08), y + Inches(0.1), w - Inches(0.16), Inches(0.2), size=10.5, color=d.b.TEAL, bold=True, shrink=True)
    row_y = y + Inches(0.5)
    fills = [d.b.SOFT, d.b.WHITE]
    for i, lane in enumerate(LANES):
        fill = fills[i % 2]
        h = Inches(0.92)
        row = [lane["title"], lane["score"], lane["buyer"], lane["proof"], lane["outcome"]]
        for x, w, cell in zip(xs, widths, row):
            d.rect(s, x, row_y, w, h, fill)
            d.text(s, cell, x + Inches(0.08), row_y + Inches(0.08), w - Inches(0.16), h - Inches(0.16), size=9.0, color=d.b.INK, shrink=True)
        row_y += h + Inches(0.05)
    footer(d, s, 4, total)


def wedge_summary(d: Deck, total: int, idx: int, title: str, lanes: list[dict], page: int):
    s = header_slide(d, title, "Grouped lane view for buyer selection and next-step positioning")
    left, right = lanes
    for col, lane in enumerate([left, right]):
        x = d.M + col * (Inches(6.15) + Inches(0.35))
        fill = d.b.SOFT if col == 0 else d.b.NAVY
        title_color = d.b.NAVY if col == 0 else d.b.TEAL
        body_color = d.b.INK if col == 0 else d.b.LIGHT_TEAL
        d.rect(s, x, Inches(1.78), Inches(6.15), Inches(4.65), fill, radius=0.05, shadow=True)
        d.text(s, lane["title"], x + Inches(0.22), Inches(1.98), Inches(5.7), Inches(0.52), size=15, color=title_color, bold=True, shrink=True)
        bullets = [
            f"Score: {lane['score']}",
            f"Buyer: {lane['buyer']}",
            f"Proof: {lane['proof']}",
            f"Outcome: {lane['outcome']}",
        ]
        d.text(s, [{"text": item, "bullet": True, "size": 11.1, "color": body_color, "space_before": 8} for item in bullets],
               x + Inches(0.22), Inches(2.55), Inches(5.7), Inches(2.45), shrink=True)
        d.rect(s, x + Inches(0.22), Inches(5.18), Inches(5.72), Inches(0.72), d.b.GOLD, radius=0.05)
        d.text(s, "Use the reviewed lane deck for direct account follow-up and the portfolio deck for top-of-funnel selection.",
               x + Inches(0.38), Inches(5.38), Inches(5.35), Inches(0.3), size=9.4, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, page, total)


def single_lane_spotlight(d: Deck, total: int, lane: dict, page: int):
    s = header_slide(d, "Closing workflow lane deserves its own spotlight because it extends the portfolio into transaction-finance operations",
                     "Single-lane detail for title, escrow, and closing readiness buyers")
    d.rect(s, d.M, Inches(1.78), Inches(12.25), Inches(4.7), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, lane["title"], d.M + Inches(0.24), Inches(2.02), Inches(8.2), Inches(0.4), size=20, color=d.b.TEAL, bold=True, shrink=True)
    bullets = [
        f"Score: {lane['score']}",
        f"Primary buyer: {lane['buyer']}",
        f"Operator proof: {lane['proof']}",
        f"Primary outcome: {lane['outcome']}",
        "Why it matters: this lane reaches title, escrow, and closing operators beyond brokerage and property-management teams.",
        "Best portfolio use: position it as the transaction-coordination wedge when the buyer pain is missing-item backlog or closing readiness.",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 12.0, "color": d.b.LIGHT_TEAL, "space_before": 8} for item in bullets],
           d.M + Inches(0.24), Inches(2.55), Inches(7.0), Inches(2.8), shrink=True)
    d.rect(s, Inches(8.35), Inches(2.0), Inches(4.1), Inches(3.95), d.b.SOFT, radius=0.05, shadow=True)
    d.text(s, "Portfolio role", Inches(8.58), Inches(2.18), Inches(3.6), Inches(0.28), size=14.5, color=d.b.NAVY, bold=True, shrink=True)
    role_lines = [
        "Expands the portfolio into closing operations.",
        "Supports title, escrow, lender, and partner workflows.",
        "Pairs well with Docusign- and Qualia-led account conversations.",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 10.8, "color": d.b.INK, "space_before": 8} for item in role_lines],
           Inches(8.58), Inches(2.58), Inches(3.4), Inches(2.4), shrink=True)
    footer(d, s, page, total)


def closing(d: Deck, total: int):
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.16), d.b.TEAL)
    d.text(s, "BOTTOM LINE", d.M, Inches(1.15), Inches(3), Inches(0.25), size=16, color=d.b.TEAL, bold=True)
    d.text(s, "The reviewed real-estate portfolio is now broad enough to support wedge selection by buyer, workflow pain, and account motion without rebuilding the strategy from scratch.", d.M, Inches(1.6), Inches(11.6), Inches(1.3), size=22, color=d.b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(3.15), Inches(11.9), Inches(0.06), d.b.GOLD)
    final_points = [
        "Use the portfolio deck for index-level selection and account mapping.",
        "Use the reviewed lane decks for specific client conversations and follow-on customization.",
        "Reuse OpenHands, branded deck, and QA patterns across every additional lane.",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 15.0, "color": d.b.LIGHT_TEAL, "space_before": 10} for item in final_points],
           d.M, Inches(3.45), Inches(10.9), Inches(1.8), shrink=True)
    d.rect(s, d.M, Inches(5.85), Inches(6.4), Inches(0.72), d.b.GOLD, radius=0.05)
    d.text(s, "Suggested next step: pick the first buyer lane, then pair this index deck with the corresponding reviewed use-case deck.",
           d.M + Inches(0.3), Inches(6.58), Inches(11.3), Inches(0.36), size=10.8, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 8, total, dark=True)


def main():
    total = 8
    d = Deck(footer="Real Estate Portfolio Index | Client Package | June 2026")
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, d.W - Inches(3.0), 0, Inches(3.0), d.H, d.b.NAVY_2)
    d.rect(s, d.W - Inches(3.0), 0, Inches(0.06), d.H, d.b.TEAL)
    d.text(s, "CLIENT PACKAGE", d.M, Inches(0.95), Inches(3), Inches(0.25), size=15, color=d.b.TEAL, bold=True)
    d.text(s, "Real Estate Portfolio\nIndex", d.M, Inches(1.45), Inches(7.6), Inches(1.28), size=31, color=d.b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.75), Inches(1.6), Inches(0.06), d.b.TEAL)
    d.text(s, "A branded portfolio-level index over five reviewed real-estate AI workflow decks: brokerage, leasing, commission, service ops, and title/escrow.", d.M, Inches(3.05), Inches(7.8), Inches(1.2), size=15.2, color=d.b.WHITE, shrink=True)
    d.text(s, "PORTFOLIO THESIS · LANE MAP · SELECTION MATRIX · BUYER GROUPING · NEXT STEP",
           d.M, Inches(5.75), Inches(8.6), Inches(0.28), size=11, color=d.b.GOLD, bold=True)
    footer(d, s, 1, total, dark=True)
    executive_summary(d, total)
    portfolio_map(d, total)
    lane_matrix(d, total)
    wedge_summary(d, total, 1, "Front-office and resident-growth lanes", [LANES[0], LANES[1]], 5)
    wedge_summary(d, total, 2, "Back-office, service, and closing lanes", [LANES[2], LANES[3]], 6)
    single_lane_spotlight(d, total, LANES[4], 7)
    closing(d, total)
    d.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
