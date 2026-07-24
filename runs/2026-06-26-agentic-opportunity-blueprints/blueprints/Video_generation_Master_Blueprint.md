---
status: reviewed
use_case: "Video Generation"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Video Generation Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** creative, marketing, and production leaders.

**Later ICPs:** campaign teams once one video brief proves the rough-cut loop.

**Pain wedge:** video generation and editing still require manual tooling and
multiple passes.

**Incumbent weakness:** video suites are powerful but not workflow-native for
business teams.

**Agentic disruption thesis:** generate first-pass video and variant edits from
a brief.

**Why now:** gen-video tools are improving and business teams need faster
content loops.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 25/30**

The score is inferred from high video workload, editing bottlenecks, and the
clear need for faster first-pass cuts.

- Problem realness: 8/10
- Solution fit: 8/10
- Buying signal + reachability: 9/10

**Who has the problem:** marketing and creative teams producing high-volume
video.

**Current workaround:** manual editing and agency workflows.

**Switching reason:** speed and variation at lower cost.

**Payment signal:** creative production budgets.

**30-day reachability:** one video brief and one asset type can prove the
wedge.

**Verdict: PROCEED, but keep the output edit-ready.**

## 2. The 30-Day Scope Definition

**Project name:** Video Draft Copilot

**Validated problem:** businesses need first-pass videos and variants, not
fully manual cuts.

**Target user:** marketer or editor.

**Core hypothesis:** the agent can generate a rough cut and handoff edit-ready
outputs.

### In Scope

1. **Brief ingest**
   - Acceptance criterion: video brief and source assets are loaded.
2. **Rough cut generation**
   - Acceptance criterion: first-pass video or clip structure is produced.
3. **Variant edits**
   - Acceptance criterion: alternate cuts are produced for review.

### Explicitly Out Of Scope

- Complex multi-track timeline UI.
- Full post-production suite.
- Timelime scrubbing as a primary interaction.
- Unreviewed publish to channels.

### Week-By-Week Milestones

- **Week 1:** ingest brief and source assets.
- **Week 2:** generate rough cut.
- **Week 3:** add transcript sync and variant edits.
- **Week 4:** pilot one content format.

**Dependencies:** source assets, transcript sync, review owner, export path.

**Acceptance test:** one brief produces a ready-to-review rough cut and an
alternate version.

**Top risks:** asset mismatch, poor cuts, and rendering failures.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: review console.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for briefs and transcripts.
- Auth: SSO plus asset-store credentials.
- Database: Postgres for briefs, clips, renders, approvals.
- Observability: OpenTelemetry and render metrics.
- Hosting: cloud app with queue worker.

**Architecture:** brief -> ingest assets -> generate rough cut -> review ->
export. The agent focuses on semantic clipping and edit-ready outputs.

**Critical design decisions:**

1. Do not build a complex NLE UI.
2. Keep transcript sync accurate.
3. Charge by finished minute, not by seats.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/video/ingest` | ingest brief / assets | bundle | project id | service token | retry queue |
| POST | `/api/video/cut` | generate rough cut | project id | cut artifact | service token | fallback to transcript only |
| POST | `/api/video/render` | render output | cut id | render result | service token | block on missing assets |

### Folder / Module Structure

- `app/video/`
- `app/api/video/`
- `services/cut/`
- `services/render/`
- `workers/export/`
- `lib/transcript/`

### Environment Variables

- `ASSET_STORE_KEY`
- `RENDER_API_KEY`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `EXPORT_BUCKET`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Video editor | high | Premiere / Resolve already exist | BUY / REUSE | not the wedge |
| Rough-cut generation | medium | manual editing is the pain | BUILD | core wedge |
| Transcript sync | medium | needed for semantic clipping | BUILD | high leverage |

**Bottom line:** reuse the editing ecosystem and build the draft generator.

## 5. MVP ROI Business Case

**Current-state cost model:** editing time, agency labor, and render iteration.

**Agentic MVP cost model:** generation, rendering, review, and storage.

**Pricing options:**

1. Fixed pilot.
2. Per finished minute.
3. Enterprise production package.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low video volume | 12-18 months | month 14+ | narrow |
| Base | faster rough-cut delivery | 6-9 months | month 8-12 | strong fit |
| Upside | many variants per campaign | 3-5 months | month 4-6 | high leverage |

**Formulas**

```text
Monthly value =
  edit time saved + agency spend reduced + render iteration reduced
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if export quality is poor, keep the product as a cut
assistant only.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Adobe Premiere Pro | editor | industry standard | heavy manual work | subscription | `runs/2026-06-26-agentic-opportunity-blueprints/source/VideoEditing_Competitor_Teardown.md` |
| Frame.io | review | collaboration | collaborator pricing traps | seats / collaborators | `runs/2026-06-26-agentic-opportunity-blueprints/source/VideoEditing_Competitor_Teardown.md` |
| DaVinci Resolve | editor | powerful | specialized training | subscription / free | `runs/2026-06-26-agentic-opportunity-blueprints/source/VideoEditing_Competitor_Teardown.md` |
| Wipster / Vimeo Review | review | simple review flows | manual clipping | subscription | `runs/2026-06-26-agentic-opportunity-blueprints/source/VideoEditing_Competitor_Teardown.md` |

