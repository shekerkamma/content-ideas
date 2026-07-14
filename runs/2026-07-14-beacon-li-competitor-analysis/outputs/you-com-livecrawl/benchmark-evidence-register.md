# Benchmark Evidence Register

Run date: 2026-07-14

Method:
- Skill: `you-com-search`
- Level: `--level 2`
- API behavior: You.com Search API with `live_crawl=true`
- Raw benchmark files:
  - `benchmarks-implementation-level2.json`
  - `benchmarks-dap-roi-level2.json`
  - `benchmarks-onboarding-level2.json`
  - `benchmarks-ai-implementation-level2.json`
- Source index: `level2-source-index.csv` now contains 100 Level 2 rows.

## Deck-Usable Benchmark Datapoints

These are usable with source/confidence caveats. Prefer primary/vendor pages for
competitor claims and analyst/consulting sources for market-level claims.

| Benchmark / Datapoint | Source | Source Type | Confidence | How To Use In Analysis |
|---|---|---|---|---|
| Beacon claims 60%+ reduction in implementation effort/timelines. | `https://www.beacon.li/` | Vendor primary | Medium | Anchor Beacon's promised value; verify in POC/customer references. |
| Beacon claims 7-day product proof / proof-of-value. | `https://www.beacon.li/` and `https://www.beacon.li/partners` | Vendor primary | Medium | Supports POC-first recommendation and sales motion. |
| Beacon claims a leading fintech achieved 85% faster handovers, 60% fewer configuration defects, and 30% lower implementation costs. | `https://www.beacon.li/customers` | Vendor primary case claim | Medium | Strongest Beacon quantitative proof point; use prominently but label as Beacon-provided case evidence. |
| WalkMe claims it reduces IT workload by 50% and delivers 85% ROI in its comparison against Pendo and Whatfix. | `https://www.walkme.com/walkme-vs-pendo-vs-whatfix/` | Vendor primary competitive page | Medium | DAP benchmark for ROI/automation claims; compare against Beacon's implementation metrics. |
| WalkMe claims 87% fewer errors and a 5.00/5.00 Forrester automation rating in its DAP comparison. | `https://www.walkme.com/walkme-vs-pendo-vs-whatfix/` | Vendor primary competitive page | Medium-Low | Useful for DAP benchmark, but should be verified against Forrester before client-final use. |
| Apty claims average 3.4x ROI in the first year based on its customer data. | `https://www.fullstory.com/blog/walkme-alternatives/` | Secondary competitor roundup citing vendor claim | Low-Medium | Directional DAP ROI benchmark; verify at source if used in slides. |
| Guideflow reports DAP implementation timelines can range from days for lighter tools to months for WalkMe/Whatfix-style enterprise deployments. | `https://www.guideflow.com/blog/best-digital-adoption-platforms` | Secondary/listicle | Low-Medium | Supports complexity/timeline axis for DAP competitors. |
| DigitalApplied reports average user activation of 37.5% across 62 B2B SaaS companies, implying roughly two-thirds of new signups never reach core value. | `https://www.digitalapplied.com/blog/customer-onboarding-time-to-value-2026-saas-metrics-framework` | Secondary benchmark article | Low-Medium | Useful as onboarding/TTV context; verify cited benchmark before final deck. |
| DigitalApplied cites Amplitude's 2025 Product Benchmark Report: more than 98% of new users churn within two weeks if they have not reached a real value milestone. | `https://www.digitalapplied.com/blog/customer-onboarding-time-to-value-2026-saas-metrics-framework` | Secondary citing analyst/product benchmark | Low-Medium | Strong TTV urgency point; verify directly with Amplitude before final. |
| Monetizely says users who complete onboarding show 3x higher CLV, 5x higher likelihood to remain after first 90 days, and 30% higher likelihood to buy additional services. | `https://www.getmonetizely.com/articles/how-to-measure-onboarding-completion-rates-a-strategic-guide-for-saas-executives` | Secondary/blog | Low | Directional onboarding ROI; do not use as primary proof without verification. |
| DesignRevision says strong activation is 40-60%, onboarding flows should take 5-15 minutes, first value should happen in 2-5 minutes, and flows longer than 20 steps can drop completion by 30-50%. | `https://designrevision.com/blog/saas-onboarding-best-practices` | Secondary/blog | Low | Useful for UX onboarding benchmark, less relevant to enterprise implementation unless framed carefully. |
| SaaSFactor says 70% of SaaS customers who churn do so within 90 days due to poor onboarding and claims 3+ feature users have 70% higher retention at 12 months. | `https://www.saasfactor.co/blogs/the-science-of-saas-onboarding-a-comprehensive-framework-for-reducing-friction-improving-activation-and-preventing-churn` | Secondary/blog citing external research | Low | Directional onboarding-risk argument; verify before client-final use. |
| Exec.com says top-performing SaaS companies hit 85% satisfaction rates in onboarding and smart enterprise SaaS companies capture 15% of first-year contract value in the first month. | `https://www.exec.com/learn/customer-onboarding-metrics` | Secondary/blog | Low | Useful for metric menu, not hard benchmark unless verified. |
| CFO Pro Analytics gives an implementation capacity example: enterprise customers at 100 hours each and mid-market customers at 25 hours each. | `https://cfoproanalytics.com/cfo-wiki/saas/designing-a-saas-implementation-cost-model/` | Finance model / secondary | Low-Medium | Useful for building implementation-cost model assumptions. |
| Storylane says a mid-career SE costs $120K-$175K+ base salary and takes 3-6 months to become fully productive. | `https://www.storylane.io/blog/saas-implementation-checklist` | Secondary/blog | Low-Medium | Useful to quantify resource bottleneck behind implementation automation. |
| BCG/McKinsey/RAND/Gartner/MIT-style secondary synthesis reports enterprise AI implementation failure rates of 70-85%, 60% no material value, and only 5% substantial value at scale. | `https://talyx.ai/insights/enterprise-ai-implementation-failure` | Secondary synthesis | Low until primary verified | Useful for "POC is non-negotiable" argument, but needs primary-source verification. |
| AI Assembly Lines cites 80% of enterprise AI pilots never reaching production scale, 60% of companies not realizing measurable AI value, and Gartner survey claims only 28% of AI use cases meet ROI expectations. | `https://aiassemblylines.com/post/why-ai-pilots-fail-to-scale` | Secondary synthesis | Low until primary verified | Useful as supporting context for implementation risk; verify before deck. |
| Consulting Huber says Accenture has a headline $3B AI commitment, approximately 77,000 AI professionals, and AI Refinery as a branded platform. | `https://consulting-huber.com/ai-consulting-frameworks-compared.html` | Secondary consulting benchmark | Low-Medium | Supports consulting/SI competitive-force slide; verify with Accenture primary page. |
| Virtasant says Accenture committed $3B to Data & AI and planned to double AI workforce to 80,000 specialists; also cites McKinsey/QuantumBlack, BCG X, and Bain/OpenAI-style AI moves. | `https://www.virtasant.com/ai-today/big-five-consulting-betting-billions-on-ai-partnerships` | Secondary consulting analysis | Low-Medium | Supports the "consulting firms are shaping the category" thesis. |
| Whitehat reports Deloitte $3B AI investment through 2030, Accenture $3.6B AI bookings in FY2025, and McKinsey Lilli usage across 72% of 45,000 employees. | `https://whitehat-seo.co.uk/blog/ai-impact-on-consulting` | Secondary consulting analysis | Low-Medium | Useful for consulting-force proof, but should be primary-verified. |

