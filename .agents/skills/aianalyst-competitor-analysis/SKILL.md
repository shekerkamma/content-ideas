---
name: aianalyst-competitor-analysis
description: "Use when the user wants competitor analysis run as an AI Analyst evidence-dataset workflow, including sourced competitive evidence ledgers, dataset/metric definitions, confidence scoring, quantitative datapoints, branded PPTX, interactive HTML, or GitHub Pages publishing."
---

# AI Analyst Competitor Analysis

This is the OpenHands/Codex discovery wrapper for the canonical repo-local skill.

Before work, read and follow:

- `/home/shekerk/content-ideas/skills/aianalyst-competitor-analysis/SKILL.md`
- `/home/shekerk/content-ideas/skills/aianalyst-competitor-analysis/references/dataset-contract.md`
- `/home/shekerk/content-ideas/skills/aianalyst-competitor-analysis/references/you-com-search-plan.md`
- `/home/shekerk/content-ideas/skills/aianalyst-competitor-analysis/references/datapoint-extraction.md`
- `/home/shekerk/content-ideas/skills/aianalyst-competitor-analysis/references/story-architect-pipeline.md`
- `/home/shekerk/content-ideas/skills/aianalyst-competitor-analysis/references/quality-gates.md`
- `/home/shekerk/content-ideas/skills/competitor-analysis-pipeline/references/quality-gates.md` before final client artifacts

Canonical source:
`skills/aianalyst-competitor-analysis/`

## Runtime Preamble

I'm using the `.agents` wrapper for `aianalyst-competitor-analysis`; I will follow the canonical repo-local skill so OpenHands, Codex, and Claude Code stay aligned.

## Gotchas

- Do not duplicate the canonical workflow here.
- Substantive workflow changes belong in `skills/aianalyst-competitor-analysis/`.
- This wrapper exists for OpenHands-style discovery.

## Shared PPTX Visual Contract

For every required PPTX artifact, add `<run>/visual-spec.json` to the artifact-generation
plan. Apply `pptx-visual-spec` after the evidence/story gates and before any Genspark recovery
or local PPTX build. Pass the validated spec to the chosen direct builder. Generated imagery
cannot carry competitor claims, metrics, logos, product proof, or source evidence; those
remain native, extracted, or approved assets according to the shared contract.
