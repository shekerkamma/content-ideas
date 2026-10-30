---
name: pages-watch
description: 'Use when the user wants GitHub Pages deploys watched until they finish — "watch the deploys", "when the Pages runs finish", "confirm build, deploy and verify-live are green", "run live-scan on both sites", "are v11 and v12 green yet", or /pages-watch [sha]. Waits for the Pages workflow run on each repo (DeepGrid v11 and v12 by default), reports every job, then runs the live leak scan against the deployed sites. Read-only: never cancels, reruns or pushes.'
argument-hint: '[commit sha | run ids] [--no-scan]'
license: MIT
metadata:
  category: CI/CD & Deployment
  cost-tier: Haiku
---

# Pages Watch

One command for the request that recurred 34 times between 9 and 27 Oct 2026:
"when the Pages runs for X finish, confirm build, deploy and verify-live are green on v11
and v12, then run live-scan". The waiting is a script, so the model only reads one table.

## Workflow

Input: `$ARGUMENTS`. A hex string is a commit SHA. Numbers are run IDs in `--repos` order.
Blank means the latest push run on `main` of each repo.

1. **Start the wait in the background.** Runs take about 70 minutes; do not poll by hand.
   ```bash
   python3 "${SKILL_DIR}/scripts/watch_runs.py" [--sha <sha>] [--run <id> --run <id>]
   ```
   Run it with the host's background mode (`run_in_background` in Claude Code). Tell the user
   which run IDs are being watched and that you will report when both finish.
2. **Read the result** when the process exits. It prints one markdown row per job.
   Exit 0 all green · 1 a job failed · 2 timed out (default 95 min) · 3 no run found or `gh` error.
3. **On exit 0, run the live scan** unless the user passed `--no-scan`:
   ```bash
   node "${SKILL_DIR}/scripts/live-scan.mjs" "${SKILL_DIR}/references/scan-config.json" \
     https://shekerkamma.github.io/deepgrid-dr-silicon-v11/ https://shekerkamma.github.io/deepgrid-dr-silicon-v12/
   ```
   It fetches the configured page, crawls every same-origin JS chunk, and checks that each
   `must_be_zero` phrase appears 0 times and each `must_hit` control appears at least once.
4. **Report** in this order: one line verdict, the job table, the scan's `LEAK`/`MISS` lines
   (or "clean, controls present"), and the commit each site is now serving.

## Judgment rules

Editable policy. Change these lines, not the scripts.

- A job that is `skipped` counts as green. `cancelled`, `failure` or `timed_out` is red.
- If one repo's run is red, still report the other repo; never stop at the first failure.
- On a red job, quote the failing step from `gh run view <id> -R <repo> --log-failed | tail -40`
  and stop. Do not rerun, cancel or push — those are the user's call.
- Run the live scan only after both runs are green. A scan of a half-deployed pair proves nothing.
- If the two sites serve different commits, say so in the verdict line even when both are green.
- Edit `references/scan-config.json` (not the script) when a new internal phrase must never ship.
- Timeout: say which run was still running and its URL; offer to watch again, never assume it passed.

## Gotchas

- WSL `gh` is logged in as the collaborator account `sheker-deepgrid`. Reading runs works; cancelling
  needs the owner account through Windows `gh`. This skill only reads.
- Without `--sha`, the "latest push run on main" can belong to an older commit on one repo when
  only the other repo was pushed. Pass `--sha` whenever the user names a commit.
- The Pages concurrency group does not cancel in progress, so a hung run blocks the queue behind it.
  A run stuck "queued" for over 20 minutes usually means that; report it rather than waiting out 95 min.
- `live-scan.mjs` needs Node 18+ for global `fetch`. GitHub Pages caches for up to 10 minutes;
  a `LEAK` right after deploy can be the old build — check the `last-modified` line before reporting.
- The proof-of-done mod runs tests in the shell's current folder, so keep the shell in the repo root.

## Skill Relationships

### Category
CI/CD & Deployment

### Dependencies
- `gh` CLI, authenticated with read access to the repos. Node 18+ for the scan.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `land-and-deploy` | Alternative / Peer | generic single-repo merge, deploy and canary flow | — |
| `canary` | Sequential downstream | deeper post-deploy browser checks are wanted | site URLs |
| `e2e-qa-review` | Sequential downstream | a full page-by-page QA sweep after the deploy is green | site URLs |

### Runtime Preamble
"Using pages-watch. I'll wait for the Pages runs in the background, report every job, then run the live leak scan on both sites. For a single-repo merge-and-deploy flow, /land-and-deploy fits better."

## Host Compatibility

### Target Hosts
- Claude Code: yes — `~/.claude/skills/pages-watch` symlinks to `skills/pages-watch/`.
- Codex/OpenAI: yes — `.agents/skills/pages-watch/` (byte-identical copy) and `skills/` via the Codex plugin.
- OpenHands / DSH: yes — same `.agents/skills/` copy; needs `gh` and `node` on PATH.

### Canonical Source
`skills/pages-watch/`.

### Tool Mapping
- `run_in_background` → on hosts without background shells, run with `--timeout` in a shell job
  and check back, or run in the foreground with a host timeout above the `--timeout` minutes.

### Source / Tool Order
1. The `gh` run and job data. 2. The live sites. No web search.

### Environment
- `PAGES_WATCH_REPOS` — comma-separated `owner/name` list; defaults to DeepGrid v11 and v12.
