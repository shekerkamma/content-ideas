# Graph Report - .  (2026-06-22)

## Corpus Check
- 12 files · ~56,000 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 77 nodes · 97 edges · 16 communities (6 shown, 10 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 19 edges (avg confidence: 0.67)
- Token cost: 114,951 input · 20,482 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Vertex AI Customer Deployments|Vertex AI Customer Deployments]]
- [[_COMMUNITY_Gemini Enterprise & Agentic Ops|Gemini Enterprise & Agentic Ops]]
- [[_COMMUNITY_Generative Media & Creative|Generative Media & Creative]]
- [[_COMMUNITY_Gemini Model Customer Agents|Gemini Model Customer Agents]]
- [[_COMMUNITY_BigQuery & Data Analytics|BigQuery & Data Analytics]]
- [[_COMMUNITY_Workspace & Code Assist|Workspace & Code Assist]]
- [[_COMMUNITY_Vertex AI Search|Vertex AI Search]]
- [[_COMMUNITY_Customer Engagement Suite|Customer Engagement Suite]]
- [[_COMMUNITY_Multimodality  Physical World|Multimodality / Physical World]]
- [[_COMMUNITY_Natural Language for Legacy IT|Natural Language for Legacy IT]]
- [[_COMMUNITY_Document AI|Document AI]]
- [[_COMMUNITY_Dialogflow|Dialogflow]]
- [[_COMMUNITY_NotebookLM|NotebookLM]]
- [[_COMMUNITY_Accenture|Accenture]]
- [[_COMMUNITY_Priceline|Priceline]]
- [[_COMMUNITY_Apollo Hospitals|Apollo Hospitals]]

## God Nodes (most connected - your core abstractions)
1. `Gemini models` - 28 edges
2. `Vertex AI` - 17 edges
3. `Gemini Enterprise / Agent Platform` - 14 edges
4. `BigQuery` - 8 edges
5. `Veo` - 6 edges
6. `Imagen` - 5 edges
7. `1,302 Real-World Gen AI Use Cases (Google Cloud)` - 4 edges
8. `Vodafone` - 4 edges
9. `Adobe` - 4 edges
10. `Google Workspace with Gemini` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Spotify` --references--> `Gemini models`  [EXTRACTED]
  raw/07-media-marketing-gaming.md → raw/00-overview-and-trends.md
- `ElevenLabs` --references--> `Gemini models`  [EXTRACTED]
  raw/07-media-marketing-gaming.md → raw/00-overview-and-trends.md
- `Arizona State University` --references--> `Gemini models`  [EXTRACTED]
  raw/08-public-sector-nonprofits.md → raw/00-overview-and-trends.md
- `Harvey (legal AI)` --references--> `Gemini models`  [EXTRACTED]
  raw/02-business-professional-services.md → raw/00-overview-and-trends.md
- `Agoda (AI Vacation Planner)` --references--> `Gemini models`  [EXTRACTED]
  raw/05-hospitality-travel.md → raw/00-overview-and-trends.md

## Communities (16 total, 10 thin omitted)

### Community 0 - "Vertex AI Customer Deployments"
Cohesion: 0.14
Nodes (15): BMW Group (SORDI.ai), Mercedes-Benz (MBUX), Toyota, Harvey (legal AI), Citi, Rogo, Anthropic Claude (on Vertex AI), Warner Bros. Discovery (+7 more)

### Community 1 - "Gemini Enterprise & Agentic Ops"
Cohesion: 0.15
Nodes (15): Deloitte (Care Finder), KPMG, PwC, Wells Fargo, Humana (Agent Assist), Merck, Bosch (AskBosch), Gemini Enterprise / Agent Platform (+7 more)

### Community 2 - "Generative Media & Creative"
Cohesion: 0.29
Nodes (10): Agoda (AI Vacation Planner), LATAM Airlines (Cosmos), Virgin Voyages (Rovey), Samsung, Adobe, ElevenLabs, 1,302 Real-World Gen AI Use Cases (Google Cloud), Imagen (+2 more)

### Community 3 - "Gemini Model Customer Agents"
Cohesion: 0.20
Nodes (10): Deutsche Bank (DB Lumina), Highmark Health (Sidekick), Honeywell, Major League Baseball (Scout Insights), Thomson Reuters, Gemini models, U.S. Food and Drug Administration, Wendy's (FreshAI) (+2 more)

### Community 4 - "BigQuery & Data Analytics"
Cohesion: 0.29
Nodes (7): CVS Health (Health100), Spotify, BigQuery, Arizona State University, Etsy, Glean, Palantir

### Community 5 - "Workspace & Code Assist"
Cohesion: 0.33
Nodes (6): Valeo, Broadcom, Gemini Code Assist, Google Workspace with Gemini, Maryland Dept. of Information Technology, Verizon

## Knowledge Gaps
- **35 isolated node(s):** `Document AI`, `Dialogflow`, `NotebookLM`, `Vertex AI Search`, `Customer Engagement Suite` (+30 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Gemini models` connect `Gemini Model Customer Agents` to `Vertex AI Customer Deployments`, `Gemini Enterprise & Agentic Ops`, `Generative Media & Creative`, `BigQuery & Data Analytics`, `Customer Engagement Suite`, `Multimodality / Physical World`, `Natural Language for Legacy IT`?**
  _High betweenness centrality (0.397) - this node is a cross-community bridge._
- **Why does `Gemini Enterprise / Agent Platform` connect `Gemini Enterprise & Agentic Ops` to `Generative Media & Creative`?**
  _High betweenness centrality (0.204) - this node is a cross-community bridge._
- **Why does `Vertex AI` connect `Vertex AI Customer Deployments` to `Gemini Enterprise & Agentic Ops`, `Generative Media & Creative`, `BigQuery & Data Analytics`?**
  _High betweenness centrality (0.200) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Gemini models` (e.g. with `Trend: Natural language for legacy IT` and `Deutsche Bank (DB Lumina)`) actually correct?**
  _`Gemini models` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Vertex AI` (e.g. with `Toyota` and `Character.ai`) actually correct?**
  _`Vertex AI` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Gemini Enterprise / Agent Platform` (e.g. with `Trend: From assistants to agentic teams` and `Deloitte (Care Finder)`) actually correct?**
  _`Gemini Enterprise / Agent Platform` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Document AI`, `Dialogflow`, `NotebookLM` to the rest of the system?**
  _35 weakly-connected nodes found - possible documentation gaps or missing edges._