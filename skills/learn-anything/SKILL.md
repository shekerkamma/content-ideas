---
name: learn-anything
description: 'Use when someone says "teach me", "I don''t know what I don''t know about", "help me understand", "I''m stuck on", "/learn-anything", "/specificity", or "/idk". Runs the 5-step Specificity Method: articulate gap → decompose → verify → reconstruct → test. Chains grill-me (fog discovery), content-research (URL ingestion), graphify (post-session knowledge graph), and GBrain (persistent recall). Use for any topic.'
allowed-tools:
- AskUserQuestion
- WebSearch
- WebFetch
- mcp__claude_ai_Exa__web_search_exa
- Read
- Write
- Bash
- Skill
metadata:
  legacy-frontmatter:
    version: 1.1.0
    trigger: /learn-anything
    aliases:
    - /specificity
    - /idk
---

# The Specificity Method

> "name it. break it. explain it. say it back. test it."
> — from the Specificity Method (youtube.com/watch?v=CJ91YJ6GvN4)

**The whole game:** Move from a fuzzy feeling ("I don't get X") to a clear, specific,
actionable gap ("I don't know *why* X does Y when Z"). Specificity is the entire game.
A feeling cannot be solved. A problem can be worked on.

---

## Skill Wiring Map

```
 ┌──────────────────────────────────────────────────────────────┐
 │  CONTEXT PULL (runs before Step 0)                           │
 │  GBrain recall + prior ~/Documents/Learning/ + brainstorms/  │
 └──────────────────┬───────────────────────────────────────────┘
                    │
                    ▼
 ┌──────────────────────────────────────────────────────────────┐
 │  learn-anything CORE (Steps 0–5)                             │
 │                                                              │
 │  Step 1 fog ──→ /grill-me → brainstorms/{date}-{slug}.md     │
 │                 ↩ read Topic string back → proceed           │
 │                                                              │
 │  Step 3 ────→ /content-research (URLs found during verify)   │
 │                 ↩ Obsidian note + graphify fed automatically  │
 │                                                              │
 └──────────────────┬───────────────────────────────────────────┘
                    │
                    ▼
 ┌──────────────────────────────────────────────────────────────┐
 │  CONTEXT PUSH (runs after Step 5)                            │
 │  Session file → GBrain write-back → /graphify knowledge map  │
 └──────────────────────────────────────────────────────────────┘
```

---

## Chaining Contracts

This skill reads and writes a **session file** as the universal handoff format.
All downstream skills consume this same file — nothing is skill-specific.

**Session file location:**
```
LEARN_DIR="${SECOND_BRAIN_DIR:-$HOME/Documents/Learning}"
FILE="$LEARN_DIR/{YYYY-MM-DD}-{topic-slug}.md"
```

**GBrain page slug convention:** `learning/{topic-slug}`

**Graphify trigger:** `graphify ~/Documents/Learning/ --update`
(incremental — only reprocesses new/changed files)

**grill-me handoff:** reads `brainstorms/{date}-{slug}.md`, extracts:
- `Topic string:` line → becomes the specific gap for Step 1
- `Entities:` line → becomes the seed nodes for Step 2 decomposition

**content-research handoff:** any URL surfaced during Step 3 verification can be
passed directly to `/content-research <url>` — it will ingest, write an Obsidian
note, and run graphify automatically. The session file `## Source URLs` section is
the canonical list for this.

---

## Context Pull — Run Before Step 0

Before doing anything else, pull prior context on this topic.

### 1. GBrain recall

```bash
gbrain search "{TOPIC}" 2>/dev/null | head -40 || echo "GBRAIN_MISS"
```

If results found: summarize what was already learned (1-3 sentences). Tell the user:
"Found prior context on [TOPIC] from [date]. Continuing from where we left off."

If miss: proceed fresh.

### 2. Prior session files

```bash
LEARN_DIR="${SECOND_BRAIN_DIR:-$HOME/Documents/Learning}"
SLUG=$(echo "{TOPIC}" | tr '[:upper:] ' '[:lower:]-' | sed 's/[^a-z0-9-]//g')
ls "$LEARN_DIR"/*"$SLUG"*.md 2>/dev/null | sort -r | head -3
```

