#!/usr/bin/env python3
"""No-network regression check for You.com full-page extraction mapping."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


def _load_search_module():
    script = Path(__file__).with_name("search.py")
    spec = importlib.util.spec_from_file_location("you_com_search", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    search = _load_search_module()
    args = argparse.Namespace(
        query="test query",
        count=10,
        livecrawl=True,
        crawl_timeout=30,
        freshness=None,
        site=[],
        exclude_site=[],
    )
    payload = search.build_payload(args)
    extraction = payload.get("extraction", {})
    assert extraction.get("extraction_mode") == "full_page", payload
    assert extraction.get("full_page", {}).get("extraction_formats") == ["markdown"], payload
    assert payload.get("crawl_timeout") == 30, payload
    print("OK: --livecrawl maps to POST full_page Markdown extraction")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
