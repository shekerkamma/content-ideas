#!/usr/bin/env python3
"""Make a small kit of sound effects with code. Nothing is downloaded and nothing is paid for.

Every sound is built from sine waves and filtered noise, so the kit is free to use anywhere.
Use it for Level 1 (code-only ads), or as quiet support under generated music.

Sounds written (48 kHz stereo WAV):
  air-pass-slow / air-pass-fast   soft airy passes for a camera move
  soft-thud                       a low, round hit for a landing or a reveal
  blip                            a small pop for something lifting off or snapping in
  tick                            one tiny click
  rise                            a quiet build that ends on a beat (align its END to the beat)
  grain-rustle-1..3               dry sand-like grains, for particles, ink, dust, paper
  sub-swell                       a low swell under a logo or end card
  pad                             a slow, soft three-chord bed (a home-made music bed)
  room                            near-silent room air, so the track is never digital silence

Needs: numpy, ffmpeg.
"""
import argparse
import os
import sys


def build(folder, seconds, seed):
    import numpy as np
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import _audio as au

    R = au.RATE
    rng = np.random.default_rng(seed)

    def noise(n):
        return rng.standard_normal((n, 2))

    def normal(x, peak=0.9):
        return x / (np.abs(x).max() + 1e-12) * peak

    def bell(t, centre, width):
        return np.exp(-(((t - centre) / width) ** 2))

    def air_pass(length, bright):
        # Three bands of noise take turns, low to high and back, so it reads as something moving past.
        n = int(length * R)
        t = np.linspace(0, 1, n)
        src = noise(n)
        out = np.zeros((n, 2))
        bands = [(180, 700, 0.30), (600, 2400 * bright, 0.48), (2000 * bright, 7000 * bright, 0.62)]
        for lo, hi, centre in bands:
            out += au.shape_spectrum(src, lo, hi) * bell(t, centre, 0.22)[:, None]
        out *= (np.sin(np.pi * t) ** 1.6)[:, None]
        out[:, 1] = np.roll(out[:, 1], int(0.004 * R))          # a few milliseconds of width
        return normal(out, 0.8)

    def soft_thud():
        n = int(1.6 * R)
        t = np.arange(n) / R
        pitch = 46 + 38 * np.exp(-t / 0.035)                     # drops quickly to a low note
        body = np.sin(2 * np.pi * np.cumsum(pitch) / R) * np.exp(-t / 0.33)
        puff = au.shape_spectrum(noise(n), 120, 900)[:, 0] * np.exp(-t / 0.05) * 0.25
        mono = (body + puff) * np.minimum(t / 0.004, 1)
        return normal(np.column_stack([mono, mono]))

    def blip():
        n = int(0.18 * R)
        t = np.arange(n) / R
        pitch = 420 + 520 * np.exp(-t / 0.012)
        mono = np.sin(2 * np.pi * np.cumsum(pitch) / R) * np.exp(-t / 0.028) * np.minimum(t / 0.001, 1)
        return normal(np.column_stack([mono, mono]), 0.8)

    def tick():
        n = int(0.06 * R)
        t = np.arange(n) / R
        click = au.shape_spectrum(noise(n), 1800, 9000)[:, 0] * np.exp(-t / 0.004)
        ring = np.sin(2 * np.pi * 3100 * t) * np.exp(-t / 0.009) * 0.5
        mono = click + ring
        return normal(np.column_stack([mono, mono]), 0.7)

    def rise():
        n = int(2.4 * R)
        t = np.linspace(0, 1, n)
        src = noise(n)
        out = np.zeros((n, 2))
        for k, (lo, hi) in enumerate([(300, 900), (800, 2400), (2200, 6000), (5000, 11000)]):
            out += au.shape_spectrum(src, lo, hi) * bell(t, 0.25 + 0.25 * k, 0.26)[:, None]
        tone = np.sin(2 * np.pi * np.cumsum(220 * 2 ** (t * 1.0)) / R) * 0.12
        out += tone[:, None]
        out *= (t ** 2.2)[:, None]
        out[-int(0.012 * R):] *= np.linspace(1, 0, int(0.012 * R))[:, None]   # stops dead on the beat
        return normal(out, 0.8)

    def grain_rustle(variant):
        # Thousands of very short grains. Most arrive early, then a long thinning tail:
        # the same shape as particles that leave fast and settle slowly.
        local = np.random.default_rng(seed + 100 + variant)
        n = int(1.5 * R)
        t = np.arange(n) / n
        density = bell(t, 0.36, 0.20) + 0.25 * bell(t, 0.70, 0.18)
        out = np.zeros((n, 2))
        usable = n - 600
        weights = density[:usable] / density[:usable].sum()
        for ch in range(2):
            grains = np.zeros(n)
            for start in local.choice(usable, size=5200, p=weights):
                size = int(local.integers(40, 220))
                grains[start:start + size] += local.standard_normal(size) * np.hanning(size) * local.uniform(0.2, 1.0)
            dry = au.shape_spectrum(grains, 2200, 9500) * 0.9 + au.shape_spectrum(grains, 900, 2400) * 0.35
            out[:, ch] = dry * (0.15 + density / density.max())
        return normal(out)

    def sub_swell():
        n = int(3.2 * R)
        t = np.arange(n) / R
        env = np.minimum(t / 0.9, 1) ** 2 * np.exp(-np.maximum(t - 0.9, 0) / 0.9)
        mono = (np.sin(2 * np.pi * 55 * t) + 0.35 * np.sin(2 * np.pi * 110 * t + 0.4)) * env
        return normal(np.column_stack([mono, np.roll(mono, 9)]))

    def pad(length):
        # Three slow chords that overlap: D sus2, G major 7, D major. The last one lands on the end card.
        n = int(length * R)
        t = np.arange(n) / R
        out = np.zeros((n, 2))
        third = length / 3.0
        chords = [
            ([73.42, 110.0, 146.83, 220.0, 329.63], -3.0, third + 3.5),
            ([98.0, 146.83, 196.0, 293.66, 369.99], third, 2 * third + 1.5),
            ([73.42, 146.83, 220.0, 293.66, 369.99, 440.0], 2 * third - 1.2, length + 3.0),
        ]
        for notes, start, stop in chords:
            env = np.clip((t - start) / 3.0, 0, 1) * np.clip((stop - t) / 3.5, 0, 1)
            env = env * env * (3 - 2 * env)
            for i, f in enumerate(notes):
                for detune, pan in ((-0.18, 0.3), (0.21, 0.7)):
                    phase = 2 * np.pi * f * (1 + detune / 100) * t + i * 1.7 + detune * 9
                    wave = np.sin(phase) + 0.22 * np.sin(2 * phase + 0.5) + 0.08 * np.sin(3 * phase)
                    wave *= (1 + 0.12 * np.sin(2 * np.pi * (0.11 + 0.03 * i) * t + i)) / (1 + i * 0.35)
                    out[:, 0] += wave * env * (1 - pan)
                    out[:, 1] += wave * env * pan
        return normal(au.shape_spectrum(out, None, 1800), 0.7)

    def room(length):
        n = int(length * R)
        return normal(au.shape_spectrum(noise(n), 60, 1400, slope=1.5), 0.25)

    kit = {
        "air-pass-slow": air_pass(2.2, 0.8),
        "air-pass-fast": air_pass(0.9, 1.25),
        "soft-thud": soft_thud(),
        "blip": blip(),
        "tick": tick(),
        "rise": rise(),
        "grain-rustle-1": grain_rustle(1),
        "grain-rustle-2": grain_rustle(2),
        "grain-rustle-3": grain_rustle(3),
        "sub-swell": sub_swell(),
        "pad": pad(seconds),
        "room": room(seconds),
    }
    os.makedirs(folder, exist_ok=True)
    for name, sound in kit.items():
        au.write(os.path.join(folder, name + ".wav"), sound)
        print(f"{name + '.wav':22s} {len(sound) / R:5.2f} s")
    print(f"Wrote {len(kit)} sounds to {folder}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("folder", help="where to write the WAV files, e.g. sounds/")
    p.add_argument("--seconds", type=float, default=18.0, help="length of the pad and room beds (default 18: make it at least as long as the ad)")
    p.add_argument("--seed", type=int, default=7, help="change it to get different noise-based sounds (default 7)")
    a = p.parse_args()
    build(a.folder, a.seconds, a.seed)


if __name__ == "__main__":
    main()
