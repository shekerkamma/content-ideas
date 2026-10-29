# Rubrics for the critic

Two published rubrics worth stealing, plus how to calibrate one to your own
taste. Read this when writing or tuning `.claude/agents/auditor.md`.

## The premise most people reject

Subjective quality **is** gradable — if you have a strong enough opinion and you
write it down. Most people assume taste cannot be scored and skip straight to
functionality, which is why so much agent output is technically correct and
visibly generic.

If you know what good looks like for your work and have never written it out,
that is the missing piece. Not a better model.

## The taste rubric

From Anthropic's app-building harness. Four criteria:

| Criterion | What it asks |
|---|---|
| Design | Does it look considered, or does it look generated? |
| Originality | Would you recognize this as one of a thousand identical outputs? |
| Craft | Do the details hold up under use — spacing, states, edge cases? |
| Functionality | Does it actually work? |

**Weighting is the interesting part.** They weight toward design and
originality, because recent models already handle functionality well. The thing
they were fighting was generic output — purple gradients, AI-slop aesthetics.

The weights are not fixed. They shift them per model generation as the model's
weak spot moves. Yours should too: weight the criteria toward whatever your
current model is worst at, and re-check that on every release.

**Calibrate with examples.** A handful of reference examples — "this is what a
considered design looks like, this is what AI slop looks like" — makes the
evaluator's taste converge on yours. This generalizes better than prose
descriptions of quality, and it is the cheapest tuning available.

## The judge rubric

From Anthropic's research system. Five criteria:

| Criterion | Question |
|---|---|
| Factual accuracy | Do the claims match the sources? |
| Citation accuracy | Do the cited sources actually say that? |
| Completeness | Are all requested aspects covered? |
| Source quality | Primary sources, or the easy secondary ones? |
| Tool efficiency | Did it take a reasonable path to get here? |

Output format: scores 0.0 to 1.0 plus a pass/fail grade, from a single judge
call. They started with about **20 test cases** — a much lower bar to begin than
most people assume.

## Writing your own

1. **Name what you are actually fighting.** Not "quality" — the specific failure
   you keep seeing. Generic output, missing edge cases, plausible-sounding
   citations that do not check out.
2. **Four to six criteria.** Fewer and the score carries no information; more
   and the critic spreads thin.
3. **Weight toward the current weak spot.** Criteria the model already nails
   contribute noise, not signal.
4. **Attach reference examples per criterion.** Two is usually enough: one that
   passes, one that fails, and say why.
5. **Score 0.0 to 1.0 per criterion, one pass/fail overall.** A single failed
   criterion fails the item. Partial passes are how "mostly done" gets shipped.
6. **Re-read it after twenty runs.** A criterion nothing ever fails is either
   solved or unmeasurable. Find out which and cut or rewrite it.

## Rubric versus contract

They are different objects and the distinction matters:

- The **rubric** lives in the auditor and is stable across runs. It encodes what
  good looks like for this kind of work.
- The **contract** lives on disk, is negotiated fresh per run, and is frozen
  before work starts. It encodes what done means for this specific job.

The rubric is how the critic thinks. The contract is what it grades against.
Changing the rubric mid-run is fine; changing the contract mid-run is not.

## Expect it to be too generous

Out of the box Claude is a bad QA agent. In early runs Anthropic's QA role would
find a real bug and respond "fix it later, might take two weeks," then move on.
The same generosity that shows up everywhere else shows up here.

It was fixed by tuning against traces, not by finding a magic prompt. Two things
help immediately:

- **Remove the escape hatches.** Ban "fix later" and partial passes explicitly.
  Every soft option you leave available will get used.
- **Make failure the default.** "Score 0.0 if you cannot verify it" flips the
  burden: the work has to prove it passed, rather than the critic having to
  prove it did not.
