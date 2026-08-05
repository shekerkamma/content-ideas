# Level playbooks — the concrete structures

`level-gates.md` says when a level passes. This file says what to actually build.
Every template below is load-bearing: the failure modes they prevent are the ones that
recur. Do not paraphrase them into something looser.

---

## Level 1 — the four-part prompt

A vague prompt produces soup. A prompt has four parts and nothing else.

```text
ROLE     You write [task] for [company], a [what you do] for [who you serve].
INPUT    [the raw material, pasted verbatim — notes, transcript, lead record]
OUTPUT   [exact shape: length, sections, what must appear, what must not]
RULES    - [banned phrasing]
         - [one ask only / one decision only]
         - [voice constraint]
```

**Build order:** pick the most repeated task, do it manually once more and keep that
version as the gold standard, write the prompt, test on three real inputs, compare to the
gold standard.

**Fix the prompt, not the output.** If you edit the output every time, the prompt is wrong.

---

## Level 3 — the six files and the project instructions

The single highest-leverage level. Everything above it inherits its quality.

Files are numbered because the project instructions reference them by name:

| File | Must contain | The part people skip |
|---|---|---|
| `01-offer.md` | What you sell, what it costs, what's included and excluded, what the client must do, typical result and timeline | Specific numbers, not ranges of adjectives |
| `02-icp.md` | Company size, role, industry, budget, buying triggers — **and disqualifiers** | **Disqualifiers matter more than qualifiers.** Who wastes your time, and why |
| `03-voice.md` | Three emails and three posts you actually wrote and were happy with, plus a banned-words list | Real samples. Not a description of your tone |
| `04-proof.md` | Case studies, numbers, names you are permitted to use, before/after — each with source and date | Only what you can evidence. This file is the ceiling on every claim |
| `05-objections.md` | The 10 things prospects say to avoid buying, and your actual best response to each | **From real conversations, not imagination** |
| `06-process.md` | Every step from first contact to signed: who does it, how long it takes | Include the ugly manual bits |

### Project instructions template

```text
You work on client acquisition for [company]. Read the project files before answering
anything about offer, pricing, targeting or positioning. Never invent a claim, number or
case study that isn't in 04-proof.md. Voice: match 03-voice.md. Short sentences. No
corporate filler. Never use the banned words list. When I give you a lead, always check
them against 02-icp.md first and tell me if they're a bad fit before writing anything. I
would rather lose a lead than waste a week. If you don't have enough information to do the
job well, ask me one question. Don't guess and don't pad.
```

**Test:** open a fresh chat in the project and ask for a cold email with no other context.
If it does not sound like you, the files are too thin — fix the files, not the prompt.

---

## Level 5 — the deliverable machine

Start from the proposal that actually closed. Strip it to structure: sections, headings,
what is fixed, what changes per client. Save as `template.md` beside the `SKILL.md`.

Input is raw call notes. Output is the finished file, not text to paste into one.

**Test against three past deals** and compare to what you actually sent.

---

## Level 7 — the six-block agent brief

An agent given a fuzzy goal will confidently do the wrong job for forty minutes. Every
block is required.

```text
GOAL              [the finished outcome, with a number and a deadline]
INPUTS            [exact paths — /inputs/leads.csv, /reference/, named skills]
STEPS             1. …  2. …  (explicit, ordered, with thresholds)
OUTPUT            [one artifact, exact path and format, plus what to report in chat]
GUARDRAILS        - Never invent contact details. Blank is fine, wrong is not.
                  - Never invent a buying signal. "None found" is a real answer.
                  - Draft only. Send nothing.
                  - If fewer qualify than requested, give fewer. Do not lower the bar.
STOP AND ASK ME IF - more than half the list fails the ICP check
                  - you cannot access a file or connector
                  - you are unsure about pricing or a claim about results
```

The last block is what separates an agent that helps from one that produces fifty
confident lies.

**Working folder:**

```text
/client-acquisition
  /inputs      lead lists, notes, transcripts
  /outputs     finished work
  /reference   the six Level-3 files
  /logs        what it did, every run
```

Run on manual approval the first three times. Read the log. Fix the brief, not the output.

---

## Level 8 — the four roles

| Agent | Job | Never does |
|---|---|---|
| Scout | Finds and scores leads. Nothing else | Writes copy |
| Writer | Turns a scored lead into outreach and proposals | Decides who to contact |
| Closer | Handles replies, objections, booking, call prep | Cold outreach |
| Auditor | Checks everything before it reaches a human or client | Creates anything |

Every agent needs an explicit **"you do not do this"** section.

**Files are the handoff, not chat.** Scout → Writer is a scored brief file. Writer →
Auditor is a draft file. Auditor → human is an approved file.

The Auditor is the one everyone skips. It is the only thing standing between you and a
fabricated case study landing in a prospect's inbox.

---

## Level 9 — schedule-safe prompts

A scheduled task cannot ask a clarifying question. Anything vague, it guesses. A prompt
that works in conversation often fails on a schedule for exactly this reason.

1. **Name the exact input source** — not "my leads" but `/inputs/leads.csv`.
2. **Name the exact output destination** and the filename format.
3. **Define what "no work today" looks like**, so it does not invent work. This one bites
   people constantly.
4. **Define what to do on failure** — usually: stop, write to the log, flag me.
5. **No open questions.** If the prompt could be read two ways, it will pick the wrong one.

Promote only a job that has run clean at Level 7 or 8 for two weeks. Watch the first five
runs. Only then add the next schedule.

---

## Level 10 — the five pieces

1. **One source of truth.** A single store every agent reads and writes. Every lead is one
   record with one state:

   ```text
   new → researched → contacted → replied → booked → proposed → won | lost | dead
   ```

   If two agents disagree about a lead's state, the system is broken. Get this right
   before anything else.

2. **One intake path.** Every lead enters the same way regardless of source — referral,
   inbound, cold, event. Same record shape, same first step. **Multiple intake paths is
   the number one reason these systems collapse.**

3. **Agents on stages, not tasks.** Each pipeline stage has one owning agent and one
   artifact that moves a lead to the next stage.

4. **Human checkpoints, written down.** Minimum: anything sent to a client, any price, any
   contract, any lead scoring above 9, anything the Auditor failed twice.

5. **A feedback loop.** Weekly, an auditor agent reads the logs and reports where leads
   died, which emails got replies, which scoring rules were wrong, and what humans had to
   fix. **Change one rule per week.** Change five and you will never know which worked.

**Build order:** map the current reality including the ugly manual bits and time each step
→ pick the state model → define the artifact per stage → then wire agents to stages.
