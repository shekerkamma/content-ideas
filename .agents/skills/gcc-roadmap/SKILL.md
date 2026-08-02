---
name: gcc-roadmap
description: >
  Use when the user asks for a "GCC implementation roadmap", "delivery
  roadmap", or roadmap deck from an ikigai report or company + BD-person
  context. Generates a 17-slide delivery journey:
  time-phased (Sprint → Transformation → Partnership) × capability-layered
  (Modernize → Activate → Innovate). Designed as Stage 3 of the
  ikigai-gamma-slidedeck pipeline, or standalone for any AI company selling
  to GCCs in India.
metadata:
  triggers:
    - gcc-roadmap
    - gcc implementation roadmap
    - implementation roadmap
    - delivery roadmap
    - roadmap deck
  version: "1.0"
  validated_on: "runs/2026-06-16-gcc-implementation-roadmap (FPT Software, 17 slides)"
  chained_from: "ikigai-gamma-slidedeck (Stage 3 — BD/company-first mode only)"
---

# gcc-roadmap

Generates a 17-slide GCC Implementation Roadmap deck. Can run standalone or
chain from `ikigai-gamma-slidedeck` as optional Stage 3.

## When To Use

- After `ikigai-gamma-slidedeck` completes for a BD/company-first person
- User asks for "implementation roadmap", "roadmap deck", "what happens after yes"
- User wants to show a GCC VP what the delivery journey looks like end-to-end
- Standalone: any AI company selling transformation to India GCCs

## Required Inputs

| Input | Source | Notes |
|---|---|---|
| `company_name` | ikigai report or user | e.g. "FPT Software" |
| `bd_person_name` | ikigai report or user | e.g. "Srikumar V R" |
| `bd_person_role` | ikigai report or user | e.g. "Director Strategic BD, FPT Software" |
| `company_platforms` | ikigai report cap table | List of platforms per layer |
| `engagement_tiers` | ikigai report offer arch | Sprint / Transformation / Partnership names + prices |
| `proof_points` | ikigai report | Key metrics, client names, deal sizes |

If chaining from `ikigai-gamma-slidedeck`, all inputs are already available in
`runs/YYYY-MM-DD-<name>-ikigai/<name>-ikigai-report.md`. Read that file first.

## Output

- Run folder: `runs/YYYY-MM-DD-<name>-gcc-roadmap/` (standalone)
  OR same run folder as ikigai if chaining: `runs/YYYY-MM-DD-<name>-ikigai/`
- `build_roadmap_deck.py` — parameterized builder (always generate)
- `<name>-gcc-roadmap-deck-draft.pptx` — 17-slide validated deck
- `_preview/contact_*.png` — QA contact sheets
- Optional reviewed copy under `$CLIENT_DELIVERY_DIR` when configured

---

## Workflow

### Step 1 — Extract inputs

If chaining from ikigai: read `<name>-ikigai-report.md` and extract:
- Company name, BD person name + role
- All 8 platform capability cards (for the three layers)
- Offer architecture tiers (Sprint / Transformation / Partnership names and prices)
- Proof points: client logos, deal sizes, key metrics

If standalone: ask the user for company name, platform stack, and engagement tiers.

### Step 2 — Map platforms to layers

Assign each company platform to one of three capability layers:

| Layer | Label | Contains |
|---|---|---|
| 1 | MODERNIZE | Legacy modernization, data readiness, dev tooling, assessment framework |
| 2 | ACTIVATE | Production AI platform, vertical AI, edge AI, AI testing/compliance |
| 3 | INNOVATE | Co-development, white-label modules, CxO co-design, innovation studio |

Use the ikigai report's capability table to drive this mapping.
The validated FPT mapping (reference):
- MODERNIZE: EMT, xMainframe, CodeVista, CASAN Framework, Data Platform
- ACTIVATE: FleziPT, KnowMed.ai, Virtual Factory, Edge AI Orchestrator, AI Testing Loop
- INNOVATE: DX Garage, Co-Development, White-Label Modules, CxO Quarterly Roadmap

### Step 3 — Generate build_roadmap_deck.py

Resolve this skill's directory, then use its adjacent
`build_deck_template.py` as the base.
Substitute all `{{VAR}}` placeholders with extracted values.

Key substitutions:
```
{{COMPANY_NAME}}         e.g. "FPT Software"
{{BD_PERSON_NAME}}       e.g. "Srikumar V R"
{{BD_PERSON_ROLE}}       e.g. "Director Strategic BD, FPT Software"
{{RUN_DATE}}             e.g. "Jun 2026"
{{FOOTER_TEXT}}          e.g. "FPT Software · GCC Implementation Roadmap · Jun 2026"
{{TIER1_NAME/PRICE}}     Sprint tier
{{TIER2_NAME/PRICE}}     Transformation tier
{{TIER3_NAME/PRICE}}     Partnership tier
{{LAYER1_PLATFORMS}}     list of (name, desc) for MODERNIZE — 5 items
{{LAYER2_PLATFORMS}}     list of (name, desc) for ACTIVATE — 5 items
{{LAYER3_PLATFORMS}}     list of (name, desc) for INNOVATE — 5 items
{{PROOF_POINTS}}         company scale + AI metrics + client references
{{OUT_PATH}}             absolute .pptx output path
```

