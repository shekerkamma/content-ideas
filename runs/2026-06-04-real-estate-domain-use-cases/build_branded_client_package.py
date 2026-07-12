#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

BRANDED_SKILL = Path("/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(BRANDED_SKILL))

from pptxkit import Deck, Inches, PP_ALIGN, MSO_ANCHOR  # type: ignore

RUN_DIR = Path(__file__).resolve().parent
OUT = RUN_DIR / "real-estate-domain-use-cases-client-package-branded-draft.pptx"

LANES = [
    {
        "kicker": "USE CASE 01  · BROKERAGE",
        "title": "Brokerage Lead Routing & Transaction Automation",
        "challenge": [
            "Slow response and weak routing waste paid and marketplace leads.",
            "Transaction work is split across CRM, docs, and finance tools.",
            "Agents reject tools that add admin without measurable lift.",
        ],
        "solution": [
            "Score and route inbound leads inside the CRM workflow.",
            "Automate follow-up, milestone nudges, and document prep.",
            "Keep automation assistive so adoption risk stays manageable.",
        ],
        "stats": [("25/35", "Reviewed lane score"), ("36%", "Cloze AI sales-lift claim"), ("30 sec", "Zillow routing timer")],
        "how": [
            "Ingest leads from portals, campaigns, and forms.",
            "Score intent and assign the next best owner and action.",
            "Track conversion, follow-up, and milestones in the CRM stack.",
        ],
        "stack": [
            ("EXPERIENCE", "CRM workspace + manager dashboard"),
            ("ORCHESTRATION", "OpenHands routing and workflow agents"),
            ("CONTEXT", "CRM, lead, listing, and milestone data"),
            ("ACTUATION", "Assignments, drafts, DocuSign, commissions"),
        ],
        "systems": "CRM · Zillow · DocuSign · QuickBooks · marketing systems",
        "users": "broker-owner · team lead · ops · agent · marketing",
        "orgs": [
            ("Compass", "Large brokerage with expanding AI workflow investment."),
            ("Zillow", "Lead-routing marketplace and AI-assist signal."),
            ("Cloze", "Connected brokerage platform with AI assist."),
            ("Rechat", "Unified AI operating system for brokerage workflows."),
        ],
    },
    {
        "kicker": "USE CASE 02  · MULTIFAMILY",
        "title": "Leasing & Resident Communication Automation",
        "challenge": [
            "Leasing teams lose prospects to slow response and broken follow-up.",
            "Renewal and resident communication work is repetitive and fragmented.",
            "Property operators need visible ROI, not another sidecar AI tool.",
        ],
        "solution": [
            "Automate prospect response, routing, and renewal nudges.",
            "Support resident communication and document-heavy leasing steps.",
            "Embed workflows in PMS and CRM tools already used by operators.",
        ],
        "stats": [("26/35", "Reviewed lane score"), ("24/7", "Always-on leasing response expectation"), ("3", "Core proof vendors: AppFolio, Yardi, Docusign")],
        "how": [
            "Capture prospect or resident inquiry from the current channel.",
            "Classify intent and trigger the right follow-up or renewal workflow.",
            "Hand off only high-value or exception cases to the team.",
        ],
        "stack": [
            ("EXPERIENCE", "leasing inbox + resident messaging"),
            ("ORCHESTRATION", "OpenHands leasing and renewal agents"),
            ("CONTEXT", "PMS, CRM, applicant, and renewal data"),
            ("ACTUATION", "messages, reminders, packets, escalations"),
        ],
        "systems": "AppFolio · Yardi · leasing CRM · Docusign",
        "users": "leasing agent · community manager · regional ops",
        "orgs": [
            ("AppFolio", "Realm-X proves AI inside property workflows."),
            ("Yardi", "CRM and resident workflow visibility at scale."),
            ("Greystar", "Operator archetype for centralized leasing flows."),
            ("Regional owner-operator", "Buyer who needs renewal and response lift."),
        ],
    },
    {
        "kicker": "USE CASE 03  · BACK OFFICE",
        "title": "Commission & Deal Payout Automation",
        "challenge": [
            "Commission processing is rules-heavy and exception-prone.",
            "Payout timing and auditability matter to brokerages and agents.",
            "Transaction state and payout state often diverge across systems.",
        ],
        "solution": [
            "Validate splits, caps, fees, and payout rules automatically.",
            "Route exceptions to the right ops owner with audit context.",
            "Synchronize payout readiness with transaction and document state.",
        ],
        "stats": [("26/35", "Reviewed lane score"), ("1,500+", "Brokerages served by Brokermint"), ("400K+", "Annual transactions cited by Brokermint")],
        "how": [
            "Pull transaction and commission inputs from current systems.",
            "Evaluate rule sets and flag payout exceptions early.",
            "Send clean handoffs into accounting and approval workflows.",
        ],
        "stack": [
            ("EXPERIENCE", "ops review queue + payout dashboard"),
            ("ORCHESTRATION", "OpenHands payout and exception agents"),
            ("CONTEXT", "transaction, split, fee, and document data"),
            ("ACTUATION", "approvals, alerts, accounting handoffs"),
        ],
        "systems": "Brokermint · Docusign · brokerage finance systems",
        "users": "brokerage ops · finance lead · transaction admin",
        "orgs": [
            ("Brokermint", "Scaled proof that the category already exists."),
            ("Docusign", "Transaction state needs to inform payout state."),
            ("Mid-market brokerage", "Buyer who values payout speed and control."),
            ("Controller or ops lead", "Primary operational stakeholder."),
        ],
    },
    {
        "kicker": "USE CASE 04  · PROPERTY OPS",
        "title": "Service Request & Maintenance Automation",
        "challenge": [
            "Maintenance intake and triage are high-volume and time-sensitive.",
            "Residents expect visibility and updates, not silent queues.",
            "Vendor coordination and prioritization create operational drag.",
        ],
        "solution": [
            "Automate request intake, triage, routing, and resident updates.",
            "Escalate true exceptions while clearing routine queue work.",
            "Keep request state visible across resident, staff, and vendor flows.",
        ],
        "stats": [("26/35", "Reviewed lane score"), ("24/7", "Maintenance response expectation"), ("3", "Core proof vendors: AppFolio, Buildium, Yardi")],
        "how": [
            "Capture a request from resident, portal, phone, or staff input.",
            "Classify urgency, route work, and trigger updates automatically.",
            "Track completion, delays, and service quality in one queue.",
        ],
        "stack": [
            ("EXPERIENCE", "resident portal + ops queue"),
            ("ORCHESTRATION", "OpenHands intake and dispatch agents"),
            ("CONTEXT", "property, unit, history, vendor, SLA data"),
            ("ACTUATION", "routing, updates, escalations, reporting"),
        ],
        "systems": "AppFolio · Buildium · Yardi · vendor workflows",
        "users": "property ops · maintenance lead · vendor coordinator",
        "orgs": [
            ("AppFolio", "Maintenance AI proof inside property operations."),
            ("Buildium", "24/7 maintenance contact-center pattern."),
            ("Yardi", "Resident-facing request and tracking workflow."),
            ("Regional PM team", "Buyer with measurable service bottlenecks."),
        ],
    },
    {
        "kicker": "USE CASE 05  · CLOSING OPS",
        "title": "Title, Escrow & Closing Workflow Automation",
        "challenge": [
            "Closing files stall on missing items and fragmented coordination.",
            "Checklist progression and exception handling are manual and repetitive.",
            "Title and escrow teams depend on multi-party document state staying aligned.",
        ],
        "solution": [
            "Automate file-opening, checklist progression, and exception routing.",
            "Coordinate updates across title, escrow, lender, and partner workflows.",
            "Improve closing readiness without replacing the core transaction stack.",
        ],
        "stats": [("26/35", "Reviewed lane score"), ("3", "Core proof vendors: Qualia, SoftPro, Docusign"), ("1", "Best initial wedge: one queue or one closing team")],
        "how": [
            "Open and classify a new file from the incoming transaction packet.",
            "Route missing items, checklist tasks, and partner updates automatically.",
            "Surface closing-readiness status and exception backlog clearly.",
        ],
        "stack": [
            ("EXPERIENCE", "closing queue + readiness dashboard"),
            ("ORCHESTRATION", "OpenHands file and checklist agents"),
            ("CONTEXT", "file, checklist, partner, lender, signature data"),
            ("ACTUATION", "task routing, updates, escalations, audit trail"),
        ],
        "systems": "Qualia · SoftPro · Docusign · lender portals",
        "users": "title ops · escrow officer · closing manager",
        "orgs": [
            ("Qualia", "Connected title and escrow workflow proof."),
            ("SoftPro", "Closing and title software category incumbent."),
            ("Docusign", "Signature and document-state coordination layer."),
            ("Title ops team", "Buyer with backlog and closing-readiness pain."),
        ],
    },
]


def header_slide(d: Deck, title: str, subtitle: str):
    s = d.slide(fill=d.b.WHITE)
    d.rect(s, 0, 0, d.W, Inches(0.16), d.b.TEAL)
    d.text(s, title, d.M, Inches(0.42), d.CW, Inches(0.92), size=18.5, color=d.b.NAVY, bold=True, shrink=True)
    d.rect(s, d.M, Inches(1.18), Inches(1.45), Inches(0.05), d.b.TEAL)
    d.text(s, subtitle, d.M, Inches(1.36), d.CW, Inches(0.26), size=10.8, color=d.b.MUTED, shrink=True)
    return s


def footer(d: Deck, s, page: int, total: int, dark: bool = False):
    d.footer(s, page, total, dark=dark)


def use_case_slide(d: Deck, lane: dict, page: int, total: int):
    s = d.slide(fill=d.b.TEAL)
    panel_w = Inches(8.85)
    strip_x = panel_w
    strip_w = d.W - panel_w
    d.rect(s, strip_x, 0, strip_w, d.H, d.b.NAVY)
    d.rect(s, strip_x, 0, Inches(0.06), d.H, d.b.GOLD)
    d.text(s, lane["kicker"], d.M, Inches(0.28), panel_w - Inches(1.0), Inches(0.3), size=12, color=d.b.NAVY, bold=True)
    d.text(s, lane["title"], d.M, Inches(0.56), panel_w - Inches(1.0), Inches(0.68), size=20, color=d.b.WHITE, bold=True, shrink=True)

    card_y = Inches(1.25)
    card_h = Inches(1.64)
    gap = Inches(0.22)
    card_w = (panel_w - d.M * 2 - gap) / 2
    for idx, (title, items) in enumerate([("Challenge", lane["challenge"]), ("Solution", lane["solution"])]):
        x = d.M + idx * (card_w + gap)
        d.rect(s, x, card_y, card_w, card_h, d.b.WHITE, radius=0.06, shadow=True)
        d.text(s, title.upper(), x + Inches(0.18), card_y + Inches(0.15), card_w - Inches(0.36), Inches(0.22), size=12, color=d.b.ACCENT, bold=True)
        d.text(s, [{"text": item, "bullet": True, "size": 8.6, "color": d.b.INK, "space_before": 2} for item in items],
               x + Inches(0.18), card_y + Inches(0.42), card_w - Inches(0.32), Inches(1.05), shrink=True, ls=0.98)

    sy = Inches(2.98)
    stat_gap = Inches(0.18)
    stat_w = (panel_w - d.M * 2 - stat_gap * 2) / 3
    for i, (num, label) in enumerate(lane["stats"]):
        x = d.M + i * (stat_w + stat_gap)
        d.rect(s, x, sy, stat_w, Inches(0.86), d.b.GOLD, radius=0.05)
        d.text(s, num, x + Inches(0.12), sy + Inches(0.08), stat_w - Inches(0.24), Inches(0.28), size=18, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, label, x + Inches(0.12), sy + Inches(0.42), stat_w - Inches(0.24), Inches(0.22), size=8.7, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)

    how_y = Inches(4.0)
    d.text(s, "HOW IT WORKS", d.M, how_y, Inches(2.3), Inches(0.22), size=12, color=d.b.NAVY, bold=True)
    step_w = (panel_w - d.M * 2 - Inches(0.6)) / 3
    for i, step in enumerate(lane["how"]):
        x = d.M + i * (step_w + Inches(0.3))
        d.rect(s, x, how_y + Inches(0.28), step_w, Inches(0.92), d.b.WHITE, radius=0.05, shadow=True)
        d.text(s, f"{i+1:02d}", x + Inches(0.12), how_y + Inches(0.36), Inches(0.34), Inches(0.2), size=14, color=d.b.GOLD, bold=True)
        d.text(s, step, x + Inches(0.52), how_y + Inches(0.32), step_w - Inches(0.62), Inches(0.54), size=7.9, color=d.b.INK, shrink=True, ls=0.98)
        if i < 2:
            d.text(s, "→", x + step_w + Inches(0.05), how_y + Inches(0.54), Inches(0.24), Inches(0.24), size=14, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER)

    st_y = Inches(5.25)
    d.rect(s, d.M, st_y, panel_w - d.M * 2, Inches(0.95), d.b.NAVY, radius=0.05)
    d.text(s, "SOLUTION STACK", d.M + Inches(0.18), st_y + Inches(0.12), Inches(2), Inches(0.2), size=12, color=d.b.GOLD, bold=True)
    stack_w = (panel_w - d.M * 2 - Inches(0.72)) / 4
    for i, (layer, detail) in enumerate(lane["stack"]):
        x = d.M + Inches(0.18) + i * stack_w
        d.text(s, layer, x, st_y + Inches(0.34), stack_w - Inches(0.08), Inches(0.18), size=8.5, color=d.b.TEAL, bold=True, shrink=True)
        d.text(s, detail, x, st_y + Inches(0.52), stack_w - Inches(0.08), Inches(0.32), size=7.2, color=d.b.WHITE, shrink=True, ls=0.98)

    by = Inches(6.45)
    bw = (panel_w - d.M * 2 - Inches(0.2)) / 2
    d.rect(s, d.M, by, bw, Inches(0.36), d.b.ACCENT, radius=0.04)
    d.text(s, f"SYSTEMS: {lane['systems']}", d.M + Inches(0.15), by, bw - Inches(0.3), Inches(0.36), size=7.1, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.rect(s, d.M + bw + Inches(0.2), by, bw, Inches(0.36), d.b.DARK_TEAL, radius=0.04)
    d.text(s, f"USERS: {lane['users']}", d.M + bw + Inches(0.35), by, bw - Inches(0.3), Inches(0.36), size=7.1, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)

    sx = strip_x + Inches(0.3)
    d.text(s, "ORGANIZATIONS", sx, Inches(0.45), strip_w - Inches(0.5), Inches(0.24), size=13, color=d.b.TEAL, bold=True)
    d.text(s, "DELIVERING / BUYING THIS", sx, Inches(0.72), strip_w - Inches(0.5), Inches(0.24), size=13, color=d.b.TEAL, bold=True)
    d.rect(s, sx, Inches(1.08), Inches(1.0), Inches(0.04), d.b.GOLD)
    oy = Inches(1.28)
    for name, desc in lane["orgs"]:
        d.text(s, name, sx, oy, strip_w - Inches(0.5), Inches(0.24), size=12.0, color=d.b.WHITE, bold=True, shrink=True)
        d.text(s, desc, sx, oy + Inches(0.26), strip_w - Inches(0.55), Inches(0.56), size=8.5, color=d.b.LIGHT_TEAL, shrink=True, ls=0.98)
        oy += Inches(0.98)
    footer(d, s, page, total, dark=True)


def executive_summary(d: Deck, total: int):
    s = header_slide(
        d,
        "The real-estate domain supports a five-lane AI engineering portfolio with clear buyers and measurable workflow pain",
        "This chain started with gbrain semantic recall, then used the latest feed plus five validated lane runs already completed on June 4, 2026",
    )
    y = Inches(1.75)
    col_w = Inches(3.92)
    gap = Inches(0.22)
    xs = [d.M, d.M + col_w + gap, d.M + 2 * (col_w + gap)]
    titles = ["Where to start", "What repeats", "What to do"]
    bodies = [
        [
            "Brokerage routing is the cleanest commercial wedge.",
            "Leasing, maintenance, commissions, and closing extend the same thesis across adjacent buyers.",
            "Each lane is already validated with structured research and a reviewed deck.",
        ],
        [
            "Incumbent software is the system of record across every lane.",
            "OpenHands is the reusable orchestration layer for workflow agents and MCP-connected tools.",
            "The value story is operational throughput, not generic assistant novelty.",
        ],
        [
            "Select the first wedge by buyer pain and existing account motion.",
            "Start with one queue, one team, or one office before broadening support.",
            "Use this deck as the portfolio index and the lane decks for account follow-up.",
        ],
    ]
    colors = [d.b.SOFT, d.b.SOFT, d.b.NAVY]
    for idx, x in enumerate(xs):
        d.rect(s, x, y, col_w, Inches(3.45), colors[idx], radius=0.05, shadow=True)
        d.text(s, titles[idx], x + Inches(0.22), y + Inches(0.18), col_w - Inches(0.4), Inches(0.25), size=16, color=d.b.TEAL if idx == 2 else d.b.NAVY, bold=True)
        d.text(s, [{"text": item, "bullet": True, "size": 11.6, "color": d.b.LIGHT_TEAL if idx == 2 else d.b.INK, "space_before": 7} for item in bodies[idx]],
               x + Inches(0.22), y + Inches(0.55), col_w - Inches(0.4), Inches(2.6), shrink=True)
    d.rect(s, d.M, Inches(5.55), d.CW, Inches(0.62), d.b.GOLD, radius=0.05)
    d.text(s, "THE ASK: choose the first wedge, then use the matching reviewed lane deck for direct client pursuit.",
           d.M + Inches(0.25), Inches(5.68), d.CW - Inches(0.5), Inches(0.28), size=10.2, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 2, total)


def implementation_slide(d: Deck, total: int):
    s = header_slide(
        d,
        "The portfolio is portable because the implementation posture stays consistent across all five lanes",
        "Structured implementation slide grounded in gbrain recall, prior lane research, and the repo's OpenHands contract",
    )
    left_w = Inches(5.85)
    right_x = d.M + left_w + Inches(0.35)
    d.rect(s, d.M, Inches(1.75), left_w, Inches(4.45), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "COMMON EXECUTION PATTERN", d.M + Inches(0.22), Inches(1.95), left_w - Inches(0.44), Inches(0.24), size=15, color=d.b.TEAL, bold=True)
    points = [
        "Use incumbent brokerage, PMS, title, and finance software as the system of record.",
        "Use OpenHands internally for routing agents, checklist agents, exception agents, and reusable skills.",
        "Connect tools through MCP-friendly APIs and workflow surfaces rather than replacing the user workspace.",
        "Start assistive: scoring, routing, drafts, queue updates, and exception handling before autonomous commitments.",
        "Measure one operational outcome per lane before expansion.",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.2, "color": d.b.WHITE, "space_before": 8} for item in points],
           d.M + Inches(0.22), Inches(2.28), left_w - Inches(0.44), Inches(3.35), shrink=True)
    cards = [
        ("Shared systems", "CRM, PMS, transaction platforms, Docusign, accounting systems, portals, and vendor or lender tools."),
        ("Selection rule", "Pick the first wedge where the buyer already owns the pain and the operational queue is visible enough to measure."),
    ]
    cy = Inches(1.75)
    for title, body in cards:
        d.rect(s, right_x, cy, Inches(5.95), Inches(2.05), d.b.SOFT, radius=0.05, shadow=True)
        d.text(s, title, right_x + Inches(0.2), cy + Inches(0.16), Inches(5.55), Inches(0.28), size=14.0, color=d.b.NAVY, bold=True, shrink=True)
        d.text(s, body, right_x + Inches(0.2), cy + Inches(0.5), Inches(5.55), Inches(1.05), size=10.5, color=d.b.INK, shrink=True)
        cy += Inches(2.2)
    footer(d, s, 8, total)


