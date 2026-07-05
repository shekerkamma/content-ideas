#!/usr/bin/env python3
"""Validate AEO workflow kit run contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = {
    "manifest": "manifest.json",
    "queries": "stage_outputs/queries.jsonl",
    "sources": "stage_outputs/sources.jsonl",
    "answer_captures": "stage_outputs/answer_captures.jsonl",
    "entities": "normalized/entities.jsonl",
    "visibility_scores": "normalized/visibility_scores.json",
    "recommendations": "normalized/recommendations.jsonl",
    "report": "final/aeo-audit.md",
    "evidence_csv": "final/evidence.csv",
}

QUERY_FIELDS = {"query_id", "cluster", "persona", "intent", "query", "priority"}
CAPTURE_FIELDS = {"capture_id", "query_id", "engine", "captured_at", "answer_text_path", "citation_urls", "raw_metadata"}
REC_FIELDS = {"recommendation_id", "priority", "theme", "action", "evidence_ids", "expected_impact", "effort", "confidence"}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate(run_dir: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    for name, rel in REQUIRED.items():
        if not (run_dir / rel).exists():
            errors.append(f"missing:{name}:{rel}")
    if errors:
        return {"status": "blocked", "errors": errors, "warnings": warnings}

    manifest = read_json(run_dir / REQUIRED["manifest"])
    queries = read_jsonl(run_dir / REQUIRED["queries"])
    sources = read_jsonl(run_dir / REQUIRED["sources"])
    captures = read_jsonl(run_dir / REQUIRED["answer_captures"])
    recs = read_jsonl(run_dir / REQUIRED["recommendations"])

    query_ids = set()
    for row in queries:
        missing = QUERY_FIELDS - set(row)
        if missing:
            errors.append(f"query_missing_fields:{row.get('query_id', '<unknown>')}:{','.join(sorted(missing))}")
        query_id = row.get("query_id")
        if query_id in query_ids:
            errors.append(f"duplicate_query_id:{query_id}")
        query_ids.add(query_id)

    source_ids = {row.get("source_id") for row in sources}
    capture_ids = set()
    non_live_methods = set()
    for row in captures:
        missing = CAPTURE_FIELDS - set(row)
        if missing:
            errors.append(f"capture_missing_fields:{row.get('capture_id', '<unknown>')}:{','.join(sorted(missing))}")
        if row.get("query_id") not in query_ids:
            errors.append(f"capture_unknown_query:{row.get('capture_id')}:{row.get('query_id')}")
        raw_path = run_dir / row.get("answer_text_path", "")
        if not raw_path.exists():
            errors.append(f"capture_missing_raw_text:{row.get('capture_id')}:{row.get('answer_text_path')}")
        method = (row.get("raw_metadata") or {}).get("collection_method", "")
        if method in {"scorecard_seed", "manual_placeholder"} or row.get("engine") in {"scorecard_seed", "manual_placeholder", "sample"}:
            non_live_methods.add(method or row.get("engine"))
        capture_ids.add(row.get("capture_id"))

    evidence_ids = capture_ids | source_ids
    for row in recs:
        missing = REC_FIELDS - set(row)
        if missing:
            errors.append(f"recommendation_missing_fields:{row.get('recommendation_id', '<unknown>')}:{','.join(sorted(missing))}")
        if not row.get("evidence_ids"):
            errors.append(f"recommendation_without_evidence:{row.get('recommendation_id')}")
        for evidence_id in row.get("evidence_ids", []):
            if evidence_id not in evidence_ids:
                errors.append(f"recommendation_unknown_evidence:{row.get('recommendation_id')}:{evidence_id}")

    if manifest.get("sample"):
        warnings.append("sample_run_status_forced_to_draft")
    if non_live_methods:
        warnings.append("non_live_evidence_status_forced_to_draft:" + ",".join(sorted(non_live_methods)))

    status = "blocked" if errors else ("draft" if manifest.get("sample") or non_live_methods else "reviewed")
    return {"status": status, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    result = validate(args.run_dir)
    qa_dir = args.run_dir / "qa"
    qa_dir.mkdir(parents=True, exist_ok=True)
    (qa_dir / "validation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    manifest_path = args.run_dir / "manifest.json"
    if manifest_path.exists():
        manifest = read_json(manifest_path)
        manifest["validation_status"] = result["status"]
        manifest["stage_status"]["validate"] = "failed" if result["errors"] else "passed"
        manifest["status"] = result["status"]
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    report_path = args.run_dir / "final" / "aeo-audit.md"
    if report_path.exists():
        text = report_path.read_text(encoding="utf-8")
        lines = [
            f"- Status: {result['status']}" if line.startswith("- Status: ") else line
            for line in text.splitlines()
        ]
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(result, indent=2))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
