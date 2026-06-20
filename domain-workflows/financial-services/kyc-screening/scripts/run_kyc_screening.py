#!/usr/bin/env python3
"""Run a local KYC/AML screening workflow.

This script intentionally keeps the business rules explicit and auditable. It is
not a replacement for a firm's production rules engine.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DISPOSITION_PRIORITY = {
    "clear": 0,
    "request-docs": 1,
    "escalate-EDD": 2,
    "decline-recommend": 3,
}


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


def add_outcome(
    outcomes: list[dict[str, Any]],
    rules_by_id: dict[str, dict[str, Any]],
    rule_id: str,
    outcome: str,
    evidence: str,
) -> None:
    rule = rules_by_id[rule_id]
    outcomes.append(
        {
            "rule_id": rule_id,
            "rule_text": rule["description"],
            "outcome": outcome,
            "severity": rule.get("severity", "medium"),
            "evidence": evidence,
        }
    )


def raise_disposition(current: str, candidate: str | None) -> str:
    if not candidate:
        return current
    if DISPOSITION_PRIORITY[candidate] > DISPOSITION_PRIORITY[current]:
        return candidate
    return current


def evaluate(record: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    rules_by_id = {rule["id"]: rule for rule in rules["rules"]}
    outcomes: list[dict[str, Any]] = []
    escalation_reasons: list[str] = []
    missing_documents: list[str] = []
    risk_rating = "low"
    disposition = "clear"

    high_risk_jurisdictions = set(rules.get("highRiskJurisdictions", []))
    applicant_jurisdiction = str(record.get("jurisdiction", ""))
    owner_jurisdictions = [
        str(owner.get("nationality", ""))
        for owner in record.get("beneficial_owners", [])
        if isinstance(owner, dict)
    ]
    risky_jurisdictions = [
        value
        for value in [applicant_jurisdiction, *owner_jurisdictions]
        if value in high_risk_jurisdictions
    ]
    if risky_jurisdictions:
        risk_rating = "high"
        escalation_reasons.append(
            "high-risk jurisdiction: " + ", ".join(sorted(set(risky_jurisdictions)))
        )
        add_outcome(
            outcomes,
            rules_by_id,
            "R-JUR-001",
            "fail",
            "Matched high-risk jurisdiction(s): "
            + ", ".join(sorted(set(risky_jurisdictions))),
        )
    else:
        add_outcome(
            outcomes,
            rules_by_id,
            "R-JUR-001",
            "pass",
            "No applicant or beneficial-owner jurisdiction matched high-risk list.",
        )

    screening = record.get("screening_results", {})
    sanctions = str(screening.get("sanctions", "not-run"))
    pep = str(screening.get("pep", "not-run"))
    adverse_media = str(screening.get("adverse_media", "not-run"))

    if sanctions == "confirmed":
        risk_rating = "high"
        disposition = raise_disposition(disposition, "decline-recommend")
        escalation_reasons.append("confirmed sanctions hit")
        add_outcome(
            outcomes,
            rules_by_id,
            "R-SAN-001",
            "fail",
            "Screening result sanctions=confirmed.",
        )
    else:
        add_outcome(
            outcomes,
            rules_by_id,
            "R-SAN-001",
            "pass",
            f"Screening result sanctions={sanctions}.",
        )

    pep_declared = any(
        bool(owner.get("pep_declared"))
        for owner in record.get("beneficial_owners", [])
        if isinstance(owner, dict)
    )
    if pep == "confirmed" or pep_declared:
        risk_rating = "high"
        disposition = raise_disposition(disposition, "escalate-EDD")
        reason = "confirmed PEP exposure" if pep == "confirmed" else "declared PEP exposure"
        escalation_reasons.append(reason)
        add_outcome(
            outcomes,
            rules_by_id,
            "R-PEP-001",
            "fail",
            f"pep={pep}; beneficial_owner_pep_declared={pep_declared}.",
        )
    else:
        add_outcome(
            outcomes,
            rules_by_id,
            "R-PEP-001",
            "pass",
            f"pep={pep}; beneficial_owner_pep_declared={pep_declared}.",
        )

    if adverse_media in {"confirmed", "possible-hit"}:
        risk_rating = "high"
        disposition = raise_disposition(disposition, "escalate-EDD")
        escalation_reasons.append(f"adverse media: {adverse_media}")
        add_outcome(
            outcomes,
            rules_by_id,
            "R-AM-001",
            "fail",
            f"Screening result adverse_media={adverse_media}.",
        )
    else:
        add_outcome(
            outcomes,
            rules_by_id,
            "R-AM-001",
            "pass",
            f"Screening result adverse_media={adverse_media}.",
        )

    applicant_type = str(record.get("applicant_type", ""))
    required_docs = rules.get("requiredDocuments", {}).get(applicant_type, [])
    statuses = doc_status(record)
    expired_documents: list[str] = []
    for doc_name in required_docs:
        status = statuses.get(doc_name)
        if status is None:
            missing_documents.append(doc_name)
        elif status == "expired":
            expired_documents.append(doc_name)
            missing_documents.append(doc_name)

    if missing_documents:
        if risk_rating == "low":
            risk_rating = "medium"
        disposition = raise_disposition(disposition, "request-docs")
        add_outcome(
            outcomes,
            rules_by_id,
            "R-DOC-001",
            "fail",
            "Missing or expired required document(s): "
            + ", ".join(sorted(missing_documents)),
        )
    else:
        add_outcome(
            outcomes,
            rules_by_id,
            "R-DOC-001",
            "pass",
            "All required documents for applicant type are received.",
        )

    owners = [
        owner
        for owner in record.get("beneficial_owners", [])
        if isinstance(owner, dict)
    ]
    total_ownership = sum(float(owner.get("ownership_percent", 0)) for owner in owners)
    if not owners or total_ownership < 75:
        if risk_rating == "low":
            risk_rating = "medium"
        add_outcome(
            outcomes,
            rules_by_id,
            "R-OWN-001",
            "fail",
            f"Beneficial ownership coverage is {total_ownership:.1f}%.",
        )
    else:
        add_outcome(
            outcomes,
            rules_by_id,
            "R-OWN-001",
            "pass",
            f"Beneficial ownership coverage is {total_ownership:.1f}%.",
        )

    source_of_funds = str(record.get("source_of_funds", "")).strip()
    if not source_of_funds or "source_of_funds" in missing_documents:
        if risk_rating == "low":
            risk_rating = "medium"
        disposition = raise_disposition(disposition, "request-docs")
        if "missing source of funds" not in escalation_reasons and risk_rating == "high":
            escalation_reasons.append("missing source of funds")
        add_outcome(
            outcomes,
            rules_by_id,
            "R-SOF-001",
            "fail",
            "Source of funds is empty or supporting document is missing.",
        )
    else:
        add_outcome(
            outcomes,
            rules_by_id,
            "R-SOF-001",
            "pass",
            "Source of funds field and supporting document are present.",
        )

    if risk_rating in {"medium", "high"} and disposition == "clear":
        disposition = "request-docs"

    return {
        "schema_version": "kyc.disposition.v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "applicant_id": record.get("applicant_id"),
        "applicant_name": record.get("applicant_name"),
        "risk_rating": risk_rating,
        "disposition": disposition,
        "missing_documents": sorted(set(missing_documents)),
        "expired_documents": sorted(set(expired_documents)),
        "escalation_reasons": sorted(set(escalation_reasons)),
        "rule_outcomes": outcomes,
        "human_review_required": disposition != "clear",
        "decision_boundary": "This workflow routes a disposition for reviewer action; it does not make final onboarding decisions.",
    }


def write_reviewer_packet(disposition: dict[str, Any], output_path: Path) -> None:
    lines = [
        "# KYC Reviewer Packet",
        "",
        f"Applicant: {disposition.get('applicant_name')} ({disposition.get('applicant_id')})",
        f"Risk rating: {disposition['risk_rating']}",
        f"Disposition: {disposition['disposition']}",
        f"Human review required: {str(disposition['human_review_required']).lower()}",
        "",
        "## Missing Documents",
    ]
    missing = disposition.get("missing_documents") or []
    lines.extend([f"- {doc}" for doc in missing] or ["- None"])
    lines.extend(["", "## Escalation Reasons"])
    reasons = disposition.get("escalation_reasons") or []
    lines.extend([f"- {reason}" for reason in reasons] or ["- None"])
    lines.extend(["", "## Rule Outcomes"])
    for outcome in disposition.get("rule_outcomes", []):
        lines.append(
            f"- {outcome['rule_id']} ({outcome['outcome']}): {outcome['evidence']}"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "This packet is for reviewer routing. It does not make final onboarding decisions.",
            "",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="Parsed applicant record JSON")
    parser.add_argument("--rules", type=Path, required=True, help="Trusted rules grid JSON")
    parser.add_argument("--out", type=Path, required=True, help="Output directory")
    args = parser.parse_args()

    record = load_json(args.input)
    rules = load_json(args.rules)
    args.out.mkdir(parents=True, exist_ok=True)

    disposition = evaluate(record, rules)
    disposition_path = args.out / "kyc-disposition.json"
    reviewer_path = args.out / "reviewer-packet.md"

    disposition_path.write_text(
        json.dumps(disposition, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_reviewer_packet(disposition, reviewer_path)

    print(json.dumps({"disposition": str(disposition_path), "reviewer_packet": str(reviewer_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

