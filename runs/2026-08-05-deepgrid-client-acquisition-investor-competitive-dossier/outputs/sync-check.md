# Sync check — PPTX ↔ HTML twin

Generated 2026-08-05. The HTML twin is generated *from* the built
PPTX, so drift is structurally prevented rather than asserted.

| Check | PPTX | HTML | Result |
|---|---|---|---|
| Slide count | 21 | 21 | PASS |
| Titles present in HTML | 21 | 21 | PASS |
| Speaker notes carried | 21 | 21 | PASS |
| External resource refs | 0 | 0 | PASS |
| Theme-aware CSS | yes | yes | PASS |

**5/5 checks pass.**

## Artifact digests

- `DeepGrid-client-acquisition-v2-reviewed.pptx` — sha256 `fd5ff87ecd7edf549f7b8e0849aa70f8`
- `client-package/site/index.html` — sha256 `99054727976910511d2cb27d1edccc76`
- shared content digest — `1148de662fa2ce79ec46324d37e1200a`

## Known differences (intentional)

- HTML renders each slide as an embedded JPEG (1280px, q78) rather than as editable shapes.
  The PPTX remains the editable artifact; the HTML is a read-only twin.
- HTML adds a table of contents, which has no PPTX equivalent.
- Native charts are editable in the PPTX and flattened in the HTML render.