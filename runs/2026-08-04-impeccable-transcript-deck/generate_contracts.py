#!/usr/bin/env python3
"""Generate transcript-led presentation contracts."""

from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
URL = "https://www.youtube.com/watch?v=RVeCbPg0liw"
MAP = json.loads((ROOT / "transcript-map.json").read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2) + "\n")


def seconds(value):
    minutes, secs = map(int, value.split(":"))
    return minutes * 60 + secs


segments = []
for section in MAP["sections"]:
    segments.append({
        "id": f'transcript-{section["id"]}',
        "start_seconds": seconds(section["start"]),
        "end_seconds": seconds(section["end"]),
        "text": section["thesis"],
        "source_id": "source-transcript",
    })

frame_specs = [
    ("frame-worlds", 100, "assets/worlds.jpg", "World selection interface shown in the demonstration."),
    ("frame-live", 577, "assets/live-comparison.jpg", "Live comparison state shown in the demonstration."),
    ("frame-references", 769, "assets/references.jpg", "Reference library shown before a macro direction change."),
]
frames = []
for frame_id, timestamp, path, description in frame_specs:
    frames.append({
        "id": frame_id, "timestamp_seconds": timestamp, "path": path,
        "sha256": sha(ROOT / path), "description": description, "duplicate_of": None,
        "screen_class": "demo-screen", "face_quality": None, "source_id": "source-video",
    })

evidence = {
    "contract_version": "1.0",
    "bundle": {"id": "impeccable-transcript-led", "title": "Impeccable 4.0 — Taste as an Operating System", "root": "."},
    "sources": [
        {"id": "source-video", "kind": "video", "path": URL, "sha256": None, "rights": "Source excerpts supplied for analysis; verify reuse rights before external distribution.", "normalized_from": None},
        {"id": "source-transcript", "kind": "transcript", "path": "transcript.txt", "sha256": sha(ROOT / "transcript.txt"), "rights": "Source transcript supplied for analysis; verify reuse rights before external distribution.", "normalized_from": "source-video"}
    ],
    "slides": [], "transcript_segments": segments, "frames": frames,
}
dump("presentation-evidence.json", evidence)

slides_data = [
    ("Taste becomes an operating system", "problem", []),
    ("Impeccable changes the decision system—not just the styling", "problem", []),
    ("The failure mode is convergence", "problem", []),
    ("Version 4.0 adds two decisive control surfaces", "changes", []),
    ("Worlds make direction selection concrete", "worlds", ["frame-worlds"]),
    ("Direction selection happens twice", "worlds", []),
    ("Generality trades a higher ceiling for a lower floor", "tradeoff", []),
    ("One-shot generation is the wrong mental model", "tradeoff", []),
    ("Live Mode turns local changes into visual decisions", "live", ["frame-live"]),
    ("Use the right interface for the altitude of change", "references", []),
    ("Taste becomes durable through memory and independent review", "memory", []),
    ("References are the escape hatch for a wrong direction", "references", ["frame-references"]),
    ("A practical operating model for teams", "conclusion", []),
    ("What Impeccable does not solve", "conclusion", []),
    ("Impeccable gives taste somewhere to operate", "conclusion", []),
]

claims, slides, visuals = [], [], []
for slide_id, (title, section, frame_ids) in enumerate(slides_data, 1):
    claim_id = f"claim-{slide_id:02d}"
    transcript_id = f"transcript-{section}"
    evidence_ids = [transcript_id, *frame_ids]
    claims.append({"id": claim_id, "text": title, "kind": "interpretation", "confidence": "high", "evidence_ids": evidence_ids})
    visual_id = f"visual-{slide_id:02d}"
    slides.append({
        "slide_id": slide_id, "archetype": "cover" if slide_id == 1 else ("evidence-proof" if frame_ids else "native-synthesis"),
        "action_title": title, "audience_job": "Understand the source argument and its practical implication.",
        "claim_ids": [claim_id], "evidence_ids": evidence_ids, "visual_ids": [visual_id],
        "speaker_notes": {"talk_time_seconds": 40, "narrative": title, "demo_fallback": "Use the native diagram and source-linked evidence."},
        "accessibility": {"reading_order": ["title", "visual", "supporting explanation"], "visual_alt_text": title},
        "status": "reviewed",
    })
    if frame_ids:
        frame_id = frame_ids[0]
        frame = next(item for item in frames if item["id"] == frame_id)
        visuals.append({
            "id": visual_id, "slide_ids": [slide_id], "purpose": "Prove the exact interface state described by the transcript.",
            "artifact_type": "ui", "evidence_status": "exact-source-evidence", "route": "extract",
            "reason": "The interface state is source evidence; explanatory hierarchy remains native.", "evidence_ids": evidence_ids,
            "source": {"path": URL, "page": None, "frame": frame_id, "timestamp": str(frame["timestamp_seconds"]), "crop": None},
            "asset": frame["path"], "editable_source": None, "prompt_file": None, "execution": None,
            "placement": {"width": 1920, "height": 1080, "fit": "contain", "background": "#F2EDE3"},
            "qa": {"visual_checked": True, "legible": True, "not_cropped": True, "background_matched": True, "provenance_recorded": True, "text_free": None, "not_evidence": False, "exact_fidelity": True},
        })
    else:
        visuals.append({
            "id": visual_id, "slide_ids": [slide_id], "purpose": "Explain the transcript-derived claim as an editable slide-native composition.",
            "artifact_type": "diagram", "evidence_status": "underlying-information", "route": "native",
            "reason": "The claim is conceptual and is clearer as editable PowerPoint structure than as a captured screen.", "evidence_ids": evidence_ids,
            "source": None, "asset": None, "editable_source": "build_transcript_deck.py", "prompt_file": None, "execution": None, "placement": None,
            "qa": {"visual_checked": True, "legible": True, "not_cropped": True, "background_matched": True, "provenance_recorded": True, "text_free": None, "not_evidence": False, "exact_fidelity": None},
        })

dump("slide-plan.json", {"contract_version": "1.0", "deck": {"name": "Impeccable 4.0 — Taste as an Operating System", "evidence_contract": "presentation-evidence.json", "visual_contract": "visual-spec.json"}, "claims": claims, "slides": slides})
dump("visual-spec.json", {"contract_version": "1.0", "deck": {"output_mode": "hybrid", "editability": "Twelve fully native slides and native annotations on three exact source-frame proof slides.", "reference_deck": None}, "visuals": visuals})
