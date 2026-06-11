# CIOS Specification v1.0 — Execution Grade

- **Status:** In Design → this document is the authoritative build spec
- **Governs:** Consulting Intelligence Operating System (CIOS) v1.0
- **Architectural authority:** `governance/CIOS-Architecture-Constitution-v1.0.md`
  (adopted per CIOS-ARCH-002; this spec defines behavior under it and MUST NOT
  violate its frozen elements, constraints A-001..005, or principles OP-001..005)
- **Architecture:** FROZEN per `consulting-os/governance/decisions/CIOS-ARCH-001.md`,
  as reconciled by CIOS-ARCH-002
- **Target builders:** Claude Code, Codex, OpenHands, future agent platforms
- **Conformance language:** MUST / MUST NOT / SHOULD / MAY (RFC 2119)
- **Requirement IDs:** `CIOS-<ENGINE>-<NNN>` — stable, never reused

Success criterion: an agent can build and operate CIOS from this document
without architectural clarification. Anything ambiguous here is a spec bug —
file it against this document, do not improvise architecture.

Conceptual origin: the Four C's second-brain/AI-OS model — traceability map
in `spec/references/four-cs-anchor.md`. Companion references:
`spec/references/company-brain.md`, `spec/references/board-deck-sop.md`.

---

## Volume 1, Part 1 — Meta Model

### 1.1 Entities

| Entity | Identity | Persisted at | Lifecycle owner |
|--------|----------|--------------|-----------------|
| `Request` | free text + timestamp | engagement manifest | Kernel |
| `DomainPack` | `slug` (kebab-case, = dir name) | `consulting-os/domains/<slug>/pack.md` | Transformation Engine |
| `InboxItem` | file under `consulting-os/inbox/<slug>/` | same | Acquisition Engine |
| `Engagement` | `<YYYY-MM-DD>-<client-or-niche>-<topic>` | `runs/<id>/` | Kernel |
| `Deliverable` | path within engagement | `runs/<id>/deliverables/` | Output Engine |
| `ConsultingAsset` | file under `domains/<slug>/assets/` | same | Proposal Engineering Engine |
| `MemoryRecord` | GBrain page slug | GBrain (`~/.gbrain`) | Memory System |
| `GoldenQuestion` | pack golden-questions numbered item | pack file | Testing Framework |
| `DecisionRecord` | `CIOS-<AREA>-<NNN>` | `consulting-os/governance/decisions/` | Governance |

**CIOS-MM-001** Every entity MUST be representable as plain files (markdown/
YAML/JSON) readable by any agent host. No entity state may live only in a
conversation.

**CIOS-MM-002** The nine domain slugs are fixed by CIOS-ARCH-001.
`industry-transformation` MAY contain sub-packs at
`domains/industry-transformation/<industry>/pack.md`; sub-packs follow the
full pack schema and lifecycle.

**CIOS-MM-005 (meta model flow — Constitution §7, mandatory)** Every
consulting output MUST be traceable backwards through
`Source → Intelligence → Domain → Consulting Context → Consulting Asset →
Consulting Output`. In file terms: registry source → inbox item → domain
classification → pack → asset file → deliverable. Constitution constraints
apply verbatim: no output without context (A-001), no context without
intelligence (A-002), no intelligence without source (A-003), no asset
without context (A-004), no output bypassing the meta model (A-005). Simple
outputs MAY satisfy the asset layer by *reusing existing assets*; an
engagement that derives a new reusable narrative/architecture/business-case
component SHOULD persist it as an asset file (CIOS-PRO-005) so the next
engagement reuses instead of recreates (OP-003).

### 1.2 State models

**DomainPack** (`status:` frontmatter field):
```
draft ──(golden questions pass AND no [NEEDS ACQUISITION]
          in §1 PoV or §2 architectures)──▶ active
active ──(freshness SLA breach, §11.1)──▶ stale
stale ──(curation pass + golden questions re-pass)──▶ active
any ──(ARB decision)──▶ archived
```

