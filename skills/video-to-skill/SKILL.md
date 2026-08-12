---
name: video-to-skill
description: Use when a YouTube or other public video URL demonstrates a repeatable workflow you want to own as a Claude Code skill — "turn this tutorial into a skill", "learn this workflow from this video", "record-a-skill but from a link", "make a skill out of this demo". Watches the video, reconstructs the procedure, separates stated thresholds into editable judgment rules, forces every borrowed environment assumption to be resolved, and gates the result before install. Not for turning a video into slides (use video-to-deck) or for authoring a skill from a written spec (use skill-builder).
license: MIT
metadata:
  category: Agent Engineering
  version: '1.0'
  compatibility: Python 3 stdlib only. Requires the `watch` skill (yt-dlp + ffmpeg). Claude Code, Codex, or any host that reads agent Markdown.
---

# Video to Skill

Point at a public video where somebody demonstrates a workflow. Get back a
Claude Code skill that performs the same job with tools, gated so it cannot be
installed while it still contains guesses.

**Cost tier:** Sonnet for the derivation, Opus only if the procedure is
genuinely tangled. The expensive part is frames, not reasoning — Stage 1 is
transcript-only and decides whether the frame pass is worth buying at all.

## What this is adapted from, and what changed

Anthropic shipped **record-a-skill** in Claude Cowork: record your screen while
narrating, and Claude turns the recording into a replayable skill. This skill is
the Claude Code analogue with the input swapped — a **video URL**, not a
recording of your own machine. That swap changes four things, and the whole
design follows from them:

| | Cowork record-a-skill | This skill |
|---|---|---|
| Input | your screen, live | someone else's video, already published |
| Signal | event stream (real clicks, keystrokes) | ~1–2 fps of pixels + narration |
| Environment | yours by construction | theirs — every path, login, and extension is borrowed |
| Execution | computer-use replays the GUI | Bash / Playwright MCP / Read / Write / API |

Two of those are losses and two are gains, and it is worth being precise about
which is which.

**The losses.** You never get coordinates or selectors, and you never get the
demonstrator's logged-in session. Stage 6 exists entirely because of the second
one.

**The gains.** Coordinates were the least transferable part anyway — a
click at (840, 312) is worthless on a different screen, while "sort the channel
by latest, then compare each video's views against that channel's own median"
survives any redesign. And a published tutorial is *narrated for an audience*,
so it states intent and thresholds out loud far more than a person recording
their own screen ever bothers to. That narration is the most valuable thing in
the file, which is why Stage 5 gives it its own section.

Do not use this skill on a recording of your own screen. If you can record it,
record-a-skill in Cowork has the event stream and this one does not.

## Resolve the skill directory

Every command below runs a bundled script. Set `SKILL_DIR` to the absolute path
of the directory containing this `SKILL.md`. Guard once:

```bash
SKILL_DIR="<absolute path of the directory containing this SKILL.md>"
test -f "$SKILL_DIR/scripts/init_skill.py" || { echo "ERROR: bad SKILL_DIR=$SKILL_DIR" >&2; exit 1; }
```

You also need the `watch` skill. Resolve its directory the same way and call it
`WATCH_DIR` (commonly `~/.claude/skills/watch`):

```bash
WATCH_DIR="${WATCH_DIR:-$HOME/.claude/skills/watch}"
test -f "$WATCH_DIR/scripts/watch.py" || { echo "ERROR: watch skill not found at $WATCH_DIR" >&2; exit 1; }
python3 "$WATCH_DIR/scripts/setup.py" --check || echo "run: python3 $WATCH_DIR/scripts/setup.py"
```

Pick a run directory once and use it throughout:

```bash
RUN_DIR="${CONTENT_HOME:-$HOME/Documents/Content}/derived-skills/$(date +%Y-%m-%d)-<slug>"
mkdir -p "$RUN_DIR"
```

---

## Stage 0 — The fit gate

Most videos are not demonstrations. A talking-head explainer, a news roundup, a
conference keynote, or a review has no procedure in it, and deriving a skill
from one produces a confident file full of invention. Run this gate before
spending anything.

