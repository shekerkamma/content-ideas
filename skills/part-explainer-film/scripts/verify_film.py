#!/usr/bin/env python3
"""Delivery gate for a part explainer, measured on the delivered file. Exit 0 clean, 2 findings, 1 blocked.

- streams: H.264 1920x1080 yuv420p + AAC; duration within 0.2 s of film.json; faststart; size cap
- audio content, not presence: each scene's narration window is louder than generated silence
- motion against a still control: in every scene the camera-move window changes the picture far more
  than the hold window of the same scene (a hold that moves is idle motion; a move that does not is a cut)
- captions: cues ordered, inside the film, non-overlapping; voice gate on file and clean
- poster: real pixel variance (a blank poster passes a size check)
Usage: verify_film.py <run-dir> --out <name> [--max-mb 25]
"""
import argparse, json, pathlib, re, subprocess, sys

def probe(p):
    return json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(p)], capture_output=True, text=True).stdout)

def mean_db(p, s, d):
    e = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{s}", "-t", f"{d}", "-i", str(p), "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.search(r"mean_volume: (-?[\d.]+) dB", e); return float(m.group(1)) if m else -99

def delta(p, s, d):
    """Mean absolute difference between consecutive frames over a window, 0-255 scale."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{s}", "-t", f"{d}", "-i", str(p), "-vf", "scale=320:180,format=gray", "-f", "rawvideo", "-"],
                         capture_output=True).stdout
    n = 320 * 180; fr = [raw[i:i + n] for i in range(0, len(raw) - n + 1, n)]
    if len(fr) < 2: return 0.0
    return sum(sum(abs(a - b) for a, b in zip(fr[k], fr[k + 1])) / n for k in range(len(fr) - 1)) / (len(fr) - 1)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("run"); ap.add_argument("--out", required=True); ap.add_argument("--max-mb", type=float, default=25)
    a = ap.parse_args(); run = pathlib.Path(a.run).resolve(); o = run / "out"
    mp4, vtt, poster = o / f"{a.out}.mp4", o / f"{a.out}.vtt", o / f"{a.out}-poster.jpg"
    for p in (mp4, vtt, poster, o / "film.json"):
        if not p.exists(): sys.exit(f"BLOCKED: missing {p}")
    film = json.load(open(o / "film.json")); F = []
    pr = probe(mp4); v = next(s for s in pr["streams"] if s["codec_type"] == "video"); au = [s for s in pr["streams"] if s["codec_type"] == "audio"]
    if (v["codec_name"], v["width"], v["height"], v["pix_fmt"]) != ("h264", 1920, 1080, "yuv420p"): F.append(f"video stream {v['codec_name']} {v['width']}x{v['height']} {v['pix_fmt']}")
    if not au or au[0]["codec_name"] != "aac": F.append("no AAC audio stream")
    dur = float(pr["format"]["duration"])
    if abs(dur - film["duration"]) > 0.2: F.append(f"duration {dur:.2f}s vs planned {film['duration']:.2f}s")
    head = open(mp4, "rb").read(4096)
    if head.find(b"moov") < 0 or head.find(b"mdat") >= 0 and head.find(b"moov") > head.find(b"mdat"): F.append("moov atom not at the front (no faststart)")
    mb = mp4.stat().st_size / 1e6
    if mb > a.max_mb: F.append(f"{mb:.1f} MB over {a.max_mb} MB")
    fps = 30
    rows = []
    for sc in film["scenes"]:
        s0 = sc["start"]; nar = mean_db(mp4, s0 + film["pre"] + 0.2, max(0.5, sc["narration"] - 0.4))
        mv = delta(mp4, s0 + 0.1, 0.6); hd = delta(mp4, s0 + 1.3, min(2.0, sc["duration"] - 1.5))
        rows.append((sc["scene"], round(nar, 1), round(mv, 2), round(hd, 2)))
        if nar < -45: F.append(f"{sc['scene']}: narration window mean {nar} dB, near silence")
        if hd > 0.3: F.append(f"{sc['scene']}: hold moves ({hd:.2f}); idle motion")
        if mv < max(1.0, 5 * hd): F.append(f"{sc['scene']}: camera move delta {mv:.2f} not clearly above hold {hd:.2f}")
    cues = re.findall(r"(\d\d):(\d\d):(\d\d\.\d+) --> (\d\d):(\d\d):(\d\d\.\d+)", vtt.read_text())
    sec = lambda h, m, s: int(h) * 3600 + int(m) * 60 + float(s)
    prev = 0
    for c in cues:
        st, en = sec(*c[:3]), sec(*c[3:])
        if st < prev - 1e-3 or en <= st or en > dur + 0.05: F.append(f"caption cue {c} out of order or bounds"); break
        prev = en
    if not cues: F.append("no caption cues")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(poster), "-vf", "scale=192:108,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    mu = sum(raw) / len(raw); sd = (sum((x - mu) ** 2 for x in raw) / len(raw)) ** .5
    if sd < 10: F.append(f"poster pixel stddev {sd:.1f}: blank or near-uniform")
    vg = run / "voice-gate.json"
    if not vg.exists() or json.load(open(vg))["findings"]: F.append("voice gate missing or not clean")
    print(f"{mp4.name}: {dur:.1f}s, {mb:.1f} MB, {len(cues)} cues, poster sd {sd:.0f}")
    print("scene   narration dB   move delta   hold delta")
    for r in rows: print(f"{r[0]:>6}   {r[1]:>8}     {r[2]:>8}     {r[3]:>8}")
    for f in F: print("FINDING", f)
    print("CLEAN" if not F else f"{len(F)} findings"); sys.exit(2 if F else 0)

if __name__ == "__main__":
    main()
