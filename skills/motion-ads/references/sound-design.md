# Sound design

Sound is the last step, after the picture is approved. It is also where an ad most often goes from good to cheap. Our first product-ad mix was rejected as buried, whoosh-heavy and robotic, and had to be rebuilt. The rules below are what the rebuild changed.

You cannot hear. Build the mix from measurements, print the numbers, and tell the person to listen once before using it.

## The rules

1. **Music leads.** In an ad the music carries the feeling and effects sit underneath. In our rejected mix the music sat 6 dB *below* the effects and read as a faint drone. In the rebuilt one it sat about 17 dB above them. If there is music, the music stem should be the loudest thing by a wide margin.
2. **No repeated whooshes.** One whoosh re-pitched under every camera move is the sound of a template. Cut them. A camera move usually needs no sound at all when the music is doing its job.
3. **A sound only where something visibly moves**, and only if that motion earns it. Prefer one real, specific sound (the click of the actual button) over five generic ones.
4. **Every cue sits on its beat.** Name the picture's beats and point cues at the names. Align hits and clicks by their loudest sample (`"align": "peak"`), risers by their end (`"align": "end"`). The mixer prints the error; it should be 0 ms.
5. **Duck the music under the key effect.** Ease the music down about 4 dB for a third of a second around the one sound that must be heard, so it pops without being loud. If the music swells just before that moment, ease the swell too, so the sound lands in a breath.
6. **Use the real rate for anything mechanical.** A fine mechanical movement can beat 8 times a second (28,800 an hour). A wall clock ticks once a second. Look the number up. A wrong rate is something an owner hears instantly.
7. **Text-to-sound cannot keep time.** Ask a model for "eight ticks a second" and you get six uneven clicks. Generate a few recordings that contain separate beats, then build the steady bed in code from many different beats (`tick_bed.py`). Do not loop a single sample: it sounds like a machine gun.
8. **Mechanical beds are felt more than heard.** Tuck them 18 to 22 dB under the music, band-limited (about 850 Hz to 6.5 kHz), only during the shots where the mechanism is on screen. Swell slightly on the close-up, fade out before the wide shot.
9. **Never digital silence.** A very quiet room tone under everything (about -46 dBFS) keeps the track alive between events.
10. **End clean.** The music resolves on the picture's last big beat, then decays. The last half second is near-silent, especially if something else follows the ad.
11. **Master to a standard.** -14 LUFS integrated and at most -1 dB true peak for YouTube.

## Building it

### The beats

The picture hands over its beats as a file: `render_page.mjs --events` for a page, `join_shots.py` for joined shots (shot starts plus the marks you named, such as the frame a button goes in). Add any others by hand.

### Level 1: sounds made by code

```bash
python3 scripts/make_sounds.py sound/kit --seconds 18
```

That gives airy passes, a soft low hit, a small pop, a tick, a rise, grain rustles, a low swell, a pad and room air. All of it is sine waves and filtered noise, so it is free to use anywhere.

What worked on a code-only ad: a low soft hit and a long airy pass on the opening pull-back; a small pop and a dry rustle on each transform, **a different rustle each time** and pitched slightly differently; a quiet rise that ends exactly as the logo completes, with a low hit under it; a soft pad underneath that resolves on the logo. The person can also drop their own music or effects into `sound/` and you place them the same way.

### Levels 2 and 3: generated music and a few real effects

- **Music** at the exact length, instrumental, with the structure written second by second and the peak placed on the picture's biggest beat (`prompt-templates.md`). Make several takes: we made eight to get two worth using. Say "build in one unbroken crescendo, do not peak early" if takes keep peaking too soon.
- **Effects**: describe the object, how close the microphone is, the room, and what it is not ("NOT a sci-fi whoosh, no bass hit").
- A generated effect is raw material. Trim it, filter it, and place it.

### The cue sheet

```json
{
  "length": "end",
  "music": {"file": "music/take-a.mp3", "gain_db": 0, "fade_in": 0.65, "fade_out": 0.9,
            "levels": [[0, 6], [3.4, 6], [4.8, 0]],
            "ducks": [{"at": "press", "before": 0.1, "after": 0.2, "depth_db": 4}]},
  "effects": [
    {"file": "sfx/room.mp3", "at": 0, "until": "end", "gain_db": -30, "fade_in": 0.5, "fade_out": 1.0},
    {"file": "sfx/press.mp3", "at": "press", "align": "peak", "gain_db": -6, "low_cut": 65},
    {"file": "sfx/tick-bed.wav", "at": "press", "shift": 0.08, "until": "shot6.start", "gain_db": -6, "fade_in": 0.4, "fade_out": 1.2},
    {"file": "sfx/cloth.mp3", "at": "shot6.start", "shift": 1.7, "gain_db": -14, "low_cut": 140, "high_cut": 2400, "fade_in": 0.3, "fade_out": 0.6}
  ]
}
```

`levels` shapes the music over time, for instance lifting a hushed intro so the first shot is not silent.

```bash
python3 scripts/tick_bed.py sound/sfx/tick-bed.wav sound/sfx/tick-1.mp3 sound/sfx/tick-2.mp3 --rate 8 --seconds 10
python3 scripts/mix_sound.py sound/cues.json sound/mix.wav --events out/picture.events.json
python3 scripts/master_audio.py sound/mix.wav sound/master.wav --video out/picture.mp4
python3 scripts/master_audio.py sound/master.mp4 --check
```

The mixer warns when one effect plays more than twice and when the effects are louder than the music.

### With a voiceover

Voice on top, music ducked about 8 dB while it talks (`"duck_under_voice_db": 8`), effects quiet and few. Leave the title and the end card room to breathe: no voice over the first and last second.

## What to report

- Each stem's level and the mix's loudness and true peak, before and after mastering.
- That every cue is on its beat.
- The level of the last half second.
- That it was checked by measurement and not by ear, and that the person should listen once.
- Where to change things: one line per cue in the cue sheet.

## Swapping the music

Keep the effects stem and the duck points; change only the music file and its `levels`. Match the new music stem to the old one's loudness, then re-master. The picture is copied untouched (`master_audio.py --video`), so trying a second score costs nothing but the generation.
