# Agent Replacement Scorecard v0 Blueprint

Status: build-ready draft from partial evidence.

## Positioning

The scorecard should not say “AI replaces SaaS” as a blanket claim.

It should say:

> AI agents compress the workflow layer first. Durable systems survive when they own records, permissions, governance, proprietary data, audit trails, or regulated workflows.

This is the clearest pattern supported by the current Claude, Gemini, and Reddit evidence.

## Scoring Model

Score each workflow from 1 to 5 on five dimensions.

### 1. Workflow Determinism

High score means the work is repeatable, rule-bound, high-volume, and has predictable inputs and outputs.

Signals:

- repeated ticket or request types
- templated drafting
- structured extraction
- standard support flows
- known catalog or policy lookup

Low score means the work requires ambiguous judgment, negotiation, creativity, or situational authority.

### 2. Data Moat And System Dependency

High replacement risk means the workflow can be completed with generic or easily accessible data.

Low replacement risk means the SaaS product owns:

- proprietary records
- workflow history
- permissions
- audit trails
- regulated context
- deep integrations
- source-of-truth status

### 3. Human Sign-Off Boundary

High replacement risk means the agent can complete the work without material review.

Low replacement risk means a human must remain accountable for:

- legal interpretation
- regulated decisions
- brand-sensitive output
- customer escalation
- commercial negotiation
- high-cost exception handling

### 4. Pilotability

High score means the replacement thesis can be tested in a bounded pilot.

Required pilot design:

- replay historical examples
- run agent and human workflow in parallel
- measure cycle time
- measure escalation rate
- measure quality or resolution rate
- measure exception frequency
- measure cost per completed outcome

### 5. Renewal And Seat-Compression Leverage

High score means agent performance can credibly change procurement behavior.

Signals:

- fewer human operators needed in the SaaS interface
- fewer paid seats required
- add-on module becomes redundant
- vendor can be renegotiated around outcome pricing
- workflow can move to a general-purpose agent layer

## Output Verdicts

### Replace

Use when the workflow layer can be automated and the current SaaS value is mostly task execution, UI navigation, drafting, triage, or repeatable support.

Recommended language:

> Replace the exposed workflow layer. Keep the system of record if it owns data, permissions, or audit history.

### Renegotiate

Use when the SaaS remains useful, but agentic automation reduces seats, add-ons, modules, or usage volume.

Recommended language:

> Renegotiate the contract around fewer seats, lower add-on dependency, or outcome-based pricing.

### Enrich

Use when the SaaS owns durable data, governance, or workflow context, and agents make the platform more valuable instead of replacing it.

Recommended language:

> Keep the platform. Add agents around it to reduce manual work and improve throughput.

### Avoid

Use when the workflow is too ambiguous, regulated, adversarial, brand-sensitive, or exception-heavy for agentic replacement.

Recommended language:

> Do not replace yet. Use AI for drafting, retrieval, or assistive work with explicit human accountability.

## Diagnostic Questions

Use these questions in the product experience.

1. What job is the buyer trying to complete?
2. Which software category currently owns that workflow?
3. Is the work repeatable or judgment-heavy?
4. Does the software own the source of truth?
5. Does the workflow require human approval?
6. Can the workflow be tested with historical examples?
7. Which paid seats, modules, or add-ons would shrink if the agent works?
8. What metric would prove replacement, renegotiation, or enrichment?

## AEO Content Pages To Build

Build non-branded pages around these buyer questions:

- Where are AI agents realistically useful in customer support workflows?
- Can AI agents reduce Zendesk, Intercom, or contact-center seats?
- When can AI agents replace document summarization and drafting add-ons?
- How should a team pilot an AI agent before replacing a workflow tool?
- Which SaaS workflows are protected by data moats and governance?
- What is the difference between replacing SaaS and renegotiating SaaS?
- What human approval boundaries should AI-agent pilots include?

## Evidence Notes

This blueprint is based on partial evidence:

- 10 independent AI-answer captures across Claude and Google AI Mode/Gemini.
- 88 Reddit buyer-language rows.
- Pattern mining found recurring support for add-on collapse, human sign-off boundaries, data moat survival, pilotability, renewal leverage, and seat compression.

It should not yet be marketed as fully validated across ChatGPT, Perplexity, Claude, and Google AI Mode.

