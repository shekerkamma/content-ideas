"""Shared audio helpers for the scripts in this folder. Needs numpy and ffmpeg on PATH.

Audio is held as float64 numpy arrays shaped (samples, 2) at 48 kHz.
Reading and writing go through ffmpeg, so any format ffmpeg knows works.
"""
import subprocess

import numpy as np

RATE = 48000


def gain(db):
    """Decibels to a linear multiplier."""
    return 10.0 ** (db / 20.0)


def level_db(x):
    """RMS level of a block in dBFS."""
    return 20.0 * np.log10(np.sqrt(np.mean(np.square(x)) + 1e-20))


def read(path, mono=False):
    """Decode any audio or video file to a float array at 48 kHz."""
    channels = 1 if mono else 2
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", str(channels), "-ar", str(RATE), "-f", "f64le", "-"],
        capture_output=True, check=True,
    ).stdout
    data = np.frombuffer(raw, dtype=np.float64)
    return data.copy() if mono else data.reshape(-1, 2).copy()


def write(path, x):
    """Write a float array as a 24-bit 48 kHz WAV."""
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        x = np.column_stack([x, x])
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-f", "f64le", "-ar", str(RATE), "-ac", "2", "-i", "-", "-c:a", "pcm_s24le", str(path)],
        input=np.ascontiguousarray(x).tobytes(), check=True,
    )


def stereo(x):
    return x if x.ndim == 2 else np.column_stack([x, x])


def shape_spectrum(x, low_cut=None, high_cut=None, slope=4.0):
    """Roll off below `low_cut` Hz and above `high_cut` Hz with a smooth slope (zero phase)."""
    if low_cut is None and high_cut is None:
        return x
    n = x.shape[0]
    spec = np.fft.rfft(x, axis=0)
    freq = np.fft.rfftfreq(n, 1.0 / RATE)
    curve = np.ones_like(freq)
    if low_cut:
        curve *= 1.0 / np.sqrt(1.0 + (low_cut / np.maximum(freq, 1e-6)) ** (2 * slope))
    if high_cut:
        curve *= 1.0 / np.sqrt(1.0 + (freq / high_cut) ** (2 * slope))
    if x.ndim == 2:
        curve = curve[:, None]
    return np.fft.irfft(spec * curve, n=n, axis=0)


def fade(x, fade_in=0.0, fade_out=0.0):
    """Raised-cosine fades at the two ends, in seconds."""
    x = x.copy()
    a, b = int(fade_in * RATE), int(fade_out * RATE)
    if a > 1:
        ramp = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, min(a, len(x))))
        x[: len(ramp)] = (x[: len(ramp)].T * ramp).T
    if b > 1:
        ramp = 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, min(b, len(x))))
        x[-len(ramp):] = (x[-len(ramp):].T * ramp).T
    return x


def change_speed(x, rate):
    """Play faster (rate > 1) or slower. Pitch moves with speed, like tape."""
    if abs(rate - 1.0) < 1e-6:
        return x
    n = max(2, int(len(x) / rate))
    pos = np.arange(n) * rate
    lo = np.minimum(np.floor(pos).astype(int), len(x) - 1)
    hi = np.minimum(lo + 1, len(x) - 1)
    t = pos - lo
    if x.ndim == 2:
        t = t[:, None]
    return x[lo] * (1 - t) + x[hi] * t


def smooth(values, seconds):
    """Moving average over a window, used for level envelopes."""
    w = max(1, int(seconds * RATE))
    kernel = np.ones(w) / w
    return np.convolve(values, kernel, mode="same")


def loudness(path):
    """Integrated loudness, true peak and range of a file, measured by ffmpeg's loudnorm."""
    import json
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vn", "-af", "loudnorm=print_format=json", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    block = err[err.rindex("{"): err.rindex("}") + 1]
    d = json.loads(block)
    return {"lufs": float(d["input_i"]), "true_peak": float(d["input_tp"]), "range": float(d["input_lra"]),
            "threshold": float(d["input_thresh"]), "offset": float(d["target_offset"])}
