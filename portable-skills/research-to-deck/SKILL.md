---
name: research-to-deck
description: >
  Use when someone says "research X and make a deck", "research to deck",
  "kb pipeline", "research and deck it", or "pipeline this topic into slides".
  Compound pipeline: topic or URLs → research → openkb compile → synthesis →
  slide deck → QA. Chains deep-research (or content-research for URLs) →
  openkb add → openkb query → openkb-deck-neon/editorial/marp → openkb-html-critic.
  One command, fully automated. Styles: neon (default), editorial, marp (MARP Markdown → HTML/PPTX).
  For a LinkedIn profile → Ikigai report → Gamma deck pipeline, use `ikigai-gamma-slidedeck` instead.
triggers:
  - research-to-deck
  - research to deck
  - kb pipeline
  - research and make a deck
  - research X and deck it
version: "1.0"
---

# research-to-deck

Compound pipeline: research → knowledge base → slide deck.

## Narrative Frame

**This skill's job:** Turn a topic into a deck that makes the reader feel like they just got briefed by someone who spent a week on it — in one command.

**Voice for the synthesis stage:** The synthesis is not a summary. It is an argument. Lead with the one finding that changes how the reader should think about this topic. End with the one action that follows from the evidence.

**Quality gate before deck generation:** Read the synthesis and ask: "If this were the only thing someone read about this topic, would they know what to do?" If not, revise the synthesis before generating slides.

**Slide quality rules (applied to all deck outputs from this pipeline):**
- Title slide subtitle = the single most important number or claim in the entire research
- Every slide title is a verdict, not a label
- The closing slide is the next action — one bold claim + one move
- Apply `~/.claude/skills/voice.md` in full during all slide writing stages

## When To Use

- User says "research X and make a deck"
- User says "/research-to-deck <topic>"
- User wants to go from raw topic or URLs to a compiled KB + polished HTML deck
- User mentions "kb pipeline" or "research pipeline"

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| `topic` | Yes (or URLs) | Research topic string, OR one or more URLs |
| `style` | Optional | `neon` (default), `editorial`, or `marp` |
| `kb_dir` | Optional | Path to openkb KB directory. Auto-detected via `openkb status` if omitted |
| `pptx` | Optional | Flag: also export to .pptx (branded-pptx-deck for neon/editorial; Marp CLI for marp) |

Parse from the user's message:
- URLs (starting with `http`) → Stage 1 uses `/content-research`
- Everything else → Stage 1 uses `/deep-research`
- `--style editorial` or "editorial" / "warm" / "serif" in message → editorial deck
- `--style neon` or "neon" / "dark" / "tech" (default) → neon deck
- `--style marp` or "marp" / "markdown slides" / "marp slides" → MARP deck
- `--pptx` → run Stage 6 after QA (or after Stage 4 for marp)

## Outputs

All artifacts land in `runs/YYYY-MM-DD-<slug>-research-deck/`:

| File | Style | Description |
|---|---|---|
| `<slug>-research.md` | all | Research brief (input to openkb) |
| `<slug>-synthesis.md` | all | openkb query synthesis (key insights) |
| `<slug>-deck.html` | neon/editorial | Final QA'd Aurora Glass or editorial HTML deck |
| `<slug>-deck.md` | marp | MARP Markdown source (editable) |
| `<slug>-deck.html` | marp | Marp-rendered self-contained HTML deck |
| `<slug>-deck.pptx` | optional | Branded PPTX (neon/editorial) or Marp PPTX (marp) |
| `run-log.md` | all | Stage-by-stage status, KB path, deck path |

---

## Pipeline

