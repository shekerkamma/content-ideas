---
name: ai-head-of-engineering-custom-internal-tool-designer
description: Use when someone wants the internal tool design step of the AI Head of Engineering flow, or asks for a custom CRM, dashboard, or workflow tool for how the business actually runs.
argument-hint: [business-motion] [painful-saas] [tracked-objects]
---

# Custom Internal Tool Designer

Design the internal tool around the real business motion, not around a generic SaaS template.

## Inputs

- What needs to be tracked
- What current SaaS makes painful
- Business motion

## Process

1. Define the real data model and source-of-truth objects.
2. Design the main views and the three most-used screens.
3. Map roles, permissions, approvals, and audit needs.
4. List automation triggers and integrations.
5. State what is deliberately not in the tool.
6. Save the result as `07-tool-designer.md`.

## Output

- Data model
- UI structure
- Roles and permissions
- Automation triggers
- Integration surface
- Deliberate exclusions

## Dependencies

- `06-ai-fit.md`
- `skills/ai-head-of-engineering/references/shared-templates.md`

## Skill Relationships

### Category
Business Automation

### Relationships
| Pattern | What it means here | Handoff artifact |
|---|---|---|
| Sequential | Feeds the launch audit and roadmap | `06-ai-fit.md` -> `07-tool-designer.md` -> `08-pre-launch-audit.md` |
| Domain cluster | One member of the AI Head of Engineering family | `runs/ai-head-of-engineering/...` |

### Host compatibility
Shared. Use repo-relative output paths and host-neutral wording.

## Gotchas

- Do not default to generic CRM fields.
- Do not hide approval flows that live in people’s heads.
- Do not overstuff the tool with SaaS-default features that no one uses.

