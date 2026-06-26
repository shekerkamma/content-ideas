---
name: saas-gap-analyzer
description: Deep OSINT pipeline to analyze B2B SaaS platforms and discover "Agentic Wedges." Built as an autonomous Loop. Scrapes deep qualitative data from niche forums to find emotionally charged workflow complaints across diverse verticals. Outputs a massive, comprehensive Markdown dossier. No hallucinations.
---

# SaaS Gap Analyzer Loop (The "Agentic Wedge" Hunter)

This skill is designed as an **Autonomous Loop**. It systematically hunts through B2B SaaS platforms to find highly-profitable, proven Agentic Wedges (AI startups that co-exist with established platforms).

**CRITICAL RULE: NO HALLUCINATIONS.** You MUST use real OSINT tools (`search_web`, `pp-hackernews`, `pp-firecrawl`) to extract *actual* URLs and *actual* long-form verbatim quotes. If the search yields no data, the check fails. Do not invent data.

## How to run it

Run `/goal Run the saas-gap-analyzer loop` to trigger this pipeline. Follow the exact loop instructions below.

====================

## The Loop Blueprint

### 1. The Action (What to accomplish)
Dynamically pick a target SaaS platform by extracting a use case from the provided scorecard resource file `resources/Agent_Use_Cases.md` (which contains 25 Agentic Use Cases across 6 agent types and 11 key industries). Use this Markdown resource as your taxonomy to find diverse, high-value targets across all key industries. Do NOT rely on narrow or hardcoded examples.
For the chosen platform, perform a Pure Qualitative Deep-Dive:
1. **Community Discovery:** Use `search_web` to identify niche professional communities, deep subreddits, or dedicated forums where power users of this platform gather.
2. **Emotional Friction Extraction:** Scrape these long-form threads and forums for deep, emotionally charged complaints about manual workflows (e.g., "I waste 10 hours a week on this", "This workflow is a nightmare"). Extract entire raw threads, user context, and psychographics along with the URLs.
3. **Synthesis:** Combine the deep qualitative pain points to formulate an "Agentic Wedge" that solves this specific, painful manual bottleneck.

### 2. The Check (How to know if it worked)
Evaluate the findings against the "Emotional Intensity & Pain Threshold":
- **Passes if:** We extracted a high volume of long-form, emotionally charged complaints directly from niche communities that prove a specific manual workflow is a severe, recurring nightmare for users.
- **Fails if:** The complaints are generic, lack deep emotional friction, or if we cannot find dense qualitative data in niche forums proving the pain.

### 3. The Feedback (What to do next)
- **If it PASSES:** Compile a **Comprehensive Markdown Dossier** (e.g., `[PlatformName]_Wedge_Dossier.md`). This must be a massive, deeply detailed report (aiming for exhaustive depth, not brief summaries) that compiles the full raw forum threads, user psychographics, the exact pain points, and the proposed Wedge strategy. Do NOT generate a slide deck.
- **If it FAILS:** Discard the platform. Dynamically pick a completely different SaaS platform from a different vertical and run The Action again.

### 4. When to Stop
Do not stop based on an arbitrary number of wedges. The loop must systematically process **ALL use cases** listed in the `resources/Agent_Use_Cases.md` resource file (and scale up to 100+ use cases as the list grows). Finish and alert the user ONLY after you have exhausted the entire list of use cases, generating a Comprehensive Markdown Dossier for every single use case that passes the validation check.
