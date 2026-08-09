#!/usr/bin/env python3
"""No-network regression check for You.com livecrawl parameter naming."""

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
        level="2",
        mode="search",
        limit=10,
        livecrawl=False,
        freshness=None,
        from_date=None,
        to_date=None,
        site=[],
        exclude_site=[],
    )
    params = dict(search._build_params(args))
    assert params.get("live_crawl") == "true", params
    assert "livecrawl" not in params, params
    assert "liveCrawl" not in params, params
    print("OK: Level 2 sends live_crawl=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
