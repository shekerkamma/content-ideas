#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, Inches, PP_ALIGN, MSO_ANCHOR


RUN = Path("runs/2026-07-01-hermes-use-cases-realization-sop")
OUT = RUN / "artifacts" / "Hermes_Use_Cases_Realization_SOP-reviewed.pptx"
DESKTOP = Path("/mnt/c/Users/sheke/OneDrive/Desktop/Hermes_Use_Cases_Realization_SOP-reviewed.pptx")


FOOTER = "Hermes Agent Use Cases & Realization SOP | 2026-07-01"


def bullets(items, size=13.2):
    return [{"text": item, "bullet": True, "size": size, "space_before": 5} for item in items]


def add_kicker(d, s, text, top=0.55):
    d.text(s, text.upper(), d.M, Inches(top), d.CW, Inches(0.28), size=12.5, color=d.b.TEAL, bold=True)


def section(d, s, label, title, subtitle):
    b = d.b
    d.rect(s, 0, 0, d.W, d.H, b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.text(s, label.upper(), Inches(0.72), Inches(1.25), Inches(3), Inches(0.32), size=13, color=b.TEAL, bold=True)
    d.text(s, title, Inches(0.72), Inches(1.72), Inches(8.7), Inches(1.35), size=38, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(0.72), Inches(3.0), Inches(1.6), Inches(0.05), b.GOLD)
    d.text(s, subtitle, Inches(0.72), Inches(3.35), Inches(7.8), Inches(0.75), size=18, color=b.LIGHT_TEAL, shrink=True)


def card(d, s, x, y, w, h, title, body, accent=None, idx=None, body_size=10.4):
    b = d.b
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(h), b.WHITE, line=b.GRID, radius=0.08, shadow=True)
    if accent:
        d.rect(s, Inches(x), Inches(y), Inches(0.08), Inches(h), accent)
    if idx:
        d.rect(s, Inches(x + 0.16), Inches(y + 0.16), Inches(0.42), Inches(0.28), b.NAVY, radius=0.06)
        d.text(s, idx, Inches(x + 0.16), Inches(y + 0.19), Inches(0.42), Inches(0.18), size=8.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        title_x = x + 0.68
        title_w = w - 0.86
    else:
        title_x = x + 0.22
        title_w = w - 0.44
    d.text(s, title, Inches(title_x), Inches(y + 0.12), Inches(title_w), Inches(0.32), size=10.8, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, Inches(x + 0.22), Inches(y + 0.50), Inches(w - 0.44), Inches(h - 0.58), size=body_size, color=b.INK, shrink=True)


def use_case_slide(d, title, subtitle, challenge, realized, steps, stack, systems, guardrails, page, total):
    b = d.b
    s = d.slide(fill=b.SOFT)
    d.header(s, title, subtitle)
    d.rect(s, d.M, Inches(1.75), Inches(3.2), Inches(5.0), b.TEAL, radius=0.06)
    d.text(s, "Challenge", Inches(0.86), Inches(2.05), Inches(2.65), Inches(0.3), size=15, color=b.NAVY, bold=True)
    d.text(s, challenge, Inches(0.86), Inches(2.45), Inches(2.65), Inches(1.45), size=10.5, color=b.NAVY, shrink=True)
    d.text(s, "Realization", Inches(0.86), Inches(4.18), Inches(2.65), Inches(0.3), size=15, color=b.NAVY, bold=True)
    d.text(s, realized, Inches(0.86), Inches(4.58), Inches(2.65), Inches(1.55), size=10.2, color=b.NAVY, shrink=True)

    d.text(s, "How It Works", Inches(4.15), Inches(1.86), Inches(4.7), Inches(0.3), size=15, color=b.NAVY, bold=True)
    x = 4.15
    for i, step in enumerate(steps, 1):
        d.rect(s, Inches(x), Inches(2.34), Inches(1.2), Inches(0.95), b.WHITE, line=b.GRID, radius=0.08, shadow=True)
        d.text(s, f"{i}", Inches(x + 0.08), Inches(2.46), Inches(0.24), Inches(0.18), size=8, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, step, Inches(x + 0.14), Inches(2.58), Inches(0.92), Inches(0.46), size=8.1, color=b.INK, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        if i < len(steps):
            d.text(s, "→", Inches(x + 1.18), Inches(2.55), Inches(0.25), Inches(0.25), size=15, color=b.MUTED, bold=True)
        x += 1.36

    d.rect(s, Inches(4.15), Inches(3.68), Inches(4.7), Inches(0.65), b.NAVY, radius=0.06)
    d.text(s, stack, Inches(4.38), Inches(3.87), Inches(4.22), Inches(0.2), size=10.8, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)

    card(d, s, 4.15, 4.67, 2.2, 1.25, "Systems", systems, accent=b.ACCENT, body_size=10.8)
    card(d, s, 6.65, 4.67, 2.2, 1.25, "Controls", guardrails, accent=b.GOLD, body_size=10.8)

    d.rect(s, Inches(9.35), Inches(1.75), Inches(3.35), Inches(5.0), b.NAVY, radius=0.05)
    d.text(s, "SOP Acceptance Gate", Inches(9.65), Inches(2.05), Inches(2.75), Inches(0.32), size=15, color=b.TEAL, bold=True)
    d.text(s, bullets([
        "Trigger is explicit",
        "Inputs and owners are listed",
        "Source order is wired",
        "Output artifact is named",
        "Autonomy level is declared",
        "Approval rules are written",
        "Verification is repeatable",
    ], size=9.4), Inches(9.65), Inches(2.55), Inches(2.75), Inches(3.35), size=9.4, color=b.WHITE, shrink=True)
    d.footer(s, page, total)


def build():
    d = Deck(footer=FOOTER)
    b = d.b
    total = 20

    # 1 cover
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(11.2), 0, Inches(2.13), d.H, b.NAVY_2)
    d.rect(s, Inches(11.2), 0, Inches(0.08), d.H, b.TEAL)
    add_kicker(d, s, "Client-ready implementation SOP")
    d.text(s, "Hermes Agent\nUse Cases & Realization", d.M, Inches(1.35), Inches(8.9), Inches(1.55), size=42, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(3.22), Inches(1.6), Inches(0.06), b.GOLD)
    d.text(s, "Spec-driven operating model for implementing personal-agent workflows with You.com search, GBrain memory, model routing, cron jobs, and approval gates.", d.M, Inches(3.62), Inches(8.4), Inches(0.9), size=18, color=b.LIGHT_TEAL, shrink=True)
    for i, chip in enumerate(["Goal-loop controlled", "AI-analyst synthesized", "Branded PPTX reviewed"]):
        d.rect(s, Inches(0.6 + i * 2.55), Inches(5.55), Inches(2.25), Inches(0.42), b.NAVY_2, line=b.TEAL, radius=0.08)
        d.text(s, chip, Inches(0.73 + i * 2.55), Inches(5.68), Inches(2.0), Inches(0.14), size=9.8, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.footer(s, 1, total, dark=True)

    # 2 executive SOP
    s = d.slide(fill=b.SOFT)
    d.header(s, "The Implementation Object Is An Operating SOP", "Every use case needs trigger, source order, output, autonomy level, and verification gate.")
    card(d, s, 0.65, 1.95, 2.8, 1.35, "1. Goal Contract", "Define outcome, artifacts, constraints, acceptance criteria, verification, loop budget, and stop conditions.", accent=b.TEAL, idx="01")
    card(d, s, 3.72, 1.95, 2.8, 1.35, "2. Chain Contract", "Define what each skill consumes, produces, and hands to the next consumer before execution.", accent=b.GOLD, idx="02")
    card(d, s, 6.79, 1.95, 2.8, 1.35, "3. Use-Case Spec", "Declare trigger, inputs, source order, autonomy level, human approval rules, and output artifact.", accent=b.ACCENT, idx="03")
    card(d, s, 9.86, 1.95, 2.8, 1.35, "4. Runbook", "Operationalize cron, model routing, cost controls, credential boundaries, and failure handling.", accent=b.AMBER, idx="04")
    d.rect(s, d.M, Inches(4.15), d.CW, Inches(1.15), b.NAVY, radius=0.06)
    d.text(s, "BLUF", Inches(0.9), Inches(4.42), Inches(0.75), Inches(0.26), size=13, color=b.GOLD, bold=True)
    d.text(s, "Hermes is implemented as a repeatable system: install the harness, wire search and memory, launch read-only routines, then move into draft and approval-gated execution.", Inches(1.75), Inches(4.32), Inches(10.7), Inches(0.5), size=12.4, color=b.WHITE, shrink=True)
    d.footer(s, 2, total)

    # 3 thesis
    section(d, d.slide(), "Section 01", "Hermes Is The Agent Operating Layer", "The harness gives the model tools, files, search, schedules, and memory.")
    d.footer(d.prs.slides[-1], 3, total, dark=True)

    # 4 architecture
    s = d.slide(fill=b.SOFT)
    d.header(s, "Reference Architecture", "Search, memory, scheduled routines, and approval gates.")
    layers = [
        ("User / Owner", "Goals, approvals, corrections, final sends"),
        ("Hermes Harness", "CLI/desktop, shell, files, browser, plugins, cron"),
        ("Model Router", "Sonnet default, Opus for code, Haiku for parsing"),
        ("Search Layer", "You.com first; Exa/Firecrawl as specialists"),
        ("Memory Layer", "GBrain markdown graph + Obsidian visibility"),
        ("Connected Systems", "Email, calendar, Slack/Teams, Zoom, CRM, social"),
    ]
    y = 1.8
    for i, (name, desc) in enumerate(layers):
        fill = b.NAVY if i == 1 else b.WHITE
        col = b.WHITE if i == 1 else b.INK
        d.rect(s, Inches(0.95), Inches(y), Inches(4.0), Inches(0.62), fill, line=b.GRID, radius=0.05, shadow=True)
        d.text(s, name, Inches(1.16), Inches(y + 0.09), Inches(1.45), Inches(0.24), size=10.5, color=b.TEAL if i == 1 else b.NAVY, bold=True)
        d.text(s, desc, Inches(2.65), Inches(y + 0.07), Inches(2.08), Inches(0.36), size=7.8, color=col, shrink=True)
        if i < len(layers) - 1:
            d.text(s, "↓", Inches(2.82), Inches(y + 0.62), Inches(0.22), Inches(0.16), size=13, color=b.MUTED, bold=True)
        y += 0.78
    d.rect(s, Inches(6.0), Inches(1.9), Inches(6.2), Inches(3.9), b.WHITE, line=b.GRID, radius=0.08, shadow=True)
    d.text(s, "Operating Loop", Inches(6.35), Inches(2.18), Inches(2.8), Inches(0.26), size=16, color=b.NAVY, bold=True)
    loop = ["Observe", "Recall", "Search", "Synthesize", "Draft", "Approve", "Execute", "Learn"]
    for i, item in enumerate(loop):
        x = 6.35 + (i % 4) * 1.38
        yy = 2.75 + (i // 4) * 1.24
        d.rect(s, Inches(x), Inches(yy), Inches(1.02), Inches(0.62), b.SOFT, line=b.TEAL, radius=0.08)
        d.text(s, item, Inches(x + 0.08), Inches(yy + 0.21), Inches(0.86), Inches(0.15), size=9.5, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        if i not in [3, 7]:
            d.text(s, "→", Inches(x + 1.08), Inches(yy + 0.18), Inches(0.22), Inches(0.2), size=12, color=b.MUTED, bold=True)
    d.footer(s, 4, total)

    # 5 source/tool order
    s = d.slide(fill=b.SOFT)
    d.header(s, "Source And Tool Order", "Policy prevents fallback to generic web search by habit.")
    order = [
        ("1", "Local Files", "Run docs, SOPs, prior artifacts, configs"),
        ("2", "GBrain Recall", "Semantic memory for people, companies, verticals"),
        ("3", "You.com", "Current web, livecrawl, research, finance research"),
        ("4", "Exa", "Semantic/source discovery and candidate leads"),
        ("5", "Firecrawl", "Full-page capture after candidate URLs are known"),
        ("6", "Specialists", "GitHub, docs, Drive, browser, Reddit tools"),
        ("7", "Generic Web", "Last fallback only; label limitations"),
    ]
    for i, (num, name, desc) in enumerate(order):
        x = 0.75 + (i % 4) * 3.05
        y = 1.82 + (i // 4) * 1.65
        card(d, s, x, y, 2.65, 1.08, name, desc, accent=b.TEAL if i < 3 else b.AMBER, idx=num, body_size=10.5)
    d.rect(s, d.M, Inches(5.55), d.CW, Inches(0.72), b.NAVY, radius=0.05)
    d.text(s, "Policy", Inches(0.9), Inches(5.78), Inches(0.7), Inches(0.16), size=10.5, color=b.GOLD, bold=True)
    d.text(s, "Generic WebSearch/search_web is last-resort only; label those outputs as fallback-sourced.", Inches(1.75), Inches(5.69), Inches(10.5), Inches(0.32), size=11.2, color=b.WHITE, shrink=True)
    d.footer(s, 5, total)

    # 6 You.com
    s = d.slide(fill=b.SOFT)
    d.header(s, "You.com Search Backend Spec", "You.com is the current-web layer; Exa/Firecrawl remain specialist routes.")
    specs = [
        ("Search API", "Default current-web grounding for agent loops; configure Hermes `web.search_backend: you`."),
        ("livecrawl", "One-shot full-page markdown retrieval when Hermes needs source content, not snippets."),
        ("Research API", "Offload exhaustive multi-query research into a cited report for deep dives."),
        ("Finance Research API", "Use for investor research, fundamentals, filings, macro/news, and finance-heavy workflows."),
        ("Freshness filters", "Day/week/month or date windows keep agent claims anchored to recency."),
        ("Domain/geo targeting", "Tighten account, region, and category research without bloated query hacks."),
    ]
    for i, (name, desc) in enumerate(specs):
        x = 0.7 + (i % 3) * 4.08
        y = 1.88 + (i // 3) * 1.65
        card(d, s, x, y, 3.55, 1.16, name, desc, accent=b.TEAL, body_size=10.8)
    d.rect(s, d.M, Inches(5.58), d.CW, Inches(0.68), b.NAVY, radius=0.05)
    d.text(s, "Implementation rule: store the key outside repo files and verify real URLs before wiring use cases.", Inches(0.92), Inches(5.75), Inches(11.45), Inches(0.28), size=11.4, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 6, total)

    # 7 GBrain
    s = d.slide(fill=b.SOFT)
    d.header(s, "GBrain Memory Spec", "Memory is a governed knowledge layer, not a pile of chat logs.")
    card(d, s, 0.75, 1.88, 2.85, 1.3, "Knowledge Graph", "Parse people, companies, projects, and relationships into connected entity notes.", accent=b.TEAL, idx="01")
    card(d, s, 3.9, 1.88, 2.85, 1.3, "Dream Cycle", "Background cleanup flags contradictions, duplicates, stale facts, and messy formatting.", accent=b.GOLD, idx="02")
    card(d, s, 7.05, 1.88, 2.85, 1.3, "Git-Backed Files", "Store memory in human-readable markdown that can be inspected, corrected, and reviewed.", accent=b.ACCENT, idx="03")
    card(d, s, 10.2, 1.88, 2.35, 1.3, "Token Discipline", "Use deterministic links where possible; reserve LLM work for higher-value synthesis.", accent=b.AMBER, idx="04", body_size=10.8)
    d.text(s, "Memory SOP", d.M, Inches(4.0), d.CW, Inches(0.3), size=16, color=b.NAVY, bold=True)
    d.text(s, bullets([
        "Recall before research for recurring people, companies, verticals, and prospects.",
        "Write back durable findings only when they will matter across sessions.",
        "Keep deliverables in repo/run files; GBrain is memory, not the system of record.",
        "Record provenance and source dates for enriched contacts/entities.",
    ], size=12.8), d.M, Inches(4.45), d.CW, Inches(1.2), size=12.8, color=b.INK, shrink=True)
    d.footer(s, 7, total)

    # 8 governance
    s = d.slide(fill=b.SOFT)
    d.header(s, "Governance: Autonomy Ladder", "Move from observe to draft to approval-gated action.")
    ladder = [
        ("Observe", "Read-only monitoring, briefs, scans", b.TEAL),
        ("Draft", "Prepare messages, notes, updates", b.ACCENT),
        ("Approve", "Human approves sends, publishes, config changes", b.GOLD),
        ("Execute", "Narrow autonomous actions with rollback", b.AMBER),
    ]
    for i, (name, desc, col) in enumerate(ladder):
        d.rect(s, Inches(0.95 + i * 3.05), Inches(2.0), Inches(2.45), Inches(1.18), col, radius=0.08, shadow=True)
        d.text(s, name, Inches(1.15 + i * 3.05), Inches(2.25), Inches(2.05), Inches(0.22), size=16, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, desc, Inches(1.12 + i * 3.05), Inches(2.7), Inches(2.1), Inches(0.26), size=10.2, color=b.NAVY, align=PP_ALIGN.CENTER, shrink=True)
        if i < 3:
            d.text(s, "→", Inches(3.48 + i * 3.05), Inches(2.38), Inches(0.32), Inches(0.2), size=16, color=b.MUTED, bold=True)
    d.rect(s, d.M, Inches(4.15), d.CW, Inches(1.3), b.WHITE, line=b.GRID, radius=0.08, shadow=True)
    d.text(s, "Approval-gated by default", Inches(0.92), Inches(4.42), Inches(2.4), Inches(0.26), size=15, color=b.NAVY, bold=True)
    d.text(s, "Publishing, investor emails, client messages, credential changes, file deletion, and config edits require explicit approval until rollback is tested.", Inches(3.25), Inches(4.34), Inches(8.95), Inches(0.5), size=11.8, color=b.INK, shrink=True)
    d.footer(s, 8, total)

    # 9 roadmap
    s = d.slide(fill=b.SOFT)
    d.header(s, "Implementation Roadmap", "Conservative sequencing reduces cost, permission, and trust risk.")
    phases = [
        ("Foundation", "Install Hermes, local setup, model provider, owner/host machine"),
        ("Search", "You.com backend, extraction fallback, key stored outside repo"),
        ("Memory", "GBrain install, Obsidian visibility, recall/write-back rules"),
        ("Controls", "Model routing, spend caps, credential inventory, audit cron"),
        ("Read-Only", "Daily brief, pre-call brief, signal monitor, contact reports"),
        ("Draft", "Investor hooks, content drafts, CRM updates, follow-ups"),
        ("Execute", "Approval-gated sends, publishes, external writes"),
        ("Improve", "Weekly QA, cron health, memory dreaming review, backlog"),
    ]
    for i, (name, desc) in enumerate(phases):
        x = 0.72 + (i % 4) * 3.08
        y = 1.82 + (i // 4) * 1.55
        card(d, s, x, y, 2.68, 1.08, name, desc, accent=b.TEAL if i < 4 else b.GOLD, idx=str(i + 1), body_size=10.4)
    d.footer(s, 9, total)

    # 10 matrix
    s = d.slide(fill=b.SOFT)
    d.header(s, "Use-Case Portfolio Matrix", "Start with high-value, lower-risk read-only or draft workflows.")
    d.rect(s, Inches(0.95), Inches(1.95), Inches(11.3), Inches(4.35), b.WHITE, line=b.GRID, radius=0.06, shadow=True)
    d.text(s, "Higher Value", Inches(0.95), Inches(1.58), Inches(1.4), Inches(0.2), size=10.5, color=b.NAVY, bold=True)
    d.text(s, "Higher Risk", Inches(11.0), Inches(6.38), Inches(1.0), Inches(0.2), size=10.5, color=b.NAVY, bold=True)
    d.rect(s, Inches(6.55), Inches(1.95), Inches(0.03), Inches(4.35), b.GRID)
    d.rect(s, Inches(0.95), Inches(4.12), Inches(11.3), Inches(0.03), b.GRID)
    points = [
        ("Daily brief", 2.0, 2.5, b.TEAL),
        ("Smart contacts", 4.0, 2.35, b.TEAL),
        ("Pre-call brief", 3.8, 3.25, b.ACCENT),
        ("Investor research", 5.8, 3.1, b.ACCENT),
        ("Signal monitor", 4.9, 4.9, b.GOLD),
        ("Content drafts", 6.9, 3.2, b.GOLD),
        ("App builder", 8.8, 4.35, b.AMBER),
        ("Auto-publish/sends", 9.7, 2.45, b.CORAL),
    ]
    for label, x, y, col in points:
        d.rect(s, Inches(x), Inches(y), Inches(1.35), Inches(0.42), col, radius=0.08, shadow=True)
        d.text(s, label, Inches(x + 0.08), Inches(y + 0.14), Inches(1.18), Inches(0.1), size=7.8, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "Recommended start zone", Inches(1.25), Inches(4.45), Inches(3), Inches(0.2), size=12, color=b.ACCENT, bold=True)
    d.text(s, "Read-only and draft-only routines create trust while proving the operating loop.", Inches(1.25), Inches(4.82), Inches(3.7), Inches(0.3), size=10.5, color=b.MUTED, shrink=True)
    d.footer(s, 10, total)

    use_case_slide(
        d, "Use Case 01: Daily Executive Brief", "Scheduled read-only intelligence layer.",
        "Executives lose time reconstructing priorities from inbox, calendar, chat, and meeting records.",
        "Hermes runs a morning/afternoon cron, recalls context from GBrain, searches only for fresh deltas, and emits a concise prioritized brief.",
        ["Trigger", "Recall", "Scan", "Rank", "Brief"],
        "Calendar + Inbox + Slack/Teams + Zoom + GBrain + You.com",
        "Calendar, email, chat, transcripts, memory",
        "No sends; cite source links; stale-source flag",
        11, total,
    )

    use_case_slide(
        d, "Use Case 02: Smart Contacts & Entities", "Relationship intelligence that stays fresh.",
        "CRM/contact data decays quickly, and important context is scattered across meetings, messages, social posts, and the public web.",
        "Hermes enriches people and organizations, writes durable entity notes to GBrain, and lets Obsidian expose relationship graph structure.",
        ["Ingest", "Enrich", "Link", "Store", "Surface"],
        "Email + Calendar + Zoom + LinkedIn/X + You.com Research + GBrain",
        "Contacts, calendar, public web, entity notes",
        "Provenance; source dates; no overwrite without review",
        12, total,
    )

    use_case_slide(
        d, "Use Case 03: Pre-Call & Investor Research", "Draft-only relationship preparation.",
        "Pre-call prep and investor outreach require repetitive research, thesis matching, prior investment review, and custom hooks.",
        "Hermes builds briefings, ranks fit, drafts hooks, and queues outreach for human review instead of sending automatically.",
        ["Event/List", "Recall", "Research", "Fit", "Draft"],
        "Calendar + GBrain + You.com/Finance Research + inbox + investor tracker",
        "Calendar, investor data, news, prior interactions",
        "Draft-only; user sends; low-confidence claims flagged",
        13, total,
    )

    use_case_slide(
        d, "Use Case 04: Signal & Content Pipeline", "Current-web sensing without living on feeds.",
        "Teams need market and social signal, but raw feeds are noisy and reactive.",
        "Hermes monitors web/news/social/creator clusters, ranks topic salience, performs deep research, and drafts content variants.",
        ["Watch", "Cluster", "Research", "Draft", "Review"],
        "YouTube + web/news + social + You.com Research + GBrain",
        "Creator transcripts, news, social signals, source pack",
        "Editorial approval; cite sources; no auto-publish",
        14, total,
    )

    use_case_slide(
        d, "Use Case 05: Cost, Model Health & Security", "The operating system must inspect itself.",
        "Autonomous loops can drift into expensive models, broken cron, stale credentials, or risky permissions.",
        "Hermes runs nightly health scans, reports model-route drift, itemizes spend, checks MCP/plugin health, and queues fixes.",
        ["Inspect", "Detect", "Rank", "Notify", "Approve"],
        "Hermes logs + API usage + config + cron + credential inventory",
        "Logs, cost data, model routes, plugin health",
        "Notify before risky fixes; no secret exposure",
        15, total,
    )

    use_case_slide(
        d, "Use Case 06: App Builder & Compaction", "Delegate implementation while preserving verification.",
        "Internal tools and knowledge cleanup sit in backlog because they require context loading, code writing, and verification.",
        "Hermes uses repo skills to build small tools, runs checks, and compacts notes/research into git-backed memory.",
        ["Prompt", "Plan", "Build", "Verify", "Write-back"],
        "Repo files + shell + browser checks + GBrain + Obsidian",
        "Codebase, run files, tests, memory graph",
        "Worktree isolation; tests; human review before merge",
        16, total,
    )

    # 17 SOP template
    s = d.slide(fill=b.SOFT)
    d.header(s, "Spec Template For Every Hermes Use Case", "Production-ready means each field is written and testable.")
    fields = [
        ("Trigger", "Cron, calendar event, user command, folder drop, API"),
        ("Inputs", "Systems, owners, credentials, freshness, sensitivity"),
        ("Source order", "GBrain → You.com → Exa → Firecrawl → specialists → fallback"),
        ("Output", "Named artifact path, format, owner, retention"),
        ("Autonomy", "Read-only, draft, approval-gated, autonomous"),
        ("Controls", "Model route, spend cap, approval gate, rollback"),
        ("Failures", "Stale source, blocked key, low confidence, runaway cost"),
        ("Verification", "Checks before live status and cadence after launch"),
    ]
    for i, (name, desc) in enumerate(fields):
        x = 0.72 + (i % 4) * 3.08
        y = 1.82 + (i // 4) * 1.52
        card(d, s, x, y, 2.68, 1.03, name, desc, accent=b.ACCENT, idx=str(i + 1), body_size=10.2)
    d.footer(s, 17, total)

    # 18 Chain QA
    s = d.slide(fill=b.SOFT)
    d.header(s, "Skill Chaining QA Gate", "The orchestrator must prove that skills compound.")
    d.rect(s, d.M, Inches(1.82), d.CW, Inches(1.0), b.NAVY, radius=0.06)
    d.text(s, "Chain Contract", Inches(0.9), Inches(2.08), Inches(1.7), Inches(0.22), size=15, color=b.GOLD, bold=True)
    d.text(s, "Skill/action → Consumes → Produces → Next consumer → Value test", Inches(2.8), Inches(2.02), Inches(8.8), Inches(0.32), size=13.2, color=b.WHITE, bold=True, shrink=True)
    statuses = [
        ("compound", "Output is ready for the next consumer and advances acceptance criteria.", b.TEAL),
        ("isolated", "Skill completed but produced no useful handoff.", b.AMBER),
        ("duplicate", "Repeats prior work without material improvement.", b.AMBER),
        ("blocked", "Cannot produce the required handoff.", b.CORAL),
        ("reroute", "Wrong skill for the phase; revise the chain.", b.GOLD),
    ]
    for i, (name, desc, col) in enumerate(statuses):
        x = 0.72 + (i % 3) * 4.08
        y = 3.35 + (i // 3) * 1.25
        card(d, s, x, y, 3.55, 0.88, name, desc, accent=col, body_size=9.8)
    d.footer(s, 18, total)

    # 19 30-day rollout
    s = d.slide(fill=b.SOFT)
    d.header(s, "30-Day Rollout Plan", "From install to governed use-case backlog.")
    weeks = [
        ("Week 1", "Install Hermes; configure model provider; wire You.com; inventory credentials; choose host machine."),
        ("Week 2", "Install GBrain; create entity schema; configure Obsidian; run recall/write-back smoke tests."),
        ("Week 3", "Launch read-only briefs, contact enrichment reports, signal monitor, and nightly cost/model scan."),
        ("Week 4", "Promote top workflows to draft mode; add approval queues; establish weekly QA and backlog review."),
    ]
    for i, (wk, body) in enumerate(weeks):
        card(d, s, 0.78 + i * 3.05, 2.02, 2.58, 2.35, wk, body, accent=b.TEAL if i < 2 else b.GOLD, idx=str(i + 1), body_size=11.2)
    d.rect(s, d.M, Inches(5.25), d.CW, Inches(0.72), b.NAVY, radius=0.05)
    d.text(s, "Exit criterion: three live routines with source tieout, approval gates, and weekly operating cadence.", Inches(0.9), Inches(5.43), Inches(11.5), Inches(0.28), size=11.5, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 19, total)

    # 20 decision
    s = d.slide(fill=b.NAVY)
    add_kicker(d, s, "Decision and next actions", top=0.72)
    d.text(s, "Approve The Hermes SOP Pilot", d.M, Inches(1.28), Inches(8.0), Inches(1.25), size=32, color=b.WHITE, bold=True, shrink=True)
    d.text(s, "Start with low-risk read-only and draft workflows. Expand only after spec, chain QA, and verification gates pass.", d.M, Inches(2.38), Inches(8.7), Inches(0.58), size=15, color=b.LIGHT_TEAL, shrink=True)
    asks = [
        ("Select 3 pilot use cases", "Daily brief, smart contacts, and pre-call/investor research are the recommended first lane."),
        ("Confirm credentials", "Approve only the minimum data sources required for those use cases."),
        ("Set approval policy", "Define which actions are draft-only versus externally executable."),
        ("Schedule week-1 build", "Install, wire You.com, verify search, and create the first runbook."),
    ]
    for i, (title, body) in enumerate(asks):
        x = 0.75 + (i % 2) * 5.95
        y = 3.45 + (i // 2) * 1.25
        d.rect(s, Inches(x), Inches(y), Inches(5.35), Inches(0.9), b.NAVY_2, line=b.TEAL, radius=0.07)
        d.text(s, title, Inches(x + 0.25), Inches(y + 0.17), Inches(2.1), Inches(0.18), size=12.5, color=b.GOLD, bold=True, shrink=True)
        d.text(s, body, Inches(x + 2.55), Inches(y + 0.15), Inches(2.45), Inches(0.32), size=10.5, color=b.WHITE, shrink=True)
    d.footer(s, 20, total, dark=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    d.save(OUT)
    try:
        DESKTOP.write_bytes(OUT.read_bytes())
        print(f"Copied to {DESKTOP}")
    except OSError as exc:
        alt = DESKTOP.with_name("Hermes_Use_Cases_Realization_SOP-reviewed-v2.pptx")
        try:
            alt.write_bytes(OUT.read_bytes())
            print(f"Desktop target unavailable ({exc}); copied to {alt}")
        except OSError as exc2:
            print(f"Desktop copy skipped ({exc2}); local reviewed deck is {OUT}")


if __name__ == "__main__":
    build()
