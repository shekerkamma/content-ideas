#!/usr/bin/env python3
"""Validate the cross-host Genspark video-to-deck handoff contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REVIEW_GATES = (
    "coverage_complete",
    "claims_validated",
    "unsupported_specifics_clean",
    "visual_render_reviewed",
    "editability_verified",
    "pptx_schema_valid",
    "office_issues_clean",
)


def require(mapping: dict, key: str, prefix: str, failures: list[str]):
    if key not in mapping:
        failures.append(f"missing {prefix}.{key}")
        return None
    return mapping[key]


def validate(data: dict) -> list[str]:
    failures: list[str] = []
    if data.get("contract_version") != "1.2":
        failures.append("contract_version must be 1.2")
    if not data.get("run_id"):
        failures.append("run_id is required")

    sections: dict[str, dict] = {}
    for name in ("source", "generation", "recovery", "delivery", "qa"):
        value = data.get(name)
        if not isinstance(value, dict):
            failures.append(f"{name} must be an object")
            value = {}
        sections[name] = value

    source = sections["source"]
    generation = sections["generation"]
    recovery = sections["recovery"]
    delivery = sections["delivery"]
    qa = sections["qa"]

    coverage_rows = require(source, "coverage_rows", "source", failures)
    if not isinstance(coverage_rows, int) or coverage_rows < 0:
        failures.append("source.coverage_rows must be a non-negative integer")

    if source.get("kind") == "video":
        if source.get("capture_mode") != "scene-complete":
            failures.append("video source.capture_mode must be scene-complete")
        if not isinstance(source.get("distinct_screen_count"), int) or source.get("distinct_screen_count", 0) <= 0:
            failures.append("video source.distinct_screen_count must be positive")
        if not isinstance(source.get("transcript_segment_count"), int) or source.get("transcript_segment_count", 0) <= 0:
            failures.append("video source.transcript_segment_count must be positive")
        for key in ("screen_manifest", "context_packet", "coverage_matrix"):
            if not source.get(key):
                failures.append(f"video source.{key} is required")

    if generation.get("slide_count_policy") != "evidence-driven":
        failures.append("generation.slide_count_policy must be evidence-driven")
    status = generation.get("status")
    allowed_generation = {
        "not_requested", "generating", "completed", "blocked_credit_limit",
        "blocked_access", "blocked_generation", "skipped_local_fallback",
    }
    if status not in allowed_generation:
        failures.append(f"invalid generation.status: {status}")
    if status == "blocked_credit_limit" and generation.get("explicit_credit_error") is not True:
        failures.append("blocked_credit_limit requires generation.explicit_credit_error=true")
    if generation.get("explicit_credit_error") is True and status != "blocked_credit_limit":
        failures.append("explicit_credit_error=true requires blocked_credit_limit status")

    captured = recovery.get("captured_slide_count")
    endpoints = recovery.get("endpoint_count")
    if not isinstance(captured, int) or captured < 0:
        failures.append("recovery.captured_slide_count must be a non-negative integer")
    if not isinstance(endpoints, int) or endpoints < 0:
        failures.append("recovery.endpoint_count must be a non-negative integer")
    if isinstance(captured, int) and isinstance(endpoints, int) and captured > endpoints:
        failures.append("captured_slide_count cannot exceed endpoint_count")
    if recovery.get("status") == "captured" and captured != endpoints:
        failures.append("recovery.status=captured requires all endpoints saved")

    editability = delivery.get("requested_editability")
    artifact_class = delivery.get("artifact_class")
    expected = {
        "image": "image-based-reference",
        "hybrid": "hybrid-editable-text",
        "native": "fully-native-editable",
    }
    if editability not in expected:
        failures.append(f"invalid delivery.requested_editability: {editability}")
    elif artifact_class != expected[editability]:
        failures.append(
            f"delivery.artifact_class must be {expected[editability]} for {editability}"
        )

    delivery_status = delivery.get("status")
    if delivery_status not in {"draft", "reviewed", "blocked"}:
        failures.append(f"invalid delivery.status: {delivery_status}")
    blockers = qa.get("blockers")
    if not isinstance(blockers, list):
        failures.append("qa.blockers must be an array")
        blockers = []
    if delivery_status == "reviewed":
        for gate in REVIEW_GATES:
            if qa.get(gate) is not True:
                failures.append(f"reviewed delivery requires qa.{gate}=true")
        if blockers:
            failures.append("reviewed delivery cannot have qa.blockers")
        if not delivery.get("pptx"):
            failures.append("reviewed delivery requires delivery.pptx")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.handoff.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR cannot read handoff: {exc}")
        return 1
    failures = validate(data)
    if failures:
        print("\n".join(f"ERROR {item}" for item in failures))
        return 1
    print(f"valid Genspark handoff: {args.handoff}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
