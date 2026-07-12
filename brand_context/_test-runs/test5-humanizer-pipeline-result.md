# Humanizer — Pipeline Mode Result

## Scenario
Simulating: `social-media-team` skill generates a LinkedIn post → calls humanizer as post-processing step.

## Pipeline Input (from upstream skill)
"In today's competitive landscape, leveraging AI-powered automation tools can help organizations drive unprecedented efficiency gains. It's worth noting that the most successful implementations start with a clear understanding of the problem space and a well-defined set of success metrics that align with broader organizational objectives."

## Pipeline Behavior
- Mode auto-selected: `deep` (voice-profile.md exists)
- Context loaded silently (no user-facing output)
- Steps 2-6 run silently
- Score delta: 2.4 → 8.1 (delta = 5.7, > 2 threshold → show summary)

## Pipeline Output (returned to calling skill)
"Most AI automation projects that work have one thing in common: they started with a specific problem and a specific number to hit. Not 'drive efficiency.' An actual metric. The tools are secondary."

## Score Summary (shown because delta > 2)
```
ORIGINAL: 2.4/10
REVISED:  8.1/10  (+5.7)

Changes:
  [4] AI cliches removed
  [3] buzzwords replaced
  [2] hedging phrases cut
  [3] voice markers added
```

## Pipeline Contract Verified:
- [x] Received text as input
- [x] Ran Steps 2-6 silently
- [x] Returned cleaned text (not saved — calling skill saves)
- [x] Showed score summary (delta > 2)
- [x] Did not show full change log (pipeline mode = minimal output)
