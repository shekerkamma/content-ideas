# Synthesis: Claude AI Workflow Use Cases in Healthcare

## Q1: Highest-value use cases by segment

**Providers:**
- **Clinical Documentation / Ambient Scribing** — saves 2–3 hrs/day per physician; post-processes ASR transcripts into SOAP notes, extracts ICD-10/CPT codes, flags discrepancies
- **Discharge Summaries & Care Transitions** — reduces preventable readmissions; generates both patient-readable and PCP-readable summaries, flags medication reconciliation gaps
- **Medical Report Structuring** — converts narrative radiology/pathology reports to structured HL7 FHIR DiagnosticReport; generates patient-readable summaries per CMS Information Blocking rule
- **Patient Communication & Care Navigation** — personalized post-visit instructions, portal message drafting, symptom triage, proactive care gap outreach — all under HIPAA BAA

**Payers:**
- **Prior Authorization Automation** — highest administrative burden in US healthcare (13 hrs/physician/week); Claude ingests clinical data, cross-references payer policy, drafts justification letters, flags gaps
- **Medical Coding & Revenue Cycle** — auto-suggests ICD-10/CPT codes; validates documentation to audit risk; identifies missed secondary diagnoses; drafts denial appeals
- **Denial Management & Appeals** — classifies denial reason, retrieves clinical evidence, drafts structured appeal letters citing CPT codes + clinical guidelines, generates peer-to-peer review scripts

**Life Sciences:**
- **Clinical Trial Eligibility Screening** — parses 30–100 inclusion/exclusion criteria; screens patient charts; drafts recruitment letters; summarizes protocol amendments
- **Pharmacovigilance / Drug Safety Reporting** — parses adverse event free text; extracts structured MedWatch fields; classifies severity per ICH E2A; drafts FDA MedWatch 3500A submissions
- **Regulatory Submission Authoring** — synthesizes clinical study reports (CTD format); drafts Module 2/5 content; cross-checks TLF consistency; generates FDA briefing packages

## Q2: ROI and compliance context for top use cases

**Prior Authorization:**
- ROI: Eliminates 13 hrs/physician/week of admin burden; at $300K avg physician salary → ~$37K/physician/year in recovered time; payers reduce manual review staffing by 30–40%
- Compliance: CMS-9115-F mandates electronic PA by January 2027; Claude's structured output enables direct API-to-payer-system integration

**Clinical Documentation:**
- ROI: 2–3 hrs/day saved per physician → $75K–$110K/year per clinician in recovered capacity; reduces physician burnout driving $500K+ replacement cost per departed physician
- Compliance: Operates under HIPAA BAA; Anthropic offers enterprise BAA coverage

## Q3: Revenue impact numbers

| Use Case | Industry Loss | Claude Impact |
|---|---|---|
| Medical coding errors | $262B/year in denied/underpaid claims (Change Healthcare) | Reduces coding errors; identifies missed diagnoses that increase reimbursement |
| Denial management | 3–5% of provider revenue lost to denials | Appeals succeed 40–60% when properly documented; Claude automates the documentation |
| Clinical trial delays | 30% average trial under-enrollment | LLM-based eligibility screening accelerates recruitment to 2–3x traditional manual screening |
| Regulatory submissions | $10–30M per NDA/BLA to write | Claude-assisted authoring compresses documentation timelines by 30–50% |
| Preventable readmissions | $26B/year nationally (15% 30-day rate) | Better discharge summaries and care gap outreach directly reduce readmission events |

## Q4: Compliance and regulatory frameworks

| Framework | Relevance to Claude Healthcare Workflows |
|---|---|
| **HIPAA BAA** | All PHI processing requires BAA; Anthropic offers enterprise BAA coverage |
| **CMS-9115-F** | Mandates electronic prior authorization by Jan 2027; accelerates PA automation adoption |
| **CMS Information Blocking Rule** | Requires patient-accessible report summaries; Claude generates them at appropriate reading levels |
| **FDA AI/ML Action Plan (2024)** | Supports AI-assisted pharmacovigilance with human oversight |
| **ONC Clinical Decision Support rules** | Requires explainability for AI-based clinical decision support; human-in-loop design required |
| **ICH E2A** | Governs adverse event severity classification in pharmacovigilance |

**Key constraint:** All Claude deployments in healthcare must include human-in-the-loop review for clinical decisions. Pure automation is feasible for administrative workflows (PA letters, denial appeals, patient communications); clinical decisions (treatment recommendations, diagnoses) require physician sign-off under current state medical practice laws.

## Q5: EHR vendors, health tech ecosystem, and market opportunity

**Vendors actively deploying LLM workflows:**
- PA Automation: Cohere Health, Abridge (multimodal AI scribe + PA)
- Ambient Scribing: Nuance DAX (Microsoft), Abridge, Suki, Ambience Healthcare
- Trial Screening: TriNetX, Mendel.ai; academic deployments at Mayo Clinic, Vanderbilt
- Most use proprietary or fine-tuned models; Claude evaluated as reasoning layer on top of base ASR/NLP

**EHR integration landscape:**
- Epic, Oracle Cerner, athenahealth — all building "AI marketplace" layers; native Claude integrations an open question for 2025–2026
- HL7 FHIR API standardization (R4/R5) enables Claude to read/write structured clinical data across systems

**Market opportunity framing:**
- Total US healthcare administrative spend: $950B+/year (JAMA, 2019) — most automatable with AI
- Claude's differentiation: 200K token context window handles full patient charts; low hallucination rate critical in clinical settings; Anthropic's Constitutional AI approach aligns with healthcare safety requirements
- First-mover advantage accrues to organizations that move from L2 (supervised) to L3 (delegated) automation in 2025–2026, ahead of CMS mandate deadlines
