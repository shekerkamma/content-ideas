#!/usr/bin/env python3
"""Repo-local Stage 0/1 pipeline runner for strategy-mode use cases."""

from __future__ import annotations

import argparse
import sys

from lib.strategy_pipeline import (
    format_use_case_list,
    latest_strategy_feed,
    run_stage1_pipeline,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("selector", nargs="?", help="use case number, id, or title match")
    parser.add_argument("--list", action="store_true", help="list use cases from the latest strategy feed")
    parser.add_argument("--content-root", default=None, help="override CONTENT_HOME")
    parser.add_argument("--runs-dir", default=None, help="directory for repo-local run artifacts")
    parser.add_argument("--query", default=None, help="override the gbrain semantic recall query")
    args = parser.parse_args()

    feed_path, data = latest_strategy_feed(args.content_root)
    if args.list or not args.selector:
        print(f"Latest strategy feed: {feed_path}")
        print(format_use_case_list(data["useCases"]))
        return 0

    ctx = run_stage1_pipeline(
        args.selector,
        content_root=args.content_root,
        runs_dir=args.runs_dir,
        query_text=args.query,
    )
    print(f"Run directory: {ctx.run_dir}")
    print(f"Use case: {ctx.use_case.get('title')}")
    print(f"GBrain Recall: {ctx.recall_mode}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"pipeline_runner.py: {exc}", file=sys.stderr)
        raise SystemExit(1)
