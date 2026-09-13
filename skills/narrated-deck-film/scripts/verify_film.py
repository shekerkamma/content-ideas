#!/usr/bin/env python3
"""Delivery gate for a narrated deck film.

Each check exists because its absence once certified a broken artifact.
Exit 0 clean, 1 blocked (a check could not run), 2 findings.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

FINDINGS, BLOCKED = [], []


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path, entries, stream=None):
    cmd = ["ffprobe", "-v", "error"]
    if stream:
        cmd += ["-select_streams", stream]
    cmd += ["-show_entries", entries, "-of", "json", path]
    p = sh(cmd)
    if p.returncode != 0:
        return None
    return json.loads(p.stdout)


def mean_volume(path):
    """dBFS mean. -v error would suppress volumedetect's own output, so it is
    deliberately not passed here."""
    p = sh(["ffmpeg", "-i", path, "-af", "volumedetect", "-f", "null", "-"])
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", p.stderr)
    return float(m.group(1)) if m else None


def silence_control():
    """Generate true digital silence and measure it the same way.

    A dB threshold picked by hand proves nothing; a control does.
    """
    with tempfile.NamedTemporaryFile(suffix=".m4a", delete=False) as t:
        path = t.name
    sh(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-t", "2", "-c:a", "aac", path])
    v = mean_volume(path)
    os.unlink(path)
    return v


def crop_frame(video, t, rect):
    """One frame's crop region as raw 8-bit grayscale bytes."""
    x, y, w, h = rect
    p = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1",
         "-vf", f"crop={w}:{h}:{x}:{y}", "-pix_fmt", "gray",
         "-f", "rawvideo", "-"], capture_output=True)
    return p.stdout if len(p.stdout) == w * h else None


def mad(a, b):
    """Mean absolute difference between two equal-length gray frames."""
    return sum(abs(p - q) for p, q in zip(a, b)) / len(a)


def check(name, ok, detail):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        FINDINGS.append(f"{name}: {detail}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    a = ap.parse_args()
    cfg = json.load(open(a.config))
    root = os.path.dirname(os.path.abspath(a.config))
    rel = lambda p: p if os.path.isabs(p) else os.path.join(root, p)
    work = rel(cfg["work_dir"])

    film = json.load(open(os.path.join(work, "film-manifest.json")))
    narr = json.load(open(os.path.join(work, "narration-manifest.json")))
    video = rel(film["output"])
    if not os.path.exists(video):
        sys.exit(f"BLOCKED: {video} does not exist.")

    print(f"== verifying {os.path.basename(video)} ==")

    # 1. Runtime is what the measured narration said it would be. Comparing to
    #    intent instead of to the manifest is how a truncated mux passes.
    fmt = probe(video, "format=duration")
    actual = float(fmt["format"]["duration"])
    exp = film["expected_seconds"]
    check("duration matches manifest", abs(actual - exp) < 1.0,
          f"expected {exp:.2f}s, got {actual:.2f}s (drift {actual-exp:+.2f}s)")

    # 2. Streams present and at the delivery spec.
    v = probe(video, "stream=codec_name,width,height,r_frame_rate", "v:0")
    au = probe(video, "stream=codec_name,channels,sample_rate", "a:0")
    if not v or not v.get("streams"):
        BLOCKED.append("no video stream")
    else:
        s = v["streams"][0]
        check("video 1920x1080 h264", s["width"] == 1920 and s["height"] == 1080
              and s["codec_name"] == "h264",
              f"{s['codec_name']} {s['width']}x{s['height']} @ {s['r_frame_rate']}")
    if not au or not au.get("streams"):
        FINDINGS.append("audio: no audio stream in the delivered film")
        print("  [FAIL] audio stream: absent")
    else:
        s = au["streams"][0]
        check("audio aac stereo 44.1k", s["codec_name"] == "aac"
              and int(s["channels"]) == 2,
              f"{s['codec_name']} {s['channels']}ch {s['sample_rate']}Hz")

    # 3. An audio stream that exists can still be silence. Compare against
    #    generated silence rather than against a hand-picked dB number.
    ctl = silence_control()
    got = mean_volume(video)
    if ctl is None or got is None:
        BLOCKED.append("volumedetect produced no reading")
    else:
        check("audio carries speech, not silence", got > ctl + 40,
              f"film {got:.1f} dB vs silent control {ctl:.1f} dB")

    # 4. An inserted clip that is really a frozen poster frame looks correct
    #    on a contact sheet. Prove movement against a static control region on
    #    the same film, not against an absolute threshold.
    if any(seg.get("motion") for seg in film["segments"]):
        t = 0.0
        moving = static_at = None
        for seg in film["segments"]:
            win = seg.get("motion_window")
            if seg.get("motion") and win and moving is None:
                moving = (t + win[0] + (win[1] - win[0]) / 2, t + 0.2)
            if not seg.get("motion") and static_at is None:
                static_at = t + seg["segment_seconds"] / 2
            t += seg["segment_seconds"]
        if moving is None or static_at is None:
            BLOCKED.append("no motion/static pair available to compare")
        else:
            inside, before = moving
            full = (0, 0, 1920, 1080)
            fa = crop_frame(video, inside, full)
            fb = crop_frame(video, inside + 0.5, full)
            sa = crop_frame(video, static_at, full)
            sb = crop_frame(video, static_at + 0.5, full)
            pre = crop_frame(video, before, full)
            if not all((fa, fb, sa, sb, pre)):
                BLOCKED.append("could not sample frames for the motion check")
            else:
                m_moving = mad(fa, fb)
                m_static = mad(sa, sb)
                m_cut = mad(fa, pre)
                # The clip must move ...
                check("inserted clip is animated, not a frozen frame",
                      m_moving > m_static * 3 and m_moving > 1.0,
                      f"insert window MAD {m_moving:.2f} vs static slide "
                      f"{m_static:.2f} over the same 0.5s")
                # ... and it must actually be on screen inside its window.
                check("insert window differs from the slide behind it",
                      m_cut > 8.0,
                      f"MAD {m_cut:.2f} between the insert and the same "
                      f"segment before it opens")

    # 5. Every ordered slide has authored narration that was actually voiced.
    voiced = {m["slide"] for m in narr["slides"] if m["duration"] > 0.5}
    want = {str(s) for s in cfg["slide_order"]}
    check("every slide voiced", voiced >= want,
          f"{len(voiced & want)}/{len(want)} slides carry narration"
          + (f"; missing {sorted(want - voiced)}" if want - voiced else ""))

    # 6. Segment count matches slide count -- a silently dropped slide
    #    otherwise just makes a shorter film.
    check("segment count matches deck", len(film["segments"]) == len(want),
          f"{len(film['segments'])} segments for {len(want)} slides")

    print()
    if BLOCKED:
        for b in BLOCKED:
            print(f"BLOCKED: {b}")
        print("UNMEASURED -- do not treat this film as reviewed.")
        sys.exit(1)
    if FINDINGS:
        print(f"{len(FINDINGS)} finding(s):")
        for f in FINDINGS:
            print(f"  - {f}")
        sys.exit(2)
    print(f"CLEAN -- {actual:.1f}s, {len(film['segments'])} slides, all gates passed.")


if __name__ == "__main__":
    main()
