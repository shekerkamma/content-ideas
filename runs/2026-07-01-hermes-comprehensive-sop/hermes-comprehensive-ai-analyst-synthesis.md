# Hermes Comprehensive Use Cases + Realization SOP

## Goal Contract
- Outcome: client-ready PPTX that explains Hermes architecture, integration components, persona/config files, and implementation SOPs for a comprehensive use-case catalog.
- Artifacts: synthesis markdown, generated PPTX, preview QA artifacts, copied Windows Desktop deck.
- Constraints: use local Hermes files, setup PDF, YouTube /watch evidence, You.com discovery, and branded PPTX workflow.
- Acceptance criteria: 100+ slides; comprehensive use cases; architecture and solution components per use case; search-tool policy included; deck QA performed.
- Research mode: local files first, You.com official/current docs, video transcript and frames, setup PDF.
- Loop budget: 3 passes: synthesis, render, QA/fix.

## Chain Contract
| Step | Skill/action | Consumes | Produces | Next consumer | Value test |
|---|---|---|---|---|---|
| 1 | watch | YouTube URL | transcript + frames | synthesis | captures live demo setup |
| 2 | you-com-search | Hermes/You API queries | source JSON | synthesis | current official docs and pricing corrections |
| 3 | ai-analyst | source pack | validated synthesis | branded deck | converts raw evidence into structure |
| 4 | branded-pptx-deck | synthesis | PPTX + QA | user | client-ready artifact |
| 5 | goal-loop-orchestrator | chain outputs | QA decisions | final | proves skills compounded |

## Source Inventory
- Hermes setup PDF extracted to sources/Hermes-Agent-Setup-Google-Docs.txt.
- YouTube /watch output: video.en.vtt, 80 frames, contact sheet.
- Local Hermes files: config.yaml extracts, SOUL.md, USER.md, MEMORY.md, cron jobs, skills inventory.
- You.com search outputs: you_search_hermes_architecture.json and you_search_you_api.json.
- Official Hermes user-stories page fetched to sources/hermes_user_stories.html.

## Important Correction
The setup PDF says livecrawl extraction is bundled into the base You.com Search API price. Current You.com docs found during this run state that livecrawl is billed separately from the base Search API call. The deck treats pricing as current-doc dependent and avoids using the older claim unqualified.

## Hermes URLs Found
- https://hermes-agent.nousresearch.com/docs/
- https://blakecrosley.com/guides/hermes
- https://hermes-agent.nousresearch.com/docs/user-guide/profiles
- https://hermes-agent.nousresearch.com/docs/user-guide/configuration
- https://lumadock.com/tutorials/hermes-memory-architecture-explained
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/profiles.md
- https://www.mindstudio.ai/blog/hermes-agent-5-pillar-architecture-memory-skills-soul-crons
- https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent
- https://www.dailydoseofds.com/p/hermes-agent-masterclass/
- https://www.mindstudio.ai/blog/hermes-agent-five-pillars-memory-skills-soul-crons

## You.com URLs Found
- https://you.com/docs/welcome
- https://you.com/docs/search/overview
- https://docs.you.com/search/overview
- https://you.com/docs/quickstart
- https://documentation.you.com/quickstart
- https://docs.you.com/api-reference/search/v1-search
- https://documentation.you.com/api-reference/search
- https://you.com/docs/api-reference/search/v1-search
- https://you.com/resources/research-api-by-you-com
- https://you.com/docs/guides/research

## Video Evidence Highlights
- 00:02:28: cybersecurity company Aconyx. I've now
- 00:03:50: on Hermes, which is the agent I'm
- 00:04:47: agents. So, Open Claw, Hermes, Think
- 00:04:54: Um it's got some better security,
- 00:05:39: Um and uh currently I'm running Hermes,
- 00:08:29: and receive emails, and run your
- 00:16:23: instructions to install the Hermes
- 00:16:31: install Hermes, you can install open
- 00:16:53: I think Hermes is the is the winner
- 00:17:06: thing that I recommend is this Hermes
- 00:17:31: skills and like all of these other
- 00:17:48: Hermes and to use Hermes. And so I I
- 00:19:10: actually going to stay outside of Hermes
- 00:19:19: interface on desktop to Hermes.
- 00:19:41: is this Hermes agent setup. Again, you
- 00:20:04: with my Hermes agent. Okay. Yeah, I'm I
- 00:20:26: far, every time I've installed Hermes,
- 00:20:46: known as a search API. These agents are
- 00:21:10: ones that Hermes recommends by default.
- 00:21:35: my setup uh is this thing called Gbrain,
- 00:21:38: okay? So, Gbrain is
- 00:22:10: all of my email and and Slack and um
- 00:22:19: Zoom, where there's data about people
- 00:22:52: it's my Hermes agent. It runs on another
- 00:23:01: is a piece of software called Obsidian.
- 00:23:04: documents. And Obsidian is
- 00:23:33: and so G brain powers all of this. It
- 00:23:58: on Twitter.
- 00:24:10: LinkedIn and Twitter and email and
- 00:24:40: Okay. So anyway, so G brain is a big
- 00:24:46: into your agent into your Hermes and
- 00:25:07: smart contacts. It ingest my email,
- 00:25:10: calendar, Zoom, Twitter, LinkedIn,
- 00:25:19: about them than they found in my email
- 00:25:21: or they found on Twitter and they found

