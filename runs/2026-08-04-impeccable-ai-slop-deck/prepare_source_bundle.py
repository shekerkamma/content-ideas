#!/usr/bin/env python3
"""Normalize watch output into the portable presentation source bundle."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RUN = Path(__file__).resolve().parent
WATCH = RUN / "watch"
FRAMES = WATCH / "frames"
WATCH_LIB = Path("/home/sheke/.codex/skills/watch/scripts")
sys.path.insert(0, str(WATCH_LIB))
from transcribe import format_transcript, parse_vtt  # noqa: E402

SOURCE = "https://www.youtube.com/watch?v=RVeCbPg0liw"
TIMES = [
    "00:00", "00:21", "00:41", "01:00", "01:20", "01:26", "01:32", "01:39",
    "01:46", "01:53", "02:10", "03:08", "03:25", "04:07", "04:26", "04:46",
    "05:24", "05:52", "06:18", "06:32", "06:44", "06:55", "07:07", "07:31",
    "08:02", "08:22", "08:42", "08:56", "09:10", "09:24", "09:36", "09:46",
    "10:01", "10:20", "10:37", "10:48", "10:59", "11:15", "11:35", "11:52",
    "12:10", "12:30", "12:49", "13:01", "13:12", "13:23", "15:10",
]

SELECTED = {
    9: "Impeccable visual-world library",
    13: "Impeccable command and documentation interface",
    23: "Side-by-side visual variation review",
    27: "Completed demonstration website",
    31: "Live visual comparison interface",
    38: "DESIGN.md and design-system capture",
    43: "External inspiration library",
    46: "Reference-led redesign result",
}


def main() -> None:
    segments = parse_vtt(WATCH / "download" / "video.en.vtt")
    (RUN / "transcript.txt").write_text(format_transcript(segments) + "\n", encoding="utf-8")
    shutil.copy2(WATCH / "download" / "video.mp4", RUN / "video.mp4")

    assets = RUN / "assets"
    assets.mkdir(exist_ok=True)
    manifest = [
        "# Frames Manifest",
        "",
        "| File | Timestamp | Classification | Description | Disposition |",
        "|---|---:|---|---|---|",
    ]
    states = []
    for index, stamp in enumerate(TIMES, start=1):
        src = FRAMES / f"frame_{index:04d}.jpg"
        description = SELECTED.get(index, "Context frame from the demonstration")
        disposition = "selected" if index in SELECTED else "context-only"
        manifest.append(
            f"| watch/frames/{src.name} | {stamp} | demonstration frame | {description} | {disposition} |"
        )
        states.append({
            "frame": f"watch/frames/{src.name}", "timestamp": stamp,
            "classification": "demonstration frame", "description": description,
            "disposition": disposition, "source": SOURCE,
        })
        if index in SELECTED:
            image = Image.open(src).convert("RGB")
            # Remove the presenter bubble without inventing visual evidence.
            crop = image.crop((0, 0, image.width, int(image.height * 0.83)))
            crop.save(assets / f"evidence-{index:02d}.jpg", quality=94)

    (RUN / "frames_manifest.md").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    (RUN / "screen-states.json").write_text(json.dumps(states, indent=2) + "\n", encoding="utf-8")

    # A compact source index for human QA.
    thumbs = []
    for index in SELECTED:
        im = Image.open(assets / f"evidence-{index:02d}.jpg").convert("RGB")
        im.thumbnail((480, 270))
        thumbs.append((index, im.copy()))
    sheet = Image.new("RGB", (1000, 620), "#F4F0E8")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for position, (index, im) in enumerate(thumbs):
        x = 20 + (position % 2) * 490
        y = 20 + (position // 2) * 150
        sheet.paste(im, (x, y + 18))
        draw.text((x, y), f"{index:02d} · {TIMES[index - 1]} · {SELECTED[index]}", fill="#151515", font=font)
    sheet.save(assets / "selected-evidence-contact-sheet.jpg", quality=92)


if __name__ == "__main__":
    main()