A video passes only if all three hold:

1. **Somebody performs a task on screen**, not merely describes one.
2. **The task recurs** — you would do it again next week.
3. **This host can execute the steps**: files, shell, HTTP, a browser via
   Playwright MCP. A workflow that lives entirely inside a native desktop app
   with no API and no web equivalent does not pass. Say so and stop.

If it fails, say which of the three failed and stop. Offering to build the skill
anyway is not helpful; the output would be fiction dressed as procedure.

## Stage 1 — Transcript pass (cheap, always first)

```bash
python3 "$WATCH_DIR/scripts/watch.py" "<url>" --detail transcript --out-dir "$RUN_DIR/watch"
```

From the transcript alone, establish:

- **The demonstration span** — the timestamp range where the task is actually
  performed. Intros, sponsor reads, community plugs, and outros are noise. On a
  15-minute tutorial the real span is often 4–6 minutes.
- **Stated thresholds and preferences** — every number and every "I'd say
  anything over X", "I don't go past Y", "I always Z". These become Stage 5.
- **Deictic cues** — "click here", "you can see", "make sure it's sorted by",
  "notice this". These are moments where the screen carries information the
  words do not. Collect their timestamps.

Judge the cues yourself; do not regex them. "Look, the point is…" is rhetoric,
not a pointer. This is the same reason `watch` leaves `--timestamps` selection
to the model.

## Stage 2 — Capture the screen states

Two things silently destroy this stage on screencasts. Check both before
reading a single frame.

### 2a. Confirm the download is HD, not 360p

`watch` takes whatever format yt-dlp offers by default. Under YouTube's SABR
restriction that is often **format 18, 640x360** — and nothing errors. A 360p
frame cannot render terminal text, a URL bar, or a code diff, so raising
`--resolution` just upscales blur at 4x the token cost.

```bash
python3 -c "import sys; sys.path.insert(0,'$WATCH_DIR/scripts'); import frames; \
print(frames.get_metadata('$RUN_DIR/watch/download/video.mp4'))"
```

If `width` is under 1280, re-download with the multi-client extractor args,
which usually restore the full format ladder:

```bash
yt-dlp -F --extractor-args "youtube:player_client=default,mweb,web_embedded" "<url>"
yt-dlp --extractor-args "youtube:player_client=default,mweb,web_embedded" \
  -f 137 -o "$RUN_DIR/hd/video1080.mp4" "<url>"    # 137 = 1920x1080 h264, video-only
```

Video-only is correct here: the transcript is already captured, so audio is
dead weight. If only 360p is ever offered, say the derivation is
**transcript-led with unreadable frames** rather than pretending otherwise.

### 2b. Use `hyperframes.py`, not `--detail token-burner`, on screencasts

`token-burner` is uncapped but still gates on `SCENE_THRESHOLD = 0.20`, tuned
for filmed video with real cuts. A screencast changes one pane while browser
chrome, editor frame, and webcam overlay hold still — those transitions never
score 0.20. Measured on a 61-minute coding tutorial:

| Mode | Frames | Worst blind spot |
|---|---|---|
| `--detail token-burner` (threshold 0.20) | 86 | **7m10s** |
| `hyperframes.py` (threshold 0.10 + gap fill) | 470 | 39s |

The threshold is a module constant with no CLI flag, which is why this needs
its own script. It reuses watch's extraction and perceptual dedup rather than
reimplementing them:

```bash
python3 "$SKILL_DIR/scripts/hyperframes.py" "$RUN_DIR/hd/video1080.mp4" \
  --out-dir "$RUN_DIR/hf" --threshold 0.10 --max-gap 40 --resolution 1280
```

The **gap fill** is the part that matters most. Without it, a stretch with no
frames is indistinguishable from a stretch where nothing happened, and a
derivation cannot tell the two apart — it will quietly conclude the workflow
skips from minute 34 to minute 41. Every run prints `max gap` and writes a
`manifest.json`; if max gap is large, the capture is not trustworthy yet.

### 2c. Read against the manifest, not blindly

