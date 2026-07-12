#!/usr/bin/env python3
"""Extract YC company records through the Printing Press YC CLI.

This script makes the content source pack reproducible without reading the
SQLite database directly. The CLI output is saved as raw provenance, then a
curated deck source pack is built from `.results`.
"""

from __future__ import annotations

import json
import subprocess
from datetime import date
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent
CLI = Path("/home/shekerk/printing-press/library/yc-companies/yc-companies-pp-cli")
DB = Path("/tmp/yc-agentic.db")
RAW_DIR = RUN_DIR / "yc-pp-cli-raw"
SOURCE_PACK = RUN_DIR / "yc-company-source-pack.json"
MANIFEST = RUN_DIR / "yc-pp-cli-extraction-manifest.json"

TARGETS = [
    ("CentralComs", "claim-001"),
    ("Lance", "claim-002"),
    ("Klarify", "claim-003"),
    ("Dodo", "claim-004"),
    ("Kastle", "claim-005"),
    ("Fazeshift", "claim-006"),
    ("Basepilot", "claim-007"),
    ("ProcIndex", "claim-008"),
    ("InspectMind AI", "claim-009"),
    ("Veritus", "claim-010"),
]

ANALYST_OVERLAY = {
    "CentralComs": {
        "wedge": "Property management maintenance operations",
        "buyer": "Property managers using AppFolio, Buildium, Yardi, and adjacent stacks",
        "workflow": "Tracks maintenance calls, chases open tickets, and keeps owners, tenants, and vendors updated.",
        "analyst_positioning": "Vertical agent for the messy middle of rental operations: maintenance intake, ticket follow-up, stakeholder updates, and system-of-record coordination.",
    },
    "Lance": {
        "wedge": "Hotel call handling and guest operations",
        "buyer": "Hotel groups and operators with high-volume guest-facing workflows",
        "workflow": "Answers calls, closes sales, navigates hotel software, and handles multi-step operational tasks.",
        "analyst_positioning": "Computer-use agent layer for hotel operations, positioned around phone volume, bookings, guest support, and operational task execution inside existing hotel software.",
    },
    "Klarify": {
        "wedge": "Therapist administration and documentation",
        "buyer": "Therapists and therapy practices",
        "workflow": "Handles clinical notes, treatment plans, letters, insurance claims, supervision prep, resources, and client acquisition.",
        "analyst_positioning": "Practice-operations agent for therapists, targeting the non-therapy workload that sits outside client sessions and is poorly served by passive practice-management software.",
    },
    "Dodo": {
        "wedge": "Clinic communications and front-office automation",
        "buyer": "Clinics with high call, text, scheduling, refill, intake, and follow-up volume",
        "workflow": "Runs scheduling, refills, intake, follow-ups, calls, and texts across clinic systems.",
        "analyst_positioning": "Multi-agent clinic communication layer that converts patient communication into completed workflow rather than another inbox for staff.",
    },
    "Kastle": {
        "wedge": "Mortgage servicing voice workflows",
        "buyer": "Mortgage servicers and traditional financial services firms",
        "workflow": "Collects payments, verifies borrowers, and qualifies new loan inquiries over the phone.",
        "analyst_positioning": "Voice-agent interface for mortgage servicing where legacy lenders need better phone infrastructure for borrower communication and inquiry handling.",
    },
    "Fazeshift": {
        "wedge": "Accounts receivable automation",
        "buyer": "Finance teams operating across QuickBooks, Stripe, NetSuite, DocuSign, HubSpot, and Salesforce",
        "workflow": "Connects fragmented finance and sales systems, then automates manual AR follow-up work.",
        "analyst_positioning": "AR agent for the fragmented quote-to-cash data layer, aimed at replacing manual finance-team follow-up across disconnected systems.",
    },
    "Basepilot": {
        "wedge": "Insurance claims operations",
        "buyer": "Insurers, TPAs, and MGAs",
        "workflow": "Line-of-business-specific agents for claims operations efficiency, cost reduction, and operational intelligence.",
        "analyst_positioning": "Claims-operations agent platform for regulated insurance workflows where generic automation needs line-of-business context.",
    },
    "ProcIndex": {
        "wedge": "Accounting operations agent suite",
        "buyer": "Accounting teams using ERP systems",
        "workflow": "Automates quote-to-cash, accounts payable, and month-end close while keeping visibility into agent actions.",
        "analyst_positioning": "Full-stack AI accounting firm positioned around end-to-end back-office execution, not just document extraction or task suggestions.",
    },
    "InspectMind AI": {
        "wedge": "Construction drawing review",
        "buyer": "Construction teams reviewing drawings before execution",
        "workflow": "Catches issues in construction drawings before they become costly rework and project delays.",
        "analyst_positioning": "Pre-construction quality-control agent for catching coordination errors early, before they turn into rework, schedule slippage, and owner disputes.",
    },
    "Veritus": {
        "wedge": "Loan servicing and collections",
        "buyer": "Consumer lenders and servicing teams",
        "workflow": "Deploys voice and omni-channel agents for servicing, collections, repayment negotiation, follow-up, and recovery.",
        "analyst_positioning": "Regulated collections and servicing agent platform, focused on reducing cost-to-collect while improving borrower follow-up and recovery operations.",
    },
}


