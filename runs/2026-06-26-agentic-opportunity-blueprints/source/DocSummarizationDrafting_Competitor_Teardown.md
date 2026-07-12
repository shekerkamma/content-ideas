# Document Summarization & Drafting: Competitor Teardown

## Target SaaS: Proposal & Document Management

### Overview of Incumbents
1. **Qvidian**: Legacy enterprise RFP and proposal management.
2. **Seismic**: Premium sales enablement and content management platform.
3. **Highspot**: Sales enablement and document tracking platform.
4. **Conga**: Document generation, CLM, and CPQ integrated heavily with Salesforce.
5. **PandaDoc**: Mid-market document automation and e-signature.

### Product Teardown (The Legacy Model)
*   **Top 3 Features**: Centralized content library, template-based document generation, and engagement tracking analytics.
*   **Pricing Tiers**: Enterprise contracts are notoriously expensive and modular. Highspot averages ~$91k/year ($45-$65/user/month). Conga charges per-module with five-figure price tags per feature. Qvidian relies entirely on opaque sales-led quotes.
*   **Onboarding Friction**: G2/TrustRadius reviews cite significant setup challenges. Conga users complain about setup complexity and data dependency (requires perfectly clean Salesforce data). Qvidian has a steep learning curve requiring dedicated administrators.

### Where They Are Strong (The Moat)
*   **Workflow Integration**: Deep hooks into Salesforce and existing CRM workflows.
*   **Compliance & Standardization**: They strictly enforce brand and legal compliance through locked templates.

### Where They Are Weak (The Vulnerability)
*   **Manual "Lego Building"**: Users still have to manually drag-and-drop content blocks. It accelerates drafting but doesn't automate it.
*   **Nickel-and-Dime Pricing**: Users on Reddit complain about massive price hikes, module gating, and the transition to rigid licensing models that triple annual costs.

## Disruptive Strategy (Our Agentic Wedge)

### 1. Direct Threats
*   **Conga** (For Salesforce-native document generation).
*   **Qvidian** (For complex, long-form RFPs).

### 2. Table Stakes Features
*   **CRM Data Ingestion**: Must pull variables directly from Salesforce/HubSpot accurately.
*   **Export to Native Formats**: Must generate clean .docx or .pdf files that look identical to the company's brand templates.

### 3. What We Deliberately MUST NOT Do
*   **Do not build a new CRM or Content Library**: We leave the source of truth in Salesforce or SharePoint. The agent is strictly the execution layer that drafts the document.

### 4. The 3 Gaps Our Agentic Wedge Exploits
1.  **From Templates to Synthesis**: Instead of a user filling out a template, the agent reads the client email, CRM history, and past RFPs to generate a highly personalized first draft instantly.
2.  **Collapse the Module Tax**: Offer end-to-end generation, review, and summarization without charging separate $10k fees for "Composer" vs. "CLM" modules.
3.  **No Dedicated Admin Required**: Bypass the steep learning curve by allowing users to prompt the agent in natural language, eliminating the need for complex merge-field coding.
