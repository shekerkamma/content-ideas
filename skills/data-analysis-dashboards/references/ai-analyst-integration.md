# AI Analyst integration

`data-analysis-dashboards` owns normalization and comparison artifacts.
`ai-analyst` owns the analytical method.

| Stage | AI Analyst behavior | Artifact |
|---|---|---|
| Question | Classify L1-L5; define the decision | analysis question in summary |
| Frame | Define grain, dimensions, metrics, exclusions | methodology block |
| Explore | Inspect dossiers, schemas, category values | input inventory |
| Source tie-out | Reconcile loaded dossiers and evidence | quality report |
| Analyze | Build comparable matrices | CSV files |
| Validate | Check completeness, semantics, and evidence | validation result |
| Chart | Apply `helpers/chart_helpers.py` SWD rules | PNG |
| Present | Context → tension → resolution | report/deck handoff |

For competitor dossiers, the grain is one row per competitor for segment and
evidence matrices, one row per competitor/gate for OEM gates, and one row per
counter-move for actions. A null means missing evidence, not failure. The
threat labels are ordered categories for display only: `NONE`, `LOW`,
`MEDIUM`, `HIGH`; `NOT_ASSESSABLE` is outside that scale.

The deterministic builder is deliberately narrow. Analyst judgment remains in
the dossier, where it can be traced to evidence. The builder must not invent a
threat, certification, gate, price, or relationship.
