---
name: competitor-analysis-pipeline
description: Use when the user asks for competitor analysis, competitive landscape, competitor benchmarking, battlecards, market map, positioning analysis, consulting-firm positioning comparisons, or client-ready competitor-analysis deliverables. Use especially when outputs must include sourced research, a structured storyline, a branded PPTX deck, an interactive HTML page, GitHub Pages publishing, or review gates such as grill-me, story-architect, STORM, GStack strategy/design review, and PPTX/HTML QA.
---

# Competitor Analysis Pipeline

Build a source-backed competitor analysis that ends in decision-ready artifacts, not a loose vendor list. The default deliverables are:

- Research dossier in `runs/<date>-<target>-competitor-analysis/outputs/`
- Branded PPTX deck in `runs/<date>-<target>-competitor-analysis/client-package/`
- Self-contained interactive HTML page in `client-package/site/index.html`
- Optional GitHub Pages publication when the user asks for a shareable URL

Read [references/quality-gates.md](references/quality-gates.md) before finalizing any client-facing deck or HTML page.

## Files

- `scripts/create_run.py` - create the standard run folder, README, and `status.json`.
- `scripts/validate_tabbed_html.js` - Playwright QA for self-contained tabbed HTML reports using `button[data-tab]` and `main section[id]`.
- `references/quality-gates.md` - final client-readiness checklist.

## Runtime Preamble

State that this skill will use a chained competitor-analysis pipeline: durable memory/GBrain recall, preferred research tools before generic web search, structured synthesis, grill-me/story-architect review, optional GStack strategy/design review, then branded PPTX and HTML QA.

## Workflow

1. **Frame the job.**
   Define the target company/product, buyer job-to-be-done, decision audience, geography, timeframe, explicit deliverables, and publish/open requirements. If the user asks for a deck, honor slide-count minimums.

2. **Create the run folder.**
   Use `runs/<YYYY-MM-DD>-<slug>-competitor-analysis/` with:
   - `inputs/`
   - `outputs/`
   - `client-package/`
   - `client-package/site/`
   - `client-package/qa/`
   Prefer:
   `python3 skills/competitor-analysis-pipeline/scripts/create_run.py "<target>"`

3. **Run recall before research.**
   Use GBrain or durable memory first when available for the company, competitors, vertical, buyer, or prior runs. Record recall status in the run notes. If GBrain is unavailable, continue and document that fallback.

4. **Research with tool discipline.**
   Do not start with generic search. Prefer this order:
   - local repo artifacts and previous run files
   - GBrain/memory recall
   - specialist research tools such as Exa, Firecrawl, content-research, enterprise-ai-competitor-landscape, STORM, or official docs
   - primary sources: company pages, docs, pricing pages, filings, press releases, GitHub repos, product pages
   - generic web search only as fallback or explicit current verification

5. **Define competitor arenas.**
   Compare by buyer job, not vendor self-description. Use 3-5 arenas such as:
   - direct category competitors
   - adjacent workflow/product competitors
   - implementation, onboarding, or services operations competitors
   - enterprise AI/automation platforms
   - consulting firms and system integrators when they shape buyer expectations

6. **Build a consistent rubric.**
   Score each competitor on the same dimensions. Typical dimensions:
   - execution depth
   - enterprise trust
   - system fit and integration
   - proof quality
   - distribution strength
   - pricing clarity
   - threat severity
   - partnerability

7. **Produce structured outputs.**
   At minimum create:
   - `outputs/company-table.csv`
   - `outputs/competitor-brief.md`
   - `outputs/story-structure-review.md`
   - `outputs/story-architect-pack.md`
   - source notes or bibliography with confidence labels

8. **Use review gates before rendering.**
   Apply `grill-me` to pressure-test content completeness, structure, storyboard, layout, and evidence quality. Use `story-architect` to turn findings into a decision storyline. Check GStack-related strategy/design review skills when the task is high-stakes or client-facing; use them as review lenses, not as a replacement for sourced research.

9. **Deck storyline.**
   Lead with the answer, then method, market map, scoring heatmap, threat priority, differentiated position, category deep dives, battlecards, consulting-firm implications, proof plan, roadmap, source confidence, and final recommendation. Avoid appendix-first or vendor-by-vendor chronology unless the user explicitly asks for a reference appendix.

10. **Build branded PPTX.**
    Use `branded-pptx-deck` or the repo's branded PPTX workflow. Never ship a blank-template client deck. Keep the builder script with run artifacts. Use `*-draft.pptx` before QA and `*-reviewed.pptx` only after QA passes.

