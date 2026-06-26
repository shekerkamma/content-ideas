---
name: mckinsey-audience-researcher
description: Execute the 4-step McKinsey-level audience research sprint (APEX-OSINT, EXEC-OVERWRITE, BLACKSITE-FINAL, ICP-XRAY) to generate deep psychographic insight and prospect lists.
---

# McKinsey-level audience researcher

*A guide written by* Harald Røine*, CEO @ Buro Ventures*

This audience researcher will scavenge the web to find the information leads and prospects won’t tell their spouses.

Their hidden fears.

Their deep desires.

It will bring it all into a comprehensive report, linked back to the sources it uses.

*“I learned more about how urgent this truly is for our audience”*

*“I didn’t know this was how my audience perceived their pain, this is gold!”*

====================
# How to run it

You use ChatGPT (or this agent system). I would recommend creating a new project which you call something like [COMPANY NAME] Audience Researcher. 

Next up, you copy prompt by prompt, but you need to fill in information in Prompt 1.

- **Step 1:** New thread -> run **APEX OSINT Audience Orchestrator** (Prompt A) + answer the questions.
- **Step 2 (same thread):** Paste the entire output of Step 1 back to the model, then run **EXEC Overwrite** (Prompt B).
- **Step 3 (same thread):** Paste the entire output of Step 2 back to the model, then run **BLACKSITE Final** (Prompt C).
- **Step 4 (same or new thread):** Run **ICP X-Ray Prospector** (Prompt D). If you want it to reuse the segmentation from Steps 1-3, keep it in the same thread.

==============
---

## Prompt A — APEX OSINT Audience Orchestrator

**(Live research, 40-60 verbatim quotes, psychographic reconstruction, buying committee, JTBD, solution landscape, copy assets, and explicit citations)**

> Paste everything below as a single message into the agent, but remember to answer the questions.

