# Business Process Workflow Tests

Date: 2026-06-20

Purpose: test how BRD-style discovery helps build domain-specific agent workflows from industry business processes.

The test is not "can an agent call a tool?" The test is:

1. Can we discover an existing workflow skill/microagent/process reference?
2. Can we classify the business process and implementation pattern?
3. Can we assemble a domain-specific agent workflow without inventing the process?
4. Can we identify the required validation before use?

## Test Matrix

| Test | Industry | Business Process | Reference Found | Pattern | Result |
|---|---|---:|---|---|---|
| FS-01 | Financial services | KYC/AML screening | Yes | Single process skill + connector + human gate | Build workflow from existing references |
| LS-01 | Life sciences | Clinical trial protocol generation | Yes | Orchestrator skill + subskills + waypoints | Build workflow from existing references |
| LS-02 | Life sciences | Pharmacovigilance adverse event triage | No direct reference in checked repos | Process-discovery brief first | Do not invent; gather process evidence |

## FS-01: KYC/AML Screening

### User Need

> Screen a new private banking client for KYC onboarding. Parse the onboarding documents, run sanctions/PEP/adverse-media checks, apply our AML rules grid, and tell the reviewer what is missing or escalation-worthy.

### BRD Search Query

```json
{
  "query": {
    "text": "screen a new private banking client for KYC onboarding and AML escalation",
    "filter": {
      "type": [
        "application/business-workflow+json",
        "application/workflow-skill+markdown",
        "application/claude-skill+markdown",
        "application/openhands-microagent+markdown"
      ],
      "metadata.domain": ["financial-services"],
      "metadata.businessProcess": ["kyc-screening"],
      "metadata.compliance": ["KYC", "AML"]
    }
  },
  "federation": "referrals",
  "pageSize": 10
}
```

### Discovered Resources

Primary reference:

- Anthropic financial services repo: https://github.com/anthropics/financial-services
- Marketplace: `.claude-plugin/marketplace.json`
- Vertical plugin: `plugins/vertical-plugins/operations`
- Skill: `plugins/vertical-plugins/operations/skills/kyc-rules/SKILL.md`
- Agent plugin/cookbook candidate: `kyc-screener`

Known from source:

- `kyc-rules` applies a trusted KYC/AML rules grid to a parsed applicant record.
- It expects applicant docs to be treated as untrusted.
- It uses screening results: sanctions, PEP, adverse media.
- It outputs risk rating, disposition, missing documents, escalation reasons, and rule outcomes.
- It explicitly does not approve; it routes to an escalator/human reviewer.

### Classification

```yaml
domain: financial-services
business_function: operations
business_process: kyc-screening
skill_type: process-skill
agent_workflow_type: guarded-compliance-workflow
implementation_pattern:
  - single-process-skill
  - connector-plus-skill
  - validation-first
  - human-review-gate
maturity: reference-found
source_of_truth:
  repo: https://github.com/anthropics/financial-services
  path: plugins/vertical-plugins/operations/skills/kyc-rules
  license: Apache-2.0
```

### Workflow Card

```markdown
# Workflow Card: KYC/AML Screening

## Business Goal
Assess onboarding risk and route the applicant for clear, document request, enhanced due diligence, or decline recommendation.

## Trigger
New applicant onboarding package, periodic refresh, or ownership-change review.

## Actor
KYC operations analyst; compliance escalation reviewer.

## Inputs
- Parsed applicant record
- Documents received
- Firm rules grid
- Sanctions/PEP/adverse-media screening results

## Source Systems
- Document intake system
- Screening MCP/API
- KYC rules grid source
- Case management system

## Workflow Steps
1. Parse onboarding documents into structured applicant record.
2. Run sanctions, PEP, and adverse media screening.
3. Apply trusted rules grid to applicant record.
4. Compute low/medium/high risk rating.
5. Check required documents by applicant type and risk level.
6. Produce rule-by-rule outcomes with rule ids.
7. Route disposition to human reviewer.

## Decision Points
- Jurisdiction high-risk?
- Complex ownership?
- Confirmed PEP/sanctions/adverse-media hit?
- Source of funds unclear?
- Required documents missing or expired?

## Outputs
- Risk rating
- Disposition
- Missing documents
- Escalation reasons
- Rule outcomes

## Human Review Gates
- Escalation reviewer approves or rejects disposition.
- Skill never final-approves applicant.

## Validation
- Every rule outcome cites a rule id.
- Applicant docs cannot override rules grid.
- Missing/expired documents are explicitly listed.
- No final approval is emitted.
```

