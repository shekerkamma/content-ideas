#!/usr/bin/env python3
"""You.com Level 2 research: search discovery plus full-page extraction."""

import argparse
import json
import os
import sys
from search import build_payload, load_env, request_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--freshness")
    parser.add_argument("--crawl-timeout", type=int, default=30, choices=range(1, 61), metavar="1-60")
    args = parser.parse_args()

    load_env()
    you_key = (os.environ.get("YOU_API_KEY") or os.environ.get("YDC_API_KEY") or "").strip()
    if not you_key:
        print("YOU_API_KEY or YDC_API_KEY is required", file=sys.stderr)
        return 2

    args.livecrawl = True
    args.site = []
    args.exclude_site = []
    search_payload = build_payload(args)
    try:
        discovery = request_json("https://ydc-index.io/v1/search", you_key, search_payload)
        sections = discovery.get("results", {})
        candidates = sections.get("web", []) + sections.get("news", [])
        full_pages = sum(
            bool((item.get("contents") or {}).get("markdown")) for item in candidates
        )
        if not candidates or not full_pages:
            raise RuntimeError("You.com returned no full-page Markdown for Level 2 extraction")
        print(
            json.dumps(
                {
                    "route": "you-search-post-full-page",
                    "backend": "https://ydc-index.io/v1/search",
                    "status": "success",
                    "result_count": len(candidates),
                    "full_page_markdown_count": full_pages,
                    "discovery": discovery,
                },
                indent=2,
            )
        )
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
