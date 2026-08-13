# DeepGrid v14 native archetype contract

## Design authority

- Source: `C:/Users/sheke/OneDrive/Desktop/DeepGrid-India-ADAS-Competitive-Strategy-v14-DesignContract-reviewed.pptx`
- Source SHA-256: `69f99f6fdcf5d7db18763d41878683282af31f718ef19296b6c864cf18ae5df5`
- Source scope: 74-slide reviewed DeepGrid competitor-strategy deck.
- Portable derivative: `assets/slide-archetypes/deepgrid-v14-native-archetypes-draft.pptx`
- Derivative SHA-256: `61fb7fff30a50643277c8b3fb0e5c8f983fad516acbb6ef4550ee2be04cf674a`

The portable derivative keeps the source theme/master basis and the v14 native rendering grammar,
but replaces client claims with synthetic content. It is an implementation reference, not reusable
competitive evidence and not a reviewed client deliverable.

## Nine design families

1. `cover` — answer, supporting logic, three-part decision panel, and decision rail.
2. `ladder` — evidence rows, provenance status, bounded verdict, and falsifier.
3. `table` — analytical lens, evidence, boundary/status, and conclusion.
4. `funnel` — progressively narrower claims as accountability rises.
5. `matrix` — four comparable evidence fields plus explicit comparison rule.
6. `heatmap` — competitor threat across buying arenas with independent evidence encoding.
7. `mechanism` — four-step causal chain ending in a decision gate.
8. `timeline` — evidence events, early signals, counterargument, and sequence.
9. `waterfall` — directional bridge from evidence accumulation to commitment release.

## Rebuild

```bash
python3 skills/compound-competitor-analysis-pptx/scripts/build_v14_archetype_template.py \
  /mnt/c/Users/sheke/OneDrive/Desktop/DeepGrid-India-ADAS-Competitive-Strategy-v14-DesignContract-reviewed.pptx \
  skills/compound-competitor-analysis-pptx/assets/slide-archetypes/deepgrid-v14-native-archetypes-draft.pptx
```

The builder uses `scripts/v14_design_renderer.py`, a sanitized portable form of the v14 renderer.
It starts from the supplied v14 presentation to retain the theme and layouts, deletes all client
slides, and constructs nine native synthetic archetypes.

## QA status

- Reviewed v14 design authority: passed Windows OfficeCLI + Microsoft PowerPoint native rendering
  across all 74 slides. The Desktop source and run artifact are byte-identical at SHA-256
  `69f99f6fdcf5d7db18763d41878683282af31f718ef19296b6c864cf18ae5df5`.
- Prior native contact sheet: `runs/2026-08-13-deepgrid-india-adas-competitor-analysis/client-package/qa/officecli/native-contact.png`,
  SHA-256 `ee5bbe5ac0851cace0c8e7a26734cb211d99ecec3c6944f21d2dac6fa5453e2f`.
- Prior native review result: no visible clipping, off-slide content, missing content, or broken
  analytical layouts; the nine archetype families therefore inherit a PowerPoint-tested design
  grammar, not an unvalidated template concept.
- OpenXML validation: passed.
- OfficeCLI 1.0.143 issue scan: zero issues.
- OfficeCLI HTML render: generated and manually inspected across all nine slides.
- Native-object editability: each slide contains multiple editable PowerPoint shapes and text boxes.
- Exact sanitized derivative native contact sheet: not regenerated in the latest session. A current
  COM `Presentations.Open` call returned HRESULT `0x80048240` while the reviewed source deck was open.
  This is a session-specific rerender blocker, not evidence that PowerPoint native QA is unavailable
  or that the v14 design system was never reviewed.

The portable derivative remains `draft` only because its exact nine-slide binary has not received a
fresh native contact sheet. Do not downgrade the reviewed status of the 74-slide v14 design authority.
