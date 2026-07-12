# Disruptive Competitor Teardown: Audit & Tax Document Synthesis (Use Case 41)

## 1. Company Overview & Legacy Competitors
**Target Incumbents:** Thomson Reuters (SurePrep / 1040SCAN), CCH (ProSystem fx Scan), Intuit (Lacerte), Drake Tax, GruntWorx.
These legacy players built early OCR (Optical Character Recognition) tech to scan tax documents, but they remain rigid and still require heavy human intervention.

## 2. Product Teardown (SurePrep & CCH ProSystem fx Scan)
*   **Top 3 Features:** OCR data extraction, digital binder organization (SPbinder), automated entry for standard forms (W-2s, 1099s).
*   **Pricing:** Convoluted "pay-per-return" models with use-it-or-lose-it credits. Substantial price hikes after year 1. 
*   **Onboarding Friction:** Rigid OCR breaks easily on complex forms (e.g., K-1s, corrected 1099s, trust returns). Reddit CPA communities complain that server failures during peak tax season are common.

## 3. Where They Are Strong
*   **Stickiness:** Excellent digital binder organization. They do save time on highly standard, low-complexity 1040 returns.

## 4. Where They Are Weak
*   **Manual Workflows:** The software relies on "dumb" OCR. Verification of the extracted data takes almost as much time as manual entry. The "human middleware" is still required for anything that doesn't fit a perfect template.

## 5. The Disruptive Strategy
*   **Direct Threats:** Thomson Reuters SurePrep, CCH ProSystem fx Scan.
*   **Table Stakes:** Secure document upload, export capability to major tax prep software (Lacerte, CCH Axcess).
*   **What We Deliberately NOT Do:** Do NOT build a new tax calculation engine. We prepare the schedules, they handle the final filing.
*   **The Agentic Wedge (3 Gaps to Exploit):**
    1.  **LLM Understanding > Rigid OCR:** Replace template-based OCR with an agentic LLM that can actually read and categorize messy "shoebox" receipts, complex K-1s, and handwritten notes.
    2.  **Eliminate Verification Fatigue:** Provide contextual confidence scores linked directly to source text, drastically reducing the time CPAs spend verifying data.
    3.  **Kill the Pay-Per-Return Model:** Offer a flexible, consumption-based pricing model that destroys their convoluted, locked-in credit bundles.
