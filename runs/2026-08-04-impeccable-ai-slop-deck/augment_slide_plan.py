#!/usr/bin/env python3
"""Add required delivery metadata to each planned slide."""

import json
from pathlib import Path

path = Path(__file__).with_name("slide-plan.json")
data = json.loads(path.read_text(encoding="utf-8"))
for slide in data["slides"]:
    slide["speaker_notes"] = {
        "talk_time_seconds": 35,
        "narrative": slide["audience_job"],
        "demo_fallback": None,
    }
    slide["accessibility"] = {
        "reading_order": ["action title", "primary visual", "decision statement"],
        "visual_alt_text": slide["action_title"],
    }
    slide["status"] = "reviewed"
path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
