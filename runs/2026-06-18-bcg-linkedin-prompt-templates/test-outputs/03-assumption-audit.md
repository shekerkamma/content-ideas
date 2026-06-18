# Assumption Audit — Apex HR

## Strategy Being Tested
Apex HR will build a Payroll module and expand into APAC simultaneously over the next 18 months to re-accelerate growth to 25%+ ARR.

## Assumption Register
| Assumption | Category | Importance | Evidence Strength | Risk |
|---|---|---|---|---|
| Payroll module will close win-rate gap vs Rippling/Deel | Competitive | Critical | Weak | If payroll not the deciding factor, build effort is wasted |
| APAC buyers have comparable willingness-to-pay | Market | High | Weak | APAC pricing pressure could dilute unit economics |
| Can build compliant payroll engine in 12 months | Operational | Critical | Weak | Payroll compliance is notoriously hard; timeline risk high |
| Existing customers will upgrade to Payroll | Economic | High | Weak | NRR 101% baseline suggests upsell motion not proven |
| 200 employees is true disqualification threshold | Competitive | High | Medium | May be 150 or 250; threshold drives ICP segmentation |
| Rippling/Deel won't further bundle during build | Competitive | High | Weak | Both well-funded and could pre-empt the response |

## Load-Bearing Assumptions
1. Payroll IS the disqualifying factor — if pricing or integrations are equally important, the product investment thesis changes
2. 12-month payroll build is achievable — payroll compliance is one of the hardest engineering problems in HR tech

## Test Plan
| Assumption | Test | Data Needed | Owner | Decision Trigger |
|---|---|---|---|---|
| Payroll = disqualifier | Win/loss analysis: % of deals lost citing payroll | CRM loss reasons + 20 interviews | Head of Sales | <50% cite payroll → pivot strategy |
| Build timeline | Architecture assessment + vendor partnership eval (Gusto, Check) | Engineering estimate + terms | CTO | Build >18mo → evaluate buy/partner first |
| APAC unit economics | 10 prospect interviews ANZ/Singapore + pilot pricing | Customer interviews, pricing data | Head of Revenue | WTP <70% of US ACV → delay APAC |

## Recommendation
Test before build. Run win/loss analysis (4 weeks) and CTO architecture assessment (4 weeks) in parallel before committing to payroll build. APAC is a distraction until the core product gap is resolved.
