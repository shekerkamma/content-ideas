# Level 3: photoreal product ads

Real-looking footage of a product, with no camera and no 3D software. An image model makes a set of keyframe stills from real photos. A video model makes each shot from one keyframe to the next. Because shot N ends on the exact picture shot N+1 starts on, the shots join into one camera move that never cuts.

Our example was a 20-second, 4K ad for a luxury steel product: six shots, eight keyframes, one camera, one light. It took about 2 hours 15 minutes. About 330 credits are in the final cut; the whole job used about 790, the rest being a model shoot-out, rejected takes and two wasted upscale runs. Budget for roughly twice what the final cut needs.

## The order of work

1. Reference photos (real ones).
2. Storyboard. Stop for approval.
3. The detail checklist and the look, written once as prompt blocks.
4. The hero keyframe. Then the other keyframes, each with the hero as its first reference.
5. A shoot-out: the hero shot on two or three video models.
6. The shots, each from keyframe to keyframe.
7. Check every take. Join. Check at full size.
8. Titles in code. Upscale. Sound.

Keep every still and every take, kept and rejected, and log every job.

## 1. Reference photos

Ten or so real photos of the product from every angle that will appear: front, three-quarter, side, back, details, in use, in the hand or on the body for scale. Write the sources in `refs/SOURCES.md`. They are private references, not material to publish (see `honesty.md`).

Then write a **detail checklist** from the photos: every part, every material, every piece of printed or engraved text, in order, with what must *not* be there. This becomes the PRODUCT block that goes in every still prompt. See `prompt-templates.md`.

## 2. Storyboard

One camera, one light, 5 to 7 shots of about 3 seconds. Plan it as a single move: each shot's last frame is the next shot's first frame. Use the real photos, cropped, as the board's frames. Do not generate keyframes until the board is approved.

Decide the last frame early. If a person will pick up from the ad on camera, design the end frame for that (see `style-and-meta-prompting.md`).

## 3. Keyframes

Every keyframe prompt is three parts: **a framing paragraph + the PRODUCT block + the LOOK block.** The blocks never change, so the product and the light are described the same way every time.

- **Make the hero frame first**: the frame that shows the most of the product, sharp. Check every detail against the photos. Re-roll until it is right.
- **Every later keyframe gets the hero as reference image 1**, with the words "an approved frame from this same shoot: keep exactly the same product, the same light, the same colour grade". Then the real photos as the other references.
- **For a small change, write a short edit prompt** with no description blocks: "Edit the reference image. Keep everything exactly as it is. Change ONE thing only: ...". Long prompts make the image model recompose the whole picture, and it will add a part or move the wrong one.
- **"Exactly the same framing and crop as reference image 1. ONE CHANGE ONLY"** is what makes a second keyframe that a video model can travel to (a finger arriving, a part moving).
- **Tiny text goes soft** when the product is small in frame. Fix it with a second pass on a model that is good at text: "keep everything, redraw the printing crisply, copy it from these references".
- **Models "help".** They turn upside-down text the right way up and tidy things that are correct. Say what must stay odd, with the real photo attached.
- **Crop afterwards** to control what is in frame. A keyframe is a starting picture, not a finished one.
- Expect to keep about a third of what you generate. We kept 8 stills out of 21.
- False content-filter refusals happen (a wrist, a hand). Re-run; check that the refused job was refunded.

### The two rules that decide whether a shot can be made

**The model can only keep text it was shown.** If text is hidden in both keyframes and slides into view mid-shot, the video model invents it, wrongly, every time. Either crop both keyframes so that text never enters the frame, or make sure the text is readable in at least one of them.

**Keep both keyframes at the same scale unless the shot is a pull-back or a push-in.** If the end frame is much wider than the start, the model zooms out and re-draws the product at every size in between, with nothing to copy. For a slide, make the end keyframe at the same magnification.

And when a shot must change scale a lot (a detail to a wide), **split it at a mid-point keyframe**: detail to whole product, then whole product to wide. The mid-point pins the details in the middle of the move. Make that keyframe as a one-change edit of the hero.

## 4. The shoot-out

Before making all the shots, run the hero shot on two or three video models from the same start frame, end frame and prompt. Judge on:

- Does it start **and end** exactly on the stills? (No end frame, no join.)
- Does printed text stay correct mid-move?
- Does the thing that should move actually move, and nothing else?
- Do colours and materials hold?

What we found in November 2026. Models and prices change, so treat this as a method, not a ranking:

| Model | What it got right | What it got wrong | Used for |
|---|---|---|---|
| `kling4_0` (first + last frame) | Starts and ends on the stills. Text stays correct. Materials hold. Eases cleanly | One take had a hidden jump cut one frame in | Five of six shots |
| `kling_o3_flf` | Starts and ends on the stills. A third of the price. Sharp native 4K mode | Small parts flicker dark mid-move. Invents text that slides in from off-frame. Ends still moving | One shot. Best value |
| `seedance_2_5` | Sharp, clean metal | Treated the start frame as a loose reference. Misspelt text. The moving part never moved | Not used |
| `veo3_1` | Native 4K. Holds the start frame | Takes a start frame only, so it cannot land on the next shot. Barely moved the part. Grade drifted | Not used |

