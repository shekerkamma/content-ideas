#!/usr/bin/env python3
"""Build a branded PPTX playbook from the Nick/Orgo solo agent business course."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")

from pptxkit import Deck, PP_ALIGN, Inches, hx


RUN_DIR = Path(__file__).resolve().parent
OUT = RUN_DIR / "solo-ai-agent-business-course-reviewed.pptx"
TOTAL = 14
FOOTER = "The $1M+ Solo AI Agent Business · Nick from Orgo · Course notes"

d = Deck(footer=FOOTER)
b = d.b

GREEN = hx("20B486")
BLUE = hx("3B82F6")
VIOLET = hx("7C3AED")
RED = hx("D64550")
SLATE = hx("EEF3F6")
SLATE_D = hx("D6DEE6")
INK_2 = hx("34465A")


def title_slide():
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.14), b.TEAL)
    d.rect(s, Inches(10.45), 0, Inches(2.88), d.H, b.NAVY_2)
    d.rect(s, Inches(10.25), 0, Inches(0.08), d.H, b.TEAL)
    d.text(s, "SCREEN-SHARED PLAYBOOK", d.M, Inches(0.78), Inches(6.5), Inches(0.3),
           size=12, color=b.TEAL, bold=True)
    d.text(s, "The $1M+ Solo\nAI Agent Business", d.M, Inches(1.25), Inches(8.8), Inches(1.8),
           size=44, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(3.22), Inches(2.1), Inches(0.06), b.TEAL)
    d.text(
        s,
        "A practical course summary: offer, market, stack, and the live workflow for agents setting up agents.",
        d.M,
        Inches(3.45),
        Inches(7.7),
        Inches(0.8),
        size=17,
        color=b.LIGHT_TEAL,
        shrink=True,
    )
    chips = ["$5K/mo", "1-3 real agents", "<48h live", "vertical outcome"]
    for i, chip in enumerate(chips):
        x = d.M + Inches(i * 2.05)
        d.rect(s, x, Inches(4.7), Inches(1.75), Inches(0.45), b.NAVY_2, line=b.TEAL, radius=0.02)
        d.text(s, chip, x, Inches(4.82), Inches(1.75), Inches(0.18), size=11,
               color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, "Content source: user-provided complete captions; frame coverage sparse.",
           d.M, Inches(6.88), Inches(8.2), Inches(0.25), size=9.5, color=hx("8FA0B3"))
    d.footer(s, 1, TOTAL, dark=True)


def header(s, title, subtitle=None, page=1):
    d.header(s, title, subtitle)
    d.footer(s, page, TOTAL)


def card(s, x, y, w, h, title, body, color=None, number=None, fill=None):
    color = color or b.TEAL
    fill = fill or b.WHITE
    d.rect(s, x, y, w, h, fill, line=SLATE_D, radius=0.02, shadow=True)
    compact = h < Inches(1.15)
    title_size = 12.0 if compact else 14.5
    body_size = 8.6 if compact else 11.3
    title_y = y + (Inches(0.13) if compact else Inches(0.2))
    body_y = y + (Inches(0.45) if compact else Inches(0.72))
    if number:
        d.rect(s, x + Inches(0.18), y + Inches(0.18), Inches(0.42), Inches(0.42), color, radius=0.08)
        d.text(s, number, x + Inches(0.18), y + Inches(0.27), Inches(0.42), Inches(0.16),
               size=10, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        tx = x + Inches(0.72)
        tw = w - Inches(0.9)
    else:
        tx = x + Inches(0.22)
        tw = w - Inches(0.44)
    d.text(s, title, tx, title_y, tw, Inches(0.28 if compact else 0.36),
           size=title_size, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, x + Inches(0.22), body_y, w - Inches(0.44),
           h - (Inches(0.55) if compact else Inches(0.88)),
           size=body_size, color=INK_2, ls=1.15 if compact else 1.25, shrink=True)


def bullets(s, items, x, y, w, h, color=None, size=12.2):
    color = color or b.TEAL
    rows = []
    for item in items:
        rows.append({"text": item, "bullet": True, "space_before": 7, "size": size})
    d.text(s, rows, x, y, w, h, size=size, color=INK_2, shrink=True)


def section_slide(page, label, title, subtitle):
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.16), d.H, b.TEAL)
    d.text(s, label, d.M, Inches(1.0), Inches(3.5), Inches(0.3), size=13,
           color=b.TEAL, bold=True)
    d.text(s, title, d.M, Inches(1.55), Inches(9.5), Inches(1.25), size=38,
           color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(3.0), Inches(2.0), Inches(0.06), b.TEAL)
    d.text(s, subtitle, d.M, Inches(3.28), Inches(8.2), Inches(0.75), size=16,
           color=b.LIGHT_TEAL, shrink=True)
    d.footer(s, page, TOTAL, dark=True)


def build():
    title_slide()

    s = d.slide(fill=b.WHITE)
    header(s, "Business In One Line", "Sell a managed digital employee, not agent infrastructure.", 2)
    d.rect(s, d.M, Inches(1.85), d.CW, Inches(1.18), b.NAVY, radius=0.02)
    d.text(s, "\"We build and manage your digital employee\"\nfor $5K/month.",
           d.M + Inches(0.35), Inches(2.03), d.CW - Inches(0.7), Inches(0.72),
           size=20, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    cols = [
        ("Customer buys", "A business outcome and a named employee that knows their company.", b.TEAL),
        ("You hide", "Tokens, models, credits, infra, auth, monitoring, and agent plumbing.", b.CORAL),
        ("Value compounds", "The agent is adjusted weekly, so the relationship looks like staff augmentation.", b.GOLD),
    ]
    for i, (t, body, c) in enumerate(cols):
        card(s, d.M + Inches(i * 4.12), Inches(3.45), Inches(3.75), Inches(1.75), t, body, c)
    d.text(s, "Positioning test: if the buyer asks about token limits,\nthe offer has already become too technical.",
           d.M, Inches(6.05), d.CW, Inches(0.62), size=13.5, color=b.NAVY, bold=True,
           align=PP_ALIGN.CENTER, shrink=True)

    s = d.slide(fill=b.WHITE)
    header(s, "The Offer Sells Abundance", "Unlimited on the outside; tightly managed on the inside.", 3)
    left = d.M
    d.rect(s, left, Inches(1.82), Inches(5.65), Inches(4.55), b.SOFT, line=SLATE_D, radius=0.02)
    d.text(s, "PUBLIC OFFER", left + Inches(0.25), Inches(2.05), Inches(5.1), Inches(0.28),
           size=12, color=b.TEAL, bold=True)
    bullets(s, [
        "Unlimited agents",
        "Unlimited usage",
        "Monitoring and support",
        "Security and access management",
        "Ongoing changes as the business changes",
    ], left + Inches(0.35), Inches(2.45), Inches(5.0), Inches(2.5), b.TEAL)
    right = d.M + Inches(6.25)
    d.rect(s, right, Inches(1.82), Inches(5.88), Inches(4.55), b.NAVY, radius=0.02)
    d.text(s, "OPERATING REALITY", right + Inches(0.25), Inches(2.05), Inches(5.4), Inches(0.28),
           size=12, color=b.GOLD, bold=True)
    bullets(s, [
        "Customers think they need 5/10/100 agents.",
        "Most accounts need 1-3 well-built agents.",
        "Token spend stays controlled by workflow design.",
        "Scope is throttled through request intake.",
        "Do not say tokens, credits, or usage caps.",
    ], right + Inches(0.35), Inches(2.45), Inches(5.15), Inches(2.65), b.GOLD, size=11.8)
    d.text(s, "The trick is packaging capacity\nin buyer language.",
           right + Inches(0.35), Inches(5.55), Inches(5.1), Inches(0.55), size=11,
           color=b.WHITE, bold=True, shrink=True)

    s = d.slide(fill=b.WHITE)
    header(s, "Go Vertical, But Let Pull Decide", "Start broad enough to learn; converge where the market responds.", 4)
    safe = [
        ("Marketing agencies", "content ops, client follow-up, reporting"),
        ("Law firms", "meetings, demand letters, open loops"),
        ("Insurance agencies", "renewals, intake, carrier follow-up"),
        ("Manufacturers", "supplier, quoting, ops coordination"),
        ("Wholesalers", "catalog, orders, customer service"),
        ("Real estate", "lead follow-up, transaction coordination"),
    ]
    avoid = [("Healthcare", "regulatory and privacy friction"), ("Finance", "regulatory and compliance burden")]
    d.text(s, "TARGET LANES", d.M, Inches(1.78), Inches(3), Inches(0.3), size=12, color=b.TEAL, bold=True)
    for i, (name, note) in enumerate(safe):
        x = d.M + Inches((i % 3) * 4.05)
        y = Inches(2.18) + Inches((i // 3) * 1.12)
        card(s, x, y, Inches(3.72), Inches(0.9), name, note, b.TEAL, fill=hx("F8FBFC"))
    d.text(s, "AVOID EARLY", d.M, Inches(4.78), Inches(3), Inches(0.3), size=12, color=RED, bold=True)
    for i, (name, note) in enumerate(avoid):
        card(s, d.M + Inches(i * 6.2), Inches(5.15), Inches(5.7), Inches(0.95), name, note, RED, fill=hx("FFF7F8"))
    d.text(s, "Niche-down options: geography, sub-type, or executive workflow. Example: commercial IDA, matrimonial law firm.",
           d.M, Inches(6.45), d.CW, Inches(0.36), size=12.5, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)

    s = d.slide(fill=b.WHITE)
    header(s, "Sell The Executive Layer First", "Different industries, same executive pain: calls, meetings, follow-ups, open loops.", 5)
    steps = [
        ("01", "Capture", "Meetings, calls, email, and ad hoc requests become structured memory.", BLUE),
        ("02", "Resolve", "The agent handles follow-ups, drafts, coordination, and status chasing.", b.TEAL),
        ("03", "Specialize", "Add vertical skills: demand letters, renewal prep, quote packets, property updates.", b.GOLD),
        ("04", "Improve", "Weekly changes turn customer feedback into a sharper digital employee.", GREEN),
    ]
    for i, (num, t, body, color) in enumerate(steps):
        x = d.M + Inches(i * 3.15)
        card(s, x, Inches(2.0), Inches(2.85), Inches(2.15), t, body, color, number=num)
        if i < 3:
            d.text(s, "→", x + Inches(2.93), Inches(2.72), Inches(0.26), Inches(0.3),
                   size=20, color=b.MUTED, bold=True)
    d.rect(s, d.M, Inches(4.85), d.CW, Inches(0.95), b.NAVY, radius=0.02)
    d.text(s, "Template the common executive agent first.\nVertical specificity is an added skill layer, not the starting point.",
           d.M + Inches(0.35), Inches(5.02), d.CW - Inches(0.7), Inches(0.62),
           size=15.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)

    section_slide(6, "GO-TO-MARKET", "Warm Inbound Beats Cold Outreach", "Content creates trust before the sales call. Free work can buy the first proof points.")

    s = d.slide(fill=b.WHITE)
    header(s, "Customer Acquisition Is Proof-Led", "\"Content is king in 2026 — just do it.\"", 7)
    lanes = [
        ("Content", "Post open build videos, teardown clips, before/after workflows, and agent demos.", b.TEAL),
        ("Case studies", "Start free or discounted if it creates referrals and a story with receipts.", b.GOLD),
        ("Warm inbound", "Use the content trail to turn buyers from skeptical to curious before the call.", GREEN),
    ]
    for i, (t, body, color) in enumerate(lanes):
        card(s, d.M + Inches(i * 4.13), Inches(2.05), Inches(3.78), Inches(2.3), t, body, color, number=f"0{i+1}")
    d.rect(s, d.M, Inches(5.05), d.CW, Inches(1.0), b.SOFT, line=SLATE_D, radius=0.02)
    d.text(s, "Contrarian but practical: you do not need to start hyper-niche.\nDiverge, find pull, then converge on the vertical that sells back to you.",
           d.M + Inches(0.35), Inches(5.22), d.CW - Inches(0.7), Inches(0.66),
           size=13.2, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)

    s = d.slide(fill=b.WHITE)
    header(s, "The Customer-Facing Layer Keeps Scope Clean", "The buyer experiences a service desk, not an engineering project.", 8)
    tools = [
        ("Granola", "Meeting capture; MCP-ready context source.", BLUE),
        ("Linear", "Customer drags requests; cap 1-2 per 48h to prevent scope creep.", b.TEAL),
        ("Loom", "Async update videos showing what changed.", b.GOLD),
        ("Calendly", "Book live working sessions without back-and-forth.", GREEN),
        ("Asana", "Internal delivery tracking and implementation queue.", VIOLET),
    ]
    for i, (name, note, color) in enumerate(tools):
        y = Inches(1.85) + Inches(i * 0.82)
        d.rect(s, d.M, y, Inches(2.0), Inches(0.55), color, radius=0.02)
        d.text(s, name, d.M + Inches(0.12), y + Inches(0.16), Inches(1.76), Inches(0.2),
               size=12, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, note, d.M + Inches(2.25), y + Inches(0.12), Inches(9.7), Inches(0.3),
               size=13, color=INK_2, shrink=True)
    d.text(s, "The cap is important: abundance is the offer; paced intake is the operating system.",
           d.M, Inches(6.28), d.CW, Inches(0.34), size=14.5, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)

    section_slide(9, "DELIVERY STACK", "Use Agents To Build Agents", "The agency becomes an agent factory: strategy, setup, auth, context, tools, and ongoing improvement.")

    s = d.slide(fill=b.WHITE)
    header(s, "Agent Stack: The Factory Pattern", "Harness, workspace, auth, mail, memory, and model routing each have a job.", 10)
    rows = [
        ("Harness", "Hermes for reliable self-evolving agents; Claude Code / Codex desktop apps to build.", b.NAVY),
        ("Workspace", "Orgo gives each customer a real computer workspace, manageable via Orgo MCP.", BLUE),
        ("Auth / Tools", "Composio provides the one-MCP interface to customer apps and security.", b.TEAL),
        ("Identity", "Agent Mail gives each agent its own inbox and persona, e.g. Mia.", b.GOLD),
        ("Memory", "Obsidian is the markdown second brain: people, projects, transcripts, decisions.", GREEN),
    ]
    for i, (layer, desc, color) in enumerate(rows):
        y = Inches(1.75) + Inches(i * 0.88)
        d.rect(s, d.M, y, Inches(2.05), Inches(0.58), color, radius=0.02)
        d.text(s, layer, d.M + Inches(0.14), y + Inches(0.17), Inches(1.77), Inches(0.2),
               size=11.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.rect(s, d.M + Inches(2.25), y, Inches(9.88), Inches(0.58), b.SOFT, line=SLATE_D, radius=0.02)
        d.text(s, desc, d.M + Inches(2.45), y + Inches(0.16), Inches(9.45), Inches(0.22),
               size=12.2, color=INK_2, shrink=True)

    s = d.slide(fill=b.WHITE)
    header(s, "Model Routing Keeps Margins Healthy", "Use the best model where it matters; route cheap work elsewhere.", 11)
    model_cards = [
        ("GPT-5.5", "Best all-around in Nick's stack: efficient tool calls, strong general execution.", b.TEAL),
        ("GLM-5.1 / Kimi", "Cheap lightweight tasks where speed and cost matter more than depth.", GREEN),
        ("Opus 4.7", "Long-horizon coding and hard implementation work.", VIOLET),
    ]
    for i, (name, body, color) in enumerate(model_cards):
        card(s, d.M + Inches(i * 4.12), Inches(1.95), Inches(3.75), Inches(2.15), name, body, color)
    d.rect(s, d.M, Inches(4.8), d.CW, Inches(1.05), b.NAVY, radius=0.02)
    d.text(s, "Margin rule: outcomes justify model spend.",
           d.M + Inches(0.35), Inches(5.02), d.CW - Inches(0.7), Inches(0.62),
           size=16, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)

    s = d.slide(fill=b.WHITE)
    header(s, "Setup Context Is A Multi-Agent Research Job", "Nick spawns source-specific agents, then merges the best practices.", 12)
    sources = [
        ("Perplexity", "current answers"),
        ("Exa", "source discovery"),
        ("Context7", "library docs"),
        ("X MCP", "fresh setup signals"),
        ("Repo/docs", "implementation truth"),
    ]
    for i, (name, note) in enumerate(sources):
        x = d.M + Inches(i * 2.45)
        d.rect(s, x, Inches(2.05), Inches(2.05), Inches(1.0), b.SOFT, line=SLATE_D, radius=0.02)
        d.text(s, name, x + Inches(0.12), Inches(2.28), Inches(1.8), Inches(0.25),
               size=13, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, note, x + Inches(0.12), Inches(2.62), Inches(1.8), Inches(0.22),
               size=9.5, color=b.MUTED, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "5 agents", d.M, Inches(3.62), Inches(1.65), Inches(0.34),
           size=17, color=b.TEAL, bold=True)
    d.text(s, "→ merge best practices → configure the customer agent",
           d.M + Inches(2.05), Inches(3.64), Inches(9.2), Inches(0.28),
           size=14.2, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, d.M, Inches(4.65), d.CW, Inches(1.05), b.SOFT, line=SLATE_D, radius=0.02)
    d.text(s, "This is the course's core operating leverage:\nagents do the setup research and scaffolding for the next agent.",
           d.M + Inches(0.35), Inches(4.88), d.CW - Inches(0.7), Inches(0.62),
           size=13.5, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)

    s = d.slide(fill=b.WHITE)
    header(s, "Live Demo Pattern: Agents Setting Up Agents", "The implementation loop is repeatable across customers.", 13)
    steps = [
        ("1", "Create workspace", "Orgo workspace with isolated computer and tools."),
        ("2", "Attach auth and apps", "Composio + customer tools + Agent Mail identity."),
        ("3", "Build the vault", "Obsidian context: people, projects, meetings, transcripts."),
        ("4", "Spawn setup agents", "Per-source research agents collect current setup practice."),
        ("5", "Merge and deploy", "Best-practice plan becomes the live digital employee."),
        ("6", "Improve weekly", "Requests, Loom updates, and monitoring feed the next iteration."),
    ]
    for i, (num, t, body) in enumerate(steps):
        x = d.M + Inches((i % 3) * 4.12)
        y = Inches(1.82) + Inches((i // 3) * 2.0)
        card(s, x, y, Inches(3.75), Inches(1.55), t, body, b.TEAL if i < 3 else b.GOLD, number=num)
    d.text(s, "The demo is not a stunt; it is a service delivery architecture.",
           d.M, Inches(6.28), d.CW, Inches(0.34), size=14.5, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)

    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.14), b.TEAL)
    d.text(s, "Execution Checklist", d.M, Inches(0.68), d.CW, Inches(0.6),
           size=34, color=b.WHITE, bold=True)
    d.rect(s, d.M, Inches(1.38), Inches(1.8), Inches(0.06), b.TEAL)
    checklist = [
        ("Package", "Digital employee, $5K/month, unlimited-feeling managed service."),
        ("Pick lanes", "Start with legacy, people-heavy verticals; avoid regulated complexity early."),
        ("Prove", "Publish build content and use early work for case studies/referrals."),
        ("Control scope", "Customer request board with 1-2 changes per 48h."),
        ("Install stack", "Hermes / Claude Code / Codex + Orgo + Composio + Agent Mail + Obsidian."),
        ("Operate", "Weekly improvements, Loom updates, monitoring, and auth hygiene."),
    ]
    for i, (t, body) in enumerate(checklist):
        y = Inches(1.86) + Inches(i * 0.7)
        d.rect(s, d.M, y + Inches(0.04), Inches(0.28), Inches(0.28), b.TEAL, radius=0.06)
        d.text(s, str(i + 1), d.M, y + Inches(0.11), Inches(0.28), Inches(0.1),
               size=8.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, t, d.M + Inches(0.45), y, Inches(1.6), Inches(0.28),
               size=13, color=b.WHITE, bold=True)
        d.text(s, body, d.M + Inches(2.1), y, Inches(9.2), Inches(0.28),
               size=12.2, color=b.LIGHT_TEAL, shrink=True)
    d.rect(s, d.M, Inches(6.45), d.CW, Inches(0.52), b.NAVY_2, line=b.TEAL, radius=0.02)
    d.text(s, "The durable wedge: become the operator who can sell business outcomes and industrialize agent delivery.",
           d.M + Inches(0.25), Inches(6.61), d.CW - Inches(0.5), Inches(0.18),
           size=12.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.footer(s, 14, TOTAL, dark=True)

    d.save(OUT)


if __name__ == "__main__":
    build()
