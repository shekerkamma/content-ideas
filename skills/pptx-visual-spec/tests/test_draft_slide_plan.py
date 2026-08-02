from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/draft_slide_plan.py"
SLIDE_PLAN_SCHEMA = json.loads((ROOT / "references/slide-plan-schema.json").read_text())


def run_draft(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def _write_evidence(tmp_path: Path, slides: list[dict]) -> Path:
    evidence = {
        "contract_version": "1.0",
        "bundle": {"id": "test-bundle", "title": "Test Deck", "root": str(tmp_path)},
        "sources": [],
        "slides": slides,
        "transcript_segments": [],
        "frames": [],
    }
    path = tmp_path / "presentation-evidence.json"
    path.write_text(json.dumps(evidence), encoding="utf-8")
    return path


def _slide(page: int, extracted_text: str | None, summary: str | None) -> dict:
    return {
        "id": f"slide-{page}",
        "page": page,
        "source_id": "src-1",
        "image": None,
        "image_sha256": None,
        "extracted_text": extracted_text,
        "summary": summary,
        "links": [],
        "transcript_segment_ids": [],
        "frame_ids": [],
    }


def test_draft_validates_against_schema(tmp_path: Path) -> None:
    evidence_path = _write_evidence(
        tmp_path,
        [
            _slide(1, "Title slide", "Title slide introducing the deck"),
            _slide(2, " ".join(["word"] * 60), "Agenda covering four workstreams"),
            _slide(3, " ".join(["word"] * 130), None),
        ],
    )

    result = run_draft([str(evidence_path)])

    assert result.returncode == 0, result.stderr
    draft = json.loads((tmp_path / "slide-plan.draft.json").read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(SLIDE_PLAN_SCHEMA).iter_errors(draft))
    assert not errors, errors


def test_archetype_heuristic_respects_max_words(tmp_path: Path) -> None:
    evidence_path = _write_evidence(
        tmp_path,
        [_slide(1, " ".join(["word"] * 20), "Short section break")],
    )

    run_draft([str(evidence_path)])

    draft = json.loads((tmp_path / "slide-plan.draft.json").read_text(encoding="utf-8"))
    archetype = draft["slides"][0]["archetype"]
    from importlib import util

    spec = util.spec_from_file_location("draft_slide_plan", SCRIPT)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    picked = next(a for a in module.ARCHETYPES if a["id"] == archetype)
    assert picked["max_words"] >= 20


def test_missing_outline_produces_todo_placeholder(tmp_path: Path) -> None:
    evidence_path = _write_evidence(
        tmp_path,
        [_slide(1, "Some slide text", None)],
    )

    result = run_draft([str(evidence_path)])

    draft = json.loads((tmp_path / "slide-plan.draft.json").read_text(encoding="utf-8"))
    assert draft["slides"][0]["action_title"] == "TODO: summarize slide 1"
    assert "need a manual action_title" in result.stdout


def test_output_never_overwrites_slide_plan(tmp_path: Path) -> None:
    canonical = tmp_path / "slide-plan.json"
    canonical.write_text("{}", encoding="utf-8")
    evidence_path = _write_evidence(tmp_path, [_slide(1, "Slide text", "Summary")])

    result = run_draft([str(evidence_path)])

    assert result.returncode == 0, result.stderr
    assert canonical.read_text(encoding="utf-8") == "{}"
    assert (tmp_path / "slide-plan.draft.json").is_file()


def test_no_slides_in_evidence_errors(tmp_path: Path) -> None:
    evidence_path = _write_evidence(tmp_path, [])

    result = run_draft([str(evidence_path)])

    assert result.returncode == 1
    assert "no slides" in result.stdout
