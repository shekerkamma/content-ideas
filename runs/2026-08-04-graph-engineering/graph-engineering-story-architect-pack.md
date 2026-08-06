# Story architect pack — Graph Engineering

## 1. BLUF

When an AI workflow has multiple steps, multiple sources of truth, work that can run in
parallel, real risk, or a required approval, stop running it as one long chat — design it
as an explicit graph of jobs, arrows, and shared state instead. You don't need new tooling
to start: draw one real workflow you already run, on a whiteboard, this week.

## 2. Audience decision

**Audience:** a technical/ops leader deciding whether and how to formalize their team's
ad hoc AI workflows into managed multi-agent systems.
**Decision the deck must land:** adopt the *qualifying test* (six conditions) before
reaching for any orchestration framework, and start with a manual first rep — not a
platform purchase — regardless of what "graph engineering" as a trend label turns out to
mean six months from now.

## 3. Tension

Most people still run multi-step AI work as one giant chat: ask a single model to
research, judge its own evidence, and hand back a confident-sounding answer in one pass.
That's fine for a low-stakes, one-off question. It breaks down the moment the task has
real stakes, needs evidence from more than one place, or requires a human to actually sign
off before something happens — because one model in one pass decided what mattered,
graded its own work, and left no seams to check.

Separately: the vocabulary for this problem is having a very online, very messy moment
right now — a new term ("graph engineering") went viral in 48 hours, spawned three
competing definitions, and got attached to a fabricated study before anyone could adopt
it responsibly. The deck has to give the audience the durable mechanics without importing
the hype.

## 4. Argument arc

1. **Context** — a new term, "graph engineering," is spreading fast, pitched as the next
   rung after prompt and context engineering.
2. **Complication** — the term itself is contested: viral in 48 hours, three competing
   definitions, and a widely shared "study" behind it that doesn't exist. Adopt the
   mechanics, not the hype cycle.
3. **What's actually real** — jobs (steps) + arrows (dependencies) + shared state is a
   directed graph, and that shape already runs in production multi-agent frameworks today.
4. **The gate** — a graph only earns its place under six specific conditions; most AI work
   still doesn't need one, so check before you build.
5. **Proof** — a full worked example (an AI-bookkeeping build/no-build decision) walked
   through plan → parallel research → skeptic → merge → human gate.
6. **Reusable shape** — three ready-made pipeline patterns (support, content, code) that
   all share one structural rule: the checker is never the writer.
7. **On-ramp** — three implementation levels, from a whiteboard to file trails to real
   orchestration tooling — deliberately starting manual.
8. **Decision / action** — pick one workflow you already run, draw it, run it once by
   hand. That's the actual ask, not "go adopt a framework."

## 5. Slide spine

| # | Slide title (assertion) | Role | Evidence | Visual treatment | Takeaway |
|---|---|---|---|---|---|
| 1 | Title / framing | Cover | — | Native | Sets scope: mechanics of structured AI workflows, not the trend label |
| 2 | Most AI work still runs as one long chat — and that's the actual problem | Exec summary / BLUF | transcript 01:51-02:39 (before/after framing), extracted evidence slide 0011 | Route 0 extract (frame_0011) + native BLUF panel | One model, one pass, no seams to check = fine for low stakes, risky for real decisions |
| 3 | "Graph engineering" is having a very contested moment — separate the mechanics from the hype | New content (not in video) | research.md §3 (viral 48h, 3 definitions, fabricated study, "nothing new" critique) | Native — timeline/callout card, no extracted frame | Adopt the durable pattern, not the trend cycle |
| 4 | Three ways people are trying to get more out of AI | Context / vocabulary | transcript 01:26-01:38, extracted evidence slide 0010 | Route 0 extract (frame_0010) | Graph engineering is workflow design, not another wording trick — **caption softened per grill-me**: shown as "one active framing," not settled progression |
| 5 | The vocabulary: jobs, arrows, shared state | Definitional | transcript 03:53-04:xx, extracted evidence slide 0015 | Route 0 extract (frame_0015) | A graph is nothing more than steps connected by dependencies, with one shared record |
| 6 | One chat vs. one graph — same question, different shape of work | Contrast | transcript 02:50-03:19, extracted evidence slide 0013 | Route 0 extract (frame_0013) | Same output format (a report); the difference is whether the work behind it can be checked |
| 7 | Don't confuse a knowledge graph with an agent graph | Clarifying distinction | transcript 06:39-06:50 area, extracted evidence slide 0017 | Route 0 extract (frame_0017) | One maps what your data means; the other maps how work should move — this deck is about the second one |
| 8 | The qualifying test — when a graph earns its place | Gate / decision criteria | transcript ~08:43-09:xx, extracted evidence slide 0019 | Route 0 extract (frame_0019) | Six conditions; none of them true means a graph is overhead, not a badge of sophistication |
| 9 | Worked example: should we build AI bookkeeping for Shopify? | Proof / demo | transcript ~10:17 area, extracted evidence slide 0021 | Route 0 extract (frame_0021) | Plan → three parallel researchers → skeptic → merge → human picks the next move |
| 10 | The pattern underneath: Diamond | Proof, generalized | transcript ~13:37 area, extracted evidence slide 0023 | Route 0 extract (frame_0023) | Planner fans out to parallel researchers, skeptic attacks findings, merge + human approve — the first graph most people should learn |
| 11 | Three ready-made pipelines you can steal | Reusable application | transcript ~17:38 area, extracted evidence slide 0027 | Route 0 extract (frame_0027) | Support, content, and code workflows all follow the same rule: the checker is never the writer |
| 12 | Three levels of implementation — start manual | Operating model / on-ramp | transcript ~15:16 area, extracted evidence slide 0025 | Route 0 extract (frame_0025) | Manual whiteboard lanes → file trails → real orchestration (LangGraph / AutoGen / n8n / Make) — earn the tooling, don't start with it |
| 13 | Where the named tools actually fit | New content (not in video) | research.md §4 (LangGraph, AutoGen GraphFlow, n8n/Make status check) | Native comparison table | LangGraph/AutoGen for stateful multi-agent logic; n8n/Make for the plumbing around it; most teams should start below all of them |
| 14 | Next move: draw one graph this week | Decision / action | transcript 24:52-25:14 | Native, no extracted frame | Pick one workflow you already run, draw jobs + arrows, delete fake waiting, run it once by hand |

