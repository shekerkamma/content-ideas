#!/usr/bin/env python3
"""Build presentation-evidence.json from cached presentation artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path


TIMESTAMP_LINE = re.compile(
    r"^\[(?P<stamp>(?:\d{1,2}:)?\d{1,2}:\d{2})\]\s+(?P<text>.+)$"
)
SLIDE_SECTION = re.compile(
    r"(?ms)^## Slide (?P<page>\d+)\s*$\n.*?^```\s*$\n(?P<text>.*?)\n^```\s*$"
)
OUTLINE_LINE = re.compile(r"^\s*(?P<page>\d+)[.)]\s+(?P<summary>.+?)\s*$")
FRAME_ROW = re.compile(
    r"^\|\s*(?P<file>[^|]+?)\s*\|\s*\[?"
    r"(?P<stamp>(?:\d{1,2}:)?\d{1,2}:\d{2})\]?\s*\|"
    r"\s*(?P<description>.*?)\s*\|$"
)
URL = re.compile(r"https?://[^\s>)\]]+")


def _seconds(stamp: str) -> int:
    parts = [int(part) for part in stamp.split(":")]
    if len(parts) == 2:
        minutes, seconds = parts
        return minutes * 60 + seconds
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds
    raise ValueError(f"unsupported timestamp: {stamp}")


def _sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _source_kind(value: str, override: str | None = None) -> str:
    if override is not None:
        return override
    remote = value.startswith(("http://", "https://"))
    suffix = Path(value.split("?", 1)[0]).suffix.lower()
    hostname = (
        value.partition("://")[2]
        .split("/", 1)[0]
        .rsplit("@", 1)[-1]
        .split(":", 1)[0]
        .lower()
        if remote
        else ""
    )
    known_video_host = hostname in {
        "youtu.be",
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "vimeo.com",
        "www.vimeo.com",
        "player.vimeo.com",
    }
    return {
        ".pptx": "pptx",
        ".pdf": "pdf",
        ".mp4": "video",
        ".mov": "video",
        ".mkv": "video",
        ".webm": "video",
        ".txt": "transcript",
    }.get(suffix, "video" if known_video_host else ("revealjs" if remote else "other"))


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "presentation"


def _discover_sources(run: Path) -> list[Path]:
    names = (
        "source.pptx",
        "slides.pptx",
        "source.pdf",
        "slides.pdf",
        "video.mp4",
        "video.mov",
        "video.mkv",
        "video.webm",
    )
    return [run / name for name in names if (run / name).is_file()]


def _parse_slide_text(path: Path) -> dict[int, str]:
    if not path.is_file():
        return {}
    return {
        int(match.group("page")): match.group("text").strip()
        for match in SLIDE_SECTION.finditer(path.read_text(encoding="utf-8"))
    }


def _parse_outline(path: Path) -> dict[int, str]:
    if not path.is_file():
        return {}
    summaries: dict[int, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = OUTLINE_LINE.match(line)
        if match:
            summaries[int(match.group("page"))] = match.group("summary")
    return summaries


def _parse_transcript(path: Path, source_id: str) -> list[dict]:
    if not path.is_file():
        return []
    records: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = TIMESTAMP_LINE.match(line.strip())
        if not match:
            continue
        records.append(
            {
                "id": f"transcript-{len(records) + 1:04d}",
                "start_seconds": _seconds(match.group("stamp")),
                "end_seconds": None,
                "text": match.group("text").strip(),
                "source_id": source_id,
            }
        )
    for current, following in zip(records, records[1:]):
        current["end_seconds"] = following["start_seconds"]
    return records


def _classify_frame(description: str | None) -> str:
    text = (description or "").lower()
    for needle, value in (
        ("terminal", "terminal-result"),
        ("diagram", "diagram"),
        ("demo", "demo-screen"),
        ("browser", "demo-screen"),
        ("screen", "demo-screen"),
        ("speaker", "talking-head"),
        ("slide", "text-slide"),
    ):
        if needle in text:
            return value
    return "unclassified"


def _parse_frames(path: Path, run: Path, source_id: str) -> list[dict]:
    if not path.is_file():
        return []
    records: list[dict] = []
    previous_id: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        match = FRAME_ROW.match(line)
        if not match or match.group("file").strip().lower() == "file":
            continue
        description = match.group("description").strip() or None
        frame_id = f"frame-{len(records) + 1:04d}"
        duplicate_of = (
            previous_id if description and description.lower() == "(same as previous)" else None
        )
        frame_path = Path(match.group("file").strip())
        if not frame_path.is_absolute():
            frame_path = run / frame_path
        records.append(
            {
                "id": frame_id,
                "timestamp_seconds": _seconds(match.group("stamp")),
                "path": _relative(frame_path, run),
                "sha256": _sha256(frame_path),
                "description": description,
                "duplicate_of": duplicate_of,
                "screen_class": "duplicate" if duplicate_of else _classify_frame(description),
                "face_quality": None,
                "source_id": source_id,
            }
        )
        if duplicate_of is None:
            previous_id = frame_id
    return records


def build(args: argparse.Namespace) -> dict:
    run = args.run.resolve()
    source_values = list(args.source or [])
    video_sources = list(getattr(args, "video_source", None) or [])
    video_source_values = set(video_sources)
    source_values.extend(video_sources)
    source_values.extend(_relative(path, run) for path in _discover_sources(run))
    source_values = list(dict.fromkeys(source_values))

    sources: list[dict] = []
    for index, value in enumerate(source_values, 1):
        local = None if value.startswith(("http://", "https://")) else run / value
        sources.append(
            {
                "id": f"source-{index:02d}",
                "kind": _source_kind(
                    value, "video" if value in video_source_values else None
                ),
                "path": value,
                "sha256": _sha256(local) if local else None,
                "rights": args.rights,
                "normalized_from": None,
            }
        )

    video_sources = [item for item in sources if item["kind"] == "video"]
    transcript_path = run / args.transcript
    transcript_source_id = "source-transcript"
    requested_transcript_source = getattr(args, "transcript_source", None)
    transcript_origin_id: str | None = None
    if transcript_path.is_file():
        if requested_transcript_source is not None:
            matching_sources = [
                item
                for item in video_sources
                if item["path"] == requested_transcript_source
            ]
            if not matching_sources:
                raise ValueError(
                    "--transcript-source must exactly match a --source or "
                    "--video-source classified as video"
                )
            transcript_origin_id = matching_sources[0]["id"]
        elif len(video_sources) > 1:
            raise ValueError(
                "multiple video sources found; pass --transcript-source to identify "
                "which video produced transcript.txt"
            )
        elif video_sources:
            transcript_origin_id = video_sources[0]["id"]
        sources.append(
            {
                "id": transcript_source_id,
                "kind": "transcript",
                "path": _relative(transcript_path, run),
                "sha256": _sha256(transcript_path),
                "rights": args.rights,
                "normalized_from": transcript_origin_id,
            }
        )

    manifest_path = run / args.frames_manifest
    requested_frame_source = getattr(args, "frame_source", None)
    if requested_frame_source is not None:
        matching_sources = [
            item for item in video_sources if item["path"] == requested_frame_source
        ]
        if not matching_sources:
            raise ValueError(
                "--frame-source must exactly match a --source or --video-source "
                "classified as video"
            )
        frame_source_id = matching_sources[0]["id"]
    elif manifest_path.is_file() and len(video_sources) > 1:
        raise ValueError(
            "multiple video sources found; pass --frame-source to identify which "
            "video produced frames_manifest.md"
        )
    elif video_sources:
        frame_source_id = video_sources[0]["id"]
    else:
        frame_source_id = "source-frame-manifest"
    if manifest_path.is_file() and frame_source_id == "source-frame-manifest":
        sources.append(
            {
                "id": frame_source_id,
                "kind": "other",
                "path": _relative(manifest_path, run),
                "sha256": _sha256(manifest_path),
                "rights": args.rights,
                "normalized_from": None,
            }
        )

    slide_source_id = next(
        (item["id"] for item in sources if item["kind"] in {"pptx", "pdf", "revealjs"}),
        "source-slide-artifacts",
    )
    if slide_source_id == "source-slide-artifacts":
        slide_artifact = run / args.slide_text
        outline_artifact = run / args.outline
        if (
            slide_artifact.is_file()
            or (run / args.slide_images).is_dir()
            or outline_artifact.is_file()
        ):
            source_artifact = (
                slide_artifact
                if slide_artifact.is_file()
                else (
                    run / args.slide_images
                    if (run / args.slide_images).is_dir()
                    else outline_artifact
                )
            )
            sources.append(
                {
                    "id": slide_source_id,
                    "kind": "other",
                    "path": _relative(source_artifact, run),
                    "sha256": _sha256(source_artifact),
                    "rights": args.rights,
                    "normalized_from": None,
                }
            )

    text_by_page = _parse_slide_text(run / args.slide_text)
    summary_by_page = _parse_outline(run / args.outline)
    images = {
        int(match.group(1)): path
        for path in (run / args.slide_images).glob("slide_*.png")
        if (match := re.fullmatch(r"slide_(\d+)", path.stem))
    }
    pages = sorted(set(text_by_page) | set(summary_by_page) | set(images))
    slides = []
    for page in pages:
        text = text_by_page.get(page)
        image = images.get(page)
        slides.append(
            {
                "id": f"source-slide-{page}",
                "page": page,
                "source_id": slide_source_id,
                "image": _relative(image, run) if image else None,
                "image_sha256": _sha256(image) if image else None,
                "extracted_text": text,
                "summary": summary_by_page.get(page),
                "links": sorted(set(URL.findall(text or ""))),
                "transcript_segment_ids": [],
                "frame_ids": [],
            }
        )

    return {
        "contract_version": "1.0",
        "bundle": {
            "id": _slug(args.bundle_id or args.title or run.name),
            "title": args.title or run.name.replace("-", " ").title(),
            "root": ".",
        },
        "sources": sources,
        "slides": slides,
        "transcript_segments": _parse_transcript(
            transcript_path, transcript_source_id
        ),
        "frames": _parse_frames(manifest_path, run, frame_source_id),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--title")
    parser.add_argument("--bundle-id")
    parser.add_argument("--source", action="append")
    parser.add_argument(
        "--video-source",
        action="append",
        help=(
            "Original video URL or filename. Repeat for multiple sources; use this "
            "for extensionless video URLs on hosts other than YouTube or Vimeo."
        ),
    )
    parser.add_argument(
        "--frame-source",
        help=(
            "Exact --source or --video-source value that produced frames_manifest.md; "
            "required when the bundle contains multiple videos."
        ),
    )
    parser.add_argument(
        "--transcript-source",
        help=(
            "Exact --source or --video-source value that produced transcript.txt; "
            "required when the bundle contains multiple videos."
        ),
    )
    parser.add_argument(
        "--rights", default="unknown; verify before client delivery"
    )
    parser.add_argument("--slide-images", default="slide_images")
    parser.add_argument("--slide-text", default="slide_ascii.md")
    parser.add_argument("--outline", default="outline.txt")
    parser.add_argument("--transcript", default="transcript.txt")
    parser.add_argument("--frames-manifest", default="frames_manifest.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.run.is_dir():
        raise SystemExit(f"run directory not found: {args.run}")
    output = args.out or args.run / "presentation-evidence.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = build(args)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    data["bundle"]["root"] = Path(
        os.path.relpath(args.run.resolve(), output.parent.resolve())
    ).as_posix()
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"wrote: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
