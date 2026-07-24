# UC-08 story architect pack

## BLUF

An engineering team can assemble a low-cost multi-model coding pilot with OpenCode,
NVIDIA-hosted prototype endpoints, and ZenMux, but it must validate access terms, model
availability, data handling, quality, and production economics before scaling.

## Audience decision

Approve a four-week, non-production pilot for a small engineering cohort, with explicit
exit criteria and no assumption that promotional or developer access remains free.

## Tension

Coding-agent subscriptions and provider-specific integrations fragment access, while
preview endpoints and promotions can change without notice. A useful pilot must prove the
workflow and operating controls—not merely demonstrate that a model can answer a prompt.

## Argument arc

1. A low-cost pilot is possible now.
2. The current problem is fragmented access, cost, and configuration.
3. The target state is one terminal workflow with governed model choice.
4. OpenCode connects the workflow to NVIDIA and ZenMux providers.
5. Current official sources support the core access and model claims, with conditions.
6. A four-week pilot can test value before production commitment.
7. Success is measured by task outcomes, reliability, cost, and governance.
8. Known risks have explicit mitigations and stop conditions.
9. The decision is to authorize a bounded pilot, not declare permanent zero cost.

## Slide spine

| # | Assertion title | Role | Evidence | Visual treatment | Speaker implication |
|---|---|---|---|---|---|
| 1 | A low-cost multi-model coding pilot is possible now | Cover / answer | Source deck + official provider docs | Dark native terminal/model-switch motif | Frame this as a pilot hypothesis. |
| 2 | The opportunity is access without premature platform lock-in | Executive summary | OpenCode provider support; developer and promotional access | Four native decision tiles + recommendation bar | Approve testing, not production. |
| 3 | Cost and configuration fragment the developer experience | Current pain | Source deck problem statement | Friction chain with impact panel | The issue is workflow fragmentation. |
| 4 | One terminal workflow can govern model choice by task | Target operating model | OpenCode `/connect` and `/models` workflow | Target-state architecture | Govern selection centrally. |
| 5 | The workflow is a four-step connection and selection loop | AI workflow | OpenCode provider documentation | Native process chain | Setup is straightforward but must be verified. |
| 6 | Official sources support the core proposition—with conditions | Proof objects | OpenCode, NVIDIA, ZenMux, Kimi official pages | Evidence matrix + condition strip | Separate verified facts from assumptions. |
| 7 | Four weeks is enough to test value and operating fit | Roadmap | Pilot design | Native milestone rail + owners | Keep the cohort and scope bounded. |
| 8 | Pilot success is task quality, reliability, and controlled cost | Metrics | Proposed measurement framework | KPI scorecard | Avoid unverified ROI claims. |
| 9 | The main risks are commercial, operational, and governance-related | Risks | Official terms + delivery assumptions | Risk/mitigation matrix | None of the risks requires abandoning the pilot. |
| 10 | Approve a bounded pilot with explicit exit criteria | Decision / next step | Synthesized recommendation | Dark decision panel + checklist | The ask is a controlled experiment. |

## Evidence map

### Direct evidence

- OpenCode documents native provider connection through `/connect` and model selection
  through `/models`, including NVIDIA and ZenMux.
- NVIDIA documents free Developer Program access to hosted NIM endpoints for prototyping,
  research, development, and testing; production requires NVIDIA AI Enterprise licensing.
- NVIDIA's model catalog showed 139 models on 22 July 2026, with individual entries marked
  as free endpoints or downloadable.
- ZenMux listed `moonshotai/kimi-k3-free` at $0 input/output pricing for a limited time.
- Kimi Code documents Kimi K3 as a 2.8T-parameter model with up to a 1M-token context window,
  subject to membership tier.

### Fair synthesis

- These components are sufficient to test a multi-model coding workflow without committing
  to a production platform contract.
- Provider and model switching can reduce lock-in only if task routing and evaluation are
  standardized.

### Interpretation / pilot hypotheses

- A small cohort can complete setup and establish a useful baseline within four weeks.
- The workflow may reduce subscription spend, but savings must be measured rather than
  asserted from the source deck's `$0` and `$100+` comparisons.

## Content cuts

- Remove the unsupported KingBench ranking and comparisons to unnamed model versions.
- Remove permanent `$0`, `100% free tier`, and `$100+` savings assertions.
- Remove the duplicated setup checklist and quote from the original risks slide.
- Avoid model-count claims tied to a static hand-curated list; show the dated catalog count
  only as an observation.
- Do not present the creator's personal usage as enterprise validation.

## Rebuild instructions

- Rebuild all ten slides as native PowerPoint objects on the 1280×720 design-system grid.
- Preserve the original ten-beat sequence while making slides 9 and 10 distinct.
- Use assertion titles, one primary proof object per slide, and varied layouts.
- Keep the deck company-neutral; use `CLIENT · UC-08 · 22 JUL 2026` in the footer.
- Put full URLs and claim qualifications in speaker notes; use compact source labels on-slide.
- Mark all commercial access, availability, and cost statements as pilot-time conditions.
- Preserve the original source file unchanged.
