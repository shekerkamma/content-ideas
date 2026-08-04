#!/usr/bin/env python3
"""Capture a real product's live page as a design reference — free, no paywall,
no signup. Wraps html_to_png.mjs's --full mode, bounds the capture to a
Read-able height, and catalogs the result into assets/references/.

This is the free-first alternative to Mobbin's paid MCP: instead of a curated
database, it screenshots the actual live source directly.

Usage:
  python3 capture_reference.py --url https://linear.app --category dashboard-dark \
      --brand linear --note "dark SaaS product UI, embedded issue detail panel"

Output: assets/references/<category>/<brand>.png + <brand>.json (metadata),
        assets/references/catalog.md updated with one line.
"""
import argparse, json, os, subprocess, sys, time
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
REFS_DIR = SKILL_DIR / "assets" / "references"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--category", required=True, help="e.g. dashboard-dark, landing-hero, pricing, onboarding, empty-state")
    ap.add_argument("--brand", required=True, help="slug, e.g. linear, stripe, notion")
    ap.add_argument("--note", default="", help="what makes this reference useful")
    ap.add_argument("--size", default="1440x900", help="viewport WxH")
    ap.add_argument("--max-height", type=int, default=2800, help="crop cap so Read() stays legible")
    ap.add_argument("--settle", type=int, default=0, help="ms to wait after load before screenshot (motion-heavy sites: intro fades, GSAP reveals)")
    a = ap.parse_args()

    cat_dir = REFS_DIR / a.category
    cat_dir.mkdir(parents=True, exist_ok=True)
    png_path = cat_dir / f"{a.brand}.png"
    tmp_path = cat_dir / f".{a.brand}-full-tmp.png"
    width = int(a.size.split("x")[0])

    script = SKILL_DIR / "scripts" / "html_to_png.mjs"
    cmd = ["node", str(script), a.url, str(tmp_path), a.size, "--full"]
    if a.settle:
        cmd += ["--settle", str(a.settle)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=90 + a.settle / 1000)
    if r.returncode != 0:
        print(f"ERROR capturing {a.url}: {r.stderr.strip()}", file=sys.stderr)
        return 1

    from PIL import Image
    im = Image.open(tmp_path)
    full_h = im.height
    cropped_h = min(full_h, a.max_height)
    im.crop((0, 0, width, cropped_h)).save(png_path)
    tmp_path.unlink()

    meta = {
        "source_url": a.url,
        "category": a.category,
        "brand": a.brand,
        "note": a.note,
        "captured_viewport": a.size,
        "full_page_height_px": full_h,
        "saved_height_px": cropped_h,
        "captured_at": time.strftime("%Y-%m-%d"),
    }
    (cat_dir / f"{a.brand}.json").write_text(json.dumps(meta, indent=2))

    catalog = REFS_DIR / "catalog.md"
    key = f"**{a.category}/{a.brand}**"
    line = f"- {key} — {a.note or '(no note)'} · source: {a.url} · {cropped_h}px captured (full page was {full_h}px) · {meta['captured_at']}\n"
    existing = catalog.read_text().splitlines(keepends=True) if catalog.exists() else []
    kept = [l for l in existing if key not in l]
    with open(catalog, "w") as f:
        f.writelines(kept)
        f.write(line)

    print(f"saved: {png_path} ({width}x{cropped_h}, full page was {full_h}px)")
    print(f"metadata: {cat_dir / (a.brand + '.json')}")
    print(f"catalog: {catalog}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
