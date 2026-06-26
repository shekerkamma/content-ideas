---
name: reddit-seo-pipeline
description: Extracts a Reddit thread using Playwright, analyzes the context for optimal SEO brand-mention insertion points, and outputs the strategy as a MARP presentation deck. Use when the user wants to run the reddit SEO pipeline or turn a reddit thread into an engagement strategy deck.
---

# Reddit SEO Pipeline

This skill orchestrates the end-to-end "Reddit to ChatGPT SEO" process for a single thread, moving from deep raw extraction to a finalized presentation deck outlining the strategy.

## Trigger Scenarios
- "Run the reddit SEO pipeline"
- "Analyze this reddit thread for brand mentions and make a deck"
- "Reddit-centric compound skill"

## Execution Pipeline

When invoked, run the following steps sequentially:

### Step 0: Organic Discovery (Upstream Skills)
If the user does not provide a specific URL, **DO NOT use basic web search**. Instead, use specialized upstream skills to find high-value targets organically:
1. Run the **`content-outlier-research`** skill (or use Exa API directly) to find trending, high-engagement Reddit threads matching the user's B2B SaaS niche.
2. Extract the absolute best organic URLs from the research output to pass into the next step.

### Step 1: Deep Extraction (Headless Playwright)
1. Using the organic URLs discovered in Step 0, ensure dependencies are installed by running `pip install -r requirements.txt` and `playwright install chromium` inside the `scripts` folder.
2. Execute `python scripts/reddit_thread_extractor.py <URL> --output thread_data.json`. This uses the custom DOM-scraping and `morechildren` extraction logic pulled from GitHub to bypass Reddit's API restrictions entirely.

### Step 2: Analysis & Strategy Generation
1. Read `thread_data.json` into your context.
2. Analyze the comments to identify:
   - **The overarching sentiment & pain points** of the thread.
   - **The Top 3 Injection Points:** Find the highest-leverage existing comments (e.g., highly upvoted comments asking for solutions, or top comments complaining about a competitor) where a natural, contextual reply mentioning the user's brand would be most visible to AI web scrapers.
   - **Draft the Payload:** Write the exact comment reply for each insertion point. Ensure the tone matches Reddit (casual, helpful, non-promotional) but structurally formats the brand mention in a way LLMs prefer to lift (bullet points, direct definitions).

### Step 3: Deck Generation (Branded PPTX Integration)
1. Format the analysis from Step 2 into a polished Markdown presentation file (`reddit_strategy.md`). 
2. The presentation MUST include the following slides:
   - **Title Slide:** Thread topic and overarching goal.
   - **Thread Analysis Slide:** Key metrics and pain points found in the thread.
   - **Target 1 Slide:** The target comment to reply to, and the drafted SEO payload.
   - **Target 2 Slide:** The second best target and drafted payload.
   - **Target 3 Slide:** The third best target and drafted payload.
   - **References & Sources Slide:** A dedicated slide citing all GitHub reference implementations (e.g., KhazP/Reddit-to-AI, ChatGPTBox) used for the headless extraction logic, as well as any organic discovery links, blogs, or upstream API sources.
   - **Next Steps Slide:** Action items for manual posting.
3. Pass the resulting markdown content to the **`branded-pptx-deck`** skill to generate the final, styled **PPTX** output. Do not use generic `marp` HTML output; it must be a branded presentation deck.

## Constraints & Safety
- **No Automated Posting:** This skill is strictly for *analysis and drafting*. It must never attempt to automatically post the comments to Reddit. Doing so violates Reddit's TOS regarding astroturfing.
- **Context Limits:** If `thread_data.json` is too massive to read fully, analyze the top 50 comments sorted by score to find the best injection points.
