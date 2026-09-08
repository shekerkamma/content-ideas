#!/usr/bin/env python3
"""One WAV per beat, synthesised locally with Kokoro. No API, no quota.

Loads the ONNX model once and generates every beat, which is why this exists
instead of shelling out to a CLI per beat.

Usage: tts_beats.py <beats.json> <out-dir> [--voice bm_george] [--lang en-gb]
  beats.json: [{"id": "uc01-00", "vo": "..."}, ...]
"""
import argparse, json, pathlib, sys, time

CACHE = pathlib.Path.home() / ".cache/hyperframes/tts"
MODEL = CACHE / "models/kokoro-v1.0.onnx"
VOICES = CACHE / "voices/voices-v1.0.bin"
MODEL_BYTES = 325532387


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("beats"); ap.add_argument("out_dir")
    ap.add_argument("--voice", default="bm_george")
    ap.add_argument("--lang", default="en-gb")
    ap.add_argument("--model", default=str(MODEL))
    ap.add_argument("--voices", default=str(VOICES))
    a = ap.parse_args()

    model = pathlib.Path(a.model)
    if not model.exists():
        sys.exit(f"BLOCKED: model missing at {model}. See SKILL.md Setup.")
    size = model.stat().st_size
    if size != MODEL_BYTES:
        # A truncated ONNX fails deep inside the runtime with an opaque error.
        sys.exit(f"BLOCKED: model is {size} bytes, expected {MODEL_BYTES}. "
                 "Resume the download with curl -C - and do not wrap it in a short timeout.")

    from kokoro_onnx import Kokoro
    import soundfile as sf

    beats = json.loads(pathlib.Path(a.beats).read_text())
    out = pathlib.Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    k = Kokoro(str(model), a.voices)

    t0, total = time.time(), 0.0
    for b in beats:
        samples, sr = k.create(b["vo"], voice=a.voice, speed=1.0, lang=a.lang)
        sf.write(str(out / f"{b['id']}.wav"), samples, sr)
        d = len(samples) / sr; total += d
        print(f"{b['id']} {d:6.2f}s", flush=True)
    print(f"\n{len(beats)} beats, {total/60:.1f} min speech, in {(time.time()-t0)/60:.1f} min")


if __name__ == "__main__":
    main()
