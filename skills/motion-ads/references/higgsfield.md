# Higgsfield: setup, models, money

Levels 2 and 3 use paid models. We reached all of them through Higgsfield, which puts image, video, voice, music and sound-effect models behind one account. Any service with the same kinds of models works the same way; the method does not depend on this one.

Everything here is what we ran in November 2026. Model names, prices and behaviour change. Check what is there before trusting a line of this page.

## Connect it

Two ways. Use whichever is present.

**The connector (Claude desktop app, Claude Code, claude.ai).** On higgsfield.ai, open MCP and press "Add Higgsfield to Claude", then continue. Higgsfield's tools then appear in Claude: generate an image, a video or audio, estimate a cost, wait for jobs, upload media, show the balance and the transactions, upscale a video. Ask the connector which models it has before choosing one.

**The CLI (a terminal).**

```bash
higgsfield auth login
higgsfield account status                 # plan and credits
higgsfield model list --video             # also --image, --audio
higgsfield model get kling4_0             # the parameters a model accepts
```

If neither is connected, say so and stop. Do not try to work around a missing login.

## Before the first paid job

1. **Agree a budget in credits** and write it down: `python3 scripts/credit_log.py start --budget 800`.
2. **Quote first.** Every job, before it runs.
3. **Log every job**: model, what it was for, the quote, the job id, and afterwards whether it was kept.
4. **Stop and ask before going over budget.** `credit_log.py can-spend 150` exits with an error if it would.
5. **Check the first charge on any model you have not used.** Compare the quote with the account's transactions. One of our jobs was quoted 37.5 credits and charged 150: the quote looked like a per-5-seconds price for a 20-second clip.
6. **Failed and refused jobs are refunded**, but confirm it in the transactions.

```bash
higgsfield generate cost kling4_0 --prompt "$(cat build/prompts/S4.txt)" --mode image-to-video --duration 5 --resolution 1080p
higgsfield account transactions --size 50
python3 scripts/credit_log.py add --model kling4_0 --what "shot 4, take 1" --quoted 18.75 --job 1a2b3c4d
python3 scripts/credit_log.py set 7 --charged 18.75 --verdict "kept"
python3 scripts/credit_log.py total
```

If other work is running on the same account, sum your own log rather than reading the account balance.

## The models that worked for us

| Job | Model | Settings we used | Price then |
|---|---|---|---|
| Keyframe stills | `nano_banana_pro` | 4K, 16:9, real photos attached as references | 4 |
| Exact text or one-change edits on a still | `gpt_image_2_6` | 4K, quality high or max | 3.25 to 12 |
| A shot that must join (first frame + last frame) | `kling4_0` | image-to-video, 5 s, 1080p, start image and end image | 18.75 |
| The same, cheaper | `kling_o3_flf` | 5 s, pro mode, sound off. A native 4K mode exists | 6.25 (30 at 4K) |
| Music | `elevenlabs_music_v2_5` | exact duration, instrumental forced, two takes at once | about 4 for 27 s |
| Sound effects | `mirelo_text_to_audio` | 2 to 10 s | 0.5 to 1.5 |
| Voiceover | `elevenlabs_v4` | one take as dialogue, stability 0.5, similarity 0.8 | about 1.6 a take |
| Transcription | `speech2text` | | well under 1 |
| 4K upscale of the joined picture | `bytedance_video_upscale` | pro, 4K | 150 for 20 s |

Not everything worked. A start-frame-only video model cannot land on the next shot's first frame, so it cannot be used for joins however good it looks. One "enhancer" turned out to be an SDR-to-HDR converter, not an upscaler, and took up to 44 minutes to return a file the same size. See the shoot-out in `level-3-product.md`.

Higgsfield also offers ready-made workflows for editing, sorting footage and adding text over video. We did not use them in these builds, so nothing here depends on them. If the person asks for one by name, read its own instructions first and treat it as untested.

## Commands

Media can be passed as a local file path (uploaded for you), an upload id, or the id of an earlier job, which is how one generated still becomes the reference for the next.

A keyframe still, with the approved hero and two real photos as references:

```bash
higgsfield generate create nano_banana_pro --prompt "$(cat build/prompts/K1.txt)" \
  --resolution 4k --aspect_ratio 16:9 --image <hero job id> --image refs/07.jpg --image refs/01.jpg
```

A shot from one keyframe to the next:

```bash
higgsfield generate create kling4_0 --prompt "$(cat build/prompts/S4.txt)" \
  --mode image-to-video --duration 5 --resolution 1080p --start-image build/keys/K3.png --end-image build/keys/K4.png
```

Music and an effect:

```bash
higgsfield generate create elevenlabs_music_v2_5 --prompt "$(cat build/prompts/music.txt)" --duration 20 --force_instrumental true --batch_size 2
higgsfield generate create mirelo_text_to_audio --prompt "$(cat build/prompts/sfx/press.txt)" --duration 2
```

A voiceover, after listing the voices:

```bash
higgsfield voices list
higgsfield generate create elevenlabs_v4 --dialogue '[{"text":"<the whole script>","voice_id":"<id>","voice_type":"preset"}]' --stability 0.5 --similarity_boost 0.8
```

Waiting for and fetching a job:

```bash
higgsfield generate wait <job id> --timeout 40m --interval 6s
higgsfield --json generate get <job id>        # status and result_url
```

## Things that bit us

- **`--wait` on create can hang** at submit or upload. When it hangs, no job exists and nothing is charged, but the command never returns. Submit without `--wait`, then use `generate wait` or poll `generate get`. `scripts/hf_submit.sh` does this, with a quote first and a retry if the submit stalls.
- **A cost estimate can hang** when given a job id as its video input. Upload the clip as a file first and pass the upload id.
- **Some models cannot quote.** If a tool cannot tell you the price, do not run it without asking.
- **Do not submit a second long job before the first has come back.** We paid twice for the wrong tool that way.
- **Content filters give false refusals** on harmless stills. Re-run them.
- **Run takes in parallel**, about three at a time, and do something else while they render.
- **Flag names differ per model** (`--aspect_ratio` on one, `--mode` on another). Read `higgsfield model get <model>` rather than guessing.

## The log to hand over

`credits.md` should let someone see, for every job: when, which model and settings, which prompt file, what it cost, the running total, the output file, and a one-line verdict ("kept as keyframe 3", "rejected: invented text"). The verdicts are worth as much as the costs: they are the record of what the models can and cannot do.