If prior sessions found: read the most recent one. Extract:
- `## Specific Gap` — what was the exact question last time
- `## Open Questions` — what remained unresolved
- `## What I Now Know` — don't re-teach this

Offer the user a choice (AskUserQuestion):
- **Continue** — resume from open questions
- **Go deeper** — use prior reconstruction as the new baseline, push further
- **Fresh start** — ignore prior sessions, start clean

### 3. Prior brainstorm files

```bash
ls brainstorms/*"$SLUG"*.md 2>/dev/null | sort -r | head -3
```

If found: read the latest. Extract `Topic string:` and `Entities:` for Step 1/2 seeding.

---

---

## Step 0 — Detect the input

Parse what the user gave you:

- **Mode A** — gap is already named: e.g. `/learn-anything why Claude sub-agents don't
  inherit parent context`  → skip Step 1 brainstorm, go straight to Step 2
- **Mode B** — fog: e.g. `/learn-anything AI agents` or `/learn-anything I don't know
  what I don't know about X` → run the full Step 1 brainstorm first

State which mode you're in before proceeding.

---

## Step 1 — Articulate the Gap

*The step almost everyone skips.*

**Goal:** Convert the vague feeling into ONE precise sentence: "I don't know X."

### If Mode B (fog):

**First — offer to route to `/grill-me`** for complex or multi-faceted topics.
Use AskUserQuestion:

> "[TOPIC] is a large territory. To find your real question, I can either ask you
> a few targeted questions here, or run `/grill-me` — a deeper interview that
> checkpoints every answer to a brainstorm file so nothing is lost."

Options:
- **Quick 3 questions here** — I'll ask targeted questions inline (2-3 min)
- **Run /grill-me** — full discovery interview, saves to `brainstorms/` (10-15 min)

**If they choose `/grill-me`:**

Invoke it via the Skill tool with the topic pre-seeded:
```
Skill("grill-me", args="{TOPIC} — goal: find the single most specific thing I don't understand")
```

After grill-me completes, read its capture file:
```bash
ls brainstorms/ | grep "{slug}" | sort -r | head -1
```

Extract from the capture file:
- `Topic string:` → this becomes the **specific gap** for Step 1
- `Entities:` → seed the decomposition list in Step 2
- Any `FLAG:` items → add to `## Open Questions` in session file

Resume at Step 2 with the extracted specific gap. Tell the user:
"Using your grill-me session: specific gap = '[EXTRACTED TOPIC STRING]'. Moving to decompose."

**If they choose quick questions:**

Ask the user three questions (one at a time via AskUserQuestion):
1. What have you already tried or read about [TOPIC]?
2. What would you do differently once you understood this?
3. What's the first sentence you couldn't explain to someone else right now?

Use their answers to calibrate depth: builders need actionable specifics, strategists
need landscape + tradeoffs, teachers need analogies + misconceptions.

Work with the user until you can complete this sentence together:
**"I don't know [SPECIFIC X]."**

State the gap clearly before moving to Step 2.

---

## Step 2 — Decompose into Pieces

*Lists are tractable. Fogs aren't.*

**Goal:** Break the named gap into its smallest moving parts. The X's (gaps) are
your real questions — not the original vague one.

### How to decompose:

1. List everything the user *thinks* they know about the topic
2. For each piece, ask: "Could you explain this to someone else right now?" 
   - YES → checkmark (known)
   - NO / UNSURE → X mark (real gap)
3. The X's become the specific sub-questions to investigate

### Decompose prompt:

```
"List every component, concept, or decision involved in [SPECIFIC GAP].
For each one, mark it as: ✓ (I understand this), ? (partial), ✗ (I don't know this).
The ✗ items are my actual questions. Ask those, not the original vague one."
```

Present the decomposed list. Highlight the X items. Confirm with the user which
X they want to tackle first — one at a time.

**Lock in the specific question** before Step 3.

---

## Step 3 — Explain and Verify (Six Accuracy Checks)

*The meat of the whole framework. AI is a pattern-matching machine — it can hand
you confident bullshit. These six checks stop that.*

**Goal:** Get a clear, accurate explanation — then actually verify it.

### Choose a Master Learning Prompt first:

