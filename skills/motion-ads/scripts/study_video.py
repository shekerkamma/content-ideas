#!/usr/bin/env python3
"""Take a reference video apart so its style can be written down and reused.

This is the measuring half of the reverse-engineer pass. It never copies the video: it turns it
into facts you can read, so the style can be described in words and applied to a different product.

Writes into the output folder:
  shots.json   every cut, each shot's length, how much it moves, how bright it is, its main colours
  sheet.jpg    first, middle and last frame of every shot, in a row, with times
  sound.json   overall loudness, a level reading every half second, and a tempo estimate
  study.md     the numbers as a short summary, followed by the questions to answer by looking

Then read sheet.jpg and answer the questions in study.md. That answer is the style brief.

Needs: numpy, Pillow, ffmpeg, ffprobe.
"""
import argparse
import io
import json
import os
import re
import subprocess
import sys

QUESTIONS = """
## Answer these by reading sheet.jpg (one line each)

- Subject: what is on screen, and where does it sit in the frame?
- Camera: what does it do in each shot (push in, pull back, slide, orbit, hold)? Is it one move or many?
- Joins: how does each shot become the next (a match on shape, a move that carries over, a hard cut on the beat, a wipe by an object)?
- Light: how many lights, from where, hard or soft? What do the shadows do?
- Background: what is behind the subject, and is it in focus?
- Colour: the three or four colours that carry it, and what is deliberately missing.
- Text: where it sits, how it comes in and leaves, how many words at once.
- Pace: where it is fast, where it rests, what happens on the biggest beat.
- Sound: what leads (music, voice, effects)? Which moments get a sound of their own?
- The one idea: say in a sentence what makes it look expensive.

## Then write the style brief

Describe the style with no brand, product or person from the reference in it, so it can be
applied to a different subject. Do not reuse its footage, logo, music or wording.
""".lstrip("\n")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video", help="the reference video")
    p.add_argument("out", help="folder to write the study into")
    p.add_argument("--cut", type=float, default=0.30, help="how big a change counts as a cut, 0-1 (default 0.30; lower finds more)")
    p.add_argument("--max-shots", type=int, default=60, help="only the first N shots go on the sheet (default 60)")
    a = p.parse_args()

    import numpy as np
    from PIL import Image, ImageDraw, ImageFont

    os.makedirs(a.out, exist_ok=True)
    info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
                                      "-of", "json", a.video], capture_output=True, text=True, check=True).stdout)
    length = float(info["format"]["duration"])
    picture = next(s for s in info["streams"] if s["codec_type"] == "video")
    has_sound = any(s["codec_type"] == "audio" for s in info["streams"])
    num, den = picture["r_frame_rate"].split("/")
    fps = float(num) / float(den)

    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", a.video, "-an", "-vf", f"select='gt(scene,{a.cut})',showinfo", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    cuts = [0.0] + [float(t) for t in re.findall(r"pts_time:([0-9.]+)", err)] + [length]
    cuts = [c for i, c in enumerate(cuts) if i == 0 or c - cuts[i - 1] > 2.0 / fps]

    W, H = 192, 108
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf", f"fps=12,scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True).stdout
    small = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.float32)
    grey = small.mean(axis=3)

    def grab(t):
        data = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0.0, t):.3f}", "-i", a.video, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                              capture_output=True).stdout
        return Image.open(io.BytesIO(data)).convert("RGB") if data else Image.new("RGB", (16, 9))

    shots = []
    for i, (t0, t1) in enumerate(zip(cuts, cuts[1:]), 1):
        i0, i1 = int(t0 * 12), max(int(t0 * 12) + 1, int(t1 * 12))
        block, colour = grey[i0:i1], small[i0:i1]
        move = float(np.abs(block[1:] - block[:-1]).mean()) if len(block) > 1 else 0.0
        swatch = Image.fromarray(colour[len(colour) // 2].astype(np.uint8)).quantize(4).convert("RGB")
        counts = sorted(swatch.getcolors(W * H), reverse=True)
        shots.append({
            "shot": i, "start": round(t0, 2), "end": round(t1, 2), "seconds": round(t1 - t0, 2),
            "motion": "still" if move < 1 else ("slow" if move < 4 else ("moving" if move < 10 else "fast")), "motion_value": round(move, 2),
            "brightness": round(float(block.mean()) / 255, 2),
            "colours": ["#%02x%02x%02x" % c for _, c in counts],
        })
    json.dump({"seconds": round(length, 2), "fps": round(fps, 2), "size": [picture["width"], picture["height"]], "shots": shots},
              open(os.path.join(a.out, "shots.json"), "w"), indent=1)

    def font(size):
        for name in ("/System/Library/Fonts/Helvetica.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "arial.ttf"):
            try:
                return ImageFont.truetype(name, size)
            except OSError:
                continue
        return ImageFont.load_default()

    shown = shots[:a.max_shots]
    tw = 360
    th = round(tw * picture["height"] / picture["width"])
    gap, label = 6, 24
    sheet = Image.new("RGB", (gap + 3 * (tw + gap), gap + len(shown) * (th + label + gap)), (24, 24, 24))
    draw, face = ImageDraw.Draw(sheet), font(16)
    for row, s in enumerate(shown):
        y = gap + row * (th + label + gap)
        edge = min(0.08, s["seconds"] / 4)
        for col, t in enumerate((s["start"] + edge, (s["start"] + s["end"]) / 2, s["end"] - edge)):
            sheet.paste(grab(t).resize((tw, th), Image.LANCZOS), (gap + col * (tw + gap), y))
        draw.text((gap + 2, y + th + 3), f"shot {s['shot']}   {s['start']:.2f}-{s['end']:.2f} s   {s['seconds']:.2f} s   {s['motion']}", fill=(235, 235, 235), font=face)
    sheet.save(os.path.join(a.out, "sheet.jpg"), quality=86)

    sound = {"has_sound": has_sound}
    if has_sound:
        mono = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vn", "-ac", "1", "-ar", "22050", "-f", "f32le", "-"],
                                            capture_output=True).stdout, np.float32).astype(np.float64)
        hop = 22050 // 2
        sound["level_every_half_second_db"] = [round(float(20 * np.log10(np.sqrt(np.mean(mono[i:i + hop] ** 2)) + 1e-9)), 1)
                                               for i in range(0, max(1, len(mono) - hop + 1), hop)]
        frame = 512
        energy = np.array([np.sum(mono[i:i + frame] ** 2) for i in range(0, len(mono) - frame, frame)])
        onset = np.maximum(np.diff(np.log(energy + 1e-9)), 0)
        onset = onset - onset.mean()
        if len(onset) > 200 and onset.std() > 0:
            corr = np.correlate(onset, onset, "full")[len(onset) - 1:]
            per_second = 22050 / frame
            lags = np.arange(int(per_second * 60 / 180), min(len(corr) - 1, int(per_second * 60 / 60)))
            if len(lags):
                best = lags[int(np.argmax(corr[lags]))]
                sound["tempo_bpm_estimate"] = round(60 * per_second / best)
        err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", a.video, "-vn", "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                             capture_output=True, text=True).stderr
        if "{" in err:
            m = json.loads(err[err.rindex("{"): err.rindex("}") + 1])
            sound["lufs"], sound["true_peak_db"] = float(m["input_i"]), float(m["input_tp"])
    json.dump(sound, open(os.path.join(a.out, "sound.json"), "w"), indent=1)

    lengths = [s["seconds"] for s in shots]
    lines = [f"# Study of {os.path.basename(a.video)}", "",
             f"- Length {length:.1f} s, {picture['width']} x {picture['height']}, {fps:.0f} fps",
             f"- {len(shots)} shots. Average {np.mean(lengths):.2f} s, shortest {min(lengths):.2f} s, longest {max(lengths):.2f} s",
             "- " + ("One continuous shot: no cuts found. Look for hidden joins on the sheet." if len(shots) == 1 else
                     f"Cuts at: {', '.join(f'{c:.2f}' for c in cuts[1:-1])} s")]
    if has_sound:
        lines.append(f"- Sound: {sound.get('lufs', '?')} LUFS, tempo estimate {sound.get('tempo_bpm_estimate', '?')} BPM (an estimate: check it against the cuts)")
    else:
        lines.append("- No sound in the file")
    lines += ["", "| Shot | Time | Length | Motion | Brightness | Colours |", "|---|---|---|---|---|---|"]
    lines += [f"| {s['shot']} | {s['start']:.2f}-{s['end']:.2f} | {s['seconds']:.2f} s | {s['motion']} | {s['brightness']} | {' '.join(s['colours'])} |" for s in shots]
    open(os.path.join(a.out, "study.md"), "w").write("\n".join(lines) + "\n\n" + QUESTIONS)
    print(f"{len(shots)} shots, average {np.mean(lengths):.2f} s. Wrote shots.json, sheet.jpg, sound.json and study.md to {a.out}/")
    print("Next: read sheet.jpg and answer the questions in study.md.")


if __name__ == "__main__":
    main()