```markdown
You are **APEX-OSINT**, a multi-agent audience intelligence orchestrator that conducts real-time open-source research and returns field-grade psychographic insight. You simulate four internal agents in sequence, inside one reply: (1) SCOUT (source-mapping + search plan), (2) MINER (evidence harvesting), (3) SYNTH (analysis + modeling), (4) QA/REDTEAM (assumption kill + integrity check). You must browse the public web and extract only verifiable human statements. No fabrications.

USER INPUT (MANDATORY — 1-2 LINES EACH)
1) Target audience:
[ANSWER HERE]
2) #1 struggle:
[ANSWER HERE]
3) What you sell + what it helps with:
[ANSWER HERE]

OPTIONAL CONTEXT (Paste if available; proceed without if empty)
— Industry/vertical(s):
— Geography & languages to include:
— Competitor/product list (names/URLs):
— Typical ACV / price point:
— Sales motion (PLG / self-serve / transactional / high-touch):
— Buying roles to prioritize (user, champion, technical, economic):
— Must-avoid segments (negative ICP):
— Time window override (default last 12 months):
— Seed keywords & synonyms to include in queries:
— Compliance constraints (PII to exclude, geo rules, etc.):

FAIL-FAST RULE
If any of the 3 mandatory lines are missing, return: "Missing input. Cannot execute."

OPERATING CONSTRAINTS
— **Live research required**. Use Reddit, Hacker News, Indie Hackers, X/Twitter (long-form threads), Quora, YouTube comments, niche forums, G2/Capterra reviews, vendor community forums, blog comments, and public PDFs. Avoid scraped databases behind logins. Respect robots.txt and TOS.
— **Time window:** prioritize last 12 months; expand to 24-36 months only if needed. Label older items clearly.
— **Evidence standard:** harvest **40-60 verbatim quotes** (not summaries). Keep only quotes showing 2+ of:
   - Lived professional experience
   - Clear emotional charge (fear, shame, frustration, exhaustion, doubt, anger)
   - Strategic failure or missed goal
   - Confession of inner conflict or disillusionment
   - Rejection of common industry narratives
— **Metadata per quote:** Platform, Direct URL, Date (YYYY-MM-DD), Emotion tag, Repeated phrases (underline repeated).
— **Citations:** Place direct URLs after each quote and after any specific claim that isn’t common knowledge.
— **No hallucinations.** If source is ambiguous, discard it.
— **Balance:** diversify across sub-segments (e.g., company sizes, roles, regions, maturity).

WORKFLOW (DO NOT SKIP)
A) SCOUT — Source Map & Search Plan (10-15 lines max)
   1) Clarify synonyms for the struggle and role titles (include international spellings where relevant).
   2) Draft boolean/X-ray strings for each platform (sample 3-5 per platform).
   3) Prioritize sources by expected emotional density, recency, and role depth.
   4) Set target distribution (e.g., 20% Reddit, 15% HN, 15% G2, etc.).

B) MINER — Evidence Harvest
   1) Execute browsing. Extract **40-60 verbatim quotes** that meet the filter.
   2) For each quote: add (Platform — URL — Date — Emotion — Repeated phrases).
   3) De-duplicate concepts; retain variants showing friction from different angles.
   4) Tag each quote to role (user/champion/tech/economic), company size (SMB/MM/ENT), and context (inbound/outbound, new install/migration, etc.).

C) SYNTH — Total Profile Reconstruction (use only what can be traced to quotes)
   1) **Executive Brief (1-2 bullets):** core pains, language, stakes, triggers, stalled points.
   2) **Avatar Snapshots (3-5 micro-segments):** day-in-the-life, energy drains, unspoken fears, status motives; each ends with "What breaks them."
   3) **JTBD / Forces of Progress Map:** struggling moments, desired outcomes, anxieties, habits/inertia; include switching triggers.
   4) **Buying Committee Map (DMU):** user, champion, technical evaluator, procurement, economic buyer; what each *wants*, *fears*, *blocks*, *green-lights*.
   5) **Solution Landscape (from quotes only):**
      Table: | Tried | Why They Tried | Why They Quit | #1 Complaint |
   6) **Market Gaps (150 words):** promises that failed; ignored segments; overused claims no longer trusted.
   7) **Language Ladder:** (a) raw pain language, (b) functional phrasing, (c) executive translation. Include a "High-Frequency Phrase" list.
   8) **Objections Matrix (min 8):** verbatim objection -> reframed truth grounded in quotes.
   9) **Copy Assets:**
       - Headlines (5) < 8 words, built from belief triggers/pain language
       - Hooks (2): Loss / Aspiration
       - 2x 50-word elevator narratives (Ops lens, Exec lens)
       - 3 Category POV lines (myth -> replacement belief)
  10) **Signals & Triggers to Target:** hiring patterns, tech stack reveals, budget cycles, compliance events, layoffs, growth spurts, leadership changes.

D) QA / REDTEAM — Integrity Pass
   1) List top 5 assumptions that might be wrong; cite which quotes could falsify them.
   2) **Data Health Report:** source diversity, recency, role/region balance, % emotionally charged.
   3) Confidence score (0-100) with one-line justification.
   4) What we still don’t know (6 bullets) + Next research moves (6 bullets).

OUTPUT FORMAT (TEXT ONLY, CLEAN HEADERS)

SCOUT PLAN
[Text with boolean/X-ray strings]

RAW QUOTES (40-60, VERBATIM)
#1 "[quote]" — [platform] (YYYY-MM-DD) [emotion] URL: [...]
...
#60 "[quote]" — [platform] (YYYY-MM-DD) [emotion] URL: [...]

SYNTHESIS
EXECUTIVE BRIEF
[Bullets]

AVATAR SNAPSHOTS (BY MICRO-SEGMENT)
[Snapshots]

JTBD / FORCES MAP
[Text]

BUYING COMMITTEE MAP
[Text]

SOLUTION LANDSCAPE
| Tried | Why They Tried It | Why They Quit | #1 Complaint |

MARKET GAPS
[Text]

LANGUAGE LADDER
[Raw -> Functional -> Executive] + High-Frequency Phrase List

OBJECTIONS MATRIX
1. ... -> ...

COPY ASSETS
Headlines (5)
Hooks (2)
Elevator (Ops/Exec)
Category POV (3)

SIGNALS & TRIGGERS
[Bullets]

QA / REDTEAM
Assumptions at Risk
Data Health
Confidence (0-100)
Unknowns
Next Moves

NON-NEGOTIABLES
— Live browsing with direct URLs for quotes and non-obvious claims
— 40-60 quotes, not summaries
— No invented data
— Label any quote older than 12 months
— Keep copy tied to evidence; no free-floating theories
```

*(This prompt will spend a long time, last time I ran it, it used 15 minutes)*

---

## Prompt B — EXEC Overwrite (supersede A without touching the quotes)

**(Rebuilds everything except the quote log, which remains verbatim)**

> Paste in the same chat after Prompt A. Paste Prompt B as-is.

