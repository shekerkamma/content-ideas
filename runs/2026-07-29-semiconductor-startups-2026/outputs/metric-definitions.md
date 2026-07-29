# Metric Definitions

## Evidence Coverage Count

- Definition: Number of ledger rows available for an entity or arena.
- Formula: `COUNT(claim_id)` grouped by competitor or arena.
- Unit: sourced claim rows.
- Source columns: `claim_id`, `competitor`, `arena`.
- Exclusions: rejected or duplicate raw snippets not promoted to the ledger.
- Confidence basis: coverage measure only; it does not measure company quality.
- Limitation: several rows may originate from one company-published source.

## High-Confidence Evidence Count

- Definition: Ledger rows supported by specific current product, financing, or cohort facts.
- Formula: `COUNT(claim_id) WHERE confidence = high`.
- Unit: sourced claim rows.
- Source columns: `claim_id`, `confidence`, `source_type`.
- Exclusions: interpretation and recommendation rows.
- Limitation: high confidence in what a company published is not independent validation.

## Partner-Readiness Posture

- Definition: Categorical next diligence posture: `ACT NOW`, `VALIDATE NEXT`, or `MONITOR`.
- Rule: apply hard gates for accessible product, integration boundary, supply/availability,
  repeatable proof, partner role, and operating economics before assigning a posture.
- Unit: company by partner lens.
- Source columns: `claim_text`, `storyboard_use`, `confidence`, `source_type`.
- Confidence basis: public evidence only; two independent raters are required in Phase 0.
- Limitation: not an organization-specific right-to-win or partner recommendation.

## Readiness Rubric Weight

- Definition: Candidate weighting used to structure Phase 0 ratings.
- Formula: Product 20% + Software 20% + Supply 20% + Customer proof 15% +
  Partner motion 15% + Economics 10%.
- Unit: weighted readiness screen.
- Source basis: analytical framework on slide 42, not a market fact.
- Limitation: weights remain uncalibrated until independent-rater Phase 0 testing.
