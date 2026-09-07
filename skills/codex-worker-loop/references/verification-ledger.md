# Verification Ledger

Verification is owned by the orchestrator and must test the real deliverable. A worker's confidence, a successful process exit, or "the tests it wrote pass" is not evidence that its content is correct — Sol writes its own test suite in the reference build, which is exactly why the orchestrator's independent check matters.

## Per-worker record

```markdown
### W<ID> — <goal>

- Wave: <n>
- Dispatch: codex exec, model <model>, effort <effort>
- Attempts: <used/cap>
- Paths touched: <git diff --stat scope>
- Output: <path to captured stdout>

| Criterion | Check performed | Exit/result | Evidence | Verdict |
|---|---|---|---|---|
| W1-C1 | `<actual command>` | 0 | `<concise real output>` | PASS |
| W1-C2 | Manual comparison against reference | mismatch | Expected X; observed Y | FIX |

Final verdict: <PASS | FIX | ESCALATE>
Named failure or escalation reason: <text or NONE>
```

## Evidence rules

Good evidence:

- The actual test, build, lint, typecheck, or deploy command and its exit status
- A `git diff` against the worker's declared scope, read in full
- Clicking through the live feature (or a browser-automation trace) and stating what was observed
- A schema/parser result against the generated artifact
- A security-focused pass: does this diff introduce a place where one tenant's data could reach another's request?

Insufficient evidence:

- The worker says it verified this
- The worker's own test suite passing (it wrote that suite — treat it as a hint, not proof)
- The output looks plausible
- The file exists
- A different worker's tests pass
- A command prints `true` without exercising the target

## Verdict rules

- `PASS`: every criterion has current evidence.
- `FIX`: one recoverable attempt remains; quote the failed criterion and the observed evidence in a fresh brief (`references/worker-brief.md` → Redispatch addendum).
- `ESCALATE`: second failure, missing required input, unsafe access requested, a security-relevant defect, or exhausted budget.

After merging accepted worker diffs, create an `INTEGRATION` record and rerun the *original* end-to-end success criteria — parts that pass individually can still fail once combined (a shared type contract two workers each interpreted slightly differently, a route one worker assumed the other would wire up). Local `PASS` rows do not imply an integration `PASS`.
