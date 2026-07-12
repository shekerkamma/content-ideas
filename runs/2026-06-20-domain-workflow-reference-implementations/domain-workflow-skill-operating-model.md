# Domain Workflow Skill Operating Model

Date: 2026-06-20

## Core Thesis

The core asset is not an agent. The core asset is a domain workflow skill library.

A domain workflow skill library captures how a business process actually works:

- what triggers the process
- what inputs are required
- which systems and tools are used
- which rules and decisions matter
- what artifacts are produced
- where humans must approve or review
- how quality is validated
- what memory/context should be reused next time

Agents, MCP servers, CLIs, automations, and managed runtimes are execution layers. They become useful only after the workflow skill exists.

## Layer Model

### 1. Discovery Layer

Purpose: discover available skills, workflows, examples, tools, and source evidence.

Sources:

- Existing skills: `SKILL.md`, OpenHands microagents, Claude skills, Codex skills.
- Repo context: `AGENTS.md`, `CLAUDE.md`, `.openhands/microagents/`, `.openhands/skills/`, `.claude/skills/`, `skills/`.
- Public reference repos: Anthropic vertical marketplaces, OpenHands extensions, official SDK examples.
- Business artifacts: SOPs, checklists, templates, tickets, runbooks, spreadsheets, decks, forms, reports.
- Tooling evidence: MCP manifests, CLI docs, API docs, scripts, CI checks.
- Operator proof: actual outputs, examples, audits, review comments, failure logs.

Output:

- `source-inventory.md`
- `skill-gap-map.md`
- `candidate-skill-registry.yaml`

### 2. Context Layer

Purpose: model the business process before writing a skill.

For each business process, capture:

- Process name
- Business owner/persona
- Trigger event
- Inputs
- Source systems
- Step sequence
- Decision points
- Domain rules
- Compliance/safety constraints
- Human review gates
- Outputs/artifacts
- Success metrics
- Failure modes
- Reusable examples

Output:

- `workflow-card.md`
- `process-map.md`
- `input-output-contract.md`

### 3. Knowledge Layer

Purpose: preserve reusable domain knowledge separately from procedural instructions.

Examples:

- regulatory rules
- scoring rubrics
- schemas
- data dictionaries
- formulas
- document templates
- benchmark ranges
- source hierarchy
- glossary
- examples of good/bad outputs

Store as:

- `references/rules.md`
- `references/schema.md`
- `references/source-hierarchy.md`
- `references/examples.md`
- `assets/templates/`

Keep `SKILL.md` lean. Put dense domain context in references.

### 4. Workflow Skill Layer

Purpose: encode the executable business process.

A process skill should specify:

- Trigger phrases in frontmatter description
- Scope and non-scope
- Required inputs
- Tool/MCP requirements
- Step-by-step workflow
- Which references to load and when
- Which scripts to run
- Decision gates
- Human review gates
- Output contract
- Validation checklist
- Failure handling
- Provenance/citation rules

### 5. Execution Layer

Purpose: make repeatable parts deterministic.

Use scripts when:

- the same transformation is repeated
- validation must be reliable
- file formats are fragile
- calculations must be exact
- outputs need schema validation

Use MCP/CLI/API tools when:

- external systems are source of truth
- auth and permissions matter
- data must be current
- tool calls need auditability

### 6. Validation Layer

Purpose: prevent the skill from becoming vague process prose.

Each workflow skill should have at least one validation path:

- static validation of manifests/frontmatter
- input schema check
- output schema check
- smoke test with sample data
- domain sanity checks
- citation/source checks
- artifact QA
- human-review checklist

Examples:

- DCF: recalculate formulas and scan for Excel errors.
- KYC: every rule outcome must cite a rule id.
- Clinical protocol: waypoint files must exist and contain required sections.
- Nextflow: test profile must pass before full run.
- Decks: overflow/overlap QA before delivery.

### 7. Registry Layer

Purpose: make skills discoverable, comparable, and maintainable.

Use a registry rather than ad hoc folders.

Suggested schema:

