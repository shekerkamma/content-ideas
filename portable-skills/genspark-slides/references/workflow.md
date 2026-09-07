# Genspark Slide Recovery Notes

Genspark agent links may show a conversation first. The generated deck often appears behind a `View` button and a route like:

`https://www.genspark.ai/autopilotagent_viewer?id=<agent-id>`

The useful network calls look like:

`https://www.genspark.ai/api/files/s/<slide-id>?pageIndex=<zero-based-index>&scale=<scale>`

Despite the file API naming, the response can be complete HTML for a slide. Save it as HTML and render locally.

Common signs:

- Page title starts with `Genspark - Slides:`.
- Viewer request logs show 22 or more `/api/files/s/...` calls.
- `scale=0.584375` requests are thumbnail/preview scale; change to `scale=1`.
- If direct HTTP fetch hits Cloudflare, use a real browser session and browser-context request cookies.

Output choices:

- Image-based PPTX: fastest, visually faithful, text is not editable.
- Branded/hybrid PPTX: write `genspark-handoff.json`, then use
  `genspark-branded-deck` with recovered HTML and renders as reference.
- Fully native/client-ready PPTX: continue from the branded handoff into
  `branded-pptx-deck` or `vault-presales-pptx-pipeline`; recovered Genspark
  HTML/renders are references, not the final slide objects.
