---
name: build-client-acquisition-function
description: Use when someone wants to systematise client acquisition — prospecting, outbound, lead qualification, proposal generation, follow-up, sales agents, an always-on acquisition workflow — or to turn acquisition prompts and playbooks into a compound skill. Triggers on "build a client acquisition function", "automate my outbound", "systematise prospecting", "sales agent team", "acquisition operating system". Diagnoses the current maturity level against a ten-level ladder, builds only the next reliable layer, creates explicit artifacts and handoffs, and preserves human approval for sending, pricing, contracts, and exceptions.
---

# Build Client Acquisition Function

Build a dependable acquisition system, not a theatrical “autonomous” demo. Start from the user's actual manual process and advance only when the current level passes its gate.

## Start every run

1. Recall prior account, offer, ICP, and workflow knowledge from GBrain when available. Record whether recall succeeded.
2. Inspect existing local artifacts before researching or inventing replacements.
3. Create a run workspace with `python3 scripts/init_run.py --name <slug> --root <run-root>`.
4. Inventory the current manual workflow: trigger, inputs, decisions, outputs, owner, time, failure modes, and approval points.
5. Read [level-gates.md](references/level-gates.md) and determine the highest level supported by evidence. Do not accept self-description alone.
6. Read [level-playbooks.md](references/level-playbooks.md) before building. It carries the concrete templates — the four-part prompt, the six numbered context files and project instructions, the six-block agent brief, the schedule-safe rules, and the lead state machine. Use them verbatim; do not paraphrase them looser.
6. Build the smallest missing artifact needed to pass the next gate.

If the user supplies prompts, documents, calls, or a playbook, preserve them under `sources/` and create a traceable `evidence-map.md` connecting claims and rules to their sources.

## Four founding rules

1. **Do not skip levels.** Level 7 built on a broken Level 3 is a faster mess.
   **Enforced, not just stated:** run `scripts/check_levels.py <run>` before reporting any
   level. It exits 1 when `status.json` claims a level above the highest *contiguous* built
   one, and treats an untouched scaffold template as not built. This rule was violated in
   prose form before the check existed — a run scaffolded `prompts/` and `chains/` as empty
   directories, built Level 3, and reported Level 3 with Levels 1 and 2 missing entirely.
2. **Automate only what has been done by hand ten times.** Otherwise you scale a bad process.
3. **Every level must kill a task on someone's calendar.** If it removes no work, it is a toy — delete it.
4. **Write the rule down once.** Every level up moves knowledge out of a head and into a file Claude can read. That is the whole game.

## Operating rules

- Do not skip levels. A later-level artifact may be prototyped, but label it blocked until every prerequisite gate passes.
- **Prove absence before writing BLOCKED.** A blocker is a claim about the corpus, and it
  must be evidenced like any other. Before recording any input as blocked on a human, grep
  every supplied source for the term and its synonyms, and record the search you ran. In one
  run three separate blockers — a product's description, the voice samples, a full product
  specification — were all sitting in documents already read. Each cost a full rebuild cycle.
  `scripts/check_blockers.py` enforces this mechanically.
- **Do not over-correct a claim.** When a claim is wrong, establish *which part* is wrong
  before retiring it. A defence figure was withdrawn entirely when only its framing was
  wrong — contracted rather than revenue, and in a sister entity — and retiring the magnitude
  threw away the strongest verifiable asset in the proof file. State the narrowest true
  version instead of deleting the claim.
- **Audit your own arithmetic.** Anything you write into the context files gets the same
  scrutiny as the source documents. Self-authored defects in one run included a percentage
  that was simply wrong and a lead-scoring model that summed to 12 on a stated scale of 10.
  Re-derive every number you introduce.
- Automate a judgment only after the user has performed and reviewed it manually at least 10 times, unless the action is reversible and purely internal.
- Research and draft automatically. Require human approval before external sending, pricing commitments, contracts, purchases, public output, destructive changes, or exceptions.
- Begin integrations read-only. Add one bounded draft-only write after a stable observation period.
- Store credentials only in host secret stores or environment configuration; never in the run or skill.
- Treat “good” as measurable. Record acceptance tests, baselines, failures, and reviewer decisions.
- Never claim a scheduled or connected system is live without an observed successful run and backend evidence.
- Stop on missing evidence, ambiguous identity, conflicting instructions, policy risk, low-confidence personalization, or abnormal volume.

## Advancement workflow

Use [artifact-contracts.md](references/artifact-contracts.md) for required filenames and schemas.

