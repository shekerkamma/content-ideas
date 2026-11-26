# Prompt templates

Fill in the parts in `{braces}`. Brand names are left out on purpose: describe the real product from its real photos, and attach the photos.

Prompts are built from blocks, so the product and the light are described in the same words every time. Save each prompt as a file in `build/prompts/` and log which file each job used.

## Contents

- [Level 1: the brief for a code-only ad](#level-1-the-brief-for-a-code-only-ad)
- [Level 2: the brief for a footage edit](#level-2-the-brief-for-a-footage-edit)
- [Level 3 stills: the PRODUCT block](#level-3-stills-the-product-block)
- [Level 3 stills: the LOOK block](#level-3-stills-the-look-block)
- [Level 3 stills: keyframes](#level-3-stills-keyframes)
- [Level 3 video: the RULES block](#level-3-video-the-rules-block)
- [Level 3 video: shots](#level-3-video-shots)
- [Blending a person in](#blending-a-person-in)
- [Music](#music)
- [Sound effects](#sound-effects)
- [Voiceover](#voiceover)
- [The reverse-engineer prompt](#the-reverse-engineer-prompt)

## Level 1: the brief for a code-only ad

Step 1, assets:

```text
I want to make a product ad for {product, in one line}. This is Level 1: code only, no image or video generators.
First get the real ingredients into assets/: the real logo as a vector file, real photos of the product, and its
real {screens / interface / packaging}, from {source}. Check the resolution of everything. Don't draw the logo
from memory. List every source in assets/SOURCES.md.
```

Step 2, storyboard:

```text
Now give me a numbered storyboard, 6 to 8 shots, 12 to 18 seconds, and stop so I can approve it.
Direction: {the product} turns in 3D on {a surface}, one continuous camera, no cuts. {What changes: its screen
goes from A to B to C}. Each one has to transform into the next, no cross-dissolves, so work out what each
shape could become. Use the real {screens} pixel for pixel. Keep the action in the dead centre of the frame.
Shallow depth of field: the subject stays sharp at every angle and everything behind it is blurry. One key light.
End with {the logo forming}, the product centred, and "{web address}" under it. No voiceover, and no on-screen
text except the web address.
```

Step 3, build:

```text
Approved. Build it as code, exactly as the storyboard says. Use the real {screens} pixel for pixel and the real
logo file. Model the product from the photos and compare it against them. Check it frame by frame and fix what
looks wrong before you show me. Do a quick 1080p draft first, then render it in 4K.
```

Step 4, sound:

```text
The picture is approved. Add sound design that matches each motion: something for {the opening move}, something
for each {transform}, and a lift into the logo. Only make a sound where something visibly moves. No voiceover.
Make the sounds with code, nothing paid. A very subtle music bed is fine if you can make it yourself.
```

## Level 2: the brief for a footage edit

```text
Cut this {length} recap down to a tight {20-30} second promo: the best moments, on the beat. Show me the cut list
before you build. Keep burned-in text out of frame where it clashes. Add code-built motion graphics in the
footage's own look: a title that builds itself, words that slide up in place (no bouncing), a counter for
{a real number from the footage}, lower thirds, a clean end card. Graphics must transform into the footage, no
cross-dissolves, and the opening goes from pure animation into real footage. Write a voiceover that fits the cut
at about 2.3 words a second using only facts that are in the footage. Generate it, make a music bed at the exact
length, and mix it.
```

## Level 3 stills: the PRODUCT block

Write it once, from the real photos. List every part, material and piece of text in a fixed order, and say what must not be there.

```text
THE PRODUCT (must match the reference photos exactly, they are real photos of it): {what it is, in one line}.
{Main material and finish: e.g. brushed steel body with polished edges}. {Second material: e.g. a black ceramic
ring that stays deep glossy black}. {Every piece of printed or engraved text, in reading order, with its colour
and position}. {Each sub-part, left to right or clockwise, with its markings}. {Text that sits at an unusual
angle: say which way its top faces, "exactly as in reference image 1"}. {Controls, ports, buttons: how many,
where}. {Moving parts and the position they are set to}. NO {things the model tends to add} anywhere.
```

## Level 3 stills: the LOOK block

```text
WHERE IT IS: {on a wrist / in a hand / on a stone surface}. {Skin tone, sleeve or surface material and colour}.
Everything behind is {black / a dark soft gradient}.

LIGHT: one hard key light only, a narrow strip light high on the upper left and slightly behind the product. No
fill light, no second light, no rim light. Shadows fall to pure black. The highlight on {the dark glossy part} is
one thin clean line, never a wide grey wash. Polished {metal} shows crisp speculars; brushed {metal} shows fine
grain.

CAMERA: 100mm macro lens, shallow depth of field, fine film grain, high-end commercial. Real photography, not a 3D
render. No added text, no watermark, no logos other than what is on the product itself.
```

## Level 3 stills: keyframes

The hero frame, made first (references: the real photos):

```text
Photoreal macro photograph for a luxury product commercial. 16:9.

FRAMING (keyframe {K3}, the hero): the camera looks at {the face of the product} from a low three-quarter angle,
about 35 degrees off straight-on, from the lower left. {The face} fills the frame and its centre is at the centre
of the frame. The left edge falls into shadow and soft focus. {Side controls} are visible at the right edge,
slightly soft. All {printed text and details} are tack sharp. {The moving part} is at {its starting position}.

{PRODUCT block}

{LOOK block}
```

Any later keyframe (reference image 1: the approved hero; then real photos):

```text
Photoreal macro photograph for a luxury product commercial. 16:9. Reference image 1 is an approved frame from this
same shoot: keep exactly the same product, the same {hand / surface}, the same single key light, the same colour
grade. The other reference images are real photos of the product: copy its details from them.

FRAMING (keyframe {K1}, {name}): {what the camera sees, what is at the left, centre and right of the frame, what is
sharp and what is soft}. {What is NOT in the frame}. Background black.

{PRODUCT block}

{LOOK block}
```

Same crop, one change (reference image 1: the keyframe it must match):

```text
{header as above}

FRAMING (keyframe {K2}, {name}): exactly the same framing, angle and crop as reference image 1: {list what is in
it}. Do not zoom out. Do not show any more of the product than reference image 1 shows. ONE CHANGE ONLY: {a
fingertip has come in from the top right corner and is pressing the upper button straight in}. {It touches only
that part and covers no text}. Background black.

{PRODUCT block}

{LOOK block}
```

A one-change edit (no blocks, on purpose):

```text
Edit the reference image. Keep everything exactly as it is: same framing, same crop, same light, same {surface},
same text, same {parts}. Change ONE thing only: {the part, described so it cannot be confused with another}.
{Move / rotate it to the new position, described against fixed landmarks}. Remove it from its old position. It
casts a soft thin shadow. Photoreal macro photograph, same grain and sharpness as the original.
```

A text-fix pass (on a model that is good at text; references: the frame, the hero, a real photo):

```text
Edit reference image 1. Keep everything exactly as it is: same framing, {hand}, light, grain, same product
position, size and angle. Change ONE thing only: the tiny printing on the product is smeared. Re-draw it crisply
and correctly, copying reference image 2 (the same product, close up) and reference image 3 (a real photo of it):
{every line of text, in order}. Photoreal, same sharpness and grain as the rest of the photo.
```

The end frame, if a person will pick up from it:

```text
{header as above}

FRAMING (keyframe {K6}, the last frame of the ad): a medium close-up of {a forearm held level across the chest, as
if the person has just glanced at it}. The product is in the exact centre of the frame, facing the camera,
upright and readable, about one sixth of the frame width. {The hand is relaxed at the right of the frame}. Behind,
{the chest in the same dark top}, out of focus. The face is NOT in the frame: the frame is cut at the collarbone.
Lots of clean black space around.
```

## Level 3 video: the RULES block

```text
RULES FOR THE WHOLE SHOT: one continuous macro camera move, no cuts, no dissolves, no zoom reversal. Real
photography look: 100mm macro lens, shallow depth of field, fine film grain. One hard key light from the upper
left only, black background, shadows fall to black; the highlight slides along {the polished metal} as the camera
moves. The product is rigid: its shape, {its engraved and printed text}, never change, never warp, never flicker
and never re-draw. No new text, no extra parts appear. Silent.
```

## Level 3 video: shots

Each is generated with a start image and an end image. Each is a shot paragraph followed by the RULES block.

A slide along the product (same scale at both ends):

```text
Luxury product commercial, extreme macro shot of {the part} of {a luxury steel product} {where it is}.

SHOT {1}, "{name}": the camera slides sideways along {the part}, staying just as close as it starts. It begins on
{detail A}, follows {the curve / the edge} past {detail B}, and ends on {detail C}. {The part} stays in the centre
of the frame and in sharp focus the whole way. A thin highlight runs along it just ahead of the camera.

FOCUS: the depth of field is razor thin and sits on {the part} only. {What is behind it} is a soft out-of-focus
blur for the whole shot. NO PRINTED WORDS ARE EVER READABLE on {the background surface} in this shot. Do not
invent any lettering.

NOTHING ON THE PRODUCT MOVES.
```

An action (a hand does one thing):

```text
SHOT {2}, "{name}": the camera holds on {the area}, easing in very slightly. A fingertip comes in from the top
right of the frame, settles on {the button} and presses it straight in with one firm, deliberate click. It
travels in about a millimetre and stays in. The finger holds there.

Only the fingertip and {that button} move. {Other controls} do not move.
```

A reveal (leave the detail, arrive on the whole):

```text
SHOT {3}, "{name}": the fingertip lifts away out of the top right of the frame. In the same move the camera rises
over the edge of the product, swings left and pulls back, until it is square on {the whole face}, which fills the
frame. The camera moves fast at first, then slows down and settles.

{Each part that must stay put, and where it stays}.
```

A push-in with one moving part:

```text
SHOT {4}, "{name}": the camera starts square on {the whole face} and pushes in smoothly towards {the lower right},
ending in a tight macro on {detail}.

THE ONLY THING ON THE PRODUCT THAT MOVES is {the moving part}: it {sweeps smoothly from position A to position B},
with a soft thin shadow. {Every other part} stays exactly where it is.
```

A pull-back to the end frame (the second half of a split shot):

```text
SHOT {6b}, "{name}": the camera starts with {the product's face} filling the frame and pulls straight back,
revealing {the hand, the sleeve, the forearm}. It ends as a still, composed medium close-up with the product in
the exact centre of the frame. The pull back is fast at first, then very slow for the last two seconds. {The arm}
barely moves, only a natural breath.

The product stays exactly the product of the first frame while it gets smaller: {its colours, named}. Nothing on
it is ever {the wrong colours}. Do not redraw or change its printing. The face is never in the frame.
```

## Blending a person in

Start frame: the ad's last frame. End frame: a still of the person from their own camera, in the same clothes as the ad's end frame.

```text
One continuous camera move, no cuts. Start: {the ad's last frame, described: extreme close-up of the product on a
wrist, dark moody studio light}. The camera smoothly pulls back and rises: the dark background turns out to be
{the person's dark top}, the lights warm up, and we reveal them sitting in {their real room, described from the
end still}. They settle into a calm, direct look at the camera. Smooth cinematic dolly-out, natural motion,
realistic, stable face, no text, no morphing objects.
```

## Music

Write the length, the tempo and the structure second by second. Say what it must not have.

For a product ad (music leads):

```text
{Intimate, refined neoclassical} score for a {dark luxury product} commercial. Exactly {20} seconds, instrumental
only. {Warm close-miked felt piano and chamber strings with solo cello}. 0 to {5} seconds: hushed, poised opening,
{a single sustained note and two sparse piano notes}, leaving breathing room at {5} seconds. {5} to {12} seconds:
the music gently awakens with {a steady understated pulse and low strings rising}. {12} to {16.5} seconds: an
unhurried crescendo, building in one unbroken line, do not peak early. At {16.75} seconds: it resolves into one
open, luminous chord, no trailer boom or harsh percussion, followed by a natural decay to near-silence by {19.5}
seconds and complete silence at {20} seconds. Expensive, timeless, acoustic, no drums, no synths, no vocals.
```

For a promo with a voiceover:

```text
{Premium cinematic electronic} event promo score, exactly {27} seconds, {120} BPM, instrumental, no vocals.
{Mood and instruments}. Structure: 0-4 s airy intro with soft pads and a rising shimmer; 4-13 s the pulse enters,
kick on every beat, the arpeggio builds; 13.5 s a lift with a short riser and impact; 14-21 s full driving groove;
21-23 s a big swell into one final impact at 23 s; 23-27 s a warm resolving tail and a fade to silence. Clean mix
with space left for a voiceover.
```

## Sound effects

Describe the object, the distance of the microphone and the room, and say what it is not.

| Sound | Prompt |
|---|---|
| A mechanical press | Extreme close-up macro foley recording of {a precision machined steel button on the product} being pressed and released. Crisp, solid, two-part mechanical click: a firm snap on press, followed immediately by a slightly softer spring release. Dry studio recording, ultra-clean, no music, no voice, no background noise. |
| Separate mechanical beats (source for a tick bed) | Listening to {the mechanism} held close in a quiet room: very soft, muted, delicate metallic ticking, steady, continuous for 10 seconds. |
| Cloth and air for a pull-back | Very soft, understated studio foley of {a knit sleeve} and gentle quiet air movement as {a wrist} shifts calmly in a dark soundstage. Barely audible. NOT a sci-fi whoosh, no bass hit, no wind roar, no music, no voice. |
| Room tone | Continuous steady dark low-frequency ambient room air tone, very soft, empty quiet room, completely flat and uninterrupted for 10 seconds. |

## Voiceover

Send the whole script as one take, a blank line between lines, numbers spelled the way they are said:

```text
{Line one.}

{Line two, twenty exceptional things, from around the world.}

{Round one: a day in the city, nineteen seventy-one.}
```

Delivery note for the voice settings or the prompt: warm, confident, unhurried, one beat of air between lines.

## The reverse-engineer prompt

After running `study_video.py` on a reference:

```text
Read {study}/sheet.jpg and {study}/study.md. Answer the questions in study.md, then write me a prompt I can use to
make a video in this style for {my product}. Describe the light, the angles, the camera moves, the pace, the
joins between shots and the sound. Leave out everything that belongs to the reference: its product, its brand,
its footage, its words, its music. Show me the prompt before you use it.
```
