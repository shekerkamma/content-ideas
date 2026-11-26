# Level 2: real footage, plus graphics, voice and music

Take real footage, cut it down, and add to it. Subtract first, then add.

Our example turned a 104-second event recap into a 27-second promo on a 120 BPM grid, with code-built graphics in the event's own look, an AI voiceover and an AI music bed. It took about 55 minutes and 15 Higgsfield credits (four voice takes, two music takes, a few transcriptions). No AI video was generated: real footage opened it.

## The order of work

1. Watch the footage.
2. Write the cut list. This is the storyboard: stop for approval.
3. Cut (subtract).
4. Write the voiceover from the footage's own facts, and generate it.
5. Build the graphics as a page and render them with a transparent background.
6. Lay the graphics over the cut.
7. Generate music at the exact length, mix, master.

## 1. Watch the footage

You cannot play video, so turn it into things you can read. Never move or change the source: work on a small proxy and keep the original for the master.

```bash
ffmpeg -i source.mp4 -vf scale=-2:540 -c:v libx264 -crf 23 -c:a aac work/proxy.mp4
python3 scripts/frame_sheet.py work/proxy.mp4 work/all.jpg --every 1 --columns 8 --width 320
python3 scripts/frame_sheet.py work/proxy.mp4 work/shot-b.jpg --from 14 --to 17 --every 0.2
python3 scripts/study_video.py work/proxy.mp4 work/study        # finds the cuts for you
```

One frame a second to find candidates, then every 0.2 to 0.4 seconds around each candidate to find clean in and out points.

Transcribe the sound so the voiceover only uses real facts (Higgsfield `speech2text`, or any transcriber you have).

Note as you go:

- the strongest moments;
- **burned-in text**: titles and captions already in the footage. Choose in and out points between them, crop them out, or reuse one on purpose if it is the piece's own line and lands where you need it;
- natural wipes (leaves, a person crossing the lens) that can hide a join;
- the footage's own look: its colours, its type, its logo. Sample these; do not guess them.

## 2. The cut list

```json
{
  "fps": 25,
  "segments": [
    {"id": "A", "t": [0.0, 3.2], "src": [1.2, 3.0], "what": "aerial over the city, slowed", "crop": [0.22, 0.34, 0.64], "interp": true},
    {"id": "B", "t": [3.2, 4.0], "src": [3.0, 3.8], "what": "the same aerial at full speed"},
    {"id": "P", "t": [23.0, 27.0], "src": [95.6, 95.6], "what": "last frame held behind the end card", "freeze": true}
  ]
}
```

- Put cuts on the music's grid. At 120 BPM a beat is 0.5 s, so every cut lands on a multiple of 0.5.
- `crop` pushes in and keeps burned-in titles out of frame.
- `interp` makes smooth slow motion. Use it on one or two shots: it is slow.
- Write `what` for every shot. The list should read as the story.

Show the list with a sheet of the chosen frames, and wait for approval.

## 3. Cut

```bash
python3 scripts/cut_footage.py cutlist.json work/proxy.mp4 out/cut-1080.mp4
python3 scripts/cut_footage.py cutlist.json work/proxy.mp4 out/before-raw-cut.mp4 --audio    # "subtract only", for comparison
python3 scripts/cut_footage.py cutlist.json source.mp4 work/base-4k.mp4 --width 3840 --height 2160   # the master
```

If the source is already 4K, cut the master straight from it. Upscaling a 1080p render of 4K footage only loses detail.

## 4. Voiceover

- Write it to the cut: about 2.2 to 2.3 words a second while talking, with air between lines. Our 27 seconds held 44 words.
- **Use only facts that are in the footage**: what its narrator says and what its text shows. Invent nothing. Add no names, titles or quotes for anyone on screen.
- Generate the whole script as **one take**, with a blank line between lines, so the voice is the same throughout. Spell out numbers the way they should be said.
- Try three or four voices. You cannot hear them, so measure (pitch, range) and transcribe each take back to check the words, then tell the person to listen before using it.
- Split the take at its pauses and place each line on its shot. Never stretch a line to fit. If it does not fit, cut words.

```bash
python3 scripts/split_takes.py sound/vo/take.mp3 sound/vo/lines --expect 12
```

A line that was recorded can still be dropped in the mix to give the music room. Say which.

## 5. Graphics

Build them as a time-driven page (`level-1-code.md`, `templates/ad-page.html`) in the footage's own look, and render with a transparent background.

- **Into footage and back out.** Open on pure animation that becomes the footage: a logo's opening is a window onto the first shot from frame one, then grows until the shot fills the frame. Close the same way in reverse: the last shot shrinks into the logo, and the end card builds around it. No cross-dissolve at either end.
- **Lower thirds**: a thin rule that draws on, the words sliding up.
- **Counters** tick up to a real number from the footage, then roll to the short form (the old line leaves upward as the new one arrives from underneath).
- **Text**: each word slides up in place inside a mask, blurred to sharp. No bounce, no scale pops.
- **Look**: colours sampled from the footage, and open-licence fonts that match its type pairing.
- **Logo**: keyed or traced from the footage's own clean frame, not redrawn from memory. Rebuild it as vector shapes measured from that frame so it stays sharp when it fills the screen.
- Say only what the footage shows. If no date appears in the footage, the end card has no date.

```bash
node scripts/render_page.mjs build/gfx.html --video work/gfx.mov --alpha --fps 25 --scale 2
```

## 6. Graphics over the cut

```bash
ffmpeg -i work/base-4k.mp4 -i work/gfx.mov -filter_complex "[0:v][1:v]overlay=format=auto,format=yuv420p" \
  -c:v libx264 -crf 14 -preset slow -colorspace bt709 -color_primaries bt709 -color_trc bt709 -an out/picture.mp4
```

If the footage itself has to move with a graphic (shrinking into a logo), have the page export that transform per frame and apply it to the footage before the overlay, so the two stay locked.

Large flat colour gradients can band after a platform re-encodes them. A very faint noise over the graphic's flat areas prevents it.

## 7. Music, mix, master

- Generate the music at the exact length of the cut, instrumental, with the tempo and the structure written into the prompt second by second (see `prompt-templates.md`). Make two takes.
- Check the tempo of what came back against your grid. Ours arrived at about 118 to 120 BPM and lined up after a 60 ms nudge (`"start": 0.06` in the cue sheet).
- Duck the music about 8 dB under the voice, quick down and slow back up.
- A few quiet effects on the graphics' big moves only: the logo opening, the landing, a counter's roll, the close. The music carries the energy.
- Master to -14 LUFS, -1 dB true peak.

```bash
python3 scripts/mix_sound.py sound/cues.json sound/mix.wav --events sound/events.json
python3 scripts/master_audio.py sound/mix.wav sound/master.wav --video out/picture.mp4
```

### Real sound from the footage

Often it cannot be reused: a recap's audio is a finished mix with a narrator and music all the way through, so there is no clean room tone or applause to lift out, and what you could lift carries the old music in the wrong key and tempo. Say so if that is the case. One short moment of real sync sound (a host's line over the last shot) can still be worth putting back.

## What to tell the person

- Which shots were kept, which were left out and why (titles burned in, name graphics).
- That no names, titles or quotes were added for anyone in the footage, and no faces were edited.
- Whose footage and marks it uses. If they are not the person's own, it is a spec piece: see `honesty.md`.
- That a vertical version needs its own layout pass. Graphics laid out for 16:9 do not survive a crop.
