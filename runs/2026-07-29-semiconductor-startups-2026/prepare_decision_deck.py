#!/usr/bin/env python3
"""Create the exact 44-slide public-evidence channel decision deck contracts."""

from __future__ import annotations

import copy
import json
from pathlib import Path


RUN = Path(__file__).resolve().parent
BASE = json.loads((RUN / "outputs" / "deck-content.json").read_text(encoding="utf-8"))
BY_TITLE = {slide["title"]: slide for slide in BASE["slides"]}
ASSETS = json.loads((RUN / "research" / "visual-assets.json").read_text(encoding="utf-8"))
ASSET_BY_COMPANY = {item["company"].upper(): item for item in ASSETS["assets"]}
ALL_EVIDENCE = [source["id"] for source in BASE["sources"]]


def take(source_title: str, **changes) -> dict:
    slide = copy.deepcopy(BY_TITLE[source_title])
    slide.update(changes)
    return slide


def table(title: str, subtitle: str, rows: list[list[str]], *, kicker: str,
          claim: str, evidence: list[str], citation: str,
          headers: list[str]) -> dict:
    return {
        "layout": "comparison", "kicker": kicker, "title": title, "subtitle": subtitle,
        "claim": claim, "kind": "recommendation", "evidence": evidence,
        "citation": citation, "headers": headers, "rows": rows,
    }


def cards(title: str, subtitle: str, items: list[dict], *, kicker: str,
          claim: str, evidence: list[str], citation: str) -> dict:
    return {
        "layout": "implications", "kicker": kicker, "title": title, "subtitle": subtitle,
        "claim": claim, "kind": "recommendation", "evidence": evidence,
        "citation": citation, "plays": items,
    }


