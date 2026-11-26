# Following a reference, meta-prompting, and blending a person in

Three techniques that sit on top of the four steps.

## 1. Copy a style: the reverse-engineer pass

When the person points at a video and says "like this", do not guess at its style and do not copy its content. Take it apart, write down what makes it work, and apply that to their product.

### Measure it

```bash
python3 scripts/study_video.py refs/reference.mp4 refs/study
```

This writes the cuts and each shot's length, how much each shot moves, its brightness and main colours, the loudness, a level reading every half second, a tempo estimate, and a sheet with the first, middle and last frame of every shot.

If the reference is online, the person should supply the file, or download it themselves with a tool they are allowed to use. Use it as a private reference only.

### Read it

Open `refs/study/sheet.jpg` and answer the questions at the bottom of `refs/study/study.md`, one line each:

- **Subject**: what is on screen and where it sits in the frame.
- **Camera**: what it does in each shot. One move or many?
- **Joins**: how each shot becomes the next.
- **Light**: how many, from where, hard or soft.
- **Background**: what is behind the subject, and whether it is in focus.
- **Colour**: the three or four that carry it, and what is missing on purpose.
- **Text**: where, how it arrives and leaves, how many words at once.
- **Pace**: where it is fast, where it rests, what the biggest beat is.
- **Sound**: what leads, and which moments get a sound of their own.
- **The one idea**: what makes it look expensive, in a sentence.

The numbers keep you honest: an "energetic" ad whose average shot is 1.9 seconds on a 120 BPM grid is a different thing from one that is a single 20-second move.

### Write the style brief

A paragraph or a short list that describes the style with nothing from the reference in it: no brand, no product, no person, no wording. It should be possible to hand the brief to someone who has never seen the reference.

Then make a storyboard for the new subject in that style, and stop for approval as usual.

### What you may and may not take

Take: structure, pacing, camera language, lighting approach, how text behaves, the kind of sound.

Do not take: footage, frames, logos, music, voice, exact wording, a distinctive character or mascot, or anything that would make a viewer think the reference's maker made this.

## 2. Meta-prompting: write the prompt before the picture

A short prompt gets a generic result. The person usually knows what they like when they see it but does not want to spell out the lens, the light and the move. So write the prompt for them, and let them edit it.

1. **Gather**: the real assets, and the style brief if there is a reference.
2. **Write a full prompt** that someone could run with no other context. It names the subject from its real photos, the look (place, one light and where it is, lens, depth of field, grain), the camera move shot by shot, how the shots join, the pace, the sound, the end frame, and what must not appear.
3. **Show it and stop.** The person reads it, removes what they do not want, adds what is missing. Reviewing a page is far easier than imagining one.
4. **That prompt is now the point of reference.** The storyboard comes from it. Every still and shot prompt is cut from it, as fixed blocks (`prompt-templates.md`), so the product and the light are described in the same words every time.

The same idea works one level down. Before a batch of paid generations, write all the prompts as files, read them back against the reference photos, and fix them on the page. A wrong word costs nothing in a text file and several credits in a render.

To re-use a result for a different product: keep the prompt, swap the PRODUCT block for one written from the new product's photos, and keep everything else.

## 3. Blend yourself in

An ad that ends, cuts to black, and then cuts to a person talking is two videos. Joined properly, the ad becomes the person's opening shot.

### Design the hand-off before you build

Choose the ad's **last frame** for the join: a composed frame the person can match in real life. In our build it was the product at the exact centre of the frame, in a dark top against a dark background, one hard light, with the frame cut at the collarbone so no face was generated.

Two things follow from that choice:

- No on-screen words in the last half second, so the join is clean.
- The music has resolved and faded by then, so the person's own sound can start.

### Option A: film it (best)

Give the person a matching sheet with the end frame on it:

1. Wear what the end frame shows.
2. The same background and the same single light, from the same side.
3. Put the end frame beside the camera monitor and match it: position, size in frame, angle.
4. Hold that pose for two seconds, then move: tilt up to the face, or lower the arm and look up.
5. Cut from the ad's last frame to the first frame of their clip.

### Option B: generate the bridge

A first-frame/last-frame video shot does the join:

- **Start frame**: the ad's last frame.
- **End frame**: a still from the person's own camera, taken from the start of their recording.
- **Prompt**: one continuous move from one to the other (see "Blending a person in" in `prompt-templates.md`): the camera pulls back and rises, the dark background turns out to be their top, the lights warm up, the room is revealed.

Then:

- Make two takes on two models and keep both.
- Check the last frame of the bridge against the first frame they actually use. If they trim their recording later, the bridge ends on a slightly different moment and the cut will jump: re-cut or regenerate.
- Put soft room air under the bridge so the sound does not drop to nothing between the ad's tail and their first word.
- About 4 seconds is enough.

### Consent

Only generate a real person's likeness when that person has asked for it and supplied the picture. Use their real frame as the end frame; do not invent their face. See `honesty.md`.
