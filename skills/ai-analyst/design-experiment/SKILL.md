---
name: design-experiment
description: >
  Design a controlled experiment (A/B test, multivariate test, or quasi-experiment)
  with clear hypothesis, success metrics, sample size, and statistical power.
  Triggered when users say "design experiment", "A/B test design", "how should we test this",
  or invoke `/design-experiment`.
---

# Skill: Design Experiment

## Purpose
Design a controlled experiment (A/B test, multivariate test, or quasi-experiment) with clear hypothesis, success metrics, sample size, and statistical power. Calls the experiment-designer agent to produce a detailed experiment specification.

## When to Use
- User says "design an experiment for {feature/change}"
- User asks "should we A/B test this?" or "how would you test that?"
- When sizing an opportunity requires validation through experimentation
- When proposing a change needs controlled validation

## Invocation
`/design-experiment {brief}` — design an experiment based on the brief
`/design-experiment --quick` — rapid prototype design (no detailed power calc)
`/design-experiment --analyze {results_file}` — analyze results from a prior experiment

## Instructions

### Step 1: Parse the Brief
Extract from the user's description:
1. **What are we testing?** — Feature, messaging change, pricing, UX variant, etc.
2. **Why test it?** — What business outcome are we trying to improve?
3. **Current baseline:** — What's the metric value today?
4. **Target improvement:** — What change would be meaningful?
5. **Constraints:** — Timeline, budget, technical limitations

Ask clarifying questions if any field is unclear.

### Step 2: Invoke Experiment-Designer Agent
Hand off to the experiment-designer agent with:
- The brief and context
- Current metric baselines (query from active dataset if available)
- User's constraints and timeline
- Instructions to produce a detailed specification

### Step 3: Generate Specification
The experiment designer agent produces:

```markdown
# Experiment Design: {Test Name}

## Hypothesis
**Null hypothesis:** {control and treatment should have equal outcome}
**Alternative hypothesis:** {treatment will improve outcome by X%}

## Experiment Type
- **Design:** [A/B test / Multivariate / Quasi-experiment]
- **Duration:** [estimated time to completion]
- **Primary metric:** {metric_name} ({direction} is better)
- **Secondary metrics:** [list]

## Sample Size & Power
- **Minimum detectable effect:** {X% improvement}
- **Statistical power:** {80% / 90% / 95%}
- **Significance level (α):** 0.05
- **Required sample size (per variant):** {N} users / sessions
- **Time to reach sample:** {estimated duration}

## Experimental Design
### Control (Variant A)
{Current experience / control condition}

### Treatment (Variant B)
{Proposed change / test condition}

### Randomization
- **Unit:** [user / session / page view]
- **Method:** [random hash of ID / feature flag with random exposure]
- **Stratification:** [if needed, e.g., by geography or user cohort]

## Success Criteria
| Metric | Baseline | Target | Interpretation |
|--------|----------|--------|-----------------|
| {primary} | {baseline}% | {baseline + MDE}% | {what this means} |
| {secondary} | {baseline} | {target} | {guardrail or supporting evidence} |

## Implementation Checklist
- [ ] Feature flag set up in {system}
- [ ] Logging instrumented (events: {event_list})
- [ ] Analysis SQL prepared (validate on 1% sample first)
- [ ] Team communication: PMs, Engineers, Analytics
- [ ] Pre-experiment baseline report generated
- [ ] Randomization validation (sanity check)

## Timeline
- **Start date:** {YYYY-MM-DD}
- **Expected completion:** {YYYY-MM-DD}
- **Decision point:** {YYYY-MM-DD}
- **Rollout/Holdout:** {YYYY-MM-DD}

## Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| {risk_name} | High/Med/Low | High/Med/Low | {what we'll do} |

## Analysis Plan
1. **Sanity checks** — validate randomization, check for data quality issues
2. **Intention-to-treat (ITT)** — all exposed users, by original assignment
3. **Heterogeneous effects** — segment results by user cohort (if powered)
4. **Spillover analysis** — check for network effects between variants (if applicable)
5. **Power check** — confirm we reached target sample size
6. **Recommendation** — ship / iterate / stop based on results

## Guardrails
Alert if:
- {metric_1} drops by >X%
- {metric_2} remains flat (no improvement)
- {metric_3} spikes (unexpected behavior)
```

### Step 4: Validate & Refine
Review the specification with the user:
- Are the hypotheses clear?
- Is the sample size realistic given traffic?
- Are metrics well-defined?
- Any concerns about implementation complexity?

Refine if needed before confirming design.

### Step 5: Output Specification
Save the experiment specification to:
```
working/experiments/{test_name}_spec_{DATE}.md
```

Provide:
- Summary of timeline and sample size
- Link to full specification
- Next steps: "Ready to implement? Brief the engineering and PM teams on the spec."

## Edge Cases
- **Insufficient traffic:** Recommend longer test duration or larger MDE
- **High variance metric:** Suggest variance reduction techniques (blocking, cohort analysis)
- **Cannibalization risk:** Design quasi-experiment if perfect randomization impossible
- **Short-term only metric:** Flag: "This metric may have novelty effects. Plan for extended follow-up period."

## Anti-Patterns
1. **Never run without a pre-specified hypothesis** — p-hacking ruins validity
2. **Never use underpowered designs to declare victory** — you'll miss real improvements
3. **Never ignore guardrails** — stopping early to protect negatives is valid
4. **Never assume SUTVA** — if users interact, randomization at user level fails
5. **Never forget intent-to-treat** — segment analysis comes after ITT validation

## Experiment Statistics Library

The coded estimators live at `skills/ai-analyst/design-experiment/scripts/experiment_stats/`.
Add that directory to `sys.path`, then import:

```python
import sys
sys.path.insert(0, "skills/ai-analyst/design-experiment/scripts")
from experiment_stats import power_proportion, proportion_test, srm_check
```

Requires pandas, numpy and scipy. Every function returns a dict carrying an
`interpretation` string written for direct quotation in a brief.

| Need | Function |
|---|---|
| Sample size before launch | `power_proportion`, `power_mean`, `power_at_n`, `detectable_effect`, `duration_estimate`, `power_sensitivity_table` |
| Randomization integrity | `srm_check`, `srm_diagnose` — run this **before** reading any result |
| Fixed-horizon readout | `proportion_test`, `welch_test`, `ratio_metric_test`, `relative_lift` |
| Peeking without inflating error | `always_valid_pvalue`, `confidence_sequence` |
| Bayesian readout | `bayesian_proportion`, `bayesian_mean`, `prob_best`, `expected_loss` |
| Many metrics at once | `adjust_pvalues` (multiple-comparison correction) |
| Tighter tests on the same traffic | `cuped_adjust`, `cuped_adjusted_power`, `winsorize` |
| Effect size | `cohens_d` |

**The SRM gate is not optional.** A 52/48 split on 10,000 users returns
`verdict: BLOCK` at p = 6.3e-5; a compromised randomization makes every downstream
number meaningless. Route to `/srm-check` on any dataset carrying a variant column.

When randomization is impossible, stop and route to `/causal` instead — it selects a
quasi-experimental method and carries the assumption checks that make the estimate
defensible.
