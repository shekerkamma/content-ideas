# Runbook — "Provide AI strategy for <niche area>"

The canonical consulting OS request. Stages map to the mission pipeline:
Operationalize (1–3) → Acquire delta (4) → Generate (5–6) → Transform (7).

## 1. Classify
- Match request against pack `keywords:` manifests → 1 primary + ≤2 secondary
  domains.
- No pack match → tell the user; offer to scaffold a pack from
  `domains/_template/` first, or proceed pack-less and say so in the
  deliverable status.

## 2. Load context (in order, stop when sufficient)
1. Read matched pack(s) in full.
2. **GBrain Recall** — search account name, vertical, and theme slugs before
   any new research (repo rule: recall before repeating research).
3. Read engagement folder if one exists; else scaffold
   `runs/<date>-<client-or-niche>-ai-strategy/`.

## 3. Freshness gate
- Pack `status: draft` or market sections >30 days old → an acquisition delta
  is REQUIRED before client-facing output, or the deliverable ships flagged
  `draft` with stale sections named.

## 4. Acquisition delta (only the gaps)
- Client-specific: their stack, announcements, hiring signals, financials.
- Pack gaps: anything marked **[NEEDS ACQUISITION]** that this engagement
  touches. Use Exa/firecrawl/content-research; verify primary sources.
- Raw notes → `runs/.../research/`; pack-worthy findings ALSO copied to
  `consulting-os/inbox/<domain>/` for later curation. Inbox is never cited
  directly.

## 5. Synthesize
- Strategy skeleton comes FROM the pack: its point of view, its maturity
  model/frameworks, its reference architectures — populated with client facts.
- Use `ai-strategy-brief` for one-pager, `ai-strategy-researcher` for the full
  document. Every claim: pack citation or fresh verified source.

## 6. Generate outputs
- Map requested deliverable to the output chain table in
  `docs/consulting-ai-os-architecture.md` §5.
- Decks: branded template + full PPTX QA gate; `reviewed` before delivery.
- Client-facing sends: always manual.

## 7. Write back (close the loop)
- Durable client/entity findings → GBrain (batched writes).
- Reusable domain insight → `consulting-os/inbox/<domain>/`.
- Anything the pack was missing that this run had to research → note it in
  the run status; that list IS the pack's next curation backlog.
- Report GBrain recall/write-back explicitly in the run status (repo rule).