**Engagement** (`state:` in manifest):
```
scoped → researching → synthesizing → generating → delivered → closed
                 (any state) → blocked
```
**CIOS-MM-003** State transitions MUST be recorded in the engagement manifest
with a timestamp. Skipping forward states is allowed (e.g., no research
needed); skipping `delivered` before `closed` is not when client-facing
deliverables exist.

**Deliverable** (`status:` per item in manifest):
```
draft → reviewed → delivered        any → blocked
```
**CIOS-MM-004** Status MUST be reflected in the filename suffix for decks
(`*-draft.pptx`, `*-reviewed.pptx`, `*-blocked.txt`), matching the repo PPTX
governance rules.

**InboxItem:** `raw → curated | discarded`. Curated items are merged into a
pack section with citation and the inbox file deleted or moved to
`inbox/<slug>/_curated/`.

### 1.3 Mission stage → engine mapping (fixed)

| Stage | Engines engaged |
|-------|-----------------|
| Acquire | Acquisition |
| Transform | Transformation, Memory |
| Operationalize | Kernel, Domain Classification, Consulting Context |
| Generate | Proposal Engineering, Output, Governance |
| (cross-cutting) | Agent Runtime, Testing, Governance |

---

## Volume 1, Part 2 — Kernel Contracts

Purpose: request intake, dispatch, engagement lifecycle ownership.

**CIOS-KER-001** On any consulting request, the Kernel MUST execute, in order:
classify (Part 5) → context load (Part 6) → freshness gate (Part 11) →
route to the runbook for the request type. The canonical runbook is
`consulting-os/runbooks/ai-strategy-request.md`.

**CIOS-KER-002** The Kernel MUST create the engagement folder before any
research output is produced:

```
runs/<id>/
  engagement.yaml      # manifest (schema §2.1)
  research/            # acquisition outputs for this engagement
  deliverables/        # final artifacts
  status.md            # human-readable run log
```

### 2.1 Engagement manifest schema (`engagement.yaml`)

```yaml
id: 2026-06-10-acme-bank-sre-aiops      # required, = dir name
client: Acme Bank                        # required (or niche if no client)
request: >                               # required, verbatim user request
  Provide AI strategy for SRE/AIOps in a regional bank
domains:
  primary: sre-aiops-transformation      # required, must be a valid slug
  secondary: []                          # 0–2 slugs
classification:
  confidence: high                       # high|medium|low
  pack_gaps: []                          # domains requested but not covered
state: scoped                            # §1.2 Engagement states
state_log:
  - {state: scoped, at: 2026-06-10T09:00Z}
freshness_gate:
  passed: false
  notes: "pack draft — acquisition delta required"
gbrain:
  recalled: []                           # page slugs read
  written: []                            # page slugs written/updated
deliverables: []                         # {type, path, status} per §8.1 types
```

**CIOS-KER-003** `gbrain.recalled`/`written` MUST be filled whenever GBrain is
used — GBrain usage is reported explicitly, never invisible setup (repo rule).

**CIOS-KER-004** The Kernel MUST NOT proceed silently when classification
returns `confidence: low` or `pack_gaps` is non-empty — it asks the user or
records the documented fallback (Part 5).

**CIOS-KER-005 (router leanness)** The kernel routing files (CLAUDE.md /
AGENTS.md / `consulting-os/README.md`) MUST stay pointers-not-content: a
~400-line ceiling per file; detail lives in packs, runbooks, and this spec
with the router linking down. When a router file exceeds the ceiling, push
content down a layer. *(ref: spec/references/company-brain.md)*

---

## Volume 1, Part 3 — Acquisition Engine Contracts

Purpose: bring external intelligence in. Two modes.

**CIOS-ACQ-001 (watchlist mode)** Input: a pack's §7 source watchlist. Output:
files in `consulting-os/inbox/<slug>/` with the schema below. Tools, in
preference order per repo rules: Exa MCP (or local Exa wrapper) → firecrawl →
content-research → `/watch` for video sources.

**CIOS-ACQ-002 (engagement-delta mode)** Input: gap list from the Consulting
Context Engine (CIOS-CTX-004). Output: notes in `runs/<id>/research/`; any
finding with cross-engagement value MUST also be copied to the domain inbox.

