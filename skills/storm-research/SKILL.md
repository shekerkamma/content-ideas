---
name: storm-research
description: Use when someone asks to run Storm Research, use the STORM method, run a STORM briefing/report on a topic, or wants a multi-perspective, citation-verified HTML research briefing. Runs five expert lenses (practitioner, academic, skeptic, economist, historian), builds a contradiction map, synthesizes a template-driven HTML report, then performs adversarial review and primary-source citation verification.
argument-hint: "[topic to research]"
user-invocable: true
allowed-tools: Bash, Read, Task, WebSearch, WebFetch, AskUserQuestion
permissions:
  network:
    - https://*
  file_read:
    - skills/storm-research/
  file_write:
    - storm-reports/
---

# Storm Research

## What This Does

Turns one topic into a verified, multi-perspective HTML briefing. The method
uses five expert lenses, maps where their claims contradict each other,
synthesizes the result into a self-contained HTML report, then adversarially
reviews and verifies the citations against primary sources before delivery.

Run the full pipeline end to end. Do not skip verification. This is heavier
than a quick lookup by design.

## Execution Model

This skill is a bounded deep-research workflow. Its core mechanism is
subagent fan-out: independent research agents investigate the same topic through
different lenses, then the main agent synthesizes and verifies their outputs.

- Resolve this skill's directory from the visible path of this `SKILL.md`; the
  report template is `report-template.html` in the same folder.
- Always use subagents when the host exposes them:
  - Claude Code: use `Task` / `general-purpose` agents.
  - Codex: use `multi_agent_v1.spawn_agent` when available.
  - Antigravity/OpenHands: use the host's available task/subagent mechanism.
- Spawn the five Phase 1 lens agents in parallel where the host supports
  parallel delegation. They must not share intermediate conclusions with one
  another. The main agent is the only synthesizer.
- Spawn Phase 4 verification agents separately from the lens agents. A verifier
  checks a citation cluster against primary sources; it must not merely trust
  the lens brief or draft report.
- If no subagent mechanism is available, stop and tell the user that the host
  cannot run true STORM. Offer a degraded single-agent approximation only if
  the user explicitly accepts that it is not a full STORM report.
- Do not quietly replace subagents with sequential prompting. That destroys the
  independence that makes the method useful.
- Host-specific tool mapping:
  - Codex uses `web.run` for current web research and source verification when
    needed;
  - use shell reads such as `sed`, `cat`, and `rg` for local files;
  - use `apply_patch` for manual file edits;
  - use `multi_tool_use.parallel` for independent shell reads/searches;
  - if a high-quality research plugin or repo skill such as `you-com-search`,
    `firecrawl`, `exa-api`, or `content-research` is explicitly available and
    appropriate, prefer it for source discovery and page ingestion. Use
    `you-com-search` before ordinary WebSearch for current-web discovery.
- Do not write deliverables to `.claude/skills`. Write reports under the current
  repo/workspace in `storm-reports/`.

## Source / Tool Order

1. Read this `SKILL.md` and `report-template.html` first.
2. Check local repo artifacts and prior `storm-reports/` or relevant run files
   if the topic clearly repeats prior work.
3. Use GBrain or durable memory when available for recurring companies,
   people, verticals, and themes.
4. Use `you-com-search` or Hermes You.com search when available for current web
   discovery, livecrawl, research, or finance research.
5. Use preferred specialist research plugins or MCPs when available, especially
   Exa for semantic discovery and Firecrawl for full-page source capture.
6. Use official and primary sources before secondary summaries.
7. Use generic web search as fallback or for source discovery, then verify
   final claims against primary sources.

## Phase 0: Scope the Topic

1. If the user supplied a topic, use it. Otherwise ask what to research.
2. State the interpretation of the topic in one line and proceed. Ask a
   clarifying question only when ambiguity would materially change the research.
3. Identify the reader's role so the action section is targeted. Infer from the
   user's context; if unclear, default to "a practitioner or decision-maker in
   this field."
4. Derive a lowercase kebab-case `topic-slug` for filenames.
5. Tell the user the pipeline is running: five lenses, contradiction map,
   synthesis, then verification.

## Phase 1: Five Expert Lens Agents

Spawn five distinct research agents. Use current, real sources and keep raw
lens briefs in your working notes, not in the chat unless the user asks.

Execution requirements:

- Spawn all five lens agents before synthesizing.
- Each lens receives the same topic framing and reader role, plus only its own
  lens prompt.
- Each lens must perform its own source discovery and return source URLs.
- Do not let a lens see another lens's output.
- Do not synthesize until all five lens briefs have returned.
- If one lens fails, retry that lens once. If it still fails, mark the run
  blocked or ask the user whether to continue with a missing-lens caveat.

For source quality, prefer primary or near-primary sources:

- official docs, company filings, product pages, changelogs, pricing pages;
- peer-reviewed papers, arXiv/preprints clearly labeled as such, university
  reports, government and regulator publications;
- credible operator case studies and direct practitioner accounts;
- market data from named firms with methodology disclosed;
- historical sources with dates, outcomes, and original context.

