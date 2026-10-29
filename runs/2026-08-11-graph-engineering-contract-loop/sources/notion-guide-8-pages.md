# Graph Engineering: The Contract Loop Behind Self-Improving Claude Code Agents

Source: https://dapta.notion.site/Graph-Engineering-The-Contract-Loop-Behind-Self-Improving-Claude-Code-Agents-3b7efeb61cbd8176b5d6c2b298efa30e
Captured: 2026-08-11 via firecrawl

![](https://dapta.notion.site/image/attachment%3Add728317-c64c-4bdc-8101-0f8981a3ce3c%3Abanner-graphs.png?table=block&id=3b7efeb6-1cbd-8176-b5d6-c2b298efa30e&spaceId=16529611-8c72-42e4-8037-4243fa5e5e36&width=2000&userId=&cache=v2&imgBuildSrc=requestProxiedImageUrl)

![🔁 Page icon](https://notion-emojis.s3-us-west-2.amazonaws.com/prod/svg-twitter/1f501.svg)

# Graph Engineering: The Contract Loop Behind Self-Improving Claude Code Agents

Keyword

GRAPHS

Status

Published

Type

Technical Tutorial

Week

August 10, 2026

[\\
\\
Step 1: The Prompt Stopped Being the Unit](https://dapta.notion.site/Step-1-The-Prompt-Stopped-Being-the-Unit-3b7efeb61cbd81c0bbd1de3682273e7a?pvs=25)

[\\
\\
Step 2: The Five Ways to Wire Two Agents Together](https://dapta.notion.site/Step-2-The-Five-Ways-to-Wire-Two-Agents-Together-3b7efeb61cbd81e091e7cf78d7de92ff?pvs=25)

[\\
\\
Step 3: Where the State Actually Lives](https://dapta.notion.site/Step-3-Where-the-State-Actually-Lives-3b7efeb61cbd8192b6f4da5ee8ad3c70?pvs=25)

[\\
\\
Step 4: The Critic That Isn't Allowed to Be Nice](https://dapta.notion.site/Step-4-The-Critic-That-Isn-t-Allowed-to-Be-Nice-3b7efeb61cbd81e39221eb6b7897cb23?pvs=25)

[\\
\\
Step 5: The Contract, Where the Whole Thing Turns](https://dapta.notion.site/Step-5-The-Contract-Where-the-Whole-Thing-Turns-3b7efeb61cbd81a0bb3cd84c8e023f30?pvs=25)

[\\
\\
Step 6: Your First Loop, Today](https://dapta.notion.site/Step-6-Your-First-Loop-Today-3b7efeb61cbd81cd8c8ded10f7efac0e?pvs=25)

[\\
\\
Step 7: Knowing What to Delete](https://dapta.notion.site/Step-7-Knowing-What-to-Delete-3b7efeb61cbd81448881df3d29ac28bf?pvs=25)



Join 500+ business owners using AI to close more deals: [AI Sales & Beer Community](https://www.skool.com/ai-sales-beer)



Build a Claude Code setup where one agent does the work, a second agent grades it against criteria they agreed on before starting, and neither one gets to call the job done alone. Real configs, real commands, and the cost of running it.

By [Josue Hernandez](https://www.linkedin.com/in/josue-hernandez04)

YouTube: [@AIJosue](https://www.youtube.com/@AIJosue)

###  What You'll Build

A two-role Claude Code setup where a builder agent and a critic agent negotiate what "done" means before any work starts, then hold each other to it

A state layer that lives on disk instead of in the session, so your work survives when the session ends

An adversarial evaluator subagent with a written rubric, real tool permissions, and its own context

A scoring contract with criteria specific enough that the critic's feedback points at one thing to fix

A working lead qualification loop you can run today, where a second agent audits the first agent's scoring

A clear read on what this costs and when it is the wrong tool

###  Who This Is For

Founders and operators who already use Claude Code and keep hitting the same wall: it says the work is done, and it isn't

Anyone running repeated work that a person currently has to spot check

Operators who want the structure behind long-running agents without a Python orchestration framework

People who have read that prompting is over and want to know what actually replaces it

###  The Guide



Steps 1 and 2 set up the vocabulary. If you already know why a single agent cannot grade itself, start at Step 3 and build. Step 6 is the one you can run tonight.

####  Step 1: Step 1: The Prompt Stopped Being the Unit

What changed, according to the people who build the tool, and what the real numbers say versus the ones going around.

→ [Read Step 1: Step 1: The Prompt Stopped Being the Unit](https://app.notion.com/p/Step-1-The-Prompt-Stopped-Being-the-Unit-3b7efeb61cbd81c0bbd1de3682273e7a)

####  Step 2: Step 2: The Five Ways to Wire Two Agents Together

Anthropic ships five composable patterns. Here is each one with a job you actually run.

→ [Read Step 2: Step 2: The Five Ways to Wire Two Agents Together](https://app.notion.com/p/Step-2-The-Five-Ways-to-Wire-Two-Agents-Together-3b7efeb61cbd81e091e7cf78d7de92ff)

####  Step 3: Step 3: Where the State Actually Lives

The file system, not the session. Exact filenames, a schema you can copy, and the six things every run does on boot.

→ [Read Step 3: Step 3: Where the State Actually Lives](https://app.notion.com/p/Step-3-Where-the-State-Actually-Lives-3b7efeb61cbd8192b6f4da5ee8ad3c70)

####  Step 4: Step 4: The Critic That Isn't Allowed to Be Nice

Why self-review fails, and how to build an evaluator that uses the thing instead of reading about it.

→ [Read Step 4: Step 4: The Critic That Isn't Allowed to Be Nice](https://app.notion.com/p/Step-4-The-Critic-That-Isn-t-Allowed-to-Be-Nice-3b7efeb61cbd81e39221eb6b7897cb23)

####  Step 5: Step 5: The Contract, Where the Whole Thing Turns

Two agents argue about what "done" means before work starts. This is the piece almost nobody builds.

→ [Read Step 5: Step 5: The Contract, Where the Whole Thing Turns](https://app.notion.com/p/Step-5-The-Contract-Where-the-Whole-Thing-Turns-3b7efeb61cbd81a0bb3cd84c8e023f30)

####  Step 6: Step 6: Your First Loop, Today

Three rungs. A lead qualification loop where a second agent audits the first one's scoring.

→ [Read Step 6: Step 6: Your First Loop, Today](https://app.notion.com/p/Step-6-Your-First-Loop-Today-3b7efeb61cbd81cd8c8ded10f7efac0e)

####  Step 7: Step 7: Knowing What to Delete

What it costs, when it is the wrong call, and how to debug a loop that is quietly lying to you.

→ [Read Step 7: Step 7: Knowing What to Delete](https://app.notion.com/p/Step-7-Knowing-What-to-Delete-3b7efeb61cbd81448881df3d29ac28bf)

###  Sources

→ [Anthropic Engineering: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

→ [Anthropic Engineering: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

→ [Anthropic Engineering: How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)

→ [Anthropic: When AI Builds Itself](https://www.anthropic.com/institute/recursive-self-improvement)

→ [Claude: Loop Engineering: Getting Started with Loops](https://claude.com/blog/getting-started-with-loops)

→ [Documentation: Claude Code: Subagents](https://code.claude.com/docs/en/sub-agents)

→ [Optional deep dive: Build Agents That Run for Hours, a workshop by two engineers on Anthropic's applied AI team (AI Engineer conference, 1h16m)](https://www.youtube.com/watch?v=mR-WAvEPRwE)

→ [Course: Stanford CS329A: Self-Improving AI Agents](https://cs329a.stanford.edu/)


---

![🧩 Page icon](https://notion-emojis.s3-us-west-2.amazonaws.com/prod/svg-twitter/1f9e9.svg)

# Step 1: The Prompt Stopped Being the Unit

###  What the person who built the tool actually said

At Anthropic's developer conference, Boris Cherny, the creator of Claude Code, said this:

> "I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops."

The person who built the tool stopped writing instructions and started writing the thing that writes instructions. His unit of work moved up a level.

That is the whole shift. Not better prompts. A different object.

###  The real number, and the one going around

You have probably seen a version of this stat: "80% of Anthropic engineers use self-improving loops." Or 90%. Or 95%. Or 99%.

Here is what Anthropic's own page says:

> "As of May 2026, more than 80% of the code we merge into Anthropic's codebase was authored by Claude."

That is a statistic about code, not about people. Somewhere between the source and your feed, a number about how much code Claude writes turned into a number about how many engineers work a certain way. The second version does not appear anywhere on Anthropic's site. When you see the same claim with a different percentage every week, that is the tell.

The real numbers are good enough without help:

| Metric | Figure | Source |
| --- | --- | --- |
| Code merged at Anthropic authored by Claude | More than 80%, as of May 2026 | Anthropic |
| Code merged per engineer per day, Q2 2026 vs 2024 | 8x, and Anthropic calls this "almost certainly an overstatement of the true productivity gain" | Anthropic |
| Claude's success rate on complex open-ended engineering problems | 76% in May 2026, up 50 points in six months | Anthropic |

Notice that Anthropic argues against its own best-looking number. Lines of code measures quantity, not quality, so they flag the 8x as inflated. That is what a real source looks like.

###  Workflow or agent, and why you need to know which one you are building

Anthropic draws a line that matters the moment you start wiring things together.

A workflow is a system where the model and your tools run through predefined code paths. You decided the order. The model fills in the steps.

An agent is a system where the model dynamically directs its own process and tool usage, deciding how to get the job done.

Most of what people call an "AI agent" is a workflow, and that is usually the right answer. Workflows are predictable, cheaper, and easier to debug. You reach for a real agent when you genuinely cannot predict the steps ahead of time.

The reason this matters for you: when your automation misbehaves, the fix is different. A broken workflow means you wired the path wrong. A broken agent means it made a bad call at a decision point, and the fix is giving it a better way to check itself. Which brings us to the actual point of this guide.

###  The proof that structure beats a better model

The cleanest evidence for any of this is older than the current wave, and it holds up.

At Sequoia's AI Ascent, Andrew Ng showed results on HumanEval, a standard coding benchmark:

| Setup | Score |
| --- | --- |
| GPT-3.5, prompted once | 48.1% |
| GPT-4, prompted once | 67.0% |
| GPT-3.5, wrapped in an iterative agentic workflow | 95.1% |

The weaker model inside a loop beat the stronger model prompted once. Not by a little.

If you only take one thing from this page: the gap between a good prompt and a good loop is bigger than the gap between two model generations. You do not need to wait for the next release. You need to change the shape of what you are running.

###  The wall you have already hit

Here is the failure mode every one of these systems runs into, in the words of an engineer on Anthropic's applied AI team describing their own work:

Models are bad at judging their own output. Not sometimes. Structurally. It will build a button, see a button, and mark the feature done, when nothing is wired behind it. It will look at a half-finished job and call it finished, because it wants to agree with you.

You have felt this. You ask for something, it reports success, and the thing does not work. The instinct is to write a stricter prompt. That instinct is wrong, and Step 4 explains exactly why it cannot work no matter how strict you get.

The fix is structural. You stop asking one thing to both do the work and decide whether the work is good.

Next: Step 2 gives you the five ways Anthropic says you can wire two agents together, each with a job you actually run.


---

![🔀 Page icon](https://notion-emojis.s3-us-west-2.amazonaws.com/prod/svg-twitter/1f500.svg)

# Step 2: The Five Ways to Wire Two Agents Together

Anthropic publishes five composable patterns for building agentic systems. Five. That is the whole vocabulary, and everything complicated is these pieces stacked.

Wiring them together is what people have started calling a graph: nodes that do work, edges that pass results, and some state in the middle. Anthropic does not use that word. They just ship the pieces.

Here is each one with a job you actually run.

###  Prompt chaining

What it is: Break the task into a fixed sequence. Each step takes the previous step's output. You can put a programmatic check, what Anthropic calls a gate, between steps to stop bad work from flowing downstream.

When to use it: The subtasks are fixed and you know the order.

Your version: Write the proposal outline, gate it (does it name a price and a timeline?), then write the full proposal from the approved outline. The gate is a plain check, not a model call. If the outline has no price, the chain stops instead of producing a polished proposal with a hole in it.

> Tip: The gate is the part people skip, and it is the cheap part. A gate can be five lines of script asking "does this file contain the three things it must contain?"

###  Routing

What it is: Classify the input first, then send it down a specialized path.

When to use it: You have distinct categories that are genuinely better handled separately, and the classification is reliable.

Your version: Inbound lead triage. Classify each inbound message as pricing question, support issue, or new opportunity, then route each to a different handler with its own instructions. A pricing question gets your pricing context. A support issue gets your help docs. Neither one carries the other's baggage.

Routing also lets you route by cost. Send the easy classification to a small fast model and the hard reasoning to a big one. Anthropic names this directly as a use case.

###  Parallelization

Two different things share this name, and mixing them up will cost you money.

Sectioning: split the work into independent pieces and run them at the same time.

Your version: while one agent drafts the client email, another independently screens it against your compliance rules. Neither waits for the other. Anthropic notes that separating concerns this way tends to beat one model juggling both.

Voting: run the same task several times and compare the answers.

Your version: three independent passes over a contract looking for unfavorable terms. If two of three flag the same clause, it is probably real. If one of three flags something, it goes to a human. You are trading tokens for confidence, deliberately.

When to use it: Sectioning when the pieces are independent. Voting when being wrong is expensive and you want more than one look.

###  Orchestrator-workers

What it is: A lead model breaks the task into subtasks on the fly, hands them to worker models, and combines the results. The difference from parallelization: the subtasks are not decided in advance. The orchestrator invents them based on what the input turns out to be.

When to use it: You genuinely cannot predict the breakdown.

Your version: Research a prospect before a call. You do not know ahead of time whether the interesting thread is their recent funding round, a hiring spree, or a bad review cycle. The orchestrator reads what it finds and decides what to chase.

Anthropic's own research system uses this shape, with a lead agent and typically three to five subagents on a complex query. It beat a single agent on the same model by 90.2% on their internal research eval.

It also used roughly 15x the tokens of a normal chat turn. Both numbers are from the same page. Hold onto that, Step 7 comes back to it.

###  Evaluator-optimizer

What it is: One model produces, another evaluates and sends back feedback, and they go around again.

When to use it: You have clear criteria and the work genuinely gets better with a round of critique. Anthropic gives a simple test: would a human reviewer's feedback measurably improve this, and can a model give that same feedback? If yes to both, this pattern fits.

Your version: Everything in Steps 4 through 6 of this guide.

This is the one worth building first, because it is the only one of the five that directly attacks the problem from Step 1. The other four move work around. This one checks it.

###  Pick one

| Pattern | Use when | Cost |
| --- | --- | --- |
| Prompt chaining | Fixed steps, known order | Low |
| Routing | Distinct categories, reliable classification | Low |
| Parallelization, sectioning | Independent pieces, want speed | Medium |
| Parallelization, voting | Being wrong is expensive | Medium to high |
| Orchestrator-workers | Cannot predict the subtasks | High |
| Evaluator-optimizer | Clear criteria, critique helps | Medium |

###  Anthropic's own brake

This is on their page and it deserves quoting, because it argues against building the complicated thing:

> "Find the simplest solution possible, and only increase complexity when needed."

They go further: for many applications, one well-built model call with good retrieval and a few examples is enough. Add complexity only when it demonstrably improves outcomes.

"Demonstrably" is doing real work in that sentence. It means you measured. Which means you need something to measure against, and that is a contract, and that is Step 5.

Next: Step 3 answers the question that breaks most first attempts. When your loop runs twenty times, where does the work actually live?


---

![💾 Page icon](https://notion-emojis.s3-us-west-2.amazonaws.com/prod/svg-twitter/1f4be.svg)

# Step 3: Where the State Actually Lives

Your loop is going to run more than once. Something has to remember what happened last time.

The answer Anthropic landed on, after building agents that run for hours, is the least exciting one available: the file system. Not a database. Not a vector store. Files on disk, in a git repo.

An engineer on their applied AI team put it plainly in their conference workshop: they are a big fan of using a file system for shared state for long-running agents. That is the whole design.

###  The four artifacts

Anthropic's published harness uses an initializer agent that runs once at the start, and then a worker agent that gets woken up over and over. The initializer's only job is to leave behind a state layer the worker can pick up cold.

It creates four things:

| Artifact | What it holds |
| --- | --- |
| feature\_list.json | Every unit of work, each with a pass or fail status |
| claude-progress.txt | A running log of what happened, in plain language |
| init.sh | The boot script that gets the environment running |
| Git repo, with an initial commit | The actual history of the work |

That is it. Four files and a repo.

init.sh

is worth calling out because it is easy to skip. It is a script the initializer writes so that every future run has one command to get started, instead of rediscovering how to launch the thing every single time. Small file, saves an enormous amount of repeated fumbling.

###  Why JSON and not Markdown

This is a one-line detail that decides whether your loop survives to run twenty.

From Anthropic's write-up:

> "The model is less likely to inappropriately change or overwrite JSON files compared to Markdown files."

Models treat Markdown as something to rewrite. They treat JSON as a data structure to update. If you keep your task list in

tasks.md

, you will eventually come back and find it "cleaned up," reorganized, with completed items quietly dropped. Keep the status in JSON. Keep the narrative in text.

> This is the single cheapest fix in this guide. Change one file extension, remove one whole category of failure.

###  A schema you can copy

Anthropic's example broke one vague request into more than 200 granular features, every one starting marked as failing. Their sample of what "granular" means:

> "a user can open a new chat, type in a query, press enter, and see an AI response"

That is one item. Not "build chat." Notice it describes something you can go do and watch succeed or fail.

Here is the shape, adapted to work you would actually run:

{"project":"Q3 lead qualification pass","created":"2026-08-10","items":\[{"id":1,"name":"Every lead in leads-raw.csv has a score between 1 and 5","status":"failing","verified\_by":"python3 scripts/check\_scores.py","notes":""},{"id":2,"name":"No lead is scored 4 or 5 without a named decision maker","status":"failing","verified\_by":"python3 scripts/check\_scores.py --rule decision-maker","notes":""},{"id":3,"name":"Every score has a one-line reason citing a field from the source row","status":"failing","verified\_by":"manual review by auditor agent","notes":""}\]}

​

Two fields carry the weight.

status

is only ever

failing

or

passing

. No "in progress," no "mostly done." A binary state is the only kind an agent cannot talk its way around.

verified\_by

is the command or check that decides. If you cannot write anything in that field, the item is written badly. Rewrite it until you can.

###  The six things every run does on boot

Anthropic publishes the exact per-session sequence. Each run:

Runs

pwd

to confirm where it is

Reads the git log and the progress file to find out what already happened

Picks the highest-priority incomplete item, just one

Starts the environment using

init.sh

Runs a basic end-to-end test to confirm things work before touching anything

Implements that one item, commits, and updates the progress file

Step 3 is the discipline that makes the whole thing work. One item per run. Not "as many as you can." The moment a run tries to do four things, a failure in the third one poisons the record of the first two, and you cannot tell from the outside what state you are in.

Step 5 is the one people cut, and it is the one that saves you. Confirming the environment works before making changes means that when something breaks afterward, you know the change caused it.

###  What goes in the progress file

claude-progress.txt

is for the things JSON cannot hold: what was tried, what failed, and what the next run should know.

2026-08-10 14:02 \| item 2 \| Added decision-maker rule check.
Found 14 of 61 leads scored 4+ with no named contact. Downgraded to 3.
Note for next run: 6 of those had a contact in the "notes" column,
not the "contact" column. Parser only reads "contact". Worth fixing.

​

That last line is the value. A run found something it was not asked to look for and left it where the next run will see it. This is how a loop gets smarter across runs without anyone retraining anything.

###  Before you move on

Your state layer is right when a run that knows nothing can open the folder, read three files, and correctly answer: what is done, what is next, and what went wrong last time.

If answering that needs anything from the previous session, the state layer is not done yet.

Next: Step 4 builds the piece that decides whether an item actually passes, and explains why it cannot be the same agent that did the work.


---

![🔍 Page icon](https://notion-emojis.s3-us-west-2.amazonaws.com/prod/svg-twitter/1f50d.svg)

# Step 4: The Critic That Isn't Allowed to Be Nice

Almost everyone builds this wrong the first time. You open one session, do the work, and tell it to check its own output. It says the work is good. The work is not good.

The reason this fails is not that your prompt was too soft. It is structural, and once you see it you cannot unsee it.

###  The asymmetry that makes a separate critic work

Here is how the applied AI team at Anthropic explains their own design choice.

Yes, the evaluator is also a language model. Yes, it has the same bias toward liking model-generated output. So why does splitting it into two help at all?

Because tuning a standalone critic to be harsh is very tractable. Tuning a builder to be self-critical is not.

Their analogy is the right one. It is easy to walk into a restaurant and tell you honestly whether the meal was good. It is much harder to cook it. Criticism and creation are different jobs with different difficulty, and you get more out of a model by asking it to do the easy one in isolation than by asking one model to do both at once.

An agent that just spent forty minutes building something is the worst possible judge of it. It has every reason to believe it worked. Give the judging job to something that did not do the work, does not know how hard it was, and was told its job is to find problems.

> The rule: self-evaluation is a trap. Use an adversarial evaluator. This was the first of five closing points in Anthropic's own workshop.

###  Building the evaluator as a real subagent

Claude Code already ships the primitive. A subagent gets its own context window, its own system prompt, its own tool permissions. That separation is exactly what you need.

Subagents are Markdown files with YAML frontmatter. Two locations:

| Location | Scope |
| --- | --- |
| .claude/agents/ | This project only |
| ~/.claude/agents/ | Every project on your machine |

The frontmatter fields are

name

,

description

,

tools

, and

model

. Everything after the frontmatter is the system prompt.

Here is a working evaluator. Save it as

.claude/agents/auditor.md

:

\-\-\-name: auditor
description: Adversarially audits completed work against the contract in contract.md. Use after any item is marked complete, before it is accepted.
tools: Read, Grep, Glob, Bash
model: sonnet\-\-\-

You are an auditor. Your job is to find what is wrong with completed work.

You did not do this work and you owe it nothing.

Process:
1. Read contract.md. These are the only criteria that count.
2. Read the actual output. Not the summary of the output. The output.
3. Score every criterion 0.0 to 1.0, then give one pass/fail grade.
4. For every score below 1.0, name the exact file and line, quote what
is wrong, and state what would make it pass.

Rules:
- "Looks fine" is not a finding. Every criterion gets a specific verdict.
- If a criterion cannot be checked from the evidence in front of you,
score it 0.0 and say the evidence is missing. Do not assume it passed.
- Never suggest deferring a problem. "Fix later" is not available to you.
- A single failed criterion fails the whole item. There is no partial pass.

​

Note the

tools

line.

Read, Grep, Glob, Bash

and nothing else. The auditor cannot edit files. It cannot quietly fix the thing it was supposed to report. Constraining tools is half the reason to use a subagent at all.

###  Make the critic use the thing

The biggest upgrade to an evaluator is not a better prompt. It is giving it hands.

In Anthropic's setup, the evaluator does not read a summary of what changed. It opens the actual thing, clicks around, and tries to use it. For web work they point at Playwright MCP or Claude for Chrome MCP.

claude mcp add playwright -- npx -y @playwright/mcp@latest

​

The difference this makes is not subtle. The bugs their evaluator caught were things like a route ordering problem that passed every unit test but would break in production, and a boolean logic bug on a delete action. Neither is findable by reading a diff. Both are obvious within ten seconds of actually using the thing.

For non-browser work the same principle holds: the check has to run the output, not describe it. That is what the

verified\_by

field from Step 3 is for.

###  Two rubrics worth stealing

Anthropic has published two, from different systems, and they are good starting points.

The taste rubric, from their app-building harness. Four criteria: design, originality, craft, functionality. They weight it toward design and originality, because recent models already handle functionality well and the thing they were fighting was generic output. They calibrate it with a handful of reference examples so the evaluator's taste converges on theirs.

The interesting claim underneath it: most people assume subjective quality cannot be graded. Anthropic's position is that it can, if you have a strong enough opinion and you write it down. If you know what good looks like for your work and have never written it out, that is the missing piece.

The judge rubric, from their research system. Five criteria:

| Criterion | Question |
| --- | --- |
| Factual accuracy | Do the claims match the sources? |
| Citation accuracy | Do the cited sources actually say that? |
| Completeness | Are all requested aspects covered? |
| Source quality | Primary sources, or the easy secondary ones? |
| Tool efficiency | Did it take a reasonable path to get here? |

Output format: scores from 0.0 to 1.0 plus a pass/fail grade, from a single judge call. They started with about 20 test cases, which is a much lower bar to begin than most people assume.

###  Yours will be too nice at first

Be ready for this, because it is normal and it is not your fault.

Anthropic was direct about it: out of the box, Claude is a bad QA agent. In their early runs the QA role would find a real bug and respond with something like "fix it later, might take two weeks," and move on. The same generosity that shows up everywhere else shows up here.

They fixed it by tuning, not by finding a magic prompt. Which is the subject of Step 7.

Two things help immediately:

Remove the escape hatches. Notice the auditor prompt above bans "fix later" explicitly and bans partial passes. Every soft option you leave available will get used.

Make failure the default. "Score 0.0 if you cannot verify it" flips the burden. The work has to prove it passed, instead of the critic having to prove it did not.

Next: Step 5 is the piece that turns two agents into a system. Before either one starts, they have to agree on what "done" means.


---

![🤝 Page icon](https://notion-emojis.s3-us-west-2.amazonaws.com/prod/svg-twitter/1f91d.svg)

# Step 5: The Contract, Where the Whole Thing Turns

You now have a builder and a critic. Here is the question that decides whether they work as a system or just take turns being wrong.

What is the critic grading against?

The obvious answer is the original request. That answer is why most two-agent setups underperform.

###  Two agents negotiate before anyone works

This is the piece from Anthropic's harness that almost nobody replicates, and it is the one their engineer flagged as the key innovation.

Before the builder writes a single line, the two agents negotiate what "done" means.

The sequence:

The builder proposes: here is what I am going to build, and here is how you should verify it.

The critic pushes back: that scope is too big, those tests are too weak, and you missed this edge case.

They go back and forth through files on disk. One writes Markdown, the other reads it, and around again.

When both agree, the contract is frozen. Then work starts.

The critic grades against the contract they agreed on, not against the original one-line request.

That fifth point is the whole thing. The critic is not holding the work up against a vague ask and improvising a standard. It is checking against criteria that both parties already signed off on, written down, before anyone had a reason to be defensive about them.

> Why this matters: it converts a fuzzy user story into testable assertions, without forcing whoever wrote the original request to specify everything up front. You get precision at the point where it is cheap to produce.

###  What the older approach was missing

The widely-copied version of this is a loop with a fixed plan file. Write

plan.md

, then loop until the plan is done.

Anthropic's assessment of the gap: it had a fixed plan, but nobody on the other side is arguing with the main loop.

A plan written once, by one agent, before anything was attempted, is a guess. It never gets challenged. Every error in it survives to the end and quietly shapes everything downstream. The negotiation exists to get a second, hostile pair of eyes on the standard itself, not just on the work.

###  Twenty-seven criteria, not six

For one app, their generator and evaluator settled on 27 contract criteria.

That number surprises people. Here is the reasoning, and it is the most practically useful thing on this page:

> Vague criteria produce vague critiques. The builder shrugs and does whatever. Granular criteria mean the agent knows: I need to fix this exact line.

Criteria granularity is not bureaucracy. It is the difference between feedback that causes a change and feedback that causes a shrug.

Too vague:

\- The lead scoring should be accurate
\- Output should be well organized
\- Handle edge cases appropriately

​

Nothing there can fail. Nothing there tells anyone what to do.

Actionable:

\- Every row in leads-scored.csv has a score of exactly 1, 2, 3, 4 or 5
\- No row scored 4 or 5 has an empty contact\_name field
\- Every score has a reason field of 10 words or more
\- Every reason quotes at least one value from the source row
\- Rows with a company\_size under 10 are never scored above 3
\- The row count in leads-scored.csv equals the row count in leads-raw.csv
\- No company appears twice in the output

​

Seven criteria. Every one is a yes or no. Several are checkable by a script with no model involved at all. When the critic says criterion four failed on rows 12, 30 and 55, the builder knows exactly what to do.

The test: read a criterion and ask whether two reasonable people could disagree about whether it passed. If they could, it is not written yet.

###  The behavior you only get from this setup

Here is a payoff that is easy to miss.

Imagine the builder keeps scoring badly on one specific criterion. It tries, gets marked down, tries again, gets marked down.

A single-agent loop patches the same broken thing forever. It has no way to conclude that the approach is wrong, only that this attempt was wrong.

A two-role setup with a scored contract throws the whole thing out and starts over. Anthropic saw exactly this: when the generator kept scoring low on one criterion, the harness would discard the work and try a different approach from scratch, rather than keep patching.

That ability to change course over a long run is not something you can prompt into a single agent. It comes from having scores over time, from someone other than the person who did the work.

###  The contract file

Keep it as

contract.md

next to your state files from Step 3. A working shape:

# Contract: Q3 lead qualification pass
Status: AGREED
Agreed on: 2026-08-10
Parties: qualifier (builder), auditor (critic)

## Scope
Score all 61 leads in leads-raw.csv. Output to leads-scored.csv.
Not in scope: enriching missing data, contacting anyone.

## Criteria\|#\| Criterion \| Check \|\|\-\-\-\|\-\-\-\|\-\-\-\|\| 1 \| Every row scored 1-5, no blanks \| scripts/check\_scores.py \|\| 2 \| No 4 or 5 without contact\_name \| scripts/check\_scores.py --rule dm \|\| 3 \| Every score has a reason, 10+ words \| scripts/check\_scores.py --rule reason \|\| 4 \| Every reason quotes a source-row value \| auditor, spot check 10 rows \|\| 5 \| company\_size under 10 never scored above 3 \| scripts/check\_scores.py --rule size \|\| 6 \| Output row count equals input row count \| scripts/check\_scores.py --rule count \|\| 7 \| No duplicate companies in output \| scripts/check\_scores.py --rule dupes \|## Disputes resolved during negotiation- Builder proposed scoring 1-10. Auditor rejected: too granular to
defend, no way to tell a 6 from a 7. Settled on 1-5.
- Auditor proposed requiring a LinkedIn URL on every 4+. Builder
rejected: not present in source data for 40% of rows. Dropped.

## Grading
Any criterion failing fails the item. No partial pass.

​

The disputes section is worth keeping. Six weeks from now, when someone asks why the scoring is 1 to 5, the answer is right there, along with the fact that somebody argued for something else and lost on the merits.

###  Kicking off the negotiation

You do not need special tooling. This prompt starts it:

Before writing any code, negotiate a contract with the auditor subagent.

1\. Draft contract.md: the scope, and the specific criteria you should be
held to. Every criterion must be checkable, ideally by a script.
2\. Ask the auditor to review it adversarially. It should push back on
scope that is too broad, criteria that are too weak, and anything missing.
3\. Revise. Repeat until the auditor agrees with no outstanding objections.
4\. Set Status: AGREED, then start work.

Do not begin the actual work until the contract says AGREED.

​

Watch that first negotiation happen. It is the fastest way to find out that what you asked for was ambiguous, and it costs a couple of minutes instead of an afternoon.

Next: Step 6 puts all of it together into a loop you can run tonight, on real work.


---

![🚀 Page icon](https://notion-emojis.s3-us-west-2.amazonaws.com/prod/svg-twitter/1f680.svg)

# Step 6: Your First Loop, Today

Three rungs. Each one runs on its own, and each one is useful before you climb to the next. Do not skip to rung three.

The worked example is lead qualification, because it is the kind of job where an agent being generous with itself costs you real money. A lead scored 5 that should have been a 2 sends someone chasing nothing.

###  Setup

mkdir lead-loop &&cd lead-loop
git init

​

Drop your leads in as

leads-raw.csv

. Anything with a company name, size, industry, and a contact field works:

company,company\_size,industry,contact\_name,notes
Ridgeline HVAC,34,home services,Dana Ruiz,inbound from site form
Coastal Realty Group,8,real estate,,asked about pricing twice
Merrick Plumbing,120,home services,Sam Oyelaran,referred by existing client

​

###  Rung 1: One agent, one goal, one real check

The smallest useful loop. No subagents yet. What makes it a loop instead of a prompt is the stop condition and the verification command.

First, write the check. This is the part that makes the whole thing honest, and it is plain Python with no model in it:

\# scripts/check\_scores.pyimport csv, sys

rows =list(csv.DictReader(open('leads-scored.csv')))
raw =list(csv.DictReader(open('leads-raw.csv')))
fails =\[\]iflen(rows)!=len(raw):
fails.append(f"row count {len(rows)} != input {len(raw)}")

seen =set()for i, r inenumerate(rows, start=2):
score = r.get('score','').strip()if score notin{'1','2','3','4','5'}:
fails.append(f"row {i}: score '{score}' not in 1-5")continueif score in{'4','5'}andnot r.get('contact\_name','').strip():
fails.append(f"row {i}: scored {score} with no contact\_name")iflen(r.get('reason','').split())<10:
fails.append(f"row {i}: reason under 10 words")if r.get('company\_size','').isdigit()andint(r\['company\_size'\])<10 \
and score in{'4','5'}:
fails.append(f"row {i}: company\_size under 10 scored {score}")if r\['company'\]in seen:
fails.append(f"row {i}: duplicate company {r\['company'\]}")
seen.add(r\['company'\])print(f"FAIL ({len(fails)})"if fails else"PASS")for f in fails\[:25\]:print(" -", f)
sys.exit(1if fails else0)

​

Now run the loop:

/goal Score every lead in leads-raw.csv into leads-scored.csv with columns
company, score, reason. Score 1-5 on fit for AI phone automation: a good
fit is a service business that misses inbound calls, has a named contact,
and 10 or more staff. Every reason must be 10+ words and quote a value
from the source row. Run \`python3 scripts/check\_scores.py\` after each pass
and keep fixing until it prints PASS. Stop after 5 attempts.

​

Three things make this work:

A verifiable exit.

/goal

runs until the goal is met or the turn cap hits. "Until the script prints PASS" is a condition a script decides, not the model.

A real turn cap. "Stop after 5 attempts." Without it, a loop that cannot succeed will keep spending. Anthropic's own example uses exactly this phrasing.

A check the model cannot argue with. Exit code 1 is exit code 1.

> Run this rung on real data before going further. You will learn more from watching it fail the check three times than from reading the rest of this page.

###  Rung 2: Add the critic and the contract

Rung 1 catches everything a script can catch. It cannot catch a score of 5 justified by a reason that sounds great and is not supported by anything in the row. That needs judgment, from something other than the thing that produced it.

Create the auditor from Step 4 at

.claude/agents/auditor.md

. Then negotiate the contract from Step 5:

Before scoring anything, negotiate a contract with the auditor subagent.

Draft contract.md with the scope and the specific criteria you should be
held to. Have the auditor review it adversarially and push back on weak
criteria. Revise until it agrees. Set Status: AGREED, then start.

​

Let the negotiation finish. Read

contract.md

yourself. This is the moment you find out whether "good fit" meant what you thought it meant.

Then run the loop:

/goal Work through contract.md one criterion at a time.

For each: do the work, run its check, then hand off to the auditor
subagent to grade it against contract.md. Only mark an item passing when
the auditor grades it pass. If the auditor fails an item, fix exactly
what it named and resubmit.

Update feature\_list.json and claude-progress.txt after each item, and
commit. Stop when every criterion passes or after 15 attempts.

​

You now have the full pattern: a builder, an adversarial critic with its own context, a frozen contract, and state on disk.

The failure you are most likely to see is the one from Step 4: the auditor being too generous. If it passes something you can see is wrong, that is not a reason to abandon the setup. It is the tuning loop starting, and Step 7 covers it.

###  Rung 3: Take yourself out of it

Once a loop runs clean twice in a row unattended, put it on a schedule.

Claude Code gives you three ways to run a loop, and they differ in how they stop:

| Command | Runs | Stops when |
| --- | --- | --- |
| /goal | Now, in your session | Goal met or turn cap hit |
| /loop | On an interval, locally | You cancel, or you close the session |
| /schedule | On Anthropic's cloud | You disable it |

/loop

keeps going while your session is open:

/loop 30m check leads-raw.csv for new rows, score any that are missing
from leads-scored.csv, and have the auditor grade them against contract.md

​

/schedule

survives you closing the laptop:

/schedule every weekday at 7am: score any new leads in leads-raw.csv
against contract.md. /goal: don't stop until every new lead is scored and
the auditor has graded the batch pass. Append a summary line to
claude-progress.txt.

​

Match the interval to how often the data actually changes. This is Anthropic's own guidance and it is the most common way people waste money here. If leads arrive a few times a day, a loop every five minutes is doing nothing 95% of the time and billing you for it.

Then check what it cost:

/usage

​

/usage

breaks down token spend by skill and subagent, so you can see whether the auditor is eating more than the builder. Run it after the first scheduled week, before you scale anything up.

###  Where to stop

Most operators should live on rung 2 for a while. Rung 3 is only worth it when the work genuinely arrives on its own schedule and you have already watched the loop run clean without you.

The ladder is the point. A loop you trust doing one job beats an ambitious one you have to check every morning, which is just the original problem with extra steps.

Next: Step 7 covers what this costs, when it is the wrong tool, and how to debug a loop that is quietly telling you what you want to hear.


---

![✂️ Page icon](https://notion-emojis.s3-us-west-2.amazonaws.com/prod/svg-twitter/2702-fe0f.svg)

# Step 7: Knowing What to Delete

Every guide on this subject ends by telling you to build more. This one ends by telling you what to take out, because that is the part that decides whether you are still running this in three months.

###  What it actually costs

The numbers, all from Anthropic's own pages:

| Setup | Token cost |
| --- | --- |
| A normal chat turn | Baseline |
| A single agent with tools | About 4x a chat turn |
| A multi-agent system | About 15x a chat turn |

And a concrete run: the demo app their team built with the full planner, builder and critic harness took about six hours and roughly $200.

Fifteen times is not a rounding error. If you are running a loop hourly on work that a single well-aimed call could handle, you built an expensive way to get the same answer.

The honest framing: this pattern is for work where being wrong is more expensive than the tokens. Lead scoring qualifies, because a bad score sends a person chasing nothing for a week. Reformatting a spreadsheet does not.

> Run
>
> /usage
>
> after your first week. Compare it against the cost of a person doing the same job. If those numbers are close, simplify.

###  When this is the wrong tool

Anthropic publishes its own list of where multi-agent setups do not fit, which is a useful thing for a vendor to publish.

Skip it when the work needs everything to share the same context. If every step depends on knowing what every other step is doing, splitting it across agents with separate contexts creates coordination cost with nothing to show for it.

Skip it when the steps have heavy dependencies on each other. Their own example: most coding tasks have fewer genuinely parallel pieces than research does. If step three cannot start until step two finishes, running them as separate agents buys you nothing.

Skip it when you have no criteria. If you cannot write down what "good" looks like, the critic has nothing to grade against and will default to being agreeable. No contract, no loop. Go write the criteria first, and you may find that was the whole job.

Skip it when a script would do. If the check is deterministic, write the script. Anthropic's own guidance is to use scripts for deterministic work rather than reasoning. The

check\_scores.py

from Step 6 catches most problems and costs nothing to run.

###  How to actually debug this

When your loop starts producing work that passes but is obviously wrong, the instinct is to run it again with a tweaked prompt. That instinct wastes days.

Anthropic was direct about what worked for them. The primary debugging loop was reading the traces, not running more experiments. Reading what the agent actually did, finding where its judgment diverged from a human's, and tuning the prompt for that specific divergence.

They compared it to reading a stack trace, and that is the right comparison. You are not guessing. You are looking at the moment it went wrong.

Their tooling tip, which you can copy today: pipe agent transcripts into files, then have a second agent read through them and suggest prompt updates. You end up with a loop that improves the loop.

mkdir -p traces
claude -p "$(cat prompts/scoring-run.txt)"> traces/run-$(date +%F-%H%M).txt 2>&1

​

Then, in a fresh session:

Read every file in traces/. Find each point where the auditor passed
something it should have failed. For each one, quote the exact moment,
say what a careful human reviewer would have caught, and propose a
specific edit to .claude/agents/auditor.md that would have caught it.
Do not rewrite the whole prompt. Give me targeted changes.

​

This is the part nobody wants to do, and it is the part that separates a loop that works from a loop that looks like it works.

###  The scaffolding is temporary, and that is the point

Here is the thing that reframed this for me.

Anthropic's team went back to their own harness and deleted parts of it. They had built a setup that started a fresh session for every single feature, because the model at the time needed the reset. A model generation later, it did not. They dropped it and ran one continuous session instead.

They also stopped running the evaluator after every sprint and moved it to the end of a generation. Same architecture, fewer moving parts.

The result: the simplified version cost roughly half what the earlier one did, and produced better work.

Their own read on it, which is worth holding onto: the earlier harness was not wrong. It was right for the model it was built for. The frontier moved, so they ran a simpler version to see what still needed to be there.

That means your scaffolding has a shelf life. Every workaround you build for a model's current weak spot is a candidate for deletion the next time the models improve. The planner, builder and critic core survived every round of their simplification. Most of the rest did not.

A habit worth having: when a new model lands, take one piece of scaffolding out and run the loop again. If nothing gets worse, it stays out.

###  The five things to remember

From the closing slide of Anthropic's own workshop:

Self-evaluation is a trap. Use an adversarial evaluator.

Structured hand-offs and clean contexts are the patterns that hold up.

Subjective quality is gradable, if you have a strong opinion and write it down.

Sit with the model and read the traces. Only then do you know what to keep and what to cut.

You do not need anyone's internal harness. The primitives are already shipped: subagents, browser control through MCP, skills for packaging your rubrics, and a permission mode that is not the dangerous one.

###  What you should have now

A state layer on disk that a cold run can pick up:

feature\_list.json

,

claude-progress.txt

,

init.sh

, and a git history

An auditor subagent with its own context, no write access, and no polite options

A contract both agents agreed to before work started, with criteria specific enough to point at one line

A loop with a real verification command and a real turn cap

A number for what it costs, and a clear sense of when not to reach for it

The prompt was never the hard part. The hard part is deciding what "done" means and building something that will tell you the truth about whether you got there.

Built on Anthropic's published engineering work. Every command and figure in this guide was checked against a first-party page. The workshop and course links on the main page are there if you want to go deeper.