#!/usr/bin/env python3
"""contact_sheet.py — tile rendered slide PNGs into review grids for visual QA.

This is your eyes for QA (the analogue of branded-pptx-deck's preview_pptx.py).
Because the deck is rendered from HTML, the PNGs ARE the final slides — so a
contact sheet is a faithful preview (no placeholder-picture problem).

  python3 contact_sheet.py --png <png-dir> --out <sheet-dir> [--cols 3] [--per 12]

Review every sheet before delivery: check for text overflow, clipped stat bars,
title/subtitle collisions, and a footer/label on each slide.
"""
import argparse, glob, math, os, sys
from PIL import Image, ImageDraw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", default="build/png")
    ap.add_argument("--out", default="build/qa")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--per", type=int, default=12, help="slides per sheet")
    ap.add_argument("--thumbw", type=int, default=640)
    a = ap.parse_args()

    pngs = sorted(glob.glob(os.path.join(a.png, "slide-*.png")))
    if not pngs:
        sys.exit(f"No slide-*.png in {a.png} — run render.mjs first.")
    os.makedirs(a.out, exist_ok=True)

    pad, label_h, bg = 24, 34, (10, 14, 19)
    tw = a.thumbw
    th = int(tw * 9 / 16)
    sheets = []
    for start in range(0, len(pngs), a.per):
        chunk = pngs[start:start + a.per]
        rows = math.ceil(len(chunk) / a.cols)
        W = a.cols * tw + (a.cols + 1) * pad
        H = rows * (th + label_h) + (rows + 1) * pad
        sheet = Image.new("RGB", (W, H), bg)
        draw = ImageDraw.Draw(sheet)
        for k, p in enumerate(chunk):
            r, c = divmod(k, a.cols)
            x = pad + c * (tw + pad)
            y = pad + r * (th + label_h + pad)
            im = Image.open(p).convert("RGB").resize((tw, th))
            sheet.paste(im, (x, y + label_h))
            draw.text((x + 2, y + 8), os.path.basename(p), fill=(150, 170, 185))
        outp = os.path.join(a.out, f"contact-{start // a.per + 1:02d}.png")
        sheet.save(outp)
        sheets.append(outp)
        print("wrote " + outp)
    print(f"DONE: {len(pngs)} slides across {len(sheets)} sheet(s) -> {a.out}")


if __name__ == "__main__":
    main()