```yaml
skills:
  - id: financial-services.kyc-rules
    domain: financial-services
    business_process: kyc-screening
    type: process-skill
    status: reference-found
    maturity: validated-reference
    source:
      repo: https://github.com/anthropics/financial-services
      path: plugins/vertical-plugins/operations/skills/kyc-rules
      license: Apache-2.0
      checked_at: 2026-06-20
    triggers:
      - kyc screening
      - apply aml rules
      - onboarding document review
    inputs:
      - parsed applicant record
      - rules grid
      - sanctions/pep/adverse media screening result
    outputs:
      - risk rating
      - disposition
      - missing documents
      - rule outcomes
    dependencies:
      mcp:
        - screening
      references:
        - rules grid
    validation:
      - every outcome cites a rule id
      - skill never final-approves
      - escalation goes to human reviewer
    runtime_targets:
      - claude-code
      - codex
      - openhands
```

## If A Workflow Skill Already Exists

Do not rewrite it first.

Process:

1. Verify source:
   - repository URL
   - license
   - last push/update
   - owner
   - issue/activity state
   - validation scripts or CI
2. Classify it:
   - vertical skill
   - process skill
   - task subskill
   - connector skill
   - validation/eval skill
   - orchestrator/agent
3. Extract dependency graph:
   - required MCP servers
   - API keys/env vars
   - scripts
   - references
   - assets/templates
   - expected input/output files
4. Normalize metadata into the registry.
5. Adapt only the runtime wrapper:
   - trigger description
   - host-specific tool mappings
   - local paths
   - env var names
   - artifact destinations
   - validation commands
6. Preserve provenance:
   - copied from / adapted from
   - source commit/date
   - license
   - deviations from source
7. Run the original validation path if available.

## If A Workflow Skill Does Not Exist

Do not start by writing `SKILL.md`.

Start with business-process discovery.

### Step 1: Build The Workflow Card

Create a one-page `workflow-card.md`:

```markdown
# Workflow Card: [Business Process]

## Business Goal
[What the business process accomplishes]

## Trigger
[What event/request starts this workflow]

## Actor
[Who performs/reviews/owns the workflow]

## Inputs
[Documents, records, APIs, data]

## Source Systems
[Systems of record and tools]

## Workflow Steps
1. ...
2. ...
3. ...

## Decision Points
- ...

## Rules / Policies
- ...

## Outputs
- ...

## Human Review Gates
- ...

## Validation
- ...

## Failure Modes
- ...

## Examples
- ...
```

### Step 2: Find Reusable Resources

For each step, decide what belongs where:

- `SKILL.md`: orchestration and core procedure
- `references/`: rules, schema, methodology, examples
- `scripts/`: deterministic extraction, validation, conversion, scoring
- `assets/`: templates, boilerplate, branded files, sample workbooks
- `evals/`: sample inputs, expected outputs, rubrics

### Step 3: Choose The Implementation Pattern

Use one of these patterns.

#### Pattern A: Single Process Skill

Use when the process is narrow and linear.

Example:

- KYC rules evaluation
- generate a client meeting brief
- convert instrument data to Allotrope

Structure:

```text
kyc-rules/
  SKILL.md
  references/rules-grid-schema.md
  scripts/validate_disposition.py
  evals/sample-applicant.json
```

#### Pattern B: Orchestrator Skill + Subskills

Use when the workflow has multiple phases, review gates, or resumable state.

Example:

- clinical trial protocol generation
- investment banking pitch workflow
- due diligence report generation

Structure:

```text
clinical-trial-protocol/
  SKILL.md
  references/00-initialize.md
  references/01-research.md
  references/02-foundation.md
  references/03-operations.md
  scripts/sample_size_calculator.py
  assets/protocol-template.md
```

State pattern:

```text
waypoints/
  00_metadata.json
  01_research_summary.json
  02_draft.md
  validation.json
```

#### Pattern C: Vertical Source Of Truth + Bundled Agent Workflows

Use when multiple workflows reuse shared skills.

Example:

- financial modeling skills reused by pitch agent, model builder, valuation reviewer

Structure:

```text
domain-library/
  vertical-plugins/financial-analysis/skills/dcf-model/
  vertical-plugins/financial-analysis/skills/comps-analysis/
  agent-plugins/pitch-agent/skills/dcf-model/
  scripts/sync-agent-skills.py
  scripts/check.py
```

Rule:

- Edit source skills in `vertical-plugins`.
- Bundle copies into composed agent workflows.
- Use a sync script to prevent drift.

#### Pattern D: Connector + Skill Pair

Use when a workflow depends on external systems.

Example:

- PubMed MCP + literature review skill
- CapIQ MCP + comps skill
- Screening MCP + KYC skill

Structure:

```text
marketplace/
  connectors/pubmed/
  skills/literature-review/
  skills/clinical-trial-protocol/
```

Rule:

- MCP provides access.
- Skill provides expertise.
- Do not mix connector logic into process instructions.

#### Pattern E: Validation-First Skill

Use when the output is high-stakes or easy to fake.

Example:

- Excel model audit
- pitch deck QC
- regulatory protocol completeness
- security remediation

Structure:

```text
valuation-review/
  SKILL.md
  scripts/validate_workbook.py
  references/audit-rubric.md
  evals/bad-model.xlsx
```

## Skill Maturity Levels

Use explicit maturity labels:

- `discovered`: source found, not evaluated
- `reference-found`: maintained reference exists
- `adapted`: copied/adapted to local runtime
- `draft-from-process`: built from process discovery, not yet validated
- `validated`: tested on representative examples
- `production`: used repeatedly with monitoring and owner review

## Domain Library Structure

Recommended repository layout:

```text
domain-workflow-library/
  registry.yaml
  domains/
    financial-services/
      domain-map.md
      processes/
        kyc-screening/
          workflow-card.md
          SKILL.md
          references/
          scripts/
          evals/
        dcf-modeling/
          workflow-card.md
          SKILL.md
          references/
          scripts/
          evals/
    life-sciences/
      domain-map.md
      processes/
        clinical-trial-protocol/
        single-cell-rna-qc/
  connectors/
    capiq/
    pubmed/
    clinical-trials/
  shared/
    citation-policy.md
    human-review-gates.md
    artifact-qa.md
  runs/
    YYYY-MM-DD-topic/
```

## Discovery To Skill Pipeline

Use this pipeline for each domain:

1. `Content Discovery`
   - Find existing skills, microagents, repos, docs, examples, and operator proof.
2. `Source Inventory`
   - Record every candidate source with license, maintenance, and relevance.
3. `Business Process Map`
   - Convert raw sources into process cards.
4. `Skill Gap Map`
   - Mark each process as existing, adaptable, or missing.
5. `Skill Assembly`
   - Import/adapt existing skills or create missing skills from workflow cards.
6. `Runtime Adaptation`
   - Bind to Codex, Claude Code, OpenHands, local CLI, GitHub Actions, cron, or service runtime.
7. `Validation`
   - Run smoke tests, script checks, artifact QA, and human gates.
8. `Registry Write-back`
   - Update registry with status, triggers, dependencies, validation, and provenance.
9. `Knowledge Write-back`
   - Store durable domain findings in the knowledge layer.

## Hard Rule

If neither a workflow skill nor enough business-process evidence exists, do not invent the workflow.

Create a `process-discovery-brief.md` instead, listing:

- what is known
- what is missing
- which SMEs/artifacts are needed
- which systems must be inspected
- what examples are required before skill creation

## What `launch-domain-specific-workflow` Should Do

The skill should behave like a workflow-library builder:

1. Ask/derive target domain and business process.
2. Search existing skill/microagent/plugin sources first.
3. Build a source inventory.
4. Classify available skills and gaps.
5. If a skill exists, adapt/register it.
6. If missing, build workflow card from process evidence.
7. Generate the minimal skill folder only after the workflow card is credible.
8. Add validation/evals before marking the skill usable.
9. Output registry entry, folder path, and next validation command.

The deliverable is not "an agent." The deliverable is a discoverable, validated domain workflow skill library.
