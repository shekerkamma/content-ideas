#!/usr/bin/env python3
"""Extract a real, sampled color palette from a captured reference image —
grounds the Color Palette table in a trend-grounded design brief with actual
pixel data instead of eyeballed guesses.

Two passes, because UI screenshots are background-dominated and often
near-monochrome:
  1. Neutral/background ramp (by lightness band) — always produces output.
  2. Accent colors (by hue, gated on a brightness floor) — may be empty; an
     empty result is a real finding (the source is genuinely near-monochrome),
     not a bug. See troubleshoot.md: HSV saturation is numerically unstable
     near black (tiny absolute RGB diffs produce inflated saturation ratios),
     so accent detection MUST gate on value/brightness, not saturation alone.

Usage:
  python3 extract_palette.py <image.png> [--crop X,Y,W,H] [--top N]
"""
import argparse, colorsys, sys
from collections import Counter
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--crop", help="X,Y,W,H — region to sample (default: whole image)")
    ap.add_argument("--top", type=int, default=6)
    ap.add_argument("--min-value", type=float, default=0.15,
                    help="brightness floor for accent detection (avoids near-black HSV-saturation instability)")
    ap.add_argument("--min-saturation", type=float, default=0.20)
    a = ap.parse_args()

    from PIL import Image
    im = Image.open(a.image).convert("RGB")
    if a.crop:
        x, y, w, h = (int(v) for v in a.crop.split(","))
        im = im.crop((x, y, x + w, y + h))
    pixels = list(im.getdata())
    total = len(pixels)

    # Pass 1: neutral/background ramp by lightness band (always meaningful)
    bands = Counter()
    for r, g, b in pixels:
        v = (r + g + b) // 3
        bands[v // 8 * 8] += 1
    print(f"# {a.image} ({im.width}x{im.height}, {total} px sampled)\n")
    print("## Neutral / background ramp (by lightness)")
    for v, count in bands.most_common(a.top):
        print(f"  #{v:02x}{v:02x}{v:02x}  {100*count/total:5.1f}%")

    # Pass 2: accent colors, gated on brightness to avoid near-black HSV instability
    accent_px = [
        (r, g, b) for r, g, b in pixels
        if (lambda h_, s_, v_: s_ > a.min_saturation and v_ > a.min_value)(*colorsys.rgb_to_hsv(r/255, g/255, b/255))
    ]
    print(f"\n## Accent colors (saturation>{a.min_saturation}, value>{a.min_value})")
    if not accent_px:
        print("  none found — source is genuinely near-monochrome in this crop.")
        print("  (real finding, not a bug — report 'restrained/no color accent' as the design signal)")
    else:
        tmp = Image.new("RGB", (len(accent_px), 1))
        tmp.putdata(accent_px)
        q = tmp.quantize(colors=min(a.top * 2, len(accent_px)), method=Image.MEDIANCUT).convert("RGB")
        counts = sorted(q.getcolors(len(accent_px)), reverse=True)
        for count, (r, g, b) in counts[:a.top]:
            print(f"  #{r:02x}{g:02x}{b:02x}  {100*count/total:5.2f}% of sampled region")

    return 0


if __name__ == "__main__":
    sys.exit(main())
