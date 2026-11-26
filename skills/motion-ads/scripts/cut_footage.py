#!/usr/bin/env python3
"""Cut real footage down to the shots in a cut list, on an exact frame grid.

This is the "subtract" half of working on real footage: choose the strongest moments, put them on
the beat, and leave the rest out. The cut list is also the storyboard for a footage edit, so write
it, get it approved, then run this.

Cut list (JSON):
{
  "fps": 25,
  "segments": [
    {"id": "A", "t": [0.0, 3.2], "src": [1.2, 3.0], "what": "aerial over the city", "crop": [0.22, 0.34, 0.64], "interp": true},
    {"id": "B", "t": [3.2, 4.0], "src": [14.3, 15.1], "what": "the dome through leaves", "file": "other-clip.mp4"},
    {"id": "Z", "t": [23.0, 27.0], "src": [95.6, 95.6], "what": "last frame held for the end card", "freeze": true}
  ]
}
  t       where the shot sits in the new edit, in seconds. Put cuts on the music's grid
          (120 BPM = a cut every 0.5 s).
  src     the part of the source to use. If it is shorter or longer than t, the shot is slowed
          or sped up to fit.
  crop    [left, top, size] as fractions of the frame: a 16:9 window, used to push in or to keep
          burned-in titles out of frame.
  interp  build in-between frames for smooth slow motion (slow to render; use on one or two shots).
  freeze  hold the single frame at src[0].
  file    a different source for this shot (default: the source given on the command line).

The source is only read, never changed. Work from a small proxy while you choose shots, then run
this again on the full-size original for the master.

Needs: ffmpeg.
"""
import argparse
import json
import os
import subprocess
import tempfile


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cutlist", help="the cut list (JSON)")
    p.add_argument("source", help="the source video")
    p.add_argument("out", help="the cut to write (.mp4)")
    p.add_argument("--width", type=int, default=1920)
    p.add_argument("--height", type=int, default=1080)
    p.add_argument("--audio", action="store_true", help="keep the source's own sound (for a before/after comparison)")
    p.add_argument("--until", type=float, help="stop at this time in the edit")
    p.add_argument("--crf", default="12", help="quality, lower is better (default 12)")
    a = p.parse_args()

    edit = json.load(open(a.cutlist))
    fps = edit["fps"]
    base = os.path.dirname(os.path.abspath(a.cutlist))
    work = tempfile.mkdtemp(prefix="cut_")
    parts = []
    for seg in edit["segments"]:
        t0, t1 = seg["t"]
        if a.until is not None:
            if t0 >= a.until - 1e-6:
                break
            t1 = min(t1, a.until)
        frames = int(t1 * fps + 0.5) - int(t0 * fps + 0.5)
        s0, s1 = seg["src"]
        src_len, out_len = max(s1 - s0, 1.0 / fps), t1 - t0
        src = os.path.join(base, seg["file"]) if "file" in seg else a.source
        filters = []
        if "crop" in seg:
            x, y, size = seg["crop"]
            filters.append(f"crop=iw*{size}:ih*{size}:iw*{x}:ih*{y}")
        filters.append(f"scale={a.width}:{a.height}:flags=lanczos,setsar=1")
        if seg.get("freeze"):
            inputs = ["-ss", f"{s0:.3f}", "-t", "0.05", "-i", src]
            filters += [f"loop=loop={frames}:size=1:start=0", f"setpts=N/{fps}/TB"]
        else:
            inputs = ["-ss", f"{s0:.3f}", "-t", f"{src_len + 0.5:.3f}", "-i", src]
            filters.append(f"setpts=(PTS-STARTPTS)*{out_len / src_len:.6f}")
            filters.append(f"minterpolate=fps={fps}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" if seg.get("interp") else f"fps={fps}")
        cmd = ["ffmpeg", "-v", "error", "-y"] + inputs
        if a.audio and seg.get("freeze"):
            cmd += ["-f", "lavfi", "-t", f"{out_len}", "-i", "anullsrc=r=48000:cl=stereo"]
        cmd += ["-vf", ",".join(filters), "-frames:v", str(frames)]
        if a.audio:
            if seg.get("freeze"):
                cmd += ["-map", "0:v", "-map", "1:a"]
            else:
                speed, tempo = src_len / out_len, []
                while speed < 0.5:
                    tempo.append("atempo=0.5")
                    speed /= 0.5
                while speed > 2.0:
                    tempo.append("atempo=2.0")
                    speed /= 2.0
                tempo.append(f"atempo={speed:.5f}")
                cmd += ["-af", ",".join(tempo + [f"atrim=0:{out_len}", "afade=t=in:d=0.012",
                                                 f"afade=t=out:st={max(0.0, out_len - 0.02):.3f}:d=0.02", "aresample=48000"])]
            cmd += ["-c:a", "pcm_s16le"]
        else:
            cmd += ["-an"]
        part = os.path.join(work, f"{len(parts):03d}.mov")
        cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", a.crf, "-pix_fmt", "yuv420p", "-r", str(fps), part]
        subprocess.run(cmd, check=True)
        parts.append(part)
        print(f"{seg['id']:>4}  {t0:6.2f}-{t1:6.2f} s  {frames:4d} frames  {seg.get('what', '')}", flush=True)

    listing = os.path.join(work, "list.txt")
    with open(listing, "w") as f:
        f.writelines(f"file '{part}'\n" for part in parts)
    sound = ["-c:a", "aac", "-b:a", "256k"] if a.audio else ["-an"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", listing, "-c:v", "copy"] + sound +
                   ["-movflags", "+faststart", a.out], check=True)
    print(f"Wrote {a.out}")


if __name__ == "__main__":
    main()
