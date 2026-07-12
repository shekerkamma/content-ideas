#!/usr/bin/env python3
"""Draft-only Hermes content pipeline runner.

The runner is intentionally conservative:
- offline mode is the default, so smoke tests do not spend API credits;
- live mode only performs You.com search when explicitly requested;
- publishing is blocked by config validation before any work starts.
"""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("PyYAML is required to read pipeline YAML configs") from exc


IMPLEMENTATION_DIR = Path(__file__).resolve().parent
DEFAULT_BASE_URL = "https://ydc-index.io"


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat()


def slugify(value: str, max_len: int = 80) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return (slug or "item")[:max_len].strip("-")


def stable_id(*parts: str, prefix: str = "") -> str:
    text = "|".join(parts)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}{digest}" if prefix else digest


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"expected YAML object: {path}")
    return data


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "pyproject.toml").exists():
            return candidate
    return Path.cwd()


def load_hermes_env_key() -> str:
    env_path = Path.home() / ".hermes" / ".env"
    if not env_path.exists():
        return ""
    for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("YOU_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def you_api_key() -> str:
    return os.getenv("YOU_API_KEY", "").strip() or load_hermes_env_key()


def result_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: list[Any] = [
        payload.get("hits"),
        payload.get("results"),
        payload.get("web"),
        payload.get("data"),
    ]
    data = payload.get("data")
    if isinstance(data, dict):
        candidates.extend([data.get("hits"), data.get("results"), data.get("web")])
    results = payload.get("results")
    if isinstance(results, dict):
        candidates.extend([results.get("hits"), results.get("results"), results.get("web")])

    for candidate in candidates:
        if isinstance(candidate, list):
            return [item for item in candidate if isinstance(item, dict)]
    return []


def pick_first(mapping: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = mapping.get(key)
        if isinstance(value, list):
            value = " ".join(str(item).strip() for item in value if item)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def you_search(query: str, limit: int) -> list[dict[str, str]]:
    key = you_api_key()
    if not key:
        raise RuntimeError("YOU_API_KEY is not set")

    base_url = os.getenv("YOU_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    params = urllib.parse.urlencode({"query": query, "num_web_results": max(1, min(limit, 20))})
    req = urllib.request.Request(
        f"{base_url}/v1/search?{params}",
        headers={"X-API-Key": key, "Accept-Encoding": "identity"},
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            body = response.read()
            if response.headers.get("Content-Encoding", "").lower() == "gzip":
                body = gzip.decompress(body)
            payload = json.loads(body.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"You.com API error {exc.code}: {body}") from exc

    normalized = []
    for item in result_items(payload):
        title = pick_first(item, ("title", "name"))
        url = pick_first(item, ("url", "link", "source_url"))
        description = pick_first(item, ("description", "snippet", "content", "text", "summary"))
        if title or url or description:
            normalized.append({"title": title, "url": url, "description": description})
    return normalized


def validate_safety(config: dict[str, Any]) -> None:
    if config.get("mode") != "draft_only":
        raise ValueError("pipeline mode must be draft_only")
    approval = config.get("approval_gates") or {}
    if approval.get("publish_allowed") is not False:
        raise ValueError("approval_gates.publish_allowed must be false")


class Lock:
    def __init__(self, lock_path: Path, force: bool = False) -> None:
        self.lock_path = lock_path
        self.force = force
        self.acquired = False

    def __enter__(self) -> "Lock":
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        if self.lock_path.exists():
            age = time.time() - self.lock_path.stat().st_mtime
            if age < 7200 and not self.force:
                raise RuntimeError(f"active lock exists: {self.lock_path}")
        write_text(self.lock_path, f"pid={os.getpid()}\nstarted_at={iso_now()}")
        self.acquired = True
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[no-untyped-def]
        if self.acquired and self.lock_path.exists():
            self.lock_path.unlink()


def flatten_sources(sources_config: dict[str, Any]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    flattened: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for cluster in sources_config.get("source_clusters", []):
        for source in cluster.get("sources", []):
            flattened.append((cluster, source))
    return flattened


def domain_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc.replace("www.", "")


def offline_source_item(cluster: dict[str, Any], source: dict[str, Any], date: str) -> dict[str, Any]:
    url = source.get("url", "")
    item_id = stable_id(cluster["id"], source["id"], url, date, prefix="src-")
    topic_fit = ", ".join(cluster.get("topic_fit", [])[:3])
    return {
        "id": item_id,
        "source_id": source["id"],
        "cluster_id": cluster["id"],
        "title": f"{source['name']} signal for {cluster['label']}",
        "url": url,
        "canonical_url": url,
        "published_at": f"{date}T00:00:00+00:00",
        "fetched_at": iso_now(),
        "author": None,
        "source_type": source.get("type", "other"),
        "trust_tier": source.get("trust_tier", "unknown"),
        "summary": (
            f"Offline seed item from {source['name']} for evaluating {topic_fit}. "
            "Use live mode to replace this with current source content."
        ),
        "raw_content_path": None,
        "dedupe_key": stable_id(url),
        "status": "new",
        "errors": [],
    }


def live_source_items(
    cluster: dict[str, Any],
    source: dict[str, Any],
    date: str,
    per_source_limit: int,
) -> list[dict[str, Any]]:
    domain = domain_from_url(source.get("url", ""))
    terms = " OR ".join(cluster.get("topic_fit", [])[:3])
    query = f"site:{domain} {terms}".strip()
    results = you_search(query, per_source_limit)
    items = []
    for result in results:
        url = result.get("url") or source.get("url", "")
        title = result.get("title") or f"{source['name']} result"
        item_id = stable_id(cluster["id"], source["id"], url, title, prefix="src-")
        items.append(
            {
                "id": item_id,
                "source_id": source["id"],
                "cluster_id": cluster["id"],
                "title": title,
                "url": url,
                "canonical_url": url,
                "published_at": None,
                "fetched_at": iso_now(),
                "author": None,
                "source_type": source.get("type", "other"),
                "trust_tier": source.get("trust_tier", "unknown"),
                "summary": result.get("description") or "No snippet returned.",
                "raw_content_path": None,
                "dedupe_key": stable_id(url),
                "status": "new",
                "errors": [],
            }
        )
    return items


def scan_sources(
    sources_config: dict[str, Any],
    config: dict[str, Any],
    paths: dict[str, Path],
    date: str,
    live: bool,
    warnings: list[str],
    errors: list[str],
) -> list[dict[str, Any]]:
    cap = int(config["daily_caps"]["source_items"])
    max_results = int(config["search"]["max_results_per_query"])
    items: list[dict[str, Any]] = []
    seen: set[str] = set()

    for cluster, source in flatten_sources(sources_config):
        if len(items) >= cap:
            break
        try:
            candidates = (
                live_source_items(cluster, source, date, max(1, min(max_results, 3)))
                if live
                else [offline_source_item(cluster, source, date)]
            )
        except Exception as exc:  # noqa: BLE001
            errors.append(f"source scan failed for {source.get('id')}: {exc}")
            continue
        for item in candidates:
            key = item.get("dedupe_key") or stable_id(item.get("url", ""))
            if key in seen:
                item["status"] = "duplicate"
            seen.add(key)
            if item["status"] == "new":
                items.append(item)
                write_json(paths["source_items"] / f"source-item-{item['source_id']}-{item['id']}.json", item)
            if len(items) >= cap:
                break

    if not live:
        warnings.append("offline mode used; source items are fixture artifacts")
    return items


def score_cluster(cluster: dict[str, Any], cluster_items: list[dict[str, Any]], weights: dict[str, float]) -> tuple[float, dict[str, float]]:
    priority = cluster.get("priority", "medium")
    authority = sum(1 for item in cluster_items if item.get("trust_tier") == "primary") / max(len(cluster_items), 1)
    breakdown = {
        "business_relevance": 92 if priority == "high" else 76,
        "source_authority": 60 + authority * 35,
        "freshness": 80,
        "novelty": 70,
        "implementation_value": 88 if "implementation" in " ".join(cluster.get("topic_fit", [])) else 74,
        "audience_fit": 82,
    }
    weighted = sum(breakdown[key] * float(weights.get(key, 0)) for key in breakdown)
    return round(weighted, 2), {key: round(value, 2) for key, value in breakdown.items()}


def rank_topics(
    sources_config: dict[str, Any],
    config: dict[str, Any],
    items: list[dict[str, Any]],
    paths: dict[str, Path],
    date: str,
) -> list[dict[str, Any]]:
    cap = int(config["daily_caps"]["topic_clusters"])
    weights = sources_config.get("ranking_weights", {})
    by_cluster: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        by_cluster.setdefault(item["cluster_id"], []).append(item)

    clusters_by_id = {cluster["id"]: cluster for cluster in sources_config.get("source_clusters", [])}
    ranked = []
    for cluster_id, cluster_items in by_cluster.items():
        cluster = clusters_by_id[cluster_id]
        score, breakdown = score_cluster(cluster, cluster_items, weights)
        cluster_payload = {
            "id": stable_id(cluster_id, date, prefix="topic-"),
            "date": date,
            "title": f"{cluster['label']}: best daily content opportunity",
            "theme": cluster["label"],
            "source_item_ids": [item["id"] for item in cluster_items],
            "score": score,
            "score_breakdown": breakdown,
            "score_reasons": [
                f"{len(cluster_items)} source item(s) found in the cluster",
                f"Priority is {cluster.get('priority', 'medium')}",
                "Topic fits the operator-facing AI content strategy",
            ],
            "recommended_angle": (
                f"Explain what changed in {cluster['label']} and convert it into "
                "a practical implementation narrative for AI operators."
            ),
            "audience_fit": "AI operators, enterprise solution architects, and founders evaluating agent workflows",
            "status": "ranked",
        }
        ranked.append(cluster_payload)

    ranked = sorted(ranked, key=lambda payload: payload["score"], reverse=True)[:cap]
    for cluster_payload in ranked:
        write_json(paths["topic_clusters"] / f"topic-cluster-{slugify(cluster_payload['title'])}.json", cluster_payload)
    return ranked


def item_index(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in items}


def generate_briefs(
    topics: list[dict[str, Any]],
    items: list[dict[str, Any]],
    config: dict[str, Any],
    paths: dict[str, Path],
    warnings: list[str],
) -> list[dict[str, Any]]:
    cap = int(config["daily_caps"]["research_briefs"])
    min_sources = int(config["quality_gates"]["min_sources_per_brief"])
    items_by_id = item_index(items)
    briefs = []
    for topic in topics:
        source_items = [items_by_id[item_id] for item_id in topic["source_item_ids"] if item_id in items_by_id]
        if len(source_items) < min_sources:
            warnings.append(f"topic {topic['id']} skipped for brief; fewer than {min_sources} sources")
            continue
        citations = []
        evidence = []
        for index, item in enumerate(source_items[:min_sources], start=1):
            citation_id = f"c{index}"
            citations.append(
                {
                    "id": citation_id,
                    "title": item["title"],
                    "url": item["url"],
                    "source_id": item["source_id"],
                    "published_at": item.get("published_at"),
                    "fetched_at": item["fetched_at"],
                }
            )
            evidence.append(
                {
                    "claim": f"{item['source_id']} contributes evidence for the {topic['theme']} opportunity.",
                    "citation_ids": [citation_id],
                }
            )

        brief_id = stable_id(topic["id"], "brief", prefix="brief-")
        brief = {
            "id": brief_id,
            "topic_cluster_id": topic["id"],
            "title": topic["title"],
            "thesis": (
                f"{topic['theme']} is a content opportunity because the sources point to "
                "practical operator demand, not just general AI news."
            ),
            "angle": topic["recommended_angle"],
            "evidence": evidence,
            "citations": citations,
            "risks": [
                "Offline or snippet-only evidence must be replaced with full source review before publishing.",
                "The article must avoid overclaiming beyond cited source material.",
            ],
            "missing_facts": [
                "Current primary-source details should be verified in live mode before final editorial approval."
            ],
            "status": "approved_for_draft",
        }
        slug = slugify(brief["title"])
        write_json(paths["research_briefs"] / f"brief-{slug}.json", brief)
        write_text(paths["research_briefs"] / f"brief-{slug}.md", brief_markdown(brief))
        briefs.append(brief)
        if len(briefs) >= cap:
            break
    return briefs


def brief_markdown(brief: dict[str, Any]) -> str:
    lines = [
        f"# {brief['title']}",
        "",
        "## Thesis",
        "",
        brief["thesis"],
        "",
        "## Angle",
        "",
        brief["angle"],
        "",
        "## Evidence",
        "",
    ]
    for entry in brief["evidence"]:
        citations = ", ".join(entry["citation_ids"])
        lines.append(f"- {entry['claim']} [{citations}]")
    lines.extend(["", "## Citations", ""])
    for citation in brief["citations"]:
        lines.append(f"- [{citation['id']}] {citation['title']} - {citation['url']}")
    lines.extend(["", "## Risks", ""])
    for risk in brief["risks"]:
        lines.append(f"- {risk}")
    return "\n".join(lines)


def generate_drafts(
    briefs: list[dict[str, Any]],
    config: dict[str, Any],
    paths: dict[str, Path],
) -> list[dict[str, Any]]:
    cap = int(config["daily_caps"]["draft_packages"])
    drafts = []
    for brief in briefs[:cap]:
        draft_id = stable_id(brief["id"], "draft", prefix="draft-")
        slug = slugify(brief["title"])
        article_path = paths["draft_packages"] / f"draft-{slug}.md"
        article = article_markdown(brief)
        write_text(article_path, article)
        draft = {
            "id": draft_id,
            "research_brief_id": brief["id"],
            "title": brief["title"],
            "dek": "A practical operator-facing draft generated from a sourced research brief.",
            "article_markdown_path": str(article_path),
            "target_audience": "AI operators, enterprise solution architects, and founders",
            "seo_aeo": {
                "primary_query": slug.replace("-", " "),
                "secondary_queries": [
                    "Hermes agent content pipeline",
                    "AI agent workflow automation",
                    "source grounded AI content workflow",
                ],
                "answer_targets": [
                    "What can a Hermes content pipeline automate?",
                    "How do you keep AI-generated content reviewable?",
                    "Where should human approval stay in an agent workflow?",
                ],
            },
            "variants": {
                "linkedin": (
                    "A useful Hermes content pipeline is not an auto-publisher. "
                    "It is a daily system for finding signals, drafting sourced briefs, "
                    "and handing humans review-ready work."
                ),
                "x_thread": [
                    "Hermes content pipeline v1 should be draft-only.",
                    "The useful loop is: source scan -> ranked topic -> sourced brief -> draft package -> human review.",
                    "The dangerous step is publishing. Keep that manual until provenance, voice, and cost controls are proven.",
                ],
                "newsletter": (
                    "This week's implementation pattern: use Hermes to turn source monitoring into "
                    "review-ready content packages, while keeping publishing behind an editorial gate."
                ),
            },
            "citation_map": [
                {
                    "draft_claim": evidence["claim"],
                    "citation_ids": evidence["citation_ids"],
                }
                for evidence in brief["evidence"]
            ],
            "status": "draft",
        }
        write_json(paths["draft_packages"] / f"draft-{slug}.json", draft)
        drafts.append(draft)
    return drafts


def article_markdown(brief: dict[str, Any]) -> str:
    citation_list = ", ".join(citation["id"] for citation in brief["citations"])
    return f"""# {brief['title']}

Status: draft

## Working Thesis

{brief['thesis']}

## Draft

The useful version of this workflow is not broad autonomy. It is a controlled
content system that watches a defined source cluster, identifies the strongest
operator-facing angle, creates a source-grounded brief, and queues a draft for
editorial review.

For this topic, the key signal is that multiple configured sources point to the
same practical question: what should an operator actually do next? The draft
should therefore avoid generic AI commentary and focus on implementation,
trade-offs, and the approval gates that keep the workflow safe.

The article should make one clear argument: an agent content pipeline becomes
valuable when it compresses source scanning and first-draft production, while
leaving claims, voice, and publishing decisions under human review.

## Evidence To Verify

This draft is grounded in citations: {citation_list}.

## Editorial Notes

- Replace offline seed evidence with live source review before publishing.
- Confirm every claim in the final article maps to the citation list.
- Keep the article specific to operator workflow, not generic AI news.
"""


def topic_items(topic: dict[str, Any], items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = item_index(items)
    return [by_id[item_id] for item_id in topic.get("source_item_ids", []) if item_id in by_id]


def best_topic(topics: list[dict[str, Any]]) -> dict[str, Any] | None:
    return topics[0] if topics else None


def best_brief_for_topic(briefs: list[dict[str, Any]], topic: dict[str, Any] | None) -> dict[str, Any] | None:
    if not briefs:
        return None
    if not topic:
        return briefs[0]
    for brief in briefs:
        if brief.get("topic_cluster_id") == topic.get("id"):
            return brief
    return briefs[0]


def citation_lines(brief: dict[str, Any]) -> list[str]:
    return [
        f"- {citation['title']} - {citation['url']}"
        for citation in brief.get("citations", [])
    ]


def source_signal_lines(source_items: list[dict[str, Any]], limit: int = 10) -> list[str]:
    lines = []
    for item in source_items[:limit]:
        summary = item.get("summary", "").strip()
        if len(summary) > 220:
            summary = summary[:217].rstrip() + "..."
        lines.append(f"- {item.get('title', 'Untitled')} - {item.get('url', '')}\n  Signal: {summary}")
    return lines


def derive_business_angle(topic: dict[str, Any] | None, source_items: list[dict[str, Any]]) -> dict[str, str]:
    corpus = " ".join(
        [topic.get("title", "") if topic else ""]
        + [item.get("title", "") + " " + item.get("summary", "") for item in source_items]
    ).lower()
    if "enterprise" in corpus and "agent" in corpus:
        return {
            "title": "The Enterprise Agent Shift Is Not More Tools. It Is Governed Operating Layers.",
            "claim": "Agent adoption is moving from isolated tools to governed operating layers.",
            "decision": "Publish a business-facing piece that connects enterprise agent adoption with the operating-layer pattern: sources, memory, tools, schedules, controls, and approval gates.",
        }
    if "developer" in corpus or "coding" in corpus:
        return {
            "title": "AI Coding Agents Need Workflow Governance Before They Need More Autonomy.",
            "claim": "The useful coding-agent story is moving from raw delegation to governed workflow orchestration.",
            "decision": "Publish a business-facing piece on how agent harnesses turn coding tools into reviewable delivery workflows.",
        }
    return {
        "title": f"{topic.get('theme', 'Agent workflows')} Needs An Operating Layer" if topic else "Agent Workflows Need An Operating Layer",
        "claim": "The content opportunity is a practical implementation story, not a generic AI trend story.",
        "decision": "Publish a business-facing piece that translates the top-ranked source cluster into a governed workflow narrative.",
    }


def article_from_sources(angle: dict[str, str], brief: dict[str, Any], source_items: list[dict[str, Any]]) -> str:
    source_titles = [item.get("title", "source signal") for item in source_items[:5]]
    sources_sentence = "; ".join(source_titles[:3])
    citations = "\n".join(citation_lines(brief))
    return f"""# {angle['title']}

Status: draft

## Working Thesis

{angle['claim']}

## Draft

Most agent conversations still start in the wrong place.

The default question is: what can the agent do?

The better business question is: what recurring workflow can the agent run with enough source grounding, memory, controls, and human approval that the output becomes useful every day?

The live source set for this run points to that second question. The highest-ranked signals included: {sources_sentence}.

The pattern is clear. Enterprises are not only asking for stronger models. They are asking how to put agents into real operating environments: connected to context, grounded in current information, governed by permissions, and observable enough to trust. At the operator level, Hermes-style workflows point in the same direction. The harness matters because it gives the model tools, files, search, memory, schedules, and reusable skills.

That is why the practical content angle is not that AI agents are popular.

The practical angle is that useful agents need operating layers.

## The Wrong Starting Point

The weak version of agent adoption is broad autonomy.

In content work, that sounds like: let the agent write posts.

In sales, it sounds like: let the agent handle outbound.

In engineering, it sounds like: let the agent build the feature.

Those statements skip the actual operating design. They do not define the source boundary, the memory boundary, the approval boundary, the cost boundary, or the failure boundary.

## The Better Starting Point

Start with one narrow workflow.

For the Hermes content pipeline, the useful loop is:

`source scan -> topic ranking -> sourced brief -> draft package -> human review -> memory write-back`

That workflow creates business value because it compresses the work before judgment. The agent monitors sources, clusters signals, creates a brief, drafts a package, and records memory candidates. The human still owns voice, claims, positioning, and publication.

That division of labor is the point.

## What The Operating Layer Needs

A governed agent workflow needs six things:

1. Sources: what the agent is allowed to read.
2. Memory: what should persist across runs.
3. Tools: search, files, extraction, model calls, and connectors.
4. Schedule: when the workflow runs without being asked.
5. Controls: cost caps, model routing, provenance, and logs.
6. Approval gates: where draft work stops and human action begins.

Without those pieces, the agent is an impressive chat session. With those pieces, it becomes operational infrastructure.

## The First Version Should Stay Boring

The right v1 is intentionally limited.

For this content pipeline, that means a small source list, one daily run, a capped number of research briefs, one draft package, visible citations, a run log, and no publishing permission.

That is enough to test whether the workflow produces review-ready business content. It is also constrained enough to avoid the usual failure mode: a broad agent that can technically do many things but cannot be trusted with one recurring job.

## Business Outcome

The useful metric is not content volume.

The useful metric is whether the pipeline can produce review-ready content packages from real source clusters, with the human editor improving judgment and voice instead of starting from a blank page.

That is the operating model worth testing.

## Source Register

{citations}
"""


def linkedin_from_angle(angle: dict[str, str]) -> str:
    return f"""# LinkedIn Post Draft

{angle['claim']}

That is the sharper story behind agent adoption right now.

The weak version is broad autonomy: let the agent handle content, outbound, research, or engineering.

The useful version is a governed workflow:

sources -> memory -> tools -> schedule -> controls -> approval gate

For a Hermes content pipeline, that becomes:

source scan -> topic ranking -> sourced brief -> draft package -> human review -> memory write-back

The business value is not more automated content.

The value is reducing the distance between market signal and review-ready point of view.

The first version should be boring: a small source list, one daily run, capped briefs, one draft package, visible citations, run logs, and no publish permission.

That is how agents move from demo to operations.
"""


def x_thread_from_angle(angle: dict[str, str]) -> str:
    return f"""# X Thread Draft

1. {angle['claim']}

2. The mistake is starting with broad autonomy.

Useful agents start with one governed workflow.

3. The pattern:

sources -> memory -> tools -> schedule -> controls -> approval gate

4. Example: Hermes content pipeline.

source scan -> topic ranking -> sourced brief -> draft package -> human review -> memory write-back

5. The agent compresses the work before judgment.

The human still owns claims, voice, and publication.

6. That is the business distinction.

Not more content.

Faster movement from live market signal to review-ready point of view.
"""


def newsletter_from_angle(angle: dict[str, str]) -> str:
    return f"""# Newsletter Blurb

{angle['claim']}

This run used live source discovery to turn a broad Hermes content-pipeline idea into a business-facing content package.

The useful pattern is not auto-publishing. It is a governed workflow that scans sources, ranks topics, creates a sourced brief, drafts a package, and stops for human review.

The reusable operating model is:

`sources -> memory -> tools -> schedule -> controls -> approval gate`

That is the difference between an agent demo and a workflow an operator can actually trust.
"""


def generate_business_deliverables(
    topics: list[dict[str, Any]],
    briefs: list[dict[str, Any]],
    drafts: list[dict[str, Any]],
    items: list[dict[str, Any]],
    paths: dict[str, Path],
    date: str,
    live: bool,
) -> list[Path]:
    if not topics or not briefs:
        return []

    topic = best_topic(topics)
    brief = best_brief_for_topic(briefs, topic)
    if not brief:
        return []
    related_items = topic_items(topic, items) if topic else items[:10]
    angle = derive_business_angle(topic, related_items)
    out = paths["deliverables"]
    generated: list[Path] = []

    files = {
        "README.md": f"""# Business Deliverables - {date}

Generated by `runner.py`.

## Business Outcome

{angle['claim']}

## Deliverables

- `business-outcome-memo.md`
- `source-register.md`
- `editorial-brief.md`
- `article-draft.md`
- `linkedin-post.md`
- `x-thread.md`
- `newsletter-blurb.md`
- `deliverables-metadata.json`

## Run Mode

{"live You.com source discovery" if live else "offline fixture mode"}

## Draft Boundary

No publish action was taken. All outputs are review artifacts.
""",
        "business-outcome-memo.md": f"""# Business Outcome Memo

## Decision

{angle['decision']}

## Why This Matters

The live source set points to a practical implementation story rather than a generic AI trend. The business opportunity is to explain how agent capability becomes repeatable work when it is wrapped in a governed operating layer.

## Target Buyer

- Enterprise AI operators
- Solution architects
- Founders building internal AI workflows
- Technical executives moving from pilot to production

## Desired Reader Action

Start with one governed workflow that has sources, memory, schedule, cost cap, and an approval gate.

## Business Value

- Supports consulting conversations around agent operating models.
- Positions Hermes as an operator-level agent harness.
- Proves the content pipeline can convert live sources into business deliverables.
- Creates reusable memory for future content runs.

## Success Metrics

- One publishable article approved after human edit.
- One LinkedIn post starts a business discussion.
- Three to five qualified conversations about agent workflow implementation.
""",
        "source-register.md": "# Source Register\n\n"
        + "\n".join(source_signal_lines(related_items, limit=12))
        + "\n\n## Brief Citations\n\n"
        + "\n".join(citation_lines(brief))
        + "\n",
        "editorial-brief.md": f"""# Editorial Brief

## Working Title

{angle['title']}

## Core Angle

{angle['claim']}

## Main Claim

The next practical agent opportunity is not broad autonomy. It is one recurring workflow wrapped with source grounding, durable memory, tool access, scheduled execution, cost controls, and human approval gates.

## Proof Points

{chr(10).join(source_signal_lines(related_items, limit=5))}

## Reader Takeaway

Do not start with a general assistant. Start with one narrow operating workflow.

## Editorial Guardrails

- Do not imply auto-publishing is safe.
- Do not claim agents eliminate human judgment.
- Keep the piece business-facing.
- Tie claims back to cited source URLs.
""",
        "article-draft.md": article_from_sources(angle, brief, related_items),
        "linkedin-post.md": linkedin_from_angle(angle),
        "x-thread.md": x_thread_from_angle(angle),
        "newsletter-blurb.md": newsletter_from_angle(angle),
    }

    for filename, content in files.items():
        path = out / filename
        write_text(path, content)
        generated.append(path)

    metadata = {
        "date": date,
        "mode": "live" if live else "offline",
        "topic_id": topic.get("id") if topic else None,
        "brief_id": brief.get("id"),
        "draft_ids": [draft.get("id") for draft in drafts],
        "business_angle": angle,
        "source_count": len(related_items),
        "deliverables": [path.name for path in generated],
        "publish_allowed": False,
    }
    metadata_path = out / "deliverables-metadata.json"
    write_json(metadata_path, metadata)
    generated.append(metadata_path)
    return generated


def write_memory_candidates(
    briefs: list[dict[str, Any]],
    paths: dict[str, Path],
) -> list[dict[str, Any]]:
    candidates = []
    for brief in briefs:
        candidates.append(
            {
                "id": stable_id(brief["id"], "memory", prefix="mem-"),
                "type": "topic",
                "title": brief["title"],
                "summary": brief["thesis"],
                "provenance": [citation["url"] for citation in brief["citations"]],
                "confidence": "medium",
            }
        )
    write_json(paths["memory"] / "memory-candidates.json", {"candidates": candidates})
    lines = ["# Memory Candidates", ""]
    for candidate in candidates:
        lines.extend(
            [
                f"## {candidate['title']}",
                "",
                candidate["summary"],
                "",
                f"Confidence: {candidate['confidence']}",
                "",
            ]
        )
    write_text(paths["memory"] / "accepted-memory.md", "\n".join(lines))
    return candidates


def build_paths(runtime_root: Path, config: dict[str, Any], date: str) -> dict[str, Path]:
    paths_cfg = config["paths"]
    return {
        "source_items": runtime_root / paths_cfg["source_queue"] / date,
        "topic_clusters": runtime_root / paths_cfg["topic_queue"] / date,
        "research_briefs": runtime_root / paths_cfg["research_briefs"] / date,
        "draft_packages": runtime_root / paths_cfg["draft_packages"] / date,
        "review_decisions": runtime_root / paths_cfg["review_decisions"] / date,
        "logs": runtime_root / paths_cfg["run_logs"] / date,
        "memory": runtime_root / paths_cfg["memory_exports"] / date,
        "deliverables": runtime_root / paths_cfg.get("deliverables", "deliverables") / date,
    }


def write_run_log(
    paths: dict[str, Path],
    run_id: str,
    started_at: str,
    status: str,
    counts: dict[str, int],
    cap_usd: float,
    estimated_usd: float,
    warnings: list[str],
    errors: list[str],
) -> None:
    payload = {
        "run_id": run_id,
        "started_at": started_at,
        "finished_at": iso_now(),
        "status": status,
        "counts": counts,
        "cost": {
            "estimated_usd": round(estimated_usd, 2),
            "cap_usd": cap_usd,
            "cap_exceeded": estimated_usd > cap_usd,
        },
        "model_routes": [
            {"step": "source_scan", "model_class": "none", "model_name": None},
            {"step": "topic_ranking", "model_class": "standard", "model_name": "configured-by-hermes"},
            {"step": "research_brief", "model_class": "standard", "model_name": "configured-by-hermes"},
            {"step": "draft_package", "model_class": "standard", "model_name": "configured-by-hermes"},
        ],
        "errors": errors,
        "warnings": warnings,
    }
    write_json(paths["logs"] / "run-log.json", payload)
    write_text(
        paths["logs"] / "cost-summary.md",
        f"# Cost Summary\n\nEstimated spend: ${estimated_usd:.2f}\n\nCap: ${cap_usd:.2f}\n",
    )
    write_text(
        paths["logs"] / "errors.md",
        "# Errors And Warnings\n\n"
        + "\n".join([f"- ERROR: {error}" for error in errors] + [f"- WARNING: {warning}" for warning in warnings]),
    )


def estimated_cost(source_count: int, topic_count: int, brief_count: int, draft_count: int, live: bool) -> float:
    search_cost = source_count * (0.03 if live else 0)
    return search_cost + topic_count * 0.05 + brief_count * 0.40 + draft_count * 1.50


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--implementation-dir", default=str(IMPLEMENTATION_DIR))
    parser.add_argument("--sources", default="sources.yaml")
    parser.add_argument("--config", default="pipeline-config.yaml")
    parser.add_argument("--output-root", default=None, help="Override runtime output root")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--live", action="store_true", help="Use You.com search instead of offline fixtures")
    parser.add_argument("--force", action="store_true", help="Replace active/stale lock")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    implementation_dir = Path(args.implementation_dir).resolve()
    root = repo_root(implementation_dir)
    sources_config = read_yaml(implementation_dir / args.sources)
    config = read_yaml(implementation_dir / args.config)
    validate_safety(config)

    runtime_root = Path(args.output_root) if args.output_root else root / config["paths"]["root"]
    if not runtime_root.is_absolute():
        runtime_root = root / runtime_root
    paths = build_paths(runtime_root, config, args.date)
    lock_path = runtime_root / config["cron"]["lock_file"]

    started_at = iso_now()
    run_id = stable_id(args.date, str(time.time()), prefix="run-")
    warnings: list[str] = []
    errors: list[str] = []

    status = "success"
    with Lock(lock_path, force=args.force):
        source_items = scan_sources(sources_config, config, paths, args.date, args.live, warnings, errors)
        topics = rank_topics(sources_config, config, source_items, paths, args.date)
        briefs = generate_briefs(topics, source_items, config, paths, warnings)
        drafts = generate_drafts(briefs, config, paths)
        memory_candidates = write_memory_candidates(briefs, paths)
        deliverables = generate_business_deliverables(topics, briefs, drafts, source_items, paths, args.date, args.live)

        if errors:
            status = "partial" if source_items else "failed"
        if not drafts:
            status = "partial"
            warnings.append("no draft package generated")
        if not deliverables:
            status = "partial"
            warnings.append("no business deliverables generated")

        counts = {
            "source_items": len(source_items),
            "topic_clusters": len(topics),
            "research_briefs": len(briefs),
            "draft_packages": len(drafts),
            "memory_candidates": len(memory_candidates),
            "deliverables": len(deliverables),
        }
        cost = estimated_cost(len(source_items), len(topics), len(briefs), len(drafts), args.live)
        cap = float(config["daily_caps"]["estimated_usd"])
        if cost > cap:
            status = "partial"
            errors.append(f"estimated cost ${cost:.2f} exceeded cap ${cap:.2f}")
        write_run_log(paths, run_id, started_at, status, counts, cap, cost, warnings, errors)

    print(f"status={status}")
    print(f"runtime_root={runtime_root}")
    print(f"run_log={paths['logs'] / 'run-log.json'}")
    return 0 if status in {"success", "partial"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
