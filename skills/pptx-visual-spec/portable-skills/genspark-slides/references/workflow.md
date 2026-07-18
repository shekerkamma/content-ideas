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
- Editable PPTX: slower, use Presentations skill; parse HTML text/layout and rebuild as native PowerPoint elements.