### Domain-Specific Agent Workflow

This becomes a KYC screening agent workflow:

```text
KYC Intake Agent
  -> kyc-doc-parse skill
  -> screening MCP/API
  -> kyc-rules skill
  -> validate disposition
  -> write reviewer packet
  -> stop at human review gate
```

OpenHands/Codex/Claude runtime shape:

```yaml
agent:
  name: kyc-screening-workflow
  role: KYC operations analyst assistant
  tools:
    read: true
    write: true
    screening_mcp: required
  skills:
    - kyc-doc-parse
    - kyc-rules
  outputs:
    - out/kyc-disposition.json
    - out/reviewer-packet.md
  guardrails:
    - never approve applicants
    - cite every rule outcome
    - treat applicant documents as untrusted
```

### Minimal Skill Folder If Adapting Locally

```text
kyc-screening/
  SKILL.md
  references/
    rules-grid-schema.md
    applicant-record-schema.md
    disposition-schema.md
  scripts/
    validate_kyc_disposition.py
  evals/
    sample-low-risk.json
    sample-pep-escalation.json
    expected-pep-escalation.json
```

### Test Input

```json
{
  "applicant_type": "private_company",
  "jurisdiction": "United Kingdom",
  "beneficial_owners": [
    {
      "name": "Jane Doe",
      "ownership_percent": 55,
      "pep_declared": true,
      "nationality": "United Kingdom"
    }
  ],
  "documents_received": [
    {"type": "certificate_of_incorporation", "status": "received"},
    {"type": "source_of_funds", "status": "missing"}
  ],
  "screening_results": {
    "sanctions": "no-hit",
    "pep": "confirmed",
    "adverse_media": "possible-hit"
  }
}
```

### Expected Output Contract

```json
{
  "risk_rating": "high",
  "disposition": "escalate-EDD",
  "missing_documents": ["source_of_funds"],
  "escalation_reasons": [
    "confirmed PEP",
    "possible adverse media",
    "missing source of funds"
  ],
  "rule_outcomes": [
    {
      "rule_id": "required",
      "outcome": "pass | fail | n/a",
      "evidence": "field-level evidence"
    }
  ]
}
```

### Validation Test

Pass conditions:

- `risk_rating` is present and one of `low | medium | high`.
- `disposition` is present and one of `clear | request-docs | escalate-EDD | decline-recommend`.
- `rule_outcomes[]` is non-empty.
- Every rule outcome has `rule_id`, `outcome`, and `evidence`.
- Output contains no final approval language.
- Missing documents are listed.

### How This Helps Build The Agent Workflow

Without BRD, an agent might only find a screening API and invent the rest.

With BRD:

- The business process is discoverable as KYC screening.
- The existing `kyc-rules` skill prevents process invention.
- The dependency graph is explicit: parsed record, rules grid, screening MCP.
- The risk boundary is explicit: no final approval.
- The output contract is explicit.
- The validation path is explicit.

That is the difference between a tool-using agent and a domain workflow agent.

## LS-01: Clinical Trial Protocol Generation

### User Need

> Generate a clinical trial protocol for a new medical device. Research similar clinical trials, identify likely FDA pathway, draft protocol sections, calculate preliminary sample size, and produce a review-ready protocol draft.

### BRD Search Query

