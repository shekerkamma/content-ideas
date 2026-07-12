# Process Discovery Brief: Pharmacovigilance Adverse Event Triage

## Status

No direct maintained workflow skill was found in the checked Anthropic life-sciences and OpenHands public references.

## Known

- This is a high-stakes regulated life-sciences workflow.
- Likely steps include adverse event intake, case validation, seriousness assessment, expectedness check, causality support, reportability/deadline determination, case narrative drafting, and safety reviewer routing.
- A human safety reviewer is required.

## Missing

- Company pharmacovigilance SOP
- Intake form schema
- Safety database/API fields
- MedDRA coding expectations
- Product labeling source
- Country/reportability rules
- Seriousness/expectedness decision tree
- Case narrative template
- Escalation and submission deadline rules
- De-identified examples and expected outputs

## Required Before Skill Creation

- 3-5 de-identified sample adverse event cases
- Expected triage outputs for each sample
- Reviewer comments or QA findings
- Source SOP or policy rules
- Safety system/API contract
- Human review gate definition

## Proposed Skill Pattern

Use an orchestrator skill plus validation-first subskills only after process evidence exists:

1. Intake validation
2. Patient/product/event extraction
3. Seriousness classification
4. Expectedness check against label
5. Reportability/deadline determination
6. Draft case narrative
7. Route to safety reviewer
8. Validate output completeness

## Hard Rule

Do not generate an executable workflow skill from general pharmacovigilance knowledge alone. Build the workflow from SOPs, examples, rules, and validation artifacts.
