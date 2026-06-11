# CIOS-ARCH-002 — Adopt Architecture Constitution v1.0 as Architectural Authority

- **Status:** APPROVED
- **Effective:** 2026-06-10
- **Decided by:** Owner (delivered the Constitution; "try" = incorporate)

## Decision

`consulting-os/governance/CIOS-Architecture-Constitution-v1.0.md` is the
architectural authority for CIOS v1.0. Where it differs from CIOS-ARCH-001 or
CIOS-SPEC-v1.0, the Constitution prevails. The spec is subordinate: it defines
*how the architecture behaves* (Constitution §16.2).

## Reconciliation (Constitution vs prior artifacts)

| # | Conflict | Resolution |
|---|----------|------------|
| 1 | Reference domain: CIOS-ARCH-001 said `sap-ai-transformation`; Constitution ADR-005 says **AI Native Engineering** | Constitution wins. `ai-native-engineering` is the reference/validation domain. The SAP pack remains as the second seeded pack (it loses no content; it gains time to fill its [NEEDS ACQUISITION] sections). Spec Part 13 rewritten accordingly. |
| 2 | Meta model: Constitution §7 has an explicit **Consulting Asset** layer (Source → Intelligence → Domain → Context → **Asset** → Output); spec had context → output directly | Asset entity, schema, lifecycle, and storage (`domains/<slug>/assets/`) added to the spec (CIOS-MM-005, CIOS-PRO-005/006). Constraint A-004 (no asset without context) and A-005 (no output may bypass the meta model) now explicit spec requirements. |
| 3 | Consulting Context required components: Constitution §8.4 lists 12 (Executive Summary, Market Landscape, Capabilities, Architectures, Patterns, Tools, Skills, Business Case, Roadmap, Risks, Proposal Assets, Deck Assets); pack template had 8 sections | Pack template v2 aligned to the 12 components (CIOS additions kept: source watchlist, golden questions, objection library). Packs carry `template_version:` in frontmatter; existing SAP pack stays v1 until its next curation pass migrates it. |
| 4 | OS model: Constitution §6 names **Learning** as a system element | Mapped to existing requirements (TRN-006 brain health, GOV-006 slip-ups-are-data, OP-005); spec notes the mapping. No new engine — Learning is a property the contracts already enforce. |

## Confirmed alignments (no change needed)

Mission (4 stages), 11 core engines, 9 domains + domain boundary rule
(= registry/no-drift rules), OP-001..005 (map to CTX-001/005, GOV-002,
OP-003=reuse→CIOS-PRO-002, OP-004=synthesize-before-storage→inbox-not-citable,
OP-005→TRN-006), constraints A-001..003 (layered load + citation rule),
anti-patterns 1–5 (sources-are-not-assets, context-before-prompting,
inbox-never-citable, outcome-centric engines, registry governance).

## Versioning going forward

Per Constitution §17.2: `1.x` clarifications via decision records; `2.0`
requires formal architecture revision. CIOS-ARCH-001's freeze remains in
force, now anchored to the Constitution.
