# Source: Felix Rieseberg, "How to be more ambitious: A tutorial for humans with models"

- URL: https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/
- Published: 2026-10-13. Fetched 2026-10-22.
- Author works on Claude at Anthropic; the advice is stated as not model-specific.
- Notes below paraphrase the article. Direct quotes are marked and kept short,
  except the deeper-version prompt, which the author offers for reuse.

## The deeper-version prompt (verbatim)

> I want a deeper version of this task, not a bigger one. Before rewriting it:
> (1) say what a top professional in this field would do here that I'm not
> asking for; (2) name the rawest material they would start from instead of
> what has already been digested for me; (3) name the specific methods and
> tools they would use; (4) say what, other than you or me, would show the
> result is right. Then rewrite my prompt to ask for exactly that.

## The four types

- **Speed** — same work, less time. Skipped; well established.
- **Altitude** — up in abstraction: the outcome, not the task. From fixing
  crashes one at a time to "keep our apps crash-free".
- **Depth** — the task the way a field-leading expert would do it, one level
  down: the underlying data, tools and problems.
- **Range** — multiple fields, using knowledge and techniques you normally
  would not.

## Altitude — the QBR ladder (Acme Inc example)

1. Give the model as much data as you have; ask what changed this quarter, why,
   and what to do.
2. Ask for the three most urgent decisions, with for/against arguments.
3. Ask for a better mechanism than a quarterly deck for catching problems early
   and moving money and people; prove from the company's history that it would
   have caught things sooner; run it beside the current one for a quarter.

Limits the author states: works best for an ultimate outcome, less well for
creative work. Tell-tale sign it fits: you will have meetings about the work.
"Claude, go make money" does not yet work for most businesses. Altitude is
where durable, human-out-of-the-loop workflows come from, and often needs a
workflow change first (crash-report fetch, version→commit mapping, access to
Windows/macOS/Linux machines to reproduce and verify fixes).

## Depth — five techniques (churn example)

1. **Same instruments as the best.** Quote: "When prompted to act like a
   professional, models often switch vocabulary without actually switching
   methods." Insist on databases and statistical models over markdown tables.
   You don't need to know the tools; the model usually does.
2. **Unreasonable goals, told they are reasonable.** 200 ms instead of 5 s. If
   it seems impossible to the model, reiterate that it is solvable and to keep
   going.
3. **Challenge what you know.** Business beliefs are rough approximations.
   Give raw data and ask the model to adversarially check assumptions — e.g.
   try to reproduce "churn is an onboarding problem" from the raw data.
4. **Produce new knowledge.** Once deep in the data, find blind spots: build a
   simulation of customers that reproduces the last year from logs, find the
   earliest unknown churn signal, and show it predicts on unseen data.
5. **Outside judge.** Do not let the model judge itself (as of October 2026).
   Ideally a tool the model can run for immediate feedback.

## Range — two techniques

1. **Nouns to verbs** (from *The Art of Innovation*, Kelley & Littman). A
   quarterly review is not "a deck"; it is getting busy people to believe a
   cause-and-effect story and decide under uncertainty in 30 minutes. The verbs
   reveal which fields help.
2. **Assemble the crew.** Production: analyst, journalist, editor; if presented,
   motion and audio designer. Red team: short seller, forensic accountant.
   Avoid role-play: don't ask it to write like a short seller; ask it to do
   what a short seller does to research a position.

All types need a computer that can install software and reach relevant data
(MCP connectors or other means).

## Why it is necessary (the closing section)

The author's argument: people are held back by what they believe possible
(self-efficacy). Evidence cited: Locke & Latham's goal-setting research
(specific hard goals beat "do your best"); Patrick Collison's "Fast" list;
Dantzig solving two unsolved problems he thought were homework; the
four-minute mile falling soon after Bannister; *The Inner Game of Tennis*;
Linux announced as "just a hobby". Practical reading for this skill: state
hard goals as achievable, show the agent the target is reachable, and allow
failed attempts.

## What the AI Labs video (youtube 92ZDgn8bgLM) adds and drops

Adds: hiring-dashboard before/after for Altitude; run the rewritten prompt in a
fresh session via `/copy`; "have another claude review it" when Codex is absent.
Drops: Depth techniques 3 and 4 above, Altitude rung 3, "tell it the goal is
reasonable", and the red-team crew. This skill restores all of them.
