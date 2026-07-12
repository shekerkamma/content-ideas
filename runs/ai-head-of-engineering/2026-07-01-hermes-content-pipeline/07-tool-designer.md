# 07 - Custom Internal Tool Designer

This workflow does not need a full app in v1, but it does need a clear internal operating surface.

## Data Model

| Object | Key Fields | Source Of Truth |
|---|---|---|
| Source | name, type, URL, priority, cadence, allowed extraction method | `sources.yaml` or markdown config |
| Source item | source, URL, title, published date, fetched date, transcript/content path | JSON queue |
| Topic cluster | theme, related items, freshness, business relevance, rank score | generated markdown/JSON |
| Research brief | thesis, evidence, citations, risks, angle, missing facts | markdown artifact |
| Draft package | title, outline, article, citations, variants, status | editorial queue |
| Review decision | approved, revise, reject, notes, reviewer, date | markdown frontmatter |
| Memory entry | topic, entity, source, summary, provenance, write-back date | GBrain/Obsidian |
| Run log | run id, duration, model route, cost estimate, errors | JSON/CSV log |

## Main Views

1. Topic triage board: ranked opportunities with reasons.
2. Brief and draft detail: source evidence, draft, variants, review status.
3. Run health dashboard: last run, errors, cost, source failures.

## Roles And Permissions

| Role | Permissions |
|---|---|
| Operator | Configure sources, approve runs, approve drafts, edit queue |
| Editor | Review briefs and drafts, approve/reject/revise |
| Hermes agent | Read sources, write queue artifacts, draft content, write logs |
| Publisher | Manual publish only after approval |

## Approval Flow

1. Hermes creates topic ranking.
2. Operator approves topics for full draft generation or allows top N under cost cap.
3. Hermes writes research brief and draft package.
4. Editor approves, rejects, or requests revision.
5. Publisher manually publishes outside v1 automation.

## Automation Triggers

- Daily scheduled scan.
- Manual "generate brief" for selected topic.
- Manual "generate draft package" from approved brief.
- Post-review memory write-back.
- Daily cost/source health summary.

## Integrations

- You.com search/livecrawl for current web grounding.
- GBrain/Obsidian for durable memory.
- Hermes cron/system cron for scheduling.
- Optional later: CMS, social scheduler, analytics.

## Not In This Tool

- Auto-publishing.
- Full CMS.
- Multi-user SaaS permissions.
- Paid ad generation.
- Automated comments/replies.
- Fully autonomous editorial judgment.

