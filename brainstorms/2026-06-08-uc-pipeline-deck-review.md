# UC Pipeline Deck Review: Brainstorm / Discovery Notes
Date: 2026-06-08 · Goal: Review all 10 use cases in uc4-full-pipeline-deck.pptx for correctness of identification, realization, and solution architecture. Fill gaps from OpenHands GitHub repo.

## Structured context
- **Topic type**: product-design
- **Topic string**: "Review 10 AI use cases across 5 industries for implementation accuracy against OpenHands primitives"
- **Entities**: OpenHands, Unilever, Hyundai, Tampa General Hospital, CommonSpirit Health, TD Bank, JPMorgan, DroneDeploy, Barton Malow, BCG, LexisNexis, Harvey AI
- **Prospect/account**: n/a (internal deck QA)
- **Target buyer**: VP Engineering / CTO / domain ops leaders
- **Verticals**: Manufacturing, Healthcare, Legal, Financial Services, Construction
- **Open decisions**: SAP AI GA status verification; "composite beats pure LLM" sourced data point

## Summary / key decisions (final — reconciled after 17 questions)

### Decision 1: Category A vs Category B split
- **Category A (buildable)**: UC-01 (PdM), UC-02 (Visual QI), UC-03 (Patient Intake), UC-05 (Contract Review)
- **Category B (benchmark)**: UC-04 (Clinical AI), UC-06 (TD Bank), UC-07 (JPMorgan COIN), UC-08 (DroneDeploy), UC-09 (BCG), UC-10 (LexisNexis)
- Category B gets restructured: "How They Solved It" + "How We'd Build It" — honest framing
- Category B drops Governance/GitHub/Brand Voice slides (not our build)

### Decision 2: OpenHands API corrections (affects all architecture slides + slide 3)
- `Agent(llm, tools)` — not `Agent(llm, tools, mcp_config, agent_context)`
- `Conversation(agent, workspace, plugins)` — not `Conversation(workspace, callbacks)`
- MCP config at platform/TOML level, not per-agent
- Skills = markdown prompts, not code bundles

