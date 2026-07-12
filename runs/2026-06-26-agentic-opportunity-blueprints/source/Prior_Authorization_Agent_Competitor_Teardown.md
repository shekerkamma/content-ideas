# Prior_Authorization_Agent_Competitor_Teardown.md

## OSINT Source Map & Methodology
- **Sources:** Reddit (/r/HealthIT, /r/medicine), G2, TrustRadius, Healthcare IT pricing benchmarks.
- **Search Strategy:** Mapped "Prior Authorization" legacy platforms against real user complaints to identify friction points and "human middleware."
- **Rationale:** Proves the gap between bloated enterprise integrations (Epic, Waystar) and an agile, AI-native agent that operates directly on unstructured EMR data.

## Company Overview: Legacy Incumbents
1. **Epic (Native Module):** Enterprise dominant, deeply embedded but rigid.
2. **Oracle Health / Cerner:** Legacy EHR, similar limitations to Epic.
3. **Waystar:** Specialized RCM and authorization cloud platform.
4. **CoverMyMeds (McKesson):** Major third-party PA network, relies on pharmacy integration.
5. **Availity:** Clearinghouse with authorization portal capabilities.
6. **Myndshft:** Emerging player, but still acts as traditional SaaS.

## Product Teardown & Pricing
- **Pricing Models:** Waystar/CoverMyMeds use custom pricing often running $2,000–$5,000+/month for mid-market, or per-transaction ($5-$15). Epic/Cerner are bundled into enterprise licenses ($10M-$100M total cost of ownership), with implementation taking months.
- **Feature Bloat:** They require expensive API bridges, specific EHR builds, and standardized data.
- **Onboarding Friction:** Reddit users note that implementing these systems requires massive IT department resources and custom configurations that break easily.

## Where They Are Strong
- Deep integration as the System of Record.
- Established clearinghouse connections and real-time benefit checks (when perfectly configured).

## Where They Are Weak (The "Human Middleware" Gap)
- **Reddit Consensus:** Despite having the software, PAs remain heavily manual. Clinicians complain of "double entry," faxes, and "broken" workflows.
- Users report that if external entities don't use updated standards, the system fails, forcing staff to use spreadsheets and make phone calls.
- Inability to read unstructured chart notes dynamically; they rely on structured data fields.

## Disruptive Strategy (Agentic Wedge)
- **Direct Threats:** CoverMyMeds, Waystar.
- **Table Stakes:** HIPAA compliance, secure credential management, basic payer portal access.
- **Deliberate Anti-Features:** Do NOT build a new clearinghouse or EHR integration engine.
- **Top 3 Gaps We Exploit:**
  1. **Zero-Integration Setup:** Instead of a $100K/9-month API integration, our Agent operates via RPA/headless browser directly on the payer portal, mimicking a human.
  2. **Unstructured Data Mastery:** The Agent reads the raw unstructured EMR chart to extract medical necessity codes, bypassing the need for doctors to fill out specific structured PA forms.
  3. **Eliminating Double Entry:** Replaces the human clerk entirely rather than just giving the clerk a "better dashboard."
