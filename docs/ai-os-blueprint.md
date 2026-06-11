# AI OS Blueprint — Four C's, contextualized to a pre-sales / AI-strategy practice

Source: Nate Herk, "Claude Fable AI Operating System" (youtube.com/watch?v=8QQ_INxAhRs, 2026-06-09).
His framework, mapped onto this repo's existing stack. He builds a creator OS
(YouTube, Skool, courses); this blueprint translates it to a **deal OS**
(prospects, accounts, briefs, decks, demos).

## The framework (from the video)

Two layers, four C's, built in order:

| C | Layer | What it means | His gut check |
|---|-------|---------------|---------------|
| 1. Context | Second brain | Who you are, your business, static knowledge. CLAUDE.md as a **router** (paths to rules, skills, wikis), not a rulebook. | Ask Claude about your business — does it answer like a stranger or a co-founder? |
| 2. Connections | Second brain | Live data the brain can reach: revenue, customers, calendar, comms, tasks, meetings, knowledge. Prefers CLIs/APIs over MCP for control + cost. | Can it pull *current* numbers, not stale snapshots? |
| 3. Capabilities | AI OS | Skills, agents, automations. Skills can be just a prompt. Iterate every use: "update the skill." Assembly-line sessions; delegate parallel work to cheaper models. | Are you *doing tasks* in the OS, or just brainstorming? |
| 4. Cadence | AI OS | Every task fires one of three ways: manual / event / schedule. Routines, loops, deterministic scripts. **Earned** through battle-testing. | Does work show up already done while you sleep? |

Cross-cutting rules from the video:
- **Keys, not prompts.** A prompt is never a permission layer. Scope API keys to
  what the agent should physically be able to do. (His cautionary tale: an agent
  emailed a wrong discount code to 150k+ people because it *could*.)
- **Tool-agnostic by design.** It's all folders and markdown — keep CLAUDE.md +
  AGENTS.md, `.claude/` + `.codex/` in parallel so any harness can drive it.
- **Verify its own work.** Give the agent the verification tools a human would
  use (browser, personas, source citations) before trusting output.
- **Every slip-up is data.** Fix the instruction/skill so it never happens again.

## Mapping: his OS → this stack (what already exists)

| Four C's | His setup (creator) | This stack (pre-sales / strategy) | Status |
|----------|--------------------|------------------------------------|--------|
| Context | CLAUDE.md router, Obsidian LLM-wiki, hot cache, master index | CLAUDE.md (rules-heavy), memory files, Obsidian + Claudian vault, GBrain pages | ✅ exists, router-shape gap |
| Connections | Skool, Stripe, QuickBooks, GWS, ClickUp, Slack, Fireflies | Gmail/GCal/GDrive MCP, Notion, Exa, Fireflies skill, ScrapeCreators, GBrain semantic recall | ✅ ahead — embedding-backed recall beats his flat markdown |
| Capabilities | ~20 project + global skills, sub-agents, dynamic workflows | 40+ skills, 7-stage pipeline-runner (content-research → scorer → brief → PPTX → strategy → deal-prep → demo) | ✅ ahead — pipeline IS his "assembly line" |
| Cadence | Routines, loops, n8n pushes, scheduled refreshes | `/loop`, `/schedule` (cloud routines) available but **everything is manually triggered** | ❌ the gap |

## Tier-1 connections, translated to a deal practice

His "what apps do you open weekly" exercise, redone for this profile:

| Domain | His source | Deal-OS source |
|--------|-----------|----------------|
| Pipeline/revenue | Skool, Stripe | `convex/deals.ts` + DealForge stages, GBrain deal pages |
| Customers/prospects | Skool, YouTube | GBrain (companies, people, named accounts) |
| Calendar | Google Workspace | GCal MCP |
| Comms | GWS, ClickUp, Slack | Gmail MCP |
| Meetings | Fireflies | Fireflies skill → GBrain write-back |
| Knowledge | YouTube transcripts, local wiki | Obsidian vault, GBrain, content-research exports |
| Competitive signal | (n/a — he makes content) | content-ideas feed (ScrapeCreators), Exa |

## Gap plan (ordered, smallest first)

1. **Reshape CLAUDE.md into a router.** Today it's mostly rules. Add a short
   routing tree at the top: where skills live, where run artifacts go
   (`$CONTENT_HOME/research/`), where memory vs GBrain vs local files split
   (this split is already documented — promote it to the routing section).
   Pulse check: if the agent searches >1 min for a file you could find
   instantly, the architecture needs updating.
2. **Skill feedback loop as habit.** After every skill run: "here's what I
   liked / didn't — update the skill." Matches the existing cross-skill
   chaining rule; make it explicit at the end of pipeline stages.
3. **Cadence — the real unlock.** Candidates, in trust order (earn autonomy):
   - **Schedule**: daily `/content-ideas` feed scrape + scored feed waiting in
     the morning (read-only, low risk — start here).
   - **Schedule**: weekly GBrain write-back sweep — promote durable findings
     from the week's runs into GBrain pages (batched to limit embedding calls).
   - **Event**: meeting booked on GCal → auto `/00-account-briefing` for that
     account the evening before.
   - **Manual stays manual**: anything client-facing (PPTX delivery, emails,
     deal-prep sends) — per the "keys, not prompts" rule, the agent should not
     hold send-keys for client comms at all.
4. **Permission layer audit.** List what every connected MCP/API key can
   *physically* do (Gmail MCP can create drafts — fine; verify it cannot send).
   GBrain cost guardrails already follow this pattern; extend it to comms.
5. **Verification as a pipeline stage.** Already partially enforced (PPTX QA
   gate, preview contact sheets). Extend: demos get a browser click-through
   (agent-browser/Playwright) before being called done.

## What NOT to copy from the video

- His "other worlds" consolidation (moving every repo under one root) — partly
  done here already (OpenHands/, hyundai-ai-vault/ live in-repo); going further
  fights the cross-host plugin packaging. Keep repos separate, keep CLAUDE.md
  pointing at them.
- Creator-stack connections (Skool, YouTube analytics, Stripe) — not this
  profile. The competitor scrape is the signal layer instead.
- His flat-markdown-only brain — GBrain's semantic retrieval is strictly
  better for recurring prospects/accounts; keep the documented GBrain vs
  local-files vs memory split.
