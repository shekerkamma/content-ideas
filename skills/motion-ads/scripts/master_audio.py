#!/usr/bin/env python3
"""Bring a mix to a delivery loudness, then measure the result.

Two-pass loudness normalisation with ffmpeg (linear gain, so the mix's own dynamics are kept),
written as a 24-bit 48 kHz WAV. Defaults suit YouTube: -14 LUFS integrated, -1 dB true peak.

Prints the loudness before and after, and the level of the last half second, so you can see that
the track really ends in silence instead of being cut off mid-tail.

With --check it only measures the file (a WAV or the finished MP4) and changes nothing.
With --video it also puts the mastered sound on the picture without re-encoding the picture.

Needs: ffmpeg. numpy only for the tail check (skipped if numpy is missing).
"""
import argparse
import json
import subprocess
import sys


def measure(path, target, peak):
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn", "-af",
         f"loudnorm=I={target}:TP={peak}:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    if "{" not in err:
        sys.exit(f"ffmpeg could not read the audio in {path}:\n{err[-600:]}")
    return json.loads(err[err.rindex("{"): err.rindex("}") + 1])


def tail_level(path, seconds=0.5):
    try:
        import numpy as np
    except ImportError:
        return None
    raw = subprocess.run(["ffmpeg", "-v", "error", "-sseof", f"-{seconds}", "-i", path, "-vn", "-ac", "2", "-ar", "48000", "-f", "f32le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    return None if len(x) == 0 else float(20 * np.log10(np.sqrt(np.mean(np.square(x.astype(np.float64)))) + 1e-9))


def show(label, m, tail):
    line = f"{label:8s} {float(m['input_i']):6.1f} LUFS   true peak {float(m['input_tp']):5.1f} dB   range {float(m['input_lra']):4.1f} LU"
    if tail is not None:
        line += f"   last 0.5 s {tail:6.1f} dBFS"
    print(line)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source", help="the mix (WAV), or with --check any audio or video file")
    p.add_argument("out", nargs="?", help="the mastered WAV to write")
    p.add_argument("--lufs", type=float, default=-14.0, help="integrated loudness target (default -14, YouTube)")
    p.add_argument("--peak", type=float, default=-1.0, help="true-peak ceiling in dB (default -1)")
    p.add_argument("--check", action="store_true", help="measure only, write nothing")
    p.add_argument("--video", help="a silent or old-sound video: also write <out>.mp4 with this picture and the new sound")
    a = p.parse_args()

    before = measure(a.source, a.lufs, a.peak)
    show("before", before, tail_level(a.source))
    if a.check:
        off = float(before["input_i"]) - a.lufs
        if abs(off) > 1.0:
            print(f"CHECK: {off:+.1f} LU away from the {a.lufs} LUFS target.")
        if float(before["input_tp"]) > a.peak + 0.3:
            print(f"CHECK: true peak is above the {a.peak} dB ceiling.")
        return
    if not a.out:
        p.error("give an output file, or use --check")

    gain = a.lufs - float(before["input_i"])
    if float(before["input_tp"]) + gain <= a.peak:
        # The mix fits under the ceiling: one plain gain change, nothing else touched.
        chain = f"volume={gain:.2f}dB"
    else:
        chain = (f"loudnorm=I={a.lufs}:TP={a.peak}:LRA=11:measured_I={before['input_i']}:measured_TP={before['input_tp']}:"
                 f"measured_LRA={before['input_lra']}:measured_thresh={before['input_thresh']}:offset={before['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.source, "-af", chain + ",aresample=48000", "-c:a", "pcm_s24le", a.out], check=True)
    after = measure(a.out, a.lufs, a.peak)
    tail = tail_level(a.out)
    show("after", after, tail)
    if tail is not None and tail > -45:
        print("CHECK: the last half second is not quiet. Fade the music out earlier, or the ad will end on a cut-off tail.")
    if a.video:
        mp4 = a.out.rsplit(".", 1)[0] + ".mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-i", a.out, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", "-shortest", mp4], check=True)
        print(f"Wrote {mp4} (picture copied untouched)")
    print(f"Wrote {a.out}")


if __name__ == "__main__":
    main()
