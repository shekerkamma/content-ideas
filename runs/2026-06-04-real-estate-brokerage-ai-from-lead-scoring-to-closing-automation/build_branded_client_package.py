#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

BRANDED_SKILL = Path("/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(BRANDED_SKILL))

from pptxkit import Deck, Inches, PP_ALIGN, MSO_ANCHOR  # type: ignore

RUN_DIR = Path(__file__).resolve().parent
DRAFT_OUT = RUN_DIR / "real-estate-brokerage-ai-from-lead-scoring-to-closing-automation-client-package-branded-draft.pptx"
REVIEWED_OUT = RUN_DIR / "real-estate-brokerage-ai-from-lead-scoring-to-closing-automation-client-package-branded-reviewed.pptx"

MANIFEST = json.loads((RUN_DIR / "selected-use-case.json").read_text(encoding="utf-8"))
FEED = json.loads(Path(MANIFEST["feed_path"]).read_text(encoding="utf-8"))
UC = next(item for item in FEED["useCases"] if item["id"] == MANIFEST["use_case_id"])
CONDENSED_CHALLENGE = [
    "Too much agent time is wasted on weak leads and manual prioritization.",
    "Transaction work is spread across CRM, docs, title, and lender tools.",
    "Pricing analysis is still slow and manual for many listings.",
]
CONDENSED_SOLUTION = [
    "Score and route leads based on behavior and CRM context.",
    "Automate transaction coordination, deadlines, and document handoffs.",
    "Generate CMA output faster with live comps and pricing logic.",
]
CONDENSED_HOW = [
    "Lead enters CRM, gets scored, and is routed or nurtured.",
    "Accepted deal triggers transaction coordination across systems.",
    "Agent requests CMA and receives a client-ready pricing pack.",
]
CONDENSED_ORGS = [
    ("Rechat", "AI-native real-estate operating system."),
    ("Breezy", "Workflow-heavy brokerage automation platform."),
    ("Compass", "Large brokerage investing in agent productivity AI."),
    ("Bedrock Robotics", "Signal that property-intelligence funding is strong."),
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


def bullets(items, size=11.4, color=None, space_before=8):
    use_color = color
    return [
        {"text": item, "bullet": True, "size": size, "color": use_color, "space_before": space_before}
        for item in items
    ]


def executive_summary(d: Deck, total: int):
    s = header_slide(
        d,
        "Brokerage AI is strongest when it improves conversion inside the tools agents already trust",
        "Stage 1 skill-chain test: pipeline-runner content research plus visible GBrain chaining on the June 4, 2026 real-estate feed",
    )
    y = Inches(1.75)
    col_w = Inches(3.92)
    gap = Inches(0.22)
    xs = [d.M, d.M + col_w + gap, d.M + 2 * (col_w + gap)]
    titles = ["What changed", "What matters", "What to do"]
    bodies = [
        [
            "Brokerage AI is moving into CRM, routing, transaction, and CMA workflows.",
            "The feed points to lead scoring, transaction coordination, and pricing intelligence."
        ],
        [
            "The strongest wedge is speed-to-lead plus workflow automation.",
            "The buyer wants conversion lift and less transaction drag, not another AI front-end."
        ],
        [
            "Start with one brokerage workflow: lead scoring and handoff.",
            "Keep OpenHands and workflow orchestration behind the scenes, not as the customer-facing pitch."
        ],
    ]
    colors = [d.b.SOFT, d.b.SOFT, d.b.NAVY]
    title_colors = [d.b.NAVY, d.b.NAVY, d.b.TEAL]
    body_colors = [d.b.INK, d.b.INK, d.b.LIGHT_TEAL]
    for idx, x in enumerate(xs):
        d.rect(s, x, y, col_w, Inches(3.1), colors[idx], radius=0.05, shadow=True)
        d.text(s, titles[idx], x + Inches(0.22), y + Inches(0.18), col_w - Inches(0.4), Inches(0.25),
               size=16, color=title_colors[idx], bold=True)
        d.text(s, bullets(bodies[idx], size=9.4, color=body_colors[idx]), x + Inches(0.22), y + Inches(0.55), col_w - Inches(0.4), Inches(2.1), shrink=True)
    d.rect(s, d.M, Inches(5.55), d.CW, Inches(0.62), d.b.GOLD, radius=0.05)
    d.text(
        s,
        "THE ASK: approve a brokerage pilot around lead scoring and transaction coordination in the current CRM stack.",
        d.M + Inches(0.25), Inches(5.68), d.CW - Inches(0.5), Inches(0.28),
        size=9.8, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True
    )
    footer(d, s, 2, total)


def use_case_realization(d: Deck, total: int):
    s = d.slide(fill=d.b.TEAL)
    panel_w = Inches(8.85)
    strip_x = panel_w
    strip_w = d.W - panel_w
    d.rect(s, strip_x, 0, strip_w, d.H, d.b.NAVY)
    d.rect(s, strip_x, 0, Inches(0.06), d.H, d.b.GOLD)
    d.text(s, UC["kicker"], d.M, Inches(0.28), panel_w - Inches(1.0), Inches(0.3), size=12, color=d.b.NAVY, bold=True)
    d.text(s, "Brokerage AI: Lead Scoring to Close", d.M, Inches(0.56), panel_w - Inches(1.0), Inches(0.68), size=20, color=d.b.WHITE, bold=True, shrink=True)

    card_y = Inches(1.25)
    card_h = Inches(1.7)
    gap = Inches(0.22)
    card_w = (panel_w - d.M * 2 - gap) / 2
    for idx, (title, items) in enumerate([("Challenge", CONDENSED_CHALLENGE), ("Solution", CONDENSED_SOLUTION)]):
        x = d.M + idx * (card_w + gap)
        d.rect(s, x, card_y, card_w, card_h - Inches(0.08), d.b.WHITE, radius=0.06, shadow=True)
        d.text(s, title.upper(), x + Inches(0.18), card_y + Inches(0.15), card_w - Inches(0.36), Inches(0.22), size=12, color=d.b.ACCENT, bold=True)
        d.text(s, bullets(items, size=8.0, color=d.b.INK, space_before=2),
               x + Inches(0.18), card_y + Inches(0.42), card_w - Inches(0.32), Inches(0.92), shrink=True, ls=0.98)

    sy = Inches(3.05)
    stat_gap = Inches(0.18)
    stats = [
        ("$404.9B", "AI real-estate market size in 2026"),
        ("25-40%", "lead-to-close lift with AI scoring"),
        ("97%", "agent AI-tool adoption signal"),
    ]
    stat_w = (panel_w - d.M * 2 - stat_gap * 2) / 3
    for i, (num, label) in enumerate(stats):
        x = d.M + i * (stat_w + stat_gap)
        d.rect(s, x, sy, stat_w, Inches(0.92), d.b.GOLD, radius=0.05)
        d.text(s, num, x + Inches(0.12), sy + Inches(0.08), stat_w - Inches(0.24), Inches(0.28), size=18, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, label, x + Inches(0.12), sy + Inches(0.42), stat_w - Inches(0.24), Inches(0.26), size=8.8, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)

    how_y = Inches(4.12)
    d.text(s, "HOW IT WORKS", d.M, how_y, Inches(2.3), Inches(0.22), size=12, color=d.b.NAVY, bold=True)
    step_w = (panel_w - d.M * 2 - Inches(0.6)) / 3
    for i, step in enumerate(CONDENSED_HOW):
        x = d.M + i * (step_w + Inches(0.3))
        d.rect(s, x, how_y + Inches(0.28), step_w, Inches(0.96), d.b.WHITE, radius=0.05, shadow=True)
        d.text(s, f"{i+1:02d}", x + Inches(0.12), how_y + Inches(0.36), Inches(0.34), Inches(0.2), size=14, color=d.b.GOLD, bold=True)
        d.text(s, step, x + Inches(0.52), how_y + Inches(0.32), step_w - Inches(0.62), Inches(0.58), size=7.2, color=d.b.INK, shrink=True, ls=0.98)
        if i < 2:
            d.text(s, "→", x + step_w + Inches(0.05), how_y + Inches(0.54), Inches(0.24), Inches(0.24), size=14, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER)

    st_y = Inches(5.42)
    d.rect(s, d.M, st_y, panel_w - d.M * 2, Inches(0.98), d.b.NAVY, radius=0.05)
    d.text(s, "SOLUTION STACK", d.M + Inches(0.18), st_y + Inches(0.12), Inches(2), Inches(0.2), size=12, color=d.b.GOLD, bold=True)
    stack_w = (panel_w - d.M * 2 - Inches(0.72)) / 4
    for i, (layer, detail) in enumerate(UC["stack"][:4]):
        x = d.M + Inches(0.18) + i * stack_w
        d.text(s, layer, x, st_y + Inches(0.34), stack_w - Inches(0.08), Inches(0.18), size=8.8, color=d.b.TEAL, bold=True, shrink=True)
        short_detail = {
            "EXPERIENCE": "Dashboard · portal · CMA reports",
            "ORCHESTRATION": "Lead, transaction, and CMA agents",
            "CONTEXT": "MLS/IDX · CRM · public records · doc status",
            "ACTUATION": "CRM write-back · docs · nurture · scheduling",
        }.get(layer, detail)
        d.text(s, short_detail, x, st_y + Inches(0.52), stack_w - Inches(0.08), Inches(0.24), size=6.2, color=d.b.WHITE, shrink=True, ls=0.98)

    by = Inches(6.48)
    bw = (panel_w - d.M * 2 - Inches(0.2)) / 2
    systems = "SYSTEMS: MLS/IDX · CRM · DocuSign · Title/Escrow · Lender"
    d.rect(s, d.M, by, bw, Inches(0.36), d.b.ACCENT, radius=0.04)
    d.text(s, systems, d.M + Inches(0.15), by, bw - Inches(0.3), Inches(0.36), size=6.2, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.rect(s, d.M + bw + Inches(0.2), by, bw, Inches(0.36), d.b.DARK_TEAL, radius=0.04)
    d.text(s, "USERS: owner · lead · agent · coordinator", d.M + bw + Inches(0.35), by, bw - Inches(0.3), Inches(0.36), size=6.2, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)

    sx = strip_x + Inches(0.3)
    d.text(s, "ORGANIZATIONS", sx, Inches(0.45), strip_w - Inches(0.5), Inches(0.24), size=13, color=d.b.TEAL, bold=True)
    d.text(s, "IN THE CURRENT LANE", sx, Inches(0.72), strip_w - Inches(0.5), Inches(0.24), size=13, color=d.b.TEAL, bold=True)
    d.rect(s, sx, Inches(1.08), Inches(1.0), Inches(0.04), d.b.GOLD)
    oy = Inches(1.28)
    for name, desc in CONDENSED_ORGS:
        d.text(s, name, sx, oy, strip_w - Inches(0.5), Inches(0.24), size=12.6, color=d.b.WHITE, bold=True, shrink=True)
        d.text(s, desc, sx, oy + Inches(0.26), strip_w - Inches(0.55), Inches(0.58), size=7.2, color=d.b.LIGHT_TEAL, shrink=True, ls=0.98)
        oy += Inches(1.0)
    footer(d, s, 3, total, dark=True)


def market_and_signals(d: Deck, total: int):
    s = header_slide(
        d,
        "The real-estate AI lane is funded, adopted, and tied to measurable brokerage outcomes",
        "Market proof built directly from the current strategy feed signals and Stage 1 content-research output",
    )
    col_w = Inches(3.95)
    gap = Inches(0.22)
    xs = [d.M, d.M + col_w + gap, d.M + 2 * (col_w + gap)]
    blocks = [
        ("Market size", [
            UC["signals"][0]["extract"],
            "This is large enough to support a real services and workflow-software wedge.",
            "The signal is useful because it frames the category as durable, not a novelty feature."
        ], d.b.SOFT, d.b.NAVY, d.b.INK),
        ("Adoption + conversion", [
            UC["signals"][1]["extract"],
            "The story is not generic AI adoption. It is conversion lift inside revenue workflows.",
            "That makes the first pilot easy to frame around lead quality and speed-to-lead."
        ], d.b.SOFT, d.b.NAVY, d.b.INK),
        ("Competitive signal", [
            "Rechat and Compass show that the operating-system layer is where workflow value compounds.",
            "Brokerages want CRM-native action, not another standalone AI console.",
            "The offer wins when it removes admin drag and preserves agent workflow continuity."
        ], d.b.NAVY, d.b.TEAL, d.b.LIGHT_TEAL),
    ]
    for x, (title, items, fill, title_color, body_color) in zip(xs, blocks):
        d.rect(s, x, Inches(1.78), col_w, Inches(3.8), fill, radius=0.05, shadow=True)
        d.text(s, title, x + Inches(0.2), Inches(1.95), col_w - Inches(0.4), Inches(0.24), size=16, color=title_color, bold=True)
        d.text(s, bullets(items, size=10.8, color=body_color), x + Inches(0.22), Inches(2.28), col_w - Inches(0.42), Inches(2.95), shrink=True)
    footer(d, s, 4, total)


def architecture(d: Deck, total: int):
    s = header_slide(
        d,
        "The winning implementation is CRM-native on the surface and orchestrated behind the scenes",
        "Architecture slide grounded in the current use case stack and prior GBrain brokerage memory",
    )
    left_w = Inches(5.8)
    right_x = d.M + left_w + Inches(0.35)
    d.rect(s, d.M, Inches(1.75), left_w, Inches(4.4), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "ORCHESTRATION AND DATA FLOW", d.M + Inches(0.22), Inches(1.95), left_w - Inches(0.4), Inches(0.24), size=15, color=d.b.TEAL, bold=True)
    stack_points = [
        "Lead scoring agent evaluates behavior, CRM history, and listing signals before routing or nurture.",
        "Transaction agent handles documents, deadlines, compliance checks, and stakeholder coordination.",
        "CMA agent assembles comps, pricing ranges, and client-ready recommendation output.",
        "CRM, MLS, DocuSign, title, and lender systems remain the systems of record.",
        "Workflow orchestration stays internal; agents and brokers work inside the brokerage stack they already know."
    ]
    d.text(s, bullets(stack_points, size=10.9, color=d.b.WHITE), d.M + Inches(0.22), Inches(2.28), left_w - Inches(0.44), Inches(3.35), shrink=True)
    cards = [
        ("Why the architecture is credible", "The use case already specifies experience, orchestration, context, and actuation layers rather than a vague AI wrapper."),
        ("What GBrain contributed", "The reused brokerage recall artifact reinforced the prior workflow spine: lead routing, lease/document support, marketing automation, and MCP-style integrations."),
    ]
    cy = Inches(1.75)
    for title, body in cards:
        d.rect(s, right_x, cy, Inches(6.0), Inches(1.98), d.b.SOFT, radius=0.05, shadow=True)
        d.text(s, title, right_x + Inches(0.2), cy + Inches(0.16), Inches(5.6), Inches(0.28), size=14.0, color=d.b.NAVY, bold=True, shrink=True)
        d.text(s, body, right_x + Inches(0.2), cy + Inches(0.5), Inches(5.6), Inches(1.18), size=10.4, color=d.b.INK, shrink=True)
        cy += Inches(2.12)
    footer(d, s, 5, total)


def risks_and_roadmap(d: Deck, total: int):
    s = header_slide(
        d,
        "The lane is commercially strong, but adoption depends on workflow fit and governance",
        "Structured risks, controls, and 90-day plan for a first brokerage pilot",
    )
    d.rect(s, d.M, Inches(1.75), Inches(6.1), Inches(4.55), d.b.SOFT, radius=0.05, shadow=True)
    d.text(s, "RISKS AND CONTROLS", d.M + Inches(0.22), Inches(1.95), Inches(2.5), Inches(0.22), size=15, color=d.b.NAVY, bold=True)
    risks = [
        "Agent trust risk: keep AI assistive first and preserve human override on routing and customer-facing actions.",
        "Data quality risk: poor CRM hygiene weakens lead scoring and downstream workflow logic.",
        "Compliance risk: document, disclosure, and fair-housing controls must be explicit in automated steps.",
        "Change-management risk: launch inside one office or team before broad workflow rollout."
    ]
    d.text(s, bullets(risks, size=10.9, color=d.b.INK), d.M + Inches(0.22), Inches(2.28), Inches(5.55), Inches(3.4), shrink=True)
    rx = Inches(6.95)
    d.rect(s, rx, Inches(1.75), Inches(5.75), Inches(4.55), d.b.NAVY, radius=0.05, shadow=True)
    d.text(s, "90-DAY ROADMAP", rx + Inches(0.22), Inches(1.95), Inches(3.0), Inches(0.22), size=15, color=d.b.TEAL, bold=True)
    roadmap = [
        "Days 1-15: map lead sources, CRM fields, routing rules, and transaction checkpoints.",
        "Days 16-35: configure the scoring, routing, and workflow logic for one brokerage stack.",
        "Days 36-60: launch for one team and track response speed, lead quality, and manual touchpoint reduction.",
        "Days 61-90: refine rules and scope expansion into transaction coordination and CMA generation."
    ]
    d.text(s, bullets(roadmap, size=10.7, color=d.b.LIGHT_TEAL), rx + Inches(0.22), Inches(2.28), Inches(5.25), Inches(3.4), shrink=True)
    footer(d, s, 6, total)


def closing(d: Deck, total: int):
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.16), d.b.TEAL)
    d.text(s, "BOTTOM LINE", d.M, Inches(1.15), Inches(3), Inches(0.25), size=16, color=d.b.TEAL, bold=True)
    d.text(
        s,
        "The tested real-estate pipeline produced a credible brokerage workflow story: capture better leads, move transactions faster, and keep the user inside the brokerage stack.",
        d.M, Inches(1.6), Inches(11.6), Inches(1.3), size=22, color=d.b.WHITE, bold=True, shrink=True
    )
    d.rect(s, d.M, Inches(3.15), Inches(11.9), Inches(0.06), d.b.GOLD)
    final_points = [
        "The Stage 1 chain is now reproducible from `/content-ideas` feed to local run artifacts.",
        "GBrain recall is visibly part of the chain even when the host falls back to prior repo-local memory.",
        "The next skill-chain step is vertical scoring, then a fuller strategy and account-specific deck branch if the lane remains a GO."
    ]
    d.text(s, bullets(final_points, size=15.0, color=d.b.LIGHT_TEAL, space_before=10), d.M, Inches(3.45), Inches(10.9), Inches(1.9), shrink=True)
    d.rect(s, d.M, Inches(5.95), Inches(11.9), Inches(0.72), d.b.GOLD, radius=0.05)
    d.text(
        s,
        "Suggested next step: keep this deck as the Stage 1 real-estate brokerage test artifact, then decide whether to continue the skill chain into vertical scoring and full strategy.",
        d.M + Inches(0.3), Inches(6.08), Inches(11.3), Inches(0.42), size=10.8, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True
    )
    footer(d, s, 7, total, dark=True)


def main():
    total = 7
    d = Deck(footer="Real Estate Brokerage AI | Client Package | June 2026")
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, d.W - Inches(3.0), 0, Inches(3.0), d.H, d.b.NAVY_2)
    d.rect(s, d.W - Inches(3.0), 0, Inches(0.06), d.H, d.b.TEAL)
    d.text(s, "CLIENT PACKAGE", d.M, Inches(0.95), Inches(3), Inches(0.25), size=15, color=d.b.TEAL, bold=True)
    d.text(s, "Real Estate Brokerage AI\nLead Scoring to Closing Automation", d.M, Inches(1.45), Inches(7.8), Inches(1.26), size=27, color=d.b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.75), Inches(1.6), Inches(0.06), d.b.TEAL)
    d.text(
        s,
        "A branded Stage 1 test package built from the June 4, 2026 strategy feed, repo-local GBrain recall reuse, and feed-grounded content-research artifacts.",
        d.M, Inches(3.05), Inches(7.8), Inches(1.0), size=14.0, color=d.b.WHITE, shrink=True
    )
    d.text(s, "USE CASE REALIZATION · MARKET PROOF · ARCHITECTURE · RISKS · ROADMAP · NEXT STEP",
           d.M, Inches(5.75), Inches(8.6), Inches(0.28), size=11, color=d.b.GOLD, bold=True)
    footer(d, s, 1, total, dark=True)
    executive_summary(d, total)
    use_case_realization(d, total)
    market_and_signals(d, total)
    architecture(d, total)
    risks_and_roadmap(d, total)
    closing(d, total)
    d.save(DRAFT_OUT)
    print(DRAFT_OUT)


if __name__ == "__main__":
    main()
