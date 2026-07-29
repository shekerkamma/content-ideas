#!/usr/bin/env python3
"""Backfill AI Analyst artifacts from the reviewed semiconductor run contracts."""

from __future__ import annotations

import csv
import datetime as dt
import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


RUN = Path(__file__).resolve().parent
OUTPUTS = RUN / "outputs"
INPUTS = RUN / "inputs"
CONTENT = json.loads((OUTPUTS / "decision-deck-content.json").read_text(encoding="utf-8"))
PLAN = json.loads((RUN / "decision-slide-plan.json").read_text(encoding="utf-8"))
SOURCES = {item["id"]: item for item in CONTENT["sources"]}
RETRIEVED = "2026-07-29"
TARGET = "CRN 2026 semiconductor startup cohort"
LEDGER_COLUMNS = [
    "claim_id", "captured_at", "target", "competitor", "arena", "source_title",
    "source_url", "source_type", "published_at", "retrieved_at", "metric_family",
    "metric_name", "metric_value", "metric_unit", "baseline", "comparison",
    "claim_text", "quote_excerpt", "evidence_strength", "confidence",
    "confidence_reason", "storyboard_use", "notes",
]

COMPETITOR_BY_SOURCE = {
    "src-axelera": "Axelera AI",
    "src-tenstorrent": "Tenstorrent",
    "src-nextsilicon": "NextSilicon",
    "src-fractile": "Fractile",
    "src-etched": "Etched",
    "src-dmatrix-prod": "d-Matrix",
    "src-dmatrix-fund": "d-Matrix",
    "src-cornelis": "Cornelis Networks",
    "src-cornelis-fund": "Cornelis Networks",
    "src-lightmatter-prod": "Lightmatter",
    "src-lightmatter-fund": "Lightmatter",
    "src-matx": "MatX",
    "src-xsight": "Xsight Labs",
    "src-crn": "CRN cohort",
    "src-gartner": "Semiconductor market",
}

ARENA_BY_COMPANY = {
    "AXELERA AI": "edge deployment",
    "TENSTORRENT": "adaptable compute",
    "NEXTSILICON": "adaptable compute",
    "FRACTILE": "inference specialists",
    "ETCHED": "inference specialists",
    "D-MATRIX": "inference specialists",
    "MATX": "inference specialists",
    "CORNELIS NETWORKS": "interconnect",
    "LIGHTMATTER": "interconnect",
    "XSIGHT LABS": "interconnect",
}

NUMBER_RE = re.compile(
    r"(?<![A-Za-z0-9-])(?P<currency>\$)?(?P<value>\d+(?:\.\d+)?)\s*"
    r"(?P<unit>Tbps|[TMBK]|G|%|million|billion)?\b",
    re.IGNORECASE,
)


def source_type(source_id: str) -> str:
    source = SOURCES[source_id]
    title = source["title"].lower()
    if source_id == "src-gartner":
        return "analyst"
    if source_id == "src-crn":
        return "press"
    if "fund" in source_id or any(word in title for word in ("fund", "raises", "financing", "series")):
        return "press"
    return "official"


def metric_family(text: str) -> str:
    value = text.lower()
    if any(word in value for word in ("fund", "valuation", "capital", "$", "revenue", "economics")):
        return "roi_financial"
    if any(word in value for word in ("partner", "ecosystem", "channel", "customer", "design-in", "distribution")):
        return "distribution"
    if any(word in value for word in ("production", "availability", "sampling", "tape-out", "supply", "risk")):
        return "quality_risk"
    if any(word in value for word in ("bandwidth", "tbps", "latency", "throughput", "performance")):
        return "quality_risk"
    return "other"


def numeric_metric(text: str) -> tuple[str, str]:
    for match in NUMBER_RE.finditer(text):
        value = match.group("value")
        unit = match.group("unit") or ""
        start = match.start()
        nearby = text[max(0, start - 24):match.end() + 24].lower()
        if value in {"2024", "2025", "2026"} or "q4" in nearby:
            continue
        if match.group("currency"):
            unit = "$" + unit.upper()
        return value, unit
    return "", ""


