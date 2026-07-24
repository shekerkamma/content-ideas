# NL Analytics (Text-to-SQL) Competitor Teardown

## The Target Use Case
**Agent Type:** Data
**SaaS Affected:** BI Dashboards (Looker-class, Tableau, Sisense, Domo)
**Verdict:** RENEGOTIATE (Trim BI seats, keep the warehouse)

## Competitor Discovery (Legacy Incumbents)
1. **Tableau (Salesforce)**
2. **Sisense**
3. **Domo**
4. **Power BI (Microsoft)**
5. **Alteryx**

## Product Teardown: The Legacy Model
### 1. Company Overview
* **Tableau:** The long-standing leader in visual analytics, heavily focused on dashboard creation and complex data visualization.
* **Sisense / Domo:** Enterprise-grade embedded analytics and dashboarding platforms focused on business users.

### 2. Pricing & The "Seat" Trap
* **Tableau:** Heavily role-based. "Creators" cost $75/mo ($900/year), while non-technical "Viewers" still cost $15-$35/mo. Real TCO includes massive training costs ($1k-$3k per Creator).
* **Sisense & Domo:** Custom enterprise pricing. Sisense often ranges from $30k to $100k+ annually based on capacity. Domo uses a "credit-based" consumption model that effectively penalizes heavy data querying and dashboard refreshes, bringing effective per-user costs to $100-$600+/month.

### 3. Onboarding Friction & Community Complaints
* **The "Spaghetti" Problem:** Reddit users consistently complain about inheriting "nightmare" Tableau workbooks with complex, undocumented calculated fields. 
* **ETL vs. BI Confusion:** The tools demand perfectly clean, structured data. When non-technical business users attempt to use them, they hit a brick wall of data engineering requirements.
* **Learning Curve:** Despite "drag and drop" promises, the 80/20 rule applies: the last 20% of a dashboard requires deep SQL/data structuring knowledge, frustrating business users and burdening analysts.

### 4. Where They Are Strong (The Moat)
* **System of Record Integration:** They sit deeply on top of the corporate data warehouse.
* **Trust & Governance:** Established mechanisms for data access control and semantic definitions.

### 5. Where They Are Weak (The Bloat)
* **Human Middleware:** They require an analyst to sit between the business stakeholder's question and the data warehouse's answer.
* **Visual Rigidity:** Users are forced to consume data exactly how the analyst built the dashboard, rather than asking dynamic, ad-hoc questions.

## The Disruptive Strategy
**Which 2 competitors are the most direct threat?**
Tableau and Looker.

**What are the Table Stakes?**
Data governance, robust access controls, and absolutely zero hallucinations in SQL generation (accuracy).

**What must we deliberately NOT do?**
Do not build a new data warehouse or storage engine. Sit on top of existing infrastructure (Snowflake, BigQuery) and ride their compute.

**The 3 Specific Gaps our Agentic Wedge Exploits:**
1. **Collapsing the Interface:** Instead of spending hours building rigid visual dashboards, the agent translates natural language directly into validated SQL, providing immediate answers to stakeholders.
2. **Destroying Per-Seat Licensing:** We kill the $15-$35/month "Viewer" seat and the $75/month "Creator" seat by moving the query generation to the agent, reducing BI spend to just the core infrastructure.
3. **Eliminating the "Spaghetti" Logic:** By defining semantic rules natively for the LLM, we eliminate the fragile, undocumented calculated fields that make legacy BI tools unmaintainable.
