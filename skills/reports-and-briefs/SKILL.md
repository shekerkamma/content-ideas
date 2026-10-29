---
name: reports-and-briefs
description: Generate evidence-backed GTM reports from intent, CRM, campaign, and outreach data. Use for weekly briefings, account engagement scores, ABM attribution, campaign analysis, target-account coverage, board traction reports, SDR benchmarks, and recurring reporting workflows.
---

# Reports & Briefs

Turn signal and outcome data into reports for teams, leadership, and boards. Read [references/data-source-protocol.md](references/data-source-protocol.md) first. Draft recurring schedules when requested; create them only after approval through the active host's scheduler.

## When to use

- A recurring team briefing or account review.
- Proving and measuring ABM's pipeline contribution.
- A board update or SDR coaching benchmark.

## Inputs

- Connected GTM systems or user-provided exports. Clearcue is optional.
- CRM pipeline data for attribution and outreach outcomes for performance comparisons.
- Reporting period, audience, definitions, and comparison baseline.

## Workflows

### Weekly GTM briefing

```text
Generate our Weekly GTM Signal Briefing from the available sources for the last 7 days. Include an executive summary, pipeline signal scorecard, top opportunities with evidence, competitor and trend watch, next priorities, coverage period, source list, and data gaps.
```

### Account engagement score report

```text
Account Engagement Score report for our full TAL (last 60 days). Score each on SIGNAL VOLUME (30%), SIGNAL QUALITY (40%: comments>shares>likes>views; decision-makers weighted; competitor = negative; triggers = bonus), CAMPAIGN ENGAGEMENT (30%). Output: score distribution + trend; top 10 and bottom 10 accounts; journey progression (Unaware→Aware→Considering→pipeline). Dashboard with trend arrows.
```

### ABM pipeline attribution report

```text
Generate an ABM Pipeline Attribution Report. Opportunities: [Company — Stage, Value, Close Date]. From the available sources, show signal and campaign history before opportunity creation. Apply the user's attribution definitions for SOURCED / INFLUENCED / ACCELERATED / NO OBSERVED TOUCH. Do not infer causation from sequence alone. Include denominators and comparison cohorts.
```

### Campaign performance analysis

```text
Analyze what's working across campaign types (1:1, 1:Few, Trigger-Based, Event-Based). For each: engagement metrics (response rate, account engagement rate = % showing increased signals during the campaign, meeting rate, touches to response); signal-to-campaign correlation (which signals convert; a threshold?); messaging analysis; timing. Recommendations: double down / stop / test next / optimize.
```

### TAL coverage & gap report

```text
TAL Coverage Report. TAL: [companies, tiers]. Analyze: 1) signal coverage (% with any signal, multi-stakeholder, decision-maker, zero); 2) channel coverage; 3) stakeholder coverage (committee roles with signals vs dark; single-thread risks; missing economic buyer); 4) gap prioritization (signal/channel/stakeholder gaps + recommendation each); 5) coverage trends. Coverage matrix with actions for the top 10 gap accounts.
```

### Board-ready traction report

```text
Board-ready traction report from the available sources (last 60-90 days). Include demand trends, observed market pull, ICP validation, competitive engagement, pipeline signals, a concise narrative, definitions, denominators, and material data limitations.
```

### SDR performance benchmark

```text
Benchmark our SDR team by combining available signal and outreach data. PER SDR: leads worked; percent signal-led vs cold; response rates with denominators; speed-to-signal; meetings booked. Control for assignment mix and sample size where possible. Use for coaching, not punitive ranking.
```

## Before delivering any report

Check every number and claim against retrieved query results or supplied records from this run. Show definitions and denominators. Mark missing evidence `UNAVAILABLE`; never fill gaps with plausible estimates. When safe concurrency is supported, process independent account batches concurrently, then audit consolidated totals before formatting.

## Output

A scannable briefing, scored dashboard, attribution/coverage report, or board summary.

## Tips

- Track score and signal MOVEMENT, not just levels — velocity predicts conversion.
- Lead board reports with momentum (demand accelerating, who's in-market), not absolute totals.
