# Codex Cloud video-analysis handoff

This directory contains locally acquired evidence for YouTube video
`KVMRSgy25fI`. Codex Cloud must consume these repository files instead of
attempting to access YouTube.

## Source

- URL: `https://www.youtube.com/watch?v=KVMRSgy25fI`
- Title: `EVERYTHING Codex Can Do That Claude Can't`
- Duration: `14:19` (`859.3s`)

## Cloud inputs

- `report.md` — local watch report with transcript and scene sampling details
- `watch/download/video.en-orig.vtt` — preserved native English captions
- `watch/download/video.en.vtt` — working caption copy
- `watch/download/video.info.json` — source metadata
- `corpus/full-test-corpus.md` — 25 timestamped demonstration scenarios
- `corpus/full-test-corpus.json` — machine-readable scenario corpus
- `corpus/scenario-pinned-cues/frames/` — 70 scene-specific hyperframes

The original video and intermediate frame caches are deliberately excluded
from the cloud handoff. The pinned frames are sufficient to inspect and test
the 25 documented scenarios. This is scene-aware sampled evidence, not an
exhaustive frame-by-frame copy of the video.

## Cloud acceptance checks

```bash
test -s runs/watch-KVMRSgy25fI/report.md
test -s runs/watch-KVMRSgy25fI/watch/download/video.en-orig.vtt
python3 -m json.tool runs/watch-KVMRSgy25fI/corpus/full-test-corpus.json >/dev/null
test "$(find runs/watch-KVMRSgy25fI/corpus/scenario-pinned-cues/frames -type f -name '*.jpg' -size +0c | wc -l)" -eq 70
```

Cloud tasks should cite repository-relative evidence paths and write their
derived output to a separate run directory. They must not redownload the
source or overwrite the preserved local evidence.
