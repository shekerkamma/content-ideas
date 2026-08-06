#!/usr/bin/env python3
"""Recover the selected Watch visual states without replacing their pixels."""

import json
import subprocess
from pathlib import Path


RUN = Path(__file__).resolve().parent
VIDEO = Path("/home/sheke/content-ideas/runs/2026-08-04-impeccable-ai-slop-deck/video.mp4")
ASSETS = RUN / "assets"
STATES = [
    ("intro", 13, "Impeccable 4.0", "A design-control system for moving beyond generic defaults."),
    ("taste", 43, "The problem is sameness", "Taste has to enter the workflow before the first composition becomes the default."),
    ("live", 76, "Live Mode changes the interaction", "Visual direction becomes something you inspect and choose—not merely describe."),
    ("worlds", 100, "Worlds supply a complete visual grammar", "A world constrains composition, typography, material, rhythm, and interaction together."),
    ("options", 134, "Options respond to the project", "The system proposes directions grounded in the current surface instead of a generic style menu."),
    ("commands", 193, "One skill exposes a design workflow", "Commands separate shaping, detection, refinement, documentation, and finish review."),
    ("patterns", 234, "Anti-patterns become detectable", "Recurring machine-made defaults can be named, located, and removed deliberately."),
    ("install", 267, "Installation is deliberately lightweight", "The design system enters the existing workflow through one package command."),
    ("brief", 332, "The example begins with purpose", "The demonstration starts from the site's reason to exist before choosing its appearance."),
    ("variations", 425, "Compare directions before committing", "Multiple treatments expose range and make the design decision visual."),
    ("baseline", 526, "The first result is a baseline", "A complete first pass creates something concrete to inspect—not an excuse to stop iterating."),
    ("comparison", 577, "Live comparison creates a selection loop", "Side-by-side alternatives make differences in hierarchy and character immediately visible."),
    ("bolder", 629, "The next pass deliberately increases range", "The workflow pushes beyond cautious polish to test a materially stronger direction."),
    ("detector", 660, "Detection turns taste into action", "The working design is checked against explicit visual anti-patterns."),
    ("design-record", 675, "The chosen world becomes a design record", "Documented decisions keep later iterations coherent instead of rediscovering taste each time."),
    ("references", 769, "Outside references add specificity", "Real visual references communicate proportion and texture that prose cannot fully encode."),
    ("reference-result", 803, "Reference becomes interpretation—not imitation", "The final pass translates the reference grammar into a distinct working result."),
]

ASSETS.mkdir(parents=True, exist_ok=True)
records = []
for index, (slug, timestamp, title, context) in enumerate(STATES, start=1):
    target = ASSETS / f"{index:02d}-{slug}.jpg"
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(timestamp),
        "-i", str(VIDEO), "-frames:v", "1", "-q:v", "2", str(target)
    ], check=True)
    records.append({"id": slug, "timestamp": timestamp, "title": title, "context": context, "asset": str(target.relative_to(RUN))})
(RUN / "visual-context-map.json").write_text(json.dumps({"items": records}, indent=2) + "\n", encoding="utf-8")
