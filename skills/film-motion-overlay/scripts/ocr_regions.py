#!/usr/bin/env python3
"""Fallback when a film has no source deck: text regions from its slide frames by OCR, written in the
same inspect.ndjson shape plan_overlay.py reads (kind=textbox, slide, text, bbox on a 1280x720 stage).

OCR is the repo-local Tesseract 5.3.4 at content-ideas/.tools/tesseract/bin/tesseract (off PATH on
purpose; TESSERACT env overrides). Tesseract's paragraphs run across a row of cards, so words are regrouped by layout: a line splits
at wide gaps, and runs stack into a region only when they overlap horizontally (card, cell). Prefer the deck's own inspect file whenever it exists: it is exact.

Usage: ocr_regions.py --frames <dir of slide-NN.png> --out ocr.inspect.ndjson [--min-conf 70]
"""
import argparse, collections, csv, glob, io, json, os, pathlib, re, subprocess, sys

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--frames", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--min-conf", type=float, default=70)
    a = ap.parse_args()
    tess = os.environ.get("TESSERACT") or str(pathlib.Path(__file__).resolve().parents[3] / ".tools/tesseract/bin/tesseract")
    if not pathlib.Path(tess).exists(): sys.exit(f"BLOCKED: no tesseract at {tess}; set TESSERACT")
    frames = sorted(glob.glob(os.path.join(a.frames, "slide-*.png")))
    if not frames: sys.exit(f"BLOCKED: no slide-NN.png in {a.frames}")
    rows = 0
    with open(a.out, "w", encoding="utf-8") as out:
        for f in frames:
            n = int(re.search(r"slide-(\d+)", f).group(1))
            tsv = subprocess.run([tess, f, "-", "tsv"], capture_output=True, text=True).stdout
            W = H = None; lines = collections.OrderedDict()
            for r in csv.DictReader(io.StringIO(tsv), delimiter="\t", quoting=csv.QUOTE_NONE):
                if r["level"] == "1": W, H = int(r["width"]), int(r["height"])
                if r["level"] != "5" or not r["text"].strip() or float(r["conf"]) < a.min_conf: continue
                lines.setdefault((r["block_num"], r["par_num"], r["line_num"]), []).append(
                    (int(r["left"]), int(r["top"]), int(r["width"]), int(r["height"]), r["text"]))
            # 1) split each line at wide gaps: Tesseract runs one "line" straight across a row of cards
            runs = []
            for ws in lines.values():
                ws.sort(); cur = [ws[0]]
                for w in ws[1:]:
                    p = cur[-1]; hgt = max(p[3], w[3])
                    if w[0] - (p[0] + p[2]) > 1.6 * hgt: runs.append(cur); cur = [w]
                    else: cur.append(w)
                runs.append(cur)
            boxes = [[min(w[0] for w in r), min(w[1] for w in r), max(w[0] + w[2] for w in r), max(w[1] + w[3] for w in r), " ".join(w[4] for w in r)] for r in runs]
            # 2) stack runs into regions only when they overlap horizontally and sit close vertically
            boxes.sort(key=lambda b: (b[1], b[0])); regions = []
            for b in boxes:
                for g in regions:
                    ov = min(g[2], b[2]) - max(g[0], b[0]); h = b[3] - b[1]
                    if ov > 0.5 * min(g[2] - g[0], b[2] - b[0]) and 0 <= b[1] - g[3] < 1.4 * h:
                        g[0], g[1], g[2], g[3] = min(g[0], b[0]), min(g[1], b[1]), max(g[2], b[2]), max(g[3], b[3]); g[4] += " " + b[4]; break
                else: regions.append(list(b))
            s = 1280 / W
            for x0, y0, x1, y1, text in regions:
                out.write(json.dumps({"kind": "textbox", "slide": n, "text": text,
                                      "bbox": [round(x0 * s), round(y0 * s), round((x1 - x0) * s), round((y1 - y0) * s)], "source": "ocr"}) + "\n"); rows += 1
    print(f"{len(frames)} slides, {rows} text regions -> {a.out}")

if __name__ == "__main__":
    main()
