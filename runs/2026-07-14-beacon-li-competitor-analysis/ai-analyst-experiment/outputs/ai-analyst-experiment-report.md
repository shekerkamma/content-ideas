# AI Analyst Experiment: Beacon.li Competitor Analysis

## Headline Finding

The strategic answer holds up: Beacon's differentiated claim is implementation execution. The updated official-page pass improves Beacon's enterprise-readiness score, but the analytical model still makes the proof gap explicit.

## Data Quality

- Company table rows: 11
- Scored heatmap rows: 7
- Duplicate company names: 0
- Scores outside 1-5 range: 0
- Source CSV parse warnings: 7
- Status: warning
- Warning: company-table vendors not directly scored: Appcues, Arrows, Dock, GuideCX, Pendo, WalkMe, Whatfix
- Warning: scored grouped vendors not exact company-table rows: Accenture/IBM, Pendo/Whatfix, WalkMe/SAP

Interpretation: the source CSV is usable for human review but not strict enough for direct dataframe ingestion because several prose fields contain unquoted commas. The deck also uses grouped vendors (`Pendo/Whatfix`, `Accenture/IBM`) while the source table stores some individual companies. This is acceptable for executive storytelling, but analytical outputs should explicitly document grouping and parse warnings.

## Derived Metrics

- `enterprise_advantage` = average of trust, proof, and distribution.
- `beacon_wedge_delta` = execution depth minus enterprise advantage.
- `threat_pressure_index` = weighted blend of trust, proof, distribution, system fit, and execution depth.
- `proof_gap_vs_execution` = execution depth minus proof quality.

## What AI Analyst Adds

- Beacon wedge delta: 2.3. This remains the strongest positive wedge in the scored set and supports the thesis.
- Beacon proof gap: 3.0. This is the clearest analytical reason the deck should emphasize a POC benchmark.
- Beacon trust score moves from 3 to 4 after official evidence for SOC 2, RBAC, SSO, audit trails, no backend/API/database access, and `trust.beacon.li`.
- The current heatmap is directionally right, but it should show derived gap metrics or a companion chart so the reader sees *why* proof is the bottleneck.
- The threat matrix should separate `market threat to Beacon` from `Beacon's own vulnerability`; the current single `Threat` column mixes those concepts.

## Top Threats By Weighted Pressure Index

- WalkMe/SAP: 4.8 (compete/reframe)
- Accenture/IBM: 4.8 (partner/attach)
- UiPath: 4.5 (compete on domain model)

## Recommended Deck Changes

1. Keep the branded PPTX as the system of record; do not replace it with a generic analytics deck.
2. Add or revise one chart near the heatmap: `Execution claim vs proof gap`, using chart `04_proof_gap_vs_execution_claim.png`.
3. Add a small data-quality note to the source-confidence slide: grouped vendor rows are used for executive readability.
4. Consider renaming the heatmap `Threat` column to `Market pressure`, then add a separate `Beacon vulnerability` callout for proof/distribution gaps.
5. Keep `ai-analyst` as an audit/charts layer in the pipeline, not the primary PPTX generator.

## Charts Produced

- `charts/01_scored_heatmap.png`
- `charts/02_execution_vs_enterprise_advantage_gap.png`
- `charts/03_threat_pressure_index.png`
- `charts/04_proof_gap_vs_execution_claim.png`
