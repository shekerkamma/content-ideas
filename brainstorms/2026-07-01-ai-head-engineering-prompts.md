# AI Head of Engineering Prompt System: Brainstorm / Discovery Notes
Date: 2026-07-01 · Goal: Extract prompt patterns from the referenced article and turn them into Hermes skills contextualized to Sheker's automotive / enterprise POC work.

## Structured context
- **Topic type**: strategy
- **Topic string**: Prompt patterns for Hermes skills tailored to enterprise solution architecture and automotive GenAI POCs
- **Entities**: Sheker, Hermes, GBrain, Notion article "The AI Head of Engineering"
- **Prospect/account**: n/a
- **Target buyer**: enterprise solution architect / internal POC operator
- **Verticals**: automotive, enterprise software, manufacturing
- **Open decisions**: which prompt families to convert first; whether these should become reusable Hermes skills, profile instructions, or both; which outputs need GBrain write-back

## Summary / key decisions
- Need to extract the article's prompt patterns and turn them into contextualized Hermes skills for Sheker's actual work.
- Skills should reflect the user's standards: real data, business value, architecture, cost/latency, stakeholder-ready output.
- You.com search surfaced the underlying Notion pattern even though the exact private URL is not indexed:
  - main instructions page as a light boot sequence
  - Roles database
  - Skills database
  - Resources database
  - Memory database
  - Dispatch table
  - routing chain: Dispatch Table -> Role -> Skill Tree -> Skill -> Reference Library -> Resources
- Public search results show adjacent role pages for Prompt Engineer, Product Manager, Engineering Manager / Growth Frameworks for Engineers, Staff Engineer, DevOps Engineer, and Technical Support Engineer.
- User supplied the actual role list for the "AI Head of Engineering" concept:
  - Scope Killer
  - 30-Day Scope Architect
  - Stack Picker
  - Build vs Buy Auditor
  - Build Estimator
  - AI Use-Case Validator
  - Custom Internal Tool Designer
  - Pre-Launch Auditor
  - 30-Day Build Roadmap
- These roles should be translated into Hermes skills tied to enterprise/automotive POCs rather than generic founder app advice.
- Role prompt notes are being captured one by one as the user provides them.

## Role notes

### Role #1 — Scope Killer
- Replaces the paid MVP scope review session used to rightsize the build.
- Goal: cut every feature that will not ship in 30 days.
- Output per feature: feasibility score `0-10`, decision `CUT / KEEP / DEFER`, one-line reasoning.
- Cut rules: polish, 3+ dependencies, vague specs, not tied to core value, admin/settings/export unless core product.
- Keep rules: core wow, monetization, trust/legal/security basics.
- Final outputs: 80/20 cut list, one-line MVP statement, and the 3 founder-favorite features that still get cut.
- Operational note: the operator should challenge the user on the real user action behind the “wow moment,” not the marketing phrasing.

### Role #2 — 30-Day Scope Architect
- Replaces the paid discovery/scope-doc phase.
- Goal: turn the MVP statement plus kept features into a 1.5-2 page scope spec.
- Required sections: `IN SCOPE`, `OUT OF SCOPE`, `MILESTONES`, `DECISIONS OWED BY FRIDAY`, `ASSUMPTIONS`, `DEFINITION OF DONE`.
- Milestones are week-by-week: foundation, core build, payment/integrations, polish/launch.
- OUT OF SCOPE must be ruthless; if it can wait for v1.1, it is out.
- Definition of Done must be testable, not vague: signup + first action, smoke test, payment test, etc.
- Operator note: surface hidden assumptions explicitly instead of assuming auth, Stripe, design, or implementation details are already solved.

### Role #3 — Stack Picker
- Replaces the paid architecture consultation before quoting.
- Goal: pick the tech stack for a 30-day MVP with explicit trade-offs.
- Per layer output: choice, 2 alternatives, reasoning.
- Layers called out: frontend, backend, database, auth, payments, email, hosting, analytics.
- Default stack unless a reason exists to change it: `Next.js + Supabase + Stripe + Resend + Vercel`.
- Reasoning must cover cost, ramp time, and vendor lock-in.
- Flag any option that adds 5+ days of ramp time to the 30-day build.
- Operator note: optimize for the fastest stack the team can actually ship, not the trendiest stack.

