# Troubleshooting gemini-api

| Symptom | Cause | Fix |
|---|---|---|
| `gemini-api: command not found` | not installed, or not on PATH | Install the pinned v0.4.4 from GitHub Releases into `~/.local/bin` after `sha256sum -c checksums.txt`. Don't use `curl \| bash` (it installs the latest). |
| exit 3 / 401 / 403 | no key, or the wrong one | `gemini-api whoami` should show an api-key source. On WSL `GEMINI_API_KEY` (or `GOOGLE_GENERATIVE_AI_API_KEY`); on Windows, Credential Manager (`auth login --api-key`). A Google AI Pro sign-in token is refused (403 `ACCESS_TOKEN_SCOPE_INSUFFICIENT`). |
| exit 2 on `analyze` | `--stream` is not an `analyze` flag | Drop it. |
| 400 `invalid_request` on `image` | unsupported `--aspect-ratio` (e.g. 16:10) or `--output-mime-type image/png` | Use a supported ratio; accept JPEG output. |
| 400 `content_blocked` on `music` | Lyria's filter, which gives no reason | Simplify the prompt once (drop negations such as "no vocals"). If it's blocked again, report it. |
| A file appears in the repo root | `transcribe` or another command run without `--out` | Move it into the run folder; always pass `--out`. |
| The research report starts mid-section | only one text part was read | `scripts/dr_extract.py` joins every `model_output` text part in order. |
| A garbled word in an image | 1K default output, or an edit of an existing image | Use `--image-size 2K`; generate rather than edit; check with OCR. |
| Omni re-letters a product marking | it redraws the scene | Use the clip as a social teaser only, or pick a still without small product text. |
| Windows: `--api-key $env:X` stores the next flag as the key | `WSLENV` passing is dead in this harness, so `$env:X` was empty | Pass the key through a mode-600 temp file read over `\\wsl.localhost`, then delete it. |
| Windows: `localhost:<port>` times out | Windows → WSL localhost forwarding is broken here | Open previews at `http://$(hostname -I \| awk '{print $1}'):<port>/`. |
| proof-of-done: exit 5, "no tests ran" | the shell was left in a run folder | `cd` back to the repo root and rerun. |
