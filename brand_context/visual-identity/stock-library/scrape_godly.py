#!/usr/bin/env python3
"""
Godly.website Design Inspiration Scraper
=========================================

Scrapes design screenshots from godly.website for visual reference.
These are NOT stock photos — they're design inspiration for layout,
typography, color, and compositional patterns.

Usage:
    # Scrape dark-themed designs
    python scrape_godly.py

    # Scrape specific category
    python scrape_godly.py --category dark

    # Limit results
    python scrape_godly.py --limit 20

Requires: requests (pip install requests) or uses urllib as fallback.

Output: ./inspiration/{category}/ with screenshots + metadata.
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# Godly uses a public API endpoint for their gallery
# These are the common filter categories
CATEGORIES = {
    "dark": "Dark themed websites",
    "minimal": "Minimal clean designs",
    "portfolio": "Portfolio websites",
    "saas": "SaaS product pages",
    "agency": "Agency websites",
    "ai": "AI/ML product pages",
    "ecommerce": "E-commerce designs",
    "3d": "3D and immersive designs",
}


def fetch_godly_page(page=1, limit=12):
    """Fetch a page of designs from godly.website's API."""
    # Godly uses a Next.js API route
    url = f"https://godly.website/api/projects?page={page}&limit={limit}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; DesignResearch/1.0)")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"  API error: {e}")
        return None


def download_screenshot(url, dest):
    """Download a screenshot image."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; DesignResearch/1.0)")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(dest, "wb") as f:
                f.write(data)
            return True
    except Exception as e:
        print(f"    FAILED: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Scrape design inspiration from godly.website")
    parser.add_argument("--category", type=str, default="dark",
                        choices=list(CATEGORIES.keys()),
                        help="Design category to scrape (default: dark)")
    parser.add_argument("--limit", type=int, default=15,
                        help="Max designs to download (default: 15)")
    parser.add_argument("--out-dir", type=str, default=None,
                        help="Output directory")
    parser.add_argument("--list-categories", action="store_true",
                        help="List categories and exit")
    args = parser.parse_args()

    if args.list_categories:
        print("Available categories:")
        for name, desc in CATEGORIES.items():
            print(f"  {name:16s} {desc}")
        return

    out_dir = Path(args.out_dir) if args.out_dir else SCRIPT_DIR / "inspiration" / args.category
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Godly.website Design Scraper")
    print(f"Category: {args.category}")
    print(f"Limit: {args.limit}")
    print(f"Output: {out_dir}")
    print("=" * 50)

    # Try fetching from their API
    print(f"\nFetching designs from godly.website...")
    result = fetch_godly_page(page=1, limit=args.limit)

    if result and isinstance(result, list):
        designs = result
    elif result and isinstance(result, dict):
        designs = result.get("projects") or result.get("data") or result.get("results") or []
    else:
        print("Could not fetch from API. Trying alternative approach...")
        # Fallback: provide curated godly.website URLs for manual browsing
        print(f"\nGodly.website may require JavaScript rendering.")
        print(f"Alternative approaches:")
        print(f"  1. Use /browse or /agent-browser to screenshot godly.website pages")
        print(f"  2. Use the Firecrawl skill: /firecrawl scrape https://godly.website")
        print(f"  3. Manually browse https://godly.website and save screenshots to {out_dir}")
        print(f"\nCurated dark-themed design URLs to explore:")

        curated_urls = [
            "https://godly.website",
            "https://www.awwwards.com/websites/dark/",
            "https://www.siteinspire.com/websites?categories=26",
            "https://muz.li/inspiration/dark-mode/",
            "https://dribbble.com/search/dark-ui-design",
        ]
        for url in curated_urls:
            print(f"  - {url}")

        # Write the URLs to a file for later reference
        with open(out_dir / "_curated_urls.md", "w") as f:
            f.write(f"# Dark Design Inspiration URLs\n\n")
            f.write(f"Curated sources for {args.category} design screenshots:\n\n")
            for url in curated_urls:
                f.write(f"- [{url}]({url})\n")
        print(f"\nSaved URL list to {out_dir / '_curated_urls.md'}")
        return

    downloaded = 0
    metadata_entries = []

    for i, design in enumerate(designs):
        if downloaded >= args.limit:
            break

        # Extract screenshot URL and metadata
        name = design.get("name") or design.get("title") or f"design-{i}"
        screenshot_url = (design.get("screenshot") or design.get("image")
                         or design.get("thumbnail") or design.get("cover"))
        site_url = design.get("url") or design.get("link") or ""
        tags = design.get("tags") or design.get("categories") or []

        if not screenshot_url:
            continue

        # Filter by category keywords if possible
        if args.category != "all":
            tag_text = " ".join(str(t) for t in tags).lower() if tags else ""
            name_lower = name.lower()
            # Loose match — include if any keyword matches
            if args.category in ("dark", "minimal", "ai", "saas"):
                # These are broad enough to include most results
                pass

        safe_name = "".join(c if c.isalnum() or c in "-_" else "-" for c in name.lower())[:50]
        filename = f"{i+1:02d}_{safe_name}.jpg"
        dest = out_dir / filename

        if dest.exists():
            downloaded += 1
            continue

        print(f"  [{i+1}/{args.limit}] {name}")
        print(f"    URL: {site_url}")

        if download_screenshot(screenshot_url, dest):
            downloaded += 1
            metadata_entries.append({
                "file": filename,
                "name": name,
                "url": site_url,
                "tags": tags,
            })

        time.sleep(0.3)

    # Save metadata
    if metadata_entries:
        with open(out_dir / "_metadata.json", "w") as f:
            json.dump(metadata_entries, f, indent=2)

        with open(out_dir / "_attribution.md", "w") as f:
            f.write(f"# Design Inspiration — {args.category}\n\n")
            f.write(f"Screenshots from godly.website for design reference only.\n")
            f.write(f"These are NOT stock photos — they are design inspiration.\n\n")
            for entry in metadata_entries:
                f.write(f"- **{entry['name']}** — [{entry['url']}]({entry['url']})\n")

    print(f"\n{'=' * 50}")
    print(f"Downloaded: {downloaded} design screenshots")
    print(f"Location: {out_dir}")


if __name__ == "__main__":
    main()
