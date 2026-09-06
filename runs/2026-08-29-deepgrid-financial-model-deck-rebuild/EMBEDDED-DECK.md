# 104-slide portfolio deck — embedded video, and the video cut

Built 2026-08-31 from the client's Google Slides deck
(`1dy1wAsPAhD5E95gbZz2_x_x8LBBUZgywYR8nNRD3bMs`, 99 slides).

## Why the deliverable is a .pptx

**Google Slides cannot embed video.** Insert > Video offers YouTube, URL, and
Drive — all links. Exporting the deck proved it: **1.5 MB, zero mp4 parts, six
`TargetMode="External"` hyperlinks**. Those six "demonstrations" were poster
images with hyperlinks, so a viewer had to be online, signed in, and click out
to Drive; nothing played in place. Native PPTX embeds, so the deliverable is
PPTX. Deck went 1.5 MB -> 59 MB.

## What was built

| | |
|---|---|
| slides | 99 -> **104** |
| embedded videos | 0 -> **11** |
| external links | 6 -> **0** |
| native shapes / live text boxes | 4,185 / 2,399 |
| flattened slides | **0** |

Five simulator slides added on the deck's own video-interstitial pattern (three
text shapes, full-bleed picture, **no footer and no page number** — so inserting
them renumbered nothing): compute box (25), SoC roadmap ladder (30), shared data
engine (37), memory spectrum (40), SoC4-A far horizon (103).

## Routing: gates, not rebuild

`vault-presales-pptx-pipeline`'s rebuild-by-default rule fires on "client
ready". It was **not** applied, on evidence: the rule exists "to guarantee the
editability contract: native objects, and no flattened slides", and this deck
already satisfies it at 4,185 shapes / 0 flattened against the skill's own
reference build of 690 / 0. A rebuild would re-author the client's design to
reach compliance it already had. The pipeline's *gates* were run instead.

## Gate results

| gate | before | after |
|---|---|---|
| pptx-toolkit structural | valid | valid |
| OpenXML validation | **failed** | passed |
| OfficeCLI `--required` | **26 issues** | **0** |
| design lint errors | 0 | 0 |
| overflow_scan | **4** | **0** |
| internal-language scan | **2** | 0 |
| blank video posters | **1** | 0 |

Defects the gates caught, in order of who caused them:

- **Mine.** Five new slides carried `r:embed="rIdMedia38"` from the template
  while their rels declared `rId5` — a `.replace('<p:nvPr/></p:nvPicPr>', ...)`
  in `build99/add3.py` was a **silent no-op** because `embed99.py` had already
  populated that node, and the call had no assert. OpenXML validation was
  failing on a file already named `-reviewed`.
- **Inherited and multiplied.** The interstitial template's three text boxes run
  4/5/6 pt short; present on the two original Google slides *and* the five
  copies made from them. 21 overflows, fixed by growing boxes, not editing copy.
- **Inherited.** `ppt/media/image3.png` was a **240x240 RGBA image with every
  channel uniformly 0** — a 799-byte blank — so slide 92 rendered empty with no
  poster for PowerPoint to draw a play button over. Replaced with a frame from
  that slide's own embedded video. **Test posters on pixel variance, not file
  size:** a large uniform image would pass a size check.
- **Inherited.** Slides 27 and 42 captioned the clips "Holt narration". Those
  clips are Gemini/Charon; Holt is the explainer video's voice. Both a
  production note (barred from client slides) and factually wrong.

## The video cut

104 slides exceeds the 45-slide Vids cap, so three parts split on section
dividers: **1-30 | 31-62 | 63-104**, each opening on context.

Narration is **authored, not auto-generated**: 104 blocks, 4,809 words —
**87 carried verbatim** from `narration-sku-explainer-87.md` (each used exactly
once, mapped by position and SKU, not by fuzzy score) plus **17 new blocks**
(`media/narration/new-blocks-17.py`). Installed at creation time and verified
30/30, 32/32, 42/42 before generating.

Result: **32:15.6, 149.1 wpm** (target 145-152), no music bed (63 true-silence
windows, 22.4% below -50 dB against a 0.1% with-music baseline), all 11
simulators composited back over the flattened posters.

Two seat geometries: SKU sims at (48,168,800,450) -> `72:252 1200x675`;
interstitials at (192,148,896,504) -> `288:222 1344x756`.
