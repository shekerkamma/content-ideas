#!/usr/bin/env python3
"""Lay frames of a video, or a folder of stills, out on one labelled sheet for review.

Claude cannot watch a video play. It can read one image with many frames on it. Make a sheet,
read it, fix what is wrong, and only then show the result.

  frame_sheet.py ad.mp4 review.jpg                    about 20 frames across the whole video
  frame_sheet.py ad.mp4 review.jpg --every 0.5        one frame every half second
  frame_sheet.py ad.mp4 join.jpg --from 2.8 --to 3.2 --every 0.04    every frame around a join
  frame_sheet.py stills/ review.jpg                   every image in a folder, by name

A sheet hides small faults. For sharpness, small text and shimmer, also look at single frames at
full size (--full writes them next to the sheet).

Needs: Pillow, ffmpeg, ffprobe.
"""
import argparse
import os
import subprocess
import sys


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source", help="a video file, or a folder of images")
    p.add_argument("out", help="the sheet to write (.jpg or .png)")
    p.add_argument("--every", type=float, help="seconds between frames (default: spread about 20 frames over the video)")
    p.add_argument("--from", dest="start", type=float, default=0.0, help="start time in seconds")
    p.add_argument("--to", dest="stop", type=float, help="end time in seconds")
    p.add_argument("--columns", type=int, default=5)
    p.add_argument("--width", type=int, default=480, help="width of each frame on the sheet in pixels (default 480)")
    p.add_argument("--full", action="store_true", help="also save each frame at full size in a folder next to the sheet")
    a = p.parse_args()

    from PIL import Image, ImageDraw, ImageFont

    def font(size):
        for name in ("/System/Library/Fonts/Helvetica.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "arial.ttf"):
            try:
                return ImageFont.truetype(name, size)
            except OSError:
                continue
        return ImageFont.load_default()

    tiles = []
    if os.path.isdir(a.source):
        names = sorted(f for f in os.listdir(a.source) if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")))
        if not names:
            sys.exit(f"No images in {a.source}")
        tiles = [(os.path.splitext(n)[0], Image.open(os.path.join(a.source, n)).convert("RGB")) for n in names]
    else:
        length = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.source],
                                      capture_output=True, text=True, check=True).stdout.strip())
        stop = min(a.stop if a.stop is not None else length, length)
        step = a.every or max((stop - a.start) / 20.0, 0.04)
        times, t = [], a.start
        while t < stop - 1e-6:
            times.append(t)
            t += step
        folder = os.path.splitext(a.out)[0] + "-frames"
        if a.full:
            os.makedirs(folder, exist_ok=True)
        for t in times:
            grab = ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", a.source, "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"]
            data = subprocess.run(grab, capture_output=True).stdout
            if not data:
                continue
            import io
            image = Image.open(io.BytesIO(data)).convert("RGB")
            if a.full:
                image.save(os.path.join(folder, f"{t:07.3f}.png"))
            tiles.append((f"{t:.2f} s", image))
        if not tiles:
            sys.exit("No frames could be read.")

    w = a.width
    h = round(w * tiles[0][1].height / tiles[0][1].width)
    gap, label_h = 8, 26
    cols = min(a.columns, len(tiles))
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (gap + cols * (w + gap), gap + rows * (h + label_h + gap)), (24, 24, 24))
    draw = ImageDraw.Draw(sheet)
    face = font(17)
    for i, (label, image) in enumerate(tiles):
        x = gap + (i % cols) * (w + gap)
        y = gap + (i // cols) * (h + label_h + gap)
        sheet.paste(image.resize((w, h), Image.LANCZOS), (x, y))
        draw.text((x + 2, y + h + 3), label, fill=(235, 235, 235), font=face)
    sheet.save(a.out, quality=88)
    print(f"Wrote {a.out}: {len(tiles)} frames, {sheet.width} x {sheet.height}")


if __name__ == "__main__":
    main()