Each lens returns exactly:

1. `CORE POSITION` in two sentences.
2. `STRONGEST EVIDENCE` as 3-5 bullets, each with a concrete data point, named
   source, and URL.
3. `THE ONE THING` only that lens would say.

Keep each lens under 400 words.

### Lens Prompts

Use these instructions internally, substituting the topic and framing.

**The Practitioner**

You work with this topic daily. Research recent operator evidence, case
studies, implementation notes, practitioner threads, and workflow data. Surface
the gap between what hands-on operators know and what academics or pundits miss:
workflow friction, what actually works, where it breaks, and what is being
oversold.

**The Academic**

You care about rigorous evidence and effect sizes, not anecdotes. Research
peer-reviewed studies, arXiv/preprints, university and research-institute
reports, journals, and systematic reviews. Separate what the evidence actually
says from popular belief. Flag thin or contested evidence and label
peer-review status.

**The Skeptic**

You build the strongest rigorous bear case. Research failures, backlash,
contradicting data, policy/regulatory changes, debunkings, and negative case
studies. Answer what proponents conveniently ignore. Be skeptical, not
performatively contrarian.

**The Economist**

You follow the money. Research revenue, valuations, market size, funding flows,
unit economics, pricing, adoption incentives, margin pressure, and who benefits
from the current narrative. Every evidence bullet should include a real number
when available.

**The Historian**

You look for genuine historical parallels. Research prior technologies,
market shifts, manias, regulatory cycles, or adoption curves with dates and
outcomes. Explain which parallels fit, which do not, and what stabilized after
the initial narrative cycle.

After the five briefs are complete, give the user a short status note: where
the lenses converge and the sharpest disagreement.

## Phase 2: Map the Contradictions

Working only from the five lens briefs, build an internal contradiction map:

1. **Direct conflicts** - specific clashing claims, not broad themes.
2. **Strongest vs weakest evidence** - rank evidence using:
   peer-reviewed causal > official data > primary company/regulatory data >
   credible operator evidence > commissioned survey > analogy > preprint.
3. **The resolving question** - the single empirical question that would settle
   the biggest contradiction.
4. **Universal agreement** - what every lens confirms, even opponents. This is
   the load-bearing likely-true finding.
5. **Blind spot** - what no lens addressed. This becomes the missing sixth lens
   and feeds the frontier question.

This map is not a separate deliverable. It feeds the findings, supported-by and
challenged-by chips, hidden connection, missing sixth lens, claim safety guide,
and frontier question.

## Phase 3: Synthesize the HTML Report

1. Read `report-template.html` in this skill folder. Clone the structure and
   keep the CSS unless a user explicitly asks for design changes.
2. Fill every section:
   - **60-second summary**: decision-maker-grade, nuanced, and dense. Lead with
     settled facts, then contested interpretation.
   - **Five key findings ranked by reliability**: highest reliability first,
     each with a 1-10 evidence-quality score, supported-by chips, challenged-by
     chips, and any post-verification correction.
   - **Contested signal**: any demoted, preprint, commissioned, or weak claim.
   - **Hidden connection**: the non-obvious link visible only across lenses.
   - **Missing sixth lens**: the blind spot that could alter conclusions.
   - **Actionable insight**: 3-6 concrete moves for the reader role.
   - **Claim safety guide**: safe to assert, say with caveat, do not assert.
   - **Frontier question**: the single question that would change everything.
   - **References**: every citation with verification status.
3. Write the report to:

```text
storm-reports/{topic-slug}-briefing.html
```

Use a v2/post-verification report as the final deliverable. If you create an
intermediate draft, name it clearly and do not present it as final.

## Phase 4: Adversarial Review and Verification

Do not skip this phase.

### 4a. Self-Review

Before finalizing, score each of the five findings 1-10 for reliability and
justify the score internally. Identify the weakest link, what would verify it,
which lens dominated the synthesis, what got underweighted, the missing sixth
perspective, and an honest overall grade.

### 4b. Verify Every Citation

For each distinct citation cluster, spawn a verifier agent to check against the
primary source. Use live web access when current facts, product details,
pricing, company status, laws, standards, or recent events matter.

Execution requirements:

- Verification agents are independent from lens agents.
- A verifier receives one citation cluster only: the claim, cited figure or
  source, and draft report wording.
- Spawn verifier agents in parallel where possible, bounded to roughly 4-6
  agents by grouping related claims.
- Do not finalize the report until verifier results have been applied.

Verification prompt to apply:

```text
Independently verify a citation against its PRIMARY source.
CLAIM: {claim + cited figure + named source}
Find the primary source. Confirm or correct: exact title/authors/venue/year/URL,
the real figure or effect size as published, sample/method and author-stated
limits, and peer-review status when relevant. For contested claims, find the
strongest credible counter-source. Return VERDICT = CONFIRMED / PARTIALLY
CONFIRMED / UNVERIFIED / FALSE, then the corrected one-line citation, then
2-4 specifics with the primary URL.
```

### 4c. Apply Corrections

Edit the report before delivery:

