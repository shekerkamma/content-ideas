# Level 1 — The Saved Prompt

**Task chosen:** qualify an inbound or sourced lead against the ICP before anyone writes to
them. This is the most repeated task in `06-process.md` — it fires on *every* lead regardless
of source, and it is the step whose absence costs the most (a week spent on a 3-truck
operator that the disqualifier list would have killed in ten seconds).

**Status:** ⚠ **Unvalidated.** Rule 2 of the framework says automate what you have done by
hand ten times. DeepGrid has no record of ten hand-run qualifications, and there is no gold
standard version to compare against. Run this by hand on ten real leads, keep the ten
answers, and only then trust the prompt. Until that happens this is a draft, not a Level 1.

**Done when:** you can paste a raw lead and send the verdict with zero edits, 8 times out of 10.

**Move up when:** you notice you always run this, then research, then write — three prompts
in a row. That is Level 2.

---

## The prompt

```text
ROLE
You qualify leads for Deepgrid Semi Pvt Ltd, an Indian ADAS compute company selling
driver-assistance kits to fleets, OEMs and government buyers.

INPUT
Here is the lead, exactly as it arrived:
[paste the email, the note, the LinkedIn message, the tender line — raw, unedited]

OUTPUT
One verdict block, in this order, nothing else:

  VERDICT      QUALIFIED / DISQUALIFIED / NEEDS ONE ANSWER
  SEGMENT      which 02-icp.md segment they fall in, or "none"
  SCORE        n/10, using the 06-process.md lead score, with the signals that earned it
  WHY          two sentences maximum
  NEXT STEP    the single next action, with an owner
  DO NOT SAY   any claim this lead would tempt us into that 04-proof.md forbids

RULES
- Check the disqualifier list in 02-icp.md FIRST, before anything else. If a disqualifier
  fires, the score is 0 and you stop. Do not score a disqualified lead.
- A disqualified lead is a good outcome. Say so plainly. We would rather lose a lead than
  waste a week.
- If the lead needs certified AEBS today, they are disqualified — AIS-162/188 is a path via
  NATRAX, not held.
- Never invent a fleet size, a budget, a timeline or a buying trigger. "Not stated" is a
  real answer and the correct one.
- If one missing fact would flip the verdict, return NEEDS ONE ANSWER and name that single
  question. Do not ask two.
- AD3 and AD4 interest never becomes pipeline regardless of score. Mark it discovery.
- No preamble, no summary, no offer to help further. The verdict block only.
```

---

## Test set — run these three before trusting it

Three real shapes, with the answer they must produce.

| # | Input | Required verdict |
|---|---|---|
| 1 | "We run 3 trucks, interstate. Interested in your ADAS. What's the price?" | DISQUALIFIED, score 0, sub-five-truck disqualifier, no price quoted |
| 2 | Container terminal, ~200 yard tractors, asking about driverless | NEEDS ONE ANSWER — design-partner track, not a sale; AD4 is discovery |
| 3 | State transport undertaking tender, 400 buses, AIS-140 line item | QUALIFIED, high score — eligibility not certification is the gate |

If it scores lead 1 above zero, or quotes a price to it, the prompt is wrong. Fix the prompt,
not the output.
