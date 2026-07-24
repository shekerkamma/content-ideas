# Competitor Teardown: Returns & Refund Triage (Use Case 49)

## Legacy Incumbents
**1. Loop Returns**
- **Overview:** Premium returns management platform aimed at mid-market and enterprise Shopify merchants.
- **Teardown:** 
  - *Top Features:* "Shop Now" exchange workflows, automated label generation, return rules engine.
  - *Pricing:* High monthly fees plus per-return transaction costs. Often criticized as "pricey" or an "end-game" tool.
  - *Onboarding Friction:* Setup is generally smooth, but dealing with edge cases, international returns, or hidden costs frustrates users.

**2. Narvar**
- **Overview:** Post-purchase tracking and returns enterprise solution.
- **Teardown:**
  - *Top Features:* Branded tracking pages, returns orchestration, analytics.
  - *Pricing:* Enterprise-level, opaque.
  - *Onboarding Friction:* Complex implementation; users complain that Narvar-branded tracking pages hijack the consumer experience.

**3. ReturnGo**
- **Overview:** Mid-market alternative to Loop.
- **Teardown:**
  - *Top Features:* Exchange automation, return policy enforcement.
  - *Pricing:* More accessible than Loop, but still adds SaaS overhead.
  - *Onboarding Friction:* Requires configuring complex rule-trees for edge cases.

## Where They Are Strong
Loop is incredibly effective at retaining revenue by pushing consumers toward exchanges (store credit/bonus value) rather than outright refunds. Narvar is deeply embedded in the enterprise logistics stack.

## Where They Are Weak
They handle the "happy path" well but fail on edge cases. If a return is damaged, lost by the carrier, or violates a nuanced policy, a human CX agent still has to intervene. They also nickel-and-dime merchants on per-return fees.

## Disruptive Strategy

**Most Direct Threats:** Loop Returns and Narvar.
**Table Stakes:** Automated shipping label generation, checking carrier APIs for tracking status, initiating Shopify refunds/exchanges.
**What we must deliberately NOT do:** We must not build a separate, confusing customer-facing portal that takes users off the brand's site. We act natively within the brand's existing helpdesk (Zendesk/Gorgias).

**The 3 Specific Gaps Our Agentic Wedge Exploits:**
1. **Handling Edge Cases (No CX Required):** Legacy rules engines break when a customer has a unique complaint (e.g., "The item arrived torn"). An agent can read the context, check the photo, and triage the refund autonomously without human escalation.
2. **Carrier Dispute Automation:** Legacy tools track the package, but if it's lost, a human must file the claim. The agent can interface directly with FedEx/UPS APIs to automatically open investigations.
3. **Flat-Rate Execution:** Replacing expensive, complex SaaS tiers and per-return fees with an agent that acts as a scalable CX team member.