1. **Assess:** Write `control/maturity-assessment.md` with evidence for levels 1–10, current level, next level, gaps, and recommendation.
2. **Design:** Write `control/advancement-plan.md` for one level only. Define the calendar task it removes, acceptance test, rollback, owner, and approval gate.
3. **Build:** Create the level's artifacts. Reuse specialist skills instead of embedding their entire methods here.
4. **Dry-run:** Test on historical or synthetic inputs. Keep all external actions disabled.
5. **Review:** Route client-facing language and documents through an appropriate review stage; use `/ce-doc-review` for material briefs, proposals, and deck packets.
6. **Pilot:** Run with human approval and log inputs, decisions, drafts, edits, failures, and outcomes.
7. **Gate:** Mark the level `passed`, `failed`, or `blocked` in `control/status.json`. Advance only on documented evidence.
8. **Compound:** Capture what worked, failed, and changed. Route durable lessons through `/ce-compound`, local knowledge, and GBrain write-back when available.

## Specialist routing

- Use research tools for current prospect, company, market, and competitor evidence. Prefer primary sources; record retrieval time and URL.
- Use existing account-briefing, audience-research, competitive-intelligence, or prospecting skills when they match the requested stage.
- Use `/ce-brainstorm` to turn a proven manual step into requirements, `/ce-plan` for implementation, `/ce-work` for code, and `/ce-code-review` for production automation.
- Use the repo's presentation pipeline for client-facing decks; do not generate an ad hoc blank PPTX.
- Use browser validation for connected workflows when UI behavior matters.

## Four-role team

At Level 8, keep responsibilities separate:

- **Scout:** discovers and verifies candidates; emits scored research, never outreach.
- **Writer:** drafts evidence-backed personalization; never sends.
- **Closer:** prepares next-step options, proposals, and follow-up drafts; never changes commercial terms without approval.
- **Auditor:** checks evidence, policy, duplication, tone, and approval status; can reject any artifact.

Agents communicate only through files defined in [artifact-contracts.md](references/artifact-contracts.md). Do not rely on hidden conversational state.

## Completion contract

Return:

- current and target maturity levels;
- the calendar task removed;
- artifacts created or changed;
- gate evidence and test results;
- human approvals still required;
- failures, risks, and rollback;
- the next recommended level, without silently building it;
- GBrain recall and write-back status.

Never call the system an “acquisition function” until Level 10 passes its gate. Use `draft`, `pilot`, `reviewed`, or `blocked` status precisely.

## Skill Relationships

### Category
Business Automation

### Dependencies
- `references/level-gates.md` — the ten gates and their pass evidence
- `references/level-playbooks.md` — the concrete templates; read before building anything
- `references/artifact-contracts.md` — run structure, status schema, handoff envelope, state machine
- `scripts/init_run.py` — creates the run workspace with numbered context files
- `assets/context-template.md` — starting shape for each context file

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `ce-brainstorm` | Sequential upstream | turning a proven manual step into requirements | requirements notes |
| `ce-plan` / `ce-work` | Sequential downstream | when a level needs real code or automation | implementation plan |
| `ce-doc-review` | Sequential downstream | before any client-facing brief or proposal ships | `deliverables/*.md` |
| `00-account-briefing` | Alternative / Peer | a single named account, not a repeatable function | briefing markdown |
| `presales-deal-prep` | Alternative / Peer | one deal in flight rather than the acquisition system | deal prep pack |
| `branded-pptx-deck` | Sequential downstream | only when a level's deliverable is genuinely a deck | `deliverables/slide-plan.json` |

### Runtime Preamble

At invocation, say:
- "Running /build-client-acquisition-function — diagnosing your current level before building anything."
- After assessment: the evidenced current level, the next gate, and the calendar task the next level removes.
- If the user asks for a level more than one above the evidenced one: say plainly that it will be built on an unproven layer, and offer the prerequisite instead.
- If no manual baseline exists for a judgement being automated: say so and propose the manual reps first.

---

## Gotchas

- **A deck is not a level.** If the output does not remove work from someone's calendar, it is a toy — the framework says delete it. Producing a strategy document instead of a working artifact is the most common way this skill gets misused.
- **Level 3 is where quality actually comes from.** Thin context files produce generic output at every level above, and the usual instinct is to fix the prompt instead of the files. Fix the files.
- **`04-proof.md` is a ceiling, not a starting point.** No level may assert a claim that is not evidenced there. This is what stops a fabricated case study reaching a prospect.
- **Disqualifiers matter more than qualifiers in `02-icp.md`.** Most ICP files list who to target and omit who wastes your time, which is the half that saves weeks.
- **The Auditor is the role everyone skips.** It creates nothing and is the only thing standing between the system and a confident fabrication going out.
- **Files are the handoff, not chat.** Agent-to-agent state passed conversationally cannot be audited, replayed, or resumed after a failure.
- **A scheduled task cannot ask a question.** Anything ambiguous, it guesses. Prompts that work in conversation routinely fail on a schedule for exactly this reason.
- **Two agents disagreeing about a lead's state means the store is broken** — fix the source of truth, never patch the agents around it.
- **Change one rule per week at Level 10.** Change five and you will never learn which one worked.
- **Never call it an acquisition function until Level 10 passes.** Use `draft`, `pilot`, `reviewed`, or `blocked` precisely.
