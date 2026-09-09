---
name: source-set-workbench
description: Use when a pile of gathered material — reports, exports, call transcripts, PDFs, scattered notes — has to become an audited deliverable and every number must trace back to a source. Runs a staged workbench over a local source set with a citation manifest and a mechanical evidence gate - frame the decision, audit what is actually known, rank and fill the gaps, argue the opposite case, analyze the data, then build the report, model, SOP, or deck. Triggers on "source set", "workbench", "audit my research", "what is my research missing", "turn these documents into a report", "ground this in my files", "argue against my own idea". Not for driving the hosted NotebookLM web product in a browser — that is the notebooklm skill.
license: MIT
metadata:
  category: Research Operations
  legacy-frontmatter:
    version: '1.0'
    argument-hint: '[job name] [--goal "the decision this serves"]'
    user-invocable: true
---

# Source Set Workbench

Turns a folder of messy material into finished work whose every claim points at
a source. Adapted from Lian Lim's *Gemini Notebook Playbook for Founders* (10
plug-and-play prompts), retargeted from a hosted notebook to local files and
this repo's tooling, and extended with the two stages that playbook lacks:
**Frame** at the front and **Verify** at the back.

**No hosted product required.** The original prompts depend on Gemini Notebook's
agentic upgrade, which shipped 2026-06-08 gated to Google AI Ultra and Workspace
customers with AI Expanded Access, web only. This skill needs none of that — it
runs on files on disk with the tools already in this repo.

## Resolve the skill directory

Every command below lives under the directory containing this `SKILL.md`. Set
`SKILL_DIR` to that absolute path — your harness reported it when this file was
read — and substitute it literally.

```bash
SKILL_DIR="<absolute path of the directory containing this SKILL.md>"
[ -f "$SKILL_DIR/scripts/init_source_set.py" ] || { echo "bad SKILL_DIR: $SKILL_DIR" >&2; exit 1; }
```

## Start

```bash
python3 "$SKILL_DIR/scripts/init_source_set.py" "Q3 paid channel review" \
  --goal "Decide which channels to cut in Q4" \
  --adopt ~/Downloads/q3-exports
```

Scaffolds `$CONTENT_HOME/workbench/<slug>/` (default `~/Documents/Content`,
never the cwd) with `sources/`, `outputs/`, `SOURCES.md`, and `brief.md`.
Re-running indexes newly added sources without renumbering existing IDs.

## Route

Read `references/stages.md` and run the stage the request calls for. Full
prompts and per-stage gates live there.

| Ask | Stage |
|---|---|
| starting out, sources not gathered yet | 0 Frame |
| "what do we actually know?", "audit my research" | 1 Audit |
| "what's missing?", "what should I go find?" | 2 Gaps → fill |
| "poke holes in this", "argue against it" | 3 Falsify |
| "which channels made money?", any metric question | 4 Data → `ai-analyst` |
| "make a deck" | 5 Deck → `present` → `branded-pptx-deck` |
| "does this make money?", "build the model" | 6 Model |
| "write it up", "executive report" | 7 Report |
| "document how we do this" | 8 SOP |
| "why are we losing deals?" | 9 Call intelligence |
| "run the whole thing" | 10 Chain, one stage per turn |
| before anything ships | V Verify |

Two rules carry across every stage: **one source set = one job**, and **name the
artifact before reading the sources**. A set named for a decision stays useful;
a set named for a company is a junk drawer by Friday.

## The evidence contract

Read `references/evidence-contract.md`. In short: every factual line cites
`[Sn]` against `SOURCES.md`; missing numbers are marked `INPUT REQUIRED` rather
than invented; and the gate is a script, not an instruction.

```bash
python3 "$SKILL_DIR/scripts/check_output.py" outputs/report.md --manifest SOURCES.md
python3 "$SKILL_DIR/scripts/check_output.py" outputs/*.md --manifest SOURCES.md --strict
```

