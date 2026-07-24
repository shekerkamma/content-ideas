#!/usr/bin/env python3
"""Build the expanded client-ready AEO strategy deck."""

from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL_DIR = Path("/home/shekerk/.claude/skills/branded-pptx-deck")
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from pptxkit import Deck, Inches, PP_ALIGN  # noqa: E402


RUN = Path(__file__).resolve().parents[1]
OUT = RUN / "final" / "agent-replacement-scorecard-aeo-expanded-client-reviewed.pptx"
FOOTER = "Agent Replacement Scorecard AEO | Expanded client deck | 2026-06-29"


def status() -> dict:
    return json.loads((RUN / "qa" / "evidence_sprint_status.json").read_text(encoding="utf-8"))


def bullet(items: list[str], size: float = 12.6) -> list[dict]:
    return [{"text": item, "bullet": True, "size": size, "space_before": 6} for item in items]


def card(d: Deck, s, x, y, w, h, title, body, accent=None, title_size=14, body_size=10.8):
    b = d.b
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(h), b.WHITE, line=b.GRID, radius=0.04, shadow=True)
    if accent:
        d.rect(s, Inches(x), Inches(y), Inches(0.08), Inches(h), accent)
    d.text(s, title, Inches(x + 0.2), Inches(y + 0.17), Inches(w - 0.4), Inches(0.28),
           size=title_size, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, Inches(x + 0.2), Inches(y + 0.58), Inches(w - 0.4), Inches(h - 0.72),
           size=body_size, color=b.INK, shrink=True)


def chip(d: Deck, s, x, y, w, label, fill, color=None):
    b = d.b
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(0.32), fill, radius=0.1)
    d.text(s, label, Inches(x + 0.1), Inches(y + 0.08), Inches(w - 0.2), Inches(0.14),
           size=8.5, color=color or b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)


def kpi(d: Deck, s, x, y, w, value, label, note):
    b = d.b
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(1.05), b.NAVY, radius=0.05)
    d.text(s, value, Inches(x + 0.18), Inches(y + 0.14), Inches(w - 0.36), Inches(0.3),
           size=20, color=b.GOLD, bold=True, shrink=True)
    d.text(s, label, Inches(x + 0.18), Inches(y + 0.49), Inches(w - 0.36), Inches(0.22),
           size=9.2, color=b.WHITE, bold=True, shrink=True)
    d.text(s, note, Inches(x + 0.18), Inches(y + 0.75), Inches(w - 0.36), Inches(0.2),
           size=7.5, color=b.LIGHT_TEAL, shrink=True)


def section(d: Deck, title: str, subtitle: str, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.text(s, f"SECTION {page:02d}", d.M, Inches(1.08), Inches(2.0), Inches(0.25), size=13, color=b.TEAL, bold=True)
    d.text(s, title, d.M, Inches(1.72), Inches(8.8), Inches(0.9), size=38, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.86), Inches(1.8), Inches(0.06), b.TEAL)
    d.text(s, subtitle, d.M, Inches(3.28), Inches(8.8), Inches(0.55), size=17, color=b.LIGHT_TEAL, shrink=True)
    d.footer(s, page, total, dark=True)
    return s


def two_col(d: Deck, title: str, subtitle: str, left_title: str, left_items: list[str],
            right_title: str, right_items: list[str], page: int, total: int):
    b = d.b
    s = d.slide(fill=b.SOFT)
    d.header(s, title, subtitle)
    card(d, s, 0.75, 1.78, 5.65, 4.35, left_title, "", b.TEAL, title_size=16)
    d.text(s, bullet(left_items, 12.2), Inches(1.0), Inches(2.48), Inches(5.05), Inches(3.15), shrink=True)
    card(d, s, 6.9, 1.78, 5.65, 4.35, right_title, "", b.GOLD, title_size=16)
    d.text(s, bullet(right_items, 12.2), Inches(7.15), Inches(2.48), Inches(5.05), Inches(3.15), shrink=True)
    d.footer(s, page, total)


