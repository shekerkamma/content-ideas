---
name: signal-strategy
description: Design, audit, and improve a provider-agnostic buying-signal portfolio. Use when deciding what intent signals to track, mapping signals to buyer behavior, evaluating signal quality against ICP and outcomes, tuning filters, or identifying coverage gaps across GTM data sources.
---

# Signal Strategy

Design and maintain the signal portfolio that other GTM workflows depend on. An intent signal is an observed behavior or event that may precede a purchase. Multiple independent signals can strengthen confidence, but correlation is not proof of intent.

Read [references/data-source-protocol.md](references/data-source-protocol.md) first. Propose one recommended portfolio with reasoning, source requirements, cost or coverage tradeoffs, and validation metrics. Ask at most one clarifying question when the business description lacks an essential element.

## When to use

- The user is setting up or replacing an intent-data workflow and needs to decide what to track.
- The user describes their business and asks what signals to create.
- The user wants to review/clean up signals that aren't producing pipeline.

## Inputs

- Business description, ICP, geography, buying trigger, sales cycle, and current GTM systems.
- For an audit: signal definitions, 30+ days of records when available, and CRM or outreach outcomes.

## Workflow

### 1. Brainstorm signals for the business

Collect a clear business description (ICP, where clients are, what triggers them to buy), then run:

```text
Suggest a provider-agnostic signal portfolio for this business: {business description}. For each signal specify the buyer behavior, observable event, likely sources, entity level, freshness window, filters, false-positive risks, independent corroborating signals, and validation metric. Map the design to currently connected systems and identify any collection gaps.
```

Guide the user to think about *behaviors before the purchase*, not the purchase itself, and to stack multiple signal types.

### 2. Audit signal quality (run monthly)

Requires multiple signal types running 30+ days plus CRM/outreach reply data.

```text
I want to audit which signals are associated with pipeline outcomes versus generating noise.

List all active signals from the available systems or supplied export. For each signal:
1. Volume: How many people/companies captured in the last 30 days?
2. ICP Match Rate: % that match our ICP?
3. Engagement Depth: mostly likes (low intent) or comments/shares (high intent)?
4. Outreach Results: reply rate of contacted people from this signal? (I'll provide this)

Score each signal: 🟢 HIGH VALUE / 🟡 NEEDS TUNING / 🔴 LOW VALUE.
For 🟡: recommend filter or boolean adjustments. For 🔴: recommend replacements.
Also identify gaps: what buying intent are we NOT capturing? Suggest 2-3 new signals.
```

## Output

A recommended set of signals to create (step 1), or a scored signal portfolio with tuning/replacement recommendations (step 2).

## Tips

- Prefer independent corroboration over repeated events from one source; measure noise in the user's own outcome data.
- Treat the portfolio as a living system: add, pause, and resume signals constantly.
- Garbage in, garbage out: good structured signal data is what makes every other skill sharp.
