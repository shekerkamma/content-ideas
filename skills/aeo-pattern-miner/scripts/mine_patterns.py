#!/usr/bin/env python3
"""Mine AEO answer captures for semantic pattern candidates.

This script deliberately avoids exact keyword-to-pattern matching. It extracts
answer-level evidence units, compares them against richer concept anchors, and
emits a review brief for human/subagent semantic judgment.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse


CONCEPTS = {
    "seat-compression": {
        "label": "Seat Compression",
        "anchor": (
            "AI agents reduce paid user licenses, support seats, operator "
            "headcount, or per-seat software demand by completing the work "
            "that humans previously performed inside a SaaS interface."
        ),
        "question": "Does the answer describe fewer humans or paid seats needed to complete the same workflow?",
    },
    "add-on-collapse": {
        "label": "Add-On Collapse",
        "anchor": (
            "AI absorbs assistant modules, point tools, bolt-on workflow "
            "products, or specialist add-ons while the buyer keeps the core "
            "platform or system of record."
        ),
        "question": "Does the answer distinguish the durable core platform from replaceable add-ons or modules?",
    },
    "workflow-layer-replacement": {
        "label": "Workflow Layer Replacement",
        "anchor": (
            "AI replaces the task execution layer of a workflow while records, "
            "databases, inventory systems, CRMs, ERPs, or compliance systems "
            "remain as durable systems underneath."
        ),
        "question": "Does the answer separate workflow execution from the underlying record system?",
    },
    "data-moat-survival": {
        "label": "Data Moat Survival",
        "anchor": (
            "Platforms survive when proprietary data, permissions, historical "
            "records, audit trails, governance, or operational context are the "
            "source of defensibility."
        ),
        "question": "Does the answer explain why a data-rich platform survives rather than gets replaced?",
    },
    "human-signoff-boundary": {
        "label": "Human Sign-Off Boundary",
        "anchor": (
            "AI drafts, triages, recommends, or executes low-risk work while "
            "humans retain accountability for regulated, ambiguous, high-risk, "
            "or customer-sensitive decisions."
        ),
        "question": "Does the answer define where human approval or accountability remains necessary?",
    },
    "interface-collapse": {
        "label": "Interface Collapse",
        "anchor": (
            "Users stop navigating dashboards, search interfaces, reports, "
            "forms, or multi-screen tools because a natural-language answer "
            "layer gives them the needed outcome directly."
        ),
        "question": "Does the answer imply the user interface becomes less important than the answer/action layer?",
    },
    "renewal-leverage": {
        "label": "Renewal Leverage",
        "anchor": (
            "A credible agent alternative changes procurement leverage, "
            "renewal negotiations, pricing models, seat commitments, outcome "
            "pricing, or vendor consolidation decisions."
        ),
        "question": "Does the answer connect agent capability to procurement, pricing, or renewal pressure?",
    },
    "pilotability": {
        "label": "Pilotability",
        "anchor": (
            "The workflow can be tested in a bounded pilot using historical "
            "examples, parallel runs, measurable outputs, cycle time, exception "
            "rate, resolution rate, or human escalation quality."
        ),
        "question": "Does the answer describe a concrete way to test the replacement or renegotiation thesis?",
    },
    "citation-authority-gap": {
        "label": "Citation Authority Gap",
        "anchor": (
            "AI answers rely on external authorities, cited pages, comparison "
            "sources, community discussions, or trusted domains; the target "
            "asset must earn citation eligibility in those answer surfaces."
        ),
        "question": "Does the answer reveal which authorities or sources shape the recommendation?",
    },
}


STOPWORDS = {
    "a",
    "about",
    "above",
    "across",
    "after",
    "again",
    "against",
    "all",
    "also",
    "am",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "because",
    "been",
    "before",
    "being",
    "between",
    "both",
    "but",
    "by",
    "can",
    "could",
    "did",
    "do",
    "does",
    "doing",
    "down",
    "during",
    "each",
    "few",
    "for",
    "from",
    "further",
    "had",
    "has",
    "have",
    "having",
    "he",
    "her",
    "here",
    "hers",
    "him",
    "his",
    "how",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "itself",
    "just",
    "me",
    "more",
    "most",
    "my",
    "no",
    "nor",
    "not",
    "of",
    "off",
    "on",
    "once",
    "only",
    "or",
    "other",
    "our",
    "out",
    "over",
    "own",
    "same",
    "she",
    "should",
    "so",
    "some",
    "such",
    "than",
    "that",
    "the",
    "their",
    "them",
    "then",
    "there",
    "these",
    "they",
    "this",
    "those",
    "through",
    "to",
    "too",
    "under",
    "until",
    "up",
    "very",
    "was",
    "we",
    "were",
    "what",
    "when",
    "where",
    "which",
    "while",
    "who",
    "why",
    "will",
    "with",
    "within",
    "you",
    "your",
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def domain(url: str) -> str:
    parsed = urlparse(url if "://" in url else f"https://{url}")
    return parsed.netloc.lower().removeprefix("www.")


def capture_text(run_dir: Path, capture: dict) -> str:
    return (run_dir / capture["answer_text_path"]).read_text(encoding="utf-8")


def evidence_type(capture: dict) -> str:
    method = (capture.get("raw_metadata") or {}).get("collection_method", "")
    engine = capture.get("engine", "")
    if method == "manual_live_capture":
        return "manual_live_capture"
    if engine == "scorecard_seed" or method == "scorecard_seed":
        return "scorecard_seed"
    if engine == "manual_placeholder" or method == "manual_placeholder":
        return "placeholder"
    if engine == "sample":
        return "sample"
    return "unknown"


def tokenize(text: str) -> Counter[str]:
    tokens = re.findall(r"[a-z][a-z0-9-]{2,}", text.lower())
    normalized: list[str] = []
    for token in tokens:
        if token in STOPWORDS:
            continue
        if token.endswith("ies") and len(token) > 4:
            token = f"{token[:-3]}y"
        elif token.endswith("s") and len(token) > 4:
            token = token[:-1]
        normalized.append(token)
    return Counter(normalized)


def cosine(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    numerator = sum(weight * right.get(token, 0) for token, weight in left.items())
    left_norm = math.sqrt(sum(weight * weight for weight in left.values()))
    right_norm = math.sqrt(sum(weight * weight for weight in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def split_evidence_units(text: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", text).strip()
    pieces = re.split(r"(?<=[.!?])\s+|(?:\s+-\s+)|(?:\n+)", cleaned)
    units = []
    for piece in pieces:
        piece = piece.strip(" -\t")
        if len(piece) >= 45:
            units.append(piece)
    return units or ([cleaned] if cleaned else [])


def capture_seeded_by_target(capture: dict, target_brand: str, text: str) -> bool:
    method = evidence_type(capture)
    if method in {"scorecard_seed", "placeholder", "sample"}:
        return True
    query = capture.get("query", "")
    cited_domains = {domain(url) for url in capture.get("citation_urls", [])}
    target_domain_only = bool(cited_domains) and cited_domains == {"shekerkamma.github.io"}
    target_named = target_brand.lower() in text.lower()
    target_prompted = target_brand.lower() in query.lower()
    return target_named and (target_prompted or target_domain_only)


def confidence_for(
    capture_ids: set[str],
    engines: set[str],
    source_domains: set[str],
    evidence_types: set[str],
    target_seeded_count: int,
) -> tuple[str, str]:
    if not capture_ids:
        return "none", "No supporting evidence units."
    if evidence_types - {"manual_live_capture"}:
        return "low", "Contains seed, placeholder, sample, or unknown evidence."
    if target_seeded_count:
        return "low", "Capture text or prompts are target-seeded; requires independent prompts."
    if len(capture_ids) >= 5 and len(engines) >= 3 and len(source_domains) >= 2:
        return "high", "Repeated across independent captures, engines, and cited domains."
    if len(capture_ids) >= 3 and len(engines) >= 2:
        return "medium", "Repeated across multiple captures and engines."
    return "low", "Needs more independent captures before promotion."


def extract_units(run_dir: Path, captures: list[dict], queries: dict[str, dict], target_brand: str) -> list[dict]:
    units: list[dict] = []
    for capture in captures:
        query = queries.get(capture["query_id"], {})
        capture = {**capture, "query": query.get("query", "")}
        text = capture_text(run_dir, capture)
        seeded = capture_seeded_by_target(capture, target_brand, text)
        urls = capture.get("citation_urls", [])
        domains = sorted({domain(url) for url in urls})
        for index, unit_text in enumerate(split_evidence_units(text), start=1):
            units.append(
                {
                    "unit_id": f"{capture['capture_id']}_u{index:02d}",
                    "capture_id": capture["capture_id"],
                    "query_id": capture["query_id"],
                    "query": query.get("query", ""),
                    "query_intent": query.get("intent", ""),
                    "query_cluster": query.get("cluster", ""),
                    "engine": capture.get("engine", ""),
                    "evidence_type": evidence_type(capture),
                    "target_seeded": seeded,
                    "citation_domains": domains,
                    "text": unit_text,
                    "tokens": tokenize(unit_text),
                }
            )
    return units


def score_concepts(units: list[dict]) -> list[dict]:
    concept_vectors = {slug: tokenize(data["anchor"]) for slug, data in CONCEPTS.items()}
    scored: dict[str, list[dict]] = defaultdict(list)
    for unit in units:
        for slug, vector in concept_vectors.items():
            score = cosine(unit["tokens"], vector)
            if score >= 0.12:
                scored[slug].append(
                    {
                        "unit_id": unit["unit_id"],
                        "capture_id": unit["capture_id"],
                        "query": unit["query"],
                        "query_intent": unit["query_intent"],
                        "engine": unit["engine"],
                        "evidence_type": unit["evidence_type"],
                        "target_seeded": unit["target_seeded"],
                        "citation_domains": unit["citation_domains"],
                        "semantic_score": round(score, 3),
                        "text": unit["text"],
                    }
                )

    rows: list[dict] = []
    for slug, evidence in scored.items():
        evidence.sort(key=lambda row: row["semantic_score"], reverse=True)
        kept = evidence[:8]
        capture_ids = {row["capture_id"] for row in kept}
        engines = {row["engine"] for row in kept if row["engine"]}
        query_intents = {row["query_intent"] for row in kept if row["query_intent"]}
        evidence_types = {row["evidence_type"] for row in kept}
        domains = {item for row in kept for item in row["citation_domains"]}
        target_seeded_count = sum(1 for row in kept if row["target_seeded"])
        confidence, rationale = confidence_for(capture_ids, engines, domains, evidence_types, target_seeded_count)
        rows.append(
            {
                "pattern_id": slug,
                "label": CONCEPTS[slug]["label"],
                "description": CONCEPTS[slug]["anchor"],
                "review_question": CONCEPTS[slug]["question"],
                "capture_ids": sorted(capture_ids),
                "engines": sorted(engines),
                "query_intents": sorted(query_intents),
                "source_domains": sorted(domains),
                "evidence_types": sorted(evidence_types),
                "target_seeded_evidence_units": target_seeded_count,
                "semantic_evidence": kept,
                "confidence": confidence,
                "confidence_rationale": rationale,
                "review_status": "needs_semantic_review",
            }
        )
    rows.sort(
        key=lambda row: (
            {"high": 0, "medium": 1, "low": 2, "none": 3}[row["confidence"]],
            -len(row["capture_ids"]),
            row["label"],
        )
    )
    return rows


def semantic_clusters(rows: list[dict]) -> list[dict]:
    clusters = []
    for row in rows:
        clusters.append(
            {
                "cluster_id": f"cluster_{row['pattern_id']}",
                "label": row["label"],
                "method": "concept_anchor_cosine_similarity",
                "unit_ids": [item["unit_id"] for item in row["semantic_evidence"]],
                "capture_ids": row["capture_ids"],
                "query_intents": row["query_intents"],
                "requires_review": True,
            }
        )
    return clusters


def summarize(manifest: dict, captures: list[dict], units: list[dict]) -> dict:
    evidence_mix = Counter(evidence_type(capture) for capture in captures)
    cited_domains: Counter[str] = Counter()
    engine_counts: Counter[str] = Counter()
    target_seeded_units = 0
    for unit in units:
        engine_counts[unit["engine"]] += 1
        target_seeded_units += int(unit["target_seeded"])
        for item in unit["citation_domains"]:
            cited_domains[item] += 1
    return {
        "run_id": manifest.get("run_id", ""),
        "target_brand": manifest.get("target_brand", ""),
        "capture_count": len(captures),
        "evidence_unit_count": len(units),
        "target_seeded_evidence_units": target_seeded_units,
        "evidence_mix": dict(evidence_mix),
        "engine_counts": dict(engine_counts),
        "top_cited_domains": cited_domains.most_common(12),
        "method": "concept-anchor semantic scoring plus required subagent/human review",
    }


def mine(run_dir: Path) -> tuple[list[dict], list[dict], dict]:
    manifest = read_json(run_dir / "manifest.json")
    captures = read_jsonl(run_dir / "stage_outputs" / "answer_captures.jsonl")
    queries = {row["query_id"]: row for row in read_jsonl(run_dir / "stage_outputs" / "queries.jsonl")}
    target_brand = manifest.get("target_brand", "")
    units = extract_units(run_dir, captures, queries, target_brand)
    rows = score_concepts(units)
    summary = summarize(manifest, captures, units)
    for unit in units:
        unit.pop("tokens", None)
    return rows, units, summary


def render_report(rows: list[dict], summary: dict) -> str:
    lines = [
        f"# AEO Semantic Pattern Mining Report: {summary['target_brand']}",
        "",
        "## Purpose",
        "",
        "This report mines captured AI-answer evidence for semantic pattern candidates. It does not use exact keyword-to-pattern hits as the basis for claims. It extracts answer evidence units, scores them against concept anchors, and requires semantic review before promotion.",
        "",
        "## Evidence Base",
        "",
        f"- Run id: `{summary['run_id']}`",
        f"- Captures analyzed: {summary['capture_count']}",
        f"- Evidence units analyzed: {summary['evidence_unit_count']}",
        f"- Evidence mix: {json.dumps(summary['evidence_mix'], ensure_ascii=False)}",
        f"- Engine evidence units: {json.dumps(summary['engine_counts'], ensure_ascii=False)}",
        f"- Target-seeded evidence units: {summary['target_seeded_evidence_units']}",
        "",
        "## Pattern Candidates",
        "",
    ]
    if not rows:
        lines.append("No semantic pattern candidates found. Add more real AI-answer captures.")
    for row in rows:
        lines.extend(
            [
                f"### {row['label']} ({row['confidence']})",
                "",
                row["description"],
                "",
                f"- Review question: {row['review_question']}",
                f"- Confidence rationale: {row['confidence_rationale']}",
                f"- Evidence captures: {', '.join(row['capture_ids']) or 'none'}",
                f"- Engines: {', '.join(row['engines']) or 'none'}",
                f"- Query intents: {', '.join(row['query_intents']) or 'none'}",
                f"- Source domains: {', '.join(row['source_domains']) or 'none'}",
                f"- Evidence types: {', '.join(row['evidence_types']) or 'none'}",
                f"- Review status: {row['review_status']}",
                "",
                "Representative evidence:",
                "",
            ]
        )
        for evidence in row["semantic_evidence"][:3]:
            seeded = " target-seeded" if evidence["target_seeded"] else ""
            lines.append(
                f"- `{evidence['unit_id']}` ({evidence['engine']}, score {evidence['semantic_score']}{seeded}): {evidence['text']}"
            )
        lines.append("")
    lines.extend(["## Cited / Referenced Domains", ""])
    for term, count in summary["top_cited_domains"]:
        lines.append(f"- {term}: {count}")
    lines.extend(
        [
            "",
            "## Subagent Review Required",
            "",
            "Before using any pattern externally, send `working/subagent-review-brief.md` to independent reviewers. One reviewer should validate whether the evidence really supports each pattern. Another should try to falsify the pattern and identify missing competitor/source evidence.",
            "",
            "## How To Use This",
            "",
            "Promote a pattern only when semantic review agrees that the evidence supports the mechanism, the captures are independent, and the cited/source landscape is strong enough. Treat low-confidence or target-seeded candidates as workflow validation, not market truth.",
            "",
        ]
    )
    return "\n".join(lines)


def render_review_brief(rows: list[dict], summary: dict) -> str:
    lines = [
        f"# Subagent Review Brief: {summary['target_brand']} AEO Patterns",
        "",
        "## Assignment",
        "",
        "Review the semantic pattern candidates below. Do not accept a candidate because the label sounds plausible. Decide whether the evidence units actually support the mechanism, whether the captures are independent, and what evidence is missing.",
        "",
        "## Evidence Warnings",
        "",
        f"- Captures: {summary['capture_count']}",
        f"- Evidence mix: {json.dumps(summary['evidence_mix'], ensure_ascii=False)}",
        f"- Target-seeded evidence units: {summary['target_seeded_evidence_units']}",
        "",
        "## Review Output Schema",
        "",
        "Return JSON lines with: `pattern_id`, `decision` (`accept`, `revise`, `reject`), `rationale`, `missing_evidence`, `better_label`.",
        "",
        "## Candidates",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"### {row['pattern_id']} - {row['label']}",
                "",
                f"Question: {row['review_question']}",
                f"Current confidence: {row['confidence']} ({row['confidence_rationale']})",
                "",
            ]
        )
        for evidence in row["semantic_evidence"][:5]:
            lines.append(f"- {evidence['unit_id']} [{evidence['engine']} | {evidence['query_intent']} | {evidence['query']}]: {evidence['text']}")
        lines.append("")
    return "\n".join(lines)


def render_audit(rows: list[dict], clusters: list[dict], summary: dict) -> dict:
    return {
        "method": summary["method"],
        "semantic_provider": "local_concept_anchor_cosine",
        "external_embedding_model": None,
        "uses_keyword_pattern_matching": False,
        "uses_predeclared_concept_anchors": True,
        "candidate_count": len(rows),
        "cluster_count": len(clusters),
        "evidence_thresholds": {
            "high": "5+ independent manual live captures, 3+ engines, 2+ source domains, no target-seeded evidence",
            "medium": "3+ independent manual live captures, 2+ engines, no target-seeded evidence",
            "low": "thin evidence, target-seeded evidence, non-live evidence, or insufficient independence",
        },
        "required_review": [
            "semantic support review against exact evidence units",
            "adversarial provenance/independence review",
            "source/citation support review before authority claims",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    rows, units, summary = mine(args.run_dir)
    clusters = semantic_clusters(rows)
    write_jsonl(args.run_dir / "normalized" / "capture_units.jsonl", units)
    write_jsonl(args.run_dir / "normalized" / "semantic_clusters.jsonl", clusters)
    write_jsonl(args.run_dir / "normalized" / "pattern_candidates.jsonl", rows)
    report_path = args.run_dir / "final" / "pattern-mining-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(rows, summary), encoding="utf-8")
    brief_path = args.run_dir / "working" / "subagent-review-brief.md"
    brief_path.parent.mkdir(parents=True, exist_ok=True)
    brief_path.write_text(render_review_brief(rows, summary), encoding="utf-8")
    audit_path = args.run_dir / "final" / "pattern-discovery-audit.json"
    audit_path.write_text(json.dumps(render_audit(rows, clusters, summary), indent=2), encoding="utf-8")
    print(report_path)
    print(brief_path)
    print(audit_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
