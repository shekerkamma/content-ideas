---
name: dataset-collect
description: 'Use when a repeated data pull should land in a local queryable store instead of a context window — "collect this every week", "pull profiles for these 40 companies", "the results are too big for the chat", "turn this one-off pull into a pipeline", "run this dry first". Declarative spec, pluggable fetch adapters, JSONL partitions, and aggregate queries that return a number rather than the records. Not a research or analysis skill: it collects and answers, it does not interpret.'
license: MIT
metadata:
  category: Agent Engineering
  version: '1.0'
  compatibility: Python 3 stdlib only. Claude Code, Codex, DeepSeek Harness, or any host with a shell.
  derived-from-video: https://www.youtube.com/watch?v=nI0Mhzcl2Fk
  derived-on: '2026-08-25'
  source-upload-date: '2026-08-24'
---

# Dataset Collect

Turns a repeated data pull into a spec file, a local store, and queries that
return answers instead of records. It deliberately does **not** analyse,
summarise, or decide — it exists so that the model doing those things never has
to hold the raw rows.

**Source:** derived from a video demonstration of a vendor CLI, then rebuilt
vendor-neutral and executed here. See `references/source-video.md` for what was
demonstrated versus what was claimed, and `references/environment-bindings.md`
for every assumption that came from the demonstrator's machine.

## When to invoke

- A pull that will be repeated: weekly competitor monitoring, a watchlist, a
  recurring enrichment pass.
- A pull whose result is too large to sit in a conversation — dozens of
  companies, hundreds of posts, any "and now do the same for the other four".
- A question that is really an aggregate: *how many*, *what is the average*,
  *which are the top five* — where the records are a means, not the answer.
- Any collection that costs money per call and therefore wants a dry run first.

Do not invoke it to *interpret* what was collected. Hand the aggregate to
whichever analysis skill owns that job.

## Procedure

Each step names the tool route it runs on in this host, not the click the
demonstrator made.

1. **Write the spec.** Route: `Read/Write`. One file describes the whole
   collection — sources, adapter, inputs, storage. Copy
   `assets/competitor-monitor/competitor-monitor.yaml` and edit it. `.json` is
   accepted wherever `.yaml` is.

   ```yaml
   name: competitor-monitor
   sources:
     - id: competitor_profiles
       adapter: http            # file | http | exa
       base_url: https://api.example.com
       endpoint: /v1/company
       headers: {Authorization: 'Bearer ${ENV:VENDOR_API_KEY}'}
       from_file: competitors.txt
       input_key: company
       parallel: 3
       on_error: skip
   storage:
     format: jsonl
     path: ./data/competitor-monitor/
   ```

   `${ENV:NAME}` is resolved from the process environment at call time, so a
   spec never carries a credential and is safe to commit.

2. **Dry run before spending anything.** Route: `Bash`. Prints the plan —
   every source, adapter, and input count — and makes zero calls.

   ```bash
   python3 scripts/dataset.py collect <spec> --dry-run
   ```

3. **Collect narrow, then wide.** Route: `Bash`. `--limit` caps inputs per
   source, so the first real run costs a handful of calls rather than all of
   them.

   ```bash
   python3 scripts/dataset.py collect <spec> --limit 2   # prove the adapter
   python3 scripts/dataset.py collect <spec>             # then the rest
   ```

   Records land at `<storage.path>/raw/<source_id>/<YYYY-MM-DD>.jsonl`. A date
   partition is a snapshot: re-running the same day replaces it rather than
   appending, so a retry cannot inflate the store.

4. **Ask the store, not the model.** Route: `Bash`. This is the step that pays
   for the other three.

   ```bash
   python3 scripts/dataset.py status <spec>
   python3 scripts/dataset.py query <spec> --source S --count
   python3 scripts/dataset.py query <spec> --source S --avg employee_count
   python3 scripts/dataset.py query <spec> --source S --where "employee_count>100" \
                                            --select name,country --limit 20
   python3 scripts/dataset.py query <spec> --source S --top followers --limit 5
   ```

   `--where` takes `=`, `!=`, `>`, `<`, `>=`, `<=`, and `~=` (case-folded
   substring), is repeatable, and ANDs. Fields accept dotted paths
   (`locations.0.country_code`).

5. **Schedule it, if it recurs.** Route: `Bash` — `cron`, a systemd user timer,
   or the host's own scheduler. `BLOCKED-ON-USER` if the schedule must land on
   a machine or account you do not control. Nothing about scheduling was
   demonstrated in the source video (see Limits), so treat this step as this
   repo's, not the demonstrator's.

6. **Add a provider** only when an existing adapter cannot reach it. Route:
   `Read/Write`. One function in `scripts/adapters.py` taking
   `(source, value, spec_dir)` and returning `list[dict]`, registered in
   `ADAPTERS`. The collector, store, and query path never learn its name.

## Judgment rules

Editable policy. Tune these; do not hardcode them into the steps.

- **Records go to disk; only answers go to the model.** The demonstrator's
  framing (video 03:34) is that filtering happens away from the context window,
  not inside it. Whether a given vendor filters server-side is a vendor claim —
  what this skill guarantees is the local half, which holds regardless.
- **Dry-run anything metered.** The demonstrator ran a dry run "before spending
  any credits" (video 06:10). Keep that reflex for any paid adapter; skip it
  freely for `file`.
- **`--limit 2` before the full run.** Not from the video. An adapter that is
  wrong is wrong on the second call as cheaply as the fortieth.