## 6. Evidence map

**Direct evidence (transcript/slide-supported, no softening needed):**
- The jobs/arrows/state vocabulary (slide 5)
- One-chat-vs-one-graph contrast (slide 6)
- Knowledge-graph-vs-agent-graph distinction (slide 7)
- Six-condition qualifying test (slide 8) — verbatim from the presenter's own slide
- Shopify worked example and Diamond Pattern (slides 9-10)
- Three ready-made pipelines (slide 11)
- Three implementation levels, including named tools LangGraph/AutoGen/n8n/Make/Claude
  Code/Codex/Excalidraw (slide 12)
- Closing call to action: pick one workflow, draw it, run it once (slide 14)

**Fair synthesis (grounded in research, not stated in video):**
- Slide 3 (contested-term framing) and slide 13 (tool status check) are built entirely
  from `research.md`, not the transcript — labeled as such in speaker notes, not
  presented as the presenter's own claim.

**Interpretation requiring softened language (see grill-me validation for full detail):**
- The video's "prompt engineering → context engineering → graph engineering" as a clean
  three-step progression (slide 4) is presenter interpretation, not settled fact —
  contemporaneous reporting describes 4-6 layers (adding harness engineering and loop
  engineering in between) and multiple sources call the whole progression narrative
  contested. Slide 4's caption is rewritten to present this as "one active framing" rather
  than an agreed sequence.

## 7. Content cuts

- All 13 talking-head-only frames and 3 blank-transition frames: no informative content,
  excluded per hyperframe manifest.
- The 2 podcast-intro-bumper frames (decorative brand animation): excluded, no informative
  content and would read as off-brand for a client deck.
- Podcast branding badge ("The Startup Ideas Podcast — Listen on Spotify/Apple") visible in
  the bottom-left of every extracted slide: left in place as part of the extracted evidence
  image (it is baked into the source pixels), but not called out or repeated in any native
  slide text — client-facing captions never mention the podcast, host name, or platform.
- Presenter's name, "the podcast," "this episode," and any other self-referential framing
  from the transcript: excluded from slide text; may appear only in run-report source
  attribution.

## 8. Rebuild instructions for the PPTX builder

- Use the 10 masked PNGs in `extracted/` as the primary evidence visual on slides 4-12,
  each inside a native slide shell (action title above, business-implication strip below,
  footer/page number, no full-bleed image).
- Slides 1, 2, 3, 13, 14 are fully native (no extracted image) — build them as
  title/BLUF/comparison/next-action layouts per `pptx-design-quality` archetypes.
- Editability mode: **hybrid editable** — native titles/callouts/captions/footers on every
  slide, plus source-backed PNG evidence on slides 4-12.
- Do not show timestamps, "transcript," "hyperframe," "YouTube," "Claude," "Codex,"
  filenames, or the podcast name/host anywhere in visible slide text.
- Slide 3 and slide 13 must carry a footnote-style citation line (e.g. "Industry
  reporting, July 2026") since their content is research-derived, not transcript-derived —
  keep the citation client-safe (no internal skill/process names).

## Quality gate check

- Does each slide have a reason to exist? Yes — each advances the arc; none is a raw
  frame dump.
- Can a reader follow the story without the raw source? Yes — assertions carry the logic.
- Are examples specific enough? Yes — Shopify bookkeeping worked example, named tools.
- Is there a clear decision/next action? Yes — slide 14.
- Unsupported claims / internal terms / visible timestamps? Slide 4's caption is the one
  claim requiring a softened rewrite (see grill-me validation); no internal terms or
  timestamps are planned on any client-facing slide.