def build() -> Path:
    st = status()
    c = st["counts"]
    g = st["gates"]
    d = Deck(footer=FOOTER)
    b = d.b
    total = 20

    # 1 cover
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(10.85), 0, Inches(2.48), d.H, b.NAVY_2)
    d.rect(s, Inches(10.85), 0, Inches(0.08), d.H, b.TEAL)
    d.text(s, "EXPANDED CLIENT STRATEGY DECK", d.M, Inches(0.85), Inches(6.7), Inches(0.25), size=13, color=b.TEAL, bold=True)
    d.text(s, "Agent Replacement\nScorecard", d.M, Inches(1.35), Inches(8.9), Inches(1.05), size=34, color=b.WHITE, bold=True, shrink=True)
    d.text(s, "AEO evidence, product blueprint, and execution plan",
           d.M, Inches(2.72), Inches(8.9), Inches(0.38), size=16.5, color=b.LIGHT_TEAL, shrink=True)
    d.rect(s, d.M, Inches(3.32), Inches(1.8), Inches(0.06), b.TEAL)
    d.text(s, "Reviewed draft based on partial evidence. Built for client discussion, not final market-proof claims.",
           d.M, Inches(3.72), Inches(8.2), Inches(0.45), size=14.5, color=b.WHITE, shrink=True)
    chip(d, s, 0.6, 4.5, 1.85, "PARTIAL EVIDENCE", b.GOLD, b.NAVY)
    chip(d, s, 2.65, 4.5, 1.65, "20 SLIDES", b.TEAL, b.NAVY)
    chip(d, s, 4.5, 4.5, 2.0, "REVIEWED DRAFT", b.NAVY_2)
    d.footer(s, 1, total, dark=True)

    # 2 agenda
    s = d.slide(fill=b.WHITE)
    d.header(s, "The deck now has a full consulting spine", "Thin decks skip the work. This version separates answer, evidence, model, execution, and ask.")
    agenda = [
        ("1", "Answer", "The wedge and the current decision."),
        ("2", "Evidence", "What we have, what is still missing, and how to use it."),
        ("3", "Patterns", "The semantic mechanisms that shape the scorecard."),
        ("4", "Product", "The diagnostic dimensions, verdicts, and example outputs."),
        ("5", "Execution", "AEO content, workflow kit, roadmap, guardrails, and next asks."),
    ]
    for i, (num, title, body) in enumerate(agenda):
        x = 0.85 + i * 2.48
        d.rect(s, Inches(x), Inches(2.0), Inches(0.48), Inches(0.48), b.NAVY, radius=0.08)
        d.text(s, num, Inches(x + 0.15), Inches(2.13), Inches(0.16), Inches(0.14), size=11, color=b.WHITE, bold=True)
        card(d, s, x, 2.75, 2.12, 2.35, title, body, b.TEAL if i < 2 else b.GOLD, title_size=14, body_size=10.5)
    d.footer(s, 2, total)

    section(d, "The Answer", "The useful thesis is layer compression, not blanket SaaS replacement.", 3, total)

    # 4 BLUF
    s = d.slide(fill=b.SOFT)
    d.header(s, "BLUF: AI compresses the workflow layer first", "The strongest evidence-backed claim is narrower and more useful than “agents replace SaaS.”")
    d.rect(s, d.M, Inches(1.9), d.CW, Inches(1.08), b.NAVY, radius=0.04)
    d.text(s, "Agents pressure add-ons, drafting, triage, and interface workflows. Records systems survive longer.",
           Inches(0.9), Inches(2.18), Inches(11.4), Inches(0.32), size=13.5, color=b.WHITE, bold=True, shrink=True)
    card(d, s, 0.8, 3.45, 3.65, 2.1, "What changes", "The user no longer needs to operate every SaaS screen to get the outcome.", b.TEAL)
    card(d, s, 4.85, 3.45, 3.65, 2.1, "What survives", "Records, permissions, audit, governed data, deep integrations, and accountability.", b.ACCENT)
    card(d, s, 8.9, 3.45, 3.65, 2.1, "What to sell", "A diagnostic that shows replace, renegotiate, enrich, or avoid by workflow layer.", b.GOLD)
    d.footer(s, 4, total)

    # 5 business objective
    two_col(
        d,
        "The goal is recommendation eligibility",
        "AEO is useful when it changes what answer engines recommend to buyers.",
        "Do not optimize for",
        ["Vanity mention counts", "Keyword ranking without buyer intent", "Target-seeded prompts", "Generic AI-replaces-SaaS thought leadership"],
        "Optimize for",
        ["Winning the recommendation", "Owning buyer-language questions", "Earning citation eligibility", "Turning evidence into a productized diagnostic"],
        5,
        total,
    )

    section(d, "Evidence Posture", "The current evidence is useful, but the deck must not overclaim it.", 6, total)

    # 7 evidence scorecard
    s = d.slide(fill=b.WHITE)
    d.header(s, "Evidence is enough for v0, not enough for proof", "Proceed with a reviewed working model while keeping the evidence gate open.")
    kpi(d, s, 0.75, 1.85, 2.1, str(c["reddit_buyer_language_rows"]), "Reddit rows", "Buyer language")
    kpi(d, s, 3.05, 1.85, 2.1, str(c["independent_ai_answer_captures"]), "AI captures", "Independent")
    kpi(d, s, 5.35, 1.85, 2.1, str(c["independent_answer_engines"]), "Engines", "Need 3")
    kpi(d, s, 7.65, 1.85, 2.1, str(c["pattern_candidates"]), "Patterns", "Review needed")
    kpi(d, s, 9.95, 1.85, 2.1, str(c["target_seeded_capture_ids"]), "Seeded rows", "Exclude from claims")
    rows = [
        ("Reddit buyer-language minimum", g["reddit_buyer_language_min_5"], "Passed"),
        ("20 independent AI-answer captures", g["independent_ai_answer_captures_min_20"], "Open"),
        ("3 independent answer engines", g["independent_answer_engines_min_3"], "Open"),
        ("No promoted target-seeded patterns", g["no_promoted_target_seeded_patterns"], "Passed"),
    ]
    y = 3.55
    for label, ok, state in rows:
        d.rect(s, d.M, Inches(y), d.CW, Inches(0.48), b.LIGHT_TEAL if ok else b.SOFT, line=b.TEAL if ok else b.AMBER, radius=0.03)
        d.text(s, label, Inches(0.85), Inches(y + 0.13), Inches(7.6), Inches(0.18), size=12.2, color=b.INK, bold=True)
        chip(d, s, 10.7, y + 0.07, 1.25, state.upper(), b.TEAL if ok else b.AMBER, b.NAVY)
        y += 0.62
    d.footer(s, 7, total)

    # 8 evidence usage
    two_col(
        d,
        "Use the evidence differently by source type",
        "AI answers, Reddit language, and scorecard seeds have different jobs.",
        "Use for claims",
        ["Independent Claude and Gemini captures", "Reddit objections and buyer language", "Non-target-seeded prompts", "Patterns that survive semantic review"],
        "Do not use for claims",
        ["Target-seeded scorecard captures", "Keyword matches alone", "Thread counts as market proof", "OpenAI/Perplexity consensus until captures exist"],
        8,
        total,
    )

    section(d, "Patterns", "The scorecard should be built from mechanisms, not loose themes.", 9, total)

    # 10 six patterns
    s = d.slide(fill=b.SOFT)
    d.header(s, "Six semantic patterns become the decision logic", "These are the mechanisms the evidence repeatedly points toward.")
    patterns = [
        ("Add-on collapse", "Bolt-on assistants and point tools are exposed.", b.TEAL),
        ("Human sign-off", "High-risk decisions keep accountability with people.", b.AMBER),
        ("Data moat", "Systems survive when they own durable context.", b.ACCENT),
        ("Pilotability", "Claims need bounded measurable tests.", b.GOLD),
        ("Renewal leverage", "Agent performance changes procurement pressure.", b.CORAL),
        ("Seat compression", "Fewer users need to work inside the SaaS UI.", b.DARK_TEAL),
    ]
    for i, (title, body, color) in enumerate(patterns):
        card(d, s, 0.75 + (i % 3) * 4.1, 1.75 + (i // 3) * 2.02, 3.62, 1.5, title, body, color)
    d.footer(s, 10, total)

    # 11 pattern-to-action
    s = d.slide(fill=b.WHITE)
    d.header(s, "Each pattern maps to a client action", "The output should tell the client what to build, buy, replace, or renegotiate.")
    rows = [
        ("Add-on collapse", "Inventory add-ons and assistant modules", "Renegotiate or remove exposed modules"),
        ("Human sign-off", "Map decisions that require accountability", "Design checkpoints and escalation paths"),
        ("Data moat", "Identify records, permissions, audit needs", "Keep/enrich durable systems"),
        ("Pilotability", "Create historical replay test set", "Run 30-day agent-vs-human pilot"),
        ("Seat compression", "Model users removed from the workflow UI", "Pressure seat commitments at renewal"),
    ]
    y = 1.75
    for pattern, diagnostic, action in rows:
        d.rect(s, d.M, Inches(y), d.CW, Inches(0.66), b.SOFT, line=b.GRID, radius=0.03)
        d.text(s, pattern, Inches(0.85), Inches(y + 0.18), Inches(2.25), Inches(0.18), size=11.5, color=b.NAVY, bold=True)
        d.text(s, diagnostic, Inches(3.35), Inches(y + 0.18), Inches(4.1), Inches(0.18), size=10.8, color=b.INK, shrink=True)
        d.text(s, action, Inches(7.95), Inches(y + 0.18), Inches(4.0), Inches(0.18), size=10.8, color=b.INK, shrink=True)
        y += 0.82
    d.footer(s, 11, total)

    section(d, "Product Blueprint", "Turn the evidence into a diagnostic, not a generic report.", 12, total)

    # 13 model
    s = d.slide(fill=b.WHITE)
    d.header(s, "The v0 scorecard needs five dimensions", "Each dimension produces both a score and a concrete operating implication.")
    dims = [
        ("Workflow determinism", "Repeatable, rule-bound, high-volume work is exposed."),
        ("Data moat", "Owned records, governance, and audit trails defend the platform."),
        ("Human sign-off", "Risk and accountability define the automation boundary."),
        ("Pilotability", "The buyer needs a bounded test before procurement action."),
        ("Renewal leverage", "Seat, add-on, and module pressure creates commercial value."),
    ]
    for i, (title, body) in enumerate(dims):
        d.rect(s, Inches(0.8), Inches(1.75 + i * 0.82), Inches(0.45), Inches(0.42), b.NAVY, radius=0.07)
        d.text(s, str(i + 1), Inches(0.94), Inches(1.86 + i * 0.82), Inches(0.15), Inches(0.12), size=10, color=b.WHITE, bold=True)
        d.text(s, title, Inches(1.45), Inches(1.78 + i * 0.82), Inches(3.1), Inches(0.2), size=13, color=b.NAVY, bold=True)
        d.text(s, body, Inches(4.8), Inches(1.78 + i * 0.82), Inches(7.3), Inches(0.22), size=11.2, color=b.INK, shrink=True)
    d.footer(s, 13, total)

    # 14 verdicts
    s = d.slide(fill=b.SOFT)
    d.header(s, "The diagnostic has four verdicts", "The language must be actionable without implying every workflow is replaceable.")
    verdicts = [
        ("Replace", "Automate the exposed workflow layer.", b.CORAL),
        ("Renegotiate", "Keep platform, reduce seats/add-ons.", b.GOLD),
        ("Enrich", "Use agents around durable systems.", b.TEAL),
        ("Avoid", "Keep humans accountable for risk.", b.MUTED),
    ]
    for i, (title, body, color) in enumerate(verdicts):
        card(d, s, 0.85 + (i % 2) * 6.0, 1.85 + (i // 2) * 1.78, 5.35, 1.25, title, body, color, title_size=16, body_size=12)
    d.rect(s, d.M, Inches(5.72), d.CW, Inches(0.5), b.NAVY, radius=0.04)
    d.text(s, "Every verdict includes exposed layer, surviving layer, checkpoint, pilot metric, and renewal implication.",
           Inches(0.9), Inches(5.88), Inches(11.4), Inches(0.18), size=11.4, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 14, total)

    # 15 example workflows
    s = d.slide(fill=b.WHITE)
    d.header(s, "Example workflow reads", "Illustrative v0 outputs, not final scored client results.")
    examples = [
        ("Conversational support", "Renegotiate", "Helpdesk remains; tier-1 support seats and bot add-ons compress."),
        ("Doc summarization", "Replace", "Office suite remains; drafting/summarization add-ons are exposed."),
        ("Legal drafting", "Enrich", "Research corpus survives; agent accelerates first draft."),
        ("Creative generation", "Renegotiate", "DAM remains; production seats and variant tooling compress."),
    ]
    y = 1.75
    for workflow, verdict, implication in examples:
        d.rect(s, d.M, Inches(y), d.CW, Inches(0.75), b.SOFT, line=b.GRID, radius=0.03)
        d.text(s, workflow, Inches(0.85), Inches(y + 0.21), Inches(2.7), Inches(0.2), size=11.8, color=b.NAVY, bold=True)
        chip(d, s, 3.9, y + 0.18, 1.45, verdict.upper(), b.TEAL if verdict == "Enrich" else b.GOLD if verdict == "Renegotiate" else b.CORAL, b.NAVY)
        d.text(s, implication, Inches(5.75), Inches(y + 0.2), Inches(6.2), Inches(0.22), size=11, color=b.INK, shrink=True)
        y += 0.94
    d.footer(s, 15, total)

    section(d, "AEO Execution", "The content system should make the scorecard recommendation-eligible.", 16, total)

    # 17 content plan
    s = d.slide(fill=b.WHITE)
    d.header(s, "Build pages around unbranded buyer questions", "Answer engines need crawlable, specific pages that match how buyers ask the question.")
    pages = [
        ("Customer support", "Where are agents useful, where do seats compress, where do humans stay?"),
        ("Document workflows", "When do drafting and summarization add-ons get replaced?"),
        ("Pilot design", "How should teams test an agent before replacing a workflow tool?"),
        ("Data moats", "Which SaaS workflows survive because they own records and governance?"),
        ("Renewal leverage", "How do teams use agents to renegotiate SaaS spend?"),
    ]
    for i, (topic, question) in enumerate(pages):
        y = 1.72 + i * 0.78
        d.rect(s, Inches(0.78), Inches(y), Inches(2.2), Inches(0.38), b.NAVY, radius=0.03)
        d.text(s, topic, Inches(0.92), Inches(y + 0.1), Inches(1.9), Inches(0.14), size=9.8, color=b.WHITE, bold=True, shrink=True)
        d.text(s, question, Inches(3.25), Inches(y + 0.08), Inches(8.7), Inches(0.18), size=11.2, color=b.INK, shrink=True)
    d.footer(s, 17, total)

    # 18 workflow kit
    s = d.slide(fill=b.SOFT)
    d.header(s, "The workflow kit compounds skills", "The operating model is repeatable evidence collection plus semantic review.")
    kit = [
        ("Prompt pack", "Generate non-target-seeded buyer questions."),
        ("AI captures", "Collect answers across engines with explicit gates."),
        ("Reddit wedge", "Extract skepticism, objections, workarounds, and comparison frames."),
        ("Pattern miner", "Map captures to semantic mechanisms."),
        ("Scorecard builder", "Turn reviewed patterns into diagnostic outputs."),
        ("QA gate", "Block overclaims until evidence thresholds pass."),
    ]
    for i, (title, body) in enumerate(kit):
        card(d, s, 0.75 + (i % 3) * 4.1, 1.72 + (i // 3) * 1.95, 3.62, 1.38, title, body, b.TEAL if i < 3 else b.GOLD)
    d.footer(s, 18, total)

    # 19 roadmap and risks
    two_col(
        d,
        "Roadmap: launch v0 while hardening proof",
        "The next move is productization plus evidence completion.",
        "30-day roadmap",
        ["Package v0 diagnostic and worksheet", "Publish five AEO pages", "Collect +10 independent captures", "Add one more answer engine", "Run semantic review and falsification"],
        "Risks to manage",
        ["Do not claim full AEO readiness", "Do not promote seeded captures", "Do not use keyword matching as proof", "Do not ignore buyer skepticism", "Do not skip citation/source strategy"],
        19,
        total,
    )

    # 20 decision ask
    s = d.slide(fill=b.NAVY)
    d.text(s, "DECISION ASK", d.M, Inches(0.8), Inches(2), Inches(0.24), size=13, color=b.TEAL, bold=True)
    d.text(s, "Approve the expanded v0\nlaunch path", d.M, Inches(1.25), Inches(8.6), Inches(1.0), size=29, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.42), Inches(1.8), Inches(0.06), b.TEAL)
    asks = [
        "Use the expanded deck as the client narrative.",
        "Build the interactive scorecard from the five-dimension model.",
        "Publish the first AEO page cluster around unbranded buyer questions.",
        "Keep evidence status as reviewed draft until 20 captures and 3 engines pass.",
    ]
    d.text(s, bullet(asks, 13.2), d.M, Inches(2.95), Inches(7.7), Inches(2.4), color=b.WHITE, shrink=True)
    d.rect(s, Inches(8.75), Inches(2.92), Inches(3.25), Inches(1.95), b.NAVY_2, radius=0.05)
    d.text(s, "Recommended posture", Inches(9.05), Inches(3.2), Inches(2.65), Inches(0.22), size=12.5, color=b.TEAL, bold=True)
    d.text(s, "Launch v0. Keep proof gates visible.", Inches(9.05), Inches(3.62), Inches(2.65), Inches(0.56), size=15.5, color=b.WHITE, bold=True, shrink=True)
    d.text(s, "Next: +10 captures + one engine.", Inches(9.05), Inches(4.34), Inches(2.65), Inches(0.24), size=9.5, color=b.LIGHT_TEAL, shrink=True)
    d.footer(s, 20, total, dark=True)

    return d.save(OUT)


if __name__ == "__main__":
    build()