- fix wrong figures, titles, dates, URLs, or characterizations;
- downgrade scores where evidence is thin;
- move preprints, commissioned surveys, and contested claims into the contested
  signal or caveat sections;
- cut fabricated or unverifiable claims;
- fill the verification banner with truthful counts:
  `N/N checked, X fabricated, Y corrected, Z demoted`;
- tag every reference as confirmed, corrected, contested, or demoted.

## Output

Final chat response should include:

- the report path;
- verification tally;
- the universal finding;
- the frontier question;
- a short claim-safety summary.

Keep the chat tight. The HTML report is the deliverable.

If the user asks you to open the file, use the platform opener only when
approved by the environment. In Codex sandboxed environments, it is acceptable
to provide the path instead of launching a browser.

## Guardrails

- Real research only. Every claim and URL must be traceable to a fetched or
  otherwise verifiable source.
- No invented studies, numbers, titles, or URLs. If a figure cannot be verified,
  demote or cut it.
- Disclose in the report that the panel is author-constructed; convergence is a
  strong hypothesis, not independent field consensus.
- Reliability means evidence quality, not strategic confidence.
- Target the reader's role. Do not default to generic advice when the user's
  context is available.
- Keep fan-out bounded: five lenses plus enough verification passes to check
  citation clusters. More perspectives require explicit user intent.
- Preserve the template's clean professional layout unless the user asks for a
  different style.

## Host Compatibility

### Target Hosts

- Claude Code: yes, with a mirror under `.claude/skills/storm-research/` if
  the user wants Claude auto-discovery.
- Codex/OpenAI: yes, canonical repo-local path:
  `skills/storm-research/SKILL.md`.
- OpenHands: yes, either through repo-local `skills/storm-research/` routing or
  a wrapper/mirror under `.agents/skills/storm-research/`.

### Canonical Source

The canonical source in this repo is `skills/storm-research/`. If mirrored into
`.claude/skills/` or `.agents/skills/`, keep this repo-local folder as the
source of truth and copy reviewed updates only.

### Tool Mapping

- Claude `Read` / `Grep` / `Glob` -> Codex shell reads / `rg`.
- Claude `Edit` / `MultiEdit` / `Write` -> Codex `apply_patch` for manual
  edits.
- Claude `Bash` -> Codex shell command with sandbox approval when needed.
- Claude `AskUserQuestion` -> concise Codex chat question, or numbered choices
  when repo `AGENTS.md` requires it.
- Claude `Task` / subagent -> Codex `multi_agent_v1.spawn_agent` when
  available; otherwise stop and ask before running a degraded approximation.
- Claude `WebSearch` / `WebFetch` -> preferred research plugins, official
  sources, or Codex web access with primary-source verification.

## Skill Relationships

### Category

Runbook

### Dependencies

Capabilities required for full STORM:

- A host subagent/task mechanism, such as Claude Code `Task` or Codex
  `multi_agent_v1.spawn_agent`.
- Web research/source retrieval for the lens agents and verifier agents.

Useful optional skills/tools:

- `you-com-search` - preferred current-web discovery/research route before
  generic WebSearch.
- `firecrawl` - full-page ingestion for important evidence sources.
- `exa-api` - semantic/source discovery when available.
- `content-research` - alternative broader research ingestion workflow.

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| host subagents | Prerequisite / Gate | always for a full STORM report | five lens briefs + verifier verdicts |
| `you-com-search` | Complement | when current web discovery/research is needed | candidate source URLs and You.com result JSON |
| `firecrawl` | Complement | when source pages need full-page capture | source URLs and captured page evidence |
| `exa-api` | Complement | when available for semantic/source discovery | candidate primary-source URLs |
| `content-research` | Alternative / Peer | when the user wants a broader research corpus instead of a single STORM briefing | research run files |

### Runtime Preamble

I'm using `storm-research` as a bounded deep-research run: five independent
lens agents, a main-thread contradiction map, and independent verifier agents.
If You.com, Firecrawl, or Exa is available, I may use it for discovery or source capture,
but the final artifact remains `storm-reports/{topic-slug}-briefing.html`.

## Gotchas

- **No subagents, no full STORM:** The method depends on independent lens
  agents and verifier agents. If the host has no subagent mechanism, stop and
  ask before running a degraded single-agent approximation.
- **False parallelism:** Running five prompts sequentially in one agent is not
  equivalent to five isolated agents. It can be useful brainstorming, but it is
  not a full STORM report.
- **Unverified v1 drafts:** Never deliver a first synthesis as final. The final
  report must include post-verification corrections and a truthful verification
  tally.
- **Primary-source drift:** Secondary articles often repeat old or incorrect
  figures. Verify titles, dates, methods, and numbers against primary sources
  before adding the reference status tag.
- **Template mismatch:** The template file is named `report-template.html` in
  this folder. Do not look for the downloaded filename
  `storm-research-report-template.html` during normal use.
- **Over-broad topics:** If the topic is too broad, narrow the frame enough for
  verifiable findings; do not produce a generic encyclopedia report.
