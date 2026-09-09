---
name: daily-sdr-ops
description: Turn fresh intent, engagement, CRM, and outreach signals into an SDR's ranked daily action list. Use for morning hit lists, instant signal response, end-of-day digests, engagement queues, profile-view review, and connection-response drafting.
---

# Daily SDR Operations

Convert fresh signals into specific morning and evening actions. If the user asks for recurrence, draft the schedule and use the active host's scheduling capability only after approval.

Read [references/data-source-protocol.md](references/data-source-protocol.md) first. Bias to action when enough verified data exists. Every lead must trace to a retrieved source record from this run, and every drafted personalization must reference a verified signal.

## When to use

- Start-of-day prioritization of who to call/message.
- Real-time response to a single new engagement.
- End-of-day review and tomorrow's priorities.
- Warming up prospects before outreach; handling profile views/connections.

## Inputs

- A connected GTM source or user-provided export containing recent signal records. Clearcue is optional.
- ICP and contactability rules; outreach history when excluding already-contacted people.

## Workflows

### Morning hit list (daily warm leads)

```text
From the available sources, pull all people with verified signals in the last 24 hours.
For each: Name, title, company; what signal they triggered; signal strength (comment > share > like).

Prioritize into a morning hit list:
🔴 CALL NOW (3-5): decision-makers who commented on something directly relevant — thinking about this RIGHT NOW.
🟡 MESSAGE TODAY (10-15): good ICP fit, engaged with relevant content. Connection request + personalized note.
🟢 ENGAGE FIRST (5-10): not ready — like/comment on THEIR recent post first to warm them up for tomorrow.

For CALL NOW and MESSAGE TODAY, write a ready-to-send message (under 300 chars) referencing their specific signal. Format as a checklist.
```

### Instant signal response

```text
Someone just engaged with our content: Name [x], Company [x], Signal [what they did].
In 30 seconds give me: 1) one-line who they are and why they matter; 2) likely pain points by industry/size; 3) a connection request (under 300 chars) referencing their engagement; 4) a follow-up for after they accept (asks a question); 5) one thing to comment on their recent activity first. Speed over perfection.
```

### End-of-day digest

```text
Pull all accessible signals from the last 24 hours. Give me an end-of-day digest:
📊 Today's numbers (total, by type, new vs returning)
🔥 Top 5 hottest leads today (who, what, act tomorrow?)
⚠️ Competitor activity today
📈 Trend watch (topic/industry/region spikes)
🎯 Tomorrow's top 3 priorities
Keep it to a 2-minute scan.
```

### Pre-outreach engagement queue

```text
From the available signal and outreach sources, pull up to 20 people with verified signals in the last 7 days who have not been contacted.
For each: name + signal; their latest post topic; a thoughtful 2-3 sentence comment that adds value (not "great post"); how it sets up later outreach. Organize as a 15-minute queue.
```

### Profile view & connection response

```text
From the available sources, pull all accessible profile-view and connection-request signals from the last 24 hours.
For each person: who they are; why they found me (other signals?); ICP fit; recent activity.
Categorize: 🔥 HIGH INTENT (view + other signals) / 👋 WORTH CONNECTING / ⏭️ SKIP.
For the first two, write an accept message (under 300 chars) and a 2-day follow-up.
```

## Output

A prioritized, message-ready checklist for the day.

## Tips

- The CALL NOW window is 24–48 hours — act before they move on.
- Treat pre-outreach engagement as a testable tactic; do not promise a response-rate lift without the user's own measured data.
- Pair the end-of-day digest with the morning hit list for a daily rhythm.
