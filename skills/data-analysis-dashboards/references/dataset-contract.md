# Competitor comparison dataset contract

Input is one or more schema-version-1 JSON dossiers accepted by
`skills/deepgrid-competitive-intelligence/scripts/validate_dossier.py`.

## Required semantics

- Competitor name is the portfolio key.
- Segment threats use `NONE`, `LOW`, `MEDIUM`, `HIGH`, or `NOT_ASSESSABLE`.
- OEM gates contain exactly seven values. `true` and `false` are observations;
  null is unavailable; a string such as `COMPANY_CLAIM` preserves provenance.
- Evidence statuses use `VERIFIED`, `COMPANY_CLAIM`, `INFERRED`, `UNAVAILABLE`,
  or `CONFLICTED`.
- Qualification and hard-disqualifier nulls remain null.

## Output metrics

- `assessable_segments`: count of segment labels other than NOT_ASSESSABLE.
- `high_threat_segments`: count of HIGH labels; not a weighted risk score.
- `known_oem_gates`: count of non-null OEM-gate values.
- `verified_evidence_share`: VERIFIED rows / all evidence rows.
- `sourced_evidence_share`: VERIFIED + COMPANY_CLAIM + CONFLICTED rows / all
  evidence rows. This measures traceability, not truth.
- `evidence_coverage`: unique evidence IDs referenced by segments / all dossier
  evidence IDs.

Every proportion includes its numerator and denominator in the CSV or summary.
No proportion is emitted when its denominator is zero.
