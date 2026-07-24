# Storyboard Data Gap Audit

Run date: 2026-07-14

## Short Answer

We now have enough Level 2 evidence to support the core storyboard:

- Beacon should be positioned as implementation execution, not generic DAP.
- The competitor universe should be split by buyer job.
- KPI evidence should focus on implementation velocity, implementation productivity, quality, cost, adoption, support productivity, and AI productivity.
- The POC should benchmark Beacon against manual services and generic agents.

But we are still missing several datapoints required to make the storyboard fully client-ready and defensible.

Update after missing-datapoint search:
- See `missing-datapoints-search-results.md`.
- The source index now contains 455 Level 2 rows from 46 raw Level 2 files.
- DAP ROI, onboarding/project KPI, agentic platform threat, and consulting/SI AI value-realization evidence are materially stronger.
- Beacon trust/security is now supported by official Beacon pages and `trust.beacon.li`.
- Beacon-specific denominators, pricing/TCO, normalized competitor metrics, and distribution depth remain the main gaps.

## Missing Or Weak Datapoints By Storyboard Need

| Storyboard Need | Current Evidence | Missing Datapoint | Why It Matters |
|---|---|---|---|
| Executive answer: Beacon owns implementation execution | Strong Beacon-owned claims and Level 2 evidence | Independent customer/reference validation of Beacon's claims | Without third-party proof, Beacon's advantage remains vendor-claimed. |
| Market map: four arenas | Good arena evidence for DAP, onboarding/project delivery, workflow/iPaaS, consulting/SI | Market size / growth / budget ownership for each arena | Helps quantify where Beacon should compete and which budget it should attach to. |
| Scored heatmap | KPI taxonomy and qualitative competitor evidence | Normalized competitor-by-competitor metrics across the same dimensions | Needed for a rigorous competitor analysis rather than a narrative comparison. |
| Threat priority | Good DAP/onboarding/iPaaS/consulting source set | Primary evidence for Unframe, UiPath, ServiceNow, Salesforce, SAP/WalkMe, and Workato AI-agent roadmaps | These threats are in the deck but not equally evidenced by Level 2 data. |
| Beacon proof gap | Strong Beacon fintech case claim: 85% faster handovers, 60% fewer defects, 30% lower cost | Baseline values behind the percentages: original handoff time, defect count, implementation cost, sample size, customer type | Percent improvements are useful, but the reader will ask, "85% of what?" |
| POC benchmark | KPI scorecard created | Target thresholds for pass/fail: e.g., reduce go-live effort by X%, defects by Y%, support tickets by Z%, within N days | A POC without thresholds is not a decision instrument. |
| ROI model | Good productivity/cost metrics: hours, utilization, deflection, cost per resolution | Loaded labor cost assumptions by role: implementation consultant, solutions engineer, support agent, CSM, PM | Required to convert productivity gains into dollars. |
| Pricing / TCO | Official pricing pages found for GUIDEcx, Pendo, and WalkMe; most enterprise pricing remains quote-based or non-transparent | Official Beacon pricing and comparable enterprise TCO architecture for key competitors | Pricing confidence remains low; affects ROI and procurement framing. |
| Enterprise trust | Official trust/security evidence now found for Beacon, WalkMe, Whatfix, Pendo, Rocketlane, GUIDEcx, Workato, UiPath, MuleSoft, Boomi, Salesforce, and ServiceNow | Full audited reports or trust-center-gated evidence where needed; exact data-residency / deployment details by vendor | Enterprise buyers will use trust as a gating criterion; this is now mostly evidenced, not missing. |
| Support productivity | Good directional deflection/cost-per-resolution data | Beacon-specific support-ticket reduction, L1-L3 resolution, FCR, SLA, CSAT metrics | Beacon claims support impact but current proof is mostly generic benchmarks. |
| Adoption / TTV | Good onboarding/TTV benchmark taxonomy | Beacon-specific activation/TTV/post-launch adoption outcomes | Needed to connect implementation execution to adoption and retention. |
| Consulting/SI arena | Good secondary evidence for consulting AI investment and positioning | Primary pages from Accenture, Deloitte, BCG, McKinsey, IBM, Capgemini on AI implementation / agents / transformation | Consulting-force slides need primary citations before client-final use. |
| Buyer pain | Vendor pages and benchmark articles | Review/forum/customer-language evidence from G2, Gartner Peer Insights, Reddit, implementation leader posts | Helps make pain points feel market-grounded, not vendor-authored. |
| Vertical wedge | Beacon B2B fintech/BFSI evidence | Fintech/BFSI implementation benchmarks: ERP mapping, cash application, KYC, compliance workflow complexity, average rollout timelines | Needed to make the vertical wedge credible. |
| Distribution | Beacon partner page and consulting/SI data | Competitor ecosystem scale: SAP/WalkMe, SI partnerships, app marketplace, implementation partner network | Distribution strength is in the rubric but weakly evidenced. |

