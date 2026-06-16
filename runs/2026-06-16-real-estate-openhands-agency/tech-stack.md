# Tech Stack Blueprint — AI Engineering Team for Real Estate

---

## OpenHands Setup

```
VPS: DigitalOcean Droplet · $20/mo
Spec: 4 vCPU / 8GB RAM / 80GB SSD · Ubuntu 22.04
Runtime: Docker (OpenHands runs containerized)
Model: Claude Sonnet 4.6 (default) · Claude Opus for complex builds
Setup: 1 afternoon with Claude Code as setup guide
Docs: https://docs.openhands.dev/
Repo: https://github.com/All-Hands-AI/OpenHands

Monthly operating cost per client:
  VPS: $20/mo (shared across clients — split as you scale)
  API (Claude/GPT): $30-80/mo (depends on task volume)
  MCP servers: mostly free (some paid tiers for high volume)
  Total: ~$50-100/mo per active client
  Margin on $2,500/mo Growth tier: ~$2,350-$2,430/mo (94%+)
```

---

## Subagents (Real Estate Stack)

Install from VoltAgent registry. These run inside OpenHands as specialist agents.

| Subagent | Role | Use Cases It Handles |
|---|---|---|
| `document-automation` | Reads + parses contracts, generates documents | TC Bot (agreement parsing), CMA (PDF generation), listing descriptions |
| `crm-specialist` | CRM reads/writes, sequence management | Lead scoring, drip campaigns, deal pipeline updates |
| `mls-integration-specialist` | MLS API connections, listing syndication | Listing auto-post, comp pulls for CMA |
| `lead-scoring-agent` | Behavioral scoring, hot-lead surfacing | Lead scoring + drip system |
| `content-writer` | Property descriptions, email copy, social captions | Listing description system |
| `data-analyst` | Comps analysis, market trend calculations | CMA generator, commission dashboard |

**Subagent chaining pattern for TC Bot:**
```
document-automation     → reads purchase agreement, extracts dates
crm-specialist          → opens deal file in Notion, logs all parties
[scheduler layer]       → creates Google Calendar events for all deadlines
content-writer          → drafts daily status emails for all parties
crm-specialist          → tracks document checklist, flags missing items
document-automation     → closes and archives file on completion
```

---

## MCP Server Stack (Real Estate)

| Category | MCP Server | What It Does in This Stack |
|---|---|---|
| **Core** | GitHub | Code storage, version control for all builds |
| **Communication** | Gmail | Daily deal status emails, listing announcements |
| **Communication** | Twilio | SMS alerts for hot leads, contingency reminders |
| **Scheduling** | Google Calendar | Deadline tracking, appointment scheduling |
| **Scheduling** | Calendly | Client booking links in intake flows |
| **Payments** | Stripe | Client invoicing, retainer collection |
| **Database** | Postgres | Lead scoring data, deal history, pattern training |
| **Documents** | Notion | Deal files, document checklists, client records |
| **Documents** | Google Drive | Listing photos, signed contracts, archives |
| **MLS** | RESO API / RETS | Comp pulls for CMA, listing syndication |
| **Syndication** | Buffer / Hootsuite | Social post scheduling (listing announcements) |
| **CRM Bridge** | Zapier | Connect to agent's existing CRM (FUB, KVCore, etc.) |

**Cost:** Most MCP servers are free or free-tier sufficient for small agent volumes.
Twilio: ~$15-20/mo for SMS at volume. Postgres: free on Railway/Supabase free tier.

---

## Architecture Diagram (Text)

```
Agent's Workflow
      │
      ▼
[OpenHands Runtime]  ←── runs on your $20/mo VPS
      │
      ├── document-automation subagent
      │         └── reads PDFs, parses contracts, generates docs
      │
      ├── crm-specialist subagent
      │         └── reads/writes Follow Up Boss / KVCore / Notion
      │
      ├── mls-integration subagent
      │         └── RESO/RETS API → comps, listing data
      │
      ├── content-writer subagent
      │         └── listing descriptions, emails, social captions
      │
      └── lead-scoring subagent
                └── behavioral signals → hot-lead SMS alerts

MCP Servers (always-on connections):
  GitHub · Gmail · Twilio · Google Calendar · Postgres · Notion · Stripe
```

---

## What You Build First (Week 1)

1. Set up VPS + Docker + OpenHands (afternoon 1)
2. Configure MCP connections: Gmail + Google Calendar + Notion + Twilio (afternoon 2)
3. Deploy TC Bot for first client:
   - Upload their purchase agreement templates to GitHub
   - Configure the deal-file Notion database
   - Test the deadline-extraction pipeline on a dummy deal
   - Set up the daily status email templates in Gmail
4. Run one real deal end-to-end with the agent supervised (Week 1-2)
5. Declare it live at Week 2 — client pays their first month

**Time investment:** 15-20 hours for first client setup. Second client: 4-6 hours
(reuse everything, just configure their credentials and templates).
