from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parents[1]
LINTER = SKILL_DIR / "scripts/lint_motion.py"
SCHEMA = SKILL_DIR / "references/deck-design-schema.json"

# Namespaces exactly as PowerPoint writes them. officecli emits p159 (the
# 2015/09 morph namespace), not p14, so these fixtures use p159 to keep the
# linter's namespace-agnostic matching honest.
NS_P159 = "http://schemas.microsoft.com/office/powerpoint/2015/09/main"
NS_MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"

MORPH_WITH_FADE_FALLBACK = (
    f'<mc:AlternateContent xmlns:mc="{NS_MC}">'
    f'<mc:Choice Requires="p159">'
    f'<p:transition xmlns:p159="{NS_P159}"><p159:morph option="byObject"/></p:transition>'
    f"</mc:Choice>"
    f"<mc:Fallback><p:transition><p:fade/></p:transition></mc:Fallback>"
    f"</mc:AlternateContent>"
)

EXIT_TIMING = (
    '<p:timing><p:tnLst><p:par><p:cTn id="1" presetClass="exit" presetID="10">'
    "</p:cTn></p:par></p:tnLst></p:timing>"
)

ENTRANCE_TIMING = (
    '<p:timing><p:tnLst><p:par><p:cTn id="1" presetClass="entr" presetID="10">'
    "</p:cTn></p:par></p:tnLst></p:timing>"
)


def _slide_xml(*fragments: str) -> bytes:
    body = "".join(fragments)
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
        ' xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        "<p:cSld><p:spTree/></p:cSld>"
        f"{body}"
        "</p:sld>"
    ).encode("utf-8")


def make_deck(path: Path, slides: list[str]) -> Path:
    with zipfile.ZipFile(path, "w") as archive:
        for index, fragments in enumerate(slides, start=1):
            archive.writestr(f"ppt/slides/slide{index}.xml", _slide_xml(fragments))
    return path


def contract(**overrides: object) -> dict:
    motion = {
        "allowed_transitions": ["morph", "fade", "none"],
        "max_transition_ms": 1000,
        "allowed_effect_classes": ["entrance", "emphasis"],
        "max_build_steps_per_slide": 6,
        "require_transition": False,
    }
    motion.update(overrides)
    return {"motion": motion, "qa": {"ignore_rules": [], "waivers": {}}}


def run_linter(deck: Path, config: Path | None = None) -> subprocess.CompletedProcess[str]:
    argv = [sys.executable, str(LINTER), str(deck), "--json"]
    if config is not None:
        argv += ["--config", str(config)]
    return subprocess.run(argv, check=False, capture_output=True, text=True)


def rule_ids(result: subprocess.CompletedProcess[str]) -> list[str]:
    return [f["rule_id"] for f in json.loads(result.stdout)["findings"]]