> Reference: Read `reference/master-prompts.md` for all 6 master learning prompts: (1) Feynman Technique — for deep conceptual understanding, (2) 80/20 Learning — for practical results fast, (3) Personal Tutor — for complete beginners, (4) Deep Research — for strategy/decisions/contested claims, (5) Learn by Doing — for code/tools/skills, (6) Mastery and Feedback — for identifying unknown unknowns.

**Ask the user which prompt style fits, or recommend one based on their Step 0 answer.**

### Deep ingestion route → `/content-research`

If the explanation references **specific URLs** (official docs, GitHub repos, YouTube
explainers, LinkedIn posts), offer to run `/content-research` on them:

> "I found [N] source URLs. Want me to run `/content-research` on them?
> It will ingest, analyze, save a structured Obsidian note, and feed them into
> your knowledge graph automatically."

If yes — invoke content-research for each URL:
```
Skill("content-research", args="{URL}")
```

The content-research skill handles the full chain: ingest → Obsidian → graphify.
After it completes, continue with the Six Accuracy Checks using the ingested content.
Record all URLs in the session file under `## Source URLs` for the graphify push.

---

### Six Accuracy Checks (run AFTER the explanation):

**1. Demand citations**
Ask: "Provide the source for each claim. No source = hypothesis, not fact."

**2. Verify the citation**
Do NOT trust the summary. Open the page. Read the actual content.
```
"Open [URL] and read the actual page — not a summary. Does the source say what
you claimed? Quote the exact relevant passage."
```

**3. Triangulate**
Cross-reference at least 3 sources: official docs + GitHub repo/issues + a
different AI model (or Reddit/forums for real-world usage patterns).
Where they agree = higher confidence. Where they diverge = flag for user.

**4. Date-check**
Explicitly add: "Check as of today [CURRENT DATE]."
AI training data is months old. Features, APIs, and best practices change weekly.
Flag anything where the answer might have changed.

**5. Probe uncertainty**
Ask: "What would falsify this explanation? If it can't be falsified, it's
pattern-matching, not fact."
Also: "Do one final sweep — did you miss any sources or get anything wrong?"
(This almost always surfaces new information.)

**6. Ask what's missing**
Ask: "What would I need to know that you haven't told me? What gaps remain?"

---

After the six checks: summarize what is now **confirmed**, what is **likely**,
and what is **still uncertain**. Be explicit about the confidence level.

---

## Step 4 — Reconstruct

*If you reach for the source to explain it, you faked understanding.*

**Goal:** Close the laptop (figuratively). Explain it back in your own words.
Your own words, your own analogies, your own mental model. Not AI jargon.
Not the blog post's phrasing.

### Reconstruction prompt:

```
"I'm going to explain what I think I now understand. Correct me where I'm wrong,
and tell me if my mental model has any gaps or subtle errors.

[User explains in their own words]"
```

### How to run this step:

1. Ask the user: "Don't look at the sources. Explain [SPECIFIC GAP] back to me
   in your own words. I'll tell you where your mental model is off."
2. User explains. You respond with:
   - What they got right (affirm)
   - What is subtly wrong or missing (correct precisely)
   - Any hidden edge case or exception their model doesn't account for
3. Repeat until the user can explain it cleanly without reaching for the source.

**Language is the test.** If they stumble on a word, they don't own the concept yet.
If they explain it in terms that *make sense for their own context*, they do.

---

## Step 5 — Apply and Test

*Mismatch = a precise gift.*

**Goal:** Make a prediction. Run it. Compare result to prediction.
A wrong prediction is not failure — it is a new, more specific gap to feed back
into Step 1.

### Sandbox preflight (run once at session start)

Before Step 1, check whether Docker is available:

```bash
python3 ~/.claude/skills/learn-anything/scripts/sandbox_runner.py --check
```

- If `{"available": true}` → sandbox is live. Tell the user: "Sandbox ready — Step 5 will run your test automatically."
- If `{"available": false, ...}` → note the reason, then tell the user: "Docker unavailable — I'll describe the test at Step 5 and you paste results back."

Store this as `SANDBOX_AVAILABLE=true/false` for Step 5.

### Technology context detection

Infer the sandbox type from the topic. Detection order:
1. Explicit override in the trigger (e.g., `/learn-anything python: async`) → use that tag
2. Keywords in Step 2 topic decomposition → detect `python / js / sql / bash / claude-code`
3. Fallback → `bash`

