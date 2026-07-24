# Research & Insight Agent Competitor Teardown

## The Target Use Case
**Agent Type:** Data
**SaaS Affected:** Market-research tooling
**Verdict:** RENEGOTIATE (Fewer research-tool seats)

## Competitor Discovery (Legacy Incumbents)
1. **Qualtrics**
2. **AlphaSense**
3. **Forrester / Gartner (per-seat portal access)**
4. **SurveyMonkey Enterprise**
5. **Medallia**

## Product Teardown: The Legacy Model
### 1. Company Overview
* **Qualtrics / Medallia:** The heavyweights of Experience Management (XM), turning surveys and feedback into massive research datasets.
* **AlphaSense:** The premium search engine for financial and market intelligence, built for analysts.

### 2. Pricing & The "Seat" Trap
* **Qualtrics:** Opaque and module-based. While basic plans exist, Enterprise XM suites easily scale from $20k to $100k+ annually based on interaction volume and AI add-ons.
* **AlphaSense:** Extremely expensive. Financial subreddits report per-seat costs ranging from $15,000 to $60,000 per year, making it a highly guarded resource.

### 3. Onboarding Friction & Community Complaints
* **The "Rip-off" Sentiment:** Reddit users frequently question the ROI of AlphaSense, arguing that the interface is overwhelming and the cost-to-value ratio is poor given the rise of cheap AI summarization tools.
* **Admin Burden:** Qualtrics administrators complain that managing the platform (fixing logic, maintaining HRIS integrations) turns into a full-time job. 
* **Opaque Pricing Hikes:** Users express frustration over constant, non-transparent price increases and paywalled features in legacy survey tools.

### 4. Where They Are Strong (The Moat)
* **Proprietary Data Corpora:** AlphaSense holds massive value in its aggregated, licensed broker research. Qualtrics holds the company's historical VoC (Voice of Customer) data.
* **Brand Authority:** Gartner/Forrester sell trust and CYA ("Cover Your Ass") insurance for executives.

### 5. Where They Are Weak (The Bloat)
* **The Synthesis Bottleneck:** Even with premium access, a human analyst must still manually read, synthesize, and format the insights into a briefing document.
* **License Scarcity:** Because seats are so expensive, insights are bottlenecked through a few licensed analysts rather than democratized to the whole team.

## The Disruptive Strategy
**Which 2 competitors are the most direct threat?**
AlphaSense and Qualtrics.

**What are the Table Stakes?**
Zero hallucination (perfect RAG), exact citation mapping back to original sources, and deep contextual synthesis.

**What must we deliberately NOT do?**
Do not try to become a proprietary data vendor or a survey collection engine. Sit on top of the data sources.

**The 3 Specific Gaps our Agentic Wedge Exploits:**
1. **Automated Synthesis:** The agent doesn't just return search results (like AlphaSense); it reads the 50 relevant SEC filings and outputs a fully formatted, ready-to-present executive briefing in minutes.
2. **Democratizing the Seat:** By separating the research corpus from the synthesis engine, the agent allows the entire company to ask insight questions without needing a $20k/year proprietary portal license.
3. **Cross-Silo Context:** Instead of siloing research in Qualtrics (customer data) and AlphaSense (market data), the agent can ingest both simultaneously, providing holistic insights that no single legacy tool can offer.
