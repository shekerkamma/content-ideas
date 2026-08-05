# The Level 3 gate test

The highest-value mechanism in this skill, and the one most often run badly or skipped.

It exists because you cannot audit context files by reading them. You wrote them, so you
supply the missing facts from memory without noticing. A cold assistant cannot, and every
gap it hits is a gap a new hire or an agent would hit too.

**Track record it earned this specification.** Across four rounds on one run it found: a
product the files never described, a voice source wrongly declared blocked, a full product
specification sitting unextracted in a source, a percentage that was simply wrong, a lead
score summing to 12 on a scale of 10, a claim the offer file made that the proof file
forbade, and a knock at a competitor that fired backwards. Document review had found none
of them.

---

## Rule 0 — test the segment you can actually sell to

The most expensive way to run this is against your most exciting segment rather than your
sellable one. Three rounds were spent on outbound to a segment that had already been demoted
to design-partner status — so "the gate failed" really meant "we cannot sell to people we
decided not to sell to."

**Pick the segment/product pair your own `02-icp.md` marks target-now and your `01-offer.md`
marks sellable today.** If those two files disagree about what is sellable, stop — that
contradiction is a bigger finding than anything the test will produce.

Run the aspirational segment too, but *after*, and score it separately.

---

## The three tasks

Always all three. The producing task alone measures the wrong thing: guardrails are easy to
get right and substance is hard, so a test with no trap tasks flatters the files.

| | Task | What it measures |
|---|---|---|
| **A** | Produce the real artifact — a cold email to a named, specific buyer with a plausible amount of detail | **Substance.** Do the files describe what you sell well enough to sell it? |
| **B** | A lead that must be refused — one that trips a disqualifier | **Discipline.** Does it disqualify *before* drafting, and name the reason? |
| **C** | A direct question whose honest answer is forbidden — margin, a competitor multiple, a retired claim | **The ceiling.** Does `04-proof.md` actually hold under pressure? |

Give the cold assistant **only** the context directory. No web, no other directories, and an
explicit instruction not to fill gaps with industry knowledge — that instruction is what
converts a plausible-sounding answer into a visible hole.

## Then demand the self-assessment

The self-assessment is worth more than the three deliverables. Ask for:

1. **A rewrite score, 1–10**, for Task A: how much would the founder rewrite? Require it to
   name specifically what was missing, and to compare its draft against `03-voice.md` move by
   move rather than in general terms.
2. **Every contradiction and gap, by filename.** Insist on filenames — it forces the finding
   to be checkable instead of a vibe.
3. **Everything it wanted to claim but the files forbade.** This is where you learn whether
   your ceiling is set correctly or is merely strangling the pitch.

Tell it to be harsh, and that the point is finding defects, not producing nice output.

---

## Scoring and the trend

One run is a snapshot; the **trend is the signal**. Record every round in
`control/gate-test-L3.md`:

| Round | Task A rewrite | B | C | What it found |
|---|---|---|---|---|

- **Rewrite 8–10** — the files are a description of a business, not a usable brain.
- **Rewrite 4–7** — real gaps remain, and they are usually one or two missing *facts*, not
  a writing problem.
- **Rewrite 1–3 and B and C pass** — Level 3 passes.
- **A improves while B or C regresses** — you have loosened the ceiling to make the pitch
  easier. Revert it. A high-scoring email built on a claim you cannot defend is the failure
  this whole system exists to prevent.

A score that stops improving between rounds means the remaining gap is not in the files. It
is that the offer does not exist yet for that buyer, and no amount of editing will fix it.

---

## What to do with each finding

**Before writing BLOCKED anywhere, prove the fact is absent.** See the
"prove absence" rule in `SKILL.md`. Three separate blockers in one run turned out to be
facts already sitting in the supplied sources.

**Fix the file, never the output.** If you find yourself editing the assistant's email, the
files are wrong. That is the same rule as Level 1, one level up.

**Re-run after fixing.** A fix you have not re-tested is a guess. Two of the errors above
were *introduced* by fixes to earlier findings, and only the next round caught them.
