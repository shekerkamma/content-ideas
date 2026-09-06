---
name: graph-engineering
description: Use when a repeated job needs an agent that cannot mark its own work done — "build a self-improving loop", "graph engineering", "contract loop", "builder and critic agents", "adversarial evaluator", "my agent says it's done and it isn't", "agent that runs for hours", "generator evaluator pattern", "long-running agent harness". Scaffolds a planner/builder/critic harness with state on disk, a frozen contract both agents negotiated, and a real verification command. Not for one-off tasks, deterministic work a script already covers, or multi-model councils (use meta-loop).
license: MIT
metadata:
  category: Agent Engineering
  version: '1.0'
  compatibility: Python 3 stdlib only. Requires git. Claude Code subagents or any host that reads agent Markdown files.
---

# Graph Engineering

Build a loop where one agent does the work, a second agent grades it against
criteria they agreed on before starting, and neither one gets to call the job
done alone.

The unit of work is no longer the prompt. It is the loop: nodes that do work,
edges that pass results, and state in the middle that survives the session.

**Cost tier:** the loop itself runs on the cheapest model that passes its own
contract — plan on Opus for the planner, Sonnet for the builder and critic.
Scaffolding and validation in this skill are plain Python and cost nothing.

## Resolve the skill directory

Every command below runs a bundled script. Set `SKILL_DIR` to the absolute path
of the directory containing this `SKILL.md`. Guard once:

```bash
SKILL_DIR="<absolute path of the directory containing this SKILL.md>"
test -f "$SKILL_DIR/scripts/init_loop.py" || { echo "ERROR: bad SKILL_DIR=$SKILL_DIR" >&2; exit 1; }
```

---

## Stage 0 — The fit gate (run this before building anything)

This pattern costs roughly **15× a normal chat turn**. Anthropic's own demo run
was ~6 hours and ~$200. Do not skip this gate to be polite.

Answer all four. Any "no" means stop and say so:

1. **Is being wrong more expensive than the tokens?** A bad lead score sends a
   person chasing nothing for a week — that qualifies. Reformatting a
   spreadsheet does not.
2. **Can you write down what "good" looks like?** No criteria, no critic. The
   critic will default to agreeable and you will have built an expensive way to
   get a rubber stamp. If you cannot write the criteria, writing them *was* the
   job — do that instead.
3. **Would a script do?** If the check is deterministic, write the script. Use
   reasoning for judgment, not for things `sort` and `grep` decide.
4. **Are the steps genuinely separable?** If every step needs to know what every
   other step is doing, splitting across agents with separate contexts buys
   coordination cost and nothing else.

Report the gate result explicitly before proceeding. "Blocked at Stage 0,
criterion 2" is a real and useful answer.

---

## Stage 1 — Scaffold the state layer

State lives on the file system, not in the session. Not a database, not a
vector store. Files in a git repo, because the next run starts cold.

```bash
python3 "$SKILL_DIR/scripts/init_loop.py" --project "<name>" --dir <path>
```

This writes four artifacts and initializes git:

| Artifact | What it holds |
|---|---|
| `feature_list.json` | Every unit of work, each `passing` or `failing` |
| `claude-progress.txt` | Timestamped narrative: tried, found, fixed, next |
| `init.sh` | One command to boot the environment |
| `contract.md` | Status `DRAFT` until Stage 3 freezes it |

Plus `.claude/agents/auditor.md` (Stage 2) and a git repo with an initial commit.

**Status is JSON, narrative is text, and that is not a style preference.** Models
rewrite Markdown and update JSON. Keep a task list in `tasks.md` and you will
come back to find it "cleaned up" with completed items quietly dropped.

Two fields carry the weight in `feature_list.json`:

- `status` is only ever `failing` or `passing`. No "in progress", no "mostly
  done" — a binary state is the only kind an agent cannot talk its way around.
- `verified_by` is the command or check that decides. **If you cannot fill this
  field, the item is written badly.** Rewrite it until you can.

Items must be granular enough to watch succeed or fail. Anthropic's own example
of the right size: *"a user can open a new chat, type in a query, press enter,
and see an AI response."* That is one item. Not "build chat."

Validate any time:

```bash
python3 "$SKILL_DIR/scripts/verify_state.py" --dir <path>
```

---

## Stage 2 — Install the critic, and keep it blind

`init_loop.py` writes `.claude/agents/auditor.md`. Read it before first use and
tune the rubric to your work — the template is a starting point, not a finished
opinion.

Three constraints are load-bearing. Weaken any one and the loop degrades to a
single agent with extra steps:

