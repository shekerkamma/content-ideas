---
name: lead-sourcing-qualification
description: Source and qualify leads from connected GTM systems, user-provided data, and verified public context. Use to build or validate lead lists, tier accounts by ICP, score intent with explicit rules, identify decision-makers, find lookalikes, extract verticals, or draft a recurring new-lead workflow.
---

# Lead Sourcing & Qualification

Turn raw companies into a short list of evidence-backed, decision-maker-ready leads. Always qualify the company first, then the person. Read [references/data-source-protocol.md](references/data-source-protocol.md) before collecting or changing data.

## Two ways to run this

**End-to-end (default):** State the goal and constraints; run the flow and present the final list for review:

```text
I need this week's warm outreach list. ICP: {…}. Tiering rules: {…}. Scoring logic: {…}. Target roles: {…}.
Pull companies with verified signals, tier them, score them, find decision-makers, and draft proposed outreach tags.
Show me the final list with your reasoning, and flag anything you weren't sure about instead of stopping to ask.
```

When the host supports safe concurrency, process independent account batches concurrently and consolidate into a single table.

**Step-by-step (review mode):** Run Steps 1–5 below individually when you're still tuning tiering/scoring rules, don't yet trust the output, or context is getting too large (detail gets lost in very long runs).

## When to use

- Build a fresh outreach list from scratch.
- Qualify, tier, or score companies the user already has.
- Find the right person to contact at qualified accounts.
- Stand up a daily scheduled new-leads task.

## Inputs

- Connected intent, CRM, enrichment, or outreach sources, or a user-provided export. Clearcue is optional.
- ICP, tiering rules, scoring logic, target roles, time window, and exclusion rules.

## Core flow (run in order)

### Step 1 — Pull all companies with signals

```text
Use the available GTM sources to list companies with verified interactions across {Signal 1: brand signals} and {Signal 2: competitor or category signals}. Include source, observed time, and record identifier or URL.
```

### Step 2 — Assign ICP tiers

```text
Go through every company and assign Tiers using these rules.

Tiering logic:
{Tier 1 - dream ICP, e.g. B2B company based in the US or UK, 10-300 employees, in Finance/HR/Recruitment}.
{Tier 2 - good fit with 1-2 criteria relaxed}.
{Tier 3 - broader net, e.g. any SaaS or AI company in the US/UK}.

Output: Build the final spreadsheet with separate sheets per tier.
```

Optional mutation: preview proposed Tier 1 and Tier 2 tags. Apply them to the connected system only after explicit approval.

### Step 3 — Score by signal strength (0–100)

```text
Score each company 0-100 based on how hot a lead they are right now. 100 = hot, 0 = not interested.

What makes a hot lead: {Recent interactions (last 1-2 weeks) with our brand content, PLUS engagement with lead magnets or competitors. Best leads show multiple signal types, not the same signal repeated.}

Recency matters most: Fresh signals (≤14 days) score highest. Old signals alone = low score.

Weak signals to penalize: {Only top-voice interactions → cap at 15. Only one competitor, nothing else → cap at 20. Only stale (30+ day) signals → cap at 10}.

Output per company: Company: [Name] Score: [0-100] Reasoning: [1-2 sentences].
```

Reach out to companies scoring ~50–60+.

### Step 4 — Find the decision-makers

```text
For the hot and warm companies in tier 1 and tier 2, tell me the best person to reach out to who might have the best signals. Ideally, they should be in the {Person details: Sales or GTM department; for smaller companies, the founder/CEO}.
```

### Step 5 — Preview outreach changes

```text
Draft an OutreachCampaign tag change for these people, showing target system, record identifier, old value, and proposed value. Do not execute without explicit approval.
```

After approval, update a connected system when available; otherwise export a CSV. Never claim a push occurred without a successful tool response.

Before delivery, verify that every score traces to retrieved evidence from this run. Remove or mark `UNAVAILABLE` any company whose evidence cannot be confirmed.

## Scheduled variant — daily new leads

If the user requests recurrence, draft a daily schedule for the active host and create it only after approval.

```text
From the available sources, return new companies from the past 24 hours. Identify the top leads for {ICP}. Prioritize verified multi-source intent. Draft a NewLeadToReview tag change for review.
```

This is a morning radar, not the outreach list — the outreach list comes from the full flow.

## Advanced sourcing

- **Target Account List (TAL) builder:** pull companies with signals in 30 days and score into Tier 1/2/3 with names, signals, and a "why Tier 1" reason; export CSV (Company, Tier, Industry, Signal Count, Last Signal Date, Top Contact, Recommended First Action). Prioritize multi-stakeholder coverage over raw signal count.
- **Validate an existing list:** paste a company list; check which have signal activity, rate intent HIGH/MEDIUM/LOW, rank by ABM readiness, and flag the top 10 in-market accounts that are *missing* from the list.
- **Lookalikes:** describe 3–5 best wins and their pre-conversion signal pattern; find companies (or people) matching that pattern, especially "competitor content + our content in the same 30-day window."
- **Vertical extraction:** pull one industry/region segment, analyze its language and pain, and produce vertical-specific value prop + sequences.

## Output

A tiered, scored, decision-maker-ready lead list with an evidence ledger, plus optional approved system updates or a CSV export.

## Tips

- The number of stakeholders showing signals matters more than the number of signals.
- The accounts you're *missing* are often the most valuable finding.