```
Input: topic string  OR  URLs
        │
        ▼
[Stage 1] Research
  topic  → /deep-research        writes <slug>-research.md
  URLs   → /content-research     writes <slug>-research.md
        │
        ▼ <slug>-research.md
        │
[Stage 2] KB Compile
  openkb add <slug>-research.md  (auto-detects or creates KB)
  reports: N concepts, M entities compiled
        │
        ▼ compiled wiki/ updated
        │
[Stage 3] Synthesis
  openkb query  (3–5 targeted questions derived from the topic)
  save synthesis to <slug>-synthesis.md
        │
        ▼ synthesis.md
        │
[Stage 4] Deck Generation
  style=neon      → /openkb-deck-neon
                    deck to output/decks/<slug>/index.html
                    copy to run folder as <slug>-deck-draft.html
  style=editorial → /openkb-deck-editorial  (same flow)
  style=marp      → /marp  (--file <slug>-synthesis.md --style neon --format html)
                    writes <slug>-deck.md + <slug>-deck.html to run folder
                    ── skips Stage 5 QA (marp output is self-contained) ──
        │
        ▼
[Stage 5] QA  (neon/editorial only — skipped for marp)
  /openkb-html-critic  patches visual bugs, overflow, nav
  saves final as <slug>-deck.html
        │
        ▼
[Stage 6] PPTX Export (optional, --pptx flag)
  neon/editorial → /branded-pptx-deck  from synthesis.md outline
  marp           → Marp CLI  ~/.local/node_modules/.bin/marp <slug>-deck.md --pptx
  saves <slug>-deck.pptx
        │
        ▼
[Stage 7] Run Log
  write run-log.md with stage status, KB path, output paths
  print delivery summary to user
```

---

## Execution Instructions

### Pre-flight

1. Parse the user's input to extract `topic_or_urls`, `style`, `kb_dir`, `pptx_flag`.
2. Generate `slug`: lowercase, kebab-case from topic (max 5 words). Example: "OpenKB retrieval as compilation" → `openkb-retrieval-compilation`.
3. Generate `run_dir`: `runs/YYYY-MM-DD-<slug>-research-deck/` relative to cwd.
4. Create `run_dir`.
5. Detect KB:
   - If `kb_dir` provided: use it.
   - Else: run `openkb status` in cwd. If a KB is found, use it.
   - Else: default to `~/Documents/Knowledge`. Create with `openkb init` if it doesn't exist (write `.openkb/config.yaml` with `model: gemini/gemini-2.5-flash` and `.env` with `LLM_API_KEY` from env).
6. Print stage plan to user before executing:
   ```
   Pipeline: research-to-deck
   Topic:    <topic>
   Style:    <neon|editorial|marp>
   KB:       <kb_path>  (marp: KB still compiled; synthesis used as deck source)
   Run dir:  <run_dir>
   Stages:   1-Research → 2-Compile → 3-Synthesize → 4-Deck [→ 5-QA] [→ 6-PPTX]
             (Stage 5 QA skipped for marp style)
   ```

### Stage 1 — Research

**If input is URLs:**
- Invoke Skill: `content-research` with the URLs
- After completion, locate the generated notes (usually in `$SECOND_BRAIN_DIR/raw/` or `~/Documents/Content/research/`)
- Copy/consolidate relevant output to `<run_dir>/<slug>-research.md`

**If input is a topic:**
- Invoke Skill: `deep-research` with the topic
- After the research brief is produced in the conversation, write it to `<run_dir>/<slug>-research.md`
- Include: title, executive summary, key findings (min 5), sources cited, open questions

The research file MUST be self-contained markdown — no external dependencies.

### Stage 2 — KB Compile

```bash
cd <kb_dir>
LITELLM_DROP_PARAMS=True openkb add <run_dir>/<slug>-research.md
```

- Report compiled counts: `N concepts, M entities added`.
- If compile fails: stop and report error. Do not proceed to Stage 3.
- On success: note the KB wiki path for Stage 3 and 4.

### Stage 3 — Synthesis

Derive 4–5 targeted questions from the topic. Example for "OpenKB as compilation":
- "What is the core innovation in the compilation approach?"
- "How does this compare to traditional RAG?"
- "What are the key benefits for developers?"
- "What entities or tools are central to this approach?"

Run each as:
```bash
cd <kb_dir>
openkb query "<question>"
```

Consolidate all answers into `<run_dir>/<slug>-synthesis.md` with clear sections per question. This becomes the source of truth for the deck narrative.

### Stage 4 — Deck Generation

**If style = neon or editorial:**

Navigate to the KB directory (deck skills write output relative to KB):
```
cd <kb_dir>
```

- **neon:** Invoke Skill: `openkb-deck-neon`
  - Instruct it: "Make a deck about <topic>. Use the synthesis from `<slug>-synthesis.md` as the narrative source. Slug: `<slug>`."
- **editorial:** Invoke Skill: `openkb-deck-editorial`
  - Same instruction.

