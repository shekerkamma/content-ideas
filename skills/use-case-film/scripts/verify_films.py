#!/usr/bin/env python3
"""Delivery gate for rendered films.

Three checks, each of which exists because its absence produced a green run
over a broken artifact:

  1. Rendered duration matches the manifest. Proves the derived-timing chain
     held end to end rather than silently falling back somewhere.
  2. Both streams present AND the audio carries content. A stream that exists
     can still be silence, so the level is compared against a generated silent
     control (anullsrc measures about -91 dB) rather than an arbitrary cutoff.
  3. The file is complete. A partial mux is a valid file that stops short, so
     never trust presence alone.

Exit 0 clean, 1 blocked (cannot measure), 2 findings.

Usage: verify_films.py <renders-dir> <manifest.json> [--tolerance 1.5]
"""
import argparse, json, pathlib, re, shutil, subprocess, sys, tempfile

def ffprobe(path, entries, stream=None):
    cmd = ["ffprobe", "-v", "error"]
    if stream: cmd += ["-select_streams", stream]
    cmd += ["-show_entries", entries, "-of", "csv=p=0", str(path)]
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()

def mean_volume(path):
    # NOTE: no -v error here. It would suppress the volumedetect output entirely.
    r = subprocess.run(["ffmpeg", "-i", str(path), "-af", "volumedetect", "-f", "null", "/dev/null"],
                       capture_output=True, text=True)
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stderr)
    return float(m.group(1)) if m else None

def silence_floor():
    """Generate a silent file and measure it, so the threshold is derived not guessed."""
    if not shutil.which("ffmpeg"): return None
    with tempfile.NamedTemporaryFile(suffix=".m4a", delete=False) as f:
        p = f.name
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                    "-t", "2", "-c:a", "aac", "-y", p], capture_output=True)
    v = mean_volume(p)
    pathlib.Path(p).unlink(missing_ok=True)
    return v

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("renders"); ap.add_argument("manifest")
    ap.add_argument("--tolerance", type=float, default=1.5, help="seconds of drift allowed")
    a = ap.parse_args()

    if not shutil.which("ffprobe"):
        print("BLOCKED: ffprobe not found — films UNMEASURED", file=sys.stderr); return 1

    man = json.loads(pathlib.Path(a.manifest).read_text())
    floor = silence_floor()
    if floor is None:
        print("BLOCKED: could not measure a silence control", file=sys.stderr); return 1
    print(f"silence control measures {floor:.1f} dB\n")

    findings = []
    files = sorted(pathlib.Path(a.renders).glob("*.mp4"))
    if not files:
        print("BLOCKED: no films found", file=sys.stderr); return 1

    for f in files:
        fid = next((k for k in man if k in f.name), None)
        dur = ffprobe(f, "format=duration")
        dur = float(dur) if dur else 0.0
        types = set(ffprobe(f, "stream=codec_type").splitlines())
        vol = mean_volume(f)
        row = [f"{f.name:<32} {dur:7.1f}s"]

        if fid is None:
            findings.append(f"{f.name}: no manifest entry — cannot verify duration")
        else:
            want = man[fid]["total"]
            drift = abs(dur - want)
            row.append(f"want {want:.1f}s drift {drift:+.2f}s")
            if drift > a.tolerance:
                findings.append(f"{f.name}: duration {dur:.1f}s vs manifest {want:.1f}s (drift {drift:.2f}s)")
        if "video" not in types: findings.append(f"{f.name}: no video stream")
        if "audio" not in types:
            findings.append(f"{f.name}: no audio stream")
        elif vol is None:
            findings.append(f"{f.name}: audio level unmeasurable")
        elif vol <= floor + 20:
            findings.append(f"{f.name}: audio at {vol:.1f} dB is within 20 dB of silence ({floor:.1f} dB)")
        else:
            row.append(f"audio {vol:.1f} dB")
        print("  " + "  ".join(row))

    if findings:
        print(f"\n{len(findings)} finding(s):", file=sys.stderr)
        for x in findings: print(f"  - {x}", file=sys.stderr)
        return 2
    print(f"\nall {len(files)} film(s) clean")
    return 0

if __name__ == "__main__":
    sys.exit(main())
