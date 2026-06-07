#!/usr/bin/env python3
"""
Stock Image Downloader for Carousel Backgrounds
================================================

Downloads themed stock images from Pexels (free API) and organizes them
into folders by theme. Images are sized for LinkedIn carousels (1080x1350).

Usage:
    # Download all themes (default 10 images each)
    python download_stock.py

    # Download specific theme
    python download_stock.py --theme dark-tech

    # Download more images per theme
    python download_stock.py --per-theme 20

    # List available themes
    python download_stock.py --list-themes

    # Add a custom search query to an existing or new theme
    python download_stock.py --theme custom --query "neon lights dark background"

    # Download from Unsplash instead (needs UNSPLASH_ACCESS_KEY)
    python download_stock.py --source unsplash

Setup:
    1. Get a free Pexels API key: https://www.pexels.com/api/
    2. Add to ~/.config/content/.env:  PEXELS_API_KEY=your_key_here
    3. Run this script.

Sources pull from tokens.json palette to prefer images matching brand colors.
"""

import argparse
import json
import os
import sys
import time
import hashlib
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

# ── Config ───────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
TOKENS_PATH = SCRIPT_DIR.parent / "tokens.json"
ENV_PATHS = [
    Path.home() / ".config" / "content" / ".env",
    Path.home() / ".env",
    Path.cwd() / ".env",
]

# ── Theme catalog ────────────────────────────────────────────
# Each theme maps to Pexels search queries optimized for carousel backgrounds.
# Multiple queries per theme = more variety.
THEMES = {
    "dark-tech": {
        "description": "Dark technology backgrounds — circuits, code, networks",
        "queries": [
            "dark technology background abstract",
            "circuit board close up dark",
            "dark server room lights",
            "coding screen dark background",
            "network connections dark abstract",
            "dark blue technology abstract",
        ],
    },
    "abstract-geometry": {
        "description": "Geometric patterns, shapes, minimalist abstracts",
        "queries": [
            "abstract geometric dark background",
            "geometric shapes minimal dark",
            "dark abstract lines pattern",
            "dark polygon background",
            "dark triangle abstract pattern",
        ],
    },
    "gradients": {
        "description": "Smooth dark gradients, color transitions",
        "queries": [
            "dark gradient background blue",
            "dark gradient abstract",
            "blue purple gradient dark",
            "dark cyan gradient background",
            "dark smooth gradient wallpaper",
        ],
    },
    "textures": {
        "description": "Dark surfaces, materials, grain, concrete, metal",
        "queries": [
            "dark texture background",
            "black concrete texture",
            "dark metal texture surface",
            "dark paper texture grain",
            "dark fabric texture closeup",
            "dark marble texture",
        ],
    },
    "minimal-dark": {
        "description": "Clean, minimal dark backgrounds with subtle elements",
        "queries": [
            "minimal dark background",
            "dark minimal abstract",
            "simple dark wallpaper",
            "dark desk minimal workspace",
            "dark background single object",
        ],
    },
    "code-terminal": {
        "description": "Code editors, terminals, programming screens",
        "queries": [
            "programming code screen dark",
            "code editor dark theme",
            "terminal command line dark",
            "developer screen dark background",
            "software code dark monitor",
        ],
    },
    "neon-glow": {
        "description": "Neon lights, glowing elements on dark backgrounds",
        "queries": [
            "neon lights dark background",
            "neon glow abstract dark",
            "cyan neon light dark",
            "neon lines dark abstract",
            "glowing light dark background",
        ],
    },
    "data-visualization": {
        "description": "Charts, dashboards, data displays on dark screens",
        "queries": [
            "data visualization dark screen",
            "dark dashboard analytics",
            "chart graph dark background",
            "digital data dark abstract",
            "statistics display dark monitor",
        ],
    },
    "nature-dark": {
        "description": "Dark moody nature — fog, night, deep water, forests",
        "queries": [
            "dark moody nature",
            "foggy forest dark",
            "dark ocean waves",
            "night sky stars dark",
            "dark mountain landscape moody",
        ],
    },
    "office-workspace": {
        "description": "Professional dark workspaces, desks, setups",
        "queries": [
            "dark office desk setup",
            "modern workspace dark",
            "laptop dark desk workspace",
            "professional office dark lighting",
            "dark home office setup",
        ],
    },
}


# ── Helpers ──────────────────────────────────────────────────
def load_env():
    """Load API keys from .env files."""
    keys = {}
    for env_path in ENV_PATHS:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        keys[k.strip()] = v.strip().strip('"').strip("'")
    return keys


