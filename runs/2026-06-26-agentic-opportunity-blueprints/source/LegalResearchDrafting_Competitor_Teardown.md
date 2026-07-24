# Legal Research & Drafting: Competitor Teardown

## Target SaaS: Legal Research & CLM

### Overview of Incumbents
1. **Westlaw (Thomson Reuters)**: The gold standard for legal research and case law.
2. **LexisNexis**: Direct competitor to Westlaw, dominating legal research.
3. **Icertis**: High-end, enterprise-grade Contract Lifecycle Management (CLM).
4. **Agiloft**: Highly configurable enterprise CLM.
5. **Relativity**: Dominant e-discovery platform.

### Product Teardown (The Legacy Model)
*   **Top 3 Features**: Proprietary case law databases, Boolean search logic, and contract lifecycle workflow routing.
*   **Pricing Tiers**: Westlaw/LexisNexis use timekeeper headcount pricing ($400-$850+/month per attorney), penalizing firms for non-active users. Icertis and Agiloft are massive enterprise investments with high licensing and implementation costs.
*   **Onboarding Friction**: Westlaw contracts are notoriously aggressive (auto-renewals, difficult to cancel). Icertis takes 4-6 months to implement. Users complain about steep learning curves, clunky UI/UX, and friction in integrating with legacy firm management systems.

### Where They Are Strong (The Moat)
*   **Proprietary Data**: Westlaw and LexisNexis own the annotated case law databases. This is an incredibly deep moat.
*   **Auditability & Security**: Enterprise CLMs provide rigorous, auditable workflows necessary for compliance.

### Where They Are Weak (The Vulnerability)
*   **Lookup vs. Synthesis**: Traditional tools require attorneys to execute complex Boolean searches, read dozens of cases, and manually synthesize the arguments into a brief.
*   **Predatory Pricing Models**: The headcount-based licensing model is deeply resented by law firms, driving a desire for alternatives.

## Disruptive Strategy (Our Agentic Wedge)

### 1. Direct Threats
*   **Westlaw / LexisNexis AI add-ons** (They are bolting AI onto their databases).
*   **Harvey** (The modern AI-native legal assistant).

### 2. Table Stakes Features
*   **Absolute Accuracy (Zero Hallucination)**: Legal agents must cite real case law. A single hallucinated case destroys trust permanently.
*   **Strict Data Privacy**: Zero data retention policies. Client data cannot be used to train base models.

### 3. What We Deliberately MUST NOT Do
*   **Do not build a proprietary case law database**: We cannot beat Westlaw's 100-year head start on data. We must act as the intelligence layer that interacts with existing public databases or sits on top of the firm's internal DMS (iManage, NetDocuments).

### 4. The 3 Gaps Our Agentic Wedge Exploits
1.  **Drafting, Not Just Searching**: Shift the paradigm from "finding a case" to "drafting the memo." The agent executes the lookup, synthesizes the precedent, and outputs a formatted first draft of the brief.
2.  **Exploit the Headcount Tax**: Offer a usage-based or flat-platform fee that undercuts the $800/attorney/month model, allowing firms to deploy the agent to paralegals and junior associates without exponential cost scaling.
3.  **DMS Intelligence**: Turn the firm's own historical contract repository (in iManage) into an active intelligence layer, allowing the agent to redline new contracts against the firm's historical standards instantly, bypassing 6-month CLM implementations.
