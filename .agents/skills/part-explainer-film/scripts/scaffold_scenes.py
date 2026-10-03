#!/usr/bin/env python3
"""Turn a part storyboard into a scene list to author: an opening problem scene, one scene per beat,
and a closing "what is still unproven" scene.

It writes structure only. `label` (2-6 on-screen words) and `narration` stay empty: they are
authored for the ear under the Holt rules (SKILL.md), never copied from the beat body, which is
kept in `source` so the gate can trace numbers and measure echo.

Usage: scaffold_scenes.py <storyboard.json> --zones zones.json --kicker "SKU-3 · HI-REL PMIC" --out scenes.json
"""
import argparse, json, os, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard"); ap.add_argument("--zones", required=True)
    ap.add_argument("--kicker", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if os.path.exists(a.out): sys.exit(f"BLOCKED: {a.out} exists; it may hold authored narration. Move it first.")
    sb = json.load(open(a.storyboard)); zones = json.load(open(a.zones))["zones"]
    scenes = [{"id": "open", "kind": "open", "marks": [], "zones": [], "label": "", "narration": "",
               "source": sb["lead"], "headline": sb["headline"]}]
    for i, b in enumerate(sb["beats"], 1):
        norm = lambda n: " ".join(n.split())   # "Flight control · hard real-time" == "Flight control  ·  hard real-time"
        byn = {norm(k): k for k in zones}; b["zones"] = [byn.get(norm(z), z) for z in b["zones"]]
        miss = [z for z in b["zones"] if z not in zones]
        if miss: sys.exit(f"BLOCKED: beat {i} names zones not on the diagram: {miss}. Diagram has {list(zones)}")
        scenes.append({"id": f"b{i}", "kind": "beat", "marks": b["marks"], "zones": b["zones"], "title": b["title"],
                       "label": "", "narration": "", "source": b["body"]})
    c = sb["closing"]
    scenes.append({"id": "close", "kind": "close", "marks": [], "zones": [], "title": c["title"], "label": "",
                   "narration": "", "source": c["body"]})
    json.dump({"part": sb["id"], "kicker": a.kicker, "headline": sb["headline"], "scenes": scenes},
              open(a.out, "w"), indent=1, ensure_ascii=False)
    print(f"{len(scenes)} scenes -> {a.out}; author every label and narration, then run gate_script.py")

if __name__ == "__main__":
    main()
