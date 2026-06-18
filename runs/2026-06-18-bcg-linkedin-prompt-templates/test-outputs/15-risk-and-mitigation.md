# Risk and Mitigation — Apex HR Payroll Strategy

## Risk Register
| Risk | Likelihood | Impact | Velocity | Root Cause | Mitigation | Owner |
|---|---|---|---|---|---|---|
| Payroll compliance failure (tax / garnishment error) | Medium | Critical | Fast | Payroll is high-stakes; errors cause legal liability | Hire dedicated compliance counsel; run parallel payroll for 90 days before GA | CTO + Legal |
| Rippling pre-emptive discounting before payroll GA | High | High | Medium | Rippling will see deal loss trend and respond | Lock renewals on 12-month contracts before GA announcement; price-lock existing customers | VP Sales |
| Check partnership collapses or pivots | Low | High | Slow | Partner dependency; Check is VC-backed, may exit or reprice | Negotiate 2-year rate lock; maintain parallel native build scoping | CTO |
| Payroll launch delayed >12 months | Medium | High | Slow | Engineering complexity underestimated; compliance blockers | Milestone-based hiring plan; monthly compliance checkpoints | CPO |
| Key engineer departures during build | Medium | High | Fast | Market demand for payroll engineers is high | Retention bonuses tied to payroll GA; hire two senior payroll engineers by Month 2 | CPO + HR |
| Win/loss analysis shows payroll is NOT the disqualifier | Medium | Critical | Immediate | Assumption unvalidated | Run analysis Week 1; strategy decision gates on result | Head of Sales |

## Early Warning Indicators
- Win rate drops >5% in one quarter despite payroll launch — competitive response escalating
- Check API rate changes >20% — partnership economics at risk
- Engineering velocity drops below plan 3 months before GA — timeline slippage
- Two or more senior engineers resign — talent risk materializing

## Contingency Plans
- If compliance failure: pause processing, notify customers within 24 hours, activate legal protocol, credit affected payrolls
- If win/loss shows payroll not disqualifier: pivot to upmarket (500–1,000) and analytics as growth levers instead
