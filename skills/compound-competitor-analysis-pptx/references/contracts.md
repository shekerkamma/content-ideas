# Contract specification

## Evidence statuses

| Status | Meaning | Permitted language |
|---|---|---|
| `verified` | Primary evidence directly supports the scoped claim | State within the evidenced boundary |
| `attributed company claim` | The company or partner claims it; independent proof absent | Attribute explicitly |
| `qualified interpretation` | Reasoned synthesis from identified evidence | Use conditional language and show logic |
| `insufficient evidence` | Evidence does not support a decision-safe assertion | State the gap and required proof |

Evidence status and competitive magnitude must use independent visual encodings.

## Slide content contract

Required fields:

```json
{
  "slide_id": 1,
  "section": "Executive thesis",
  "assertion_title": "Complete answer-led sentence",
  "analytical_question": "One decision question",
  "executive_answer": "Bounded answer",
  "evidence_blocks": [{
    "label": "Short evidence label",
    "claim": "Claim with scope",
    "evidence_ids": ["E-001"],
    "evidence_status": "verified"
  }],
  "comparison_logic": "How evidence is compared or combined",
  "counterargument": "Strongest alternative explanation",
  "implication": "Business consequence",
  "decision": "Specific decision",
  "owner": "Named role",
  "trigger": "Observable event and time boundary",
  "exhibit": {"archetype": "evidence-ladder", "elements": []},
  "source_note": "Source IDs and caveats"
}
```

## Slide design contract

Required fields:

```json
{
  "slide_number": 1,
  "content_contract_id": 1,
  "family": "evidence-ladder",
  "visual_thesis": "What the geometry must prove",
  "design_prompt": "Complete per-slide construction prompt",
  "layout_contract": {
    "grid": "7/5 split",
    "focal_point": "bounded verdict",
    "reading_flow": "evidence → confidence → decision",
    "density_budget": "65–90 visible words",
    "title_zone": "top 14%",
    "exhibit_zone": "middle 64%",
    "decision_zone": "bottom 15%",
    "whitespace": "minimum 20%",
    "alignment": "12-column grid",
    "hierarchy": "title > verdict > evidence > annotation > source"
  },
  "graphic_contract": {
    "encoding": "Geometry and color semantics",
    "comparison_logic": "What is compared",
    "dominant_mark": "one",
    "annotation_limit": 3,
    "evidence_encoding": "Independent status encoding",
    "counterargument_treatment": "Visible subordinate falsifier",
    "source_treatment": "Quiet footnote rail"
  },
  "typography_contract": {},
  "content_limits": {},
  "evidence_regions": [],
  "visual_routes": [],
  "prohibited": [],
  "qa_questions": []
}
```

## Deck-wide contracts

- `deck-brief.md`: audience, decision, narrative promise, voice, evidence/editability constraints,
  anti-references, success criteria.
- `deck-design.json`: typography, palette, density, shape count, contrast, lint thresholds, explicit
  waivers only.
- `template-profile.json`: template source, aspect ratio, brand tokens, geometry, composition rules,
  approved archetypes.
- `slide-plan.json`: audience job, claims, evidence, visuals, notes, accessibility intent.
- `visual-spec.json`: one route and provenance record per meaningful visual region.

Do not reuse stale waivers from another deck version. Counts, slide totals, filenames, and render
evidence in QA files must match the current deliverable.
