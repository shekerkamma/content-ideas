# 05 - Build Estimator

Blended rate: $125/hour.

## Feature Estimates

| Feature | Low | High | Cost Range | Confidence | Risks |
|---|---:|---:|---:|---|---|
| Source cluster config and schemas | 8 | 12 | $1,000-$1,500 | High | Poor source definitions, changing audience, malformed feeds |
| Source monitoring and normalization | 14 | 22 | $1,750-$2,750 | Medium | Source access limits, extraction failures, duplicate detection |
| You.com search integration wrapper | 8 | 14 | $1,000-$1,750 | Medium | Local wrapper mismatch, rate limits, livecrawl behavior |
| Topic ranking engine | 14 | 20 | $1,750-$2,500 | Medium | Weak scoring rubric, noisy inputs, over-ranking novelty |
| Research brief generation | 16 | 24 | $2,000-$3,000 | Medium | Citation quality, stale sources, context length |
| Draft article package generation | 18 | 28 | $2,250-$3,500 | Medium | Voice quality, hallucination, repetitive structure |
| Promotional variants | 6 | 10 | $750-$1,250 | High | Platform fit, tone, formatting |
| Editorial queue | 8 | 14 | $1,000-$1,750 | High | Status tracking, file naming, review conventions |
| GBrain/local memory write-back | 10 | 18 | $1,250-$2,250 | Medium | API availability, duplicate memories, provenance |
| Cost/run logging | 8 | 12 | $1,000-$1,500 | High | Token accounting gaps, multiple provider logs |
| Smoke tests and launch hardening | 14 | 22 | $1,750-$2,750 | Medium | Non-deterministic outputs, flaky source access |

## Roll-Up

- Total low: 124 hours / $15,500
- Total high: 196 hours / $24,500
- 30-day solo-dev capacity target: 160 hours

## Capacity Check

The high estimate exceeds 160 hours. To keep the first build inside 30 days:

- Keep only one article package format.
- Limit source clusters to 10-20 sources.
- Generate only three promotional variants.
- Use markdown queue, not dashboard.
- Use local memory write-back if GBrain wiring blocks progress.

## Most Likely Overrun

Research brief generation. Source quality, citation discipline, and extraction behavior can expand quickly.

## Most Likely Under-Run

Promotional variants. Once the draft package exists, variant generation is straightforward.

