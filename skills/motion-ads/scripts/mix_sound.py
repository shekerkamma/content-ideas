#!/usr/bin/env python3
"""Mix music, voice and effects onto the picture's own beats, from one cue sheet.

Every cue names a beat (an event from the picture) or a time in seconds, so when the picture is
re-timed the sound follows. The script places each sound, ducks the music under the voice and under
the effects you mark, and writes the mix plus one stem per layer. It then prints how far each cue
landed from its beat and how loud each layer is.

Cue sheet (JSON):
{
  "length": 20.0,                         seconds, or the name of an event such as "end"
  "music": {
    "file": "music/take1.mp3",
    "gain_db": 0, "start": 0.0,           "start" skips into the file (to sit on a bar line)
    "fade_in": 0.6, "fade_out": 0.9,
    "duck_under_voice_db": 8,             music drops this much while the voice talks
    "ducks":  [{"at": "click", "before": 0.1, "after": 0.2, "depth_db": 4}],
    "levels": [[0, 6], [4.8, 0], ["reveal", 1.5]]      a gain curve in dB over time
  },
  "voice":   [{"file": "vo/line-01.wav", "at": 0.5, "gain_db": 0}],
  "effects": [{"file": "sounds/soft-thud.wav", "at": "reveal", "shift": -0.2, "align": "peak",
               "gain_db": -12, "speed": 0.9, "pan": 0.0, "low_cut": 80, "high_cut": 6000,
               "fade_in": 0, "fade_out": 0, "until": "end"}]
}
"align" says which part of the sound sits on the beat: "start" (default), "peak" or "end".
"until" turns a sound into a bed: it is looped or trimmed to run from "at" to that beat.

Events file (--events): {"name": seconds, ...} or [{"name": ..., "t": seconds}, ...].
Needs: numpy, ffmpeg. Master the result with master_audio.py.
"""
import argparse
import json
import os
import sys


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cues", help="the cue sheet (JSON)")
    p.add_argument("out", help="the mix to write, e.g. sound/mix.wav (stems are written next to it)")
    p.add_argument("--events", help="JSON file of named beats from the picture")
    p.add_argument("--root", help="folder that file paths in the cue sheet are relative to (default: the cue sheet's folder)")
    a = p.parse_args()

    import numpy as np
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import _audio as au

    R = au.RATE
    sheet = json.load(open(a.cues))
    root = a.root or os.path.dirname(os.path.abspath(a.cues))
    events = {}
    if a.events:
        raw = json.load(open(a.events))
        events = {e["name"]: float(e["t"]) for e in raw} if isinstance(raw, list) else {k: float(v) for k, v in raw.items()}

    def when(value):
        if isinstance(value, (int, float)):
            return float(value)
        if value not in events:
            sys.exit(f"Cue points at the beat '{value}', which is not in the events file. Known beats: {sorted(events)}")
        return events[value]

    def path(name):
        return name if os.path.isabs(name) else os.path.join(root, name)

    total = int(round(when(sheet["length"]) * R))
    time = np.arange(total) / R

    def place(layer, sound, start):
        a0, b0 = max(0, start), min(total, start + len(sound))
        if b0 > a0:
            layer[a0:b0] += sound[a0 - start:b0 - start]

    # voice
    voice = np.zeros((total, 2))
    for line in sheet.get("voice", []):
        x = au.read(path(line["file"])) * au.gain(line.get("gain_db", 0))
        place(voice, au.fade(x, 0.01, 0.04), int(round(when(line["at"]) * R)))

    # effects
    effects = np.zeros((total, 2))
    report, uses = [], {}
    for cue in sheet.get("effects", []):
        x = au.read(path(cue["file"]))
        x = au.change_speed(x, cue.get("speed", 1.0))
        x = au.shape_spectrum(x, cue.get("low_cut"), cue.get("high_cut"))
        target = when(cue["at"]) + cue.get("shift", 0.0)
        if "until" in cue:
            need = max(1, int(round((when(cue["until"]) - target) * R)))
            while len(x) < need:                                   # loop with a short crossfade
                lap = min(int(0.5 * R), len(x) // 4)
                tail, head = x[-lap:] * np.linspace(1, 0, lap)[:, None], x[:lap] * np.linspace(0, 1, lap)[:, None]
                x = np.concatenate([x[:-lap], tail + head, x[lap:]])
            x = x[:need]
        x = au.fade(x, cue.get("fade_in", 0.0), cue.get("fade_out", 0.0))
        pan = cue.get("pan", 0.0)
        x = x * au.gain(cue.get("gain_db", 0)) * np.array([min(1.0, 1 - pan), min(1.0, 1 + pan)])
        mode = cue.get("align", "start")
        anchor = {"start": 0, "end": len(x), "peak": int(np.argmax(np.abs(x).sum(axis=1)))}[mode]
        start = int(round(target * R)) - anchor
        place(effects, x, start)
        report.append((cue["file"], cue["at"], target, (start + anchor) / R, mode))
        if "until" not in cue:
            uses[cue["file"]] = uses.get(cue["file"], 0) + 1

    # music
    music = np.zeros((total, 2))
    spec = sheet.get("music")
    if spec:
        x = au.read(path(spec["file"]))[int(spec.get("start", 0.0) * R):]
        x = np.concatenate([x, np.zeros((max(0, total - len(x)), 2))])[:total]
        curve = np.zeros(total)
        if spec.get("levels"):
            pts = sorted((when(t), float(db)) for t, db in spec["levels"])
            curve += np.interp(time, [q[0] for q in pts], [q[1] for q in pts])
        for duck in spec.get("ducks", []):
            t0 = when(duck["at"])
            window = ((time >= t0 - duck.get("before", 0.1)) & (time <= t0 + duck.get("after", 0.2))).astype(float)
            curve -= au.smooth(window, 0.06) * duck.get("depth_db", 4)
        under = spec.get("duck_under_voice_db", 0)
        if under and np.abs(voice).max() > 0:
            talking = (au.smooth(np.abs(voice).sum(axis=1), 0.03) > au.gain(-42)).astype(float)
            held = np.minimum(1.0, au.smooth(talking, 0.35) * 2.0)      # quick down, slow back up
            curve -= np.maximum(au.smooth(talking, 0.06), held) * under
        x = x * au.gain(spec.get("gain_db", 0)) * au.gain(curve)[:, None]
        music = au.fade(x, spec.get("fade_in", 0.0), spec.get("fade_out", 0.0))

    mix = music + voice + effects
    stem = os.path.splitext(a.out)[0]
    au.write(a.out, mix)
    for name, layer in (("music", music), ("voice", voice), ("effects", effects)):
        if np.abs(layer).max() > 0:
            au.write(f"{stem}-{name}.wav", layer)

    print("Cue                              beat             wanted    landed    off")
    for name, beat, wanted, landed, mode in report:
        print(f"{os.path.basename(name)[:32]:32s} {str(beat)[:14]:14s} {wanted:8.3f}  {landed:8.3f}  {(landed - wanted) * 1000:+5.1f} ms ({mode})")
    print()
    for name, layer in (("music", music), ("voice", voice), ("effects", effects), ("mix", mix)):
        if np.abs(layer).max() > 0:
            print(f"{name:8s} level {au.level_db(layer):6.1f} dBFS   peak {20 * np.log10(np.abs(layer).max()):6.1f} dBFS")
    if np.abs(mix).max() > 1.0:
        print("NOTE: the mix peaks above full scale. That is fine before mastering: master_audio.py brings it down.")
    for name, count in uses.items():
        if count > 2:
            print(f"CHECK: '{os.path.basename(name)}' plays {count} times. A sound repeated on every move reads as robotic; use it once or vary the source.")
    if spec and np.abs(effects).max() > 0 and au.level_db(effects) > au.level_db(music):
        print("CHECK: the effects are louder than the music. For an ad, let the music lead and keep effects underneath.")
    print(f"Wrote {a.out} ({total / R:.2f} s)")


if __name__ == "__main__":
    main()
