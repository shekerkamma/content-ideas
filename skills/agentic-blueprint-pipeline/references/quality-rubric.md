# Master Blueprint Quality Rubric

Use this as the acceptance gate before a blueprint can be marked `reviewed`.

## Hard Gates

- Contains all 10 required artifacts.
- Includes at least 8 credible sources for gold-standard blueprints.
- Uses at least 3 competitor-specific sources.
- Labels assumptions where exact pricing, ACV, labor cost, or deployment data is
  unavailable.
- Includes a reconstructed ROI model with base/upside/downside cases.
- Includes implementation-depth details: schema/data model, API surface,
  integration plan, env vars, folder/module structure, observability, smoke
  test, and rollback.
- Names out-of-scope items and not-to-build items.
- Includes security/privacy/regulatory risks where relevant.
- Includes a test plan with observable verification, not vague acceptance text.
- Includes deck-ready executive positioning.

## Scoring

Score each area from 0-3.

| Area | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Evidence depth | Unsupported | Generic | Some sources | Source-backed and current |
| Competitor specificity | None | Category only | Named competitors | Named competitors + wedge |
| ROI quality | Missing | Hand-wavy | Range model | Scenario model with assumptions |
| Implementation credibility | Vague | Stack list | Architecture outline | Schema/API/integrations/deployment details |
| Scope discipline | Missing | Broad | MVP-ish | Tight 30-day proof |
| Testability | Missing | Generic | Some AC | Clear AC + edge cases |
| Data/security | Missing | Light | Covers data | Covers data + privacy/regulation |
| Positioning clarity | Generic | Some wedge | Clear wedge | Memorable market narrative |

Minimum reviewed score: 20/24, with no hard gate failures.

## Status Rules

- `draft-needs-research`: missing hard evidence or current competitor research.
- `draft-needs-operator-review`: evidence exists but strategy/ROI needs judgment.
- `reviewed`: passes hard gates and scores at least 20.
- `blocked`: key market or regulatory facts cannot be verified.