### 3.1 Inbox item schema

```markdown
---
captured: 2026-06-10
source_url: https://...        # primary source, required
source_type: vendor-doc | repo | analyst | news | video | community
domain: sap-ai-transformation
target_section: 3              # pack section number it likely feeds
summary: one-line claim
---
<extracted content with enough quote/context to verify the claim>
```

**CIOS-ACQ-003** Every inbox item MUST carry a resolvable primary
`source_url`. Secondary reporting MAY be captured only with the primary
source it cites.

**CIOS-ACQ-004** Acquisition MUST NOT write to pack files. Only the
Transformation Engine merges into packs.

**CIOS-ACQ-005** Acquisition runs are read-only with respect to external
systems — they never authenticate to client systems or post anywhere.

**CIOS-ACQ-006 (source policy)** Per `governance/decisions/CIOS-SRC-001.md`,
the knowledge layer is built from exactly two source classes:
- **Tier 1 — the top-10 GitHub registry** (`consulting-os/sources.md`):
  repos + their official docs are the only authoritative sources for
  technical claims, reference architectures, and capability statements.
- **Tier 2 — practitioner & vendor-engineering signal**: (a) LinkedIn posts —
  proof points, objections, sentiment; technical claims MUST be re-grounded
  in Tier 1 before curation. (b) Curated YouTube channels (registry-listed,
  e.g. SAP on Azure, SAP on AWS) — vendor-engineering architecture/deployment
  content; cite with video URL + timestamp; re-ground in Tier 1 when a
  repo/doc equivalent exists, and a timestamped video citation MAY stand for
  architecture patterns that have no repo equivalent — never for capability
  claims a repo could verify. Acquisition via `/watch` and content-research.
All other material (vendor marketing, analyst reports, news) is Tier 3 —
context narrative only, never the sole citation for an `active`-pack claim.
Pack §7 watchlists MUST be drawn from the registry; expanding the top-10 set
means updating the registry first, not adding ad-hoc sources to one pack.

**CIOS-ACQ-007 (resolution order and gap-fill mechanisms)** For any
technical claim, acquisition resolves in this order, stopping at the first
source that answers:
1. OpenHands repo/docs (registry #1 — primary across ALL domains, per
   CIOS-SRC-001 amendment);
2. other Tier-1 registry repos;
3. a gap-fill mechanism, chosen by claim type:
   - **curated YouTube channels** (registry Tier 2b, via `/watch`) — for
     architecture patterns, deployment walkthroughs, and capability
     demonstrations; rich context for any domain's missing gaps, cited
     URL @timestamp;
   - a **printing-press CLI** against the authoritative API — for structured
     data and API surfaces (use an existing pp-CLI from the fleet or generate
     a new one via research → generate → build → shipcheck, e.g. against
     `api.sap.com` or the GitHub API);
4. otherwise the claim is recorded as **[NEEDS ACQUISITION]** — never
   sourced from model memory or ad-hoc scraping.
New pp-CLIs created for acquisition are themselves capabilities: they SHOULD
be kept and registered so the next engagement reuses rather than regenerates
them.

---

## Volume 1, Part 4 — Transformation Engine Contracts

Purpose: raw intelligence → curated pack content; entity facts → memory.

**CIOS-TRN-001 (curation)** Input: inbox items for one domain. Process per
item: verify source resolves → dedupe against existing pack content →
merge into the named `target_section` with inline citation → update pack
`freshness:` and bump `version:` (patch for content, minor for new
section-level claims) → mark item curated.

**CIOS-TRN-002** Curation is human-gated: the Transformation Engine prepares
the merged diff; a human approves before the pack file is updated. Packs are
the product — no auto-merge.

**CIOS-TRN-003 (citation format)** Pack claims cite as
`(source: <url>, <YYYY-MM>)` or `[gbrain:<slug>]` for internal proof points.
A claim without a citation MUST be marked **[NEEDS ACQUISITION]**.

**CIOS-TRN-004 (memory split)** During curation: facts about *entities*
(companies, people, accounts, recurring themes) go to GBrain via Memory
contracts (Part 10); facts about the *domain* stay in the pack. The same fact
MAY exist in both with cross-reference.

