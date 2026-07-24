---
name: skill-builder
description: Use when creating, auditing, or improving a project skill from Codex/OpenHands, especially when the skill must stay compatible with Claude Code, Codex, and OpenHands. This is a compatibility wrapper for the canonical project skill-builder.
---

# skill-builder

This is the Codex/OpenHands discovery wrapper for the canonical project skill-builder.

Before doing any skill-builder work, read the canonical instructions completely:

- `/home/shekerk/content-ideas/.claude/skills/skill-builder/SKILL.md`
- `/home/shekerk/content-ideas/.claude/skills/skill-builder/reference.md` when technical detail is needed

Use the canonical `.claude/skills/skill-builder/` files as the source of truth. Do not duplicate or independently evolve this wrapper.

## Host Compatibility

### Target Hosts
- Claude Code: yes -- canonical implementation at `.claude/skills/skill-builder/SKILL.md`.
- Codex/OpenAI: yes -- this wrapper makes the skill discoverable under `.agents/skills/skill-builder/SKILL.md`.
- OpenHands: yes -- this wrapper follows the `.agents/skills/<name>/SKILL.md` project-skill path.

### Canonical Source
`.claude/skills/skill-builder/` is canonical. This wrapper only routes Codex/OpenHands to that source.

### Tool Mapping
Follow the canonical skill's `Tool Mapping` section.

### Source / Tool Order
Follow the canonical skill's `Source / Tool Order` section.

## Skill Relationships

### Category
Scaffolding & Templates

### Dependencies
Skills that must be installed for this skill to work:
- `skill-builder` canonical source -- `/home/shekerk/content-ideas/.claude/skills/skill-builder/SKILL.md`

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `skill-builder` | Behavioral overlay | always; this wrapper delegates to the canonical skill-builder | `/home/shekerk/content-ideas/.claude/skills/skill-builder/SKILL.md` |

### Runtime Preamble
I'm using the `.agents` wrapper for `skill-builder`; I will read and follow the canonical `.claude/skills/skill-builder/SKILL.md` before acting.

## Gotchas

- **Do not edit this wrapper instead of the canonical skill:** all substantive changes belong in `/home/shekerk/content-ideas/.claude/skills/skill-builder/`.
- **Do not copy the full canonical skill here:** duplicated instructions will drift.
- **Codex/OpenHands discovery only:** this wrapper exists to make routing work; the canonical skill still defines the audit/build behavior.