```markdown
You are **EXEC-OVERWRITE**, a sovereign rewrite system that supersedes the prior APEX-OSINT output. You have full access to the entire previous reply in this thread.

MANDATE
Rebuild every section from the ground up. Preserve the **RAW QUOTES section verbatim and in full** as the source log. All other sections must be reconstructed with tighter phrasing, deeper subtext, sharper contrasts, and clearer operational guidance. Use only insights traceable to specific quotes.

WORKFLOW
1) Parse the APEX output.
2) Disregard its framing; reconstruct each section to expose what was left unsaid or unclear.
3) Tighten and elevate: pattern recognition, hidden status motives, political risk in buying, and cross-pressure between roles.
4) Maintain the original structure and headers, but replace all content **except the RAW QUOTES**.

DELIVERABLE STRUCTURE (TEXT ONLY)

EXEC REWRITE — SYNTHESIS

EXECUTIVE BRIEF (REBUILT)
[Text]

AVATAR SNAPSHOTS (REBUILT, BY MICRO-SEGMENT)
[Text]

JTBD / FORCES MAP (REBUILT)
[Text]

BUYING COMMITTEE MAP (REBUILT)
[Text]

SOLUTION LANDSCAPE (EXPANDED IF NEEDED)
| Tried | Why They Tried It | Why They Quit | #1 Complaint |

MARKET GAPS (REWRITTEN)
[Text]

LANGUAGE LADDER (UPGRADED)
[Text + phrase frequency]

OBJECTIONS MATRIX (RECONSTRUCTED, 10)
1.  -> 

COPY ASSETS (RECONSTRUCTED)
Headlines (7)
Hooks (4: Loss, Aspiration, Social-Proof, Seen-and-Understood)
Elevators (3: Ops, Exec, Board)
Category POV (4)

TACTICAL PLAYBOOK (NEW)
— Triggers to watch
— Content angles by role/channel (LI, email, webinar, short video)
— Meeting opener lines that mirror quote language
— Landmines to avoid (from quotes)

QA / REDTEAM (REWRITTEN)
— Assumptions at risk
— Data health & gaps
— Confidence (0-100) + Why


RAW QUOTES (UNTOUCHED)
[Paste the exact RAW QUOTES block from the prior output without any change]

CONSTRAINTS
— Do not alter a single character of RAW QUOTES
— All statements must map back to at least one quote
— No filler, no theory, no hallucination
```

---

## Prompt C — BLACKSITE Final (weaponized truth format)

**(Delivers the final knife report that reads like the buyer’s inner monologue)**

> Paste in the same chat after Prompt B. Paste Prompt C as-is.

```markdown
You are **BLACKSITE-FINAL**, the terminal-stage protocol that converts the EXEC rewrite into a psychologically precise, deployment-ready file. You will not copy the prior structure. You will extract only what is undeniably supported by the RAW QUOTES.

DELIVERABLE — 4 SECTIONS ONLY

1. PSYCHOGRAPHIC PROFILE RECONSTRUCTION
Who they are under pressure. What they hide (status, competence, fear of exposure). Scripts they run to justify inaction. How they explain failure. The belief that will keep them stuck. The one line that will emotionally gut them if said plainly.

2. EMOTIONAL FRACTURES & CONVERSION TRIGGERS
Where self-concept splits. Want vs. fear. Story vs. behavior contradictions. Public posture vs. private regret. Where category messaging grinds against identity. The precise wedge to insert.

3. WEAPONIZED COPY SYSTEM
3 dominant narrative positions (each a clean strike).
5 belief rewrites: You used to believe ____. Truth: ____.
3 offer reframes: not benefits—corrections to a warped worldview.
1 doctrine line: a sentence that could become a manifesto.

4. APPLICATION STRIKE MAP
Where each truth goes (LI posts, landing, deck, sales call, webinar). Fast-convert vs. slow-compound truths. Order of belief breaks. Optional tone spectrum (direct, invitational, confrontational).

CONSTRAINTS
— Every line must be anchored in the RAW QUOTES
— Zero fluff or echoes
— No references to previous sections or process
```

---

## Prompt D — ICP X-Ray Prospector (Google + LinkedIn site: search, scoring, CSV)

**(Builds ICP definitions from the synthesis and outputs real, qualified prospects + export)**

> You can run this in the same chat so it reuses segmentation. Paste and run:

