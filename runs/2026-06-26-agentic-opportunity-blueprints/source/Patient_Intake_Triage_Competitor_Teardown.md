# Patient_Intake_Triage_Competitor_Teardown.md

## OSINT Source Map & Methodology
- **Sources:** Reddit (/r/medicine, /r/HealthIT), KLAS Research, G2.
- **Search Strategy:** Searched for patient, doctor, and IT complaints regarding Phreesia and MyChart implementations.
- **Rationale:** Exposes the friction of forcing patients into proprietary apps and the resulting administrative burden on clinicians.

## Company Overview: Legacy Incumbents
1. **Phreesia:** The dominant standalone patient intake/check-in pad software.
2. **Epic (MyChart):** Enterprise patient portal.
3. **Cerner (HealtheLife):** Enterprise patient portal.
4. **Weave:** SMB communication and intake.
5. **SimplePractice:** Solo/SMB behavioral health and wellness intake.
6. **athenaCommunicator:** Athenahealth's patient engagement module.

## Product Teardown & Pricing
- **Pricing Models:** Phreesia uses quote-based subscriptions (thousands of dollars per month + implementation fees based on volume/providers). Epic MyChart is tied to $10M+ enterprise EHR deployments.
- **Feature Set:** Digital check-in pads, insurance capture, pre-visit questionnaires, copay collection.

## Where They Are Strong
- Payment processing, demographic data collection, and integration with native scheduling.

## Where They Are Weak (The "Human Middleware" Gap)
- **Reddit Consensus:** Providers complain about Phreesia’s forced "check-in rates" and clunky "bolt-on" nature. 
- **The "In-Basket" Nightmare:** MyChart generates massive administrative burden for doctors who have to manually read unstructured patient messages and triage them.
- Patients complain about slow portal performance, too many pop-ups, and app-fatigue.

## Disruptive Strategy (Agentic Wedge)
- **Direct Threats:** Phreesia, Epic MyChart.
- **Table Stakes:** Secure SMS capability, demographic capture.
- **Deliberate Anti-Features:** Do NOT build a new patient portal app or proprietary tablet hardware.
- **Top 3 Gaps We Exploit:**
  1. **Conversational Intake:** Bypasses clunky apps by using natural conversational AI (SMS/WhatsApp) to ingest raw symptoms dynamically, adjusting questions based on answers.
  2. **Diagnostic Pre-population:** Rather than just sending a PDF questionnaire to the EHR, the Agent synthesizes the symptoms and pre-populates the physician's diagnostic workflow/SOAP note.
  3. **Triage Automation:** Automatically routes the patient to the right acuity level without requiring a triage nurse to read a MyChart message.
