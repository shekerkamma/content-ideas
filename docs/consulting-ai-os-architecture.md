# Consulting AI OS — Solution Architecture

Mission pipeline: **Acquire → Transform → Operationalize → Generate** consulting
intelligence. This document maps the engine list onto the existing stack
(skills, GBrain, pipeline-runner, branded deck workflow), defines the one new
core artifact — the **domain context pack** — and walks the canonical test case
end-to-end: *"provide AI strategy for [niche area]."*

Companion docs: `docs/ai-os-blueprint.md` (Four C's foundation),
`consulting-os/` (kernel skeleton, pack template, runbooks).

---

## 1. Architecture principle

The system is **not** eleven new things to build. Most engines already exist as
skills; what's missing is the layer that makes consulting output *repeatable
per domain*: pre-engineered context. A strategy brief is only as good as the
context loaded before synthesis. So the unit of investment is the **domain
context pack** — a versioned folder of curated, source-verified consulting
intelligence per domain — and every engine is defined by how it reads or
writes packs.

```
                      ┌─────────────────────────────────────────────┐
                      │                  KERNEL                      │
                      │   CLAUDE.md router + skill registry +        │
                      │   domain classification                      │
                      └──────┬───────────────────────────┬──────────┘
        ACQUIRE              │ TRANSFORM                 │ GENERATE
┌────────────────────┐ ┌─────▼──────────────────┐ ┌──────▼─────────────────┐
│ Acquisition Engine │ │ Transformation Engine  │ │ Output Engine          │
│ content-research   │ │ graphify / second-brain│ │ branded-pptx-deck      │
│ /watch, firecrawl  │─▶ GBrain write-back      │ │ ai-strategy-researcher │
│ Exa, scrape, feeds │ │ pack curation          │ │ drawio, visualizer     │
└────────────────────┘ └─────┬──────────────────┘ │ comms-drafter          │
                             │                    └──────▲─────────────────┘
                       ┌─────▼──────────────────┐        │
                       │ CONSULTING CONTEXT     │        │
                       │ ENGINE (the new core)  │────────┘
                       │ domain packs +         │  OPERATIONALIZE
                       │ GBrain recall +        │
                       │ engagement context     │
                       └─────┬──────────────────┘
                             │
                  ┌──────────▼──────────────┐
                  │ Proposal Engineering    │
                  │ presales-deal-prep,     │
                  │ vertical-scorer,        │
                  │ contract-reviewer       │
                  └─────────────────────────┘

  Cross-cutting: Agent Runtime (Claude Code/Codex harness, subagents)
                 Memory System (GBrain + memory files + Obsidian)
                 Governance (QA gates, delivery status, keys-not-prompts)
                 Testing Framework (pack lint, golden-question evals)
```

---

## 2. Engine → implementation mapping

| Engine | Status | Implementation |
|--------|--------|----------------|
| **Kernel** | reuse + extend | CLAUDE.md router + `consulting-os/README.md` routing tree. Owns: request intake, domain classification dispatch, engagement folder creation. |
| **Acquisition Engine** | reuse | `content-research`, `/watch`, `firecrawl`, Exa MCP, `scrape-creators`, content-ideas feed. New: each pack declares its **source watchlist** so acquisition runs are targeted, not ad hoc. |
| **Transformation Engine** | reuse + extend | `graphify`, `second-brain`, GBrain write-back. New responsibility: **pack curation** — raw research → structured pack sections with source citations and a freshness date. |
| **Domain Classification Engine** | build (small) | A routing step in the kernel runbook: classify request → 1 primary + ≤2 secondary domains → load those packs. Keyword + semantic match against pack manifests; ambiguity goes to the user as a question, never guessed silently. |
| **Consulting Context Engine** | **build (the core)** | `consulting-os/domains/<domain>/pack.md` + assets. Loads in layers: pack (domain truth) → GBrain (entity/account memory) → engagement folder (this deal's facts). See §3. |
| **Proposal Engineering Engine** | reuse | `presales-deal-prep`, `vertical-scorer`, `ai-strategy-brief`, `contract-reviewer`, `difficult-conversation-prep`. Consumes loaded context; never re-researches what a pack already holds. |
| **Output Engine** | reuse | `branded-pptx-deck` (board decks — QA gate applies), `ai-strategy-researcher` (Word reports), `drawio` + `architecture-presentation` (assessments), `workflow-visualizer` (operating models), `comms-drafter` (briefings). Each of the 8 output types maps to a named skill chain — see §5. |
| **Agent Runtime** | reuse | Claude Code / Codex harness. Assembly-line sessions per pipeline stage; delegate parallel research to cheaper models. Tool-agnostic per the Four C's blueprint. |
| **Memory System** | reuse | Three-tier split already documented: GBrain (entities, compounding knowledge), local files (deliverables, packs), memory files (behavioral). Packs are **local files** — they are versioned deliverable infrastructure, not GBrain pages. GBrain holds the *entity* layer: accounts, people, prior engagements. |
| **Governance System** | reuse + extend | Existing: PPTX QA gate, `draft/reviewed/blocked` statuses, GBrain cost guardrails, keys-not-prompts. New: **pack freshness SLA** (stale pack = blocked deliverable, §6) and source-verification rule (every claim in a client deliverable traces to a pack citation or fresh primary source). |
| **Testing Framework** | build (small) | Pack lint (required sections present, citations resolve, freshness date) + **golden questions** per domain: 3–5 canned strategy questions with expected-answer rubrics. Run after every pack update. Plugs into existing pytest setup. |

---

## 3. The domain context pack (Consulting Context Engine)

One pack per domain under `consulting-os/domains/<slug>/`. Spec lives at
`consulting-os/domains/_template/pack.md`. Sections:

| Section | Contents | Feeds |
|---------|----------|-------|
| Manifest | slug, classification keywords, freshness date, version | Domain Classification |
| Point of view | The 5–8 opinionated theses we sell in this domain | All outputs — this is the differentiation |
| Reference architectures | Named stacks with verified primitives (e.g., SAP: Gemini + ADK + MCP → OData, never Joule) | Assessments, roadmaps |
| Market landscape | Vendors, competitors, analyst signals, pricing benchmarks | Vendor evals, business cases |
| Proof points | Case studies, operator metrics, our prior wins (links to GBrain pages) | Proposals, board decks |
| Frameworks | Maturity models, scoring rubrics, decision trees we apply | Roadmaps, operating models |
| Objection library | Common pushback + tested responses | Deal prep |
| Source watchlist | URLs/feeds/repos acquisition monitors for this domain | Acquisition Engine |
| Golden questions | Test prompts + expected-answer rubrics | Testing Framework |

**Layered context load order** (cheap → expensive, stop when sufficient):
1. **Pack** — static domain truth (free, local read)
2. **GBrain semantic recall** — has this account/vertical/theme appeared before? (embedding recall, cheap)
3. **Engagement folder** — this client's facts under `runs/<engagement>/`
4. **Fresh acquisition delta** — only for what the pack doesn't cover or is stale on (Exa/firecrawl, costed)

This ordering is the whole point of "context engineering pipelines per
capability area": synthesis never starts from a cold web search again.

### Initial domain pack set (9)

`ai-native-engineering`, `enterprise-agent-platforms`, `enterprise-rag-knowledge`,
`sre-aiops-transformation`, `sap-ai-transformation`, `cloud-modernization`,
`platform-engineering`, `proposal-engineering`, `industry-transformation`.

Note: `proposal-engineering` is both a domain (we consult on it) and an engine
(we use it). The pack holds the methodology; the engine is the skill chain.
`industry-transformation` is a meta-pack — thin core + per-industry sub-packs
added on demand (automotive first, given existing Hyundai/TMNA work).

---

## 4. Mission pipeline — how the four stages run

| Stage | Trigger | What happens | Cadence (per Four C's: earned) |
|-------|---------|--------------|-------------------------------|
| **Acquire** | scheduled + on-demand | Run each pack's source watchlist through content-research/Exa; raw notes land in `consulting-os/inbox/<domain>/` | Start manual; graduate to weekly scheduled scan per active domain |
| **Transform** | after acquire | Curate inbox → pack sections (cite, date, dedupe); entity facts → GBrain write-back (batched) | Manual review gate stays — packs are the product, no auto-merge |
| **Operationalize** | per request | Classify → layered context load → engagement folder scaffold | Always on-demand |
| **Generate** | per request | Output skill chain for the requested deliverable type, governance gates applied | Always on-demand; client-facing sends always manual |

---

## 5. Output type → skill chain map

| Output | Chain |
|--------|-------|
| Board strategy deck | context load → `ai-strategy-brief` (narrative) → `branded-pptx-deck` (QA gate, reviewed status) |
| Executive briefing | context load → `00-account-briefing` / `ai-strategy-brief` one-pager |
| Proposal | context load → `presales-deal-prep` → proposal doc + objection prep |
| Transformation roadmap | context load → pack frameworks → phased roadmap doc → optional deck |
| Operating model | context load → `workflow-visualizer` + operating model doc |
| Architecture assessment | context load (reference architectures) → `drawio` → `architecture-presentation` |
| Vendor evaluation | pack market landscape + fresh delta → `vertical-scorer`-style scored matrix |
| Business case | context load → `opportunity-sizer`-style sizing → business case doc + deck |

---

## 6. Governance additions

1. **Pack freshness SLA.** Each pack manifest carries `freshness:` (date of last
   curated update). Market-sensitive sections older than **30 days** for an
   active pursuit → the run must do an acquisition delta before generating, or
   mark the deliverable `draft` with the stale sections flagged. Reference
   architectures and frameworks age slower — 90 days.
2. **Citation rule.** Client deliverables only carry claims traceable to a pack
   citation or a fresh primary source verified in the run. (Extends the
   existing "final cited sources are primary and current" rule.)
3. **Existing gates unchanged.** PPTX QA, delivery statuses, branded template
   requirement, GBrain cost guardrails, keys-not-prompts all apply as-is.

---

## 7. Test case — "Provide AI strategy for SRE/AIOps in a regional bank"

The canonical scenario, end-to-end:

1. **Classify** — kernel matches `sre-aiops-transformation` (primary) +
   `industry-transformation/financial-services` (secondary, may not exist yet —
   classification reports the gap rather than faking coverage).
2. **Context load** — read both packs; GBrain recall on the account name and
   "regional bank AIOps" themes; scaffold `runs/<date>-<client>-sre-aiops/`.
3. **Acquisition delta** — pack freshness check; if the market-landscape
   section is current, only client-specific research runs (their stack,
   incidents, hiring signals, earnings).
4. **Synthesize** — strategy built *from the pack's point of view and
   frameworks* (e.g., its AIOps maturity model), populated with client facts.
   This is where pack investment pays: the skeleton of the answer pre-exists.
5. **Generate** — requested outputs via §5 chains; deck through the branded QA
   gate to `reviewed`.
6. **Write back** — durable client/market findings → GBrain (batched); any
   reusable domain insight → pack inbox for next curation pass. Run status
   reports GBrain recall and write-back explicitly.

Total new research per engagement shrinks to the **client-specific delta** —
the domain layer is amortized across every engagement in that domain.

---

## 8. Build roadmap (phased, smallest useful first)

**Phase 1 — prove the loop with one pack (this week)**
- [x] Pack template (`consulting-os/domains/_template/pack.md`)
- [x] Kernel routing README + test-case runbook
- [x] First pack: `sap-ai-transformation` (most existing material: no-Joule
  stance, Gemini+ADK+MCP stack, Hyundai vault, OpenHands grounding)
- [ ] Run the test case once against the SAP pack; capture what the pack was
  missing; curate it in. (Skill-feedback loop applied to packs.)

**Phase 2 — coverage (next 2–3 weeks)**
- [ ] Packs for the 3 most-pursued domains next (suggest: enterprise-agent-platforms,
  enterprise-rag-knowledge, ai-native-engineering — closest to existing research)
- [ ] Pack lint + golden-question harness in pytest
- [ ] Domain classification step formalized in the kernel runbook

**Phase 3 — cadence (after packs are battle-tested)**
- [ ] Weekly scheduled acquisition scan per active domain (read-only — safe first automation)
- [ ] Freshness report: which packs are stale, what's in inbox awaiting curation
- [ ] Remaining packs on demand, pulled by real pursuits (usage pulls the next C)

**Phase 4 — productize (optional)**
- [ ] Package as a skill (`consulting-os` skill with runbooks as stages) so the
  whole pipeline triggers from one command, same cross-host pattern as
  content-ideas
