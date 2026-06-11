---
captured: 2026-06-10
source_url: multiple (each claim carries its own primary URL below)
source_type: vendor-doc
domain: sap-ai-transformation
target_section: 2
summary: Joule commercial model, DSAG adoption reality, clean-core=AI-readiness from SAP, automotive proof points
---

## Joule / SAP Business AI commercial model (Tier 1-class: SAP's own docs)

- Hybrid model: **Base AI free** in all cloud subscriptions (Joule Base —
  navigational/informational/transactional CRUD); **Premium AI** = per-user-
  per-month packages + AI Units; **AI Foundation** on BTPEA credits
  (source: learning.sap.com/courses/selling-sap-business-ai pricing module,
  2026-05; sap.com/products/artificial-intelligence/pricing).
- Agent metering by steps: Basic 5 / Standard 10 / Advanced 25 requests per
  step in PUPM packages; consumption path 0.005 / 0.01 / 0.025 AI Units per
  step for custom (Joule Studio) agents (source:
  learning.sap.com/courses/introducing-joule/understanding-the-commercial-model, 2026-03).
- Joule Premium PUPM tiers ~8 down to 1 AI Units/user/month by volume;
  Document Grounding 0.005 AI Units/record (source: sap.com pricing page).

## Market reality (Tier 3 — strong, named surveys)

- **DSAG Investment Survey 2026: only 3% of SAP customers run SAP Business
  AI in production; 77% of AI-active enterprises use non-SAP tools.** Joule
  requires RISE/GROW contracts — on-premise excluded entirely. Min package
  100 AI Units ≈ €700/yr (€7/unit), overage 150–200% of contracted rate; no
  public price list; agentic deployments consume **3–20×** the AI Units of
  copilot projections (sources: innobu.com sap-joule-2026-agentic-enterprise-ai,
  2026-04; finoptory.ai/en/resources/sap-business-ai, 2026-05).
- SAPinsider (2026-05): SAP's own customer data — Joule adoption gated by
  enterprise readiness (clean core, data quality, standardization), not
  technology. SAP's Pfiester: clean-core customers "better positioned for
  AI." >90% of SAP projects delivered by SI partners (Jan Gilg). Joule
  positioned as SAP's "control point for business interaction."
- 40+ SAP agents, 2,400+ Joule skills, A2A protocol across 35 solutions
  shipped Q1 2026 (innobu). Supply-chain agents (Production Master Data,
  Material Reservation) GA Q2 2026 (source: news.sap.com Hannover Messe,
  2026-04). ECC 6.0 support ends 2027-12-31 → 10,000+ customers face
  migration decisions (innobu).

## Automotive proof points

- **JLR**: clean-core S/4HANA with extensibility pyramid governance
  (standard → green key-user → amber BAdIs → red core mods), Fiori-only
  policy, BTP + RAP sidecar apps; Halewood brownfield go-live with 120
  integrations, 200+ cars by day 3, targets met week 1 (sources:
  studiocelanie.com JLR clean-core article 2026-06; sapinsider.org JLR
  scaling 2026-03).
- **Martur Fompak** (automotive seating, SAP Sapphire 2026-05): Joule +
  embodied AI humanoid-robot intralogistics on S/4HANA + EWM; 400 daily
  line feeds, 100% SAP-driven decisions, 5× efficiency target (source:
  news.sap.com, vendor case study — Tier 3).
- **Autonomous SCM whitepaper** (news.sap.com, 2026-06): automotive
  electronics co. centralized ordering across ~30 plants, disruption
  response −95%; operators converge on human-in-the-loop governance and
  **progressive autonomy thresholds** — independent validation of the
  earned-autonomy thesis.
