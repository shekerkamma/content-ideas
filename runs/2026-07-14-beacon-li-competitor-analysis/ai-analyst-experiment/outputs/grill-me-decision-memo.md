# Grill-Me Decision Memo: AI Analyst Experiment

Date: 2026-07-14

## Decision

Do not recreate the Beacon.li competitor-analysis deck with `ai-analyst` as the primary deck builder. Keep the reviewed 40-slide branded PPTX as the system of record.

Use `ai-analyst` as an analytical audit and chart-generation stage inside the competitor-analysis pipeline.

## Why

`ai-analyst` added real value in three places:

1. **Data quality:** it found that `company-table.csv` is not strict dataframe-ready CSV because several prose fields contain unquoted commas.
2. **Scoring clarity:** it converted the heatmap into derived metrics that make the key logic explicit.
3. **Chart insight:** it produced a proof-gap chart showing that Beacon has the largest gap between execution claim and proof quality.

It did not add enough value to replace the branded PPTX workflow:

- The current deck is a strategy/positioning deliverable, not a metric-readout deck.
- `ai-analyst` would likely produce a generic Marp-style analytical deck.
- Native branded PPTX QA, client styling, and GitHub Pages delivery are better handled by the competitor-analysis pipeline plus `branded-pptx-deck`.

## Fold Back Into PPTX

Recommended future revision:

1. Add a native branded version of `charts/04_proof_gap_vs_execution_claim.png` near the scored heatmap.
2. Rename the heatmap column `Threat` to `Market pressure`, or split it into:
   - `Market pressure`
   - `Beacon vulnerability`
3. Add a source-confidence note that grouped vendor rows are used for executive readability.
4. Regenerate `company-table.csv` as strict CSV or JSON if it will be reused for automation.

## Do Not Fold Back

- Do not replace the native PPTX heatmap with the Matplotlib heatmap.
- Do not rebuild the whole deck in Marp.
- Do not add all derived metrics to slides; keep the deck executive-readable.

## Pipeline Implication

Update the mental model:

```text
competitor-analysis-pipeline
→ ai-analyst audit/charts when structured scoring exists
→ grill-me critique
→ branded-pptx-deck only if the audit finds a material improvement
```

For Beacon, the material improvement is one proof-gap chart and a clearer market-pressure/vulnerability distinction.
