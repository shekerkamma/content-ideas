# Fable 5 Slide Validation

Method: skeptical slide-by-slide challenge against caption evidence and efficient visual coverage.

## Global Checks

- The deck follows the video's three-part structure: skills, existing features, ambitious planning.
- The deck adds executive framing but avoids claims not grounded in the video.
- The deck avoids raw screenshot insertion and uses editable PowerPoint diagrams.
- Presenter-only frames are excluded and accounted for.

## Slide-Level Review

| Slide | Claim challenge | Evidence basis | Rebuild decision |
|---|---|---|---|
| 1 | Does the cover overstate the urgency? | The speaker says Fable 5 is back briefly and available only for a few more days. | Keep urgency, avoid exact calendar claim on slide. |
| 2 | Is "reusable leverage" an interpretation? | The speaker says to use access to improve things that are helpful even after access ends. | Keep as fair synthesis. |
| 3 | Is broad-context positioning supported? | The speaker repeatedly contrasts Fable's broader context understanding with smaller decomposed work. | Keep. |
| 4 | Are the three moves complete? | Video description and closing summary name improving skills, existing features, and researching/ambitious planning. | Keep. |
| 5 | Is skill improvement a real use case? | First major section demonstrates reviewing a skill library. | Keep. |
| 6 | Is the workflow sequence invented? | It follows the demo: select model, run skill review, inspect recommendations, codify changes. | Keep. |
| 7 | Are quality criteria supported? | The speaker discusses intent, downstream handoffs, edge cases, and practical implementation. | Keep. |
| 8 | Does the feature review section fit? | The second major section reviews an existing project that needs to work before market. | Keep. |
| 9 | Are root-cause and implementation sequence supported? | The speaker describes repeated failed commits, server-side orchestration, tool usage, and plans. | Keep. |
| 10 | Is ambitious planning supported? | The third section uses Fable for research and planning complex features. | Keep. |
| 11 | Is server-side streaming too specific? | The speaker uses server-side streaming, events, tokens, and front-end rendering as the concrete example. | Keep. |
| 12 | Is the small-chunk comparison fair? | The speaker says other tools would require breaking the problem into many smaller pieces. | Keep, label as operating comparison. |
| 13 | Are caught issues accurate? | The speaker mentions repeated loops, interruption/pause handling, incorrect assumptions, and missed areas. | Keep. |
| 14 | Is the five-day plan too prescriptive? | It operationalizes the temporary-window message; not a direct quote. | Keep as recommended action plan. |
| 15 | Does the conclusion match the video? | It restates the closing recommendation to use Fable for the three high-value categories. | Keep. |

## Design Review

- Each slide uses an assertion title, not a section label.
- Every slide has a primary visual or structured panel.
- Tables and flows are native PowerPoint shapes.
- No slide depends on pasted screenshots.
- Avoided visible internal production terms.

