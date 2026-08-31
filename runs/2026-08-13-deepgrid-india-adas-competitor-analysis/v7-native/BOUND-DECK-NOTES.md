# Prompt templates → bound content: build and QA record

Two artifacts, in order. The first defines the structure; the second is generated
under it.

| # | Artifact | Slides | Status |
|---|---|---:|---|
| 1 | `DeepGrid-India-ADAS-Prompt-Templates-reviewed.pptx` | 9 | reviewed |
| 2 | `DeepGrid-India-ADAS-Competitor-Dossier-Bound-reviewed.pptx` | 74 | reviewed |

## 1 · The adapted prompt-template deck

Replicates the supplied guide's page architecture measured shape-by-shape, not
approximated: domain chip `62,24,442,27` · title `62,56` · WHEN TO USE and
WORKFLOW in the left column · **KEY PROMPT box `586,142,653,254`** · OUTPUT
INCLUDES `586,408` in two columns of three · Calibri throughout.

The seven patterns are **adapted, not inherited**. Each exists because all 73
dossier slides were profiled and that structure was found in them:

| Pattern | Slides | Distinguishing envelope field | Exhibit |
|---|---:|---|---|
| P1 Evidence Ladder | 21 | `rungs[].confidence` | rung width = confidence |
| P2 Threat × Arena | 11 | `matrix.cells[].rating` | bar length = rating |
| P3 Staged Move | 18 | `stages[].reversible` | numbered chain, arrows |
| P4 Bounded Argument | 18 | `positions[].stance` | three stances, none softened |
| P5 Dated Plan | 2 | `phases[].span_weeks` | rail, spans to scale |
| P6 Cost Bridge | 1 | `steps[].value` + `verified` | waterfall, height = magnitude |
| P7 Confidence Register | 2 | `claims[].importance × evidence` | scored dot register |

**One deliberate departure from the guide.** Its own palette fails WCAG AA:
`#00C9A7` on white is 2.12:1 and `#009B82` on its chip is 3.12:1 — 54 findings
when replicated verbatim. The layout, grammar and identity are kept exactly; text
takes `#00755F` (5.66:1) and `#00695C` (5.90:1), while `#00C9A7` stays on fills
and rules, which carry no text-contrast requirement.

## 2 · The content deck, bound to those templates

`src/bind_envelopes.py` projects each slide's extracted evidence into the typed
envelope its pattern declares, then validates it against that pattern's stated
rules. **73 of 73 bound to their intended pattern; zero fallbacks.**

Two rules were wrong on the first pass and were corrected against the evidence,
not around it:

- P2 required ≥2 rating rows. One competitor rated across three arenas is a valid
  P2 exhibit — that is literally its WHEN TO USE. Slides 22/50/52 recovered.
- Slide 57 was mapped to the cost bridge but carries a status-graded positioning
  map with no costed steps. Re-mapped to P7.

A slide that cannot satisfy its pattern is never forced; it falls back to P4,
whose own WHEN TO USE is "no structured evidence exists — the reasoning is the
exhibit", and the reason is recorded in `bound-envelopes.json`.

### Defects found by rendering and fixed

| Defect | Cause | Fix |
|---|---|---|
| ~250px dead space per page | no slack distribution | leftover height grows the exhibit rows, not the gaps (`grow` param) |
| Heatmap columns showed a cell value as an arena | arena scan read both `label` and `text` of one block | one candidate per block; an arena name can never also be a row |
| Rail phases labelled "2 — Evidence Reset" | split on the first hyphen, inside "Weeks 1-2" | split on the em/en dash only |
| Chain nodes numbered "01  1 · POSITION" | source enumerator kept | strip the leading `N ·` |
| Ladder gap repeated the weakest rung verbatim | no dedupe | suppress the gap line when identical |
| P6 drew unverified magnitudes with no caveat | rule stated in the template, not implemented | caveat printed whenever any step is `verified: false` |

Dead space after the fix: **mean 22px, max 104px** (measured on all 73 renders).