470 frames is more than one context should swallow. Use `manifest.json` to
select: even-sample across the demonstration span for the arc, then add frames
at the timestamps where the transcript says a command was run. Read in batches
and align each to the transcript by its `time` field.

Do not skip the sparse-looking stretches on the assumption they are idle. That
assumption is exactly what 2b exists to make checkable.

Where the frame budget is genuinely tight, spend it on the **execution**
segments, not the narrated overview. The overview tells you the intended shape;
the execution shows what the commands actually emit, which is where a
derivation gets its real content and every gotcha.

If the demonstration span exceeds ~10 minutes of *distinct* work, split it and
derive one skill per coherent sub-task. A skill that does two jobs routes badly
and is tuned by nobody.

## Stage 3 — Reconstruct the procedure as tool routes

This is the translation step, and the place where derived skills most often go
wrong. **Do not transcribe clicks.** For each action the demonstrator performed,
write down what they *achieved*, then choose how this host achieves it:

| What you saw | Wrong (mimicry) | Right (tool route) |
|---|---|---|
| Typed a channel name, clicked Videos, sorted by latest | "click the Videos tab" | fetch the channel's recent uploads — `Bash` (yt-dlp / API) or `Playwright MCP` |
| Eyeballed views against other videos | "look at the numbers" | compute the ratio against the channel's own median — `Bash` |
| Screenshotted each hit into Figma | "paste into Figma" | render a sorted HTML report — `Write` |

Every step carries exactly one route: `Bash`, `Playwright MCP`, `Read/Write`,
`API`, or `BLOCKED-ON-USER`. A step whose route is `BLOCKED-ON-USER` halts the
run when reached — it does not get silently skipped, and it does not get
approximated.

Steps performed off-screen, or in a cut, were never demonstrated. Mark them as
gaps rather than inferring them.

## Stage 4 — Scaffold with provenance attached

```bash
python3 "$SKILL_DIR/scripts/init_skill.py" \
  --name <kebab-case-name> \
  --url "<url>" \
  --work-dir "$RUN_DIR/watch" \
  --out-dir "$RUN_DIR/staged"
```

This writes a staging copy only. It refuses to scaffold into a live skills tree,
because a half-filled skill sitting in `~/.claude/skills` is discoverable and
will be invoked before it is finished.

It reuses the metadata `watch` already downloaded, so the upload date costs no
extra network call. That date is load-bearing: it is how a future reader knows
when to stop trusting the UI shown in the video.

## Stage 5 — Separate judgment from procedure

The thresholds collected in Stage 1 go into `## Judgment rules` as editable
policy, each carrying the timestamp it came from — not inlined into step text.

The distinction is not cosmetic. Steps describe mechanism and change when a tool
changes. Judgment describes *what counts as a good result* and changes when you
change your mind. Burying "anything over 2.5× is worth keeping" inside step 4
means the one number most likely to need tuning is the hardest thing in the file
to find.

Attribute honestly: a threshold the demonstrator stated is theirs, not a law.
Write it as "the demonstrator used 2.5× (video 10:39)" so a future reader knows
it is a starting point rather than a finding.

## Stage 6 — Resolve environment bindings

This stage has no counterpart in Cowork's record-a-skill, and it is the entire
difference between the two. Cowork recorded *you*, so the paths, the logins, and
the installed extensions were already correct. Here every one of them is
borrowed.

Enumerate everything that was true only because of the demonstrator's machine:
browser extensions doing work on screen, saved logins, paid tool tiers, local
file paths, regional defaults, an account with data yours does not have.

Resolve each one as exactly one of:

- **confirm** — verified present here too
- **substitute** — same job, different mechanism on this machine
- **drop** — it existed only for their setup
- **BLOCKED-ON-USER** — needs a credential or a human decision

Never resolve by assuming. A binding guessed wrong yields a skill that fails
silently somewhere else, which is strictly worse than one that refuses to start.
Any step needing a logged-in session is `BLOCKED-ON-USER` by default, and no
credential is ever written into the skill, its references, or any run artifact.

## Stage 7 — Gate, then install

