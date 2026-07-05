---
name: aeo-pattern-miner
description: Use when mining AEO/AI-search answer captures for recurring market patterns, buyer language, cited authorities, category themes, and gaps between AI-answer narratives and the Agent Replacement Scorecard.
argument-hint: "[run-dir]"
permissions:
  file_read:
    - runs/
    - skills/aeo-pattern-miner/
  file_write:
    - runs/
  shell:
    allowed_scripts:
      - scripts/mine_patterns.py
---

# aeo-pattern-miner

Mine captured AI answers for real market patterns. This skill treats AI-search
answers as a sensemaking surface: what themes, examples, sources, and buyer
frames are already showing up?

This is not a keyword matcher. The pipeline extracts answer-level evidence
units, groups them with semantic/concept-anchor scoring, and creates a
subagent-review brief so independent reviewers can accept, reject, split, or
rename candidate patterns against the raw evidence.

Use this after `aeo-orchestrator` or `aeo-live-capture` has produced
`answer_captures.jsonl` and raw answer text.

Business purpose: this is the missing layer between AEO evidence and strategy.
It should help discover real market mechanisms from AI-answer surfaces before
we rewrite diagnostics, decks, or consulting offers around them.

## Runtime Preamble

Say: "Running `aeo-pattern-miner`: I will mine captured AI answers for recurring
patterns, cite the capture IDs behind each pattern, and separate observed
patterns from our own scorecard thesis."

## Workflow

1. Read the run folder:
   - `manifest.json`
   - `stage_outputs/answer_captures.jsonl`
   - `stage_outputs/raw/*.txt`
   - `stage_outputs/sources.jsonl`
2. Mine captures for:
   - semantic evidence units
   - recurring economic mechanisms
   - architecture/workflow mechanisms
   - buyer/procurement frames
   - risk/human-review boundaries
   - citation/source authority patterns
   - repeated category examples and contradictions
3. Write:
   - `normalized/capture_units.jsonl`
   - `normalized/semantic_clusters.jsonl`
   - `normalized/pattern_candidates.jsonl`
   - `working/subagent-review-brief.md`
   - `final/pattern-discovery-audit.json`
   - `final/pattern-mining-report.md`
4. Use the report to decide what diagnostic or scorecard pattern deserves
   business-facing treatment.

## Command

```bash
python3 skills/aeo-pattern-miner/scripts/mine_patterns.py runs/<run-id>
```

## Pattern Rule

Patterns are not "true" because the model says them. They are candidates when:

- they appear across multiple captures, or
- they appear in one high-intent capture with clear citation/source support, or
- they reveal a gap between AI-answer language and our scorecard language.

Do not promote a candidate from semantic similarity alone. A promoted pattern
needs exact evidence units, independent captures, source/citation support when
the claim is about authority, and semantic/adversarial review.

## Subagent Review Protocol

Use subagents after deterministic extraction, not before. Give reviewers
`working/subagent-review-brief.md`, `normalized/capture_units.jsonl`, and the
raw capture paths. Ask for strict JSONL review rows:

```json
{"pattern_id":"...","decision":"accept|revise|reject","rationale":"...","missing_evidence":["..."],"better_label":"...","accepted_evidence_unit_ids":["..."],"rejected_evidence_unit_ids":["..."]}
```

Recommended review lanes:

- semantic support reviewer - does the exact evidence support the mechanism?
- adversarial reviewer - are captures independent, non-circular, and not thesis
  laundering?
- source/citation reviewer - do cited domains actually support authority claims?
- buyer/procurement reviewer - does the evidence support commercial action?

## Skill Relationships

### Category
Data & Analysis

### Dependencies
- `aeo-orchestrator` or `aeo-live-capture` - provides answer captures.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `aeo-orchestrator` | Sequential upstream | after query/capture run | `stage_outputs/answer_captures.jsonl` |
| `aeo-live-capture` | Sequential upstream | when real AI answers were pasted | `stage_outputs/raw/cap_live_*.txt` |
| `aeo-gap-analyzer` | Peer | gap analyzer recommends actions; pattern miner discovers themes | `normalized/pattern_candidates.jsonl` |
| `agentic-blueprint-pipeline` | Downstream | when a pattern becomes an implementation thesis | `final/pattern-mining-report.md` |
| subagent reviewers | Sequential downstream | when semantic candidates need validation | `working/subagent-review-brief.md` |

## Host Compatibility

Canonical source: `skills/aeo-pattern-miner/SKILL.md`.

Works in Claude Code, Codex, and OpenHands because it uses local artifacts and a
stdlib Python script.

## Gotchas

- Do not treat seed captures as market evidence without labeling them.
- Manual live captures prove only what was pasted into the run. If the operator
  pasted test text, label the report as workflow validation, not market
  evidence.
- Do not collapse distinct mechanisms into generic "AI replaces SaaS."
- Do not promote a pattern to business-facing copy unless it has evidence unit
  IDs, not just capture IDs.
- Do not call source-domain frequency a citation-authority pattern unless the
  cited source supports the specific claim.
