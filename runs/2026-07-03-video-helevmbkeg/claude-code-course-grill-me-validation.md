# Slide-Level Validation

This is the mandatory skeptical pass before PPTX rendering. It challenges slide claims against the transcript and the visual inventory.

## Key Claim Checks

| Claim | Challenge | Evidence | Decision |
|---|---|---|---|
| The course is a business operating system, not just a coding tutorial. | Is this overreach? | The transcript spends major sections on sellable websites, automations, support inboxes, lead enrichment, and pricing. | Keep as executive framing; mark as fair synthesis. |
| Claude Code is local execution versus browser advice. | Is this directly supported? | 00:02:36-00:04:09 contrasts browser copy-paste with Claude Code reading files, editing files, running code, and testing. | Keep. |
| Project rules and skills create repeatability. | Is this directly supported? | 00:16:03-00:23:22 demonstrates project instructions and reusable skills. | Keep. |
| Beginner path is websites, automations, AI systems. | Is this directly supported? | 00:26:26-00:28:30 lays out three levels. | Keep. |
| Planning should precede building. | Is this directly supported? | 01:45:45-01:50:36 explains build plan, implementation plan, build, test/refine and says building is a smaller share of effort. | Keep. |
| Pricing should anchor to ROI. | Is this directly supported? | 02:03:44-02:10:26 covers 5x ROI, result-based pricing, and setup plus recurring. | Keep. |
| Four-week rollout is in the video. | Is this directly supported? | The video gives steps but not a literal four-week program. | Keep only as recommendation, not direct claim. |
| Market-size claims should appear. | Are they robust enough? | Transcript mentions small business website market sizing, but no independent verification was run for this deck. | Exclude from client slides. |

## Design Checks

- Raw screenshots contain creator face overlays, YouTube/video UI, terminal details, and small code text. They are not suitable as main client visuals.
- Native PowerPoint shapes are the correct route for readability and editability.
- The deck should avoid visible production terms and file paths.

## Rebuild Decisions

- Use no original screenshot visuals in the deck.
- Keep video-derived proof in source artifacts, not visible client slide text.
- Use action titles throughout.
- Keep pricing examples qualitative unless they are direct examples from the transcript.

