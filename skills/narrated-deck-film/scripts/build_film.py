#!/usr/bin/env python3
"""Compose one video segment per slide, then concatenate the film.

Every segment's runtime comes from the narration manifest. No duration is
hand-typed here and none is re-measured from the audio a second time.

Two motion treatments:
  insert - the clip takes the full frame for a window inside the segment
  pip    - the clip sits in a corner for the whole segment
`insert` is the default because a dense slide has no free corner, and a
corner overlay on one covers live content.

Stdlib + ffmpeg. Resumable: an existing, correct-length segment is left alone.
"""
import argparse
import json
import os
import subprocess
import sys

FPS = 30
W, H = 1920, 1080
FADE = 0.35


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"BLOCKED: ffmpeg failed\n  {' '.join(cmd[:12])} ...\n{p.stderr[-1500:]}")
    return p


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def prepare_motion(src, work, trim=None):
    """Re-encode the capture to H.264 once.

    Playwright records VP8 in WebM with no container duration. Feeding that
    straight into a loop filter is what makes a clip read as a frozen frame.
    """
    if not src:
        return None
    if not os.path.exists(src):
        sys.exit(f"BLOCKED: motion source missing: {src}")
    # A capture usually has idle stretches. An insert that lands on one shows
    # a still screenshot while looking deliberate, so the active region is
    # selected here rather than hoped for. The trim is in the filename so
    # changing it invalidates the cache.
    tag = ""
    if trim:
        tag = f"-{float(trim.get('start', 0)):g}-{float(trim['duration']):g}"
    out = os.path.join(work, f"motion-h264{tag}.mp4")
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        return out
    print(f"  transcoding motion source -> {os.path.basename(out)}")
    cmd = ["ffmpeg", "-y"]
    if trim:
        cmd += ["-ss", str(trim.get("start", 0)), "-t", str(trim["duration"])]
    cmd += ["-i", src, "-an", "-c:v", "libx264", "-crf", "20",
            "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS), out]
    run(cmd)
    return out


def ken_burns(total, zoom_max):
    """Pan rate derived from this segment's own length, so the move completes
    exactly once. A fixed per-frame rate finishes early on a long slide and
    then stalls for the rest of it."""
    # Drive the zoom off `on`, the output frame counter, NOT off zoompan's
    # accumulating `zoom`. With `-loop 1` feeding a still, `zoom+rate` does not
    # accumulate: measured 0.007 mean drift across a whole segment against
    # 13.26 for the `on` form. A film built on the accumulating form is a
    # slideshow of identical frames that still encodes and still passes a
    # duration check, so this must be verified by measuring drift, never by
    # reading the filter string back.
    frames = max(int(total * FPS), 1)
    span = zoom_max - 1.0
    pre = int(W * 1.2) // 2 * 2
    return (f"scale={pre}:-2,"
            f"zoompan=z='1+{span:.6f}*on/{frames}'"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS}")


def segment(img, audio, out, total, pad, motion, cue, zoom_max):
    kb = ken_burns(total, zoom_max)
    window = None
    fit = (f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
           f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps={FPS}")

    if motion and cue and cue.get("mode", "insert") == "insert":
        secs = min(float(cue.get("seconds", 7)), max(total - 2 * FADE, 1.0))
        t0 = max(0.5, min(total * float(cue.get("start_frac", 0.35)),
                          total - secs - 0.5))
        t1 = t0 + secs
        window = [round(t0, 3), round(t1, 3)]
        fc = (f"[0:v]{kb}[bg];"
              f"[1:v]{fit},format=yuva420p,setpts=PTS-STARTPTS+{t0:.3f}/TB,"
              f"fade=t=in:st={t0:.3f}:d={FADE}:alpha=1,"
              f"fade=t=out:st={t1-FADE:.3f}:d={FADE}:alpha=1[mv];"
              f"[bg][mv]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[v];"
              f"[2:a]apad=pad_dur={pad},aresample=async=1[aout]")
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", img,
               "-stream_loop", "-1", "-i", motion, "-i", audio]
        cue_note = f"insert {t0:.1f}-{t1:.1f}s"
    elif motion and cue:
        p = {"w": 680, "h": 400, "margin_x": 50, "margin_y": 50}
        p.update({k: v for k, v in cue.items() if k in p})
        fc = (f"[0:v]{kb}[bg];"
              f"[1:v]scale={p['w']}:{p['h']},setsar=1,fps={FPS}[p];"
              f"[bg][p]overlay=W-w-{p['margin_x']}:H-h-{p['margin_y']}[v];"
              f"[2:a]apad=pad_dur={pad},aresample=async=1[aout]")
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", img,
               "-stream_loop", "-1", "-i", motion, "-i", audio]
        cue_note = f"pip {p['w']}x{p['h']}"
    else:
        fc = f"[0:v]{kb}[v];[1:a]apad=pad_dur={pad},aresample=async=1[aout]"
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", img, "-i", audio]
        cue_note = ""

    cmd += ["-filter_complex", fc, "-map", "[v]", "-map", "[aout]",
            "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
            "-t", f"{total:.3f}", "-movflags", "+faststart", out]
    run(cmd)
    return cue_note, window


