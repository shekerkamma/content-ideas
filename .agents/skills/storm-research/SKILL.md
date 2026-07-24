---
name: storm-research
description: Use when someone asks to run Storm Research, use the STORM method, run a STORM briefing/report on a topic, or wants a multi-perspective, citation-verified HTML research briefing. Codex/OpenHands discovery wrapper for the canonical repo-local skill.
argument-hint: "[topic to research]"
---

# storm-research

This is the Codex/OpenHands discovery wrapper for the canonical repo-local
Storm Research skill.

Before running Storm Research, read and follow the canonical instructions:

- `/home/shekerk/content-ideas/skills/storm-research/SKILL.md`
- `/home/shekerk/content-ideas/skills/storm-research/report-template.html`

Do not duplicate or independently evolve this wrapper. All substantive changes
belong in `skills/storm-research/`.

## Host Compatibility

### Target Hosts

- Codex/OpenAI: yes -- this wrapper makes the skill discoverable under
  `.agents/skills/storm-research/SKILL.md`.
- OpenHands: yes -- same `.agents/skills/<name>/SKILL.md` project-skill path.
- Claude Code: use a mirror under `.claude/skills/storm-research/` if needed.

### Canonical Source

`skills/storm-research/` is canonical. This wrapper only routes the host to that
source.

## Skill Relationships

### Category

Runbook

### Dependencies

Skills that must be installed for this skill to work:

- `storm-research` canonical source --
  `/home/shekerk/content-ideas/skills/storm-research/SKILL.md`

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `storm-research` | Behavioral overlay | always; this wrapper delegates to the canonical skill | `storm-reports/{topic-slug}-briefing.html` |

### Runtime Preamble

I'm using the `.agents` wrapper for `storm-research`; I will read and follow
the canonical `skills/storm-research/SKILL.md` before acting.

## Gotchas

- **Do not edit this wrapper instead of the canonical skill:** substantive
  changes belong in `skills/storm-research/`.
- **Do not copy the full canonical skill here:** duplicated instructions drift.
- **Discovery only:** this file exists to make Codex/OpenHands routing work.
