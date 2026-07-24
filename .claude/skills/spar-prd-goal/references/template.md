# SPAR-PRD-GOAL — Interview Prompt & PRD Output

The self-contained prompt this skill runs, plus a worked example. Paste the
prompt block into any Claude session to run it standalone (no skill needed).

## The interview prompt (copy-paste engine)

```
You are helping me write a quick PRD for work I'll do with Claude Code using /goal.
The work might be a new build, a refactor, a bug fix, a script, or any other kind
of project. Interview me first, then write the PRD.

Rules:
- Ask me one question at a time. Wait for my answer before moving on.
- If my answer is vague or I skip something, push back and ask the sharper version.
- Adapt follow-up wording to the kind of project I'm describing (web app, API, CLI,
  script, data pipeline, refactor, etc.) but cover all six topics.
- Do not write the PRD until I've answered all six questions.
- When you have what you need, say "I have what you need" and produce the PRD.

Ask me these six questions, one at a time. Wording can adapt to my project type,
but each question must cover the topic listed:

1. SCOPE — "In one sentence, what are you trying to accomplish, and who is it for /
   why does it matter? Is this a new build, a change to existing code, or something
   else?"
2. STACK — "What tech stack, language, or tools are involved? If it's existing code
   and you're not sure, tell me and I'll check the repo."
3. SURFACES — "What are the concrete things that will exist or change when this is
   done? List them. Files, functions, API endpoints, CLI commands, pages, database
   tables, or anything else a person could point at."
4. DATA — "What inputs does this take and what outputs does it produce? Include
   anything stored, anything read from somewhere else, and the shape of the data
   if it matters."
5. CONSTRAINTS — "What must NOT change or break? For new builds, what are you
   explicitly cutting from v1? For existing code, what behavior must be preserved
   exactly?"
6. DONE — "How will we know this is finished? List every distinct thing that should
   be true when it works. For each one, tell me how I'd verify it — a command to
   run, a file to check, a behavior to test. The more specific, the better. Also:
   what seed data should exist so the verification is meaningful?"

After all six answers, produce the PRD in this exact structure:

# [Project Name] PRD
## One-Liner
## Why
## Stack
## Surfaces
## Data
## Constraints
## Success Criteria

The Success Criteria section must be a numbered list of discrete, verifiable checks
I can paste directly after /goal. Each check must: (a) state one thing that must be
true, and (b) name how Claude should prove it — a command output, a file dump, a
curl response, a test result, or a specific behavior demonstrated in the transcript.
End with a single sentence describing what seed data should exist before
verification runs. The whole section must be copy-pasteable as a /goal condition.

After the PRD, also render it as a ready-to-paste /goal prompt in this exact
5-part shape:

/goal

TASK: [One-Liner]
WHY: [Why]
OUTCOME: [Surfaces + Data, phrased as the finished result]
CONSTRAINTS: [Constraints, ending with "Stop after N turns." — default 30]
VERIFICATION: [Success Criteria checks + seed data sentence]

Start with question 1 now.
```

## Worked example — output PRD

```
# CSV Feed Deduper PRD

## One-Liner
Add a dedup pass to the feed generator so repeated competitor posts never appear twice in the For You feed.

## Why
Duplicate posts make the daily feed feel broken and waste the user's review time; the feed is the product's front door.

## Stack
Python 3 stdlib only (json, hashlib); existing generate_feed.py; pytest.

## Surfaces
- skills/content-ideas/scripts/lib/dedup.py (new)
- generate_feed.py: call dedup() before render (changed)
- tests/test_dedup.py (new)

## Data
- Input: list[dict] feed items with fields {id, url, title, ts}
- Output: same list, first occurrence of each (url) kept, rest dropped, order preserved
- Nothing persisted; pure in-memory transform

## Constraints
- Must NOT change feed item schema or the HTML template
- Must NOT add pip dependencies (stdlib only)
- v1 dedups on url only; fuzzy/title matching is out of scope

## Success Criteria
1. `python3 -m pytest tests/test_dedup.py -q` exits 0 — paste the summary line.
2. Feeding two items with the same url returns one — show the test assertion + output.
3. Order is preserved for non-duplicates — dump the returned list ids in the transcript.
4. `grep -r "import " skills/content-ideas/scripts/lib/dedup.py` shows only stdlib — paste output.
5. Full suite still green: `python3 -m pytest -q` exits 0 — paste the summary line.
Seed data: a fixture list of 4 items where items[0] and items[2] share a url.
```

## Worked example — emitted /goal prompt

```
/goal

TASK: Add a dedup pass to the feed generator so repeated competitor posts never appear twice in the For You feed.
WHY: Duplicate posts make the daily feed feel broken and waste the user's review time; the feed is the product's front door.
OUTCOME: New skills/content-ideas/scripts/lib/dedup.py; generate_feed.py calls dedup() before render; new tests/test_dedup.py. Input list[dict] {id, url, title, ts} → first occurrence per url kept, order preserved, pure in-memory.
CONSTRAINTS: Do not change the feed item schema or HTML template. No pip dependencies (stdlib only). v1 dedups on url only — fuzzy/title matching is out of scope. Stop after 30 turns.
VERIFICATION: (1) `python3 -m pytest tests/test_dedup.py -q` exits 0 — paste summary. (2) Two items with the same url return one — show assertion + output. (3) Order preserved for non-duplicates — dump returned ids. (4) `grep -r "import " .../dedup.py` shows only stdlib — paste output. (5) Full suite green: `python3 -m pytest -q` exits 0 — paste summary. Seed data: fixture list of 4 items where items[0] and items[2] share a url.
```