## Missing Datapoints To Prioritize Next

After the follow-up search, de-prioritize these as mostly addressed:

- DAP ROI proof for WalkMe, Whatfix, and Pendo.
- Rocketlane/GUIDEcx KPI language for implementation/onboarding operations.
- UiPath and Workato agentic automation threat evidence.
- Accenture/Deloitte/BCG/Gartner primary-source AI value-realization evidence.

Keep these as priority gaps:

1. **Beacon baseline denominators**
   - Original handoff duration behind "85% faster."
   - Original configuration defect rate/count behind "60% fewer defects."
   - Original implementation cost behind "30% lower cost."
   - Number/type of implementations included in the case.

2. **Competitor KPI matrix**
   - Still needed: normalized values in one matrix across all vendors.
   - Partially found: WalkMe / Whatfix / Pendo ROI and error/support claims; Rocketlane/GUIDEcx KPI language; Workato/UiPath agentic platform claims; Accenture/Deloitte/BCG/Gartner AI value evidence.
   - Still weak: Kantata, MuleSoft, Boomi, Salesforce, ServiceNow, SAP/WalkMe ecosystem, Unframe, IBM/Capgemini primary evidence.

3. **Official trust/security matrix**
   - Mostly addressed for the main named vendors.
   - New artifact: `official-trust-pricing-partner-matrix.md`.
   - Remaining work is validation depth, not discovery: audited report access, data-residency details, and deployment-model specifics where needed.

4. **POC pass/fail thresholds**
   - Time-to-configure.
   - Rework hours avoided.
   - Validation defects caught before go-live.
   - Support tickets deflected.
   - Implementation hours avoided.
   - Customer/admin time saved.

5. **TCO calculator inputs**
   - Loaded hourly cost by role.
   - Average implementation hours by customer segment.
   - Average number of implementation handoffs.
   - Average rework percentage.
   - Average support ticket volume during hypercare.
   - Cost per support resolution by channel.

6. **Primary-source verification**
   - Improved: Accenture, Deloitte, BCG, Gartner primary-source AI value-realization claims.
   - Still needed: McKinsey/IBM/Capgemini primary detail, original Forrester/IDC source documents for DAP ROI where accessible, and Beacon customer-proof denominators.

## Storyboard Impact

The current storyboard is viable, but the following slides should be marked
`directional` unless the missing datapoints are collected:

- Scored competitive heatmap.
- Threat-priority matrix.
- ROI / pricing / TCO slide.
- POC benchmark slide.
- Any slide using AI failure-rate benchmarks.

The slides that are already well supported:

- BLUF / positioning.
- Four-arena market map.
- Buyer-job matrix.
- Beacon proof-gap framing.
- Enterprise trust / security readiness matrix.
- KPI scorecard framework.
- POC-first recommendation.

## Recommended Next Search Pass

Run Level 2 searches for:

1. `site:walkme.com ROI error reduction IT workload Forrester digital adoption platform`
2. `site:whatfix.com ROI support ticket reduction digital adoption platform implementation time`
3. `site:pendo.io ROI adoption analytics implementation time digital adoption platform`
4. `site:rocketlane.com professional services utilization onboarding cycle time implementation margin`
5. `site:guidecx.com customer onboarding time to value implementation project metrics`
6. `site:uipath.com agentic automation enterprise workflow productivity implementation`
7. `site:workato.com AI agents workflow automation ROI implementation productivity`
8. `site:accenture.com AI implementation agents transformation data AI investment`
9. `site:deloitte.com generative AI implementation productivity enterprise transformation`
10. `site:bcg.com generative AI value realization implementation productivity`
