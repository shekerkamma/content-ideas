# AEO Audit: Acme AEO

- Domain: `acme-aeo.example`
- Market: US
- Objective: Find where AI answers recommend competitors instead of Acme AEO.
- Status: draft

## Visibility Summary

- Captures analyzed: 2
- Target mentions: 0
- Competitor mentions: 4
- Target visibility rate: 0%

## Recommendations

### rec_001: competitor recommended (high)

Create or refresh comparison content that directly addresses the buyer prompts where competitors appear and the target brand is absent.

- Evidence ids: cap_001, cap_002
- Expected impact: Increase eligibility for recommendation and comparison-style AI answers.
- Effort: medium
- Confidence: medium

### rec_002: citation gap (high)

Build crawlable owned pages and pursue third-party citations that describe the target brand in category, comparison, and problem-solution language.

- Evidence ids: cap_001, cap_002
- Expected impact: Improve source availability for AI answers that rely on cited pages.
- Effort: high
- Confidence: medium

## Query Evidence

### q_001: best enterprise AI search optimization platforms

- Engine: sample
- Mentioned entities: Profound, AthenaHQ
- Citation domains: profound.com, athenahq.ai
- Raw answer: `stage_outputs/raw/cap_001.txt`

### q_003: alternatives to Profound for enterprise AI search optimization

- Engine: sample
- Mentioned entities: AthenaHQ, Peec AI
- Citation domains: athenahq.ai, peec.ai
- Raw answer: `stage_outputs/raw/cap_002.txt`
