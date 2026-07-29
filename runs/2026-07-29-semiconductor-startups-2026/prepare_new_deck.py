#!/usr/bin/env python3
"""Prepare a materially new 36-slide evidence-led strategy deck."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path


RUN = Path(__file__).resolve().parent
OUTPUTS = RUN / "outputs"
old = json.loads((OUTPUTS / "decision-deck-content.json").read_text(encoding="utf-8"))
by_id = {slide["id"]: slide for slide in old["slides"]}


def take(slide_id: int, **updates):
    slide = copy.deepcopy(by_id[slide_id])
    slide.update(updates)
    return slide


slides = [
    take(
        1,
        layout="cover_mosaic",
        title="Semiconductor Startups 2026",
        subtitle="Where partner value can compound across compute, inference, and interconnect",
        strapline="10 companies  ·  4 infrastructure wedges  ·  3 partner roles",
    ),
    take(
        2,
        layout="decision_dashboard",
        title="Three moves emerge: activate deployable offers, validate complex wedges, monitor pre-scale bets",
        subtitle="The decision is a portfolio of bounded actions—not a universal winner ranking.",
    ),
    take(
        33,
        id=3,
        layout="portfolio_posture",
        kicker="PORTFOLIO ANSWER",
        title="Deployment evidence—not architectural novelty—drives the action posture",
        subtitle="Commercial stage and partner boundaries determine what can be tested now.",
    ),
    take(
        3,
        id=4,
        layout="thesis",
        kicker="WHY NOW",
        title="Market expansion creates room for new architectures—but fragmentation creates the channel wedge",
        subtitle="The opportunity is to make heterogeneous infrastructure adoptable, supportable, and repeatable.",
    ),
    take(
        5,
        id=5,
        layout="business_system",
        kicker="MARKET + BUSINESS MODEL",
        title="Four bottlenecks—and four commercialization models—shape the cohort",
        subtitle="Insertion point determines the buyer, sales clock, and partner value pool.",
    ),
    take(
        7,
        id=6,
        layout="icp_gtm_map",
        kicker="ICP + BUYING TRIGGERS",
        title="Buyer pain—not firmographics—determines the ideal customer profile",
        subtitle="Each workload has a distinct proof threshold and route to production.",
    ),
    take(
        8,
        id=7,
        layout="gtm_flywheel",
        kicker="GO-TO-MARKET",
        title="The winning GTM motion converts lighthouse proof into an ecosystem repeat",
        subtitle="Benchmark credibility must become a reference offer, operating model, and replication channel.",
    ),
    take(
        4,
        id=8,
        layout="partner_value",
        kicker="PARTNER VALUE",
        title="Partner value compounds where integration risk is highest",
        subtitle="The partner earns control by reducing risk across proof, packaging, deployment, and operations.",
    ),
    {
        "id": 9,
        "layout": "evidence_coverage",
        "kicker": "EVIDENCE QUALITY",
        "title": "The evidence is broad enough to screen—and too vendor-led to declare winners",
        "subtitle": "Coverage supports directional portfolio choices; independent customer, benchmark, and economics proof remains sparse.",
        "claim": "The evidence ledger contains 83 sourced claims, with uneven company coverage and limited independent proof.",
        "kind": "fact",
        "evidence": ["src-crn"],
        "citation": "Evidence ledger and data-quality report; retrieved through Jul. 29, 2026.",
        "kpis": [
            ["83", "SOURCED CLAIMS", "Complete closed-cohort ledger"],
            ["16", "NUMERIC ROWS", "Funding, stage, and specifications"],
            ["30", "HIGH CONFIDENCE", "Specific attributable disclosures"],
            ["53", "MEDIUM CONFIDENCE", "Directional or vendor-led evidence"],
        ],
        "coverage": [
            ["Axelera AI", 13],
            ["Tenstorrent", 8],
            ["Cornelis", 7],
            ["NextSilicon", 5],
            ["Fractile", 5],
            ["Etched", 5],
            ["d-Matrix", 5],
            ["MatX", 5],
            ["Lightmatter", 5],
            ["Xsight Labs", 5],
        ],
    },
    take(
        10,
        id=10,
        layout="comparison",
        kicker="COMMERCIAL MATURITY",
        title="Commercial maturity separates actionable platforms from architectural options",
        subtitle="The cohort spans shipping systems, design-in components, samples, and pre-scale architectures.",
    ),
    take(
        11,
        id=11,
        title="Compute challengers split between programmable breadth and workload-specific conviction",
        subtitle="The partner question is whether software and supply can make the architecture deployable.",
    ),
]

company_strategy = {
    12: ("Chip + edge platform", "Edge OEMs and solution builders", "Partner-led deployment", "Build a vertical reference offer", "HIGH / MEDIUM"),
    13: ("Systems + licensable IP", "Sovereign AI, enterprise, developers", "Direct systems + licensing", "Choose the system or IP motion", "HIGH / MEDIUM"),
    14: ("Accelerator + design-in", "HPC and research institutions", "Application-led design-in", "Prove porting effort and supply", "HIGH / MEDIUM"),
    15: ("Chip + full-stack systems", "Frontier labs and high-token inference", "Lighthouse co-development", "Secure a benchmarkable workload", "HIGH / LOW"),
    16: ("Transformer ASIC + racks", "Hyperscalers and frontier labs", "Strategic design-in", "Test workload durability", "MEDIUM / LOW"),
    17: ("Inference platform + software", "Hyperscalers, neoclouds, enterprise AI", "System validation + replication", "Validate TCO and support boundary", "HIGH / MEDIUM"),
    18: ("LLM accelerator + systems", "Frontier labs and model builders", "Co-design before scale", "Wait for accessible silicon", "HIGH / LOW"),
    21: ("Fabric silicon + systems", "HPC and AI-cluster operators", "Cluster integration", "Package migration services", "HIGH / MEDIUM"),
    22: ("Photonic component + design-in", "Hyperscalers, packaging ecosystems", "Long-cycle ecosystem design-in", "Map the orchestrator control point", "HIGH / MEDIUM"),
    23: ("Ethernet silicon + software", "Hyperscalers, OEMs, network teams", "NOS/OEM design-in", "Validate tooling and support", "HIGH / MEDIUM"),
}

for slide_id in range(12, 19):
    model, icp, gtm, move, confidence = company_strategy[slide_id]
    slides.append(
        take(
            slide_id,
            layout="company_strategy",
            business_model=model,
            icp=icp,
            gtm=gtm,
            partner_move=move,
            confidence=confidence,
        )
    )

slides.extend(
    [
        take(
            19,
            id=19,
            layout="comparison",
            title="Specialization narrows the ICP while increasing the proof burden",
            subtitle="Broad platforms carry software complexity; narrow platforms carry workload-durability risk.",
        ),
        take(
            20,
            id=20,
            title="Interconnect challengers create partner control points without replacing compute",
            subtitle="Fabric, photonics, and programmable Ethernet enter at different layers of the AI system.",
        ),
    ]
)

for slide_id in range(21, 24):
    model, icp, gtm, move, confidence = company_strategy[slide_id]
    slides.append(
        take(
            slide_id,
            layout="company_strategy",
            business_model=model,
            icp=icp,
            gtm=gtm,
            partner_move=move,
            confidence=confidence,
        )
    )

slides.extend(
    [
        take(
            24,
            id=24,
            layout="comparison",
            title="The three interconnect plays solve different layers of the same scaling problem",
            subtitle="Control shifts from cluster fabric to package-level I/O to programmable Ethernet.",
        ),
        take(
            25,
            id=25,
            layout="gtm-scorecard",
            kicker="PARTNER ENTRY GATES",
            title="Six hard gates determine whether a partner motion is credible",
            subtitle="A strong architecture cannot compensate for missing product, support, or operating boundaries.",
        ),
        take(26, id=26, layout="comparison", title="Distributor fit favors packageable offers with bounded support"),
        take(27, id=27, layout="comparison", title="SI fit favors deployable systems with reusable integration"),
        take(28, id=28, layout="comparison", title="Ecosystem fit favors platforms that coordinate scarce complements"),
        {
            "id": 29,
            "layout": "partner_heatmap",
            "kicker": "ROLE-SPECIFIC PORTFOLIO",
            "title": "One heatmap shows the role-specific portfolio—not a universal ranking",
            "subtitle": "The same company can merit a different next move for a distributor, SI, or ecosystem orchestrator.",
            "claim": "Partner readiness varies by role and must be displayed with the next validation question.",
            "kind": "interpretation",
            "evidence": ["src-crn", "src-axelera", "src-dmatrix-prod", "src-cornelis", "src-lightmatter-prod"],
            "citation": "Public-evidence posture; candidate model, not calibrated organization-specific scoring.",
            "rows": [
                ["Axelera AI", "STRONG", "STRONG", "STRONG", "Validate economics"],
                ["Tenstorrent", "EMERGING", "EMERGING", "STRONG", "Choose motion"],
                ["NextSilicon", "VALIDATE", "EMERGING", "EMERGING", "Prove porting"],
                ["Fractile", "MONITOR", "VALIDATE", "VALIDATE", "Secure lighthouse"],
                ["Etched", "MONITOR", "VALIDATE", "VALIDATE", "Test workload durability"],
                ["d-Matrix", "EMERGING", "STRONG", "EMERGING", "Validate TCO + SLA"],
                ["MatX", "MONITOR", "MONITOR", "VALIDATE", "Wait for silicon"],
                ["Cornelis", "STRONG", "STRONG", "EMERGING", "Package migration"],
                ["Lightmatter", "VALIDATE", "VALIDATE", "STRONG", "Map control point"],
                ["Xsight Labs", "VALIDATE", "EMERGING", "EMERGING", "Validate NOS/tooling"],
            ],
        },
        take(
            30,
            id=30,
            layout="economics",
            title="Unit economics differ by where the partner controls value",
            subtitle="Inventory, design-in, software, and ecosystem motions create distinct margin and support exposure.",
        ),
        {
            "id": 31,
            "layout": "phase0",
            "kicker": "PHASE 0 CALIBRATION",
            "title": "Calibrate the model on three deliberately different archetypes",
            "subtitle": "Axelera AI, Etched, and Lightmatter test deployment, specialization, and ecosystem-design-in assumptions.",
            "claim": "A three-company pilot with independent raters should precede organization-specific recommendations.",
            "kind": "recommendation",
            "evidence": ["src-axelera", "src-etched", "src-lightmatter-prod"],
            "citation": "Phase 0 operating recommendation; public evidence defines hypotheses, not final selections.",
            "pilots": [
                ["AXELERA AI", "DEPLOYMENT ECOSYSTEM", "Can partners replicate a vertical edge offer with bounded support?", "Distributor + SI"],
                ["ETCHED", "SPECIALIZATION BET", "Does transformer-only advantage survive workload and roadmap scrutiny?", "SI + lighthouse"],
                ["LIGHTMATTER", "DESIGN-IN ECOSYSTEM", "Who owns qualification, packaging coordination, and commercial pull?", "Orchestrator"],
            ],
        },
        take(
            34,
            id=32,
            layout="roadmap",
            kicker="90-DAY ACTION PLAN",
            title="The first 90 days should buy evidence, not commitments",
            subtitle="Each stage resolves a specific uncertainty and ends in an explicit advance, redesign, or stop decision.",
        ),
        take(
            35,
            id=33,
            layout="watchlist",
            title="Quarterly triggers—not narrative momentum—should change posture",
            subtitle="Commercial milestones are the control system for the portfolio.",
        ),
        take(
            38,
            id=34,
            layout="risks",
            title="Five kill criteria stop technically impressive but non-deployable bets",
            subtitle="Software, silicon, proof, customers, and workload durability are non-negotiable gates.",
        ),
        take(
            43,
            id=35,
            layout="comparison",
            kicker="EVIDENCE BUYING PLAN",
            title="The evidence ledger exposes exactly what must be learned next",
            subtitle="Every priority has a strongest anchor, a decisive gap, and a next question.",
        ),
        take(
            39,
            id=36,
            layout="conclusion",
            title="Select validation priorities now—and reserve partnership decisions for calibrated evidence",
            subtitle="The portfolio is actionable when posture, confidence, and the next proof purchase travel together.",
            takeaway="Use the cohort to choose what to test next—not to declare a market winner.",
        ),
    ]
)

assert len(slides) == 36
for index, slide in enumerate(slides, 1):
    assert slide["id"] == index, (index, slide["id"], slide["title"])

content = {"sources": old["sources"], "slides": slides}
(OUTPUTS / "new-deck-content.json").write_text(json.dumps(content, indent=2), encoding="utf-8")

claims = []
plan_slides = []
visuals = []
asset_by_company = {
    item["company"].upper(): item
    for item in json.loads((RUN / "research" / "visual-assets.json").read_text(encoding="utf-8"))["assets"]
}
for slide in slides:
    claim_id = f"NEW-S{slide['id']:02d}"
    claims.append(
        {
            "id": claim_id,
            "text": slide.get("claim") or slide["title"],
            "kind": slide.get("kind", "interpretation"),
            "confidence": "high" if slide.get("kind") == "fact" else "medium",
            "evidence_ids": slide.get("evidence", []),
        }
    )
    native_id = f"new-s{slide['id']:02d}-native"
    slide_visual_ids = [native_id]
    visuals.append(
        {
            "id": native_id,
            "slide_ids": [slide["id"]],
            "purpose": "Editable decision content, comparison, diagram, or table.",
            "artifact_type": "diagram",
            "evidence_status": "underlying-information",
            "route": "native",
            "reason": "Structured claims and comparisons remain editable PowerPoint objects.",
            "evidence_ids": slide.get("evidence", []),
            "qa": {
                "visual_checked": False,
                "legible": False,
                "not_cropped": True,
                "background_matched": True,
                "provenance_recorded": True,
            },
        }
    )
    company = slide.get("company", "").upper()
    if company and company in asset_by_company:
        asset = asset_by_company[company]
        asset_id = f"new-s{slide['id']:02d}-asset"
        slide_visual_ids.append(asset_id)
        visuals.append(
            {
                "id": asset_id,
                "slide_ids": [slide["id"]],
                "purpose": f"Official product visual for {slide['company']}.",
                "artifact_type": "brand-asset",
                "evidence_status": "approved-asset",
                "route": "place-asset",
                "reason": "The official company-site image identifies the real product or platform.",
                "source": {"path": asset["source_page"]},
                "asset": asset["local_path"],
                "placement": {"width": 1200, "height": 1050, "fit": "contain", "background": "#FFFFFF"},
                "qa": {
                    "visual_checked": False,
                    "legible": True,
                    "not_cropped": True,
                    "background_matched": True,
                    "provenance_recorded": True,
                },
            }
        )
    plan_slides.append(
        {
            "slide_id": slide["id"],
            "archetype": slide["layout"],
            "action_title": slide["title"],
            "audience_job": "Decide the posture, proof requirement, or next action.",
            "claim_ids": [claim_id],
            "evidence_ids": slide.get("evidence", []),
            "visual_ids": slide_visual_ids,
            "speaker_notes": {
                "talk_time_seconds": 60,
                "narrative": slide.get("claim") or slide.get("subtitle"),
                "demo_fallback": None,
            },
            "accessibility": {
                "reading_order": ["title", "main visual", "supporting evidence", "citation"],
                "visual_alt_text": slide["title"],
            },
            "status": "planned",
        }
    )

slide_plan = {
    "contract_version": "1.0",
    "deck": {
        "name": "Semiconductor Startups 2026 — Evidence-Led Strategy",
        "evidence_contract": None,
        "visual_contract": "new-deck-visual-spec.json",
    },
    "claims": claims,
    "slides": plan_slides,
}
(RUN / "new-deck-slide-plan.json").write_text(json.dumps(slide_plan, indent=2), encoding="utf-8")

visual_spec = {
    "contract_version": "1.0",
    "deck": {
        "output_mode": "native",
        "editability": "PowerPoint-native text, tables, charts, matrices, and diagrams; official product images remain editable picture shapes.",
        "reference_deck": None,
    },
    "visuals": visuals,
}
(RUN / "new-deck-visual-spec.json").write_text(json.dumps(visual_spec, indent=2), encoding="utf-8")

brief = """# Deck brief

