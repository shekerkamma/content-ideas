#!/usr/bin/env python3
from pathlib import Path
import json
import sys

sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, Inches, PP_ALIGN


RUN = Path("runs/hermes-content-pipeline-real-auto")
DATE = "2026-07-01"
DELIVERABLES = RUN / "deliverables" / DATE
LOGS = RUN / "logs" / DATE
OUT = RUN / "artifacts" / "Hermes_Content_Pipeline_Business_Package-reviewed.pptx"
FOOTER = "Hermes Content Pipeline Business Package | 2026-07-01"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def bullets(items, size=12.0, space=5):
    return [{"text": item, "bullet": True, "size": size, "space_before": space} for item in items]


def add_footer(d, s, page, total, dark=False):
    d.footer(s, page, total, dark=dark)


def card(d, s, x, y, w, h, title, body, accent=None, idx=None, body_size=10.5, title_size=11.2):
    b = d.b
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(h), b.WHITE, line=b.GRID, radius=0.06, shadow=True)
    if accent:
        d.rect(s, Inches(x), Inches(y), Inches(0.07), Inches(h), accent)
    if idx:
        d.rect(s, Inches(x + 0.15), Inches(y + 0.14), Inches(0.42), Inches(0.28), b.NAVY, radius=0.04)
        d.text(s, idx, Inches(x + 0.15), Inches(y + 0.18), Inches(0.42), Inches(0.18), size=8.0, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        tx = x + 0.68
        tw = w - 0.86
    else:
        tx = x + 0.22
        tw = w - 0.44
    d.text(s, title, Inches(tx), Inches(y + 0.12), Inches(tw), Inches(0.38), size=title_size, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, Inches(x + 0.22), Inches(y + 0.58), Inches(w - 0.44), Inches(h - 0.68), size=body_size, color=b.INK, shrink=True)


def stat(d, s, x, y, w, h, value, label, note="", fill=None):
    b = d.b
    fill = fill or b.NAVY
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(h), fill, radius=0.07, shadow=True)
    d.text(s, value, Inches(x + 0.18), Inches(y + 0.16), Inches(w - 0.36), Inches(0.40), size=24, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, label, Inches(x + 0.18), Inches(y + 0.66), Inches(w - 0.36), Inches(0.24), size=10.3, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    if note:
        d.text(s, note, Inches(x + 0.18), Inches(y + 0.98), Inches(w - 0.36), Inches(0.26), size=8.5, color=b.LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)


def section(d, label, title, subtitle, page, total):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.text(s, label.upper(), Inches(0.72), Inches(1.20), Inches(3.0), Inches(0.30), size=12.5, color=b.TEAL, bold=True)
    d.text(s, title, Inches(0.72), Inches(1.72), Inches(8.9), Inches(1.25), size=38, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(0.72), Inches(3.10), Inches(1.65), Inches(0.06), b.GOLD)
    d.text(s, subtitle, Inches(0.72), Inches(3.48), Inches(8.3), Inches(0.65), size=17, color=b.LIGHT_TEAL, shrink=True)
    add_footer(d, s, page, total, dark=True)


def build():
    run_log = load_json(LOGS / "run-log.json")
    metadata = load_json(DELIVERABLES / "deliverables-metadata.json")
    counts = run_log["counts"]
    cost = run_log["cost"]

    d = Deck(footer=FOOTER)
    b = d.b
    total = 13

    # 1. Cover
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(11.15), 0, Inches(2.18), d.H, b.NAVY_2)
    d.rect(s, Inches(11.15), 0, Inches(0.08), d.H, b.TEAL)
    d.text(s, "CLIENT-READY BUSINESS PACKAGE", d.M, Inches(0.72), d.CW, Inches(0.26), size=12.5, color=b.TEAL, bold=True)
    d.text(s, "Hermes Content Pipeline", d.M, Inches(1.35), Inches(8.6), Inches(0.70), size=42, color=b.WHITE, bold=True, shrink=True)
    d.text(s, "From live source signals to review-ready business content", d.M, Inches(2.16), Inches(8.4), Inches(0.46), size=20, color=b.LIGHT_TEAL, shrink=True)
    d.rect(s, d.M, Inches(2.92), Inches(1.72), Inches(0.06), b.GOLD)
    d.text(s, "A concrete Hermes realization: scheduled source scanning, topic ranking, source-grounded briefs, draft package creation, approval gates, and memory write-back.", d.M, Inches(3.35), Inches(8.55), Inches(0.82), size=17, color=b.WHITE, shrink=True)
    chips = ["Live run", "No auto-publish", "Source-grounded", "Cost-capped"]
    for i, chip in enumerate(chips):
        d.rect(s, Inches(0.6 + i * 2.1), Inches(5.45), Inches(1.75), Inches(0.42), b.NAVY_2, line=b.TEAL, radius=0.08)
        d.text(s, chip, Inches(0.74 + i * 2.1), Inches(5.58), Inches(1.47), Inches(0.13), size=9.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(d, s, 1, total, dark=True)

    # 2. Executive decision
    s = d.slide(fill=b.SOFT)
    d.header(s, "Decision: Build The Operating Layer", "The pipeline turns market signal into review-ready judgment, with controls.")
    d.rect(s, d.M, Inches(1.82), d.CW, Inches(1.24), b.NAVY, radius=0.06)
    d.text(s, "BLUF", Inches(0.88), Inches(2.18), Inches(0.72), Inches(0.22), size=12.0, color=b.GOLD, bold=True)
    d.text(s, "Agent adoption is moving from isolated tools to governed operating layers. The useful Hermes use case is a repeatable workflow that compresses research and drafting before a human decides what ships.", Inches(1.72), Inches(2.03), Inches(10.45), Inches(0.58), size=11.0, color=b.WHITE, shrink=True)
    card(d, s, 0.72, 3.48, 2.88, 1.52, "Business Outcome", "Article package, social drafts, newsletter copy, and memory candidates from a real source run.", accent=b.TEAL, body_size=10.0)
    card(d, s, 3.93, 3.48, 2.88, 1.52, "Buyer Relevance", "Enterprise AI operators, solution architects, founders, and technical executives.", accent=b.GOLD, body_size=10.0)
    card(d, s, 7.14, 3.48, 2.88, 1.52, "Operating Model", "Sources, memory, tools, schedule, controls, and approval gates create repeatable work.", accent=b.ACCENT, body_size=10.0)
    card(d, s, 10.35, 3.48, 2.18, 1.52, "Guardrail", "No publish permission; final claims and voice stay human-owned.", accent=b.CORAL, body_size=9.4)
    d.text(s, "Success metric: 3-5 qualified conversations about implementing governed agent workflows.", d.M, Inches(5.75), d.CW, Inches(0.30), size=14.0, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(d, s, 2, total)

    # 3. Evidence base
    s = d.slide(fill=b.SOFT)
    d.header(s, "Evidence Favors Governed Agents", "The source register points to enterprise adoption, agent tooling, and operational governance.")
    evidence = [
        ("Enterprise adoption", "OpenAI enterprise reports point to AI moving from experimentation into organization-wide deployment."),
        ("Agent tooling", "OpenAI's agent-building releases emphasize tools, deployment, and reliable agent behavior."),
        ("Governance gap", "Agent work needs permissions, context, approval, observability, and source grounding."),
        ("Hermes fit", "Hermes exposes files, shell, browser, skills, search, memory, and cron."),
        ("Content angle", "The story is not more AI content. It is an operating system for recurring knowledge work."),
        ("Buyer action", "Start with one narrow workflow that has sources, memory, cost cap, and approval gate."),
    ]
    for i, (title, body) in enumerate(evidence):
        x = 0.72 + (i % 3) * 4.08
        y = 1.88 + (i // 3) * 1.58
        card(d, s, x, y, 3.55, 1.22, title, body, accent=b.TEAL if i < 3 else b.GOLD, idx=str(i + 1), body_size=9.8)
    d.rect(s, d.M, Inches(5.58), d.CW, Inches(0.62), b.NAVY, radius=0.05)
    d.text(s, "Primary brief citations: OpenAI enterprise AI report, OpenAI next-phase enterprise AI, OpenAI tools for building agents.", Inches(0.88), Inches(5.76), Inches(11.6), Inches(0.23), size=10.8, color=b.WHITE, shrink=True)
    add_footer(d, s, 3, total)

    # 4. Run metrics
    s = d.slide(fill=b.SOFT)
    d.header(s, "Real Run Output", "This was not a smoke test; the pipeline produced artifacts against a cap.")
    stats = [
        (str(counts["source_items"]), "source items", "current source scan"),
        (str(counts["topic_clusters"]), "topic clusters", "ranked opportunities"),
        (str(counts["research_briefs"]), "research briefs", "source-backed synthesis"),
        (str(counts["draft_packages"]), "draft package", "review-ready bundle"),
        (str(counts["deliverables"]), "deliverables", "business artifacts"),
        ("$" + str(cost["estimated_usd"]), "estimated cost", "$12.00 cap"),
    ]
    for i, (value, label, note) in enumerate(stats):
        x = 0.82 + (i % 3) * 4.05
        y = 1.92 + (i // 3) * 1.52
        stat(d, s, x, y, 3.30, 1.20, value, label, note, fill=b.NAVY if i != 5 else b.NAVY_2)
    d.rect(s, d.M, Inches(5.70), d.CW, Inches(0.55), b.WHITE, line=b.GRID, radius=0.06, shadow=True)
    d.text(s, "Run status: success | Publish allowed: false | Errors: none | Human approval still required.", Inches(0.92), Inches(5.88), Inches(11.4), Inches(0.18), size=11.4, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(d, s, 4, total)

    # 5. Workflow architecture
    section(d, "Section 01", "Workflow Architecture", "The business output comes from a governed sequence, not one prompt.", 5, total)

    # 6. Pipeline operating model
    s = d.slide(fill=b.SOFT)
    d.header(s, "Source Signal To Review Package", "A narrow loop is easier to trust, evaluate, and improve.")
    steps = [
        ("Source scan", "Pull allowed sources and collect fresh candidate signals."),
        ("Topic ranking", "Cluster signals and choose the strongest daily business angle."),
        ("Sourced brief", "Summarize proof points, claims, citations, and guardrails."),
        ("Draft package", "Create article, LinkedIn post, X thread, and newsletter copy."),
        ("Human review", "Approve claims, voice, positioning, and publishing decision."),
        ("Memory write-back", "Persist durable facts and lessons for future runs."),
    ]
    for i, (title, body) in enumerate(steps):
        x = 0.72 + (i % 3) * 4.08
        y = 1.88 + (i // 3) * 1.42
        card(d, s, x, y, 3.55, 1.00, title, body, accent=b.TEAL if i < 3 else b.GOLD, idx=str(i + 1), body_size=9.0, title_size=10.0)
    d.rect(s, d.M, Inches(5.20), d.CW, Inches(0.86), b.NAVY, radius=0.06)
    d.text(s, "Control thesis", Inches(0.92), Inches(5.42), Inches(1.35), Inches(0.20), size=11.3, color=b.GOLD, bold=True)
    d.text(s, "The agent compresses work before judgment. It does not own judgment.", Inches(2.45), Inches(5.36), Inches(9.65), Inches(0.28), size=11.0, color=b.WHITE, shrink=True)
    add_footer(d, s, 6, total)

    # 7. Hermes solution components
    s = d.slide(fill=b.SOFT)
    d.header(s, "Hermes Solution Components", "Each component exists because a recurring workflow needs a boundary.")
    comps = [
        ("Harness", "Desktop/CLI runtime with files, shell, browser, tools, and skills."),
        ("Search", "You.com current-web search; livecrawl for pages; specialist tools when needed."),
        ("Memory", "GBrain/Obsidian-style durable context with explicit recall and write-back."),
        ("Schedule", "Cron job runs daily without waiting for a manual prompt."),
        ("Controls", "Cost cap, model routing, source register, run log, and error log."),
        ("Approval", "No publishing; drafts queue for human claim and voice review."),
    ]
    for i, (title, body) in enumerate(comps):
        x = 0.72 + (i % 3) * 4.08
        y = 1.84 + (i // 3) * 1.62
        card(d, s, x, y, 3.55, 1.16, title, body, accent=b.ACCENT if i % 2 else b.TEAL, idx=str(i + 1), body_size=10.3)
    d.rect(s, d.M, Inches(5.58), d.CW, Inches(0.74), b.NAVY, radius=0.05)
    d.text(s, "Implementation rule: every component needs an owner, allowed actions, fallback behavior, and visible artifacts.", Inches(0.90), Inches(5.78), Inches(11.45), Inches(0.30), size=10.0, color=b.WHITE, bold=True, shrink=True)
    add_footer(d, s, 7, total)

    # 8. Controls
    s = d.slide(fill=b.SOFT)
    d.header(s, "Controls: Keep Version 1 Boring", "A narrow first version makes trust measurable.")
    d.rect(s, Inches(0.85), Inches(1.88), Inches(5.55), Inches(3.90), b.WHITE, line=b.GRID, radius=0.08, shadow=True)
    d.text(s, "V1 allows", Inches(1.18), Inches(2.16), Inches(1.6), Inches(0.25), size=17, color=b.NAVY, bold=True)
    d.text(s, bullets([
        "Small, explicit source list",
        "One daily run",
        "Capped research briefs",
        "One draft package per run",
        "Visible source register and run log",
        "Memory candidates, not silent memory mutation",
    ], size=11.4), Inches(1.20), Inches(2.68), Inches(4.80), Inches(2.25), size=11.4, color=b.INK, shrink=True)
    d.rect(s, Inches(6.95), Inches(1.88), Inches(5.55), Inches(3.90), b.NAVY, radius=0.08, shadow=True)
    d.text(s, "V1 forbids", Inches(7.28), Inches(2.16), Inches(1.6), Inches(0.25), size=17, color=b.GOLD, bold=True)
    d.text(s, bullets([
        "Auto-publishing",
        "Unbounded browsing",
        "Unreviewed claims",
        "Open-ended outbound",
        "Credential/config changes",
        "File deletion or repo mutation",
    ], size=11.4), Inches(7.30), Inches(2.68), Inches(4.75), Inches(2.25), size=11.4, color=b.WHITE, shrink=True)
    add_footer(d, s, 8, total)

    # 9. Publish package
    section(d, "Section 02", "Business Deliverables", "The output is a publishing and sales-enablement package, not raw research notes.", 9, total)

    # 10. Deliverable package
    s = d.slide(fill=b.SOFT)
    d.header(s, "Deliverables Produced", "The run already created business-facing assets that can be reviewed, edited, and shipped.")
    packages = [
        ("Business memo", "Decision, buyer, desired action, value, and success metrics."),
        ("Editorial brief", "Title, angle, claim, proof points, guardrails, and takeaway."),
        ("Article draft", "Long-form point of view on governed operating layers."),
        ("LinkedIn post", "Business narrative for discussion, without generic AI hype."),
        ("X thread", "Six-part concise narrative for signal testing."),
        ("Newsletter blurb", "Short-form distribution copy for email/community channels."),
    ]
    for i, (title, body) in enumerate(packages):
        x = 0.72 + (i % 3) * 4.08
        y = 1.84 + (i // 3) * 1.58
        card(d, s, x, y, 3.55, 1.18, title, body, accent=b.TEAL if i < 3 else b.GOLD, body_size=9.4)
    d.rect(s, d.M, Inches(5.60), d.CW, Inches(0.62), b.NAVY, radius=0.05)
    d.text(s, metadata["business_angle"]["title"], Inches(0.88), Inches(5.77), Inches(11.6), Inches(0.22), size=11.0, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(d, s, 10, total)

    # 11. Narrative storyboard
    s = d.slide(fill=b.SOFT)
    d.header(s, "Storyline For Market Use", "The narrative is direct: governed workflows beat broad autonomy.")
    beats = [
        ("1. Bad question", "What can the agent do?"),
        ("2. Better question", "What recurring workflow can it run safely every day?"),
        ("3. Operating layer", "Sources, memory, tools, schedule, controls, approval."),
        ("4. Hermes example", "Scan, rank, brief, draft, review, remember."),
        ("5. Business result", "Faster path from live signal to review-ready point of view."),
    ]
    for i, (title, body) in enumerate(beats):
        x = 0.72 + i * 2.48
        d.rect(s, Inches(x), Inches(2.05), Inches(2.02), Inches(2.50), b.WHITE, line=b.GRID, radius=0.08, shadow=True)
        d.rect(s, Inches(x), Inches(2.05), Inches(2.02), Inches(0.48), b.NAVY if i != 4 else b.TEAL, radius=0.08)
        d.text(s, title, Inches(x + 0.14), Inches(2.18), Inches(1.74), Inches(0.22), size=8.0, color=b.WHITE if i != 4 else b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, body, Inches(x + 0.18), Inches(2.95), Inches(1.66), Inches(0.82), size=10.6, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        if i < 4:
            d.text(s, "->", Inches(x + 2.08), Inches(3.12), Inches(0.26), Inches(0.16), size=10.8, color=b.MUTED, bold=True)
    d.text(s, "Line to use: the agent does not replace editorial judgment; it removes the blank page before judgment starts.", d.M, Inches(5.64), d.CW, Inches(0.46), size=10.8, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(d, s, 11, total)

    # 12. Implementation next steps
    s = d.slide(fill=b.SOFT)
    d.header(s, "Implementation Plan", "Move from a successful run to a repeatable business system.")
    phases = [
        ("Day 1-2", "Source policy", "Lock source list, You.com mode order, freshness windows, and citation rules."),
        ("Day 3-4", "Cron runbook", "Schedule daily run, cost cap, run log, error file, and artifact destinations."),
        ("Day 5-7", "Review loop", "Define human editor gate, publish checklist, and memory acceptance workflow."),
        ("Week 2", "Scale carefully", "Add source categories, vertical-specific briefs, CRM hooks, and reporting dashboard."),
    ]
    for i, (time, title, body) in enumerate(phases):
        x = 0.78 + i * 3.08
        d.rect(s, Inches(x), Inches(2.00), Inches(2.55), Inches(2.15), b.WHITE, line=b.GRID, radius=0.08, shadow=True)
        d.text(s, time, Inches(x + 0.18), Inches(2.25), Inches(2.15), Inches(0.22), size=11.2, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, title, Inches(x + 0.18), Inches(2.70), Inches(2.15), Inches(0.34), size=12.5, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, body, Inches(x + 0.22), Inches(3.20), Inches(2.05), Inches(0.74), size=8.4, color=b.INK, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, d.M, Inches(5.34), d.CW, Inches(0.78), b.NAVY, radius=0.05)
    d.text(s, "Decision ask: approve this as the first governed Hermes workflow. Add sales or investor workflows only after V1 review quality is proven.", Inches(0.92), Inches(5.54), Inches(11.35), Inches(0.34), size=9.8, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(d, s, 12, total)

    # 13. Source appendix
    s = d.slide(fill=b.SOFT)
    d.header(s, "Source Appendix", "Primary sources used by the business package.")
    source_rows = [
        ("OpenAI", "The state of enterprise AI", "openai.com/index/the-state-of-enterprise-ai-2025-report"),
        ("OpenAI", "The next phase of enterprise AI", "openai.com/index/next-phase-of-enterprise-ai"),
        ("OpenAI", "New tools for building agents", "openai.com/index/new-tools-for-building-agents"),
        ("OpenAI", "Building governed AI agents", "developers.openai.com/cookbook/.../agentic_governance_cookbook"),
        ("Hermes", "Bundled autonomous-agent docs", "hermes-agent.nousresearch.com/docs/user-guide/.../autonomous-ai-agents-hermes-agent"),
        ("Hermes", "Hermes user stories", "hermes-agent.nousresearch.com/docs/user-stories"),
    ]
    y = 1.82
    for org, title, url in source_rows:
        d.rect(s, Inches(0.78), Inches(y), Inches(11.75), Inches(0.60), b.WHITE, line=b.GRID, radius=0.04)
        d.text(s, org, Inches(0.98), Inches(y + 0.19), Inches(1.0), Inches(0.18), size=8.4, color=b.TEAL, bold=True, shrink=True)
        d.text(s, title, Inches(2.08), Inches(y + 0.17), Inches(3.15), Inches(0.18), size=8.4, color=b.NAVY, bold=True, shrink=True)
        d.text(s, url, Inches(5.45), Inches(y + 0.17), Inches(6.70), Inches(0.18), size=7.0, color=b.MUTED, shrink=True)
        y += 0.68
    d.rect(s, d.M, Inches(6.20), d.CW, Inches(0.38), b.NAVY, radius=0.04)
    d.text(s, "Deck status: reviewed after PPTX validation and preview inspection.", Inches(0.88), Inches(6.30), Inches(11.5), Inches(0.16), size=7.8, color=b.WHITE, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(d, s, 13, total)

    d.save(OUT)


if __name__ == "__main__":
    build()
