#!/usr/bin/env python3
"""Export a run's feed as flat tables for a shareable dashboard.

Reads `feed-data.json` from a run directory and writes chart-ready files to
`<run-dir>/dashboard/`:

    posts.csv       one row per post (platform, creator, engagement, outlier)
    ideas.csv       one row per idea card (funnel stage, hook, source)
    use-cases.csv   one row per strategy-mode use case (only when present)
    summary.json    headline counts plus per-platform and per-funnel totals

These feed a hosted dashboard (for example the Claude desktop app's Dashboard
artifact type). The local For You page from generate_feed.py stays the place
where the user reacts to items; this export is a read-only view for sharing.

Usage:
    python3 export_dashboard.py <run-dir>
    python3 export_dashboard.py <run-dir> --feed path/to/feed-data.json --out dir
"""

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

POST_FIELDS = [
    "title", "url", "platform", "creator", "handle", "timestamp", "sortValue",
    "likes", "replies", "reposts", "views", "bookmarks", "saves",
    "zScore", "performance", "isOutlier",
]
IDEA_FIELDS = ["title", "funnel", "concept", "suggestedHook", "whyNow", "sourceUrl"]
USE_CASE_FIELDS = ["id", "title", "kicker", "verticalName", "users", "signalCount"]


def _is_outlier(post):
    return post.get("zScore") is not None or post.get("performanceDirection") == "up"


def post_rows(feed):
    rows = []
    for post in feed.get("posts") or []:
        eng = post.get("engagement") or {}
        rows.append({
            "title": post.get("title"),
            "url": post.get("url"),
            "platform": post.get("platform"),
            "creator": post.get("displayName") or post.get("handle"),
            "handle": post.get("handle"),
            "timestamp": post.get("timestamp"),
            "sortValue": post.get("sortValue"),
            "likes": eng.get("likes"),
            "replies": eng.get("replies"),
            "reposts": eng.get("reposts"),
            "views": eng.get("views"),
            "bookmarks": eng.get("bookmarks"),
            "saves": eng.get("saves"),
            "zScore": post.get("zScore"),
            "performance": post.get("performance"),
            "isOutlier": _is_outlier(post),
        })
    return rows


def idea_rows(feed):
    rows = []
    for idea in (feed.get("ideas") or {}).get("items") or []:
        brief = idea.get("brief") or {}
        rows.append({
            "title": idea.get("title"),
            "funnel": idea.get("funnel"),
            "concept": idea.get("concept"),
            "suggestedHook": brief.get("suggestedHook"),
            "whyNow": brief.get("whyNow"),
            "sourceUrl": idea.get("sourceUrl"),
        })
    return rows


def use_case_rows(feed):
    return [{
        "id": uc.get("id"),
        "title": uc.get("title"),
        "kicker": uc.get("kicker"),
        "verticalName": uc.get("verticalName"),
        "users": uc.get("users"),
        "signalCount": len(uc.get("signals") or []),
    } for uc in feed.get("useCases") or []]


def summary(feed, posts, ideas, use_cases):
    return {
        "date": (feed.get("meta") or {}).get("date"),
        "posts": len(posts),
        "outliers": sum(1 for p in posts if p["isOutlier"]),
        "ideas": len(ideas),
        "useCases": len(use_cases),
        "postsByPlatform": dict(Counter(p["platform"] or "unknown" for p in posts)),
        "ideasByFunnel": dict(Counter(i["funnel"] or "unknown" for i in ideas)),
        "patterns": list((feed.get("ideas") or {}).get("patterns") or []),
    }


def _write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: "" if row.get(k) is None else row.get(k) for k in fields})


def export(feed, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    posts, ideas, use_cases = post_rows(feed), idea_rows(feed), use_case_rows(feed)
    written = [out_dir / "posts.csv", out_dir / "ideas.csv"]
    _write_csv(written[0], POST_FIELDS, posts)
    _write_csv(written[1], IDEA_FIELDS, ideas)
    stale = out_dir / "use-cases.csv"
    if use_cases:
        _write_csv(stale, USE_CASE_FIELDS, use_cases)
        written.append(stale)
    elif stale.exists():
        stale.unlink()
    summary_path = out_dir / "summary.json"
    summary_path.write_text(
        json.dumps(summary(feed, posts, ideas, use_cases), indent=2) + "\n",
        encoding="utf-8",
    )
    written.append(summary_path)
    return written


def main(argv=None):
    parser = argparse.ArgumentParser(description="Export feed-data.json as dashboard tables")
    parser.add_argument("run_dir", help="Run directory (contains feed-data.json)")
    parser.add_argument("--feed", help="Path to feed-data.json (default: <run-dir>/feed-data.json)")
    parser.add_argument("--out", help="Output directory (default: <run-dir>/dashboard)")
    args = parser.parse_args(argv)

    run_dir = Path(args.run_dir).expanduser()
    feed_path = Path(args.feed).expanduser() if args.feed else run_dir / "feed-data.json"
    if not feed_path.is_file():
        print(f"error: {feed_path} not found", file=sys.stderr)
        return 1
    try:
        feed = json.loads(feed_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"error: {feed_path} is not valid JSON: {exc}", file=sys.stderr)
        return 1

    out_dir = Path(args.out).expanduser() if args.out else run_dir / "dashboard"
    for path in export(feed, out_dir):
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
