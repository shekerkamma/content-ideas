# CIOS Agent Specifications v1.0

The Constitution §16 layer between schemas and implementation:
`Architecture Constitution → Behavioral Specification → Data Model & Schemas
→ **Agent Specifications** → Implementation → Operation`.

Each spec defines a **runnable agent role** any host (Claude Code, Codex,
OpenHands) can execute. Roles are bound to contracts in
`CIOS-SPEC-v1.0.md`; an agent that satisfies its contract list conforms,
regardless of host. One session SHOULD run one role (CIOS-ART-002); a human
MAY play any role manually — the spec is the same.

Common to all agents:
- Read `consulting-os/README.md` first (kernel routing), then this file's
  section for the assigned role.
- Plain-file inputs/outputs only (CIOS-MM-001). Chat output is never the
  artifact.
- Stop and report — never improvise architecture — when a needed rule is
  ambiguous (spec bug protocol).

---

## AGT-01 — Acquisition Agent

- **Mission stage:** Acquire
- **Contracts:** ACQ-001..007, SRC policy (CIOS-SRC-001), GOV-007 when scheduled
- **Trigger:** watchlist run (manual now, scheduled Phase 3) or a gap list
  from AGT-03
- **Reads:** `consulting-os/sources.md`, pack §source-watchlist, gap list
- **Writes:** `consulting-os/inbox/<domain>/*.md` (inbox schema §3.1);
  engagement deltas also to `runs/<id>/research/`
- **Tools:** Exa/WebFetch → firecrawl → `/watch` (YouTube Tier 2b) →
  printing-press CLIs (structured APIs). Resolution order per ACQ-007.
- **Guardrails:** read-only externally; never writes packs; every item
  carries a resolvable primary `source_url`; token cap ~20K when unattended.
- **Done when:** each watchlist/gap item has an inbox file or an explicit
  "no source found" note.

## AGT-02 — Curation Agent (Transformation)

- **Mission stage:** Transform
- **Contracts:** TRN-001..006, TST-001/002/007, OP-004
- **Trigger:** inbox items pending for a domain
- **Reads:** `inbox/<domain>/`, the domain pack, GBrain (entity split check)
- **Writes:** pack updates (version bump, freshness, citations), GBrain
  entity pages (batched), `inbox/<domain>/_curated/` moves
- **Guardrails:** prepares diffs — a human approves before pack changes land
  (TRN-002); claims without verified sources become [NEEDS ACQUISITION],
  never silent assertions; runs pack lint + golden questions after every
  merge; prunes stale facts on sight.
- **Done when:** inbox empty (curated/discarded), lint green, pack status
  honestly set, 90-day unused-asset report emitted (TST-007).

## AGT-03 — Context Builder (Consulting Context Engine)

- **Mission stage:** Operationalize
- **Contracts:** KER-001..004, CLS-001..005, CTX-001..005, GOV-001
- **Trigger:** any consulting request
- **Reads:** packs (classification → load), GBrain recall, engagement folder
- **Writes:** `runs/<id>/engagement.yaml` (+ folder scaffold), the gap list
- **Guardrails:** layered load order is mandatory; low classification
  confidence → ask the user (interactive) or flag draft (unattended);
  freshness gate verdict recorded before any synthesis starts.
- **Done when:** manifest complete, context loaded, gap list handed to
  AGT-01 (if needed) and the synthesis skeleton (pack PoV + frameworks)
  identified for AGT-04/05.

## AGT-04 — Proposal Engineer

- **Mission stage:** Generate (asset layer)
- **Contracts:** PRO-001..006, MM-005, OP-002/003
- **Trigger:** engagement reaches `synthesizing`
- **Reads:** loaded context (pack, GBrain, engagement, delta), `assets/`
- **Writes:** pursuit reasoning (scoring, objection prep, narratives) into
  `runs/<id>/`, new/updated asset files (PRO-005 frontmatter, use_count)
- **Tools:** existing skills — presales-deal-prep, vertical-scorer,
  ai-strategy-brief, contract-reviewer, grill-me
- **Guardrails:** reuse before creation (check assets first); never
  re-research what context answers; commercial claims only from cited
  benchmarks or fresh primary sources.
- **Done when:** every claim in the synthesis traces per MM-005 and reusable
  components are persisted as assets.

## AGT-05 — Output Generator

- **Mission stage:** Generate (output layer)
- **Contracts:** OUT-001..005, GOV-002/003, deliverable lifecycle MM-004
- **Trigger:** synthesis complete; deliverable types confirmed
- **Reads:** synthesis + assets; `BRANDED_PPTX_TEMPLATE` / pptxkit workflow
- **Writes:** `runs/<id>/deliverables/*` (+ builder scripts kept in run
  folder), manifest `deliverables:` registration
- **Guardrails:** branded workflow only for decks — blocked beats unbranded;
  full PPTX QA gate before `reviewed`; board-deck intake schema resolved
  before building (OUT-005); never transmits to clients (OUT-004).
- **Done when:** every deliverable registered with an honest status and the
  QA evidence is in the run folder.

## AGT-06 — Validator (Testing Framework)

- **Mission stage:** cross-cutting
- **Contracts:** TST-001..007
- **Trigger:** after any pack edit (lint + golden questions); after any
  delivered engagement (quality scores); on demand (baseline comparison)
- **Reads:** packs, run folders, assets
- **Writes:** test results into the run `status.md` / curation notes;
  baseline answers to `domains/<slug>/assets/_baseline-gq1.md`
- **Guardrails:** golden questions answered from the pack ALONE — loading
  anything else invalidates the result; failing packs get demoted, not
  excused; quality self-scores require one-line justifications.
- **Done when:** verdicts recorded where the next agent will read them.

---

## Composition patterns

- **Full engagement:** AGT-03 → (AGT-01 if gaps) → AGT-04 → AGT-05 →
  AGT-06, with AGT-02 closing the loop post-run. This is the acceptance
  trace (spec Part 13.1) as a role pipeline.
- **Maintenance cycle (Phase 3 cadence):** AGT-01 (scheduled watchlist) →
  AGT-02 (human-gated curation) → AGT-06 (lint + goldens), weekly per
  active domain, caps per GOV-007/008.
- **Delegation:** any role MAY delegate parallelizable sub-work to cheaper
  models (ART-003); the role owner merges results into its own artifacts.
