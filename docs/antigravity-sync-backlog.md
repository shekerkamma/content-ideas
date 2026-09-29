# Antigravity Cross-Host Synchronization & Incremental Backlog

## Overview
This document tracks the synchronization status between Windows Antigravity (CLI & IDE), WSL Antigravity, Claude Code CLI, and Codex CLI.

Components are ported progressively in controlled waves:
- **Wave 1 (Active / Foundation)**: CLI configurations, IDE editor settings, essential plugins, and core Linux-native MCP servers.
- **Wave 2 (Active / Top 50 Skills & Extended Suite)**: Top 50 canonical skills, founder plugins, and extended Linux MCP servers.
- **Wave 2.5 (Active / Batch 2 & Browser Bridge)**: 45 additional operator/engineering skills (total 95 active skills), Chrome DevTools Protocol bridge, and lightweight fetch MCP.
- **Wave 3 (Staged Backlog / Deferred)**: Additional domain plugins (`firebase`, `science`), Windows-only binaries, and host-bound browser profiles.

---

## Component Matrix & Portability Status

### 1. Antigravity CLI & IDE Core Configuration
| Component | Source Path | Target WSL Path | Port Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **CLI Settings** | `C:\Users\sheke\.gemini\antigravity-cli\settings.json` | `~/.gemini/antigravity-cli/settings.json` | ✅ Synced | Configured with `dangerouslySkipPermissions: true`, `always-proceed`, and WSL workspace paths (`/home/sheke/content-ideas`). |
| **IDE Settings (User)** | `AppData\Roaming\Antigravity\User\settings.json` | `~/.antigravity-server/data/User/settings.json` | ✅ Synced | Autonomous mode, zero-friction tool/edit approvals, Linux paths. |
| **IDE Keybindings** | `AppData\Roaming\Antigravity\User\keybindings.json` | `~/.antigravity-server/data/User/keybindings.json` | ✅ Synced | Terminal Shift+Enter multi-line newline sequence. |
| **IDE Plugins Config** | `C:\Users\sheke\.gemini\config\config.json` | `~/.gemini/config/config.json` | ✅ Synced | Plugin activations for SDK, Chrome DevTools, Guidance, and Founders bundle. |

### 2. Plugins Inventory & Status
| Plugin | Origin | Status | Wave | Scope / Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `google-antigravity-sdk` | Windows AGY | ✅ Active | Wave 1 | Core Python SDK integration for Antigravity agents |
| `modern-web-guidance-plugin` | Windows AGY | ✅ Active | Wave 1 | Modern web engineering standards & guidance |
| `free-claude-code-plugin` | Windows AGY | ✅ Active | Wave 1 | Proxy gateway router integration for Claude/Codex |
| `chrome-devtools-plugin` | Windows AGY | ✅ Active | Wave 1 | Chrome DevTools protocol inspection |
| `gemini-notebook-founders` | Windows AGY | ✅ Active | Wave 2 | 11-skill business/founder playbook bundle with operational rules |
| `firebase` | Windows AGY | 📋 Backlog | Wave 3 | Firebase deploy and management plugin |
| `science` | Windows AGY | 📋 Backlog | Wave 3 | Scientific computing and research |
| `android-cli-plugin` | Windows AGY | ⏸️ Deferred | Wave 3 | Android CLI development tooling |

