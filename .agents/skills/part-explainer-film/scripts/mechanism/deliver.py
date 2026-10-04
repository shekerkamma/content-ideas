#!/usr/bin/env python3
"""Gate a rendered mechanism film and package it for the site.

deliver.py <part>  ->  videos/<part>-mechanism/out/<part>-mechanism.{mp4,vtt,-poster.jpg}

Gate (exit 2 on any finding): the render is newer than every build input, it is 1920x1080 with an
audio stream, its length matches the composition within 0.25 s, the voice is audible, and every
caption word lands inside the film. The VTT is sentence cues from the script-aligned caption words
(the same pattern as dg32-fault-path-explained.vtt); the poster is scene 1 fully drawn with the caption
band painted ink, proven clean.
"""
import json, pathlib, re, shutil, subprocess, sys

ROOT = pathlib.Path.home() / "hyperframes-videos/videos"   # the projects live beside the template, not in the skill


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def ts(t):
    h, r = divmod(max(0.0, t), 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def cues(words, max_words=12):
    """Sentence cues: break at a sentence end, at a pause over 0.45 s (an ellipsis the captions dropped),
    or at a comma once a cue is long; never past max_words."""
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        gap = (nxt["start"] - w["end"]) if nxt else 9
        if (re.search(r"[.?!]$", w["text"]) or gap > 0.45 or (len(cur) >= 8 and w["text"].endswith(","))
                or len(cur) >= max_words):
            out.append(cur); cur = []
    if cur: out.append(cur)
    return [(c[0]["start"], c[-1]["end"], " ".join(x["text"] for x in c)) for c in out]


def lib_ink():
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import lib
    return "0x" + lib.C["ink"].lstrip("#")


def make_loop(proj, mp4, dest):
    """A silent hero loop for the product page: scene 1 as it builds, cropped above the caption band (lib.py
    keeps content above y = 880), no audio. The page's full film carries the narration and captions."""
    groups = json.load(open(pathlib.Path(proj) / "caption_groups.json"))
    end = min(g["start"] for g in groups["groups"] if g["frame"] == 2) - 0.2
    sh("ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-t", f"{end:.2f}", "-an", "-vf", "crop=1920:880:0:0,scale=1280:-2,fps=30",
       "-c:v", "libx264", "-crf", "30", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dest))
    band = sh("ffprobe", "-v", "error", "-show_entries", "stream=width,height:format=duration", "-of", "csv=p=0", str(dest)).stdout.split()
    print(f"loop {pathlib.Path(dest).name}: {' '.join(band)}")


def main(part):
    proj = ROOT / f"{part}-mechanism"; mp4 = proj / "renders/video.mp4"; findings = []
    if not mp4.exists():
        sys.exit(f"BLOCKED: {mp4} not rendered")
    inputs = [proj / "index.html", proj / "audio_meta.json", proj / "caption_groups.json", *(proj / "compositions").rglob("*.html")]
    stale = [p.name for p in inputs if p.stat().st_mtime > mp4.stat().st_mtime]
    if stale: findings.append(f"render is older than {stale[:3]}")
    pr = json.loads(sh("ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height:format=duration", "-of", "json", str(mp4)).stdout)
    v = [s for s in pr["streams"] if s["codec_type"] == "video"]; a = [s for s in pr["streams"] if s["codec_type"] == "audio"]
    if not v or (v[0]["width"], v[0]["height"]) != (1920, 1080): findings.append("video is not 1920x1080")
    if not a: findings.append("no audio stream")
    dur = float(pr["format"]["duration"]); groups = json.load(open(proj / "caption_groups.json"))
    if abs(dur - groups["total_duration_s"]) > 0.25: findings.append(f"length {dur:.2f} s vs composition {groups['total_duration_s']:.2f} s")
    vol = re.search(r"mean_volume: (-?[\d.]+)", sh("ffmpeg", "-i", str(mp4), "-af", "volumedetect", "-f", "null", "-").stderr)
    if not vol or float(vol.group(1)) < -35: findings.append(f"voice too quiet or silent ({vol and vol.group(1)} dB)")
    words = [w for g in groups["groups"] for w in g["words"]]
    script = [w["text"] for v in json.load(open(proj / "audio_meta.json"))["voices"] for w in v["words"]]
    if [w["text"] for w in words] != script: findings.append("burned-in captions are not in script order (overlapping word times)")
    late = [w["text"] for w in words if w["end"] > dur + 0.05]
    if late: findings.append(f"{len(late)} caption words after the film ends")
    if findings:
        for f in findings: print("FINDING:", f)
        sys.exit(2)
    out = proj / "out"; out.mkdir(exist_ok=True); name = f"{part}-mechanism"
    shutil.copy(mp4, out / f"{name}.mp4")
    vtt = ["WEBVTT", ""]
    prev = 0.0
    for i, (s, e, t) in enumerate(cues(words), 1):
        s = max(s, prev); prev = e          # scenes overlap by their 0.5 s tails; two cues on screen at once read as noise
        vtt += [str(i), f"{ts(s)} --> {ts(e)}", t, ""]
    (out / f"{name}.vtt").write_text("\n".join(vtt), encoding="utf-8")
    # Poster: scene 1 fully drawn, 0.3 s before it hands over, with the caption band painted ink. The first
    # posters carried a half-sentence ("still come"); waiting for a caption pause sent two parts to their closing
    # slide. lib.py keeps every element above y = 880, so the band holds only captions; prove it is clean after.
    t1 = min(g["start"] for g in groups["groups"] if g["frame"] == 2) - 0.3
    poster = out / f"{name}-poster.jpg"
    sh("ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t1:.2f}", "-i", str(mp4), "-frames:v", "1", "-vf",
       f"drawbox=x=0:y=885:w=1920:h=195:color={lib_ink()}:t=fill", "-q:v", "3", str(poster))
    band = sh("ffmpeg", "-i", str(poster), "-vf", "crop=1920:180:0:900,signalstats,metadata=print:key=lavfi.signalstats.YMAX", "-f", "null", "-").stderr
    ymax = re.search(r"YMAX=(\d+)", band)
    if not ymax or int(ymax.group(1)) > 80:
        print(f"FINDING: poster caption band is not clean (YMAX {ymax and ymax.group(1)})"); sys.exit(2)
    make_loop(proj, mp4, out / f"{name}-loop.mp4")
    print(f"{part}: {dur:.1f} s, {len(cues(words))} cues -> {out}")


if __name__ == "__main__":
    if sys.argv[1] == "--loop":                       # deliver.py --loop <project-dir> <film.mp4> <dest.mp4>
        make_loop(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        main(sys.argv[1])
