# Content Research: Manufacturing Predictive Maintenance

## Selected Use Case
- Source PDF: `/mnt/c/Users/sheke/Downloads/Ai Engineering Use Cases Framework Document.pdf`
- PDF use case: `UC06 – Predictive Maintenance`
- Objective: Predict machine failures proactively
- Agent stack in source: `IoT-agent`, `anomaly-detection-agent`, `SAP-PM-agent`
- Enterprise integrations in source: `SAP PM`, `IoT Gateways`
- Claimed implementation benefit in source: `40% faster implementation`

## Source Notes

### 1. AI-Driven Manufacturing & OpenHands Realization Framework (local PDF)
- Defines a manufacturing realization model built around reusable AI agents and enterprise integrations.
- UC06 maps cleanly to the pipeline because it already specifies objective, agent stack, deliverables, integrations, models, and expected business benefit.
- Hyundai is the natural named account because the later pages frame the broader realization around Hyundai manufacturing transformation.

### 1a. Verified OpenHands platform signals
- Repo: https://github.com/OpenHands/OpenHands
- Docs index: https://docs.openhands.dev/sdk.md
- Key verified capabilities:
  - OpenHands has a Software Agent SDK for defining agents in code and running them locally or at cloud scale.
  - OpenHands provides a CLI, headless mode, and a web app/server model rather than only an interactive UI.
  - OpenHands supports MCP transports including SSE, Streamable HTTP, and stdio, which fits the PDF's integration thesis around enterprise tools and external systems.
  - OpenHands supports skills and repository agents, which is useful for manufacturing-specific guidance, plant conventions, and reusable domain workflows.
  - OpenHands offers enterprise self-hosting in a customer's VPC via Kubernetes, which matters for manufacturing environments with OT security and data residency concerns.
- Why it matters: the PDF's proposed agent stack is not just conceptual. Verified OpenHands primitives exist for agent orchestration, headless execution, MCP tool integration, and controlled deployment models.

### 2. MakinaRocks + Hyundai Motor deployment
- URL: https://www.makinarocks.ai/en/news/makinarocks-and-hyundai-motor-expand-global-ai-deployment-to-1400-factory-robots/
- Published: April 23, 2026
- Key signals:
  - Hyundai and MakinaRocks are expanding predictive robotics AI across global production hubs.
  - Failures are predicted up to five days in advance.
  - Reported accuracy is above 90%.
  - Planned scale reaches roughly 1,400 robots by end of 2026.
- Why it matters: this is direct proof that automotive predictive maintenance has crossed from pilot rhetoric to scaled deployment.

### 3. Deloitte 2025 Smart Manufacturing Survey
- URL: https://www.deloitte.com/us/en/insights/industry/manufacturing-industrial-products/2025-smart-manufacturing-survey.html
- Key signals:
  - 92% of manufacturers view smart manufacturing as a competitiveness driver over the next three years.
  - Respondents report 10% to 20% improvement in production output, 7% to 20% productivity improvement, and 10% to 15% unlocked capacity.
  - Maintenance is one of the less mature functions, making it a live transformation wedge.
  - 65% to 70% of manufacturers are outsourcing technology, data, cybersecurity, AI, and automation roles.
- Why it matters: this supports both market demand and outsourcing readiness.

### 4. Deloitte Predictive Maintenance infographic
- URL: https://www.deloitte.com/content/dam/assets-zone3/us/en/docs/services/consulting/2024/us-smart-manufacturing-predictive-maintenance-infographic.pdf
- Key signals:
  - Industrial manufacturers lose about $50B per year to unplanned downtime.
  - Relative to preventive maintenance, predictive maintenance is associated with 53% less unplanned downtime and 79% fewer defects.
  - Typical benefits cited include 5% to 20% downtime reduction, 10% to 30% lower inventory levels, and 5% to 20% labor productivity increase.
  - Main implementation barriers are weak business cases, increasing complexity, and inadequate change management.
- Why it matters: this gives both upside and the main failure modes.

### 5. SAP manufacturing signals
- URL: https://news.sap.com/2025/03/sap-hannover-messe-2025-manufacturing-potential-adaptive-ai-driven-future/
- Key signals:
  - SAP frames downtime reduction as a core manufacturing value case.
  - SAP Asset Performance Management now includes embedded IoT monitoring.
  - SAP Field Service Management with AI improves diagnostics and first-time fix rates.
- Why it matters: SAP-native deployment is more credible than a greenfield AI stack in plants that already run SAP.

### 6. NIST manufacturing economics
- URL: https://nvlpubs.nist.gov/nistpubs/ams/NIST.AMS.600-16.pdf
- Key signals:
  - Downtime amounts to 8.3% of planned production time in discrete manufacturing.
  - NIST cites $245B in downtime costs for discrete manufacturing.
- Why it matters: the pain is large enough to support ROI narratives even when the first plant rollout is tightly scoped.

## Synthesis
- Best wedge: robotic cells and high-utilization equipment where downtime is visible, costly, and already tracked in SAP PM.
- Core differentiator: AI delivery that lands inside the plant's current maintenance workflow instead of requiring a standalone analytics destination.
- OpenHands fit: use OpenHands as the internal orchestration layer for sub-agents, MCP connectors, and repeatable delivery workflows rather than pitching it as the end-user product.
- Main risk: plants underestimate integration, governance, and technician adoption complexity.
