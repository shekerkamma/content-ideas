---
name: be-ambitious
description: 'Use when the user asks to be more ambitious with a task or prompt — "be ambitious", "go beyond the task", "what would a top expert do here", "make this prompt deeper", "aim higher", "bring in the crew", or /be-ambitious <task>. Rewrites a task prompt along Altitude (outcome, not task), Depth (expert instruments, unreasonable goals, challenge assumptions, produce new knowledge) and Range (other fields via noun-to-verb), checks the agent has the resources to reach it, and names an outside judge so the agent never grades its own work.'
argument-hint: '<task prompt, or blank to use the current task>'
license: MIT
metadata:
  category: Runbook
  source: 'Felix Rieseberg, "How to be more ambitious: A tutorial for humans with models", 2026-10-13'
  cost-tier: Sonnet
---

# Be Ambitious

Turns "do exactly what I asked" into "work toward the result I want".
Based on Felix Rieseberg's article (see `references/felix-article.md`).
The model does what you ask; the ceiling is the ask.

Four types of ambition. Speed (same work, faster) is assumed and skipped.

| Type | Question it asks | Fits when | Fits badly when |
|---|---|---|---|
| Altitude | What is the goal beyond the goal? | You are after an outcome; people will hold meetings about it | Creative work; outcomes no agent can own yet ("go make money") |
| Depth | How would the best person in the field do this? | The task must be done really well | Throwaway work |
| Range | Which other fields would see what this one misses? | The work touches people, trust, money, law or attention | A narrow mechanical fix |

Pick the types that fit. All three is not the default.

## Workflow

Input: `$ARGUMENTS` (a task prompt). If blank, use the task in the current conversation.

1. **State the task back in one line**, then the goal beyond it (Altitude step 1)
   as a guess the user can correct. If you cannot guess the outcome, ask one
   question — what should be different after this is done? — and stop.

