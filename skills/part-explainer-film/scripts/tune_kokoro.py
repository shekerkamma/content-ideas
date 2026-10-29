#!/usr/bin/env python3
"""Per-scene Kokoro speed from a measured voice gate, so each scene lands near the Holt pace.

Kokoro's speech rate varies by sentence (one SKU-1 placeholder ran 123-174 wpm across scenes at speed
1.0, and opening its pauses still left the film at 156). New speed = old x target / measured, clamped
to 0.85-1.15 because Kokoro's speed is non-linear and a large step overshoots. Writes `kokoro_speed`
into scenes.json; re-voice with voice.py --provider kokoro, extend pauses, and gate again.
Usage: tune_kokoro.py scenes.json [--target 148]
"""
import argparse, json, pathlib

ap = argparse.ArgumentParser(); ap.add_argument("scenes"); ap.add_argument("--target", type=float, default=148); a = ap.parse_args()
run = pathlib.Path(a.scenes).resolve().parent
gate = {r["scene"]: r["wpm"] for r in json.load(open(run / "voice-gate.json"))["scenes"]}
d = json.load(open(a.scenes))
for s in d["scenes"]:
    old = s.get("kokoro_speed", 1.0); new = round(min(1.15, max(0.85, old * a.target / gate[s["id"]])), 3)
    s["kokoro_speed"] = new; print(f"{s['id']:>6} {gate[s['id']]:4d} wpm  speed {old} -> {new}")
json.dump(d, open(a.scenes, "w"), indent=1, ensure_ascii=False)
