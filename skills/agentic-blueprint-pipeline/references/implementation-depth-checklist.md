# Implementation Depth Checklist

Use this before marking any Master Implementation Blueprint `reviewed`.

The deliverable should feel like a capability demonstrator: the buyer should
believe the team can start discovery and implementation immediately if engaged,
because the major architectural decisions are already mapped. It is not an
instruction to build the product now.

## Hard Requirements

- **Stack:** exact recommended tools, not generic categories.
- **Architecture:** system boundary, runtime topology, agent loop, human review
  points, and failure behavior.
- **Schema / data model:** table or entity names, purpose, key fields, indexes,
  tenancy/security model, and retention/deletion policy.
- **API surface:** method/path, purpose, input/output shape, auth, and failure
  behavior.
- **Integrations:** incumbent systems, data direction, permissions/auth, and
  fallback behavior.
- **Folder/module structure:** enough shape for a builder to start scaffolding.
- **Environment variables:** required secrets/config values.
- **QA:** acceptance criteria, edge cases, data-boundary tests, and verification
  method.
- **Deployment:** staging, production sequence, smoke test, rollback, logs,
  metrics, alerts, and dashboards.

## Review Questions

1. Could a builder start a repo from this without asking what the core modules
   are?
2. Could an architect identify the main tables/entities and API routes?
3. Could a security reviewer see the auth, tenancy, data retention, and audit
   model?
4. Could a QA reviewer turn the edge cases into tests?
5. Could a buyer see how this replaces slow traditional discovery with
   AI-native execution readiness, without implying we are already building the
   use case?

If any answer is no, keep status `draft-needs-operator-review`.
