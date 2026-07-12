---
title: "AG-UI user interface for ADK"
source_type: "documentation"
source_url: "https://adk.dev/integrations/ag-ui/"
captured_on: "2026-06-04"
---

# Summary

Google ADK documents AG-UI as an open protocol for streaming events, client state, and bi-directional communication between agents and users. The integration is presented as a first-class path for turning ADK agents into full-featured applications rather than chat-only endpoints.

# Key Points

- AG-UI is positioned as an open protocol for rich clients across web, mobile, and CLI surfaces.
- ADK quickstart pairs an ADK agent backend with a CopilotKit web client.
- The documented pattern runs two servers: a web UI and an ADK agent API.
- Generative UI is implemented by rendering tool calls into UI components rather than returning only text.
- Shared state is bidirectional: UI changes can flow back into the agent runtime.

# Implementation Signals

- The stack is not just "agent plus frontend"; it is protocol plus runtime plus component rendering.
- Google is explicitly documenting AG-UI inside ADK integration docs, which is a meaningful maturity signal.
- This supports the use-case claim that enterprise agent frontends can be standardized rather than hand-built per agent.

# Raw Evidence Notes

- ADK says AG-UI handles streaming events, client state, and bi-directional communication.
- The example uses CopilotKit as the concrete client implementation.
- The docs show a `useRenderToolCall(...)` pattern to render a UI component from a tool invocation.

# Relevance To Use Case

This is the strongest primary implementation source in the bundle. It validates the technical feasibility of an enterprise Generative UI pattern built around agent orchestration rather than static screens.
