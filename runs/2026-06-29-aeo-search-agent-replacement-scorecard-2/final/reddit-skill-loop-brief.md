# Reddit Skill Loop Brief

- Run: `2026-06-29-aeo-search-agent-replacement-scorecard-2`
- Purpose: use Reddit as semantic buyer-language evidence for AEO, not keyword matching and not automated posting.
- Status: `needs_external_retrieval` until real thread/comment exports are loaded.

## Skill Roles

- `reddit-new-factcheck`: qualify whether a semantic pain, objection, or comparison has real Reddit practitioner support.
- `reddit-seo-pipeline`: extract and analyze a known high-value Reddit thread; use for manual strategy only.

## Generated Fact-Check Pack

- `stage_outputs/reddit_factcheck_claim_pack.json` can be passed to `reddit-new-factcheck/scripts/old_reddit_evidence.py` or used with Exa/ScrapeCreators/logged-in Reddit discovery.
- Query strings are discovery aids only; the acceptance gate is semantic qualification.

## Queue

### rsq_001 - reddit-new-factcheck

- Source probe: `rsp_163`
- Topic: ad & creative generation at scale
- Probe type: `job_to_be_done`
- Candidate subreddit: `PPC`
- Fact-check question: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around ad & creative generation at scale?
- Extraction goal: Qualify whether real Reddit practitioner language supports the AEO pain, objection, or comparison frame.
- Evidence gate: accept only persona/workflow-matched posts or comments with concrete pain, workaround, objection, adoption signal, or comparison.

### rsq_002 - reddit-new-factcheck

- Source probe: `rsp_030`
- Topic: ai shopping / sales consultant
- Probe type: `job_to_be_done`
- Candidate subreddit: `Entrepreneur`
- Fact-check question: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around ai shopping / sales consultant?
- Extraction goal: Qualify whether real Reddit practitioner language supports the AEO pain, objection, or comparison frame.
- Evidence gate: accept only persona/workflow-matched posts or comments with concrete pain, workaround, objection, adoption signal, or comparison.

### rsq_003 - reddit-new-factcheck

- Source probe: `rsp_001`
- Topic: conversational support
- Probe type: `job_to_be_done`
- Candidate subreddit: `CustomerSuccess`
- Fact-check question: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around conversational support?
- Extraction goal: Qualify whether real Reddit practitioner language supports the AEO pain, objection, or comparison frame.
- Evidence gate: accept only persona/workflow-matched posts or comments with concrete pain, workaround, objection, adoption signal, or comparison.

### rsq_004 - reddit-new-factcheck

- Source probe: `rsp_114`
- Topic: doc summarization & drafting
- Probe type: `job_to_be_done`
- Candidate subreddit: `Entrepreneur`
- Fact-check question: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around doc summarization & drafting?
- Extraction goal: Qualify whether real Reddit practitioner language supports the AEO pain, objection, or comparison frame.
- Evidence gate: accept only persona/workflow-matched posts or comments with concrete pain, workaround, objection, adoption signal, or comparison.

### rsq_005 - reddit-new-factcheck

- Source probe: `rsp_143`
- Topic: legal research & drafting
- Probe type: `job_to_be_done`
- Candidate subreddit: `Lawyertalk`
- Fact-check question: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around legal research & drafting?
- Extraction goal: Qualify whether real Reddit practitioner language supports the AEO pain, objection, or comparison frame.
- Evidence gate: accept only persona/workflow-matched posts or comments with concrete pain, workaround, objection, adoption signal, or comparison.

### rsq_006 - reddit-new-factcheck

- Source probe: `rsp_085`
- Topic: messaging-channel chatbot
- Probe type: `job_to_be_done`
- Candidate subreddit: `CustomerSuccess`
- Fact-check question: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around messaging-channel chatbot?
- Extraction goal: Qualify whether real Reddit practitioner language supports the AEO pain, objection, or comparison frame.
- Evidence gate: accept only persona/workflow-matched posts or comments with concrete pain, workaround, objection, adoption signal, or comparison.

