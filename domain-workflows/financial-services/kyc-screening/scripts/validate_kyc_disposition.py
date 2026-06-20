#!/usr/bin/env python3
"""Validate a KYC screening workflow output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED_RISK = {"low", "medium", "high"}
ALLOWED_DISPOSITIONS = {
    "clear",
    "request-docs",
    "escalate-EDD",
    "decline-recommend",
}
FORBIDDEN_FINAL_DECISION_TERMS = [
    "approved",
    "approval granted",
    "accept client",
    "client accepted",
    "clear to onboard",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def doc_status(record: dict[str, Any]) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for doc in record.get("documents_received", []):
        if isinstance(doc, dict) and doc.get("type"):
            statuses[str(doc["type"])] = str(doc.get("status", "received"))
    return statuses


def expected_missing_documents(record: dict[str, Any], rules: dict[str, Any]) -> set[str]:
    applicant_type = str(record.get("applicant_type", ""))
    required = rules.get("requiredDocuments", {}).get(applicant_type, [])
    statuses = doc_status(record)
    missing = set()
    for doc_name in required:
        if statuses.get(doc_name) in {None, "expired"}:
            missing.add(doc_name)
    return missing


def rule_ids(disposition: dict[str, Any]) -> set[str]:
    return {
        str(outcome.get("rule_id"))
        for outcome in disposition.get("rule_outcomes", [])
        if isinstance(outcome, dict)
    }


def validate(
    disposition: dict[str, Any],
    record: dict[str, Any],
    rules: dict[str, Any],
    expected_minimum: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []

    if disposition.get("risk_rating") not in ALLOWED_RISK:
        errors.append("risk_rating must be low, medium, or high")

    if disposition.get("disposition") not in ALLOWED_DISPOSITIONS:
        errors.append("disposition has an unsupported value")

    outcomes = disposition.get("rule_outcomes")
    if not isinstance(outcomes, list) or not outcomes:
        errors.append("rule_outcomes must be a non-empty list")
    else:
        for idx, outcome in enumerate(outcomes):
            if not isinstance(outcome, dict):
                errors.append(f"rule_outcomes[{idx}] must be an object")
                continue
            for key in ("rule_id", "outcome", "evidence"):
                if not outcome.get(key):
                    errors.append(f"rule_outcomes[{idx}] missing {key}")
            if outcome.get("outcome") not in {"pass", "fail", "n/a"}:
                errors.append(f"rule_outcomes[{idx}] has unsupported outcome")

    expected_missing = expected_missing_documents(record, rules)
    actual_missing = set(disposition.get("missing_documents", []))
    if not expected_missing.issubset(actual_missing):
        errors.append(
            "missing_documents does not include expected required docs: "
            + ", ".join(sorted(expected_missing - actual_missing))
        )

    ids = rule_ids(disposition)
    screening = record.get("screening_results", {})
    pep_declared = any(
        bool(owner.get("pep_declared"))
        for owner in record.get("beneficial_owners", [])
        if isinstance(owner, dict)
    )
    if screening.get("pep") == "confirmed" or pep_declared:
        if disposition.get("risk_rating") != "high":
            errors.append("confirmed or declared PEP exposure must set risk_rating=high")
        if disposition.get("disposition") not in {"escalate-EDD", "decline-recommend"}:
            errors.append("confirmed or declared PEP exposure must route to escalation")
        if "R-PEP-001" not in ids:
            errors.append("confirmed or declared PEP exposure must cite R-PEP-001")

    if screening.get("sanctions") == "confirmed":
        if disposition.get("disposition") != "decline-recommend":
            errors.append("confirmed sanctions must route to decline-recommend")
        if "R-SAN-001" not in ids:
            errors.append("confirmed sanctions must cite R-SAN-001")

    if screening.get("adverse_media") in {"confirmed", "possible-hit"}:
        if disposition.get("disposition") not in {"escalate-EDD", "decline-recommend"}:
            errors.append("adverse media hit must route to escalation")
        if "R-AM-001" not in ids:
            errors.append("adverse media hit must cite R-AM-001")

    if expected_missing and "R-DOC-001" not in ids:
        errors.append("missing required documents must cite R-DOC-001")

    if "source_of_funds" in expected_missing and "R-SOF-001" not in ids:
        errors.append("missing source_of_funds must cite R-SOF-001")

    serialized = json.dumps(disposition, sort_keys=True).lower()
    for term in FORBIDDEN_FINAL_DECISION_TERMS:
        if term in serialized:
            errors.append(f"forbidden final-decision term found: {term}")

    if disposition.get("human_review_required") is False and disposition.get("disposition") != "clear":
        errors.append("non-clear dispositions must require human review")

    if expected_minimum:
        if expected_minimum.get("risk_rating") and disposition.get("risk_rating") != expected_minimum["risk_rating"]:
            errors.append(
                "risk_rating does not match expected minimum: "
                + str(expected_minimum["risk_rating"])
            )
        if expected_minimum.get("disposition") and disposition.get("disposition") != expected_minimum["disposition"]:
            errors.append(
                "disposition does not match expected minimum: "
                + str(expected_minimum["disposition"])
            )
        expected_docs = set(expected_minimum.get("missing_documents", []))
        if not expected_docs.issubset(set(disposition.get("missing_documents", []))):
            errors.append(
                "missing_documents does not match expected minimum: "
                + ", ".join(sorted(expected_docs - set(disposition.get("missing_documents", []))))
            )
        expected_rule_ids = set(expected_minimum.get("must_include_rule_ids", []))
        if not expected_rule_ids.issubset(ids):
            errors.append(
                "rule_outcomes does not include expected rule ids: "
                + ", ".join(sorted(expected_rule_ids - ids))
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("disposition", type=Path)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--rules", type=Path, required=True)
    parser.add_argument("--expected-minimum", type=Path)
    args = parser.parse_args()

    disposition = load_json(args.disposition)
    record = load_json(args.input)
    rules = load_json(args.rules)
    expected_minimum = load_json(args.expected_minimum) if args.expected_minimum else None

    errors = validate(disposition, record, rules, expected_minimum)
    result = {
        "status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
