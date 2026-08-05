#!/usr/bin/env python3
"""Create a deterministic client-acquisition-function run workspace."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


DIRS = (
    "sources", "context", "prompts", "chains", "deliverables", "connections",
    "agents", "handoffs/scored", "handoffs/drafted", "handoffs/approved",
    "handoffs/rejected", "schedules", "control", "logs", "outputs",
)
# Numbered so the project instructions can reference them by exact filename.
CONTEXT = (
    ("01-offer", "What you sell, cost, inclusions, exclusions, what the client must do, "
                 "typical result and timeline. Use specific numbers."),
    ("02-icp", "Company size, role, industry, budget, buying triggers — and DISQUALIFIERS, "
               "which matter more than the qualifiers."),
    ("03-voice", "Three real emails and three real posts you were happy with, plus a "
                 "banned-words list. Samples, not descriptions."),
    ("04-proof", "Claim, evidence, source, date, limitations. This file is the CEILING on "
                 "every claim the system may make."),
    ("05-objections", "Ten objections taken from real conversations, each with diagnosis, "
                      "response, evidence, escalation."),
    ("06-process", "Every step from first contact to signed, including the ugly manual "
                   "bits, with owner and duration."),
)
PROJECT_INSTRUCTIONS = """# Project instructions

You work on client acquisition for [company]. Read the project files before answering
anything about offer, pricing, targeting or positioning. Never invent a claim, number or
case study that isn't in 04-proof.md. Voice: match 03-voice.md. Short sentences. No
corporate filler. Never use the banned words list. When I give you a lead, always check
them against 02-icp.md first and tell me if they're a bad fit before writing anything. I
would rather lose a lead than waste a week. If you don't have enough information to do the
job well, ask me one question. Don't guess and don't pad.
"""
ROLES = ("scout", "writer", "closer", "auditor")


L1_PROMPT = """# Level 1 — The Saved Prompt

Task: <the ONE task you repeat most. Not the one that sounds coolest.>

Status: draft. Rule 2 — automate only what you have done by hand ten times. If you have not,
say so here and run it by hand first. A prompt written before the gold standard cannot be
validated, because there is nothing to compare it against.

Done when: paste raw input, hit enter, send with zero edits 8 times out of 10.
Move up when: you keep running three prompts in a row to finish one job. That is Level 2.

## The prompt

```text
ROLE
You <task> for <company>, a <what you do> for <who you serve>.

INPUT
<the raw material, pasted verbatim>

OUTPUT
<exact shape: length, sections, what must appear, what must not>

RULES
- <banned phrasing>
- One ask only / one decision only
- <voice constraint, pointing at 03-voice.md>
- <what "I do not know" looks like, so it does not guess>
```

## Gold standard

Path to the hand-written version this must reproduce: <path, or NONE — and if NONE, this is
not yet a Level 1>

## Test set — three real inputs, with the answer each must produce

| # | Input | Required output |
|---|---|---|
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |

Fix the prompt, not the output. If you edit the output every time, the prompt is wrong.
"""

L2_CHAIN = """# Level 2 — The Chain

One job, several steps, each answer feeding the next. Run in a single chat, one message at a
time. Do not paste every step at once — that collapses back to Level 1 and produces mush.

Status: draft. Never run end to end.

## The job as numbered steps

Write the job as steps BEFORE writing any prompt. If you cannot number it, you do not
understand the job yet.

1.
2.
3.
4.

## Checkpoint

After step <n>, a human reads and approves or corrects before the chain continues.
This is where quality comes from, and it is the step people skip.

## STEP 1 — <NAME>

```text

```

Output must look like: <so the next step can consume it>

## STEP 2 — <NAME>  → CHECKPOINT

```text

```

## What this removes from the calendar

Rule 3: a level that removes no calendar work is a toy — delete it.

| Today | With the chain |
|---|---|
|  |  |

Measure it on the first real run and write the result to logs/. If it removes nothing,
delete the chain rather than keeping it for appearances.
"""

L9_SCHEDULE = """# Level 9 — Schedule-safe prompt

A scheduled task cannot ask a clarifying question. Anything vague, it guesses.

Promote only a job that has run clean at Level 7 or 8 for two weeks. Watch the first five
runs. Only then add the next schedule.

Status: draft. Not promoted.

1. Exact input source (a path, not "my leads"):
2. Exact output destination and filename format:
3. What "no work today" looks like, so it does not invent work:
4. What to do on failure (usually: stop, write to the log, flag me):
5. Open questions: NONE. If the prompt could be read two ways, it will pick the wrong one.

## The prompt

```text

```
"""


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not cleaned:
        raise ValueError("name must contain a letter or digit")
    return cleaned


def write_new(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    run = args.root.resolve() / slug(args.name)
    run.mkdir(parents=True, exist_ok=True)
    for directory in DIRS:
        (run / directory).mkdir(parents=True, exist_ok=True)
    for name, guidance in CONTEXT:
        title = name.split("-", 1)[1].title()
        write_new(
            run / "context" / f"{name}.md",
            f"# {title}\n\nStatus: draft\n\n> {guidance}\n\n"
            "## Rules\n\n## Evidence\n\n## Examples\n\n## Exclusions and unknowns\n",
        )
    write_new(run / "context" / "project-instructions.md", PROJECT_INSTRUCTIONS)
    write_new(run / "prompts" / "01-<most-repeated-task>.md", L1_PROMPT)
    write_new(run / "chains" / "01-<the-job>.md", L2_CHAIN)
    write_new(run / "schedules" / "01-<the-job>.md", L9_SCHEDULE)
    for role in ROLES:
        write_new(run / "agents" / f"{role}.md", f"# {role.title()}\n\n## Mission\n\n## Inputs\n\n## Outputs\n\n## Stop conditions\n")
    write_new(run / "evidence-map.md", "# Evidence map\n\n| ID | Claim or rule | Source | Retrieved | Notes |\n|---|---|---|---|---|\n")
    write_new(run / "control" / "maturity-assessment.md", "# Maturity assessment\n\n## Evidence by level\n\n## Current level\n\n## Next gap\n")
    write_new(run / "control" / "advancement-plan.md", "# Advancement plan\n\n## Calendar task removed\n\n## Acceptance test\n\n## Human approval\n\n## Rollback\n")
    status = {
        "status": "draft", "current_level": 0, "target_level": 1,
        "gate": "pending", "calendar_task_removed": "",
        "human_approvals": [], "tests": [], "risks": [], "next_action": "",
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    status_path = run / "control" / "status.json"
    if not status_path.exists():
        status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    print(run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