Fatal: unsourced magnitudes, citations to undefined IDs, an output with no
citations at all. Warned: unresolved sentinels (fatal under `--strict`) and
indexed-but-uncited sources.

**Passing the gate means well-formed, not true.** It verifies that a number is
attributed, never that the number is in the source it names. Only Stage V does
that, by re-deriving from sources without looking at the draft.

## What changed from the source playbook

| Original | Here | Why |
|---|---|---|
| "everything inside this notebook" | `sources/` + `SOURCES.md` with stable IDs | claims become checkable; provenance and retrieval dates survive |
| "it can find sources for you" | Research Tool Order: local → GBrain → Exa → Firecrawl → specialist MCP → WebSearch last | repo-wide rule; WebSearch first wastes the good tools |
| "mark it INPUT REQUIRED" | same marker, enforced by `check_output.py --strict` | advice that nothing checks is decoration |
| "create a PowerPoint" | route to `present` → `branded-pptx-deck` + the PPTX QA gate | client-facing decks have non-negotiable branding and QA rules here |
| "analyze your business data" | route to `ai-analyst` | it already has source-tieout and independent validation agents |
| — | **Stage 0 Frame** | the playbook's own setup advice, promoted to a gated stage |
| — | **Stage V Verify** | the playbook has no step that checks output against sources |

## Judgment rules

Editable policy for how this skill weighs evidence. Tune it here — do not
hardcode it into the stage prompts.

- **Popularity is not fit.** Never rank a source, vendor, or tool by how often
  it is cited, starred, or shared. Citation counts and stars are bookmark
  counts that only increase: they record that people noticed something once,
  not that it answers this question. Rank on fit to the stated decision, then
  on recency carrying an exact date.
- **Split every comparable in two: what transfers, and what exists only because
  that organization is that size.** A benchmark from a company with a hundred
  analysts reflects their headcount and data infrastructure, not yours.
  Importing their process without their reasons imports cost without benefit,
  and sizing your plan against their numbers inflates it until sound options
  look unaffordable. State which half a recommendation rests on.
- **Cost every recommendation at three points, not one:** today with current
  volume, the day the volume doubles, and at 10x. "Free to start" is not "cheap
  to operate." Name the cap and the crossing point, not just today's invoice.
- **A vendor's self-measured number is a claim about the vendor, not a fact
  about the world.** Cite it, name who measured it, and never let it stand as
  the sole support for a decision.
- **Where sources disagree, keep both.** Averaging two conflicting figures
  produces a third figure no source supports.

## Cost tier

Cheapest chain that can execute it: **Haiku** for Stages 0, 2 (indexing), 7,
and the gates; **Sonnet** for Stages 1, 3, 8, 9. Stage 4 delegates to
`ai-analyst` and Stage 5 to `branded-pptx-deck`, which carry their own tiers.
Do not silently upgrade the executor — that is a policy change, ask first.

## Verification

Executed 2026-08-15 on WSL2 / Python 3.

- `init_source_set.py` — scaffolded a workspace from 3 adopted files; manifest
  produced S1–S3 with paths and retrieval dates; re-run appended without
  renumbering. PASS
- `check_output.py` — on a fixture containing one sourced claim, one unsourced
  `34%`, a dangling `[S9]`, a single-digit count, an ISO date, a waived line, a
  sentinel, and a fenced code block: caught the unsourced magnitude and the
  dangling citation as fatal (exit 1), warned the sentinel, flagged the uncited
  source, and correctly ignored the other four. Clean file exits 0; `--strict`
  promotes the sentinel to fatal (exit 1). PASS
- `openpyxl` 3.1.5 confirmed present system-wide, so Stage 6 writes real
  workbooks rather than CSV substitutes. PASS
- Stages 1–3 and 7–10 are prompt contracts, not code. They are **NOT EXECUTED**
  against a live source set in this repo. Their gates are stated per stage in
  `references/stages.md`; treat their claimed behavior as a hypothesis until a
  real run is recorded here.
