# Agent-Native Apps Deck Rebuild: Research Synthesis

Deck status target: `reviewed`

GBrain Recall: attempted on 2026-06-12, but local recall/query calls timed out waiting for the PGLite lock. The rebuild proceeds from the supplied transcript plus current official sources.

## Source Spine

- Supplied YouTube transcript: "The BEST New AI Opportunity Nobody Is Talking About (Codex + Cursor)", source URL `https://www.youtube.com/watch?v=fH6bMRm8fQo&t=133s`.
- OpenAI Codex CLI docs: Codex CLI is a local coding agent that can read, change, and run code in the selected directory. The docs also list MCP as a way to give Codex additional third-party tools and context.
- OpenAI Codex GitHub repo: Codex CLI is a lightweight coding agent that runs locally on the computer; the repo points to terminal, IDE, desktop, and cloud Codex surfaces.
- Model Context Protocol docs: MCP is an open standard for connecting AI applications to external systems such as data sources, tools, and workflows.
- MCP tools specification: MCP tools are model-controlled and should keep a human in the loop with visible tool exposure, invocation indicators, and confirmation prompts.
- Notion MCP docs: Notion's MCP guide shows AI tools connecting to Notion so they can read and write workspace content based on access and permissions.
- Cursor docs: Cursor positions its docs around Agent mode, Rules, MCP, Skills, CLI, models, and teams/enterprise setup.

## Core Thesis

The business opportunity is not "add an AI chatbot to an existing app." It is to build work surfaces that a user's own agent can enter, inspect, operate, and improve while the human sees the work happen. This shifts the product design question from "what agent do we build inside our app?" to "how does our app become a high-leverage surface for the user's agent?"

## Narrative Arc

1. The old pattern is app-native AI: each product has its own bounded assistant, context, and workflow assumptions.
2. The new pattern is agent-native software: the user's agent brings local context, tool access, memory, and judgment into a shared work surface.
3. The technical reason this is now practical is the convergence of local agent hosts, browser/workspace surfaces, MCP/tool connectors, CLIs/APIs, and durable project context.
4. The product opportunity is strongest where work is repeated, visible, context-heavy, and easy for a human to review.
5. The build playbook starts with the job-to-be-done, then the shared surface, then the tool contract, then the approval/memory loop.

## Quality Rules For This Rebuild

- Minimum 20 slides; target 28 slides.
- Use one consistent body font family and large presentation-sized body text.
- Avoid decorative AI-generated images for architecture slides.
- Use PPT-native vector-like diagrams with large labels, clear flow, and narrative descriptions.
- Every slide must be self-explanatory: action title, narrative paragraph, diagram or structured evidence, and a bottom-line takeaway.
- Final output must validate as PPTX XML and must not include connector XML known to trigger repair prompts.
