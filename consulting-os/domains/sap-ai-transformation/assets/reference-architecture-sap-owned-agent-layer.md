---
asset: reference-architecture
derived_from: ai-native-engineering/assets/reference-architecture-owned-agent-platform + sap pack §4A + engagement 2026-06-10-automotive-sap-ai-strategy
last_used: 2026-06-10
use_count: 1
---

# Asset — Owned Agent Layer over SAP (reference architecture narrative)

SAP adaptation of the owned-agent-platform asset. All agent-layer primitives
verified per ANE pack; SAP-side surface grounded in api.sap.com OData.

**One-paragraph version:**
The owned agent layer keeps SAP as the system of record and moves reasoning
outside it. A **context layer** (engagement brain: specs, skills, process
knowledge) feeds **ADK agents on Gemini** (with CopilotKit AG-UI for
generative dashboards over plant KPIs — the A2UI-style pattern SAP itself is
moving toward); agents reach SAP only through **MCP servers wrapping OData
v2/v4 services with least-privilege, per-agent service users** — read-only
first, write scopes earned per battle-tested use case. **Governance** wraps
everything: approval gates on writes, budget caps and audit logging per
service account, pinned model versions for unattended runs. Clean-core
discipline in the S/4 program is what produces the governed API surface this
architecture runs on — one transformation, not two.

```
Context      engagement brain: specs · skills · process knowledge
Reasoning    ADK agents (Gemini) · AG-UI generative dashboards
Integration  MCP servers → SAP OData v2/v4 · scoped service users (read-first)
Systems      S/4HANA (clean core) · EWM · PLM · MES/non-SAP
Governance   approval gates on writes · budget caps · audit · pinned models
```

**Citations:** pack §4A primitives (ADK/AG-UI verified in-house, AGUIToolset
rule); api.sap.com (OData surface); SAP Generative UI direction
[gbrain:concepts/generative-ui-sap] as convergent validation.
