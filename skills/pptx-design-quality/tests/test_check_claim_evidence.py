from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


import pytest

pytest.importorskip(
    "jsonschema",
    reason="jsonschema is an opt-in skill dependency (see this skill's requirements.txt); the validator scripts under test import it",
)

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts/check_claim_evidence.py"


def run_check(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def _evidence(tmp_path: Path, slide_text: str) -> Path:
    data = {
        "contract_version": "1.0",
        "bundle": {"id": "bundle-1", "title": "Deck", "root": str(tmp_path)},
        "sources": [],
        "slides": [
            {
                "id": "slide-1",
                "page": 1,
                "source_id": "src-1",
                "image": None,
                "image_sha256": None,
                "extracted_text": slide_text,
                "summary": None,
                "links": [],
                "transcript_segment_ids": [],
                "frame_ids": [],
            }
        ],
        "transcript_segments": [],
        "frames": [],
    }
    path = tmp_path / "presentation-evidence.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def _plan(tmp_path: Path, claim: dict, evidence_filename: str = "presentation-evidence.json") -> Path:
    data = {
        "contract_version": "1.0",
        "deck": {"name": "Deck", "evidence_contract": evidence_filename, "visual_contract": "visual-spec.json"},
        "claims": [claim],
        "slides": [
            {
                "slide_id": 1,
                "archetype": "big-number",
                "action_title": "Revenue grew",
                "audience_job": "Retain one material metric",
                "claim_ids": [claim["id"]],
                "evidence_ids": ["slide-1"],
                "visual_ids": [],
                "speaker_notes": {"talk_time_seconds": None, "narrative": None, "demo_fallback": None},
                "accessibility": {"reading_order": ["title"], "visual_alt_text": None},
                "status": "planned",
            }
        ],
    }
    path = tmp_path / "slide-plan.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_unsourced_number_is_flagged(tmp_path: Path) -> None:
    evidence_path = _evidence(tmp_path, "Revenue grew 12% year over year")
    claim = {
        "id": "claim-1",
        "text": "Revenue grew 45% year over year",
        "kind": "metric",
        "confidence": "high",
        "evidence_ids": ["slide-1"],
    }
    plan_path = _plan(tmp_path, claim)

    result = run_check([str(evidence_path), str(plan_path)])

    assert result.returncode == 2
    assert "UNSOURCED_NUMBER" in result.stdout
    assert "45%" in result.stdout


def test_sourced_number_passes(tmp_path: Path) -> None:
    evidence_path = _evidence(tmp_path, "Revenue grew 45% year over year")
    claim = {
        "id": "claim-1",
        "text": "Revenue grew 45% year over year",
        "kind": "metric",
        "confidence": "high",
        "evidence_ids": ["slide-1"],
    }
    plan_path = _plan(tmp_path, claim)

    result = run_check([str(evidence_path), str(plan_path)])

    assert result.returncode == 0, result.stdout
    assert "clean" in result.stdout


def test_unverifiable_evidence_is_flagged(tmp_path: Path) -> None:
    evidence_path = _evidence(tmp_path, None)  # type: ignore[arg-type]
    claim = {
        "id": "claim-1",
        "text": "Revenue grew 45% year over year",
        "kind": "fact",
        "confidence": "medium",
        "evidence_ids": ["slide-1"],
    }
    plan_path = _plan(tmp_path, claim)

    result = run_check([str(evidence_path), str(plan_path)])

    assert result.returncode == 2
    assert "UNVERIFIABLE_EVIDENCE" in result.stdout


def test_interpretation_claims_are_skipped(tmp_path: Path) -> None:
    evidence_path = _evidence(tmp_path, "No numbers here at all")
    claim = {
        "id": "claim-1",
        "text": "This suggests 500% future growth is likely",
        "kind": "interpretation",
        "confidence": "low",
        "evidence_ids": ["slide-1"],
    }
    plan_path = _plan(tmp_path, claim)

    result = run_check([str(evidence_path), str(plan_path)])

    assert result.returncode == 0, result.stdout


def test_null_evidence_contract_is_a_noop(tmp_path: Path) -> None:
    evidence_path = _evidence(tmp_path, "Revenue grew 12%")
    claim = {
        "id": "claim-1",
        "text": "Revenue grew 999% year over year",
        "kind": "metric",
        "confidence": "high",
        "evidence_ids": ["slide-1"],
    }
    plan_path = _plan(tmp_path, claim, evidence_filename="presentation-evidence.json")
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan["deck"]["evidence_contract"] = None
    plan_path.write_text(json.dumps(plan), encoding="utf-8")

    result = run_check([str(evidence_path), str(plan_path)])

    assert result.returncode == 0, result.stdout


def test_waived_rule_is_suppressed(tmp_path: Path) -> None:
    evidence_path = _evidence(tmp_path, "Revenue grew 12%")
    claim = {
        "id": "claim-1",
        "text": "Revenue grew 45%",
        "kind": "metric",
        "confidence": "high",
        "evidence_ids": ["slide-1"],
    }
    plan_path = _plan(tmp_path, claim)
    config_path = tmp_path / "deck-design.json"
    config_path.write_text(
        json.dumps({"qa": {"ignore_rules": ["UNSOURCED_NUMBER"], "waivers": {"UNSOURCED_NUMBER": "reviewed manually"}}}),
        encoding="utf-8",
    )

    result = run_check([str(evidence_path), str(plan_path), "--config", str(config_path)])

    assert result.returncode == 0, result.stdout
