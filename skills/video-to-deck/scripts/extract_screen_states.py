#!/usr/bin/env python3
"""Extract candidate screen states from a downloaded product-demo video."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


def parse_crop(value: str | None) -> tuple[int, int, int, int] | None:
    if not value:
        return None
    parts = tuple(int(part) for part in value.split(","))
    if len(parts) != 4 or min(parts[2:]) <= 0:
        raise ValueError("crop must be x,y,width,height")
    x, y, width, height = parts
    return x, y, x + width, y + height


def thumbnail(path: Path, crop: tuple[int, int, int, int] | None) -> Image.Image:
    with Image.open(path) as source:
        image = source.convert("L")
        if crop:
            image = image.crop(crop)
        return image.resize((64, 36))


def mean_delta(left: Image.Image, right: Image.Image) -> float:
    return ImageStat.Stat(ImageChops.difference(left, right)).mean[0]


def select_state_indices(
    frames: list[Path], threshold: float, crop: tuple[int, int, int, int] | None
) -> tuple[list[int], list[float]]:
    if not frames:
        return [], []
    selected = [0]
    deltas = [0.0]
    previous = thumbnail(frames[0], crop)
    for index, frame in enumerate(frames[1:], 1):
        current = thumbnail(frame, crop)
        delta = mean_delta(previous, current)
        deltas.append(delta)
        if delta >= threshold:
            selected.append(index)
        previous = current
    if selected[-1] != len(frames) - 1:
        selected.append(len(frames) - 1)
    return selected, deltas


def run(args: argparse.Namespace) -> Path:
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is required")
    video = Path(args.video).resolve()
    if not video.exists():
        raise SystemExit(f"video not found: {video}")
    out = Path(args.out_dir).resolve()
    raw = out / "sampled"
    states = out / "states"
    raw.mkdir(parents=True, exist_ok=True)
    states.mkdir(parents=True, exist_ok=True)
    for path in [*raw.glob("frame_*.png"), *states.glob("state_*.png")]:
        path.unlink()

    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video),
        "-vf", f"fps={args.fps}", str(raw / "frame_%05d.png"),
    ]
    subprocess.run(command, check=True)
    frames = sorted(raw.glob("frame_*.png"))
    crop = parse_crop(args.crop)
    selected, deltas = select_state_indices(frames, args.threshold, crop)
    pinned = {round(float(value) * args.fps) for value in args.pin.split(",") if value.strip()}
    selected = sorted(set(selected) | {min(max(i, 0), len(frames) - 1) for i in pinned})

    records = []
    for state_number, frame_index in enumerate(selected, 1):
        source = frames[frame_index]
        target = states / f"state_{state_number:04d}.png"
        shutil.copy2(source, target)
        records.append({
            "id": f"state-{state_number:04d}",
            "timestamp_seconds": round(frame_index / args.fps, 3),
            "source_frame": str(source.relative_to(out)),
            "state_frame": str(target.relative_to(out)),
            "delta": round(deltas[frame_index], 3),
            "class": "unclassified",
            "meaningful": None,
            "route": "unassigned",
            "asset": None,
            "slide_ids": [],
            "disposition": "pending",
            "reason": None,
        })
    manifest = {
        "video": str(video),
        "fps": args.fps,
        "threshold": args.threshold,
        "crop": args.crop,
        "sampled_frame_count": len(frames),
        "candidate_state_count": len(records),
        "states": records,
    }
    path = out / "screen-states.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {path} with {len(records)} candidate states from {len(frames)} samples")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--fps", type=float, default=1.0)
    parser.add_argument("--threshold", type=float, default=1.0)
    parser.add_argument("--crop", help="content ROI as x,y,width,height")
    parser.add_argument("--pin", default="", help="comma-separated timestamps in seconds")
    run(parser.parse_args())


if __name__ == "__main__":
    main()
