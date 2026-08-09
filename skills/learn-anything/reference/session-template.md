# Session File Format

Used by the Context Push step (after Step 5). This is the universal handoff format
consumed by graphify, content-research, and GBrain across sessions.

## File Location

```bash
LEARN_DIR="${SECOND_BRAIN_DIR:-$HOME/Documents/Learning}"
mkdir -p "$LEARN_DIR"
SLUG=$(echo "[TOPIC]" | tr '[:upper:] ' '[:lower:]-' | sed 's/[^a-z0-9-]//g')
DATE=$(date +%Y-%m-%d)
FILE="$LEARN_DIR/$DATE-$SLUG.md"
```

## Required Format

```markdown
# Learning Session: [TOPIC]
Date: [DATE]
Slug: [SLUG]
Specific Gap: [FINAL SPECIFIC QUESTION FROM STEP 1]

## What I Now Know
[User's own reconstruction from Step 4 — their words, not AI jargon]

## Confirmed Facts (with sources)
- [claim] — [source URL] — confidence: [HIGH/MEDIUM/LOW]

## Source URLs
- [url-1]
- [url-2]

## Knowledge Map

### Nodes
- [CONCEPT_A]: [one-line description]
- [CONCEPT_B]: [one-line description]

### Relationships
- [CONCEPT_A] → REQUIRES → [CONCEPT_B]
- [CONCEPT_A] → CONTRASTS_WITH → [CONCEPT_C]
- [CONCEPT_B] → ENABLES → [CONCEPT_D]

## Open Questions
- [remaining X items or new gaps discovered during testing]

## Test Results
- Predicted: [X] | Got: [Y] | Match: YES / NO → [what the mismatch taught us]

## Next Step
[What to investigate next, or "complete" if done]
```

## Field Notes

- **`## What I Now Know`** — user's own words from Step 4 reconstruction. Not AI jargon, not the blog post's phrasing. If they can't write this section without looking at sources, Step 4 is not done.
- **`## Confirmed Facts`** — only claims that passed the Six Accuracy Checks. Unverified claims go to Open Questions.
- **`## Source URLs`** — canonical list for the content-research handoff. Any URL here that was NOT ingested during Step 3 gets offered to content-research at session close.
- **`## Knowledge Map`** — what graphify parses as entities and edges. Relationship verbs must describe *why* the connection matters:
  - `REQUIRES` — A cannot exist or function without B
  - `CAUSES` — A produces B as an effect
  - `CONTRASTS_WITH` — A and B differ in a meaningful way
  - `ENABLES` — A makes B possible but doesn't require it
  - `IS_PART_OF` — A is a component of B
  - `IMPLEMENTS` — A is a concrete realization of B
  - `REPLACES` — A supersedes or substitutes for B
- **`## Open Questions`** — remaining X items from Step 2, plus any new gaps discovered during Step 5 testing. These seed the next session's Step 1.
- **`## Test Results`** — every prediction from Step 5 recorded here, including mismatches. Mismatches are the most valuable entries — they capture the exact new specific gap discovered.
- **`## Next Step`** — single next action: a new specific gap to feed back into Step 1, a URL to ingest, or "complete" if all Step 2 items are resolved.

## GBrain Page Body

When writing back to GBrain (`learning/[SLUG]`), use only:
- `## What I Now Know` block
- `## Confirmed Facts` block
- Tags: `learning`, `[topic-area]`, `[date]`

Do not write the full session file to GBrain — the local file is the complete record.
