# Workflow

## 1. Scope and evidence

Resolve audience, decision, slide-count floor, editability, brand template, delivery path, and source
artifacts. Recall prior work through GBrain when available. Search primary/current sources; use
fresh-page extraction for important claims. Never infer certification, production nomination,
customer status, or procurement eligibility from marketing language.

Write claim-level evidence with:

- evidence ID;
- exact claim;
- source title, URL/path, publisher, publication date, retrieval date;
- source type and primary/secondary status;
- evidence status;
- scope, qualifiers, and expiry/staleness risk;
- destination slide IDs.

## 2. Analyze before storyboarding

Define metrics, comparison universe, inclusion rules, scoring scales, denominators, confidence, and
missing-data treatment. Use buyer/control-point logic. Do not score qualitative claims as facts.

## 3. Architect the story

Build this spine when applicable:

```text
decision context → market architecture → priority threats → competitor dossiers →
DeepGrid advantage boundaries → strategic options → decisions → 30/90-day actions → appendix
```

Write titles first. Reading titles alone must reproduce the argument. Preserve the requested slide
count; do not compress a deep-research deck merely to make authoring easier.

## 4. Write content contracts

Generate one content envelope per slide using `prompt-templates.md`. Validate all required fields,
evidence IDs, and evidence statuses before layout work. Keep complete research in the contract even
when only a bounded subset becomes visible.

## 5. Compare design directions

For at least three representative slides, compare three materially different visual directions.
Record the selected direction and at least four concrete differences from the incumbent. Recoloring
is not a direction.

## 6. Write design contracts

For every slide, define grid, focal point, reading flow, dominant exhibit, encoding, hierarchy,
whitespace, density, annotation limits, source treatment, prohibited patterns, and QA questions.
Use the archetype only as a starting point; the per-slide prompt must bind the actual evidence and
decision.

## 7. Build natively

Build from validated JSON, not hand-typed slides. Keep all analytical marks editable. Preserve exact
source pixels where their appearance is evidence. Store full content contracts in notes when visible
copy is distilled.

## 8. Critique, audit, polish

Inspect representative pages early. Then inspect every slide in contact sheets. Fix the system when
defects repeat; do not patch 74 instances of the same broken renderer. Run contract validation,
package validation, design lint, OfficeCLI validation/issues, HTML render, and native PowerPoint
render.

## 9. Promote and deliver

Write `qa-summary.md`. Promote only if every required gate passes. Copy only the promoted file to the
configured delivery directory. On WSL/Windows, use a new filename if PowerPoint has locked the old
one. Verify source/destination checksums and open the delivered file.
