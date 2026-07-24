# Hermes Use Cases And Realization

Source context: Dimmitri Shapiro workshop transcript, local Hermes/GBrain notes,
and this repo's AI OS blueprint.

## Core Pattern

Hermes is useful when it is treated as an always-on personal-agent harness, not
as another chat box. The harness gives the model durable context, tools, file
access, browser/search access, scheduled routines, and MCP connections. The
realization pattern is:

1. Connect high-signal data sources.
2. Store durable knowledge in GBrain/Obsidian-style memory.
3. Add search for current enrichment.
4. Add conservative scheduled routines.
5. Keep high-risk actions human-approved.

## Use Cases

| Use case | Hermes realization | Automation level | Guardrails |
|---|---|---:|---|
| Personal daily brief | Pull calendar, inbox, Slack/Teams, recent meeting transcripts, and GBrain recall into a morning/afternoon digest. | Scheduled read-only | No send permissions; cite source links. |
| Smart contacts | Enrich meeting participants, investors, prospects, and partners from email/calendar plus You.com search, then write durable entity notes to GBrain. | Scheduled + event-triggered | Record source dates; never overwrite human-entered facts without provenance. |
| Investor/deal research | Build target lists, enrich thesis fit, prior investments, partner interests, outreach angles, and next-best action. | Manual/scheduled draft | Draft only; user sends emails/messages. |
| Pre-call account briefing | Calendar event triggers GBrain recall, company research, competitor/news scan, and a concise briefing. | Event-triggered | Block if sources are stale or uncertain. |
| Social/news signal monitoring | Watch AI, vertical, competitor, and account signals; summarize only meaningful deltas. | Scheduled read-only | Filter noise; include why the signal matters. |
| Content pipeline | Monitor creator/news clusters, rank topics, perform deep research, draft SEO/AEO content and promotional variants. | Scheduled drafts | Require editorial review before publish. |
| Self-maintenance | Nightly scan for runaway costs, model drift, failing cron jobs, stale credentials, and broken MCP servers. | Scheduled operational | Notify before risky fixes; cap spend. |
| Lightweight app builder | Build small internal tools from phone/desktop prompts, using repo skills and verification commands. | Manual delegated | Use isolated worktrees; run tests/browser checks. |
| Knowledge compaction | Refactor notes, meeting data, and research into clean durable pages and links. | Scheduled low-risk | Keep deliverables in repo files; GBrain is memory, not the system of record. |
| Security/permission audit | Report what each connected credential can physically do and recommend least-privilege changes. | Scheduled/manual | Keys are the permission layer, not prompts. |

## You.com Search Realization

The setup guide specifically positions You.com as the preferred Hermes search
API because it can collapse search and extraction work into fewer calls.

| Capability | Hermes use | Realization note |
|---|---|---|
| Search API | General current-web grounding for agent loops. | Configure `web.search_backend: you` and keep the key in `~/.hermes/.env`. |
| `livecrawl` | Full-page markdown retrieval when Hermes needs source content, not just snippets. | Add to the provider once the local Hermes wrapper supports extraction or query options for livecrawl. |
| Research API | Multi-step deep research where Hermes would otherwise run many search/reflection calls. | Best for exhaustive briefs, competitive scans, and market maps. |
| Finance Research API | Financial data, filings, company fundamentals, price/macro/news context. | Use for investor research and finance-heavy workflows instead of generic web search. |
| Freshness filters | Time-bounded claims, news, model releases, investor activity. | Prefer explicit windows such as day/week/month or date ranges. |
| Domain/geo targeting | Reduce noise for account research and regional GTM. | Use domain includes/excludes and geography where possible. |

## Recommended Initial Build Order

1. **Search provider**: configure You.com as the Hermes `web_search` backend for
   current enrichment.
2. **Memory**: keep GBrain as the durable semantic recall layer.
3. **Housekeeping cron**: add daily cost, model-route, MCP-health, and security
   scans before adding revenue-facing autonomy.
4. **Read-only briefings**: daily brief, account brief, and social/news monitor.
5. **Drafting workflows**: investor outreach, content drafts, and CRM updates.
6. **Human-approved execution**: publishing, client emails, investor messages,
   and file deletion stay approval-gated.

## Implementation Notes

- Configure Hermes search explicitly so You.com is used even when other keys
  such as Firecrawl or Exa are present.
- Keep extraction separate until You.com contents extraction is fully verified
  in this Hermes provider. Existing Exa/Firecrawl extraction can remain active.
- Do not paste API keys into prompts or repo files. Store them in
  `~/.hermes/.env` or a secret manager.
- For recurring prospects, companies, people, and verticals, perform GBrain
  recall first and write durable findings back after the run.
