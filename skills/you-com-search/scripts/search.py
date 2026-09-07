#!/usr/bin/env python3
"""You.com Search API wrapper for Claude Code CLI on WSL."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ENV_FILES = (
    Path("/mnt/c/Users/sheke/AppData/Local/hermes/.env"),
    Path.home() / ".hermes" / ".env",
)


def load_env() -> None:
    for path in ENV_FILES:
        if not path.is_file():
            continue
        for raw in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip().removeprefix("export ").strip(), value.strip().strip('"\''))


def request_json(url: str, key: str, payload: dict) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"X-API-Key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"You.com HTTP {exc.code}: {detail}") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--livecrawl", action="store_true")
    parser.add_argument("--freshness")
    parser.add_argument("--site", action="append", default=[])
    parser.add_argument("--exclude-site", action="append", default=[])
    args = parser.parse_args()

    load_env()
    key = os.environ.get("YOU_API_KEY", "").strip()
    if not key:
        print("YOU_API_KEY is not configured", file=sys.stderr)
        return 2

    payload = {"query": args.query, "count": max(1, min(args.count, 100))}
    if args.livecrawl:
        payload.update({"livecrawl": "all", "livecrawl_formats": ["markdown"]})
    if args.freshness:
        payload["freshness"] = args.freshness
    if args.site:
        payload["include_domains"] = args.site
    if args.exclude_site:
        payload["exclude_domains"] = args.exclude_site

    try:
        print(json.dumps(request_json("https://ydc-index.io/v1/search", key, payload), indent=2))
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
