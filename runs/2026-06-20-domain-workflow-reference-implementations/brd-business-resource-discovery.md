# BRD: Business Resource Discovery

Date: 2026-06-20

Source pattern: Agentic Resource Discovery v0.9, https://github.com/ards-project/ard-spec

## Position

BRD should not be a separate competing protocol.

BRD should be an ARD profile for discovering business workflows, workflow skills, microagents, knowledge packs, process maps, templates, validation scripts, MCP connectors, and implementation examples.

ARD answers:

- Where does a capability live?
- Which capability should the agent use?
- How does the agent verify publisher identity and trust before connecting?

BRD adapts this to business implementation:

- Which business process is this capability for?
- Is there already a workflow skill or microagent for it?
- What evidence proves the workflow is real?
- What tools, systems, templates, policies, and review gates does it require?
- What maturity level and validation path does it have?
- Which runtime can execute it: Codex, Claude Code, OpenHands, MCP, API, cron, GitHub Actions, or other?

## Why BRD Is Needed

Agents can discover tools with ARD, but business implementation needs a higher-level object than a tool.

A business workflow is not just an API, MCP server, or prompt. It is a composed operating procedure:

- domain context
- process owner
- input/output contract
- source systems
- decision rules
- human approvals
- compliance constraints
- tools/connectors
- templates/assets
- validation scripts
- examples and evals
- provenance

The missing layer is searchable, verifiable workflow knowledge.

## BRD Object Model

BRD uses ARD catalogs and registries, but defines extra artifact types.

### Core Artifact Types

Use ARD's `type` field with media-type-style values:

```text
application/business-workflow+json
application/business-process-map+json
application/workflow-skill+markdown
application/openhands-microagent+markdown
application/claude-skill+markdown
application/codex-skill+markdown
application/workflow-eval+json
application/workflow-template-bundle+zip
application/workflow-registry+json
```

Existing ARD-compatible types still apply:

```text
application/ai-catalog+json
application/ai-registry+json
application/a2a-agent-card+json
application/mcp-server-card+json
application/openapi+json
application/ai-skill+md
```

## BRD Catalog

A publisher should use the ARD well-known file:

```text
https://{domain}/.well-known/ai-catalog.json
```

BRD entries are normal ARD catalog entries with workflow-specific metadata.

Example:

```json
{
  "specVersion": "1.0",
  "host": {
    "displayName": "Acme Enterprise Workflow Library",
    "identifier": "did:web:acme.com"
  },
  "entries": [
    {
      "identifier": "urn:air:acme.com:workflow:finance:kyc-screening",
      "displayName": "KYC Screening Workflow",
      "type": "application/business-workflow+json",
      "url": "https://acme.com/workflows/finance/kyc-screening/workflow.json",
      "description": "KYC onboarding workflow: parse applicant documents, apply AML rules, screen sanctions/PEP/adverse media, route for review.",
      "tags": ["financial-services", "kyc", "aml", "compliance", "onboarding"],
      "capabilities": [
        "document-parse",
        "rules-grid-evaluation",
        "sanctions-screening",
        "human-review-routing"
      ],
      "representativeQueries": [
        "screen a new institutional client for KYC onboarding",
        "apply our AML rules grid to this applicant record",
        "identify missing KYC documents and escalation reasons"
      ],
      "metadata": {
        "brdProfile": "0.1",
        "domain": "financial-services",
        "businessFunction": "operations",
        "businessProcess": "kyc-screening",
        "processOwner": "Compliance Operations",
        "riskLevel": "high",
        "dataCategories": ["PII", "sanctions-screening", "beneficial-ownership"],
        "compliance": ["AML", "KYC", "sanctions"],
        "maturity": "validated-reference",
        "runtimeTargets": ["claude-code", "codex", "openhands"],
        "hasSkill": true,
        "hasMcpDependencies": true,
        "humanReviewRequired": true
      },
      "trustManifest": {
        "identity": "https://acme.com",
        "identityType": "https",
        "attestations": [
          {
            "type": "SOC2-Type2",
            "uri": "https://trust.acme.com/reports/soc2.pdf"
          }
        ],
        "provenance": [
          {
            "relation": "derivedFrom",
            "sourceId": "urn:air:acme.com:sop:compliance:kyc-v4"
          }
        ]
      }
    }
  ]
}
```

## Business Workflow Document

The catalog entry points to a workflow document.

