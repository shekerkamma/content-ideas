#!/usr/bin/env python3
"""Validate visible multi-skill impact for a presentation build."""
import argparse, json, math
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--check-files", action="store_true")
    args = ap.parse_args()
    path = Path(args.manifest).resolve()
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = []
    count = int(data.get("slide_count", 0))
    if count < 1: errors.append("slide_count must be positive")
    stages = data.get("stages") or []
    required = {"watch", "presentation-source-bundle", "ai-analyst", "story-architect", "presentation-content-writer", "impeccable", "explainer-graphic", "ai-graphics", "branded-pptx-deck", "pptx-toolkit", "officecli"}
    applied = {s.get("skill") for s in stages if s.get("status") == "applied"}
    errors += [f"required stage not applied: {x}" for x in sorted(required - applied)]
    for stage in stages:
        if not stage.get("proper_layer") or not stage.get("impact"):
            errors.append(f"stage lacks layer/impact evidence: {stage.get('skill')}")
    content = data.get("content") or {}
    if int(content.get("visible_slide_count", 0)) != count: errors.append("content writer must map visible content on every slide")
    if int(content.get("notes_slide_count", 0)) not in {0, count}: errors.append("native notes must be complete or omitted")
    direction = data.get("direction") or {}
    if int(direction.get("candidate_count", 0)) < 3: errors.append("direction comparison requires three candidates")
    if int(direction.get("representative_slide_count", 0)) < 3: errors.append("direction comparison requires three representative slides")
    if not direction.get("selected") or len(direction.get("material_differences") or []) < 4: errors.append("selected direction needs four material differences")
    visual = data.get("visual_system") or {}
    if int(visual.get("archetype_count", 0)) < 3: errors.append("visual system requires three archetypes")
    minimum = math.ceil(count * .6) if count else 1
    if int(visual.get("slides_covered", 0)) < minimum: errors.append(f"visual system must cover at least {minimum} slides")
    if not visual.get("editable_sources"): errors.append("visual system requires editable source evidence")
    qa = data.get("qa") or {}
    for gate in ["contracts_valid", "lint_clean", "officecli_zero_issues", "real_render_reviewed", "independent_review_passed"]:
        if qa.get(gate) is not True: errors.append(f"QA gate not passed: {gate}")
    if args.check_files:
        for stage in stages:
            for item in stage.get("outputs") or []:
                if not (path.parent / item).resolve().exists(): errors.append(f"missing output: {item}")
        for item in visual.get("editable_sources") or []:
            if not (path.parent / item).resolve().exists(): errors.append(f"missing editable visual source: {item}")
    if errors:
        print("\n".join(errors)); return 1
    print(f"valid: {path}"); return 0


if __name__ == "__main__": raise SystemExit(main())
