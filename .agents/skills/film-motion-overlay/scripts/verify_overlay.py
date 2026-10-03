#!/usr/bin/env python3
"""Prove a motion overlay changed the picture and nothing else. Exit 0 clean, 2 findings, 1 blocked.

- audio: packet MD5 (stream copy) AND decoded-PCM MD5 identical to the original
- subtitles: identical text when present; video duration within two frames of the original
- motion against a control: inside each planned move window the new film changes far more than the
  original does at the same time (the original is the still control); the new film's holds stay still
Usage: verify_overlay.py <run-dir> --original orig.mp4 --new new.mp4
"""
import argparse, hashlib, json, pathlib, subprocess, sys

def out(*a): return subprocess.run([str(x) for x in a], capture_output=True).stdout
def md5(b): return hashlib.md5(b).hexdigest()[:16]
def vdur(p): return float(json.loads(out("ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=duration", "-of", "json", p))["streams"][0]["duration"])

def delta(p, s, d):
    raw = out("ffmpeg", "-v", "error", "-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", p, "-vf", "scale=320:180,format=gray", "-f", "rawvideo", "-")
    n = 320 * 180; fr = [raw[i:i + n] for i in range(0, len(raw) - n + 1, n)]
    return sum(sum(abs(x - y) for x, y in zip(fr[k], fr[k + 1])) / n for k in range(len(fr) - 1)) / max(1, len(fr) - 1)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("run"); ap.add_argument("--original", required=True); ap.add_argument("--new", required=True)
    a = ap.parse_args(); run = pathlib.Path(a.run).resolve(); F = []
    pk = [md5(out("ffmpeg", "-v", "error", "-i", p, "-map", "0:a", "-c", "copy", "-f", "data", "-")) for p in (a.original, a.new)]
    pcm = [md5(out("ffmpeg", "-v", "error", "-i", p, "-map", "0:a", "-f", "s16le", "-")) for p in (a.original, a.new)]
    sub = [md5(out("ffmpeg", "-v", "error", "-i", p, "-map", "0:s?", "-c:s", "srt", "-f", "srt", "-")) for p in (a.original, a.new)]
    print(f"audio packets {pk[0]} / {pk[1]}   decoded {pcm[0]} / {pcm[1]}   subtitles {sub[0]} / {sub[1]}")
    if len(out("ffmpeg", "-v", "error", "-i", a.original, "-map", "0:a", "-c", "copy", "-f", "data", "-")) < 1000: sys.exit("BLOCKED: original has no audio to compare")
    if pk[0] != pk[1]: F.append("audio packets differ")
    if pcm[0] != pcm[1]: F.append("decoded audio differs")
    if sub[0] != sub[1]: F.append("subtitle text differs")
    d0, d1 = vdur(a.original), vdur(a.new)
    if abs(d0 - d1) > 2 / 30: F.append(f"video duration {d1:.3f}s vs original {d0:.3f}s")
    tl = json.load(open(run / "timeline.json")); moves = 0
    for s in tl["segments"]:
        t, mv = s["start"], []
        for it in s["items"]:
            if "/m" in it["file"].replace("\\", "/").rsplit("/", 1)[-1][:2] or it["file"].rsplit("/", 1)[-1].startswith("m"):
                mv.append(t)
            t += it["dur"]
        if not mv: continue
        # group consecutive move frames into windows
        wins, w0, prev = [], mv[0], mv[0]
        for x in mv[1:] + [None]:
            if x is None or x - prev > 0.05: wins.append((w0, prev + 1 / 30)); w0 = x
            if x is not None: prev = x
        for w in wins:
            moves += 1
            # floor 0.4: a spotlight with no push (a card too big to zoom into) measured 0.78 against a still 0.00
            new, ctl = delta(a.new, w[0], w[1] - w[0]), delta(a.original, w[0], w[1] - w[0])
            if new < max(0.4, 4 * ctl): F.append(f"slide {s['slide']} move at {w[0]:.1f}s: delta {new:.2f} vs original {ctl:.2f}")
        last_end = max(w[1] for w in wins); hold_end = s["start"] + s["duration"] - tl["fade"] - 0.1
        if hold_end - last_end > 1.0:
            h = delta(a.new, last_end + 0.2, min(2.0, hold_end - last_end - 0.3))
            if h > 0.3: F.append(f"slide {s['slide']}: hold after the last move drifts ({h:.2f})")
    print(f"{moves} move windows checked against the original as a still control")
    for f in F: print("FINDING", f)
    print("CLEAN" if not F else f"{len(F)} findings"); sys.exit(2 if F else 0)

if __name__ == "__main__":
    main()
