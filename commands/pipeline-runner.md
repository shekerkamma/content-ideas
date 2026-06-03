---
description: Run a use case from the latest /content-ideas feed through the AI strategy and pre-sales pipeline (vertical-scorer → strategy brief → research → deal prep).
argument-hint: "[use case number or name] — e.g. \"1\" or \"on-premise LLM for healthcare\" (omit to list)"
allowed-tools: [Bash, Read, Write, AskUserQuestion]
---

Invoke the `pipeline-runner` skill (defined in `skills/pipeline-runner/SKILL.md`) with the user's arguments: $ARGUMENTS

Follow the skill's full pipeline: load the latest feed-data.json → pick a use case →
Stage 1 (vertical-scorer gate) → Stage 2 (ai-strategy-brief) → Stage 3 (research-to-strategy, optional) →
Stage 4 (presales-deal-prep, optional). Each stage gates the next.
