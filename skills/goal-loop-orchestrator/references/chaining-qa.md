## Step 3.5: Skill Chaining QA Gate

Before executing a chain, and after every loop pass, verify that the selected
skills are compounding toward the goal instead of running as isolated motions.

### Chain Contract

For every skill/action in the chain, define:

```markdown
## Chain Contract
| Step | Skill/action | Consumes | Produces | Next consumer | Value test |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |
```

Definitions:

- `Consumes`: the exact artifact, source pack, decision, file, URL list, prior
  run output, or user input the skill must use.
- `Produces`: the exact artifact, evidence, decision, file, or state change the
  skill must leave behind.
- `Next consumer`: the downstream skill/action that will use the output.
- `Value test`: the observable reason this step moves the goal closer to the
  acceptance criteria.

If a step has no concrete input, no concrete output, no downstream consumer,
and no value test, remove it from the chain or mark it as optional/advisory.

### Pass-Level Chaining Check

After each skill/action pass, answer these checks before continuing:

```markdown
## Skill Chaining QA
- Skill/action just run:
- Intended input consumed:
- Actual input consumed:
- Intended output produced:
- Actual output produced:
- Downstream consumer:
- Evidence the next step can use it:
- Material progress toward acceptance criteria:
- Duplication or overlap with prior pass:
- Missing dependency or skipped gate:
- Chain status: compound / isolated / duplicate / blocked / reroute
- Decision: continue / revise chain / stop / ask user
```

Use these statuses:

- `compound`: output was consumed or is ready for the named downstream consumer,
  and the goal measurably advanced.
- `isolated`: the skill completed but produced no useful handoff or no
  downstream step can consume it.
- `duplicate`: the skill repeated prior work without adding materially better
  evidence, decisions, implementation, or verification.
- `blocked`: the skill could not run or could not produce the required handoff.
- `reroute`: the selected skill was the wrong tool for the phase; revise the
  chain before continuing.

### Broken Chain Patterns

Stop and revise the chain when any of these appear:

- A skill produces output that no later skill reads.
- A downstream skill ignores the upstream artifact and starts from scratch.
- Two skills perform the same discovery, research, synthesis, or QA without a
  distinct role.
- A skill only restates the goal or produces advice when the chain needs an
  artifact, evidence pack, decision, implementation, or verification.
- A skill succeeds operationally but does not move any acceptance criterion.
- Evidence discovery is treated as validation without the required qualifying
  skill, such as Reddit discovery without `reddit-new-factcheck`.
- Deck, strategy, PRD, or implementation work begins before required upstream
  evidence or planning gates are satisfied.
- Generic WebSearch/search_web bypasses wired search dependencies when
  You.com, Exa, Firecrawl, or specialist tools are available.
- A loop continues after a pass produced no material change.

### Reroute Rules

If a pass is `isolated`, `duplicate`, or `reroute`:

1. Stop the current chain before starting another skill.
2. Identify the missing handoff or wrong assumption.
3. Rewrite the Chain Contract for the remaining steps.
4. Remove any skill that has no concrete value test.
5. Continue only if the revised chain has a named next consumer and verification
   path.

If a pass is `blocked`, try one local fallback that preserves the same handoff
contract. If the same blocker repeats, stop and report the blocker rather than
running unrelated skills.

