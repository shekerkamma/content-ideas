#!/usr/bin/env python3
"""Assemble a part explainer from rendered frames and gated voice. Durations come from voice.json only.

Per scene: the camera move (frames/<scene>/m###.png at the render fps), then hold.png for the rest of
the scene. Scene length = PRE + narration + POST, so the narration starts while the camera settles
and every cut sits inside a Holt transition pause (PRE + POST ~ 1.05 s). Captions ship as a WebVTT
track (cues per sentence, timed by character share of the scene's narration), never burned in: the
lower half of the frame is the diagram, and text over it would hide the thing being explained.

Usage: build_film.py <run-dir> --out <name>   -> <run>/out/<name>.mp4, .vtt, -poster.jpg, film.json
"""
import argparse, json, pathlib, re, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from spoken import strip_tags

PRE, POST, END_HOLD = 0.45, 0.6, 1.6

def sh(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode: sys.exit(f"BLOCKED: {' '.join(a[:6])}...\n{r.stderr[-800:]}")
    return r.stdout

def ts(t):
    return f"{int(t//3600):02d}:{int(t%3600//60):02d}:{t%60:06.3f}"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("run"); ap.add_argument("--out", required=True); a = ap.parse_args()
    run = pathlib.Path(a.run).resolve(); out = run / "out"; tmp = run / "work" / "segments"; out.mkdir(exist_ok=True); tmp.mkdir(parents=True, exist_ok=True)
    fr = json.load(open(run / "frames" / "frames.json")); fps = fr["fps"]
    vo = {v["scene"]: v for v in json.load(open(run / "voice.json"))["scenes"]}
    sc = json.load(open(run / "scenes.json"))["scenes"]
    vlist, alist, cues, t0, timing = [], [], [], 0.0, []
    for i, s in enumerate(sc):
        v = vo[s["id"]]; post = END_HOLD if i == len(sc) - 1 else POST
        move = next(x for x in fr["scenes"] if x["scene"] == s["id"])["move_frames"] / fps
        dur = round(PRE + v["duration"] + post, 3); hold = dur - move
        if hold <= 0: sys.exit(f"BLOCKED: scene {s['id']} is shorter than its camera move")
        seg = tmp / f"{i:02d}-{s['id']}.mp4"; aud = tmp / f"{i:02d}-{s['id']}.wav"
        fd = run / "frames" / s["id"]
        sh("ffmpeg", "-v", "error", "-y", "-framerate", str(fps), "-i", str(fd / "m%03d.png"), "-loop", "1", "-framerate", str(fps), "-t", f"{hold:.3f}", "-i", str(fd / "hold.png"),
           "-filter_complex", f"[0:v][1:v]concat=n=2:v=1:a=0,fps={fps},format=yuv420p[v]", "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-tune", "stillimage", "-r", str(fps), str(seg))
        sh("ffmpeg", "-v", "error", "-y", "-i", str(run / v["audio"]), "-af", f"aresample=48000,adelay={int(PRE*1000)}:all=1,apad,atrim=0:{dur}",
           "-ac", "2", "-ar", "48000", str(aud))
        vlist.append(seg); alist.append(aud)
        # captions: one cue per sentence, by character share of the spoken span
        text = strip_tags(s["narration"]).replace("...", ".")
        sents = [x.strip() for x in re.split(r"(?<=[.?!])\s+", text) if x.strip()]
        span, at, total = v["duration"], t0 + PRE, sum(len(x) for x in sents)
        for x in sents:
            d = span * len(x) / total; cues.append((at, at + d, x)); at += d
        timing.append({"scene": s["id"], "start": round(t0, 3), "duration": dur, "narration": v["duration"]}); t0 += dur
    lst = tmp / "video.txt"; lst.write_text("".join(f"file '{p}'\n" for p in vlist))
    alst = tmp / "audio.txt"; alst.write_text("".join(f"file '{p}'\n" for p in alist))
    sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(tmp / "video.mp4"))
    sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(alst), "-c", "pcm_s16le", str(tmp / "audio.wav"))
    mp4 = out / f"{a.out}.mp4"
    sh("ffmpeg", "-v", "error", "-y", "-i", str(tmp / "video.mp4"), "-i", str(tmp / "audio.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
       "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(mp4))
    (out / f"{a.out}.vtt").write_text("WEBVTT\n\n" + "\n".join(f"{ts(s)} --> {ts(e)}\n{x}\n" for s, e, x in cues), encoding="utf-8")
    # The poster is the opening frame: the part's label over its whole diagram. A mid-film beat was a random
    # frame under a different title on every card of the videos page (visual round, 2026-10-03).
    poster = run / "frames" / sc[0]["id"] / "hold.png"
    sh("ffmpeg", "-v", "error", "-y", "-i", str(poster), "-q:v", "3", str(out / f"{a.out}-poster.jpg"))
    json.dump({"scenes": timing, "duration": round(t0, 3), "pre": PRE, "post": POST}, open(out / "film.json", "w"), indent=1)
    print(f"{mp4} {t0:.1f}s, {len(cues)} caption cues, poster from {poster.parent.name}")

if __name__ == "__main__":
    main()
