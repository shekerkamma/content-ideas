---
description: Run a use case from the latest /content-ideas feed through the AI strategy and pre-sales pipeline (vertical-scorer → strategy brief → research → deal prep).
argument-hint: "[use case number or name] — e.g. \"1\" or \"on-premise LLM for healthcare\" (omit to list)"
allowed-tools: [Bash, Read, Write, AskUserQuestion]
---

Invoke the `pipeline-runner` skill (defined in `skills/pipeline-runner/SKILL.md`) with the user's arguments: $ARGUMENTS

Follow the skill's full pipeline: load the latest /content-ideas feed → pick a use case →
`GBrain Recall` → `content-research` → `vertical-scorer` → `ai-strategy-brief` →
`branded-pptx-deck` → `research-to-strategy` (optional) → `presales-deal-prep` (optional) →
`GBrain Write-back`. Each stage gates the next.

For repo-local Stage 0/1 execution, the same use-case handoff can be run with:

```bash
python3 skills/content-ideas/scripts/pipeline_runner.py --list
python3 skills/content-ideas/scripts/pipeline_runner.py 1
```
