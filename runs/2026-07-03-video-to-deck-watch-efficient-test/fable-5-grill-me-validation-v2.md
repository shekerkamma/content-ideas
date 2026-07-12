# Fable 5 Rebuild Validation V2

Method: skeptical review of each slide against the user-provided transcript.

## Validation Questions

| Slide | Challenge | Transcript-backed answer | Decision |
|---|---|---|---|
| 1 | Is the deck really about scarce access? | The opening contrasts random one-shot experiments with three higher-value uses before access becomes expensive. | Keep. |
| 2 | Does the executive summary over-generalize? | The transcript repeatedly names reusable skills, existing features, and ambitious planning as the three recommended uses. | Keep and make specific. |
| 3 | Is the allocation choice explicit enough? | The speaker frames the decision as random throwaway projects versus three concrete use cases. | Add decision filter. |
| 4 | Is Fable's differentiation explained? | The speaker says Fable is better at context, intent, details, and seeing goals through completion. | Add as operating thesis. |
| 5 | Is the skill-library example specific? | The demo uses a go-to-market skill library for channel strategy, positioning, pricing, landing-page structure, and copy. | Include named work types. |
| 6 | Are the skill findings accurate? | The transcript says details like brand voice, customer language, and design specifics were not translating downstream. | Include as finding. |
| 7 | Is the adapter concept grounded? | The speaker says design tools need different prompt formats and adapter steps. | Include as operating pattern. |
| 8 | Is the product review example specific? | The app added agent loops, bugs started, and launch readiness required a higher-level diagnosis. | Include as feature-readiness use case. |
| 9 | Is the root cause accurate? | The transcript says server-side loop is stateless while the conversation is not, and the client is doing too much orchestration. | Include as central diagnostic. |
| 10 | Does the deck explain why patching failed? | The speaker describes repeated duct-tape commits that fixed symptoms without solving the underlying problem. | Include contrast. |
| 11 | Is the checkpointer recommendation grounded? | The transcript says the system needs a server-side checkpointer that persists state through interrupts and user replies. | Include in architecture slide. |
| 12 | Is the planning section grounded? | The speaker describes combining background knowledge, goals, notes, feature ideas, and research. | Include as planning workflow. |
| 13 | Is streaming specific enough? | The transcript distinguishes token streaming from server event streaming to the front end. | Include both lanes. |
| 14 | Is the comparison with another model fair? | The speaker says the other plan would reintroduce bugs, mishandle interrupts, contain factually wrong assumptions, and miss codebase areas. | Include as risk taxonomy. |
| 15 | Does the action plan follow from the transcript? | The speaker recommends using the remaining days on one or all three high-value uses. | Keep as operational recommendation. |
| 16 | Does conclusion add value? | It restates the allocation decision and makes the next move concrete. | Keep. |

## Rebuild Standard

- Every slide must explain one business or engineering implication.
- Every section must include what the demo showed and why it matters.
- No slide should look like pasted notes.
- No raw captured frames are used as primary visuals.

