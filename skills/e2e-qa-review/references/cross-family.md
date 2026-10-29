# Cross-family review (optional)

Reviewers from different model families find different things: one family reports more, with more noise;
another reports fewer, better vetted (Theo, 22:30-24:30). Use one as a second reviewer on large or risky
changes, and triage its findings like any other: supported, unresolved, contradicted.

Codex CLI on this machine (see the repo CLAUDE.md for why each flag is there):

```bash
codex exec -m gpt-5.6-sol -s read-only - < qa/REVIEW-BRIEF.md   # prompt on stdin, closes it
# resuming a thread: `resume` has no -s flag, so pass the sandbox explicitly or it inherits full access
codex exec resume <thread-id> -c sandbox_mode="read-only" - < qa/REVIEW-FOLLOWUP.md
```

- Pass the prompt on stdin (or `stdin=subprocess.DEVNULL` with argv); an inherited open stdin hangs the call
  with no output.
- Never resume without `-c sandbox_mode="read-only"`: the config default is full access.
- Test the exact model id once; a family name is not a routable id.
- The brief: the contract, the diff or route list, "list only problems you would block the merge for; for
  each, file and line, why it is wrong, how to show it fails; mark what you could not confirm".
- `claudex-loop:codex-review` wraps a persistent adversarial session if installed.