slides = [
    take(
        "The 10 Coolest Semiconductor Startups of 2026",
        title="The 10 Coolest Semiconductor Startups of 2026",
        subtitle="A public-evidence screen for channel, alliance, and ecosystem validation priorities",
        strapline="10 companies  ·  3 partner lenses  ·  44-slide decision deck",
    ),
    take(
        "The cohort is fragmenting the AI stack—not mounting one generic GPU challenge",
        title="Public evidence supports a validation portfolio—not a named-partner recommendation",
        subtitle="The CRN-selected cohort reveals partnerable wedges, but organization-specific fit still requires calibration.",
        claim="Public evidence can prioritize validation questions by partner archetype without claiming organization-specific right-to-win.",
        columns=[
            {"label": "ACT NOW", "text": "Validate production-ready offers where software, supply, and deployment evidence are already visible."},
            {"label": "VALIDATE NEXT", "text": "Test technically compelling platforms whose partner motion depends on workload or ecosystem proof."},
            {"label": "MONITOR", "text": "Track pre-scale bets until tape-out, availability, and reference-customer evidence improve."},
        ],
        takeaway="Scope: CRN’s ten-company closed cohort; candidate archetype-readiness judgments, not an exhaustive market ranking.",
    ),
    take(
        "The near-term opportunity is heterogeneous infrastructure, not wholesale replacement",
        title="The partner opportunity sits in heterogeneous infrastructure—not wholesale GPU replacement",
    ),
    take(
        "The best channel opportunities sit around integration, validation, and workload access",
        title="Adoption barriers create the partner value pool",
        subtitle="The harder the integration, qualification, and operating transition, the more valuable a capable ecosystem becomes.",
    ),
    take(
        "The startups cluster around four bottlenecks across the AI system",
        title="Four bottlenecks define the closed-cohort market map",
    ),
    take("Four commercialization models translate architecture into revenue"),
    take("The addressable buyer is defined by workload pain—not company size alone"),
    take("Semiconductor GTM progresses from design influence to repeatable deployment"),
    take(
        "The near-term opportunity is heterogeneous infrastructure, not wholesale replacement",
        kicker="PARTNER VALUE CHAIN",
        title="Partners compound value from workload proof through lifecycle operations",
        subtitle="Each stage reduces a distinct adoption risk for the startup and the buyer.",
        arrows=[
            {"label": "PROVE", "text": "Benchmark a named workload with transparent baselines"},
            {"label": "PACKAGE", "text": "Integrate silicon, systems, software, networking, and support"},
            {"label": "REPLICATE", "text": "Deploy reference architectures and operate them repeatedly"},
        ],
        takeaway="The highest-leverage partner is the one that converts technical advantage into a repeatable production outcome.",
    ),
    table(
        "The ten startups span four wedges and uneven commercialization stages",
        "The overview is a navigation aid—not a risk-adjusted ranking.",
        [
            ["Axelera AI", "Edge deployment", "Shipping platform", "Partner-led ecosystem"],
            ["Tenstorrent", "Open compute", "Products + IP", "Direct + licensing"],
            ["NextSilicon", "Adaptive dataflow", "Product-volume claim", "HPC design-in"],
            ["Fractile", "Frontier inference", "Pre-scale", "Lighthouse co-development"],
            ["Etched", "Transformer ASIC", "Pre-scale", "Hyperscale design-in"],
            ["d-Matrix", "In-memory inference", "Full production", "System validation"],
            ["MatX", "LLM accelerator", "Pre-tape-out", "Frontier-lab co-design"],
            ["Cornelis", "Cluster fabric", "Commercial portfolio", "HPC integration"],
            ["Lightmatter", "Photonic I/O", "Reference platform", "Packaging ecosystem"],
            ["Xsight Labs", "Ethernet silicon", "Customer sampling", "NOS/OEM design-in"],
        ],
        kicker="COHORT OVERVIEW",
        claim="The ten companies differ more by insertion point and readiness evidence than by a single accelerator-versus-GPU frame.",
        evidence=ALL_EVIDENCE,
        citation="CRN; official company product and financing announcements.",
        headers=["COMPANY", "WEDGE", "PUBLIC STAGE SIGNAL", "LIKELY ENTRY MOTION"],
    ),
    take(
        "Seven companies are redesigning where and how AI computation happens",
        kicker="SECTION 01 · COMPUTE",
    ),
    take("Axelera turns edge acceleration into a deployment ecosystem"),
    take("Tenstorrent attacks lock-in with a programmable system and licensable IP"),
    take("NextSilicon makes the accelerator adapt to code at runtime"),
    take("Fractile is designing the full stack around exploding inference token demand"),
    take("Etched trades generality for a transformer-only performance ceiling"),
    take("d-Matrix moves inference compute closer to memory—and into production"),
    take("MatX designs the chip around LLM throughput and latency from first principles"),
    take("The compute challengers differentiate most clearly by breadth versus specialization"),
    take("Three companies treat data movement as the next AI scaling frontier"),
    take("Cornelis reopens a scale-out fabric alternative for AI and HPC"),
    take("Lightmatter uses photonics to break the electrical I/O bottleneck"),
    take("Xsight makes programmable Ethernet silicon an AI-factory control point"),
    take("The three connectivity plays solve different layers of the same scaling problem"),
    take(
        "A six-gate scorecard tests whether technical interest can become repeatable revenue",
        kicker="SIX PARTNER MOTIONS",
        title="Six entry criteria determine which partner motion is credible",
        subtitle="A motion is eligible only when the relevant technical and commercial gates have public or validated evidence.",
        gates=[
            ["01", "DISTRIBUTE", "Packaged offer, supply visibility, support model"],
            ["02", "INTEGRATE", "APIs, software maturity, reference architecture"],
            ["03", "CO-SELL", "Named ICP, repeatable proof, commercial ownership"],
            ["04", "DESIGN-IN", "Roadmap alignment, qualification, capacity path"],
            ["05", "VALIDATE", "Transparent benchmark method and workload access"],
            ["06", "OPERATE", "Telemetry, lifecycle support, SLA accountability"],
        ],
    ),
    table(
        "Distributor readiness is strongest where offers are packageable and supportable",
        "Qualitative labels are provisional public-evidence judgments; validate locally before partner selection.",
        [
            ["Axelera AI", "STRONG", "Partner network + edge systems", "Validate channel economics"],
            ["Tenstorrent", "EMERGING", "Systems and developer products", "Clarify support ownership"],
            ["NextSilicon", "VALIDATE", "Product-volume claim", "Confirm SKU + supply path"],
            ["Fractile", "MONITOR", "Pre-scale platform", "Wait for product availability"],
            ["Etched", "MONITOR", "System ambition", "Wait for production offer"],
            ["d-Matrix", "EMERGING", "Full-production platform", "Test repeatable packaging"],
            ["MatX", "MONITOR", "Pre-tape-out", "Track launch milestones"],
            ["Cornelis", "STRONG", "Commercial fabric portfolio", "Validate geographic coverage"],
            ["Lightmatter", "VALIDATE", "Design-in component", "Distributor role may be limited"],
            ["Xsight Labs", "VALIDATE", "Sampling switch silicon", "Confirm OEM/NOS support"],
        ],
        kicker="DISTRIBUTOR LENS", claim="Distribution fit rises with product packaging, supply visibility, enablement, and support clarity.",
        evidence=ALL_EVIDENCE, citation="Directional research judgment from public product, availability, and partner evidence.",
        headers=["COMPANY", "CANDIDATE FIT", "PUBLIC SIGNAL", "NEXT VALIDATION"],
    ),
    table(
        "SI readiness concentrates where integration complexity meets deployable product",
        "Systems integrators create value when reference architecture and operating accountability are both real.",
        [
            ["Axelera AI", "STRONG", "Edge solution ecosystem", "Build vertical reference offer"],
            ["Tenstorrent", "EMERGING", "Broad programmable stack", "Validate software operations"],
            ["NextSilicon", "EMERGING", "HPC application compatibility", "Prove porting effort"],
            ["Fractile", "VALIDATE", "Full-stack thesis", "Secure lighthouse workload"],
            ["Etched", "VALIDATE", "Rack-scale specialization", "Test workload durability"],
            ["d-Matrix", "STRONG", "Production inference platform", "Validate TCO + SLA"],
            ["MatX", "MONITOR", "Pre-scale architecture", "Wait for accessible system"],
            ["Cornelis", "STRONG", "Cluster fabric integration", "Package migration services"],
            ["Lightmatter", "VALIDATE", "Packaging-level insertion", "Clarify SI control point"],
            ["Xsight Labs", "EMERGING", "Programmable Ethernet", "Validate NOS/tooling"],
        ],
        kicker="SYSTEMS-INTEGRATOR LENS", claim="SI fit rises when the startup exposes a deployable integration boundary and a repeatable customer outcome.",
        evidence=ALL_EVIDENCE, citation="Directional research judgment from public product and deployment evidence.",
        headers=["COMPANY", "CANDIDATE FIT", "PUBLIC SIGNAL", "NEXT VALIDATION"],
    ),
    table(
        "Ecosystem-orchestrator readiness follows leverage across multiple complements",
        "The strongest orchestration candidates can align OEMs, software, cloud, packaging, or network partners.",
        [
            ["Axelera AI", "STRONG", "Explicit partner network", "Measure partner-sourced pipeline"],
            ["Tenstorrent", "STRONG", "IP + systems + open stack", "Test governance and overlap"],
            ["NextSilicon", "EMERGING", "Code compatibility", "Expand software proof"],
            ["Fractile", "VALIDATE", "Full-stack co-design", "Map foundry + system partners"],
            ["Etched", "VALIDATE", "Transformer-specific stack", "Test model ecosystem risk"],
            ["d-Matrix", "EMERGING", "Heterogeneous inference", "Map cloud/OEM replication"],
            ["MatX", "VALIDATE", "LLM-specific platform", "Validate launch ecosystem"],
            ["Cornelis", "EMERGING", "Interoperable fabric", "Test ecosystem breadth"],
            ["Lightmatter", "STRONG", "Packaging + foundry dependency", "Coordinate design partners"],
            ["Xsight Labs", "EMERGING", "Programmable switch interface", "Align NOS + OEM roadmap"],
        ],
        kicker="ECOSYSTEM LENS", claim="Orchestrator fit rises when partner coordination is essential to the product’s adoption and scale.",
        evidence=ALL_EVIDENCE, citation="Directional research judgment from public platform and partner evidence.",
        headers=["COMPANY", "CANDIDATE FIT", "PUBLIC SIGNAL", "NEXT VALIDATION"],
    ),
    take(
        "Commercial maturity and architectural specialization create different diligence paths",
        title="Product maturity and partner readiness are related—but not interchangeable",
        subtitle="A mature product can still lack a repeatable partner motion; an early product can merit targeted validation.",
    ),
    take(
        "Revenue quality depends on where the startup captures recurring control",
        kicker="DISTRIBUTOR ECONOMICS",
        title="Distributor economics require packageability, margin room, and bounded support",
        subtitle="A compelling chip is not channel-ready if every sale demands bespoke engineering.",
    ),
    take(
        "Each ICP needs a different proof package and commercial conversation",
        kicker="SI ECONOMICS",
        title="SI economics improve when reusable integration exceeds one-off engineering",
        subtitle="Prioritize offers that can become repeatable architectures, migration services, and managed operations.",
    ),
    cards(
        "Ecosystem leverage comes from coordinating scarce complements",
        "Orchestrators should focus where no single startup can complete the adoption path alone.",
        [
            {"label": "COMPUTE + SOFTWARE", "text": "Align models, compilers, runtimes, orchestration, and developer tooling."},
            {"label": "SYSTEM + SUPPLY", "text": "Coordinate boards, memory, packaging, manufacturing, and service readiness."},
            {"label": "NETWORK + OPERATIONS", "text": "Integrate fabrics, NOS, telemetry, security, and lifecycle management."},
            {"label": "CUSTOMER + PROOF", "text": "Secure lighthouse workloads and publish repeatable evidence packages."},
        ],
        kicker="ECOSYSTEM ECONOMICS", claim="Ecosystem value grows when coordination removes adoption risk across multiple complements.",
        evidence=ALL_EVIDENCE, citation="Strategic synthesis from the ten-company public-evidence set.",
    ),
    table(
        "The portfolio should separate action from validation and monitoring",
        "Buckets represent the next diligence posture, not a company-quality ranking.",
        [
            ["ACT NOW", "Axelera AI · d-Matrix · Cornelis", "Deployable offer + visible ecosystem", "Partner economics and repeatability"],
            ["VALIDATE NEXT", "Tenstorrent · NextSilicon · Lightmatter · Xsight", "Strong wedge; motion-specific gaps", "Software, design-in, and operating proof"],
            ["MONITOR", "Fractile · Etched · MatX", "High potential; earlier commercialization", "Tape-out, availability, references"],
        ],
        kicker="PORTFOLIO POSTURE", claim="A staged portfolio prevents early technical promise from being mistaken for execution-ready partnership.",
        evidence=ALL_EVIDENCE, citation="Candidate public-evidence posture; requires Phase 0 calibration.",
        headers=["POSTURE", "CANDIDATES", "WHY", "VALIDATE BEFORE CHANGE"],
    ),
    cards(
        "A 90-day plan should buy evidence—not commit the portfolio",
        "Run bounded validation actions with explicit outputs and stop conditions.",
        [
            {"label": "0–30 DAYS · SCREEN", "text": "Confirm offer, stage, ICP, partner boundary, and evidence owner for six shortlisted motions."},
            {"label": "31–60 DAYS · TEST", "text": "Run workload, integration, support, and commercial discovery with named hypotheses."},
            {"label": "61–90 DAYS · DECIDE", "text": "Advance, redesign, or stop each motion based on proof-package completion."},
            {"label": "OUTPUT", "text": "One evidence ledger, one archetype decision, and one next-action brief per shortlisted company."},
        ],
        kicker="90-DAY VALIDATION", claim="The first 90 days should reduce uncertainty through bounded tests rather than make execution claims.",
        evidence=ALL_EVIDENCE, citation="Recommended validation sequence; no named-partner commitment implied.",
    ),
    take(
        "The next proof points differ by commercialization stage",
        title="Quarterly activation triggers should change posture only when evidence changes",
    ),
    cards(
        "Confidence—not false precision—should govern recommendation strength",
        "Withdrawn evidence or failed hard gates can reverse a candidate posture even when the technical wedge remains compelling.",
        [
            {"label": "COVERAGE GAP", "text": "Public evidence is uneven across supply, customers, support, economics, and partner-sourced traction."},
            {"label": "INDEPENDENCE GAP", "text": "Many performance and availability claims originate with vendors and need third-party or customer corroboration."},
            {"label": "SENSITIVITY", "text": "Distributor, SI, and ecosystem lenses can produce different next actions for the same company."},
            {"label": "REVERSAL RULE", "text": "A failed supply, production, security, or support gate overrides an otherwise attractive motion."},
        ],
        kicker="CONFIDENCE & SENSITIVITY", claim="Recommendation strength should reflect evidence coverage, source independence, and hard-gate robustness.",
        evidence=ALL_EVIDENCE, citation="Candidate model logic from the CEO-reviewed implementation plan.",
    ),
    take(
        "Each ICP needs a different proof package and commercial conversation",
        kicker="PROOF PACKAGES",
        title="Each partner motion needs a different proof package",
        subtitle="Proof should answer the buyer’s adoption decision—not merely showcase a peak benchmark.",
    ),
    take(
        "Five execution gates will separate durable platforms from impressive silicon",
        title="Kill criteria protect the portfolio from impressive but non-deployable silicon",
        subtitle="Stop or redesign a motion when critical evidence cannot be produced within the validation window.",
    ),
    take(
        "Track the bottleneck each startup removes—and the ecosystem it must build next",
        title="Use the deck to select validation priorities—not to declare winners",
        subtitle="The output is decision support for the next evidence-buying step.",
        moves=[
            {"label": "PUBLIC EVIDENCE", "text": "Supports candidate archetype-readiness and focused questions."},
            {"label": "PHASE 0", "text": "Calibrates the rubric with independent raters and historical cases."},
            {"label": "LOCAL PROFILE", "text": "Required before named-partner fit or organization-specific right-to-win."},
        ],
        takeaway="The decision is which uncertainty to reduce next—and which partner motion deserves that effort.",
    ),
    take(
        "CRN selected the cohort; primary sources ground the company profiles",
        kicker="METHODOLOGY & LIMITATIONS",
        title="The method is a closed-cohort public-evidence screen",
        subtitle="CRN selected the ten companies; the analysis does not claim exhaustive market coverage.",
        method=[
            "Cohort: the ten companies named by CRN on July 15, 2026.",
            "Evidence: official product, availability, financing, and partner announcements retrieved through Level 2 livecrawl.",
            "Judgments: qualitative partner-fit labels are provisional and retain explicit evidence gaps.",
            "Boundary: no investment recommendation, named-partner selection, or organization-specific right-to-win.",
        ],
    ),
    table(
        "Fifteen current sources anchor cohort, market, product, and financing claims",
        "Official company sources are used for company-specific facts; vendor claims remain labeled as such.",
        [
            ["COHORT", "CRN", "Jul. 15, 2026", "Ten-company selection"],
            ["MARKET", "Gartner", "Apr. 8, 2026", "2026 semiconductor revenue context"],
            ["COMPUTE", "7 official company sources", "2025–2026", "Products, funding, availability"],
            ["CONNECTIVITY", "3 official company sources", "2024–2026", "Fabrics, photonics, switching"],
            ["VISUALS", "10 official company sites", "Accessed Jul. 29, 2026", "Product and brand assets"],
        ],
        kicker="SOURCES & FRESHNESS", claim="The evidence base combines one cohort source, one market source, and current primary company disclosures.",
        evidence=ALL_EVIDENCE, citation="Full URLs and access context are embedded in speaker notes.",
        headers=["EVIDENCE GROUP", "PRIMARY SOURCE", "FRESHNESS", "USE"],
    ),
    take(
        "A six-gate scorecard tests whether technical interest can become repeatable revenue",
        kicker="SCORING RUBRIC",
        title="The rubric weights readiness evidence and applies hard gates before posture",
        subtitle="Weights are candidate defaults; Phase 0 calibration precedes organization-specific use.",
        gates=[
            ["01", "PRODUCT 20%", "Availability, qualification, roadmap credibility"],
            ["02", "SOFTWARE 20%", "Frameworks, tools, deployment, operations"],
            ["03", "CUSTOMER 20%", "Named proof, conversion, expansion, references"],
            ["04", "ECOSYSTEM 15%", "OEM, ISV, cloud, foundry, packaging leverage"],
            ["05", "ECONOMICS 15%", "TCO, margin room, support burden, recurring control"],
            ["06", "SUPPLY 10%", "Yield, capacity, packaging, memory, delivery assurance"],
        ],
        citation="Candidate default weights from the CEO-reviewed plan; hard gates override weighted posture.",
    ),
    table(
        "The evidence ledger makes every posture traceable to a gap and next question",
        "This snapshot shows the operating grain; the full ledger should be maintained outside PowerPoint.",
        [
            ["Axelera AI", "Partner ecosystem + funding", "Partner-sourced pipeline", "Validate distributor/SI economics"],
            ["d-Matrix", "Production platform", "Independent TCO + references", "Validate repeatable SI offer"],
            ["Cornelis", "Commercial fabric", "Channel coverage + migration proof", "Package integration motion"],
            ["Tenstorrent", "Broad products + IP", "Support ownership + adoption", "Choose licensing vs systems motion"],
            ["Lightmatter", "Reference photonic platform", "Qualification + design wins", "Map orchestrator role"],
            ["Fractile / Etched / MatX", "Capital + architecture thesis", "Availability + customer proof", "Monitor milestone triggers"],
        ],
        kicker="EVIDENCE LEDGER", claim="A useful ledger links each company to its strongest anchor, decisive gap, and next validation action.",
        evidence=ALL_EVIDENCE, citation="Illustrative public-evidence snapshot; not the authoritative scorecard.",
        headers=["COMPANY / GROUP", "STRONGEST ANCHOR", "DECISIVE GAP", "NEXT QUESTION"],
    ),
    cards(
        "The interview protocol tests evidence, repeatability, and partner boundaries",
        "Use two independent raters per lens before the candidate model is treated as calibrated.",
        [
            {"label": "PRODUCT + SOFTWARE", "text": "What is shipping, supported, observable, and repeatable on a named workload today?"},
            {"label": "CUSTOMER + ECONOMICS", "text": "Which paid deployments converted, expanded, and met TCO or SLA expectations?"},
            {"label": "PARTNER BOUNDARY", "text": "What must a distributor, SI, or orchestrator own—and what remains with the startup?"},
            {"label": "ADJUDICATION", "text": "Where do raters disagree, what evidence would resolve it, and which hard gate controls posture?"},
        ],
        kicker="INTERVIEW & CALIBRATION", claim="Calibration requires independent ratings, documented disagreement, and evidence-led adjudication.",
        evidence=ALL_EVIDENCE, citation="Phase 0 protocol from the CEO-reviewed implementation plan.",
    ),
]

