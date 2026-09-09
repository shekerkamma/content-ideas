# Storyboard format

Provider-agnostic. The gate reads this and nothing else; it never contacts a
vendor and needs no key.

## Beat fields

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Stable name. A beat that cannot be named cannot be reviewed. |
| `kind` | yes | `scene` or `transition`. A transition is a beat, not a gap. |
| `visual` | yes | What is on screen and what the camera does. |
| `vh` | yes | Scroll distance in viewport heights. **A decision, not a derivation.** |
| `copy` | one of | Headings, supporting line, calls to action. |
| `copy_waived` | one of | Why this beat carries none, e.g. "No copy - let the motion lead". |
| `clip` | no | Which source clip this beat scrubs. Several beats may share one. |
| `clip_seconds` | no | Footage length. Independent of `vh`. |
| `continues_from` | no | `{"clip": "<parent>", "frame": "last"}` — declares the seam. |
| `sourced` | no | `true` marks a credibility claim as verified rather than invented. |

## Why vh and clip_seconds are separate

A six-second clip can span one viewport height of scroll or five. Frame count
improves temporal sampling; it does not lengthen the experience. The gate fails
a plan where every beat's `vh` is the same multiple of its `clip_seconds`,
because that is footage length wearing a pacing plan's clothes.

Conversely, stretching a handful of frames across a long scroll produces stepped
playback. Budget the distance first, then ask whether the clip has the frames to
fill it — and request a longer or separate clip when it does not.

## Why seams are declared, not inferred

`continues_from` names the exact parent clip and frame. Longer scroll distance
cannot change what is visible in the source frames, so a seam that was never
planned cannot be repaired by pacing. The generation order the gate emits
guarantees a parent clip is produced and inspected before its child is
requested.

## Thresholds

Defaults live at the top of `scripts/check_story.py` and are policy, not physics:

```python
MIN_COPY_VH = 1.0        # copy below this is never read
MIN_BEAT_VH = 0.4        # below this nothing registers as a beat
MAX_BEAT_VH = 8.0        # above this the page reads as stalled
DURATION_COUPLING = 0.05 # ratio spread under this = inherited, not budgeted
```

Change them deliberately and say why. A gate whose threshold moves to make a red
run go green has stopped measuring anything.
