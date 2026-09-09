---
name: personalized-outreach-campaigns
description: Generate outreach sequences and campaign assets from verified intent, engagement, CRM, and account context. Use for 1:1 or 1:few campaigns, multi-stakeholder messaging, trigger-based outreach, ABM briefs, ad copy, event outreach, and content matching.
---

# Personalized Outreach & Campaigns

Turns signal context into ready-to-send sequences and campaign assets. The rule across all of them: always reference the specific signal, never a generalization.

Read [references/data-source-protocol.md](references/data-source-protocol.md) first. Use safe concurrency for independent stakeholders only when supported, then align tone and coordination in a final pass. Verify every personalization claim against retrieved evidence from this run. Draft messages by default; sending or enrolling contacts requires explicit approval.

## When to use

- Build a personalized 1:1 sequence for a single account.
- Run a 1:Few campaign across a cluster of similar accounts.
- Coordinate messaging across multiple stakeholders.
- React to a trigger event, plan an event, or match content to accounts.

## Inputs

- Account or segment, audience, offer, desired channel, tone, and constraints.
- Available intent, CRM, outreach, content-library, or user-provided data. Clearcue is optional.

## Workflows

### 1:1 account outreach sequence

```text
I'm launching a personalized 1:1 ABM campaign for [Company Name]. From the available sources, pull verified account context and label inferred buying stage or pain. Build a sequence for [Primary Contact, Title]:
TOUCH 1 LinkedIn connect (Day 1, <300 chars, references a signal, not a pitch)
TOUCH 2 LinkedIn follow-up (Day 3-4, leads with a relevant insight, soft ask)
TOUCH 3 Email (Day 7, openable subject, bridges pain to solution, low-friction CTA)
TOUCH 4 Value add (Day 14, share content tied to their signals, no ask)
TOUCH 5 Direct ask (Day 21, confident 15-min ask). Write all 5, human not templated.
```

### 1:Few segment campaign

```text
Run a 1:Few campaign targeting [segment]. From the available sources, pull matching companies or contacts with verified signals in 30 days. Give a segment profile, evidence-backed messaging, per-account variations, sequence plan, success metrics, and escalation rule. Leave personalization blank when evidence is unavailable.
```

### Multi-stakeholder sequence

```text
Multi-thread play at [Company Name]. Stakeholders with signals: [list].
Write a coordinated but distinct sequence for each: Economic Buyer (ROI angle, peer tone), Champion (day-to-day pain relief, collaborative), Evaluator (technical credibility, evidence). Coordination rules: offset by 2-3 days; how a response from one changes another's message. Write all messages.
```

### Trigger-based outreach

```text
A trigger fired: Company [x], Contact [x], Trigger [x], prior signals [y/n].
Give: urgency assessment; optimal channel; THE MESSAGE (opens by referencing the trigger naturally — observant not creepy, bridges to relevance now, clear ask, <300 chars LinkedIn / <100 words email); follow-up plan; CRM note. Write the message now.
```

### ABM campaign brief generator

```text
Build a full ABM campaign brief for [segment]. From the available sources, pull verified signal data and generate: campaign overview; audience intelligence; messaging strategy; channel plan; sequence timeline; success metrics and escalation; team responsibilities. Separate verified observations from hypotheses.
```

### LinkedIn ad copy by segment

```text
LinkedIn ad copy for an ABM matched list. Segment: [x]. From the available sources, analyze verified topics, observed language, and competitor exposure. Generate five ad drafts and list the evidence or hypothesis behind each. Do not infer private pain from public engagement alone.
```

### Event-based outreach play

```text
[Event Name] is in [3 weeks]. Cross-reference my target list against verified event-attendance records and 30-day activity from the available sources. Segment by observed evidence and ICP fit. Build pre-event, at-event, and post-event plays with message drafts for the top 10 attendees.
```

### Personalized content matcher

```text
Match content to target accounts: [companies + contacts]. From the available sources, identify verified topics and observed format engagement; label journey stage as inferred. Our library: [assets]. For each, give the best content match, evidence, a short share-message draft, timing, and any content gap.
```

## Output

Ready-to-send message sequences, campaign briefs, ad variations, or content-match recommendations.

## Tips

- Specificity wins: cite the exact post/signal, not "I noticed you're interested in X".
- A 1:Few campaign's job is to identify which accounts graduate to 1:1 — set a clear escalation trigger.
- Measure trigger-based messages against the user's baseline; do not promise a performance lift without comparable outcome data.
