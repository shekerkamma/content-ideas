---
name: investor-competitive-dossier
description: Build a deep, evidence-led investor or venture diligence dossier and native branded PowerPoint from a company cohort, market list, article, URL, or sector thesis. Use when the user asks for an investor deck, investment landscape, startup cohort analysis, competitive investor memo, evidence-adjusted valuation story, portfolio thesis, qualitative competitor analysis, or says an existing market deck is shallow, lacks a storyboard, lacks real competitors, or needs Livecrawl/Exa/STORM research and PowerPoint delivery.
---

# Investor Competitive Dossier

Build an investor decision product, not a vendor list. Chain recall, current-web acquisition,
claim-level evidence controls, independent research lenses, competitive arenas, story review,
native branded PPTX, real Office QA, and durable learning capture.

State at invocation:

> I am using the investor competitive dossier compound pipeline: GBrain recall, You.com Level
> 2 and Exa acquisition, evidence ledger and metric controls, independent STORM lenses,
> competitor/story architecture, branded native PowerPoint, Office QA, and GBrain write-back.

## Required reading

- Read [references/workflow-contract.md](references/workflow-contract.md) before starting or resuming.
- Read [references/investor-analysis-patterns.md](references/investor-analysis-patterns.md) before
  defining arenas, company teardowns, valuation framing, or portfolio roles.
- Read [references/host-portability.md](references/host-portability.md) when installing,
  synchronizing, validating, or repairing this skill across hosts.
- Read the complete instructions for `evidence-led-competitor-pipeline`,
  `aianalyst-competitor-analysis`, `storm-research`, `competitor-analysis-pipeline`, and
  `branded-pptx-deck` before invoking those stages.
- For a PowerPoint build, route through `skills/present/` and follow the mandatory
  `pptx-visual-spec` and design-quality contracts.

## Pipeline

1. **Resume and frame.** Use one canonical run root:
   `runs/<YYYY-MM-DD>-<target>-investor-competitive-dossier/`. Preserve an existing run and
   place every chained skill's artifacts under that root, even when a child skill documents a
   different default. Create or update `status.json` and
   `inputs/operating-prompt.yaml`. Name the audience, decision, cohort, timeframe,
   deliverables, and evidence threshold. Treat 24 slides as a planning default for a material
   investor dossier—not a hard gate unless the user specifies a minimum. Set no maximum: the
   argument and evidence determine length.

2. **Recall before research.** Run semantic GBrain recall for the sector, companies,
   executives, prior runs, and known corrections. Inventory repo-local research and prior
   deliverables. Record recall status even when it returns no matches.

3. **Acquire current evidence.** Use this order:
   local/GBrain → You.com Level 2 → Exa semantic expansion → official/primary follow-up →
   Firecrawl/Printing Press only for unresolved full-page/site capture → generic search only
   for verification gaps. This order overrides conflicting child-skill defaults. Level 2 must
   return both discovery and fresh
   extraction; log the actual route and per-page statuses. Save queries and failures in
   `outputs/search-log.md`. Never treat a search snippet as extracted proof.

4. **Create the evidence product.** Invoke `aianalyst-competitor-analysis`. Produce the
   claim-level ledger, metric definitions, data-quality report, allowed numbers, scoring or
   evidence-state model, and competitor brief. Define metrics before ranking. Prefer ordinal
   evidence states when private-company data cannot support precise scoring.

5. **Run independent lenses.** Invoke full `storm-research` with practitioner, academic,
   skeptic, economist, and historian agents. Keep them independent and persist briefs under
   `working/storm/lenses/`. Save the contradiction map at
   `working/storm/contradiction-map.md`. Run separate verifier agents against citation
   clusters, save results under `working/storm/verifiers/`, summarize them in
   `outputs/citation-verification.md`, and apply corrections before artifact build or rebuild.

6. **Map real competitive arenas.** Include sector incumbents, adjacent startups,
   customer-built/internal alternatives when relevant, standards or regulatory substitutes,
   channels, and strategic acquirers. Do not assume companies on the source list compete
   directly with one another.

