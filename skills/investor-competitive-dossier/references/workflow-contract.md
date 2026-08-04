# Workflow contract

## Ownership

| Stage | Owner | Handoff |
|---|---|---|
| Recall | GBrain and local inventory | prior facts, corrections, source pointers |
| Acquisition | You.com Level 2, Exa, then capture fallback | query log, fresh captures, extraction statuses |
| Evidence | AI Analyst competitor analysis | ledger, metric definitions, quality, allowed numbers |
| Perspectives | STORM | five independent lenses, contradiction map, verifier results |
| Competitive model | Competitor-analysis pipeline | arenas, alternatives, heatmap, investor brief |
| Story | Story architect and document review | BLUF, storyboard, evidence map, content cuts |
| Visual/build | Present + branded PPTX | contracts, editable deck, builder |
| QA | Design lint, OfficeCLI, material comparison | exact-artifact evidence and status |
| Compounding | GBrain write-back | durable findings and corrections |

## Invariants

1. Data taps collect evidence; they do not assign conviction.
2. The evidence ledger is the claim source of truth.
3. Every visible number must appear in `allowed-numbers.yaml`.
4. Financing is runway/expectation evidence, not product-market proof.
5. Product, silicon, validation, production, bookings, revenue, and deployment are separate states.
6. The story is locked before slides are built.
7. Company claims remain labeled after they are repeated by press.
8. A repeated teardown frame may aid comparison; repeated unsupported conclusions do not.
9. The final status is determined by gates, not the filename.

## Canonical paths and precedence

- Keep all artifacts under `runs/<YYYY-MM-DD>-<target>-investor-competitive-dossier/`.
- Child-skill output examples do not create additional run roots.
- Research precedence is local/GBrain → You.com Level 2 → Exa → primary follow-up →
  Firecrawl/Printing Press capture fallback → generic verification.
- Persist STORM lenses and verifier results under `working/storm/`; do not leave them only in
  chat or ephemeral agent messages.
- A PPTX-only run can be a QA-passed draft. Complete reviewed promotion requires the HTML
  twin, sync check, and delivery manifest.
- The branded template is mandatory. Custom identity tokens are optional only when the
  resolved template already supplies the approved client identity.

## Resume behavior

- Read `status.json` first.
- Reuse valid captures and QA only when they match the exact source or artifact checksum.
- Backfill missing controls without deleting prior artifacts.
- Never restart research merely because a new deck version is requested.

## Compound loop

```text
recall → acquire → evidence → independent lenses → verify → story → review → build → QA
   ↑                                                                            ↓
   └──────────────────────────── GBrain learning write-back ────────────────────┘
```