### 3. MCP Servers Inventory & Status
| Server Name | Protocol / Command | Source | Status | Wave | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `google-developer-knowledge` | HTTPS (`developerknowledge.googleapis.com`) | Windows AGY | ✅ Active | Wave 1 | Native Google auth provider |
| `gbrain` | HTTP (`http://127.0.0.1:3131/mcp`) | WSL Codex | ✅ Active | Wave 1 | Semantic memory and knowledge layer |
| `playwright-isolated` | `npx -y @playwright/mcp@latest` | WSL Claude/Codex | ✅ Active | Wave 1 | Linux headless chromium automation (`chromium-1228`) |
| `context7` | HTTPS (`mcp.context7.com`) | Windows AGY | ✅ Active | Wave 1 | Real-time context expansion |
| `session-handoff` | Local binary (`codex-mcp/session-handoff-start`) | WSL Codex | ✅ Active | Wave 1 | Cross-session continuity |
| `notebooklm` | `uvx --from notebooklm-py[mcp] notebooklm-mcp` | WSL Claude | ✅ Active | Wave 2 | Google NotebookLM Python MCP |
| `notion` | `npx -y @notionhq/notion-mcp-server` | WSL Claude | ✅ Active | Wave 2 | Notion workspace integration |
| `higgsfield` | HTTPS (`mcp.higgsfield.ai/mcp`) | WSL Claude | ✅ Active | Wave 2 | Higgsfield video model generation |
| `chrome-devtools` | `chrome-devtools-mcp@latest --browser-url=http://127.0.0.1:9222` | Windows AGY | ✅ Active | Wave 2.5 | Chrome DevTools Protocol bridge for live tab control |
| `fetch` | `uvx mcp-server-fetch` | Upstream | ✅ Active | Wave 2.5 | Fast markdown web page reader |

---

### 4. Active Skills (95 Total Skills Installed)
Configured via Antigravity's native `skills.json` at:
- Global: `~/.gemini/config/skills.json`
- Workspace: `.agents/skills.json`

#### Category 1: Product Development & Autonomous Execution (10)
1. `plaid` — Product roadmap execution & build loop
2. `karpathy-guidelines` — Surgical coding, minimal diffs & verification
3. `improve` — Codebase architectural survey & improvement plans
4. `ponytail` — YAGNI & standard library simplicity
5. `ponytail-review` — Complexity and dead-abstraction hunting
6. `ponytail-audit` — Whole-repo over-engineering scanner
7. `grill-me` — Interactive design & requirement interview
8. `meta-loop` — Multi-agent iterative goal loop
9. `goal-loop-orchestrator` — Long-horizon objective orchestrator
10. `autoplan` — Automatic task breakdown & execution planner

#### Category 2: Code Craft, Git Hygiene & Dev Security (10)
11. `code-review-specialist` — Dedicated code review with line-by-line actionable feedback
12. `code-simplification` — Eliminate boilerplate, premature abstractions, and dead code
13. `codebase-design` — Structural patterns, modular architecture, and boundaries
14. `git-guardrails-claude-code` — Safe Git operations and branch safety
15. `git-workflow-and-versioning` — Branching strategies, release tagging, and PR discipline
16. `resolving-merge-conflicts` — Surgical three-way merge resolution
17. `security-and-hardening` — Vulnerability detection, secrets prevention, and hardening
18. `debugging-and-error-recovery` — Root-cause debugging and reproducible regression tests
19. `performance-optimization` — Profiling, hot-path analysis, and latency reduction
20. `ci-cd-and-automation` — Pipeline automation and testing workflows

#### Category 3: Fractional AI CTO & Architecture (8)
21. `ai-head-of-engineering` — Executive technical leadership and roadmap direction
22. `ai-head-of-engineering-30-day-build-roadmap` — 30-day execution sprints and milestones
23. `ai-head-of-engineering-build-vs-buy-auditor` — Rigorous build-vs-buy financial auditing
24. `ai-head-of-engineering-stack-picker` — Pragmatic technology stack selection
25. `ai-head-of-engineering-scope-architect` — Strict MVP scoping and feature pruning
26. `ai-head-of-engineering-scope-killer` — Ruthless removal of non-critical scope
27. `architecture-presentation` — Visual technical architecture decks
28. `architecture-to-everything` — Convert architectural specs to code and documentation

#### Category 4: Presentation & Executive Deck Engineering (10)
29. `present` — Master presentation router
30. `branded-pptx-deck` — Native branded PowerPoint builder
31. `pptx-toolkit` — Controlled PPTX inspection and edits
32. `pptx-design-quality` — Archetype layouts, typography & QA
33. `pptx-visual-spec` — Slide layout constraints & visual spec
34. `presentation-source-bundle` — Source asset intake and normalization
35. `presentation-content-writer` — Structured executive slide copywriting
36. `story-architect` — Narrative arc and executive framing
37. `impeccable` — Frontend design polish, typography & tokens
38. `genspark-slides` — Hosted AI slide generation engine

