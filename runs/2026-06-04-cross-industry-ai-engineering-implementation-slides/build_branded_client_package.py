#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

BRANDED_SKILL = Path("/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(BRANDED_SKILL))

from pptxkit import Deck, Inches, PP_ALIGN, MSO_ANCHOR  # type: ignore

RUN_DIR = Path(__file__).resolve().parent
OUT = RUN_DIR / "cross-industry-ai-engineering-implementation-slides-client-package-branded-draft.pptx"
SELECTED = json.loads((RUN_DIR / "selected-use-cases.json").read_text(encoding="utf-8"))

LANES = [
    {
        "kicker": "INDUSTRY 01  · MANUFACTURING",
        "title": "Predictive Maintenance AI Agent",
        "challenge": [
            "Reactive maintenance drives visible downtime and expensive interventions.",
            "Plants need condition-based alerts tied to planner workflows, not another standalone model demo.",
            "Operational trust depends on explainability and SAP work-order follow-through.",
        ],
        "solution": [
            "Fuse sensor data, anomaly detection, and RUL estimation in one orchestrated flow.",
            "Trigger planner-ready SAP PM work orders through MCP-connected systems.",
            "Start with one asset family before wider rollout.",
        ],
        "stats": [("$5K-10K", "Revenue band"), ("52", "PdM MCP tools"), ("40%+", "Speedup signal")],
        "how": [
            "Sensor data enters via MQTT or OPC-UA and is normalized for analysis.",
            "OpenHands agents call PdM and SAP-connected MCP tools to detect, explain, and route issues.",
            "Critical findings become planner-ready work orders and operator summaries.",
        ],
        "stack": [
            ("EXPERIENCE", "planner console + maintenance summary"),
            ("ORCHESTRATION", "OpenHands conversation and agent stack"),
            ("CONTEXT", "sensor streams, asset history, failure patterns"),
            ("ACTUATION", "SAP PM work orders, alerts, reports"),
        ],
        "systems": "MQTT · OPC-UA · PdM MCP · SAP PM · historian",
        "users": "maintenance planner · reliability lead · plant ops",
        "orgs": [
            ("PDF framework", "Identifies predictive maintenance as the highest-value manufacturing lane."),
            ("OpenHands", "Supplies the reusable agent, plugin, and MCP orchestration primitives."),
            ("SAP PM", "Acts as the action system for work orders and maintenance execution."),
            ("Plant team", "Starts with one critical asset family and one workflow owner."),
        ],
    },
    {
        "kicker": "INDUSTRY 02  · LAW FIRMS",
        "title": "Contract Generation & Review Agent",
        "challenge": [
            "Drafting and review consume high-value lawyer time on repeatable contract patterns.",
            "Jurisdiction rules, approvals, and signature flow create fragmented tool usage.",
            "Risk review needs traceable findings, not opaque one-shot AI output.",
        ],
        "solution": [
            "Orchestrate template fill, clause review, and research across MCP services.",
            "Use specialized generation, review, and research agents.",
            "Keep outputs in DOCX and memo formats with review gates.",
        ],
        "stats": [("$3K-5K", "Revenue band"), ("40+", "Template count"), ("67", "Review agents")],
        "how": [
            "Client intake identifies agreement type and required fields.",
            "Generation, review, and legal research agents call MCP-connected tools in sequence.",
            "Approved output moves into DocuSign and matter-management workflows.",
        ],
        "stack": [
            ("EXPERIENCE", "matter intake + review workspace"),
            ("ORCHESTRATION", "OpenHands skill and agent chain"),
            ("CONTEXT", "templates, clauses, jurisdiction rules, matter data"),
            ("ACTUATION", "DOCX output, redlines, signature routing"),
        ],
        "systems": "Open Agreements · DocuSign · legal research MCP · Clio",
        "users": "associate · partner · legal ops · billing lead",
        "orgs": [
            ("PDF framework", "Positions contract generation and review as the clearest legal wedge."),
            ("OpenHands", "Packages multi-agent review and reusable skills cleanly."),
            ("Template systems", "Provide repeatable starting points instead of blank-document generation."),
            ("Firm stakeholders", "Need auditable review outputs and approval controls."),
        ],
    },
    {
        "kicker": "INDUSTRY 03  · HEALTHCARE",
        "title": "Patient Intake + Insurance Verification",
        "challenge": [
            "Front-desk teams still rekey intake data and chase payer eligibility manually.",
            "Patient experience drops when verification and reminders break across systems.",
            "HIPAA makes deployment discipline non-negotiable.",
        ],
        "solution": [
            "Automate intake validation, EHR writeback, eligibility checks, and reminders.",
            "Keep PHI inside the customer-controlled workflow boundary.",
            "Escalate failed verification and consent exceptions.",
        ],
        "stats": [("$3K-5K", "Revenue band"), ("FHIR R4", "Primary system standard"), ("24h", "Reminder workflow anchor")],
        "how": [
            "Patient intake data is validated and written into a FHIR-compatible record.",
            "Eligibility and scheduling calls run through MCP-connected services with exception routing.",
            "Confirmed appointments trigger reminders and post-visit claim workflow preparation.",
        ],
        "stack": [
            ("EXPERIENCE", "patient intake + staff exception queue"),
            ("ORCHESTRATION", "OpenHands workflow and policy skills"),
            ("CONTEXT", "patient profile, payer data, consent state"),
            ("ACTUATION", "EHR updates, SMS, bookings, claims"),
        ],
        "systems": "FHIR APIs · payer eligibility · Twilio · scheduling",
        "users": "front desk · practice manager · billing staff",
        "orgs": [
            ("PDF framework", "Frames intake and eligibility as the first healthcare automation wedge."),
            ("OpenHands", "Supports policy-aware orchestration and repeatable workflow packaging."),
            ("FHIR stack", "Keeps the EHR interaction on standards-based interfaces."),
            ("Practice teams", "Need exception handling more than full end-to-end autonomy."),
        ],
    },
    {
        "kicker": "INDUSTRY 04  · MARKETING",
        "title": "Automated Reporting Dashboard + SEO Agent",
        "challenge": [
            "Analysts manually consolidate GA4, Search Console, ads, and CMS outputs every reporting cycle.",
            "SEO recommendations often stall between audit, content, and publishing teams.",
            "Agencies need repeatable client delivery, not bespoke weekly analysis.",
        ],
        "solution": [
            "Run reporting and SEO workflows through headless execution and MCP-connected APIs.",
            "Combine data collection, narrative generation, and publication support in one repeatable run.",
            "Use the lane as a low-friction proof of the delivery model.",
        ],
        "stats": [("$2K-4K", "Revenue band"), ("4", "Core systems"), ("Headless", "Execution fit")],
        "how": [
            "Campaign and SEO data is pulled from analytics, search, ads, and CMS systems.",
            "OpenHands assembles the reporting narrative and SEO recommendations through scheduled runs.",
            "Output is published as a branded report and routed to client or content workflows.",
        ],
        "stack": [
            ("EXPERIENCE", "client report + SEO work queue"),
            ("ORCHESTRATION", "OpenHands headless reporting agents"),
            ("CONTEXT", "GA4, GSC, Meta, CMS, content history"),
            ("ACTUATION", "reports, recommendations, drafts, updates"),
        ],
        "systems": "GA4 · Search Console · Meta Ads · WordPress",
        "users": "account manager · analyst · SEO lead · content team",
        "orgs": [
            ("PDF framework", "Shows the most lightweight services implementation path."),
            ("OpenHands", "Adds scheduled execution and reusable workflow packaging."),
            ("Agency operators", "Value consistency, speed, and white-label delivery."),
            ("Client teams", "See faster reporting and clearer action follow-through."),
        ],
    },
]


def header_slide(d: Deck, title: str, subtitle: str):
    s = d.slide(fill=d.b.WHITE)
    d.rect(s, 0, 0, d.W, Inches(0.16), d.b.TEAL)
    d.text(s, title, d.M, Inches(0.42), d.CW, Inches(0.86), size=19, color=d.b.NAVY, bold=True, shrink=True)
    d.rect(s, d.M, Inches(1.18), Inches(1.45), Inches(0.05), d.b.TEAL)
    d.text(s, subtitle, d.M, Inches(1.36), d.CW, Inches(0.26), size=10.8, color=d.b.MUTED, shrink=True)
    return s


def footer(d: Deck, s, page: int, total: int, dark: bool = False):
    d.footer(s, page, total, dark=dark)


def hero(d: Deck, total: int):
    s = header_slide(
        d,
        "One implementation-ready AI engineering use case per industry",
        "Built from the source framework PDF, prior GBrain-derived artifacts, and current OpenHands primary documentation",
    )
    d.rect(s, d.M, Inches(1.78), Inches(4.0), Inches(3.9), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "SELECTED LANES", d.M + Inches(0.22), Inches(1.98), Inches(2.5), Inches(0.24), size=15, color=d.b.TEAL, bold=True)
    picks = [
        "Manufacturing: predictive maintenance",
        "Law firms: contract generation and review",
        "Healthcare: patient intake and eligibility verification",
        "Marketing agencies: reporting dashboard and SEO automation",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 12, "color": d.b.WHITE, "space_before": 8} for item in picks],
           d.M + Inches(0.22), Inches(2.3), Inches(3.5), Inches(2.7), shrink=True)
    d.rect(s, Inches(5.0), Inches(1.78), Inches(7.7), Inches(3.9), d.b.SOFT, radius=0.05, shadow=True)
    d.text(s, "WHY THIS DECK EXISTS", Inches(5.22), Inches(1.98), Inches(3.4), Inches(0.24), size=15, color=d.b.NAVY, bold=True)
    rationale = [
        "The PDF is strongest when translated into concrete implementation slides, not left as a broad industry scan.",
        "Each lane already has a workflow trigger, an action system, and an MCP-friendly integration posture.",
        "OpenHands supplies the reusable orchestration model across all four industries.",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.4, "color": d.b.INK, "space_before": 8} for item in rationale],
           Inches(5.22), Inches(2.32), Inches(7.2), Inches(2.6), shrink=True)
    d.rect(s, d.M, Inches(6.0), d.CW, Inches(0.62), d.b.GOLD, radius=0.05)
    d.text(s, "Skill chain: GBrain Recall -> content-research -> industry-research-analysis-branded-deck",
           d.M + Inches(0.25), Inches(6.13), d.CW - Inches(0.5), Inches(0.26), size=10.8, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 1, total)


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
        d.text(s, [{"text": item, "bullet": True, "size": 8.4, "color": d.b.INK, "space_before": 2} for item in items],
               x + Inches(0.18), card_y + Inches(0.42), card_w - Inches(0.32), Inches(1.05), shrink=True, ls=0.98)

    sy = Inches(2.98)
    stat_gap = Inches(0.18)
    stat_w = (panel_w - d.M * 2 - stat_gap * 2) / 3
    for i, (num, label) in enumerate(lane["stats"]):
        x = d.M + i * (stat_w + stat_gap)
        d.rect(s, x, sy, stat_w, Inches(0.86), d.b.GOLD, radius=0.05)
        d.text(s, num, x + Inches(0.12), sy + Inches(0.08), stat_w - Inches(0.24), Inches(0.28), size=18, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, label, x + Inches(0.12), sy + Inches(0.42), stat_w - Inches(0.24), Inches(0.22), size=8.6, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)

    how_y = Inches(4.0)
    d.text(s, "HOW IT WORKS", d.M, how_y, Inches(2.3), Inches(0.22), size=12, color=d.b.NAVY, bold=True)
    step_w = (panel_w - d.M * 2 - Inches(0.6)) / 3
    for i, step in enumerate(lane["how"]):
        x = d.M + i * (step_w + Inches(0.3))
        d.rect(s, x, how_y + Inches(0.28), step_w, Inches(0.92), d.b.WHITE, radius=0.05, shadow=True)
        d.text(s, f"{i+1:02d}", x + Inches(0.12), how_y + Inches(0.36), Inches(0.34), Inches(0.2), size=14, color=d.b.GOLD, bold=True)
        d.text(s, step, x + Inches(0.52), how_y + Inches(0.32), step_w - Inches(0.62), Inches(0.54), size=7.8, color=d.b.INK, shrink=True, ls=0.98)
        if i < 2:
            d.text(s, "→", x + step_w + Inches(0.05), how_y + Inches(0.54), Inches(0.24), Inches(0.24), size=14, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER)

    st_y = Inches(5.25)
    d.rect(s, d.M, st_y, panel_w - d.M * 2, Inches(0.95), d.b.NAVY, radius=0.05)
    d.text(s, "SOLUTION STACK", d.M + Inches(0.18), st_y + Inches(0.12), Inches(2), Inches(0.2), size=12, color=d.b.GOLD, bold=True)
    stack_w = (panel_w - d.M * 2 - Inches(0.72)) / 4
    for i, (layer, detail) in enumerate(lane["stack"]):
        x = d.M + Inches(0.18) + i * stack_w
        d.text(s, layer, x, st_y + Inches(0.34), stack_w - Inches(0.08), Inches(0.18), size=8.4, color=d.b.TEAL, bold=True, shrink=True)
        d.text(s, detail, x, st_y + Inches(0.52), stack_w - Inches(0.08), Inches(0.32), size=7.1, color=d.b.WHITE, shrink=True, ls=0.98)

    by = Inches(6.45)
    bw = (panel_w - d.M * 2 - Inches(0.2)) / 2
    d.rect(s, d.M, by, bw, Inches(0.36), d.b.ACCENT, radius=0.04)
    d.text(s, f"SYSTEMS: {lane['systems']}", d.M + Inches(0.15), by, bw - Inches(0.3), Inches(0.36), size=7.0, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.rect(s, d.M + bw + Inches(0.2), by, bw, Inches(0.36), d.b.DARK_TEAL, radius=0.04)
    d.text(s, f"USERS: {lane['users']}", d.M + bw + Inches(0.35), by, bw - Inches(0.3), Inches(0.36), size=7.0, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)

    sx = strip_x + Inches(0.3)
    d.text(s, "IMPLEMENTATION NOTES", sx, Inches(0.45), strip_w - Inches(0.5), Inches(0.24), size=13, color=d.b.TEAL, bold=True)
    oy = Inches(1.05)
    for name, desc in lane["orgs"]:
        d.text(s, name, sx, oy, strip_w - Inches(0.5), Inches(0.24), size=12.4, color=d.b.WHITE, bold=True, shrink=True)
        d.text(s, desc, sx, oy + Inches(0.22), strip_w - Inches(0.55), Inches(0.56), size=8.8, color=d.b.LIGHT_TEAL, shrink=True, ls=0.98)
        oy += Inches(0.9)
    footer(d, s, page, total, dark=True)


def architecture_slide(d: Deck, total: int):
    s = header_slide(
        d,
        "The shared architecture is OpenHands-first, MCP-connected, and system-of-record aware",
        "Implementation pattern verified against current OpenHands docs and applied consistently across all four use cases",
    )
    d.rect(s, d.M, Inches(1.75), Inches(5.7), Inches(4.5), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "OPENHANDS IMPLEMENTATION PRIMITIVES", d.M + Inches(0.22), Inches(1.95), Inches(5.1), Inches(0.24), size=15, color=d.b.TEAL, bold=True)
    left_points = [
        "Plugins package skills, hooks, MCP servers, agents, and commands as one reusable vertical bundle.",
        "Agent integrations use `mcp_config`, and MCP tools are discovered automatically during initialization.",
        "Conversation manages lifecycle, state orchestration, workspace coordination, and runtime services.",
        "CLI MCP flow is straightforward: add servers, start OpenHands, inspect `/mcp`, then use enabled tools.",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 11.2, "color": d.b.WHITE, "space_before": 8} for item in left_points],
           d.M + Inches(0.22), Inches(2.28), Inches(5.2), Inches(3.4), shrink=True)

    right_x = Inches(6.1)
    d.rect(s, right_x, Inches(1.75), Inches(6.6), Inches(2.25), d.b.SOFT, radius=0.05, shadow=True)
    d.text(s, "CROSS-INDUSTRY PACKAGING", right_x + Inches(0.2), Inches(1.95), Inches(6.1), Inches(0.24), size=15, color=d.b.NAVY, bold=True)
    packaging = [
        "One plugin per industry lane",
        "Domain skill set per workflow family",
        "MCP connectors for the action systems already in use",
        "Headless runs for scheduled delivery",
        "Human gates where compliance requires them",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 10.6, "color": d.b.INK, "space_before": 6} for item in packaging],
           right_x + Inches(0.2), Inches(2.28), Inches(6.1), Inches(1.45), shrink=True)

    d.rect(s, right_x, Inches(4.15), Inches(6.6), Inches(2.1), d.b.GOLD, radius=0.05)
    d.text(s, "RECOMMENDED BUILD ORDER", right_x + Inches(0.2), Inches(4.32), Inches(3.2), Inches(0.24), size=15, color=d.b.NAVY, bold=True)
    build_order = [
        "1. Manufacturing for strategic depth and enterprise wedge",
        "2. Law for strong open-source readiness",
        "3. Healthcare for guarded workflow automation",
        "4. Marketing for the fastest repeatable services proof",
    ]
    d.text(s, [{"text": item, "bullet": True, "size": 10.4, "color": d.b.NAVY, "space_before": 6} for item in build_order],
           right_x + Inches(0.2), Inches(4.62), Inches(6.1), Inches(1.25), shrink=True)
    footer(d, s, total, total)


def build():
    total = 6
    d = Deck()
    hero(d, total)
    for idx, lane in enumerate(LANES, start=2):
        use_case_slide(d, lane, idx, total)
    architecture_slide(d, total)
    d.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