7. **Lock the decision story.** Build `outputs/story-architect-pack.md` before PowerPoint.
   Use assertion titles and this default arc:

   `answer → storyboard → market structure → arenas → evidence rules → cohort comparison →
   company teardowns → cross-company synthesis → contradictions → bull/bear → valuation →
   portfolio roles → diligence plan → scenarios → kill criteria → recommendation`

   Give every company qualitative treatment. Each teardown must state real competitors, why
   it can win, what is proven, what is missing, and the disconfirming signal. Cut unsupported
   composite scores, allocations, and rankings.

8. **Review before rendering.** Apply a document/story review to the markdown packet. Fix
   weak argument structure, missing counterarguments, unsupported numbers, and repeated
   marketing language before touching slides.

9. **Build native branded PowerPoint.** Invoke `branded-pptx-deck`; use the resolved branded
   template and retain the builder. Create the required presentation contracts. Keep titles,
   matrices, diagrams, evidence states, and citations editable. Company teardown consistency
   is useful, but vary section and synthesis layouts so the deck does not become monotonous.

10. **Validate and prove the redesign.** Run package validation, deterministic lint, real
    OfficeCLI render/issue scan, contact-sheet inspection, visible-number/source scans, and
    editable-shape checks. For a redesign, run `compare_pptx.py --require-material` against
    the previous deck. If the exact prior PPTX cannot be located, stop the redesign comparison
    gate and request it; a verbal description is insufficient. Do not suppress real design problems. Classify intentional analytical
    density explicitly when it is retained.

11. **Deliver honestly.** Use `draft`, `reviewed`, or `blocked`. A valid PPTX is not
    automatically reviewed. Copy/open on Windows only after exact-artifact QA. A PPTX-only
    request may finish as a QA-passed `draft`. `reviewed` under the complete evidence-led
    pipeline additionally requires the self-contained HTML twin, sync check, and delivery
    manifest. Never build or publish HTML merely to change a filename unless it is in scope.

12. **Compound the learning.** Write durable sector findings, factual corrections, proof
    thresholds, and reusable deck lessons to GBrain. Keep deliverables and the evidence ledger
    local; GBrain is recall, not the system of record.

## Mandatory outputs

Use the existing evidence-led run contract. At minimum retain:

```text
status.json
inputs/operating-prompt.yaml
outputs/search-log.md
outputs/evidence-ledger.csv
outputs/evidence-ledger.md
outputs/metric-definitions.md
outputs/data-quality-report.md
outputs/scoring-model.md
outputs/allowed-numbers.yaml
outputs/competitor-brief.md
outputs/story-architect-pack.md
outputs/storyboard-qa.md
outputs/artifact-traceability.md
outputs/citation-verification.md
outputs/story-structure-review.md
outputs/sync-check.md (required for complete reviewed promotion)
outputs/run-learnings.md
working/storm/lenses/
working/storm/contradiction-map.md
working/storm/verifiers/
deck-brief.md
deck-design.json
template-profile.json
presentation-evidence.json
slide-plan.json
visual-spec.json
build_*.py
*-draft.pptx or *-reviewed.pptx
qa/
client-package/site/index.html (required for complete reviewed promotion)
client-package/delivery-manifest.json (required for complete reviewed promotion)
```

## Stop conditions

Do not promote when any of these is true:

- search discovery occurred without fresh extraction but Level 2 is claimed;
- a ranking metric is undefined or vendor evidence is silently treated as independent;
- the competitor universe omits material incumbents, substitutes, or sector-relevant
  customer-built/internal alternatives;
- the deck is a vendor chronology with no decision storyboard;
- any cohort company lacks qualitative analysis;
- funding, contracts, pipeline, bookings, revenue, and production are conflated;
- STORM lenses or independent citation verification are incomplete;
- material redesign is requested but the PPTX comparison does not pass;
- real Office render QA or editable-text verification is missing.

## Final response

Report the deck path and slide count, artifact status, research backends and actual Level 2
status, evidence/verifier tally, material-change result when applicable, Office QA result,
the 2–4 most differentiated investment conclusions, and any open promotion gate.