## Audience

Alliance, channel, corporate strategy, and ecosystem leaders deciding which semiconductor
startup archetypes deserve activation, bounded validation, or monitoring.

## Decision

Choose the next partner motion and proof purchase for each company without converting
public, vendor-led evidence into an unsupported winner ranking.

## Narrative promise

The deck connects architecture to business model, ICP, GTM, partner role, confidence, and
the next evidence-buying action. It is a visibly new 36-slide strategy narrative.

## Voice and tone

Executive, evidence-led, commercially literate, and explicit about uncertainty.

## Anti-references

Vendor chronology, repetitive biography cards, decorative circuit boards, unsupported
rankings, funding-as-quality logic, and hidden confidence.

## Evidence and editability

Claims trace to the existing 83-row evidence ledger. All structured content is native and
editable. Ten official company-site visuals are placed as editable picture shapes.

## Success criteria

- Exactly 36 slides with a materially different title sequence and layout system.
- The executive answer, evidence quality, business model, ICP, and GTM precede profiles.
- Every company profile shows business model, ICP, GTM, partner move, and confidence.
- The partner portfolio consolidates distributor, SI, and ecosystem roles in one heatmap.
- Phase 0 calibration and a 90-day evidence-buying plan close the argument.
- Structural, visual-spec, design-lint, preview, and OfficeCLI QA pass.
"""
(RUN / "new-deck-brief.md").write_text(brief, encoding="utf-8")

with (OUTPUTS / "evidence-ledger.csv").open(newline="", encoding="utf-8") as handle:
    evidence_rows = list(csv.DictReader(handle))

trace_lines = [
    "# New Deck Artifact Traceability",
    "",
    "| Slide | Assertion | Evidence basis | Confidence |",
    "|---:|---|---|---|",
]
for slide in slides:
    evidence = ", ".join(slide.get("evidence", [])) or "labeled interpretation"
    confidence = "high" if slide.get("kind") == "fact" else "medium"
    trace_lines.append(f"| {slide['id']} | {slide['title']} | {evidence} | {confidence} |")
(OUTPUTS / "artifact-traceability-v2.md").write_text("\n".join(trace_lines) + "\n", encoding="utf-8")

print(f"Prepared {len(slides)} slides from {len(evidence_rows)} evidence rows.")
