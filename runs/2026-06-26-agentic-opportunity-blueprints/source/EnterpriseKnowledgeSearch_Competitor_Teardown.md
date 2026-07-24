# Enterprise Knowledge Search: Competitor Teardown

## Target SaaS: Enterprise Search & Knowledge Management

### Overview of Incumbents
1. **Coveo**: Premium enterprise AI search. Massive scale, heavy implementation.
2. **Sinequa**: High-end platform for complex, multi-system environments requiring deep governance.
3. **Guru**: Knowledge management wiki with AI overlays. Positioned for mid-market to enterprise.
4. **Glean**: Modern workplace search, deeply integrated with Google Workspace and Slack.
5. **Elastic Enterprise Search**: Developer-focused, highly customizable but requires engineering resources.

### Product Teardown (The Legacy Model)
*   **Top 3 Features**: Unified federated search, permissions-based access trimming, and manual knowledge curation.
*   **Pricing Tiers**: Custom-quoted and highly opaque. Glean often starts at $50–$75+ per user/month with $200k+ annual contracts. Coveo can reach $50k+ annually. Most require massive upfront commitments (100+ seats).
*   **Onboarding Friction**: Users on Reddit and G2 highlight intense integration complexity. Connecting heterogeneous data sources requires specialized engineering. Guru users complain about "content rot" and the heavy administrative burden to maintain knowledge accuracy.

### Where They Are Strong (The Moat)
*   **Integrations & Security**: They have built robust connectors to hundreds of silos (Jira, Salesforce, Slack) while respecting document-level permissions.
*   **System of Record**: For wiki-style tools like Guru, they become the de facto system of record for company policies.

### Where They Are Weak (The Vulnerability)
*   **Administrative Overhead**: Maintaining the system requires constant human curation. "Out-of-the-box" relevance is often poor without manual tuning.
*   **Prohibitive Cost**: Widespread per-seat pricing means companies restrict access to save money, defeating the purpose of enterprise-wide search.

## Disruptive Strategy (Our Agentic Wedge)

### 1. Direct Threats
*   **Glean** (Closest modern equivalent).
*   **Coveo** (Incumbent enterprise heavyweight).

### 2. Table Stakes Features
*   **RBAC & Security Trimming**: If the agent surfaces a confidential HR document to an engineer, it's dead on arrival.
*   **Native Connectors**: Must seamlessly index Drive, Slack, and Jira out-of-the-box.

### 3. What We Deliberately MUST NOT Do
*   **Do not build another Wiki/Database**: We will not ask users to migrate or manually input data. The agent must sit on top of their existing messy silos and synthesize on the fly. 

### 4. The 3 Gaps Our Agentic Wedge Exploits
1.  **Kill the Per-Seat Tax**: Shift from a $75/user/month license to a consumption-based token model, allowing the entire company to access knowledge without license gating.
2.  **Eliminate "Content Rot"**: Instead of relying on humans to update wiki cards, the agent dynamically synthesizes answers from the live data layer, ensuring answers are never stale.
3.  **Zero-Setup Deployment**: Replace the 6-month consulting integration with a 1-click OAuth integration pipeline that builds a semantic graph autonomously.
