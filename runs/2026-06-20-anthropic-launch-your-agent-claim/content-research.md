# Content Research: Anthropic `launch-your-agent` Claim

Run date: 2026-06-20
Status: corrected after user-supplied repo

## Research Scope

Input claim: Anthropic released a free, open-source "Launch Your Agent" skill for Claude Code that interviews the user, builds a cloud-hosted agent, runs it 24/7, connects memory, improves every run, requires no server setup, and costs only API usage.

Correction context: My first pass searched `anthropics/skills` and missed the separate repository. The correct repo is `https://github.com/anthropics/launch-your-agent`.

Tooling status:
- GBrain MCP: not available in this host.
- Exa / Firecrawl keys: not configured in shell.
- Printing Press CLI: available, but no Exa or Firecrawl catalog/library entry exists for this run.
- Source discovery used: local clones of `anthropics/skills` and `anthropics/launch-your-agent`, GitHub web view, Anthropic/Claude docs, and official pricing docs.

## Bottom Line

The user-provided link is correct. Anthropic does have a public repository named `launch-your-agent`, and it contains a Claude Code skill at `.claude/skills/launch-your-agent/SKILL.md`.

The viral post is substantially more accurate than my earlier artifact said. The skill really is designed to take a technical founder from an idea to a Claude Managed Agent through interview, v0 scoping, launch, Outcome grading, iteration, and scheduled deployment when the task is recurring.

The remaining caveats are important:
- It is a **reference implementation**, explicitly marked "not maintained and not accepting contributions."
- It launches in the user's own Anthropic account and requires their `ANTHROPIC_API_KEY`.
- "Zero tool wiring" is still too strong. The skill structures tool, MCP, vault, memory, permission, and deployment configuration; it does not make those concerns disappear.
- "Only API costs" is imprecise. Official pricing says Claude Managed Agents are billed for tokens plus session runtime, with extra charges for tools such as web search.

Best framing: "Anthropic quietly shipped a reference Claude Code skill called `launch-your-agent`. It is not just a prompt; it is a guided agent-ops scaffold for Claude Managed Agents."

## Repo Search Findings

Local repo searched: `/tmp/anthropic-launch-your-agent-search`

Verified files:
- `/tmp/anthropic-launch-your-agent-search/README.md`
- `/tmp/anthropic-launch-your-agent-search/.claude/skills/launch-your-agent/SKILL.md`
- `/tmp/anthropic-launch-your-agent-search/.claude/skills/wrap-up/SKILL.md`
- `/tmp/anthropic-launch-your-agent-search/.claude/skills/launch-your-agent/references/interview.md`
- `/tmp/anthropic-launch-your-agent-search/.claude/skills/launch-your-agent/references/cma-api.md`
- `/tmp/anthropic-launch-your-agent-search/.claude/skills/launch-your-agent/references/examples-bank.md`
- `/tmp/anthropic-launch-your-agent-search/.claude/skills/launch-your-agent/references/build-sheet.example.json`
- `/tmp/anthropic-launch-your-agent-search/cma-primitives.md`
- `/tmp/anthropic-launch-your-agent-search/LICENSE`

Repo facts:
- Repo name: `anthropics/launch-your-agent`
- Skill name: `launch-your-agent`
- Trigger shown in README: `/launch-your-agent`
- Companion skill: `/wrap-up`
- License: Apache License 2.0
- Repo status: reference implementation, not maintained, not accepting contributions
- Latest cloned commit: `05e9627`, dated 2026-06-17

## Fact-Check Matrix

