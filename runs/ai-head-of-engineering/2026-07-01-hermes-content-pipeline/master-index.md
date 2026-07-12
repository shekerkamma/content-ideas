# Hermes Content Pipeline - AI Head of Engineering Run

Date: 2026-07-01

## Build Idea

Build a Hermes-based content pipeline that monitors AI/operator-relevant source clusters, ranks content opportunities, performs source-grounded research, drafts SEO/AEO-friendly long-form content, and queues promotional variants for human editorial approval.

## Founder / Operator Context

- Operator wants concrete Hermes use cases, not more abstract skill framework.
- Target workflow is the content pipeline described in `docs/hermes-use-cases-and-realization.md`.
- Intended usage is business-facing content production, likely around AI agents, enterprise AI, Hermes/OpenClaw-style workflows, and implementation narratives.

## Constraints

- First implementation must fit a 30-day build.
- Draft-only workflow. No automatic publishing in v1.
- Search provider should prefer You.com for current web grounding.
- GBrain / Obsidian-style memory is the durable knowledge layer.
- High-risk actions require human approval.
- Repo files remain the system of record for deliverables.
- No API keys are stored in repo files.

## Role Order And Status

| Role | Status | Output |
|---|---|---|
| Scope Killer | complete | `01-scope-killer.md` |
| 30-Day Scope Architect | complete | `02-scope-architect.md` |
| Stack Picker | complete | `03-stack-picker.md` |
| Build vs Buy Auditor | complete | `04-build-vs-buy.md` |
| Build Estimator | complete | `05-build-estimator.md` |
| AI Use-Case Validator | complete | `06-ai-fit.md` |
| Custom Internal Tool Designer | complete | `07-tool-designer.md` |
| Pre-Launch Auditor | complete | `08-pre-launch-audit.md` |
| 30-Day Build Roadmap | complete | `09-roadmap.md` |

## Key Decisions

- The clear-cut use case is: **Hermes drafts a source-grounded content brief and article package from monitored source clusters, then queues it for human review.**
- The first 30-day version should not auto-publish.
- The first version should not build a full CMS or analytics platform.
- You.com search/livecrawl should be the preferred current-web grounding tool.
- Firecrawl/Exa can remain fallbacks where extraction is already wired.
- GBrain write-back is in scope for durable source, topic, and entity memory.
- Editorial approval, cost caps, and source provenance are launch gates.

## Open Flags

- Live vendor pricing was not validated in this run; production cost model needs a pricing check before budget approval.
- Exact source cluster list must be finalized before Week 1 Friday.
- Target audience and editorial voice must be finalized before draft evaluation.
- Existing Hermes local API/config shape must be confirmed before implementation.

## Implementation Package

The first implementation package is in `implementation/`.

It includes source configuration, pipeline config, queue schemas, run folder layout, cron workflow, a Hermes cron job template, the plain-English cron creation prompt, a local runner, and a smoke validator.

## Smoke Test

Offline smoke output was generated under `runs/hermes-content-pipeline-smoke/`.

Result:
- `runner.py` completed with `status=success`.
- `validate_artifacts.py` completed with `artifact validation ok`.
- Generated 14 source items, 4 topic clusters, 3 research briefs, 1 draft package, 3 memory candidates, and a run log.
