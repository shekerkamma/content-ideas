# Reference repos and ADK + AG-UI (Generative UI) rules

<!-- Moved out of CLAUDE.md so it only loads when needed. Read on demand. -->

## Reference repos (cloned locally)

- `~/awesome-llm-apps/generative_ui_agents/` — 7 Generative UI agent demos
  (Google ADK + CopilotKit AG-UI). All deps installed. Each project has its
  own Python venv at `agent/.venv/` and Node deps in `node_modules/`.
  Requires `.env` with API keys (Gemini, Tavily, etc.) to run.
- `~/real-estate-dashboard-agent/` — forked from ai-dashboard-canvas-agent,
  customized for Summit Realty Group (DFW brokerage). Run with `npm run dev`.
  Pushed to `github.com/shekerkamma/real-estate-dashboard-agent`.
- `~/gbrain/` — GBrain knowledge brain. Bun runtime. 50 skills. MCP server.

## ADK + AG-UI (Generative UI) rules

- When building or forking any ADK agent that uses CopilotKit frontend tools
  (`useCopilotAction` — e.g. `add_chart`, `update_chart`, `delete_chart`),
  the agent's server-side `tools` list MUST include `AGUIToolset()` from
  `ag_ui_adk`. Without it, the AG-UI middleware cannot inject frontend tool
  definitions at runtime and ADK throws "Tool not found." Import:
  `from ag_ui_adk import ADKAgent, AGUIToolset`
- Frontend-side tools (registered via `useCopilotAction` in React) must NOT
  be duplicated as server-side `FunctionTool` stubs. They arrive via the
  `RunAgentInput.tools` payload and are injected as `ClientProxyTool` wrappers
  through the `AGUIToolset` → `ClientProxyToolset` substitution.
- Pipeline use cases can produce working demos as a Stage 7 artifact:
  pipeline use case → fork a generative UI demo from
  `~/awesome-llm-apps/generative_ui_agents/` → customize with domain-specific
  tools and instructions → ship as proof-of-concept. The RE dashboard is the
  first instance of this pattern.
- Gemini free tier rate limits: `gemini-3.5-flash` has 20 RPM, hits limits
  fast during interactive demos. Prefer `gemini-2.5-flash` for ADK agents.

