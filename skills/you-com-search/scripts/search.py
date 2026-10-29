#!/usr/bin/env python3
"""You.com Search API wrapper for Claude Code, Codex, and Hermes on WSL."""

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


MANAGED_KEYS = {"YOU_API_KEY", "YDC_API_KEY", "EXA_API_KEY"}


def load_env() -> None:
    """Load active host credentials before inherited/stale shell values.

    The Windows Hermes file is the active cross-host credential source on this
    WSL machine.  Only managed research keys are overridden; unrelated process
    environment variables are left untouched.
    """
    loaded: set[str] = set()
    for path in ENV_FILES:
        if not path.is_file():
            continue
        for raw in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip().removeprefix("export ").strip()
            if key in MANAGED_KEYS and key not in loaded:
                os.environ[key] = value.strip().strip('"\'')
                loaded.add(key)


def build_payload(args: argparse.Namespace) -> dict:
    payload = {"query": args.query, "count": max(1, min(args.count, 100))}
    if args.livecrawl:
        payload.update(
            {
                "extraction": {
                    "extraction_mode": "full_page",
                    "full_page": {"extraction_formats": ["markdown"]},
                },
                "crawl_timeout": args.crawl_timeout,
            }
        )
    if args.freshness:
        payload["freshness"] = args.freshness
    if args.site:
        payload["include_domains"] = args.site
    if args.exclude_site:
        payload["exclude_domains"] = args.exclude_site
    return payload


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
    parser.add_argument("--crawl-timeout", type=int, default=30, choices=range(1, 61), metavar="1-60")
    parser.add_argument("--freshness")
    parser.add_argument("--site", action="append", default=[])
    parser.add_argument("--exclude-site", action="append", default=[])
    args = parser.parse_args()

    load_env()
    key = (os.environ.get("YOU_API_KEY") or os.environ.get("YDC_API_KEY") or "").strip()
    if not key:
        print("YOU_API_KEY is not configured", file=sys.stderr)
        return 2

    payload = build_payload(args)

    try:
        print(json.dumps(request_json("https://ydc-index.io/v1/search", key, payload), indent=2))
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
