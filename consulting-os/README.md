# Consulting OS — Kernel

Routing tree for the consulting AI OS. Architecture:
`docs/consulting-ai-os-architecture.md`. Foundation: `docs/ai-os-blueprint.md`.

## What lives where

- `domains/<slug>/pack.md` — domain context packs (the core asset).
  Template: `domains/_template/pack.md`
- `sources.md` — canonical source registry (top-10 GitHub + LinkedIn signal,
  per CIOS-SRC-001). Pack watchlists draw only from this.
- `inbox/<slug>/` — raw acquisition notes awaiting curation into a pack.
  Never cite inbox material in a client deliverable.
- `runbooks/` — operational procedures (request intake, pack curation)
- Engagement artifacts go to `runs/<date>-<client>-<topic>/` at repo root,
  NOT here. Packs are domain truth; runs are engagement-specific.

## Request intake (Domain Classification)

On any consulting request ("AI strategy for X", "assess Y", "proposal for Z"):

1. Match the request against each pack's `keywords:` manifest field —
   1 primary domain, up to 2 secondary.
2. No pack matches → say so. Offer to scaffold a new pack from the template
   first, or proceed pack-less marked as such. Never silently fake coverage.
3. Then follow `runbooks/ai-strategy-request.md`.

## Context load order (cheap → expensive, stop when sufficient)

1. Domain pack(s) — local read, free
2. GBrain semantic recall — account / vertical / theme pages
3. Engagement folder — this client's accumulated facts
4. Fresh acquisition delta — only for gaps and stale sections (Exa/firecrawl)

## Standing rules

- Pack freshness SLA: market-sensitive sections >30 days old on an active
  pursuit require an acquisition delta or a `draft` flag. Architectures and
  frameworks: 90 days.
- Every client-deliverable claim traces to a pack citation or a verified
  fresh primary source.
- All existing governance applies: branded PPTX template + QA gate, delivery
  statuses, GBrain cost guardrails, keys-not-prompts, no SAP Joule.
- After every engagement: durable entity findings → GBrain (batched);
  reusable domain insight → `inbox/<domain>/` for the next curation pass.

## Domain packs

Architectural authority: `governance/CIOS-Architecture-Constitution-v1.0.md`
(adopted via `governance/decisions/CIOS-ARCH-002.md`).

| Pack | Status |
|------|--------|
| `ai-native-engineering` | **REFERENCE DOMAIN** (ADR-005) — v0.3, **active**, 1 asset, acceptance-tested |
| `sap-ai-transformation` | v0.2 draft (template v2) — §2 market landscape needs acquisition |
| `enterprise-agent-platforms` | planned (phase 2) |
| `enterprise-rag-knowledge` | planned (phase 2) |
| `sre-aiops-transformation` | planned |
| `cloud-modernization` | planned |
| `platform-engineering` | planned |
| `proposal-engineering` | planned |
| `industry-transformation` | planned (meta-pack; automotive sub-pack first) |
