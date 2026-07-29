#!/usr/bin/env python3
"""Validate evidence, slide-plan, and visual contracts as one presentation handoff."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator


SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = SKILL_ROOT / "references"
SCHEMAS = {
    "evidence": REFERENCES / "presentation-evidence-schema.json",
    "plan": REFERENCES / "slide-plan-schema.json",
    "visual": REFERENCES / "visual-spec-schema.json",
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _schema_errors(label: str, data: dict) -> list[str]:
    schema = _load(SCHEMAS[label])
    errors = sorted(
        Draft202012Validator(schema).iter_errors(data),
        key=lambda error: list(error.absolute_path),
    )
    return [
        f"{label}.{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: "
        f"{error.message}"
        for error in errors
    ]


def _ids(records: list[dict], label: str, failures: list[str]) -> set[str]:
    values = [str(record["id"]) for record in records if "id" in record]
    duplicates = sorted({value for value in values if values.count(value) > 1})
    failures.extend(f"{label}: duplicate id {value}" for value in duplicates)
    return set(values)


def _missing(
    references: list[str],
    available: set[str],
    location: str,
    failures: list[str],
) -> None:
    for reference in references:
        if reference not in available:
            failures.append(f"{location}: unknown reference {reference}")


def validate(evidence: dict, plan: dict, visual: dict) -> list[str]:
    failures = [
        *_schema_errors("evidence", evidence),
        *_schema_errors("plan", plan),
        *_schema_errors("visual", visual),
    ]
    if failures:
        return failures

    source_ids = _ids(evidence["sources"], "evidence.sources", failures)
    slide_evidence_ids = _ids(evidence["slides"], "evidence.slides", failures)
    transcript_ids = _ids(
        evidence["transcript_segments"], "evidence.transcript_segments", failures
    )
    frame_ids = _ids(evidence["frames"], "evidence.frames", failures)
    evidence_id_groups = {
        "sources": source_ids,
        "slides": slide_evidence_ids,
        "transcript_segments": transcript_ids,
        "frames": frame_ids,
    }
    evidence_id_locations: dict[str, list[str]] = {}
    for group, identifiers in evidence_id_groups.items():
        for identifier in identifiers:
            evidence_id_locations.setdefault(identifier, []).append(group)
    for identifier, groups in sorted(evidence_id_locations.items()):
        if len(groups) > 1:
            failures.append(
                f"evidence: id {identifier} is reused across {', '.join(groups)}"
            )
    evidence_ids = source_ids | slide_evidence_ids | transcript_ids | frame_ids
    sources_by_id = {item["id"]: item for item in evidence["sources"]}
    evidence_slides_by_id = {item["id"]: item for item in evidence["slides"]}
    frames_by_id = {item["id"]: item for item in evidence["frames"]}

    for source in evidence["sources"]:
        normalized_from = source.get("normalized_from")
        if normalized_from is not None:
            _missing(
                [normalized_from],
                source_ids,
                f"evidence.sources[{source['id']}].normalized_from",
                failures,
            )
            if normalized_from == source["id"]:
                failures.append(
                    f"evidence.sources[{source['id']}].normalized_from: "
                    "cannot reference itself"
                )

    for segment in evidence["transcript_segments"]:
        _missing(
            [segment["source_id"]],
            source_ids,
            f"evidence.transcript_segments[{segment['id']}].source_id",
            failures,
        )
        end = segment["end_seconds"]
        if end is not None and end < segment["start_seconds"]:
            failures.append(
                f"evidence.transcript_segments[{segment['id']}]: end_seconds precedes start_seconds"
            )

    for frame in evidence["frames"]:
        _missing(
            [frame["source_id"]],
            source_ids,
            f"evidence.frames[{frame['id']}].source_id",
            failures,
        )
        if frame["duplicate_of"] is not None:
            _missing(
                [frame["duplicate_of"]],
                frame_ids,
                f"evidence.frames[{frame['id']}].duplicate_of",
                failures,
            )
            if frame["duplicate_of"] == frame["id"]:
                failures.append(
                    f"evidence.frames[{frame['id']}].duplicate_of: cannot reference itself"
                )

    for slide in evidence["slides"]:
        _missing(
            [slide["source_id"]],
            source_ids,
            f"evidence.slides[{slide['id']}].source_id",
            failures,
        )
        _missing(
            slide["transcript_segment_ids"],
            transcript_ids,
            f"evidence.slides[{slide['id']}].transcript_segment_ids",
            failures,
        )
        _missing(
            slide["frame_ids"],
            frame_ids,
            f"evidence.slides[{slide['id']}].frame_ids",
            failures,
        )

    claim_ids = _ids(plan["claims"], "plan.claims", failures)
    for claim in plan["claims"]:
        _missing(
            claim["evidence_ids"],
            evidence_ids,
            f"plan.claims[{claim['id']}].evidence_ids",
            failures,
        )
        if claim["kind"] in {"fact", "metric"} and not claim["evidence_ids"]:
            failures.append(
                f"plan.claims[{claim['id']}].evidence_ids: fact and metric claims require evidence"
            )

    planned_slide_ids = [slide["slide_id"] for slide in plan["slides"]]
    duplicate_slide_ids = sorted(
        {value for value in planned_slide_ids if planned_slide_ids.count(value) > 1}
    )
    failures.extend(
        f"plan.slides: duplicate slide_id {value}" for value in duplicate_slide_ids
    )
    planned_slide_id_set = set(planned_slide_ids)

    visual_ids = _ids(visual["visuals"], "visual.visuals", failures)
    visuals_by_id = {item["id"]: item for item in visual["visuals"]}
    planned_visual_ids_by_slide = {
        slide["slide_id"]: set(slide["visual_ids"]) for slide in plan["slides"]
    }
    for item in visual["visuals"]:
        _missing(
            item.get("evidence_ids", []),
            evidence_ids,
            f"visual.visuals[{item['id']}].evidence_ids",
            failures,
        )
        unknown_slides = sorted(set(item["slide_ids"]) - planned_slide_id_set)
        failures.extend(
            f"visual.visuals[{item['id']}].slide_ids: unknown slide {slide_id}"
            for slide_id in unknown_slides
        )
        for slide_id in item["slide_ids"]:
            if (
                slide_id in planned_visual_ids_by_slide
                and item["id"] not in planned_visual_ids_by_slide[slide_id]
            ):
                failures.append(
                    f"visual.visuals[{item['id']}].slide_ids: slide {slide_id} "
                    f"does not map back to visual {item['id']}"
                )
        if item["route"] == "extract" and not item.get("evidence_ids"):
            failures.append(
                f"visual.visuals[{item['id']}].evidence_ids: extract routes require source evidence"
            )
        if item["route"] == "extract" and item.get("source") is not None:
            locator = item["source"]
            cited_ids = set(item.get("evidence_ids", []))
            frame_id = locator.get("frame")
            page = locator.get("page")
            source_path = locator["path"]
            if frame_id is not None:
                frame = frames_by_id.get(frame_id)
                if frame_id not in cited_ids:
                    failures.append(
                        f"visual.visuals[{item['id']}].source.frame: {frame_id} "
                        "must appear in evidence_ids"
                    )
                if frame is None:
                    failures.append(
                        f"visual.visuals[{item['id']}].source.frame: unknown frame {frame_id}"
                    )
                elif (
                    frame["source_id"] in sources_by_id
                    and sources_by_id[frame["source_id"]]["path"] != source_path
                ):
                    failures.append(
                        f"visual.visuals[{item['id']}].source.path: {source_path} "
                        f"does not match frame {frame_id}'s source"
                    )
            elif page is not None:
                matching_slide_ids = {
                    slide_id
                    for slide_id, slide in evidence_slides_by_id.items()
                    if slide["page"] == page
                    and slide["source_id"] in sources_by_id
                    and sources_by_id[slide["source_id"]]["path"] == source_path
                }
                if not matching_slide_ids.intersection(cited_ids):
                    failures.append(
                        f"visual.visuals[{item['id']}].source.page: page {page} at "
                        f"{source_path} must identify a slide in evidence_ids"
                    )
            else:
                matching_source_ids = {
                    source_id
                    for source_id, source in sources_by_id.items()
                    if source["path"] == source_path
                }
                if not matching_source_ids.intersection(cited_ids):
                    failures.append(
                        f"visual.visuals[{item['id']}].source.path: {source_path} "
                        "must identify a source in evidence_ids when frame and page are null"
                    )

    for slide in plan["slides"]:
        slide_id = slide["slide_id"]
        _missing(
            slide["claim_ids"],
            claim_ids,
            f"plan.slides[{slide_id}].claim_ids",
            failures,
        )
        _missing(
            slide["evidence_ids"],
            evidence_ids,
            f"plan.slides[{slide_id}].evidence_ids",
            failures,
        )
        _missing(
            slide["visual_ids"],
            visual_ids,
            f"plan.slides[{slide_id}].visual_ids",
            failures,
        )
        if (
            slide["status"] != "omitted"
            and slide["archetype"] != "cover"
            and not slide["claim_ids"]
            and not slide["evidence_ids"]
        ):
            failures.append(
                f"plan.slides[{slide_id}]: non-cover slides require a claim or direct evidence"
            )
        for visual_id in slide["visual_ids"]:
            item = visuals_by_id.get(visual_id)
            if item is not None and slide_id not in item["slide_ids"]:
                failures.append(
                    f"plan.slides[{slide_id}].visual_ids: {visual_id} does not map back to slide {slide_id}"
                )

    return failures


def _is_remote(path: str) -> bool:
    return urlparse(path).scheme in {"http", "https"}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_files(evidence: dict, evidence_path: Path) -> list[str]:
    failures: list[str] = []
    root = evidence_path.parent / evidence["bundle"]["root"]
    candidates: list[tuple[str, str, bool, str | None]] = []
    candidates.extend(
        (f"source {item['id']}", item["path"], True, item["sha256"])
        for item in evidence["sources"]
    )
    candidates.extend(
        (
            f"slide {item['id']} image",
            item["image"],
            False,
            item["image_sha256"],
        )
        for item in evidence["slides"]
        if item["image"] is not None
    )
    candidates.extend(
        (f"frame {item['id']}", item["path"], False, item["sha256"])
        for item in evidence["frames"]
    )
    for label, value, allow_directory, expected_sha256 in candidates:
        if _is_remote(value):
            continue
        path = root / value
        exists = path.exists() if allow_directory else path.is_file()
        if not exists:
            failures.append(f"{label}: missing file {root / value}")
            continue
        if expected_sha256 is not None and path.is_file():
            actual_sha256 = _sha256(path)
            if actual_sha256 != expected_sha256:
                failures.append(
                    f"{label}: checksum mismatch for {path} "
                    f"(expected {expected_sha256}, got {actual_sha256})"
                )
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("slide_plan", type=Path)
    parser.add_argument("visual_spec", type=Path)
    parser.add_argument("--check-files", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        evidence = _load(args.evidence)
        plan = _load(args.slide_plan)
        visual = _load(args.visual_spec)
    except (OSError, json.JSONDecodeError) as exc:
        print(exc)
        return 1

    failures = validate(evidence, plan, visual)
    if args.check_files and not failures:
        failures.extend(validate_files(evidence, args.evidence))
    if failures:
        print("\n".join(failures))
        return 1
    print(f"valid: {args.evidence} + {args.slide_plan} + {args.visual_spec}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