def run_search(name: str) -> dict:
    cmd = [
        str(CLI),
        "search",
        name,
        "--db",
        str(DB),
        "--data-source",
        "local",
        "--json",
        "--max-age",
        "0",
        "--limit",
        "10",
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def exact_company(envelope: dict, name: str) -> dict:
    results = envelope.get("results") or []
    lowered = name.lower()
    for item in results:
        if item.get("name", "").lower() == lowered:
            return item
    for item in results:
        if item.get("slug", "").lower() == lowered.replace(" ", "-"):
            return item
    raise RuntimeError(f"No exact YC company match found for {name!r}")


def subindustry(record: dict) -> str:
    raw = record.get("subindustry") or ""
    if "->" in raw:
        return raw.split("->", 1)[1].strip()
    if " -\u003e " in raw:
        return raw.split(" -\u003e ", 1)[1].strip()
    return raw or record.get("industry", "")


def main() -> int:
    if not CLI.exists():
        raise SystemExit(f"Printing Press YC CLI not found: {CLI}")
    if not DB.exists():
        raise SystemExit(f"Synced YC DB not found: {DB}")
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    companies = []
    manifest_rows = []
    for name, claim_id in TARGETS:
        envelope = run_search(name)
        raw_path = RAW_DIR / f"{name.lower().replace(' ', '-')}.json"
        raw_path.write_text(json.dumps(envelope, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        record = exact_company(envelope, name)
        overlay = ANALYST_OVERLAY[name]
        companies.append(
            {
                "claim_id": claim_id,
                "name": record["name"],
                "slug": record["slug"],
                "batch": record.get("batch", ""),
                "team_size": record.get("team_size"),
                "status": record.get("status", ""),
                "is_hiring": bool(record.get("isHiring")),
                "industry": record.get("industry", ""),
                "subindustry": subindustry(record),
                "yc_one_liner": record.get("one_liner", ""),
                "yc_long_description": record.get("long_description", ""),
                "website": record.get("website", ""),
                "url": record.get("url", ""),
                "api": record.get("api", ""),
                "source_raw_cli_json": str(raw_path.relative_to(RUN_DIR)),
                **overlay,
            }
        )
        manifest_rows.append(
            {
                "query": name,
                "claim_id": claim_id,
                "raw_output": str(raw_path.relative_to(RUN_DIR)),
                "meta": envelope.get("meta", {}),
                "results_returned": len(envelope.get("results") or []),
                "selected_slug": record.get("slug"),
            }
        )

    SOURCE_PACK.write_text(
        json.dumps(
            {
                "source": "Printing Press YC CLI (`yc-companies-pp-cli search --db /tmp/yc-agentic.db --data-source local --json`)",
                "status": "draft_source_pack",
                "generated_at": date.today().isoformat(),
                "companies": companies,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    MANIFEST.write_text(
        json.dumps(
            {
                "cli": str(CLI),
                "db": str(DB),
                "generated_at": date.today().isoformat(),
                "queries": manifest_rows,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(SOURCE_PACK)
    print(MANIFEST)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
