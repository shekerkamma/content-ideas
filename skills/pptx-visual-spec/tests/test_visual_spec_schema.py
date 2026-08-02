import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "references" / "visual-spec-schema.json").read_text())


def base_spec(route: str, evidence_status: str) -> dict:
    return {
        "contract_version": "1.0",
        "deck": {"output_mode": "native", "editability": "native slide shell", "reference_deck": None},
        "visuals": [
            {
                "id": "visual-1",
                "slide_ids": [1],
                "purpose": "Test visual",
                "artifact_type": "illustration",
                "evidence_status": evidence_status,
                "route": route,
                "reason": "Contract test",
                "source": None,
                "asset": None,
                "editable_source": None,
                "prompt_file": None,
                "execution": None,
                "placement": None,
                "qa": {
                    "visual_checked": True,
                    "legible": True,
                    "not_cropped": True,
                    "background_matched": None,
                    "provenance_recorded": True,
                    "text_free": None,
                    "not_evidence": None,
                    "exact_fidelity": None,
                },
            }
        ],
    }


def errors(spec: dict) -> list:
    return list(Draft202012Validator(SCHEMA).iter_errors(spec))


def test_native_visual_is_valid():
    assert not errors(base_spec("native", "underlying-information"))


def test_image_model_requires_text_free_non_evidence_and_execution():
    spec = base_spec("image-model", "generated-illustrative")
    assert errors(spec)

    visual = spec["visuals"][0]
    visual.update(
        asset="assets/generated/cover.png",
        prompt_file="prompts/cover.txt",
        execution={
            "path": "codex-built-in-image_gen",
            "auth_mode": "chatgpt-subscription",
            "orchestration_model": "codex",
            "requested_engine": None,
            "resolved_engine": None,
        },
        placement={"width": 1536, "height": 1024, "fit": "cover", "background": "#0A1628"},
    )
    visual["qa"]["text_free"] = True
    visual["qa"]["not_evidence"] = True
    assert not errors(spec)


def test_extract_requires_exact_source_and_fidelity():
    spec = base_spec("extract", "exact-source-evidence")
    assert errors(spec)

    visual = spec["visuals"][0]
    visual["source"] = {"path": "source.pdf", "page": 2, "frame": None, "timestamp": None, "crop": None}
    visual["asset"] = "assets/extracted/figure.png"
    visual["qa"]["exact_fidelity"] = True
    assert not errors(spec)
