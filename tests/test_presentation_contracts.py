from __future__ import annotations

import importlib.util
import json
import subprocess
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = (
    ROOT
    / "skills"
    / "pptx-visual-spec"
    / "scripts"
    / "validate_presentation_contracts.py"
)
BUILDER_PATH = (
    ROOT
    / "skills"
    / "presentation-source-bundle"
    / "scripts"
    / "build_presentation_evidence.py"
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_module("validate_presentation_contracts", VALIDATOR_PATH)
BUILDER = load_module("build_presentation_evidence", BUILDER_PATH)


def valid_contracts() -> tuple[dict, dict, dict]:
    evidence = {
        "contract_version": "1.0",
        "bundle": {"id": "demo", "title": "Demo", "root": "."},
        "sources": [
            {
                "id": "source-video",
                "kind": "video",
                "path": "video.mp4",
                "sha256": None,
                "rights": "client-supplied",
                "normalized_from": None,
            }
        ],
        "slides": [],
        "transcript_segments": [
            {
                "id": "transcript-0001",
                "start_seconds": 0,
                "end_seconds": 5,
                "text": "The product reduces manual work.",
                "source_id": "source-video",
            }
        ],
        "frames": [
            {
                "id": "frame-0001",
                "timestamp_seconds": 2,
                "path": "frames/frame_0002.png",
                "sha256": None,
                "description": "Product demo screen",
                "duplicate_of": None,
                "screen_class": "demo-screen",
                "face_quality": None,
                "source_id": "source-video",
            }
        ],
    }
    plan = {
        "contract_version": "1.0",
        "deck": {
            "name": "Demo",
            "evidence_contract": "presentation-evidence.json",
            "visual_contract": "visual-spec.json",
        },
        "claims": [
            {
                "id": "claim-1",
                "text": "The product reduces manual work.",
                "kind": "fact",
                "confidence": "high",
                "evidence_ids": ["transcript-0001"],
            }
        ],
        "slides": [
            {
                "slide_id": 1,
                "archetype": "product-proof",
                "action_title": "The workflow removes a manual step",
                "audience_job": "Understand the operating improvement",
                "claim_ids": ["claim-1"],
                "evidence_ids": ["frame-0001"],
                "visual_ids": ["visual-1"],
                "speaker_notes": {
                    "talk_time_seconds": 45,
                    "narrative": "Walk through the captured state.",
                    "demo_fallback": None,
                },
                "accessibility": {
                    "reading_order": ["title", "visual", "takeaway"],
                    "visual_alt_text": "Product screen after the manual step is removed",
                },
                "status": "planned",
            }
        ],
    }
    visual = {
        "contract_version": "1.0",
        "deck": {
            "output_mode": "native",
            "editability": "native shell with exact evidence image",
            "reference_deck": None,
        },
        "visuals": [
            {
                "id": "visual-1",
                "slide_ids": [1],
                "purpose": "Show the exact product state",
                "artifact_type": "ui",
                "evidence_status": "exact-source-evidence",
                "route": "extract",
                "reason": "The application state is evidence",
                "evidence_ids": ["frame-0001"],
                "source": {
                    "path": "video.mp4",
                    "page": None,
                    "frame": "frame-0001",
                    "timestamp": "00:02",
                    "crop": None,
                },
                "asset": "assets/frame-0001.png",
                "editable_source": None,
                "prompt_file": None,
                "execution": None,
                "placement": None,
                "qa": {
                    "visual_checked": True,
                    "legible": True,
                    "not_cropped": True,
                    "background_matched": True,
                    "provenance_recorded": True,
                    "text_free": None,
                    "not_evidence": None,
                    "exact_fidelity": True,
                },
            }
        ],
    }
    return evidence, plan, visual


def test_cross_contracts_accept_valid_evidence_plan_and_visual() -> None:
    evidence, plan, visual = valid_contracts()
    assert VALIDATOR.validate(evidence, plan, visual) == []


def test_cross_contracts_reject_unknown_claim_evidence() -> None:
    evidence, plan, visual = valid_contracts()
    plan["claims"][0]["evidence_ids"] = ["missing-evidence"]
    failures = VALIDATOR.validate(evidence, plan, visual)
    assert "plan.claims[claim-1].evidence_ids: unknown reference missing-evidence" in failures


def test_evidence_ids_must_be_globally_unique() -> None:
    evidence, plan, visual = valid_contracts()
    evidence["frames"][0]["id"] = "source-video"
    plan["slides"][0]["evidence_ids"] = ["source-video"]
    visual["visuals"][0]["evidence_ids"] = ["source-video"]
    failures = VALIDATOR.validate(evidence, plan, visual)
    assert "evidence: id source-video is reused across sources, frames" in failures


def test_extract_visual_requires_evidence_reference() -> None:
    evidence, plan, visual = valid_contracts()
    visual["visuals"][0]["evidence_ids"] = []
    failures = VALIDATOR.validate(evidence, plan, visual)
    assert (
        "visual.visuals[visual-1].evidence_ids: extract routes require source evidence"
        in failures
    )


def test_extract_visual_requires_resolvable_source_object() -> None:
    evidence, plan, visual = valid_contracts()
    visual["visuals"][0]["source"] = None
    visual["visuals"][0]["evidence_ids"] = ["transcript-0001"]
    failures = VALIDATOR.validate(evidence, plan, visual)
    assert any(
        failure.startswith("visual.visuals.0.source: None is not of type 'object'")
        for failure in failures
    )


def test_extract_frame_locator_must_match_cited_evidence() -> None:
    evidence, plan, visual = valid_contracts()
    second_frame = dict(evidence["frames"][0])
    second_frame["id"] = "frame-0002"
    second_frame["path"] = "frames/frame_0003.png"
    evidence["frames"].append(second_frame)
    visual["visuals"][0]["source"]["frame"] = "frame-0002"
    failures = VALIDATOR.validate(evidence, plan, visual)
    assert (
        "visual.visuals[visual-1].source.frame: frame-0002 must appear in evidence_ids"
        in failures
    )


def test_extract_frame_path_must_match_cited_source() -> None:
    evidence, plan, visual = valid_contracts()
    evidence["sources"].append(
        {
            "id": "source-other",
            "kind": "video",
            "path": "other.mp4",
            "sha256": None,
            "rights": "client-supplied",
            "normalized_from": None,
        }
    )
    visual["visuals"][0]["source"]["path"] = "other.mp4"
    failures = VALIDATOR.validate(evidence, plan, visual)
    assert (
        "visual.visuals[visual-1].source.path: other.mp4 does not match "
        "frame frame-0001's source"
        in failures
    )


def test_slide_visual_mapping_must_be_bidirectional() -> None:
    evidence, plan, visual = valid_contracts()
    visual["visuals"][0]["slide_ids"] = [2]
    failures = VALIDATOR.validate(evidence, plan, visual)
    assert "visual.visuals[visual-1].slide_ids: unknown slide 2" in failures
    assert (
        "plan.slides[1].visual_ids: visual-1 does not map back to slide 1" in failures
    )


def test_visual_slide_mapping_must_be_bidirectional() -> None:
    evidence, plan, visual = valid_contracts()
    plan["slides"][0]["visual_ids"] = []
    failures = VALIDATOR.validate(evidence, plan, visual)
    assert (
        "visual.visuals[visual-1].slide_ids: slide 1 does not map back to visual visual-1"
        in failures
    )


def test_builder_imports_cached_slide_transcript_and_frame_artifacts(
    tmp_path: Path,
) -> None:
    (tmp_path / "slides.pdf").write_bytes(b"pdf")
    (tmp_path / "video.mp4").write_bytes(b"video")
    slide_images = tmp_path / "slide_images"
    slide_images.mkdir()
    (slide_images / "slide_1.png").write_bytes(b"png")
    (tmp_path / "slide_ascii.md").write_text(
        "## Slide 1\n\n![Slide 1](slide_images/slide_1.png)\n\n"
        "```\nA grounded title\nhttps://example.com/proof\n```\n",
        encoding="utf-8",
    )
    (tmp_path / "outline.txt").write_text(
        "1. Evidence-backed opening slide\n", encoding="utf-8"
    )
    (tmp_path / "transcript.txt").write_text(
        "[00:00] Opening claim\n[00:05] Supporting detail\n", encoding="utf-8"
    )
    (tmp_path / "frames_manifest.md").write_text(
        "| File | Timestamp | Description |\n"
        "|------|-----------|-------------|\n"
        "| frame_0000.png | [00:00] | Product demo screen |\n",
        encoding="utf-8",
    )
    (tmp_path / "frame_0000.png").write_bytes(b"frame")

    data = BUILDER.build(
        Namespace(
            run=tmp_path,
            out=None,
            title="Grounded deck",
            bundle_id=None,
            source=None,
            rights="client-supplied",
            slide_images="slide_images",
            slide_text="slide_ascii.md",
            outline="outline.txt",
            transcript="transcript.txt",
            frames_manifest="frames_manifest.md",
        )
    )

    assert data["bundle"]["id"] == "grounded-deck"
    assert data["slides"][0]["extracted_text"] == (
        "A grounded title\nhttps://example.com/proof"
    )
    assert data["slides"][0]["summary"] == "Evidence-backed opening slide"
    assert data["slides"][0]["source_id"] == "source-01"
    assert data["slides"][0]["links"] == ["https://example.com/proof"]
    assert data["transcript_segments"][0]["end_seconds"] == 5
    transcript_source = next(
        source for source in data["sources"] if source["id"] == "source-transcript"
    )
    assert transcript_source["normalized_from"] == "source-02"
    assert data["frames"][0]["screen_class"] == "demo-screen"
    schema = json.loads(
        (
            ROOT
            / "skills"
            / "pptx-visual-spec"
            / "references"
            / "presentation-evidence-schema.json"
        ).read_text(encoding="utf-8")
    )
    errors = list(VALIDATOR.Draft202012Validator(schema).iter_errors(data))
    assert errors == []


def build_with_cli(run: Path, output: Path | None = None) -> dict:
    command = [
        "python3",
        str(BUILDER_PATH),
        "--run",
        str(run),
        "--title",
        "Test deck",
    ]
    if output is not None:
        command.extend(["--out", str(output)])
    subprocess.run(command, check=True, capture_output=True, text=True)
    result = output or run / "presentation-evidence.json"
    return json.loads(result.read_text(encoding="utf-8"))


def test_extensionless_video_urls_retain_video_provenance(tmp_path: Path) -> None:
    (tmp_path / "frames_manifest.md").write_text(
        "| File | Timestamp | Description |\n"
        "|------|-----------|-------------|\n"
        "| frame.png | [00:01] | Product demo screen |\n",
        encoding="utf-8",
    )
    (tmp_path / "frame.png").write_bytes(b"frame")
    command = [
        "python3",
        str(BUILDER_PATH),
        "--run",
        str(tmp_path),
        "--source",
        "https://www.youtube.com/watch?v=demo",
        "--video-source",
        "https://media.example.test/watch/demo",
        "--frame-source",
        "https://media.example.test/watch/demo",
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)
    evidence = json.loads(
        (tmp_path / "presentation-evidence.json").read_text(encoding="utf-8")
    )
    video_sources = {
        item["path"]: item["id"]
        for item in evidence["sources"]
        if item["kind"] == "video"
    }
    assert set(video_sources) == {
        "https://www.youtube.com/watch?v=demo",
        "https://media.example.test/watch/demo",
    }
    assert evidence["frames"][0]["source_id"] == video_sources[
        "https://media.example.test/watch/demo"
    ]


def test_multiple_video_sources_require_frame_source(tmp_path: Path) -> None:
    (tmp_path / "frames_manifest.md").write_text(
        "| File | Timestamp | Description |\n"
        "| frame.png | 00:01 | Product demo screen |\n",
        encoding="utf-8",
    )
    (tmp_path / "frame.png").write_bytes(b"frame")
    command = [
        "python3",
        str(BUILDER_PATH),
        "--run",
        str(tmp_path),
        "--video-source",
        "https://media.example.test/one",
        "--video-source",
        "https://media.example.test/two",
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode != 0
    assert "multiple video sources found" in result.stderr


def test_multiple_video_sources_require_transcript_source(tmp_path: Path) -> None:
    (tmp_path / "transcript.txt").write_text(
        "[00:01] Product claim\n", encoding="utf-8"
    )
    base_command = [
        "python3",
        str(BUILDER_PATH),
        "--run",
        str(tmp_path),
        "--video-source",
        "https://media.example.test/one",
        "--video-source",
        "https://media.example.test/two",
    ]
    result = subprocess.run(base_command, capture_output=True, text=True)
    assert result.returncode != 0
    assert "pass --transcript-source" in result.stderr

    selected = "https://media.example.test/two"
    subprocess.run(
        [*base_command, "--transcript-source", selected],
        check=True,
        capture_output=True,
        text=True,
    )
    evidence = json.loads(
        (tmp_path / "presentation-evidence.json").read_text(encoding="utf-8")
    )
    source_id_by_path = {item["path"]: item["id"] for item in evidence["sources"]}
    transcript_source = next(
        item for item in evidence["sources"] if item["id"] == "source-transcript"
    )
    assert transcript_source["normalized_from"] == source_id_by_path[selected]


def test_nested_manifest_uses_run_relative_frame_paths(tmp_path: Path) -> None:
    metadata = tmp_path / "metadata"
    frames = tmp_path / "frames"
    metadata.mkdir()
    frames.mkdir()
    (frames / "frame.png").write_bytes(b"frame")
    (metadata / "frames_manifest.md").write_text(
        "| File | Timestamp | Description |\n"
        "| frames/frame.png | 00:05 | Product demo screen |\n",
        encoding="utf-8",
    )
    command = [
        "python3",
        str(BUILDER_PATH),
        "--run",
        str(tmp_path),
        "--frames-manifest",
        "metadata/frames_manifest.md",
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)
    evidence_path = tmp_path / "presentation-evidence.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    assert evidence["frames"][0]["path"] == "frames/frame.png"
    assert evidence["frames"][0]["timestamp_seconds"] == 5
    assert VALIDATOR.validate_files(evidence, evidence_path) == []


def test_image_only_bundle_allows_directory_source(tmp_path: Path) -> None:
    images = tmp_path / "slide_images"
    images.mkdir()
    (images / "slide_1.png").write_bytes(b"png")
    evidence = build_with_cli(tmp_path)
    evidence_path = tmp_path / "presentation-evidence.json"
    assert VALIDATOR.validate_files(evidence, evidence_path) == []


def test_outline_only_bundle_creates_a_resolvable_source(tmp_path: Path) -> None:
    (tmp_path / "outline.txt").write_text("1. Opening summary\n", encoding="utf-8")
    evidence = build_with_cli(tmp_path)
    assert evidence["slides"][0]["source_id"] == "source-slide-artifacts"
    source_ids = {source["id"] for source in evidence["sources"]}
    assert "source-slide-artifacts" in source_ids


def test_external_output_preserves_run_as_bundle_root(tmp_path: Path) -> None:
    run = tmp_path / "run"
    output_dir = tmp_path / "contracts"
    run.mkdir()
    output_dir.mkdir()
    (run / "slides.pdf").write_bytes(b"pdf")
    output = output_dir / "presentation-evidence.json"
    evidence = build_with_cli(run, output)
    assert evidence["bundle"]["root"] == "../run"
    assert VALIDATOR.validate_files(evidence, output) == []


def test_file_validation_rejects_checksum_drift(tmp_path: Path) -> None:
    source = tmp_path / "video.mp4"
    source.write_bytes(b"original")
    evidence = build_with_cli(tmp_path)
    evidence_path = tmp_path / "presentation-evidence.json"
    assert VALIDATOR.validate_files(evidence, evidence_path) == []
    source.write_bytes(b"changed")
    failures = VALIDATOR.validate_files(evidence, evidence_path)
    assert any("source source-01: checksum mismatch" in failure for failure in failures)


def test_greenfield_slide_plan_allows_null_evidence_contract() -> None:
    schema = json.loads(
        (
            ROOT
            / "skills"
            / "pptx-visual-spec"
            / "references"
            / "slide-plan-schema.json"
        ).read_text(encoding="utf-8")
    )
    template = json.loads(
        (
            ROOT
            / "skills"
            / "pptx-visual-spec"
            / "assets"
            / "slide-plan.template.json"
        ).read_text(encoding="utf-8")
    )
    template["deck"]["evidence_contract"] = None
    errors = list(VALIDATOR.Draft202012Validator(schema).iter_errors(template))
    assert errors == []
