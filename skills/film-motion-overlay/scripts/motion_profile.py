#!/usr/bin/env python3
"""Share of a film that is still, and its longest still run, sampled at 2 fps (mean frame delta < 0.15 on 0-255).
Measured 2026-10-03: static deck films 96-97 % still with 31-33 s holds; a motion-graphics film 15 %, longest 1 s.
Usage: motion_profile.py <film.mp4> [...]"""
import subprocess, sys

def profile(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vf", "fps=2,scale=160:90,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    n = 160 * 90; fr = [raw[i:i + n] for i in range(0, len(raw) - n + 1, n)]
    if len(fr) < 2: sys.exit(f"BLOCKED: could not decode {p}")
    d = [sum(abs(a - b) for a, b in zip(fr[k], fr[k + 1])) / n for k in range(len(fr) - 1)]
    run = best = 0
    for x in d: run = run + 1 if x < 0.15 else 0; best = max(best, run)
    still = sum(1 for x in d if x < 0.15) / len(d)
    verdict = "needs motion" if still >= 0.6 else "already moving; skip"
    print(f"{p}: {len(fr)/2:.0f}s, still {still:.0%}, longest still {best/2:.1f}s -> {verdict}")

for p in sys.argv[1:]: profile(p)
