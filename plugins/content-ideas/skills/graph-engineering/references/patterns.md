# The five composable patterns

Anthropic publishes five patterns for agentic systems. That is the whole
vocabulary — everything complicated is these pieces stacked. Wiring them
together is what people call a graph: nodes that do work, edges that pass
results, state in the middle.

Read this when choosing a shape, or when someone proposes something elaborate
and you want to name what it actually is.

## Prompt chaining

Break the task into a fixed sequence; each step takes the previous step's
output. Put a programmatic **gate** between steps to stop bad work flowing
downstream.

**Use when** the subtasks are fixed and you know the order.

**Example** — write the proposal outline, gate it (does it name a price and a
timeline?), then write the full proposal from the approved outline. The gate is
a plain check, not a model call. If the outline has no price, the chain stops
instead of producing a polished proposal with a hole in it.

The gate is the part people skip and it is the cheap part: five lines of script
asking "does this file contain the three things it must contain?"

## Routing

Classify the input first, then send it down a specialized path.

**Use when** you have distinct categories genuinely better handled separately,
and the classification is reliable.

**Example** — inbound lead triage. Classify each message as pricing question,
support issue, or new opportunity, then route to a handler with its own
instructions. A pricing question gets your pricing context; a support issue gets
your help docs. Neither carries the other's baggage.

Routing also lets you route by cost: small fast model for the classification,
big model for the hard reasoning.

## Parallelization

Two different things share this name, and confusing them costs money.

**Sectioning** — split into independent pieces, run simultaneously. One agent
drafts the client email while another independently screens it against
compliance rules. Neither waits. Separating concerns this way tends to beat one
model juggling both.

**Voting** — run the same task several times and compare. Three independent
passes over a contract looking for unfavorable terms: two of three flagging the
same clause is probably real; one of three goes to a human. You are trading
tokens for confidence, deliberately.

**Use when** the pieces are independent (sectioning) or being wrong is
expensive (voting).

## Orchestrator-workers

A lead model breaks the task into subtasks *on the fly*, hands them to workers,
and combines results. The difference from parallelization: the subtasks are not
decided in advance — the orchestrator invents them based on what the input turns
out to be.

**Use when** you genuinely cannot predict the breakdown.

**Example** — research a prospect before a call. You do not know ahead of time
whether the interesting thread is their funding round, a hiring spree, or a bad
review cycle. The orchestrator reads what it finds and decides what to chase.

Anthropic's research system uses this shape — a lead agent with typically three
to five subagents on a complex query. It beat a single agent on the same model
by 90.2% on their internal research eval, and used roughly **15× the tokens** of
a normal chat turn. Both numbers come from the same page.

## Evaluator-optimizer

One model produces, another evaluates and sends back feedback, and they go
around again.

**Use when** you have clear criteria and the work genuinely improves with
critique. Anthropic's test: would a human reviewer's feedback measurably improve
this, and can a model give that same feedback? Yes to both means this fits.

**This is the pattern the `graph-engineering` skill builds.** It is the one
worth building first, because it is the only one of the five that directly
attacks self-evaluation. The other four move work around; this one checks it.

## Picking one

| Pattern | Use when | Cost |
|---|---|---|
| Prompt chaining | Fixed steps, known order | Low |
| Routing | Distinct categories, reliable classification | Low |
| Parallelization — sectioning | Independent pieces, want speed | Medium |
| Parallelization — voting | Being wrong is expensive | Medium to high |
| Orchestrator-workers | Cannot predict the subtasks | High |
| Evaluator-optimizer | Clear criteria, critique helps | Medium |

## The brake, from the vendor

> "Find the simplest solution possible, and only increase complexity when
> needed."

For many applications one well-built model call with good retrieval and a few
examples is enough. Add complexity only when it **demonstrably** improves
outcomes — and "demonstrably" means you measured, which means you needed
criteria, which is the contract.

## Where the loop composes

The generator/evaluator pair is not restricted to one builder and one critic.
It drops into a longer workflow: a generator for synthetic data with its own QA
agent, handing to an integrator with its own QA agent, and so on. Each builder
in a multi-step pipeline can carry its own critic. Agent teams and this pattern
overlap rather than compete — a team broken into front end, back end, and
integration each deserves a critic paired with it.

## When to skip all of this

- **Everything needs the same context.** If every step depends on knowing what
  every other step is doing, separate contexts create coordination cost with
  nothing to show for it.
- **The steps have heavy dependencies.** Most coding tasks have fewer genuinely
  parallel pieces than research does. If step three cannot start until step two
  finishes, separate agents buy you nothing.
- **You have no criteria.** No contract, no loop. The critic defaults to
  agreeable. Go write the criteria — that may have been the whole job.
- **A script would do.** Deterministic work gets a script, not reasoning.

## Cost, plainly

| Setup | Token cost |
|---|---|
| A normal chat turn | Baseline |
| A single agent with tools | ~4× |
| A multi-agent system | ~15× |

A concrete run: Anthropic's demo app with the full planner/builder/critic
harness took about six hours and roughly **$200**. Their later simplified
harness cost roughly **half** that and produced better work.

Fifteen times is not a rounding error. This pattern is for work where being
wrong costs more than the tokens.
