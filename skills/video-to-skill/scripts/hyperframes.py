#!/usr/bin/env python3
"""Dense screen-state capture for screencasts, where watch's scene engine goes blind.

`watch --detail token-burner` is uncapped but still gates on SCENE_THRESHOLD =
0.20, a value tuned for filmed video with real cuts. A screencast changes a
terminal pane or a code region while browser chrome, editor frame, and webcam
overlay hold still, so those transitions never score 0.20 and the engine returns
a sparse set with multi-minute blind spots -- while reporting success.

Measured on a 61-minute coding tutorial (L4g6GGLzAyo):

    threshold 0.20 (watch default) ->   86 frames, gaps up to 7m10s
    threshold 0.10                 ->  441 frames
    threshold 0.05                 -> 1059 frames
    threshold 0.03                 -> 1462 frames

Two changes make the capture trustworthy on this material:

1. a screencast-tuned threshold, and
2. a max-gap fill, so a stretch that genuinely never triggers still gets
   sampled. Without it, "no frames here" is indistinguishable from "nothing
   happened here", and a derivation cannot tell the two apart.

Reuses watch's own extraction and perceptual dedup rather than reimplementing
them. Stdlib only, plus watch's frames.py and the ffmpeg binary.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SCREENCAST_THRESHOLD = 0.10
DEFAULT_MAX_GAP = 45.0


def load_watch_frames(watch_dir: Path):
    scripts = watch_dir / "scripts"
    if not (scripts / "frames.py").is_file():
        sys.stderr.write(
            f"ERROR: no frames.py under {scripts}\n"
            "Pass --watch-dir pointing at the installed watch skill.\n"
        )
        raise SystemExit(2)
    sys.path.insert(0, str(scripts))
    import frames  # type: ignore

    return frames


def fill_gaps(
    frames_mod,
    video_path: str,
    out_dir: Path,
    kept: list[dict],
    duration: float,
    max_gap: float,
    resolution: int,
) -> list[dict]:
    """Sample any stretch longer than max_gap that scene detection never fired on."""
    times = sorted(f["timestamp_seconds"] for f in kept)
    needed: list[float] = []
    edges = [0.0, *times, duration]
    for a, b in zip(edges, edges[1:]):
        span = b - a
        if span <= max_gap:
            continue
        n = int(span // max_gap)
        step = span / (n + 1)
        needed.extend(a + step * (i + 1) for i in range(n))
    if not needed:
        return []
    # extract_at_timestamps returns (frames, meta), not a bare list.
    filled, _meta = frames_mod.extract_at_timestamps(
        video_path, out_dir, needed, resolution=resolution
    )
    for f in filled:
        f["reason"] = "gap-fill"
    return filled


def coverage(frames_list: list[dict], duration: float) -> dict:
    times = sorted(f["timestamp_seconds"] for f in frames_list)
    if not times:
        return {"count": 0}
    edges = [0.0, *times, duration]
    gaps = [b - a for a, b in zip(edges, edges[1:])]
    return {
        "count": len(times),
        "max_gap_seconds": round(max(gaps), 1),
        "mean_gap_seconds": round(sum(gaps) / len(gaps), 1),
        "first": round(times[0], 1),
        "last": round(times[-1], 1),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", help="local video file (download it once with watch first)")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--watch-dir", default=os.environ.get("WATCH_DIR", str(Path.home() / ".claude/skills/watch")))
    ap.add_argument("--threshold", type=float, default=SCREENCAST_THRESHOLD,
                    help=f"ffmpeg scene threshold (default {SCREENCAST_THRESHOLD}; watch uses 0.20)")
    ap.add_argument("--max-gap", type=float, default=DEFAULT_MAX_GAP,
                    help=f"seconds; longer stretches get sampled anyway (default {DEFAULT_MAX_GAP})")
    ap.add_argument("--resolution", type=int, default=1024)
    ap.add_argument("--cap", type=int, help="even-sample down to this many frames after dedup")
    ap.add_argument("--no-dedup", action="store_true")
    args = ap.parse_args()

    video = Path(args.video).expanduser()
    if not video.is_file():
        sys.stderr.write(f"ERROR: no such video: {video}\n")
        return 2

    frames_mod = load_watch_frames(Path(args.watch_dir).expanduser())
    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    meta = frames_mod.get_metadata(str(video))
    # frames.get_metadata returns duration_seconds; a missing key here silently
    # zeroed the tail edge and made the coverage report meaningless.
    duration = float(meta.get("duration_seconds") or 0.0)
    if duration <= 0:
        sys.stderr.write("ERROR: could not read duration; coverage would be meaningless\n")
        return 2
    if meta.get("width", 0) < 1280:
        sys.stderr.write(
            f"WARNING: source is only {meta.get('width')}x{meta.get('height')}. "
            "On a screencast, terminal and code text will not be legible. "
            "Re-download with an HD format before deriving.\n"
        )

    print(f"scene detection at threshold {args.threshold} (watch default is 0.20)...", file=sys.stderr)
    candidates = frames_mod.extract_scene_candidates(
        str(video), out_dir, resolution=args.resolution,
        max_frames=None, threshold=args.threshold,
    )
    print(f"  {len(candidates)} candidates", file=sys.stderr)

    if args.no_dedup:
        kept, dropped = candidates, 0
    else:
        kept, dropped = frames_mod.dedupe_perceptual(candidates)
        print(f"  {dropped} near-identical dropped -> {len(kept)}", file=sys.stderr)

    if args.cap and len(kept) > args.cap:
        kept = frames_mod._even_sample(kept, args.cap)
        print(f"  even-sampled to {len(kept)}", file=sys.stderr)

    before = coverage(kept, duration)
    filled = fill_gaps(frames_mod, str(video), out_dir, kept, duration,
                       args.max_gap, args.resolution)
    if filled:
        print(f"  {len(filled)} gap-fill frames for stretches over {args.max_gap}s", file=sys.stderr)
    allf = frames_mod.merge_frames(kept, filled) if filled else kept

    after = coverage(allf, duration)
    manifest = {
        "video": str(video),
        "duration_seconds": duration,
        "threshold": args.threshold,
        "max_gap_seconds": args.max_gap,
        "resolution": args.resolution,
        "candidates": len(candidates),
        "deduped_dropped": dropped,
        "gap_filled": len(filled),
        "coverage_before_fill": before,
        "coverage_after_fill": after,
        "frames": [
            {
                "index": i,
                "timestamp": round(f["timestamp_seconds"], 2),
                "time": frames_mod.format_time(f["timestamp_seconds"]),
                "reason": f.get("reason", "scene-change"),
                "path": str(f["path"]),
            }
            for i, f in enumerate(allf)
        ],
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"\n{len(allf)} frames -> {out_dir}")
    print(f"coverage: max gap {after['max_gap_seconds']}s, mean {after['mean_gap_seconds']}s "
          f"(before gap-fill: max {before['max_gap_seconds']}s)")
    print(f"manifest: {out_dir / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
