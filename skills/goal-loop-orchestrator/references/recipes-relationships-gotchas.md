## Reusable Recipes

When a workflow is likely to recur, capture the chain as a reusable recipe in
the final response or a local artifact if the user asks.

Example recipe format:

```markdown
## Recipe: Research-to-Deck
1. Recall / prior context -> notes
2. Research -> source pack
3. Strategy synthesis -> brief
4. Branded deck -> draft
5. Deck QA -> reviewed deliverable
6. Write-back -> durable memory
```

## Example Invocation

Sample user prompt:

```text
I have a rough idea for an AI support triage tool. Refine the goal, pick the
right skills, and get me to a verified PRD plus build plan.
```

Expected behavior:

```markdown
## Goal Contract
- Outcome: verified PRD and build plan for an AI support triage tool
- Artifacts: `vision.json`, `docs/prd.md`, `docs/product-roadmap.md`
- Constraints: use local repo skills first; no external installs without approval
- Acceptance criteria: PRD covers users, workflows, data, risks, MVP scope, and roadmap
- Verification: validate PLAID outputs and check roadmap tasks are actionable
- Loop budget: 3 total passes
- Stop conditions: validated artifacts exist, budget reached, or missing product input blocks progress

## Skill Chain
| Phase | Skill/action | Why | Input | Output | Verification |
|---|---|---|---|---|---|
| 1 | `plaid` plan | Product idea -> PRD/roadmap | rough idea | `vision.json`, docs | schema/doc validation |
| 2 | `karpathy-guidelines` overlay | Keep build plan surgical and verifiable | PRD/roadmap | tightened roadmap | acceptance criteria check |
| 3 | direct review | Confirm completeness | generated docs | final handoff | residual risk list |

## Loop State
- Pass: 1
- Max passes: 3
- Acceptance criteria met: no
- Verification status: pending product artifact generation
- Material change since previous pass: goal contract and chain selected
- Stop / continue decision: continue
- Reason: artifacts do not exist yet
```

## Skill Relationships

### Category
Business Automation

### Dependencies
None required. Optional external discovery may use `npx skills`, web research,
or host-provided tool discovery when available, but only after local skills are
insufficient and user approval is obtained for installs.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `grill-me` | Upstream / peer | when the goal needs deep discovery or stress-testing | `brainstorms/{date}-{slug}.md` |
| `ai-analyst` | Required upstream | for any data question, quantitative synthesis, metric, chart, forecast, segmentation, funnel, cohort, or opportunity sizing | validated findings, analysis JSON, chart PNGs, confidence/validation notes |
| `strategy-consulting` / strategy research policy | Research/synthesis | when the goal involves market maps, moats, wedges, competitive strategy, investment thesis, or pipeline strategy | source-backed strategy brief, confidence labels, research mode |
| `you-com-search` | Research discovery | when current web search, livecrawl, research, finance research, or Reddit/forum candidate URL discovery is needed | You.com result JSON, candidate source URLs, cited research output |
| `exa-api` | Research discovery | when semantic source discovery, competitor discovery, buyer-language page discovery, docs, forums, or market signals are needed | Exa discovery JSON, source candidates, rejected leads |
| `firecrawl` | Research ingestion | when important pages need full-page capture after discovery | Firecrawl JSON/markdown captures with status/source metadata |
| `plaid` | Sequential downstream | when the refined goal is a product idea, PRD, roadmap, design, launch, or build | `vision.json`, `docs/*.md` |
| `karpathy-guidelines` | Behavioral overlay | during coding, review, or refactoring passes | verification-oriented implementation plan |
| `content-ideas` | Sequential downstream | when the goal is social/content research or idea generation | dated research feed |
| `aeo-reddit-opportunity-finder` | Required upstream for Reddit validation | when buyer-language, skepticism, switching, workflow pain, or comparison-frame evidence is needed from Reddit | semantic Reddit probes and opportunity report |
| `reddit-new-factcheck` | Required qualification gate for Reddit validation | after semantic probes or thread discovery produce candidate Reddit sources | claim pack, evidence pack, fact-check report, rejection notes |
| `reddit-seo-pipeline` | Reddit extraction helper | when specific Reddit thread URLs are known | thread JSON and extracted comments |
| `branded-pptx-deck` | Required downstream | when the output is a slide deck, PowerPoint, executive deck, board deck, or client-ready presentation | reviewed PPTX and QA artifacts |
| `playwright-cli` | Verification downstream | when browser/UI validation is needed | screenshots, traces, test output |

### Runtime Preamble
When this skill triggers, say briefly: "I’ll refine the goal first, then run the
smallest skill chain needed and loop until the acceptance criteria are met or a
real blocker appears."

## Gotchas

- **Do not start with skill search.** A skill chain selected before the goal is
  refined usually optimizes for tools instead of outcomes.
- **Do not load all candidate skills.** Metadata first, full instructions only
  when the phase needs that skill.
- **Do not treat a chain plan as execution.** The loop must actually run the
  selected phases unless the user asked only for a plan.
- **Do not mark done without verification.** If checks are unavailable, say so
  and name the residual risk.
- **Do not validate strategy with simple search.** For moat, wedge, market, and
  pipeline work, generic web search can find leads but cannot by itself prove
  buyer pain or defensibility. Use You.com/specialist research routes first or
  label the output as a hypothesis.
- **Do not choose hypothesis mode for convenience.** For strategy work,
  `validated-research` is the default. Use `hypothesis` only when tools are
  unavailable/blocked or the user explicitly asks for a fast scan.
- **Do not hand-roll data synthesis.** If the work involves metrics, datasets,
  charts, quantitative findings, trends, cohorts, funnels, forecasts, or
  opportunity sizing, route through `ai-analyst` first and use its validated
  findings as the handoff.
- **Do not make ad hoc decks.** If the user asks for slides, PowerPoint,
  executive/board deck, or client-ready presentation, route to
  `branded-pptx-deck` and its QA gates. Do not present a deck as final without
  branded PPTX validation and preview review.
- **Do not skip the capability probe.** For strategy research, explicitly check
  for You.com, Reddit, Exa, Firecrawl, and subagent routes before falling back.
  Missing tools are a limitation to report, not a reason to pretend the
  evidence is stronger than it is.
- **Do not use simple search as Reddit validation.** Reddit claims must go
  through semantic probes, focused claims, retrieval, qualification, and human
  review when needed. Raw Exa `site:reddit.com` hits, old.reddit search output,
  or script weak-support false positives are not qualified evidence.
- **Do not accept off-topic Reddit rows.** If subreddit/source context,
  practitioner persona, workflow language, or concrete pain/objection/switching
  signal is missing, reject the row and report `no qualified Reddit evidence`.
- **Do not loop forever.** Respect the loop budget. Stop on no-progress,
  repeated actions, or polish-only remaining work.
- **Do not install external skills silently.** Discovery can be automatic;
  installation requires approval.
- **Do not let handoffs get vague.** Each handoff must say what changed, where
  the artifact is, what was verified, and what remains open.
