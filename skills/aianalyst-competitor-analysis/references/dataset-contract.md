# AI Analyst Competitor Dataset Contract

Use this contract when competitor research is converted into an evidence dataset.

## Evidence Ledger Schema

`outputs/evidence-ledger.csv` should use these columns unless a run has a documented reason to add more:

| Column | Required | Description |
|---|---:|---|
| `claim_id` | yes | Stable unique ID such as `EV-0001`. |
| `captured_at` | yes | ISO date/time or date when the claim was captured. |
| `target` | yes | Target company/product being analyzed. |
| `competitor` | yes | Company/product/source entity the row concerns. |
| `arena` | yes | Buyer-job arena, such as DAP, onboarding ops, consulting/SI, automation platform. |
| `source_title` | yes | Human-readable source title. |
| `source_url` | yes | Source URL or local artifact path. |
| `source_type` | yes | `official`, `case_study`, `pricing`, `docs`, `analyst`, `review`, `press`, `filing`, `social`, `internal`, or `other`. |
| `published_at` | no | Publication date when known. |
| `retrieved_at` | yes | Retrieval date. |
| `metric_family` | yes | `roi_financial`, `time_velocity`, `support_productivity`, `trust_compliance`, `ai_automation`, `quality_risk`, `distribution`, `pricing`, or `other`. |
| `metric_name` | no | Normalized metric name, such as onboarding cycle reduction. |
| `metric_value` | no | Numeric value if extracted. |
| `metric_unit` | no | `%`, `days`, `hours`, `$`, `count`, etc. |
| `baseline` | no | Baseline value or comparison basis when stated. |
| `comparison` | no | Comparator, e.g. before/after, competitor, industry benchmark. |
| `claim_text` | yes | Concise extracted claim, paraphrased unless quotation is necessary. |
| `quote_excerpt` | no | Short supporting excerpt within copyright limits. |
| `evidence_strength` | yes | `high`, `medium`, or `low`. |
| `confidence` | yes | `high`, `medium`, or `low`, considering source quality and specificity. |
| `confidence_reason` | yes | Why the confidence label was assigned. |
| `storyboard_use` | yes | Where the evidence belongs: heatmap, battlecard, proof gap, roadmap, datapoints, etc. |
| `notes` | no | Caveats, normalization notes, or duplicate/source issues. |

## Source Type Rules

- `official`: company product page, docs, pricing, security, trust center.
- `case_study`: vendor-published customer proof. Useful but biased.
- `analyst`: Gartner, Forrester, IDC, G2 category summaries, credible consulting reports.
- `review`: user-review sites or review excerpts; label sample-size caveats.
- `press`: funding, launch, partnership, leadership news.
- `filing`: SEC, annual report, public-company documents.
- `internal`: customer CRM, win/loss notes, implementation data, support data.

## Evidence Strength

- `high`: primary/current source with specific numeric claim, or verified internal data.
- `medium`: credible source with specific non-numeric claim, or vendor-published metric without independent verification.
- `low`: broad claim, stale source, unclear basis, or weak secondary source.

## Dataset Registration

When the run needs repeatable AI Analyst querying, create:

```text
.knowledge/datasets/<dataset_id>/
├── manifest.yaml
├── schema.md
├── quirks.md
└── metrics/index.yaml
```

Recommended `manifest.yaml` fields:

```yaml
id: beacon_competitor_evidence
display_name: "Beacon competitor evidence ledger"
type: csv
path: "runs/<run>/outputs/evidence-ledger.csv"
created_at: "2026-07-14"
grain: "one row per sourced competitive claim"
primary_key: "claim_id"
owner: "content-ideas"
contains_credentials: false
```

`schema.md` should list columns, types, allowed values, and grain. `quirks.md` should document vendor-published proof, missing dates, source imbalance, duplicated claims, and known scraping limitations. `metrics/index.yaml` should name every derived metric used in charts or scoring.

Do not put passwords, API keys, private tokens, or raw customer PII in `.knowledge`.

## Metric Definition Minimum

Every scored or charted metric needs:

- plain-English definition
- formula or extraction rule
- unit of analysis
- source columns
- allowed source types
- exclusions
- confidence basis
- limitations

Example:

```markdown
## Metric: Evidence-Backed ROI Proof Count

Plain English: Number of sourced rows for a competitor that include a specific ROI, cost, revenue, or payback claim.
Formula: COUNT(claim_id) WHERE metric_family = 'roi_financial' AND metric_value IS NOT NULL
Unit of analysis: competitor per run
Source columns: competitor, metric_family, metric_value, confidence
Exclusions: low-confidence rows unless shown separately
Limitations: Counts availability of proof, not actual product performance.
```

## Data Quality Report Minimum

Include:

- total rows
- rows by competitor
- rows by arena
- rows by source type
- rows by metric family
- numeric rows vs qualitative rows
- primary/current source share
- vendor-published proof share
- stale/missing publication dates
- duplicate or near-duplicate claims
- competitors with insufficient evidence
- claims used in final deck/story and their confidence

## Scoring Model Minimum

Each score must define:

- dimension name
- scale, usually 1-5
- scoring rule
- evidence fields used
- weight
- confidence adjustment
- examples for score 1, 3, and 5

Prefer showing both `score` and `confidence`; do not hide weak evidence behind precise-looking averages.
