# Checks before you show anything

You cannot watch a video play and you cannot hear. So check by reading frames and by measuring, say exactly what was checked, and say what was not.

## Picture

| Check | How | Catches |
|---|---|---|
| The whole piece on one sheet | `frame_sheet.py out/ad.mp4 out/sheet.jpg --every 0.5` | Wrong shot order, a subject off centre, a dead hold, a colour cast |
| Every frame around each join | `frame_sheet.py ... --from 2.8 --to 3.2 --every 0.04` | A stop, a pop, a duplicate frame |
| Single frames at full size | `frame_sheet.py ... --full`, then open them | Soft focus, smeared small text, wrong characters |
| Three frames in a row over fine patterns | the same, 1 frame apart | Shimmer on dots, lines and grids |
| The delivered file, zoomed in | Frames from the final 4K file, cropped to the detail | Faults that a 1080p preview hides |
| Against the real thing | Result beside the real product photo | Wrong proportions, logo position, a missing or extra part, text order |
| Centre | The sheet, with the centre of each frame in mind | A subject that drifts off the middle |
| Motion on holds | Two frames a second apart on every hold | A frozen frame |
| Text | Read every word on the sheet | A typo, a word over the product, a title that never leaves |

For generated clips, also:

| Check | How | Catches |
|---|---|---|
| Hidden cuts | `find_jumps.py shots/*.mp4` | A jump one frame into a take |
| Joins | `find_jumps.py a.mp4 b.mp4 c.mp4 --joins` | A shot that does not start where the last one ended |
| Joined speed | The report from `join_shots.py` | The camera slowing to a stop at a keyframe |
| After an upscale | `ffprobe` for size, frame count and frame rate; a frame before and after | A changed frame count, a colour shift, re-invented text |

Count things that can be counted (hands, buttons, fingers, links, numbers on a scale) and read every character of text against the reference. Models add and drop these quietly.

## The file

```bash
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt,color_space,nb_frames:format=duration -of default=nw=1 out/ad.mp4
```

- The size and frame rate that were asked for.
- H.264, `yuv420p`, tagged BT.709. A file written with non-standard colour settings shows the wrong contrast in some editors.
- The length matches the plan to the frame.
- Stereo AAC at 48 kHz, if there is sound.

## Sound

| Check | How | Target |
|---|---|---|
| Sync | The table `mix_sound.py` prints | Every cue 0 ms from its beat |
| Loudness | `master_audio.py out/ad.mp4 --check` | About -14 LUFS integrated |
| True peak | the same | At or below -1 dB |
| The ending | "last 0.5 s" in the same output | Near silence, below about -45 dBFS |
| Balance | The stem levels `mix_sound.py` prints | Music well above effects; voice clear of both |
| Repeats | The mixer's own warning | No effect used more than twice |
| Voice words | Transcribe the placed voice track | Every line present, in its slot |

## What to say when you hand over

- **Checked**, and how: "every keyframe and take at six or more frames against the real photos; every join by frame difference; every cue on its beat; loudness measured".
- **Not checked**: playback at full speed by eye, and the mix by ear. Ask for one watch-through with sound.
- **Known flaws**, each with a timecode and how visible it is. Small, brief flaws in motion are normal in generated footage; hiding them is not.
- **Departures from the brief or the storyboard**, and why.
- **Housekeeping**: anything you installed, created outside the project, or removed. Do not delete the person's files or rejected takes.
