# 03 — Make the skill do a job, not a book report

## The problem this chapter fixes
Claude has technically read these books. Ask about Breakthrough Advertising and
it names the frameworks straight back. Ask it to *write a landing page* using
them and you get the same AI-sounding copy as everyone else, because the model
forgets specifics and defaults to the most probable output. **A summary does not
fix that.** What fixes it is forcing the model to run the actual techniques with
the actual worked examples and decision rules in front of it.

So the test is not "does it describe the book" but **"can Claude run the book on
my work."** Two edits get you there.

## Edit 1 — Write the description as the phrases you'd actually type
The description line is the *only* thing Claude sees before deciding whether to
pull the skill off the shelf. "Knowledge from $100M Offers" gets ignored. One
that lists the jobs gets used:

```
description: The working method from "$100M Offers" by Alex Hormozi.
  Main job: take a rough offer idea and build a Grand Slam Offer end
  to end (value equation scoring, trim and stack, scarcity, urgency,
  bonuses, a written guarantee, a name). Use whenever someone says:
  build my offer, package this service, what should I charge, my
  offer isn't converting, write me a guarantee, add bonuses, or asks
  about the value equation or trim and stack. Use it even when the
  book is not named.
```

Note the last line: **"Use it even when the book is not named."**

## Edit 2 — Give SKILL.md a workflow with modes
The best book skills have two modes, one before and one after. The Challenger
Sale skill has PREP (builds a call sheet from prospect details) and GRADE (takes
the recording back and scores against the six steps, including how early the
pitch started). That turns a sales book into a loop you improve inside weekly.

Ask for this when conversion finishes:
```
Add a Workflow section at the top of SKILL.md with two modes.
PREP: before the work, take my inputs and produce a one-page plan
using the book's framework, citing the chapter each step comes from.
GRADE: after the work, take my transcript or draft and score it
step by step against the same framework, naming what I skipped.
Keep every step traceable to a chapter file.
```

## The rule
A book skill earns its place when it has **a job, a trigger, and a chapter to
point at for every step.** Anything less is a book report, and Claude already
has plenty of those.
