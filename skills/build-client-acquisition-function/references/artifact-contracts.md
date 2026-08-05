# Artifact contracts

## Run structure

```text
<run>/
  sources/
  context/{01-offer,02-icp,03-voice,04-proof,05-objections,06-process}.md
  context/project-instructions.md
  prompts/
  chains/
  deliverables/
  connections/
  agents/{scout,writer,closer,auditor}.md
  handoffs/{scored,drafted,approved,rejected}/
  schedules/
  control/{maturity-assessment.md,advancement-plan.md,status.json}
  logs/
  outputs/
  evidence-map.md
```

## Status schema

`control/status.json` must contain:

```json
{
  "status": "draft|pilot|reviewed|blocked",
  "current_level": 0,
  "target_level": 1,
  "gate": "pending|passed|failed|blocked",
  "calendar_task_removed": "",
  "human_approvals": [],
  "tests": [],
  "risks": [],
  "next_action": "",
  "updated_at": "ISO-8601"
}
```

## Handoff envelope

Every agent handoff is a Markdown file with YAML frontmatter:

```yaml
artifact_id: stable-id
stage: scored|drafted|approved|rejected
subject_id: stable prospect or opportunity id
created_at: ISO-8601
created_by: scout|writer|closer|auditor|human
source_ids: []
confidence: 0.0
approval_required: true
```

The body contains facts, inference labels, decisions, unresolved questions, and the requested next action. Auditor decisions must cite the exact evidence or rule used.

## Lead record and state machine

Every lead is one record in one store. One state, from this list only:

```text
new -> researched -> contacted -> replied -> booked -> proposed -> won | lost | dead
```

Two agents disagreeing about a lead's state means the system is broken. Fix the store, not
the agents. Every lead enters through **one intake path** regardless of source.

## Human checkpoints (minimum)

Written down in advance, not decided case by case: anything sent to a client, any price,
any contract, any lead scoring above 9, anything the Auditor failed twice.

## Six context files

- `01-offer.md`: buyer outcome, mechanism, scope, exclusions, pricing, typical result and timeline. Specific numbers.
- `02-icp.md`: firmographic and situational fit, buying triggers, **and disqualifiers — which matter more than the qualifiers**.
- `03-voice.md`: three real emails and three real posts you were happy with, plus a banned-words list. Samples, not descriptions.
- `04-proof.md`: claim, evidence, source, date, limitations. **This file is the ceiling on every claim the system may make.**
- `05-objections.md`: ten objections taken from real conversations, each with diagnosis, response, evidence, escalation.
- `06-process.md`: every step from first contact to signed, including the ugly manual bits, with owner and duration.

See [level-playbooks.md](level-playbooks.md) for the project-instructions template that binds these together.

Use `assets/context-template.md` to start each file.
