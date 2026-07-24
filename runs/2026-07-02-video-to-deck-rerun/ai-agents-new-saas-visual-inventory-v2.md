# AI Agents Are The New SaaS - Visual Inventory V2

Source video: `https://www.youtube.com/watch?v=83fWzQSWB10`

Source media:

- Cached MP4: `runs/2026-07-02-video-to-deck-smoke/watch-output/download/video.mp4`
- Old sparse watch frames: `runs/2026-07-02-video-to-deck-smoke/watch-output/frames/`
- Dense 10-second frames: `runs/2026-07-02-video-to-deck-rerun/dense-frames-10s/`
- Scene-change frames: `runs/2026-07-02-video-to-deck-rerun/scene-frames/`

## Correction

The earlier manifest was too sparse. It relied on 12 cached watch frames and
missed several distinct visual beats from the full video. The corrected deck
must use the denser frame inventory before building slides.

## Distinct Visual Beats

| Beat | Representative frames | Type | Required deck treatment |
|---|---:|---|---|
| SaaS market growth / public cloud application services chart | dense `0001` | chart/evidence | Recreate as chart or cite as market-context visual; do not ignore |
| SaaS logos / previous SaaS winners | dense `0002` | context collage | Use as context beat or replace with clean native logo/text comparison |
| Building agents is the new SaaS | dense `0004`, scene `0007`, `0028` | diagram | Recreate as clean Excalidraw/native diagram |
| SIT software map | dense `0006`, scene `0019` | framework/table | Recreate as structured quadrant/table, not a screenshot |
| Unit economics crush | dense `0007`, scene `0021` | diagram/table | Recreate as Excalidraw/native diagram |
| Pick a workflow with a paycheck attached | dense `0026`-`0037`, scene `0011`, `0041` | diagram/scorecard | Recreate once; mark remaining repeats duplicate |
| Slang AI restaurant example | dense `0018`-`0019`, scene `0029`-`0030` | product example/evidence | Include as evidence/example slide or synthesized case card |
| Home-services/operator examples | scene `0032`-`0035` | evidence imagery | Include as grouped vertical evidence; do not redraw faces exactly |
| Samday/contact-center example | dense `0023`, scene `0038`-`0039` | product example/evidence | Include as evidence/example slide or synthesized case card |
| Founder-sized wedges | dense `0015`-`0021`, scene `0009`, `0036` | diagram | Recreate as clean vertical wedge map |
| Shadow the human before you build | dense `0038`-`0055`, scene `0013` | diagram | Recreate once; mark remaining repeats duplicate |
| Build the smallest useful agent | dense `0058`-`0069`, scene `0043`, `0045` | diagram/process | Recreate as its own slide |
| Architecture-pattern reference | dense `0070`, scene `0046` | external reference | Account for as supporting reference; do not over-copy |
| Agentic workflows text slide | dense `0071`-`0072`, scene `0047` | text slide | Recreate as concise native slide, not a pasted paragraph |
| Wrapper makes it SaaS | dense `0078`-`0091`, scene `0015`, `0049` | diagram | Recreate once; mark repeats duplicate |
| Sell the pilot like labor, then productize | dense `0096`-`0111`, scene `0017`, `0051`, `0053` | diagram | Recreate once; mark repeats duplicate |
| Own the workflow | dense `0113`-`0123`, scene `0055` | diagram/process | Recreate as its own slide |
| Presenter-only close | dense `0124`-`0156`, old frames `0010`-`0012` | talking head | Exclude from main deck |

## Rebuild Rule

The corrected deck should be rebuilt from this inventory, not patched from the
earlier 10-slide draft.

Minimum slide spine:

1. Thesis: agents are the new SaaS, but only through workflow ownership
2. Market context: SaaS growth and prior software winners
3. Why agents: unit economics compress
4. Where to search: workflow with a paycheck attached
5. Wedge examples: restaurants, home services, property services, contact center
6. Observe before building: shadow the human
7. Build small: draft, triage, coordinate, act
8. Workflow architecture: sequential/hierarchical agentic workflows
9. Wrapper: control room creates trust
10. Commercialization: sell labor-like pilot, then productize
11. Defensibility: own the workflow
12. Artifact/accountability appendix: visual beat to slide/source map

## Google Slides Review Path

Use Google Slides as the visual iteration surface after a rebuilt deck exists:

1. Build a clean local `.pptx` or native slide package from this inventory.
2. Import to Google Slides as native Google Slides.
3. Verify through Google Slides thumbnails after import.
4. Iterate layout in Slides if needed.
5. Export final branded PPTX only after slide-level visual QA passes.