After deck is written to `<kb_dir>/output/decks/<slug>/index.html`:
- Copy to `<run_dir>/<slug>-deck-draft.html`
- Proceed to Stage 5 (QA).

**If style = marp:**

Invoke Skill: `marp` with:
- `--file <run_dir>/<slug>-synthesis.md`
- `--style neon`
- `--format html`
- `--slug <slug>-deck`
- `--out <run_dir>`

The marp skill will write `<run_dir>/<slug>-deck.md` (source) and `<run_dir>/<slug>-deck.html` (export).

**Skip Stage 5** — marp output is self-contained HTML; no HTML critic pass needed.
Proceed directly to Stage 6 (if `--pptx`) or Stage 7.

### Stage 5 — QA  (neon/editorial only)

**Skip this stage entirely if style = marp.**

Invoke Skill: `openkb-html-critic` on `<run_dir>/<slug>-deck-draft.html`
- It patches in-place: visual bugs, overflow, nav, CSS specificity issues.
- After QA: copy/rename to `<run_dir>/<slug>-deck.html` (the final deliverable).

### Stage 6 — PPTX Export (conditional)

Only if `pptx_flag = true`.

**If style = neon or editorial:**
- Invoke Skill: `branded-pptx-deck`
- Source: `<run_dir>/<slug>-synthesis.md` as outline
- Output: `<run_dir>/<slug>-deck.pptx`

**If style = marp:**
- Run Marp CLI directly:
  ```bash
  MARP=~/.local/node_modules/.bin/marp
  $MARP <run_dir>/<slug>-deck.md --pptx --output <run_dir>/<slug>-deck.pptx
  ```
- Requires Chromium; if browser not found, report and skip PPTX.

### Stage 7 — Run Log

Write `<run_dir>/run-log.md`:

```markdown
# research-to-deck run log
date: <ISO date>
topic: <topic>
style: <neon|editorial|marp>
kb: <kb_path>

## Stage results
- Stage 1 Research:  ✓ <slug>-research.md (<word count> words, <N> sources)
- Stage 2 Compile:   ✓ <N> concepts, <M> entities
- Stage 3 Synthesis: ✓ <slug>-synthesis.md (<N> questions answered)
- Stage 4 Deck:      ✓ <N> slides, style=<neon|editorial|marp>
- Stage 5 QA:        ✓ <slug>-deck.html (patched: <issues fixed>) | skipped (marp)
- Stage 6 PPTX:      [skipped | ✓ <slug>-deck.pptx]

## Deliverables
- Research brief: <run_dir>/<slug>-research.md
- Synthesis:      <run_dir>/<slug>-synthesis.md
- Deck source:    <run_dir>/<slug>-deck.md    (marp only)
- Deck (final):   <run_dir>/<slug>-deck.html
- PPTX:           <run_dir>/<slug>-deck.pptx  (if generated)
```

Print a clean delivery summary to the user showing file paths and next steps.

---

## Error Handling

| Stage | Failure | Action |
|---|---|---|
| Stage 1 | Research skill returns nothing | Ask user to try narrower topic or provide URLs |
| Stage 2 | `openkb add` fails (API key, model) | Report compile error + KB config hint; stop |
| Stage 2 | Compile succeeds but 0 concepts | Warn; continue with synthesis using research file directly |
| Stage 3 | Query returns empty | Use research file directly as synthesis source |
| Stage 4 | neon/editorial deck skill fails | Report; offer to retry with alternate style |
| Stage 4 | marp skill fails (binary not found) | Install: `npm install --prefix ~/.local @marp-team/marp-cli` |
| Stage 5 | HTML critic finds no issues | Note "no patches needed"; still deliver as final |
| Stage 5 | Called for marp style | Skip silently — not applicable |
| Stage 6 | branded-pptx-deck blocked (no template) | Report blocked; deliver HTML deck as final |
| Stage 6 | marp pptx fails (no Chromium) | Report; deliver HTML deck only |

## KB Configuration (for auto-created KBs)

If creating a new KB at `~/Documents/Knowledge`:
```yaml
# ~/Documents/Knowledge/.openkb/config.yaml
model: gemini/gemini-2.5-flash
long_doc_page_threshold: 20
```
```
# ~/Documents/Knowledge/.env
LLM_API_KEY=<GOOGLE_GENERATIVE_AI_API_KEY from env>
```
Always run `openkb add` with `LITELLM_DROP_PARAMS=True` to suppress Gemini caching conflicts.

