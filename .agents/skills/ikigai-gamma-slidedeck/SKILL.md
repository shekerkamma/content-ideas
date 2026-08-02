---
name: ikigai-gamma-slidedeck
description: >
  Use when the user asks for an "ikigai slide deck", "LinkedIn to slides", or
  a combined LinkedIn profile → Ikigai Pro report → presentation pipeline.
  Uses Gamma when available with a branded-pptx-deck fallback.
  One command, fully automated. Reusable for any person.
  Primary path: Gamma MCP (gammaUrl returned).
  Fallback path: branded pptxkit build_deck.py with validated local delivery.
metadata:
  triggers:
    - ikigai-gamma-slidedeck
    - ikigai slide deck
    - linkedin ikigai slides
    - linkedin to slides
    - ikigai deck
  version: "1.2"
  validated_on:
    - "runs/2026-06-13-shravan-ikigai-genspark (individual-first framing)"
    - "runs/2026-06-16-srikumar-ikigai (BD/company-first framing, 26 slides, pptxkit path)"
---

# ikigai-gamma-slidedeck

Compound skill: LinkedIn profile → full Ikigai Pro report → slide deck.

## When To Use

- User says "run ikigai for <name>" or "ikigai slide deck for <name>"
- User provides a LinkedIn profile source (PDF path, URL, or pasted text)
- User wants both the written report AND a slide deck in one pipeline run

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| `profile_source` | Yes | PDF path (Windows `C:\…` or WSL `/mnt/c/…`), LinkedIn URL, or pasted text |
| `person_name` | Yes | Full name or slug; used for the run folder |
| `context` | Optional | Extra framing (industry focus, BD vs founder, languages, etc.) |

## Outputs

All artifacts land in `runs/YYYY-MM-DD-<name>-ikigai/`:

| File | Description |
|---|---|
| `<name>-ikigai-report.md` | Full 7-section ikigai report |
| `build_deck.py` | Parameterized pptxkit builder (always generated — enables offline rebuild) |
| `<name>-ikigai-deck-draft.pptx` | pptxkit-built deck (fallback path, or always if Gamma unavailable) |
| `_preview/contact_*.png` | QA contact sheets (pptxkit path only) |
| `run-log.md` | Run log with delivery status, deck URL or configured delivery path, deck structure |

Gamma path additionally returns a `gammaUrl` shared with the user.

---

## Pipeline Overview

```
Profile Source
      │
      ▼
[Stage 1] Ingest + Ikigai Analysis    ← ikigai SKILL.md stages 1–7
      │
      ▼ report.md + key data extracted
      │
      ├──► [Stage 2A] Gamma Deck         if mcp__claude_ai_Gamma__generate available
      │         └── gammaUrl → user
      │
      └──► [Stage 2B] pptxkit Deck       fallback (terminal host / Gamma unavailable)
                └── .pptx + preview → run folder / configured delivery directory
      │
      ▼
[Stage 3] GCC Roadmap Deck (OPTIONAL)  ← BD/company-first mode only
      │    If user confirms, invoke gcc-roadmap skill:
      │    → reads ikigai report for company/platform/tier data
      │    → generates 17-slide time × capability roadmap deck
      │    → validates + QA previews + delivers to the configured destination
      │
      ▼
[Stage 4] Run Log + Delivery
```

---

## Stage 1 — Ikigai Analysis

Execute stages 1–7 from `.agents/skills/ikigai/SKILL.md` in full.

**Key extractions to carry forward into the deck:**
After completing the report, pull these values for deck parameterisation:

```
PERSON_NAME        Full name
PERSON_ROLE        Current title and company (e.g. "Director Strategic BD, FPT Software")
TAGLINE            One-line position summary
VALIDATION_SCORE   Composite /100 (e.g. 88)
VALIDATION_LABEL   EXCEPTIONAL / STRONG GO / VIABLE
NICHE_LAYER1       Market (broad segment)
NICHE_LAYER2       Niche (specific sub-segment)
NICHE_LAYER3       Problem (exact gap)
ONE_LINER          The killer positioning sentence
OFFER_TIER1        Name · price · what's included · ideal client
OFFER_TIER2        Name · price · what's included · ideal client (★ recommended)
OFFER_TIER3        Name · price · what's included · ideal client
MILESTONE_1        Phase 1 · timeline · revenue target · milestone
MILESTONE_2        Phase 2 · timeline · revenue target · milestone
MILESTONE_3        Phase 3 · timeline · revenue target · milestone
MILESTONE_4        Phase 4 · timeline · revenue target · milestone
KEY_LOVES          6 bullets
KEY_GOODAT         6 bullets
COMPETITOR_ROWS    5 rows: Competitor | Positioning | Falls Short
```

For BD/company roles also extract:
```
COMPANY_NAME       e.g. "FPT Software"
COMPANY_CAPABILITIES  List of products/platforms
COMPANY_PROOFPOINTS   Metrics (client count, deal sizes, etc.)
```

---