**CIOS-TRN-005** After any pack edit, the Testing Framework's pack lint and
golden questions MUST run (Part 12). A failing pack cannot hold or gain
`active` status.

**CIOS-TRN-006 (brain health)** Three standing curation habits, small and
constant rather than large and occasional *(ref: spec/references/company-brain.md)*:
(a) engagement findings are logged the day the engagement closes, not later;
(b) entries record **what drove the result**, not just what was built — the
reasoning is the asset, the stack is reproducible;
(c) stale facts are pruned on sight — old pricing, dropped tools, abandoned
positioning. Stale context is worse than missing context because the agent
trusts it. A pruned claim either gets a fresh citation or a
**[NEEDS ACQUISITION]** marker, never silent retention.

---

## Volume 1, Part 5 — Domain Classification Contracts

Purpose: request → domains, deterministically and honestly.

**CIOS-CLS-001 (algorithm)**
1. Tokenize the request; match against every pack's `keywords:` list
   (case-insensitive, substring and stem matches count).
2. Score = number of distinct keyword hits per pack.
3. Primary = highest score; secondary = next ≤2 packs with score ≥1.
4. Tie or zero scores → semantic step: compare request meaning against pack
   `title` + §1 PoV headings; if still ambiguous → `confidence: low`.

**CIOS-CLS-002 (confidence)** `high` = primary score ≥2 and a clear margin;
`medium` = single-hit match; `low` = semantic-only or tie.

**CIOS-CLS-003** `confidence: low` → the agent MUST ask the user to pick the
domain (AskUserQuestion on interactive hosts; on non-interactive runs, record
the ambiguity, proceed with the top candidate, and flag every deliverable
`draft`).

**CIOS-CLS-004 (no-coverage)** No pack scores ≥1 → offer two paths and never
fake coverage: (a) scaffold a new pack from `domains/_template/pack.md` in
`draft` and proceed flagged, or (b) proceed pack-less with the deliverable
carrying an explicit "no domain pack — generic synthesis" notice.

**CIOS-CLS-005** Classification output is recorded in `engagement.yaml`
(`domains:` + `classification:` blocks). Schema is fixed by §2.1.

---

## Volume 1, Part 6 — Consulting Context Contracts

Purpose: assemble the layered context before synthesis. This is the engine
the others exist to feed.

**CIOS-CTX-001 (load order, mandatory)**
1. Pack(s) — full read of primary; secondary packs at minimum §1 PoV + §5
   frameworks.
2. GBrain semantic recall — query the account name, vertical, and theme
   slugs. Prefer semantic retrieval over keyword; escalate to synthesis
   (`gbrain query`) only when merged interpretation is needed (cost rule).
3. Engagement folder — all of `runs/<id>/` if it exists.
4. Acquisition delta — ONLY for identified gaps (CIOS-CTX-004).

**CIOS-CTX-002** Lower layers MUST NOT be fetched when higher layers already
answer the need. The stop-when-sufficient judgment is the agent's, but
skipping layer 1 or 2 entirely is a contract violation.

**CIOS-CTX-003 (precedence)** On conflict: engagement facts (client-specific,
freshest) > fresh acquisition delta > pack > GBrain. A conflict between pack
and fresh primary source MUST be filed to the domain inbox as a curation
correction.

**CIOS-CTX-004 (gap list)** Output of context load = a gap list: questions the
loaded context cannot answer + pack sections marked **[NEEDS ACQUISITION]**
that the engagement touches + sections breaching freshness SLA. The gap list
is the *only* authorized input to engagement-delta acquisition.

**CIOS-CTX-005** Synthesis MUST take its skeleton from the pack: lead with §1
point of view, structure analysis with §5 frameworks, ground designs in §2
reference architectures. Client facts populate the skeleton; the skeleton is
not reinvented per engagement.

---

## Volume 1, Part 7 — Proposal Engineering Contracts

Purpose: pursuit-specific reasoning on top of loaded context.

