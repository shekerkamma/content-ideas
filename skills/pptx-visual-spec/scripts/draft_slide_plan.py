#!/usr/bin/env python3
"""Draft a slide-plan.json from a presentation-evidence.json bundle.

Never writes the canonical slide-plan.json; always writes a distinctly named
draft that must be reviewed, copied over, and validated with
validate_presentation_contracts.py. Writing claim text is a narrative/factual
judgment left to a human or agent — drafted slides carry evidence_ids but no
claims.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


# Mirrors skills/pptx-design-quality/references/slide-archetypes.json's id/max_words
# pairs. Duplicated rather than imported cross-skill; keep in sync if that catalog
# changes its word budgets or adds/removes archetypes.
ARCHETYPES = [
    {"id": "cover", "max_words": 28, "audience_job": "Understand the promise and context"},
    {"id": "executive-summary", "max_words": 110, "audience_job": "Grasp the answer, evidence, and decision on one page"},
    {"id": "section-divider", "max_words": 24, "audience_job": "Reset context between argument sections"},
    {"id": "big-number", "max_words": 42, "audience_job": "Retain one material metric and implication"},
    {"id": "three-card-argument", "max_words": 90, "audience_job": "Compare three parallel claims or workstreams"},
    {"id": "comparison", "max_words": 100, "audience_job": "Understand a consequential contrast"},
    {"id": "decision-scorecard", "max_words": 120, "audience_job": "Choose between options using explicit criteria"},
    {"id": "roadmap", "max_words": 110, "audience_job": "Understand sequence, ownership, and outcomes"},
    {"id": "operating-model", "max_words": 115, "audience_job": "Understand roles, flows, and governance"},
    {"id": "use-case-realization", "max_words": 145, "audience_job": "See how a use case becomes an executable solution"},
    {"id": "risk-mitigation", "max_words": 105, "audience_job": "Understand material risks and mitigations"},
    {"id": "recommendation-ask", "max_words": 75, "audience_job": "Know the recommendation, commitment, and next move"},
]


def pick_archetype(word_count: int) -> dict[str, Any]:
    """Return the tightest-fitting archetype whose max_words covers word_count."""
    candidates = [entry for entry in ARCHETYPES if word_count <= entry["max_words"]]
    if not candidates:
        return max(ARCHETYPES, key=lambda entry: entry["max_words"])
    return min(candidates, key=lambda entry: entry["max_words"])


def draft_slide(slide: dict[str, Any]) -> dict[str, Any]:
    text = slide.get("extracted_text") or ""
    word_count = len(text.split())
    archetype = pick_archetype(word_count)

    summary = slide.get("summary")
    action_title = summary if summary else f"TODO: summarize slide {slide['page']}"

    return {
        "slide_id": slide["page"],
        "archetype": archetype["id"],
        "action_title": action_title,
        "audience_job": archetype["audience_job"],
        "claim_ids": [],
        "evidence_ids": [slide["id"]],
        "visual_ids": [],
        "speaker_notes": {
            "talk_time_seconds": None,
            "narrative": None,
            "demo_fallback": None,
        },
        "accessibility": {
            "reading_order": ["title"],
            "visual_alt_text": None,
        },
        "status": "planned",
    }


def draft_slide_plan(evidence: dict[str, Any], evidence_filename: str) -> dict[str, Any]:
    return {
        "contract_version": "1.0",
        "deck": {
            "name": evidence.get("bundle", {}).get("title") or "Untitled deck",
            "evidence_contract": evidence_filename,
            "visual_contract": "visual-spec.json",
        },
        "claims": [],
        "slides": [draft_slide(slide) for slide in evidence.get("slides", [])],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path, help="Path to presentation-evidence.json")
    parser.add_argument(
        "--out", type=Path, help="Draft output path (default: <evidence-dir>/slide-plan.draft.json)"
    )
    args = parser.parse_args()

    try:
        evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}")
        return 1

    if not evidence.get("slides"):
        print("error: presentation-evidence.json has no slides to draft a plan from")
        return 1

    out_path = args.out or args.evidence.parent / "slide-plan.draft.json"
    plan = draft_slide_plan(evidence, args.evidence.name)
    out_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    todo_count = sum(1 for slide in plan["slides"] if slide["action_title"].startswith("TODO:"))
    print(f"drafted {len(plan['slides'])} slide(s) to {out_path}")
    if todo_count:
        print(f"{todo_count} slide(s) have no outline.txt summary and need a manual action_title")
    print("Review, then: cp", out_path, "<run-dir>/slide-plan.json")
    print(
        "Validate with: python3 scripts/validate_presentation_contracts.py "
        "<evidence> <run-dir>/slide-plan.json <run-dir>/visual-spec.json"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
