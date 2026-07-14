# Official Trust, Pricing, and Partner Evidence Matrix

Run date: 2026-07-14

Method:
- Skill: `you-com-search`
- Level: `--level 2`
- API behavior: You.com Search API with `live_crawl=true`
- Raw files: 12 `official-*-trust-pricing-partners-level2.json` files
- Extract: `official-trust-pricing-partner-extract.csv`
- Refreshed source index: `level2-source-index.csv` with 455 Level 2 rows from 46 raw files

## Executive Readout

The official-page pass materially improves the evidence base for the deck. The biggest correction is Beacon: public official pages now support an enterprise-trust claim, including SOC 2, RBAC, SSO, audit trails, no backend/API access, and a Sprinto-powered trust center. This means the prior "Beacon trust missing" gap should be closed, with the caveat that the deck should cite the exact public trust pages rather than imply audited report access.

Official pricing remains the weakest evidence area. Pendo, WalkMe, and GUIDEcx expose pricing pages, but enterprise pricing is still mostly quote-based or package-framed rather than transparent TCO. Beacon public pricing was not found. Use pricing only as a "procurement transparency" or "TCO evidence availability" dimension, not as a hard cost comparison.

Partner/ecosystem evidence is strongest for mature platform vendors and SAP-adjacent DAP: WalkMe, Salesforce, ServiceNow, MuleSoft, Boomi, Workato, and UiPath. Beacon has a public partner page, but the named ecosystem depth is still emerging compared with incumbents.

## Competitor Matrix

| Vendor | Trust / Security Evidence | Pricing / TCO Evidence | Partner / Ecosystem Evidence | Storyboard Impact |
|---|---|---|---|---|
| Beacon | Official pages state Beacon runs above the UI, does not access databases/APIs/sensitive data, and is SOC 2 compliant with RBAC, SSO, and audit trails. Trust center pages exist at `trust.beacon.li`, including compliance and controls pages. Some vertical pages also reference ISO/GDPR. | No public pricing found in the official pass. | Partner page says Beacon is building an ecosystem of consulting firms, SIs, and technology vendors. | Move Beacon trust from "gap" to "supported vendor claim / public trust center." Keep pricing as missing. Score ecosystem as emerging. |
| WalkMe | Official security page and agreements reference SOC 2, ISO 27001, GDPR, pen testing, customer data safeguards, and FedRAMP-related positioning. | Official pricing page exists, but transparent enterprise price bands were not found. | Strongest DAP ecosystem evidence: WalkMe claims largest trained partner/certified professional pool and SAP resources; older analyst PDF references SI/ISV partner depth. | Score high on enterprise trust and distribution. Use as the benchmark incumbent for ecosystem scale. |
| Whatfix | Official pages cite SOC 2, ISO 27001, GDPR, SSO, SCIM, RBAC, audit trails, data residency/security evaluation criteria, and a security framework policy. | No clear official transparent enterprise pricing surfaced. | Official R2E services partner program found. Use-case marketplace also supports breadth. | Strong trust evidence and partner motion; pricing remains low-transparency. |
| Pendo | Official support/trust/privacy pages cite annual SOC 2 Type II audit, GDPR, TX-RAMP, HIPAA, SAML/SSO, MFA, trust center, and AI security review resources. | Official pricing page exists but does not expose a simple enterprise TCO. | Strong integration/product ecosystem signal, but official partner depth was less direct than WalkMe/Salesforce-style ecosystems in this pass. | Score high on enterprise trust and product analytics maturity; medium on ecosystem for this storyboard unless further official partner evidence is added. |
| Rocketlane | Official pages cite SOC 1 Type 2, SOC 2 Type 2, CSA STAR Level One, ISO 27001, GDPR, SSO/SAML, audit logs, role-based permissions, and regional/security controls. | Pricing appears in Rocketlane's own comparison/blog content, but official package pricing needs separate validation before deck use. | Partner/customer portal and integrations appear in product content; broader SI ecosystem not strongly surfaced. | Strong for onboarding/PS trust. Treat as implementation operations competitor rather than distribution-heavy platform. |
| GUIDEcx | Official homepage/pricing/DPA/help pages cite SOC 2, data encryption, SSO, secure infrastructure, and Drata trust link. | Official pricing page exists with Starter, Premium, and Advanced package framing. | Official integrations page says GUIDEcx integrates with thousands of systems and references technology partnerships. | Useful for onboarding category comparison and pricing-transparency dimension. |
| Workato | Official platform/docs cite BYOK, hourly key rotation, container isolation, audit trails, SAML SSO/JIT, RBAC, security FAQs, and governance. | No simple public TCO found in this pass. | Strong integration ecosystem by product nature; platform and docs position Workato as enterprise orchestration across apps, APIs, and agents. | Score high as broad integration/orchestration threat; trust/gov evidence strengthens agentic-platform threat slide. |
| UiPath | Official trust/security and docs cite zero-trust architecture, auditing, compliance, governance, FedRAMP environment controls, data sovereignty, PII protection, and ISO/IEC 42001 AI management certification positioning. | No simple public enterprise TCO found in this pass. | Strong global partner and automation ecosystem; official trust page references partner code of conduct and enterprise-scale governance. | High enterprise-platform threat; use for secure agentic automation contrast. |
| MuleSoft | Official trust center cites ISO 27001, SOC 1, SOC 2, HIPAA, PCI DSS, encryption, identity management, and API security controls. | No simple public TCO found in this pass. | Strong Salesforce ecosystem adjacency and API/integration platform ecosystem. | High integration-platform threat for API-led enterprises; contrast against Beacon's no-API UI execution. |
| Boomi | Official compliance/security pages cite enterprise iPaaS security, RBAC, certifications/compliance, data security controls, API governance, and partner/customer trust framing. | No simple public TCO found in this pass. | Strong iPaaS/API ecosystem with developer portals, subscriptions, governance, and partner-facing API products. | High integration-platform threat where API-first automation is feasible. |
| Salesforce | Official trust/compliance documentation and compliance site evidence support mature enterprise trust, FedRAMP/Government Cloud, security architecture, and broad compliance documentation. | Pricing not relevant unless comparing Salesforce-native automation modules directly. | Very strong GSI/partner ecosystem; official partner ecosystem content highlights large-scale implementation and ROI support. | Use as ecosystem gravity proof, not direct Beacon feature competitor. |
| ServiceNow | Official trust/compliance center and TrustShare cite SOC 2 Type 2, FedRAMP, continuous compliance, and AI platform trust/security material. | Pricing not relevant unless comparing ServiceNow workflow/AI modules directly. | Very strong enterprise workflow ecosystem and platform partner motion. | Use as workflow-platform adjacency and enterprise governance benchmark. |