### rsq_007 - reddit-new-factcheck

- Source probe: `rsp_184`
- Topic: personalized marketing content
- Probe type: `job_to_be_done`
- Candidate subreddit: `PPC`
- Fact-check question: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around personalized marketing content?
- Extraction goal: Qualify whether real Reddit practitioner language supports the AEO pain, objection, or comparison frame.
- Evidence gate: accept only persona/workflow-matched posts or comments with concrete pain, workaround, objection, adoption signal, or comparison.

### rsq_008 - reddit-new-factcheck

- Source probe: `rsp_058`
- Topic: travel & booking planner
- Probe type: `job_to_be_done`
- Candidate subreddit: `Entrepreneur`
- Fact-check question: Do Reddit practitioners discuss concrete pain, workarounds, objections, or comparisons around travel & booking planner?
- Extraction goal: Qualify whether real Reddit practitioner language supports the AEO pain, objection, or comparison frame.
- Evidence gate: accept only persona/workflow-matched posts or comments with concrete pain, workaround, objection, adoption signal, or comparison.

### rsq_009 - reddit-seo-pipeline

- Source probe: `rsp_205`
- Topic: Add-On Collapse
- Probe type: `pattern_validation`
- Candidate subreddit: `Entrepreneur`
- Fact-check question: Which specific Reddit threads show a high-intent switching or comparison discussion around Add-On Collapse?
- Extraction goal: Extract candidate threads for manual analysis once a specific Reddit URL is found.
- Evidence gate: accept only persona/workflow-matched posts or comments with concrete pain, workaround, objection, adoption signal, or comparison.

### rsq_010 - reddit-seo-pipeline

- Source probe: `rsp_209`
- Topic: Data Moat Survival
- Probe type: `pattern_validation`
- Candidate subreddit: `Entrepreneur`
- Fact-check question: Which specific Reddit threads show a high-intent switching or comparison discussion around Data Moat Survival?
- Extraction goal: Extract candidate threads for manual analysis once a specific Reddit URL is found.
- Evidence gate: accept only persona/workflow-matched posts or comments with concrete pain, workaround, objection, adoption signal, or comparison.

### rsq_011 - reddit-seo-pipeline

- Source probe: `rsp_213`
- Topic: Seat Compression
- Probe type: `pattern_validation`
- Candidate subreddit: `Entrepreneur`
- Fact-check question: Which specific Reddit threads show a high-intent switching or comparison discussion around Seat Compression?
- Extraction goal: Extract candidate threads for manual analysis once a specific Reddit URL is found.
- Evidence gate: accept only persona/workflow-matched posts or comments with concrete pain, workaround, objection, adoption signal, or comparison.

### rsq_012 - reddit-seo-pipeline

- Source probe: `rsp_217`
- Topic: Workflow Layer Replacement
- Probe type: `pattern_validation`
- Candidate subreddit: `Entrepreneur`
- Fact-check question: Which specific Reddit threads show a high-intent switching or comparison discussion around Workflow Layer Replacement?
- Extraction goal: Extract candidate threads for manual analysis once a specific Reddit URL is found.
- Evidence gate: accept only persona/workflow-matched posts or comments with concrete pain, workaround, objection, adoption signal, or comparison.

## How To Use

1. For each `reddit-new-factcheck` item, discover or provide Reddit thread URLs using logged-in Reddit, Exa, ScrapeCreators, or `old_reddit_evidence.py` if reachable.
2. For each known URL, run `reddit-seo-pipeline` extraction and save thread JSON into this run.
3. Save old Reddit fallback output under `stage_outputs/reddit_evidence_raw/` or convert accepted posts/comments into `stage_outputs/reddit_threads.jsonl` / `stage_outputs/reddit_comments.jsonl`.
4. Rerun `aeo-evidence-sprint-loop`; the loop will normalize buyer language and rerun semantic pattern mining.

Do not count the queue itself as evidence. It is only the retrieval worklist.
