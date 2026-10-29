# Completeness audit and missing-gate controls

## Evidence integrity

- Normalize legal/company/product names and record aliases before deduplication.
- Date every volatile claim and set a freshness/expiry rule for pricing, funding, leadership,
  certification, customer nominations, deployment counts and regulation.
- Separate source publication date, event date and retrieval date.
- Capture contradiction records rather than silently selecting one source.
- Require primary-source corroboration for certification, homologation, named customers, production
  wins and regulatory obligations when decision-critical.
- Record negative evidence carefully: “not found in reviewed sources” is not “does not exist.”

## Comparable-scope integrity

- Normalize stack layer, vehicle/product scope, geography, customer type, deployment stage and price
  basis before comparing competitors.
- Do not rank full systems, perception modules, sensors, software and channel partners on one scale
  without separate arenas.
- Define every score scale, weight, missing-data rule and confidence modifier.
- Run sensitivity analysis for weighted rankings and show when a rank is unstable.
- Distinguish threat severity from evidence confidence and partnerability.

## Content integrity

- Scan every visible number against `allowed-numbers.yaml`.
- Scan visible text for internal tool names, raw paths, timestamps, “audit,” “validation,” “synthesis,”
  model names and production notes.
- Verify claim IDs and review-control IDs survive into slide contracts and notes.
- Verify every competitor dossier uses like-for-like headings but evidence-specific conclusions.
- Verify counterarguments, falsifiers and “what changes our view” triggers are visible.
- Run title-only narrative, duplicate-claim and decision/owner/trigger completeness checks.

## Visual and editability integrity

- Derive the template profile from the actual reference deck and validate brand geometry.
- Record route/provenance for every meaningful visual region.
- Verify exact evidence was extracted rather than approximated.
- Verify analytical exhibits remain PowerPoint-native/editable unless explicitly declared otherwise.
- Check images for crop, DPI, rights, logos and alt text.
- Check reading order, notes, slide titles and accessibility descriptions.
- Ensure chart axes, units, denominators, scales and directional-only disclaimers are explicit.

## Review materiality

- For redesigns, compare previous and candidate PPTX and require material slide-level change.
- Map every Grill-Me/Meta LOOP control to a changed contract field and rendered region.
- Require independent content/design review after integration; invocation logs are not review proof.
- Reject a pass when the original user criticism remains visible even if lint is clean.

## Technical and delivery integrity

- Validate OpenXML and package relationships.
- Run deterministic design lint with no stale or blanket waivers.
- Run OfficeCLI issue scan and HTML contact sheets.
- Run Windows-native Microsoft PowerPoint contact sheet when available; close active PowerPoint
  sessions if COM acquisition fails, or remain draft/blocked.
- Verify all slides, notes, fonts, numbering, footers, hyperlinks and accessibility metadata.
- Verify final and delivered checksums match.
- Write `delivery-manifest.json`, `sync-check.md`, QA summary and explicit status.

## Model and skill attribution

- Record actual models/tools used, real invocation status, batch IDs, output paths and budgets.
- Do not infer model routing from a catalogue or claim Meta LOOP/LLM Council when capability gates or
  required roles did not run.
- Maintain `skill-application-manifest.json` proving visible impact by layer.

## Close-the-loop controls

- Write `run-learnings.md` with generalized corrections.
- Write durable sourced findings to GBrain when available; never write client deliverables, secrets,
  unsupported scores or transient drafts.
- Convert observable triggers into a monitoring queue with owner, source, cadence and action.
- Mark evidence and threat scores stale when trigger dates pass.

## Reviewed promotion checklist

Reviewed requires all gates above plus:

```text
evidence locked
metrics/scoring locked
story locked
Grill-Me controls resolved
Meta LOOP blueprint implemented or capability fallback disclosed
bounded batches consolidated
content/design contracts validated
material change passed when applicable
native editable build passed
visible-number/internal-term scans passed
accessibility/notes passed
OfficeCLI + native PowerPoint review passed
delivery manifest and checksum passed
```