**Direct threats:** Frame.io and Descript.

**What not to build:** a complex multi-track timeline UI.

**Agentic wedge:** semantic auto-clipping, outcome-based pricing, and
elimination of timeline scrubbing.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| rough cut | brief loaded | generation runs | playable draft produced | playback test |
| sync | transcript available | cut runs | captions align | transcript test |
| variant | base cut approved | variant runs | alternative edit produced | review diff |

### Edge Cases

- Missing source asset.
- Transcript mismatch.
- Render failure.
- Unsupported aspect ratio.
- Duplicate cut request.
- Review timeout.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| briefs | marketer | brief table | project owner | per run | required fields |
| assets | source store | asset table | source system | batch / realtime | checksum |
| cuts | agent | cut table | agent | per run | transcript alignment |
| approvals | reviewer | approval table | reviewer | realtime | immutable |

**Retention and deletion:** retain approved cut lineage, delete transient
drafts after retention, and keep render history.

**Privacy/security:** asset rights and tenant isolation matter; enforce access
controls and provenance.

**Analytics questions:** which cut styles perform best and which sources create
the most render failures?

## 9. Deployment Sequencing

**Pre-deploy checklist:** brief, assets, transcript sync, reviewer owner,
rollback flag.

**Staging:** generate-only, then review.

**Production sequence:** one format, one brief type, one review path.

**Smoke test:** one brief produces a playable cut.

**Rollback:** disable generation and keep manual editing only.

**Observability:**

- Logs: brief, asset, cut, render.
- Metrics: time to rough cut, render success, edit rate.
- Alerts: transcript mismatch, render failure, asset missing.
- Dashboards: rough-cut throughput and edit hotspots.

## 10. Post-Launch Iteration Plan

**Metrics:** time to rough cut, variant throughput, and edit rate.

**Week-by-week:**

- Week 1: add another asset type.
- Week 2: improve semantic clipping.
- Week 3: tighten transcript sync.
- Week 4: package for another format.

**Pivot signals:** keep it cut-only if render quality is weak, and avoid
timeline UI creep.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/VideoEditing_Competitor_Teardown.md` - video-editing incumbent map and semantic auto-clipping wedge.
- Adobe Premiere - https://www.adobe.com/products/premiere.html - accessed 2026-06-26 - professional video editing and generative features backdrop.
- Frame.io - https://frame.io/ - accessed 2026-06-26 - review and collaboration backdrop.
- Descript - https://www.descript.com/ - accessed 2026-06-26 - AI video editing and transcript-first workflow backdrop.
- These incumbents show that the wedge is semantic auto-clipping and edit-ready output, not a complex timeline replacement.
- The draft should stay focused on first-pass generation plus transcript sync, because that is where the buyer feels the time savings.
- A good first sale is a narrow format like a 30-second social cut or product teaser, where the brief is clear and the expected output is edit-ready.
- The product should preserve export quality and captions, because those are the non-negotiable checks before any publish step.
- In other words, the assistant should remove the tedious clipping work while leaving creative judgment and final publish control with the user.
- That keeps the product inside a defensible wedge: rough cuts, transcript-aware edits, and fast iteration, not a full post-production suite.
- Keeping the scope cut-only also prevents timeline feature creep from swallowing the actual wedge.
- This is a production assistant for first-pass work, not a replacement for professional editing craft.
