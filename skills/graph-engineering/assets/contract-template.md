# Contract: {{PROJECT}}

Status: DRAFT
Agreed on: (set when Status becomes AGREED)
Parties: builder, auditor
Drafted: {{DATE}}

<!--
  Status stays DRAFT until the auditor has reviewed these criteria
  adversarially and has no outstanding objections. Work must not start against
  a DRAFT contract.

  Gate on it:  python3 <skill-dir>/scripts/check_contract.py --dir .
-->

## Scope

What this run covers:

- REPLACE ME

Explicitly not in scope:

- REPLACE ME

## Criteria

Every criterion is one yes/no. The test: could two reasonable people disagree
about whether it passed? If so, it is not written yet. Prefer criteria a script
decides over criteria a model judges.

| # | Criterion | Check |
|---|---|---|
| 1 | REPLACE ME — a single yes/no assertion | `python3 scripts/check.py` |
| 2 | REPLACE ME | `python3 scripts/check.py --rule <name>` |
| 3 | REPLACE ME | auditor, spot check 10 rows |
| 4 | REPLACE ME | |
| 5 | REPLACE ME | |

<!--
  Anthropic's generator and evaluator settled on 27 criteria for one app.
  Five is a floor, not a target. Vague criteria produce vague critiques; the
  builder shrugs and does whatever. Granular criteria mean the builder knows
  which exact line to fix.
-->

## Disputes resolved during negotiation

Record what each side pushed for and how it resolved. Six weeks from now this
is the only record of why the standard is what it is.

- REPLACE ME — e.g. "Builder proposed scoring 1-10. Auditor rejected: no way to
  defend a 6 versus a 7. Settled on 1-5."

## Grading

- Any criterion failing fails the item. There is no partial pass.
- A criterion that cannot be verified from available evidence scores 0.0.
- Deferral is not an available verdict.