### Alignment check, before building anything on it

Titles looked misaligned against their kickers (slide 42 is titled FPGA→ASIC cost
while its kicker reads "COMPETITOR 8/10"). Measured across all 73 by token
overlap: offset 0 scores 0.573, offset +1 scores 0.266, offset −1 scores 0.296.
**There is no index shift** — the kicker is a section label that lags the content
in the source deck. Six slides mismatch locally and are listed in
`qa/bound-layout-stats.json`.

## QA gates

| Gate | Template deck | Content deck |
|---|---|---|
| `lint_pptx.py` errors | 0 | 0 |
| `TEXT_LOW_CONTRAST` | 0 (was 54) | 0 (was 9) |
| `TEXT_OVERFLOW_RISK` | 4 | 134 (previous build: 185) |
| OpenXML validation | passed | passed |
| OfficeCLI issues | 0 | 0 |
| Rendered + inspected | 9/9 | 74/74 |
| `validate_run.py --competitor --reviewed` | — | pass |

`SLIDE_MISSING_TITLE` and `DECK_COLOR_COUNT` are pre-existing characteristics of
this builder family — identical counts on the previously reviewed v7Story deck —
not regressions.

**Not run:** the native Microsoft PowerPoint render (`--native-windows`). Both
decks are reviewed against HTML contact sheets and PNG renders only.

## Reproduce

```bash
python3 src/bind_envelopes.py
DECK_RUN=. DECK_NAME=india-adas-prompt-templates DECK_RENDER=1 node src/build_template_deck.mjs
DECK_RUN=. DECK_NAME=DeepGrid-India-ADAS-Competitor-Dossier-Bound DECK_RENDER=1 node src/build_bound_deck.mjs
```

---

# Round 2 · storyboard + visual story assets + live research

`DeepGrid-India-ADAS-Competitor-Dossier-Story-reviewed.pptx` — 83 slides.
Applies `/narrative-builder` (Pyramid Principle + SCQA) over the 73 bound pages.

## The defect the storyboard fixes

The source order split every competitor across four separate blocks — Gahan's
evidence at slide 20, its threat map at 22, our move at 21, its falsifier at 59.
No competitor was ever argued in one place. `src/build_narrative.py` regroups
into five acts, and inside Act III each rival now runs
**evidence → threat by arena → our move → the falsifier**.

| Act | Pages | Question it answers |
|---|---:|---|
| I · The verdict | 4 | What should DeepGrid do, before any of the evidence? |
| II · The field | 7 | Who occupies India CV ADAS, and what does each arena reward? |
| III · The contest | 44 | Per rival: what is proven, where are they strong, what would change it? |
| IV · The wedge | 12 | What exactly does DeepGrid sell, and why would an integrator embed it? |
| V · The plan | 6 | What must be true in 90 days, and who owns each gate? |

## Visual story assets added

- **Storyboard on a page** — SCQA strip over act bands drawn *to scale*, so the
  reader sees Act III is 60% of the deck before reading a word.
- **Pyramid** — governing thought over three supports, each with what it rests on
  and where it is proved.
- **Evidence delta** — what live research changed, with the primary artifact
  embedded beside it.
- **Five act dividers** — each carries the act's question and what it settles.
- **Hostile questions** — the six a skeptical board actually asks, answered on
  the page rather than in an appendix.

## Live research · You.com livecrawl → Exa → Firecrawl

Nine queries aimed at the gaps the dossier itself names. **162 results, 114
dated, 7/7 primary artifacts captured.** Raw output in `research/`.

**The finding that changes the map:** Aptiv's Gen 6 smart camera features
**STRADVISION's** AI-based vision technology (Aptiv PLC, 6 Jan 2026). They are not
separate rivals — one is embedded in the other. The bounded-perception-layer
thesis is proven by a competitor, and STRADVISION already occupies the exact slot
DeepGrid is bidding for.

