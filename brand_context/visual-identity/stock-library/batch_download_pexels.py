#!/usr/bin/env python3
"""
Batch download Pexels stock images for carousel backgrounds.
URLs scraped from Pexels search pages — free to use under Pexels license.
Downloads at portrait size (1080x1350) for LinkedIn carousels.
"""

import os
import re
import time
import json
import urllib.request
import urllib.error
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
OUT_DIR = SCRIPT_DIR / "themes"

# Pexels direct image URLs — scraped from search results
# All images are free under Pexels license (no API key needed for direct URLs)
THEMES = {
    "dark-tech": {
        "description": "Dark technology backgrounds — circuits, servers, networks",
        "urls": [
            "https://images.pexels.com/photos/13027585/pexels-photo-13027585.jpeg",
            "https://images.pexels.com/photos/12707786/pexels-photo-12707786.jpeg",
            "https://images.pexels.com/photos/7562087/pexels-photo-7562087.jpeg",
            "https://images.pexels.com/photos/8118270/pexels-photo-8118270.jpeg",
            "https://images.pexels.com/photos/10653941/pexels-photo-10653941.jpeg",
            "https://images.pexels.com/photos/3520679/pexels-photo-3520679.jpeg",
            "https://images.pexels.com/photos/8108716/pexels-photo-8108716.jpeg",
            "https://images.pexels.com/photos/13156181/pexels-photo-13156181.jpeg",
            "https://images.pexels.com/photos/18337643/pexels-photo-18337643.jpeg",
            "https://images.pexels.com/photos/234527/pexels-photo-234527.jpeg",
        ],
    },
    "gradients-abstract": {
        "description": "Dark gradients, abstract curves, neon glows",
        "urls": [
            "https://images.pexels.com/photos/1526/dark-blur-blurred-gradient.jpg",
            "https://images.pexels.com/photos/7135029/pexels-photo-7135029.jpeg",
            "https://images.pexels.com/photos/13216333/pexels-photo-13216333.jpeg",
            "https://images.pexels.com/photos/6985268/pexels-photo-6985268.jpeg",
            "https://images.pexels.com/photos/6985132/pexels-photo-6985132.jpeg",
            "https://images.pexels.com/photos/7135037/pexels-photo-7135037.jpeg",
            "https://images.pexels.com/photos/7640905/pexels-photo-7640905.jpeg",
            "https://images.pexels.com/photos/6985262/pexels-photo-6985262.jpeg",
            "https://images.pexels.com/photos/13062586/pexels-photo-13062586.jpeg",
            "https://images.pexels.com/photos/6985190/pexels-photo-6985190.jpeg",
        ],
    },
    "textures": {
        "description": "Dark surfaces — concrete, metal, grain, fabric",
        "urls": [
            "https://images.pexels.com/photos/6485524/pexels-photo-6485524.jpeg",
            "https://images.pexels.com/photos/7641148/pexels-photo-7641148.jpeg",
            "https://images.pexels.com/photos/7598386/pexels-photo-7598386.jpeg",
            "https://images.pexels.com/photos/5685251/pexels-photo-5685251.jpeg",
            "https://images.pexels.com/photos/6485435/pexels-photo-6485435.jpeg",
            "https://images.pexels.com/photos/3398703/pexels-photo-3398703.jpeg",
            "https://images.pexels.com/photos/7598774/pexels-photo-7598774.jpeg",
            "https://images.pexels.com/photos/6373386/pexels-photo-6373386.jpeg",
            "https://images.pexels.com/photos/6485526/pexels-photo-6485526.jpeg",
            "https://images.pexels.com/photos/4863013/pexels-photo-4863013.jpeg",
        ],
    },
    "code-terminal": {
        "description": "Code editors, terminals, programming screens",
        "urls": [
            "https://images.pexels.com/photos/256502/pexels-photo-256502.jpeg",
            "https://images.pexels.com/photos/6424583/pexels-photo-6424583.jpeg",
            "https://images.pexels.com/photos/14553730/pexels-photo-14553730.jpeg",
            "https://images.pexels.com/photos/9858906/pexels-photo-9858906.jpeg",
            "https://images.pexels.com/photos/14553704/pexels-photo-14553704.jpeg",
            "https://images.pexels.com/photos/6424587/pexels-photo-6424587.jpeg",
            "https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg",
            "https://images.pexels.com/photos/2653362/pexels-photo-2653362.jpeg",
            "https://images.pexels.com/photos/6424584/pexels-photo-6424584.jpeg",
            "https://images.pexels.com/photos/92905/pexels-photo-92905.jpeg",
        ],
    },
}


def extract_photo_id(url):
    """Extract Pexels photo ID from URL."""
    match = re.search(r'pexels-photo-(\d+)', url)
    if match:
        return match.group(1)
    # Handle older URL format like /photos/1526/...
    match = re.search(r'/photos/(\d+)/', url)
    if match:
        return match.group(1)
    return url.split('/')[-1].split('.')[0]


def download_image(url, dest):
    """Download image at portrait size for carousels."""
    # Pexels supports on-the-fly resizing via query params
    separator = "&" if "?" in url else "?"
    sized_url = f"{url}{separator}auto=compress&cs=tinysrgb&w=1080&h=1350&fit=crop"

    req = urllib.request.Request(sized_url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(dest, "wb") as f:
                f.write(data)
            size_kb = len(data) / 1024
            print(f"    OK ({size_kb:.0f} KB)")
            return True
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
        print(f"    FAILED: {e}")
        return False


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    failed = 0

    for theme_name, theme_data in THEMES.items():
        theme_dir = OUT_DIR / theme_name
        theme_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n[{theme_name}] {theme_data['description']}")

        attr_lines = [
            f"# {theme_name} — Pexels Attribution\n\n",
            "All images free under [Pexels License](https://www.pexels.com/license/).\n\n",
        ]

        for i, url in enumerate(theme_data["urls"]):
            photo_id = extract_photo_id(url)
            filename = f"{theme_name}_{i+1:02d}_{photo_id}.jpg"
            dest = theme_dir / filename

            if dest.exists() and dest.stat().st_size > 1000:
                print(f"  [{i+1}/{len(theme_data['urls'])}] {filename} — already exists")
                total += 1
                attr_lines.append(f"- Photo {photo_id} via [Pexels](https://www.pexels.com/photo/{photo_id}/)\n")
                continue

            print(f"  [{i+1}/{len(theme_data['urls'])}] {filename} — downloading...")
            if download_image(url, dest):
                total += 1
                attr_lines.append(f"- Photo {photo_id} via [Pexels](https://www.pexels.com/photo/{photo_id}/)\n")
            else:
                failed += 1

            time.sleep(0.5)

        with open(theme_dir / "_attribution.md", "w") as f:
            f.writelines(attr_lines)

    # Write metadata
    metadata = {}
    for theme_name, theme_data in THEMES.items():
        theme_dir = OUT_DIR / theme_name
        actual_count = len(list(theme_dir.glob("*.jpg")))
        metadata[theme_name] = {
            "description": theme_data["description"],
            "count": actual_count,
            "source": "pexels",
            "license": "Pexels License (free to use)",
        }
    with open(OUT_DIR / "_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n{'=' * 50}")
    print(f"Downloaded: {total} images")
    print(f"Failed: {failed}")
    print(f"Library: {OUT_DIR}")
    print(f"Themes: {', '.join(THEMES.keys())}")


if __name__ == "__main__":
    main()
