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
VALIDATOR = SKILL_DIR / "scripts/validate_template_profile.py"
INITIALIZER = SKILL_DIR / "scripts/init_deck_context.py"
TEMPLATE = SKILL_DIR / "assets/template-profile.template.json"


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        check=False,
        capture_output=True,
        text=True,
    )


def test_shipped_template_is_valid() -> None:
    result = run_validator(TEMPLATE)
    assert result.returncode == 0, result.stderr


def test_unknown_archetype_is_rejected(tmp_path: Path) -> None:
    profile = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    profile["archetypes"].append("invented-layout")
    path = tmp_path / "template-profile.json"
    path.write_text(json.dumps(profile), encoding="utf-8")

    result = run_validator(path)

    assert result.returncode == 1
    assert "unknown archetype invented-layout" in result.stderr


def test_initializer_creates_all_design_contracts(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(INITIALIZER), "--run", str(tmp_path), "--title", "Client deck"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert (tmp_path / "deck-brief.md").is_file()
    assert (tmp_path / "deck-design.json").is_file()
    assert (tmp_path / "template-profile.json").is_file()