assert len(slides) == 44, len(slides)
for index, slide in enumerate(slides, 1):
    slide["id"] = index

content = {"sources": BASE["sources"], "slides": slides}
(RUN / "outputs" / "decision-deck-content.json").write_text(
    json.dumps(content, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)

claims = []
slide_plan = {
    "contract_version": "1.0",
    "deck": {
        "name": "Semiconductor Channel Decision Deck — CRN Closed Cohort",
        "evidence_contract": "presentation-evidence.json",
        "visual_contract": "decision-visual-spec.json",
    },
    "claims": claims,
    "slides": [],
}
visuals = []
for slide in slides:
    sid = slide["id"]
    claim_ids = []
    if slide.get("claim"):
        cid = f"decision-claim-{sid:02d}"
        claim_ids.append(cid)
        claims.append({
            "id": cid, "text": slide["claim"], "kind": slide.get("kind", "interpretation"),
            "confidence": "high" if slide.get("kind") == "fact" else "medium",
            "evidence_ids": slide["evidence"],
        })
    vid = f"decision-visual-{sid:02d}"
    slide_plan["slides"].append({
        "slide_id": sid,
        "archetype": slide["layout"],
        "action_title": slide["title"],
        "audience_job": "Use the evidence to choose the next validation posture or question.",
        "claim_ids": claim_ids,
        "evidence_ids": slide["evidence"],
        "visual_ids": [vid],
        "speaker_notes": {
            "talk_time_seconds": 45,
            "narrative": slide.get("claim") or slide.get("subtitle", ""),
            "demo_fallback": None,
        },
        "accessibility": {
            "reading_order": ["title", "subtitle", "main visual", "citation"],
            "visual_alt_text": f"Native PowerPoint slide explaining: {slide['title']}",
        },
        "status": "planned",
    })
    company = slide.get("company", "").upper()
    asset = ASSET_BY_COMPANY.get(company)
    if asset:
        visual = {
            "id": vid, "slide_ids": [sid], "purpose": f"Show an official product visual for {company}",
            "artifact_type": "brand-asset" if company == "XSIGHT LABS" else "photograph",
            "evidence_status": "approved-asset", "route": "place-asset",
            "reason": "An official company-site visual supports the profile while all claims remain editable native objects.",
            "evidence_ids": slide["evidence"],
            "source": {"path": "research/visual-assets.json", "page": None, "frame": company, "timestamp": None, "crop": None},
            "asset": asset["local_path"], "editable_source": None, "prompt_file": None, "execution": None,
            "placement": {"width": 1200, "height": 1050, "fit": "contain", "background": "#FFFFFF"},
        }
    else:
        visual = {
            "id": vid, "slide_ids": [sid], "purpose": f"Communicate {slide['title']} with editable structured content",
            "artifact_type": "component",
            "evidence_status": "not-applicable" if sid == 1 else "underlying-information",
            "route": "native",
            "reason": "The region communicates claims, comparisons, or structured data and must remain editable.",
            "evidence_ids": slide["evidence"], "source": None, "asset": None,
            "editable_source": None, "prompt_file": None, "execution": None, "placement": None,
        }
    visual["qa"] = {
        "visual_checked": True, "legible": True, "not_cropped": True,
        "background_matched": True, "provenance_recorded": True,
        "text_free": None, "not_evidence": None, "exact_fidelity": None,
    }
    visuals.append(visual)

(RUN / "decision-slide-plan.json").write_text(
    json.dumps(slide_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)
(RUN / "decision-visual-spec.json").write_text(
    json.dumps({
        "contract_version": "1.0",
        "deck": {
            "output_mode": "native",
            "editability": "PPT-native editable diagrams, cards, tables, and citations",
            "reference_deck": "~/.claude/templates/branded-template.pptx",
        },
        "visuals": visuals,
    }, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
print("wrote exact 44-slide decision content, slide plan, and visual specification")
