# Clinical_Trial_Matching_Competitor_Teardown.md

## OSINT Source Map & Methodology
- **Sources:** eClinical industry reports, G2, TrustRadius.
- **Search Strategy:** Analyzed legacy CTMS (Clinical Trial Management Systems) and specialized matching software.
- **Rationale:** Highlights the manual bottleneck of matching unstructured medical records to complex inclusion/exclusion criteria.

## Company Overview: Legacy Incumbents
1. **IQVIA (CTM):** Massive CRO and legacy software provider.
2. **Medidata (Dassault Systèmes):** Dominant clinical cloud platform.
3. **Veeva Vault:** Enterprise clinical data suite.
4. **Tempus AI:** Modern, data-driven matching (EHR-focused).
5. **Antidote:** Specialized patient matching platform.
6. **OpenClinica:** Modern EDC/CTMS.

## Product Teardown & Pricing
- **Pricing Models:** Enterprise custom quotes. Customization fees range from £10,000–£100,000+. Total platform costs reach hundreds of thousands annually.
- **Feature Set:** Protocol design, site management, EDC (Electronic Data Capture), basic query-based matching.

## Where They Are Strong
- Regulatory compliance (21 CFR Part 11), massive scale, global site management.

## Where They Are Weak (The "Human Middleware" Gap)
- Matching relies heavily on structured data. If a patient's history is buried in unstructured PDFs, faxes, or clinical notes, human study coordinators must manually read the charts to verify complex inclusion/exclusion criteria.
- Outdated UIs and massive deployment times (6-12 months).

## Disruptive Strategy (Agentic Wedge)
- **Direct Threats:** IQVIA, Tempus AI.
- **Table Stakes:** HIPAA compliance, secure data handling.
- **Deliberate Anti-Features:** Do NOT build a full-blown CTMS or EDC system.
- **Top 3 Gaps We Exploit:**
  1. **Unstructured Criterion Matching:** The Agent ingests massive unstructured patient histories and natively understands semantic inclusion/exclusion criteria, eliminating manual chart reviews by coordinators.
  2. **Micro-Deployments:** Instead of a £100,000 enterprise rollout, the Agent operates as a lightweight tool that sites can use on day one.
  3. **Instant ROI:** Replaces the expensive human hours spent screening patients who ultimately fail out of trials, vastly lowering Customer Acquisition Cost (CAC) for pharmaceutical sponsors.
