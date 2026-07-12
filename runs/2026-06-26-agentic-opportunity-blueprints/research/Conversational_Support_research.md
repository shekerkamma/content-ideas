# Conversational Support Research Memo

As of June 26, 2026, the market is moving from chatbot add-on to digital labor
priced by resolved work. The best wedge is not replacing Zendesk/Freshdesk on
day one; it is attaching to the incumbent help desk and renegotiating economics
from seats/FTEs to verified tier-1 outcomes.

## Incumbents And Categories

- Help desk suites: Zendesk, Salesforce Service Cloud, Freshdesk/Freshworks,
  Intercom/Fin. These own inbox, ticketing, routing, knowledge base, reporting,
  SLAs, and enterprise procurement.
- AI-native support agents: Fin, Ada, Gorgias AI Agent, Tidio/Lyro, Forethought,
  Cognigy/NICE, LivePerson. These compete on autonomous resolution,
  multichannel operation, and measurable deflection.
- CCaaS/contact-center platforms: NICE CXone, Genesys, Five9, Talkdesk,
  LivePerson. Stronger in voice, routing, workforce management, QA, and
  enterprise telephony.
- BPO/tier-1 outsourcing: Concentrix, Teleperformance/TP, TaskUs,
  SupportNinja, Helpware. These sell staffed capacity, QA, training, workforce
  management, and operational accountability.
- Vertical help desks: Gorgias is especially relevant for Shopify/ecommerce,
  where support actions include refunds, returns, order edits, subscriptions,
  discounts, and product recommendations.

## Pricing And Pricing Friction

- Fin/Intercom: Fin priced at `$0.99 per outcome`. Intercom still charges seats
  for help desk plans: Essential promotional `$19/seat/month`, Advanced `$85`,
  Expert `$132`. Standalone Fin can run with an existing help desk, no seats
  required, but has minimum monthly commitments.
- Freshdesk: Growth `$19/agent/month`, Pro `$55`, Enterprise `$89`, billed
  annually. Freddy AI Agent includes 500 sessions on Pro/Enterprise, then `$49`
  per 100 sessions.
- Salesforce Service Cloud: Starter `$25/user/month`, Pro `$100`, Enterprise
  `$165`.
- Gorgias: pricing is by ticket volume rather than seats; plans start at
  `$10/mo`, `$50/mo`, `$300/mo`, and `$750/mo`, with AI Agent around
  `$0.90-$1.00` per resolved conversation depending on tier.
- Zendesk: public page emphasizes AI agents and contact-sales AI details;
  TechRadar reported outcome-based AI pricing tied to verified resolutions.
- BPO friction: Helpware pricing depends on requirements and uses hourly,
  subscription, transaction, outcome, or gainsharing models. Hiring takes 2-4
  weeks minimum after contract/calibration. SupportNinja tiers are quote-based.

## Buyer Pain And Workflow Friction

- Zendesk CX Trends 2026: 74% of customers are frustrated by repeating their
  story; 74% expect 24/7 service because of AI; 88% expect faster response than
  a year ago; 95% expect explanations for AI-made decisions.
- Customer-service chatbot research from Kagan, Hathaway, and Dada describes
  gatekeeper aversion: customers avoid bots when they expect an imperfect first
  stage before reaching an expert. Adoption improves when companies show wait
  times, explain bot limits, and provide fast live-agent fallback.
- Nubank's 2026 customer-support agent paper frames the production challenge:
  reliable handoff, sensitive-data handling, narrow-but-deep workflows, and
  strong evaluation. Its large-scale deployment reported a 37 percentage-point
  tNPS lift and 29 percentage-point self-service-rate lift in one card-delivery
  use case versus prior agent variants.

## Disruptive Agentic Wedge

Position as tier-1 resolution capacity, paid only when resolved, not as a
chatbot or help desk.

The wedge offer:

