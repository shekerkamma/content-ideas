# Level 2 — The Chain: a cold outreach round

One job, five steps, each answer feeding the next. Run in a single chat, one message at a
time, in order. **Do not paste all five at once** — that collapses back to Level 1 and
produces generic mush.

**Status:** ⚠ **Unvalidated.** Never run end to end on real DeepGrid leads.

**The job, written as steps first** (framework build step 1 — if you cannot number it, you do
not understand the job):

1. Take a list of candidate organisations and find the visible signal
2. Qualify them against the ICP and kill the bad ones
3. Pick the angle for the survivors
4. Write the first email
5. Write the follow-up sequence

**Checkpoint: after STEP 2.** A human reads the disqualification list and approves it before
any writing happens. This is where quality comes from, and it is the step people skip.

---

## STEP 1 — SIGNAL

```text
Here are the organisations I am considering:
[list — name, and anything I already know]

For each, tell me:
  - what they operate (fleet type and rough size, if visible)
  - who would own an ADAS decision there
  - one visible sign they have a problem we address: a mandate exposure, a tender, an
    incident, a throughput target, a stated safety programme

Format as a table. If there is no visible sign, write "none" — do not invent one.
A row with "none" is a useful row.

Output must carry the organisation name unchanged so the next step can use it.
```

## STEP 2 — QUALIFY  → **CHECKPOINT**

```text
Take the table above. For each row, run the qualification in 01-qualify-lead.md:
verdict, segment, score out of 10, and the disqualifier if one fires.

Sort into three groups: QUALIFIED, NEEDS ONE ANSWER, DISQUALIFIED.
For each disqualified row give the one-line reason.

Do not write any outreach yet.
```

> **STOP. A human reads this before step 3.** Confirm the disqualifications are right —
> a wrong disqualification is invisible later, because that lead simply never gets written to.
> If more than half the list is disqualified, the sourcing is wrong, not the list. Fix the
> source before continuing.

## STEP 3 — ANGLE

```text
Take only the QUALIFIED rows. For each, give me:
  - the specific pressure they are under, in their words not ours
  - what it costs them, in money, time or exposure — only if it is visible; otherwise "not visible"
  - the one sentence that would make them reply
  - the claim we would need to support it, and whether 04-proof.md actually contains it

If the sentence needs a claim we do not hold, say so and give a weaker sentence we can
defend. Do not write emails yet.
```

## STEP 4 — WRITE

```text
Write the first email for each qualified organisation, using 02-first-contact.md.
Under 120 words. Open with the specific signal from STEP 1. No flattery.
Ask for a 20-minute call, propose two times.

After each email, list on one line every claim it makes and where in 04-proof.md it lives.
If a claim has no line, rewrite the email.
```

## STEP 5 — FOLLOW-UPS

```text
For each email, write 3 follow-ups: day 3, day 7, day 14.

Each one adds new information or a different angle — a mandate date, a different segment
proof point, a narrower ask. None of them says "just bumping this" or "following up".

The day 14 message gives them a clean way to say no, and means it.

Nothing in the sequence may claim anything the first email could not.
```

---

## What this chain is expected to remove from the calendar

Framework Rule 3: a level that removes no calendar work is a toy, delete it.

| Today | With the chain |
|---|---|
| Research + qualify + write a round of 10, by hand | ~15 minutes plus one human checkpoint |
| Disqualification decided ad hoc, per lead, from memory | Applied identically every round, from `02-icp.md` |
| Claims checked against whichever document was open | Every claim traced to `04-proof.md` at step 4 |

**Unproven.** Measure it on the first real round: how long it took by hand versus with the
chain, and how many of the drafts were sent without edits. Write the result in `logs/`.
If it removes nothing, delete the chain rather than keeping it for appearances.