## Stage 2A — Gamma Deck (Primary Path)

Use when `mcp__claude_ai_Gamma__generate` is available in the host.

### Step 1 — Get a professional dark theme

```
mcp__claude_ai_Gamma__get_themes()
```

Pick a theme whose tone/color keywords include: professional, dark, navy, corporate,
executive, midnight, or similar. Prefer a theme without decorative stock photos.
Note the `themeId`.

If no good match → omit `themeId` and let Gamma default.

### Step 2 — Build the inputText

Construct the Gamma outline from the ikigai report. See `gamma-outline.md` in this
skill folder for the full template. Substitute report values into the template.

Rules for the inputText:
- Use `---` separators between every slide (required for `cardSplit: "inputTextBreaks"`)
- Each slide = `## Slide Title` + bullet points or short paragraphs
- No slide should have more than 6 bullet points
- Include explicit stat figures for proof-point slides (credibility)
- The One-Liner slide should have the full sentence in quotes and attribution
- The closing slide should have three clear columns of content

### Step 3 — Call Gamma generate

```python
mcp__claude_ai_Gamma__generate(
    title=f"{PERSON_NAME} — Ikigai Pro Report",
    inputText=<outline from gamma-outline.md with substitutions>,
    numCards=26,
    textMode="preserve",       # content is pre-written — don't rewrite
    cardSplit="inputTextBreaks",  # honor --- as slide boundaries
    themeId=<from step 1 or omit>,
    cardOptions={"dimensions": "16x9"},
    imageOptions={"source": "noImages"},  # business deck — no AI imagery
    textOptions={
        "audience": "executives",
        "tone": "professional",
        "amount": "detailed"
    },
    exportAs="pptx"            # also offer the pptx download link
)
```

The tool returns immediately with a `generationId` and `gammaUrl`.
Share the `gammaUrl` with the user. Do not call `get_generation_status` unless
the user explicitly asks for a status check.

### Step 4 — Log to run-log.md

Record:
- `gammaUrl`
- `themeId` used (or "default")
- `exportUrl` if available (pptx download — expires ~1 week)
- Slide count
- Delivery status: `gamma-generated`

---

## Stage 2B — Branded PPTX Deck (Fallback Path)

Use when:
- `mcp__claude_ai_Gamma__generate` is NOT available (terminal / CLI host)
- Gamma returns an error or is blocked
- User explicitly requests a .pptx file instead of Gamma

### Step 1 — Generate build_deck.py

Create `runs/YYYY-MM-DD-<name>-ikigai/build_deck.py` by substituting extracted
report values into `build_deck_template.py` (in this skill folder).

The template defines slide sections; substitute:
- All `{{VAR}}` placeholders with extracted report values
- Person-specific bullets, tables, proof points from the report

For BD/company roles, include the proof-point slides (slides 7–12 in the Srikumar
validated run):
- Company scale KPIs
- Company AI credentials / partnerships
- Client testimonials (5 rows)
- 2× use-case realization slides (dark navy layout)
- Person BD proof points (patent, grants, ventures, scale)

For solo founder / individual roles, replace company slides with:
- Portfolio / past ventures deep-dive
- Specific client case studies or testimonials if available
- Skills + certifications breakdown

### Step 2 — Run the builder

Run `python3 runs/YYYY-MM-DD-<name>-ikigai/build_deck.py` from the repository
root.

Verify: output line must say `[validated]` — pptxkit's built-in XML check.
If it fails, fix the script and rerun.

### Step 3 — QA preview

```python
import sys; from pathlib import Path
sys.path.insert(0, "<resolved-branded-pptx-deck-dir>/scripts")
import preview_pptx
preview_pptx.render(
    "runs/YYYY-MM-DD-<name>-ikigai/<name>-ikigai-deck-draft.pptx",
    Path("runs/YYYY-MM-DD-<name>-ikigai/_preview")
)
```

Read all contact sheets. Check:
- No red overflow boxes on any slide
- No title/subtitle collisions
- Footer present on every slide
- Stat bars, callout strips, side panels — text not clipped

Fix any issues in `build_deck.py`, rerun, re-preview.

### Step 4 — Deliver

Keep the deck and reproducible builder in the run folder. After visual QA,
rename the deck with a `-reviewed.pptx` suffix. If `$CLIENT_DELIVERY_DIR` is
configured, copy that reviewed file there. Otherwise report the run-folder path
and do not invent a Desktop destination.

---

## Stage 3 — GCC Implementation Roadmap (Optional, BD/company-first only)

After the positioning deck is delivered, if the person's role is BD/sales at a tech
company (company-first framing), ask the user:

> "Want me to also generate the GCC Implementation Roadmap deck — shows the full
> 18-month delivery journey (Sprint → Transformation → Partnership × Modernize /
> Activate / Innovate)? It's 17 slides and uses the company platform data from the
> ikigai report."

If the user confirms:

1. Read `<name>-ikigai-report.md` to extract:
   - `COMPANY_NAME`, `BD_PERSON_NAME`, `BD_PERSON_ROLE`
   - Platform capabilities (map to MODERNIZE / ACTIVATE / INNOVATE layers)
   - Offer tiers (Sprint, Transformation, Partnership names and prices)
   - Proof points (deal sizes, client count, key metrics)

2. Invoke the gcc-roadmap skill:
   ```
   Skill(skill="gcc-roadmap", args="chain from <name>-ikigai-report.md")
   ```

3. The skill will generate `<name>-gcc-roadmap-deck-draft.pptx` in the same
   run folder (or a new run folder if chaining), then copy it to
   `$CLIENT_DELIVERY_DIR` only when configured.

4. Update `run-log.md` to record both decks and their delivery status.

If the user declines or the person is a solo founder / individual: skip Stage 3.

---

## Stage 4 — Run Log

Write `runs/YYYY-MM-DD-<name>-ikigai/run-log.md`:

```markdown
# <PERSON_NAME> Ikigai — Run Log

Status: `<gamma-generated | reviewed | draft>`

## Source
- Profile: <profile_source>
- Report: <name>-ikigai-report.md

## Deck Output
### Gamma path (if used)
- gammaUrl: <url>
- exportUrl: <pptx download url>
- Theme: <themeId or "default">

### pptxkit path (if used)
- PPTX: <name>-ikigai-deck-draft.pptx
- Delivery: <CLIENT_DELIVERY_DIR path, or "run folder only">
- Builder: build_deck.py
- Preview: _preview/contact_*.png

## Slide Count
<N> slides

## Framing
<BD/company-first | individual-first> — <brief reason>

## Validation Score
<score>/100 <label>

## Stage 3 — GCC Roadmap
<generated | skipped — <reason>>
- PPTX: <name>-gcc-roadmap-deck-draft.pptx (if generated)
- Delivery: <CLIENT_DELIVERY_DIR path, or "run folder only"> (if generated)
```

---

## Framing Rule (inherited from ikigai skill)

**BD / partnerships / sales role at a tech company →**
Frame around the **company's capabilities**. Person = trusted door-opener.
Offer architecture = company engagement tiers, not personal consulting rates.
Include proof-point slides: company scale, AI credentials, client voices, use cases.

**Solo founder / independent consultant →**
Frame around the **individual**. Person = the product.
Use personal offer tiers, personal case studies, personal proof points.

---

## Do Not

- Generate the deck before completing all 7 stages of the ikigai report
- Use Gamma `textMode: "generate"` or `"condense"` — this rewrites the pre-written content; always use `"preserve"`
- Omit `cardSplit: "inputTextBreaks"` when the outline has `---` separators
- Choose a Gamma theme with heavy stock photography for a business/strategy deck
- Skip the pptxkit `validate_pptx()` check (it's built into `Deck.save()`)
- Overwrite a file open in PowerPoint — use a new name with a version suffix
- Mark delivery status as `reviewed` without actually reading the contact sheets

---

## Success Criteria

- All 7 ikigai stages completed; report file exists
- Deck delivered via Gamma URL (primary) or reviewed local `.pptx` (fallback)
- `run-log.md` updated with delivery status
- `build_deck.py` present in the run folder regardless of which path was taken
  (enables offline rebuild / client-specific modification at any time)
- Every slide has explicit evidence: no claims without a source from the report

---

## Resources

- Ikigai analysis skill: sibling `ikigai` skill
- Gamma outline template: `gamma-outline.md` beside this file
- pptxkit fallback template: `build_deck_template.py` beside this file
- Stage 3 gcc-roadmap skill: sibling `gcc-roadmap` skill
- Validated BD run (ikigai deck): `~/content-ideas/runs/2026-06-16-srikumar-ikigai/` (26 slides, pptxkit path)
- Validated BD run (roadmap deck): `~/content-ideas/runs/2026-06-16-gcc-implementation-roadmap/` (17 slides)
- Validated founder run: `~/content-ideas/runs/2026-06-13-shravan-ikigai-genspark/`
- pptxkit API and brand palette: resolve the installed
  `branded-pptx-deck` skill; block branded output if unavailable

## Skill Relationships

### Category
Business Automation

### Dependencies
- `ikigai` — required upstream analysis.
- Gamma or `branded-pptx-deck` — at least one presentation path must be available.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `ikigai` | Sequential upstream | every run | `runs/.../<name>-ikigai-report.md` |
| `gcc-roadmap` | Sequential downstream | optional BD/company-first Stage 3 | company capabilities, tiers, and proof points |
| `branded-pptx-deck` | Fallback | Gamma unavailable or local PPTX requested | reviewed `.pptx`, builder, and previews |

### Runtime Preamble
State which presentation path is available, the framing mode, and whether the
result can be reviewed or must be marked draft/blocked.

## Gotchas

- Never start the deck before the full ikigai report is complete.
- Never call a local PPTX reviewed without inspecting the rendered previews.
- Never invent a Desktop delivery path; use `$CLIENT_DELIVERY_DIR` when configured.
