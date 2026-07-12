# AI Analyst Pack: Agent Replacement Scorecard

## Classification
L5 presentation repair / full analytical deck

## Question
Which SaaS layers are exposed to agent replacement, renegotiation, or durability?

## Data Quality
- Rows: 25
- Duplicate use cases: 0
- Blockers: none
- Warning: dataset is curated, not statistically sampled.

## Validated Findings
- Verdict counts: {'REPLACE': 10, 'RENEGOTIATE': 9, 'KEEP': 6}
- Data moat is the strongest separator: low moat maps to replace, medium to renegotiate, high to keep.
- High-volume rows produce 9 of 10 replacement calls.
- Formula violations: 0

## Story Architecture
- Start with dataset and score mechanics.
- Show use cases domain by domain before making the executive argument.
- Establish data moat as the central explanatory mechanism.
- Translate verdicts into replace, renegotiate, and keep commercial playbooks.
- Use AEO pages to publish model-derived buyer answers, not generic AI claims.

## Guardrails
- Do not claim statistical market validation.
- Do not claim universal SaaS replacement.
- Do not imply guaranteed savings without client spend data.
- Use proof rows as examples unless source URLs are tied out.