#### Category 5: High-Ticket Sales, Deals & Consulting (9)
39. `presales-deal-prep` — Enterprise deal research and positioning
40. `strategy-consulting` — Management consulting frameworks and client deliverables
41. `ai-strategy-council` — Multi-model advisory council for strategy evaluation
42. `ai-strategy-brief` — Executive one-page strategy briefings
43. `mckinsey-audience-researcher` — Audience psychographics and stakeholder mapping
44. `challenger-sale` — Commercial teaching and constructive tension sales choreography
45. `engagement-management` — Delivery governance and client milestone management
46. `solution-delivery` — Enterprise delivery roadmaps and phase sign-offs
47. `difficult-conversation-prep` — Scenario simulation for high-stakes meetings

#### Category 6: Market Intelligence & Competitive Analysis (10)
48. `enterprise-ai-competitor-landscape` — 100-150 company market maps & quadrants
49. `competitor-analysis-pipeline` — Structured competitive teardowns
50. `evidence-led-competitor-pipeline` — Primary evidence competitor analysis
51. `aianalyst-competitor-analysis` — Analytical competitor evidence synthesis
52. `compound-competitor-analysis-pptx` — Competitor PPTX package builder
53. `investor-competitive-dossier` — Venture & investor deck rebuilds
54. `saas-gap-analyzer` — SaaS market white-space identification
55. `disruptive-teardown-pipeline` — Disruptive business model teardowns
56. `deepgrid-competitive-intelligence` — Hardware/semiconductor market intelligence
57. `pricing-creativity` — Monetization & pricing architecture

#### Category 7: Deep Web Research, AEO & Harvesting (18)
58. `storm-research` — Deep multi-perspective research synthesis
59. `content-research` — Systematic domain & topic research
60. `dataset-collect` — Declarative recurring data pull pipelines
61. `anysite-cli` — Multi-source CLI web data extraction
62. `exa-api` — Exa neural search discovery
63. `you-com-search` — Live web & news research
64. `last30days` — High-signal 30-day temporal research
65. `watch` — Video intake & content extraction
66. `scrape-creators` — Creator & influencer intelligence
67. `reddit-seo-pipeline` — Social intent & opportunity discovery
68. `aeo-orchestrator` — Master AI Engine Optimization loop
69. `aeo-query-planner` — Strategic search query planning
70. `aeo-source-discovery` — Deep authoritative source discovery
71. `aeo-evidence-sprint-loop` — Rapid evidence harvesting cycle
72. `aeo-reddit-opportunity-finder` — Reddit brand opportunity finder
73. `firecrawl` — Deep web scraping and batch crawling API
74. `hackernews` — Hacker News sentiment, technical discussions & launches
75. `substack` — Substack thought-leadership and industry newsletter intelligence

#### Category 8: Founder Playbook & Media/Knowledge Systems (20)
76. `gemini-notebook-playbook` — Research & data into finished business work
77. `research-auditor` — Audit research claims and validity
78. `missing-research-finder` — Identify holes and blind spots in research
79. `devils-advocate` — Stress-test assumptions and proposals
80. `business-data-analysis` — Financial and operational modeling
81. `powerpoint-builder` — Rapid business slide construction
82. `excel-model-generator` — Structured financial and unit economics models
83. `openhands-niche-agency` — Done-for-you AI engineering agency model
84. `channel-to-kb-ytdlp` — YouTube channel to Karpathy-style LLM wiki
85. `mcp-capability-probe` — MCP schema and tool mapping
86. `hyperframes` — Narrative programmatic video engine
87. `hyperframes-cli` — Command-line renderer and asset packager
88. `ai-graphics` — Generative visual asset pipeline
89. `explainer-graphic` — Visual schematics and infographic creator
90. `drawio` — Technical architectural diagram builder
91. `excalidraw` — Hand-drawn style conceptual wireframes
92. `openkb` — Open Knowledge Base framework
93. `video-to-deck` — Convert video footage and talks into structured slide decks
94. `use-case-film` — Long-form narrated explainer films for complex domains
95. `sync-gbrain` — Synchronize findings and durable models to local GBrain store

---

### 5. Remaining Skills Staged in Backlog
The remaining 239 specialized/niche skills in `/home/sheke/content-ideas/skills/` remain available in the repository source and can be mounted into `include_only` on demand.