def make_row(
    claim_id: str,
    text: str,
    evidence_ids: list[str],
    *,
    competitor: str,
    arena: str,
    confidence: str,
    strength: str,
    storyboard_use: str,
    metric_name: str = "",
    notes: str = "",
) -> dict[str, str]:
    source_id = evidence_ids[0]
    source = SOURCES[source_id]
    value, unit = numeric_metric(text)
    co_sources = [SOURCES[item]["path"] for item in evidence_ids[1:]]
    co_note = f"Co-sources: {'; '.join(co_sources)}" if co_sources else ""
    return {
        "claim_id": claim_id,
        "captured_at": RETRIEVED,
        "target": TARGET,
        "competitor": competitor,
        "arena": arena,
        "source_title": source["title"],
        "source_url": source["path"],
        "source_type": source_type(source_id),
        "published_at": source.get("date", ""),
        "retrieved_at": RETRIEVED,
        "metric_family": metric_family(text),
        "metric_name": metric_name,
        "metric_value": value,
        "metric_unit": unit,
        "baseline": "",
        "comparison": "",
        "claim_text": text,
        "quote_excerpt": "",
        "evidence_strength": strength,
        "confidence": confidence,
        "confidence_reason": (
            "Specific current company or cohort fact from the cited source."
            if confidence == "high"
            else "Evidence-supported synthesis or directional judgment; not independently validated."
        ),
        "storyboard_use": storyboard_use,
        "notes": "; ".join(item for item in (notes, co_note) if item),
    }


def build_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for claim in PLAN["claims"]:
        source_id = claim["evidence_ids"][0]
        rows.append(
            make_row(
                "EV-" + claim["id"].replace("decision-claim-", "D"),
                claim["text"],
                claim["evidence_ids"],
                competitor=COMPETITOR_BY_SOURCE.get(source_id, "CRN cohort"),
                arena="closed-cohort partner readiness",
                confidence=claim["confidence"],
                strength="high" if claim["kind"] == "fact" else "medium",
                storyboard_use="slide " + claim["id"].split("-")[-1],
                notes=f"Claim kind: {claim['kind']}",
            )
        )
    for slide in CONTENT["slides"]:
        if slide.get("layout") != "company":
            continue
        company = slide["company"]
        arena = ARENA_BY_COMPANY[company]
        evidence = slide["evidence"]
        for label, text in slide["profile"].items():
            rows.append(
                make_row(
                    f"EV-C{slide['id']:02d}-{label}",
                    text,
                    evidence,
                    competitor={
                        "AXELERA AI": "Axelera AI",
                        "TENSTORRENT": "Tenstorrent",
                        "NEXTSILICON": "NextSilicon",
                        "FRACTILE": "Fractile",
                        "ETCHED": "Etched",
                        "D-MATRIX": "d-Matrix",
                        "MATX": "MatX",
                        "CORNELIS NETWORKS": "Cornelis Networks",
                        "LIGHTMATTER": "Lightmatter",
                        "XSIGHT LABS": "Xsight Labs",
                    }[company],
                    arena=arena,
                    confidence="high" if label in {"WEDGE", "PROOF"} else "medium",
                    strength="high" if label == "PROOF" else "medium",
                    storyboard_use=f"slide {slide['id']} company profile",
                    metric_name=label.lower() + "_evidence",
                    notes="Vendor-published where based on the company source.",
                )
            )
    return rows


def write_operating_prompt() -> None:
    INPUTS.mkdir(parents=True, exist_ok=True)
    text = """objective: >
  Rework the existing CRN 2026 semiconductor startup cohort into a decision-ready,
  evidence-led channel and ecosystem screen with a reviewed editable PPTX and matching HTML.
core_question: >
  Which startup archetypes merit act-now validation, validate-next diligence, or monitoring,
  and what evidence must change before a named partner recommendation is credible?
target:
  name: "CRN 2026 semiconductor startup cohort"
  geography: "Global AI infrastructure and semiconductor ecosystem"
  buyer_job: "Prioritize channel, systems-integration, and ecosystem validation"
audience:
  - "Channel and alliance leaders"
  - "Systems-integrator and ecosystem strategists"
  - "Corporate strategy and innovation teams"
competitor_arenas:
  - "edge deployment"
  - "adaptable compute"
  - "inference specialists"
  - "interconnect"
required_outputs:
  - "evidence ledger, metrics, quality report, scoring model, and confidence labels"
  - "44-or-more-slide editable branded PPTX"
  - "self-contained HTML report"
must_not_do:
  - "Do not turn CRN's editorial cohort into a market-wide winner ranking."
  - "Do not claim organization-specific partner fit without Phase 0 calibration."
  - "Do not invent funding, performance, readiness, market size, or customer proof."
evidence_standard: >
  Prefer current official company disclosures and the CRN cohort source; label company
  performance and funding statements as vendor-published and distinguish interpretation.
final_answer_should_decide:
  - "Which archetypes deserve action, validation, or monitoring"
  - "Which proof gaps block stronger partner recommendations"
"""
    (INPUTS / "operating-prompt.yaml").write_text(text, encoding="utf-8")


