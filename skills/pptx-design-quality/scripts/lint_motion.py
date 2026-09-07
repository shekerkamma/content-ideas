#!/usr/bin/env python3
"""Lint PPTX slide transitions and animation builds against the motion contract.

Static contact sheets and Office render QA both inspect resting frames, so they
cannot see motion at all. This linter closes that gap by reading the transition
and timing XML directly out of the package.

It deliberately does not shell out to `officecli`. `officecli` is the authoring
tool for motion; reading the XML back independently keeps the check from being
derived from the same abstraction that wrote it.
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"
NS_MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"

# OOXML presetClass token -> the contract's vocabulary.
PRESET_CLASSES = {
    "entr": "entrance",
    "exit": "exit",
    "emph": "emphasis",
    "path": "path",
}

# Non-effect children of <p:transition> that never name the transition type.
_TRANSITION_NOISE = {"sndAc", "sound", "extLst"}

# PowerPoint's named speeds, in milliseconds, used when p14:dur is absent.
_SPEED_MS = {"slow": 1000, "med": 500, "fast": 250}

DEFAULTS: dict[str, Any] = {
    "motion": None,
    "qa": {"ignore_rules": [], "waivers": {}},
}


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    message: str
    slide: int | None = None
    shape: str | None = None


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def load_config(path: Path | None) -> dict[str, Any]:
    merged = json.loads(json.dumps(DEFAULTS))
    if path is None:
        return merged
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(raw.get("motion"), dict):
        merged["motion"] = raw["motion"]
    if isinstance(raw.get("qa"), dict):
        merged["qa"] = {**merged["qa"], **raw["qa"]}
    return merged


def _slide_parts(archive: zipfile.ZipFile) -> list[str]:
    names = [
        name
        for name in archive.namelist()
        if name.startswith("ppt/slides/slide") and name.endswith(".xml")
    ]

    def order(name: str) -> int:
        digits = "".join(c for c in Path(name).stem if c.isdigit())
        return int(digits) if digits else 0

    return sorted(names, key=order)


def _effective_transitions(root: ET.Element) -> list[ET.Element]:
    """Return transitions, taking mc:Choice over mc:Fallback so a morph with a
    fade fallback is counted once, as the morph the audience actually sees."""
    chosen: list[ET.Element] = []
    for alt in root.iter(f"{{{NS_MC}}}AlternateContent"):
        choice = alt.find(f"{{{NS_MC}}}Choice")
        branch = choice if choice is not None else alt.find(f"{{{NS_MC}}}Fallback")
        if branch is not None:
            chosen.extend(
                node for node in branch.iter() if _local(node.tag) == "transition"
            )
    if chosen:
        return chosen
    return [node for node in root.iter() if _local(node.tag) == "transition"]


def _transition_kind(transition: ET.Element) -> str | None:
    for child in transition:
        name = _local(child.tag)
        if name in _TRANSITION_NOISE:
            continue
        return name
    return None


def _transition_ms(transition: ET.Element) -> tuple[int | None, bool]:
    """(duration_ms, exact). exact=False means it was inferred from spd=."""
    raw = transition.get(f"{{{NS_P14}}}dur") or transition.get("dur")
    if raw is not None:
        try:
            return int(raw), True
        except ValueError:
            return None, True
    speed = transition.get("spd")
    if speed in _SPEED_MS:
        return _SPEED_MS[speed], False
    return None, True


def _build_steps(root: ET.Element) -> list[str]:
    """Animation classes on this slide, one entry per effect node."""
    steps: list[str] = []
    for node in root.iter():
        if _local(node.tag) != "cTn":
            continue
        preset = node.get("presetClass")
        if preset in PRESET_CLASSES:
            steps.append(PRESET_CLASSES[preset])
    return steps


def lint_motion(pptx_path: Path, config: dict[str, Any]) -> dict[str, Any]:
    motion = config.get("motion")
    findings: list[Finding] = []

    with zipfile.ZipFile(pptx_path) as archive:
        slides = _slide_parts(archive)
        if not slides:
            findings.append(
                Finding("DECK_NO_SLIDES", "error", "Presentation contains no slides.")
            )
        parsed = [
            (index, ET.fromstring(archive.read(name)))
            for index, name in enumerate(slides, start=1)
        ]

    if motion is None:
        return _report(pptx_path, findings, config, contract=False)

    allowed_transitions = {t.lower() for t in motion["allowed_transitions"]}
    allowed_classes = set(motion["allowed_effect_classes"])
    max_ms = motion["max_transition_ms"]
    max_steps = motion["max_build_steps_per_slide"]
    require_transition = motion["require_transition"]

    for index, root in parsed:
        transitions = _effective_transitions(root)
        kinds = [k for k in (_transition_kind(t) for t in transitions) if k]

        if not kinds:
            if require_transition and "none" not in allowed_transitions:
                findings.append(
                    Finding(
                        "MOTION_TRANSITION_MISSING",
                        "warning",
                        "Slide declares no transition but the motion contract "
                        "requires one.",
                        index,
                    )
                )
        for transition, kind in zip(transitions, kinds):
            if kind.lower() not in allowed_transitions:
                findings.append(
                    Finding(
                        "MOTION_TRANSITION_OFF_CONTRACT",
                        "warning",
                        f"Transition '{kind}' is not in the contract's allowed set "
                        f"({', '.join(sorted(allowed_transitions))}).",
                        index,
                    )
                )
            duration, exact = _transition_ms(transition)
            if duration is not None and duration > max_ms:
                qualifier = "" if exact else " (inferred from spd=)"
                findings.append(
                    Finding(
                        "MOTION_TRANSITION_TOO_LONG",
                        "warning",
                        f"Transition runs {duration}ms{qualifier}; the contract "
                        f"allows {max_ms}ms.",
                        index,
                    )
                )

        steps = _build_steps(root)
        if len(steps) > max_steps:
            findings.append(
                Finding(
                    "MOTION_BUILD_TOO_LONG",
                    "warning",
                    f"Slide has {len(steps)} animation steps; the contract allows "
                    f"{max_steps}.",
                    index,
                )
            )
        for effect_class, count in sorted(Counter(steps).items()):
            if effect_class in allowed_classes:
                continue
            if effect_class == "exit":
                findings.append(
                    Finding(
                        "MOTION_EXIT_BREAKS_REST_STATE",
                        "error",
                        f"Slide has {count} exit animation(s). Content that exits is "
                        "absent from the slide's resting state, so it is missing from "
                        "PDF export, contact sheets, and Office render QA. Allow "
                        "'exit' in motion.allowed_effect_classes only if that is "
                        "deliberate.",
                        index,
                    )
                )
            else:
                findings.append(
                    Finding(
                        "MOTION_EFFECT_CLASS_OFF_CONTRACT",
                        "warning",
                        f"Slide uses {count} '{effect_class}' animation(s), which the "
                        "contract does not permit.",
                        index,
                    )
                )

    return _report(pptx_path, findings, config, contract=True)


def _report(
    pptx_path: Path,
    findings: list[Finding],
    config: dict[str, Any],
    *,
    contract: bool,
) -> dict[str, Any]:
    qa = config.get("qa", {})
    ignored_rules = set(qa.get("ignore_rules", []))
    waiver_reasons = qa.get("waivers", {})

    def is_valid_waiver(finding: Finding) -> bool:
        reason = waiver_reasons.get(finding.rule_id)
        return (
            finding.severity == "warning"
            and finding.rule_id in ignored_rules
            and isinstance(reason, str)
            and bool(reason.strip())
        )

    active = [f for f in findings if not is_valid_waiver(f)]
    ignored = [f for f in findings if is_valid_waiver(f)]
    counts = Counter(f.severity for f in active)
    return {
        "contract_version": "1.0",
        "file": str(pptx_path),
        "motion_contract": contract,
        "status": "clean" if not active else "findings",
        "counts": {
            "error": counts.get("error", 0),
            "warning": counts.get("warning", 0),
            "ignored": len(ignored),
        },
        "findings": [asdict(f) for f in active],
        "ignored_findings": [asdict(f) for f in ignored],
    }


def _print_text(report: dict[str, Any]) -> None:
    if not report["motion_contract"]:
        print(
            f"no motion contract: {report['file']} "
            "(deck-design.json declares no 'motion' block; nothing to enforce)"
        )
        return
    print(
        f"{report['status']}: {report['file']} "
        f"({report['counts']['error']} errors, "
        f"{report['counts']['warning']} warnings)"
    )
    for finding in report["findings"]:
        location = f" slide {finding['slide']}" if finding["slide"] is not None else ""
        print(
            f"- {finding['severity'].upper()} {finding['rule_id']}{location}: "
            f"{finding['message']}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", help="PowerPoint file to inspect")
    parser.add_argument("--config", type=Path, help="deck-design.json path")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text")
    parser.add_argument("--out", type=Path, help="Write the JSON report to this path")
    args = parser.parse_args()

    pptx_path = Path(args.pptx)
    try:
        if not pptx_path.is_file():
            raise FileNotFoundError(pptx_path)
        report = lint_motion(pptx_path, load_config(args.config))
    except (
        OSError,
        KeyError,
        TypeError,
        ValueError,
        json.JSONDecodeError,
        zipfile.BadZipFile,
        ET.ParseError,
    ) as exc:
        print(f"motion lint failed: {exc}", file=sys.stderr)
        return 1

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        _print_text(report)
    return 0 if report["status"] == "clean" else 2


if __name__ == "__main__":
    raise SystemExit(main())
