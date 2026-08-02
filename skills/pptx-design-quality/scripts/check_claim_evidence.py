#!/usr/bin/env python3
"""Deterministic claim-vs-evidence consistency check for a slide-plan.json.

Generalizes video-to-deck's Grill-Me claim check and the Genspark
factual-integrity checklist into a reusable mechanical pre-pass any
evidence-derived deck can run, not only video- or Genspark-sourced ones.
Does not replace either richer, semantic review procedure — this is a fast,
deterministic first pass only: regex number matching, not claim verification.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


NUMBER_TOKEN = re.compile(r"\$?\d[\d,]*\.?\d*%?[MBKmbk]?")


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    message: str
    claim_id: str


def _normalize(token: str) -> str:
    return token.replace(",", "").lower()


def _numbers_in(text: str) -> set[str]:
    return {_normalize(match) for match in NUMBER_TOKEN.findall(text)}


def _evidence_corpus(evidence: dict[str, Any], evidence_ids: list[str]) -> tuple[str, bool]:
    """Concatenate cited evidence text; report whether any of it has text at all."""
    slides_by_id = {item["id"]: item for item in evidence.get("slides", [])}
    segments_by_id = {item["id"]: item for item in evidence.get("transcript_segments", [])}
    frames_by_id = {item["id"]: item for item in evidence.get("frames", [])}

    texts: list[str] = []
    has_any_text = False
    for evidence_id in evidence_ids:
        record = slides_by_id.get(evidence_id) or segments_by_id.get(evidence_id) or frames_by_id.get(evidence_id)
        if record is None:
            continue
        text = record.get("extracted_text") or record.get("text") or record.get("description")
        if text:
            texts.append(text)
            has_any_text = True
    return "\n".join(texts), has_any_text


def check(evidence: dict[str, Any], plan: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    if plan.get("deck", {}).get("evidence_contract") is None:
        return findings

    for claim in plan.get("claims", []):
        if claim.get("kind") not in {"fact", "metric"}:
            continue

        corpus, has_text = _evidence_corpus(evidence, claim.get("evidence_ids", []))
        if not has_text:
            findings.append(
                Finding(
                    rule_id="UNVERIFIABLE_EVIDENCE",
                    severity="warning",
                    message="claim's cited evidence has no extractable text to check against",
                    claim_id=claim["id"],
                )
            )
            continue

        unsourced = sorted(_numbers_in(claim.get("text", "")) - _numbers_in(corpus))
        for number in unsourced:
            findings.append(
                Finding(
                    rule_id="UNSOURCED_NUMBER",
                    severity="error",
                    message=f"number {number!r} in claim text does not appear in its cited evidence",
                    claim_id=claim["id"],
                )
            )
    return findings


def _apply_waivers(findings: list[Finding], config: dict[str, Any] | None) -> list[Finding]:
    if not config:
        return findings
    ignored = set(config.get("qa", {}).get("ignore_rules", []))
    return [finding for finding in findings if finding.rule_id not in ignored]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path, help="presentation-evidence.json")
    parser.add_argument("slide_plan", type=Path, help="slide-plan.json")
    parser.add_argument("--config", type=Path, help="deck-design.json (for qa.ignore_rules waivers)")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text")
    parser.add_argument("--out", type=Path, help="Write the JSON report to this path")
    args = parser.parse_args()

    try:
        evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
        plan = json.loads(args.slide_plan.read_text(encoding="utf-8"))
        config = json.loads(args.config.read_text(encoding="utf-8")) if args.config else None
    except (OSError, json.JSONDecodeError) as exc:
        print(f"check failed: {exc}", file=sys.stderr)
        return 1

    findings = _apply_waivers(check(evidence, plan), config)
    report = {
        "status": "clean" if not findings else "findings",
        "findings": [asdict(finding) for finding in findings],
    }

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif not findings:
        print("clean: no unsourced numbers or unverifiable evidence")
    else:
        for finding in findings:
            print(f"- {finding.severity.upper()} {finding.rule_id} ({finding.claim_id}): {finding.message}")

    return 0 if not findings else 2


if __name__ == "__main__":
    raise SystemExit(main())