def slug(s):
    return "".join(c if c.isalnum() else "-" for c in str(s))[:24]


def resolve_image(cfg, root, slides_dir, s):
    """Explicit per-slide file first, then the numbering pattern.

    Structural slides added by the storyboard carry names, not deck positions,
    so a pattern alone cannot address them.
    """
    explicit = (cfg.get("slide_files") or {}).get(s)
    if explicit:
        return explicit if os.path.isabs(explicit) else os.path.join(root, explicit)
    key = int(s) if str(s).isdigit() else s
    return os.path.join(slides_dir, cfg["slide_pattern"].format(slide=key))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    cfg = json.load(open(a.config))
    root = os.path.dirname(os.path.abspath(a.config))
    rel = lambda p: p if os.path.isabs(p) else os.path.join(root, p)

    work = rel(cfg["work_dir"])
    segs_dir = os.path.join(work, "segments")
    os.makedirs(segs_dir, exist_ok=True)

    man = json.load(open(os.path.join(work, "narration-manifest.json")))
    by_slide = {m["slide"]: m for m in man["slides"]}

    mcfg = cfg.get("motion") or {}
    cues = {str(c["slide"]): c for c in mcfg.get("cues", [])}
    motion = prepare_motion(rel(mcfg["source"]) if mcfg.get("source") else None,
                            work, mcfg.get("trim"))
    if cues and not motion:
        sys.exit("BLOCKED: config declares motion cues but no source.")

    pad = float(cfg.get("tail_padding", 0.9))
    zoom_max = float(cfg.get("zoom_max", 1.08))
    zoom_by = {str(k): float(v) for k, v in (cfg.get("zoom_by_slide") or {}).items()}
    slides_dir = rel(cfg["slides_dir"])
    order = [str(s) for s in cfg["slide_order"]]

    unknown = set(cues) - set(order)
    if unknown:
        sys.exit(f"BLOCKED: motion cues name slides not in slide_order: {sorted(unknown)}")

    print(f"== building {len(order)} segments ==")
    paths, plan, windows = [], [], {}
    for i, s in enumerate(order, 1):
        img = resolve_image(cfg, root, slides_dir, s)
        if not os.path.exists(img):
            sys.exit(f"BLOCKED: slide image missing for slide {s}: {img}")
        if s not in by_slide:
            sys.exit(f"BLOCKED: slide {s} has no entry in the narration manifest.")
        total = round(by_slide[s]["duration"] + pad, 3)
        z = zoom_by.get(s, zoom_max)
        out = os.path.join(segs_dir, f"seg-{slug(s)}.mp4")
        cue = cues.get(s)
        cached = (not a.force and os.path.exists(out)
                  and os.path.getsize(out) > 10000
                  and abs(duration(out) - total) < 0.15)
        note = ""
        if cached:
            note = (cue.get("mode", "insert") if cue else "")
            if cue and cue.get("mode", "insert") == "insert":
                secs = min(float(cue.get("seconds", 7)), max(total - 2 * FADE, 1.0))
                t0 = max(0.5, min(total * float(cue.get("start_frac", 0.35)),
                                  total - secs - 0.5))
                windows[s] = [round(t0, 3), round(t0 + secs, 3)]
            print(f"  slide {s:>3}  cached  {total:6.2f}s  {note}")
        else:
            note, window = segment(img, rel(by_slide[s]["audio"]), out, total,
                                   pad, motion, cue, z)
            windows[s] = window
            print(f"  slide {s:>3}  built   {total:6.2f}s  {note}")
        plan.append({"slide": s, "image": os.path.relpath(img, root),
                     "narration": by_slide[s]["duration"],
                     "segment_seconds": total,
                     "motion": (cue or {}).get("mode") if cue else None,
                     "motion_window": windows.get(s)})
        paths.append(out)

    lst = os.path.join(work, "concat.txt")
    with open(lst, "w") as f:
        for p in paths:
            f.write(f"file '{p}'\n")

    final = rel(cfg["output"])
    os.makedirs(os.path.dirname(final), exist_ok=True)
    print("\n== concatenating ==")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-c", "copy", "-movflags", "+faststart", final])

    expected = round(sum(p["segment_seconds"] for p in plan), 2)
    json.dump({"output": os.path.relpath(final, root),
               "expected_seconds": expected, "segments": plan},
              open(os.path.join(work, "film-manifest.json"), "w"), indent=2)
    print(f"{final}\n  expected {expected}s, actual {duration(final):.2f}s")


if __name__ == "__main__":
    main()