def closing(d: Deck, total: int):
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.16), d.b.TEAL)
    d.text(s, "BOTTOM LINE", d.M, Inches(1.15), Inches(3), Inches(0.25), size=16, color=d.b.TEAL, bold=True)
    d.text(s, "Real-estate AI is strongest as a portfolio of workflow wedges, each tied to a buyer, a queue, and a system-of-record that already exists.", d.M, Inches(1.6), Inches(11.6), Inches(1.25), size=22, color=d.b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(3.05), Inches(11.9), Inches(0.06), d.b.GOLD)
    final_points = [
        "Start with the wedge that matches the current account motion: brokerage, leasing, back office, service, or closing.",
        "Use OpenHands as the internal execution layer and keep the user workflow inside the existing real-estate stack.",
        "After the first wedge proves ROI, expand horizontally into the other reviewed lanes.",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 14.8, "color": d.b.LIGHT_TEAL, "space_before": 10} for item in final_points],
           d.M, Inches(3.38), Inches(10.9), Inches(1.95), shrink=True)
    d.rect(s, d.M, Inches(5.82), Inches(6.5), Inches(0.84), d.b.GOLD, radius=0.05)
    d.text(s, "Suggested next step: select the first wedge and pair this portfolio deck with the corresponding reviewed lane deck for the target account.",
           d.M + Inches(0.3), Inches(6.03), Inches(11.3), Inches(0.44), size=10.0, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 9, total, dark=True)


