# Document AI / Extraction Competitor Teardown

## The Target Use Case
**Agent Type:** Data
**SaaS Affected:** IDP / OCR SaaS (Intelligent Document Processing)
**Verdict:** REPLACE

## Competitor Discovery (Legacy Incumbents)
1. **ABBYY (FlexiCapture / Vantage)**
2. **Kofax (TotalAgility / Capture)**
3. **Ephesoft**
4. **IBM Datacap**
5. **Automation Anywhere (Document Automation)**

## Product Teardown: The Legacy Model
### 1. Company Overview
* **ABBYY & Kofax:** The traditional titans of OCR (Optical Character Recognition) and enterprise data capture. Built on decades-old positional scanning technology that evolved into "intelligent" capture.

### 2. Pricing & The "Seat" Trap
* **ABBYY:** Page-based and capacity-based licensing. Entry-level starts around $4,000 for low volume (50k pages), but mid-sized deployments (250k-1M pages) cost $15,000 to $40,000 annually ($0.06 - $0.10 per page).
* **Kofax:** Custom enterprise pricing mixing concurrent user licenses and document volume. 
* **The Hidden Tax:** Both platforms demand massive professional services fees ($10k-$30k+ in year one) just to set up templates and rules. Language packs are often sold as expensive add-ons (30% markup).

### 3. Onboarding Friction & Community Complaints
* **Template Hell:** The biggest complaint is the reliance on rigid zoning templates. If an invoice or form shifts by a few pixels, the extraction fails.
* **Setup Complexity:** Implementing new document types requires highly trained specialists to build complex regex rules, creating a massive bottleneck.
* **Maintenance Burden:** IT teams complain about the constant need to retrain and babysit the models as vendor layouts change.

### 4. Where They Are Strong (The Moat)
* **High-Speed Batch Processing:** Excellent at ingesting thousands of perfectly standardized, high-dpi scanned pages per minute.
* **Deep Legacy Integration:** Tightly coupled with legacy ERPs, SAP, and legacy ECM (Enterprise Content Management) systems.

### 5. Where They Are Weak (The Bloat)
* **Unstructured Data:** Terrible at handling free-form text, diverse layouts, or documents that don't fit a pre-defined mold.
* **Time-to-Value:** A 9-month implementation cycle just to accurately extract data from 10 different vendor invoice formats.

## The Disruptive Strategy
**Which 2 competitors are the most direct threat?**
ABBYY and Kofax.

**What are the Table Stakes?**
Deterministic, structured output (perfect JSON), high accuracy/confidence scores, and secure handling of PII/financial data.

**What must we deliberately NOT do?**
Do not attempt to become the ERP or the downstream system of record. Be the intelligent, frictionless middleman.

**The 3 Specific Gaps our Agentic Wedge Exploits:**
1. **Zero-Template Extraction:** Using LLM vision and semantic understanding, the agent extracts data based on meaning, not pixel position. This destroys the $30k professional services implementation cost.
2. **Instant Onboarding:** A new document type can be added by simply prompting the agent with a natural language schema, collapsing a 3-week IT project into a 3-minute task.
3. **Handling Unstructured Chaos:** The agent can ingest messy, unstructured emails containing PDF attachments, read the context, extract the data, and route it—something legacy OCR literally cannot do without human pre-processing.