| Delta | Was | Now | Move |
|---|---|---|---|
| ZF | specifics need corroboration | India E-Mobility CV OEM nomination, 16 features, 300,000 km validated, ARAI certified, GSR 184e (ZF, 3 Dec 2025) | corroborated, hold HIGH |
| STRADVISION | India CV not established | global CV OEM selected SVNet for its India lineup (16 Apr 2026) | insufficient → **verified** |
| drivebuddyAI | $2.5m / 3,000 trucks | +$5.3m for 3,600 electric buses and trucks incl. mining (23 Jun 2026) | raise; mining now contested |
| Regulatory | "rebase to 2027–28" | instrument is **GSR 184e**; Aptiv cites 2027; draft AIS-162 covers M2/M3/N2/N3 | corroborated; gazette outstanding |
| Gahan | needs profiling | two engines, livecrawl, 18 results, **zero primary sources** | lower priority — a measured absence |
| Sterling×MINIEYE | exchange-filed Jan 2026 | confirmed ×4 outlets; MINIEYE is HK-listed/China-based | hold; falsifier unfired |
| bitsensing / Netrasemi | attributed | $25m Series B confirmed; Netrasemi A2000 targets mid-2027 | hold; add dated re-test |

**Why source screenshots rather than competitor marketing images.** The
visual-sourcing rule routes exact-state evidence to EXTRACT. A capture of Aptiv's
own press release *is* the evidence; a competitor's product render is decoration
that would imply proof it does not carry. 193 image candidates were harvested and
catalogued in `research/findings.json`; none were used as evidence.

## QA

| Gate | Result |
|---|---|
| `lint_pptx.py` errors | 0 |
| `TEXT_LOW_CONTRAST` | 0 |
| `TEXT_BOX_OVERLAP` | 0 |
| OpenXML validation | passed |
| OfficeCLI issues | 0 |
| `validate_run.py --competitor --reviewed` | pass |
| Rendered + inspected | 83/83 |
| **Native Microsoft PowerPoint render** | **passed — all 83 inspected** |

### Native render: why it was "not run", and what it caught

It was never blocked. Windows OfficeCLI, PowerShell and PowerPoint 2016 were all
present the whole time — the flag simply was not passed. The first attempt then
failed with *"--render native requires Windows with Microsoft PowerPoint
installed"*, which is misleading: PowerPoint COM was fine (verified: version
16.0). The real cause was that **PowerPoint was already running**, holding the
deck opened for review, and COM automation cannot drive a busy interactive
instance. Closing it made the native path work first time.

That render then caught a defect both the HTML gate and the PNG renders missed:
the **decision band's stop/escalate line wrapped to a second line and printed
past the band, under the footer**. `officecli issues` reported 0 because the text
stayed inside the slide, and the artifact-tool PNG hid it because its text metrics
are narrower than PowerPoint's. Fixed by rebuilding the band as three real columns
(Decision · Owner-trigger · Stop/escalate) at 80px. `TEXT_OVERFLOW_RISK` fell
from 146 to 17 as a side effect.

**Operating note:** close PowerPoint before running `--native-windows`, or the
render fails with a message that blames the installation. Office reports as
"Unlicensed Product" on this machine; COM render still works.

Two further defects were found by rendering and fixed: Act V's purple read 4.42:1 as text
on the dark card (bars keep the saturated colour, text takes a separate AA ramp),
and the delta page's hero claim was given a fixed 44px box that a three-line
claim overran into the text below it.

**Not run:** native Microsoft PowerPoint render (`--native-windows`).

## Reproduce

```bash
python3 src/bind_envelopes.py
python3 src/build_narrative.py
python3 src/research_gaps.py        # needs YOU_API_KEY + EXA_API_KEY
python3 src/capture_primary.py      # needs FIRECRAWL_API_KEY
DECK_RUN=. DECK_NAME=DeepGrid-India-ADAS-Competitor-Dossier-Story DECK_RENDER=1 \
  node src/build_bound_deck.mjs
```
