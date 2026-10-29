# Recipes: exact commands

Every command was run on 2026-10-26 with gemini-api v0.4.4. `R` is the run folder; `S` is this
skill's folder (`skills/gemini-media-lane`). The checks use `python3 $S/scripts/check_media.py`.

## teaser (video 0:48)

```bash
R=runs/2026-10-26-gemini-media-<slug>; mkdir -p $R; F=<film.mp4>
# 1. Gemini watches the film: teaser line + thumbnail time
gemini-api analyze -i $F "Watch this film. Reply with exactly two lines. Line 1: one sentence \
(max 22 words) a narrator can say as a 10-second teaser, using only facts the film states. \
Line 2: the timestamp (mm:ss) of the single most striking still frame." --no-interactive > $R/teaser-analysis.txt
# 2. Look at that frame; if dim or mid-transition, pick from a contact sheet
ffmpeg -y -loglevel error -ss <mm:ss> -i $F -frames:v 1 $R/thumb.png
ffmpeg -y -loglevel error -i $F -vf "fps=1/5,scale=480:-1,tile=4x2" -frames:v 1 $R/sheet.png
# 3. Omni animates the still (360p ~ $0.34 / 10 s; ~40 s wall time)
gemini-api video "Animate this still into a 10-second teaser shot: slow cinematic push-in ... \
The title text stays sharp and unchanged. No new text." -i $R/thumb.png --resolution 360p \
  --poll-timeout 9m --out $R/teaser-omni --no-interactive
# 4. Narration (spell product names phonetically if the voice mangles them)
gemini-api tts "<line 1>" --voice Charon --out $R/teaser-voice.wav --no-interactive
# 5. Mix: narration at 1 s over the clip's own ambience, 10 s total
ffmpeg -y -loglevel error -i $R/teaser-omni.mp4 -i $R/teaser-voice.wav -filter_complex \
 "[0:a]volume=0.5[bed];[1:a]adelay=1000|1000,apad[v];[bed][v]amix=inputs=2:duration=first:dropout_transition=0,loudnorm=I=-16:TP=-1.5[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 160k -t 10 -movflags +faststart $R/teaser.mp4
# 6. Checks
python3 $S/scripts/check_media.py av $R/teaser.mp4 --duration 10
gemini-api transcribe -i $R/teaser.mp4 --format text --out $R/teaser.check.txt --no-interactive
ffmpeg -y -loglevel error -i $R/teaser-omni.mp4 -vf "fps=1,scale=320:-1,tile=5x2" -frames:v 1 $R/omni-sheet.png  # look for re-lettered text
```

If the narration runs longer than about 8.5 s, shorten the line instead of extending the clip.

## music (video 4:45)

```bash
gemini-api music "Upbeat modern background music for a product launch video" --out $R/launch-music --no-interactive
python3 $S/scripts/check_media.py av $R/launch-music.mp3 --min-duration 60
```
Default model `lyria-3.5`: about 3:00, 44.1 kHz stereo, 192 kb/s MP3, about 35 s to make.
`-m lyria-3-clip-preview` makes short clips.

## banner (video 5:03)

Default: Gemini makes text-free art, and code sets the words (proven on the DG32-2DOM cards, 2026-10-26).

```bash
# 1. Text-free art. Square layout: art fills the lower part. Landscape: art fills the right side.
gemini-api image "<subject, palette, motif> on a dark navy background, cinematic lighting. \
No text, no letters, no numbers, no logos anywhere." \
  --aspect-ratio 1:1 --image-size 2K --out $R/art --no-interactive      # 16:9 for landscape
python3 $S/scripts/check_media.py textfree $R/art.jpg                     # then look at it yourself
# 2. Card: fill the template, render, OCR the text region
python3 $S/scripts/make_card.py --layout square --art $R/art.jpg \
  --title "<TITLE>" --tagline "<TAGLINE>" --out $R                        # or --layout landscape
```

| Layout | Canvas | Art placement | OCR region |
|---|---|---|---|
| `square` | 1080×1080 (LinkedIn/IG feed) | lower 640 px, top edge faded | `0,0,1,0.42` |
| `landscape` | 1200×627 (LinkedIn link/post) | right 640 px, left edge faded | `0,0.25,0.52,0.75` |

`make_card.py` writes `card-<layout>.html` (the editable source), `art.jpg` and `card-<layout>.png`.
To change the words, edit the HTML and re-render with
`node ~/.claude/skills/ai-graphics/scripts/html_to_png.mjs card-square.html card-square.png 1080x1080`.
It is free and deterministic. If the art's subject sits off-centre, adjust `background-position`
in the HTML.

Only on request: model-drawn text, i.e. the text inside the image prompt ("Large title text reading
exactly: X ... in a rounded sans-serif where O is a perfect circle ... no punctuation"), then
`check_media.py ocr $R/banner.jpg "X" "Y" --region ...`. In testing it read "D0M" for "DOM" and added
full stops, and the square version was OCR-inconclusive at 3 of 4 scales.

Gemini outputs a 2752×1536 (16:9) or 2048×2048 (1:1) JPEG. Supported ratios are 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9, 1:8, 8:1, 1:4 and 4:1.

## research-page (video 6:17)

```bash
# 1. Start research (standard agent, $1-3 typical)
gemini-api agent run "<question>. Cite sources and say which figures come from vendor marketing." \
  --agent deep-research-preview-04-2026 --background --stream=false --output-format json \
  --jq '.id' --no-interactive > $R/dr-id.txt
# 2. Poll once a minute in a background job (stop after 30 checks)
ID=$(cat $R/dr-id.txt); for i in $(seq 1 30); do
  s=$(gemini-api agent status "$ID" --stream=false --output-format json --jq '.status' --no-interactive | tr -d '"')
  echo "$(date +%T) $s" >> $R/dr-poll.log
  case $s in completed|failed|cancelled) gemini-api agent status "$ID" --stream=false --output-format json --no-interactive > $R/dr-result.json; break;; esac
  sleep 60; done
# 3. Meanwhile: page media, all from gemini-api
gemini-api image "<hero brief>. No text, no logos, no letters anywhere." --aspect-ratio 16:9 --image-size 2K --out $R/site/media/hero --no-interactive
gemini-api video "<slow push-in on the hero>. No text." -i $R/site/media/hero.jpg --resolution 360p --out $R/site/media/hero-loop --no-interactive
gemini-api tts "<welcome line from the user's source>" --voice Charon --out $R/site/media/welcome.wav --no-interactive
gemini-api music "Calm modern ambient background music for a technology product website" --out $R/site/media/background --no-interactive
# 4. Write site/index.html around those files (hero bg, muted autoplay loop, welcome + music buttons)
# 5. When the research completes
python3 $S/scripts/dr_extract.py $R/dr-result.json $R/research.md --media $R/site/media
```
Then render `research.md` to HTML, list five findings, carry the report's vendor-marketing
flags, and record the usage (`usage` in `dr-result.json`) with a cost estimate.

A reference run took 6 min 39 s: 948k input tokens (9% cached), 54k output plus thinking, 31
searches, about $2.40. The page was finished before the research.
