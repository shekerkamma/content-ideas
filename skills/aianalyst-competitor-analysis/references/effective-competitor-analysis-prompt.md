# Effective Competitor Analysis Prompt

Use this as the default operating prompt for AI Analyst competitor-analysis runs. Fill the bracketed placeholders with the target context, then save the completed version to `inputs/operating-prompt.yaml` before research begins.

This prompt is deliberately narrower than a launch report. It optimizes for a competitive decision, evidence quality, and artifact traceability.

The **copy-ready YAML prompt is the canonical prompt**. Any filled examples are illustrative only and must not be copied into a different company run.

## Copy-Ready YAML Prompt

```yaml
objective: >
  Build a decision-ready competitor analysis for <TARGET_COMPANY_OR_PRODUCT_NAME>
  that determines whether <TARGET_SHORT_NAME> can own <TARGET_STRATEGIC_POSITION>
  and how it should defend that position against direct competitors, adjacent
  tools, incumbent platforms, services-led substitutes, and internal-build
  alternatives.

core_question: >
  Is <TARGET_SHORT_NAME>'s wedge strong enough to own a distinct position, or will buyers
  compress it into known alternatives such as <KNOWN_CATEGORY_1>,
  <KNOWN_CATEGORY_2>, <KNOWN_CATEGORY_3>, consulting/SI delivery, or internal
  build?

audience:
  - "VC-backed founders"
  - "CFO / COO / GTM leaders"
  - "Product and strategy leaders"

decision_to_enable:
  - "Where should <TARGET_SHORT_NAME> compete, partner, attach, and avoid?"
  - "Which competitor arenas create the highest compression risk?"
  - "Which claims are evidence-backed enough for investor, sales, and product use?"
  - "What proof must be built next to increase confidence?"

target:
  name: "<TARGET_COMPANY_OR_PRODUCT_NAME>"
  url: "<TARGET_URL>"
  geography: "<GEOGRAPHY_OR_MARKET_SCOPE>"
  buyer_job: "<PRIMARY_BUYER_JOB>"
  suspected_wedge: "<ONE_SENTENCE_WEDGE>"

competitor_arenas:
  direct:
    buyer_job: "<same buyer job as target>"
    examples:
      - "<DIRECT_COMPETITOR_1>"
      - "<DIRECT_COMPETITOR_2>"
  adjacent:
    buyer_job: "<adjacent buyer job that can absorb budget>"
    examples:
      - "<ADJACENT_COMPETITOR_1>"
      - "<ADJACENT_COMPETITOR_2>"
  incumbent_platforms:
    buyer_job: "<enterprise platform / automation / system-of-record job>"
    examples:
      - "<INCUMBENT_1>"
      - "<INCUMBENT_2>"
  services_substitutes:
    buyer_job: "consulting, SI, agency, or managed-service delivery"
    examples:
      - "<SERVICES_SUBSTITUTE_1>"
      - "<SERVICES_SUBSTITUTE_2>"
      - "<SERVICES_SUBSTITUTE_3>"
  internal_build:
    buyer_job: "internal automation, ops, implementation, data, or engineering team"
    examples:
      - "internal scripts"
      - "workflow automation team"
      - "implementation ops team"

evidence_standard:
  source_order:
    - "GBrain / prior run recall"
    - "repo-local artifacts"
    - "You.com Level 2 livecrawl or equivalent full-page retrieval"
    - "official company pages, docs, trust centers, pricing pages, case studies"
    - "third-party analyst/review/funding databases with confidence caveats"
    - "generic web search only for targeted verification or fallback"
  freshness:
    default: "2023-current year where possible"
    volatile_facts: "verify current pricing, funding, leadership, product claims, customer proof, and certifications"
  claim_policy:
    - "Every visible claim in client artifacts must trace to evidence rows, defined metrics, scoring model, or labeled interpretation."
    - "Vendor-published claims must be labeled vendor-published unless independently verified."
    - "Do not invent pricing, TAM, ROI, ARR, growth, implementation cost, customer counts, or benchmark numbers."
    - "If a number is supported, plug it in with source/caveat; if unsupported, remove it or replace it with qualitative wording."

dataset_outputs:
  - "outputs/evidence-ledger.csv using the AI Analyst evidence schema"
  - "outputs/metric-definitions.md"
  - "outputs/data-quality-report.md"
  - "outputs/scoring-model.md"
  - "outputs/competitor-brief.md"
  - "outputs/story-architect-pack.md"
  - "outputs/artifact-traceability.md"

analysis_required:
  market_structure:
    - "Map competitors by buyer job and arena, not as one flat vendor list."
    - "Identify direct competitors, adjacent tools, incumbents, services substitutes, and internal build."
  scoring:
    - "Define all scoring dimensions before scoring."
    - "Score each competitor on the same rubric."
    - "Label confidence when source coverage is uneven."
  proof:
    - "Extract hard numbers, named customers, trust/compliance signals, integrations, funding, pricing, partner/distribution proof, deployment claims, and outcome claims."
    - "Separate primary, vendor-published, third-party, analyst, and low-confidence evidence."
  strategy:
    - "State where <TARGET_SHORT_NAME> wins."
    - "State where incumbents can compress the position."
    - "State what proof would change the recommendation."
    - "Provide compete / partner / attach / avoid guidance."

required_artifacts:
  report:
    format: "decision brief or structured report"
    must_include:
      - "executive answer"
      - "competitor arena map"
      - "evidence coverage and confidence"
      - "threat matrix or heatmap"
      - "proof gap analysis"
      - "positioning recommendation"
      - "proof plan"
      - "30/60/90-day roadmap"
  deck:
    tool_chain:
      - "Use Genspark AI Slides only as hosted generation/reference when requested or useful."
      - "Final client PPTX must be recreated through genspark-branded-deck hybrid-editable path or branded-pptx-deck native path."
    requirements:
      - "Final PPTX must be editable, not image-only."
      - "Visible numbers must trace to upstream AI Analyst dataset artifacts."
      - "Use assertion titles."
      - "No unsupported numbers."
  html:
    requirements:
      - "Build self-contained static HTML at client-package/site/index.html."
      - "Stage publish source at client-package/pages/<slug>/index.html."
      - "Publish with /publish-static-page or github-pages-publisher when a public URL is requested."

must_not_do:
  - "Do not write a generic market report."
  - "Do not let a launch-report outline drive the analysis unless a section directly affects competitive strategy."
  - "Do not organize only as one section per competitor."
  - "Do not bury evidence-led datapoints in an appendix."
  - "Do not treat vendor-published proof as independently validated."
  - "Do not ship image-only slides as final delivery."
  - "Do not repeatedly regenerate slides to fix evidence errors; clean deterministically after one correction/expansion pass."

quality_gates:
  - "Prompt-fit review completed."
  - "Evidence ledger created and data quality reported."
  - "Metrics defined before scoring."
  - "Story-architect pack completed before deck/HTML build."
  - "Artifact traceability maps every slide/HTML section to claim IDs, metrics, scores, or labeled interpretation."
  - "Allowed-number list and unsupported-number scan completed for slides and HTML."
  - "Editable PPTX QA passed with OfficeCLI or documented equivalent."
  - "Static HTML browser validation passed."
  - "GitHub Pages URL verified when published."

final_answer_should_decide:
  - "The category or position <TARGET_SHORT_NAME> should claim."
  - "The highest-risk competitor arenas."
  - "The proof gaps that block a stronger claim."
  - "The next actions for product, GTM, and proof-building."
```

