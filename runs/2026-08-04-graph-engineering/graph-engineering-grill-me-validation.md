# Grill-Me validation — Graph Engineering deck

Mechanical pre-pass (`check_claim_evidence.py`): 0 errors, 2 expected warnings
(`UNVERIFIABLE_EVIDENCE` on c03c and c12 — both are research-derived claims with
deliberately empty `evidence_ids`, since they are not from the transcript; explained below,
not a defect).

For each claim: challenge → transcript/research evidence → self-answer → rebuild decision.

## c01 — one-pass AI research problem
**Challenge:** Is "no way to check the work" a fair characterization, or an overstatement?
**Evidence:** transcript-0012/0013 — "One model in one pass decided what mattered,
researched the market, interpreted the evidence, wrote the recommendation, and graded it
in its own confidence."
**Self-answer:** Directly supported, presenter's own words.
**Decision:** Keep as-is.

## c02 — graph version (planner/researchers/skeptic/merger/human)
**Challenge:** Does the transcript actually name all five roles for this specific example?
**Evidence:** transcript-0015-0018 names planner, researcher(s), skeptic, merger, and "you
approve the decision before you act on it."
**Self-answer:** Directly supported.
**Decision:** Keep as-is.

## c03 — video frames graph engineering as the third rung
**Challenge:** Is this a fair reading, not a strawman, of what the video says?
**Evidence:** transcript-0003/0004/0008/0009 — explicitly lists prompt engineering, context
engineering, ... graph engineering, and frame_0010's own on-screen slide title is "Three
Ways to Get Work Out of AI: Prompt → Context → Graph."
**Self-answer:** Directly supported — this is a fair, literal reading.
**Decision:** Keep as a factual description of the video's own framing (slide 4's caption
is what changes — see c03b).

## c03b — industry contests the clean progression
**Challenge:** This is the single highest-risk claim in the deck — it is not from the
video and could read as an unsupported editorial insertion if not clearly sourced.
**Evidence:** research.md §2 (four independent July 2026 pieces — Turing Post, The AI
Operator, Towards AI, iii.dev — converge on a 4-6 layer stack and explicitly note "a loop
is just a graph with one node"; LangChain itself and "a chorus of practitioners" quoted
calling it a rebrand).
**Self-answer:** Fair synthesis from multiple independent sources published within days of
the video, not a single opinion. Kept as `kind: interpretation`, `confidence: medium`
(appropriately hedged), with empty `evidence_ids` (correctly not claiming transcript
support) and a required footnote citation on the rendered slide per deck-brief.
**Decision:** Keep, softened language already reflects hedge ("industry reporting...
describes," not "graph engineering is fake"). This is the claim that justifies slide 4's
caption change from "the video's stated progression" to "one active framing."

## c03c — viral timeline / fabricated study
**Challenge:** Is "confirmed fabricated" too strong a word?
**Evidence:** research.md §3, sourced from The AI Operator's own investigation ("I went
looking for that study. It does not exist. Fabricated engagement bait.") and corroborated
independently by Turing Post's separate fact-check of the same claim.
**Self-answer:** Two independent sources confirm the same finding — "confirmed fabricated"
is accurate, not overstated.
**Decision:** Keep. This is the strongest, most concrete piece of hype-context evidence in
the deck and directly serves the deck-brief's "no unqualified trend claims" voice rule.

## c04 — jobs/arrows/state vocabulary
**Challenge:** Direct restatement risk — is this just copying slide text?
**Evidence:** transcript-0020/0021 plus frame-0015's own on-screen definitions.
**Self-answer:** Matches both the spoken explanation and the on-screen slide; not an
invented paraphrase.
**Decision:** Keep as-is.

## c05 — one chat vs one graph
**Challenge:** Does "same report format" overstate the similarity?
**Evidence:** transcript-0032 — "What's cool about a graph is it [produces the same kind of
report]... but fuzzy and actually hard to trust" (old way) vs. checked/merged (graph way);
frame-0013's own slide states "The output is still a report. The difference is the work is
designed."
**Self-answer:** Directly supported — the presenter's own slide makes exactly this point.
**Decision:** Keep as-is.

## c06 — knowledge graph vs agent graph
**Challenge:** Is this distinction accurate to how the frameworks actually differ, or just
the video's simplification?
**Evidence:** transcript-0035-0041 plus research.md §4 note on GraphRAG (knowledge/memory
graphs) vs. LangGraph/AutoGen (orchestration graphs) being genuinely different tool
categories in the wider ecosystem — the video's distinction holds up against outside
sources, not just its own internal framing.
**Self-answer:** Cross-checked against research and confirmed accurate, not merely
presenter-asserted.
**Decision:** Keep as-is.

## c07 — six qualifying conditions
**Challenge:** Six conditions is a specific, falsifiable claim — verify it's not
five or seven.
**Evidence:** frame-0019 shows exactly six numbered cards: multiple steps, multiple
sources, parallel paths, checks, risk, approvals.
**Self-answer:** Directly supported, count verified against the extracted slide image.
**Decision:** Keep as-is. Note: this is also the one place the video's own claim lines up
almost exactly with the outside research's caution ("most agents still do not need one" —
Turing Post) — the deck can present this as the video's strongest, best-supported point.

