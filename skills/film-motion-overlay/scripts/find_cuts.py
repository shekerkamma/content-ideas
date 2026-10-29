#!/usr/bin/env python3
"""Real slide-cut times of a deck film: the darkest frame of each fade-through-black, at frame accuracy.
Build records (film.json) can drift from the encoded film by several frames per segment; cuts must be
measured from the film itself. Usage: find_cuts.py <film.mp4> [--fps 30]"""
import argparse, json, subprocess, sys
ap = argparse.ArgumentParser(); ap.add_argument("film"); ap.add_argument("--fps", type=int, default=30); a = ap.parse_args()
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.film, "-vf", f"fps={a.fps},scale=64:36,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
n = 64 * 36; lum = [sum(raw[i:i + n]) / n for i in range(0, len(raw) - n + 1, n)]
# A fade-through-black is a dip RELATIVE to both neighbours (a dark navy slide is dark all along, so an
# absolute threshold fires on it every frame: measured, a false "cut" every 2 s on a dark title slide).
W = a.fps // 2; cuts = []
for k in range(W, len(lum) - W):
    before, after = max(lum[k - W:k]), max(lum[k + 1:k + W + 1])
    if lum[k] == min(lum[k - W:k + W + 1]) and lum[k] < 0.6 * min(before, after) and (not cuts or k / a.fps - cuts[-1] > 2):
        cuts.append(round(k / a.fps, 3))
print(json.dumps(cuts))
