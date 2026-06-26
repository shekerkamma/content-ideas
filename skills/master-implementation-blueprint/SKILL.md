---
name: master-implementation-blueprint
description: End-to-end pipeline to autonomously generate a 10-artifact Master Implementation Blueprint for Agentic AI Use Cases.
---

# Master Implementation Blueprint Pipeline

This skill acts as the **Blueprint Generation Engine**. It takes an Agentic AI Use Case and autonomously pumps out a comprehensive 10-part implementation strategy. Although we are using this for market positioning and capability demonstration rather than traditional $100K-tier delivery, the artifacts must reflect elite execution capability and precise tech stack details.

## The Goal
For the target use cases listed in the dashboard (`resources/Agent_Use_Cases.md` & `resources/Agent_Use_Cases_Phase2.md`), generate a cohesive Master Blueprint containing 10 specific artifacts that prove our disruptive execution model.

## The 10-Artifact Stack

For each use case, execute the following 10 prompts/stages and synthesize the outputs:

1. **The Diagnostic:** Problem-Solution Fit Validation (identifying the manual "Human Middleware" friction).
2. **The 30-Day Scope:** Scope definition to hand to a builder, focusing on the Agentic Wedge.
3. **Tech Stack & Architecture:** Explicit, modern tech stack details (e.g., Python, LangChain, specific LLMs, Vercel) demonstrating how lightweight the agentic approach is vs. legacy.
4. **Build vs. Buy Matrix:** Justification for the custom agentic orchestration over bloated incumbent SaaS.
5. **ROI Business Case:** Cost-per-action/outcome vs. legacy per-seat licensing.
6. **Competitor Teardown:** Market mapping of the legacy incumbents and our disruptive strategy.
7. **Acceptance Criteria & Edge Cases:** Robust AC demonstrating engineering maturity.
8. **Data Architecture & Analytics:** How the agent accesses and processes native data securely.
9. **Deployment Sequencing:** Agile, fast-time-to-value deployment roadmap.
10. **Post-Launch Iteration Plan:** Day 31+ evolution and self-healing strategies.

## The Execution Loop

1. **Read the Target:** Pick the next use case from the dashboard.
2. **Execute Prompts 1-10:** Process the use case through the 10 stages outlined above. You can utilize `search_web` for real-world context if needed to ground the ROI or Tech Stack choices.
3. **Format & Output:** Compile the 10 artifacts into a single comprehensive Markdown document named `[UseCaseName]_Master_Blueprint.md`.
4. **Iterate:** Repeat until the requested use cases are fully generated.

## Output Structure
Each `[UseCaseName]_Master_Blueprint.md` should use clear headings (H2s for each of the 10 artifacts) and focus heavily on proving that we have the elite execution capability to replace legacy software with a fast, modern Agentic approach.
