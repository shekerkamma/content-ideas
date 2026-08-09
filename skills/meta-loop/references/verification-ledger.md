# Verification ledger

Record one row per criterion for every worker and for final integration.

```markdown
### W1 — <goal>
- Model: <actual Codex model>
- Attempts: <used/cap>
- Output: <path>

| Criterion | Check | Result | Evidence | Verdict |
|---|---|---|---|---|
| W1-C1 | `<real command or source comparison>` | 0 | `<concise output>` | PASS |

Final verdict: PASS | FIX | ESCALATE
Named failure: <criterion and observed defect, or NONE>
```

Good evidence exercises the actual deliverable: a real test/build/parser, a primary-source comparison, or an observable UI check. A worker statement, file existence, or unrelated green test is insufficient.

After Opus synthesis, add an `INTEGRATION` record and rerun the original success criteria. Report both Opus calls and whether each note was applied or rebutted.
