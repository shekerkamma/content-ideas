---
asset: reference-architecture
derived_from: ai-native-engineering pack §4A + engagement 2026-06-10-acceptance-ane-strategy
last_used: 2026-06-10
use_count: 2   # acceptance run; adapted for sap engagement 2026-06-10
---

# Asset — Owned Agent Platform (reference architecture narrative)

Reusable architecture writeup for proposals, assessments, and decks.
All primitives verified against OpenHands docs/repo 2026-06 (registry #1).

**One-paragraph version:**
The owned agent platform separates three layers that swap independently: a
**context layer** (repo-based brain — routing files, skills, specs, memory —
portable across Claude Code, Codex, and OpenHands, which defines sub-agents
as plain Markdown files), an **execution layer** (OpenHands: SDK for
codified agents, CLI for interactive work, self-hosted Enterprise via
Helm/Kubernetes for unattended work in a private VPC; MIT-licensed core,
multi-LLM), and an **integration layer** (MCP servers with scoped service
accounts). Governance wraps all three: org roles/permissions, Docker/
Apptainer sandbox isolation, action-confirmation policies, and budget/token
caps on every unattended run.

**Block diagram (text):**
```
Context layer    repo brain: CLAUDE.md/AGENTS.md · skills · specs · memory
                       │ (cold-startable by any agent host)
Execution layer  OpenHands SDK · CLI · Cloud · Enterprise (Helm/K8s, VPC)
                       │ acts through
Integration      MCP servers · scoped service accounts · GitHub workflows
                       │ governed by
Governance       roles/permissions · sandboxes · confirmation policies · caps
```

**Citations:** github.com/OpenHands/OpenHands README (deployment modes,
MIT license, multi-LLM); docs.openhands.dev — enterprise/k8s-install,
sdk/guides/security, sdk/guides/mcp, sdk/guides/agent-file-based,
organizations/roles-permissions (2026-06).