def download_file(url, dest, headers=None):
    """Download a file with progress indication."""
    req = urllib.request.Request(url)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(dest, "wb") as f:
                f.write(data)
            return True
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
        print(f"    FAILED: {e}")
        return False


def search_pexels(query, api_key, per_page=10, orientation="portrait", page=1):
    """Search Pexels API and return photo results."""
    params = urllib.parse.urlencode({
        "query": query,
        "per_page": per_page,
        "orientation": orientation,
        "page": page,
        "size": "large",
    })
    url = f"https://api.pexels.com/v1/search?{params}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", api_key)

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"    API error: {e}")
        return None


def search_unsplash(query, access_key, per_page=10, orientation="portrait", page=1):
    """Search Unsplash API and return photo results."""
    params = urllib.parse.urlencode({
        "query": query,
        "per_page": per_page,
        "orientation": orientation,
        "page": page,
    })
    url = f"https://api.unsplash.com/search/photos?{params}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Client-ID {access_key}")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"    API error: {e}")
        return None


def download_theme_pexels(theme_name, theme_config, out_dir, api_key,
                          per_theme=10, existing_ids=None):
    """Download images for a theme from Pexels."""
    if existing_ids is None:
        existing_ids = set()

    theme_dir = out_dir / theme_name
    theme_dir.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    queries = theme_config["queries"]
    imgs_per_query = max(2, per_theme // len(queries))

    for query in queries:
        if downloaded >= per_theme:
            break

        print(f"  Searching: \"{query}\"")
        result = search_pexels(query, api_key, per_page=imgs_per_query)
        if not result or "photos" not in result:
            continue

        for photo in result["photos"]:
            if downloaded >= per_theme:
                break

            photo_id = str(photo["id"])
            if photo_id in existing_ids:
                continue

            # Use portrait size (closest to 1080x1350)
            img_url = photo["src"].get("portrait") or photo["src"].get("large")
            if not img_url:
                continue

            photographer = photo.get("photographer", "unknown").replace(" ", "-").lower()
            filename = f"{theme_name}_{photo_id}_{photographer}.jpg"
            dest = theme_dir / filename

            if dest.exists():
                existing_ids.add(photo_id)
                downloaded += 1
                continue

            print(f"    Downloading: {filename}")
            if download_file(img_url, dest):
                existing_ids.add(photo_id)
                downloaded += 1

                # Write attribution
                attr_file = theme_dir / "_attribution.md"
                with open(attr_file, "a") as f:
                    f.write(f"- [{photographer}]({photo.get('photographer_url', '')}) "
                            f"via [Pexels]({photo.get('url', '')})\n")

            # Rate limit: 200 req/hr = ~3 req/sec is safe
            time.sleep(0.5)

    print(f"  {theme_name}: {downloaded} images downloaded → {theme_dir}")
    return downloaded


def download_theme_unsplash(theme_name, theme_config, out_dir, access_key,
                            per_theme=10, existing_ids=None):
    """Download images for a theme from Unsplash."""
    if existing_ids is None:
        existing_ids = set()

    theme_dir = out_dir / theme_name
    theme_dir.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    queries = theme_config["queries"]
    imgs_per_query = max(2, per_theme // len(queries))

    for query in queries:
        if downloaded >= per_theme:
            break

        print(f"  Searching: \"{query}\"")
        result = search_unsplash(query, access_key, per_page=imgs_per_query)
        if not result or "results" not in result:
            continue

        for photo in result["results"]:
            if downloaded >= per_theme:
                break

            photo_id = photo["id"]
            if photo_id in existing_ids:
                continue

            # Use regular size
            img_url = photo["urls"].get("regular") or photo["urls"].get("full")
            if not img_url:
                continue

            user = photo.get("user", {}).get("username", "unknown")
            filename = f"{theme_name}_{photo_id}_{user}.jpg"
            dest = theme_dir / filename

            if dest.exists():
                existing_ids.add(photo_id)
                downloaded += 1
                continue

            print(f"    Downloading: {filename}")
            if download_file(img_url, dest):
                existing_ids.add(photo_id)
                downloaded += 1

                # Trigger download tracking (Unsplash requirement)
                dl_url = photo.get("links", {}).get("download_location")
                if dl_url:
                    try:
                        req = urllib.request.Request(dl_url)
                        req.add_header("Authorization", f"Client-ID {access_key}")
                        urllib.request.urlopen(req, timeout=5)
                    except Exception:
                        pass

                attr_file = theme_dir / "_attribution.md"
                with open(attr_file, "a") as f:
                    f.write(f"- [{user}](https://unsplash.com/@{user}) "
                            f"via [Unsplash](https://unsplash.com/photos/{photo_id})\n")

            time.sleep(0.5)

    print(f"  {theme_name}: {downloaded} images downloaded → {theme_dir}")
    return downloaded


# ── Main ─────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Download themed stock images for carousel backgrounds")
    parser.add_argument("--theme", type=str, default=None,
                        help="Download a specific theme (default: all)")
    parser.add_argument("--per-theme", type=int, default=10,
                        help="Images per theme (default: 10)")
    parser.add_argument("--list-themes", action="store_true",
                        help="List available themes and exit")
    parser.add_argument("--query", type=str, default=None,
                        help="Custom search query (use with --theme custom)")
    parser.add_argument("--source", type=str, default="pexels",
                        choices=["pexels", "unsplash"],
                        help="Image source (default: pexels)")
    parser.add_argument("--out-dir", type=str, default=None,
                        help="Output directory (default: ./themes/)")
    args = parser.parse_args()

    # List themes
    if args.list_themes:
        print("Available themes:")
        print("=" * 50)
        for name, config in sorted(THEMES.items()):
            print(f"  {name:24s} {config['description']}")
        print(f"\n  Total: {len(THEMES)} themes")
        print(f"\n  Usage: python {Path(__file__).name} --theme dark-tech --per-theme 15")
        return

    # Load API keys
    env = load_env()

    if args.source == "pexels":
        api_key = env.get("PEXELS_API_KEY") or os.environ.get("PEXELS_API_KEY")
        if not api_key:
            print("ERROR: PEXELS_API_KEY not found.")
            print()
            print("Get a free key in 30 seconds:")
            print("  1. Go to https://www.pexels.com/api/")
            print("  2. Create account → Request API Access")
            print("  3. Copy your key")
            print(f"  4. Add to {ENV_PATHS[0]}:")
            print(f'     PEXELS_API_KEY=your_key_here')
            print()
            print("Or pass directly: PEXELS_API_KEY=xxx python download_stock.py")
            sys.exit(1)
    elif args.source == "unsplash":
        api_key = env.get("UNSPLASH_ACCESS_KEY") or os.environ.get("UNSPLASH_ACCESS_KEY")
        if not api_key:
            print("ERROR: UNSPLASH_ACCESS_KEY not found.")
            print()
            print("Get a free key:")
            print("  1. Go to https://unsplash.com/developers")
            print("  2. Create app → Copy Access Key")
            print(f"  3. Add to {ENV_PATHS[0]}:")
            print(f'     UNSPLASH_ACCESS_KEY=your_key_here')
            sys.exit(1)

    # Output directory
    out_dir = Path(args.out_dir) if args.out_dir else SCRIPT_DIR / "themes"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Handle custom query
    if args.query:
        theme_name = args.theme or "custom"
        if theme_name not in THEMES:
            THEMES[theme_name] = {
                "description": f"Custom: {args.query}",
                "queries": [args.query],
            }
        else:
            THEMES[theme_name]["queries"].append(args.query)

    # Determine which themes to download
    if args.theme:
        if args.theme not in THEMES:
            print(f"ERROR: Unknown theme '{args.theme}'")
            print(f"Run with --list-themes to see available themes")
            sys.exit(1)
        themes_to_download = {args.theme: THEMES[args.theme]}
    else:
        themes_to_download = THEMES

    # Download
    print(f"Stock Image Downloader")
    print(f"Source: {args.source.upper()}")
    print(f"Themes: {len(themes_to_download)}")
    print(f"Per theme: {args.per_theme}")
    print(f"Output: {out_dir}")
    print("=" * 50)

    total = 0
    existing_ids = set()

    # Scan existing files to avoid re-downloading
    for theme_dir in out_dir.iterdir():
        if theme_dir.is_dir():
            for f in theme_dir.glob("*.jpg"):
                parts = f.stem.split("_")
                if len(parts) >= 2:
                    existing_ids.add(parts[1])

    for name, config in themes_to_download.items():
        print(f"\n[{name}] {config['description']}")
        if args.source == "pexels":
            count = download_theme_pexels(name, config, out_dir, api_key,
                                          args.per_theme, existing_ids)
        else:
            count = download_theme_unsplash(name, config, out_dir, api_key,
                                            args.per_theme, existing_ids)
        total += count

    print(f"\n{'=' * 50}")
    print(f"Total downloaded: {total} images")
    print(f"Library: {out_dir}")
    print(f"\nAttribution files in each theme folder (_attribution.md)")
    print(f"All images are free to use under Pexels/Unsplash license.")


if __name__ == "__main__":
    main()
