---
name: architecture-to-everything
description: >-
  Use when the user says "document this architecture fully", "architecture to everything",
  "turn this system into all formats", "full architecture package", or wants a complete
  multi-format output (diagram + doc + deck + interactive HTML + NotebookLM) from a
  single system description. Orchestrates drawio, architecture-presentation,
  workflow-visualizer, and notebooklm as sub-tasks.
user_invocable: true
---

# Architecture-to-Everything Skill System

Orchestrator that chains four child skills to produce every possible output
format from a single system architecture description. Input: a system name and
description (or existing drawio file). Output: four deliverables in four formats.

## Onboarding (first run only)

If `~/.claude/skills/architecture-to-everything/config.json` does not exist, ask:

1. **Deck theme**: "Enterprise Consulting (white)" or "Midnight Executive (dark)"? → default: Enterprise Consulting
2. **Interactive HTML style**: Dark background / light background → default: dark
3. **Include NotebookLM?**: Yes/No → default: Yes
4. **Default system context**: What domain are your architectures usually in? → default: AI / cloud / manufacturing

Save as `config.json`.

## Pipeline

### Stage 1: Draw.io → Diagram
Invoke the `/drawio` skill.
- Generate a component-flow diagram (NOT swimlanes) from the system description
- White background, labeled boxes, numbered arrows, grouped zones
- If the user already has a .drawio file: skip this stage and use it as input

**Pass forward:** .drawio file path + component list + data flows

### Stage 2: Architecture Presentation → Deck + Doc
Invoke the `/architecture-presentation` skill.
- Create and validate `<run>/visual-spec.json` through `pptx-visual-spec` and pass it to
  `architecture-presentation` before PPTX rendering.
- Generate the architecture explanation doc (.md)
- Generate the 10-slide pptx deck — use `Hyundai_PeopleTech_AI_Plant_Operations.pptx` as the reference template for theme/colors/layout (if it exists in the working directory)
- Both derived from the drawio diagram and system description
- Use **`/notion`** to create a team-accessible page with the architecture doc (if Notion is configured)

**Pass forward:** .md doc path + .pptx path + component descriptions

### Stage 3: Workflow Visualizer → Interactive HTML
Invoke the `/workflow-visualizer` skill.
- Map the architecture as an interactive HTML diagram
- Clickable nodes, hover for details, highlighted connections
- Dark background, color-coded node types
- Self-contained HTML, no dependencies

**Pass forward:** .html file path

### Stage 4: NotebookLM → Q&A (if enabled)
Invoke the `/notebooklm` skill (or provide manual steps).
- Upload the .md doc to NotebookLM
- Generate a Briefing Doc
- Enable Q&A on the architecture

**Output files:**
```
<system>-architecture.drawio
<system>-architecture.md
<system>-architecture.pptx
<system>-workflow.html
+ NotebookLM notebook (manual or automated)
```

## Completion

After all stages:
1. List all 4 output files with paths
2. Open pptx and HTML if auto-open is available
3. Provide NotebookLM steps
4. Print a summary: "Architecture documented in 4 formats: diagram, doc, slides, interactive HTML"

## Example usage

```
/architecture-to-everything "Hyundai AI Plant Operations Platform"
/architecture-to-everything — use the existing predictive-maintenance.drawio
/architecture-to-everything "microservices payment gateway with Stripe, Redis, PostgreSQL"
/architecture-to-everything config
```

---

## Skill Relationships

### Category
Runbook

### Dependencies
All four child skills must be installed for the full pipeline to run:
- `drawio` — Stage 1 diagram generation
- `architecture-presentation` — Stage 2 deck + doc
- `workflow-visualizer` — Stage 3 interactive HTML
- `notebooklm` — Stage 4 Q&A notebook (optional but recommended)

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `drawio` | Orchestrator → sub-task | Stage 1, always | `<system>-architecture.drawio` |
| `architecture-presentation` | Orchestrator → sub-task | Stage 2, always | `<system>-architecture.md`, `<system>-architecture.pptx` |
| `workflow-visualizer` | Orchestrator → sub-task | Stage 3, always | `<system>-workflow.html` |
| `notebooklm` | Orchestrator → sub-task | Stage 4, if enabled in config | `<system>-architecture.md` (uploaded) |
| `drawio` | Domain cluster | same system input | — |
| `workflow-visualizer` | Domain cluster | same system input | — |

### Runtime Preamble
At invocation, confirm with the user:
- "I'll run 4 stages: drawio diagram → architecture doc + deck → interactive HTML → NotebookLM. All from your system description."
- "Do you already have a `.drawio` file? If yes, I'll skip Stage 1."
- "NotebookLM step requires manual Chrome action — I'll give you the steps."

---

## Gotchas

- **NotebookLM is not fully automatable:** The Chrome MCP cannot navigate to `notebooklm.google.com`. Always fall back to manual steps for Stage 4 — never silently skip without telling the user.
- **Stage order matters:** Stages 2 and 3 both depend on the system description extracted in Stage 1. Do not run them in parallel before Stage 1 is complete.
- **drawio CLI must be on PATH:** If it's unavailable (sandbox, missing install), Stage 1 produces XML-only output. Subsequent stages can still run using the system description directly — document the gap to the user.
- **Config file is first-run only:** If `~/.claude/skills/architecture-to-everything/config.json` exists, skip the onboarding questions and use saved preferences.
- **Never use swimlanes in the architecture diagram:** Use component-flow boxes with arrows per the `drawio` skill's architecture preset.
