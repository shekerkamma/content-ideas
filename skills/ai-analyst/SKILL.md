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

## What You Get

- **39 skills** — question framing, metric definition, data exploration, forecasting, experiment design, and more
- **18 agents** — specialized analytical agents for hypothesis testing, cohort analysis, root cause investigation, storytelling, chart-making, and deck creation
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
