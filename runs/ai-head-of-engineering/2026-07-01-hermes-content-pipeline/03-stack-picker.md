# 03 - Stack Picker

## Stack Principle

This is an agent workflow, not a SaaS app first. Use Hermes, files, search, memory, and scheduled jobs before building a UI.

## Layer Choices

| Layer | Choice | Alternatives | Reasoning |
|---|---|---|---|
| Agent harness | Hermes | OpenClaw, custom lightweight harness | Hermes matches the target use case and supports scheduled agent workflows. |
| Scheduler | Hermes cron / system cron | GitHub Actions, VPS cron | Local scheduled jobs are fastest for v1; cloud scheduling can come later. |
| Search | You.com Search + livecrawl where supported | Exa, Firecrawl | You.com is preferred for current-web grounding; Exa/Firecrawl remain extraction fallbacks. |
| Memory | GBrain + Obsidian-style markdown | Local markdown only, vector DB | GBrain gives durable semantic recall; markdown keeps deliverables inspectable. |
| Storage | Repo run files + JSON/markdown queues | SQLite, Supabase | File-first is enough for 30 days and keeps artifacts portable. |
| Draft generation | Claude Sonnet default, Haiku for extraction, Opus for hard synthesis | OpenAI GPT-4.1/5 family, Gemini | Model routing reduces cost while keeping quality for reasoning-heavy steps. |
| Review queue | Markdown/Obsidian folder | Notion, custom Next.js UI | Avoids UI build tax in v1. |
| Analytics | CSV/JSON run logs | PostHog, Plausible | Track workflow quality first, not traffic attribution. |
| Hosting | Always-on local Mac/VPS | Vercel app, container platform | The workflow is scheduled and file-oriented, not user-facing web traffic. |

## Ramp-Time Flags

- Full dashboard: adds 5-10 days and should be deferred.
- CMS integration: adds credential and publish-risk complexity; defer.
- Multi-channel scheduling: adds platform-specific auth and policy risk; defer.
- Vector DB migration: not needed until local/GBrain memory hits limits.

## Recommended V1 Stack

Hermes + You.com + GBrain/Obsidian + repo markdown/JSON queues + scheduled jobs + model routing + human editorial queue.