**1. The critic did not do the work and gets no access to how it was done.**
This is the constraint most people get wrong, and Anthropic tried it the other
way first. Do not feed the builder's transcript, reasoning, or intermediate
steps to the critic. It muddies the two model streams and makes it easy for the
model to talk itself into believing something works. The critic judges the
output and says "this is an issue" — the builder reflects on its own work and
figures out the fix.

**2. The critic cannot write.** Tools are `Read, Grep, Glob, Bash` and nothing
else. A critic with edit access quietly fixes what it was supposed to report,
and you lose the signal. Constraining tools is half the reason to use a subagent.

**3. The critic uses the thing, it does not read about it.** This is the single
biggest upgrade available, and it is not a prompt change. Give it hands:

```bash
claude mcp add playwright -- npx -y @playwright/mcp@latest
```

The bugs this catches are the ones no diff review finds — a route-ordering bug
that passes every unit test and breaks in production, a boolean logic bug on a
delete action. Both are obvious within ten seconds of actually using the thing.
For non-browser work the principle is identical: the check must *run* the
output. That is what `verified_by` is for.

**Expect it to be too nice at first.** Out of the box Claude is a bad QA agent —
it will find a real bug and respond "fix later, might take two weeks." That is
normal, it is not your prompt being too soft, and the fix is Stage 5. Two things
help immediately: remove every escape hatch ("fix later" and partial passes are
banned in the template), and make failure the default — score 0.0 when a
criterion cannot be verified, so the work has to prove it passed.

Rubrics worth stealing are in `references/rubrics.md`.

---

## Stage 3 — Negotiate the contract, then freeze it

This is the stage almost nobody builds, and it is the one that turns two agents
into a system.

The critic must not grade against the original request. It grades against
criteria both agents argued over and signed before anyone had a reason to be
defensive.

Kick it off:

```text
Before writing any code, negotiate a contract with the auditor subagent.

1. Draft contract.md: the scope, and the specific criteria you should be held
   to. Every criterion must be checkable, ideally by a script.
2. Ask the auditor to review it adversarially. It should push back on scope
   that is too broad, criteria that are too weak, and anything missing.
3. Revise. Repeat until the auditor agrees with no outstanding objections.
4. Set Status: AGREED, then start work.

Do not begin the actual work until the contract says AGREED.
```

Then gate on it:

```bash
python3 "$SKILL_DIR/scripts/check_contract.py" --dir <path>
```

The script fails the contract when criteria are unmeasurable, when the `Check`
column is empty, when `Status` is not `AGREED`, or when it finds hedge words
that cannot fail. It is a mechanical pre-pass, not a substitute for reading the
contract yourself.

**Granularity is the whole game.** Anthropic's generator and evaluator settled on
**27 criteria** for one app. Vague criteria produce vague critiques; the builder
shrugs and does whatever. Granular criteria mean the agent knows: fix this exact
line.

The test: read a criterion and ask whether two reasonable people could disagree
about whether it passed. If they could, it is not written yet.

| Not written yet | Written |
|---|---|
| The lead scoring should be accurate | Every row in `leads-scored.csv` has a score of exactly 1, 2, 3, 4 or 5 |
| Output should be well organized | The row count in `leads-scored.csv` equals the row count in `leads-raw.csv` |
| Handle edge cases appropriately | Rows with `company_size` under 10 are never scored above 3 |

Keep the **Disputes** section. Six weeks on, when someone asks why scoring is
1–5, the answer is there along with the fact that somebody argued for 1–10 and
lost on the merits.

**Keep the planner out of the loop.** If a planner produced the original spec,
it sets the outer lines of the product and then stays out. Its job is not to
intervene mid-run and re-litigate whether a feature is possible. Re-inject the
spec as a reference point; do not give the planner a vote in the contract.

---

## Stage 4 — Run the loop

Three rungs. Each is useful on its own. Do not skip to rung three.

**Rung 1 — one agent, one goal, one real check.** No subagents yet. What makes
it a loop rather than a prompt is the stop condition and the verification
command. Write the deterministic check first, in plain Python with no model in
it, then:

```text
/goal <the work>. Run `python3 scripts/check_scores.py` after each pass and
keep fixing until it prints PASS. Stop after 5 attempts.
```

Three things make this work: a verifiable exit a script decides, a real turn cap
so a loop that cannot succeed stops spending, and a check the model cannot argue
with. Exit code 1 is exit code 1.

Run rung 1 on real data before going further. You will learn more from watching
it fail the check three times than from reading the rest of this page.

**Rung 2 — add the critic and the contract.** Rung 1 catches everything a script
can catch. It cannot catch a score of 5 justified by a reason that sounds great
and is supported by nothing in the row.

