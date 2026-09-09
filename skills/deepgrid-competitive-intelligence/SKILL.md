---
name: deepgrid-competitive-intelligence
description: Research and assess competitors for DeepGrid Semi in Indian commercial-vehicle ADAS and automotive semiconductors. Use for competitor dossiers, Segment A/B/C threat assessments, AIS-162 and qualification comparisons, OEM-gate analysis, messaging collision maps, strategic white space, 90-day counter-moves, recurring competitor monitoring, and evidence-controlled inputs to a client-ready DeepGrid strategy deck.
---

# DeepGrid Competitive Intelligence

Produce decision-grade competitor analysis against DeepGrid's actual GTM strategy. Do not create a generic feature comparison.

## Required references

Read these files before research or scoring:

1. [references/deepgrid-strategy.md](references/deepgrid-strategy.md) — company facts, segments, gates, scorecard, disqualifiers, claims, and messaging.
2. [references/research-contract.md](references/research-contract.md) — source hierarchy, evidence states, freshness, comparison rules, and research workflow.
3. [references/report-contract.md](references/report-contract.md) — required analytical output and PPTX handoff.

## Workflow

1. Run GBrain semantic recall for DeepGrid, the competitor, Indian CV ADAS, and the relevant segment when GBrain is available. Treat recalled material as leads, not current proof.
2. Define the competitor scope and observation date. Separate the legal company, product, semiconductor, integrator, channel, and customer program.
3. Search current primary sources first: regulations and standards bodies, certification issuers, company product documentation, regulatory filings, official tenders, GeM records, OEM/Tier-1 announcements, and attributable technical publications.
4. Record every material claim in `evidence-ledger.csv` with a stable evidence ID, source URL, publication/observation date, excerpt or faithful paraphrase, evidence status, and affected analytical control.
5. Classify evidence as `VERIFIED`, `COMPANY_CLAIM`, `INFERRED`, `UNAVAILABLE`, or `CONFLICTED`. Never silently upgrade a company claim to verified fact.
6. Build one competitor dossier using [assets/competitor-dossier.template.json](assets/competitor-dossier.template.json). Apply Segment A/B/C threat levels independently; one global threat label is insufficient.
7. Score DeepGrid's six qualification dimensions only when customer-level evidence exists. A competitor capability is not itself a customer opportunity. Use `null` when a dimension is not scorable.
8. Apply the four hard-disqualifier inversions with explicit evidence. Do not infer pilot pricing, certified availability, type-approval responsibility, or vehicle access.
9. Identify messaging collisions by persona, then state the falsifier: what evidence would invalidate DeepGrid's or the competitor's narrative.
10. Recommend three to five 90-day moves. Each move must name an allowed owner, completion criterion, evidence dependency, trigger, and stop/escalate rule.
11. Run `python scripts/validate_dossier.py <dossier.json>` before using the dossier in a comparison matrix, report, or presentation.
12. For multiple competitors, consolidate only validated dossiers into [assets/comparison-matrix.template.csv](assets/comparison-matrix.template.csv). Preserve missing data; never normalize `UNAVAILABLE` into zero.
13. Route a client presentation through `present` → `compound-competitor-analysis-pptx` → `branded-pptx-deck`. The dossier, comparison matrix, and evidence ledger are upstream analytical inputs, not substitutes for deck contracts or QA.
14. Write durable sourced findings back to GBrain when useful across sessions. Keep deliverables and evidence files in the local run directory.

## Non-negotiable analysis rules

- Compare shipping product with shipping product and roadmap with roadmap.
- Treat DGS001 as DeepGrid's current market-entry product; treat the ASIC as a planned margin event.
- Never call DeepGrid a full-stack AEBS supplier. The EBS Tier-1 and OEM own brake actuation and the AIS-162 safety case.
- Do not claim DeepGrid is mandate-ready, ASIL-D, AEC-Q100 qualified, IATF 16949 certified, or AIS-162 type-approved.
- Label the Rs 65,000→Rs 1,750 compute BOM and 45%→72% margin bridge as `PLAN FIGURE`.
- Never quote an India per-unit price for Mobileye, Bosch, Qualcomm, or Nvidia truck ADAS without a directly comparable public source.
- Do not treat a foreign company as excluded from Segment A without the specific tender's procurement and local-content rules.
- Do not treat GeM listing as proof of Class-I local-supplier status.
- Do not treat ISO 26262 process claims as equivalent to an AIS-162 vehicle type approval.
- Preserve negative and conflicting evidence.

## Output

Create a run directory containing:

```text
evidence-ledger.csv
competitors/<slug>/dossier.json
competitors/<slug>/dossier.md
comparison-matrix.csv
executive-threat-report.md
validation/
```

When a deck is requested, add the governed presentation artifacts required by `present`; do not weaken its evidence, design, editability, or QA gates.
