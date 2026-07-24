# Grill-Me Validation - AI Agents Are The New SaaS

Status: `grill-me` skill body was not exposed in this Codex session, so this
uses the same adversarial pattern: challenge each storyline claim against the
transcript, self-answer the challenge, and record rebuild decisions.

Source transcript:
`runs/2026-07-02-video-to-deck-smoke/watch-output/download/video.en.vtt`

Supporting excerpt file:
`runs/2026-07-02-video-to-deck-rerun/grill-me-transcript-excerpts.md`

## Self-Questions And Answers

1. Is the core thesis supported?
   - Challenge: Does the transcript actually say agent SaaS sells work?
   - Answer: Yes. Around 00:01:38-00:01:50, the speaker says the product is
     the job and contrasts SaaS selling software with agent SaaS selling work.
   - Deck decision: Keep the core thesis.

2. Is the labor-market framing supported?
   - Challenge: Does the transcript support framing agents as labor?
   - Answer: Yes. Around 00:00:43-00:00:54, the speaker says agents can be
     packaged like SaaS and sold as labor, and says labor is a multi-trillion
     dollar market.
   - Deck decision: Keep, but avoid invented market sizing beyond the
     transcript's directional language.

3. Is the workflow-selection scorecard supported?
   - Challenge: Are the scorecard dimensions in the deck grounded in the
     transcript?
   - Answer: Yes. Around 00:04:42-00:07:05, the speaker lists frequency,
     clear finish line, software touched, learnable edge cases, felt loss/pain,
     and budget ownership.
   - Deck decision: Keep and align phrasing to those dimensions.

4. Is shadowing operators before building supported?
   - Challenge: Does the transcript support the operator-shadowing workflow?
   - Answer: Yes. Around 00:07:22-00:09:12, the speaker says to shadow a human
     before prompting/coding, watch 10-20 jobs, screen record, narrate, and
     specify trigger, context, tools, actions, approvals, escalation, success.
   - Deck decision: Keep.

5. Is "minimum useful agent" supported?
   - Challenge: Does the transcript use that concept and the four starter
     patterns?
   - Answer: Yes. Around 00:09:37-00:11:28, the speaker describes the minimal
     useful agent and lists draft-and-approve, triage, coordinator, and bounded
     action.
   - Deck decision: Use "minimum useful agent" / "smallest useful version"
     wording consistently.

6. Is the workflow-before-autonomy claim supported?
   - Challenge: Does the transcript support saying workflow comes before
     dynamic agent behavior?
   - Answer: Yes. Around 00:11:31-00:11:56, the speaker cites Anthropic
     guidance that many agent problems should start as workflows; a workflow
     follows a predictable path and autonomy is earned by adding judgment only
     where it creates value.
   - Deck decision: Keep and use the transcript's "predictable path" phrasing.

7. Is the wrapper/trust/evals claim supported?
   - Challenge: Does the transcript support wrapper, logs, approvals, controls,
     handoffs, and evals?
   - Answer: Yes. Around 00:12:52-00:15:29, the speaker says the product
     wrapper makes it SaaS, the agent does the work while the wrapper creates
     trust, and recommends a 50-example eval set.
   - Deck decision: Keep.

8. Is pilot-like-labor and pricing supported?
   - Challenge: Does the transcript support the pilot and productize sequence?
   - Answer: Yes. Around 00:15:54-00:18:35, the speaker says sell the pilot
     like labor, manually do work with AI, start with three customers in one
     niche, charge setup + monthly, then add usage/outcome pricing later.
   - Deck decision: Keep.

9. Is "moat/defensibility" supported?
   - Challenge: Does the transcript use "moat" or explicitly frame workflow
     ownership as defensibility?
   - Answer: No. That was consultant synthesis, not direct transcript wording.
     The transcript-supported idea is "you earn the software by doing the work
     first" and "build the product around the repeated pattern" around
     00:18:04-00:18:35.
   - Deck decision: Replace the moat slide with transcript-backed productization
     language.

10. Is workflow-teardown distribution supported?
    - Challenge: Does the transcript support old-way/new-way teardown content?
    - Answer: Yes. Around 00:18:38-00:21:24, the speaker recommends workflow
      teardowns, showing old way versus agent way, building content, and putting
      paid ads behind winners.
    - Deck decision: Keep.

11. Is the 30-day plan supported?
    - Challenge: Does the transcript support the 30-day sequence?
    - Answer: Yes. Around 00:22:02-00:24:13, the speaker gives day/week steps:
      pick niche, interview operators, pick workflow, write spec, test manually
      with AI, build smallest useful version, create eval set, sell pilots,
      add wrapper, publish workflow teardowns.
    - Deck decision: Keep.

12. Are any client slides exposing internal process terms?
    - Challenge: Do visible slides mention tools or internal workflow details?
    - Answer: v7 visible text was already checked clean for internal terms.
      Maintain that in v8.
    - Deck decision: Keep source/tool/audit language out of visible slides.

## Rebuild Decisions

- Keep the overall storyline.
- Preserve visible recreated drawing visuals.
- Add no client-facing source/tool/internal process notes.
- Keep executive summary and conclusion.
- Replace "Defensibility / moat" language with transcript-backed
  productization language.
- Tighten a few slide titles to the transcript's actual phrases:
  "product is the job", "workflow with a paycheck attached", "minimum useful
  agent", "product wrapper", "sell the pilot like labor", and "workflow
  teardowns."
