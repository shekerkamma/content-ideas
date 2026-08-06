#!/usr/bin/env python3
"""Build the visual-context reconstruction contract from selected states."""

import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
states = json.loads((RUN / "selected-states.json").read_text(encoding="utf-8"))
items = []
for index, state in enumerate(states, start=2):
    items.append({
        "id": f"reconstruction-{index - 1:02d}",
        "state_ids": [state["id"]],
        "timestamp_seconds": state["timestamp_seconds"],
        "transcript_window": [f"transcript context around {state['timestamp_seconds']} seconds"],
        "visible_title": state["visual_summary"],
        "visual_summary": state["visual_summary"],
        "context_summary": state["context_summary"],
        "assets": [state["asset"]],
        "route": "extract",
        "slide_ids": [index],
        "disposition": "placed",
        "reason": None,
    })
(RUN / "reconstruction-map.json").write_text(json.dumps({
    "contract_version": "1.0", "mode": "reconstruction", "items": items
}, indent=2) + "\n", encoding="utf-8")

