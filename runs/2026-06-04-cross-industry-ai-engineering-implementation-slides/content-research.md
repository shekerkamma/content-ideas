# Content Research: Cross-Industry AI Engineering Implementation Slides

## Skill Chain

1. `GBrain Recall`
2. `content-research`
3. `industry-research-analysis-branded-deck`

## Sources used

1. Local PDF: `/mnt/c/Users/sheke/Downloads/Ai Engineering Use Cases Framework Document.pdf`
2. Repo-local GBrain recall artifact:
   - `/home/shekerk/content-ideas/runs/2026-06-04-cross-industry-ai-engineering-implementation-slides/research-notes/01-gbrain-recall.md`
3. Existing implementation spec derived from the same framework:
   - `/home/shekerk/Documents/Content/research/2026-06-04/implementation-specs/use-case-implementation-specs.md`
4. OpenHands official docs:
   - `https://docs.openhands.dev/sdk/guides/plugins`
   - `https://docs.openhands.dev/sdk/arch/tool-system`
   - `https://docs.openhands.dev/sdk/arch/conversation`
   - `https://docs.openhands.dev/openhands/usage/cli/mcp-servers`
5. OpenHands GitHub repository:
   - `https://github.com/OpenHands/OpenHands`

## PDF-grounded industry selection

The source PDF contains these SMB and cross-industry lanes:

- Dental & Healthcare Practices
- Real Estate Brokerages
- Law Firms
- Marketing Agencies
- Manufacturing & Plant Operations

This deck selects one implementation-ready use case from each non-real-estate industry represented in the existing implementation spec:

- Manufacturing: `UC-MFG-01 Predictive Maintenance AI Agent`
- Law: `UC-LAW-01 Contract Generation & Review Agent`
- Healthcare: `UC-HEALTH-01 Patient Intake Automation + Insurance Verification`
- Marketing: `UC-MKT-01 Automated Reporting Dashboard + SEO Agent`

## Current OpenHands implementation primitives verified

### Plugins

- OpenHands plugins bundle skills, hooks, MCP servers, agents, and commands into one reusable package.
- Plugin structure supports `.plugin/plugin.json`, `skills/`, `hooks/`, `agents/`, `commands/`, and `.mcp.json`.

### MCP

- OpenHands supports MCP through `Agent.mcp_config`.
- MCP tools are automatically discovered from MCP servers during agent initialization.
- CLI-managed MCP workflow is explicit:
  - `openhands mcp add`
  - start `openhands`
  - inspect with `/mcp`
  - use enabled MCP tools inside the conversation

### Conversation

- `Conversation` is the orchestration entrypoint for agent lifecycle, state orchestration, workspace coordination, and runtime services.

### Repository posture

- The official GitHub repository remains the source of truth for OpenHands implementation.
- The repo is positioned as `OpenHands: AI-Driven Development`.

## Why these four use cases are implementation-ready

- Each lane already has a clear workflow trigger, action system, and MCP-compatible integration pattern.
- Each lane maps naturally onto the OpenHands plugin packaging model.
- Each lane can be delivered as a reusable managed-service accelerator rather than a one-off prototype.

## Output intent

- Build a single branded PPTX that presents:
  - one selected use case per industry
  - a detailed implementation slide for each
  - a shared OpenHands solution architecture pattern across industries

