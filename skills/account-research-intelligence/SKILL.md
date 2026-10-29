---
name: account-research-intelligence
description: Research target accounts before a campaign using connected GTM systems, user-provided data, and current authoritative sources. Use for account briefs, buying-committee maps, trigger monitoring, competitor exposure, journey assessment, champion discovery, and warm-intro paths.
---

# Account Research & Intelligence

Deep research before any campaign touch. ABM lives and dies on relevance, and relevance requires knowing more about the account than they expect.

Read [references/data-source-protocol.md](references/data-source-protocol.md) before collecting evidence. For multiple accounts, process independent account batches concurrently only when the active host supports it, then consolidate into one brief or table. Every claim must trace to a retrieved record or cited current source; label reasoned conclusions as `INFERRED`.

## When to use

- Before launching a campaign on a named account.
- To map who's involved in a deal and who's missing.
- To monitor target accounts for time-sensitive trigger events.
- To find internal champions or a warm intro path.

## Inputs

- A target account or account list.
- Any available intent, engagement, CRM, outreach, enrichment, or campaign data. Clearcue may be used when connected, but is optional.

## Workflows

### Account deep-dive brief

```text
I'm about to launch a campaign on [Company Name]. Give me a complete account intelligence brief.
From the available GTM sources: SIGNAL HISTORY (every person, what/when, trend); STAKEHOLDER INSIGHTS (topics each cares about, alignment/conflict); COMPETITOR EXPOSURE (who, which competitors, what topics); COMPANY CONTEXT (use current authoritative sources plus verified signals: funding, hires, launches, initiatives, tech-stack evidence, likely pain); CAMPAIGN RECOMMENDATIONS (entry point, messaging angle, channel, content to share). Include provenance and confidence in a one-page brief.
```

### Buying-committee map

```text
I'm running a campaign on [Company Name]. From the available signal and CRM sources, find every person with a verified signal. Map into a committee:
👑 Economic Buyer (VP+) / 🎯 Champion (engaged 2+) / 🔍 Evaluator-Influencer / 🔴 Potential Blocker (competitor-engaged) / ⬜ Missing Roles (who SHOULD be here but has no signals).
For each stakeholder: outreach approach, message angle, sequence order. Output as a visual committee map.
```

### Trigger-event monitor

```text
Here are my Tier 1/2 target accounts: [list].
From the available sources, check verified new signals in the last 7 days and cross-reference triggers:
📢 HIGH (act in 24h): new funding; new VP/CRO/CMO; first-time brand engagement; competitor engagement.
📋 MEDIUM (act in 1 week): posting about scaling; leadership posting a problem we solve; relevant industry content.
🔎 WATCH: first like; tracked-event attendance.
For each trigger: what, who, why it matters, a ready-to-send message, how long the window stays open. Prioritize by urgency.
```

### Competitive-exposure report

```text
From the available sources, pull all verified competitive engagement from my target list in the last 30 days.
1) Accounts in active comparison mode (engage with both us + competitors); 2) competitor-only accounts + entry strategy; 3) competitor content themes / feature gaps; 4) timing (how recent, increasing?).
For each comparison-mode account: a differentiation message for the specific competitor angle, the right moment to send, who to send to.
```

### Buying-journey assessment

```text
Give me a buying journey assessment for [Company Name]. Pull all accessible signal data and disclose source gaps.
Map the stage: ❄️ Unaware → 👀 Aware → 🤔 Considering → 🔥 Evaluating → ⚡ Ready to Buy.
Give: current stage, velocity, breadth (# stakeholders), confidence. Then the recommended play for that stage and the single next best action in 48 hours.
```

### Find champions

```text
Tell me who our champions are at {Company} with the strongest intent. Prioritise {Signal 1: brand engagement}, {Signal 2: lead magnet / competitor interaction}, {ICP: position in Sales/GTM department}.
```

### Warm-intro path finder

```text
I need to get into [Target Company]. From the available sources: 1) direct signals from anyone there; 2) known engaged contacts who connect to them; 3) similar companies with verified signal activity; 4) shared event overlap; 5) a warm-intro request template. Rank paths by warmth and evidence confidence.
```

## Output

A one-page account brief and/or buying-committee map, trigger alerts, or a ranked list of intro paths.

## Tips

- The "missing roles" gap is where deals die — find the silent economic buyer early.
- The "new VP hired" trigger is the most underused: reach new leaders in their first 30 days.