Store as `TECH_CONTEXT` for Step 5.

### Apply prompt:

```
"Based on what I now understand about [SPECIFIC GAP], I predict that if I do [X],
the result will be [Y]."
```

### Test loop — sandbox path (SANDBOX_AVAILABLE=true):

1. User states prediction.
2. Write a minimal scaffold that tests exactly the prediction — the smallest code that
   produces the output the user predicts, or fails if the prediction is wrong.
3. Build `step5-task.json` and run the sandbox:

```bash
SLUG="[session-slug]"
SANDBOX_DIR="/tmp/learn-sandbox/$SLUG"
mkdir -p "$SANDBOX_DIR"

# Write step5-task.json
cat > "$SANDBOX_DIR/step5-task.json" << 'EOF'
{
  "slug": "[SLUG]",
  "prediction": "[USER PREDICTION VERBATIM]",
  "tech_context": "[TECH_CONTEXT]",
  "scaffold": "[MINIMAL CODE THAT TESTS THE PREDICTION]",
  "success_criterion": "[WHAT OUTPUT PROVES THE PREDICTION CORRECT]"
}
EOF

# Run sandbox
echo "Running sandbox..."
python3 ~/.claude/skills/learn-anything/scripts/sandbox_runner.py \
  --task "$SANDBOX_DIR/step5-task.json"
```

4. Read `step5-result.json` from `$SANDBOX_DIR`. Inject verdict:
   - `exit_code == 0` and stdout matches success criterion → **"Your prediction was correct."** Show actual output.
   - `exit_code != 0` or output doesn't match → **"Your prediction didn't match."** Show actual output + stderr.
   - `timed_out == true` → treat as mismatch: "Test timed out after 60s."
   - `docker_error` set → fall back to manual path, explain the error in one line.

5. After verdict:
   - **Match** → understanding validated. Move to next piece or declare done.
   - **Mismatch** → "Excellent. This is a new, precise gap." The actual output IS the new gap.
     Feed it back into Step 1 as Mode A: "Here's the new precise gap: [mismatch detail]."

6. Clean up: `rm -rf "$SANDBOX_DIR"`

### Test loop — manual path (SANDBOX_AVAILABLE=false):

1. User states prediction.
2. Write the same minimal scaffold and show it to the user with: "Run this and paste the output back."
3. User pastes result.
4. Same match/mismatch verdict and Step 1 re-entry logic as above.

**The loop:** Step 5 mismatch → Step 1 (Mode A, new precise gap) → Step 2 → Step 3
→ Step 4 → Step 5. Each loop tightens understanding.

Declare the session complete when:
- The user can predict outcomes correctly
- OR the user explicitly says "I have enough to move forward"
- OR all items from Step 2 are resolved

---

## Context Push — Run After Step 5

The session is not complete until context is pushed to all three layers.
Do NOT skip this — it is what makes the skill compound across sessions.

### 1. Write the session file (always)