## Placeholder Guide

| Placeholder | Fill With |
|---|---|
| `<TARGET_COMPANY_OR_PRODUCT_NAME>` | Full name of the company, product, or service being analyzed |
| `<TARGET_SHORT_NAME>` | Short label used in narrative and charts |
| `<TARGET_STRATEGIC_POSITION>` | The category, wedge, or market position the target wants to own |
| `<KNOWN_CATEGORY_1..3>` | Existing categories buyers may use to bucket the target |
| `<TARGET_URL>` | Official target website or product URL |
| `<GEOGRAPHY_OR_MARKET_SCOPE>` | Region, vertical, market, or buyer context |
| `<PRIMARY_BUYER_JOB>` | The buyer job the target solves |
| `<ONE_SENTENCE_WEDGE>` | Clear one-sentence differentiation hypothesis |
| `<DIRECT_COMPETITOR_*>` | Companies solving the same buyer job |
| `<ADJACENT_COMPETITOR_*>` | Adjacent tools that can absorb budget or attention |
| `<INCUMBENT_*>` | Large platforms, systems of record, or automation incumbents |
| `<SERVICES_SUBSTITUTE_*>` | Consulting firms, SIs, agencies, BPOs, managed-service providers, or other services-led substitutes |
| `<slug>` | URL-safe output path for static HTML publishing |

## Optional Filled Example

The example below shows how the placeholders can be filled for one company. Do not treat it as part of the generic prompt.

```yaml
objective: >
  Build a decision-ready competitor analysis for Beacon.li that determines
  whether Beacon can own AI implementation execution and how it should defend
  that position against DAPs, onboarding/implementation ops tools, enterprise
  automation platforms, consulting/SI delivery, and internal automation teams.

core_question: >
  Is Beacon's wedge strong enough to own "AI implementation execution," or will
  buyers compress it into known alternatives such as digital adoption platforms,
  customer onboarding tools, RPA/workflow automation, consulting/SI delivery, or
  internal build?

target:
  name: "Beacon.li"
  url: "https://www.beacon.li/"
  geography: "US / global B2B SaaS buyer context"
  buyer_job: "complete complex SaaS implementations faster with fewer defects"
  suspected_wedge: "AI agents that execute implementation work inside complex SaaS products without backend integration."

competitor_arenas:
  direct:
    buyer_job: "AI implementation execution"
    examples: ["Unframe", "implementation-specific AI agents", "internal AI build"]
  adjacent:
    buyer_job: "digital adoption and onboarding operations"
    examples: ["WalkMe/SAP", "Pendo", "Whatfix", "Rocketlane", "GuideCX"]
  incumbent_platforms:
    buyer_job: "workflow automation, integration, agentic platforms"
    examples: ["UiPath", "Workato", "ServiceNow", "Salesforce", "Boomi", "MuleSoft"]
  services_substitutes:
    buyer_job: "transformation and implementation delivery"
    examples: ["Accenture", "Deloitte", "BCG", "McKinsey", "IBM Consulting"]
  internal_build:
    buyer_job: "ops, implementation, support, and automation teams building scripts or agents"
    examples: ["internal automation team", "implementation ops team", "support engineering"]

final_answer_should_decide:
  - "Beacon should claim implementation execution, not adoption or generic AI automation."
  - "DAPs and automation incumbents create the highest compression risk."
  - "Beacon's vendor-published proof is useful but needs measured POC scorecards and customer-denominator validation."
  - "The next artifact should be a POC benchmark pack and battlecards, not a broad launch report."
```

## How To Save

When starting a run, write the filled version to:

```text
inputs/operating-prompt.yaml
```

If the user's original prompt was broad, also write:

```text
outputs/prompt-fit-review.md
```

State what was kept, what was demoted to QA checklist, and what was removed.
