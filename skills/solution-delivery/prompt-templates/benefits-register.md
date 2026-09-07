---
skill: /benefits-register
pack: solution-delivery
chains-from: /business-case-builder, /adoption-plan
chains-into: /post-implementation-review, /performance-review
---

# Prompt Template: Benefits Register

**When to use:** At project start — translate the business case into a tracked register of measurable benefits with owners, baselines, and milestone targets.

## Copy-paste prompt

```
Run /benefits-register for [CLIENT NAME]:

Project: [PROJECT NAME]
Go-live date: [DATE]

Business case summary (from /business-case-builder or brief):
- Total benefit claimed: [£X / $X over Y years]
- Key benefit categories: [e.g. "Cost reduction, revenue uplift, risk reduction, efficiency gain"]

For each benefit, provide:
1. [BENEFIT NAME]
   - Type: [FINANCIAL / OPERATIONAL / STRATEGIC / RISK]
   - Baseline: [current state measure — e.g. "Processing cost: £12 per invoice"]
   - Target: [post-implementation measure — e.g. "£6 per invoice"]
   - Measurement method: [HOW will this be measured]
   - Data source: [WHERE will the data come from]
   - Owner: [WHO is accountable for realising this benefit]
   - Timing: [when benefit starts materialising — e.g. "Month 3 post go-live"]

2. [BENEFIT NAME]
   [same structure...]

Potential disbenefits (negative effects of the change):
- [DISBENEFIT] — [affected group] — [mitigation]
```

## Expected output
Benefits register with baseline/target/owner per benefit, 30/90/180-day milestone targets, measurement schedule, disbenefit register, and benefits realisation governance (who reviews, how often).

## Chain next
- Benefits register becomes the measurement backbone for `/post-implementation-review`
- Tracking cadence feeds into `/performance-review` (continuous-improvement)
