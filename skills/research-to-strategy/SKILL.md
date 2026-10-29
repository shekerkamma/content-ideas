---
name: research-to-strategy
description: 'End-to-end pipeline: ingest sources (YouTube, LinkedIn, web) → build knowledge graph → run through AI strategy council → output as slide deck. Use when the user says "research this topic and give me a strategy", "turn this research into a recommendation", "analyze and present".'
metadata:
  legacy-frontmatter:
    user_invocable: true
---

# Research-to-Strategy Skill System

Orchestrator that chains four child skills to turn scattered research sources
into a board-ready strategic recommendation. Input: topic + source URLs.
Output: knowledge graph + council judgment + presentation.

## Onboarding (first run only)

If `~/.claude/skills/research-to-strategy/config.json` does not exist, ask:

1. **Strategy audience**: Who sees the output? (board / exec / engineering / general) → default: exec
2. **Council mode**: Full 5-agent council or quick 3-agent? → default: full
3. **Output format**: Slides only / slides + doc / doc only → default: slides + doc
4. **Knowledge graph**: Include graphify output? Yes/No → default: Yes

Save as `config.json`.

## Pipeline

### Stage 1: Content Research → Ingest
Invoke the `/content-research` skill, enriched with deeper research tools:
- Use **Exa** (`web_search_exa`) for deep, semantically-rich source discovery (academic papers, technical blogs, industry reports)
- Use **`/wikipedia`** for baseline context on the topic (definitions, history, key players)
- Use **`/firecrawl`** to scrape any specific URLs the user provides for full-page content
- Use **`/content-research`** to ingest all sources (URLs, videos, documents) into structured notes
- Do NOT fall back to basic WebSearch — always prefer Exa and Firecrawl for richer results
- Create structured research notes with frontmatter
- Tag content as `<!-- deck-usable -->` or `<!-- internal-only -->`
- Extract key claims, data points, and expert opinions

**Pass forward:** research notes + extracted claims + source list

### Stage 2: Knowledge Graph → Connect
Invoke the `/graphify` skill.
- Build a knowledge graph from the research notes
- Identify relationships between concepts, people, technologies
- Surface non-obvious connections and patterns
- Generate graph visualization

**Pass forward:** knowledge graph + key relationships + pattern insights

### Stage 3: Strategy Council → Judge
Invoke the `/ai-strategy-council` skill.
- Run the topic through the multi-agent strategy council
- Each agent (CEO, CTO, CFO, CMO, COO perspectives) evaluates independently
- Council produces: consensus recommendation, dissenting views, risk assessment
- Score the opportunity using the vertical scorer

**Pass forward:** council recommendation + scores + risk assessment

### Stage 4: Presentation → Deliver
Invoke the `/presentation` skill or `/architecture-presentation` skill (depending on content type).
- Generate a slide deck with the strategy recommendation
- Include: market context, research findings, council judgment, recommendation, next steps
- Apply configured theme and audience framing
- Add speaker notes

**Output files:**
```
<topic>-research.md
<topic>-knowledge-graph.md          (graphify output)
<topic>-strategy-council.md
<topic>-strategy-recommendation.pptx
<topic>-visual-spec.json
```

Before the PPTX stage, apply `pptx-visual-spec`, validate the visual spec, and pass it to the
selected direct deck builder. Research evidence and strategic claims remain native, exact, or
approved assets according to the shared contract.

## Completion

After all stages:
1. Print the **executive summary**: one paragraph with the recommendation
2. Highlight any **dissenting views** from the council
3. List confidence level and key assumptions
4. List all output files

## Example usage

```
/research-to-strategy "AI in automotive manufacturing" https://youtube.com/... https://linkedin.com/...
/research-to-strategy "predictive maintenance market 2026" — use these 5 links
/research-to-strategy config
```
