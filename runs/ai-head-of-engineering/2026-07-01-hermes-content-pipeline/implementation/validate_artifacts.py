#!/usr/bin/env python3
"""Lightweight artifact validator for the draft-only content pipeline.

This intentionally avoids external JSON Schema dependencies. It checks the
contract fields that matter for the v1 smoke test.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "source-item": ["id", "source_id", "cluster_id", "title", "url", "fetched_at", "summary", "status"],
    "topic-cluster": ["id", "date", "title", "source_item_ids", "score", "score_reasons", "recommended_angle", "status"],
    "research-brief": ["id", "topic_cluster_id", "title", "thesis", "evidence", "citations", "risks", "status"],
    "draft-package": ["id", "research_brief_id", "title", "article_markdown_path", "variants", "citation_map", "status"],
    "run-log": ["run_id", "started_at", "finished_at", "status", "counts", "cost", "model_routes"],
}

REQUIRED_DELIVERABLES = [
    "README.md",
    "business-outcome-memo.md",
    "source-register.md",
    "editorial-brief.md",
    "article-draft.md",
    "linkedin-post.md",
    "x-thread.md",
    "newsletter-blurb.md",
    "deliverables-metadata.json",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"expected object: {path}")
    return payload


def check_required(kind: str, path: Path, payload: dict[str, Any]) -> list[str]:
    errors = []
    for field in REQUIRED_FIELDS[kind]:
        if field not in payload:
            errors.append(f"{path}: missing {field}")
    return errors


def validate_root(root: Path, date: str) -> list[str]:
    errors: list[str] = []
    checks = [
        ("source-item", root / "queue/source-items" / date, "*.json"),
        ("topic-cluster", root / "queue/topic-clusters" / date, "*.json"),
        ("research-brief", root / "queue/research-briefs" / date, "*.json"),
        ("draft-package", root / "queue/draft-packages" / date, "*.json"),
        ("run-log", root / "logs" / date, "run-log.json"),
    ]

    for kind, folder, pattern in checks:
        files = list(folder.glob(pattern))
        if not files:
            errors.append(f"{folder}: no {kind} artifacts")
            continue
        for path in files:
            try:
                payload = load_json(path)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{path}: invalid json: {exc}")
                continue
            errors.extend(check_required(kind, path, payload))
            if kind == "draft-package" and payload.get("status") != "draft":
                errors.append(f"{path}: draft package status must remain draft")
            if kind == "run-log" and payload.get("cost", {}).get("cap_exceeded") is True:
                errors.append(f"{path}: cost cap exceeded")
    deliverables_dir = root / "deliverables" / date
    for filename in REQUIRED_DELIVERABLES:
        path = deliverables_dir / filename
        if not path.exists():
            errors.append(f"{deliverables_dir}: missing deliverable {filename}")
        elif path.suffix == ".md" and not path.read_text(encoding="utf-8").strip():
            errors.append(f"{path}: empty deliverable")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", help="Runtime root, e.g. runs/hermes-content-pipeline-smoke")
    parser.add_argument("--date", required=True)
    args = parser.parse_args()

    errors = validate_root(Path(args.root), args.date)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("artifact validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
