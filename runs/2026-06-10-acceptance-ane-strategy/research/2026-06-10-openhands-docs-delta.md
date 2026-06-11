---
captured: 2026-06-10
source_url: https://docs.openhands.dev/llms.txt
source_type: repo
domain: ai-native-engineering
target_section: 3
summary: OpenHands documented primitives — MCP, sandboxing, sub-agents, skills/plugins, GitHub workflows, enterprise controls
---

Verified from the official docs index (each claim has a dedicated doc page):

- **MCP**: architecture + guides + CLI server management
  (sdk/arch/mcp.md, sdk/guides/mcp.md, openhands/usage/cli/mcp-servers.md) —
  "MCP enables dynamic tool integration from external servers"
- **Sandboxing/security**: Docker sandbox isolation; Apptainer rootless
  containers (HPC); custom sandbox images; action security analysis with
  confirmation policies (sdk/guides/security.md, sdk/arch/security.md)
- **Sub-agents/delegation**: parallel sub-agent delegation; synchronous task
  tool set; **file-based agents defined as plain Markdown files**
  (sdk/guides/agent-delegation.md, agent-file-based.md) — folders-and-files
  portability confirmed at platform level
- **Skills & plugins**: skills add domain knowledge; plugins "bundle skills,
  hooks, MCP servers, agents into reusable packages" (sdk/guides/skill.md,
  plugins.md) — direct fit for packaging consulting accelerators
- **Repository customization**: `.openhands` directory + lifecycle hooks
- **GitHub workflows**: official GitHub Action for CI/CD; PR review,
  reviewer assignment, TODO implementation guides
- **Enterprise**: Helm/Kubernetes install, resource limits, external
  PostgreSQL, enterprise-vs-OSS comparison; org roles & permissions; API key
  management. NOTE: no dedicated "budget enforcement" doc page in the index —
  budget claim from the landing page stands but cite landing page, not deeper
  docs. [verify wording at next curation]
- **SDK**: "clean, modular SDK with production-ready tools"; API reference
  covers agent, conversation, event, llm, tool, workspace, security modules
