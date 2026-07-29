#!/usr/bin/env python3
"""Initialize, inspect, and validate evidence-led competitor-analysis runs."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


SKILL = Path(__file__).resolve().parents[1]
CONTRACT_PATH = SKILL / "references" / "skillpipe.json"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def load_contract() -> dict[str, Any]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def rel_exists(run: Path, rel: str) -> bool:
    return (run / rel).exists()


def glob_exists(run: Path, pattern: str) -> bool:
    return any(run.glob(pattern))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def init_run(args: argparse.Namespace) -> int:
    run = args.run.resolve()
    for rel in ("inputs", "working", "outputs", "client-package/site", "client-package/qa"):
        (run / rel).mkdir(parents=True, exist_ok=True)
    status_path = run / "status.json"
    if status_path.exists():
        print(f"PRESERVED: {status_path}")
        return 0
    status = {
        "run_id": run.name,
        "target": args.target,
        "artifact_status": "draft",
        "current_stage": "frame",
        "minimum_slide_count": args.min_slides,
        "completed_gates": [],
        "blocked_gates": [],
        "artifact_paths": {
            "operating_prompt": "inputs/operating-prompt.yaml",
            "evidence_ledger": "outputs/evidence-ledger.csv",
            "allowed_numbers": "outputs/allowed-numbers.yaml",
            "story_pack": "outputs/story-architect-pack.md",
            "reviewed_pptx": None,
            "html_local": "client-package/site/index.html",
            "manifest": "client-package/delivery-manifest.json"
        },
        "next_command": (
            "Inventory existing sources and write inputs/operating-prompt.yaml plus "
            "outputs/search-log.md"
        ),
        "updated_at": utc_now()
    }
    write_json(status_path, status)
    print(f"CREATED: {status_path}")
    return 0


def stage_report(run: Path, stage: dict[str, Any]) -> dict[str, Any]:
    required = stage.get("requires_all", [])
    required_any = stage.get("requires_any", [])
    required_globs = stage.get("requires_glob", [])
    missing = [item for item in required if not rel_exists(run, item)]
    missing_globs = [item for item in required_globs if not glob_exists(run, item)]
    any_ok = not required_any or any(rel_exists(run, item) for item in required_any)
    if not any_ok:
        missing.append("one of: " + ", ".join(required_any))
    return {
        "stage": stage["id"],
        "passed": not missing and not missing_globs,
        "missing": missing,
        "missing_globs": missing_globs,
        "gate": stage["gate"]
    }


def validate(args: argparse.Namespace) -> int:
    run = args.run.resolve()
    contract = load_contract()
    if not run.exists():
        raise SystemExit(f"run folder not found: {run}")
    if args.stage == "complete":
        reports = [stage_report(run, stage) for stage in contract["stages"]]
        missing = [item for item in contract["complete_requires"] if not rel_exists(run, item)]
        missing_globs = [
            item for item in contract["complete_globs"] if not glob_exists(run, item)
        ]
        passed = all(item["passed"] for item in reports) and not missing and not missing_globs
        result = {
            "contract_version": contract["contract_version"],
            "run": str(run),
            "stage": "complete",
            "passed": passed,
            "stage_reports": reports,
            "missing": missing,
            "missing_globs": missing_globs,
            "checked_at": utc_now()
        }
    else:
        stage = next((item for item in contract["stages"] if item["id"] == args.stage), None)
        if not stage:
            names = ", ".join(item["id"] for item in contract["stages"])
            raise SystemExit(f"unknown stage {args.stage!r}; choose one of: {names}, complete")
        result = stage_report(run, stage)
        result.update({"run": str(run), "checked_at": utc_now()})
        passed = result["passed"]
    if args.json_out:
        write_json(args.json_out.resolve(), result)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if passed else 1


def status(args: argparse.Namespace) -> int:
    run = args.run.resolve()
    path = run / "status.json"
    if not path.exists():
        print(f"NO STATUS: {path}")
        return 1
    state = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(state, indent=2, ensure_ascii=False))
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="initialize a run without overwriting existing files")
    init.add_argument("run", type=Path)
    init.add_argument("--target", required=True)
    init.add_argument("--min-slides", type=int, default=20)
    init.set_defaults(func=init_run)
    show = sub.add_parser("status", help="print status.json")
    show.add_argument("run", type=Path)
    show.set_defaults(func=status)
    check = sub.add_parser("validate", help="validate stage handoff artifacts")
    check.add_argument("run", type=Path)
    check.add_argument(
        "--stage",
        default="complete",
        choices=["frame", "research", "evidence", "story", "artifacts", "qa", "complete"]
    )
    check.add_argument("--json-out", type=Path)
    check.set_defaults(func=validate)
    return p


def main() -> int:
    args = parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
