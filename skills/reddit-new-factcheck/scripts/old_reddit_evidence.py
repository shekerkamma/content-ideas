#!/usr/bin/env python3
"""Collect Reddit evidence from old.reddit.com HTML.

This is a fallback for environments where Reddit's JSON endpoints return 403
but old.reddit HTML is reachable. It writes the same normalized JSON shape used
by prepare_factcheck.py: {"post": ..., "comments": [...]}.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 factcheck-research"


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def fetch_text(url: str, timeout: int = 25) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", "replace")


def old_url(url: str) -> str:
    if url.startswith("/"):
        url = "https://old.reddit.com" + url
    url = html.unescape(url)
    url = url.replace("https://www.reddit.com", "https://old.reddit.com")
    url = url.replace("https://reddit.com", "https://old.reddit.com")
    return url.split("?")[0]


def score_value(text: str) -> int:
    text = text.replace(",", "")
    match = re.search(r"(-?\d+)", text)
    return int(match.group(1)) if match else 0


def reddit_search(query: str, limit: int) -> list[dict[str, str]]:
    params = urllib.parse.urlencode({"q": query, "sort": "relevance", "t": "year"})
    url = f"https://old.reddit.com/search?{params}"
    soup = BeautifulSoup(fetch_text(url), "lxml")
    results: list[dict[str, str]] = []
    for link in soup.select("a.search-title"):
        href = old_url(link.get("href", ""))
        if "/comments/" not in href:
            continue
        title = compact(link.get_text(" "))
        results.append({"title": title, "url": href, "query": query})
        if len(results) >= limit:
            break
    return results


def text_from_md(node) -> str:
    if node is None:
        return ""
    return compact(node.get_text(" "))


def parse_comment_permalink(thing, base_url: str) -> str:
    for selector in ["a.bylink", "a[data-event-action='permalink']"]:
        link = thing.select_one(selector)
        if link and link.get("href"):
            return old_url(link["href"])
    comment_id = thing.get("data-fullname", "")
    return f"{base_url.rstrip('/')}/?context=3#{comment_id}" if comment_id else base_url


def parse_thread(url: str, max_comments: int) -> dict[str, Any]:
    soup = BeautifulSoup(fetch_text(url), "lxml")
    link = soup.select_one("div.thing.link")
    post_title = compact(link.select_one("a.title").get_text(" ")) if link and link.select_one("a.title") else ""
    post_author = compact(link.select_one("a.author").get_text(" ")) if link and link.select_one("a.author") else ""
    post_score = score_value(link.select_one("div.score.unvoted").get_text(" ")) if link and link.select_one("div.score.unvoted") else 0
    post_body = text_from_md(link.select_one("div.usertext-body div.md") if link else None)
    subreddit = ""
    if link:
        subreddit = link.get("data-subreddit") or ""
    comments = []
    for thing in soup.select("div.thing.comment"):
        body = text_from_md(thing.select_one("div.usertext-body div.md"))
        if not body or body in {"[deleted]", "[removed]"}:
            continue
        author_node = thing.select_one("a.author")
        score_node = thing.select_one("span.score.unvoted")
        comments.append(
            {
                "id": thing.get("data-fullname", ""),
                "author": compact(author_node.get_text(" ")) if author_node else "",
                "text": body,
                "score": score_value(score_node.get_text(" ")) if score_node else 0,
                "depth": score_value(" ".join(thing.get("class", []))),
                "permalink": parse_comment_permalink(thing, url),
                "source_url": url,
                "subreddit": subreddit,
            }
        )
        if len(comments) >= max_comments:
            break
    return {
        "post": {
            "title": post_title,
            "author": post_author,
            "score": post_score,
            "content": post_body,
            "url": url,
            "permalink": url,
            "subreddit": subreddit,
        },
        "comments": comments,
        "source": {"url": url, "method": "old_reddit_html"},
    }


def load_queries(claim_pack: Path, max_queries: int, extra_queries: list[str]) -> list[str]:
    claims = json.loads(claim_pack.read_text(encoding="utf-8")).get("claims", [])
    queries = [q for q in extra_queries if q.strip()]
    for claim in claims:
        if claim.get("evidence_need") == "primary_required":
            continue
        query = claim.get("reddit_query", "")
        if query:
            queries.append(query)
        if len(queries) >= max_queries:
            break
    seen: set[str] = set()
    output = []
    for query in queries:
        norm = compact(query.lower())
        if norm and norm not in seen:
            output.append(query)
            seen.add(norm)
    return output[:max_queries]


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claim-pack", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--max-queries", type=int, default=8)
    parser.add_argument("--results-per-query", type=int, default=4)
    parser.add_argument("--max-threads", type=int, default=10)
    parser.add_argument("--max-comments", type=int, default=80)
    parser.add_argument("--sleep", type=float, default=0.75)
    parser.add_argument("--query", action="append", default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    queries = load_queries(args.claim_pack, args.max_queries, args.query)
    discovered: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    for query in queries:
        for result in reddit_search(query, args.results_per_query):
            if result["url"] in seen_urls:
                continue
            discovered.append(result)
            seen_urls.add(result["url"])
            if len(discovered) >= args.max_threads:
                break
        if len(discovered) >= args.max_threads:
            break
        time.sleep(args.sleep)

    threads = []
    for index, result in enumerate(discovered, 1):
        try:
            data = parse_thread(result["url"], args.max_comments)
            out = args.out_dir / f"reddit-thread-{index:02d}.json"
            write_json(out, data)
            threads.append(
                {
                    **result,
                    "output": str(out),
                    "comments": len(data.get("comments", [])),
                    "post_title": data.get("post", {}).get("title", ""),
                    "subreddit": data.get("post", {}).get("subreddit", ""),
                }
            )
        except Exception as exc:  # noqa: BLE001 - record and keep collecting
            threads.append({**result, "error": f"{type(exc).__name__}: {exc}"})
        time.sleep(args.sleep)

    manifest = {
        "method": "old_reddit_html",
        "queries": queries,
        "threads": threads,
        "thread_count": len([item for item in threads if item.get("output")]),
    }
    write_json(args.out_dir / "reddit-discovery-manifest.json", manifest)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
