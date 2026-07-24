#!/usr/bin/env python3
"""Collect pasted live AI-answer captures for an existing AEO run."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ORCHESTRATOR_SCRIPTS = Path(__file__).resolve().parents[2] / "aeo-orchestrator" / "scripts"
sys.path.insert(0, str(ORCHESTRATOR_SCRIPTS))

from run_pipeline import (  # noqa: E402
    append_jsonl,
    build_entities,
    build_recommendations,
    build_sources,
    now_iso,
    read_json,
    read_jsonl,
    render_outputs,
    score_visibility,
    write_json,
)


NON_LIVE_ENGINES = {"scorecard_seed", "manual_placeholder", "sample"}
NON_LIVE_METHODS = {"scorecard_seed", "manual_placeholder"}


def is_non_live(capture: dict) -> bool:
    method = (capture.get("raw_metadata") or {}).get("collection_method", "")
    return capture.get("engine") in NON_LIVE_ENGINES or method in NON_LIVE_METHODS


def next_live_id(existing: list[dict]) -> str:
    max_id = 0
    for row in existing:
        capture_id = row.get("capture_id", "")
        if capture_id.startswith("cap_live_"):
            try:
                max_id = max(max_id, int(capture_id.rsplit("_", 1)[1]))
            except ValueError:
                pass
    return f"cap_live_{max_id + 1:03d}"


def parse_urls(raw: str) -> list[str]:
    return [part.strip() for part in raw.replace("\n", ",").split(",") if part.strip()]


def multiline_input(prompt: str) -> str:
    print(prompt)
    print("Paste text. End with a line containing only: EOF")
    lines: list[str] = []
    while True:
        line = input()
        if line.strip() == "EOF":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def interactive_answers(queries: list[dict], limit: int | None) -> list[dict]:
    selected = sorted(queries, key=lambda row: (row.get("priority", 99), row.get("query_id", "")))
    if limit:
        selected = selected[:limit]
    answers: list[dict] = []
    for query in selected:
        print("\n" + "=" * 72)
        print(f"{query['query_id']}: {query['query']}")
        print("=" * 72)
        use = input("Capture this query? [y/N] ").strip().lower()
        if use != "y":
            continue
        engine = input("Engine used (ChatGPT/Claude/Perplexity/Google AI Mode/etc): ").strip() or "manual_live"
        answer = multiline_input("Answer text:")
        urls = parse_urls(input("Citation URLs, comma-separated if shown: ").strip())
        answers.append(
            {
                "query_id": query["query_id"],
                "engine": engine,
                "answer": answer,
                "citation_urls": urls,
            }
        )
    return answers


def load_answers(path: Path | None, use_stdin: bool) -> list[dict]:
    if use_stdin:
        return json.loads(sys.stdin.read())
    if path:
        return json.loads(path.read_text(encoding="utf-8"))
    return []


def write_live_captures(run_dir: Path, answers: list[dict], replace_non_live: bool) -> list[dict]:
    captures_path = run_dir / "stage_outputs" / "answer_captures.jsonl"
    existing = read_jsonl(captures_path)
    kept = [row for row in existing if not (replace_non_live and is_non_live(row))]
    raw_dir = run_dir / "stage_outputs" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    for answer in answers:
        if not answer.get("query_id") or not answer.get("answer"):
            raise SystemExit("Each answer requires query_id and answer")
        capture_id = next_live_id(kept)
        raw_path = raw_dir / f"{capture_id}.txt"
        raw_path.write_text(answer["answer"].strip() + "\n", encoding="utf-8")
        kept.append(
            {
                "capture_id": capture_id,
                "query_id": answer["query_id"],
                "engine": answer.get("engine", "manual_live"),
                "captured_at": answer.get("captured_at", now_iso()),
                "answer_text_path": str(raw_path.relative_to(run_dir)),
                "citation_urls": answer.get("citation_urls", []),
                "raw_metadata": {
                    **answer.get("raw_metadata", {}),
                    "collection_method": "manual_live_capture",
                },
            }
        )
    append_jsonl(captures_path, kept)
    return kept


def recompute(run_dir: Path, captures: list[dict]) -> None:
    config = read_json(run_dir / "inputs" / "config.json")
    queries = read_jsonl(run_dir / "stage_outputs" / "queries.jsonl")

    sources = build_sources(config, captures)
    append_jsonl(run_dir / "stage_outputs" / "sources.jsonl", sources)

    entities = build_entities(config, captures, run_dir)
    append_jsonl(run_dir / "normalized" / "entities.jsonl", entities)

    scores = score_visibility(config, queries, captures, run_dir)
    write_json(run_dir / "normalized" / "visibility_scores.json", scores)

    recs = build_recommendations(config, scores)
    append_jsonl(run_dir / "normalized" / "recommendations.jsonl", recs)

    render_outputs(run_dir, config, queries, captures, scores, recs)

    manifest = read_json(run_dir / "manifest.json")
    manifest["stage_status"]["answer_capture"] = "passed"
    manifest["stage_status"]["source_discovery"] = "passed"
    manifest["stage_status"]["normalize_extract"] = "passed"
    manifest["stage_status"]["score"] = "passed"
    manifest["stage_status"]["synthesize"] = "passed"
    manifest["stage_status"]["render"] = "passed"
    manifest["validation_status"] = "pending"
    manifest["status"] = "draft"
    write_json(run_dir / "manifest.json", manifest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--answers-json", type=Path)
    parser.add_argument("--stdin-json", action="store_true")
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--replace-non-live", action="store_true")
    args = parser.parse_args()

    run_dir = args.run_dir
    queries = read_jsonl(run_dir / "stage_outputs" / "queries.jsonl")
    answers = load_answers(args.answers_json, args.stdin_json)
    if args.interactive:
        answers.extend(interactive_answers(queries, args.limit))
    if not answers:
        raise SystemExit("No answers supplied. Use --interactive, --answers-json, or --stdin-json.")

    captures = write_live_captures(run_dir, answers, args.replace_non_live)
    recompute(run_dir, captures)
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
