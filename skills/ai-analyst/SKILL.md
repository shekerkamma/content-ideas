---
name: ai-analyst
description: 'AI-powered product analytics: ask a business question in plain English, get validated findings, publication-quality charts, and a slide deck. USE THIS for ANY data question, analytical request, metric inquiry, or visualization request. Triggers on: analyze, chart, metrics, trends, churn, revenue, conversion, retention, segments, cohorts, funnels, KPIs, forecast, or any quantitative question.'
allowed-tools:
- Bash(*)
- Read
- Write
- Edit
- Glob
- Grep
---

# AI Analyst — Claude Code Edition

Ask a business question in plain English. Get validated findings, publication-quality charts, and a slide deck.

Converted from the [AI Analyst Plugin](https://github.com/ai-analyst-lab/ai-analyst-plugin) for Claude Cowork.

## PPTX Visual Contract

When the requested output includes PowerPoint, apply the mandatory `pptx-visual-spec`
contract before visualization. The `export-results` subskill must emit and validate
`<run>/visual-spec.json`, then hand it to the selected direct deck builder. Connector output
is an upstream reference surface, not an exception to the visual-routing rules.

## Excel Input

Excel is **not** read directly by the analysis path. `pd.read_excel` on a normal business
export succeeds while making the report banner the column names, and nothing raises — a
profiler then reports five all-object columns and the analysis proceeds on garbage.

Run `/excel-ingest` first: it names every sheet with its detected header row, reports merged
cells rather than repairing them, refuses to choose between two data-shaped sheets, and writes
`<workbook>__<sheet>.csv` into the data directory. Everything downstream is unchanged.
`read_table` raises and points here when handed a workbook.

## Causal Inference and Experimentation

When the question is *did this cause that*, route by whether randomization is possible:

- **Randomization possible** → `/design-experiment`. Power and sample size before launch,
  then `experiment_stats/` for the readout. Peeking is safe only through
  `always_valid_pvalue` / `confidence_sequence`.
- **Randomization impossible** → `/causal`. Selects Pre-Post, DiD, propensity matching, or
  regression adjustment, then checks the assumption each one rests on and reports how strong
  an unmeasured confounder would need to be to erase the effect.
- **Any experiment dataset** → `/srm-check` first. A sample ratio mismatch invalidates every
  number downstream, so it runs as a gate, not a diagnostic.
- **Before trusting a repeated answer** → `/reliability`. Stability, not correctness: a wrong
  query is perfectly stable, which is exactly why this check needs no answer key.

These carry runnable estimators rather than prose. They require `scipy`, `statsmodels`, and
`scikit-learn`, which are not installed by default — the skills state this and stop rather
than approximating. Provenance and verification: `references/provenance.md`.

## What You Get

- **43 skills** — question framing, metric definition, data exploration, forecasting, experiment design, causal inference, and more
- **28 agents** — specialized analytical agents for hypothesis testing, cohort analysis, root cause investigation, causal inference, experiment readout, storytelling, chart-making, and deck creation
- **Publication-quality charts** — styled visualizations with consistent theming
- **Slide decks** — Marp-powered presentations ready for stakeholder readouts
- **Data validation** — built-in confidence scoring, source tieout, and logical validation

## Quick Start

Just ask a question:
- "Which channel has the highest churn and why?"
- "Show me MRR trends over time"
- "Compare Q1 vs Q2 conversion rates"

The `ask-question` skill is the mandatory entry point. It loads workspace context, routes to the right analytical agent, and ensures quality standards.

## Pipeline

```
Question → Frame → Hypothesize → Explore → Validate Source
    → Analyze → Investigate Root Cause → Size Opportunity
    → Design Experiment → Validate Findings
    → Storyboard → Chart → Critique → Narrate → Present → Communicate
```

## Sub-Skills (39)

| Category | Skills |
|----------|--------|
| **Entry Point** | ask-question |
| **Setup** | connect-data, setup, first-run-welcome, install-marp |
| **Framing** | question-framing, question-router, business-context |
| **Data** | explore-data, deep-profile, data-quality-check, compare-datasets, switch-dataset |
| **Analysis** | run-analysis, analysis-design-spec, define-metric, forecast, patterns, size-opportunity |
| **Quality** | guardrails, semantic-validation, triangulation, tracking-gaps |
| **Output** | export-results, visualization-patterns, presentation-themes, stakeholder-comms |
| **Memory** | archaeology, knowledge-bootstrap, log-correction, feedback-capture, view-history, view-metrics |
| **Pipeline** | manage-runs, resume-analysis, archive-analysis, close-the-loop |
| **Architecture** | architect, design-experiment |

## Agents (18)

| Agent | Purpose |
|-------|---------|
| question-framing | Turn vague questions into structured analytical problems |
| hypothesis | Create testable hypotheses |
| data-explorer | Understand available data |
| source-tieout | Validate data loading integrity |
| descriptive-analytics | Segmentation, funnels, drivers |
| overtime-trend | Time-series analysis |
| cohort-analysis | Retention curves, LTV |
| root-cause-investigator | Drill down to root causes |
| opportunity-sizer | Quantify business impact |
| experiment-designer | Design A/B tests |
| story-architect | Design narrative storyboard |
| narrative-coherence-reviewer | Review story flow |
| chart-maker | Generate styled charts |
| visual-design-critic | Review chart quality |
| storytelling | Wrap analysis in narrative |
| validation | Verify findings |
| deck-creator | Create Marp slide decks |
| comms-drafter | Slack summaries, email briefs |