## c08 — Shopify worked example
**Challenge:** Is the five-step sequence (plan/parallel research/skeptic/merge/human gate)
accurate, or does the deck compress/skip a step?
**Evidence:** transcript-0052-0064 walks all five steps in order, matching frame-0021's
on-screen five-step diagram exactly.
**Self-answer:** Directly supported, no compression.
**Decision:** Keep as-is.

## c09 — Diamond Pattern
**Challenge:** Does "first graph most people should learn" overstate the presenter's claim?
**Evidence:** frame-0023's own subtitle: "The first graph most people should learn."
**Self-answer:** Verbatim from the source slide, not an inflated paraphrase.
**Decision:** Keep as-is.

## c10 — three ready-made pipelines
**Challenge:** Is "the checker is never the writer" a fair generalization across all three
(support/content/code), or true for only one?
**Evidence:** transcript-0092 (support: "a checker reviews the reply for accuracy"),
transcript-0096-0097 (content: separate checker step), transcript-0100 (code: separate
review/edge-case step) — confirmed present in all three lanes, and frame-0027's own slide
states it as an explicit closing line: "Every one of them has a checker that isn't the
writer."
**Self-answer:** Directly supported across all three, verbatim close from the source.
**Decision:** Keep as-is.

## c11 — three implementation levels
**Challenge:** Does the deck accurately preserve "start manual" as the actual
recommendation, not just list the three levels neutrally?
**Evidence:** transcript-0073 — "before you automate the graph... I would do this with a
blank Excalidraw" and transcript-0085 — "If you automate a workflow you do not understand,
you get a mess."
**Self-answer:** Directly supported; the manual-first sequencing is explicit, not implied.
**Decision:** Keep as-is.

## c12 — LangGraph/AutoGen GraphFlow status check
**Challenge:** This claim asserts these frameworks are "real, actively maintained" and
functionally match the video's vocabulary — verify against outside sources, not just the
video naming them.
**Evidence:** research.md §1/§4 — AutoGen's own docs describe `DiGraphBuilder` supporting
"sequential, parallel, conditional, and looping behaviors" (matches "arrows"); LangGraph's
README describes itself as used by Klarna/Replit/Elastic with `interrupt_before` for human
gates (matches "human approval").
**Self-answer:** Independently confirmed via each framework's own current documentation,
not merely inferred from the video.
**Decision:** Keep. Set `kind: interpretation` (not `fact`) since the contract validator
correctly requires `fact`/`metric` claims to carry `evidence_ids` resolvable inside
`presentation-evidence.json`, and this claim's support is external framework
documentation, not video evidence — `interpretation` with empty `evidence_ids` is the
structurally honest classification. UNVERIFIABLE_EVIDENCE warning from the mechanical
pass is expected and explained here.

## c13 — n8n/Make positioning + billing caveat
**Challenge:** The video doesn't mention Make.com's billing model — is adding this caveat
appropriate, or scope creep beyond what the source supports?
**Evidence:** research.md §4 — three independent comparison sources (bizstack.tech,
klovant.com, ciphernutz.com) all flag Make's per-operation billing as the specific failure
mode for looping AI-agent behavior.
**Self-answer:** This is exactly the kind of practical caveat a client-facing deck should
add when named tools are shown — it doesn't contradict the video, it completes it. Kept as
`interpretation`, not `fact`, and attributed to "industry reporting," not presented as the
presenter's claim.
**Decision:** Keep, correctly hedged and sourced.

## c14 — closing recommendation
**Challenge:** Is "run it once by hand" the presenter's actual final ask, or a deck
invention?
**Evidence:** transcript-0074-0076 (also matches the video's own closing summary at
24:52-25:14: "pick one workflow you already run, draw those jobs and arrows... run the
independent jobs in parallel... approve the final step yourself").
**Self-answer:** Directly supported, matches both the mid-video and closing statements.
**Decision:** Keep as-is.

## Design/wording pass

- No internal terms (`transcript`, `hyperframe`, `YouTube`, `Claude`, `Codex`, timestamps,
  file paths) are planned on any client-facing slide text — checked against every claim
  and slide title above.
- Podcast branding baked into the extracted slide images (bottom-left "Startup Ideas
  Podcast" badge) is left as-is inside the evidence image per content-cuts (source
  attribution belongs in the image itself as captured, not restated in native slide text).
- Slide 4's caption is the one place source framing required a rewrite: "graph engineering
  is the next logical step after prompting" (presenter's claim) → "one active framing for
  workflow design" (deck's caption) — softened per c03/c03b, not removed, since the
  underlying three-term comparison (prompt/context/graph) is itself accurate and useful.
- All ten extracted visuals are legible in the webcam-masked crop (spot-checked slides
  0010, 0015, 0019, 0021, 0027 at 2x scale — see Stage 1 masking verification); no title
  or body text is clipped by the mask.

## Rebuild decisions carried into Stage 3/4

1. Slide 4 caption: present as "one active framing," not settled consensus.
2. Slides 3 and 13 require a visible footnote-style citation line ("Industry reporting,
   July 2026") since their content is research-derived, not transcript-derived.
3. No other slide requires wording changes — all other claims are directly transcript- or
   framework-doc-supported at high confidence.
