from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REGISTRY = Path(__file__).resolve().parents[1] / "references" / "skill-registry.json"


def test_external_capabilities_have_portable_fallbacks() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    capabilities = registry["external_capabilities"]
    sources = {entry["name"]: ROOT / entry["source"] for entry in registry["skills"] if "source" in entry}
    assert len({entry["name"] for entry in capabilities}) == len(capabilities)
    for entry in capabilities:
        fallback = sources[entry["fallback_skill"]] / "SKILL.md"
        assert fallback.exists(), f"missing fallback skill for {entry['name']}"


def test_ai_analyst_is_a_complete_mirror() -> None:
    mirror = Path(__file__).resolve().parents[1] / "portable-skills" / "ai-analyst"
    assert (mirror / "LICENSE").is_file()
    assert (mirror / "export-results" / "SKILL.md").is_file()
    assert len(list(mirror.glob("*/SKILL.md"))) >= 30
