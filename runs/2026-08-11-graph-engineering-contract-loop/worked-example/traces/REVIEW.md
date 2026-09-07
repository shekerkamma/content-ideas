# Trace review packet

Generated: 2026-08-11 02:21
Traces: `/home/sheke/content-ideas/runs/2026-08-11-graph-engineering-contract-loop/worked-example/traces`

## The prompt to run in a fresh session

```text
Read every trace file listed below, in full. Do not summarize them to me.

For each point where the auditor passed something it should have failed:
1. Quote the exact moment from the trace, with the file name.
2. Say what a careful human reviewer would have caught there.
3. Propose a specific edit to `.claude/agents/auditor.md` that would have
   caught it.

Do not rewrite the whole prompt. Give me targeted changes, each tied to the
trace line that justifies it.

If you find no such moment, say so plainly rather than inventing one.
```

## Trace files

| File | Size | Lines | Signals to check first |
|---|---|---|---|
| `auditor-criterion-7.md` | 2.8 KB | 56 | — |

**1 trace(s), 2.8 KB total. 0 carry at least one signal.**

The signal column is a hint about which file to open first. It is a regex over the text, not a verdict — a trace with no signals can still be where the loop went wrong, and a flagged line can be entirely fine in context.

Read the whole thing. Grepping traces with a second agent is a useful first pass for finding where a run veered off; it does not replace reading them line by line. Understanding why the model thought what it thought is the skill being built here.
