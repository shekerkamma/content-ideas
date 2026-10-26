#!/usr/bin/env python3
"""Output checks for gemini-media-lane. Stdlib only; shells out to ffprobe/ffmpeg/tesseract.

  check_media.py wav FILE                       one RIFF header, size field = file - 8, readable
  check_media.py av FILE [--duration S] [--min-duration S]
                                                duration, audio present, loudness, no long silence
  check_media.py ocr IMAGE "LINE" ["LINE" ...]  every expected line read exactly by Tesseract
                                                (native, or the WSL build via wsl.exe on Windows)

Exit 0 = pass, 1 = check failed, 2 = usage or a missing tool.
"""
from __future__ import annotations
import argparse, os, re, shutil, struct, subprocess, sys, wave
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
# Inside WSL, relative to $HOME: the repo-local build the Windows copies of this skill borrow.
WSL_TESSERACT = os.environ.get("WSL_TESSERACT", "$HOME/content-ideas/.tools/tesseract/bin/tesseract")


def find_tesseract() -> tuple[list[str], str] | None:
    """argv prefix that reads an image path and prints its text, plus a label. None if none found.

    Order: TESSERACT_BIN, the repo-local build, PATH, standard Windows installs, then (on
    Windows) the WSL repo build through wsl.exe, so a Windows copy needs no install.
    """
    candidates = [os.environ.get("TESSERACT_BIN"), str(REPO / ".tools/tesseract/bin/tesseract"),
                  shutil.which("tesseract")]
    if os.name == "nt":
        for base in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)"),
                     os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs")):
            if base:
                candidates.append(os.path.join(base, "Tesseract-OCR", "tesseract.exe"))
    for c in candidates:
        if c and Path(c).is_file():
            return [c], c
    wsl = shutil.which("wsl.exe") or shutil.which("wsl")
    if os.name == "nt" and wsl:
        probe = subprocess.run([wsl, "-e", "sh", "-c", f'test -x "{WSL_TESSERACT}"'], capture_output=True)
        if probe.returncode == 0:
            # wslpath turns the Windows image path into a WSL one inside the same call.
            return [wsl, "-e", "sh", "-c", f'exec "{WSL_TESSERACT}" "$(wslpath -a "$1")" "$2" "$3" "$4"', "_"], \
                f"wsl.exe → {WSL_TESSERACT}"
    return None


def fail(msg: str) -> int:
    print(f"FAIL {msg}")
    return 1


def check_wav(path: str) -> int:
    b = Path(path).read_bytes()
    if not b.startswith(b"RIFF") or b[8:12] != b"WAVE":
        return fail(f"{path}: not a RIFF/WAVE file")
    if b.count(b"RIFF") != 1:
        return fail(f"{path}: {b.count(b'RIFF')} RIFF headers (double-wrapped)")
    if struct.unpack("<I", b[4:8])[0] != len(b) - 8:
        return fail(f"{path}: RIFF size field does not match the file length")
    with wave.open(path) as w:
        dur = w.getnframes() / w.getframerate()
        print(f"PASS {path}: {w.getframerate()} Hz, {w.getnchannels()} ch, {dur:.2f} s")
    return 0


def _probe(path: str) -> tuple[float, bool]:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
                          "-of", "default=nw=1", path], capture_output=True, text=True, check=True).stdout
    dur = float(re.search(r"duration=([\d.]+)", out).group(1))
    return dur, "codec_type=audio" in out


def check_av(path: str, duration: float | None, min_duration: float | None) -> int:
    dur, has_audio = _probe(path)
    if duration is not None and abs(dur - duration) > 0.25:
        return fail(f"{path}: duration {dur:.2f} s, expected {duration} s")
    if min_duration is not None and dur < min_duration:
        return fail(f"{path}: duration {dur:.2f} s, under {min_duration} s")
    if not has_audio:
        return fail(f"{path}: no audio stream")
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-vn", "-af",
                          "volumedetect,silencedetect=noise=-45dB:d=2", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    mean = float(re.search(r"mean_volume: (-?[\d.]+) dB", log).group(1))
    gaps = len(re.findall(r"silence_start", log))
    if mean < -30:
        return fail(f"{path}: mean volume {mean} dB (too quiet or silent)")
    if gaps:
        return fail(f"{path}: {gaps} silent gap(s) longer than 2 s")
    print(f"PASS {path}: {dur:.2f} s, audio mean {mean} dB, no silent gaps")
    return 0


def check_ocr(path: str, expected: list[str]) -> int:
    found = find_tesseract()
    if not found:
        print("tesseract not found (TESSERACT_BIN, repo .tools, PATH, Program Files, or WSL via wsl.exe)")
        return 2
    argv, label = found
    text = subprocess.run(argv + [str(Path(path).resolve()), "-", "--psm", "11"],
                          capture_output=True, text=True).stdout
    if not text.strip():
        print(f"tesseract ({label}) returned no text for {path}")
        return 1
    norm = lambda s: " ".join(s.split()).lower()
    seen = norm(text)
    missing = [e for e in expected if norm(e) not in seen]
    if missing:
        return fail(f"{path}: OCR did not find {missing}; read: {' | '.join(l for l in text.splitlines() if l.strip())[:300]}")
    print(f"PASS {path}: OCR found {expected}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("wav").add_argument("file")
    a = sub.add_parser("av"); a.add_argument("file")
    a.add_argument("--duration", type=float); a.add_argument("--min-duration", type=float)
    o = sub.add_parser("ocr"); o.add_argument("file"); o.add_argument("expected", nargs="+")
    args = ap.parse_args()
    if not Path(args.file).exists():
        print(f"no such file: {args.file}")
        return 2
    if args.cmd == "wav":
        return check_wav(args.file)
    if args.cmd == "av":
        return check_av(args.file, args.duration, args.min_duration)
    return check_ocr(args.file, args.expected)


if __name__ == "__main__":
    sys.exit(main())
