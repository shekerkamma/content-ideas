# CIOS-ARCH-001 — Freeze CIOS Architecture v1.0

- **Status:** APPROVED
- **Effective:** 2026-06-10
- **Decided by:** Owner (acting Architecture Review Board)

## Decision

No further architectural changes shall be made until CIOS Specification v1.0
(Execution Grade) is completed.

## Frozen (change requires an ARB-approved v2.0 decision)

- Mission: Acquire → Transform → Operationalize → Generate consulting intelligence
- Meta Model
- Core Engine set (11): Kernel, Acquisition, Transformation, Domain
  Classification, Consulting Context, Proposal Engineering, Output, Agent
  Runtime, Memory, Governance, Testing
- Primary Consulting Domains (9): ai-native-engineering,
  enterprise-agent-platforms, enterprise-rag-knowledge,
  sre-aiops-transformation, sap-ai-transformation, cloud-modernization,
  platform-engineering, proposal-engineering, industry-transformation
- Operating Principles (layered context load, freshness SLA, citation rule,
  keys-not-prompts, tool-agnostic folders-and-files)
- Logical Repository Structure (`consulting-os/{domains,inbox,runbooks,spec,governance}`,
  engagements under `runs/`)
- Reference Domain: `sap-ai-transformation`
- Output set (8): board strategy decks, executive briefings, proposals,
  transformation roadmaps, operating models, architecture assessments,
  vendor evaluations, business cases

## Expandable (implementation details of the frozen architecture)

Contracts, schemas, state models, lifecycles, agent specifications,
transformation rules, classification rules, output pipelines, testing
framework, validation framework, governance framework.

## Next deliverable

**CIOS Specification v1.0** — Execution Grade. Target audience: Claude Code,
Codex, OpenHands, future agent platforms. Success criterion: an agent can
build the operating system from the spec without additional architectural
clarification. Location: `consulting-os/spec/CIOS-SPEC-v1.0.md`.

## References

- `docs/consulting-ai-os-architecture.md` (frozen architecture, v1.0)
- `docs/ai-os-blueprint.md` (Four C's foundation)
