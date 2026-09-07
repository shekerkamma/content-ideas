---
name: data-readiness-assessment
description: Evaluates whether an organisation's data is fit for AI — assessing quality, access, lineage, governance, and coverage gaps by use case. Use before committing to AI use cases or before data platform investment decisions.
---

# Data Readiness Assessment

## When To Use

Use before selecting or committing to AI use cases, or when a proposed use case is stalling. Ninety percent of AI projects that fail to reach production do so because of data issues that were not assessed upfront. A data readiness assessment makes those issues visible before the investment is made, not after.

## Consulting Approach

Data readiness is use-case specific, not global. An organisation may have excellent transactional data for a demand-forecasting model while having no usable data for a customer-churn predictor. Assess readiness per use case or use case cluster, not for "the organisation" in the abstract. The five readiness dimensions — availability, quality, access, lineage, and governance — each produce different remediation paths.

## Workflow

1. Identify the target use cases or use case clusters to assess (import from `/ai-use-case-prioritiser` if available).
2. For each use case, map the data required: source systems, data types, volume, frequency, history depth.
3. Score each data requirement across five dimensions: Availability, Quality, Access, Lineage, Governance.
4. Identify critical gaps: data that is required, low-scored, and has no short-term remediation path.
5. Estimate remediation effort for each gap: Quick fix (<4 weeks), Medium (4–12 weeks), Long-term (>12 weeks / strategic investment).
6. Produce a readiness verdict per use case: Ready, Conditionally Ready, or Blocked.

## Output Format

```markdown
# Data Readiness Assessment — [Organisation / Use Case Scope]
**Date:** [YYYY-MM-DD]

## Use Case Data Map
| Use Case | Required Data | Source System | Volume | Frequency | History Required |
|---|---|---|---|---|---|

## Readiness Scorecard (per use case)
| Use Case | Availability | Quality | Access | Lineage | Governance | Verdict |
|---|---|---|---|---|---|---|

**Score:** 1 = Critical gap · 2 = Significant gap · 3 = Minor gaps · 4 = Ready
**Verdict:** Ready · Conditionally Ready · Blocked

## Critical Gaps
| Gap | Use Case Affected | Dimension | Root Cause | Remediation | Effort | Owner |
|---|---|---|---|---|---|---|

## Remediation Roadmap
| Priority | Remediation Action | Use Cases Unblocked | Effort | Owner | Target Date |
|---|---|---|---|---|---|

## Verdict Summary
| Use Case | Verdict | Condition (if Conditional) | Earliest Possible Start |
|---|---|---|---|

## Data Platform Implications
[What platform investments, governance changes, or sourcing decisions are needed before AI delivery can begin?]
```

## Quality Bar

- Readiness scores must be use-case specific — a global data score is not actionable.
- "Blocked" verdicts must name the specific gap and estimated remediation timeline.
- Remediation must be sequenced against the use case delivery plan — a 12-week data fix for a Week-4 AI pilot is a programme risk.
- Do not recommend use cases as "ready" if any dimension scores 1 — flag as Conditionally Ready at minimum.