```text
/goal Work through contract.md one criterion at a time.

For each: do the work, run its check, then hand off to the auditor subagent to
grade it against contract.md. Only mark an item passing when the auditor grades
it pass. If the auditor fails an item, fix exactly what it named and resubmit.

Update feature_list.json and claude-progress.txt after each item, and commit.
Stop when every criterion passes or after 15 attempts.
```

**One item per run.** Not "as many as you can." The moment a run tries four
things, a failure in the third poisons the record of the first two and you
cannot tell from outside what state you are in.

**Rung 3 — take yourself out of it.** Only once the loop has run clean twice
unattended.

| Command | Runs | Stops when |
|---|---|---|
| `/goal` | Now, in your session | Goal met or turn cap hit |
| `/loop` | On an interval, locally | You cancel or close the session |
| `/schedule` | On Anthropic's cloud | You disable it |

Match the interval to how often the data actually changes. A loop every five
minutes against data that arrives twice a day is idle 95% of the time and bills
you for all of it. Check `/usage` after the first scheduled week, before scaling
anything.

Most operators should live on rung 2 for a while. A loop you trust doing one job
beats an ambitious one you check every morning — which is the original problem
with extra steps.

For human-in-the-loop, use hooks as the stop condition rather than weakening the
critic. But prefer baking the fix into the harness: an inserted human is usually
covering for a harness problem you have not diagnosed yet.

---

## Stage 5 — Tune from traces, not from experiments

When the loop starts passing work that is obviously wrong, the instinct is to
re-run with a tweaked prompt. That instinct wastes days.

The primary debugging loop is **reading the traces**. Not running more
experiments. Read what the agent actually did, find where its judgment diverged
from yours, and tune the prompt for that specific divergence. It is the same
muscle as reading a stack trace: you are not guessing, you are looking at the
moment it went wrong.

Capture runs, then collate them:

```bash
mkdir -p traces
claude -p "$(cat prompts/scoring-run.txt)" > "traces/run-$(date +%F-%H%M).txt" 2>&1

python3 "$SKILL_DIR/scripts/collate_traces.py" --dir <path>
```

`collate_traces.py` writes `traces/REVIEW.md` — an index of captured runs with
the divergence-hunting prompt pre-filled. Open a fresh session and run that
prompt against it.

Read the traces yourself too. Grepping them with a second agent is a useful
first pass for finding where a run veered off; it is not a replacement. The
skill you are building is empathizing with the model — understanding why it
thought what it thought — and that only comes from reading line by line.

---

## Stage 6 — Delete scaffolding on every model release

Your scaffolding has a shelf life. Every workaround you build for a model's
current weak spot is a candidate for deletion the next time the models improve.

Anthropic deleted parts of their own harness: fresh sessions per feature
(dropped — the model no longer needed the reset), sprint decomposition (dropped),
evaluator cadence (moved from every sprint to end of generation). The simplified
version cost **roughly half** and produced better work. The earlier harness was
not wrong; it was right for the model it was built for.

The planner/builder/critic core survived every round of simplification. Most of
the rest did not.

**The habit:** when a new model lands, take one piece of scaffolding out and run
the loop again. If nothing gets worse, it stays out. Log the result in
`claude-progress.txt` so the next person knows what was tried.

---

## Verification discipline

Four failure modes that survive a green check. All four were found by the
critic, in a real run of this skill against a 315-skill repo, after the builder
had already reported the work done.

**1. A check can go green because what it measures moved.** A name-collision
check hashed the `name:` field. Three collisions were "fixed" by renaming, and
it passed — while all three pairs kept byte-identical `description:` and
`triggers:`, which is what routing actually selects on. Fixing that surfaced the
same defect one layer down, in `## When to invoke`.

> When a criterion goes from red to green, ask what moved. If the fix changed
> the field the check reads rather than the behavior the check protects, the
> check now certifies the defect.

**2. A check can stop measuring instead of being satisfied.** A description
rule returned early on folded YAML blocks. Rewriting 36 descriptions into folded
form would have made it pass without inspecting anything. A trigger parser
required list items indented deeper than their key; the repo's YAML puts them at
the same indent, so it returned `[]` for every affected skill and the whole half
of the rule was inert.

> A rule reporting zero failures is indistinguishable from a broken one until
> you mutation-test it. Break the thing on purpose and confirm the check fails.
> Do this when you write the rule, not when someone doubts it.

**3. Confirm which of two same-named sources is current before trusting either.**
Two checkouts of the same tool existed. The one that looked canonical — a git
repo with a remote — was three months stale; the current version lived inside a
host install directory. Thirty-nine files were "restored" from the wrong one.

