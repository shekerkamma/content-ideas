#!/usr/bin/env python3
"""Corrected full pipeline deck — all 17 grill-session findings applied.

Changes from original:
- Category A (buildable) vs Category B (benchmark) split
- OpenHands API corrected: Agent(llm, tools), MCP at platform level
- MCP servers: verified vs to-build honest split
- machina-ai removed (doesn't exist)
- Competitive landscape updated with 2026 research data
- Template variables resolved (brand_name = "AI Market Research")
- Slide 99 structural bug fixed (UC-10 under Section 03)
- Slide 110 external references fixed
- UC-05 metrics softened to "projected"
- Per-industry taglines
"""
from __future__ import annotations

import sys
from pathlib import Path

BRANDED_SKILL = Path("/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(BRANDED_SKILL))

from pptxkit import Deck, Inches, PP_ALIGN, MSO_ANCHOR  # type: ignore

RUN_DIR = Path(__file__).resolve().parent
OUT = RUN_DIR / "uc4-full-pipeline-corrected-draft.pptx"

BRAND = "AI Market Research"

# ── Helpers ─────────────────────────────────────────────────────────────────

def _footer(d, s, page, total, dark=False):
    d.footer(s, page, total, dark=dark)


def _header(d, title, subtitle):
    s = d.slide(fill=d.b.WHITE)
    d.rect(s, 0, 0, d.W, Inches(0.16), d.b.TEAL)
    d.text(s, title, d.M, Inches(0.42), d.CW, Inches(0.86), size=19, color=d.b.NAVY, bold=True, shrink=True)
    d.rect(s, d.M, Inches(1.18), Inches(1.45), Inches(0.05), d.b.TEAL)
    d.text(s, subtitle, d.M, Inches(1.36), d.CW, Inches(0.26), size=10.8, color=d.b.MUTED, shrink=True)
    return s


def _section(d, num, name, ucs, tagline, page, total):
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.12), d.b.TEAL)
    d.text(s, f"SECTION {num:02d}", d.M, Inches(2.0), d.CW, Inches(0.4),
           size=14, color=d.b.TEAL, bold=True)
    d.text(s, name, d.M, Inches(2.45), d.CW, Inches(0.9),
           size=36, color=d.b.WHITE, bold=True, shrink=True)
    d.text(s, ucs, d.M, Inches(3.4), d.CW, Inches(0.3),
           size=14, color=d.b.GOLD, bold=True)
    d.rect(s, d.M, Inches(3.9), Inches(4), Inches(0.04), d.b.TEAL)
    d.text(s, tagline, d.M, Inches(4.1), d.CW, Inches(0.4),
           size=12, color=d.b.LIGHT_TEAL, shrink=True)
    d.text(s, f"{BRAND} · AI Use Cases — Full Pipeline | 2026",
           d.M, Inches(6.8), d.CW, Inches(0.3), size=9, color=d.b.MUTED, shrink=True)
    _footer(d, s, page, total, dark=True)
    return s


# ── Category A slide builders (buildable UCs: full 10-slide set) ────────────

def cat_a_title(d, uc, page, total):
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.12), d.b.TEAL)
    d.text(s, uc["kicker"], d.M, Inches(1.5), d.CW, Inches(0.3), size=12, color=d.b.TEAL, bold=True)
    d.text(s, uc["title"], d.M, Inches(1.85), d.CW, Inches(0.8), size=28, color=d.b.WHITE, bold=True, shrink=True)
    d.text(s, uc["headline_stat"], d.M, Inches(2.75), d.CW, Inches(0.3), size=14, color=d.b.GOLD, bold=True, shrink=True)
    d.text(s, uc["company_line"], d.M, Inches(3.2), d.CW, Inches(0.3), size=11, color=d.b.LIGHT_TEAL, shrink=True)
    d.rect(s, d.M, Inches(3.7), Inches(2.2), Inches(0.32), d.b.TEAL, radius=0.04)
    d.text(s, f"VERTICAL SCORE: {uc['score']}", d.M + Inches(0.15), Inches(3.7),
           Inches(1.9), Inches(0.32), size=10, color=d.b.WHITE, bold=True,
           anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, f"Source: {uc['source']}", d.M, Inches(4.3), d.CW, Inches(0.3),
           size=9, color=d.b.MUTED, shrink=True)
    _footer(d, s, page, total, dark=True)