```bash
python3 "$SKILL_DIR/scripts/check_derived_skill.py" "$RUN_DIR/staged/<name>"
```

The gate fails on: unfilled placeholders, a missing or empty `## Judgment
rules`, any `UNRESOLVED` binding row, a missing `## Verification` command,
absent provenance, credential-shaped strings, and a name that collides with an
already-installed skill.

Install only on exit 0, and only where the user asked:

```bash
cp -r "$RUN_DIR/staged/<name>" ~/.claude/skills/
```

In this repo, a skill going into `skills/` must also pass the repo-wide gate:

```bash
python3 scripts/check_skills.py
```

## Stage 8 — Execute it. This is the stage that validates the skill

Everything before this produces a *hypothesis about a workflow*. Reading frames
tells you what someone appeared to do; only running it tells you what the
workflow actually does. The gate enforces this: without an execution record in
`## Verification`, `check_derived_skill.py` fails.

Execute on the narrowest real case — one channel, one invoice, one repo — in a
throwaway location. Then **verify the result independently** rather than
believing the run's own report; an agent reporting its own success is the same
failure the derivation is trying to avoid.

Feed every correction back into SKILL.md, the bindings, and the provenance file.
This is not bookkeeping. It is the only step that converts a plausible file into
a true one, and it routinely rewrites the derivation:

> Running `ai-blueprint-build-loop` falsified four derived claims. The largest:
> the demonstrator says at 06:57 that `/feature` cuts the git branch. It does
> not — `/implement` does. Both the transcript and the derivation inherited the
> author's own mistake about his own tool, and no amount of re-reading frames
> would have caught it. One command settled it.

Record in `## Verification`: **`Executed <YYYY-MM-DD>`**, the version or commit
run against, and what was independently confirmed.

**When execution is genuinely blocked** — a paid service, hardware you lack, a
destructive action — write `NOT EXECUTED` explicitly and pass
`--allow-unexecuted`. That turns the failure into a warning and forces the
status into the file, so nobody downstream mistakes a hypothesis for a tested
skill. Never route around the rule by deleting the section.

---

## Host Compatibility

| Host | Status |
|---|---|
| Claude Code | Full. `Read` renders frames as images, which Stage 2 depends on. |
| Codex CLI / Desktop | Full, with `WATCH_DIR` pointed at the Codex install (`~/.codex/skills/watch`). Frame reading depends on the host's image support; without it, run Stage 1 and derive from transcript alone, and say the derivation is transcript-only. |
| Any host reading `AGENTS.md` | Scripts are stdlib Python and shell out to `yt-dlp`/`ffmpeg`, so both scaffold and gate work anywhere. |

Nothing here depends on a Claude-only UI field. `AskUserQuestion` is an
enhancement for Stage 6; on hosts without it, present the unresolved bindings as
a numbered list and wait for the user's answers.

### Tool Mapping

The route names Stage 3 assigns are capabilities, not Claude tool names. Read
them through this table on other hosts:

| Route | Claude Code | Codex / other hosts |
|---|---|---|
| `Bash` | `Bash` | shell execution |
| `Read/Write` | `Read`, `Write`, `Edit` | file read/write |
| `Playwright MCP` | `mcp__playwright__*` | any MCP browser server, or the `agent-browser` skill |
| `API` | `Bash` + `curl`, or an MCP server | same |
| `BLOCKED-ON-USER` | `AskUserQuestion` | numbered prompt in chat |

A derived skill that names a Claude-only tool in its steps has been written
wrong: name the capability, and let the host bind it.

### Source / Tool Order

This overrides the global research order, and the override matters:
under the default order the model would reach for GBrain and web search to
resolve an unclear step. Here that is the failure mode, not the fix — filling a
procedural gap from the open web produces a plausible step that was never
demonstrated, which is exactly the invention Stage 0 exists to prevent.

1. **Frames** — what was actually on screen. Authoritative on every factual
   question about what happened.
2. **Transcript** — stated intent, thresholds, and reasoning. Authoritative on
   *why*, and the only source for judgment rules.