def write(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_motion_is_optional_in_schema() -> None:
    """A deck-design.json without 'motion' must stay valid — this addition
    cannot break contracts already on disk."""
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert "motion" in schema["properties"]
    assert "motion" not in schema["required"]


def test_no_contract_reports_nothing(tmp_path: Path) -> None:
    deck = make_deck(tmp_path / "d.pptx", [MORPH_WITH_FADE_FALLBACK + EXIT_TIMING])
    result = run_linter(deck)
    assert result.returncode == 0
    assert json.loads(result.stdout)["motion_contract"] is False


def test_compliant_deck_is_clean(tmp_path: Path) -> None:
    deck = make_deck(tmp_path / "d.pptx", [MORPH_WITH_FADE_FALLBACK + ENTRANCE_TIMING])
    cfg = write(tmp_path / "c.json", contract())
    result = run_linter(deck, cfg)
    assert result.returncode == 0, result.stdout
    assert rule_ids(result) == []


def test_exit_animation_is_an_error(tmp_path: Path) -> None:
    """The load-bearing rule: content that exits is absent from the resting
    frame, so contact sheets and PDF export silently lose it."""
    deck = make_deck(tmp_path / "d.pptx", [EXIT_TIMING])
    cfg = write(tmp_path / "c.json", contract())
    result = run_linter(deck, cfg)
    assert result.returncode == 2
    findings = json.loads(result.stdout)["findings"]
    assert [f["rule_id"] for f in findings] == ["MOTION_EXIT_BREAKS_REST_STATE"]
    assert findings[0]["severity"] == "error"


def test_exit_allowed_when_declared(tmp_path: Path) -> None:
    deck = make_deck(tmp_path / "d.pptx", [EXIT_TIMING])
    cfg = write(
        tmp_path / "c.json",
        contract(allowed_effect_classes=["entrance", "emphasis", "exit"]),
    )
    assert run_linter(deck, cfg).returncode == 0


def test_off_contract_transition_is_flagged(tmp_path: Path) -> None:
    deck = make_deck(tmp_path / "d.pptx", ["<p:transition><p:vortex/></p:transition>"])
    cfg = write(tmp_path / "c.json", contract())
    assert "MOTION_TRANSITION_OFF_CONTRACT" in rule_ids(run_linter(deck, cfg))


def test_morph_choice_wins_over_fade_fallback(tmp_path: Path) -> None:
    """mc:Fallback carries <p:fade/>. Counting it would both double-report and
    describe a transition the audience never sees."""
    deck = make_deck(tmp_path / "d.pptx", [MORPH_WITH_FADE_FALLBACK])
    cfg = write(tmp_path / "c.json", contract(allowed_transitions=["morph"]))
    result = run_linter(deck, cfg)
    assert result.returncode == 0, result.stdout


def test_animeffect_transition_attribute_is_not_a_slide_transition(
    tmp_path: Path,
) -> None:
    """<p:animEffect transition="out"> lives in the timing tree. Matching on the
    attribute instead of the element name would invent a transition here."""
    deck = make_deck(
        tmp_path / "d.pptx",
        [
            '<p:timing><p:tnLst><p:par><p:cTn id="1" presetClass="entr">'
            '<p:animEffect transition="out" filter="fade"/>'
            "</p:cTn></p:par></p:tnLst></p:timing>"
        ],
    )
    cfg = write(tmp_path / "c.json", contract(allowed_transitions=["morph"]))
    assert "MOTION_TRANSITION_OFF_CONTRACT" not in rule_ids(run_linter(deck, cfg))


@pytest.mark.parametrize(
    ("attr", "expected"),
    [('p14:dur="2500"', True), ('spd="slow"', False), ("", False)],
)
def test_transition_duration_cap(tmp_path: Path, attr: str, expected: bool) -> None:
    ns = ' xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main"'
    deck = make_deck(
        tmp_path / "d.pptx", [f"<p:transition{ns} {attr}><p:fade/></p:transition>"]
    )
    cfg = write(tmp_path / "c.json", contract(max_transition_ms=1000))
    flagged = "MOTION_TRANSITION_TOO_LONG" in rule_ids(run_linter(deck, cfg))
    assert flagged is expected


def test_build_step_budget(tmp_path: Path) -> None:
    steps = "".join(
        f'<p:cTn id="{i}" presetClass="entr"></p:cTn>' for i in range(1, 5)
    )
    deck = make_deck(tmp_path / "d.pptx", [f"<p:timing><p:tnLst>{steps}</p:tnLst></p:timing>"])
    cfg = write(tmp_path / "c.json", contract(max_build_steps_per_slide=3))
    assert "MOTION_BUILD_TOO_LONG" in rule_ids(run_linter(deck, cfg))


def test_missing_transition_only_when_required(tmp_path: Path) -> None:
    deck = make_deck(tmp_path / "d.pptx", [""])
    lenient = write(tmp_path / "a.json", contract(require_transition=False))
    assert rule_ids(run_linter(deck, lenient)) == []
    strict = write(
        tmp_path / "b.json",
        contract(require_transition=True, allowed_transitions=["morph"]),
    )
    assert "MOTION_TRANSITION_MISSING" in rule_ids(run_linter(deck, strict))


def test_warning_is_waivable_but_error_is_not(tmp_path: Path) -> None:
    deck = make_deck(
        tmp_path / "d.pptx", ["<p:transition><p:vortex/></p:transition>" + EXIT_TIMING]
    )
    payload = contract()
    payload["qa"] = {
        "ignore_rules": [
            "MOTION_TRANSITION_OFF_CONTRACT",
            "MOTION_EXIT_BREAKS_REST_STATE",
        ],
        "waivers": {
            "MOTION_TRANSITION_OFF_CONTRACT": "vortex approved for the divider",
            "MOTION_EXIT_BREAKS_REST_STATE": "attempted waiver of an error",
        },
    }
    cfg = write(tmp_path / "c.json", payload)
    result = run_linter(deck, cfg)
    assert result.returncode == 2
    assert rule_ids(result) == ["MOTION_EXIT_BREAKS_REST_STATE"]


def test_deck_with_no_slides(tmp_path: Path) -> None:
    deck = make_deck(tmp_path / "d.pptx", [])
    cfg = write(tmp_path / "c.json", contract())
    assert "DECK_NO_SLIDES" in rule_ids(run_linter(deck, cfg))
