#!/usr/bin/env python3
"""Run the AEO real-evidence sprint loop for one run folder."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[3]
REDDIT_SCRIPT = RUN_ROOT / "skills" / "aeo-reddit-opportunity-finder" / "scripts" / "find_opportunities.py"
PATTERN_SCRIPT = RUN_ROOT / "skills" / "aeo-pattern-miner" / "scripts" / "mine_patterns.py"


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


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_script(script: Path, run_dir: Path) -> None:
    subprocess.run([sys.executable, str(script), str(run_dir)], check=True)


def selected_probes(run_dir: Path, limit: int = 8) -> list[dict]:
    probes = read_jsonl(run_dir / "stage_outputs" / "reddit_semantic_probes.jsonl")
    priority = {
        "job_to_be_done": 0,
        "software_failure": 1,
        "ai_skepticism": 2,
        "comparison_frame": 3,
        "switching_trigger": 4,
        "pattern_validation": 5,
    }
    probes.sort(key=lambda row: (priority.get(row.get("probe_type", ""), 99), row.get("topic", ""), row.get("subreddit", "")))
    selected: list[dict] = []
    seen_topics: set[str] = set()
    seen_probe_ids: set[str] = set()
    for probe_type in ["job_to_be_done", "software_failure", "ai_skepticism", "comparison_frame", "switching_trigger"]:
        for probe in probes:
            topic = probe.get("topic", "")
            probe_id = probe.get("probe_id", "")
            if probe.get("probe_type") != probe_type or topic in seen_topics or probe_id in seen_probe_ids:
                continue
            selected.append(probe)
            seen_topics.add(topic)
            seen_probe_ids.add(probe_id)
            if len(selected) >= limit:
                return selected
    for probe in probes:
        topic = probe.get("topic", "")
        probe_id = probe.get("probe_id", "")
        if topic in seen_topics or probe_id in seen_probe_ids:
            continue
        selected.append(probe)
        seen_topics.add(topic)
        seen_probe_ids.add(probe_id)
        if len(selected) >= limit:
            break
    return selected


def prompt_from_probe(index: int, probe: dict) -> dict:
    topic = probe.get("topic", "this workflow")
    probe_type = probe.get("probe_type", "buyer_question")
    if probe_type == "job_to_be_done":
        prompt = f"What software or workflow do teams usually use to handle {topic}, and where are AI agents realistically useful or not useful?"
    elif probe_type == "software_failure":
        prompt = f"When {topic} software is expensive or creates manual workarounds, what should a company automate, renegotiate, or keep?"
    elif probe_type == "ai_skepticism":
        prompt = f"What are the main reasons AI agents fail or need human review in {topic} workflows?"
    elif probe_type == "comparison_frame":
        prompt = f"What are the practical alternatives teams compare when choosing how to handle {topic}: SaaS tools, internal workflows, outsourcing, or AI agents?"
    elif probe_type == "switching_trigger":
        competitor = probe.get("competitor") or "an incumbent SaaS vendor"
        prompt = f"What would make a company switch away from {competitor} or reduce usage for {topic}?"
    else:
        prompt = f"What real examples support or challenge this SaaS-and-agent pattern: {topic}?"
    return {
        "prompt_id": f"aip_{index:03d}",
        "source_probe_id": probe.get("probe_id"),
        "probe_type": probe_type,
        "topic": topic,
        "subreddit_context": probe.get("subreddit"),
        "prompt": prompt,
        "target_seeded": False,
        "required_engines": ["ChatGPT", "Claude", "Perplexity", "Google AI Mode"],
        "capture_instruction": "Paste dated, verbatim answers into the AEO live-capture workflow. Do not mention the target asset or scorecard in the prompt.",
    }


def generate_prompt_pack(run_dir: Path) -> list[dict]:
    probes = selected_probes(run_dir)
    prompts = [prompt_from_probe(index, probe) for index, probe in enumerate(probes, start=1)]
    write_jsonl(run_dir / "stage_outputs" / "ai_answer_prompt_pack.jsonl", prompts)
    return prompts


def reddit_skill_queue_item(index: int, probe: dict) -> dict:
    probe_type = probe.get("probe_type", "buyer_question")
    topic = probe.get("topic", "this workflow")
    subreddit = probe.get("subreddit")
    if probe_type in {"job_to_be_done", "software_failure", "ai_skepticism", "comparison_frame"}:
        recommended_skill = "reddit-new-factcheck"
        extraction_goal = "Qualify whether real Reddit practitioner language supports the AEO pain, objection, or comparison frame."
        factcheck_question = f"Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around {topic}?"
    else:
        recommended_skill = "reddit-seo-pipeline"
        extraction_goal = "Extract candidate threads for manual analysis once a specific Reddit URL is found."
        factcheck_question = f"Which specific Reddit threads show a high-intent switching or comparison discussion around {topic}?"
    return {
        "queue_id": f"rsq_{index:03d}",
        "source_probe_id": probe.get("probe_id"),
        "recommended_skill": recommended_skill,
        "subreddits": [subreddit] if subreddit else [],
        "semantic_probe": {
            "topic": topic,
            "probe_type": probe_type,
            "buyer_job": probe.get("buyer_job"),
            "failure_mode": probe.get("failure_mode"),
            "competitor": probe.get("competitor"),
            "semantic_selection_criteria": probe.get("semantic_selection_criteria"),
        },
        "factcheck_question": factcheck_question,
        "extraction_goal": extraction_goal,
        "evidence_required": [
            "thread_url",
            "subreddit",
            "comment_or_post_locator",
            "dated excerpt",
            "persona/workflow match",
            "concrete pain, workaround, objection, adoption signal, or comparison",
        ],
        "status": "needs_external_retrieval",
    }


def generate_reddit_skill_queue(run_dir: Path) -> list[dict]:
    probes = selected_probes(run_dir, limit=12)
    queue = [reddit_skill_queue_item(index, probe) for index, probe in enumerate(probes, start=1)]
    write_jsonl(run_dir / "stage_outputs" / "reddit_skill_queue.jsonl", queue)
    write_json(run_dir / "stage_outputs" / "reddit_factcheck_claim_pack.json", reddit_factcheck_claim_pack(queue))
    brief_path = run_dir / "final" / "reddit-skill-loop-brief.md"
    brief_path.write_text(render_reddit_skill_brief(run_dir, queue), encoding="utf-8")
    return queue


def generate_ai_capture_matrix(run_dir: Path, prompts: list[dict]) -> list[dict]:
    engines = ["ChatGPT", "Claude", "Perplexity", "Google AI Mode"]
    topic_query_ids = {
        "ad & creative generation at scale": "q_031",
        "ai shopping / sales consultant": "q_006",
        "conversational support": "q_001",
        "doc summarization & drafting": "q_021",
        "legal research & drafting": "q_026",
        "messaging-channel chatbot": "q_016",
        "personalized marketing content": "q_036",
        "travel & booking planner": "q_011",
    }
    selected_prompts = prompts[:5]
    rows: list[dict] = []
    for prompt in selected_prompts:
        for engine in engines:
            rows.append(
                {
                    "task_id": f"act_{len(rows)+1:03d}",
                    "prompt_id": prompt["prompt_id"],
                    "query_id": topic_query_ids.get(prompt.get("topic"), ""),
                    "source_probe_id": prompt.get("source_probe_id"),
                    "topic": prompt.get("topic"),
                    "engine": engine,
                    "prompt": prompt["prompt"],
                    "capture_status": "needed",
                    "evidence_rule": "Run this exact prompt in the named engine. Do not mention the target asset, scorecard, brand, or URL. Paste the dated verbatim answer and visible citation URLs into a live-capture ingest file.",
                }
            )
    write_jsonl(run_dir / "stage_outputs" / "ai_answer_capture_matrix.jsonl", rows)
    template = [
        {
            "task_id": row["task_id"],
            "prompt_id": row["prompt_id"],
            "query_id": row["query_id"],
            "engine": row["engine"],
            "prompt": row["prompt"],
            "captured_at": "YYYY-MM-DDTHH:MM:SSZ",
            "answer": "",
            "citation_urls": [],
            "notes": "Fill answer/citations after running the exact prompt in the named engine. Leave prompt unchanged.",
        }
        for row in rows
    ]
    write_json(run_dir / "stage_outputs" / "ai_live_capture_ingest_template.json", template)
    brief_path = run_dir / "final" / "ai-answer-capture-plan.md"
    brief_path.write_text(render_ai_capture_plan(run_dir, rows), encoding="utf-8")
    return rows


def render_ai_capture_plan(run_dir: Path, rows: list[dict]) -> str:
    engines = sorted({row["engine"] for row in rows})
    prompts = sorted({row["prompt_id"] for row in rows})
    lines = [
        "# AI Answer Capture Plan",
        "",
        f"- Run: `{run_dir.name}`",
        f"- Required independent captures: `{len(rows)}`",
        f"- Required engines: `{len(engines)}` ({', '.join(engines)})",
        f"- Prompt coverage: `{len(prompts)}` non-target-seeded prompts",
        "",
        "## Evidence Rules",
        "",
        "- Run each prompt exactly as written.",
        "- Do not mention the target asset, scorecard, brand, page URL, or this workflow.",
        "- Paste the full dated answer text and any visible citation/source URLs.",
        "- If an engine shows no citations, leave citations empty and preserve the answer text.",
        "- Do not synthesize, summarize, rewrite, or backfill answers.",
        "",
        "## Capture Matrix",
        "",
    ]
    for row in rows:
        lines.append(f"### {row['task_id']} - {row['engine']} - {row['prompt_id']}")
        lines.append("")
        lines.append(row["prompt"])
        lines.append("")
    lines.extend(
        [
            "## Ingest",
            "",
            "Fill `stage_outputs/ai_live_capture_ingest_template.json` with the real answers.",
            "Then ingest with the AEO live-capture workflow or transform each filled item into `aeo-live-capture` answers-json rows.",
            "",
        ]
    )
    return "\n".join(lines)


def reddit_factcheck_claim_pack(queue: list[dict]) -> dict:
    claims = []
    for item in queue:
        probe = item["semantic_probe"]
        topic = probe.get("topic") or "this workflow"
        subreddit = item["subreddits"][0] if item["subreddits"] else "SaaS"
        if item["recommended_skill"] == "reddit-new-factcheck":
            query = f"subreddit:{subreddit} {topic} AI workflow pain workaround objection comparison"
        else:
            query = f"subreddit:{subreddit} {topic} SaaS AI agent replacement workflow"
        claims.append(
            {
                "claim_id": item["queue_id"].replace("rsq_", "RC-"),
                "source_locator": item["source_probe_id"],
                "claim_text": item["factcheck_question"],
                "evidence_need": "reddit_evidence",
                "reddit_query": query,
                "probe_type": probe.get("probe_type"),
                "semantic_selection_criteria": {
                    "persona_workflow_match": True,
                    "requires_concrete_signal": True,
                    "reject_literal_keyword_only_matches": True,
                    "accepted_signals": [
                        "pain",
                        "workaround",
                        "objection",
                        "adoption signal",
                        "comparison",
                    ],
                },
            }
        )
    return {
        "source": "aeo-evidence-sprint-loop",
        "method": "semantic_reddit_queue_for_factcheck",
        "claims": claims,
        "limitations": [
            "Queries are discovery prompts only; accepted evidence requires semantic qualification.",
            "Do not accept a Reddit result because it matched keywords.",
        ],
    }


def evidence_status(run_dir: Path, prompts: list[dict]) -> dict:
    reddit_language = read_jsonl(run_dir / "normalized" / "reddit_buyer_language.jsonl")
    captures = read_jsonl(run_dir / "stage_outputs" / "answer_captures.jsonl")
    capture_units = read_jsonl(run_dir / "normalized" / "capture_units.jsonl")
    pattern_candidates = read_jsonl(run_dir / "normalized" / "pattern_candidates.jsonl")
    reviews = read_jsonl(run_dir / "normalized" / "pattern_reviews.jsonl")
    target_seeded_capture_ids = {row.get("capture_id") for row in capture_units if row.get("target_seeded")}
    manual_live_captures = [
        row
        for row in captures
        if (row.get("raw_metadata") or {}).get("collection_method") == "manual_live_capture"
        and row.get("engine") not in {"scorecard_seed", "manual_placeholder", "sample"}
    ]
    independent_captures = [row for row in manual_live_captures if row.get("capture_id") not in target_seeded_capture_ids]
    independent_engines = {row.get("engine") for row in independent_captures if row.get("engine")}
    target_seeded_candidates = [
        row
        for row in pattern_candidates
        if row.get("confidence") in {"high", "medium"} and row.get("target_seeded_evidence_units", 0)
    ]
    accepted_reviews = [row for row in reviews if row.get("decision") == "accept"]
    gates = {
        "reddit_buyer_language_min_5": len(reddit_language) >= 5,
        "independent_ai_answer_captures_min_20": len(independent_captures) >= 20,
        "independent_answer_engines_min_3": len(independent_engines) >= 3,
        "no_promoted_target_seeded_patterns": not target_seeded_candidates,
        "review_acceptance_or_package_ready": bool(accepted_reviews) or bool(pattern_candidates),
        "prompt_pack_ready": len(prompts) >= 5,
    }
    if all(gates.values()):
        status = "evidence_ready"
    elif gates["prompt_pack_ready"]:
        status = "evidence_collecting"
    else:
        status = "workflow_ready"
    return {
        "status": status,
        "gates": gates,
        "counts": {
            "reddit_buyer_language_rows": len(reddit_language),
            "ai_answer_prompt_rows": len(prompts),
            "answer_captures": len(captures),
            "manual_live_captures": len(manual_live_captures),
            "independent_ai_answer_captures": len(independent_captures),
            "independent_answer_engines": len(independent_engines),
            "target_seeded_capture_ids": len(target_seeded_capture_ids),
            "pattern_candidates": len(pattern_candidates),
            "accepted_pattern_reviews": len(accepted_reviews),
        },
        "engine_counts": dict(Counter(row.get("engine") for row in captures if row.get("engine"))),
        "independent_engine_counts": dict(Counter(row.get("engine") for row in independent_captures if row.get("engine"))),
        "next_missing_gates": [name for name, passed in gates.items() if not passed],
    }


def render_reddit_skill_brief(run_dir: Path, queue: list[dict]) -> str:
    lines = [
        "# Reddit Skill Loop Brief",
        "",
        f"- Run: `{run_dir.name}`",
        "- Purpose: use Reddit as semantic buyer-language evidence for AEO, not keyword matching and not automated posting.",
        "- Status: `needs_external_retrieval` until real thread/comment exports are loaded.",
        "",
        "## Skill Roles",
        "",
        "- `reddit-new-factcheck`: qualify whether a semantic pain, objection, or comparison has real Reddit practitioner support.",
        "- `reddit-seo-pipeline`: extract and analyze a known high-value Reddit thread; use for manual strategy only.",
        "",
        "## Generated Fact-Check Pack",
        "",
        "- `stage_outputs/reddit_factcheck_claim_pack.json` can be passed to `reddit-new-factcheck/scripts/old_reddit_evidence.py` or used with Exa/ScrapeCreators/logged-in Reddit discovery.",
        "- Query strings are discovery aids only; the acceptance gate is semantic qualification.",
        "",
        "## Queue",
        "",
    ]
    for item in queue:
        probe = item["semantic_probe"]
        lines.append(f"### {item['queue_id']} - {item['recommended_skill']}")
        lines.append("")
        lines.append(f"- Source probe: `{item['source_probe_id']}`")
        lines.append(f"- Topic: {probe.get('topic')}")
        lines.append(f"- Probe type: `{probe.get('probe_type')}`")
        if item["subreddits"]:
            lines.append(f"- Candidate subreddit: `{', '.join(item['subreddits'])}`")
        lines.append(f"- Fact-check question: {item['factcheck_question']}")
        lines.append(f"- Extraction goal: {item['extraction_goal']}")
        lines.append("- Evidence gate: accept only persona/workflow-matched posts or comments with concrete pain, workaround, objection, adoption signal, or comparison.")
        lines.append("")
    lines.extend(
        [
            "## How To Use",
            "",
            "1. For each `reddit-new-factcheck` item, discover or provide Reddit thread URLs using logged-in Reddit, `you-com-search`, Exa, ScrapeCreators, or `old_reddit_evidence.py` if reachable.",
            "2. For each known URL, run `reddit-seo-pipeline` extraction and save thread JSON into this run.",
            "3. Save old Reddit fallback output under `stage_outputs/reddit_evidence_raw/` or convert accepted posts/comments into `stage_outputs/reddit_threads.jsonl` / `stage_outputs/reddit_comments.jsonl`.",
            "4. Rerun `aeo-evidence-sprint-loop`; the loop will normalize buyer language and rerun semantic pattern mining.",
            "",
            "Do not count the queue itself as evidence. It is only the retrieval worklist.",
            "",
        ]
    )
    return "\n".join(lines)


def render_plan(run_dir: Path, prompts: list[dict], status: dict, reddit_queue: list[dict], capture_matrix: list[dict]) -> str:
    lines = [
        "# Real Evidence Sprint Loop",
        "",
        f"- Run: `{run_dir.name}`",
        f"- Loop status: `{status['status']}`",
        "",
        "## Gate Status",
        "",
    ]
    for gate, passed in status["gates"].items():
        marker = "PASS" if passed else "TODO"
        lines.append(f"- {marker}: `{gate}`")
    lines.extend(["", "## Counts", ""])
    for name, value in status["counts"].items():
        lines.append(f"- {name}: {value}")
    lines.extend(["", "## AI Answer Prompt Pack", ""])
    for prompt in prompts:
        lines.append(f"### {prompt['prompt_id']} - {prompt['probe_type']}")
        lines.append("")
        lines.append(prompt["prompt"])
        lines.append("")
        lines.append(f"- Source probe: `{prompt['source_probe_id']}`")
        lines.append(f"- Required engines: {', '.join(prompt['required_engines'])}")
        lines.append("")
    lines.extend(["## Reddit Skill Queue", ""])
    for item in reddit_queue[:8]:
        lines.append(f"- `{item['queue_id']}` -> `{item['recommended_skill']}`: {item['factcheck_question']}")
    if len(reddit_queue) > 8:
        lines.append(f"- plus {len(reddit_queue) - 8} additional queue items in `stage_outputs/reddit_skill_queue.jsonl`")
    lines.append("")
    lines.extend(["## AI Answer Capture Matrix", ""])
    lines.append(f"- Capture tasks: {len(capture_matrix)}")
    lines.append("- File: `stage_outputs/ai_answer_capture_matrix.jsonl`")
    lines.append("- Ingest template: `stage_outputs/ai_live_capture_ingest_template.json`")
    lines.append("- Instructions: `final/ai-answer-capture-plan.md`")
    lines.append("")
    lines.extend(
        [
            "## Next Loop",
            "",
            "1. Use `final/reddit-skill-loop-brief.md` and `stage_outputs/reddit_skill_queue.jsonl` to collect real Reddit thread/comment evidence.",
            "2. Load real Reddit threads/comments into `stage_outputs/reddit_threads.jsonl` or `stage_outputs/reddit_comments.jsonl`.",
            "3. Capture the matrix answers from ChatGPT, Claude, Perplexity, and Google AI Mode.",
            "4. Add captures through `aeo-live-capture`.",
            "5. Rerun this loop until gates pass.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    run_dir = args.run_dir
    run_script(REDDIT_SCRIPT, run_dir)
    run_script(PATTERN_SCRIPT, run_dir)
    prompts = generate_prompt_pack(run_dir)
    reddit_queue = generate_reddit_skill_queue(run_dir)
    capture_matrix = generate_ai_capture_matrix(run_dir, prompts)
    status = evidence_status(run_dir, prompts)
    status_path = run_dir / "qa" / "evidence_sprint_status.json"
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(status, indent=2), encoding="utf-8")
    plan_path = run_dir / "final" / "real-evidence-sprint-plan.md"
    plan_path.write_text(render_plan(run_dir, prompts, status, reddit_queue, capture_matrix), encoding="utf-8")
    print(plan_path)
    print(status_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
