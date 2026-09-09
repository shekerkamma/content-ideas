# Scroll story gate

A pre-generation check for scroll-scrubbed pages: it reads a storyboard and
refuses plans that will fail after the footage is paid for.

**This is a reference, not a loaded skill.** It gates a workflow this repo has
not yet run — there is no configured provider for scroll-scrub asset generation
(`KIE_AI_API_KEY` unset), and no scroll-scrub project exists under `runs/`.
Keeping it out of `skills/` avoids paying its catalog cost every session for a
job that has not started. Promote it back — add a `SKILL.md`, copy to the skill
trees — when a scroll-scrub build becomes real.

The page builder itself is `nateherk-design:scroll-craft`, an installed plugin
with its own engine, encode script and 23k words of references. This gate does
not duplicate it; it only covers the go/no-go before generation, which
scroll-craft leaves to judgement.

## Run it

```bash
python3 docs/scroll-story-gate/check_story.py <storyboard.json>          # 0 clean, 1 blocked, 2 findings
python3 docs/scroll-story-gate/check_story.py <storyboard.json> --plan   # + generation order
```

Format and thresholds: [plan-format.md](plan-format.md).
Fixtures: `fixtures/clean.json` passes, `fixtures/broken.json` fires 11
findings, `fixtures/coupled.json` isolates exactly one so the duration-coupling
branch is proven rather than assumed. `tests/test_scroll_story_gate.py` keeps
all three honest.

## What it enforces

- **Scroll distance is budgeted, not inherited from clip length.** A plan whose
  every beat sets `vh` as the same multiple of `clip_seconds` is footage length
  wearing a pacing plan's clothes.
- Copy-bearing beats get at least 1.0vh, or the text is never read.
- A beat with no copy waives it explicitly — silence is indistinguishable from
  an oversight.
- Every cross-clip seam names its parent frame; the emitted order produces a
  parent before its child.
- Credibility claims need `sourced: true`, because a render will never catch an
  invented testimonial.

Provider-agnostic by design, and a test asserts it: no vendor is named anywhere
in the gate or its docs.

## Provenance

Derived from comparing `Barty-Bart/gpt-6-astra-10k-websites` against the
installed `scroll-craft`. That comparison mostly favoured scroll-craft — 1,211
lines of engine and 23k words of references against the prompt's 2,720 words,
and deeper on seams (82 vs 2), holds (106 vs 8) and pacing (20 vs 6). Its
frame-index formula transfers nothing, since the engine already implements
clamping, decode management, preloading and reduced-motion.

The pre-generation check is the part that did not already exist here.
