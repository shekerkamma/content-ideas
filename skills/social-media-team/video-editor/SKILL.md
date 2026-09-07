---
name: video-editor
description: "Auto-edit video footage via Descript API: remove filler words, add captions to intro, insert B-roll, apply brand layers."
user-invocable: false
allowed-tools: Bash, Read, Write, Edit, Agent, WebFetch, WebSearch
---

# Video Editor Agent

Automates video editing through the Descript API and its Underlord AI.
Handles filler word removal, intro enhancement, captions, B-roll, and brand styling.

## Inputs

- Video file path (raw footage)
- `script.md` — today's script (for alignment and section markers)
- `config.json` — brand colors, brand font, intro/outro assets
- Descript API key from `.env`

## Process

### Step 1: Upload to Descript

Upload the raw footage to Descript via API:

```bash
curl -X POST "https://api.descript.com/v1/projects" \
  -H "Authorization: Bearer $DESCRIPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "YYYY-MM-DD-video-title",
    "media_url": "[video file URL or upload path]"
  }'
```

**Note**: Descript API may use different endpoints. Check current docs via:
```
WebFetch https://docs.descript.com/api
```
Adapt all API calls to match the current Descript API specification.

### Step 2: Filler Word Removal

Use Descript's Underlord AI to remove filler words:

```
Underlord prompt: "Remove all filler words including 'um', 'uh', 'like', 'you know',
'basically', 'actually', 'so', 'right', repeated words, and false starts.
Keep the speech natural — don't create jarring cuts."
```

### Step 3: Gap Compression

Remove dead air and long pauses:

```
Underlord prompt: "Compress all gaps between words to a maximum of 0.5 seconds.
Remove long pauses but keep natural breathing room. Do not speed up speech —
only remove silence."
```

### Step 4: Intro Enhancement (First 30 Seconds)

The intro section gets special treatment:

#### 4a: Captions (Intro Only)
Add animated captions to the first 30 seconds ONLY (not the whole video):

```
Underlord prompt: "Add word-by-word animated captions to the first 30 seconds.
Style: [brand font], [brand color] text, bold keywords, centered bottom third.
Do NOT add captions after the 30-second mark."
```

#### 4b: B-Roll Layers
For `[SHOW: ...]` cues in the script's intro section:

```
Underlord prompt: "At the following timestamps, overlay B-roll:
- [timestamp]: [description from script SHOW cue]
Use Descript's stock media or generate AI B-roll for each cue."
```

If Descript can generate AI B-roll, use it. Otherwise, search Descript's
stock library with relevant keywords.

#### 4c: Subtle Background Music
Add quiet background music to the intro:

```
Underlord prompt: "Add subtle, low-energy background music to the first 30 seconds.
Volume: 15-20% of voice level. The voice must be clearly dominant.
Music style: modern, upbeat but not distracting. Fade out at 30 seconds."
```

#### 4d: Motion/Animation
Make the intro visually dynamic:

```
Underlord prompt: "Add subtle zoom animations to the first 30 seconds.
Slow push-in on face during hook (0-5s), cut to screen recording during
demo tease (18-25s). Keep transitions smooth, not flashy."
```

### Step 5: Intro & Outro Bumpers

If intro/outro assets are configured:

```
Underlord prompt: "Add the intro bumper [asset path] at 0:00 (before the hook).
Add the outro bumper [asset path] after the CTA at the end.
Transition: cross-dissolve, 0.5 seconds."
```

### Step 6: Brand Color Grading (Optional)

If brand requires consistent color treatment:

```
Underlord prompt: "Apply a subtle color grade to match brand aesthetic:
warm tones, slightly desaturated, consistent exposure throughout."
```

### Step 7: Export & Review

Export the edited video:

```bash
curl -X POST "https://api.descript.com/v1/projects/PROJECT_ID/export" \
  -H "Authorization: Bearer $DESCRIPT_API_KEY" \
  -d '{
    "format": "mp4",
    "quality": "high",
    "resolution": "1080p"
  }'
```

### Step 8: Output

Save to `~/social-media-content/YYYY-MM-DD/`:
- `edited-video.mp4` — the final edited video
- `edit-log.md` — what was changed:

```markdown
# Edit Log — YYYY-MM-DD

## Edits Applied
- **Filler words removed**: X instances
- **Gaps compressed**: X seconds of dead air removed
- **Intro captions**: 0:00 - 0:30 (word-by-word animated)
- **B-roll inserted**: [list of timestamps and descriptions]
- **Background music**: 0:00 - 0:30, volume 18%
- **Intro bumper**: added at 0:00
- **Outro bumper**: added at end

## Timeline
- Original duration: X:XX
- Edited duration: X:XX
- Time saved: X:XX

## Review Status
- [ ] Creator approved
- [ ] Ready to upload
```

## YouTube Upload (Optional — requires creator approval)

If the creator has enabled auto-upload in config:

```bash
# Upload to YouTube via YouTube Data API v3
curl -X POST "https://www.googleapis.com/upload/youtube/v3/videos?part=snippet,status" \
  -H "Authorization: Bearer $YOUTUBE_OAUTH_TOKEN" \
  -F "video=@edited-video.mp4" \
  -F 'snippet={"title":"[title]","description":"[description]","tags":["tag1","tag2"],"categoryId":"28"}' \
  -F 'status={"privacyStatus":"private"}'
```

**Always upload as PRIVATE first** — the creator reviews and publishes manually.