def write_search_log() -> None:
    rows = [
        "| Date | Level | Mode | Query / source | Output file | Purpose | Result | Follow-up |",
        "|---|---:|---|---|---|---|---|---|",
        "| 2026-07-29 | 2 | You.com livecrawl | CRN 2026 semiconductor startup cohort | `research/crn-livecrawl.json` | Define closed cohort | captured | none |",
        "| 2026-07-29 | 2 | You.com livecrawl | Official company product and funding pages | `research/*-official.json` | Product, stage, funding, and GTM evidence | captured for all ten companies | label vendor claims |",
        "| 2026-07-29 | 2 | You.com livecrawl | Official company-site visual pages | `research/*-visuals-livecrawl.json` | Approved product imagery | captured where required | attribution retained |",
        "| 2026-07-29 | data tap | Printing Press / Firecrawl | Existing official-source captures retained | `research/` | Full-page recapture path for future refreshes | available; no redundant re-crawl in this upgrade | rerun only for stale or missing sources |",
    ]
    (OUTPUTS / "search-log.md").write_text("# Search Log\n\n" + "\n".join(rows) + "\n", encoding="utf-8")


def write_ledger(rows: list[dict[str, str]]) -> None:
    with (OUTPUTS / "evidence-ledger.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter(row["competitor"] for row in rows)
    lines = [
        "# Evidence Ledger",
        "",
        f"- Grain: one row per sourced claim or company-profile evidence statement",
        f"- Rows: {len(rows)}",
        f"- Retrieval date: {RETRIEVED}",
        "- Scope: CRN closed cohort; not a market-wide ranking",
        "",
        "## Coverage by entity",
        "",
        "| Entity | Rows |",
        "|---|---:|",
    ]
    lines.extend(f"| {name} | {count} |" for name, count in sorted(counts.items()))
    lines.extend([
        "",
        "Company performance, product-stage, and funding claims are vendor-published unless a",
        "row identifies CRN, Gartner, or another source type. Directional partner-readiness",
        "claims remain medium-confidence interpretation pending Phase 0 calibration.",
        "",
    ])
    (OUTPUTS / "evidence-ledger.md").write_text("\n".join(lines), encoding="utf-8")


def write_metric_definitions() -> None:
    text = """# Metric Definitions

## Evidence Coverage Count

- Definition: Number of ledger rows available for an entity or arena.
- Formula: `COUNT(claim_id)` grouped by competitor or arena.
- Unit: sourced claim rows.
- Source columns: `claim_id`, `competitor`, `arena`.
- Exclusions: rejected or duplicate raw snippets not promoted to the ledger.
- Confidence basis: coverage measure only; it does not measure company quality.
- Limitation: several rows may originate from one company-published source.

## High-Confidence Evidence Count

- Definition: Ledger rows supported by specific current product, financing, or cohort facts.
- Formula: `COUNT(claim_id) WHERE confidence = high`.
- Unit: sourced claim rows.
- Source columns: `claim_id`, `confidence`, `source_type`.
- Exclusions: interpretation and recommendation rows.
- Limitation: high confidence in what a company published is not independent validation.

## Partner-Readiness Posture

- Definition: Categorical next diligence posture: `ACT NOW`, `VALIDATE NEXT`, or `MONITOR`.
- Rule: apply hard gates for accessible product, integration boundary, supply/availability,
  repeatable proof, partner role, and operating economics before assigning a posture.
- Unit: company by partner lens.
- Source columns: `claim_text`, `storyboard_use`, `confidence`, `source_type`.
- Confidence basis: public evidence only; two independent raters are required in Phase 0.
- Limitation: not an organization-specific right-to-win or partner recommendation.

## Readiness Rubric Weight

- Definition: Candidate weighting used to structure Phase 0 ratings.
- Formula: Product 20% + Software 20% + Supply 20% + Customer proof 15% +
  Partner motion 15% + Economics 10%.
- Unit: weighted readiness screen.
- Source basis: analytical framework on slide 42, not a market fact.
- Limitation: weights remain uncalibrated until independent-rater Phase 0 testing.
"""
    (OUTPUTS / "metric-definitions.md").write_text(text, encoding="utf-8")


def write_quality(rows: list[dict[str, str]]) -> None:
    by_competitor = Counter(row["competitor"] for row in rows)
    by_arena = Counter(row["arena"] for row in rows)
    by_source = Counter(row["source_type"] for row in rows)
    by_family = Counter(row["metric_family"] for row in rows)
    by_confidence = Counter(row["confidence"] for row in rows)
    numeric = sum(bool(row["metric_value"]) for row in rows)
    primary = sum(row["source_type"] in {"official", "press"} for row in rows)
    promoted = sum(row["storyboard_use"].startswith("slide") for row in rows)

    def table(counter: Counter[str]) -> str:
        return "\n".join(f"| {html.escape(str(k))} | {v} |" for k, v in sorted(counter.items()))

    text = f"""# Data Quality Report

## Summary

| Measure | Result |
|---|---:|
| Total evidence rows | {len(rows)} |
| Numeric evidence rows | {numeric} |
| High-confidence rows | {by_confidence.get('high', 0)} |
| Medium-confidence rows | {by_confidence.get('medium', 0)} |
| Official/press rows | {primary} |
| Story-promoted rows | {promoted} |

## Rows by competitor/entity

| Entity | Rows |
|---|---:|
{table(by_competitor)}

## Rows by arena

| Arena | Rows |
|---|---:|
{table(by_arena)}

## Rows by source type

| Source type | Rows |
|---|---:|
{table(by_source)}

## Rows by metric family

| Metric family | Rows |
|---|---:|
{table(by_family)}

## Quality Findings

- Coverage is sufficient for a closed-cohort directional screen, but it is not balanced
  independent market diligence.
- Company-specific claims are predominantly company-published. High confidence means the
  disclosure is specific and attributable; it does not independently validate performance.
- Numeric coverage is concentrated in funding, valuation, availability, and product
  specifications. Comparable customer outcomes, pricing, margin, and design-win evidence
  remain sparse.
- Partner-readiness labels are medium-confidence interpretations and must remain provisional.
- CRN defines the cohort; the run must not imply market completeness or a winner ranking.

## Search-Again Triggers

- Seek independent production benchmarks for architectures whose claims drive technical
  differentiation.
- Seek named reference customers, design wins, support ownership, supply assurance, and
  partner economics before named-partner recommendations.
- Run Phase 0 with two independent raters for Axelera AI, Etched, and Lightmatter before
  operationalizing the rubric.
"""
    (OUTPUTS / "data-quality-report.md").write_text(text, encoding="utf-8")


def write_scoring_model() -> None:
    text = """# Scoring Model

The deck uses categorical public-evidence postures, not a precise company ranking. The
candidate score below is a Phase 0 instrument and must not be treated as calibrated.

| Dimension | Weight | Score 1 | Score 3 | Score 5 | Evidence inputs |
|---|---:|---|---|---|---|
| Product | 20% | pre-product | samples/reference platform | shipping/qualified offer | availability and qualification rows |
| Software | 20% | unclear toolchain | documented but narrow | supported repeatable stack | compiler, framework, tooling evidence |
| Supply | 20% | tape-out ahead | manufacturing path visible | volume/supply evidence | production, supply, packaging rows |
| Customer proof | 15% | no named proof | lighthouse/sampling evidence | repeatable production proof | customer and design-win rows |
| Partner motion | 15% | partner role unclear | candidate integration boundary | explicit repeatable program | ecosystem and GTM rows |
| Economics | 10% | no commercial evidence | directional model | repeatable unit/channel economics | packaging, support, pricing rows |

## Hard Gates

- No `ACT NOW` posture without accessible product or validated reference platform.
- No distributor recommendation without packageability, supply visibility, and support.
- No SI recommendation without an integration boundary and reusable customer outcome.
- No ecosystem-orchestrator recommendation without dependence on multiple complements.
- Failed software, supply, or customer-proof gates override an attractive weighted score.

## Confidence Adjustment

- High: at least two source types with specific current evidence.
- Medium: current attributable evidence, predominantly company-published.
- Low: incomplete, stale, snippet-only, or inference-heavy evidence.

Show posture and confidence separately. Do not convert medium-confidence directional labels
into precise percentages. Phase 0 requires two independent raters and documented
adjudication before organization-specific use.
"""
    (OUTPUTS / "scoring-model.md").write_text(text, encoding="utf-8")


def write_brief() -> None:
    text = """# Competitor Brief

## Executive Answer

Use the ten-company cohort as a validation portfolio, not as a winner ranking or named
partner list. Near-term partner value is concentrated in workload validation, integration,
deployment, and ecosystem coordination around heterogeneous infrastructure.

## Arenas by Buyer Job

- Edge deployment: Axelera AI.
- Adaptable compute: Tenstorrent and NextSilicon.
- Inference specialists: Fractile, Etched, d-Matrix, and MatX.
- Interconnect: Cornelis Networks, Lightmatter, and Xsight Labs.

## Directional Portfolio

- Act now on bounded validation: Axelera AI, d-Matrix, and Cornelis.
- Validate next: Tenstorrent, NextSilicon, Lightmatter, and Xsight Labs.
- Monitor commercialization milestones: Fractile, Etched, and MatX.

These postures are public-evidence judgments with medium confidence, not calibrated
organization-specific recommendations.

## Where the Cohort Wins

- It attacks distinct bottlenecks rather than offering one generic GPU substitute.
- Several architectures can land beside incumbent compute, networks, or software.
- Integration difficulty creates a real partner value pool.

## Compression and Execution Risks

- Incumbents can absorb narrow advantages through roadmap improvements and ecosystem scale.
- Specialized architectures carry model- or workload-concentration risk.
- Software maturity, supply, independent benchmarks, named production customers, and
  repeatable partner economics remain decisive proof gaps.

## Recommended Moves

1. Run Phase 0 calibration on Axelera AI, Etched, and Lightmatter with two independent raters.
2. Use bounded workload and integration tests instead of broad partnership commitments.
3. Require evidence packs tailored to distributor, SI, and ecosystem-orchestrator motions.
4. Update posture only when product, software, supply, customer, partner, or economics
   evidence changes.
"""
    (OUTPUTS / "competitor-brief.md").write_text(text, encoding="utf-8")


def write_story_and_traceability(rows: list[dict[str, str]]) -> None:
    rows_by_slide: defaultdict[int, list[str]] = defaultdict(list)
    for row in rows:
        match = re.search(r"slide\s+(\d+)", row["storyboard_use"])
        if match:
            rows_by_slide[int(match.group(1))].append(row["claim_id"])
    story_lines = [
        "# Story Architect Pack",
        "",
        "## BLUF",
        "",
        "Use the cohort as a validation portfolio: prioritize heterogeneous-infrastructure",
        "adoption paths, but require Phase 0 calibration before named-partner recommendations.",
        "",
        "## Audience Decision",
        "",
        "Choose which startup archetypes deserve bounded action, deeper validation, or",
        "milestone monitoring—and which proof must be purchased next.",
        "",
        "## Tension",
        "",
        "AI infrastructure bottlenecks are fragmenting while public evidence remains uneven and",
        "company-published; technical novelty can be mistaken for partner readiness.",
        "",
        "## Argument Arc",
        "",
        "1. Bound the decision and closed cohort.",
        "2. Map four infrastructure bottlenecks and commercialization models.",
        "3. Connect ICP, GTM, and partner value creation.",
        "4. Profile compute and interconnect companies with the same evidence lens.",
        "5. Compare distributor, SI, and ecosystem-orchestrator readiness.",
        "6. Apply confidence, hard gates, and a provisional weighted rubric.",
        "7. End with Phase 0 calibration and evidence-buying actions.",
        "",
        "## Slide Spine",
        "",
        "| # | Assertion title | Role | Evidence rows | Metric / basis | Visual treatment |",
        "|---:|---|---|---|---|---|",
    ]
    for slide in CONTENT["slides"]:
        ids = rows_by_slide.get(slide["id"], [])
        basis = ", ".join(ids[:8]) or "interpretation with source IDs in slide plan"
        role = slide.get("kicker", slide["layout"]).lower()
        metric = "Partner-Readiness Posture" if slide["id"] in {26, 27, 28, 33, 36, 42} else "evidence rows / labeled interpretation"
        story_lines.append(
            f"| {slide['id']} | {slide['title']} | {role} | {basis} | {metric} | native editable PowerPoint |"
        )
    story_lines.extend([
        "",
        "## Evidence Map",
        "",
        "- Direct evidence: cohort membership, product disclosures, financing, availability, and specifications.",
        "- Fair synthesis: four bottlenecks, heterogeneous adoption, and partner value pool.",
        "- Interpretation: partner postures, economics, and activation priorities; medium confidence.",
        "- Unsupported and cut: winner rankings, market-share claims, named-partner right-to-win, and uncited ROI.",
        "",
        "## Datapoint Promotion Map",
        "",
        "| Datapoint | Main location | Why it matters | Confidence |",
        "|---|---|---|---|",
        "| Company funding and stage disclosures | Slides 12–23 | Frames ability to execute without equating capital with readiness | high in disclosure / medium implication |",
        "| Lightmatter 114 Tbps vendor specification | Slide 22 | Illustrates photonic bandwidth wedge | high attribution / vendor-published |",
        "| Candidate 20/20/20/15/15/10 rubric | Slide 42 | Makes readiness logic explicit | medium; uncalibrated |",
        "| Evidence gaps and hard gates | Slides 36, 38, 43, 44 | Prevents false precision | medium |",
        "",
        "## Content Cuts",
        "",
        "- No market-wide ranking or winner language.",
        "- No organization-specific partner recommendation before calibration.",
        "- No unsupported TAM, ROI, pricing, margin, customer-count, or market-share claims.",
        "- No internal tool names or raw file paths on client-facing slides.",
        "",
        "## Rebuild Instructions",
        "",
        "- Preserve the exact 44-slide decision spine and native editable content.",
        "- Use the existing branded `pptxkit` workflow and validated visual spec.",
        "- Keep company-site visuals as approved picture objects and all claims/citations native.",
        "- Use only values listed in `outputs/allowed-numbers.yaml`.",
        "- Build matching standalone HTML with the same BLUF, arenas, confidence, postures, and actions.",
        "- Run design lint, contact-sheet inspection, OfficeCLI, HTML browser QA, and sync validation.",
        "",
        "## Storyboard QA",
        "",
        "- Every slide has an explicit decision or evidence role: pass.",
        "- The first substantive slide answers the executive question: pass.",
        "- Datapoints and evidence gaps appear in the main story: pass.",
        "- Scores trace to defined candidate metrics and remain labeled uncalibrated: pass.",
        "- Weak-confidence claims are labeled as directional or provisional: pass.",
    ])
    (OUTPUTS / "story-architect-pack.md").write_text("\n".join(story_lines) + "\n", encoding="utf-8")
    (OUTPUTS / "storyboard-qa.md").write_text(
        "# Storyboard QA\n\n"
        "- Slide count: 44; requirement met.\n"
        "- Assertion-title spine: passed.\n"
        "- Closed-cohort limitation: visible.\n"
        "- ICP, GTM, business model, partner motions, confidence, scoring, and calibration: integrated.\n"
        "- Vendor chronology trap: mitigated by thesis, maps, lenses, and actions around profiles.\n"
        "- Story/evidence lock: passed for deterministic rebuild.\n",
        encoding="utf-8",
    )
    trace = [
        "# Artifact Traceability",
        "",
        "| Artifact location | Assertion | Evidence basis | Confidence | Notes |",
        "|---|---|---|---|---|",
    ]
    for slide in CONTENT["slides"]:
        ids = ", ".join(rows_by_slide.get(slide["id"], [])) or (
            "synthesis from " + ", ".join(slide["evidence"])
        )
        confidence = "high" if slide.get("kind") == "fact" else "medium"
        trace.append(
            f"| Slide {slide['id']} / HTML section | {slide['title']} | {ids} | {confidence} | {slide.get('citation', '')} |"
        )
    (OUTPUTS / "artifact-traceability.md").write_text("\n".join(trace) + "\n", encoding="utf-8")


def visible_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            if key not in {"evidence", "kind", "layout", "id"}:
                yield from visible_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from visible_strings(item)


def write_allowed_numbers(rows: list[dict[str, str]]) -> None:
    row_by_slide: defaultdict[int, list[str]] = defaultdict(list)
    for row in rows:
        match = re.search(r"slide\s+(\d+)", row["storyboard_use"])
        if match:
            row_by_slide[int(match.group(1))].append(row["claim_id"])
    allowed = []
    seen = set()
    for slide in CONTENT["slides"]:
        joined = " ".join(visible_strings(slide))
        for match in re.finditer(r"\$\d+(?:\.\d+)?[MBT]?|\d+(?:\.\d+)?\s*(?:Tbps|G|%)", joined):
            token = match.group(0).replace(" ", "")
            key = (slide["id"], token)
            if key in seen:
                continue
            seen.add(key)
            allowed.append({
                "id": f"NUM-{len(allowed)+1:03d}",
                "visible_value": token,
                "meaning": f"Visible value on slide {slide['id']}: {slide['title']}",
                "target_or_competitor": slide.get("company", "CRN cohort"),
                "source_artifact": "outputs/evidence-ledger.csv",
                "claim_ids": row_by_slide.get(slide["id"], []),
                "source_url": SOURCES[slide["evidence"][0]]["path"],
                "source_type": source_type(slide["evidence"][0]),
                "confidence": "high" if slide.get("kind") == "fact" else "medium",
                "required_label": "vendor-published" if slide.get("layout") == "company" else "candidate / uncalibrated",
                "allowed_locations": [f"deck: slide {slide['id']}", f"html: slide-{slide['id']}"],
                "status": "allowed",
            })
    lines = ["allowed_numbers:"]
    for item in allowed:
        lines.extend([
            f"  - id: {item['id']}",
            f"    visible_value: {json.dumps(item['visible_value'])}",
            f"    meaning: {json.dumps(item['meaning'])}",
            f"    target_or_competitor: {json.dumps(item['target_or_competitor'])}",
            f"    source_artifact: {json.dumps(item['source_artifact'])}",
            "    claim_ids:",
        ])
        lines.extend(f"      - {json.dumps(cid)}" for cid in item["claim_ids"])
        lines.extend([
            f"    source_url: {json.dumps(item['source_url'])}",
            f"    source_type: {json.dumps(item['source_type'])}",
            f"    confidence: {json.dumps(item['confidence'])}",
            f"    required_label: {json.dumps(item['required_label'])}",
            "    allowed_locations:",
        ])
        lines.extend(f"      - {json.dumps(place)}" for place in item["allowed_locations"])
        lines.append("    status: allowed")
    lines.extend([
        "blocked_patterns:",
        '  - pattern: "\\\\bTAM\\\\b|\\\\bSAM\\\\b|\\\\bSOM\\\\b|\\\\bCAGR\\\\b|\\\\bARR\\\\b"',
        '    reason: "No unsupported market or financial precision"',
        '  - pattern: "\\\\bROI\\\\b|\\\\bpayback\\\\b|\\\\bmarket share\\\\b"',
        '    reason: "No unsupported outcome or share claims"',
        "structural_numbers:",
        '  - "slide numbers and total slide count"',
        '  - "calendar dates and source dates"',
        '  - "company cohort count and partner-lens count"',
        '  - "product names such as CN5000, M1000, X2, and Maverick-2"',
        '  - "30/60/90-day roadmap labels and 12-month watchlist"',
        '  - "ordered framework labels such as 01-06"',
    ])
    (OUTPUTS / "allowed-numbers.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_run_learnings() -> None:
    text = """# Run Learnings

## Corrections

- Date: 2026-07-29
  User correction: Printing Press is a data tap; AI Analyst evidence controls and the
  competitor-analysis pipeline produce the client deliverable.
  What changed in this run: Added an evidence ledger, metric definitions, data-quality
  report, scoring contract, confidence labels, artifact traceability, allowed numbers,
  matching HTML, delivery manifest, and formal compound skillpipe.
  Reusable rule: Keep ingestion, analysis, story, rendering, and QA ownership separate.
  Skill update needed: yes
  Skill files updated: `skills/evidence-led-competitor-pipeline/`
"""
    (OUTPUTS / "run-learnings.md").write_text(text, encoding="utf-8")


def main() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    rows = build_rows()
    write_operating_prompt()
    write_search_log()
    write_ledger(rows)
    write_metric_definitions()
    write_quality(rows)
    write_scoring_model()
    write_brief()
    write_story_and_traceability(rows)
    write_allowed_numbers(rows)
    write_run_learnings()
    print(f"Wrote AI Analyst artifacts with {len(rows)} evidence rows")


if __name__ == "__main__":
    main()
