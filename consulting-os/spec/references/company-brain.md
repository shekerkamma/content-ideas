# Reference — "Company Brain" (Dima Bilous, anfloy.notion.site, captured 2026-06-09)

Source PDF: `Company Brain.pdf` (owner's Desktop). Contextual input to CIOS
Specification v1.0. Incorporated as implementation detail under CIOS-ARCH-001
(no architecture change — CIOS's brain/operator/connections separation is the
same shape as our Four C's split).

## Core model (validates frozen CIOS architecture)

- **Brain = data** (markdown repo: context/, memory/, skills/, CLAUDE.md).
  It runs nothing. = CIOS packs + engagement files.
- **Operator = Claude** running on top (local Claude Code or cloud Routines).
  = CIOS Agent Runtime.
- **Connections = MCP** into live apps. = CIOS Connections layer.
- Separation is the point: swap the model, keep the brain. Same thesis as
  CIOS-ART-001 (tool-agnostic, cold-start from repo).
- Context positioning: YC S26 RFS lists "Company Brain"; a16z 2026 thesis =
  context is the bottleneck, not the model. Useful market framing for the
  `enterprise-rag-knowledge` and `ai-native-engineering` packs (§3 landscape)
  — copied to those domains' inboxes when packs are scaffolded.

## Extracted rules adopted into CIOS-SPEC v1.0

| Source guidance | Spec requirement |
|---|---|
| CLAUDE.md lean, 300–400 line ceiling, pointers not duplication | CIOS-KER-005 |
| Log every project the day it ships; record *what drove the result*, not just what was built; prune stale facts (stale context worse than missing — the agent trusts it) | CIOS-TRN-006 |
| Human-in-the-loop on anything irreversible; least-privilege MCP (read first, write per-tool when needed) | already CIOS-GOV-004 (confirmed) |
| Token caps on unattended runs: ~20K review / ~60K fix / ~100K weekly maintenance; one job = one definition of done; audit via stream-json; alert on weekly spend | CIOS-GOV-007 |
| June 15 2026 billing change: Agent SDK / headless / GitHub Actions move to automation credits (≈$20 Pro / $100 Max5x / $200 Max20x, no rollover), API rates after; interactive sessions unaffected | CIOS-GOV-008 |
| Branch protection on main; brain updates via PR; memory/ as changelog | CIOS-GOV-009 |
| Scaling ladder: 1) ingestion (auto-capture from transcripts/CRM), 2) retrieval (vector search), 3) currency (date tags + supersession). Add each only when the simpler version visibly breaks | CIOS-MEM-006 |

## Notes on fit

- CIOS is already at ladder rung 2–3: GBrain = retrieval (embedding-backed),
  freshness SLA + `[NEEDS ACQUISITION]` markers = currency. Rung 1 (auto
  ingestion) is deliberately deferred to architecture roadmap Phase 3 cadence.
- Their "routines" cadence examples (nightly CRM hygiene, weekly memory
  drafting) parallel the CIOS Phase 3 acquisition scans — same trust-laddering.
- Their repo template is a *small-team general* brain; CIOS is a *consulting
  domain* brain. The pack layer (point of view, frameworks, objection
  libraries, golden questions) is CIOS's differentiation and has no equivalent
  in the template.
