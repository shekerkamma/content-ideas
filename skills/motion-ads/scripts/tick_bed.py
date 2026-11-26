#!/usr/bin/env python3
"""Build a steady mechanical bed (ticking, clicking, a motor's pulse) from real recorded beats.

Text-to-sound models cannot keep time: ask for "eight ticks a second" and you get six uneven clicks.
Looping one sample sounds like a machine gun. This script does it the way that worked:

  1. find every separate beat in one or more recordings,
  2. cut each one out and shrink it to the size of the product (--speed),
  3. lay them on an exact grid at the real rate (--rate), alternating two pools so it goes
     tick-tock, with tiny random changes in level and position so no two beats are identical,
  4. filter it and add a hint of room.

Use the product's real rate. A fine mechanical movement beats 8 times a second (28,800 an hour);
an older one 6 or 5. A wall clock beats once a second. Look the number up, do not guess.

Needs: numpy, ffmpeg.
"""
import argparse
import os
import sys


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("out", help="the WAV to write")
    p.add_argument("sources", nargs="+", help="one or more recordings that contain separate beats")
    p.add_argument("--rate", type=float, required=True, help="beats per second of the real mechanism")
    p.add_argument("--seconds", type=float, required=True, help="length of the bed")
    p.add_argument("--speed", type=float, default=1.65, help="play each beat this much faster, which makes it sound smaller (default 1.65)")
    p.add_argument("--low-cut", type=float, default=850, help="remove rumble below this, Hz (default 850)")
    p.add_argument("--high-cut", type=float, default=6500, help="remove hiss above this, Hz (default 6500)")
    p.add_argument("--threshold", type=float, default=0.12, help="how loud a beat must be to count, 0-1 of the loudest (default 0.12)")
    p.add_argument("--level", type=float, default=-30.0, help="RMS level of the bed in dBFS (default -30: felt more than heard)")
    p.add_argument("--seed", type=int, default=4130)
    a = p.parse_args()

    import numpy as np
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import _audio as au

    R = au.RATE
    rng = np.random.default_rng(a.seed)
    pools = ([], [])
    for src in a.sources:
        x = au.read(src, mono=True)
        env = au.smooth(np.abs(au.shape_spectrum(x, 600, None)), 0.012)
        floor = env.max() * a.threshold
        i, stop, found = int(0.05 * R), len(env) - int(0.25 * R), 0
        while i < stop:
            if env[i] > floor:
                peak = i + int(np.argmax(env[i:i + int(0.08 * R)]))
                piece = x[max(0, peak - int(0.02 * R)):peak + int(0.2 * R)]
                small = au.change_speed(piece, a.speed * (1.04 if found % 2 == 0 else 0.97))   # tick slightly higher than tock
                small = au.fade(small, 0.003, 0.025)
                small = small / (np.sqrt(np.mean(small ** 2)) + 1e-12)
                pools[found % 2].append(small)
                found += 1
                i = peak + int(0.3 * R)
            else:
                i += 1
        print(f"{os.path.basename(src)}: {found} beats found")
    if not pools[0] or not pools[1]:
        sys.exit("Not enough separate beats found. Lower --threshold, or record a cleaner source with gaps between beats.")

    n = int(a.seconds * R)
    bed = np.zeros((n, 2))
    order = [rng.permutation(len(pools[0])), rng.permutation(len(pools[1]))]
    used = [0, 0]
    for k in range(int(a.seconds * a.rate)):
        side = k % 2
        beat = pools[side][order[side][used[side] % len(pools[side])]]
        used[side] += 1
        if used[side] % len(pools[side]) == 0:
            order[side] = rng.permutation(len(pools[side]))
        level = (1.0 if side == 0 else 0.93) * au.gain(rng.uniform(-0.7, 0.7))
        at = max(0, int((k / a.rate + rng.uniform(-0.0005, 0.0005)) * R))
        end = min(n, at + len(beat))
        pan = rng.uniform(-0.04, 0.04)
        bed[at:end, 0] += beat[:end - at] * level * (1 - pan)
        bed[at:end, 1] += beat[:end - at] * level * (1 + pan)

    bed = au.shape_spectrum(bed, a.low_cut, a.high_cut, slope=2.0)
    room = np.zeros_like(bed)
    for ms, amount, swap in ((13, 0.16, False), (23, 0.10, True), (37, 0.06, False)):   # three short reflections
        d = int(ms * R / 1000)
        room[d:] += (bed[:-d, ::-1] if swap else bed[:-d]) * amount
    bed = bed + au.shape_spectrum(room, None, 4000, slope=2.0)
    bed = np.clip(bed / (np.sqrt(np.mean(bed ** 2)) + 1e-12) * au.gain(a.level), -0.95, 0.95)
    au.write(a.out, bed)
    print(f"Wrote {a.out}: {a.seconds:.1f} s at {a.rate:g} beats a second, from {len(pools[0]) + len(pools[1])} different beats")


if __name__ == "__main__":
    main()