## Benchmark Themes For Slides

1. **Implementation effort and timeline compression**
   - Beacon's own claim: 60%+ lower implementation effort/timeline.
   - Beacon case claim: 85% faster handovers, 60% fewer config defects, 30% lower implementation costs.
   - Supporting model: implementation cost depends on hours, team composition, scope, and feature complexity.

2. **DAP / adoption ROI**
   - WalkMe claims 50% IT workload reduction, 85% ROI, and 87% fewer errors.
   - Apty claims 3.4x first-year ROI.
   - DAP timelines range from days for lightweight tools to months for enterprise deployments.

3. **Onboarding and time-to-value**
   - Activation/TTV benchmarks consistently show onboarding is an early churn inflection point.
   - Useful candidate metrics: activation rate, time to first value, onboarding completion rate, onboarding cycle time, 7-day retention, first 90-day retention.

4. **Enterprise AI value realization**
   - Secondary sources repeatedly cite high AI pilot failure / no-value rates.
   - Use this to justify Beacon's POC-first proof plan, not as a final benchmark until primary sources are verified.

5. **Consulting/SI pressure**
   - Major consultancies are investing billions and staffing large AI practices.
   - This strengthens the slide thesis that consulting firms and SIs are not just channels; they define buyer expectations and compete for implementation budget.

## Deck Guidance

- Treat Beacon, WalkMe, and other vendor-owned metrics as claims, not independent proof.
- Use Level 2 benchmark data to enrich scoring and storyline, but mark weak sources as `directional`.
- For final client deck, primary-verify high-impact numbers from:
  - Beacon customer proof
  - WalkMe/Forrester ROI claims
  - BCG/McKinsey/Gartner/RAND/MIT AI failure/value-realization claims
  - Accenture/Deloitte/BCG/McKinsey AI investment and workforce claims
