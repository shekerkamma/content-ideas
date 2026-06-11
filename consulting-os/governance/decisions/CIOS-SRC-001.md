# CIOS-SRC-001 — Knowledge Layer Source Policy

- **Status:** APPROVED (source classes); top-10 list PENDING owner confirmation
- **Effective:** 2026-06-10
- **Decided by:** Owner

## Decision

The CIOS knowledge layer (second brain / domain packs) is built **entirely**
from two source classes:

1. **Canonical GitHub resources — a curated top-10 set** (e.g., OpenHands).
   Repos and their official docs are the ground truth for implementation
   claims, reference architectures, and capability statements. Code beats
   marketing: if a capability isn't in the repo/docs, it doesn't go in a pack.
2. **Practitioner & vendor-engineering signal** — (a) LinkedIn posts: proof
   points, adoption evidence, market sentiment, objection material; never
   authoritative for technical claims. (b) Curated YouTube channels
   (registry-listed; initial set: SAP on Azure, SAP on AWS — owner addition
   2026-06-10): vendor-engineering architecture and deployment content,
   cited with URL + timestamp, re-grounded in Tier 1 where a repo/doc
   equivalent exists.

Everything else (vendor marketing, analyst reports, news) is **context only**
— it may inform pack §3 market-landscape narrative but cannot be the sole
citation for a claim in an `active` pack.

## Rationale

- Keeps the brain verifiable: every technical claim traces to versioned code
  or official docs.
- Matches the existing repo rule that OpenHands repo/docs are the source of
  truth over invented orchestration.
- LinkedIn is where operator proof points surface first; the existing
  ScrapeCreators/content-ideas tooling already acquires it.

## Implementation

- Registry: `consulting-os/sources.md` (kernel-level, single canonical list).
- Spec requirement: CIOS-ACQ-006.
- Pack §7 watchlists MUST draw from the registry; additions to the top-10 set
  require updating the registry first (one list, no per-pack drift).

## Amendment (2026-06-10, owner)

- **OpenHands is the PRIMARY source across ALL domains, including SAP.**
  Every domain's acquisition checks OpenHands repo/docs first; the other
  Tier-1 repos supplement, not replace, it.
- **Printing-press fallback authorized:** where OpenHands (or the wider
  Tier-1 set) lacks coverage, acquire via a printing-press-generated CLI
  against the authoritative API (research → generate → build → shipcheck).
  Resolution order per claim: OpenHands → other Tier-1 repos → pp-CLI against
  the authoritative API → **[NEEDS ACQUISITION]**.
- The earlier "SAP gap" note is superseded by the above.

## Amendment 2 (2026-06-10, implementation finding)

- **Tier 2c added: operator engineering blogs** (first-party operator
  metrics, e.g. Intercom/Atlassian/Shopify engineering posts). Citable as
  proof points and PoV evidence; technical capability claims still re-ground
  in Tier 1. Found during the first ANE backlog acquisition pass — this
  evidence class was stronger than LinkedIn but unclassified (spec-bug
  protocol: amend, log, proceed).

## Open item

Owner has confirmed OpenHands as #1 (primary, all domains). Slots 2–10 are
proposed in the registry and require owner confirmation or replacement before
the registry is marked `confirmed`.
