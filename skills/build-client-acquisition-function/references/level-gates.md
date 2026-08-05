# Maturity levels and gates

Advance one level at a time. Evidence must be stored in the run workspace.

| Level | Capability | Required proof to pass |
|---|---|---|
| 1 | Saved prompt | Four-part structure (ROLE/INPUT/OUTPUT/RULES). Paste raw input, send result with zero edits **8 times out of 10** against a manually-written gold standard. |
| 2 | Chain | Ordered prompt stages, named intermediate artifacts, at least one human checkpoint, restartable from the failed stage. |
| 3 | Brain | Six numbered files (`01-offer` … `06-process`) plus project instructions. A **cold chat in the project**, given no context, produces something sendable with light edits. `04-proof.md` is the ceiling on every claim. |
| 4 | Skill | Trigger, inputs, workflow, output contract, guardrails, and validation are packaged; implicit and explicit invocation both work. |
| 5 | Deliverable machine | `template.md` derived from a deal that actually closed. Notes in, sendable file out, **under 10 minutes including review**, tested against three past deals. |
| 6 | Connection | Read-only integration is observed for one week; one bounded draft-only write then succeeds with logs and rollback. |
| 7 | Agent | Six-block brief with all blocks present, especially STOP AND ASK ME IF. Send the brief, leave for an hour, return to work you would have accepted from a junior. Manual approval for the first three runs. Cannot externally send. |
| 8 | Team | Scout, Writer, Closer, and Auditor have non-overlapping ownership, fixed file handoffs, and an enforced auditor veto. |
| 9 | Always on | Promoted only from a job running clean at Level 7/8 for **two weeks**. Prompt passes all five schedule-safe rules, including an explicit definition of "no work today". **First five runs watched** and logged. No unapproved sends. |
| 10 | Function | One source of truth with the agreed state machine; **one intake path** for every source; agents own stages not tasks; human checkpoints written down in advance; weekly feedback loop changing **exactly one rule per week**. A 20% traffic pilot runs two weeks. |

## Failure policy

A failed gate remains useful evidence. Record the failing cases, the smallest corrective change, and the retest. Do not weaken a threshold after seeing results. A user may explicitly change a threshold, but record the change and rationale.
