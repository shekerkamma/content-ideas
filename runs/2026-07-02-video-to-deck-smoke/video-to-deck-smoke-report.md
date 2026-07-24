# Video-to-Deck Smoke Test

Date: 2026-07-02

## Input

- URL: `https://www.youtube.com/watch?v=83fWzQSWB10`
- Skill under test: `video-to-deck`
- Test mode: smoke test, sparse full-video frame extraction

## Dependency Check

| Dependency | Status | Notes |
|---|---|---|
| `video-to-deck` | Pass | Repo-local copy exists at `skills/video-to-deck/SKILL.md` |
| `watch` | Pass | Skill resolves and setup is ready |
| `content-research` | Pass | Skill resolves; routes video URLs to `watch` |
| `excalidraw` | Pass | Repo-local portable skill creates `.excalidraw` JSON without requiring live MCP canvas tools |
| `explainer-graphic` | Pass | Skill resolves |
| `architecture-presentation` | Pass | Skill resolves; appropriate for technical/solution architecture only |
| `yt-dlp` | Pass | Installed |
| `ffmpeg` / `ffprobe` | Pass | Installed |

## Watch Execution

Command:

```bash
python3 skills/watch/scripts/watch.py "https://www.youtube.com/watch?v=83fWzQSWB10" \
  --max-frames 12 \
  --resolution 512 \
  --out-dir runs/2026-07-02-video-to-deck-smoke/watch-output \
  --no-whisper
```

Result: Pass after network escalation.

The first sandboxed run failed because DNS resolution for `www.youtube.com` was blocked. The escalated run succeeded.

Extracted video metadata:

- Title: `AI Agents are the new SaaS`
- Uploader: `Greg Isenberg`
- Duration: `26:03`
- Resolution: `1280x720`
- Transcript: `603` caption segments via native captions
- Frames: `12` JPG frames at 512px wide

Artifacts:

- Frames: `runs/2026-07-02-video-to-deck-smoke/watch-output/frames/`
- Captions: `runs/2026-07-02-video-to-deck-smoke/watch-output/download/video.en.vtt`
- Metadata: `runs/2026-07-02-video-to-deck-smoke/watch-output/download/video.info.json`
- Video file: `runs/2026-07-02-video-to-deck-smoke/watch-output/download/video.mp4`

Important note: this is a 26-minute video. The smoke run intentionally sampled only 12 frames, so it validates ingestion but is too sparse for high-fidelity visual reconstruction. Use focused timestamp ranges for Excalidraw recreation.

## Routing Validation

The updated `video-to-deck` visual routing rule is working for this input.

Selected visual route: `excalidraw`

Reason:

- The video is a conceptual/business-framework talk.
- The sampled frame shows a conceptual unit-economics comparison, not a technical architecture diagram.
- The transcript is about the business playbook for "agents as the new SaaS": product-is-the-job, workflow selection, shadowing humans, packaging, pricing, distribution, and 30-day plan.
- Under the updated rule, conceptual models and business workflows should route to Excalidraw by default.

Rejected route:

- `architecture-presentation` / `.drawio`

Reason:

- The video does not primarily describe a software architecture, integration map, cloud topology, deployment model, or component-level system design.

## Excalidraw Runtime Resolution

Initial blocker:

- The first exposed Excalidraw skill expected a live Excalidraw MCP server and tools such as canvas creation, screenshot, and element creation.
- Tool discovery in this Codex session did not expose Excalidraw MCP tools.

Resolution:

- `skills/excalidraw` was converted from the live-MCP Claude symlink into a repo-local portable Excalidraw skill.
- The portable skill creates standard `.excalidraw` JSON files directly, which can be opened at excalidraw.com or uploaded later.
- Live MCP canvas tools are now optional, not required.

Validated artifact:

- `runs/2026-07-02-video-to-deck-smoke/agents-new-saas-concept.excalidraw`

Validation:

- Parsed successfully with `python3 -m json.tool`.
- Represents the conceptual "AI Agents are the new SaaS" model as editable Excalidraw elements.

## Recommended Focused Follow-Up

For a real Excalidraw recreation, run focused capture on the visual sections instead of sparse full-video sampling. Useful ranges from the transcript:

```bash
python3 skills/watch/scripts/watch.py "https://www.youtube.com/watch?v=83fWzQSWB10" \
  --start 00:00 \
  --end 01:30 \
  --max-frames 60 \
  --resolution 1024 \
  --out-dir runs/2026-07-02-video-to-deck-smoke/focused-0000-0130
```

```bash
python3 skills/watch/scripts/watch.py "https://www.youtube.com/watch?v=83fWzQSWB10" \
  --start 04:12 \
  --end 07:16 \
  --max-frames 80 \
  --resolution 1024 \
  --out-dir runs/2026-07-02-video-to-deck-smoke/focused-0412-0716
```

## Verdict

Smoke test result: pass for the Codex-compatible path.

- Pass: skill discovery, dependency resolution, video download, caption extraction, frame extraction, and visual route decision.
- Pass: Excalidraw output generation via portable `.excalidraw` JSON.
- Note: live Excalidraw canvas screenshot iteration remains unavailable unless an Excalidraw MCP server is separately installed and exposed to Codex.