For stills: `nano_banana_pro` looked like a real macro photo and obeyed camera angle and light, and made every keyframe. `gpt_image_2_6` got every character of text right and did exact one-change edits, but ignored the camera angle and looked like a catalogue shot, so it was the fixer.

## 5. The shots

Every shot prompt is **a shot paragraph + the RULES block** (see `prompt-templates.md`). Each is generated with a start image and an end image, 5 seconds, 1080p, sound off.

- Describe the camera move in order: where it starts, what it passes, where it stops, and its speed ("fast at first, then slowing").
- Say what on the product moves, and say that **nothing else does**.
- Name the things that must not change, and the colours they must never become. When a shot kept turning a part the wrong colour, "nothing is ever gold, the surface is never grey" fixed it.
- Where a shot starts matters. A side-on start made the model redraw the face badly; a top-down start worked.
- Run three at a time. Each takes 2.5 to 6 minutes.
- Expect several takes for the hard shots. We made 29 takes for 6 shots.

## 6. Check every take, then join

```bash
python3 scripts/frame_sheet.py shots/S4.mp4 out/S4.jpg --every 0.4
python3 scripts/find_jumps.py shots/S1.mp4 shots/S2.mp4 shots/S3.mp4 --joins
```

Look at six or more frames of every take against the real photos: order of parts, every character of text, the count of things that should be counted.

Then join. A plain join looks like the camera stops dead at every keyframe, because each clip eases in and out on its own. `join_shots.py` re-times each clip from its measured motion so speed carries across the join, drops the duplicate frame, and trims the model's dead-still last frames.

```json
{"fps": 24, "size": [1920, 1080], "shots": [
  {"file": "shots/S1.mp4", "frames": 72, "tail": 5},
  {"file": "shots/S2.mp4", "frames": 72, "bump": 0.5, "tail": 3, "marks": {"press": 59}},
  {"file": "shots/S6a.mp4", "frames": 42, "bump": 0.6, "tail": 14, "start": 0.2},
  {"file": "shots/S6b.mp4", "frames": 78, "bump": 0.8, "end": 0.1}
]}
```

```bash
python3 scripts/join_shots.py build/plan.json out/picture.mov
```

It also writes the beats (shot starts and your named marks, such as the frame a button goes in) for the sound.

**Zoom into the delivered file, not the preview.** One of our shots looked right on a 1080p sheet; at 4K small text smeared for a second and a half. Check single frames at full size at every join and through every fast move.

## 7. Titles, finish, upscale

- Add words in code, over the joined picture (`level-2-footage.md`, graphics). Put them where the product never goes during the move: we had to move a tagline because the product crossed the bottom centre. Take them off before the last half second if a hand-off follows.
- A tagline you wrote is yours, not the brand's. Say so in the notes.
- Add the spec-ad label if the product is not the person's own (`honesty.md`).
- **Upscaling.** Check what a tool really does before paying for a long clip. One "enhancer" we tried returned the same 1080p size as an HDR file after 24 to 44 minutes; it was not an upscaler. `bytedance_video_upscale` gave true 3840x2160 with no colour shift and no re-invented text, but was charged at four times its quote. After upscaling, check the frame count, the frame rate, the colour, and the small text.
- Upscale the joined picture once, not each shot.

## 8. Sound

See `sound-design.md`. For product ads in particular: music leads, the one physical action gets one real sound exactly on its frame, and anything mechanical runs at its true rate.

## What went wrong for us, and the fix

| What went wrong | Why | Fix |
|---|---|---|
| Invented text as a surface slid into view, three takes in a row | The text was hidden in both keyframes | Crop both keyframes so it never enters the frame |
| The product was redrawn with extra parts mid-shot | The end keyframe was much wider than the start | Make the end keyframe at the same magnification |
| Small text smeared mid pull-back, visible only at 4K | A detail-to-wide move with nothing to copy in between | Split the shot at a mid-point keyframe |
| A part changed colour mid-move | The start angle hid it | Start from an angle that shows it; name the colours it must never be |
| A still had impossible geometry | Asked for a view the model could not reason about | "Exactly the same crop as the approved frame. ONE CHANGE ONLY" |
| A still had an extra part; an edit moved the wrong one | The prompt was long, so the model recomposed | A short edit prompt with no description block |
| Text at the bottom was the wrong way up | The model made it readable | Say it must be upside down, with the real photo attached |
| A take had a hidden jump cut after frame 1 | Model glitch | `find_jumps.py` on every take |
| The camera stopped at every join | Each clip eases on its own | `join_shots.py` |
| The joined file played only the last shots | A stream-copy join wrote broken timestamps | Join with a re-encode (the script does) |
| The tagline sat on top of the product | The product crosses that area during the move | Check the title's area on every frame it is up |
| Generated ticking was six uneven clicks | Text-to-sound cannot keep time | `tick_bed.py` |
| A quote was four times too low | The quote looked like a per-5-seconds price | Check the account's charges after the first job on any new model |
