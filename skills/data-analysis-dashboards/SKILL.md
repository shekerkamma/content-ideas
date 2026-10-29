---
name: data-analysis-dashboards
description: Build evidence-preserving GTM and competitive comparison matrices, validated analytical outputs, and presentation-ready charts. Use for DeepGrid competitor portfolios, ICP validation, engagement patterns, and any analysis that must move from source data to a report or deck.
---

# Data Analysis & Dashboards

This is the output layer for structured GTM analysis. It uses the repo-local
`ai-analyst` skill as its analytical engine; it is not a substitute for that
methodology and is no longer a prompt-only dashboard guide.

Read these before work:

1. [references/data-source-protocol.md](references/data-source-protocol.md)
2. [references/ai-analyst-integration.md](references/ai-analyst-integration.md)
3. [references/dataset-contract.md](references/dataset-contract.md)
4. `../ai-analyst/ask-question/SKILL.md` for every analytical request
5. `../ai-analyst/run-analysis/SKILL.md` for a full pipeline or deck

## Mandatory analytical chain

1. **Frame:** state the decision, unit of analysis, comparison set, metrics,
   and non-comparable fields. Classify the request using AI Analyst L1-L5.
2. **Tie out sources:** validate every input dossier first. Record input count,
   evidence count, and last-observed date.
3. **Check quality:** report missingness, duplicate evidence IDs, invalid
   categories, and source-status mix. Missing evidence remains unavailable.
4. **Analyze:** create segment-threat, OEM-gate, evidence-confidence, and action
   matrices. Keep descriptive facts separate from analyst interpretations.
5. **Validate:** reconcile row counts to inputs, check ordinal ranges, inspect
   every `HIGH` threat against its evidence, and state confidence.
6. **Visualize:** use AI Analyst SWD styling. The chart title must communicate a
   finding, not merely name the metric. Never display `NOT_ASSESSABLE` as zero.
7. **Export:** retain machine-readable CSV/JSON, a methodology/quality report,
   and presentation-ready PNG. A PPTX stage consumes these artifacts; it must
   not recalculate them manually.

## DeepGrid competitor portfolio

Build deterministic matrices from validated DeepGrid competitor dossiers:

```bash
python3 skills/data-analysis-dashboards/scripts/build_competitor_matrices.py \
  --dossier path/to/competitor-a/dossier.json \
  --dossier path/to/competitor-b/dossier.json \
  --out runs/<run>/analysis

python3 skills/data-analysis-dashboards/scripts/validate_analysis_run.py \
  runs/<run>/analysis
```

Required outputs:

- `segment-threat-matrix.csv`
- `oem-gate-matrix.csv`
- `evidence-confidence-matrix.csv`
- `action-matrix.csv`
- `analysis-summary.json`
- `data-quality-report.md`
- `segment-threat-overview.png` when chart dependencies are available

Use the CSV matrices for comparison tables and the PNG only as a supporting
visual. For client PPTX work, route the validated artifacts through
`skills/present/` and the branded presentation workflow required by the repo.

## Other GTM analysis

For ICP, engagement, or audience-overlap analysis, use the same mandatory
chain. Define denominators and metric semantics before calculation, show
coverage gaps, distinguish correlation from causation, and never infer absent
CRM outcomes. Clearcue is an optional adapter; files, databases, or other
connectors may supply the input.

## Stop conditions

- Stop quantitative ranking when fewer than two comparable competitors exist;
  output a single-company diagnostic instead.
- Do not average ordinal threat labels into a synthetic score unless the user
  explicitly approves the weighting.
- Do not treat company claims as independently verified evidence.
- Do not produce a client-ready chart or deck if source tie-out or validation
  fails.