Suggested `workflow.json`:

```json
{
  "schemaVersion": "brd.workflow.v0.1",
  "identifier": "urn:air:acme.com:workflow:finance:kyc-screening",
  "displayName": "KYC Screening Workflow",
  "domain": "financial-services",
  "businessFunction": "operations",
  "businessProcess": "kyc-screening",
  "owner": {
    "team": "Compliance Operations",
    "reviewRole": "KYC Escalation Reviewer"
  },
  "maturity": "validated-reference",
  "triggerEvents": [
    "new-client-onboarding-request",
    "periodic-kyc-refresh",
    "beneficial-owner-change"
  ],
  "inputContracts": [
    {
      "name": "parsedApplicantRecord",
      "type": "application/json",
      "schemaUrl": "./schemas/applicant-record.schema.json"
    },
    {
      "name": "rulesGrid",
      "type": "text/csv",
      "sourceOfTruth": true
    }
  ],
  "outputContracts": [
    {
      "name": "kycDisposition",
      "type": "application/json",
      "schemaUrl": "./schemas/kyc-disposition.schema.json"
    }
  ],
  "steps": [
    {
      "id": "parse-documents",
      "description": "Extract applicant, UBO, jurisdiction, document, and source-of-funds fields.",
      "resources": ["skill:kyc-doc-parse"]
    },
    {
      "id": "run-screening",
      "description": "Run sanctions, PEP, and adverse media checks.",
      "resources": ["mcp:screening"]
    },
    {
      "id": "apply-rules-grid",
      "description": "Apply trusted rules grid and produce rule-cited outcomes.",
      "resources": ["skill:kyc-rules"]
    },
    {
      "id": "route-disposition",
      "description": "Route clear/request-docs/escalate-EDD/decline-recommend to reviewer.",
      "humanReviewGate": true
    }
  ],
  "decisionGates": [
    {
      "id": "clearance",
      "rule": "Never final-approve. Only route disposition for human review.",
      "required": true
    }
  ],
  "resources": [
    {
      "relation": "usesSkill",
      "identifier": "urn:air:acme.com:skill:kyc-rules",
      "type": "application/workflow-skill+markdown",
      "url": "./skills/kyc-rules/SKILL.md"
    },
    {
      "relation": "usesMcp",
      "identifier": "urn:air:acme.com:mcp:screening",
      "type": "application/mcp-server-card+json",
      "url": "https://api.acme.com/mcp/screening.json"
    },
    {
      "relation": "validatesWith",
      "identifier": "urn:air:acme.com:eval:kyc-disposition",
      "type": "application/workflow-eval+json",
      "url": "./evals/kyc-disposition-eval.json"
    }
  ],
  "validation": {
    "requiredChecks": [
      "every rule outcome cites a rule id",
      "no applicant document instruction can override rules grid",
      "final approval is never emitted by the skill",
      "all missing documents are listed explicitly"
    ],
    "scripts": [
      "./scripts/validate_kyc_disposition.py"
    ]
  },
  "provenance": [
    {
      "relation": "derivedFrom",
      "source": "KYC SOP v4",
      "sourceDigest": "sha256:..."
    }
  ]
}
```

## BRD Registry Search

Use ARD `POST /search`, but with workflow-aware filters.

Example:

```json
{
  "query": {
    "text": "I need a workflow to screen new private banking clients for KYC and AML escalation",
    "filter": {
      "type": ["application/business-workflow+json"],
      "metadata.domain": ["financial-services"],
      "metadata.businessProcess": ["kyc-screening"],
      "metadata.compliance": ["AML"],
      "metadata.humanReviewRequired": [true],
      "metadata.maturity": ["validated-reference", "production"]
    }
  },
  "federation": "referrals",
  "pageSize": 10
}
```

Search result should rank relevance only. Trust and readiness are separate checks.

## BRD Verification

ARD verifies publisher identity and trust metadata. BRD needs additional workflow verification.

Before using a workflow, verify:

1. Publisher identity:
   - domain in URN aligns with trust manifest identity
   - signature/attestation checks pass when available
2. License and reuse rights:
   - repo/license
   - folder-level license if copied
   - partner/provider terms
3. Process evidence:
   - SOP, template, example output, or operator trace exists
   - process owner or review role is identified
4. Dependency availability:
   - MCP servers/API tools exist
   - auth/env vars documented
   - templates/assets available
