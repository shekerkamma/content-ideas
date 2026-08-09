#!/usr/bin/env python3
"""Validate and ingest the AEO AI-answer capture matrix."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


RUN_ROOT = Path(__file__).resolve().parents[3]
LIVE_CAPTURE_SCRIPT = RUN_ROOT / "skills" / "aeo-live-capture" / "scripts" / "capture_answers.py"
LOOP_SCRIPT = RUN_ROOT / "skills" / "aeo-evidence-sprint-loop" / "scripts" / "run_loop.py"


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_rows(rows: list[dict], min_captures: int, min_engines: int) -> list[str]:
    errors: list[str] = []
    if len(rows) < min_captures:
        errors.append(f"needs_at_least_{min_captures}_rows")
    engines = {row.get("engine") for row in rows if row.get("engine")}
    if len(engines) < min_engines:
        errors.append(f"needs_at_least_{min_engines}_engines")
    for index, row in enumerate(rows, start=1):
        label = row.get("task_id") or f"row_{index}"
        if not row.get("query_id"):
            errors.append(f"{label}:missing_query_id")
        if not row.get("engine"):
            errors.append(f"{label}:missing_engine")
        answer = (row.get("answer") or "").strip()
        if not answer:
            errors.append(f"{label}:missing_answer")
        if row.get("captured_at") in {"YYYY-MM-DDTHH:MM:SSZ", "", None}:
            errors.append(f"{label}:missing_captured_at")
        prompt = (row.get("prompt") or "").lower()
        answer_lower = answer.lower()
        if "agent replacement scorecard" in prompt:
            errors.append(f"{label}:target_seeded_prompt")
        if "agent replacement scorecard" in answer_lower:
            errors.append(f"{label}:answer_mentions_target_asset")
    return errors


def to_answers_json(rows: list[dict]) -> list[dict]:
    answers = []
    for row in rows:
        answers.append(
            {
                "query_id": row["query_id"],
                "engine": row["engine"],
                "answer": row["answer"],
                "citation_urls": row.get("citation_urls") or [],
                "captured_at": row.get("captured_at"),
                "raw_metadata": {
                    "source_task_id": row.get("task_id"),
                    "source_prompt_id": row.get("prompt_id"),
                    "source_prompt": row.get("prompt"),
                    "collection_note": "AEO non-target-seeded capture matrix",
                },
            }
        )
    return answers


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--template", type=Path)
    parser.add_argument("--min-captures", type=int, default=20)
    parser.add_argument("--min-engines", type=int, default=3)
    parser.add_argument("--replace-non-live", action="store_true")
    parser.add_argument("--no-rerun-loop", action="store_true")
    args = parser.parse_args()

    run_dir = args.run_dir
    template = args.template or run_dir / "stage_outputs" / "ai_live_capture_ingest_template.json"
    rows = read_json(template)
    if not isinstance(rows, list):
        raise SystemExit("Capture template must be a JSON list")
    errors = validate_rows(rows, args.min_captures, args.min_engines)
    if errors:
        report = {
            "status": "blocked",
            "template": str(template),
            "errors": errors,
            "counts": {
                "rows": len(rows),
                "engines": dict(Counter(row.get("engine") for row in rows if row.get("engine"))),
                "filled_answers": sum(1 for row in rows if (row.get("answer") or "").strip()),
            },
        }
        out = run_dir / "qa" / "ai_capture_matrix_validation.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(out)
        raise SystemExit("Capture matrix is not ready for ingest")

    answers_path = run_dir / "stage_outputs" / "ai_live_answers_for_ingest.json"
    answers_path.write_text(json.dumps(to_answers_json(rows), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    cmd = [sys.executable, str(LIVE_CAPTURE_SCRIPT), str(run_dir), "--answers-json", str(answers_path)]
    if args.replace_non_live:
        cmd.append("--replace-non-live")
    subprocess.run(cmd, check=True)
    if not args.no_rerun_loop:
        subprocess.run([sys.executable, str(LOOP_SCRIPT), str(run_dir)], check=True)
    print(answers_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
