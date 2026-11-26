#!/usr/bin/env python3
"""Scan generated clips for hidden cuts and pops, and check that clips meet at their joins.

A video model sometimes hides a jump cut one frame into a take, or pops for a single frame.
You will not see it on a contact sheet. This measures how much the picture changes on every frame
and flags any frame that changes far more than its neighbours.

With --joins the clips are treated as a sequence, and the last frame of each is compared with the
first frame of the next. A small number means the two shots really meet on the same picture.

Needs: numpy, ffmpeg.
"""
import argparse
import os
import subprocess
import sys


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("clips", nargs="+", help="video files, in film order if you use --joins")
    p.add_argument("--joins", action="store_true", help="also compare each clip's last frame with the next clip's first frame")
    p.add_argument("--ratio", type=float, default=2.8, help="flag a frame that changes this many times more than its neighbours (default 2.8)")
    p.add_argument("--floor", type=float, default=4.0, help="ignore changes smaller than this, on a 0-255 scale (default 4)")
    a = p.parse_args()

    import numpy as np

    W, H = 192, 108
    ends, problems = [], 0
    for clip in a.clips:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", clip, "-vf", f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
                             capture_output=True).stdout
        frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(float)
        if len(frames) < 3:
            sys.exit(f"{clip}: could not read frames")
        change = np.abs(frames[1:] - frames[:-1]).mean(axis=(1, 2))
        usual = np.array([np.median(change[max(0, i - 4):i + 5]) for i in range(len(change))])
        ratio = change / (usual + 0.5)
        jumps = [(int(i) + 1, round(float(change[i]), 1)) for i in np.where((ratio > a.ratio) & (change > a.floor))[0]]
        still = int((change[-6:] < 0.2).sum())
        problems += len(jumps)
        note = f"JUMP at frame {jumps}" if jumps else "no jumps"
        print(f"{os.path.basename(clip):30s} {len(frames):4d} frames   first moves {change[:3].round(1)}   last moves {change[-3:].round(1)}   {note}"
              + (f"   ({still} dead-still frames at the end: trim them when joining)" if still >= 3 else ""))
        ends.append((frames[0], frames[-1], os.path.basename(clip)))
    if a.joins:
        print()
        for (_, last, name_a), (first, _, name_b) in zip(ends, ends[1:]):
            gap = float(np.abs(first - last).mean())
            verdict = "meets" if gap < 3 else ("close" if gap < 6 else "DOES NOT MEET")
            problems += gap >= 6
            print(f"join {name_a} -> {name_b}: difference {gap:.2f}   {verdict}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
