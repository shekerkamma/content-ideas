#!/usr/bin/env python3
"""Convert the Agent Replacement Scorecard HTML into an AEO config seed."""

from __future__ import annotations

import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path


class ScorecardParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "tr":
            return
        attr = {key: value or "" for key, value in attrs}
        classes = set(attr.get("class", "").split())
        if "main" not in classes:
            return
        self.rows.append(
            {
                "type": attr.get("data-type", ""),
                "verdict": attr.get("data-verdict", ""),
                "search": html.unescape(attr.get("data-search", "")),
            }
        )


def title_case_topic(raw: str) -> str:
    return re.sub(r"\s+", " ", raw).strip(" -").lower()


def extract_topic(row: dict) -> str:
    search = row["search"]
    if not search:
        return ""
    proof_markers = [" mercedes ", " volkswagen ", " agoda ", " luxgen ", " geotab ", " humana ", " harvey ", " grupo ", " wpp ", " veo ", " adobe ", " bmw ", " valeo ", " suzano ", " code-agent ", " spotify ", " document ai deployments ", " honeywell ", " mlb ", " google security ", " security-agent ", " citi ", " u.s. fda "]
    idxs = [search.find(marker) for marker in proof_markers if marker in search]
    cut = min(idxs) if idxs else min(len(search), 80)
    return title_case_topic(search[:cut])


def compact_answer(row: dict) -> str:
    search = re.sub(r"\s+", " ", row.get("search", "")).strip()
    if not search:
        return ""
    topic = extract_topic(row)
    verdict = row.get("verdict", "").title()
    agent_type = row.get("type", "agentic")
    return (
        f"For {topic}, the scorecard classifies this as {verdict} in the "
        f"{agent_type} category. Basis: {search[:700]}"
    )


def extract_competitor_terms(rows: list[dict], limit: int) -> list[str]:
    terms: list[str] = []
    for row in rows:
        search = row["search"]
        for candidate in re.findall(r"\b(?:Zendesk|Glean|Westlaw|LexisNexis|Looker|Adobe|Google Security Operations|NotebookLM|SOAR|GRC|CCaaS|BI dashboards|IDP|OCR|DAM)\b", search, flags=re.I):
            normalized = candidate.strip()
            if normalized and normalized.lower() not in {term.lower() for term in terms}:
                terms.append(normalized)
        if len(terms) >= limit:
            break
    return terms[:limit]


def build_seed_captures(rows: list[dict], source_url: str, limit: int) -> list[dict]:
    captures: list[dict] = []
    seed_rows = [row for row in rows if row.get("verdict") == "REPLACE"] or rows
    for row in seed_rows[:limit]:
        topic = extract_topic(row)
        if not topic:
            continue
        captures.append(
            {
                "query": f"Should AI agents replace or renegotiate SaaS for {topic}?",
                "engine": "scorecard_seed",
                "answer": compact_answer(row),
                "citation_urls": [source_url],
                "raw_metadata": {
                    "collection_method": "scorecard_seed",
                    "verdict": row.get("verdict", ""),
                    "type": row.get("type", ""),
                    "note": "Seed answer generated from the supplied scorecard, not a live AI-answer capture.",
                },
            }
        )
    captures.extend(
        [
            {
                "query": "Which SaaS workflows are most likely to be replaced by AI agents?",
                "engine": "manual_placeholder",
                "answer": "Paste a real ChatGPT, Claude, Perplexity, or Google AI Mode answer here.",
                "citation_urls": [source_url],
                "raw_metadata": {
                    "collection_method": "manual_placeholder",
                    "note": "Replace this with live AI-answer evidence.",
                },
            },
            {
                "query": "Agentic AI vs SaaS replacement scorecard",
                "engine": "manual_placeholder",
                "answer": "Paste a real AI answer here and keep the cited URLs in citation_urls.",
                "citation_urls": [source_url],
                "raw_metadata": {
                    "collection_method": "manual_placeholder",
                    "note": "Replace this with live AI-answer evidence.",
                },
            },
        ]
    )
    return captures


def build_config(rows: list[dict], source_url: str, target_brand: str, domain: str, topic_limit: int) -> dict:
    replace_rows = [row for row in rows if row.get("verdict") == "REPLACE"]
    seed_rows = replace_rows or rows
    topics = []
    for row in seed_rows:
        topic = extract_topic(row)
        if topic and topic not in topics:
            topics.append(topic)
        if len(topics) >= topic_limit:
            break
    competitors = extract_competitor_terms(rows, 8) or [
        "Gartner",
        "IDC",
        "Google Cloud gen AI use cases",
        "Agent Replacement Index",
    ]
    return {
        "target_brand": target_brand,
        "domain": domain,
        "competitors": competitors,
        "market": "US",
        "language": "en",
        "objective": (
            "Audit whether AI answers surface this Agent Replacement Scorecard "
            "when buyers ask which SaaS workflows agents can replace, renegotiate, or enrich."
        ),
        "topics": topics,
        "engines": ["manual"],
        "source_basis": {
            "type": "scorecard_html",
            "url": source_url,
            "rows": len(rows),
            "replace_rows": len(replace_rows),
        },
        "manual_captures": build_seed_captures(rows, source_url, min(topic_limit, 10)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", type=Path, required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--target-brand", default="Agent Replacement Scorecard")
    parser.add_argument("--domain", default="shekerkamma.github.io/content-ideas")
    parser.add_argument("--topic-limit", type=int, default=12)
    args = parser.parse_args()

    parser_obj = ScorecardParser()
    parser_obj.feed(args.html.read_text(encoding="utf-8"))
    config = build_config(parser_obj.rows, args.source_url, args.target_brand, args.domain, args.topic_limit)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
