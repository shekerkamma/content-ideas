---
name: ai-head-of-engineering-pre-launch-auditor
description: "Use when someone wants the pre-launch audit step of the AI Head of Engineering flow, or asks for edge cases, security gaps, and launch readiness before release."
argument-hint: "[build-summary] [stack] [production-config]"
---

# Pre-Launch Auditor

Audit the build before anyone says it has launched.

## Inputs

- Build summary
- Stack
- Production config

## Process

1. Enumerate edge cases across the whole build.
2. Check security boundaries, auth, RLS, webhook verification, and secrets handling.
3. Verify production readiness items like env vars, backups, monitoring, and email deliverability.
4. Run the launch-gate smoke test.
5. Save the result as `08-pre-launch-audit.md`.

## Output

- Edge cases
- Security gaps
- Production readiness checklist
- Launch-gate smoke test

## Dependencies

- `07-tool-designer.md`
- `skills/ai-head-of-engineering/references/shared-templates.md`

## Skill Relationships

### Category
Product Verification

### Relationships
| Pattern | What it means here | Handoff artifact |
|---|---|---|
| Sequential | Feeds the roadmap and launch decision | `07-tool-designer.md` -> `08-pre-launch-audit.md` -> `09-roadmap.md` |
| Domain cluster | One member of the AI Head of Engineering family | `runs/ai-head-of-engineering/...` |

### Host compatibility
Shared. The output should be reusable in any host because the audit is file-based.

## Gotchas

- Do not pass launch based on happy-path tests.
- Do not trust test-mode webhooks to represent production.
- Do not announce launch until the smoke test passes on production configuration.