- Runs on top of Zendesk, Freshdesk, Salesforce, Intercom, Gorgias, or inbox
  email.
- Starts with 2-3 high-volume workflows: order status, refund/return status,
  password/account access, billing explanation, appointment/reschedule, or
  subscription changes.
- Prices against avoided seats/BPO hours: first 1,000 verified resolutions at a
  fixed pilot price, then per verified resolution.
- Uses a human fallback guarantee: unresolved or low-confidence cases escalate
  with summary, customer history, tool outputs, and next-best action.
- Differentiates from incumbent AI by being faster to deploy, narrower in
  scope, accountable on economics, and useful during BPO/help-desk renewal.

## 30-Day MVP Implications

Build the MVP as a resolution layer, not a new help desk.

- Week 1: ingest help-center docs, macros, SOPs, recent tickets, tags,
  escalation policy, and compliance rules. Pick two workflows with clear
  success/failure labels.
- Week 2: integrate one help desk plus 2-4 tools: CRM/customer profile,
  order/subscription system, billing/refund system, knowledge base. No
  free-form autonomy for money-moving actions.
- Week 3: ship agent with retrieval, workflow routines, tool calls, escalation,
  transcript summary, and admin review queue.
- Week 4: run shadow mode, then limited live traffic. Report resolution rate,
  escalation rate, hallucination/policy-failure rate, CSAT/tNPS proxy,
  handle-time saved, avoided BPO hours, and cost per verified resolution.

Required product surface: source-grounded answers, confidence thresholding,
customer-visible transparency, talk-to-human escape hatch, audit logs,
redaction, role-based access, test set/eval dashboard.

## Risks, Security, Regulatory

- Data exposure and hallucination: customer support agents combine untrusted
  customer text with privileged backend tools.
- LLM security: OWASP lists prompt injection, sensitive-information disclosure,
  insecure plugin/tool design, excessive agency, and overreliance as core
  LLM-app risks.
- Regulated workflows: financial services, health, insurance, telecom, and
  employment support need explicit boundaries around advice, eligibility,
  refunds, cancellations, claims, and records retention.
- Customer trust: customers want transparency, explanations, and human fallback.
- Labor/contract risk: BPO replacement can trigger SLA, data-processing,
  union/works-council, offshore-transfer, and vendor-exit constraints.
- Operational liability: failed refunds, incorrect policy promises, account
  lockouts, and bad debt/medical/insurance guidance need compensating controls.

## Sources

- Intercom Pricing: https://www.intercom.com/pricing
- Freshdesk Pricing: https://www.freshworks.com/freshdesk/pricing/
- Salesforce Service Cloud Pricing:
  https://www.salesforce.com/products/service-cloud/pricing/
- Gorgias Pricing: https://www.gorgias.com/pricing
- Zendesk Pricing: https://www.zendesk.com/pricing/
- Zendesk CX Trends 2026: https://cxtrends.zendesk.com/
- Helpware CX Pricing: https://helpware.com/cx/pricing
- SupportNinja Pricing: https://www.supportninja.com/pricing
- Ada pricing funnel: https://www.ada.cx/pricing/
- OWASP Top 10 for LLM Applications:
  https://owasp.org/www-project-top-10-for-large-language-model-applications/
- NIST AI Risk Management Framework:
  https://airc.nist.gov/airmf-resources/airmf/
- Kagan, Hathaway, Dada, "Deploying Chatbots in Customer Service":
  https://arxiv.org/abs/2504.06145
- Gupta et al., "Building Customer Support AI Agents at 100M-User Scale":
  https://arxiv.org/abs/2606.08867
- TechRadar, Zendesk outcome-based AI pricing:
  https://www.techradar.com/pro/zendesk-links-ai-pricing-to-verified-resolution-outcomes
- ITPro, AI agent rollback/governance survey coverage:
  https://www.itpro.com/technology/artificial-intelligence/ai-agents-arent-cutting-it-in-customer-service
