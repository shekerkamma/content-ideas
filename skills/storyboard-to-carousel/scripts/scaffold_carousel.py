#!/usr/bin/env python3
"""Turn a part storyboard into a carousel to author: cover, one slide per beat, the honest close, a call to action.

Titles come from the storyboard (they are already assertions). Every `body` is left empty: it is
authored for a reader scrolling a feed (one sentence, at most 25 words, what the block means), never
pasted from the beat body, which stays in `source` for the gate.

Usage: scaffold_carousel.py <storyboard.json> --zones zones.json --kicker "SKU-3 · HI-REL PMIC" --url <product page> --out carousel.json
"""
import argparse, json, os, sys

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("storyboard"); ap.add_argument("--zones", required=True)
    ap.add_argument("--kicker", required=True); ap.add_argument("--url", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if os.path.exists(a.out): sys.exit(f"BLOCKED: {a.out} exists and may hold authored copy. Move it first.")
    sb = json.load(open(a.storyboard)); zones = json.load(open(a.zones))["zones"]
    slides = [{"id": "cover", "kind": "cover", "title": sb["headline"], "body": "", "source": sb["lead"], "zones": [], "marks": []}]
    for i, b in enumerate(sb["beats"], 1):
        norm = lambda n: " ".join(n.split())   # "Flight control · hard real-time" == "Flight control  ·  hard real-time"
        byn = {norm(k): k for k in zones}; b["zones"] = [byn.get(norm(z), z) for z in b["zones"]]
        miss = [z for z in b["zones"] if z not in zones]
        if miss: sys.exit(f"BLOCKED: beat {i} names zones not on the diagram: {miss}")
        slides.append({"id": f"b{i}", "kind": "beat", "title": b["title"], "body": "", "source": b["body"], "zones": b["zones"], "marks": b["marks"]})
    slides.append({"id": "close", "kind": "close", "title": sb["closing"]["title"], "body": "", "source": sb["closing"]["body"], "zones": [], "marks": []})
    slides.append({"id": "cta", "kind": "cta", "title": "", "body": "", "source": "", "zones": [], "marks": []})
    json.dump({"part": sb["id"], "kicker": a.kicker, "url": a.url, "slides": slides}, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(f"{len(slides)} slides -> {a.out}; author every body (and the cta title), then run gate_carousel.py")

if __name__ == "__main__":
    main()
