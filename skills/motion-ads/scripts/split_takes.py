#!/usr/bin/env python3
"""Split one voiceover take into its lines, at the pauses.

Generate the whole script as ONE take, with a blank line between lines, so the voice stays the
same from start to end. Then split it here and place each line on its shot with mix_sound.py.
Lines are never stretched to fit: if a line is too long for its shot, cut words and re-record.

Writes line-01.wav, line-02.wav, ... and lines.json with each line's length. If you give --expect
and the count does not match, nothing is trusted: listen, then change --pause or --quiet.

The voice is also cleaned lightly on the way through (rumble removed, gentle compression,
a little presence). Turn that off with --raw.

Needs: numpy, ffmpeg.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("take", help="the voiceover file")
    p.add_argument("folder", help="where to write the lines")
    p.add_argument("--pause", type=float, default=0.25, help="a gap at least this long, in seconds, separates two lines (default 0.25)")
    p.add_argument("--quiet", type=float, default=-35.0, help="anything this far below the loudest part counts as silence, dB (default -35)")
    p.add_argument("--expect", type=int, help="how many lines the script has")
    p.add_argument("--raw", action="store_true", help="do not clean the voice")
    a = p.parse_args()

    import numpy as np
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import _audio as au

    R = au.RATE
    source = a.take
    if not a.raw:
        source = os.path.join(tempfile.mkdtemp(prefix="vo_"), "clean.wav")
        clean = ("highpass=f=75,equalizer=f=250:t=q:w=1.2:g=-1.5,equalizer=f=3800:t=q:w=1.0:g=2,"
                 "acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=2")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.take, "-af", clean, "-ar", str(R), "-ac", "1", source], check=True)
    voice = au.read(source, mono=True)
    env = au.smooth(np.abs(voice), 0.02)
    loud = env > env.max() * au.gain(a.quiet)
    edges = np.flatnonzero(np.diff(np.concatenate([[0], loud.astype(int), [0]])))
    spans = []
    for start, stop in zip(edges[::2], edges[1::2]):
        if spans and (start - spans[-1][1]) / R < a.pause:
            spans[-1][1] = stop
        else:
            spans.append([start, stop])
    spans = [s for s in spans if (s[1] - s[0]) / R > 0.08]

    os.makedirs(a.folder, exist_ok=True)
    listing = []
    for i, (start, stop) in enumerate(spans, 1):
        lead, trail = int(0.05 * R), int(0.14 * R)
        piece = au.fade(voice[max(0, start - lead):min(len(voice), stop + trail)], 0.012, 0.06)
        name = f"line-{i:02d}.wav"
        au.write(os.path.join(a.folder, name), piece)
        listing.append({"file": name, "seconds": round(len(piece) / R, 2), "from": round(start / R, 2), "to": round(stop / R, 2)})
        print(f"{name}  {len(piece) / R:5.2f} s   (take {start / R:6.2f}-{stop / R:6.2f} s)")
    json.dump(listing, open(os.path.join(a.folder, "lines.json"), "w"), indent=1)
    if a.expect is not None and a.expect != len(spans):
        sys.exit(f"Found {len(spans)} lines, expected {a.expect}. Change --pause or --quiet and run it again.")
    print(f"Wrote {len(spans)} lines to {a.folder}")


if __name__ == "__main__":
    main()
