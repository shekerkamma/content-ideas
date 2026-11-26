# The storyboard

The storyboard is the cheapest place to change the ad. It is also the only place the person directs before work is spent. Make it, show it, and stop.

## Before you draw it, ask (only what you cannot work out)

- What is the product and who is it for?
- How long, and what shape (16:9, 9:16, 1:1)?
- What is the one thing the viewer should remember?
- Is there a video whose style this should follow? (If so, run the reverse-engineer pass first. See `style-and-meta-prompting.md`.)
- What is the last thing on screen: a web address, a logo, a line?
- Voiceover or not? Music or just effects?
- For paid levels: what is the credit budget?

Do not ask about things you can decide well yourself. Decide, and write the decision on the board so it can be changed.

## Size

- 12 to 20 seconds is 6 to 8 shots. A shot shorter than a second reads as a flicker; one longer than four needs something changing inside it.
- One idea per shot.

## What every shot says

| Field | What to write |
|---|---|
| Time | Start and end in seconds |
| Title | Three or four words |
| On screen | What the viewer sees, in plain words. Name the real asset used |
| Moves | What moves and how: the camera, the subject, the background. Always something |
| Becomes | **How this shot turns into the next.** The most important line on the board |
| Sound | What is heard, and on which motion. Leave it empty if nothing changes |
| Text | Only if words appear: the exact words, where, and how they arrive |

If you cannot fill in "Becomes" without writing "fades to" or "cuts to", the two shots do not belong next to each other yet. Find the shape they share: a circle that is a lens, then a dial, then a logo; a line that is a horizon, then an underline; a camera move that simply continues.

## The header

Above the shots, put the whole ad in two sentences and the rules that hold for every shot (for example: one camera, no cuts; subject on the centre mark; one key light; no voiceover).

## Frames

Each card should have a picture, even a rough one:

- Level 1: render rough stills of the page with `render_page.mjs --stills`.
- Level 2: frames pulled from the footage at the chosen moments.
- Level 3: the real reference photos, cropped to the framing you intend. Do not generate keyframes before approval: they cost credits.

If there is no picture yet, write a one-line sketch of the framing instead.

## Making the board

1. Copy `templates/storyboard.html` into `storyboard/`.
2. Write `storyboard/board.js` next to it. `examples/board-eink-display.js` is a filled-in one.
3. Render it to one image:

```bash
node scripts/render_page.mjs storyboard/storyboard.html --stills storyboard/out --at 0
```

The red mark in the middle of every frame is the centre of the screen. The subject of each shot should sit on it.

## The gate

Show the image and say, in one or two lines, what you would like a decision on. Then wait.

- "Approved": build exactly what the board says.
- Changes: redraw the board, show it again. Do not start building on a half-approved board.
- If the build later has to depart from the board (a shot that could not be made), say so, and update the board to match what was built so the two never disagree.

For an edit of real footage, the cut list (`level-2-footage.md`) is the storyboard: one line per shot with its source time, its place in the edit and what it shows. Show that for approval, with a sheet of the chosen frames.
