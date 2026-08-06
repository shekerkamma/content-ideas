#!/usr/bin/env python3
"""Extract clean, high-value visual states for the reconstruction deck."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

RUN = Path(__file__).resolve().parent
VIDEO = Path("/home/sheke/content-ideas/runs/2026-08-04-impeccable-ai-slop-deck/video.mp4")
ASSETS = RUN / "assets"

STATES = [
    ("01-intro", 13, "Impeccable 4.0 introduction", "Impeccable 4.0 is introduced as a design-control system."),
    ("02-taste", 43, "Avoid generic AI design", "The opening problem is sameness: generic visual defaults instead of deliberate taste."),
    ("03-live", 76, "Live mode", "Live mode is presented as the release's largest workflow change."),
    ("04-worlds", 100, "Visual worlds", "A world supplies a coherent visual grammar before composition begins."),
    ("05-options", 134, "Context-specific options", "The interface proposes directions that respond to the current project."),
    ("06-commands", 193, "One skill and its commands", "A single installed skill exposes a family of design and review commands."),
    ("07-detect", 234, "Anti-pattern detection", "Detection makes recurring generic patterns visible and actionable."),
    ("08-install", 267, "Installation", "The demonstrated setup is a single package-install command."),
    ("09-brief", 332, "Website brief", "The example begins with purpose and content, not decoration."),
    ("10-variations", 425, "Visual variations", "Multiple directions are generated so the user can select visually."),
    ("11-result", 526, "First finished result", "The first complete page establishes a usable baseline rather than a final answer."),
    ("12-live-compare", 577, "Live comparison", "Side-by-side inspection turns iteration into a selection loop."),
    ("13-bolder", 629, "Bolder alternatives", "The next pass deliberately pushes range instead of polishing one default."),
    ("14-detect-ui", 660, "Detector results", "The detector identifies concrete anti-patterns in the working design."),
    ("15-design-md", 675, "Design system record", "Design decisions are captured so the direction remains coherent across iterations."),
    ("16-reference", 769, "Inspiration library", "External references provide visual specificity that prose cannot fully encode."),
    ("17-reference-result", 803, "Reference-led result", "The reference is translated into a distinct implementation rather than copied literally."),
]


def extract_frame(timestamp: int, target: Path) -> None:
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(timestamp),
        "-i", str(VIDEO), "-frames:v", "1", "-q:v", "2", str(target)
    ], check=True)


def mask_presenter(path: Path) -> None:
    image = Image.open(path).convert("RGB")
    width, height = image.size
    # The fixed presenter overlay obscures the source screen, so it cannot be recovered.
    # Cover only that non-evidence overlay with a matte sampled from the adjacent screen.
    x0, y0 = int(width * 0.72), int(height * 0.61)
    sample = image.crop((int(width * 0.66), y0, x0, height))
    sample.thumbnail((1, 1))
    ImageDraw.Draw(image).rectangle((x0, y0, width, height), fill=sample.getpixel((0, 0)))
    image.save(path, quality=95)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    records = []
    for asset_id, timestamp, visual, context in STATES:
        target = ASSETS / f"{asset_id}.jpg"
        extract_frame(timestamp, target)
        mask_presenter(target)
        records.append({
            "id": asset_id,
            "timestamp_seconds": timestamp,
            "asset": str(target.relative_to(RUN)),
            "visual_summary": visual,
            "context_summary": context,
            "provenance": "source-extracted",
        })
    shutil.copy2(
        "/home/sheke/content-ideas/runs/2026-08-04-impeccable-ai-slop-deck/transcript.txt",
        RUN / "transcript.txt",
    )
    (RUN / "selected-states.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
