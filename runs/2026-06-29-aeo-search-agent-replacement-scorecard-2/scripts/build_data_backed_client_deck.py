#!/usr/bin/env python3
"""Build a data-backed client deck for the AEO scorecard run."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

SKILL_DIR = Path("/home/shekerk/.claude/skills/branded-pptx-deck")
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from pptxkit import Deck, Inches, PP_ALIGN  # noqa: E402


RUN = Path(__file__).resolve().parents[1]
OUT = RUN / "final" / "agent-replacement-scorecard-aeo-data-backed-client-reviewed.pptx"
FOOTER = "Agent Replacement Scorecard AEO | Data-backed reviewed draft | 2026-06-29"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def bullet(items: list[str], size: float = 11.4) -> list[dict]:
    return [{"text": item, "bullet": True, "size": size, "space_before": 5} for item in items]


def card(d: Deck, s, x, y, w, h, title, body="", accent=None, title_size=13.4, body_size=10.2):
    b = d.b
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(h), b.WHITE, line=b.GRID, radius=0.035, shadow=True)
    if accent:
        d.rect(s, Inches(x), Inches(y), Inches(0.07), Inches(h), accent)
    d.text(s, title, Inches(x + 0.18), Inches(y + 0.15), Inches(w - 0.36), Inches(0.28),
           size=title_size, color=b.NAVY, bold=True, shrink=True)
    if body:
        d.text(s, body, Inches(x + 0.18), Inches(y + 0.55), Inches(w - 0.36), Inches(h - 0.68),
               size=body_size, color=b.INK, shrink=True)


def chip(d: Deck, s, x, y, w, label, fill, color=None):
    b = d.b
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(0.32), fill, radius=0.1)
    d.text(s, label, Inches(x + 0.08), Inches(y + 0.08), Inches(w - 0.16), Inches(0.13),
           size=8.4, color=color or b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)


def kpi(d: Deck, s, x, y, w, value, label, note, fill=None):
    b = d.b
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(1.04), fill or b.NAVY, radius=0.04)
    d.text(s, str(value), Inches(x + 0.16), Inches(y + 0.13), Inches(w - 0.32), Inches(0.30),
           size=20, color=b.GOLD, bold=True, shrink=True)
    d.text(s, label, Inches(x + 0.16), Inches(y + 0.49), Inches(w - 0.32), Inches(0.22),
           size=8.8, color=b.WHITE, bold=True, shrink=True)
    d.text(s, note, Inches(x + 0.16), Inches(y + 0.75), Inches(w - 0.32), Inches(0.2),
           size=7.3, color=b.LIGHT_TEAL, shrink=True)


def bars(d: Deck, s, data: list[tuple[str, int]], x, y, w, row_h=0.42, max_value=None, color=None):
    b = d.b
    max_value = max_value or max(v for _, v in data) or 1
    for i, (label, value) in enumerate(data):
        yy = y + i * row_h
        d.text(s, label, Inches(x), Inches(yy + 0.08), Inches(2.55), Inches(0.13),
               size=8.8, color=b.INK, bold=True, shrink=True)
        d.rect(s, Inches(x + 2.75), Inches(yy + 0.09), Inches(w - 3.3), Inches(0.15), b.GRID)
        bw = (w - 3.3) * value / max_value
        d.rect(s, Inches(x + 2.75), Inches(yy + 0.09), Inches(max(0.05, bw)), Inches(0.15), color or b.TEAL)
        d.text(s, str(value), Inches(x + w - 0.42), Inches(yy + 0.065), Inches(0.4), Inches(0.14),
               size=8.4, color=b.NAVY, bold=True, align=PP_ALIGN.RIGHT)


def table(d: Deck, s, rows: list[tuple[str, str, str]], x, y, w, row_h=0.46, headers=("Item", "Metric", "Implication")):
    b = d.b
    col = [w * 0.28, w * 0.22, w * 0.50]
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(0.36), b.NAVY)
    xx = x
    for i, h in enumerate(headers):
        d.text(s, h, Inches(xx + 0.12), Inches(y + 0.1), Inches(col[i] - 0.18), Inches(0.12),
               size=8.2, color=b.WHITE, bold=True, shrink=True)
        xx += col[i]
    for r, row in enumerate(rows):
        yy = y + 0.42 + r * row_h
        d.rect(s, Inches(x), Inches(yy), Inches(w), Inches(row_h - 0.04), b.SOFT if r % 2 == 0 else b.WHITE, line=b.GRID)
        xx = x
        for i, val in enumerate(row):
            d.text(s, val, Inches(xx + 0.12), Inches(yy + 0.12), Inches(col[i] - 0.2), Inches(0.14),
                   size=7.9, color=b.INK if i else b.NAVY, bold=(i == 0), shrink=True)
            xx += col[i]


def section(d: Deck, title: str, subtitle: str, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.text(s, f"SECTION {page:02d}", d.M, Inches(1.0), Inches(2.0), Inches(0.25), size=12.5, color=b.TEAL, bold=True)
    d.text(s, title, d.M, Inches(1.65), Inches(8.8), Inches(0.85), size=36, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.72), Inches(1.8), Inches(0.06), b.TEAL)
    d.text(s, subtitle, d.M, Inches(3.1), Inches(8.8), Inches(0.52), size=16, color=b.LIGHT_TEAL, shrink=True)
    d.footer(s, page, total, dark=True)


def build() -> Path:
    status = read_json(RUN / "qa" / "evidence_sprint_status.json")
    counts = status["counts"]
    gates = status["gates"]
    pattern_rows = read_jsonl(RUN / "normalized" / "pattern_candidates.jsonl")
    reddit_rows = read_jsonl(RUN / "normalized" / "reddit_buyer_language.jsonl")
    opp_rows = read_jsonl(RUN / "normalized" / "reddit_aeo_opportunities.jsonl")
    capture_units = read_jsonl(RUN / "normalized" / "capture_units.jsonl")
    prompts = read_jsonl(RUN / "stage_outputs" / "ai_answer_prompt_pack.jsonl")
    reviews = read_jsonl(RUN / "normalized" / "pattern_reviews.jsonl")

    signal_counts = Counter()
    subreddit_counts = Counter()
    topic_counts = Counter()
    for row in reddit_rows:
        subreddit_counts[row.get("subreddit", "unknown")] += 1
        topic_counts[(row.get("qualification") or {}).get("source_topic", "unknown")] += 1
        for signal in row.get("matched_signals") or []:
            signal_counts[signal] += 1
    engine_units = Counter(row.get("engine", "unknown") for row in capture_units if not row.get("target_seeded"))
    seeded_units = sum(1 for row in capture_units if row.get("target_seeded"))
    review_counts = Counter(row.get("decision", "unknown") for row in reviews)

    d = Deck(footer=FOOTER)
    b = d.b
    total = 22

    # 1
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(10.8), 0, Inches(2.53), d.H, b.NAVY_2)
    d.rect(s, Inches(10.8), 0, Inches(0.08), d.H, b.TEAL)
    d.text(s, "DATA-BACKED CLIENT DECK", d.M, Inches(0.82), Inches(5.4), Inches(0.24), size=13, color=b.TEAL, bold=True)
    d.text(s, "Agent Replacement\nScorecard", d.M, Inches(1.28), Inches(8.8), Inches(1.0), size=34, color=b.WHITE, bold=True, shrink=True)
    d.text(s, "AEO evidence, data points, scorecard mechanics, and execution plan",
           d.M, Inches(2.6), Inches(8.8), Inches(0.34), size=15.5, color=b.LIGHT_TEAL, shrink=True)
    d.rect(s, d.M, Inches(3.18), Inches(1.8), Inches(0.06), b.TEAL)
    d.text(s, "Built from run artifacts: Reddit rows, AI-answer captures, pattern candidates, review gates, and prompt pack.",
           d.M, Inches(3.58), Inches(8.1), Inches(0.42), size=13.5, color=b.WHITE, shrink=True)
    chip(d, s, 0.6, 4.35, 1.65, "88 REDDIT ROWS", b.GOLD, b.NAVY)
    chip(d, s, 2.45, 4.35, 1.65, "10 AI CAPTURES", b.TEAL, b.NAVY)
    chip(d, s, 4.3, 4.35, 1.6, "9 PATTERNS", b.NAVY_2)
    d.footer(s, 1, total, dark=True)

    # 2
    s = d.slide(fill=b.WHITE)
    d.header(s, "Proceed, but label it correctly", "The data supports a v0 scorecard launch; it does not support a final market-proof claim.")
    card(d, s, 0.75, 1.75, 3.65, 2.0, "Decision", "Launch a reviewed v0 diagnostic, not a definitive AEO proof asset.", b.TEAL)
    card(d, s, 4.85, 1.75, 3.65, 2.0, "Evidence basis", "88 Reddit rows, 10 independent AI captures, 2 independent engines, 9 pattern candidates.", b.GOLD)
    card(d, s, 8.95, 1.75, 3.55, 2.0, "Open gap", "Need 20 independent captures and 3 independent engines before stronger claims.", b.CORAL)
    d.rect(s, d.M, Inches(4.55), d.CW, Inches(0.85), b.NAVY, radius=0.04)
    d.text(s, "Product wedge: score workflow compression while records, permissions, and audit trails survive.",
           Inches(0.9), Inches(4.82), Inches(11.4), Inches(0.28), size=11.3, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 2, total)

    section(d, "Evidence Base", "Use the run data explicitly: what passed, what failed, and what it implies.", 3, total)

    # 4
    s = d.slide(fill=b.WHITE)
    d.header(s, "Evidence funnel: current vs target", "Current proof gates, without hand-wavy confidence.")
    funnel = [
        ("Reddit buyer language", counts["reddit_buyer_language_rows"], 5, "passed"),
        ("Independent AI captures", counts["independent_ai_answer_captures"], 20, "open"),
        ("Independent engines", counts["independent_answer_engines"], 3, "open"),
        ("Pattern candidates", counts["pattern_candidates"], 1, "review"),
        ("Accepted pattern reviews", counts["accepted_pattern_reviews"], 1, "open"),
    ]
    y = 1.75
    for label, current, required, state in funnel:
        d.rect(s, d.M, Inches(y), d.CW, Inches(0.58), b.SOFT, line=b.GRID, radius=0.03)
        d.text(s, label, Inches(0.82), Inches(y + 0.17), Inches(3.3), Inches(0.18), size=11.2, color=b.NAVY, bold=True)
        maxv = max(current, required, 1)
        d.rect(s, Inches(4.25), Inches(y + 0.2), Inches(4.5), Inches(0.14), b.GRID)
        d.rect(s, Inches(4.25), Inches(y + 0.2), Inches(4.5 * current / maxv), Inches(0.14), b.TEAL if current >= required else b.AMBER)
        d.text(s, f"{current} / {required}", Inches(9.0), Inches(y + 0.16), Inches(1.0), Inches(0.16), size=10, color=b.INK, bold=True)
        chip(d, s, 10.45, y + 0.13, 1.2, state.upper(), b.TEAL if state == "passed" else b.AMBER, b.NAVY)
        y += 0.72
    d.footer(s, 4, total)

    # 5
    s = d.slide(fill=b.SOFT)
    d.header(s, "AI capture coverage is the bottleneck", "The useful data is real, but engine coverage is not yet broad enough.")
    kpi(d, s, 0.75, 1.72, 2.2, counts["answer_captures"], "Total captures", "Includes seeded rows")
    kpi(d, s, 3.15, 1.72, 2.2, counts["independent_ai_answer_captures"], "Independent", "Usable for claims")
    kpi(d, s, 5.55, 1.72, 2.2, counts["target_seeded_capture_ids"], "Seeded", "Exclude from claims")
    kpi(d, s, 7.95, 1.72, 2.2, counts["independent_answer_engines"], "Engines", "Need 3")
    kpi(d, s, 10.35, 1.72, 2.2, "10", "Capture gap", "Need +10")
    bars(d, s, sorted(status["engine_counts"].items(), key=lambda x: x[1], reverse=True), 1.0, 3.45, 10.8, row_h=0.48, color=b.TEAL)
    d.footer(s, 5, total)

    # 6
    s = d.slide(fill=b.WHITE)
    d.header(s, "Answer units skew to Gemini", "Claims should not be presented as engine consensus yet.")
    usable_units = sum(engine_units.values())
    kpi(d, s, 0.75, 1.72, 2.3, usable_units, "Usable units", "Non-target-seeded")
    kpi(d, s, 3.3, 1.72, 2.3, seeded_units, "Seeded units", "Excluded")
    kpi(d, s, 5.85, 1.72, 2.3, len(capture_units), "All units", "Raw unit count")
    bars(d, s, engine_units.most_common(), 1.0, 3.25, 10.8, row_h=0.55, color=b.DARK_TEAL)
    d.footer(s, 6, total)

    # 7
    s = d.slide(fill=b.SOFT)
    d.header(s, "Reddit evidence shapes prompts", "Reddit is buyer language and objection evidence, not market-size proof.")
    kpi(d, s, 0.75, 1.72, 2.3, len(reddit_rows), "Buyer rows", "Qualified snippets")
    kpi(d, s, 3.3, 1.72, 2.3, len(subreddit_counts), "Subreddits", "Source spread")
    kpi(d, s, 5.85, 1.72, 2.3, len(topic_counts), "Topics", "Workflow spread")
    kpi(d, s, 8.4, 1.72, 2.3, sum(signal_counts.values()), "Signal tags", "Multi-label")
    bars(d, s, signal_counts.most_common(), 1.0, 3.25, 10.8, row_h=0.42, color=b.GOLD)
    d.footer(s, 7, total)

    # 8
    s = d.slide(fill=b.WHITE)
    d.header(s, "Reddit signals: objections and workarounds", "The content should answer skepticism, not just explain the scorecard.")
    rows = [(r["signal"], str(r["evidence_count"]), f"Prompt around {r['signal']} language") for r in opp_rows[:6]]
    table(d, s, rows, 0.75, 1.72, 11.85, row_h=0.56, headers=("Signal", "Rows", "AEO action"))
    d.footer(s, 8, total)

    section(d, "Pattern Evidence", "Pattern slides need counts, engine coverage, and review status.", 9, total)

    # 10
    s = d.slide(fill=b.WHITE)
    d.header(s, "Pattern coverage by independent captures", "Capture count is not proof, but it is a useful prioritization signal.")
    pattern_counts = [(p["label"], len(p.get("capture_ids") or [])) for p in pattern_rows]
    bars(d, s, sorted(pattern_counts, key=lambda x: x[1], reverse=True), 0.9, 1.72, 11.0, row_h=0.46, color=b.TEAL)
    d.footer(s, 10, total)

    # 11
    s = d.slide(fill=b.SOFT)
    d.header(s, "Pattern coverage table", "Use medium-confidence patterns as hypotheses, not accepted market truths.")
    rows = []
    for p in pattern_rows[:7]:
        engines = ", ".join(p.get("engines") or [])
        rows.append((p["label"], f"{len(p.get('capture_ids') or [])} captures / {len(p.get('engines') or [])} engines", engines[:70]))
    table(d, s, rows, 0.7, 1.62, 11.95, row_h=0.52, headers=("Pattern", "Coverage", "Engines"))
    d.footer(s, 11, total)

    # 12
    s = d.slide(fill=b.WHITE)
    d.header(s, "Semantic review is the missing promotion gate", "The review file currently records rejection pressure, not accepted patterns.")
    kpi(d, s, 0.75, 1.75, 2.3, len(reviews), "Review rows", "Adversarial checks")
    kpi(d, s, 3.3, 1.75, 2.3, review_counts.get("reject", 0), "Rejected", "Do not promote")
    kpi(d, s, 5.85, 1.75, 2.3, counts["accepted_pattern_reviews"], "Accepted", "Current state")
    card(d, s, 0.75, 3.35, 5.55, 2.05, "Client implication",
         "This is a product blueprint deck, not a proof deck. The next evidence sprint must convert hypotheses into accepted reviewed patterns.", b.GOLD)
    card(d, s, 6.95, 3.35, 5.55, 2.05, "Deck implication",
         "Every strong claim needs a visible evidence status: observed, hypothesis, rejected, or accepted.", b.CORAL)
    d.footer(s, 12, total)

    # 13
    s = d.slide(fill=b.SOFT)
    d.header(s, "Six hypotheses become dimensions", "The deck should show how data turns into product logic.")
    dims = [
        ("Workflow determinism", "High-volume, rule-bound workflows are more exposed."),
        ("Data moat", "Records, permissions, audit, and governance defend the system."),
        ("Human sign-off", "Risk and accountability define the automation boundary."),
        ("Pilotability", "Historical replay and parallel runs make claims testable."),
        ("Renewal leverage", "Seat/add-on compression creates the commercial wedge."),
        ("Citation eligibility", "Pages must earn inclusion in AI answer surfaces."),
    ]
    for i, (title, body) in enumerate(dims):
        card(d, s, 0.75 + (i % 3) * 4.1, 1.72 + (i // 3) * 1.88, 3.62, 1.32, title, body, b.TEAL if i < 3 else b.GOLD)
    d.footer(s, 13, total)

    section(d, "Product + AEO Plan", "Translate the evidence into pages, diagnostics, and capture workflows.", 14, total)

    # 15
    s = d.slide(fill=b.WHITE)
    d.header(s, "Prompt pack drives the AEO queue", "Non-target-seeded prompts become capture prompts and page briefs.")
    rows = []
    for p in prompts[:8]:
        rows.append((p["topic"][:34], p["subreddit_context"], "Non-target-seeded page + capture prompt"))
    table(d, s, rows, 0.65, 1.55, 12.05, row_h=0.48, headers=("Topic", "Reddit context", "Use"))
    d.footer(s, 15, total)

    # 16
    s = d.slide(fill=b.SOFT)
    d.header(s, "AEO pages need buyer questions", "Build pages that answer where agents are useful.")
    pages = [
        ("Customer support", "Reduce support seats?"),
        ("Document workflows", "Replace drafting add-ons?"),
        ("Legal drafting", "Mandatory review?"),
        ("Creative generation", "Compress production seats?"),
        ("Data moats", "Records/audit moat?"),
        ("Pilot design", "Test before renewal?"),
    ]
    table(d, s, pages, 0.7, 1.65, 11.95, row_h=0.56, headers=("Page", "Buyer question", ""))
    d.footer(s, 16, total)

    # 17
    s = d.slide(fill=b.WHITE)
    d.header(s, "Workflow examples: exposed vs surviving", "This is the tangible client artifact.")
    rows = [
        ("Conversational support", "Tier-1 queues / bot add-ons", "Helpdesk records + escalation"),
        ("Doc summarization", "Drafting add-on seats", "Office suite + document store"),
        ("Legal drafting", "First-draft workflow", "Research corpus + attorney review"),
        ("Creative generation", "Variant production seats", "DAM + brand governance"),
        ("AI shopping", "Guided selling scripts", "Catalog, inventory, pricing system"),
    ]
    table(d, s, rows, 0.7, 1.65, 11.95, row_h=0.58, headers=("Workflow", "Exposed layer", "Surviving layer"))
    d.footer(s, 17, total)

    # 18
    s = d.slide(fill=b.SOFT)
    d.header(s, "Operating workflow compounds evidence", "This is the repeatable kit, not a one-off deck.")
    steps = [
        ("1", "Generate prompts", "Use Reddit buyer language and non-target-seeded questions."),
        ("2", "Capture answers", "Collect across ChatGPT, Claude, Perplexity, Google AI Mode."),
        ("3", "Mine patterns", "Use semantic matching, not keyword matching."),
        ("4", "Review/falsify", "Promote only accepted mechanisms."),
        ("5", "Publish pages", "Turn gaps into crawlable AEO assets."),
        ("6", "Rerun gates", "Measure recommendation eligibility."),
    ]
    for i, (num, title, body) in enumerate(steps):
        card(d, s, 0.75 + (i % 3) * 4.1, 1.65 + (i // 3) * 1.95, 3.62, 1.38, f"{num}. {title}", body, b.TEAL if i < 3 else b.GOLD)
    d.footer(s, 18, total)

    # 19
    s = d.slide(fill=b.WHITE)
    d.header(s, "30-day data targets make the plan measurable", "The next deck should show passed gates, not just a stronger story.")
    rows = [
        ("AI captures", f"{counts['independent_ai_answer_captures']} now", "Reach 20 independent captures"),
        ("Answer engines", f"{counts['independent_answer_engines']} now", "Reach 3 independent engines"),
        ("Pattern reviews", f"{counts['accepted_pattern_reviews']} accepted", "Accept/reject each promoted pattern"),
        ("AEO pages", "0 page cluster shipped", "Publish 5 buyer-question pages"),
        ("Citation gap", "No cited external domains", "Earn/source third-party citation candidates"),
    ]
    table(d, s, rows, 0.7, 1.62, 11.95, row_h=0.62, headers=("Metric", "Current", "30-day target"))
    d.footer(s, 19, total)

    # 20
    s = d.slide(fill=b.SOFT)
    d.header(s, "Claim guardrails", "The deck is more credible when it says what it cannot prove yet.")
    card(d, s, 0.75, 1.75, 5.65, 3.5, "Safe claims",
         "Reviewed draft. Directional v0 model. Evidence supports workflow-layer compression as a hypothesis. Reddit provides buyer language and objections.", b.TEAL, title_size=15)
    card(d, s, 6.9, 1.75, 5.65, 3.5, "Unsafe claims",
         "Full AEO readiness. Consensus across ChatGPT, Claude, Perplexity, and Google. Statistical validation. Accepted market patterns.", b.CORAL, title_size=15)
    d.footer(s, 20, total)

    # 21
    s = d.slide(fill=b.WHITE)
    d.header(s, "Decision ask: v0 + evidence sprint", "Launch the diagnostic; upgrade proof quality in the next sprint.")
    asks = [
        ("Launch v0 scorecard", "5 dimensions + 4 verdicts."),
        ("Publish page cluster", "Build 5 unbranded AEO pages."),
        ("Complete capture gate", "Add +10 captures + one engine."),
        ("Run semantic review", "Accept/reject promoted patterns."),
    ]
    table(d, s, asks, 0.8, 1.8, 11.7, row_h=0.78, headers=("Ask", "Reason", ""))
    d.footer(s, 21, total)

    # 22
    s = d.slide(fill=b.NAVY)
    d.text(s, "APPENDIX", d.M, Inches(0.9), Inches(2.2), Inches(0.24), size=13, color=b.TEAL, bold=True)
    d.text(s, "Data sources used in this deck", d.M, Inches(1.45), Inches(8.2), Inches(0.55), size=31, color=b.WHITE, bold=True, shrink=True)
    files = [
        "qa/evidence_sprint_status.json",
        "normalized/reddit_buyer_language.jsonl",
        "normalized/reddit_aeo_opportunities.jsonl",
        "normalized/capture_units.jsonl",
        "normalized/pattern_candidates.jsonl",
        "normalized/pattern_reviews.jsonl",
        "stage_outputs/ai_answer_prompt_pack.jsonl",
    ]
    d.text(s, bullet(files, 12.4), d.M, Inches(2.55), Inches(8.4), Inches(2.8), color=b.WHITE, shrink=True)
    d.rect(s, Inches(8.55), Inches(2.75), Inches(3.2), Inches(1.7), b.NAVY_2, radius=0.04)
    d.text(s, "Status", Inches(8.85), Inches(3.02), Inches(2.6), Inches(0.2), size=12.5, color=b.TEAL, bold=True)
    d.text(s, "Reviewed draft. Gates open.", Inches(8.85), Inches(3.45), Inches(2.5), Inches(0.5), size=14, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 22, total, dark=True)

    return d.save(OUT)


if __name__ == "__main__":
    build()
