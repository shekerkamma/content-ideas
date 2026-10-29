# Environment bindings

Every row below was true on the demonstrator's machine and had to be resolved
before this skill could run here. Resolutions are `confirm`, `substitute`,
`drop`, or `BLOCKED-ON-USER`. None was resolved by assuming.

| # | Binding | In the video | Resolution | Notes |
|---|---|---|---|---|
| 1 | Data provider | AnySite — one vendor behind MCP, CLI, and REST | **substitute** | Rebuilt as pluggable adapters (`file`, `http`, `exa`). AnySite is reachable through `http` like any REST provider; nothing in the skill names it. |
| 2 | Provider API key | AnySite key generated in their dashboard; trial credits and a "plan ends" banner visible on screen at 07:02 | **BLOCKED-ON-USER** | No AnySite credential exists on this machine — searched `~/.bashrc`, `~/.config/content/.env`, `.claude/settings.local.json`, `~/.cursor/mcp.json`, `~/.codex/config.toml`, `~/.dsh/`, and the Windows-side `.fcc`/hermes configs. Any paid adapter needs the user to supply one. |
| 3 | A working search key | — | **confirm** | `EXA_API_KEY` is set, and the `exa` adapter was run live against it. This is why the skill has an executed verification rather than a hypothetical one. |
| 4 | Storage format | parquet | **substitute** | Neither `pyarrow` nor `duckdb` is installed (checked system Python 3.12.3 and `~/.venvs/data`), and this repo's runtime rule is stdlib-only. JSONL keeps the same partition layout — `raw/<source_id>/<date>` — with no dependency. |
| 5 | Query engine | DuckDB over parquet, seen at 06:51 | **substitute** | Streaming stdlib query in `dataset.py`. Supports count, avg, sum, min, max, top-N, filters, and dotted field paths. Anyone who installs DuckDB can point it at the JSONL directly. |
| 6 | Spec format | YAML, parsed by the vendor CLI | **substitute** | `yaml` is not stdlib. `specfile.py` parses a strict subset and raises on anything it does not understand rather than guessing; `.json` is accepted natively. |
| 7 | Editor / host | Cursor on Windows, PowerShell prompts throughout | **drop** | Nothing in the workflow needs an editor. Steps are shell commands. |
| 8 | Scheduling | Narrated at 06:52–07:08, never shown on screen | **drop** | Reconstructing an unseen config would be invention. The skill points at cron or a systemd timer and says so. |
| 9 | Parallelism | `parallel: 3` in the on-screen spec | **confirm** | Implemented with `concurrent.futures`, capped at 16 so a spec cannot open an unbounded number of sockets. |
| 10 | Error policy | `on_error: skip` in the on-screen spec | **confirm, then tightened** | Implemented as shown. Execution then revealed that `skip` also swallowed *total* failure — see below. |

## What execution changed

Two bindings looked resolved on paper and were not:

- **`on_error: skip` did not mean what the spec implied.** With every input
  failing, the run exited 0 and printed `Done.` Tolerating partial failure is
  the documented intent; tolerating total failure is a silent-success bug in a
  scheduled pipeline. Total failure now exits 1, verified against a healthy run
  that still exits 0.
- **Date partitions were append-mode.** The video's `partition_by: [source_id,
  collected_date]` reads as a snapshot; the first implementation appended, so a
  same-day re-run doubled the store from 5 records to 10 and skewed every
  aggregate. Writes now replace the partition.

Neither was visible from the video. Both were found by running the skill.

## Credentials

Any step needing a logged-in session or a paid key is `BLOCKED-ON-USER` by
default. Specs reference credentials only as `${ENV:NAME}`, resolved from the
process environment at call time, so a spec is safe to commit. A missing
variable is a hard error naming the variable, never an empty string silently
substituted. `probe`-style outputs and capability maps are scrubbed of any
token before they are written.

Per this repo's two-layer convention, a key needs to exist in **both**
`~/.bashrc` (the cross-host baseline that Codex and DSH read) and
`.claude/settings.local.json`'s `env` block (which Claude Code injects into
non-interactive Bash calls). Setting only one of the two produces a skill that
works in one host and fails in another for no visible reason.