## Gaps Closed

- Beacon trust/security: public official evidence now exists.
- DAP trust/security: WalkMe, Whatfix, and Pendo are now well-supported by official pages.
- Onboarding/PS trust/security: Rocketlane and GUIDEcx are now well-supported by official pages.
- Enterprise platform trust/security: Workato, UiPath, MuleSoft, Boomi, Salesforce, and ServiceNow have strong official trust/compliance evidence.
- Partner/ecosystem evidence: WalkMe/SAP, Whatfix R2E, GUIDEcx integrations, and enterprise platform ecosystems are now better evidenced.

## Gaps Still Open

- Beacon public pricing/TCO.
- Beacon raw case denominators behind percentage claims.
- Transparent enterprise pricing for WalkMe, Whatfix, Pendo, Rocketlane, Workato, UiPath, MuleSoft, Boomi, Salesforce, and ServiceNow.
- Named partner depth for Beacon, Rocketlane, GUIDEcx, and Pendo beyond high-level official ecosystem/integration pages.
- Direct audited report access for some trust claims may require vendor trust-center login or NDA.

## Recommended Storyboard Updates

1. Add an "Enterprise Readiness" row to the competitor heatmap with three sub-signals: public trust center, named compliance certifications, and enterprise identity/governance controls.
2. Re-score Beacon's enterprise readiness upward: no backend/API access plus SOC 2/RBAC/SSO/audit trails is a meaningful differentiator for implementation automation.
3. Keep a separate "Commercial Transparency" row: GUIDEcx, Pendo, and WalkMe have official pricing pages, but public enterprise TCO remains limited.
4. Use partner ecosystem as a threat axis, not a generic advantage. WalkMe/SAP, Salesforce, ServiceNow, MuleSoft, Boomi, Workato, and UiPath should score high because their channels can shape enterprise buying even where Beacon has product differentiation.
5. Add a sourcing caveat on percentage benchmarks: Beacon and competitor ROI metrics are strong for narrative, but raw baselines are still not public.