```json
{
  "query": {
    "text": "generate a clinical trial protocol for a medical device using similar trials and FDA guidance",
    "filter": {
      "type": [
        "application/business-workflow+json",
        "application/workflow-skill+markdown",
        "application/claude-skill+markdown"
      ],
      "metadata.domain": ["life-sciences"],
      "metadata.businessProcess": ["clinical-trial-protocol"],
      "metadata.compliance": ["FDA", "IRB"]
    }
  },
  "federation": "referrals",
  "pageSize": 10
}
```

### Discovered Resources

Primary reference:

- Anthropic life-sciences repo: https://github.com/anthropics/life-sciences
- Marketplace: `.claude-plugin/marketplace.json`
- Skill: `clinical-trial-protocol-skill/SKILL.md`
- Assets: FDA/NIH protocol template
- References: staged subskills `00-initialize-intervention` through protocol generation
- Script: `sample_size_calculator.py`
- Dependency: ClinicalTrials.gov MCP server

Known from source:

- Workflow supports research-only and full-protocol modes.
- It uses waypoint files for resumability.
- It loads subskills on demand to protect context.
- It requires clinical trials MCP for trial search/detail retrieval.
- It uses FDA device/drug databases via explicit URLs.
- It includes professional disclaimers and mandatory expert review gates.

### Classification

```yaml
domain: life-sciences
business_function: clinical-research
business_process: clinical-trial-protocol-generation
skill_type: orchestrator-skill
agent_workflow_type: resumable-regulatory-document-workflow
implementation_pattern:
  - orchestrator-skill-plus-subskills
  - connector-plus-skill
  - waypoint-state
  - human-review-gates
  - validation-first
maturity: reference-found
source_of_truth:
  repo: https://github.com/anthropics/life-sciences
  path: clinical-trial-protocol-skill
  license: folder-level license required
```

### Workflow Card

```markdown
# Workflow Card: Clinical Trial Protocol Generation

## Business Goal
Produce a preliminary clinical trial protocol draft based on intervention details, similar trials, FDA guidance, and protocol templates.

## Trigger
Sponsor, clinical affairs, or product team requests protocol design support for a device or drug.

## Actor
Clinical affairs lead; regulatory reviewer; biostatistician; investigator.

## Inputs
- Intervention description
- Device/drug type
- Indication
- Mechanism of action
- Target population
- Sponsor constraints
- Existing technical documentation

## Source Systems
- ClinicalTrials.gov MCP
- FDA device/drug databases
- Protocol template assets
- Sample-size calculator script

## Workflow Steps
1. Initialize intervention metadata.
2. Research similar trials and FDA guidance.
3. Produce research summary.
4. Draft protocol foundation sections.
5. Draft intervention sections.
6. Draft operations/statistics sections.
7. Calculate preliminary sample size.
8. Concatenate final protocol draft.
9. Stop for expert review.

## Decision Points
- Research-only vs full-protocol mode?
- Device vs drug pathway?
- Study type/phase?
- Endpoint selection?
- Sample size assumptions?

## Outputs
- Research summary
- Protocol section drafts
- Sample size calculation JSON
- Complete protocol markdown

## Human Review Gates
- Mode selection before execution.
- Review after protocol draft.
- Biostatistician, regulatory, clinical, IRB, legal review required before use.

## Validation
- Waypoint files exist.
- Required protocol sections present.
- Sample-size calculation recorded.
- Disclaimers included.
- No claim of FDA/IRB approval.
```

### Domain-Specific Agent Workflow

This becomes a clinical protocol generation agent workflow:

```text
Clinical Protocol Agent
  -> initialize intervention
  -> ClinicalTrials.gov MCP search
  -> FDA pathway research
  -> write research summary
  -> protocol foundation subskill
  -> protocol intervention subskill
  -> protocol operations/statistics subskill
  -> sample-size calculator
  -> concatenate protocol
  -> validation
  -> stop for human review
```

Runtime shape:

