# Competitor-analysis skill wiring

## Routing decision

Use the narrowest upstream that covers the decision:

| Request | Start with | Then hand to this skill when |
|---|---|---|
| Current sourced competitor landscape, battlecards, branded deck/HTML | `competitor-analysis-pipeline` | research table and story pack exist |
| Repeatable evidence-controlled scoring, confidence and traceability | `evidence-led-competitor-pipeline` | evidence and story gates pass |
| Metric-first benchmarking or quantified heatmaps | `aianalyst-competitor-analysis` | ledger, metric specs, data quality and allowed numbers exist |
| Enterprise AI universe of 100–150 companies | `enterprise-ai-competitor-landscape` | normalized universe and category outputs exist |
| Investor/startup cohort diligence | `investor-competitive-dossier` | thesis, cohort and diligence evidence exist |
| Surgical edits to an already reviewed competitor deck | `pptx-toolkit` | exact slide/shape operations are named |

Do not run several overlapping competitor skills merely to claim coverage. Use
`evidence-led-competitor-pipeline` as the compound orchestrator when multiple stages are required.

## Canonical stage graph

```text
GBrain Recall + local run inventory
        ↓
source discovery: You.com Level 2 / Exa / Firecrawl / official sources
        ↓
raw captures + search log
        ↓
aianalyst-competitor-analysis
  evidence-ledger.csv
  metric-definitions.md
  data-quality-report.md
  scoring-model.md
  allowed-numbers.yaml
  competitor-brief.md
        ↓
story-architect + grill-me
  story-architect-pack.md
  story-structure-review.md
  slide spine + evidence map + cuts
        ↓
compound-competitor-analysis-pptx
  slide-content-contracts.json
  slide-design-contracts.json
  slide-plan.json + visual-spec.json
        ↓
branded-pptx-deck
  native editable builder + draft PPTX
        ↓
design lint + OfficeCLI HTML/native PowerPoint QA
        ↓
reviewed PPTX
        ↓
competitor-analysis-pipeline downstream package
  synchronized HTML / battlecards / delivery manifest / optional publishing
        ↓
GBrain Write-back + monitoring triggers
```

Data taps discover and capture. They never score, recommend, or write client claims. Renderers
format validated contracts. They never reinterpret evidence.

## Required upstream handoff

Do not start slide authoring until these exist or are explicitly waived with a reason:

```text
status.json
outputs/search-log.md
outputs/evidence-ledger.csv
outputs/metric-definitions.md
outputs/data-quality-report.md
outputs/scoring-model.md
outputs/allowed-numbers.yaml
outputs/competitor-brief.md
outputs/story-architect-pack.md
outputs/story-structure-review.md
```

The evidence ledger must be one row per claim and include competitor/entity, claim, evidence ID,
source, date, source type, evidence status, confidence, scope, and destination slide IDs.

`allowed-numbers.yaml` is the only source for visible quantitative claims. The slide contract may
carry qualitative synthesis only when it is labeled `qualified interpretation`.

## Handoff mapping into slide contracts

| Upstream artifact | Slide-contract consumer |
|---|---|
| Evidence ledger | evidence blocks, source notes, evidence-status encoding |
| Metric definitions | chart axes, heatmap scales, score labels, units and denominators |
| Data-quality report | caveats, confidence, missing-data treatment, search-again triggers |
| Scoring model | ranking logic, weights, sensitivity and scorecard exhibits |
| Allowed numbers | visible metrics and numerical titles |
| Competitor brief | executive answer, arenas, threats, win/partner/avoid logic |
| Story-architect pack | slide order, titles, transitions, evidence map and content cuts |
| Grill-me review | counterarguments, falsifiers, missing proof, slide-specific rewrites |

## Competitor slide families

Use a portfolio, not one repetitive company template:

1. decision context and mandate/timing;
2. market architecture by buyer job and control point;
3. competitor universe and inclusion logic;
4. comparable threat heatmap with confidence;
5. priority competitor dossiers;
6. control-point collision maps;
7. proof/evidence ladders;
8. partner-versus-compete decisions;
9. pricing/economics bridges only when metrics are comparable;
10. counter-moves, owners, triggers, and stop rules;
11. evidence appendix and diligence queue.

Comparable dossier pages use consistent geometry. Non-comparable competitors must not be forced into
the same scorecard. Separate stack layers, buyer arenas, and product scope.

## Upstream gates

Block slide authoring when:

- research notes exist but no claim-level ledger exists;
- metrics, scales, weights, or denominators are undefined;
- source coverage differs materially across competitors but confidence is hidden;
- an important fact is only a vendor claim and attribution is absent;
- rankings exceed the evidence quality;
- story slides do not map to evidence rows or labeled interpretation;
- visible numbers are absent from `allowed-numbers.yaml`;
- the latest grill/story review is not reflected in the slide spine.

## Downstream handoffs

The reviewed PPTX may feed:

- synchronized self-contained competitor HTML;
- buyer/persona battlecards;
- sales objection and messaging collision maps;
- partnership and channel target lists;
- diligence requests and primary-source search queues;
- 30/90-day competitive response plans;
- evidence-event monitoring and threat-score updates;
- investor diligence dossiers;
- GBrain durable findings.

Every derivative must retain claim IDs, evidence statuses, allowed-number controls, and the same
decision boundaries. Do not copy slide prose into battlecards without preserving provenance.

## Downstream completion contract

Write `client-package/delivery-manifest.json` with:

- research/evidence artifact paths and row counts;
- story pack and review paths;
- builder, PPTX, slide count and editability mode;
- HTML/battlecard paths when requested;
- OfficeCLI validation, issues, HTML/native render paths and status;
- material-change report for redesigns;
- sync check and delivery checksum;
- explicit `draft`, `reviewed`, or `blocked` status.

Write durable sourced findings back to GBrain only after delivery. Never write unsupported scores,
internal drafts, client deliverables, or credentials to GBrain.