11. **Build interactive HTML.**
    Make `client-package/site/index.html` self-contained unless the user requests a framework app. The first screen should be the actual report, not a landing page. Tabs/sections must map one-to-one; no hidden orphan sections.

12. **Validate and publish.**
    Run PPTX validation, preview/contact sheets, OfficeCLI QA when available, and Playwright HTML navigation checks. If publishing to GitHub Pages, commit and push the final HTML to the configured Pages branch and verify the live URL with a cache-busting query string.
    For tabbed HTML reports, prefer:
    `node skills/competitor-analysis-pipeline/scripts/validate_tabbed_html.js <html-file-or-url> --screenshot <run>/client-package/qa/html/final.png`

13. **Deliver for Windows when requested.**
    Copy final artifacts to the configured delivery directory or the user's Windows Desktop/OneDrive path when that is the established workflow. Open artifacts with Windows PowerShell only after final QA.

## Output Standards

Use explicit artifact status:

- `draft`: generated but not fully reviewed
- `reviewed`: render QA, content QA, and source confidence checks passed
- `blocked`: required data/tooling/render path is unavailable

Final response must include:

- PPTX path and slide count
- HTML local path
- public URL if published
- QA status
- what review gates were used
- the differentiated strategic answer in 2-4 bullets

## Skill Relationships

### Category
Business Automation

### Dependencies
Skills that must be installed for this skill to work:
- `branded-pptx-deck` - required for native branded PowerPoint deliverables
- `grill-me` - required for pressure-testing structure and content quality
- `story-architect` - required for decision-ready storyboard and narrative spine

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `content-research` | Sequential upstream | URL or website ingestion is needed | `outputs/research-notes.md` |
| `enterprise-ai-competitor-landscape` | Sequential upstream | enterprise AI competitor universe is needed | `outputs/company-table.csv` |
| `storm-research` | Parallel / Complement | deeper multi-perspective research is useful | `outputs/storm-brief.md` |
| `grill-me` | Amplifier | always before final client-facing artifacts | `outputs/story-structure-review.md` |
| `story-architect` | Amplifier | always for deck/page storyline | `outputs/story-architect-pack.md` |
| `branded-pptx-deck` | Sequential downstream | PPTX requested | `client-package/*-reviewed.pptx` |
| `data-analytics:publish-artifact-to-sites` | Alternative / Peer | Data Analytics artifact hosting is required instead of static HTML | hosted artifact URL |
| GStack strategy/design review skills | Behavioral overlay | optional high-stakes review of strategy and layout | `outputs/gstack-review-notes.md` |

### Runtime Preamble
I am using `competitor-analysis-pipeline`, which chains research, structured synthesis, grill-me/story-architect review, optional GStack review lenses, and branded PPTX/HTML QA. Generic web search is a fallback, not the first research step.

## Host Compatibility

### Target Hosts
- Claude Code: yes, when routed through repo-local `skills/` or mirrored to `.claude/skills/competitor-analysis-pipeline/`
- Codex/OpenAI: yes, discovery path `skills/competitor-analysis-pipeline/SKILL.md` through repo skill routing
- OpenHands: yes, wrapper path `.agents/skills/competitor-analysis-pipeline/SKILL.md`

### Canonical Source
`skills/competitor-analysis-pipeline/SKILL.md` is the canonical repo-local source.

### Tool Mapping
- Claude `Read` / `Grep` / `Glob` -> Codex shell reads and `rg`
- Claude `Edit` / `MultiEdit` -> Codex `apply_patch`
- Claude `Bash` -> Codex shell command
- Claude `AskUserQuestion` -> concise chat question or numbered choices when repo rules require it
- Claude `Task` / subagent -> Codex main-thread execution or available multi-agent tools

## Gotchas

- **Vendor-list trap:** Do not organize the whole deliverable as one slide per competitor. Start with buyer job, arenas, rubric, heatmap, and threat priority.
- **Unstructured research trap:** Do not mix sourced facts, assumptions, and recommendations without confidence labels.
- **Generic search trap:** Do not start with generic web search when GBrain, local artifacts, specialist research tools, Firecrawl, Exa, content-research, or official sources are available.
- **Consulting appendix trap:** If Accenture, BCG, McKinsey, IBM, Deloitte, or other consultancies shape buyer expectations, integrate them as an arena or force, not just an appendix.
- **Deck QA trap:** Do not mark a PPTX reviewed until real render/preview QA and text-overflow checks pass.
- **HTML QA trap:** Do not publish an interactive page until all tabs activate and every section is reachable.
