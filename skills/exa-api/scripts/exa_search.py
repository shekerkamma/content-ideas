#!/usr/bin/env python3
"""Exa semantic search wrapper for Claude Code CLI on WSL."""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def load_env() -> None:
    for path in (Path("/mnt/c/Users/sheke/AppData/Local/hermes/.env"), Path.home() / ".hermes" / ".env"):
        if not path.is_file():
            continue
        for raw in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip().removeprefix("export ").strip(), value.strip().strip('"\''))


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: exa_search.py QUERY [NUM_RESULTS]", file=sys.stderr)
        return 2
    load_env()
    key = os.environ.get("EXA_API_KEY", "").strip()
    if not key:
        print("EXA_API_KEY is not configured", file=sys.stderr)
        return 2
    payload = {"query": sys.argv[1], "numResults": int(sys.argv[2]) if len(sys.argv) > 2 else 10, "contents": {"highlights": True}}
    request = urllib.request.Request(
        "https://api.exa.ai/search",
        data=json.dumps(payload).encode(),
        headers={"x-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            print(json.dumps(json.load(response), indent=2))
        return 0
    except urllib.error.HTTPError as exc:
        print(f"Exa HTTP {exc.code}: {exc.read().decode(errors='replace')}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
