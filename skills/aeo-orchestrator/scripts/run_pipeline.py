#!/usr/bin/env python3
"""Run a local, file-backed AEO visibility audit.

This is intentionally stdlib-only so Claude Code, Codex, and OpenHands can run
the same workflow without environment setup.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


REQUIRED_QUERY_FIELDS = {"query_id", "cluster", "persona", "intent", "query", "priority"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug[:60] or "run"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def domain_from_url(url: str) -> str:
    parsed = urlparse(url if "://" in url else f"https://{url}")
    return parsed.netloc.lower().removeprefix("www.")


def sample_config() -> dict:
    return {
        "target_brand": "Acme AEO",
        "domain": "acme-aeo.example",
        "competitors": ["Profound", "AthenaHQ", "Peec AI"],
        "market": "US",
        "language": "en",
        "objective": "Find where AI answers recommend competitors instead of Acme AEO.",
        "topics": ["enterprise AI search optimization", "AI answer engine visibility"],
        "engines": ["sample"],
        "manual_captures": [
            {
                "query": "best enterprise AI search optimization platforms",
                "engine": "sample",
                "answer": (
                    "Profound is frequently recommended for enterprise AI search visibility, "
                    "with AthenaHQ also appearing for brand monitoring. The target brand is "
                    "not mentioned in this answer."
                ),
                "citation_urls": ["https://www.profound.com/", "https://www.athenahq.ai/"],
            },
            {
                "query": "alternatives to Profound for enterprise AI search optimization",
                "engine": "sample",
                "answer": (
                    "Common alternatives include AthenaHQ and Peec AI. A new entrant would need "
                    "clear comparison content and third-party citations to appear here."
                ),
                "citation_urls": ["https://www.athenahq.ai/", "https://peec.ai/"],
            },
        ],
    }


def make_queries(config: dict) -> list[dict]:
    topics = config.get("topics") or [config.get("objective", "AI search visibility")]
    brand = config["target_brand"]
    competitors = config.get("competitors", [])
    primary_competitor = competitors[0] if competitors else "leading competitor"
    rows: list[dict] = []
    templates = [
        ("category", "enterprise buyer", "commercial investigation", "best {topic} platforms"),
        ("comparison", "enterprise buyer", "vendor comparison", "{brand} vs {competitor} for {topic}"),
        ("alternatives", "growth leader", "alternative search", "alternatives to {competitor} for {topic}"),
        ("problem", "marketing leader", "problem solution", "how to improve {topic} for B2B buyers"),
        ("selection", "CRO", "recommendation", "which {topic} vendor should a B2B company choose"),
    ]
    idx = 1
    for topic in topics:
        for cluster, persona, intent, template in templates:
            rows.append(
                {
                    "query_id": f"q_{idx:03d}",
                    "cluster": cluster,
                    "persona": persona,
                    "intent": intent,
                    "query": template.format(topic=topic, brand=brand, competitor=primary_competitor),
                    "priority": 1 if cluster in {"category", "comparison", "alternatives"} else 2,
                }
            )
            idx += 1
    existing = {row["query"].strip().lower() for row in rows}
    for capture in config.get("manual_captures") or []:
        query = (capture.get("query") or "").strip()
        if not query or query.lower() in existing:
            continue
        rows.append(
            {
                "query_id": f"q_{idx:03d}",
                "cluster": "answer_capture_seed",
                "persona": "buyer",
                "intent": "captured answer evidence",
                "query": query,
                "priority": 1,
            }
        )
        existing.add(query.lower())
        idx += 1
    return rows


def match_query_id(query: str, queries: list[dict], fallback_index: int) -> str:
    normalized = query.strip().lower()
    for row in queries:
        if row["query"].strip().lower() == normalized:
            return row["query_id"]
    return queries[min(fallback_index, len(queries) - 1)]["query_id"]


def build_sources(config: dict, captures: list[dict]) -> list[dict]:
    urls: list[str] = []
    if config.get("domain"):
        urls.append(f"https://{config['domain']}")
    for capture in captures:
        urls.extend(capture.get("citation_urls", []))
    seen: set[str] = set()
    rows: list[dict] = []
    for url in urls:
        if not url:
            continue
        normalized = url if "://" in url else f"https://{url}"
        normalized = normalized.rstrip("/")
        if normalized in seen:
            continue
        seen.add(normalized)
        domain = domain_from_url(normalized)
        source_type = "official" if domain == config.get("domain", "").lower() else "competitor"
        rows.append(
            {
                "source_id": f"src_{len(rows) + 1:03d}",
                "url": normalized,
                "domain": domain,
                "source_type": source_type,
                "is_primary": source_type == "official",
                "retrieved_at": now_iso(),
                "freshness_status": "unknown",
            }
        )
    return rows


def build_captures(run_dir: Path, config: dict, queries: list[dict]) -> list[dict]:
    manual = config.get("manual_captures") or []
    if not manual:
        manual = [
            {
                "query": queries[0]["query"],
                "engine": "manual",
                "answer": f"No supplied answer capture. {config['target_brand']} requires manual evidence collection.",
                "citation_urls": [],
            }
        ]
    rows: list[dict] = []
    raw_dir = run_dir / "stage_outputs" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    for idx, capture in enumerate(manual, start=1):
        capture_id = f"cap_{idx:03d}"
        raw_path = raw_dir / f"{capture_id}.txt"
        raw_path.write_text(capture.get("answer", "").strip() + "\n", encoding="utf-8")
        rows.append(
            {
                "capture_id": capture_id,
                "query_id": match_query_id(capture.get("query", ""), queries, idx - 1),
                "engine": capture.get("engine", "manual"),
                "captured_at": capture.get("captured_at", now_iso()),
                "answer_text_path": str(raw_path.relative_to(run_dir)),
                "citation_urls": capture.get("citation_urls", []),
                "raw_metadata": capture.get("raw_metadata", {"collection_method": "manual_or_sample"}),
            }
        )
    return rows


def build_entities(config: dict, captures: list[dict], run_dir: Path) -> list[dict]:
    names = [(config["target_brand"], "brand")] + [(name, "competitor") for name in config.get("competitors", [])]
    rows: list[dict] = []
    for name, entity_type in names:
        evidence_ids: list[str] = []
        source_capture_ids: list[str] = []
        pattern = re.compile(re.escape(name), re.IGNORECASE)
        for capture in captures:
            text = (run_dir / capture["answer_text_path"]).read_text(encoding="utf-8")
            if pattern.search(text):
                evidence_ids.append(capture["capture_id"])
                source_capture_ids.append(capture["capture_id"])
        rows.append(
            {
                "entity_id": f"ent_{len(rows) + 1:03d}",
                "name": name,
                "entity_type": entity_type,
                "aliases": [],
                "source_capture_ids": source_capture_ids,
                "evidence_ids": evidence_ids,
            }
        )
    for capture in captures:
        for url in capture.get("citation_urls", []):
            rows.append(
                {
                    "entity_id": f"ent_{len(rows) + 1:03d}",
                    "name": domain_from_url(url),
                    "entity_type": "source",
                    "aliases": [url],
                    "source_capture_ids": [capture["capture_id"]],
                    "evidence_ids": [capture["capture_id"]],
                }
            )
    return rows


def score_visibility(config: dict, queries: list[dict], captures: list[dict], run_dir: Path) -> dict:
    names = [config["target_brand"]] + config.get("competitors", [])
    by_entity = {name: {"mentions": 0, "captures": [], "citation_domains": []} for name in names}
    by_query = {}
    citation_counter: Counter[str] = Counter()
    query_by_id = {row["query_id"]: row for row in queries}
    for capture in captures:
        text = (run_dir / capture["answer_text_path"]).read_text(encoding="utf-8")
        query_mentions = []
        for name in names:
            if re.search(re.escape(name), text, re.IGNORECASE):
                by_entity[name]["mentions"] += 1
                by_entity[name]["captures"].append(capture["capture_id"])
                query_mentions.append(name)
        domains = [domain_from_url(url) for url in capture.get("citation_urls", [])]
        citation_counter.update(domains)
        for name in names:
            for domain in domains:
                if slugify(name).replace("-", "") in domain.replace("-", "").replace(".", ""):
                    by_entity[name]["citation_domains"].append(domain)
        by_query[capture["query_id"]] = {
            "capture_id": capture["capture_id"],
            "query": query_by_id.get(capture["query_id"], {}).get("query", ""),
            "engine": capture["engine"],
            "mentioned_entities": query_mentions,
            "citation_domains": domains,
            "target_brand_mentioned": config["target_brand"] in query_mentions,
            "competitors_mentioned": [name for name in config.get("competitors", []) if name in query_mentions],
        }
    target_mentions = by_entity[config["target_brand"]]["mentions"]
    competitor_mentions = sum(by_entity[name]["mentions"] for name in config.get("competitors", []))
    return {
        "target_brand": config["target_brand"],
        "competitors": config.get("competitors", []),
        "summary": {
            "capture_count": len(captures),
            "target_mentions": target_mentions,
            "competitor_mentions": competitor_mentions,
            "target_visibility_rate": target_mentions / len(captures) if captures else 0,
            "top_citation_domains": citation_counter.most_common(10),
        },
        "by_query": by_query,
        "by_entity": by_entity,
    }


def build_recommendations(config: dict, scores: dict) -> list[dict]:
    rows: list[dict] = []
    capture_evidence = [
        row["capture_id"]
        for row in scores["by_query"].values()
        if row.get("capture_id")
    ]
    if scores["summary"]["competitor_mentions"] > scores["summary"]["target_mentions"]:
        rows.append(
            {
                "recommendation_id": "rec_001",
                "priority": "high",
                "theme": "competitor recommended",
                "action": "Create or refresh comparison content that directly addresses the buyer prompts where competitors appear and the target brand is absent.",
                "evidence_ids": capture_evidence[:3],
                "expected_impact": "Increase eligibility for recommendation and comparison-style AI answers.",
                "effort": "medium",
                "confidence": "medium",
            }
        )
    if not scores["by_entity"][config["target_brand"]]["citation_domains"]:
        rows.append(
            {
                "recommendation_id": f"rec_{len(rows) + 1:03d}",
                "priority": "high",
                "theme": "citation gap",
                "action": "Build crawlable owned pages and pursue third-party citations that describe the target brand in category, comparison, and problem-solution language.",
                "evidence_ids": capture_evidence[:3],
                "expected_impact": "Improve source availability for AI answers that rely on cited pages.",
                "effort": "high",
                "confidence": "medium",
            }
        )
    if not rows:
        rows.append(
            {
                "recommendation_id": "rec_001",
                "priority": "medium",
                "theme": "measurement baseline",
                "action": "Repeat the audit with more real answer captures to establish a stronger visibility baseline before making major content changes.",
                "evidence_ids": capture_evidence[:3],
                "expected_impact": "Improve confidence and reduce false precision.",
                "effort": "low",
                "confidence": "high",
            }
        )
    return rows


def render_outputs(run_dir: Path, config: dict, queries: list[dict], captures: list[dict], scores: dict, recs: list[dict]) -> None:
    final_dir = run_dir / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    report = final_dir / "aeo-audit.md"
    lines = [
        f"# AEO Audit: {config['target_brand']}",
        "",
        f"- Domain: `{config.get('domain', '')}`",
        f"- Market: {config.get('market', '')}",
        f"- Objective: {config.get('objective', '')}",
        f"- Status: draft",
        "",
        "## Visibility Summary",
        "",
        f"- Captures analyzed: {scores['summary']['capture_count']}",
        f"- Target mentions: {scores['summary']['target_mentions']}",
        f"- Competitor mentions: {scores['summary']['competitor_mentions']}",
        f"- Target visibility rate: {scores['summary']['target_visibility_rate']:.0%}",
        "",
        "## Recommendations",
        "",
    ]
    for rec in recs:
        lines.extend(
            [
                f"### {rec['recommendation_id']}: {rec['theme']} ({rec['priority']})",
                "",
                rec["action"],
                "",
                f"- Evidence ids: {', '.join(rec['evidence_ids'])}",
                f"- Expected impact: {rec['expected_impact']}",
                f"- Effort: {rec['effort']}",
                f"- Confidence: {rec['confidence']}",
                "",
            ]
        )
    lines.extend(["## Query Evidence", ""])
    capture_by_qid = {capture["query_id"]: capture for capture in captures}
    for query in queries:
        capture = capture_by_qid.get(query["query_id"])
        if not capture:
            continue
        qscore = scores["by_query"].get(query["query_id"], {})
        lines.extend(
            [
                f"### {query['query_id']}: {query['query']}",
                "",
                f"- Engine: {capture['engine']}",
                f"- Mentioned entities: {', '.join(qscore.get('mentioned_entities', [])) or 'none'}",
                f"- Citation domains: {', '.join(qscore.get('citation_domains', [])) or 'none'}",
                f"- Raw answer: `{capture['answer_text_path']}`",
                "",
            ]
        )
    report.write_text("\n".join(lines), encoding="utf-8")

    with (final_dir / "evidence.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "query_id",
                "query",
                "engine",
                "target_brand_mentioned",
                "competitors_mentioned",
                "citation_domains",
                "raw_answer_path",
            ],
        )
        writer.writeheader()
        query_by_id = {query["query_id"]: query for query in queries}
        for capture in captures:
            qscore = scores["by_query"].get(capture["query_id"], {})
            writer.writerow(
                {
                    "query_id": capture["query_id"],
                    "query": query_by_id.get(capture["query_id"], {}).get("query", ""),
                    "engine": capture["engine"],
                    "target_brand_mentioned": qscore.get("target_brand_mentioned", False),
                    "competitors_mentioned": "; ".join(qscore.get("competitors_mentioned", [])),
                    "citation_domains": "; ".join(qscore.get("citation_domains", [])),
                    "raw_answer_path": capture["answer_text_path"],
                }
            )


def create_manifest(run_dir: Path, config: dict, sample: bool) -> dict:
    return {
        "run_id": run_dir.name,
        "created_at": now_iso(),
        "target_brand": config["target_brand"],
        "domain": config.get("domain", ""),
        "competitors": config.get("competitors", []),
        "market": config.get("market", ""),
        "language": config.get("language", "en"),
        "objective": config.get("objective", ""),
        "engines": config.get("engines", ["manual"]),
        "sample": sample,
        "stage_status": {
            "init": "passed",
            "query_plan": "pending",
            "source_discovery": "pending",
            "answer_capture": "pending",
            "normalize_extract": "pending",
            "score": "pending",
            "synthesize": "pending",
            "validate": "pending",
            "render": "pending",
        },
        "artifact_paths": {},
        "validation_status": "pending",
        "status": "draft",
    }


def run(config: dict, sample: bool, run_root: Path) -> Path:
    date_prefix = datetime.now(timezone.utc).date().isoformat()
    run_dir = run_root / f"{date_prefix}-aeo-search-{slugify(config['target_brand'])}"
    suffix = 2
    base = run_dir
    while run_dir.exists():
        run_dir = Path(f"{base}-{suffix}")
        suffix += 1
    for subdir in ["inputs", "stage_outputs/raw", "normalized", "qa", "final"]:
        (run_dir / subdir).mkdir(parents=True, exist_ok=True)
    write_json(run_dir / "inputs" / "config.json", config)
    manifest = create_manifest(run_dir, config, sample)
    write_json(run_dir / "manifest.json", manifest)

    queries = make_queries(config)
    append_jsonl(run_dir / "stage_outputs" / "queries.jsonl", queries)
    manifest["stage_status"]["query_plan"] = "passed"

    captures = build_captures(run_dir, config, queries)
    append_jsonl(run_dir / "stage_outputs" / "answer_captures.jsonl", captures)
    manifest["stage_status"]["answer_capture"] = "passed"

    sources = build_sources(config, captures)
    append_jsonl(run_dir / "stage_outputs" / "sources.jsonl", sources)
    manifest["stage_status"]["source_discovery"] = "passed"

    entities = build_entities(config, captures, run_dir)
    append_jsonl(run_dir / "normalized" / "entities.jsonl", entities)
    manifest["stage_status"]["normalize_extract"] = "passed"

    scores = score_visibility(config, queries, captures, run_dir)
    write_json(run_dir / "normalized" / "visibility_scores.json", scores)
    manifest["stage_status"]["score"] = "passed"

    recs = build_recommendations(config, scores)
    append_jsonl(run_dir / "normalized" / "recommendations.jsonl", recs)
    manifest["stage_status"]["synthesize"] = "passed"

    render_outputs(run_dir, config, queries, captures, scores, recs)
    manifest["stage_status"]["render"] = "passed"
    manifest["artifact_paths"] = {
        "queries": "stage_outputs/queries.jsonl",
        "sources": "stage_outputs/sources.jsonl",
        "answer_captures": "stage_outputs/answer_captures.jsonl",
        "entities": "normalized/entities.jsonl",
        "visibility_scores": "normalized/visibility_scores.json",
        "recommendations": "normalized/recommendations.jsonl",
        "report": "final/aeo-audit.md",
        "evidence_csv": "final/evidence.csv",
    }
    write_json(run_dir / "manifest.json", manifest)
    return run_dir


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path)
    parser.add_argument("--sample", action="store_true")
    parser.add_argument("--run-root", type=Path, default=Path("runs"))
    args = parser.parse_args()
    if not args.sample and not args.config:
        parser.error("Provide --sample or --config path")
    config = sample_config() if args.sample else read_json(args.config)
    missing = [key for key in ["target_brand", "objective"] if not config.get(key)]
    if missing:
        raise SystemExit(f"Missing required config fields: {', '.join(missing)}")
    run_dir = run(config, args.sample, args.run_root)
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
