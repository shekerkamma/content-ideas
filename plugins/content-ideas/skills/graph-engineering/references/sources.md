# Sources

Every figure, quote, and command in this skill traces to a first-party page or
to the recorded workshop. Captured 2026-08-11.

## Primary — Anthropic

| Source | What it supports |
|---|---|
| [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) | The five composable patterns; workflow vs agent; "find the simplest solution possible"; when multi-agent does not fit |
| [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | The four state artifacts; JSON over Markdown; the six-step per-session boot sequence; the 200-feature initializer and the granularity example |
| [How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system) | Orchestrator-workers shape; 90.2% eval result; ~15× token cost; the five-criterion judge rubric; ~20 starting test cases |
| [When AI Builds Itself](https://www.anthropic.com/institute/recursive-self-improvement) | ">80% of code merged at Anthropic authored by Claude, as of May 2026"; the 8× merged-code-per-engineer figure and Anthropic's own caveat that it overstates the gain; 76% success rate on complex open-ended engineering problems |
| [Loop Engineering: Getting Started with Loops](https://claude.com/blog/getting-started-with-loops) | `/goal`, `/loop`, `/schedule`; turn caps; matching interval to data change rate |
| [Claude Code: Subagents](https://code.claude.com/docs/en/sub-agents) | Subagent file format, `.claude/agents/` vs `~/.claude/agents/`, frontmatter fields, tool restriction |

## Primary — recorded workshop

**"Build Agents That Run for Hours"** — Ash Prabaker and Andrew Wilson, applied
AI team at Anthropic. AI Engineer conference, 1:15:40.
<https://www.youtube.com/watch?v=mR-WAvEPRwE>

Supports the material that does not appear in the written posts:

- The generator/evaluator design is explicitly borrowed from GANs — generator
  builds, discriminator grades, adversarial pressure between them.
- **Why a separate critic works:** tuning a standalone critic to be harsh is
  tractable; tuning a builder to be self-critical is not. The restaurant
  analogy — easy to judge a meal, much harder to cook it.
- **The critic must not see the builder's context.** They tried the other way.
  It "muddies the two model streams" and makes it easier for the model to kid
  itself that something works. The critic says "this is an issue"; the builder
  reflects on its own work. (§ 60:45 in the recording.)
- **Three roles, not two:** planner, generator, evaluator — a PM / IC / QA org
  structure with a context window each. The planner deliberately does *not*
  plan granular technical details, because an error there cascades and
  magnifies across every sprint. It is kept out of the build loop; the spec is
  re-injected as a reference point instead.
- The 27 contract criteria figure, and the negotiation-before-work sequence.
- **Evaluator with hands:** Playwright MCP / Claude for Chrome MCP. The bugs
  caught — FastAPI route ordering that passes unit tests but breaks in prod, a
  boolean logic bug on a delete action.
- The retro game maker comparison: same prompt, same model, solo loop versus
  harness. ~$200 and ~6 hours for the harness run.
- **Course correction:** when the generator kept scoring low on one criterion,
  the harness discarded the work and restarted from scratch rather than
  patching. A behavior never seen when the generator judged itself.
- **Out of the box Claude is a bad QA agent** — "fix it later, might take two
  weeks."
- **Reading traces is the primary debugging loop**, not running more
  experiments. "No, you got to read the whole thing." Piping transcripts to a
  second agent is a first pass, not a replacement.
- The simplification pass: fresh-context-per-feature dropped, sprint
  decomposition dropped, evaluator cadence moved from per-sprint to end of
  generation. Roughly half the cost, better output. "The harness was not wrong;
  it was right for 4.5. The frontier moved."
- Brownfield caveat: the pattern is opinionated and suits greenfield. On an
  existing codebase, point the evaluator at the current state and expect to
  build your own rubric first.
- Human-in-the-loop belongs in hooks as a stop condition — and is usually
  covering for a harness problem better fixed in the harness.
- File system for shared state, with breadcrumbs left deliberately for the next
  model or human: "tried this, evaluated, found this bug, implemented this fix,
  this fix worked ✓" plus a timestamped log.

## Secondary — the walkthrough that prompted this skill

**"Graph Engineering: The Contract Loop Behind Self-Improving Claude Code
Agents"** — Josue Hernandez (Dapta), 8 pages, published 2026-08-10.
<https://dapta.notion.site/Graph-Engineering-The-Contract-Loop-Behind-Self-Improving-Claude-Code-Agents-3b7efeb61cbd8176b5d6c2b298efa30e>

Supplies the worked lead-qualification example, the `check_scores.py` shape, the
three-rung ladder, and the `contract.md` structure including the disputes
section. Its figures were spot-checked against the Anthropic pages above.

One correction carried into this skill: the guide presents the loop as two
roles. The workshop is explicit that it is three, and that the planner is
deliberately excluded from the build loop.

## Non-source

Andrew Ng's HumanEval figures (GPT-3.5 at 48.1% / GPT-4 at 67.0% single-pass vs
GPT-3.5 in an agentic loop at 95.1%) come from a Sequoia AI Ascent talk, cited
in the walkthrough. They support the general claim that loop structure beats a
model generation. They are not Anthropic figures and are not load-bearing for
anything this skill does — treat them as illustration, not evidence.
