---
status: reviewed
use_case: "Fraud and Risk Detection"
last_updated: "2026-06-26"
source_confidence:
  competitor: high
  pricing: medium
  workflow: high
---

# Fraud and Risk Detection Disruptive Competitor Teardown

## Market Frame
- Workflow: investigate flagged transactions, logins, or account events and produce an explainable risk decision.
- Target buyer: fraud, payments, and risk operations teams in ecommerce and fintech.
- Existing spend category: fraud engines, identity/risk add-ons, chargeback tooling, and manual review queues.
- Incumbent economic model: per-transaction, enterprise, or outcome-linked pricing with data dependencies.
- Agentic wedge: synthesize customer history and outside signals into a reasoned risk memo rather than a black-box score alone.

## Incumbent Map
| Incumbent | Category | Buyer | Pricing Signal | Onboarding / Admin Friction | Strength | Weakness |
|---|---|---|---|---|---|---|
| Stripe Radar | Fraud detection | Payments teams | Platform add-on / usage-based | Rule tuning and payment-flow integration | Native to Stripe payments | Best when payments already run through Stripe |
| Sift | Fraud / risk platform | Fraud ops | Sales-led enterprise pricing | Event instrumentation and policy tuning | Good identity and behavior signals | Requires integration discipline |
| Riskified | Ecommerce risk platform | Ecommerce risk teams | Sales-led / outcome-linked | Checkout and policy integration | Strong ecommerce focus | Merchant-specific implementation |
| Risk / fraud spreadsheets | Manual review | Smaller ops teams | Labor only | Exception handling and analyst memory | Cheap to start | Slow, inconsistent, and hard to scale |

## Direct Threats
1. Native payment-fraud add-ons.
2. Ecommerce fraud platforms with decisioning and liability-shift language.
3. Manual review queues operating on rules and analyst judgment.

## Adjacent / Hidden Competitors
- Identity verification and account-security vendors.
- Chargeback management tools.
- Device fingerprinting and IP intelligence tools.
- Internal risk models already embedded in payment gateways.

## Pricing Friction
- Fraud vendors frequently sell on enterprise or usage-based terms.
- Many packages are bundled with broader payment or risk platforms.
- Implementation cost includes event instrumentation and policy tuning.
- The customer often pays both the software vendor and the manual review team.

## Onboarding And Workflow Friction
- Instrumenting the transaction and identity event stream.
- Aligning fraud policy with business risk tolerance.
- Handling cold start users with limited history.
- Keeping review decisions explainable to support, payments, and finance.

## What Not To Build
- Do not promise a fully autonomous black-box fraud score.
- Do not replace the payment gateway or identity system.
- Do not suppress uncertainty in cold-start cases.
- Do not eliminate human review for high-value or high-risk events.

## What To Keep
- System of record: payment gateway, case management, and transaction history.
- Existing review queue and chargeback workflow.
- Human escalation for edge cases and policy changes.

## Agentic Wedge
- Wedge statement: turn a flagged transaction into a readable investigation packet.
- Why it wins: faster reviews, fewer false positives, and better analyst throughput.
- Why now: fraud vendors are powerful but still rely on heavy instrumentation and manual policy work.
- 30-day proof: one high-volume fraud signal, one risk memo, and one analyst approval loop.

## Blueprint Inputs
- Scope implication: start with one signal class and one decision path.
- Architecture implication: read-only event stream, feature store, and case UI.
- Build-vs-buy implication: buy the payment and identity rails, build the investigation layer.
- ROI implication: use reduced manual review time and lower false positives.
- QA/deployment implication: explainability, audit logs, and analyst override paths are mandatory.

## Source Notes
- Stripe Radar - https://stripe.com/radar - accessed 2026-06-26 - payment-fraud add-on positioning.
- Sift homepage - https://www.sift.com/ - accessed 2026-06-26 - fraud prevention and risk-based authentication.
- Riskified homepage - https://www.riskified.com/ - accessed 2026-06-26 - ecommerce fraud prevention and chargeback guarantee.

