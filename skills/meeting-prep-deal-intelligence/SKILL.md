---
name: meeting-prep-deal-intelligence
description: Support active deals using connected CRM, intent, engagement, calendar, and outreach data plus current authoritative context. Use for meeting preparation, multi-threading, stalled-deal revival, post-demo intelligence, re-engagement, pipeline health, and expansion or churn reviews.
---

# Meeting Prep & Deal Intelligence

Use when there are active opportunities to win. If the user requests recurring pre-meeting briefs, draft the automation and create it only through an available host scheduler after approval.

Read [references/data-source-protocol.md](references/data-source-protocol.md) first. When safe concurrency is available, process independent deals in parallel and consolidate them. Deal scores and signals must trace to retrieved evidence from this run; never estimate heat from memory.

## When to use

- Before a sales call or demo.
- To map and coordinate a multi-stakeholder deal.
- To revive quiet deals, triage post-demo, or assess pipeline health.
- To spot expansion and churn signals inside customer accounts.

## Inputs

- Deal, meeting, contact, or customer identifiers.
- Available CRM, intent, engagement, calendar, outreach, or user-provided records. Clearcue is optional.

## Workflows

### Meeting preparation brief

```text
I am preparing for a meeting with {Person name} from {Company}. Review all signals (company-level and individual) and prepare a concise, bullet-pointed briefing:
1. Pain Points & Intent (what they're trying to solve, from what they engage with)
2. Awareness of Us (site visits, content, team interactions)
3. Competitor Evaluation (which competitors)
4. Urgency Indicators (lead magnets/tools in our category)
5. Buying Committee Signals (who else at the company is active)
6. Team-Level Signals (which departments are most engaged)
7. Company Context (what they do, ICP, stage, size, funding)
```

Read the brief *before* the meeting, not during. Optionally add conversation starters, likely objections, and a multi-thread map.

### Account multi-threading

```text
I'm working a deal at [Company Name]. From the available sources, find every person with a verified signal. Map a deal influence chart: 👑 Decision Makers / 🎯 Potential Champions / 👀 Lightly Engaged / 🔴 Competitor-engaged. Label role assignments as inferred unless confirmed in CRM or by the user, and flag key roles with no observed signals.
```

### Stalled deal / account revival

```text
These deals/accounts have gone quiet: [companies].
From the available sources, check for verified signals in 30 days: contact re-engagement, new stakeholders, competitor engagement, hiring, funding, or leadership changes. For each, give evidence-backed revival confidence and a message draft. Treat close-lost as a recommendation, never an automatic CRM change.
```

### Post-demo intelligence

```text
I demoed with [Contact] at [Company] recently. From the available sources, show verified activity from this person and company in the last 7 days. Separate pre-demo from post-demo activity. Treat due diligence, comparison, and internal sharing as hypotheses unless directly confirmed. Then give an evidence-backed deal-health score, follow-up draft, timing, and objections to investigate.
```

### Re-engagement follow-up trigger

```text
People I contacted in the last 30-60 days who haven't replied: [list].
From the available signal and outreach sources, check verified new signals since my last message. For each, draft a follow-up that references the signal naturally and stays under 300 characters. Prioritize by recency; treat competitor engagement as context, not automatic proof of urgency.
```

### Pipeline health dashboard

```text
My active deals: [Company — Stage, Deal Size].
From the available sources, pull verified signal activity for these companies in the last 14 days. Score each deal: 🟢 Heating Up / 🟡 Steady / 🔴 Cooling Down / ⚫ Insufficient or no observed activity. Show the rubric, evidence, most recent signal, competitor engagement, recommended action, and data gaps.
```

### Customer expansion & churn signals

```text
Our customers: [companies]. From the available sources, find verified signals that may indicate expansion, advocacy, or churn risk. Explain alternative interpretations and confidence. For each account, recommend the next validation step and draft an appropriate play.
```

## Output

A one-page pre-call brief, deal influence map, revival plan, pipeline dashboard, or expansion/churn list.

## Tips

- The strongest post-demo signal is NEW people at the company engaging — reach them directly.
- Reconcile signal health with CRM stage; treat disagreement as a review trigger, not proof that either source is correct.