### Role #4 — Build vs Buy Auditor
- Replaces hidden strategy work inside SOWs.
- Goal: decide `BUILD / BUY / HYBRID` for each feature with 3-year cost math.
- For each feature, compare build, buy, and hybrid in terms of cost, data ownership, ship time, switching cost, and maintenance.
- Default integrations to buy: auth, payments, transactional email, file storage, search.
- Flag when buy requires 6+ weeks of integration or when build creates avoidable lock-in.
- Operator note: include integration burden explicitly; cheap software that takes weeks to wire is not cheap.

### Role #5 — Build Estimator
- Replaces the estimation phase.
- Goal: estimate each feature in hours and dollars for a Next.js + Supabase MVP.
- Per feature output: build hours low/high, dollar cost at a blended rate, confidence, and 3 risks that could blow the estimate.
- Breakdown per feature: frontend, backend, integration, testing, polish.
- Roll-up output: total range, single biggest overrun risk, single likely under-run.
- Flag when total exceeds `160 hours` and identify what gets cut to ship in 30 days.
- Operator note: apply a real multiplier to auth, payments, and webhooks; docs-time is not shipped-time.

### Role #6 — AI Use-Case Validator
- Replaces the AI consulting engagement that decides whether AI belongs in the feature.
- Goal: decide whether the use case is a good fit for AI and which pattern to use.
- Output includes an `AI FIT SCORE (0-30)` across task structure, verifiability, failure tolerance, cost per call, latency tolerance, and hallucination risk.
- Pattern choices: LLM-only, LLM + RAG, LLM + tools, LLM + agent loop, or `DON'T USE AI`.
- Model recommendation must name the model family and cost estimate per 1,000 uses.
- Must list 3 production failure modes and the minimum eval set before launch.
- Operator note: if a rules system or lookup table solves it, do not force AI into the stack.

### Role #7 — Custom Internal Tool Designer
- Replaces the custom software design phase for internal tools.
- Goal: design a CRM, dashboard, or workflow tool around the actual business motion.
- Required sections: data model, UI structure, roles + permissions, automation triggers, integrations, and `NOT IN THIS TOOL`.
- Data model must use business-specific fields, not generic SaaS defaults.
- UI should focus on the 3 most-used screens and bulk actions.
- Roles section must expose approval flows and audit requirements.
- Operator note: ask who decides X for each action so the hidden approval flow becomes explicit.

### Role #8 — Pre-Launch Auditor
- Replaces the QA + security audit before launch.
- Goal: audit the build before anyone is told it launched.
- Required checks: edge cases, security gaps, production readiness, and launch-gate smoke test.
- Edge cases should span the build and include empty state, error state, slow network, double-clicks, auth boundary, invalid input, and browser refresh/back mid-flow.
- Security gaps should explicitly test auth bypass, direct API access, RLS gaps, webhook verification, secrets exposure, and SQL injection vectors.
- Production readiness must check env vars, Stripe secrets, email deliverability, backups, error monitoring, and uptime monitoring.
- Operator note: do not announce launch until the real-money smoke test and access boundary tests pass.

### Role #9 — 30-Day Build Roadmap
- Replaces the project management retainer.
- Goal: map the 30-day sprint week by week with Friday deadlines and rollback triggers.
- Required sections: week-by-week plan, dependency map, Friday demos, rollback plan, minimum lovable product if the schedule compresses.
- Each Friday is a gate, not a loose milestone.
- Week 1 should be constrained because setup and environment work consume more time than founders expect.
- Operator note: if Week 2 is already drifting, the roadmap should be killed or reset rather than pretending the plan is still real.

## Setup guide / operating sequence
- Inputs required: Claude account, a workspace to save outputs, and about 90 minutes to run the first 3 roles end-to-end.
- Workflow: open Claude, paste each role prompt, fill the bracketed placeholders, save each output as a markdown file, and feed the previous output into the next role.
- Sequence matters:
  1. Scope Killer
  2. 30-Day Scope Architect
  3. Stack Picker
  4. Build vs Buy Auditor
  5. Build Estimator
  6. AI Use-Case Validator
  7. Custom Internal Tool Designer
  8. Pre-Launch Auditor
  9. 30-Day Build Roadmap
- The `Where Claude breaks` sections are part of the useful content and should be read before running each prompt.

## Q&A log

## Open flags (pending input)
- What exact prompt families from the article should be converted first? -> user
- Need the article text if it materially affects the extraction -> source read / user
- Notion page text not yet accessible from the public URL/search -> user export or linked subpages
- `NOTION_API_KEY` is unset in this session and the page is not shared to a visible integration -> user to wire access or provide export
- Need to decide whether to build a general role-prompt skill pack or separate skills per role family -> user
- All 9 roles captured. Ready to synthesize into Hermes skill notes or a skill pack.