- **`on_error: skip` for wide sweeps, `halt` for small exact ones.** The
  demonstrator used `skip` across five companies (video 06:17). Skip is right
  when a missing input is tolerable and wrong when it is the point.
- **`parallel: 3` is the demonstrated default** (video 06:17), capped here at
  16. Raise it only against a provider whose rate limit you have actually read.
- **Prefer an aggregate flag over `--select`.** `--count` and `--avg` return one
  line. Reach for row output only when a human will read the rows.
- **A partition is a snapshot, not a log.** If you need change-over-time, query
  across dates; do not append twice to one date to fake history.

## Environment bindings

Everything below was true on the demonstrator's machine. See
`references/environment-bindings.md` for the full accounting.

| Binding | In the video | On this machine |
|---|---|---|
| Data provider | AnySite (paid, promo code, trial credits visible) | **substitute** — pluggable adapters; `exa` verified live, `http` covers any REST provider including AnySite |
| Provider credential | AnySite API key in dashboard | **BLOCKED-ON-USER** for any paid adapter; `EXA_API_KEY` confirmed present, `file` needs none |
| Store format | parquet | **substitute** — JSONL; no `pyarrow`/`duckdb` on this machine and the repo runtime is stdlib-only |
| Query engine | DuckDB `read_parquet(...)` | **substitute** — streaming stdlib query in `dataset.py` |
| Spec format | YAML via the vendor CLI | **substitute** — strict YAML subset parser, plus native `.json` |
| Host | Cursor on Windows, PowerShell | **drop** — POSIX shell; no Cursor dependency anywhere |
| Scheduling | asserted, never shown on screen | **drop** — use cron/systemd; see Limits |

## Verification

```bash
cd skills/dataset-collect
rm -rf assets/competitor-monitor/data
python3 scripts/dataset.py collect assets/competitor-monitor/competitor-monitor.yaml --dry-run
python3 scripts/dataset.py collect assets/competitor-monitor/competitor-monitor.yaml
python3 scripts/dataset.py query  assets/competitor-monitor/competitor-monitor.yaml \
        --source competitor_profiles --count            # -> 5
python3 scripts/dataset.py query  assets/competitor-monitor/competitor-monitor.yaml \
        --source competitor_profiles --avg employee_count  # -> 407.0
python3 -m pytest tests/ -q
```

**Executed 2026-08-25** against this repo at branch
`feat/dsh-multi-model-providers`, Python 3.12.3.

Independently confirmed, not self-reported:

- Dry run made zero calls and wrote nothing; `collect` then wrote 5 records to
  `raw/competitor_profiles/2026-08-25.jsonl`, matching the record count and
  wording the source video shows at 06:31.
- `--avg employee_count` returned `407.0`; hand-checked against the fixture
  ((243+373+48+1367+4)/5 = 407).
- The `exa` adapter was run against the live Exa API from a throwaway
  directory: 2 inputs, 6 records, real URLs returned.
- **Two defects were found by executing and then fixed**, neither visible from
  reading the video:
  1. With every input failing (`EXA_API_KEY` unset, `on_error: skip`), the run
     printed `Done.` and exited **0**. A scheduled pipeline would have reported
     success forever after a credential expired. Total failure now exits 1;
     verified in both directions — a healthy run still exits 0.
  2. Re-running the same day **appended**, taking the store from 5 records to
     10 and silently skewing every aggregate. Partitions are now idempotent;
     three consecutive identical runs leave exactly 5.

- **Cross-host discovery was measured, not assumed.** DeepSeek Harness's own
  `@deepseek-ai/dsh-skill-filesystem` provider was driven directly against this
  repo: it resolves `<projectRoot>/.agents/skills` at rank 200, and `list()`
  returned this skill by name with its description parsed and zero warnings.
  The frontmatter was re-parsed with the same `yaml` package DSH ships.

## Limits

- Derived from pixels and narration, not an event stream. Steps performed
  off-screen were never captured.
- **Scheduling was asserted, never demonstrated.** The narration says a
  schedule can be added to the pipeline (video 06:52–07:08), but no schedule
  block appears in any frame. Step 5 is this repo's construction.
- **The narration and the screen disagree about the pipeline's shape.** The
  narration describes three steps — search, enrich, store to a database (video
  05:56–06:06). The YAML on screen at 06:17 has **one** source writing parquet
  files, with database loading offered afterwards as a separate optional
  command. The screen is what was built.
- **"Filtering happens on the provider's side" is a vendor claim, not a
  measurement.** The frames show a filtered result, which is equally consistent
  with client-side filtering. This skill does not depend on it either way.
- Third-party UI in the source video dates from 2026-08-24. Treat every vendor
  specific as expiring evidence.
- The spec parser accepts a deliberate YAML subset and errors on anything else.
  That is a feature — use `.json` when a spec genuinely needs full YAML.
- `--sql` is not implemented. If DuckDB is installed, point it at the JSONL
  directly (`read_json_auto`); this skill will not shell out to it for you.

## Host compatibility

| Host | Status |
|---|---|
| Claude Code | Full. Scripts run under `Bash`. |
| Codex CLI / Desktop | Full. Stdlib only; nothing Claude-specific in any step. |
| DeepSeek Harness | Full. Discovered from `<projectRoot>/.agents/skills` (rank 200) or `~/.dsh/skills`; frontmatter uses only keys DSH parses. |
| Any host with a shell | Full. |
