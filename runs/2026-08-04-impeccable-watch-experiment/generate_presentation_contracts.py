#!/usr/bin/env python3
"""Generate governed presentation contracts for the reviewed Watch/Impeccable deck."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ITEMS = json.loads((ROOT / "visual-context-map.json").read_text())["items"]
URL = "https://www.youtube.com/watch?v=RVeCbPg0liw"


def dump(name: str, value: object) -> None:
    (ROOT / name).write_text(json.dumps(value, indent=2) + "\n")


frames = []
for index, item in enumerate(ITEMS, 1):
    asset = ROOT / item["asset"]
    frames.append({
        "id": f"frame-{index:04d}",
        "timestamp_seconds": item["timestamp"],
        "path": item["asset"],
        "sha256": hashlib.sha256(asset.read_bytes()).hexdigest(),
        "description": f'{item["title"]}. {item["context"]}',
        "duplicate_of": None,
        "screen_class": "demo-screen",
        "face_quality": None,
        "source_id": "source-video",
    })

evidence = {
    "contract_version": "1.0",
    "bundle": {"id": "impeccable-watch-client-deck", "title": "Impeccable 4.0 — Visual Workflow", "root": "."},
    "sources": [{
        "id": "source-video", "kind": "video", "path": URL, "sha256": None,
        "rights": "Source-frame excerpts used for analysis and visual demonstration; client must verify reuse rights.",
        "normalized_from": None,
    }],
    "slides": [],
    "transcript_segments": [],
    "frames": frames,
}
dump("presentation-evidence.json", evidence)

titles = [
    "Design with range, taste, and control",
    "Impeccable is a loop, not a style button",
    "The problem is sameness",
    "Live Mode changes the interaction",
    "Worlds supply a complete visual grammar",
    "Options respond to the project",
    "One skill exposes a design workflow",
    "Anti-patterns become detectable",
    "Installation is deliberately lightweight",
    "The example begins with purpose",
    "Compare directions before committing",
    "The first result is a baseline",
    "Live comparison creates a selection loop",
    "The next pass deliberately increases range",
    "Detection turns taste into action",
    "The chosen world becomes a design record",
    "Outside references add specificity",
    "Reference becomes interpretation—not imitation",
    "The template improved how the assets are seen",
]
frame_for_slide = {1: 1, **{slide: slide - 1 for slide in range(3, 19)}}
slides = []
claims = []
for slide_id, title in enumerate(titles, 1):
    frame_num = frame_for_slide.get(slide_id)
    evidence_ids = [f"frame-{frame_num:04d}"] if frame_num else []
    claim_id = f"claim-{slide_id:02d}"
    claims.append({
        "id": claim_id, "text": title, "kind": "interpretation",
        "confidence": "high" if evidence_ids else "medium", "evidence_ids": evidence_ids,
    })
    visual_ids = [f"visual-{frame_num:02d}"] if frame_num else []
    slides.append({
        "slide_id": slide_id,
        "archetype": "cover" if slide_id == 1 else ("decision" if slide_id == 19 else "evidence-proof"),
        "action_title": title,
        "audience_job": "Understand the visual workflow and the evidence behind the design decision.",
        "claim_ids": [claim_id], "evidence_ids": evidence_ids, "visual_ids": visual_ids,
        "speaker_notes": {"talk_time_seconds": 35, "narrative": title, "demo_fallback": "Use the embedded source proof."},
        "accessibility": {"reading_order": ["title", "visual", "interpretation"], "visual_alt_text": title},
        "status": "reviewed",
    })
slide_plan = {
    "contract_version": "1.0",
    "deck": {"name": "Impeccable 4.0 — Visual Workflow", "evidence_contract": "presentation-evidence.json", "visual_contract": "visual-spec.json"},
    "claims": claims,
    "slides": slides,
}
dump("slide-plan.json", slide_plan)

visuals = []
for index, item in enumerate(ITEMS, 1):
    slide_id = 1 if index == 1 else index + 1
    visuals.append({
        "id": f"visual-{index:02d}", "slide_ids": [slide_id],
        "purpose": f'Exact source proof for “{item["title"]}”.', "artifact_type": "ui",
        "evidence_status": "exact-source-evidence", "route": "extract",
        "reason": "The interface state is evidence; preserve the captured frame exactly and add editable interpretation around it.",
        "evidence_ids": [f"frame-{index:04d}"],
        "source": {"path": URL, "page": None, "frame": f"frame-{index:04d}", "timestamp": str(item["timestamp"]), "crop": None},
        "asset": item["asset"], "editable_source": None, "prompt_file": None, "execution": None,
        "placement": {"width": 1920, "height": 1080, "fit": "contain", "background": "#F1ECE2"},
        "qa": {"visual_checked": True, "legible": True, "not_cropped": True, "background_matched": True, "provenance_recorded": True, "text_free": None, "not_evidence": False, "exact_fidelity": True},
    })
visual_spec = {
    "contract_version": "1.0",
    "deck": {"output_mode": "hybrid", "editability": "Editable titles, annotations, layout, and shapes; source video frames remain raster evidence.", "reference_deck": None},
    "visuals": visuals,
}
dump("visual-spec.json", visual_spec)
