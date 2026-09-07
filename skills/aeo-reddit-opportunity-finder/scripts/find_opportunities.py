#!/usr/bin/env python3
"""Generate semantic Reddit opportunity artifacts for an AEO run."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


DEFAULT_SUBREDDITS = {
    "support": ["CustomerSuccess", "callcentres", "Zendesk", "sysadmin"],
    "legal": ["lawfirm", "legaltech", "Lawyertalk"],
    "security": ["cybersecurity", "blueteamsec", "sysadmin"],
    "analytics": ["BusinessIntelligence", "dataengineering", "analytics"],
    "creative": ["marketing", "PPC", "graphic_design"],
    "code": ["ExperiencedDevs", "programming", "cscareerquestions"],
    "hr": ["humanresources", "recruiting", "AskHR"],
    "default": ["SaaS", "Entrepreneur", "smallbusiness", "consulting"],
}

BUYER_LANGUAGE_HINTS = [
    "too expensive",
    "manual",
    "takes forever",
    "hate",
    "switching",
    "alternative",
    "replace",
    "workflow",
    "seat",
    "license",
    "pricing",
    "support",
    "dashboard",
    "spreadsheet",
    "compliance",
]

CONCRETE_SIGNAL_TERMS = {
    "pain": ["pain", "painful", "frustration", "breaks", "broken", "hardest", "choke point", "too much", "killing me"],
    "workaround": ["workaround", "spreadsheet", "paper", "manual", "fallback", "hack", "using ai to", "used ai to"],
    "objection": ["cautious", "not a replacement", "dealbreaker", "fail", "risk", "doesn't work", "skeptical", "challenge"],
    "adoption_signal": [
        "beta",
        "rollout",
        "implemented",
        "launched",
        "got access",
        "started running",
        "we use",
        "we're using",
        "using ai to",
        "used ai to",
        "i use",
        "i used",
    ],
    "comparison": ["alternative", "replace", "switch", "instead of", "compare", "less control", "one person owning"],
}

TOPIC_CONCEPTS = {
    "ad & creative generation at scale": [
        "ad",
        "ads",
        "campaign",
        "creative",
        "targeting",
        "conversion",
        "pixel",
        "cpc",
        "ads manager",
    ],
    "conversational support": [
        "customer success",
        "support",
        "ticket",
        "tickets",
        "escalation",
        "churn",
        "account management",
        "csm",
        "customer",
    ],
    "messaging-channel chatbot": [
        "support",
        "chatbot",
        "chat",
        "ticket",
        "conversation",
        "customer",
        "escalation",
        "ai support",
    ],
    "doc summarization & drafting": [
        "document",
        "documents",
        "draft",
        "drafting",
        "summary",
        "summarization",
        "writeup",
        "how-to",
        "content",
    ],
    "legal research & drafting": [
        "legal",
        "law",
        "lawyer",
        "attorney",
        "research",
        "drafting",
        "westlaw",
        "lexis",
    ],
    "personalized marketing content": [
        "marketing",
        "content",
        "copy",
        "creative",
        "campaign",
        "ads",
        "personalized",
    ],
    "ai shopping / sales consultant": [
        "sales",
        "shop",
        "shopping",
        "ecommerce",
        "client",
        "objection",
        "pitch",
        "close",
    ],
    "travel & booking planner": [
        "travel",
        "booking",
        "planner",
        "itinerary",
        "hotel",
        "flight",
        "trip",
    ],
}

TOPIC_NOISE_TERMS = [
    "wpp",
    "authentic brands group",
    "pods",
    "kpmg",
    "pwc",
    "deloitte",
    "harvey",
    "thomson reuters",
    "deutsche bank db lumina",
    "westlaw",
    "lexisnexis",
    "clm employee",
    "adobe",
    "elevenlabs",
    "agoda",
    "priceline",
    "latam cosmos",
    "virgin voyages",
    "mercedes",
    "zendesk",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:80] or "item"


def clean_topic(text: str) -> str:
    cleaned = text.lower().strip()
    if "," in cleaned:
        cleaned = cleaned.split(",", 1)[0]
    for term in TOPIC_NOISE_TERMS:
        cleaned = cleaned.replace(term, "")
    cleaned = re.sub(r"\bbest\s+", "", cleaned)
    cleaned = re.sub(r"\bwhich\s+", "", cleaned)
    cleaned = re.sub(r"\bshould ai agents replace or renegotiate saas for\s+", "", cleaned)
    cleaned = re.sub(r"\bhow to improve\s+", "", cleaned)
    cleaned = re.sub(r"\bfor b2b buyers\b", "", cleaned)
    cleaned = re.sub(r"\bplatforms?\b", "", cleaned)
    cleaned = re.sub(r"\btools?\b", "", cleaned)
    cleaned = re.sub(r"\bproduction seats creative\b", "", cleaned)
    cleaned = re.sub(r"\bdoc / productivity add-ons empl\b", "", cleaned)
    cleaned = re.sub(r"\bmarketing content\b$", "marketing content", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" -/")
    return cleaned or text.strip()


def is_clean_topic(text: str) -> bool:
    lower = text.lower()
    noisy = [
        "alternatives to",
        " vs ",
        "which ",
        "vendor should",
        "agent replacement scorecard",
        "best ",
    ]
    return not any(marker in lower for marker in noisy)


def topics_from_queries(queries: list[dict]) -> list[str]:
    preferred_clusters = {"category", "answer_capture_seed"}
    topics: list[str] = []
    seen: set[str] = set()
    for query in queries:
        if query.get("cluster") not in preferred_clusters:
            continue
        topic = clean_topic(query.get("query", ""))
        if not topic or not is_clean_topic(topic):
            continue
        if topic in seen:
            continue
        seen.add(topic)
        topics.append(topic)
    return topics


def general_probe_templates(topic: str) -> list[dict]:
    return [
        {
            "probe_type": "job_to_be_done",
            "semantic_probe": f"Practitioners discussing the real job behind {topic}: what outcome they need, what work they repeat, and where the current process slows them down.",
            "why_it_matters": "Find buyer language that should shape non-target-seeded AEO prompts.",
        },
        {
            "probe_type": "software_failure",
            "semantic_probe": f"Users complaining that current {topic} software or process is expensive, awkward, unreliable, too seat-based, or creates manual workarounds.",
            "why_it_matters": "Validate whether the wedge is replacement, renegotiation, or enrichment.",
        },
        {
            "probe_type": "ai_skepticism",
            "semantic_probe": f"Practitioners challenging whether AI or agents can safely handle {topic}, including failure cases, compliance limits, and human-review boundaries.",
            "why_it_matters": "Find objections the AEO prompts and diagnostic must address.",
        },
        {
            "probe_type": "comparison_frame",
            "semantic_probe": f"Threads where people compare vendors, internal workflows, spreadsheets, outsourcing, and AI approaches for accomplishing {topic}.",
            "why_it_matters": "Discover the alternatives AI answer engines should be tested against.",
        },
    ]


def switching_probe(topic: str, competitor: str) -> dict:
    return {
        "probe_type": "switching_trigger",
        "semantic_probe": f"Buyers discussing what would make them switch away from {competitor} or reduce dependence on tools used for {topic}.",
        "why_it_matters": "Identify commercial triggers for an exposure diagnostic.",
    }


def load_thread_data(run_dir: Path) -> list[dict]:
    rows = read_jsonl(run_dir / "stage_outputs" / "reddit_threads.jsonl")
    rows.extend(read_jsonl(run_dir / "stage_outputs" / "reddit_comments.jsonl"))
    thread_data = run_dir / "stage_outputs" / "thread_data.json"
    if thread_data.exists():
        data = read_json(thread_data)
        if isinstance(data, dict):
            comments = data.get("comments") or []
            for comment in comments:
                rows.append(
                    {
                        "thread_url": data.get("url") or data.get("thread_url"),
                        "subreddit": data.get("subreddit"),
                        "title": data.get("title"),
                        "comment_id": comment.get("id"),
                        "score": comment.get("score"),
                        "text": comment.get("body") or comment.get("text") or "",
                    }
                )
    raw_dirs = [
        run_dir / "stage_outputs" / "reddit_evidence_raw",
        run_dir / "reddit-evidence-raw",
    ]
    for raw_dir in raw_dirs:
        if not raw_dir.exists():
            continue
        discovery_by_output = {}
        manifest_path = raw_dir / "reddit-discovery-manifest.json"
        if manifest_path.exists():
            manifest = read_json(manifest_path)
            for item in manifest.get("threads") or []:
                if item.get("output"):
                    discovery_by_output[item["output"]] = item
        for path in sorted(raw_dir.glob("reddit-thread-*.json")):
            data = read_json(path)
            post = data.get("post") or {}
            source = data.get("source") or {}
            discovery = discovery_by_output.get(str(path)) or discovery_by_output.get(path.as_posix()) or {}
            thread_url = post.get("url") or post.get("permalink") or source.get("url")
            subreddit = post.get("subreddit")
            title = post.get("title")
            post_text = post.get("content") or post.get("selftext") or ""
            source_query = discovery.get("query")
            if post_text:
                rows.append(
                    {
                        "thread_url": thread_url,
                        "subreddit": subreddit,
                        "title": title,
                        "comment_id": "post",
                        "score": post.get("score"),
                        "text": post_text,
                        "source_query": source_query,
                        "source_file": str(path),
                    }
                )
            for comment in data.get("comments") or []:
                rows.append(
                    {
                        "thread_url": thread_url or comment.get("source_url"),
                        "subreddit": comment.get("subreddit") or subreddit,
                        "title": title,
                        "comment_id": comment.get("id"),
                        "score": comment.get("score"),
                        "text": comment.get("body") or comment.get("text") or "",
                        "permalink": comment.get("permalink"),
                        "source_query": source_query,
                        "source_file": str(path),
                    }
                )
    return rows


def topic_bucket(text: str) -> str:
    lower = text.lower()
    if any(word in lower for word in ["zendesk", "support", "contact", "chatbot"]):
        return "support"
    if any(word in lower for word in ["legal", "law", "westlaw", "lexis"]):
        return "legal"
    if any(word in lower for word in ["security", "soar", "siem", "remediation"]):
        return "security"
    if any(word in lower for word in ["bi", "analytics", "dashboard", "sql"]):
        return "analytics"
    if any(word in lower for word in ["creative", "marketing", "ad", "content"]):
        return "creative"
    if any(word in lower for word in ["code", "developer", "ide"]):
        return "code"
    if any(word in lower for word in ["hr", "onboarding", "employee"]):
        return "hr"
    return "default"


def semantic_probes(manifest: dict, queries: list[dict], patterns: list[dict]) -> list[dict]:
    competitors = (manifest.get("competitors") or ["SaaS"])[:3]
    topics = [clean_topic(topic) for topic in (manifest.get("topics") or [])][:8]
    if not topics:
        topics = topics_from_queries(queries)[:8]
    rows: list[dict] = []
    seen: set[tuple[str, str, str, str]] = set()
    for topic in topics[:20]:
        bucket = topic_bucket(topic)
        templates = general_probe_templates(topic)
        templates.extend(switching_probe(topic, competitor) for competitor in competitors)
        for template in templates:
            competitor = template["semantic_probe"].split("switch away from ", 1)[1].split(" or ", 1)[0] if template["probe_type"] == "switching_trigger" else ""
            for subreddit in DEFAULT_SUBREDDITS.get(bucket, DEFAULT_SUBREDDITS["default"]):
                key = (subreddit, template["probe_type"], topic, competitor)
                if key in seen:
                    continue
                seen.add(key)
                rows.append(
                    {
                        "probe_id": f"rsp_{len(rows)+1:03d}",
                        "subreddit": subreddit,
                        "probe_type": template["probe_type"],
                        "semantic_probe": template["semantic_probe"],
                        "why_it_matters": template["why_it_matters"],
                        "topic": topic,
                        "competitor": competitor,
                        "bucket": bucket,
                        "selection_rule": "Select threads by semantic fit to the probe, not by literal word match.",
                        "retrieval_rule": "Use semantic retrieval or human review; do not accept a thread because it matches a query string.",
                    }
                )
    for pattern in patterns:
        label = pattern.get("label") or pattern.get("pattern_id", "")
        for subreddit in DEFAULT_SUBREDDITS["default"]:
            rows.append(
                {
                    "probe_id": f"rsp_{len(rows)+1:03d}",
                    "subreddit": subreddit,
                    "probe_type": "pattern_validation",
                    "semantic_probe": f"Threads where practitioners naturally describe, dispute, or provide examples for the pattern candidate `{label}` without being prompted by our scorecard language.",
                    "why_it_matters": "Check whether a semantic pattern candidate exists in buyer language before using it in a diagnostic.",
                    "topic": label,
                    "competitor": "",
                    "bucket": "pattern",
                    "selection_rule": "Select threads by semantic fit to the pattern mechanism, not by literal label match.",
                    "retrieval_rule": "Use semantic retrieval or human review; do not accept a thread because it matches a query string.",
                }
            )
    return rows


def source_topic(row: dict) -> str:
    query = row.get("source_query") or ""
    if not query:
        return ""
    cleaned = re.sub(r"^subreddit:\S+\s+", "", query).strip()
    for marker in [" AI workflow ", " SaaS AI agent "]:
        if marker in cleaned:
            return cleaned.split(marker, 1)[0].strip()
    return cleaned


def conceptual_hits(text: str, terms: list[str]) -> list[str]:
    lower = text.lower()
    return [term for term in terms if term in lower]


def qualification_for_row(row: dict) -> tuple[bool, dict]:
    topic = source_topic(row)
    title = row.get("title") or ""
    text = row.get("text") or ""
    thread_context = f"{title} {text[:1200]}"
    topic_terms = TOPIC_CONCEPTS.get(topic, [])
    topic_hits = conceptual_hits(thread_context, topic_terms)
    signal_hits = {
        signal: hits
        for signal, terms in CONCRETE_SIGNAL_TERMS.items()
        if (hits := conceptual_hits(text, terms))
    }
    rejected_reasons = []
    if not topic:
        rejected_reasons.append("missing_source_topic_context")
    if topic and not topic_hits:
        rejected_reasons.append("thread_or_comment_does_not_match_source_topic_concepts")
    if not signal_hits:
        rejected_reasons.append("no_concrete_pain_workaround_objection_adoption_or_comparison_signal")
    if set(signal_hits) == {"adoption_signal"} and len(signal_hits["adoption_signal"]) == 1:
        rejected_reasons.append("adoption_signal_too_thin_without_pain_objection_or_comparison")
    if row.get("score") is not None and row.get("score") < 0:
        rejected_reasons.append("negative_score")
    qualified = not rejected_reasons
    return qualified, {
        "source_topic": topic,
        "topic_concept_hits": topic_hits,
        "concrete_signal_hits": signal_hits,
        "rejected_reasons": rejected_reasons,
    }


def extract_buyer_language(reddit_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    language_rows: list[dict] = []
    rejected_rows: list[dict] = []
    for row in reddit_rows:
        text = row.get("text") or row.get("body") or row.get("title") or ""
        qualified, qualification = qualification_for_row(row)
        if not qualified:
            rejected_rows.append(
                {
                    "thread_url": row.get("thread_url") or row.get("url"),
                    "subreddit": row.get("subreddit"),
                    "comment_id": row.get("comment_id") or row.get("id"),
                    "score": row.get("score"),
                    "title": row.get("title"),
                    "snippet": re.sub(r"\s+", " ", text).strip()[:300],
                    "qualification": qualification,
                }
            )
            continue
        snippet = re.sub(r"\s+", " ", text).strip()[:500]
        language_rows.append(
            {
                "language_id": f"rbl_{len(language_rows)+1:03d}",
                "thread_url": row.get("thread_url") or row.get("url"),
                "subreddit": row.get("subreddit"),
                "comment_id": row.get("comment_id") or row.get("id"),
                "score": row.get("score"),
                "matched_signals": list(qualification["concrete_signal_hits"].keys()),
                "snippet": snippet,
                "qualification": qualification,
                "prompt_implication": "Use this wording to create non-target-seeded AEO prompts.",
            }
        )
    return language_rows, rejected_rows


def opportunities(probe_rows: list[dict], language_rows: list[dict], reviews: list[dict]) -> list[dict]:
    rows: list[dict] = []
    rejected = [row for row in reviews if row.get("decision") == "reject"]
    revised = [row for row in reviews if row.get("decision") == "revise"]
    if language_rows:
        signal_counts = Counter(signal for row in language_rows for signal in row["matched_signals"])
        for signal, count in signal_counts.most_common(10):
            rows.append(
                {
                    "opportunity_id": f"rao_{len(rows)+1:03d}",
                    "type": "prompt_update",
                    "priority": "high" if count >= 3 else "medium",
                    "signal": signal,
                    "action": f"Create non-target-seeded AEO prompts using Reddit buyer wording around `{signal}`.",
                    "evidence_count": count,
                }
            )
    else:
        rows.append(
            {
                "opportunity_id": "rao_001",
                "type": "discovery_needed",
                "priority": "high",
                "signal": "no_reddit_evidence_loaded",
                "action": "Run Reddit thread discovery before claiming buyer-language patterns.",
                "evidence_count": 0,
            }
        )
    if rejected:
        rows.append(
            {
                "opportunity_id": f"rao_{len(rows)+1:03d}",
                "type": "pattern_validation_gap",
                "priority": "high",
                "signal": "subagent_rejected_patterns",
                "action": "Use semantic Reddit review to find independent buyer language before retrying rejected semantic patterns.",
                "evidence_count": len(rejected),
            }
        )
    if revised:
        rows.append(
            {
                "opportunity_id": f"rao_{len(rows)+1:03d}",
                "type": "hypothesis_to_validate",
                "priority": "medium",
                "signal": "subagent_revised_patterns",
                "action": "Use Reddit examples to sharpen revised pattern labels before using them in a diagnostic.",
                "evidence_count": len(revised),
            }
        )
    rows.append(
        {
                "opportunity_id": f"rao_{len(rows)+1:03d}",
                "type": "search_plan",
                "priority": "high",
                "signal": "reddit_semantic_probes",
                "action": f"Review the top {min(30, len(probe_rows))} Reddit semantic probes with semantic retrieval or human screening, then save matched threads to stage_outputs/reddit_threads.jsonl.",
                "evidence_count": len(probe_rows),
            }
        )
    return rows


def render_report(manifest: dict, probe_rows: list[dict], language_rows: list[dict], opportunity_rows: list[dict]) -> str:
    lines = [
        f"# Reddit AEO Opportunity Report: {manifest.get('target_brand', 'AEO Run')}",
        "",
        "## Purpose",
        "",
        "Reddit is the wedge/signal layer: buyer language, skepticism, objections, and comparison frames that should sharpen AEO prompts and semantic pattern validation.",
        "",
        "## Evidence Loaded",
        "",
        f"- Reddit buyer-language rows: {len(language_rows)}",
        f"- Semantic probes generated: {len(probe_rows)}",
        f"- Opportunities generated: {len(opportunity_rows)}",
        "",
        "## Top Opportunities",
        "",
    ]
    for row in opportunity_rows:
        lines.append(f"- **{row['priority']} / {row['type']}**: {row['action']}")
    lines.extend(["", "## Top Semantic Probes", ""])
    for row in probe_rows[:20]:
        lines.append(f"- r/{row['subreddit']} / {row['probe_type']}: {row['semantic_probe']}")
        lines.append(f"  - Selection rule: {row['selection_rule']}")
    if language_rows:
        lines.extend(["", "## Buyer-Language Signals", ""])
        for row in language_rows[:20]:
            lines.append(f"- {', '.join(row['matched_signals'])}: {row['snippet']}")
    lines.extend(
        [
            "",
            "## Operating Rule",
            "",
            "Use Reddit to improve prompts and find skepticism. Do not treat Reddit thread counts, keyword hits, or search rankings as market proof and do not automate posting.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    manifest = read_json(args.run_dir / "manifest.json")
    queries = read_jsonl(args.run_dir / "stage_outputs" / "queries.jsonl")
    patterns = read_jsonl(args.run_dir / "normalized" / "pattern_candidates.jsonl")
    reviews = read_jsonl(args.run_dir / "normalized" / "pattern_reviews.jsonl")
    reddit_rows = load_thread_data(args.run_dir)
    probes = semantic_probes(manifest, queries, patterns)
    buyer_language, rejected_language = extract_buyer_language(reddit_rows)
    opportunity_rows = opportunities(probes, buyer_language, reviews)
    write_jsonl(args.run_dir / "stage_outputs" / "reddit_semantic_probes.jsonl", probes)
    write_jsonl(args.run_dir / "normalized" / "reddit_buyer_language.jsonl", buyer_language)
    write_jsonl(args.run_dir / "normalized" / "reddit_buyer_language_rejected.jsonl", rejected_language)
    write_jsonl(args.run_dir / "normalized" / "reddit_aeo_opportunities.jsonl", opportunity_rows)
    report_path = args.run_dir / "final" / "reddit-opportunity-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(manifest, probes, buyer_language, opportunity_rows), encoding="utf-8")
    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