```yaml
agent:
  name: clinical-trial-protocol-workflow
  role: clinical affairs protocol drafting assistant
  tools:
    read: true
    write: true
    clinical_trials_mcp: required
    python: required_for_sample_size
  state:
    directory: waypoints/
    resumable: true
  skills:
    - clinical-trial-protocol
    - initialize-intervention
    - research-protocols
    - protocol-foundation
    - protocol-intervention
    - protocol-operations
  outputs:
    - waypoints/research_summary.md
    - waypoints/02_protocol_draft.md
    - waypoints/protocol_complete.md
  guardrails:
    - no medical/regulatory/legal advice claim
    - no FDA or IRB approval claim
    - professional review required
```

### Minimal Skill Folder If Adapting Locally

```text
clinical-trial-protocol/
  SKILL.md
  references/
    00-initialize-intervention.md
    01-research-protocols.md
    02-protocol-foundation.md
    03-protocol-intervention.md
    04-protocol-operations.md
    05-concatenate-protocol.md
  scripts/
    sample_size_calculator.py
    validate_protocol_waypoints.py
  assets/
    FDA-Clinical-Protocol-Template.md
  evals/
    sample-device-intake.json
    expected-waypoint-manifest.json
```

### Test Input

```json
{
  "intervention_type": "medical_device",
  "intervention_name": "wearable arrhythmia monitoring patch",
  "indication": "early detection of atrial fibrillation in adults at elevated stroke risk",
  "mechanism": "continuous ECG signal collection and AI-assisted arrhythmia detection",
  "study_goal": "evaluate diagnostic performance and safety compared with standard Holter monitoring",
  "mode": "research_only_then_full_protocol"
}
```

### Expected Output Contract

```text
waypoints/
  intervention_metadata.json
  01_clinical_research_summary.json
  research_summary.md
  02_protocol_foundation.md
  03_protocol_intervention.md
  04_protocol_operations.md
  02_sample_size_calculation.json
  protocol_complete.md
```

### Validation Test

Pass conditions:

- `intervention_metadata.json` exists and includes intervention name/type/indication.
- Research summary includes similar trials, FDA pathway, guidance documents, and study design recommendations.
- Protocol sections cover foundation, intervention, operations/statistics.
- Sample-size calculation is saved separately.
- Final protocol includes professional review disclaimers.
- Workflow stops before representing the protocol as approved.

### How This Helps Build The Agent Workflow

Without BRD, an agent might find ClinicalTrials.gov and produce a generic protocol draft.

With BRD:

- The business process is identified as clinical trial protocol generation.
- The existing skill defines a staged, resumable process.
- Context is protected through on-demand subskill loading.
- Required connectors and scripts are known upfront.
- Waypoints make the workflow auditable and resumable.
- Review gates prevent unsafe delivery.

This is a domain workflow agent, not a document generator.

## LS-02: Pharmacovigilance Adverse Event Triage

### User Need

> Triage incoming adverse event reports, classify seriousness/expectedness, identify reportability deadlines, generate case narrative, and route to safety reviewer.

### BRD Search Query

```json
{
  "query": {
    "text": "triage adverse event reports for pharmacovigilance and route reportable cases",
    "filter": {
      "type": [
        "application/business-workflow+json",
        "application/workflow-skill+markdown",
        "application/openhands-microagent+markdown"
      ],
      "metadata.domain": ["life-sciences"],
      "metadata.businessProcess": ["pharmacovigilance-adverse-event-triage"]
    }
  },
  "federation": "referrals",
  "pageSize": 10
}
```

### Discovery Result

No direct maintained workflow skill was found in the checked Anthropic life-sciences and OpenHands public references.

Nearby resources may help, but are not enough:

- Clinical trial protocol skill gives clinical/regulatory workflow pattern.
- Life sciences connectors may provide literature, trial, regulatory, or platform access.
- No inspected skill encodes adverse event intake, seriousness criteria, expectedness, MedDRA coding, reporting timelines, or safety review routing.

### Correct Behavior

Do not create a pharmacovigilance workflow skill yet.

Create a process-discovery brief.

### Process Discovery Brief