### Decision 3: MCP server honesty
- **Verified repos**: predictive-maintenance-mcp, open-agreements, lavern, suzielaw, claude-for-legal, anylegal-oss
- **To be built**: FHIR wrapper, Twilio wrapper, Calendly wrapper, SAP MES wrapper, vision-pipeline wrapper
- **Remove**: machina-ai (doesn't exist on PyPI)
- **Mark as PoC**: mcp-maintenance-cap (unverified, may be private)

### Decision 4: Branding
- brand_name = "AI Market Research"
- Per-industry taglines defined (see Q15)
- Closer: "10 use cases. 5 industries. One honest architecture."

### Decision 5: Competitive landscape updates
- Harvey AI: $11B valuation, $300M ARR, 142K lawyers
- CoCounsel: 20K+ firms, 5-8 hrs/day saved
- LexisNexis: add 344% ROI benchmark
- SAP AI: verify GA status

### Decision 6: Slide 110 fixes
- Keep C.H. Robinson, replace EU 3PL (unsourced), replace Macy's with Unilever

### Decision 7: Structural fix
- Slide 99 "SECTION 06 Legal" → merge UC-10 into Section 03

### Decision 8: UC-05 metrics softened
- "Projected: 70% review time reduction" (industry estimate, not production result)
- 45K = verification corpus, not fine-tuning training data

### Total changes required
- **Slide 3**: rewrite master architecture
- **4 Category A UC architecture slides**: fix API, mark MCP wrappers as "to build"
- **6 Category B UC sets**: restructure from 10 slides to ~6 (How They Did It + How We'd Build It)
- **5 competitive landscape slides**: update with 2026 research data
- **Slide 99**: fix section numbering
- **Slide 110**: replace unsourced references
- **All slides**: resolve template variables
- **Estimated new slide count**: ~85 (down from 111 due to Category B restructure)

## Q&A log

### Q1 — Use case identification: "Our" solution vs. case study benchmarks
- Asked: The deck mixes two categories — buildable solutions (UC-01, 02, 03, 05) using real OpenHands/MCP repos vs. case study benchmarks (UC-04, 06, 07, 08, 09, 10) using proprietary platforms (Palantir, Layer 6, COIN, DroneDeploy, LexisNexis). Should the deck separate "what we build" from "what validates the market"?
- Captured: **Yes — confirmed.** Category B use cases (UC-04, 06, 07, 08, 09, 10) should be reframed as market validation / competitive benchmarks, not "our implementation." Architecture slides for Category B should show how we'd replicate the outcome using our stack (OpenHands + MCP), not pretend the named company uses OpenHands. Category A (UC-01, 02, 03, 05) are the buildable solutions.
- Flags: All Category B architecture slides need rewrite — currently they falsely map proprietary platforms to `Agent(llm, tools, mcp_config)` pattern.

### Q2 — Category B reframe: slide structure for benchmark UCs
- Asked: For Category B UCs (TD Bank, JPMorgan, DroneDeploy, BCG, Tampa General, LexisNexis), should we restructure to: (1) Title, (2) The Problem, (3) How They Solved It, (4) Key Metrics, (5) How We'd Build It — our OpenHands+MCP architecture, (6) Competitive Positioning? Drop Governance/GitHub/Brand Voice for Category B.
- Captured: **Yes — confirmed.** Category B gets restructured: "How They Solved It" (their proprietary approach) + "How We'd Build It" (our OpenHands+MCP replication). Governance/GitHub/Brand Voice slides dropped for Category B since we're not the builder.
- Flags: 6 UCs × architecture slides need complete rewrite with honest "our approach" framing.

### Q3 — OpenHands API: core architecture claim is wrong
- Asked: The deck shows `Agent(llm, tools, mcp_config, agent_context) → Conversation(workspace, callbacks)` on every architecture slide + slide 3. Verified: actual API is `Agent(llm, tools)` with MCP at platform/TOML level, skills are markdown prompts not code bundles, no built-in domain MCP servers. Correct all slides?
- Captured: **Yes — proceed with corrections.** Fix the API signature on slide 3 and all 10 architecture slides. Mark external MCP servers as community/external. Represent skills accurately as prompt-based instructions.
- Flags: none — greenlit for implementation.

### Q4 — MCP server repos: which ones are real?
- Asked: Verifying GitHub repos cited in the deck (predictive-maintenance-mcp, mcp-maintenance-cap, open-agreements, lavern, suzielaw, anylegal-oss, claude-for-legal, machina-ai).
- Captured: **Verification complete.**
  - **EXISTS**: predictive-maintenance-mcp (52 endpoints, v0.8.0, MIT), open-agreements (25 templates), lavern (67 agents, v0.15.0, Apache 2.0), suzielaw (19 jurisdictions), anylegal-oss (12 tools, 80+ countries), claude-for-legal (12 plugins, 80+ agents, 20 MCP connectors, ~8k stars)
  - **UNCERTAIN**: mcp-maintenance-cap (user profile exists, referenced in SAP blog, repo may be private)
  - **NOT FOUND**: machina-ai on PyPI — does not exist. Must remove from deck.
- Flags: Remove `machina-ai` reference from UC-01 slide 10+11. Mark `mcp-maintenance-cap` as unverified.

### Q5 — UC-04 (Clinical AI / Sepsis): Palantir as "MCP Server"
- Asked: Slide 41 lists "Palantir Platform" as an MCP server. Palantir is proprietary, not MCP. Since UC-04 is Category B, should we reframe as benchmark-then-replicate? "Palantir built this; here's how we'd achieve similar outcomes with open infrastructure."
- Captured: **Agreed.** UC-04 architecture slide reframed: "How They Did It" (Palantir Foundry + proprietary ML) + "How We'd Build It" (OpenHands agents + FHIR R4 MCP + vitals streaming + sepsis scoring + clinician-in-the-loop). Headline "700+ lives saved" stays as market validation.
- Flags: none

### Q6 — UC-06 & UC-07 (Financial Services): proprietary stacks mapped to fake MCP servers
- Asked: UC-06 (TD Bank) uses Layer 6 + deterministic rules, not MCP servers. UC-07 (JPMorgan COIN) predates LLMs entirely — purpose-built ML since 2016. Both architecture slides show fake MCP server names. Reframe as Category B benchmarks?
- Captured: **Agreed.** Both reframed as Category B.
  - UC-06: "How They Did It" = Layer 6 + Claude + GPT + deterministic rules + human adjudicator. "How We'd Build It" = OpenHands doc-extraction agent + MCP-connected rules engine + human confirmation mode.
  - UC-07: "How They Did It" = purpose-built ML, 150-attribute extraction, 9 years of refinement. "How We'd Build It" = modern equivalent using OpenHands + document understanding models + human review loop. Honest that COIN's 9-year data flywheel is not replicable day one.
- Flags: none — greenlit

### Q7 — UC-08 & UC-09 (Construction) + Slide 99 structural bug
- Asked: DroneDeploy is proprietary (34M annotation moat, own AI agents). BCG is a consulting framework, not a product. Both have invented MCP servers. Reframe as Category B? Also: slide 99 says "SECTION 06 - Legal" but Legal was already Section 03. Fix?
- Captured: **Agreed on all three.**
  - UC-08: Category B. "How They Did It" = DroneDeploy proprietary platform + 13-year data moat. "How We'd Build It" = OpenHands vision agents + YOLOv8/OpenCV + BIM MCP + Procore API. Honest that 34M corpus is their moat.
  - UC-09: Category B. "How They Did It" = BCG consulting framework, 2 pilots. "How We'd Build It" = lighter CV stack, risk detection + progress tracking as services play.
  - Slide 99: Fix section numbering — UC-10 goes under Section 03 (Legal), not a new Section 06.
- Flags: none

### Q8 — UC-01 (PdM): machina-ai doesn't exist on PyPI
- Asked: `machina-ai` cited on slides 10-11 does not exist on PyPI. Remove? Keep predictive-maintenance-mcp (verified), mark mcp-maintenance-cap as "SAP Community PoC."
- Captured: **Agreed.** Remove machina-ai entirely. Keep predictive-maintenance-mcp as primary (verified, 52 endpoints, v0.8.0). Mark mcp-maintenance-cap as "SAP Community PoC" not production. No cross-wiring of repos across industries.
- Flags: none

### Q9 — UC-03 (Patient Intake): FHIR/Twilio/Calendly MCP servers are aspirational
- Asked: FHIR R4 MCP, Twilio MCP, Calendly MCP listed with specific endpoints but no actual repos exist. These are wrapper concepts around real APIs. Mark as "to be built" since UC-03 is Category A?
- Captured: **Agreed.** Keep the MCP server designs (endpoints are plausible and well-scoped) but mark them as "wrapper MCP servers — to be built" rather than implying they ship today. The underlying APIs (FHIR R4, Twilio, Calendly) are real. The MCP wrapper layer is our value-add / implementation deliverable.
- Flags: none

### Q10 — UC-02 (Visual QI): vision-pipeline MCP and sap-mes MCP also aspirational
- Asked: Same pattern as UC-03 — vision-pipeline MCP (5 endpoints) and sap-mes MCP (4 endpoints) are well-designed but don't exist as repos. GitHub repos listed (ultralytics, opencv, TensorRT) are ingredients, not MCP servers. Mark as "to be built"?
- Captured: **Agreed.** Same treatment as UC-03. Mark as "wrapper MCP servers — to be built." The endpoint designs stay (they're the implementation spec). GitHub repos are ingredients. Be explicit: "MCP wrappers to be built over these foundations."
- Flags: none

### Q11 — UC-05 (Legal Contract Review): strongest UC but metrics need softening
- Asked: UC-05 has the richest verified toolchain (open-agreements, lavern, suzielaw, claude-for-legal, anylegal-oss all exist). But: (1) "40hrs→12hrs, $2.4M, 99.1% accuracy" sourced from DreamzTech blog, not independent study. (2) "45K-contract training" may conflate fine-tuning with verification corpus — lavern uses debate protocol, not fine-tuned model. Soften to "projected" estimates?
- Captured: **Agreed.** Keep the architecture (strongest UC). Soften metrics: "Projected: 70% review time reduction" rather than stated fact. Attribute DreamzTech as "industry estimate" not "production result." Clarify 45K number as verification corpus for the debate protocol, not fine-tuning training data.
- Flags: none

### Q12 — UC-10 (LexisNexis): Forrester ROI number + Category B reframe
- Asked: Deck says 284% ROI (Forrester TEI June 2025). Newer research found 344% ROI for comparable legal AI. Keep 284% for Lexis+ specifically, add 344% as market benchmark? Also: UC-10 architecture lists proprietary LexisNexis products as MCP servers — since Category B, "How We'd Build It" should reference suzielaw + lavern + claude-for-legal.
- Captured: **Agreed.** Keep 284% as the Lexis+ AI specific Forrester number. Add 344% as contextual market benchmark without mixing. UC-10 reframed as Category B: "How They Did It" = LexisNexis proprietary corpus + Protege platform. "How We'd Build It" = suzielaw (19 jurisdictions) + lavern (67-agent debate) + claude-for-legal (12 plugins) as the open-source equivalent stack.
- Flags: none

### Q13 — Slide 3 (Master Architecture): corrected version
- Asked: Replace wrong API signatures with verified ones. Split MCP servers into Verified vs To Build. Fix skills description from "code bundles" to "markdown prompts."
- Captured: **Agreed.** Corrected slide 3:
  - ORCHESTRATION: `Agent(llm, tools) → Conversation(agent, workspace, plugins)`
  - MCP CONFIG: platform-level `config.toml` under `[mcp]` — SSE, HTTP, or stdio
  - MCP SERVERS split: **Verified** (predictive-maintenance-mcp, open-agreements, lavern, suzielaw, claude-for-legal) vs **To Build** (FHIR wrapper, Twilio wrapper, SAP MES wrapper, vision-pipeline wrapper)
  - SKILLS: `SKILL.md markdown prompts with keyword triggers → domain instructions`
  - USER LAYER and SYSTEM OF RECORD: unchanged (correct as-is)
- Flags: none

### Q14 — Completeness check: three remaining issues
- Asked: (1) `{{brand_name}}` and `{{tagline}}` template variables on brand voice slides — resolve or keep? (2) Competitive landscape data stale — e.g., Harvey AI now $11B/$300M ARR. (3) Slide 110 references C.H. Robinson and EU 3PL which aren't in the 10 UCs.
- Captured: **All three need attention.**
  1. Template variables: need resolution (covered in Q15)
  2. Competitive landscape: needs updating with research data (covered in Q16)
  3. Slide 110: needs review of external references (covered in Q17)
- Flags: none

### Q15 — Template variables: brand_name and tagline
- Asked: `{{brand_name}}` and `{{tagline}}` appear on every slide. Hard-code or parameterize? What values?
- Captured: **Brand name = contextual per deck purpose.** Since this deck is research-driven pre-sales intelligence, not a branded client deliverable:
  - `brand_name` = to be set based on deck context (e.g., "AI Market Research" for this deck)
  - `tagline` = derived per industry/use case, not a fixed brand tagline
  - Approach: parameterize via env vars for reuse, with sensible defaults per deck type
  - For this specific deck: brand_name = "AI Market Research", tagline = per-industry contextual lines
- Flags: none — taglines defined below

**Per-industry taglines (confirmed):**
- Manufacturing: "Where predictive beats reactive — and the data already exists"
- Healthcare: "Automate the paperwork, augment the clinician"
- Legal: "67 agents debating so lawyers can judge"
- Financial Services: "Let LLMs read, let rules compute, let humans decide"
- Construction: "The camera doesn't get tired. The superintendent acts on data."
- Closer (slide 111): "10 use cases. 5 industries. One honest architecture."
- brand_name = "AI Market Research"

### Q16 — Competitive landscape slides stale — update with research data
- Asked: Harvey AI now $11B/$300M ARR (deck says "$100K+/yr enterprise only"). CoCounsel now 20K+ firms (deck says "no agent architecture"). Update all competitive slides with verified 2026 numbers?
- Captured: **Agreed.** Update competitive slides:
  - Harvey AI: $11B valuation, $300M ARR, 142K lawyers, 50% of Am Law 100, 1,500+ customers in 60+ countries
  - CoCounsel: 20,000+ firms, 5-8 hrs/day saved per attorney, research time cut 80%
  - LexisNexis: add 344% ROI (Forrester) as additional market benchmark
  - SAP AI: verify if now GA (was Q2-Q3 2026 target)
  - Keep "our approach" positioning but with honest competitor descriptions that a knowledgeable buyer wouldn't dismiss
- Flags: SAP AI GA status needs verification

### Q17 — Slide 110 ("What Winners Have in Common"): external references
- Asked: Slide cites C.H. Robinson, EU 3PL (92% vs 78% composite), and Macy's — none are among the 10 UCs. Keep, replace, or source?
- Captured: **Agreed.**
  - C.H. Robinson: keep — strong external benchmark with verified data (30+ agents, 3M tasks, 35% productivity)
  - EU 3PL "92% composite vs 78% pure agentic": replace — unsourced, reads as invented. Substitute with a sourced number from one of the 10 UCs (e.g., TD Bank's deterministic+LLM split, or Unilever's 92% accuracy with composite sensor+ML approach)
  - Macy's: replace with Unilever's 6-month trust-building phase (already in UC-01, well-documented)
- Flags: need to find a sourced "composite beats pure LLM" data point from the 10 UCs

## Open flags (pending input)
- OpenHands API verification → **COMPLETED — critical corrections found** (see below)
- GitHub repo verification for all cited MCP servers → needs web search

### OpenHands Fact-Check Results (verified 2026-06-08)

**WRONG in deck — must fix:**
1. `Agent(llm, tools, mcp_config, agent_context)` is WRONG. Actual: `Agent(llm: LLM, tools: list[Tool])`. `mcp_config` is NOT an Agent param. `agent_context` is a property on AgentBase, not a constructor arg.
2. `Conversation(workspace, callbacks)` is WRONG. Actual: `Conversation(agent, workspace, plugins=None, persistence_dir=None, conversation_id=None, callbacks=None, ...)`.
3. MCP config lives at platform/TOML level (`config.template.toml` under `[mcp]`), not passed to Agent or Conversation.
4. Skills are **markdown prompt files** with keyword triggers, NOT "reusable vertical code bundles." Do not describe them as packaged bundles.
5. No built-in domain MCP servers exist in OpenHands. No SAP, FHIR, or legal servers. Only Tavily search is auto-mounted.

**CORRECT in deck:**
- Plugin system exists (marketplace flow, `plugin.json`, merges skills+hooks+MCP)
- MCP integration is first-class (SSE, Streamable HTTP, stdio transports)
- Headless/CLI execution confirmed (confirmation_mode, CI/CD pipelines)
- Docker sandbox is default runtime; Kubernetes also supported
- Conversation manages lifecycle (run/pause/close), state, security
