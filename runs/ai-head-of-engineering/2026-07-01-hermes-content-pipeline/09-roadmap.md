# 09 - 30-Day Build Roadmap

## Week 1 - Foundation

### Monday-Tuesday

- Define target audience and editorial voice.
- Create source config schema.
- Select 10-20 initial sources.
- Create run folder, queue schema, and artifact naming conventions.

### Wednesday-Thursday

- Implement manual source scan.
- Implement source item normalization.
- Add basic run log.
- Confirm You.com/search wrapper behavior in the target host.

### Friday Deadline

Manual scan produces a source queue from configured sources.

### Rollback Trigger

If source extraction is unreliable by Friday, cut video/transcript sources and start with RSS/docs/news URLs only.

## Week 2 - Ranking And Research

### Monday-Tuesday

- Implement topic clustering.
- Implement ranking rubric.
- Add score explanations.

### Wednesday-Thursday

- Generate research briefs for top-ranked topics.
- Add citation/source checks.
- Add stale-source warnings.

### Friday Deadline

Top 5 opportunities and 3 sourced research briefs exist in the queue.

### Rollback Trigger

If clustering is weak, use rule-based topic grouping and manual topic approval.

## Week 3 - Draft Package

### Monday-Tuesday

- Generate article draft from approved brief.
- Add SEO/AEO structure pass.
- Add voice constraints.

### Wednesday-Thursday

- Generate LinkedIn, X, and newsletter variants.
- Add editorial status fields.
- Add approve/reject/revise workflow.

### Friday Deadline

Three draft packages are queued for editorial review.

### Rollback Trigger

If draft quality is weak, ship research briefs plus outlines instead of full articles.

## Week 4 - Hardening And Launch

### Monday-Tuesday

- Add cost caps.
- Add cron lock.
- Add failure summaries.
- Add GBrain/local memory write-back.

### Wednesday

- Run staging soak test with daily run.
- Review edge cases and source failures.

### Thursday

- Run production-like draft-only smoke test.
- Confirm no publish credentials are available to the workflow.

### Friday

- Launch draft-only content pipeline or delay if smoke test fails.

## Dependency Map

- Source config blocks source scan.
- Source scan blocks ranking.
- Ranking blocks research brief generation.
- Research brief blocks draft generation.
- Editorial status blocks memory write-back.
- Cost logging and cron lock block scheduled launch.

## Critical Path

Source config -> source scan -> ranking -> research brief -> draft package -> editorial queue -> smoke test.

## Friday Demos

- Week 1: source queue from configured sources.
- Week 2: ranked opportunities and sourced briefs.
- Week 3: draft packages in editorial queue.
- Week 4: scheduled draft-only run with cost and approval controls.

## Minimum Lovable Product At Day 21

Manual source scan, ranked topic list, research briefs, and draft outlines. Full article drafting can be added after launch if quality is not yet reliable.