## Use Case Catalog
### UC01. Daily Executive Brief
- Outcome: One morning packet replaces scattered checking across email, calendar, Slack, news, and social feeds.
- Trigger: Scheduled cron or user asks for today's brief
- Components: Cron scheduler, You.com Search/Research, GBrain recall, Calendar/email connectors, Messaging gateway
- Acceptance: Brief includes meetings, risks, asks, and sources.; No outbound action occurs without explicit approval.; Missed-source rate is tracked weekly.
### UC02. Smart Contacts And Entities
- Outcome: A self-updating relationship layer gives Hermes context before meetings and outreach.
- Trigger: New meeting, email thread, or entity mention
- Components: GBrain graph, Obsidian, You.com Research, Entity extraction skill, Dedup/fuzzy matching
- Acceptance: Each profile has source provenance.; Duplicates are merged or flagged.; Agent can answer why a contact matters.
### UC03. Pre-Call Account Brief
- Outcome: Every meeting starts with account context, current signals, and a proposed conversation plan.
- Trigger: Calendar event within next 24 hours
- Components: Calendar connector, You.com Search, GBrain recall, Zoom transcript store, Brief template
- Acceptance: Brief has attendee map, account context, open asks, and risks.; Recent external facts are dated.; Sensitive assumptions are labeled.
### UC04. Investor Intelligence And Outreach Tracker
- Outcome: Fundraising research becomes a live investor map with thesis match, hooks, and follow-up state.
- Trigger: Seed raise, pipeline refresh, investor reply
- Components: You.com Research, Finance Research, Spreadsheet writer, Email drafting, Inbox monitor
- Acceptance: Rows include source URLs and confidence.; Drafts are personalized, not spam templates.; Follow-up cadence respects human approval.
### UC05. Relationship Manager And Coach
- Outcome: The agent nudges relationship maintenance based on real context, not a static CRM reminder.
- Trigger: No contact for N days or important public signal
- Components: GBrain graph, You.com Search, Signal monitor cron, Drafting skill
- Acceptance: Recommendations cite the trigger.; No message is sent without approval.; User feedback tunes future ranking.
### UC06. Social And News Signal Monitor
- Outcome: Hermes filters the information flood into a few signals worth acting on.
- Trigger: Hourly/daily cron or explicit research request
- Components: You.com Search, Reddit skills, YouTube watch/video skill, Cron, Topic taxonomy
- Acceptance: Digest separates fact, inference, and recommendation.; Sources are current and linked.; Repeated noise is suppressed.
### UC07. Twitter/X Engagement Radar
- Outcome: The agent identifies high-value conversations and prepares replies without consuming the user's day.
- Trigger: New signal from monitored accounts/topics
- Components: Browser/computer-use for logged-in access, You.com Search, Social skill, Approval queue
- Acceptance: Queue contains rationale per reply.; Human can approve, edit, or reject.; Rejected styles are learned.
### UC08. LinkedIn Relationship And Posting Assistant
- Outcome: Hermes can work around limited LinkedIn API access by using browser-based workflows carefully.
- Trigger: User asks for LinkedIn prep or scheduled review
- Components: Computer-use/browser, You.com Search, GBrain, Content drafting skill
- Acceptance: Every action is reversible or approved.; No private data leaks into public posts.; Drafts match user's voice.
### UC09. Content Intelligence Blog Pipeline
- Outcome: The MindStudio-style blog system turns AI-news monitoring into high-volume SEO/AEO content.
- Trigger: Daily content run
- Components: YouTube transcript skill, You.com Search/Research, Content writer, Ad generator, CMS connector
- Acceptance: Posts cite research sources.; No duplicate thin content.; Performance feeds next topic selection.
### UC10. YouTube Video Research Weekly Job
- Outcome: A plain-English cron can turn video monitoring into recurring research briefs.
- Trigger: Every Monday 9am or user-defined schedule
- Components: Watch-video skill, Cron, You.com Search, Frame archive, Research template
- Acceptance: Timestamped evidence is retained.; Claims are verified or labeled unverified.; Long videos are focused when needed.
### UC11. SEO And AEO Content Variant Factory
- Outcome: Hermes can generate many search-answer variants while preserving source discipline.
- Trigger: New topic, product launch, or content refresh
- Components: You.com Search, Firecrawl/Contents, Content skill, AEO evidence skills, CMS
- Acceptance: Each claim maps to source.; No invented metrics.; Variant purpose is explicit.
### UC12. Cost And Model Spend Scan
- Outcome: Daily cost inspection prevents autonomous agents from becoming expensive background noise.
- Trigger: Nightly cron or threshold breach
- Components: Cron, Cost parser, Activity-dependent model policy, Config editor, Alert delivery
- Acceptance: Dashboard itemizes spend.; Recommendations include risk.; Changes are versioned.
### UC13. Activity-Dependent Model Routing
- Outcome: Hermes chooses model strength based on task type instead of running everything on the most expensive model.
- Trigger: Any task start or subtask classification
- Components: Model selector skill, Fallback provider chain, Config.yaml, Cost monitor
- Acceptance: Route is visible in logs.; Premium model use has reason.; Fallbacks are tested.
### UC14. Security And Permissions Audit
- Outcome: The agent should inspect its own risk surface before it expands capability.
- Trigger: Daily cron, new integration, or profile export
- Components: Security audit skill, Config parser, Secret redaction, Cron scanner, MCP inventory
- Acceptance: Secrets are masked.; High-risk changes require approval.; Audit result is dated and stored.
### UC15. MCP And Plugin Health Monitor
- Outcome: The agent watches its tool layer so workflows fail loudly instead of silently degrading.
- Trigger: Scheduled healthcheck or failed tool call
- Components: MCP health skill, Plugin inventory, Tool-search policy, Alert channel
- Acceptance: Report lists affected workflows.; No install runs without approval.; Fallback path is documented.
### UC16. Cross-Channel Data Ingestion
- Outcome: Hermes turns email, Slack, calendar, Zoom, and files into a unified context stream.
- Trigger: Scheduled ingestion or new artifact
- Components: Connectors, Transcript processor, Entity extractor, GBrain write-back, Dedup logic
- Acceptance: Source coverage is tracked.; Private data stays local unless approved.; Duplicates and conflicts are flagged.
### UC17. GBrain Dreaming And Knowledge Compaction
- Outcome: Nightly memory maintenance keeps the knowledge graph clean enough to trust.
- Trigger: Nightly cron or large ingestion batch
- Components: GBrain service, Git-backed Markdown, Dream cron, Conflict detector
- Acceptance: Changes are inspectable.; Conflicts are not silently overwritten.; Graph becomes easier to query.
### UC18. Obsidian Graph Visualization
- Outcome: A visual graph helps humans inspect and correct what the agent believes.
- Trigger: User opens knowledge review or entity audit
- Components: Obsidian, GBrain vault, Markdown schemas, Graph filters
- Acceptance: Graph nodes map to real notes.; Human edits are preserved.; Agent can cite edited notes.
### UC19. Phone-To-App Builder
- Outcome: The agent can build or modify small tools while the user is away from the workstation.
- Trigger: Mobile message asks for app/tool/workflow
- Components: Messaging gateway, Coding agent/proxy, GitHub skills, Playwright/dogfood QA
- Acceptance: Artifact runs locally.; Tests or smoke checks pass.; Changes are summarized with file paths.
### UC20. Code And Repo Self-Improvement
- Outcome: Hermes captures repeated workflows as skills and improves its own operating procedures.
- Trigger: Repeated successful task pattern
- Components: Skill creator, Curator, Goal-loop orchestrator, Repo skill root
- Acceptance: Skill has trigger, dependencies, and verification.; It consumes/produces concrete artifacts.; It is discoverable in target hosts.
### UC21. Back-Office Browser And Desktop Automation
- Outcome: Hermes can use browser and computer-use tools when APIs are absent.
- Trigger: User asks for repetitive web/native app work
- Components: Browser toolset, Computer-use, Dogfood QA, OCR/document skill
- Acceptance: Screenshots or logs prove completion.; No hidden irreversible action.; User can replay SOP.
### UC22. Spreadsheet And Document Automation
- Outcome: Hermes can turn rough research or operating data into structured spreadsheets and documents.
- Trigger: User requests tracker, report, or transformation
- Components: Spreadsheet connector, Document parser, You.com enrichment, Export skill
- Acceptance: Rows have provenance.; Formulas calculate correctly.; Deck/report can consume the table.
### UC23. Team Or Company GBrain
- Outcome: A shared memory graph can support a whole team while preserving profile and permission boundaries.
- Trigger: Team wants shared knowledge layer
- Components: GBrain server, Hermes profiles, MCP auth, Git-backed vault, Access policy
- Acceptance: Shared facts have owners.; Sensitive memories are scoped.; Profiles can be packaged safely.
### UC24. Multi-Profile Role Agents
- Outcome: Profiles replace one giant assistant with role-specific agents that can be packaged and reused.
- Trigger: Need assistant, researcher, PM, engineer, or sales profiles
- Components: Hermes profiles, SOUL.md, Profile descriptions, Skill packages, Cron
- Acceptance: Profile is discoverable.; Credentials stay local.; Role-specific behavior is observable.
### UC25. Messaging Gateway Assistant
- Outcome: Telegram, WhatsApp, Discord, or Slack can become the interface to Hermes.
- Trigger: Message arrives through gateway
- Components: Gateway config, Channel prompts, Media handling, Cron delivery, Approval policy
- Acceptance: No secrets typed into chat.; Large artifacts are linked or delivered safely.; Channel noise stays controlled.
### UC26. Kanban And Multi-Agent Work Board
- Outcome: A board can turn vague tasks into specs and route them to the right profile.
- Trigger: New backlog item or triage card
- Components: Hermes dashboard/kanban, Specifier model, Profiles, Goal-loop orchestrator
- Acceptance: Every card has acceptance criteria.; Output artifacts are attached.; Blocked cards show reason.
### UC27. Finance Research And Deal Diligence
- Outcome: You.com Finance Research can ground investor, company, and market questions in financial indexes.
- Trigger: Investor prep, market scan, diligence question
- Components: You.com Finance Research, Spreadsheet tracker, Citation verifier, GBrain write-back
- Acceptance: Citations are present.; Numbers have dates.; Risks and uncertainties are explicit.
### UC28. Deep Market Research Agent
- Outcome: Hermes can run multi-step market research without forcing the user to manage every query.
- Trigger: Strategic question or market scan
- Components: You.com Research, Exa/Firecrawl fallback, GBrain recall, AI analyst validation
- Acceptance: Report lists source URLs.; Confidence is labeled.; Decision options are concrete.
### UC29. Customer And Community Signal Triage
- Outcome: Community threads, support issues, and Reddit signals become a product-opportunity queue.
- Trigger: Scheduled community scan
- Components: Reddit skills, You.com Search, Factcheck workflow, Opportunity scorer
- Acceptance: Pain points include source snippets/URLs.; Claims are fact-checked.; Actions are assigned owners.
### UC30. Automotive POC Factory Agent
- Outcome: Hermes should be tuned to Sheker's real standard: demo on real data, architecture, cost, and business deck.
- Trigger: New automotive GenAI POC request
- Components: USER.md policy, GBrain recall, Architecture-presentation, Draw.io, Branded PPTX
- Acceptance: Live demo runs on realistic data.; Architecture is production-aware.; Deck explains ROI and path to scale.
### UC31. Skill Dependency Hardening
- Outcome: Search-capable skills should prefer wired search tools instead of drifting to generic web search.
- Trigger: Skill creation/update or audit
- Components: Goal-loop orchestrator, You.com skill, Exa/Firecrawl skills, Reddit skills, Skill auditor
- Acceptance: Search dependencies are explicit.; Generic search is fallback only.; Skills produce downstream-ready artifacts.
### UC32. Open Source Agent Evaluation Lab
- Outcome: Hermes can compare OpenClaw, Hermes, NanoClaw, and custom harnesses against real workflows.
- Trigger: New personal-agent framework appears
- Components: You.com Search, GitHub skill, Dogfood tests, Cost monitor, Benchmark rubric
- Acceptance: Matrix shows evidence.; Recommendation includes tradeoffs.; Tests are reproducible.
