#!/usr/bin/env python3
"""Read every beat WAV and emit the timing manifest.

This is the ONLY place a duration is decided. Compositions read this file;
nothing downstream may hand-type a start or a length. Changing voice therefore
costs one re-run here, not a re-timing pass.

Usage: measure_beats.py <beats.json> <audio-dir> <out-manifest.json> [--gap 0.55]
"""
import argparse, json, pathlib, sys, wave


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("beats"); ap.add_argument("audio_dir"); ap.add_argument("out")
    ap.add_argument("--gap", type=float, default=0.55, help="silence appended after each beat")
    a = ap.parse_args()

    beats = json.loads(pathlib.Path(a.beats).read_text())
    audio = pathlib.Path(a.audio_dir)
    films, missing = {}, []
    for b in beats:
        p = audio / f"{b['id']}.wav"
        if not p.exists():
            missing.append(b["id"]); continue
        with wave.open(str(p)) as w:
            dur = w.getnframes() / w.getframerate()
        fid = b["id"].rsplit("-", 1)[0]
        films.setdefault(fid, []).append((b["id"], dur + a.gap))
    if missing:
        sys.exit(f"BLOCKED: {len(missing)} beat(s) have no audio: {missing[:6]}")

    man = {}
    for fid, rows in films.items():
        t, out = 0.0, []
        for i, (bid, d) in enumerate(rows):
            out.append({"i": i, "id": bid, "start": round(t, 3), "dur": round(d, 3)})
            t += d
        man[fid] = {"total": round(t, 3), "beats": out}
        print(f"{fid:<10} {t/60:5.2f} min  {len(out)} beats")
    pathlib.Path(a.out).write_text(json.dumps(man, indent=1))
    print(f"\nTOTAL {sum(v['total'] for v in man.values())/60:.1f} min -> {a.out}")


if __name__ == "__main__":
    main()