**CIOS-PRO-001** Skill bindings (existing skills, used as-is):
`presales-deal-prep` (pursuit pipeline), `vertical-scorer` (GO/WAIT/PASS
scoring), `ai-strategy-brief` (one-pager), `contract-reviewer` (terms),
`difficult-conversation-prep` (hard conversations), `grill-me` (extract
owner knowledge into the engagement).

**CIOS-PRO-002** Proposal work MUST consume the loaded context; re-researching
a question the pack already answers is a contract violation (wasted tokens,
drift risk). The objection library (§6 of the pack) seeds objection prep.

**CIOS-PRO-003** Scoring uses pack §5 rubrics where they exist;
`vertical-scorer` general frameworks otherwise. The score sheet lands in
`runs/<id>/deliverables/`.

**CIOS-PRO-004** Pricing/commercial claims MUST come from pack §3 market
benchmarks or fresh primary sources — never from model memory.

**CIOS-PRO-005 (consulting assets — Constitution §8.5)** The Proposal
Engineering Engine owns the Asset layer: reusable components derived from
pack context — executive narratives, value propositions, differentiators,
business-case skeletons, transformation stories, reference-architecture
writeups, operating-model patterns. Assets live at
`domains/<slug>/assets/<kebab-name>.md` with frontmatter:

```yaml
asset: executive-narrative | value-proposition | differentiator |
       business-case | transformation-story | reference-architecture |
       operating-model | roadmap-pattern
derived_from: <pack section or engagement id>   # A-004: never from thin air
last_used: YYYY-MM-DD
```

**CIOS-PRO-006 (reuse before creation — OP-003)** Before drafting any
deliverable component, check `domains/<slug>/assets/` for an existing asset
of that type. Reuse-and-adapt beats regenerate; after an engagement, update
the asset's `last_used` and fold improvements back into the asset file.

---

## Volume 1, Part 8 — Output Engine Contracts

### 8.1 Output types and pipelines (fixed set of 8)

| `type` (manifest value) | Pipeline | Gates |
|---|---|---|
| `board-deck` | context → `ai-strategy-brief` narrative → `branded-pptx-deck` | full PPTX QA (CIOS-GOV-003) |
| `executive-briefing` | context → `00-account-briefing` / `ai-strategy-brief` | citation check |
| `proposal` | context → `presales-deal-prep` chain | citation + pricing source check |
| `transformation-roadmap` | context → pack §5 frameworks → phased doc (+ optional deck) | citation check (+ PPTX QA if deck) |
| `operating-model` | context → `workflow-visualizer` + model doc | citation check |
| `architecture-assessment` | context → pack §2 → `drawio` → `architecture-presentation` | primitives-verified check (CIOS-OUT-003) |
| `vendor-evaluation` | pack §3 + delta → scored matrix (`vertical-scorer` pattern) | every score row sourced |
| `business-case` | context → sizing (opportunity-sizer pattern) → case doc + deck | assumptions table mandatory |

**CIOS-OUT-001** Every deliverable MUST be registered in `engagement.yaml`
`deliverables:` with `{type, path, status}` before being presented to the
user.

**CIOS-OUT-002** Decks: branded template only (`BRANDED_PPTX_TEMPLATE`, else
`~/.claude/templates/branded-template.pptx`, else the branded-pptx-deck
workflow). Template unavailable → deliverable `blocked`, never an unbranded
substitute. Builder script stays in the engagement folder for reproducible QA.

**CIOS-OUT-003** Architecture deliverables MUST use verified primitives only:
OpenHands claims grounded in the OpenHands repo/docs; ADK/AG-UI patterns per
repo rules (e.g., `AGUIToolset()` requirement); no invented orchestration.

**CIOS-OUT-004** Client-facing *sending* (email, upload, share) is always
manual — the Output Engine produces files; a human transmits them
(keys-not-prompts). Copy-out to `CLIENT_DELIVERY_DIR` only for `reviewed`
artifacts, only when the env var is set.

**CIOS-OUT-005 (board-deck intake schema and slide contract)**
*(ref: spec/references/board-deck-sop.md)*
The `board-deck` pipeline MUST resolve this intake set before building —
from pack → GBrain → engagement context first (CIOS-CTX-001 order), asking
the user only for residual gaps:

```yaml
board_deck_intake:
  company: {name, industry, hq, primary_market, mission}
  business: {product_lines: [], revenue, ebitda, report_currency}
  competitive: {competitors: [3 named]}
  plan: {time_horizon_years, esg_priorities?, constraints?}
  brand: {accent_hex?, logo?}        # default: branded template's own brand
```

Slide contract (augments the repo slide contract — action title, structured
support, evidence/implication — and the PPTX QA gate):
- 20–30 slides max excluding appendix
- ≤5 bullets per slide, ≤12 words per bullet
- speaker notes 100–150 words per slide
- visuals vector or 16:9 PNG, no raster stretching
- citations per CIOS-GOV-002 (stricter than the source SOP's rule)

---

## Volume 1, Part 9 — Agent Runtime Contracts

Purpose: host-agnostic execution. CIOS runs identically under Claude Code,
Codex, OpenHands, or any AGENTS.md-reading host.

**CIOS-ART-001** All runtime instructions live in files (CLAUDE.md /
AGENTS.md / runbooks / this spec). A host MUST be able to cold-start CIOS
from the repo alone. No host-specific feature may be load-bearing; host
features (subagents, plan mode, schedules) are accelerators only.

**CIOS-ART-002 (session discipline)** Pipeline stages run as separate
sessions/phases where the host allows: acquisition, curation, synthesis, and
output generation each get a clean context, passing artifacts via files
(assembly-line rule). A stage MUST be resumable from its files alone.

**CIOS-ART-003 (delegation)** Parallelizable research MAY be delegated to
cheaper models (Sonnet/Haiku class); synthesis and client-facing writing run
on the strongest available model. Delegated work returns summaries to files,
not to chat only.

**CIOS-ART-004 (paths)** All host- or machine-specific locations come from
env vars (`BRANDED_PPTX_TEMPLATE`, `CLIENT_DELIVERY_DIR`, `SECOND_BRAIN_DIR`,
`OBSIDIAN_VAULT_DIR`, `CONTENT_HOME`). Unset + no documented fallback →
report the step blocked/skipped; never invent a machine-specific path.

**CIOS-ART-005 (research tooling)** Hosts exposing stronger research tools
(Exa MCP, desktop research plugins) SHOULD be preferred for acquisition;
terminal hosts use the closest equivalent (Exa API wrapper). Discovery
advantage never waives delivery/QA/source rules.

---

## Volume 1, Part 10 — Memory Contracts

**CIOS-MEM-001 (three tiers, fixed)**
- **GBrain** — entities that compound: companies, people, prospects,
  verticals, themes, meeting notes, deal context, prior findings.
- **Local files** — packs, engagement artifacts, deliverables. GBrain is
  NEVER the system of record for deliverables.
- **Agent memory files** — behavioral guidance and user preferences only.

**CIOS-MEM-002 (read)** GBrain Recall is a mandatory chain stage before
strategy synthesis or pursuit research (Part 6). Prefer `gbrain search` /
semantic recall (cheap) over `gbrain query` synthesis (token cost) unless
merged interpretation is required.

**CIOS-MEM-003 (write)** GBrain Write-back runs at engagement close for
durable findings likely to recur. Writes are batched to minimize embedding
calls. Page slugs written are recorded in `engagement.yaml`.

**CIOS-MEM-004 (cost guardrails, inherited)** Search mode stays
`conservative`; no dream-cycle/enrichment crons; both require explicit user
approval to change.

**CIOS-MEM-005** GBrain entity pages MAY cite pack sections and vice versa
(`[gbrain:<slug>]` / repo paths), keeping one source of truth per fact with
cross-references rather than duplication.

**CIOS-MEM-006 (scaling ladder)** Memory capability grows in three rungs —
ingestion (auto-capture from transcripts/CRM), retrieval (vector search),
currency (date tags + supersession) — and a rung is added **only when the
simpler version visibly breaks**, not before
*(ref: spec/references/company-brain.md)*. CIOS v1.0 position: retrieval is
live (GBrain embeddings); currency is live (freshness SLA +
**[NEEDS ACQUISITION]** markers); auto-ingestion is deliberately deferred to
roadmap Phase 3 cadence and MUST NOT be built earlier.

---

## Volume 1, Part 11 — Governance Contracts

**CIOS-GOV-001 (freshness SLA)** Market-sensitive pack sections (§3, §6
pricing-dependent entries): 30 days on active pursuits. Reference
architectures and frameworks (§2, §5): 90 days. Breach → pack `status: stale`
→ engagement freshness gate fails → acquisition delta required, or
deliverables ship `draft` with stale sections named.

**CIOS-GOV-002 (citation rule)** Client deliverables carry only claims
traceable to a pack citation or a fresh verified primary source from this
engagement. Inbox material is never citable.

**CIOS-GOV-003 (PPTX gate, inherited verbatim)** Branded builder saves with
validation; overlap/overflow check; `preview_pptx.py` contact sheets reviewed
when available (else state "unreviewed for visual QA", not final); fix
overlaps before delivery; explicit `draft|reviewed|blocked` status; matching
filename suffixes; builder script kept in the run folder; only `reviewed`
decks reach the delivery path; minimum visual checklist per repo CLAUDE.md.

**CIOS-GOV-004 (permission layer)** Keys, not prompts. Agents hold read
credentials by default; write/send capabilities are granted per battle-tested
use case and never for client communications. A prompt is never a permission
layer.

**CIOS-GOV-005 (decisions)** Architecture-level changes require a decision
record in `governance/decisions/` (`CIOS-<AREA>-<NNN>`). The frozen scope of
CIOS-ARCH-001 requires an explicit v2.0 ARB decision to amend.

**CIOS-GOV-006 (slip-ups are data)** Any agent error → update the governing
skill/runbook/pack so it cannot recur, in the same session where the error
was found.

**CIOS-GOV-007 (unattended-run guardrails)** Every scheduled/headless CIOS
run (Phase 3 cadence onward) MUST carry *(ref: spec/references/company-brain.md)*:
- a token cap — defaults: ~20K review/scan jobs, ~60K fix/curation-prep jobs,
  ~100K weekly maintenance; no uncapped loops;
- one job, one definition of done — no open-ended prompts on a schedule;
- audit logging (pipe `stream-json` output to the run log) with alerting on
  weekly spend, not single runs.

**CIOS-GOV-008 (automation billing)** As of 2026-06-15, headless Claude Code,
Agent SDK, and GitHub Actions runs bill against a separate automation credit
(then API rates), while interactive sessions stay on subscription. Cadence
design MUST budget accordingly: heavy maintenance weekly not hourly, caps per
CIOS-GOV-007, and interactive-first for anything that doesn't truly need to
run unattended.

**CIOS-GOV-009 (change control on the brain)** The repo is the source of
truth and SHOULD carry branch protection on `main` once CIOS goes
multi-contributor: pack and spec changes land via PR, and the engagement/
memory log doubles as the changelog. Until then, CIOS-TRN-002's human
curation gate is the minimum control.

---

## Volume 1, Part 12 — Testing Contracts

**CIOS-TST-001 (pack lint)** A pack is lint-clean when: frontmatter has all
required fields with valid values (slug = dir name; status in enum; freshness
parseable; ≥3 keywords); all 8 numbered sections present; every claim in an
`active` pack carries a citation or **[NEEDS ACQUISITION]** marker; §8 has
≥3 golden questions with rubrics.

**CIOS-TST-002 (golden questions)** After every pack edit, each §8 question is
answered using ONLY that pack + the rubric is checked. Pass = rubric elements
present. `active` requires all-pass; failure → pack stays/returns to `draft`.

**CIOS-TST-003 (harness)** Lint is implemented as stdlib-only pytest
(`tests/test_consulting_packs.py`), consistent with repo rules (no runtime
pip installs, no network in tests). Golden-question evaluation is
agent-executed (it needs a model); the runbook step is mandatory even though
unattended CI cannot run it.

**CIOS-TST-004 (pipeline acceptance)** CIOS v1.0 is accepted when the
Reference Implementation scenario (Part 13) runs end-to-end with every
contract in this spec satisfied and the run status documenting each gate.

**CIOS-TST-005 (baseline comparison — Constitution §10.11)** For each domain,
golden question 1 SHOULD have a recorded **no-context baseline**: the same
question answered with no pack loaded, stored at
`domains/<slug>/assets/_baseline-gq1.md`. The pack proves its value when the
context-loaded answer beats the baseline on the §11 rubric. Re-run the
comparison when the pack major-versions.

**CIOS-TST-006 (output & context quality scoring — Constitution §10.11)**
Every delivered engagement records two 1–5 self-scores in `status.md`,
each with a one-line justification:
- **Output quality:** rubric coverage, citation completeness, gate compliance.
- **Context quality:** how much of the answer came from the pack vs had to be
  freshly researched (5 = pack supplied the skeleton and most evidence;
  1 = pack contributed almost nothing). Context scores ≤2 trigger a curation
  backlog entry automatically.

**CIOS-TST-007 (reuse measurement — Constitution §10.11)** Reuse is measured
through asset frontmatter: every asset use updates `last_used`; assets also
carry `use_count` (increment per engagement). At each curation pass, report
assets unused for 90+ days — candidates for refresh or archive. The pack
lint warns (not fails) on missing `use_count`.

---

## Volume 1, Part 13 — Reference Implementation

**Reference domain:** `ai-native-engineering` (Constitution ADR-005 — rich
sources [OpenHands is registry #1], high relevance, strong consulting value;
adopted per CIOS-ARCH-002). `sap-ai-transformation` remains the second seeded
pack and the cross-domain stress test.
**Reference runbook:** `consulting-os/runbooks/ai-strategy-request.md`.

### 13.1 Acceptance scenario

Execute golden question 1 of the reference pack as a full engagement:

> "A 400-developer enterprise software organization asks: what should our
> AI-native engineering strategy be?"

Expected execution trace (each step cites its contract):
1. Kernel intake; engagement folder + manifest created (KER-001/002).
2. Classification → primary `ai-native-engineering`, `confidence: high`
   (CLS-001/002).
3. Context load in order; gap list from the pack's **[NEEDS ACQUISITION]**
   markers (CTX-001/004); GBrain recall recorded.
4. Freshness gate evaluated (pack `draft` → acquisition delta on the gap
   list only — OpenHands repo/docs first per ACQ-007; pack-worthy findings
   copied to inbox (GOV-001, ACQ-002)).
5. Synthesis from pack skeleton: point-of-view lead, maturity/adoption
   framework staging, OpenHands-grounded reference architecture (CTX-005);
   reusable components persisted as assets (PRO-005, MM-005).
6. Outputs: `executive-briefing` + `board-deck` registered in manifest;
   deck through full PPTX gate to `reviewed` (OUT-001/002, GOV-003).
7. Write-back: client entity → GBrain (batched, recorded); domain findings →
   inbox; pack-gap list noted in status as curation backlog (MEM-003,
   TRN-001 queue).
8. Post-run: curation pass on inbox → pack toward `active` (TRN-001/002,
   TST-001/002).

### 13.2 Build order for an implementing agent

1. Verify repo skeleton exists (`consulting-os/` tree per CIOS-ARCH-001/002);
   scaffold any missing directory.
2. Implement `tests/test_consulting_packs.py` per TST-001; run it; fix the
   reference pack until lint-clean.
3. Seed the `ai-native-engineering` reference pack (template v2) from
   OpenHands repo/docs knowledge; SAP pack stays template v1 until its next
   curation pass.
4. Execute §13.1 end-to-end; record contract IDs satisfied in the run status.
5. Curate the resulting inbox into the reference pack; re-run golden
   questions; promote to `active` when passing.
6. Only then scaffold the next domain packs (architecture roadmap phase 2).

---

*End of CIOS Specification v1.0. Gaps found during implementation are spec
bugs — amend this document (allowed scope) and log material interpretation
decisions in `governance/decisions/`.*