| Claim | Verdict | Evidence |
|---|---|---|
| "Anthropic just released a free, open-source skill for Claude Code." | True with caveat. | The public repo is under `anthropics/launch-your-agent`, includes `.claude/skills/launch-your-agent/SKILL.md`, and is Apache-2.0 licensed. Caveat: the README calls it a reference implementation and says it is not maintained. |
| "The skill is called Launch Your Agent." | True. | The repo is `launch-your-agent`, the skill manifest name is `launch-your-agent`, and the README tells users to type `/launch-your-agent`. |
| "Takes idea to live, cloud-hosted AI agent in minutes." | Mostly true, but "minutes" depends on setup and run time. | The skill is explicitly built to interview, scope a v0, stage payloads, launch a Managed Agent in the user's account, run it, grade it, and schedule it if recurring. It still needs Claude Code, an Anthropic API key, and successful API/tool configuration. |
| "Claude interviews you first." | True. | The main skill and `references/interview.md` define an iterative founder interview that maps answers to Managed Agents primitives: Agent, Environment, Session, Outcome, Tools, Skills, MCP, Vaults, Memory stores, and Deployments. |
| "Anthropic runs the loop 24/7 on their servers." | Directionally true with caveats. | Managed Agents are hosted by Anthropic and scheduled deployments can trigger sessions on cron. It is not literally always-on by default; scheduled deployments run on configured cadence, and each firing creates a session. |
| "Agents connect to memory and improve every run." | Partly true. | The skill supports memory stores, and `cma-primitives.md` frames memory as how run #10 can become smarter than run #1. But memory only helps if configured, attached, and written safely; it is not automatic model training. |
| "Zero server setup, no error handling, no tool wiring." | Overstated. | The skill removes much of the infra burden, but it still stages API payloads, tools, MCP servers, vault credentials, permission policies, memory resources, environment/networking, launch scripts, and troubleshooting fallbacks. |
| "You pay only API costs, no additional platform fee." | Mostly false / imprecise. | The repo says runs cost cents, but official pricing says Managed Agents are billed on tokens plus session runtime, and web search has separate standard pricing. Runtime is currently listed at $0.08 per session-hour. |
| "Agents write their own prompts and grade their own results." | Better phrased as Outcome-graded iteration. | The skill defaults to a `user.define_outcome` kickoff with rubric and `max_iterations: 3`. The Managed Agents harness grades each iteration with a separate grader and feeds gaps back for revision. |

## Source Bundle

Primary repo:
- `anthropics/launch-your-agent` — https://github.com/anthropics/launch-your-agent
- README: describes the Claude Code skill, `/launch-your-agent`, requirements, outputs, reference implementation status, and Apache 2.0 license.
- `.claude/skills/launch-your-agent/SKILL.md`: four-phase workflow: interview -> stage/launch -> grade/iterate -> run without the user.
- `.claude/skills/launch-your-agent/references/interview.md`: maps interview answers to CMA primitives.
- `.claude/skills/launch-your-agent/references/cma-api.md`: verified command shapes for agents, environments, sessions, outcomes, memory stores, vaults, and deployments.
- `cma-primitives.md`: inventory of Managed Agents primitives, limits, pricing/cost notes, scheduled deployments, memory, and constraints.

Primary docs:
- Claude Code skills docs — https://code.claude.com/docs/en/skills
- Agent Skills open standard — https://agentskills.io/
- Claude Managed Agents overview — https://platform.claude.com/docs/en/managed-agents/overview
- Managed Agents scheduled deployments — https://platform.claude.com/docs/en/managed-agents/scheduled-deployments
- Managed Agents memory stores — https://platform.claude.com/docs/en/managed-agents/memory
- Managed Agents outcomes — https://platform.claude.com/docs/en/managed-agents/define-outcomes
- Claude API pricing, Managed Agents section — https://platform.claude.com/docs/en/about-claude/pricing

Related repo:
- `anthropics/skills` — https://github.com/anthropics/skills
- Relevant prior finding: this repo contains `claude-api` and `/claude-api managed-agents-onboard`, which is related but not the same as `launch-your-agent`.

## Content Angle

Core angle: My earlier search looked in the general `anthropics/skills` repo and missed the separate `launch-your-agent` repo. The correction is more interesting than the error: Anthropic has packaged Managed Agents setup as a Claude Code skill, not just as API docs.

