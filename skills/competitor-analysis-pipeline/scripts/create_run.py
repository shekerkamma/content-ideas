#!/usr/bin/env python3
"""Create a standard competitor-analysis run folder."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "target"


def write_if_missing(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a competitor-analysis run folder.")
    parser.add_argument("target", help="Target company, product, or category.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Run date, YYYY-MM-DD.")
    parser.add_argument("--root", default="runs", help="Root folder for runs.")
    parser.add_argument("--slug", help="Override generated slug.")
    parser.add_argument("--force", action="store_true", help="Overwrite scaffold README/status files.")
    args = parser.parse_args()

    slug = args.slug or slugify(args.target)
    run_dir = Path(args.root) / f"{args.date}-{slug}-competitor-analysis"
    dirs = [
        "inputs",
        "outputs",
        "client-package",
        "client-package/site",
        "client-package/qa",
        "client-package/qa/officecli",
        "client-package/qa/html",
    ]
    for rel in dirs:
        (run_dir / rel).mkdir(parents=True, exist_ok=True)

    status = {
        "target": args.target,
        "slug": slug,
        "status": "draft",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "pipeline": "competitor-analysis-pipeline",
        "deliverables": {
            "brief": "outputs/competitor-brief.md",
            "company_table": "outputs/company-table.csv",
            "story_review": "outputs/story-structure-review.md",
            "story_pack": "outputs/story-architect-pack.md",
            "pptx": None,
            "html": "client-package/site/index.html",
            "published_url": None,
        },
        "qa": {
            "gbrain_recall": "pending",
            "research_source_order": "pending",
            "grill_me": "pending",
            "story_architect": "pending",
            "gstack_review": "optional",
            "pptx_qa": "pending",
            "html_qa": "pending",
            "publish_verification": "pending",
        },
    }
    write_if_missing(run_dir / "status.json", json.dumps(status, indent=2) + "\n", args.force)
    write_if_missing(
        run_dir / "README.md",
        f"""# {args.target} Competitor Analysis

Status: draft

## Pipeline

- Skill: `competitor-analysis-pipeline`
- Run folder: `{run_dir}`
- Target: {args.target}

## Required Gates

- [ ] GBrain/durable memory recall attempted
- [ ] Specialist research used before generic web search
- [ ] Competitor arenas and shared rubric defined
- [ ] `grill-me` structure/content review completed
- [ ] `story-architect` pack completed
- [ ] Branded PPTX built and QA-passed, if requested
- [ ] Self-contained HTML built and navigation QA-passed, if requested
- [ ] Published URL verified, if requested
""",
        args.force,
    )
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
