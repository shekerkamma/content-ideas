---
name: ai-build-buy-partner
description: Evaluates build vs buy vs partner options for each AI capability, producing a sourcing decision with rationale, vendor shortlist, and commercial model recommendation. Use when the AI operating model is defined and sourcing decisions must be made for each capability in the portfolio.
---

# AI Build-Buy-Partner

## When To Use

Use after the AI operating model is defined and use cases are prioritised. Every AI capability in the portfolio requires a sourcing decision — and the default assumption that "we will build it ourselves" or "we will buy a platform" is rarely optimal across an entire portfolio. Different use cases warrant different sourcing approaches.

## Consulting Approach

The build-buy-partner decision is driven by four factors: strategic differentiation (does this capability give us competitive advantage?), capability (do we have or can we build the skills?), speed (how quickly do we need this?), and total cost. Capabilities that are differentiating and in-house-buildable should be built. Commoditised capabilities that vendors have already solved should be bought. Capabilities where we need expertise we cannot acquire quickly enough should be partnered. The trap is treating all capabilities the same.

## Workflow

1. List every AI capability required across the use case portfolio (not use cases — capabilities that underpin them: e.g. NLP, computer vision, predictive modelling, RAG pipeline, ML Ops platform).
2. Score each capability on Differentiation (H/M/L): would building this in-house give competitive advantage?
3. Score each capability on Internal Feasibility (H/M/L): do we have or can we rapidly acquire the skills and data to build this?
4. Score each capability on Speed-to-Value (H/M/L): how urgently is this capability needed?
5. Apply the decision matrix to derive Build / Buy / Partner recommendation per capability.
6. For Buy and Partner options, produce a vendor shortlist with commercial model recommendation.

## Output Format

```markdown
# AI Build-Buy-Partner — [Organisation]
**Date:** [YYYY-MM-DD]

## Capability Register
| # | Capability | Use Cases It Enables | Differentiation | Internal Feasibility | Speed-to-Value | Decision |
|---|---|---|---|---|---|---|

**Decision matrix:**
- High Diff + High Feasibility → Build
- High Diff + Low Feasibility → Partner (protect the IP)
- Low Diff + High Feasibility → Build or Buy (cost comparison)
- Low Diff + Low Feasibility → Buy

## Decision Deep-Dives

### Build Capabilities
| Capability | Rationale | Skills Needed | Build Timeline | Investment |
|---|---|---|---|---|

### Buy Capabilities
| Capability | Rationale | Vendor Shortlist | Preferred Vendor | Commercial Model | Annual Cost |
|---|---|---|---|---|---|

### Partner Capabilities
| Capability | Rationale | Partner Shortlist | Partnership Type | IP Ownership | Exit Rights |
|---|---|---|---|---|---|

## Vendor Shortlist (for Buy / Partner)
| Vendor | Capabilities | Strengths | Risks | Commercial Model | Reference Clients |
|---|---|---|---|---|---|

## Commercial Model Recommendation
[SaaS subscription / consumption-based / outcome-based / build-operate-transfer. Which model fits each capability and why.]

## Portfolio Risk Assessment
[What happens if a key vendor exits the market or is acquired? Where are single points of failure in the sourcing strategy?]
```

## Quality Bar

- Every capability needs an explicit decision — "to be determined" is not a sourcing strategy.
- Differentiation scores must be challenged: most organisations overestimate how differentiating their AI use cases are.
- Partner decisions must address IP ownership and exit rights — an AI capability built on a partner's proprietary model is a dependency, not a capability.
- Cost estimates must include total cost of ownership, not just licence fees — integration, maintenance, and upskilling costs must be included.