Positioning:
- Correction: "I was wrong: the repo exists."
- Practitioner: "Here is what the skill actually does."
- Strategic: "The durable shift is agent ops becoming a reusable skill."

Recommended title:
"Correction: Anthropic Really Did Ship `launch-your-agent`"

Alternate titles:
- "I Found the Real Anthropic Launch Your Agent Repo"
- "Anthropic's `launch-your-agent` Is Agent Ops in Skill Form"
- "This Claude Code Skill Turns Managed Agents Into a Founder Workflow"

## Hook Options

1. "I said Anthropic did not have a Launch Your Agent skill. I was wrong. It is a separate repo."
2. "The viral post was more accurate than I thought. Anthropic's `launch-your-agent` repo is real."
3. "This is not just a prompt. It is a Claude Code skill that walks a founder from idea to Managed Agent."
4. "The real story is not that Claude writes prompts. It is that agent setup is becoming a repeatable skill."

## Corrected LinkedIn Draft

Correction: Anthropic really did ship `launch-your-agent`.

I first searched the general `anthropics/skills` repo and did not find it.

The actual repo is separate:

`github.com/anthropics/launch-your-agent`

And it is more interesting than a prompt template.

It contains a Claude Code skill that walks a technical founder through:

- what they want the agent to do
- what "done" means
- what tools, files, repos, MCP servers, vaults, skills, memory, and schedule it needs
- how to scope the first version
- how to launch it in their own Anthropic account
- how to grade it with an Outcome rubric
- how to iterate
- how to schedule it if the task should recur

The claim still needs precision.

It is not "zero wiring."
It is structured wiring.

It is not "memory magically improves the model."
It is memory stores attached to sessions, with explicit read/write behavior.

It is not "free to run."
Managed Agents are billed for tokens and session runtime.

But the core idea is real:

Anthropic is turning agent operations into a reusable skill.

That is the shift worth paying attention to.

The future is not just better prompts.
It is packaged workflows that help agents launch, grade, remember, schedule, and improve safely.

## Video Brief

Concept: "I was wrong about Anthropic's Launch Your Agent skill"

Why now: The repo exists and directly matches the circulating claim more closely than the first-pass research indicated.

Differentiator: Lead with the correction, then separate verified mechanics from hype.

Suggested opening line: "I fact-checked the viral Anthropic agent post and got one thing wrong: I searched the wrong repo."

Structure:
1. Show the wrong first-pass conclusion.
2. Show the correct repo: `anthropics/launch-your-agent`.
3. Show the skill path: `.claude/skills/launch-your-agent/SKILL.md`.
4. Explain the flow: interview, scope v0, build `my-agent/`, launch in user account, Outcome grade, iterate, schedule.
5. Explain the caveats: reference implementation, API key required, token plus session-runtime billing, tool wiring still exists.
6. End with the takeaway: agent ops is becoming a skill.

Funnel: TOFU/MOFU. Strong correction hook; technical enough to build trust.

CTA: "Follow for repo-backed AI agent breakdowns, including the corrections."

## What Not To Repeat Without Precision

- Do not say it has no maintenance caveat. The README says reference implementation, not maintained, not accepting contributions.
- Do not say no setup is required. It needs Claude Code, an Anthropic API key, `.env` hygiene, staged payloads, and configured primitives.
- Do not say no tool wiring is needed. Say the skill guides and stages the wiring.
- Do not say memory automatically improves the agent. Say memory stores can persist state across sessions when configured.
- Do not say it is only token/API cost. Official pricing includes session runtime and tool charges such as web search.

## Next Research Steps

1. Run `/launch-your-agent` inside a clone if we want a hands-on teardown of generated artifacts.
2. Compare `launch-your-agent` with `/claude-api managed-agents-onboard` from `anthropics/skills` to map overlap and differences.
3. Produce a visual architecture explainer: Skill -> build sheet -> Agent/Environment/Session -> Outcome -> Memory -> Deployment.
4. Track the repo for new commits, releases, or whether it gets folded into the main `anthropics/skills` distribution.