### Step 4 — Run, validate, QA

```bash
python3 build_roadmap_deck.py
```

Must print `[validated]`. Then run preview:

```python
import sys; from pathlib import Path
sys.path.insert(0, "<resolved-branded-pptx-deck-dir>/scripts")
import preview_pptx
preview_pptx.render("<pptx_path>", Path("<preview_dir>"))
```

Read all contact sheets. Fix any overflow before delivering.
If the branded builder or preview tooling cannot be resolved, mark the deck
`blocked` or `draft` as appropriate; never present it as reviewed.

### Step 5 — Deliver

If `$CLIENT_DELIVERY_DIR` is configured, copy the reviewed deck there. Otherwise
leave it in the run folder and report that no external delivery destination was
configured. Never invent a machine-specific Desktop path.

---

## Slide Structure (17 slides — fixed)

| # | Slide | Layout |
|---|---|---|
| 1 | Cover — company + "GCC Implementation Roadmap" | Dark navy |
| 2 | The Promise — 18 months from mandate to production | 3 statement panels |
| 3 | Three Layers — Modernize · Activate · Innovate | 3-column cards with platform list |
| 4 | MASTER ROADMAP MATRIX — time × capability grid | Dark navy matrix (centrepiece) |
| 5 | Phase 1 — AI Readiness Sprint detail | 2-column: workstreams + deliverables |
| 6 | Phase 2 — Transformation Year 1 | Table: workstream, platform, deliverable, milestone |
| 7 | Phase 3 — Transformation Year 2 | 6 dark navy cards |
| 8 | Phase 4 — Strategic Partnership | Dark table: element, GCC value, company value |
| 9 | MODERNIZE deep dive | Table: platform, what it does, proof metric, timeline |
| 10 | ACTIVATE deep dive | 6 platform cards with proof strip |
| 11 | INNOVATE deep dive | 6 cards: co-dev, white-label, CxO, DX Garage, IP, partnership |
| 12 | GCC Ownership Milestones — what GCC owns at each stage | Table |
| 13 | Platform-to-Phase Mapping — full breadth in one view | Dense table |
| 14 | Governance & Stage Gates | Left: 4 stage gates · Right: cadence table |
| 15 | Commercial Arc — revenue progression + proof | Table + stat strip |
| 16 | Why Company + BD Person | 2-column: company stack · person trust |
| 17 | Closing / Next Step | 3-column: start here, what BD does next, Month 18 |

---

## Framing Rules

- **Always company-first** — this deck is about what the company delivers, not the BD person
- The BD person appears on slides 16 and 17 only — as the relationship owner and programme sponsor
- All proof points must be company-attributed, not personal advisory claims
- The three layers (Modernize / Activate / Innovate) must map to real company platforms — no invented capabilities

## Do Not

- Change the 17-slide structure without user confirmation
- Invent platform capabilities not evidenced in the ikigai report or company website
- Skip the pptxkit `validate_pptx()` check
- Skip the preview QA step — the matrix slide (slide 4) is the most overflow-prone
- Label an unpreviewed deck as reviewed

## Success Criteria

- 17 slides, [validated] output
- All contact sheets reviewed, no red overflow
- Slide 4 (matrix) readable at normal zoom — if text is too small, reduce to 8pt minimum
- Platform-to-layer mapping is accurate to the company's actual stack
- Reviewed deck remains in the run folder and is copied to
  `$CLIENT_DELIVERY_DIR` only when configured

## Resources

- Validated FPT run: `~/content-ideas/runs/2026-06-16-gcc-implementation-roadmap/`
- build_deck.py reference: `~/content-ideas/runs/2026-06-16-gcc-implementation-roadmap/build_deck.py`
- build_deck_template.py: `build_deck_template.py` beside this file
- pptxkit API: resolve the installed `branded-pptx-deck` skill; block branded
  output if it is unavailable
- Chained from: sibling `ikigai-gamma-slidedeck` skill (Stage 3)

## Skill Relationships

### Category
Business Automation

### Dependencies
- `branded-pptx-deck` or compatible pptxkit workflow — required for branded output and QA

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `ikigai` | Sequential upstream | standalone report is the source | `runs/.../<name>-ikigai-report.md` |
| `ikigai-gamma-slidedeck` | Sequential upstream | BD/company-first chained run | `runs/.../<name>-ikigai-report.md` |
| `branded-pptx-deck` | Orchestrator dependency | every PPTX build | reviewed `.pptx` and preview contact sheets |

### Runtime Preamble
State whether this is standalone or chained from an ikigai report, whether the
branded builder is available, and where reviewed output will be delivered.

## Gotchas

- Never invent company platforms or proof points; trace them to supplied evidence.
- Never label a deck reviewed until validation and visual QA both pass.
- Never copy output to a machine-specific Desktop path; use
  `$CLIENT_DELIVERY_DIR` only when configured.