> Rank sources by version and commit date, not by which looks more official.
> A git remote is not a freshness signal.

**4. Diff both directions before any sync.** Twice in one run, content was
destroyed by copying a "newer" file over an "older" one. Both times the
diagnosis came from looking only at what the source had *extra*, never at what
the destination had extra. Both were bidirectional divergence — a per-tree
convention in one, and a whole relationships table in the other.

> "Newer" is a claim about both files. If you have only diffed one direction,
> you have not established it. Prefer a merge you can justify line by line, and
> when you cannot, register the divergence instead of resolving it.

**And a rule about exceptions.** Any registry, waiver, or allowlist that excuses
a criterion is itself a claim, and needs the same evidence bar as the work.
Enforce the evidence mechanically: a check that verifies an exception was
*registered* but not that it was *justified* is a blanket waiver wearing a
schema. In the run above, one exception entry cited three facts; two were false
and one was fabricated outright.

---

## Judgment rules

Editable policy for how this skill weighs evidence when recommending a pattern,
model, or tool. Tune these here — do not hardcode them into step instructions.

- **Popularity is not fit.** Never rank a harness pattern, framework, or agent
  library by GitHub stars, download counts, or how often it trends. Stars are a
  bookmark count that only increases: they record that people liked something
  once, not that it fits this loop. Rank on fit to the stated constraints, then
  on maintenance signals carrying an exact date.
- **Split every reference harness in two: what transfers, and what exists only
  because that team is that team.** Anthropic's harness reflects their model
  access, their post-training feedback loop, and engineers who read traces full
  time. The planner/builder/critic core transfers. Their sprint machinery,
  cost tolerance, and 200-feature initializers mostly do not. Say which half a
  recommendation rests on.
- **Cost the loop at three points, not one:** a single manual run today, the
  first week on a schedule, and 10× that volume. A multi-agent loop is ~15× a
  chat turn and a single agent with tools is ~4×; a cadence that looks free in
  a one-off run is a monthly bill by week three. Name the crossing point.
- **A model release is a reason to re-open the design, not to defend it.**
  Prefer the simpler harness whenever the simpler harness still passes the
  contract. Scaffolding earns its place per model generation, not once.

---

## Gotchas

- **A contract that is not `AGREED` is not a contract.** Work started against a
  `DRAFT` contract produces critiques the builder can litigate. Gate on
  `check_contract.py` before Stage 4.
- **Never give the critic write access.** It will fix what it should have
  reported, and the loop goes quiet instead of failing loudly.
- **Never pipe the builder's transcript into the critic.** Anthropic tried this;
  it muddies the streams and makes self-deception easier. Output only.
- **Never let `status` grow a third value.** The first time "in progress" appears
  in `feature_list.json`, the loop has stopped being auditable.
- **Don't run the loop on work with no criteria.** Go write the criteria. That
  was probably the whole job.
- **Don't reach for this on brownfield without tuning.** The pattern is
  opinionated and suits greenfield best. On an existing codebase, point the
  critic at the current state, give it the spec, and expect to build your own
  rubric before the loop is worth running unattended.
- **`/schedule` before two clean unattended runs is how people find out their
  loop was lying at 7am every weekday.**
- **Bound every bulk edit to the narrowest pattern that does the job.** A sed
  broad enough to fix 11 documentation lines also rewrote 50 third-party package
  coordinates and turned 13 working URLs into 404s. Diff the changed-line count
  per file before trusting a sweep; one intended change per file should show as
  exactly one.
- **A criterion nobody can satisfy is a broken criterion, not a hard one.** One
  criterion here turned out to contradict another — satisfying it would have
  broken the mirror rule — so no legal action could ever pass it. Retire it and
  say why in the record. That is different from waiving it, which is what you do
  when the criterion is right and the work is not.
- **`verified_by` must run in the environment that ships.** A bytecode check
  walked the filesystem and reported 46 failures, every one a gitignored local
  artifact. Ask the thing that defines what ships — here, `git ls-files` — not
  the working directory.

## Related skills

- `meta-loop` — multi-model council with Opus aggregating isolated Codex
  workers. Use for independent parallel analysis, not for a builder/critic loop
  with disk state.
- `goal-loop-orchestrator` — plans which skills to chain. Use it upstream when
  the goal needs routing before any loop exists.
- `karpathy-guidelines` — coding guardrails the builder role should follow.

## Sources

Every figure and command in this skill is checked against a first-party page.
See `references/sources.md` for the full list with what each one supports.
