# Forecasting / Predictive Ops Competitor Teardown

## The Target Use Case
**Agent Type:** Data
**SaaS Affected:** Predictive-analytics SaaS
**Verdict:** KEEP (The agent augments; the operational data wins)

## Competitor Discovery (Legacy Incumbents)
1. **SAS Analytics**
2. **Dataiku**
3. **Alteryx**
4. **RapidMiner**
5. **SPSS (IBM)**

## Product Teardown: The Legacy Model
### 1. Company Overview
* **SAS & SPSS:** The massive, entrenched legacy giants of statistical analysis and predictive modeling.
* **Dataiku & Alteryx:** Modern low-code/no-code data science platforms designed to democratize predictive analytics for business users.

### 2. Pricing & The "Seat" Trap
* **Alteryx:** A single Designer seat can cost $3k-$5k/year, but enterprise Server and automation add-ons push contracts deep into the 5- and 6-figure range.
* **SAS & Dataiku:** Highly opaque. SAS prices based on users, cores, and even revenue. Dataiku utilizes role-based pricing (Designers vs. Viewers) that easily scales into the hundreds of thousands of dollars for enterprise deployments.

### 3. Onboarding Friction & Community Complaints
* **The "Spaghetti Workflow" Issue:** Reddit users frequently complain that Alteryx and Dataiku visual workflows become unmanageable tangles of nodes and lines, making them harder to debug than raw Python code.
* **Cost vs. Value Barrier:** Many users struggle to justify the exorbitant licensing fees when open-source alternatives (Python, KNIME) or modern dbt workflows can achieve similar results.
* **Handoff Friction:** Passing a visual model to an unlicensed stakeholder or migrating it to a production engineering environment is a massive pain point.

### 4. Where They Are Strong (The Moat)
* **The Underlying Data:** The true value lies in the proprietary operational data (e.g., IoT sensors, telematics) feeding the forecasts.
* **Auditability:** Visual node-based interfaces provide a clear (if messy) lineage of data transformation for compliance teams.

### 5. Where They Are Weak (The Bloat)
* **Proprietary Interfaces:** Users are forced to learn a highly specific, proprietary UI abstraction layer just to execute standard data science tasks.
* **Seat-Gated Access:** The insights are locked behind expensive "Viewer" or "Designer" seats, preventing true operational scale.

## The Disruptive Strategy
**Which 2 competitors are the most direct threat?**
Alteryx and Dataiku.

**What are the Table Stakes?**
Robust data pipeline integration, explainability of the predictive model, and secure data handling.

**What must we deliberately NOT do?**
Do not attempt to replace the underlying operational systems (like Geotab for fleet tracking or Honeywell for industrial IoT). The data is their moat; we are the execution layer.

**The 3 Specific Gaps our Agentic Wedge Exploits:**
1. **Bypassing the Visual Canvas:** Instead of manually wiring 50 nodes together to run a predictive churn model, the agent translates the business intent into executable Python or SQL on the fly, eliminating the need for the low-code middleman.
2. **Democratizing the Output:** The agent delivers the forecast directly to the operator in natural language or a clean UI, killing the need to buy $100/mo "Viewer" seats for the whole operations team.
3. **Automated Maintenance:** Instead of a data scientist manually debugging a broken visual workflow, the agent can autonomously monitor data drift, rewrite its own queries, and update the predictive model in real-time.