---

## Skill Relationships

### Category
Business Automation

### Dependencies
Skills that must be installed for this skill to work:
- `openkb` — KB compile and synthesis (Stage 2–3)
- `deep-research` — for topic inputs (Stage 1, topic path)
- `content-research` — for URL inputs (Stage 1, URL path)
- `openkb-deck-neon` or `openkb-deck-editorial` — deck generation (Stage 4, neon/editorial)
- `marp` — deck generation (Stage 4, marp style)
- `openkb-html-critic` — QA (Stage 5, neon/editorial only)
- `branded-pptx-deck` — PPTX export (Stage 6, optional)

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `deep-research` | Sequential upstream (invoked) | when input is a topic string | research brief written to `<run_dir>/<slug>-research.md` |
| `content-research` | Sequential upstream (invoked) | when input is one or more URLs | ingested notes consolidated to `<run_dir>/<slug>-research.md` |
| `openkb` | Sequential (invoked) | always — Stages 2 and 3 | compiled `wiki/` tree; synthesis from `openkb query` → `<slug>-synthesis.md` |
| `openkb-deck-neon` | Sequential downstream (invoked) | style = neon (default) | `<kb_dir>/output/decks/<slug>/index.html` |
| `openkb-deck-editorial` | Sequential downstream (invoked) | style = editorial | `<kb_dir>/output/decks/<slug>/index.html` |
| `marp` | Sequential downstream (invoked) | style = marp | `<run_dir>/<slug>-deck.md` + `<slug>-deck.html` |
| `openkb-html-critic` | Sequential downstream (invoked) | after neon/editorial Stage 4 | patches `<slug>-deck-draft.html` → `<slug>-deck.html` |
| `branded-pptx-deck` | Sequential downstream (invoked) | `--pptx` flag + neon/editorial style | `<run_dir>/<slug>-deck.pptx` |
| `ikigai-gamma-slidedeck` | Alternative / Peer | same orchestration pattern, domain-specific (LinkedIn → Gamma deck) | — |

### Runtime Preamble

At invocation, confirm inputs and pipeline variant:

- "Is your input a topic string or URLs? Topic → `/deep-research`; URLs → `/content-research`."
- "Which deck style? `neon` (default dark), `editorial` (warm serif), or `marp` (Markdown-native, exports PPTX cleanly)."
- "Do you need a `.pptx`? Add `--pptx` to also run the branded-pptx-deck stage."
- "Peer alternative for LinkedIn-first decks: `/ikigai-gamma-slidedeck`."

---

## Gotchas

- **Stage 2 compile failure halts the pipeline:** If `openkb add` fails (bad API key, missing model config), do not attempt to continue to Stage 3 — synthesis has nothing to query. Fix the KB config and re-run from Stage 2.
- **Never skip the synthesis quality gate:** Before generating slides, read the synthesis and confirm: "If this were the only thing someone read, would they know what to do?" If not, revise — a weak synthesis produces an unfocused deck.
- **`LITELLM_DROP_PARAMS=True` is required for Gemini:** Without it, openkb throws a caching-param conflict on every `add` or `query` call. Always prefix both commands with it.
- **Stage 5 QA is not optional for neon/editorial:** The HTML critic catches overflow, nav, and CSS specificity bugs that make the deck unpresentable. Skip it and the deck is a draft, not a deliverable.
- **marp style skips Stage 5 entirely:** The marp skill produces self-contained HTML. Running openkb-html-critic on it would break marp's CSS. Never apply the HTML critic to marp output.
- **Slug must be stable across stages:** Generate it once in pre-flight and reuse it everywhere. Changing the slug mid-pipeline breaks file references between stages.

## Shared PPTX Visual Contract

When the requested output includes PPTX, apply the mandatory `pptx-visual-spec` overlay after
synthesis and before the selected deck-generation stage. Create and validate
`<run>/visual-spec.json`, then pass it unchanged to Marp, `branded-pptx-deck`,
`genspark-branded-deck`, or another direct builder. This orchestrator does not choose an image
provider independently of the visual spec.
