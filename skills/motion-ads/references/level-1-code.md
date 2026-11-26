# Level 1: code only

A finished ad made with nothing but code and local tools. No image or video generator, no paid tools. The picture is a web page rendered to video, and the sound is made by code too.

Our example was a 16-second, 4K ad for a desk e-ink display. From the approved storyboard to the finished 4K picture took about 15 minutes, of which the 4K render was 1.4 minutes. The whole job, assets to final checks, took about 37 minutes.

## When to use it

Good: screens, apps, dashboards, logos, type, charts, devices with simple shapes (a slab, a box, a card), flat illustration.

Not good: brushed metal, glass, skin, liquid, fabric. Code-built versions of these look flat and plastic, with wrong reflections. We built the same luxury product both ways to check, and the code version looked fake. Use Level 3 for those.

## How the picture is made

One HTML page draws the whole ad. It is driven by time, not by a clock:

```js
window.ad = {
  duration: 16,                    // seconds
  width: 1920, height: 1080,       // the stage
  seek(t) { /* draw the frame for time t */ },
  events: { 'logo.land': 12.7 },   // named beats, handed to the sound
  ready: assetsLoaded              // optional promise
};
```

`scripts/render_page.mjs` calls `seek(t)` for each frame, takes a screenshot and pipes it to ffmpeg. Because each frame is drawn from `t` alone, the render is exact and repeatable.

`templates/ad-page.html` is a small working starter. For 3D, keep a copy of three.js in the project (`build/vendor/`), render into a canvas the size of the stage, and let `seek(t)` be the only thing that changes the scene.

Rules for the page:

- **One block of beats at the top.** Every time in the ad is a named number in one object. Changing the timing means changing a number there and nothing else. Export the same names as `events` so the sound follows.
- **No `Date.now()`, no `setInterval`, no CSS animations that run by themselves.** Everything is a function of `t`.
- **Easing is written out.** Fast first, then a long settle (a quartic ease-out) for arrivals; ease in and out for moves that pass through.
- **A draft mode.** Let a query string lower the quality (`?draft=1`: fewer samples, smaller size) so a draft renders in seconds: `--query draft=1`.

## Real assets, pixel for pixel

- Use the real logo file (SVG). Do not redraw it.
- Use real screens at the device's own resolution and map them onto the model unscaled where you can.
- Model a device from its product photos, then put a frame of your model next to the front-on photo and compare: bezel, proportions, logo position. Leave out details that never face the camera.

## Transforms instead of dissolves

Ask how one thing can physically become the next. Three that work in code:

- **Pixels travel.** For flat images (one screen to another, a screen to a logo), `scripts/ink_morph.py` pairs every dark pixel of image A with a nearby dark pixel of image B. Animate the pairs and A re-forms into B. Give neighbouring pixels the same start time, as a wave spreading from one point, so shapes stretch and flow. Random start times turn the picture into dust.
- **A shape opens.** A logo's opening grows until what is behind it fills the frame, so the logo becomes the window.
- **The camera carries it.** One continuous move, so there is nothing to dissolve between.

When two transforms follow each other, vary the direction (out from a point, then across a diagonal) but keep the speed the same, so they read as one idea.

## Look

- One key light. A neutral colour temperature. Pale, plain surroundings unless the brand says otherwise.
- Shallow depth of field: the subject sharp at every angle, the background round and soft. If the blur looks smeared sideways, the blur is wrong, not artistic.
- The subject on the centre of the frame for the whole piece.
- The camera never stops completely until the end card, and even there a slow light sweep keeps the frame alive.
- Only the text that is needed. Our ad added one thing: the web address on the end card.

## Build order

1. Rough stills for the storyboard. Stop for approval.
2. The page, with a fast draft mode.
3. A 1080p draft. Make a review sheet and read it.
4. Notes rounds (below). Fix, re-render the draft, re-read.
5. The full-size render: `--scale 2` turns a 1920x1080 stage into 3840x2160.
6. Beats out to a file for the sound: `--events`.

```bash
node scripts/render_page.mjs build/ad.html --stills out/check --at 3.0,4.9,12.0 --query draft=1
python3 scripts/frame_sheet.py out/check out/check.jpg
node scripts/render_page.mjs build/ad.html --video out/draft.mp4 --query draft=1
python3 scripts/frame_sheet.py out/draft.mp4 out/draft-sheet.jpg --every 0.8
node scripts/render_page.mjs build/ad.html --video out/ad-4k-silent.mp4 --fps 30 --scale 2 --gpu
node scripts/render_page.mjs build/ad.html --events sound/events.json
```

## The notes that fixed our build

Nobody typed these. They are what the frame-by-frame review turned up, and they are the kind of note to give yourself.

- *The background blur is smeared sideways.* It should be round and soft.
- *Everything is too yellow.* Paler desk, off-white wall, a more neutral light.
- *When the ink moves it turns into dust.* Make neighbouring pixels leave together and take the same path.
- *The opening is too fast.* Let the first close-up last longer.
- *The camera does most of its turning in the first five seconds.* Spread it out so it keeps turning.
- *A screen is too faint to read.* Swap it for a layout that reads at this size.

## Checks specific to this level

- A frame at full size for sharpness, not just the sheet.
- Three frames in a row over any fine dotted or lined pattern, to catch shimmer.
- The model next to the real product photo.
- Colour: the MP4 is tagged BT.709 by the renderer. Files written with non-standard colour settings show the wrong contrast in some editors.
- Small screens: very fine moving detail can read as speckle on a phone. Say so if it applies.

## Frame rate

Choose the frame rate for where it will be used. 30 fps sits cleanly in a 30 or 60 fps YouTube timeline; 24 or 25 suits footage shot at those rates.

## Sound

See `sound-design.md`. For Level 1: `make_sounds.py` for the kit, a cue sheet that names the page's own beats, `mix_sound.py`, `master_audio.py`. Our mix had 15 cues, each exactly on its beat.

## A before and after

To show why transforms matter, render two of the shots as a plain cross-dissolve and put it beside the same stretch of the real ad. One page with a mode switch does both. It is the fastest way to show someone the difference.
