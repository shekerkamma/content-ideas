---
name: responsible-ai-framework
description: Defines an organisation's responsible AI principles, risk tier taxonomy, governance structure, and per-use-case guardrails. Use before deploying AI in customer-facing or high-stakes internal contexts, or when regulators or boards require an AI governance position.
---

# Responsible AI Framework

## When To Use

Use before deploying AI in any customer-facing, regulated, or high-stakes context — or when a board, regulator, or enterprise risk function requires a documented AI governance position. Responsible AI frameworks built after an incident are remediation; built before deployment, they are risk management.

## Consulting Approach

Accenture's responsible AI approach is built on six principles: Fairness, Reliability, Transparency, Privacy, Security, and Inclusivity. The framework does not apply these principles uniformly — it tiers AI use cases by risk level and applies proportionate governance. A chatbot that answers FAQ questions requires less governance overhead than an AI model that makes hiring recommendations. The key design question is: where could this AI cause harm, to whom, and under what conditions?

## Workflow

1. Define the organisation's responsible AI principles (adapt from the six Accenture principles or applicable regulation such as EU AI Act).
2. Design the use case risk tier taxonomy: Low (informational, human in loop), Medium (decision support, limited autonomy), High (autonomous decisions affecting people), Critical (regulated domains, irreversible outcomes).
3. Assign existing and planned use cases to risk tiers.
4. Define governance requirements per tier: review process, documentation, testing, monitoring, human override.
5. Design the review board: who reviews High and Critical use cases before deployment.
6. Define the ongoing monitoring and audit cycle.

## Output Format

```markdown
# Responsible AI Framework — [Organisation]
**Version:** [n]  **Date:** [YYYY-MM-DD]  **Owner:** [Role]

## Principles
| Principle | Definition | How We Apply It | What We Will Not Do |
|---|---|---|---|
| Fairness | | | |
| Reliability | | | |
| Transparency | | | |
| Privacy | | | |
| Security | | | |
| Inclusivity | | | |

## Risk Tier Taxonomy
| Tier | Definition | Examples | Governance Required |
|---|---|---|---|
| Low | | | |
| Medium | | | |
| High | | | |
| Critical | | | |

## Use Case Risk Register
| Use Case | Tier | Key Risks | Human Override Required? | Regulatory Exposure |
|---|---|---|---|---|

## Governance Requirements by Tier
| Requirement | Low | Medium | High | Critical |
|---|---|---|---|---|
| Pre-deployment review | | | | |
| Bias / fairness testing | | | | |
| Explainability documentation | | | | |
| Human override mechanism | | | | |
| Monitoring cadence | | | | |
| Incident response plan | | | | |

## Review Board
| Role | Responsibility | Tier Scope | Quorum |
|---|---|---|---|

## Monitoring & Audit
| Activity | Frequency | Owner | Output |
|---|---|---|---|

## Regulatory Mapping
[Which regulations apply (EU AI Act, GDPR, sector-specific)? How does this framework satisfy each?]
```

## Quality Bar

- Principles must be accompanied by "what we will not do" statements — principles without limits are marketing, not governance.
- Risk tiers must be defined by impact on people, not by technical complexity.
- Every High and Critical use case must have a named human override mechanism — "the system can be overridden" is not sufficient.
- Monitoring cadence must be defined before deployment, not after the first incident.
