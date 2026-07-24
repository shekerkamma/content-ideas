#!/usr/bin/env python3
"""Build the branded executive Reddit fact-check dossier."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN_DIR = Path(__file__).resolve().parent
PPTXKIT = Path("/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(PPTXKIT))

from pptxkit import Deck, Inches, PP_ALIGN  # noqa: E402


OUT = RUN_DIR / "reddit-factcheck-dossier-branded-draft.pptx"
CLAIM_PACK = RUN_DIR / "claim-pack.json"
ANNOTATED_DECK = RUN_DIR / "agent-validation-authority-reddit-factchecked-draft.pptx"


def load_claims() -> list[dict]:
    return json.loads(CLAIM_PACK.read_text(encoding="utf-8"))["claims"]


def slide_num(locator: str) -> int:
    match = re.search(r"\b(?:Slide|Section)\s+(\d+)\b", locator, re.I)
    return int(match.group(1)) if match else 0


def display_id(value: str) -> str:
    match = re.search(r"(\d+)$", value)
    return f"C-{int(match.group(1)):03d}" if match else value.upper()


def short(text: str, limit: int = 120) -> str:
    text = re.sub(r"\s+", " ", text).strip().replace("*", "")
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "..."


def evidence_label(claim: dict) -> str:
    if claim["evidence_need"] == "primary_required":
        return "Primary source required"
    if claim["evidence_need"] == "mixed":
        return "Mixed: Reddit + primary"
    return "Needs Reddit evidence"


def claim_priority(claim: dict) -> int:
    text = claim["claim"].lower()
    score = 0
    if claim.get("primary_source_required"):
        score += 3
    if claim["evidence_need"] == "mixed":
        score += 2
    if any(term in text for term in ["gartner", "sr 26-2", "occ", "fdic", "fed", "nist", "iso"]):
        score += 3
    if re.search(r"\d|%|\$|figure|priced|80\\%|40\\%", text):
        score += 2
    if any(term in text for term in ["klarna", "wendy", "mercedes", "home depot", "big 4", "harvey"]):
        score += 2
    return score


def title_slide(d: Deck) -> None:
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.rect(s, Inches(9.6), 0, Inches(3.73), d.H, b.NAVY_2)
    d.text(s, "REDDIT FACT-CHECK DOSSIER", d.M, Inches(0.8), Inches(7.6), Inches(0.3), size=14, color=b.TEAL, bold=True)
    d.text(s, "Agent Validation & Assurance Authority", d.M, Inches(1.35), Inches(8.6), Inches(1.35), size=34, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.65), Inches(1.7), Inches(0.06), b.TEAL)
    d.text(
        s,
        "Draft executive summary of claim triage and Reddit evidence requirements. "
        "The annotated source deck is generated separately and remains the working review copy.",
        d.M,
        Inches(3.05),
        Inches(8.1),
        Inches(0.72),
        size=15,
        color=b.LIGHT_TEAL,
        shrink=True,
    )
    d.text(s, f"Status: DRAFT | Built {date.today().isoformat()}", d.M, Inches(6.55), Inches(4.8), Inches(0.3), size=11, color=b.GOLD, bold=True)
    d.text(s, "Reddit evidence pending", Inches(9.95), Inches(1.0), Inches(2.7), Inches(0.95), size=20, color=b.WHITE, bold=True, shrink=True)
    d.text(s, "Do not treat this as a completed factual verdict until Reddit threads are captured and reviewed.", Inches(9.95), Inches(2.05), Inches(2.55), Inches(1.2), size=13, color=b.LIGHT_TEAL, shrink=True)


def summary_slide(d: Deck, claims: list[dict]) -> None:
    b = d.b
    counts = Counter(c["evidence_need"] for c in claims)
    s = d.slide(fill=b.SOFT)
    d.header(s, "Executive Verdict: Evidence Collection Ready", "Claim extraction is complete; Reddit verification is the next gate.")
    metrics = [
        (str(len(claims)), "Claims extracted", b.GOLD),
        (str(counts["reddit_evidence"]), "Need Reddit evidence", b.TEAL),
        (str(counts["primary_required"]), "Primary-source only", b.CORAL),
        (str(counts["mixed"]), "Mixed evidence claims", b.AMBER),
    ]
    x = d.M
    for value, label, color in metrics:
        d.rect(s, x, Inches(1.85), Inches(2.85), Inches(1.15), b.NAVY, radius=0.08, shadow=True)
        d.text(s, value, x + Inches(0.18), Inches(2.04), Inches(1.05), Inches(0.38), size=26, color=color, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, label, x + Inches(0.18), Inches(2.48), Inches(2.48), Inches(0.26), size=11, color=b.WHITE, align=PP_ALIGN.CENTER, shrink=True)
        x += Inches(3.05)
    bullets = [
        "The source deck has an annotated review copy with claim rails and appended Fact Check Notes slides.",
        "Most claims are market-language, pain, adoption, and positioning claims where Reddit can provide useful operator evidence.",
        "Numeric, regulatory, named-company, and date claims must remain blocked until primary sources are attached.",
        "No Reddit thread JSON is currently attached, so the dossier is draft rather than reviewed.",
    ]
    d.text(s, [{"text": item, "bullet": True, "space_before": 8, "size": 15} for item in bullets], d.M, Inches(3.45), d.CW, Inches(2.2), shrink=True)
    d.footer(s, 2, 8)


def method_slide(d: Deck) -> None:
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, "Reddit Evidence Has Clear Limits", "Use Reddit to validate community language and pain; use primary sources for hard facts.")
    columns = [
        ("Reddit Can Support", ["Operator pain and objections", "Practitioner language", "Vendor complaints", "Demand signals", "Repeated failure themes"], b.TEAL),
        ("Reddit Cannot Prove Alone", ["Market-size numbers", "Regulatory interpretation", "Named-company facts", "Funding/headcount/status", "Forecasts and dated claims"], b.CORAL),
        ("Required Output Standard", ["Claim ID traceability", "Source URL metadata", "Short evidence rationale", "Limits stated clearly", "No opinion-only verdicts"], b.GOLD),
    ]
    x = d.M
    for title, items, color in columns:
        d.rect(s, x, Inches(1.85), Inches(3.9), Inches(4.55), b.SOFT, radius=0.04, shadow=True)
        d.rect(s, x, Inches(1.85), Inches(3.9), Inches(0.14), color)
        d.text(s, title, x + Inches(0.22), Inches(2.18), Inches(3.45), Inches(0.52), size=14, color=b.NAVY, bold=True, shrink=True)
        d.text(s, [{"text": item, "bullet": True, "space_before": 7, "size": 12} for item in items], x + Inches(0.28), Inches(2.84), Inches(3.35), Inches(2.75), shrink=True)
        x += Inches(4.15)
    d.footer(s, 3, 8)


def triage_slide(d: Deck, claims: list[dict]) -> None:
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, "Claim Triage Prioritizes Reddit Review", "Highest-risk claims combine public facts, dates, named entities, or quantified assertions.")
    by_slide: dict[int, list[dict]] = defaultdict(list)
    for claim in claims:
        by_slide[slide_num(claim["locator"])].append(claim)
    rows = sorted(by_slide.items(), key=lambda pair: pair[0])[:14]
    max_count = max(len(items) for _, items in rows)
    y = 1.8
    for slide, items in rows:
        primary = sum(1 for item in items if item["evidence_need"] == "primary_required")
        mixed = sum(1 for item in items if item["evidence_need"] == "mixed")
        reddit = len(items) - primary - mixed
        d.text(s, f"S{slide}", d.M, Inches(y + 0.03), Inches(0.48), Inches(0.22), size=8.5, color=b.MUTED, bold=True)
        x = d.M + Inches(0.58)
        bar_w = Inches(8.9) * len(items) / max_count
        d.rect(s, x, Inches(y), bar_w, Inches(0.18), b.TEAL)
        if primary:
            d.rect(s, x + bar_w, Inches(y), Inches(0.34 * primary), Inches(0.18), b.CORAL)
        if mixed:
            d.rect(s, x + bar_w + Inches(0.34 * primary), Inches(y), Inches(0.34 * mixed), Inches(0.18), b.AMBER)
        d.text(s, f"{len(items)} claims  |  Reddit {reddit}  Primary {primary}  Mixed {mixed}", x + Inches(9.15), Inches(y - 0.04), Inches(2.3), Inches(0.26), size=8.5, color=b.INK, shrink=True)
        y += 0.34
    d.text(s, "Color key: teal = Reddit evidence; coral = primary source required; amber = mixed.", d.M, Inches(6.74), d.CW, Inches(0.25), size=10.5, color=b.MUTED)
    d.footer(s, 4, 8)


def priority_claims_slide(d: Deck, claims: list[dict]) -> None:
    b = d.b
    s = d.slide(fill=b.SOFT)
    d.header(s, "Priority Checks Before Reviewed Status", "These claims create the most credibility risk if unsupported.")
    priority = sorted(claims, key=claim_priority, reverse=True)[:6]
    y = 1.75
    for claim in priority:
        color = b.CORAL if claim.get("primary_source_required") else b.AMBER if claim["evidence_need"] == "mixed" else b.TEAL
        d.rect(s, d.M, Inches(y), d.CW, Inches(0.74), b.WHITE, radius=0.04, shadow=True)
        d.rect(s, d.M, Inches(y), Inches(0.12), Inches(0.74), color)
        d.text(s, display_id(claim["id"]), d.M + Inches(0.25), Inches(y + 0.15), Inches(0.78), Inches(0.28), size=8.5, color=color, bold=True)
        d.text(s, short(claim["claim"], 118), d.M + Inches(1.05), Inches(y + 0.13), Inches(7.5), Inches(0.34), size=9.5, color=b.INK, bold=True, shrink=True)
        d.text(s, f"{claim['locator']} | {evidence_label(claim)}", d.M + Inches(8.75), Inches(y + 0.17), Inches(2.95), Inches(0.3), size=7.5, color=b.MUTED, shrink=True)
        y += 0.82
    d.footer(s, 5, 8)


def reddit_discovery_slide(d: Deck, claims: list[dict]) -> None:
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, "Reddit Discovery Pack: Start With These Queries", "These queries are generated from the deck claims and should feed thread extraction.")
    reddit_claims = [c for c in claims if c["evidence_need"] in {"reddit_evidence", "mixed"}][:10]
    y = 1.75
    for claim in reddit_claims[:8]:
        d.text(s, display_id(claim["id"]), d.M, Inches(y), Inches(0.62), Inches(0.2), size=8.5, color=b.TEAL, bold=True)
        d.text(s, short(claim["reddit_query"], 150), d.M + Inches(0.75), Inches(y), Inches(10.95), Inches(0.22), size=9.5, color=b.INK, shrink=True)
        y += 0.48
    d.rect(s, d.M, Inches(6.15), d.CW, Inches(0.52), b.NAVY)
    d.text(s, "Next action: capture Reddit URLs/JSON, rerun evidence scoring, regenerate annotated deck and this dossier as reviewed.", d.M + Inches(0.2), Inches(6.3), d.CW - Inches(0.4), Inches(0.18), size=10.5, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 6, 8)


def artifacts_slide(d: Deck) -> None:
    b = d.b
    s = d.slide(fill=b.SOFT)
    d.header(s, "Delivery Artifacts Are Split By Use Case", "Source-review deck for edits; executive dossier for decision and prioritization.")
    cards = [
        ("Annotated Source Deck", "Original PPTX review copy with fact-check rails and Fact Check Notes slides.", "agent-validation-authority-reddit-factchecked-draft.pptx", b.TEAL),
        ("Evidence Report", "Markdown audit trail with every claim, evidence need, query, and limitation.", "reddit-factcheck-report.md", b.GOLD),
        ("Machine Artifacts", "JSON source for repeatable scoring and deck regeneration.", "claim-pack.json / document-segments.json", b.AMBER),
    ]
    y = 1.95
    for title, desc, file_name, color in cards:
        d.rect(s, d.M, Inches(y), d.CW, Inches(1.05), b.WHITE, radius=0.05, shadow=True)
        d.rect(s, d.M, Inches(y), Inches(0.15), Inches(1.05), color)
        d.text(s, title, d.M + Inches(0.35), Inches(y + 0.16), Inches(3.0), Inches(0.28), size=15, color=b.NAVY, bold=True, shrink=True)
        d.text(s, desc, d.M + Inches(3.55), Inches(y + 0.18), Inches(4.5), Inches(0.35), size=11, color=b.INK, shrink=True)
        d.text(s, file_name, d.M + Inches(8.3), Inches(y + 0.15), Inches(3.55), Inches(0.45), size=8.2, color=b.MUTED, bold=True, shrink=True)
        y += 1.28
    d.footer(s, 7, 8)


def close_slide(d: Deck) -> None:
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.text(s, "DECISION", d.M, Inches(0.75), Inches(2.2), Inches(0.28), size=13, color=b.TEAL, bold=True)
    d.text(s, "Move From Claim Extraction To Evidence Review", d.M, Inches(1.25), Inches(9.8), Inches(1.0), size=29, color=b.WHITE, bold=True, shrink=True)
    d.text(
        s,
        [
            {"text": "Keep the annotated source deck as the working edit layer.", "bullet": True, "space_before": 10, "size": 18, "color": b.LIGHT_TEAL},
            {"text": "Attach Reddit thread JSON and primary sources for high-risk claims.", "bullet": True, "space_before": 10, "size": 18, "color": b.LIGHT_TEAL},
            {"text": "Regenerate reviewed outputs only after evidence inspection and PPTX QA.", "bullet": True, "space_before": 10, "size": 18, "color": b.LIGHT_TEAL},
        ],
        d.M,
        Inches(2.55),
        Inches(10.4),
        Inches(2.0),
        shrink=True,
    )
    d.rect(s, d.M, Inches(5.9), d.CW, Inches(0.55), b.GOLD)
    d.text(s, "Current status: DRAFT, not a final Reddit-verified verdict.", d.M + Inches(0.22), Inches(6.06), d.CW - Inches(0.44), Inches(0.22), size=12.5, color=b.NAVY, bold=True)
    d.footer(s, 8, 8, dark=True)


def main() -> int:
    claims = load_claims()
    d = Deck(footer="Reddit Fact-Check Dossier | Agent Validation Authority")
    title_slide(d)
    summary_slide(d, claims)
    method_slide(d)
    triage_slide(d, claims)
    priority_claims_slide(d, claims)
    reddit_discovery_slide(d, claims)
    artifacts_slide(d)
    close_slide(d)
    d.save(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