2. **Resources check — before raising the goal.** Ambition needs a computer,
   the ability to install software, and data. Name, concretely, what the agent
   would use to:
   - **See** the problem (crash reports, logs, analytics, the live page, a screenshot tool, an MCP connector)
   - **Understand** it (source, git history, schema, the version→commit map, docs)
   - **Try and check** a fix (a test machine, sandbox, dev server, holdout data)

   Mark each **have / missing**. A missing lane caps the ambition: say what it
   caps, and propose the setup step (Felix had to wire crash-report fetch,
   version→commit mapping and Windows/macOS/Linux machines before "keep the
   apps crash-free" could work). Do not write a prompt that needs a lane that
   does not exist.

3. **Altitude** (if it fits). Climb the ladder and offer the rungs:
   - Rung 1 — the result, not the task: "Tell me what changed, why, and what we should do about it."
   - Rung 2 — the decision: "Work out the three most urgent decisions, with the numbers and for/against arguments."
   - Rung 3 — replace the process and prove it: "Design a better way to get this outcome than <current artifact>, show from our own history that it would have caught things sooner, and run it beside the current one for <period>."
   Also look for the durable version: a standing goal ("keep X crash-free")
   that removes the human from the task-after-task loop.

4. **Depth** (if it fits). First run the deeper-version prompt on the task
   (verbatim in `references/felix-article.md`): what a top professional would
   do that was not asked; the rawest material they start from; their specific
   methods and tools; what other than you or me would show it is right.
   Then apply the techniques that fit:
   - **Expert instruments, not expert vocabulary.** Name the tools the best
     practitioners use (database + statistical model, not a markdown table;
     profiler, not guesses) and require them.
   - **Unreasonable goal, stated as reasonable.** 200 ms, not 5 s. Pair it with
     the measurement that decides it. If the agent says it is impossible,
     restate that it is solvable and to keep going — once, with the measure.
   - **Challenge what you know.** Take the belief the task rests on and make
     the agent try to reproduce it from raw data, adversarially: "We believe
     churn is an onboarding problem. Try to reproduce that from the raw data."
   - **Produce new knowledge.** Once deep in the data, ask for the blind spot:
     build a model or simulation that reproduces the past from raw logs, find a
     signal nobody knows about, and **show it predicts on data it has not
     seen** (a holdout split before looking, not after).
   - **Outside judge** — step 6.

5. **Range** (if it fits).
   - **Nouns to verbs.** Rewrite what the thing *is* as what it *does for
     people*. "A quarterly deck" → "getting busy people to believe a story
     about cause and effect and decide under uncertainty in 30 minutes." "A
     recruiting app" → "getting strangers and companies to trust each other".
   - **Assemble the crew** from the verbs: production fields (analyst,
     journalist, editor, designer) plus a red team (short seller, forensic
     accountant, attacker, regulator).
   - **Methods, not role-play.** Each member is defined by what that field
     *does* — "do what a short seller does to research a position", never
     "write like a short seller". Give each a concrete method and output.
   - Each member reports findings with evidence first; fixes are applied
     after, in one coordinated pass, so a later fix does not undo an earlier
     one. (Felix does not prescribe an order; this is a local rule.)

6. **Outside judge — required for every ambitious prompt.** The agent never
   grades its own work. Choose the strongest judge available, in this order:
   1. A check the agent can run that **could fail**: tests, a gate, a
      benchmark, a holdout set, the real page in a browser. Run it once
      against the old version first to prove it can go red.
   2. A different model: Codex via `claudex-loop:codex-review` (read-only
      sandbox), or another provider.
   3. A fresh Claude session on a different model version, non-interactive.
   4. The `verifier` subagent (`.claude/agents/verifier.md`) — fresh context,
      runs checks, never fixes.
   Write the judge and its pass condition into the prompt.

7. **Write the output** (format below) to
   `runs/<YYYY-MM-DD>-be-ambitious-<slug>/ambitious-prompt.md` and show it in
   chat. Recommend running the rewritten prompt in a **fresh session** (in
   Claude Code: `/copy`, then `/clear` or a new session) so it starts from the
   ambitious prompt, not the old conversation.

8. **Stop and ask before executing** anything long or costly: a Range crew,
   multi-hour runs, paid APIs, or more subagents than the user asked for. Give
   the estimated number of agents and runs.

## Output format

```markdown
# Ambitious prompt: <slug>

Original task: <one line>
Goal beyond the goal: <one line>
Types used: Altitude / Depth / Range (and why the others were skipped)

## Resources
| Lane | Have / missing | What | If missing, what it caps |
|---|---|---|---|
| See | | | |
| Understand | | | |
| Try & check | | | |

## Rewritten prompt
<the full prompt, ready to paste>

## Outside judge
Judge: <check / model / session> — pass when: <measurable condition>
Proved it can fail by: <how, or "not yet — do this first">

## Crew (Range only)
| Field | Verb it serves | Method | Output |
|---|---|---|---|

## Not done / limits
<missing lanes, rungs declined, anything the user must set up>
```

## Judgment rules

Editable policy. Change these lines, not the workflow.

- Resources before ambition: a missing see/understand/try lane is reported, not prompted around.
- Altitude stops at the highest rung an agent can actually own and verify today.
- Unreasonable goals always carry a number and the instrument that measures it.
- "Challenge what you know" targets the one belief the task most depends on, not every belief.
- New-knowledge claims need a holdout chosen before the analysis looks at it.
- Range crew size: 3–6 fields; at least one red-team field.
- Outside judge is mandatory; a check derived from the artifact it tests does not count.
- Never execute a crew or multi-hour run without the user's go-ahead.

## Gotchas

- **Vocabulary, not method:** "Act as a senior engineer" changes the words, not the work. Every expert reference must name a tool, method or raw input.
- **Role-play transcripts:** crew members that "write like" a field make the transcript stranger and the result no better. Define them by what they do.
- **Self-grading:** the same model reviewing its own output agrees with itself. A judge that cannot fail is not a judge — prove it red on the old version.
- **Altitude on creative work:** "make it great" has no outcome to climb toward. Use Depth or Range instead.
- **Goal without a measure:** "make it fast" invites tweaks; "200 ms p95 on the home route, measured by X" forces a rethink.
- **Prompting past a missing lane:** an ambitious prompt with no way to see or test the problem produces confident fiction.
- **Tuned on its own eval:** a "new signal" scored on the data it was found in proves nothing. Holdout first.
- **Codex review writes files:** `codex exec resume` has no `-s` flag; pass `-c sandbox_mode=read-only` or the judge edits the work it is judging.
- **Overspawn:** Range is where cost explodes. Ask before spawning; reuse one crew pass rather than many.
- **Scope vs karpathy-guidelines:** ambition raises the goal, not the edit footprint. Agree the bigger goal with the user, then implement it surgically.

## Skill Relationships

### Category
Runbook

### Dependencies
- None required. Uses an outside judge if one is installed (see table).

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `prompt-master` | Alternative / Peer | general prompt rewrite or audit without the ambition ladder | — |
| `grill-me` | Sequential upstream | goal is unclear after step 1 | brainstorm notes |
| `benai-interview-me` | Alternative / Peer | bounded requirement interview instead of grill-me | interview notes |
| `plaid` | Sequential downstream | the rewritten prompt is a roadmap or product build | `runs/<date>-be-ambitious-<slug>/ambitious-prompt.md` |
| `claudex-loop:codex-review` | Amplifier (outside judge) | Codex is available | review findings in chat |
| `verifier` | Prerequisite / Gate before "done" | always available fallback judge | VERDICT line |
| `karpathy-guidelines` | Behavioral overlay | implementation of the rewritten prompt | — |

### Runtime Preamble
"Using be-ambitious. I'll check what the agent can see, understand and test first, then raise the goal. If the goal itself is unclear, /grill-me first. For a plain prompt clean-up without raising the goal, /prompt-master fits better."

## Host Compatibility

### Target Hosts
- Claude Code: yes — `~/.claude/skills/be-ambitious` symlinks to `skills/be-ambitious/`.
- Codex/OpenAI: yes — `.agents/skills/be-ambitious/SKILL.md` (byte-identical copy) and `skills/` via the Codex plugin.
- OpenHands / DSH: yes — `.agents/skills/be-ambitious/SKILL.md`.

### Canonical Source
`skills/be-ambitious/`. `.agents/skills/be-ambitious/` is a byte-identical copy (`check_skills.py --rule crosstree`).

### Tool Mapping
- `AskUserQuestion` → a concise chat question.
- Subagents for a Range crew → Codex multi-agent tools if available, else run each field sequentially in the main thread.
- `/copy` + fresh session → copy the prompt from `ambitious-prompt.md` into a new session.
- `claudex-loop:codex-review` → on Codex, use a different provider or a fresh read-only session as the judge.

### Source / Tool Order
1. Read this file and `references/felix-article.md`.
2. Read the user's repo, data and prior run files — the rawest material is usually local.
3. GBrain recall for recurring entities or prior strategy work, when available.
4. External research only when the Depth step needs a field's current tools, via Exa before generic web search.