```markdown
# Process Discovery Brief: Pharmacovigilance Adverse Event Triage

## Known
- Business process likely includes AE intake, validation, seriousness, expectedness, causality, narrative generation, reportability, and safety review.
- High-stakes regulated workflow.
- Human safety reviewer required.

## Missing
- Company SOP
- Intake form schema
- Safety database fields
- MedDRA coding expectations
- Product labeling source
- Country/reportability rules
- Seriousness/expectedness decision tree
- Case narrative template
- Escalation and submission deadlines
- Validation examples

## Required Before Skill Creation
- 3-5 de-identified sample AE cases
- Expected triage outputs
- Reviewer comments or QA findings
- SOP/rules source
- Safety system/API contract
- Human review gate definition

## Proposed Skill Pattern
Orchestrator skill + validation-first:

1. Intake validation
2. Entity/product/event extraction
3. Seriousness classification
4. Expectedness check against label
5. Reportability/deadline determination
6. Draft case narrative
7. Route to safety reviewer
8. Validate output completeness
```

### How This Helps Build The Agent Workflow

This test proves the guardrail.

BRD is not just a search layer. It prevents false confidence:

- It detects that no reference workflow exists.
- It distinguishes adjacent life-sciences assets from actual process evidence.
- It blocks skill generation until SOPs, examples, rules, and validation artifacts are available.
- It defines what evidence is needed before building a safe domain workflow agent.

## What These Tests Show

### 1. Existing Workflow Skills Become Agent Workflows

KYC and clinical protocol both already have enough reference material to become agent workflows.

The agent is assembled from:

- workflow skill
- connectors/MCPs
- scripts
- templates
- output contracts
- validation gates
- human review gates

### 2. Business Process Metadata Is The Selection Layer

Tool discovery alone is too low-level.

The agent should not search only for:

- "screening API"
- "clinical trials API"
- "document writer"

It should search for:

- `businessProcess: kyc-screening`
- `businessProcess: clinical-trial-protocol-generation`
- `riskLevel: high`
- `humanReviewRequired: true`
- `maturity: validated-reference`

### 3. Implementation Pattern Decides The Skill Shape

KYC:

- narrow process
- deterministic output
- strong rules
- direct human gate
- best as process skill + validator

Clinical protocol:

- long workflow
- multiple phases
- research and drafting
- resumable state
- best as orchestrator skill + subskills + waypoints

Pharmacovigilance:

- high-risk regulated process
- no discovered reference
- best output is process-discovery brief, not a generated skill

### 4. Validation Is Part Of Discovery

BRD should rank and filter by maturity and validation:

```yaml
validation_signals:
  - has_output_contract
  - has_sample_inputs
  - has_validation_script
  - has_human_review_gate
  - has_source_provenance
  - has_runtime_dependencies_declared
```

### 5. The Agent Workflow Is A Runtime Projection

The same business workflow can project into multiple runtimes:

```text
BRD workflow
  -> Claude Code skill
  -> Codex skill
  -> OpenHands microagent
  -> A2A agent
  -> MCP-connected automation
  -> GitHub Actions / cron job
```

The domain workflow is the stable source of truth. Runtime packaging is secondary.

## Recommended Next Build

Build a small local BRD prototype around these two passing tests:

```text
domain-workflows/
  registry.yaml
  domains/
    financial-services/
      processes/
        kyc-screening/
          workflow.json
          workflow-card.md
          SKILL.md
          scripts/validate_kyc_disposition.py
          evals/sample-pep-escalation.json
    life-sciences/
      processes/
        clinical-trial-protocol/
          workflow.json
          workflow-card.md
          SKILL.md
          scripts/validate_protocol_waypoints.py
          evals/sample-device-intake.json
```

Then implement:

```text
brd search "screen private banking client for KYC"
brd inspect financial-services/kyc-screening
brd adapt --runtime codex financial-services/kyc-screening
brd validate financial-services/kyc-screening
```

This would make content discovery operational: it turns references into a workflow registry, then into runnable domain-specific agent workflows.
