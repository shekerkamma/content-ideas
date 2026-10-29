#!/usr/bin/env python3
"""Validate a DeepGrid competitor dossier before downstream use."""

import json
import re
import sys
from pathlib import Path

THREATS = {"NONE", "LOW", "MEDIUM", "HIGH", "NOT_ASSESSABLE"}
STATUSES = {"VERIFIED", "COMPANY_CLAIM", "INFERRED", "UNAVAILABLE", "CONFLICTED"}
OWNERS = {"Head of Sales", "CEO", "BD", "Engineering", "CFO", "VP Silicon"}
RETIRED = [
    r"39\.3\s*TOPS",
    r"12\.9x\s+cheaper",
    r"\b(?:84|88)%\s+gross margin",
    r"mandate[- ]ready",
    r"mandate live since April 2026",
]
PLAN_NUMBERS = [r"63[,.]?250", r"65[,.]?000", r"1[,.]?750", r"45%", r"72%"]


def fail(errors, message):
    errors.append(message)


def main(path_string):
    path = Path(path_string)
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = []
    text = json.dumps(data, ensure_ascii=False)

    if data.get("schema_version") != 1:
        fail(errors, "schema_version must be 1")
    competitor = data.get("competitor", {})
    if not competitor.get("name") or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", competitor.get("as_of", "")):
        fail(errors, "competitor.name and ISO competitor.as_of are required")

    for key in ("A", "B", "C"):
        segment = data.get("segments", {}).get(key, {})
        if segment.get("threat") not in THREATS:
            fail(errors, f"Segment {key} threat must be one of {sorted(THREATS)}")
        if not segment.get("justification"):
            fail(errors, f"Segment {key} requires justification")

    evidence = data.get("evidence", [])
    evidence_ids = set()
    for i, item in enumerate(evidence):
        eid = item.get("evidence_id")
        if not eid or eid in evidence_ids:
            fail(errors, f"evidence[{i}] requires a unique evidence_id")
        evidence_ids.add(eid)
        if item.get("status") not in STATUSES:
            fail(errors, f"evidence[{i}] has invalid status")
        if item.get("status") in {"VERIFIED", "COMPANY_CLAIM", "CONFLICTED"} and not item.get("source_url"):
            fail(errors, f"evidence[{i}] requires source_url for status {item.get('status')}")

    for segment_name, segment in data.get("segments", {}).items():
        for eid in segment.get("evidence_ids", []):
            if eid not in evidence_ids:
                fail(errors, f"Segment {segment_name} references unknown evidence ID {eid}")

    moves = data.get("counter_moves", [])
    if not 3 <= len(moves) <= 5:
        fail(errors, "counter_moves must contain 3 to 5 moves")
    for i, move in enumerate(moves):
        if move.get("owner") not in OWNERS:
            fail(errors, f"counter_moves[{i}] owner must use the allowed owner vocabulary")
        for field in ("action", "done_when", "trigger", "stop_or_escalate"):
            if not move.get(field):
                fail(errors, f"counter_moves[{i}] requires {field}")

    for pattern in RETIRED:
        if re.search(pattern, text, flags=re.I):
            fail(errors, f"retired claim detected: {pattern}")
    if re.search(r"\bASIL[- ]?D\b", text, flags=re.I) and not re.search(r"(?:does not|not|no)\s+(?:hold|have|claim|certif|achiev).{0,30}ASIL[- ]?D", text, flags=re.I):
        fail(errors, "ASIL-D appears without an explicit negative/qualified context")
    for pattern in PLAN_NUMBERS:
        for match in re.finditer(pattern, text, flags=re.I):
            window = text[max(0, match.start() - 120): match.end() + 120]
            if "PLAN FIGURE" not in window:
                fail(errors, f"DeepGrid planning number lacks nearby PLAN FIGURE label: {match.group(0)}")

    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALID: {competitor['name']} ({len(evidence)} evidence records)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_dossier.py <dossier.json>")
    raise SystemExit(main(sys.argv[1]))
