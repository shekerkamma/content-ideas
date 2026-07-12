# Video-to-Deck Watch Efficient Smoke Test

Date: 2026-07-03

## Objective

Validate that the updated `watch` skill can support the `video-to-deck` Stage 1
hyperframe extraction path using efficient mode.

## Source

- URL: `https://www.youtube.com/watch?v=1Ynhg4673P4`
- Title: `Fable 5 Disappears In 5 Days — Do These 3 Things First`
- Uploader: `Sean Kochel`
- Duration: `23:57` / `1437.0s`
- Resolution: `1280x720`

## Command

```bash
python3 /home/shekerk/.claude/skills/watch/scripts/watch.py \
  "https://www.youtube.com/watch?v=1Ynhg4673P4" \
  --detail efficient \
  --out-dir runs/2026-07-03-video-to-deck-watch-efficient-test/watch-output
```

## Result

Status: `pass`

- Watch skill version installed: `0.2.0`
- Setup preflight: `can_proceed=true`
- Detail mode: `efficient`
- Extraction mode observed: `keyframe`
- Frame output: `50` selected frames
- Candidate frames: `256`
- Near-duplicates dropped: `106`
- Transcript: `684` segments via captions
- Output directory: `runs/2026-07-03-video-to-deck-watch-efficient-test/watch-output`

## Artifacts

- Metadata: `watch-output/download/video.info.json`
- Captions: `watch-output/download/video.en.vtt`
- Downloaded media: `watch-output/download/video.mp4`
- Frames: `watch-output/frames/`
- Contact sheets:
  - `watch-efficient-contact-01.jpg`
  - `watch-efficient-contact-02.jpg`
  - `watch-efficient-contact-03.jpg`

## Video-to-Deck Finding

The updated watch skill works correctly for the intended efficient hyperframe
pass. It produced a denser and more useful first-pass visual inventory than the
old sparse watch behavior: 50 keyframe-based visual states across the full
23-minute video, with duplicate suppression.

One orchestration gap was found and fixed: `video-to-deck` previously said to
invoke `/watch` but did not explicitly require `--detail efficient`. The skill
now requires `--detail efficient` for the first full-video visual pass, then
uses focused reruns (`--start`, `--end`, `--timestamps`, or higher detail) only
where the initial pass shows that more visual fidelity is needed.

## Caveats

- The source video is 23 minutes long, so 50 frames are still a sparse full-video
  inventory. This is acceptable for first-pass deck planning, but visually dense
  sections should be rerun with focused ranges.
- Efficient mode includes presenter-only frames; `video-to-deck` must still
  classify frames and exclude talking-head-only frames from the client deck.
- The watch output does not itself create a final deck. It validates Stage 1
  extraction and handoff readiness for downstream `video-to-deck` stages.
