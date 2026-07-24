# 08 - Pre-Launch Auditor

## Launch Gate

Launch only as a draft-only internal workflow. Publishing remains manual.

## Edge Cases

1. No sources return new items.
2. One source returns malformed content.
3. Duplicate source items appear across feeds.
4. A source URL redirects.
5. A source blocks automated access.
6. Transcript is missing for a video.
7. Search returns stale articles.
8. Search returns low-authority sources.
9. Source item date is missing.
10. Source item language is not English.
11. Topic cluster merges unrelated items.
12. Ranking overweights recency.
13. Ranking overweights source popularity.
14. Ranking ignores business relevance.
15. Research brief has citations but weak claim support.
16. Research brief cites inaccessible pages.
17. Draft includes unsupported claims.
18. Draft repeats source wording too closely.
19. Draft has no clear business point of view.
20. Draft is too generic.
21. Promotional variant changes the claim meaning.
22. Markdown frontmatter is malformed.
23. Queue file name collides with an existing draft.
24. Review status is missing.
25. Memory write-back duplicates old entries.
26. Memory write-back stores low-confidence claims.
27. Daily run exceeds cost cap.
28. Model routing uses expensive model for extraction.
29. Cron runs twice.
30. Previous run has not finished before next run starts.
31. Network call times out.
32. Search API returns rate-limit error.
33. LLM call returns empty output.
34. LLM output violates required schema.
35. GBrain is unavailable.
36. Local disk path is missing.
37. Operator changes source config during run.
38. Editorial queue contains rejected drafts in next run context.
39. Draft accidentally includes private notes.
40. Secrets appear in logs.
41. Source URL contains tracking parameters.
42. Citation list and article body disagree.
43. Article title overclaims.
44. Content angle conflicts with existing published content.
45. Pipeline writes outside the run folder.
46. Cost log fails silently.
47. Run summary says success despite skipped sources.
48. Manual approval state is ignored.
49. Publish-ready label is applied without review.
50. Recovery run overwrites prior artifacts.

## Security Gaps To Check

- API keys are only in env files or secret manager, never repo artifacts.
- Hermes write permissions are limited to expected workspace paths.
- Publishing credentials are not available to the draft pipeline in v1.
- Search and extraction logs do not store secrets.
- GBrain write-back includes provenance and confidence.
- Cron lock prevents concurrent runs.

## Production Readiness Checklist

- Source config finalized.
- Daily cost cap configured.
- Model routing configured.
- Search provider configured.
- GBrain/local memory write-back tested.
- Run logs written.
- Editorial queue path tested.
- Schema validation tested.
- Approval state respected.
- Manual publish boundary confirmed.

## Smoke Test

1. Run source scan on 10 configured sources.
2. Confirm at least 20 items land in the source queue or record source failures.
3. Generate top 5 ranked opportunities.
4. Generate 1 research brief from the top opportunity.
5. Generate 1 draft article package from that brief.
6. Confirm citations map to source URLs.
7. Confirm promotional variants are marked as drafts.
8. Reject the draft and verify it is not reused as approved.
9. Approve a revised draft and verify memory write-back.
10. Confirm no publish action occurs.

