#!/usr/bin/env python3
"""Small CLI wrapper for You.com Search/Research APIs."""

from __future__ import annotations

import argparse
import gzip
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


BASE_URL = os.getenv("YOU_BASE_URL", "https://ydc-index.io").rstrip("/")


def _load_hermes_env_key() -> str:
    env_path = Path.home() / ".hermes" / ".env"
    if not env_path.exists():
        return ""
    for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("YOU_API_KEY="):
            continue
        return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def _api_key() -> str:
    return os.getenv("YOU_API_KEY", "").strip() or _load_hermes_env_key()


def _endpoint(mode: str) -> str:
    if mode == "search":
        return f"{BASE_URL}/v1/search"
    if mode == "research":
        return f"{BASE_URL}/v1/research"
    if mode == "finance":
        return f"{BASE_URL}/v1/finance/research"
    raise ValueError(f"unsupported mode: {mode}")


def _build_params(args: argparse.Namespace) -> dict[str, str]:
    params = {"query": args.query}
    if args.mode == "search":
        params["num_web_results"] = str(args.limit)
        if args.livecrawl:
            params["livecrawl"] = "true"
    if args.freshness:
        params["freshness"] = args.freshness
    if args.from_date:
        params["from_date"] = args.from_date
    if args.to_date:
        params["to_date"] = args.to_date
    for site in args.site:
        params.setdefault("site", site)
    for site in args.exclude_site:
        params.setdefault("exclude_site", site)
    return params


def request_json(args: argparse.Namespace) -> dict:
    key = _api_key()
    if not key:
        raise SystemExit("YOU_API_KEY is not set")

    url = f"{_endpoint(args.mode)}?{urllib.parse.urlencode(_build_params(args))}"
    req = urllib.request.Request(
        url, headers={"X-API-Key": key, "Accept-Encoding": "identity"}
    )
    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as response:
            body = response.read()
            if response.headers.get("Content-Encoding", "").lower() == "gzip":
                body = gzip.decompress(body)
            return json.loads(body.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"You.com API error {exc.code}: {body}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="You.com Search API wrapper")
    parser.add_argument("query", help="Query or research question")
    parser.add_argument(
        "--mode",
        choices=["search", "research", "finance"],
        default="search",
        help="API mode to use",
    )
    parser.add_argument("--limit", type=int, default=10, help="Search result count")
    parser.add_argument("--livecrawl", action="store_true", help="Request livecrawl")
    parser.add_argument("--freshness", help="Freshness filter, e.g. day/week/month")
    parser.add_argument("--from-date", help="Start date, YYYY-MM-DD")
    parser.add_argument("--to-date", help="End date, YYYY-MM-DD")
    parser.add_argument("--site", action="append", default=[], help="Domain include")
    parser.add_argument(
        "--exclude-site", action="append", default=[], help="Domain exclude"
    )
    parser.add_argument("--timeout", type=int, default=60, help="HTTP timeout seconds")
    args = parser.parse_args()

    result = request_json(args)
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
