#!/usr/bin/env python3
"""Rebuild a narrated deck film's picture with the planned motion, keeping its sound and captions exactly.

Video: per segment, the rendered frames at their listed durations, the original FADE in and out, at the
original segment length; segments concatenated. Audio and soft-subtitle streams are COPIED from the
original file (-c copy), never re-encoded, so verify_overlay.py can prove them packet-identical.

Usage: build_overlay.py <run-dir> --original film.mp4 --out new.mp4
"""
import argparse, json, pathlib, subprocess, sys

def sh(*a):
    r = subprocess.run([str(x) for x in a], capture_output=True, text=True)
    if r.returncode: sys.exit(f"BLOCKED: {' '.join(map(str, a[:5]))}...\n{r.stderr[-800:]}")
    return r.stdout

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("run"); ap.add_argument("--original", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args(); run = pathlib.Path(a.run).resolve(); tl = json.load(open(run / "timeline.json"))
    seg_dir = run / "work" / "segments"; seg_dir.mkdir(parents=True, exist_ok=True); fps, fade = tl["fps"], tl["fade"]
    parts = []
    # Frame-exact span boundaries, pinned to the original's frame count: cutting each span to whole frames
    # on its own drifted 3 frames short over 9 slides (measured 2026-10-03).
    ov = float(json.loads(sh("ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=duration", "-of", "json", a.original))["streams"][0]["duration"])
    total = round(ov * fps); plan_end = tl["segments"][-1]["start"] + tl["segments"][-1]["duration"]
    edge = lambda t: round(t / plan_end * total)
    for s in tl["segments"]:
        lst = seg_dir / f"{s['slide']:02d}.txt"
        body = "".join(f"file '{i['file']}'\nduration {i['dur']}\n" for i in s["items"]) + f"file '{s['items'][-1]['file']}'\n"
        lst.write_text(body)
        out = seg_dir / f"{s['slide']:02d}.mp4"; nfr = edge(s["start"] + s["duration"]) - edge(s["start"]); d = nfr / fps
        sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
           "-vf", f"fps={fps},format=yuv420p,fade=t=in:st=0:d={fade},fade=t=out:st={d - fade:.3f}:d={fade}",
           "-frames:v", str(nfr), "-r", str(fps), "-c:v", "libx264", "-preset", "medium", "-crf", "22", str(out))
        parts.append(out)
    cat = seg_dir / "all.txt"; cat.write_text("".join(f"file '{p}'\n" for p in parts))
    sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", cat, "-c", "copy", seg_dir / "video.mp4")
    pr = json.loads(sh("ffprobe", "-v", "error", "-show_streams", "-of", "json", a.original))["streams"]
    maps = ["-map", "0:v", "-map", "1:a"] + (["-map", "1:s"] if any(x["codec_type"] == "subtitle" for x in pr) else [])
    sh("ffmpeg", "-v", "error", "-y", "-i", seg_dir / "video.mp4", "-i", a.original, *maps, "-c", "copy",
       "-map_metadata", "1", "-movflags", "+faststart", a.out)
    print(f"{a.out}: {len(parts)} segments; audio{' + subtitles' if len(maps) > 4 else ''} copied from {pathlib.Path(a.original).name}")

if __name__ == "__main__":
    main()