> Reference: Read `reference/session-template.md` for the full session file format. Required fields: title, date, slug, specific gap, What I Now Know (user's own words), Confirmed Facts with sources and confidence, Source URLs, Knowledge Map (nodes + relationships with verbs: REQUIRES/CAUSES/CONTRASTS_WITH/ENABLES/IS_PART_OF/IMPLEMENTS/REPLACES), Open Questions, Test Results, Next Step.

### 2. GBrain write-back

```bash
gbrain put "learning/$SLUG" 2>/dev/null || echo "GBRAIN_SKIP"
```

Write a GBrain page with:
- Title: `learning/[SLUG]`
- Body: the `## What I Now Know` + `## Confirmed Facts` blocks from the session file
- Tags: `learning`, `[topic-area]`, `[date]`

If gbrain is unavailable, skip silently — the session file is the fallback.

### 3. Offer graphify update

After writing the session file, offer to update the knowledge graph:

> "Session saved to `~/Documents/Learning/`. Want me to run `/graphify` on the
> learning folder to update your knowledge graph? It's incremental — only the
> new session gets processed."

If yes:
```
Skill("graphify", args="~/Documents/Learning/ --update --wiki")
```

The `--wiki` flag also generates an `index.md` for agent-crawlable navigation.
After graphify completes, tell the user the graph location and offer to open it.

### 4. Offer content-research for unprocessed source URLs

If `## Source URLs` in the session file contains URLs that were NOT already
processed via content-research during Step 3:

> "There are [N] source URLs not yet in your Obsidian vault. Want me to run
> `/content-research` on them now?"

If yes — invoke content-research for each remaining URL.

---

## Completion

End every session with:

> **name it** ✓ → **break it** ✓ → **explain it** ✓ → **say it back** ✓ → **test it** ✓
>
> Failure is the system, not the fallback. If a step surfaces a new gap, run it again.
> That's not getting stuck — that's learning working exactly as designed.

---

## Quick Reference: Which Prompt for Which Situation?

| Situation | Use |
|-----------|-----|
| Concept feels abstract, can't picture it | Feynman Technique |
| Need to use this skill ASAP, time-boxed | 80/20 Learning |
| Completely new territory | Personal Tutor |
| Making a decision / choosing between options | Deep Research |
| Learning a tool, framework, language | Learn by Doing |
| Not sure what you don't know | Mastery and Feedback |

---

## Credit

Framework: "The Specificity Method" — youtube.com/watch?v=CJ91YJ6GvN4
Master Prompts: "6 Master Prompts to Learn Anything" — Nipam Kalita (LinkedIn)

---

## Skill Relationships

### Category
Runbook

### Dependencies
Skills that enhance this skill (none are hard blockers — all are optional integrations):
- `grill-me` — fog discovery at Step 1 (optional, user-driven)
- `content-research` — deep URL ingestion at Step 3 (optional, surfaces when URLs are found)
- `graphify` — post-session knowledge graph (optional, offered after Step 5)
- GBrain MCP — persistent recall and write-back (graceful skip if unavailable)

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `grill-me` | Sequential upstream (optional) | Mode B (fog) + user chooses full interview | `brainstorms/{date}-{slug}.md` — `Topic string:` and `Entities:` lines extracted for Step 1/2 |
| `content-research` | Sequential downstream (optional) | URLs found during Step 3 verification | URL list from `## Source URLs` in session file passed to `/content-research <url>` |
| `graphify` | Sequential downstream (optional) | offered after Step 5 context push | `$SECOND_BRAIN_DIR/Learning/{date}-{slug}.md` — session file with `## Knowledge Map` section |
| `sandbox_runner.py` | Prerequisite / Gate | must be checked at session start before Step 1 | `~/.claude/skills/learn-anything/scripts/sandbox_runner.py --check` → `SANDBOX_AVAILABLE` |

### Runtime Preamble

At invocation, surface prior context and available integrations:

- "Checking GBrain for prior work on this topic..." (run recall silently; surface result if found)
- "If your topic is large and multi-faceted, I can run `/grill-me` to do a full discovery interview first — it saves to a brainstorm file so nothing is lost."
- "After the session, I'll offer to run `/graphify` on your Learning folder to update your knowledge graph, and `/content-research` on any URLs we find."

---

## Gotchas

- **Sandbox check must run before Step 1, not at Step 5:** `SANDBOX_AVAILABLE` affects the Step 5 test loop path. Running the check late means the user reaches Step 5 without knowing whether Docker is available, which breaks the flow at the worst moment.
- **grill-me handoff is `Topic string:` extraction, not free-form reading:** Read the brainstorm file and extract the exact `Topic string:` line. Do not infer the topic from the whole file — the line is the canonical specific gap.
- **Never re-teach what the prior session file already has:** Read `## What I Now Know` from the most recent session file before Step 2. If it's already covered, skip it and build on it.
- **content-research handles the full ingest chain:** Do not manually write Obsidian notes or run graphify on URLs. Invoke `/content-research <url>` — it does ingest → Obsidian → graphify automatically. The session file `## Source URLs` is the handoff list.
- **GBrain write-back uses the `learning/` slug convention:** The page slug must be `learning/{topic-slug}` — not the topic string directly. Slug mismatch breaks cross-session recall because GBrain won't find the page on semantic search.
- **Do not skip the session file write:** The session file is the fallback for every downstream skill (graphify, content-research URL list) when GBrain is unavailable. Write it even if the session was short.