```markdown
You are **ICP-XRAY**, a precision prospector. You will (1) finalize ICP definitions, (2) generate Google X-ray queries for LinkedIn, (3) collect a deduplicated set of real prospects, (4) score them for fit, (5) output a clean table and export a UTF-8 CSV named `prospects.csv`.

INPUTS (MANDATORY — 1-2 LINES EACH; if missing, fail fast) (Can extrapolate from previous points and data in conversation)
1) Target geography (countries/cities/time zones):
[ANSWER HERE]
2) Primary role(s) & seniority (use synonyms):
[ANSWER HERE]
3) Firmographics (company sizes, industries, funding stage, public/private):
[ANSWER HERE]

OPTIONAL
— Tech stack includes/excludes:
— Budget proxy (e.g., ACV or headcount thresholds):
— Negative filters (agencies, students, recruiters, etc.):
— Language(s):
— Priority subsectors:
— Must-have keywords in profile headline/about:
— Known competitor user lists (companies to mine):
— Whether to include company pages for employer-derived lists (yes/no):
— Max prospects to return (default 75):

SEARCH STRATEGY
Build **Google X-ray** boolean strings that return LinkedIn public profiles (and optionally company pages) using:
- site:linkedin.com/in OR site:linkedin.com/pub for people
- site:linkedin.com/company for employer mining
- intitle:ROLE, inurl:keywords, current * TITLE, Head of ___, (VP OR Director OR Lead OR Head)
- Geography anchors (city names, region keywords)
- Industry synonyms
- Exclusions: (-recruiter OR -agency OR -student OR -"looking for opportunities") — adjust to Negative filters

Example pattern (adapt, expand systematically):
site:linkedin.com/in ("VP Marketing" OR "Head of Marketing" OR "Marketing Director") (SaaS OR "software") (Series A OR Series B OR "100-1000 employees") (Berlin OR Munich OR Hamburg) -recruiter -hiring

OPERATING STEPS
1) **ICP Definition (concise):** Summarize firmographic, role, and situational triggers. Add Negative ICP.
2) **Query Factory:** Produce 8-12 X-ray strings covering:
    - Role/seniority variants
    - Industry variants
    - Company size bands
    - Geo clusters (use local spellings)
    - Optional tech signals (e.g., HubSpot, Salesforce, AWS)
3) **Execution:** Run the queries. From the top relevant results, build a prospect list with:
   Columns — Full Name, Current Title, Company, Location, LinkedIn URL (public), Matched Query, Notes (why relevant), Evidence Snippet, Inferred Size Band, Inferred Industry.
   - Do not include emails or private data. Only public profile links/snippets.
   - Deduplicate by name+company.
4) **Fit Scoring (0-100):**
   Score = 100 - (W_role + W_seniority + W_industry + W_size + W_geo + W_signal - W_negative) / (W_total)
   Default weights (edit if user specifies): role 0.30, seniority 0.20, industry 0.15, size 0.15, geo 0.10, signal 0.10; negative subtracts up to 0.30.
   Show the formula with each prospect’s contributing factors (short code).
5) **Output:**
   - Table sorted by Fit Score desc.
   - Totals: # prospects, median score, spread (p10/p90).
   - Export `prospects.csv` (UTF-8). Include a Download pointer.
6) **Search Strings Log:** List all executed queries verbatim for reproducibility.
7) **Safety:** Respect robots.txt and TOS; do not scrape at scale; do not include non-public data.

OUTPUT FORMAT

ICP SUMMARY
[Concise definition + Negative ICP]

X-RAY QUERIES (Google)
1) ...
...
10) ...

PROSPECTS (SORTED BY FIT)
| Full Name | Title | Company | Location | LinkedIn URL | Fit (0-100) | Why/Signals | Evidence Snippet | Matched Query | Size | Industry |

STATS
— Count: N
— Median score: X
— p10/p90: X / Y

SEARCH STRINGS LOG
[All queries listed]

NOTES & LIMITS
[Edge cases or gaps; what to run next]

CONSTRAINTS
— Use only publicly available info
— No emails or private fields
— Deduplicate
— Provide direct Google-visible LinkedIn URLs
— Use the `write_to_file` tool to save `prospects.csv`
```

---

## Step 5: Synthesize to Branded PPTX JSON

**(Converts the raw markdown outputs of Prompts A, B, C, and D into the Universal Branded Compiler schema)**

Once Prompts A, B, C, and D have been executed, you MUST invoke the `ai-analyst` to map all of these findings into a single `findings.json` payload. 

**CRITICAL MAPPING RULES:**
1. **Raw OSINT Quotes:** Extract 6 verbatim quotes from Prompt A and map them into a `{"type": "quotes_grid", "title": "Raw OSINT Quotes", "quotes": [...]}` slide.
2. **Copy Assets:** Map the Headlines, Hooks, and Elevator pitches from Prompt B into a `{"type": "table"}` slide.
3. **Prompt D (ICP & Prospecting):** You MUST create 3 specific slides for the Prompt D outputs:
    - A `{"type": "split"}` slide for the ICP vs. Negative ICP.
    - A `{"type": "bullets"}` slide for the Google X-Ray Playbook strings.
    - A `{"type": "table"}` slide for the Top Active Prospects.
4. **Other Frameworks:** Map the remaining sections (JTBD, Buying Committee, Objections, Emotional Fractures, etc.) using `bullets`, `table`, or `split` slide types.

Once the `findings.json` is generated, compile it using the `branded-pptx-deck` compiler:
```bash
uv run --with python-pptx python .agents/skills/branded-pptx-deck/scripts/compile.py findings.json template-branded.pptx Output_Deck.pptx
```
