# DealForge Goal + PLAID Test

This repo is a clean test snapshot for using Codex/Claude `/goal` with PLAID-generated product artifacts.

## What This Tests

- Repo-local PLAID skill usage from `skills/plaid/SKILL.md`
- Karpathy-style coding guardrails from `skills/karpathy-guidelines/SKILL.md`
- Codex-facing instructions in `AGENTS.md`
- Claude Code-facing instructions in `CLAUDE.md` and `.claude/settings.json`
- A bounded `/goal` execution against `docs/product-roadmap.md`

## Goal Used

```text
Build DealForge Phase 1 from docs/product-roadmap.md using the repo-local PLAID artifacts.
Scope: complete TASK-001 through TASK-005 only.
Read docs/prd.md, docs/product-vision.md, vision.json, and docs/product-roadmap.md as the product contract.
Implement a Next.js App Router + TypeScript + Tailwind foundation, Convex schema/auth config stubs,
Clerk integration scaffold, dashboard layout with empty state, and first-sign-in user creation path.
Mark each Phase 1 roadmap checkbox complete only after implementation and verification.
Verify with available install/build/lint/typecheck commands.
Stop if required credentials or missing product/design decisions prevent meaningful progress and cannot be safely stubbed.
```

## Verification

```bash
npm install
npm run lint
npm run typecheck
npm run build
```

Verified locally:

- `npm run lint` passes
- `npm run typecheck` passes
- `npm run build` passes

## Claude Code validation

Use the same prompt shape in Claude Code, but point it at the repo-local skills and roadmap:

```text
/plaid build

Build DealForge Phase 1 from docs/product-roadmap.md using the repo-local PLAID artifacts.
Scope: complete TASK-001 through TASK-005 only.
Read docs/prd.md, docs/product-vision.md, vision.json, and docs/product-roadmap.md as the product contract.
Implement a Next.js App Router + TypeScript + Tailwind foundation, Convex schema/auth config stubs,
Clerk integration scaffold, dashboard layout with empty state, and first-sign-in user creation path.
Mark each Phase 1 roadmap checkbox complete only after implementation and verification.
Verify with available install/build/lint/typecheck commands.
Stop if required credentials or missing product/design decisions prevent meaningful progress and cannot be safely stubbed.
```

Runtime note:

- A live `claude` binary is not available in this shell, so the Claude validation here is config-level and prompt-level only.
- Claude-side skill resolution is still set up through `/home/shekerk/.claude/skills/plaid/SKILL.md` and `/home/shekerk/content-ideas/.claude/settings.json`.

## Notes

- Clerk and Convex are scaffolded for Phase 1. Real deployments need Clerk and Convex environment variables.
- `docs/design.md` is not present, so the UI follows the restrained brand guidance in `docs/product-vision.md`.
- Phase 2 pipeline work is intentionally out of scope for this snapshot.
