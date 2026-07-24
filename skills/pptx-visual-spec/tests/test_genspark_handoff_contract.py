from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_genspark_handoff.py"
TEMPLATE = ROOT / "references" / "genspark-handoff-template.json"
SPEC = importlib.util.spec_from_file_location("validate_genspark_handoff", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def valid_video_handoff() -> dict:
    data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    data["run_id"] = "2026-07-22-test"
    data["source"].update(
        distinct_screen_count=10,
        transcript_segment_count=20,
        coverage_rows=8,
    )
    return data


def test_template_becomes_valid_with_video_evidence_counts() -> None:
    assert MODULE.validate(valid_video_handoff()) == []


def test_credit_block_requires_explicit_ui_or_api_evidence() -> None:
    data = valid_video_handoff()
    data["generation"]["status"] = "blocked_credit_limit"
    assert "blocked_credit_limit requires generation.explicit_credit_error=true" in MODULE.validate(data)


def test_reviewed_requires_every_gate_and_pptx() -> None:
    data = valid_video_handoff()
    data["delivery"]["status"] = "reviewed"
    failures = MODULE.validate(data)
    assert any("qa.coverage_complete" in failure for failure in failures)
    assert any("delivery.pptx" in failure for failure in failures)


def test_hybrid_cannot_be_labelled_fully_native() -> None:
    data = valid_video_handoff()
    data["delivery"]["requested_editability"] = "hybrid"
    assert any("hybrid-editable-text" in failure for failure in MODULE.validate(data))
