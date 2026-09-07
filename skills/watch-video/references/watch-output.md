# Watch Output Contract

Expected output:

- `report.md`: markdown summary from upstream `/watch`
- `watch/`: extracted frames, metadata, subtitles, and downloaded media artifacts

Downstream extraction should look for:

- source title
- uploader/channel
- duration
- frame paths with timestamps
- transcript fenced block
- visually important frame timestamps

For decks:

1. Convert the report into a slide outline.
2. Use selected frame paths as visual references.
3. Send a clear preview request to Genspark AI Slides.
4. Capture Genspark HTML through `genspark-slides`.
5. Rebuild client-ready outputs with `presentations:Presentations`.
