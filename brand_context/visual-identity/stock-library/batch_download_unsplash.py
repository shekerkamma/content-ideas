#!/usr/bin/env python3
"""
Batch download free Unsplash images found via Exa search.
Organizes into themed folders for carousel backgrounds.
"""

import json
import os
import time
import urllib.request
import urllib.error
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
OUT_DIR = SCRIPT_DIR / "themes"

# Images found via Exa search — Unsplash free-to-use photos
THEMES = {
    "dark-tech": {
        "description": "Dark technology backgrounds — circuits, code, networks",
        "photos": [
            {"id": "Uth1P7sF73c", "credit": "Adi Goldstein"},
            {"id": "cZgRe9BlYR4", "credit": "Alexandre Debiève"},
            {"id": "6dJ6nRcmg1U", "credit": "Umberto"},
            {"id": "okgGLg93-vY", "credit": "Markus Spiske"},
            {"id": "EaI_VX4uqVs", "credit": "Michael Dziedzic"},
            {"id": "O9CEZz7YVK4", "credit": "Luca Bravo"},
            {"id": "cfVRxXcA0pY", "credit": "Alexandre Debiève"},
            {"id": "v4aoojn7Ptg", "credit": "Vishnu Mohanan"},
            {"id": "XivABkdV6_Q", "credit": "Vishnu Mohanan"},
            {"id": "iHLiMvS8JEs", "credit": "Luca Bravo"},
        ],
    },
    "gradients-neon": {
        "description": "Gradients, neon glows, geometric abstracts",
        "photos": [
            {"id": "puevMYGnHkw", "credit": "Pawel Czerwinski"},
            {"id": "XzdxbH02wuo", "credit": "Pawel Czerwinski"},
            {"id": "FqGeOOkN4qs", "credit": "Pawel Czerwinski"},
            {"id": "OGx5c4cuaMU", "credit": "Pawel Czerwinski"},
            {"id": "R2RScZislCY", "credit": "Shubham Dhage"},
            {"id": "M8M3czYe6GM", "credit": "Sebastian Svenson"},
            {"id": "vLZD_PKr8Vc", "credit": "Maxim Berg"},
            {"id": "oUdR2wJAoEE", "credit": "Pawel Czerwinski"},
            {"id": "xbPTWdE7tQ4", "credit": "Milad Fakurian"},
            {"id": "x7Mxcuw4Pc8", "credit": "Milad Fakurian"},
        ],
    },
    "textures": {
        "description": "Dark surfaces, materials, grain, concrete, metal",
        "photos": [
            {"id": "x1LZdXbix1Y", "credit": "Annie Spratt"},
            {"id": "Twp5TuFHXYw", "credit": "Pawel Czerwinski"},
            {"id": "bHyoM3_sebE", "credit": "Annie Spratt"},
            {"id": "d_dd6ecFs_g", "credit": "Joel Filipe"},
            {"id": "HQNS-r0b1I8", "credit": "Pawel Czerwinski"},
            {"id": "malflzbGTMY", "credit": "Pawel Czerwinski"},
            {"id": "qVt5xDOD-rw", "credit": "Pawel Czerwinski"},
            {"id": "1U7swO_FBTg", "credit": "Pawel Czerwinski"},
            {"id": "kHG5d5g8Dvo", "credit": "Pawel Czerwinski"},
            {"id": "CBvDWJqRBIQ", "credit": "Pawel Czerwinski"},
        ],
    },
    "code-terminal": {
        "description": "Code editors, terminals, programming screens",
        "photos": [
            {"id": "5sLNGV2EFRM", "credit": "Markus Spiske"},
            {"id": "FjtWczJWRlc", "credit": "Markus Spiske"},
            {"id": "9-U8xW54Le0", "credit": "Mohammad Rahmani"},
            {"id": "n3ba57RKVNs", "credit": "Ilya Pavlov"},
            {"id": "v-jFS1AsHXo", "credit": "Sai Kiran Anagani"},
            {"id": "HnfsOiBpzU0", "credit": "Luca Bravo"},
            {"id": "gKmacp0V9Bw", "credit": "Chris Ried"},
            {"id": "WD7S-Lz12Es", "credit": "Mohammad Rahmani"},
            {"id": "oYzjGQ7LCVE", "credit": "Kevin Ku"},
            {"id": "v9iowyOH7QQ", "credit": "Kevin Ku"},
        ],
    },
}


def download_image(photo_id, dest, width=1080, height=1350):
    """Download from Unsplash's direct image URL."""
    url = f"https://images.unsplash.com/photo-{photo_id}?w={width}&h={height}&fit=crop&auto=format&q=80"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; BrandAssetDownloader/1.0)")
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

        # Attribution file
        attr_lines = [f"# {theme_name} — Unsplash Attribution\n\n"]

        for i, photo in enumerate(theme_data["photos"]):
            pid = photo["id"]
            credit = photo["credit"]
            filename = f"{theme_name}_{i+1:02d}_{pid}.jpg"
            dest = theme_dir / filename

            if dest.exists():
                print(f"  [{i+1}/{len(theme_data['photos'])}] {filename} — already exists")
                total += 1
                attr_lines.append(
                    f"- [{credit}](https://unsplash.com/@{credit.lower().replace(' ', '')}) "
                    f"via [Unsplash](https://unsplash.com/photos/{pid})\n"
                )
                continue

            print(f"  [{i+1}/{len(theme_data['photos'])}] {filename} — downloading...")
            if download_image(pid, dest):
                total += 1
                attr_lines.append(
                    f"- [{credit}](https://unsplash.com/@{credit.lower().replace(' ', '')}) "
                    f"via [Unsplash](https://unsplash.com/photos/{pid})\n"
                )
            else:
                failed += 1

            time.sleep(0.3)  # rate limit courtesy

        # Write attribution
        with open(theme_dir / "_attribution.md", "w") as f:
            f.writelines(attr_lines)

    # Write metadata
    metadata = {}
    for theme_name, theme_data in THEMES.items():
        metadata[theme_name] = {
            "description": theme_data["description"],
            "count": len(theme_data["photos"]),
            "source": "unsplash",
            "license": "Unsplash License (free to use)",
        }
    with open(OUT_DIR / "_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n{'=' * 50}")
    print(f"Downloaded: {total} images")
    print(f"Failed: {failed} images")
    print(f"Library: {OUT_DIR}")
    print(f"Themes: {', '.join(THEMES.keys())}")


if __name__ == "__main__":
    main()