def main():
    total = 9
    d = Deck(footer="Real Estate Domain AI Use Cases | Client Package | June 2026")
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, d.W - Inches(3.0), 0, Inches(3.0), d.H, d.b.NAVY_2)
    d.rect(s, d.W - Inches(3.0), 0, Inches(0.06), d.H, d.b.TEAL)
    d.text(s, "CLIENT PACKAGE", d.M, Inches(0.95), Inches(3), Inches(0.25), size=15, color=d.b.TEAL, bold=True)
    d.text(s, "Real Estate Domain\nAI Use Cases", d.M, Inches(1.45), Inches(7.8), Inches(1.25), size=32, color=d.b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.75), Inches(1.6), Inches(0.06), d.b.TEAL)
    d.text(s, "A branded multi-use-case portfolio deck built from gbrain semantic recall, the latest strategy feed, and five validated real-estate lane runs already completed in this repo.",
           d.M, Inches(3.05), Inches(7.9), Inches(1.2), size=15.2, color=d.b.WHITE, shrink=True)
    d.text(s, "DETAILED USE CASES · DOMAIN THESIS · IMPLEMENTATION PATTERN · BUYER SELECTION",
           d.M, Inches(5.75), Inches(9.0), Inches(0.28), size=11, color=d.b.GOLD, bold=True)
    footer(d, s, 1, total, dark=True)
    executive_summary(d, total)
    for page, lane in enumerate(LANES, start=3):
        use_case_slide(d, lane, page, total)
    implementation_slide(d, total)
    closing(d, total)
    d.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
