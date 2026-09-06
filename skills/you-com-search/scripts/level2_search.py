#!/usr/bin/env python3
"""Hermes-equivalent Level 2 research: You.com discovery -> Exa fresh contents."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

from search import load_env, request_json


def exa_contents(key: str, urls: list[str]) -> dict:
    request = urllib.request.Request(
        "https://api.exa.ai/contents",
        data=json.dumps({"urls": urls, "text": True, "maxAgeHours": 0}).encode(),
        headers={"x-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"Exa HTTP {exc.code}: {detail}") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--freshness")
    args = parser.parse_args()

    load_env()
    you_key = os.environ.get("YOU_API_KEY", "").strip()
    exa_key = os.environ.get("EXA_API_KEY", "").strip()
    if not you_key or not exa_key:
        print("YOU_API_KEY and EXA_API_KEY are both required", file=sys.stderr)
        return 2

    search_payload = {"query": args.query, "count": max(1, min(args.count, 5))}
    if args.freshness:
        search_payload["freshness"] = args.freshness
    try:
        discovery = request_json("https://ydc-index.io/v1/search", you_key, search_payload)
        sections = discovery.get("results", {})
        candidates = sections.get("web", []) + sections.get("news", [])
        urls = list(dict.fromkeys(item.get("url") for item in candidates if item.get("url")))[: args.count]
        if not urls:
            raise RuntimeError("You.com returned no URLs for Level 2 extraction")
        extracted = exa_contents(exa_key, urls)
        print(json.dumps({"route": "you-search -> exa-fresh-contents", "discovery": discovery, "extracted": extracted}, indent=2))
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