def cat_a_problem(d, uc, page, total):
    s = _header(d, uc["problem_title"], f"{uc['kicker']} — The Problem")
    for i, pt in enumerate(uc["problems"]):
        y = Inches(1.75) + i * Inches(0.72)
        d.rect(s, d.M, y, Inches(0.42), Inches(0.42), d.b.TEAL, radius=0.04)
        d.text(s, f"{i+1:02d}", d.M + Inches(0.06), y, Inches(0.3), Inches(0.42),
               size=14, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        d.text(s, pt, d.M + Inches(0.56), y + Inches(0.06), d.CW - Inches(0.7), Inches(0.36),
               size=11, color=d.b.INK, shrink=True)
    _footer(d, s, page, total)


def cat_a_realized(d, uc, page, total):
    s = _header(d, uc["realized_title"], f"{uc['kicker']} — How It's Realized")
    for i, pt in enumerate(uc["realized"]):
        y = Inches(1.75) + i * Inches(0.72)
        d.rect(s, d.M, y, Inches(0.42), Inches(0.42), d.b.GOLD, radius=0.04)
        d.text(s, f"{i+1:02d}", d.M + Inches(0.06), y, Inches(0.3), Inches(0.42),
               size=14, color=d.b.NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        d.text(s, pt, d.M + Inches(0.56), y + Inches(0.06), d.CW - Inches(0.7), Inches(0.36),
               size=11, color=d.b.INK, shrink=True)
    _footer(d, s, page, total)


def cat_a_metrics(d, uc, page, total):
    s = _header(d, f"KEY METRICS — {uc['kicker']}", "")
    stats = uc["stats"]
    cols = min(len(stats), 3)
    rows = (len(stats) + cols - 1) // cols
    gap = Inches(0.22)
    card_w = (d.CW - gap * (cols - 1)) / cols
    card_h = Inches(1.2)
    for i, (num, label, detail) in enumerate(stats):
        r, c = divmod(i, cols)
        x = d.M + c * (card_w + gap)
        y = Inches(1.65) + r * (card_h + Inches(0.18))
        d.rect(s, x, y, card_w, card_h, d.b.NAVY, radius=0.06, shadow=True)
        d.text(s, num, x + Inches(0.15), y + Inches(0.12), card_w - Inches(0.3), Inches(0.4),
               size=28, color=d.b.TEAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, label, x + Inches(0.15), y + Inches(0.55), card_w - Inches(0.3), Inches(0.22),
               size=11, color=d.b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, detail, x + Inches(0.15), y + Inches(0.8), card_w - Inches(0.3), Inches(0.28),
               size=8.5, color=d.b.LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)
    _footer(d, s, page, total)


def cat_a_how(d, uc, page, total):
    s = _header(d, f"HOW IT WORKS — {uc['kicker']}", "")
    steps = uc["how_steps"]
    for i, step in enumerate(steps):
        y = Inches(1.65) + i * Inches(0.72)
        d.rect(s, d.M, y, d.CW, Inches(0.58), d.b.SOFT if i % 2 == 0 else d.b.WHITE, radius=0.04)
        d.text(s, f"STEP {i+1}", d.M + Inches(0.15), y + Inches(0.06), Inches(0.8), Inches(0.2),
               size=9, color=d.b.TEAL, bold=True)
        d.text(s, step, d.M + Inches(0.15), y + Inches(0.26), d.CW - Inches(0.3), Inches(0.26),
               size=10, color=d.b.INK, shrink=True)
        if i < len(steps) - 1:
            d.text(s, "↓", d.M + d.CW / 2 - Inches(0.1), y + Inches(0.58), Inches(0.2), Inches(0.14),
                   size=10, color=d.b.TEAL, bold=True, align=PP_ALIGN.CENTER)
    _footer(d, s, page, total)


def cat_a_architecture(d, uc, page, total):
    """Corrected architecture slide — honest API, MCP split."""
    s = d.slide(fill=d.b.WHITE)
    d.rect(s, 0, 0, d.W, Inches(0.12), d.b.TEAL)
    d.text(s, f"ARCHITECTURE — {uc['kicker']}", d.M, Inches(0.28), d.CW, Inches(0.3),
           size=12, color=d.b.MUTED, bold=True)
    d.text(s, uc["arch_title"], d.M, Inches(0.6), d.CW, Inches(0.5),
           size=20, color=d.b.NAVY, bold=True, shrink=True)

    # Agent stack
    agent_w = Inches(5.5)
    d.rect(s, d.M, Inches(1.25), agent_w, Inches(2.8), d.b.NAVY, radius=0.06, shadow=True)
    d.text(s, "AGENT STACK", d.M + Inches(0.2), Inches(1.4), Inches(2), Inches(0.22),
           size=11, color=d.b.GOLD, bold=True)
    ay = Inches(1.7)
    for name, desc in uc["agents"]:
        d.text(s, name, d.M + Inches(0.2), ay, agent_w - Inches(0.4), Inches(0.22),
               size=10.5, color=d.b.TEAL, bold=True, shrink=True)
        d.text(s, desc, d.M + Inches(0.2), ay + Inches(0.2), agent_w - Inches(0.4), Inches(0.35),
               size=8.5, color=d.b.WHITE, shrink=True, ls=1.0)
        ay += Inches(0.6)

    # MCP servers
    mcp_x = d.M + agent_w + Inches(0.25)
    mcp_w = d.CW - agent_w - Inches(0.25)
    d.rect(s, mcp_x, Inches(1.25), mcp_w, Inches(2.8), d.b.SOFT, radius=0.06, shadow=True)
    d.text(s, "MCP SERVERS", mcp_x + Inches(0.2), Inches(1.4), mcp_w - Inches(0.4), Inches(0.22),
           size=11, color=d.b.NAVY, bold=True)
    my = Inches(1.7)
    for name, endpoints, status in uc["mcp_servers"]:
        color = d.b.TEAL if status == "verified" else d.b.AMBER
        tag = "VERIFIED" if status == "verified" else "TO BUILD"
        d.text(s, f"{name}  [{tag}]", mcp_x + Inches(0.2), my, mcp_w - Inches(0.4), Inches(0.2),
               size=9.5, color=color, bold=True, shrink=True)
        d.text(s, endpoints, mcp_x + Inches(0.2), my + Inches(0.18), mcp_w - Inches(0.4), Inches(0.32),
               size=8, color=d.b.INK, shrink=True, ls=1.0)
        my += Inches(0.55)

    # Deployment + corrected pattern
    d.rect(s, d.M, Inches(4.2), d.CW, Inches(0.75), d.b.TEAL, radius=0.05)
    d.text(s, "DEPLOYMENT", d.M + Inches(0.2), Inches(4.3), Inches(1.5), Inches(0.2),
           size=10, color=d.b.NAVY, bold=True)
    d.text(s, uc["deployment"], d.M + Inches(1.8), Inches(4.3), d.CW - Inches(2.0), Inches(0.2),
           size=9, color=d.b.WHITE, shrink=True)
    d.text(s, "Pattern: Agent(llm, tools) → Conversation(agent, workspace, plugins) | MCP config at platform level (config.toml)",
           d.M + Inches(0.2), Inches(4.6), d.CW - Inches(0.4), Inches(0.2),
           size=8.5, color=d.b.NAVY, bold=True, shrink=True)

    # Tech stack + GitHub
    d.rect(s, d.M, Inches(5.1), d.CW, Inches(1.4), d.b.NAVY, radius=0.05)
    d.text(s, "TECH STACK & GITHUB", d.M + Inches(0.2), Inches(5.2), Inches(3), Inches(0.2),
           size=11, color=d.b.GOLD, bold=True)
    gy = Inches(5.45)
    repos_per_row = 3
    repo_w = (d.CW - Inches(0.8)) / repos_per_row
    for i, (repo, desc) in enumerate(uc["github_repos"]):
        r, c = divmod(i, repos_per_row)
        gx = d.M + Inches(0.2) + c * repo_w
        gy2 = Inches(5.45) + r * Inches(0.48)
        d.text(s, repo, gx, gy2, repo_w - Inches(0.1), Inches(0.18),
               size=8.5, color=d.b.TEAL, bold=True, shrink=True)
        d.text(s, desc, gx, gy2 + Inches(0.16), repo_w - Inches(0.1), Inches(0.24),
               size=7.5, color=d.b.WHITE, shrink=True)

    # Systems + users bar
    by = Inches(6.65)
    bw = (d.CW - Inches(0.2)) / 2
    d.rect(s, d.M, by, bw, Inches(0.3), d.b.ACCENT, radius=0.03)
    d.text(s, f"SYSTEMS: {uc['systems']}", d.M + Inches(0.1), by, bw - Inches(0.2), Inches(0.3),
           size=7, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.rect(s, d.M + bw + Inches(0.2), by, bw, Inches(0.3), d.b.DARK_TEAL, radius=0.03)
    d.text(s, f"USERS: {uc['users']}", d.M + bw + Inches(0.3), by, bw - Inches(0.2), Inches(0.3),
           size=7, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    _footer(d, s, page, total)


def cat_a_governance(d, uc, page, total):
    s = _header(d, f"Governance & Compliance — {uc['uc_id']}", f"{uc['industry']} — Standards, audits, and compliance requirements")
    for i, item in enumerate(uc["governance"]):
        y = Inches(1.75) + i * Inches(0.58)
        d.text(s, f"✓  {item}", d.M, y, d.CW, Inches(0.44), size=11, color=d.b.INK, shrink=True)
    _footer(d, s, page, total)


def cat_a_competitive(d, uc, page, total):
    s = _header(d, f"COMPETITIVE LANDSCAPE — {uc['kicker']}", "")
    comps = uc["competitors"]
    card_h = Inches(0.85)
    for i, (name, price, desc) in enumerate(comps):
        y = Inches(1.65) + i * (card_h + Inches(0.12))
        is_ours = "our" in name.lower()
        bg = d.b.TEAL if is_ours else d.b.SOFT
        tc = d.b.WHITE if is_ours else d.b.INK
        d.rect(s, d.M, y, d.CW, card_h, bg, radius=0.05)
        d.text(s, name, d.M + Inches(0.2), y + Inches(0.12), Inches(3), Inches(0.24),
               size=13, color=d.b.NAVY if not is_ours else d.b.WHITE, bold=True, shrink=True)
        d.text(s, price, d.M + Inches(3.5), y + Inches(0.12), Inches(2.5), Inches(0.24),
               size=10, color=d.b.MUTED if not is_ours else d.b.GOLD, bold=True, shrink=True)
        d.text(s, desc, d.M + Inches(0.2), y + Inches(0.42), d.CW - Inches(0.4), Inches(0.3),
               size=9.5, color=tc, shrink=True)
    _footer(d, s, page, total)


def cat_a_insight(d, uc, page, total):
    s = d.slide(fill=d.b.WHITE)
    d.rect(s, 0, 0, d.W, Inches(0.12), d.b.GOLD)
    d.text(s, f"THE ACTUAL INSIGHT — {uc['uc_id']}", d.M, Inches(0.4), d.CW, Inches(0.3),
           size=12, color=d.b.MUTED, bold=True)
    d.rect(s, d.M, Inches(0.9), d.CW, Inches(2.8), d.b.NAVY, radius=0.06, shadow=True)
    d.text(s, uc["insight"], d.M + Inches(0.3), Inches(1.1), d.CW - Inches(0.6), Inches(2.4),
           size=14, color=d.b.WHITE, shrink=True, ls=1.15)

    # Buyer + Revenue + Deployment cards
    card_y = Inches(4.0)
    card_w = (d.CW - Inches(0.4)) / 3
    for i, (label, val) in enumerate([("BUYER", uc["buyer"]), ("REVENUE MODEL", uc["revenue"]), ("DEPLOYMENT", uc["deploy_mode"])]):
        x = d.M + i * (card_w + Inches(0.2))
        d.rect(s, x, card_y, card_w, Inches(1.1), d.b.SOFT, radius=0.05)
        d.text(s, label, x + Inches(0.15), card_y + Inches(0.12), card_w - Inches(0.3), Inches(0.2),
               size=10, color=d.b.TEAL, bold=True)
        d.text(s, val, x + Inches(0.15), card_y + Inches(0.38), card_w - Inches(0.3), Inches(0.58),
               size=10.5, color=d.b.INK, shrink=True)

    d.text(s, f"Source: {uc['source']}", d.M, Inches(5.4), d.CW, Inches(0.2),
           size=9, color=d.b.MUTED, shrink=True)
    _footer(d, s, page, total)


# ── Category B slide builders (benchmark UCs: 6-slide set) ──────────────────

def cat_b_title(d, uc, page, total):
    cat_a_title(d, uc, page, total)  # same layout


def cat_b_problem(d, uc, page, total):
    cat_a_problem(d, uc, page, total)  # same layout


def cat_b_how_they_did_it(d, uc, page, total):
    s = _header(d, uc["realized_title"], f"{uc['kicker']} — How They Solved It")
    d.rect(s, d.M, Inches(1.6), Inches(1.8), Inches(0.28), d.b.CORAL, radius=0.04)
    d.text(s, "THEIR PROPRIETARY STACK", d.M + Inches(0.15), Inches(1.6),
           Inches(1.5), Inches(0.28), size=8.5, color=d.b.WHITE, bold=True,
           anchor=MSO_ANCHOR.MIDDLE)
    for i, pt in enumerate(uc["realized"]):
        y = Inches(2.05) + i * Inches(0.72)
        d.rect(s, d.M, y, Inches(0.42), Inches(0.42), d.b.GOLD, radius=0.04)
        d.text(s, f"{i+1:02d}", d.M + Inches(0.06), y, Inches(0.3), Inches(0.42),
               size=14, color=d.b.NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        d.text(s, pt, d.M + Inches(0.56), y + Inches(0.06), d.CW - Inches(0.7), Inches(0.36),
               size=11, color=d.b.INK, shrink=True)
    _footer(d, s, page, total)


def cat_b_metrics(d, uc, page, total):
    cat_a_metrics(d, uc, page, total)  # same layout


def cat_b_how_wed_build_it(d, uc, page, total):
    """Our replication architecture — honest about what exists vs what we'd build."""
    s = _header(d, f"How We'd Build It — {uc['kicker']}", "Our OpenHands + MCP replication of the same outcome")
    d.rect(s, d.M, Inches(1.6), Inches(2.2), Inches(0.28), d.b.TEAL, radius=0.04)
    d.text(s, "OUR OPEN ARCHITECTURE", d.M + Inches(0.15), Inches(1.6),
           Inches(1.9), Inches(0.28), size=8.5, color=d.b.WHITE, bold=True,
           anchor=MSO_ANCHOR.MIDDLE)

    # Agent stack
    ay = Inches(2.05)
    d.text(s, "AGENT STACK", d.M, ay, Inches(2), Inches(0.2), size=10, color=d.b.NAVY, bold=True)
    ay += Inches(0.25)
    for name, desc in uc.get("our_agents", []):
        d.text(s, f"  {name}", d.M, ay, Inches(3), Inches(0.18), size=9, color=d.b.TEAL, bold=True, shrink=True)
        d.text(s, f"    {desc}", d.M, ay + Inches(0.16), d.CW * 0.5, Inches(0.22), size=8.5, color=d.b.INK, shrink=True)
        ay += Inches(0.4)

    # MCP servers
    mx = d.CW * 0.5 + d.M + Inches(0.2)
    mw = d.CW * 0.5 - Inches(0.2)
    my = Inches(2.05)
    d.text(s, "MCP SERVERS", mx, my, mw, Inches(0.2), size=10, color=d.b.NAVY, bold=True)
    my += Inches(0.25)
    for name, status in uc.get("our_mcp", []):
        color = d.b.TEAL if status == "verified" else d.b.AMBER
        tag = "VERIFIED" if status == "verified" else "TO BUILD"
        d.text(s, f"  {name}  [{tag}]", mx, my, mw, Inches(0.2), size=9, color=color, bold=True, shrink=True)
        my += Inches(0.25)

    # Key difference callout
    d.rect(s, d.M, Inches(4.8), d.CW, Inches(0.85), d.b.GOLD, radius=0.05)
    d.text(s, "KEY DIFFERENCE", d.M + Inches(0.2), Inches(4.9), Inches(2), Inches(0.2),
           size=11, color=d.b.NAVY, bold=True)
    d.text(s, uc.get("key_difference", "Open architecture, composable agents, platform-level MCP — not locked to one vendor."),
           d.M + Inches(0.2), Inches(5.15), d.CW - Inches(0.4), Inches(0.35),
           size=10, color=d.b.NAVY, shrink=True)

    d.text(s, "Pattern: Agent(llm, tools) → Conversation(agent, workspace, plugins) | MCP config at platform level",
           d.M, Inches(5.85), d.CW, Inches(0.2), size=8.5, color=d.b.MUTED, shrink=True)
    _footer(d, s, page, total)


def cat_b_competitive(d, uc, page, total):
    cat_a_competitive(d, uc, page, total)  # same layout


# ── USE CASE DATA ───────────────────────────────────────────────────────────

# Category A UCs
UC01 = {
    "kicker": "UC-01 | MANUFACTURING", "uc_id": "UC-01", "industry": "Manufacturing",
    "title": "Predictive Maintenance — Sensor → Anomaly → Work Order",
    "headline_stat": "Unilever Indaiatuba: $2.3M saved, 92% accuracy, 6.5-month payback",
    "company_line": "Unilever (Brazil)  |  2023, expanded to 7+ sites by Q4 2025",
    "score": "32/35 GO", "source": "NSSG Insights Mar 2026 + Unilever case study",
    "problem_title": "Equipment Downtime Costs $50K-$250K/Hour",
    "problems": [
        "Equipment downtime costs $50K-$250K/hour in manufacturing plants",
        "Calendar-based maintenance wastes 30%+ of budget on unnecessary interventions",
        "Unilever baseline: 8.2% unplanned downtime, $5.1M annual maintenance spend",
        "Technician trust in AI predictions is the real deployment barrier — not model accuracy",
        "50,000+ IoT sensors generating time-series data across compressors, HVAC, packaging",
        "3 years of historical failure data needed before any model could train",
    ],
    "realized_title": "52-Endpoint MCP Server + SAP PM Integration",
    "realized": [
        "50K+ IoT sensors → anomaly detection 14-28 days before failure at 92% accuracy",
        "52-endpoint MCP server: FFT, envelope analysis, RUL estimation (ISO 13374)",
        "Auto-generates SAP PM work orders with equipment ID, failure type, predicted date",
        "6-month trust-building phase with technician feedback loops before full reliance",
        "Started with 12 machines causing 80% of downtime — focused deployment",
        "Amazon SageMaker processes time-series data; ONNX Runtime for edge inference",
    ],
    "stats": [
        ("$2.3M", "Annual Savings", "45% reduction from $5.1M baseline"),
        ("92%", "Detection Accuracy", "14-28 days before predicted failure"),
        ("52", "MCP Endpoints", "ISO 13374 six-block diagnostic architecture"),
        ("6.5 mo", "Payback Period", "$1.2M investment recovered"),
        ("40%", "Downtime Reduction", "8.2% → 4.9% unplanned downtime"),
        ("85%+", "OEE Achieved", "Highest in Unilever global network"),
    ],
    "how_steps": [
        "Sensor reading arrives (MQTT/OPC-UA) → load_signal + analyze_spectrum + extract_features",
        "detect_anomalies (semi-supervised, trained on 3yr baseline) → anomaly_score",
        "IF anomaly_score > threshold → analyze_envelope (bearing-specific: BPFO/BPFI/BSF/FTF)",
        "assess_severity (ISO 20816-3 zone A/B/C/D) → estimate_rul (Weibull)",
        "IF severity >= Zone C OR rul_days < 14 → generate_report → create_work_order (SAP PM OData)",
        "Work order: equipment_id, failure_type, predicted_date, priority, recommended_ops",
        "Technician completes → feedback loop → model retraining on actual vs predicted",
    ],
    "arch_title": "Predictive Maintenance Agent Architecture",
    "agents": [
        ("sensor-fusion-agent", "Ingests multi-signal data (vibration, temp, pressure) from MQTT/OPC-UA gateway"),
        ("anomaly-detection-agent", "ML inference (XGBoost + LSTM) + ISO 20816-3 severity classification"),
        ("explainability-agent", "SHAP-based root-cause analysis → human-readable failure narratives"),
        ("sap-pm-agent", "Creates SAP PM work orders via OData: equipment_id, order_type, priority"),
    ],
    "mcp_servers": [
        ("predictive-maintenance-mcp (52 endpoints)", "load_signal, analyze_spectrum, detect_anomalies, assess_severity, estimate_rul, generate_report", "verified"),
        ("mcp-maintenance-cap (SAP Community PoC)", "get_maintenance_orders, create_work_order, get_equipment_history — OData → SAP S/4HANA PM", "to_build"),
    ],
    "deployment": "Headless batch: sensor analysis + work orders | Interactive: operator CLI queries",
    "github_repos": [
        ("LGDiMaggio/predictive-maintenance-mcp", "v0.8.0 — 52 endpoints, ISO 13374"),
        ("bernardcaldas/mcp-maintenance-cap", "SAP CAP PoC — PM work orders"),
        ("All-Hands-AI/OpenHands", "Agent SDK — headless mode + MCP config"),
        ("huggingface/transformers", "Time-series anomaly detection models"),
    ],
    "systems": "SCADA/OPC-UA | SAP PM | IoT Gateway | CMMS | Historian",
    "users": "Maintenance technicians | Plant engineers | Reliability managers",
    "governance": [
        "ISO 13374 six-block diagnostic architecture (acquisition → processing → detection → severity → prognostics → decision)",
        "ISO 20816-3 vibration severity classification (Zone A/B/C/D thresholds)",
        "Sensor calibration audit per ISO 6789 — annual recertification required",
        "Model drift monitoring: weekly accuracy check against actuals",
        "Technician override logging: all manual overrides of AI predictions tracked",
    ],
    "competitors": [
        ("Sight Machine", "$100K+/yr SaaS", "Manufacturing analytics platform — broad but expensive, no SAP integration"),
        ("Uptake", "$100K+/yr SaaS", "Asset performance management — enterprise pricing, long deployments"),
        ("Siemens Senseye", "Cloud PdM", "Gen-AI-enhanced failure prediction (Dec 2025) — cloud-based, production-grade"),
        ("Bosch AI", "50 plants", "2,000+ production lines interconnected; opening AI platform to externals (CES 2026)"),
        ("Our approach", "4 weeks, 50-70% cheaper", "Open-source MCP, pilot-first, technician trust-building baked in"),
    ],
    "insight": "3 years of labeled failure data eliminated the data-collection phase that kills most manufacturing AI. Started with 12 machines causing 80% of downtime. The model was technically ready before the humans were. Trust took 6 months to build. Budget for trust, not just training.",
    "buyer": "VP Manufacturing / Plant Manager",
    "revenue": "$5-10K/mo per plant",
    "deploy_mode": "Headless batch: openhands --headless",
}

UC02 = {
    "kicker": "UC-02 | MANUFACTURING", "uc_id": "UC-02", "industry": "Manufacturing",
    "title": "Visual Quality Inspection — Camera → CNN → SAP MES",
    "headline_stat": "YOLOv8 at line speed: 99.2% accuracy, 85% false positive reduction",
    "company_line": "Hyundai Framework + Multi-Plant  |  Reference architecture, 4-6 week deployment",
    "score": "32/35 GO", "source": "GBrain impl spec UC-MFG-02 + Hyundai framework",
    "problem_title": "Manual Inspection Fails at Scale",
    "problems": [
        "15-20% false positive rate in manual inspection across production lines",
        "Inspector fatigue: accuracy drops to 72% by hour 6 of shift",
        "$2.3M average annual quality cost per plant from missed defects",
        "Inconsistent criteria across shifts — 3 inspectors, 3 different standards",
        "Generic CV doesn't understand defect taxonomy per manufacturing context",
        "Edge inference latency must be <5ms to keep up with line speed (120 units/hr)",
    ],
    "realized_title": "Edge AI + Active Learning + SAP MES Integration",
    "realized": [
        "YOLOv8 real-time defect detection: 640x640 input, 1.2ms edge inference on Jetson Orin",
        "Multi-camera 360 inspection at line speed (120 units/hr) — no throughput reduction",
        "Three-tier confidence routing: >0.85 auto-reject; 0.5-0.85 operator review; <0.5 passes",
        "Active learning pipeline: operator corrections feed continuous model retraining",
        "Defect taxonomy: surface (scratch/dent/pit/crack), dimensional, contamination, assembly",
        "Per-shift quality reports auto-generated with SPC dashboard + Cpk monitoring",
    ],
    "stats": [
        ("99.2%", "Detection Accuracy", "Across all defect categories"),
        ("85%", "FP Reduction", "From 15-20% manual FP rate"),
        ("$1.8M", "Annual Savings", "Per plant from reduced quality costs"),
        ("<2ms", "Inference Time", "YOLOv8 on Jetson Orin NX edge GPU"),
        ("4-6 wk", "Deployment", "Camera install → model trained → production"),
        ("120/hr", "Line Speed", "No throughput reduction from inspection"),
    ],
    "how_steps": [
        "GigE Vision camera captures part → Image preprocessing (normalize, resize 640x640)",
        "Jetson Orin NX runs YOLOv8 inference (<2ms) → Defect classification",
        "Bounding box + confidence score → Three-tier routing decision",
        "IF confidence > 0.85 AND defect: auto-reject → log_inspection_result (SAP MES)",
        "IF 0.5-0.85: operator review → operator decision feeds active learning pipeline",
        "Per-shift aggregate → generate_quality_report → SPC dashboard (Cpk monitoring)",
        "Continuous: new labeled defects feed model retraining → OTA update to edge devices",
    ],
    "arch_title": "Visual Quality Inspection Agent Architecture",
    "agents": [
        ("vision-capture-agent", "GigE Vision camera control, image preprocessing, multi-camera sync"),
        ("inference-agent", "YOLOv8 / EfficientDet CNN → defect classification with confidence scores"),
        ("quality-routing-agent", "Routes by confidence: auto-reject, human review, or pass"),
        ("sap-mes-agent", "Logs results to SAP MES, creates quality notifications"),
    ],
    "mcp_servers": [
        ("vision-pipeline MCP (5 endpoints)", "capture_image, run_inference, classify_defect, get_defect_history, generate_quality_report", "to_build"),
        ("sap-mes MCP (OData) (4 endpoints)", "log_inspection_result, get_production_order, update_quality_status, create_quality_notification", "to_build"),
    ],
    "deployment": "Edge: Jetson Orin NX per station | Line-speed 120/hr | OTA model updates",
    "github_repos": [
        ("ultralytics/ultralytics", "YOLOv8 — real-time detection, ONNX export"),
        ("opencv/opencv", "Camera capture, preprocessing, GigE Vision"),
        ("NVIDIA/TensorRT", "Edge inference optimization for Jetson"),
        ("minio/minio", "S3-compatible defect image storage"),
    ],
    "systems": "SAP MES | GigE Vision | Jetson Orin | MinIO | SPC Dashboard",
    "users": "Quality engineers | Line supervisors | Plant managers",
    "governance": [
        "IEC 62443 industrial cybersecurity for connected inspection stations",
        "Image retention: 7 years minimum, AES-256 encrypted storage (MinIO)",
        "Edge device certificate rotation every 90 days (automated via PKI)",
        "Model version tracking: every deployment logged with accuracy metrics",
        "Operator override audit trail: all manual decisions vs AI recommendations tracked",
    ],
    "competitors": [
        ("Instrumental", "YC W14", "SaaS visual inspection — broad but less customizable"),
        ("Landing AI", "Andrew Ng", "Data-centric AI for manufacturing — high-touch, expensive consulting"),
        ("BMW AIQX", "All BMW plants", "95-99% accuracy, 50% inspection time cut, 60% defect reduction — deployed worldwide"),
        ("Cognex", "Machine vision HW", "Hardware-first, limited AI — strong optics, weak intelligence"),
        ("Our approach", "Open-source stack", "YOLOv8 + active learning + SAP MES integration, 4-6 week deploy"),
    ],
    "insight": "Human inspectors get tired. The camera doesn't. But they kept humans for the 0.3% the camera wasn't sure about. Best of both. The active learning loop is the key — every operator correction makes the model better.",
    "buyer": "VP Quality / Quality Manager",
    "revenue": "$5-10K/mo per plant",
    "deploy_mode": "Edge: Jetson Orin NX per station",
}

UC03 = {
    "kicker": "UC-03 | HEALTHCARE", "uc_id": "UC-03", "industry": "Healthcare",
    "title": "Patient Intake Automation — Form → EHR → Insurance → Booking",
    "headline_stat": "3-agent pipeline: 80% staff time saved, <30 sec insurance verification",
    "company_line": "Reference Architecture (FHIR + Twilio + Calendly)  |  Implementation-ready, HIPAA-compliant",
    "score": "Viable", "source": "GBrain impl spec + AI Engineering Framework",
    "problem_title": "40% of Staff Time Consumed by Paperwork",
    "problems": [
        "Manual intake: 12-15 minutes per patient, 40% of staff time consumed by paperwork",
        "Insurance verification: 270/271 EDI calls take 3-8 minutes per patient manually",
        "No-show rate 18-25% due to lack of automated reminders and cost transparency",
        "HIPAA compliance burden: every PHI access must be logged and audited",
        "Fragmented workflow: EHR, insurance portal, scheduling tool, SMS — all separate",
        "Prior authorization is bureaucratic, not clinical — most requests meet standard criteria",
    ],
    "realized_title": "3 Agents + 3 MCP Servers = End-to-End Automation",
    "realized": [
        "3-agent pipeline: intake-agent → insurance-verification-agent → scheduling-agent",
        "FHIR R4 MCP server: create_patient, get_insurance_eligibility, submit_claim",
        "Automated SMS reminders via Twilio MCP: confirmation, cost estimate, 24h reminder",
        "OpenHands Docker sandbox isolates PHI — never leaves infrastructure perimeter",
        "Confidence routing: standard cases automated, edge cases to nurse review",
        "Post-visit: update_patient + submit_claim (837 EDI) — closes the loop",
    ],
    "stats": [
        ("80%", "Staff Time Saved", "Intake + verification + scheduling automated"),
        ("<30 sec", "Insurance Check", "vs 3-8 min manual 270/271 EDI"),
        ("40%", "No-Show Reduction", "SMS reminders + cost transparency"),
        ("HIPAA", "Compliant by Design", "AES-256, TLS 1.3, Docker sandbox, BAA"),
        ("3", "MCP Integrations", "FHIR R4 + Twilio + Calendly"),
        ("$3-5K/mo", "Revenue Per Practice", "Per-practice subscription model"),
    ],
    "how_steps": [
        "Patient submits online intake form → validate fields (name, DOB, insurance ID)",
        "create_patient (FHIR R4) → demographics + medical history stored in EHR",
        "get_insurance_eligibility (270/271 EDI) → IF eligible: calculate copay/deductible",
        "send_sms via Twilio (appointment confirmation + cost estimate)",
        "create_booking via Calendly (get_available_slots → create_booking)",
        "24h before: send_reminder → reduces no-show rate by 40%",
        "Post-visit: update_patient (FHIR) + submit_claim (837 EDI)",
    ],
    "arch_title": "Patient Intake Automation Agent Architecture",
    "agents": [
        ("intake-agent", "Validates form data, creates FHIR patient resource, populates demographics"),
        ("insurance-verification-agent", "270/271 EDI eligibility → copay/deductible calculation"),
        ("scheduling-agent", "Calendly slot lookup → booking → SMS confirmation via Twilio"),
    ],
    "mcp_servers": [
        ("FHIR R4 MCP (5 endpoints)", "create_patient, update_patient, search_patient, get_insurance_eligibility, submit_claim", "to_build"),
        ("Twilio MCP (3 endpoints)", "send_sms, send_reminder, get_message_status", "to_build"),
        ("Calendly MCP (3 endpoints)", "get_available_slots, create_booking, cancel_booking", "to_build"),
    ],
    "deployment": "Docker sandbox (PHI isolation) | BAA with 3rd parties | Confirmation mode",
    "github_repos": [
        ("medplum/medplum", "Open-source FHIR server + EHR platform"),
        ("smart-on-fhir/client-js", "SMART on FHIR authorization"),
        ("twilio/twilio-node", "Twilio SDK for SMS/voice"),
        ("microsoft/presidio", "PII detection for HIPAA compliance"),
        ("All-Hands-AI/OpenHands", "Docker sandbox + confirmation mode"),
    ],
    "systems": "EHR (FHIR) | Insurance EDI | Twilio | Calendly",
    "users": "Front desk staff | Practice managers | Billing coordinators",
    "governance": [
        "HIPAA: AES-256 encryption at rest, TLS 1.3 in transit for all PHI",
        "BAA (Business Associate Agreement) required with Twilio, Calendly, FHIR provider",
        "Minimum necessary principle: agents access only required PHI fields per operation",
        "Audit logging: every PHI access logged with timestamp, agent, operation",
        "OpenHands Docker sandbox: PHI never leaves infrastructure perimeter",
    ],
    "competitors": [
        ("Phreesia", "$250M revenue", "Patient intake market leader — no AI agent orchestration"),
        ("Zocdoc", "Scheduling leader", "Scheduling but no insurance verification or EHR intake"),
        ("Notable Health", "AI intake", "AI-powered intake but no MCP integration or agent architecture"),
        ("Gap", "No integrated agent", "Nobody offers integrated intake + verify + schedule as agent pipeline"),
        ("Our approach", "3 agents + 3 MCPs", "Full pipeline, HIPAA by design, $3-5K/mo per practice"),
    ],
    "insight": "Prior auth is bureaucratic, not clinical. Most requests meet criteria — someone just needs to check the boxes. The AI checks the boxes. Edge cases still go to a nurse. The 270/271 EDI call is the perfect automation target — deterministic, structured, zero clinical judgment.",
    "buyer": "Practice Manager / VP Operations",
    "revenue": "$3-5K/mo per practice",
    "deploy_mode": "Docker sandbox (PHI isolation)",
}

UC05 = {
    "kicker": "UC-05 | LEGAL", "uc_id": "UC-05", "industry": "Legal",
    "title": "Contract Generation & Review — 67-Agent Debate Protocol",
    "headline_stat": "Projected: 70% review time reduction, 99.1% clause accuracy (industry estimate)",
    "company_line": "Top-100 Global Law Firm  |  22-week build, production by week 10",
    "score": "30/35 GO", "source": "DreamzTech Apr 2026 (industry estimate) + verified repos",
    "problem_title": "60% of Billable Time on Contract Drafting & Review",
    "problems": [
        "Paralegal review: 40 hours per contract across 90+ clause types",
        "Outside counsel spend growing 15% annually — firms need to shift work internal",
        "Mid-market firms (<50 attorneys) priced out of Harvey AI ($11B valuation, $300M ARR)",
        "Clause extraction breaks when documents exceed LLM context windows",
        "Jurisdiction-specific customization: 19 jurisdictions, different rules per state/country",
        "Lawyers spent 28 hours finding clauses and only 12 on actual judgment",
    ],
    "realized_title": "3 Agents + 5 MCP Servers + Debate Protocol",
    "realized": [
        "3 agents: contract-generation + contract-review (67-agent debate) + legal-research",
        "open-agreements MCP: 25+ templates (NDA, MSA, SaaS, SAFE, NVCA, employment, DPA)",
        "lavern MCP: 3-layer verification — evaluator gate → adversarial debate → 10-pass consensus",
        "suzielaw MCP: 22 legal providers across 19 jurisdictions — CourtListener, EUR-Lex",
        "Claude 200K context handles 300-page agreements in single pass — no chunking",
        "A2I confidence gating: <0.85 confidence → human review queue, not autonomous decision",
    ],
    "stats": [
        ("~70%", "Review Time ↓ (proj.)", "Industry estimate: 40 hrs → ~12 hrs per contract"),
        ("$2.4M", "Billable Hrs Recaptured", "Projected annual value (industry estimate)"),
        ("99.1%", "Clause Accuracy (est.)", "Across 90+ clause types per DreamzTech"),
        ("22 wk", "Full Build", "10 weeks to first production capability"),
        ("67", "Debate Agents", "Lavern adversarial review protocol (verified)"),
        ("5", "MCP Servers", "All verified: open-agreements, lavern, suzielaw, DocuSign, Clio"),
    ],
    "how_steps": [
        "Client request → identify agreement type → list_templates (open-agreements) → get_template_fields",
        "Interview client for field values (grouped by section) → fill_template → DOCX output",
        "Review Phase 1: planning agent reads contract (read-only) → structured review plan",
        "Review Phase 2: execution agent → risk assessment matrix + redlines + missing clauses",
        "Alternative: Lavern full adversarial (67 agents, debate protocol) → executive memo",
        "Legal research: suzielaw searches 22 providers across 19 jurisdictions for precedent",
        "High-confidence → auto-flag | Low-confidence (<0.85) → A2I human review queue",
    ],
    "arch_title": "Contract Generation & Review Agent Architecture",
    "agents": [
        ("contract-generation-agent", "Template selection → field interview → fill_template → DOCX → DocuSign"),
        ("contract-review-agent", "Phase 1: read-only planning → Phase 2: risk matrix + redlines → memo"),
        ("legal-research-agent", "suzielaw: jurisdiction-specific case search — 22 providers, 19 jurisdictions"),
        ("billing-agent", "Time capture → Clio time entries → invoice generation"),
    ],
    "mcp_servers": [
        ("open-agreements MCP (5 endpoints)", "list_templates, get_template_fields, fill_template, search_templates, validate_fields — 25+ templates", "verified"),
        ("lavern MCP (21 tools)", "start_review, get_findings, approve_finding, export_deliverable — 67-agent debate", "verified"),
        ("suzielaw MCP (3 endpoints)", "legal_search (19 jurisdictions), legal_get_document, legal_find_in_document", "verified"),
        ("DocuSign MCP (3 endpoints)", "create_envelope, send_for_signature, get_status", "to_build"),
        ("Clio MCP (5 endpoints)", "get_matters, create_time_entry, generate_invoice", "to_build"),
    ],
    "deployment": "Interactive: contract drafting | Headless: batch review | Weekly: Clio billing",
    "github_repos": [
        ("open-agreements/open-agreements", "v0.7.5 — 25+ templates, MCP server"),
        ("AnttiHero/lavern", "v0.15.0 — 67 agents, debate protocol, 21 MCP tools"),
        ("firelex/suzielaw", "19-jurisdiction legal research, 22 providers"),
        ("anthropics/claude-for-legal", "12 plugins, 80+ agents, 20 MCP connectors"),
        ("anylegal-ai/anylegal-oss", "12 tools, 80+ country legislation"),
    ],
    "systems": "iManage | DocuSign | CLM | Aderant | Clio",
    "users": "Paralegals | Associates | M&A partners | Legal ops",
    "governance": [
        "Client-attorney privilege preserved: all processing within firm infrastructure",
        "A2I confidence gating: clauses with <0.85 confidence routed to human review",
        "Verification corpus used in debate protocol — not fine-tuned model training",
        "Audit trail: every AI recommendation logged with confidence score and basis",
        "Jurisdictional compliance: template selection validates governing law",
    ],
    "competitors": [
        ("Harvey AI", "$11B valuation, $300M ARR", "142K lawyers, 50% of Am Law 100, 1,500+ customers in 60+ countries"),
        ("Thomson Reuters CoCounsel", "20,000+ firms", "Saves 5-8 hrs/day per attorney; research time cut 80%"),
        ("Ironclad", "CLM platform", "Contract lifecycle management — more workflow than AI intelligence"),
        ("LexisNexis Lexis+ AI", "284% ROI (Forrester)", "Source-grounded legal AI — 344% ROI for comparable platforms"),
        ("Our approach", "Mid-market, open MCP", "50-70% cheaper, 5 verified MCP servers, debate protocol, $3-5K/mo"),
    ],
    "insight": "Lawyers spent 28 hours finding clauses and 12 on judgment. Now they spend 12 on judgment. Everyone does what they're actually good at. The debate protocol (67 agents, adversarial review) catches what single-pass review misses. And every MCP server in this stack actually exists.",
    "buyer": "Legal Ops / Managing Partner",
    "revenue": "$3-5K/mo per firm",
    "deploy_mode": "Interactive: contract drafting with client interview",
}

# Category B UCs
UC04 = {
    "kicker": "UC-04 | HEALTHCARE", "uc_id": "UC-04", "industry": "Healthcare",
    "title": "Clinical AI — Sepsis Detection + Care Gap Closure",
    "headline_stat": "Tampa General: 700+ lives saved | CommonSpirit: 61K care gap orders",
    "company_line": "Tampa General Hospital + CommonSpirit Health  |  Production 2025 (both)",
    "score": "Viable", "source": "Becker's Hospital Review Dec 2025",
    "problem_title": "Clinical Signals Missed at Scale",
    "problems": [
        "Sepsis: early indicators missed in high-volume EDs — catastrophic if delayed",
        "Tampa General needed real-time vitals monitoring + care coordination across units",
        "CommonSpirit: 140+ hospitals, screening compliance inconsistent across sites",
        "Manual risk stratification cannot scale across 200+ AI-assisted clinical workflows",
        "Outcome verification: need binary, measurable results to prove clinical AI works",
        "Physician adoption barrier: clinicians won't use tools that add clicks without value",
    ],
    "realized_title": "Predictive ML Integrated into Clinical Workflow",
    "realized": [
        "TGH + Palantir: proprietary AI-driven care coordination center integrates EHR signals",
        "Predictive ML detects sepsis indicators → automated intervention triggers (proprietary)",
        "Nebraska Medicine extension: 5% shorter stays = 37 additional beds without construction",
        "CSH: Proprietary AI ingests EHR data → personalized cancer screening timelines",
        "200+ AI tools active across 140+ hospital system — proprietary platform approach",
        "Clinician-in-the-loop: AI recommends, clinician reviews and acts — not bypass",
    ],
    "stats": [
        ("700+", "Lives Saved", "Tampa General — sepsis detection program"),
        ("5%", "LOS Reduction", "Nebraska Medicine — equivalent to 37 beds"),
        ("61K", "Care Gap Orders", "CommonSpirit FY2025 — 5x YoY increase"),
        ("140+", "Hospitals", "CommonSpirit deployment scale"),
        ("200+", "AI Tools Active", "Across CommonSpirit health system"),
        ("37", "Virtual Beds", "Capacity gained without construction"),
    ],
    "our_agents": [
        ("vitals-monitoring-agent", "Real-time EHR vitals stream → sepsis risk scoring → early warning"),
        ("care-coordination-agent", "Discharge timing + bed allocation + intervention triggers"),
        ("screening-agent", "Patient risk factors → personalized screening timelines → order recommendation"),
    ],
    "our_mcp": [
        ("FHIR R4 MCP (bidirectional EHR)", "to_build"),
        ("Vitals streaming MCP", "to_build"),
        ("Clinical decision support MCP", "to_build"),
    ],
    "key_difference": "Palantir built this as a proprietary platform. We'd replicate with OpenHands agents + FHIR R4 MCP wrappers + clinician confirmation mode — open, composable, not locked to one vendor.",
    "competitors": [
        ("Palantir Foundry", "TGH partner", "Care coordination platform — strong but expensive, enterprise-only"),
        ("Epic Sepsis Model", "Built-in EHR", "High false positive rate historically — improved in recent versions"),
        ("Viz.ai", "Stroke/PE detection", "Narrow use case — strong for radiology, not general clinical AI"),
        ("Our positioning", "Agent architecture", "Composable agents via FHIR — not locked to one platform"),
    ],
    "insight": "Sepsis has a well-defined signal set, clear intervention window, and catastrophic downside. Outcome is binary and verifiable. Find the binary outcomes first. Care gap closure is the same pattern — deterministic criteria, structured data, standardized orders. Automate the matching, not the medicine.",
    "buyer": "CMO / VP Clinical Operations",
    "revenue": "Enterprise (health system deployment)",
    "deploy_mode": "Real-time: continuous vitals monitoring",
}

UC06 = {
    "kicker": "UC-06 | FINANCIAL SERVICES", "uc_id": "UC-06", "industry": "Financial Services",
    "title": "TD Bank — Mortgage Processing Agent (15hrs → Minutes)",
    "headline_stat": "$826M origination volume, deployed January 2026, compliance from day 1",
    "company_line": "TD Bank  |  January 2026 — production",
    "score": "Production", "source": "American Banker, May 2026",
    "problem_title": "15+ Hours Per Mortgage Application",
    "problems": [
        "Mortgage applications require 15+ hours of manual document review per application",
        "Cross-referencing borrower docs (ID, bank statements, pay stubs) is error-prone",
        "LLMs hallucinate on arithmetic — annualizing income is a known failure mode",
        "Risk and compliance review adds 3-5 days to the mortgage cycle",
        "100K+ applications per year — manual processing physically impossible at volume",
        "Competitive pressure: fintechs processing in days while banks take weeks",
    ],
    "realized_title": "Deterministic Math + LLM Document Reading (Layer 6)",
    "realized": [
        "TD Bank uses Layer 6 (acquired AI company) + Claude + GPT — proprietary stack",
        "Deterministic rules-based tools handle ALL arithmetic — LLM never does math",
        "Cross-references fields across documents, flags inconsistencies automatically",
        "Risk/compliance team built into the project from day 1 — not bolted on",
        "Human adjudicator reviews AI-generated credit summary — approves/rejects",
        "One use case done right before expanding to other banking operations",
    ],
    "stats": [
        ("15hr→min", "Processing Time", "Per mortgage application"),
        ("$826M", "2025 Origination", "U.S. residential mortgage volume"),
        ("Jan 2026", "Production Deploy", "Full production, not pilot"),
        ("Day 1", "Compliance Built In", "Risk team embedded from start"),
        ("100K+", "Applications/Year", "Scale of mortgage operation"),
        ("0", "LLM Math Operations", "All arithmetic is deterministic"),
    ],
    "our_agents": [
        ("document-extraction-agent", "OCR/NLP reads purchase agreements, IDs, bank statements → structured output"),
        ("cross-reference-agent", "Validates fields across documents — flags inconsistencies"),
        ("credit-summary-agent", "Generates complete credit summary: DTI, risk flags, recommendation"),
        ("compliance-agent", "Ensures every decision has audit trail + governance"),
    ],
    "our_mcp": [
        ("Document processing MCP", "to_build"),
        ("Deterministic rules engine MCP", "to_build"),
        ("Core banking MCP (OData)", "to_build"),
    ],
    "key_difference": "TD Bank used Layer 6 (proprietary). We'd replicate with OpenHands agents + deterministic rules MCP + human confirmation mode. Same principle: LLM reads, rules compute, human decides.",
    "competitors": [
        ("JPMorgan COIN", "360K hours saved, 9+ years", "Purpose-built ML for contracts — different scope (commercial vs mortgage)"),
        ("Blend", "Mortgage automation SaaS", "Digital lending platform — workflow automation, limited AI"),
        ("Mastercard DI", "143B txns/year", "Same real-time decisioning pattern: 20-300% detection lift, <50ms"),
        ("Our differentiation", "Agentic + deterministic", "LLM reads documents, rules engine does math, human decides"),
    ],
    "insight": "They didn't let the LLM do math. Deterministic tools for arithmetic, LLM for document reading. Sharp task boundaries. Human signs off on every credit decision. Risk/compliance from day one. One use case done right before expanding. Dead simple discipline.",
    "buyer": "VP Mortgage Operations / CTO",
    "revenue": "Enterprise (internal deployment)",
    "deploy_mode": "Production: full mortgage pipeline",
}

UC07 = {
    "kicker": "UC-07 | FINANCIAL SERVICES", "uc_id": "UC-07", "industry": "Financial Services",
    "title": "JPMorgan COIN — 360K Attorney-Hours Saved, 9+ Years Running",
    "headline_stat": "Purpose-built ML extracts 150 attributes from commercial credit agreements",
    "company_line": "JPMorgan Chase  |  June 2016, still in production (9+ years)",
    "score": "Production (9+ years)", "source": "TacticalVC Apr 2026; Finextra Sep 2025",
    "problem_title": "12,000 Credit Agreements Need 150 Attributes Each",
    "problems": [
        "12,000 commercial credit agreements per year require 150+ attributes each",
        "Multi-day manual review for covenants, collateral, payment schedules, defaults",
        "Error rate in manual extraction unacceptable at institutional lending scale",
        "Expanding scope: NDAs, custody agreements, CDS documentation — same problem",
        "900+ data scientists, $9.6B/year tech budget — scale demands purpose-built solutions",
        "Attorneys spending time on extraction instead of negotiation and strategy",
    ],
    "realized_title": "Purpose-Built ML — Not an LLM (Predates LLMs by Years)",
    "realized": [
        "Custom ML extracts 150 attributes from commercial credit agreements in seconds",
        "Trained on firm's own contract archive — learned JPMorgan's clause language",
        "Expanded over 9 years to NDAs, custody agreements, CDS, trade documentation",
        "Not an LLM — purpose-built precision extraction ML on private cloud infrastructure",
        "Error rate reduced ~80% vs manual extraction across all 150 attribute types",
        "Lawyers shifted to negotiation and strategy — not replaced, redirected",
    ],
    "stats": [
        ("360K", "Attorney-Hours Saved/yr", "Across commercial lending operations"),
        ("12K", "Contracts/yr", "Processed in seconds vs multi-day cycles"),
        ("~80%", "Error Rate ↓", "Vs manual extraction across 150 attributes"),
        ("9+ yrs", "In Production", "Since June 2016, continuously expanded"),
        ("150", "Attributes Extracted", "Covenants, collateral, payments, defaults"),
        ("$9.6B", "Annual Tech Budget", "Scale of JPMorgan technology investment"),
    ],
    "our_agents": [
        ("extraction-agent", "Layout-preserving extraction via LayoutLM / document AI models"),
        ("classification-agent", "Covenant type, collateral category, payment structure classification"),
        ("validation-agent", "Cross-reference extracted attributes against document structure"),
    ],
    "our_mcp": [
        ("Document AI MCP (LayoutLM)", "to_build"),
        ("Contract management MCP", "to_build"),
    ],
    "key_difference": "COIN is purpose-built ML (not LLM) with 9 years of refinement on JPMorgan's own data. Our modern equivalent uses document understanding models (LayoutLM) + OpenHands agents — but COIN's 9-year data flywheel is not replicable on day one. Honest about that.",
    "competitors": [
        ("TD Bank", "Agentic AI (2026)", "Newer approach: LLM + deterministic — different scope (mortgage vs commercial)"),
        ("Kira Systems (Litera)", "Contract analysis", "AI contract review — acquired by Litera, enterprise pricing"),
        ("Eigen Technologies", "Document intelligence", "NLP extraction for financial services — narrow focus"),
        ("Our framing", "Lessons learned", "9 years proves: narrow domain + own data + continuous refinement = endurance"),
    ],
    "insight": "Contracts follow predictable structures. Narrow domain, closed text, static rules. Started with single document type, 150 attributes. Lawyers shifted to negotiation — not replaced, redirected. Purpose-built ML on your own data beats general-purpose LLM on someone else's.",
    "buyer": "CTO / VP Legal Operations",
    "revenue": "Enterprise ($9.6B tech budget)",
    "deploy_mode": "Production: continuous 12K contracts/year",
}

UC08 = {
    "kicker": "UC-08 | CONSTRUCTION", "uc_id": "UC-08", "industry": "Construction",
    "title": "DroneDeploy — 34M Annotations, 4 AI Agents, 3M+ Sites",
    "headline_stat": "Autonomous overnight capture → morning reports, 48% injury reduction",
    "company_line": "DroneDeploy + Barton Malow  |  Production across 3M+ sites, break-even Sep 2025",
    "score": "Production (3M+ sites)", "source": "DroneDeploy Blog Apr 2026 + BCG 2026",
    "problem_title": "Construction Sites Are Unstructured and Underdocumented",
    "problems": [
        "Manual site walks miss events, rely entirely on superintendent memory",
        "Safety violations go undetected — poor documentation is industry-wide",
        "Progress reporting takes 2 days of manual compilation per project",
        "Generic computer vision doesn't understand what 'installed' means per trade",
        "Subcontractor management: no objective comparison across trades or sites",
        "Data center construction exploding: 300+ projects, users up 128% YoY",
    ],
    "realized_title": "4 Proprietary AI Agents + 13-Year Data Moat",
    "realized": [
        "DroneDeploy's proprietary 4 AI agents: Progress AI, Safety AI, Inspection AI, Embodied AI",
        "Autonomous ground robots (Rocos) + docked drones — proprietary hardware integration",
        "13-year annotation corpus: 34M labeled examples across 3M sites in 180 countries",
        "Safety AI trained on 120K labeled examples — proprietary domain-specific model",
        "770M images processed in 2025 alone — proprietary processing pipeline",
        "The 34M annotation corpus is the moat — competitors cannot replicate this data flywheel",
    ],
    "stats": [
        ("34M", "Training Annotations", "13-year corpus across 180 countries"),
        ("+340%", "Safety Catches", "Real-time violation detection improvement"),
        ("48%", "Injury Reduction", "Over 12-month deployment period"),
        ("3M+", "Sites in Production", "Global deployment scale"),
        ("770M", "Images (2025)", "Processed in single calendar year"),
        ("Sep 2025", "Break-Even", "Company reached profitability"),
    ],
    "our_agents": [
        ("progress-tracking-agent", "Capture vs plan comparison → deviation reports (YOLOv8 + OpenCV)"),
        ("safety-monitoring-agent", "PPE detection, guardrail violations, zone intrusions"),
        ("inspection-agent", "Structural analysis, defect identification, compliance documentation"),
    ],
    "our_mcp": [
        ("Vision pipeline MCP (YOLOv8)", "to_build"),
        ("BIM integration MCP", "to_build"),
        ("Procore API MCP", "to_build"),
    ],
    "key_difference": "DroneDeploy's moat is 34M annotations over 13 years — not replicable. Our approach: same agent pattern with open-source CV (YOLOv8 + OpenCV) for specific site use cases, without claiming to match their corpus scale.",
    "competitors": [
        ("Buildots", "Indoor CV", "Progress tracking via hardhat cameras — indoor only, no outdoor/drone"),
        ("OpenSpace", "360 walk-through", "Manual trigger, not autonomous"),
        ("Skydio", "Drone hardware", "Autonomous drone — strong flight, limited analytics"),
        ("DroneDeploy edge", "34M annotation moat", "13-year corpus across 180 countries — the data flywheel"),
    ],
    "insight": "13-year annotation corpus — 34M labeled examples across 180 countries — is the moat. The superintendent now acts on data instead of generating it. Generic CV fails because it doesn't understand what 'installed' means for different trades.",
    "buyer": "VP Construction / Project Director",
    "revenue": "Enterprise (break-even Sep 2025)",
    "deploy_mode": "Autonomous: overnight capture missions",
}

UC09 = {
    "kicker": "UC-09 | CONSTRUCTION", "uc_id": "UC-09", "industry": "Construction",
    "title": "BCG: AI Construction Site Assistant — 6x ROI, 48% Injury Reduction",
    "headline_stat": "Computer vision for risk detection, progress tracking, productivity benchmarking",
    "company_line": "German DevCo (BCG pilot)  |  Pilot on 2 live projects, BCG 2026 Executive Perspectives",
    "score": "Pilot (6x ROI validated)", "source": "BCG Executive Perspectives, 2026",
    "problem_title": "Poor Documentation, Manual Walks, Memory-Based Decisions",
    "problems": [
        "Historical poor incident documentation — site walks miss events, rely on memory",
        "Productivity benchmarking impossible without objective data across subcontractors",
        "Manual progress reporting delays corrective action by days, not hours",
        "Subcontractor management: no objective comparison metric across trades",
        "Legal liability gaps from inconsistent site documentation practices",
        "BCG models 400-700 bps margin uplift achievable across construction vertical",
    ],
    "realized_title": "BCG Consulting Framework — CV Risk Detection + Documentation",
    "realized": [
        "BCG consulting framework (not a product): computer vision risk detection on pilot sites",
        "AI-driven progress tracking: automated documentation vs plan comparison",
        "Productivity benchmarking: objective metrics across subcontractors and trades",
        "Smart notifications: immediate alerts when risks or deviations detected",
        "Validated on 2 live pilot projects by a German development company",
        "BCG Executive Perspectives report validates 400-700 bps margin uplift potential",
    ],
    "stats": [
        ("6x", "ROI", "Across deployed pilot projects"),
        ("12%", "Productivity Boost", "In first 6 months of deployment"),
        ("48%", "Injury Reduction", "Over 12-month deployment period"),
        ("30%", "Timeline Compression", "Project timeline reduction (BCG model)"),
        ("400-700", "bps Margin Uplift", "BCG model across construction vertical"),
        ("2", "Live Pilots", "German DevCo projects in production"),
    ],
    "our_agents": [
        ("risk-detection-agent", "Real-time CV analysis → risk identification → smart notifications"),
        ("progress-tracking-agent", "Capture vs plan comparison → automated deviation reports"),
        ("benchmarking-agent", "Productivity metrics per subcontractor/trade → objective comparison"),
    ],
    "our_mcp": [
        ("CV pipeline MCP (YOLOv8)", "to_build"),
        ("Project management MCP (BIM/ERP)", "to_build"),
    ],
    "key_difference": "BCG validated the ROI model (400-700 bps). We'd build the actual product: lighter CV stack with OpenHands agents for risk detection + progress tracking as a services play.",
    "competitors": [
        ("DroneDeploy", "Market leader, 34M annotations", "The benchmark for construction AI — autonomous capture + AI agents"),
        ("Buildots", "Indoor progress tracking", "Hardhat cameras — strong indoor, limited outdoor/safety"),
        ("OpenSpace", "360 capture", "Manual walk-through — not automated, not real-time"),
        ("Our positioning", "BCG-validated ROI", "BCG validates 400-700 bps uplift — we build the product"),
    ],
    "insight": "Construction has historically had poor incident documentation. AI that captures every site state photographically creates an objective record — closes legal liability gaps, triggers faster corrective action. You can't manage what you can't see. Now they can see everything.",
    "buyer": "VP Construction / COO",
    "revenue": "Enterprise (pilot → 400-700 bps uplift)",
    "deploy_mode": "Real-time: continuous site monitoring",
}

UC10 = {
    "kicker": "UC-10 | LEGAL", "uc_id": "UC-10", "industry": "Legal",
    "title": "LexisNexis Lexis+ AI — 284% ROI, Payback Under 6 Months",
    "headline_stat": "Forrester TEI: $1.2M benefits, 13% outside counsel reduction, source-grounded",
    "company_line": "LexisNexis (Forrester TEI Study)  |  Forrester Total Economic Impact study, June 2025",
    "score": "Production (284% ROI validated)", "source": "GlobeNewswire / Forrester TEI, June 2025",
    "problem_title": "In-House Teams Overwhelmed, Too Much to Outside Counsel",
    "problems": [
        "In-house legal teams overwhelmed — shipping too much work to expensive outside counsel",
        "Legal research hours: associates spending 25%+ time on case lookups and precedent",
        "Hallucinated case citations are the #1 trust barrier for legal AI adoption",
        "Need to increase matters handled internally without adding headcount",
        "Outside counsel costs growing 15% annually — unsustainable trajectory",
        "Generic AI tools not grounded in verified primary law — fabricated citations destroy trust",
    ],
    "realized_title": "Proprietary Source-Grounded AI on Verified Primary Law Corpus",
    "realized": [
        "LexisNexis proprietary gen AI grounded in their verified primary law corpus",
        "Contract drafting assistance: suggests clauses from verified precedent, review + accept",
        "Protege personalized AI assistant: adapts to individual attorney's practice area",
        "Source-grounded citations eliminate the hallucination problem entirely (proprietary corpus)",
        "Shifts outside-counsel work internal — more valuable than raw efficiency gains",
        "Forrester TEI methodology: validated by independent third-party research firm",
    ],
    "stats": [
        ("284%", "ROI (3-Year)", "Forrester Total Economic Impact study"),
        ("$1.2M", "Total Benefits", "Over 3-year evaluation period"),
        ("13%", "Outside Counsel ↓", "Reduction in external legal spend → $602.5K"),
        ("<6 mo", "Payback Period", "Investment recovered in under 6 months"),
        ("25%", "Fewer Lawyer Hours", "On research inquiries → $574.2K saved"),
        ("344%", "Market Benchmark", "Forrester ROI for comparable legal AI platforms"),
    ],
    "our_agents": [
        ("research-agent", "Legal question → suzielaw corpus search → source-cited answer"),
        ("drafting-agent", "Contract clause suggestion from open-agreements templates → review + accept"),
        ("review-agent", "Lavern 67-agent debate protocol → adversarial verification"),
    ],
    "our_mcp": [
        ("suzielaw MCP (19 jurisdictions)", "verified"),
        ("lavern MCP (67-agent debate)", "verified"),
        ("claude-for-legal (12 plugins)", "verified"),
        ("open-agreements MCP", "verified"),
    ],
    "key_difference": "LexisNexis's moat is their verified primary law corpus. Our open-source equivalent: suzielaw (19 jurisdictions, 22 providers) + lavern (67-agent debate) + claude-for-legal (12 plugins). Not corpus-equivalent, but the agent architecture and verification layer are real and verified.",
    "competitors": [
        ("Harvey AI", "$11B valuation, $300M ARR", "142K lawyers, 50% of Am Law 100 — market leader, enterprise-only"),
        ("Thomson Reuters CoCounsel", "20,000+ firms", "5-8 hrs/day saved per attorney; research time cut 80%"),
        ("Casetext (Thomson Reuters)", "CoCounsel", "Acquired by Thomson Reuters — AI research assistant"),
        ("Our framing", "Source-grounding lesson", "Winner is grounded in verified law — open stack replicates the pattern"),
    ],
    "insight": "Legal AI's core problem is hallucinated case citations. Grounding in a verified database eliminates fabrication. The right business case: outside-counsel reduction is more valuable than raw efficiency. Shifting work internal via AI beats doing existing work faster. Frame it as revenue retained, not time saved.",
    "buyer": "General Counsel / Legal Ops Director",
    "revenue": "Enterprise (SaaS subscription)",
    "deploy_mode": "SaaS: browser-based research + drafting",
}


# ── Build orchestration ─────────────────────────────────────────────────────

CAT_A = [UC01, UC02, UC03, UC05]
CAT_B = [UC04, UC06, UC07, UC08, UC09, UC10]

SECTIONS = [
    (1, "Manufacturing", "UC-01 | UC-02", "Where predictive beats reactive — and the data already exists",
     [("A", UC01), ("A", UC02)]),
    (2, "Healthcare", "UC-03 | UC-04", "Automate the paperwork, augment the clinician",
     [("A", UC03), ("B", UC04)]),
    (3, "Legal", "UC-05 | UC-10", "67 agents debating so lawyers can judge",
     [("A", UC05), ("B", UC10)]),
    (4, "Financial Services", "UC-06 | UC-07", "Let LLMs read, let rules compute, let humans decide",
     [("B", UC06), ("B", UC07)]),
    (5, "Construction", "UC-08 | UC-09", "The camera doesn't get tired. The superintendent acts on data.",
     [("B", UC08), ("B", UC09)]),
]


def count_slides():
    """Pre-count total slides."""
    total = 3  # cover + portfolio + architecture
    for _, _, _, _, ucs in SECTIONS:
        total += 1  # section divider
        for cat, _ in ucs:
            if cat == "A":
                total += 8  # title, problem, realized, metrics, how, arch, governance, competitive, insight → 9 but we'll count
            else:
                total += 6  # title, problem, how_they, metrics, how_wed, competitive
    total += 2  # winners + closer
    return total


def build():
    total = 3  # cover + portfolio + corrected architecture
    for _, _, _, _, ucs in SECTIONS:
        total += 1  # section divider
        for cat, _ in ucs:
            total += 9 if cat == "A" else 6
    total += 2  # winners + closer

    d = Deck()
    page = 1

    # ── Slide 1: Cover ──
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.12), d.b.TEAL)
    d.text(s, "FULL PIPELINE — PRE-SALES INTELLIGENCE", d.M, Inches(1.5), d.CW, Inches(0.3),
           size=12, color=d.b.TEAL, bold=True)
    d.text(s, "AI Use Cases That Actually Ship", d.M, Inches(1.9), d.CW, Inches(0.8),
           size=36, color=d.b.WHITE, bold=True, shrink=True)
    d.text(s, "10 Use Cases · 5 Industries · Verified Repos · Honest Architecture · Corrected API",
           d.M, Inches(2.8), d.CW, Inches(0.3), size=12, color=d.b.GOLD, bold=True, shrink=True)
    # Stat badges
    badges = [("10", "Use Cases"), ("5", "Industries"), ("6", "Verified MCP"), ("4", "Buildable"), ("6", "Benchmarks")]
    bw = Inches(1.8)
    bg = Inches(0.18)
    bx = d.M
    by = Inches(3.5)
    for num, label in badges:
        d.rect(s, bx, by, bw, Inches(0.85), d.b.TEAL, radius=0.05)
        d.text(s, num, bx + Inches(0.1), by + Inches(0.08), bw - Inches(0.2), Inches(0.36),
               size=24, color=d.b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, label, bx + Inches(0.1), by + Inches(0.48), bw - Inches(0.2), Inches(0.22),
               size=10, color=d.b.LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)
        bx += bw + bg

    d.text(s, f"Data pipeline: GBrain recall → Exa research → OpenHands verification → pptxkit render",
           d.M, Inches(4.7), d.CW, Inches(0.3), size=10, color=d.b.MUTED, shrink=True)
    d.text(s, BRAND, d.M, Inches(5.5), d.CW, Inches(0.3), size=14, color=d.b.GOLD, bold=True)
    _footer(d, s, page, total, dark=True)
    page += 1

    # ── Slide 2: Portfolio ──
    s = _header(d, "Portfolio: 5 Industries, 10 Use Cases, One Architecture",
                "Agent(llm, tools) → Conversation(agent, workspace, plugins) | MCP at platform level")
    labels = [
        ("Manufacturing", "32/35 GO", "$5-10K/mo", "PdM (Unilever $2.3M) + Visual QI (YOLOv8, 99.2%)", "A+A"),
        ("Healthcare", "Viable", "$3-5K/mo", "Patient Intake (FHIR+Twilio) + Clinical AI (TGH+CSH)", "A+B"),
        ("Legal", "30/35 GO", "$3-5K/mo", "Contract Review (67-agent) + LexisNexis (284% ROI)", "A+B"),
        ("Financial Svcs", "Production", "Enterprise", "TD Bank (15hr→min) + JPMorgan (360K hrs/yr)", "B+B"),
        ("Construction", "Production", "Enterprise", "DroneDeploy (34M annotations) + BCG (6x ROI)", "B+B"),
    ]
    for i, (name, score, rev, desc, cat) in enumerate(labels):
        y = Inches(1.75) + i * Inches(0.95)
        d.rect(s, d.M, y, d.CW, Inches(0.78), d.b.NAVY, radius=0.05)
        d.text(s, name, d.M + Inches(0.2), y + Inches(0.1), Inches(2.2), Inches(0.24),
               size=14, color=d.b.WHITE, bold=True)
        d.rect(s, d.M + Inches(2.5), y + Inches(0.1), Inches(1.2), Inches(0.24), d.b.TEAL, radius=0.03)
        d.text(s, score, d.M + Inches(2.55), y + Inches(0.1), Inches(1.1), Inches(0.24),
               size=9, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        d.rect(s, d.M + Inches(3.85), y + Inches(0.1), Inches(1.2), Inches(0.24), d.b.GOLD, radius=0.03)
        d.text(s, rev, d.M + Inches(3.9), y + Inches(0.1), Inches(1.1), Inches(0.24),
               size=9, color=d.b.NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        d.text(s, desc, d.M + Inches(0.2), y + Inches(0.4), Inches(8), Inches(0.22),
               size=10, color=d.b.LIGHT_TEAL, shrink=True)
        # Category tag
        d.text(s, f"[{cat}]", d.M + Inches(5.3), y + Inches(0.1), Inches(0.6), Inches(0.24),
               size=8, color=d.b.AMBER, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    _footer(d, s, page, total)
    page += 1

    # ── Slide 3: Corrected Architecture ──
    s = _header(d, "ONE ARCHITECTURE, EVERY INDUSTRY — CORRECTED",
                "Verified against OpenHands GitHub repo (2026-06-08)")
    layers = [
        ("USER LAYER", "CLI / Generative UI (AG-UI) / Headless Batch", d.b.SOFT),
        ("ORCHESTRATION", "Agent(llm, tools) → Conversation(agent, workspace, plugins)", d.b.NAVY),
        ("MCP CONFIG", "Platform-level config.toml under [mcp] — SSE, Streamable HTTP, or stdio transports", d.b.ACCENT),
        ("VERIFIED MCP", "predictive-maintenance-mcp · open-agreements · lavern · suzielaw · claude-for-legal", d.b.TEAL),
        ("TO BUILD MCP", "FHIR wrapper · Twilio wrapper · Calendly wrapper · SAP MES wrapper · vision-pipeline", d.b.AMBER),
        ("DOMAIN SKILLS", "SKILL.md markdown prompts with keyword triggers → domain instructions (not code bundles)", d.b.SOFT),
        ("SYSTEM OF RECORD", "SAP S/4HANA · EHR/FHIR · iManage · CRM · TMS · BIM · Core Banking", d.b.NAVY),
    ]
    for i, (label, desc, bg) in enumerate(layers):
        y = Inches(1.7) + i * Inches(0.72)
        d.rect(s, d.M, y, d.CW, Inches(0.6), bg, radius=0.04)
        tc = d.b.WHITE if bg in (d.b.NAVY, d.b.ACCENT, d.b.TEAL) else d.b.NAVY
        d.text(s, label, d.M + Inches(0.2), y + Inches(0.06), Inches(2.2), Inches(0.2),
               size=10, color=d.b.GOLD if bg == d.b.NAVY else d.b.NAVY, bold=True)
        d.text(s, desc, d.M + Inches(2.5), y + Inches(0.06), d.CW - Inches(2.7), Inches(0.44),
               size=9.5, color=tc, shrink=True)
    _footer(d, s, page, total)
    page += 1

    # ── Sections + UCs ──
    for sec_num, sec_name, sec_ucs, sec_tagline, ucs in SECTIONS:
        _section(d, sec_num, sec_name, sec_ucs, sec_tagline, page, total)
        page += 1

        for cat, uc in ucs:
            if cat == "A":
                cat_a_title(d, uc, page, total); page += 1
                cat_a_problem(d, uc, page, total); page += 1
                cat_a_realized(d, uc, page, total); page += 1
                cat_a_metrics(d, uc, page, total); page += 1
                cat_a_how(d, uc, page, total); page += 1
                cat_a_architecture(d, uc, page, total); page += 1
                cat_a_governance(d, uc, page, total); page += 1
                cat_a_competitive(d, uc, page, total); page += 1
                cat_a_insight(d, uc, page, total); page += 1
            else:
                cat_b_title(d, uc, page, total); page += 1
                cat_b_problem(d, uc, page, total); page += 1
                cat_b_how_they_did_it(d, uc, page, total); page += 1
                cat_b_metrics(d, uc, page, total); page += 1
                cat_b_how_wed_build_it(d, uc, page, total); page += 1
                cat_b_competitive(d, uc, page, total); page += 1

    # ── Slide: What Winners Have in Common ──
    s = _header(d, "WHAT THE WINNERS HAVE IN COMMON", "")
    rules = [
        ("01", "Define the number before writing code",
         "TD Bank: processing hours. C.H. Robinson: quote time. Unilever: downtime %. A metric with a baseline before day 1."),
        ("02", "Automate the boring part, not the judgment",
         "AI handles extraction, matching, triage. Lawyers still decide. Underwriters still sign. Superintendents still prioritize."),
        ("03", "Proprietary data is the moat, not the model",
         "DroneDeploy 34M annotations. JPMorgan 9 years of contract data. Same models, different data, wildly different outcomes."),
        ("04", "Composite AI beats pure LLM",
         "TD Bank: deterministic math for arithmetic, LLM for reading. Unilever: XGBoost+LSTM ensemble, not single model. Use the right tool per sub-task."),
        ("05", "Trust is a deployment phase, not a launch event",
         "Unilever: 6-month technician trust-building before full reliance. Budget time for humans to catch up with the machine."),
    ]
    for i, (num, title, desc) in enumerate(rules):
        y = Inches(1.65) + i * Inches(1.05)
        d.rect(s, d.M, y, Inches(0.5), Inches(0.5), d.b.TEAL, radius=0.04)
        d.text(s, num, d.M + Inches(0.05), y, Inches(0.4), Inches(0.5),
               size=16, color=d.b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        d.text(s, title, d.M + Inches(0.65), y + Inches(0.04), d.CW - Inches(0.8), Inches(0.26),
               size=13, color=d.b.NAVY, bold=True, shrink=True)
        d.text(s, desc, d.M + Inches(0.65), y + Inches(0.32), d.CW - Inches(0.8), Inches(0.5),
               size=10, color=d.b.INK, shrink=True, ls=1.05)
    _footer(d, s, page, total)
    page += 1

    # ── Closer ──
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.12), d.b.TEAL)
    d.text(s, "The best AI project is the one that actually ships.",
           d.M, Inches(2.0), d.CW, Inches(1.0), size=30, color=d.b.WHITE, bold=True, shrink=True)
    d.text(s, "Not the one with the cleanest architecture, the most sophisticated model,\nor the biggest budget. The one that ships. With a number attached.",
           d.M, Inches(3.1), d.CW, Inches(0.8), size=14, color=d.b.LIGHT_TEAL, shrink=True, ls=1.2)
    d.text(s, "10 use cases. 5 industries. One honest architecture.",
           d.M, Inches(4.2), d.CW, Inches(0.4), size=16, color=d.b.GOLD, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, BRAND, d.M, Inches(5.2), d.CW, Inches(0.4), size=18, color=d.b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    _footer(d, s, page, total, dark=True)

    d.save(OUT)
    print(f"Wrote {OUT} ({page} slides)")


if __name__ == "__main__":
    build()
