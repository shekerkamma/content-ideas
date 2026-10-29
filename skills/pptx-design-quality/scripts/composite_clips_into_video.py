#!/usr/bin/env python3
"""Put a deck's embedded demo clips back into an exported Slides-to-video film.

Google Vids imports a deck as STILL SLIDES, so a `.pptx` carrying embedded media
loses it: the demo slides arrive as their poster frame and sit motionless for
the whole scene while the narration describes what they are doing. There is also
no way to tell Vids "prefer the deck narration over this clip's audio", because
the clip never reaches the Vids document.

So composite it back afterwards. The clips contribute VIDEO ONLY and the audio
stream is copied, so the voiceover survives bit-for-bit -- verify that with an
audio-stream MD5 before and after, not by listening.

Scene windows are derived from the film's own caption stream: each narration
block's first cue marks its scene start, and the next block's first cue marks
the end. That survives a re-export and needs no browser session.

Usage:
  composite_clips_into_video.py <film.mp4> <out.mp4> <spec.json>

spec.json: [{"clip": "...mp4", "start": 305.82, "end": 324.70,
             "seat": [48,168,800,450], "stage": [1280,720]}, ...]
"""
from __future__ import annotations
import json, subprocess, sys


def probe_size(path: str) -> tuple[int, int]:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=width,height", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    w, h = out.split(",")[:2]
    return int(w), int(h)


def main() -> int:
    film, out, spec_path = sys.argv[1], sys.argv[2], sys.argv[3]
    spec = json.load(open(spec_path))
    fw, fh = probe_size(film)

    inputs, parts, last = ["-i", film], [], "0:v"
    for i, s in enumerate(spec, start=1):
        inputs += ["-i", s["clip"]]
        sx, sy, sw, sh = s["seat"]
        stw, sth = s.get("stage", [1280, 720])
        # A slide stage maps to the film by a flat scale factor. Verify it by
        # drawing the rect on a real frame before encoding -- one crop check
        # catches a letterbox or crop assumption.
        k = fw / stw
        assert abs(fh / sth - k) < 0.01, f"stage {stw}x{sth} is not the film's aspect {fw}x{fh}"
        x, y, w, h = round(sx * k), round(sy * k), round(sw * k), round(sh * k)
        parts.append(f"[{i}:v]scale={w}:{h}:flags=lanczos,setpts=PTS-STARTPTS+{s['start']}/TB[c{i}]")
        nxt = f"t{i}"
        parts.append(f"[{last}][c{i}]overlay={x}:{y}:"
                     f"enable='between(t,{s['start']},{s['end']})':eof_action=pass[{nxt}]")
        last = nxt
    fc = ";".join(parts)

    cmd = (["ffmpeg", "-y", "-loglevel", "error"] + inputs +
           ["-filter_complex", fc, "-map", f"[{last}]", "-map", "0:a:0",
            "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-crf", "20", "-preset", "medium", "-r", "30",
            "-c:a", "copy", "-movflags", "+faststart", out])
    subprocess.run(cmd, check=True)

    a = subprocess.run(["ffmpeg", "-v", "error", "-i", film, "-map", "0:a:0", "-f", "md5", "-"],
                       capture_output=True, text=True).stdout.strip()
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", out, "-map", "0:a:0", "-f", "md5", "-"],
                       capture_output=True, text=True).stdout.strip()
    print(f"audio in : {a}\naudio out: {b}\nvoiceover preserved: {a == b}")
    return 0 if a == b else 1


if __name__ == "__main__":
    sys.exit(main())
