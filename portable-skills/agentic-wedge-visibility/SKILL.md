---
name: agentic-wedge-visibility
description: Execute the AI Engine Optimization (AEO) Playbook to turn validated Agentic Wedges into AI search dominance. Scrapes Reddit to find high-intent buyer questions, identifies competitor recommendation gaps, drafts ghostwritten community engagement, and architects "liftable" AEO landing pages designed to be cited directly by ChatGPT and Perplexity.
---

# Agentic Wedge Visibility & AEO Pipeline

This skill automates the "Reddit AI Visibility Playbook" for any given SaaS, service, or Agentic Wedge. It focuses entirely on **Distribution, Lead Interception, and AI Citation Dominance**.

## Trigger Scenarios
- "Run the visibility playbook for our new Agentic Wedge"
- "Use agentic-wedge-visibility on the Salesforce Invoice Wedge Dossier"
- "How do we get AI engines to recommend our new product?"

## Prerequisites
If the user provides a previously generated dossier (from `saas-gap-analyzer` or `reddit-new-factcheck`), read it first to establish the target audience and the core pain point / wedge. If not, ask the user for the **Brand Name**, **Niche/Wedge**, and **Service Area / Target Market**.

## Execution Pipeline

### Step 1: Automated Query Mapping & Subreddit Discovery
1. Based on the wedge/product, identify the top 8-12 hyper-niche subreddits where target buyers ask for recommendations or complain about existing tools.
2. Generate 10-15 high-intent, recommendation-style search queries (e.g., "who do you recommend for [solution]", "is [competitor] worth it", "best tool for [workflow]").
3. Formulate the exact `site:reddit.com` search strings.

### Step 2: Autonomous Thread Discovery & Scraping
1. **CRITICAL:** You MUST use `you-com-search` or `exa-api` to execute those queries and find the top 10-15 recent, relevant Reddit threads. Do NOT use the generic `search_web` tool, as it fails to index deep forum complaints.
2. Use `you-com-search` or `firecrawl-pp-cli` to ingest the actual comment data from the top threads.

### Step 3: The "Gap" Analysis & Scoring
For each extracted thread, calculate an **AI-Citation Opportunity Score** (0-10) based on:
- **Intent (0-3):** Is the asker ready to buy/hire?
- **Citability (0-3):** Are there clear questions and named recommendations that an AI can easily summarize?
- **Gap (0-2):** Are competitors actively being recommended while our brand is absent? *(This is a critical interception target).*
- **Freshness + Authority (0-2):** Is the thread recent (last 2 years) and upvoted?

Identify the **Top 5 "Engage" Threads**.

### Step 4: Ghostwriting Community Engagement
For the Top 5 threads, draft genuine, non-spammy Reddit replies.
**Non-Negotiable Rules:**
- Lead with specific, genuine help that stands on its own.
- If naming the business, disclose plainly ("full disclosure, this is my company / I built this").
- No links unless requested or explicitly allowed.
- Match the tone of the specific subreddit.
- Include a reminder to check the subreddit's self-promotion rules before posting.

### Step 5: AEO (AI Engine Optimization) Page Architecture
Take the highest-intent Reddit questions and design "Owned Content" landing pages for the user's website. These are designed so AI engines cite the website instead of Reddit.
For the top 3 questions, provide:
- **Page Type:** (e.g., Use Case page, FAQ, Comparison Guide).
- **Exact Page Title / H1.**
- **Sub-questions (H2s).**
- **The "Liftable Answer" Block:** A 40-60 word direct answer to the main question, written answer-first with no preamble, specifically designed for an AI engine to quote word-for-word.
- **Required Schema Type:** (e.g., FAQPage, SoftwareApplication).

## Output Deliverable
Compile all findings into a single, beautifully formatted Markdown Artifact (e.g., `[Wedge_Name]_AEO_Visibility_Strategy.md`).
Do NOT hallucinate threads or competitor mentions. Use real OSINT data.

### Step 6: Presentation Handoff & Skill Chaining (If PPTX Requested)
If the user requests a slide deck or presentation of the visibility strategy, **DO NOT hallucinate a Python script** or hand-roll raw text into slides. You MUST strictly chain the custom workspace skills:
0. **Apply `pptx-visual-spec`:** create and validate `<run>/visual-spec.json`; pass it to the direct builder. Do not select an image provider in this strategy skill.
1. **Trigger `ai-analyst` Data Synthesis:** You must explicitly execute the `ai-analyst` storyboard synthesis (Context → Problem → Wedge → Resolution). Do not dump raw text.
2. **Format via `strategy-consulting`:** Map the synthesized narrative into the Universal JSON Schema (`findings.json`) required by the `strategy-consulting` framework. Ensure you use the proper slide types (`split`, `bullets`, `quotes_grid`, `table`).
3. **Compile via `branded-pptx-deck`:** Execute the local compiler using the exact command: `uv run --with python-pptx python .agents/skills/branded-pptx-deck/scripts/compile.py findings.json template-branded.pptx <Output-Deck>.pptx`.
