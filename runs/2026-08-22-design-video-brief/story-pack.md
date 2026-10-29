# Story pack — /design video brief

Produced with the `story-architect` method before rebuilding the deck. The first
build skipped this step, which is why it read as a chronological list of
features rather than an argument.

## 1. BLUF

`/design` removes the export round-trip and makes hand-editing faster than
prompting — but the canvas is a **document, not a shared workspace**, so nothing
you change reaches the agent until you press Save.

## 2. Audience decision

Adopt `/design` for UI exploration, and adopt one habit with it: **Save before
you speak.**

## 3. Tension

The canvas feels native and direct — you click an element, drag a colour slider,
and the change appears instantly. That immediacy is the trap: it implies the
agent sees what you see. It does not. The video's own demo breaks on exactly
this, on camera, and the presenter spends thirty seconds not knowing why.

## 4. Argument arc

| Beat | Role | Lands |
|---|---|---|
| 1 | Context | Designing with an agent cost a round-trip you performed by hand |
| 2 | Context | One command collapses it into the project folder |
| 3 | Proof | Five directions from one prompt — you compare instead of overwrite |
| 4 | Proof | Two clicks beat a model turn; this is the real unlock, not generation |
| 5 | **Turn** | The site ships without the edits. The demo breaks. |
| 6 | Explanation | The canvas is a published document; edits are local until Save |
| 7 | Action | Prompt for structure, click for style, Save before you speak |

## 5. Slide spine

| # | Assertion | Role | Evidence | Visual |
|---|---|---|---|---|
| 1 | The canvas is native now. Your edits still aren't. | Cover | — | Midnight field, one rule |
| 2 | One command, one habit, and the habit is the hard part | Exec summary | 00:07, 12:02 | Thesis slab + 4 metrics |
| 3 | Design used to cost a round-trip you made by hand | Context | 02:09–02:34 | Three handoff cards |
| 4 | Now it is one command inside the project folder | Context | 03:04–03:48 | Four-node chain + constraint |
| 5 | Five directions arrive at once, so you compare instead of overwrite | Proof | 04:01–04:41, 06:22 | Three cards |
| 6 | Clicking beats prompting — that is the actual unlock | Proof | 07:13–09:09, 08:20 | Dark; by-hand vs by-prompt |
| 7 | Then the site shipped without his edits | **Turn** | 11:38–11:53 | Dark; single failure statement |
| 8 | Because the canvas is a document, not a shared workspace | Explanation | 12:02 + build check | Two-panel mental model |
| 9 | Two framings in the video will mislead you | Analysis | build check | Three cards |
| 10 | Prompt for structure, click for style, Save before you speak | Action | — | Ask panel + adoption list |

## 6. Evidence map

- **Direct evidence** (the presenter's own words or actions on camera): the old
  share-and-copy workflow; five variations from one prompt; iterating by artboard
  number; the properties panel and colour picker; the localhost site; the missing
  edits and the un-pressed Save.
- **Fair synthesis**: that comparison-not-overwrite is the reason a canvas beats
  tabs; that direct manipulation, not generation, is the durable advantage.
- **Interpretation** (slide 9 only, and labelled as checked against the build):
  the canvas is a published artifact; edits live in the page state until Save
  republishes; it is an early preview whose editor never updates after publish.

## 7. Content cuts

- **Setup mechanics beyond one line.** Opening a folder and typing a command does
  not need its own beat; it is context, not argument.
- **The subscribe break (06:39).** Presenter housekeeping.
- **Visible timestamps on slide faces.** Moved to speaker notes — the
  `story-architect` quality gate prohibits them, and they made every slide read
  as a transcript row.
- **The blue-styling variant detail.** One example of iteration is enough; two is
  a demo recap.

## 8. Rebuild instructions

1. Cut from twelve parallel slides to ten with a turn at slide 7.
2. Promote the broken demo from a feature card to the deck's pivot, on its own
   dark slide.
3. Add the mandatory executive summary (slide 2) and conclusion (slide 10).
4. Move every timestamp into speaker notes; keep slide faces assertion-only.
5. Give slide 8 a mental model, not a restatement: document vs workspace.