3. **Video metadata** — upload date, title, channel; provenance only.
4. **This host's own environment** — what is installed, what is on PATH, what a
   command actually returns. Authoritative on how to execute a step.
5. **Official docs for a tool the derivation introduces** — permitted only for
   a tool *you* chose in Stage 3 (its flags and behavior), never to reconstruct
   what the demonstrator did.

Where the three video sources disagree, the screen wins. An auto-generated
summary shown inside the video is not a source; it is a claim to check.

Never web-search to fill a gap in the demonstration. Mark it as a gap.

## Judgment rules

Editable policy for this skill. Tune these; do not hardcode them into the stages.

- **Transcript before frames, always.** Frames are the entire token cost. A
  transcript pass costs a few thousand tokens and tells you where to spend.
- **Verify source resolution before raising `--resolution`.** Upscaling a 360p
  frame to 1024px costs 4x the tokens and adds no information. Check the source
  width first (Stage 2a); the fix is a better download, never a bigger frame.
- **Coverage before fidelity.** A sparse capture with 7-minute holes produces a
  confident derivation of a workflow that was never shown. Get max-gap under a
  minute first, then spend what is left on resolution.
- **Captions are not authoritative for anything typed.** Auto-captions rendered
  `/overview` as "slashoverview" and dropped four commands entirely. Any
  command, path, flag, or filename must be read off a frame.
- **One skill per coherent task.** If the demonstration covers two jobs, emit
  two skills. Combined skills route badly and get tuned by nobody.
- **A demonstrated step beats a described step.** When narration and screen
  disagree, the screen is what happened; note the discrepancy rather than
  silently picking one.
- **Prefer the demonstrator's *why* over their *how*.** The how is bound to a
  UI that will change. The why is the part worth keeping.
- **Cap derivation at the demonstration span.** Deriving from a full 15-minute
  upload imports the sponsor read and the outro as if they were steps.
- **Popularity is not fit.** A video's view count says nothing about whether its
  workflow suits your constraints. A 3-million-view tutorial and a 400-view one
  get the same Stage 0 gate.
- **The demonstrator is not authoritative about their own tool.** Narration is
  evidence of intent, not of behavior. Where narration, on-screen text, and a
  live run disagree, the ranking is: execution, then screen, then narration.
- **Verify the run independently.** A derived skill that reports its own
  success has proved nothing. Re-check the artifact yourself — hit the
  endpoint, read the file, inspect the branch.

## Limits

- **No event stream.** Pixels at 1–2 fps plus narration. Fast actions, keyboard
  shortcuts, and anything in a jump cut were never captured. The gaps are marked,
  not filled.
- **No inherited session.** Nothing logged-in transfers. Auth is always
  `BLOCKED-ON-USER`.
- **Expiring evidence.** Third-party UI in a video ages from the day it was
  uploaded. Provenance records that date precisely so a future failure gets
  diagnosed as staleness rather than a bug.
- **Native desktop apps are out of scope** unless they expose an API or a web
  equivalent. Stage 0 rejects these rather than pretending.
- **Derivation is not execution.** Passing the frontmatter, bindings, and
  provenance rules means the skill is well-formed and honest about its
  assumptions. Only Stage 8 tells you it is *true* — which is why the gate
  now fails without an execution record rather than accepting a command block
  as a substitute for having run one.

## Security & permissions

- Runs `yt-dlp` and `ffmpeg` locally through the `watch` skill against a public
  URL; no account, no session cookies, no posting.
- Writes only into the run directory and, on an explicit final copy, the skills
  directory the user named. `init_skill.py` refuses to scaffold into a live
  skills tree.
- `check_derived_skill.py` scans for credential-shaped strings and fails the
  gate rather than warning, because a derived skill is a file people copy.
- Recording-side warnings from Cowork apply in reverse here: you are consuming
  someone else's published video. Do not derive from private, unlisted, or
  paywalled material you were not given the right to reuse, and keep the
  provenance file intact so the source is always attributable.

**Bundled scripts:** `scripts/init_skill.py` (scaffold + provenance),
`scripts/check_derived_skill.py` (pre-install gate).