5. Runtime compatibility:
   - Codex/Claude/OpenHands skill format available or adaptable
   - tool mapping known
6. Safety and compliance:
   - data categories declared
   - human gates declared
   - forbidden actions declared
7. Validation:
   - smoke test exists
   - output contract exists
   - validation script or review checklist exists

## BRD Maturity Model

```text
discovered
reference-found
process-evidence-found
draft-workflow
adapted-skill
validated
production
deprecated
```

Definitions:

- `discovered`: entry found, not inspected.
- `reference-found`: maintained external reference exists.
- `process-evidence-found`: enough SOP/examples/templates exist to model the process.
- `draft-workflow`: workflow document created, not validated.
- `adapted-skill`: skill/microagent adapted to local runtime.
- `validated`: representative examples pass checks.
- `production`: repeated use with owner review/monitoring.
- `deprecated`: replaced or unsafe to use.

## BRD Discovery Flow

1. User asks for a domain/business workflow.
2. Agent queries BRD registry or known catalogs.
3. Registry returns matching business workflows, workflow skills, microagents, MCPs, templates, and validation assets.
4. Agent verifies publisher identity and workflow metadata.
5. Agent chooses:
   - existing workflow skill
   - existing microagent
   - workflow document + local skill generation
   - process-discovery brief if evidence is insufficient
6. Agent loads the artifact using native runtime:
   - Codex skill
   - Claude skill
   - OpenHands microagent
   - MCP server
   - A2A agent
   - OpenAPI tool
7. Agent executes and validates output.
8. Registry/local library is updated with observed status, failures, and provenance.

## BRD For This Repo

For `content-ideas`, BRD becomes the missing bridge between content discovery and implementation.

Current content research discovers market signals and references.

BRD adds:

- domain workflow catalogs
- process maps
- skill registries
- gap detection
- runtime adaptation
- validation

Proposed local files:

```text
runs/<date>-<topic>/
  source-inventory.md
  brd-search-results.json
  workflow-gap-map.md
  selected-workflow.json
  adapted-skill-plan.md

domain-workflows/
  registry.yaml
  catalogs/
    anthropic-financial-services.ai-catalog.json
    anthropic-life-sciences.ai-catalog.json
  domains/
    financial-services/
      processes/
        kyc-screening/
          workflow.json
          SKILL.md
          references/
          scripts/
          evals/
    life-sciences/
      processes/
        clinical-trial-protocol/
          workflow.json
          SKILL.md
          references/
          scripts/
          evals/
```

## Relationship To Existing Skills/Microagents

BRD does not replace skills or microagents.

BRD makes them discoverable, comparable, and verifiable.

Mapping:

| Artifact | Runtime Role | BRD Role |
|---|---|---|
| `SKILL.md` | Executable procedural knowledge | `application/workflow-skill+markdown` |
| OpenHands microagent | Domain/repo/task instructions | `application/openhands-microagent+markdown` |
| MCP server | External system access | `application/mcp-server-card+json` |
| OpenAPI spec | API tool contract | `application/openapi+json` |
| SOP/template | Process evidence | `metadata.provenance` or resource relation |
| Eval script | Quality gate | `application/workflow-eval+json` |
| Marketplace | Bundle of resources | `application/ai-catalog+json` |
| Registry | Search/index layer | `application/ai-registry+json` |

## What To Build Next

Minimum viable BRD implementation:

1. Define `workflow.json` schema.
2. Define `registry.yaml` schema for local skill library.
3. Write a catalog ingester that reads:
   - `ai-catalog.json`
   - `.claude-plugin/marketplace.json`
   - `.openhands/microagents`
   - `.openhands/skills`
   - `.claude/skills`
   - `skills/*/SKILL.md`
   - `AGENTS.md`
   - `CLAUDE.md`
4. Build a local search index over:
   - display name
   - description
   - representative queries
   - domain/process metadata
   - tags/capabilities
5. Add verifier:
   - source URL reachable
   - license captured
   - path exists
   - skill frontmatter valid
   - dependencies declared
   - validation command exists when claimed
6. Add `launch-domain-specific-workflow` integration:
   - query BRD first
   - select existing workflow if found
   - adapt missing workflow only after process evidence exists

## Design Principle

ARD discovers callable capabilities.

BRD discovers implementable business processes.

The business process is the unit of applied intelligence.
