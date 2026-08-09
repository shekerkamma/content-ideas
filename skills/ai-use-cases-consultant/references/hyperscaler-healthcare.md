# Hyperscaler Comparison — Healthcare AI (Payer Focus)

## Recommendation matrix

| Scenario | First choice | Why |
|---|---|---|
| New payer platform, cloud-agnostic | **AWS** | Broadest HIPAA BAA coverage, HealthLake FHIR R4 store, Comprehend Medical NLP |
| Existing GCP data estate / BigQuery | **GCP** | Knowledge Catalog MCP for data governance, MedLM for clinical NLP, SAIF automated controls |
| Microsoft/Teams/Office365 shop | **Azure** | Copilot Studio, Power Automate, M365 HIPAA data boundary |
| PHI detection and masking at scale | **AWS** | Macie + Comprehend Medical PHI detection is the most mature combination |
| Clinical AI + Google DeepMind models | **GCP** | MedLM integration, RadMD (radiology AI), partnership with hospital systems |
| FHIR-native interoperability (CMS Final Rule) | **AWS** | HealthLake FHIR R4 with CMS Final Rule 2024 compliance pre-built |

## AWS healthcare services with HIPAA BAA

All of the following sign HIPAA Business Associate Agreements:
- Amazon HealthLake (FHIR R4 store)
- Amazon Bedrock (Claude, Titan, Llama via Bedrock)
- Amazon Textract (document OCR)
- Amazon Comprehend Medical (PHI detection, ICD/RxNorm extraction)
- Amazon Macie (S3 PHI scanning)
- AWS KMS (encryption)
- Amazon DynamoDB, S3, Lambda, SageMaker

**Critical rule:** Never pass raw PHI to a model endpoint without a signed BAA. All services in the chain must sign.

## PHI tokenization pipeline (AWS)

```
Incoming document
  → Textract (OCR / text extraction)
  → Comprehend Medical (NER: PERSON, DIAGNOSIS, MEDICATION, DATE, PHONE)
  → Macie (PHI scan + alert on undetected entities)
  → Lambda tokenizer (replace PHI with UUID tokens)
  → Token map persisted to HealthLake / DynamoDB
  → Tokenized text passed to Bedrock (Claude) for clinical reasoning
  → Response de-tokenized before returning to clinician UI
```

## GCP healthcare architecture highlights

- **VPC Service Controls**: perimeter `payer-hipaa-ai` wraps aiplatform, healthcare, bigquery, storage, dataplex, cloudkms. Prevents data exfiltration even with compromised credentials.
- **BeyondCorp Enterprise**: zero-trust access for clinical reviewer workstations.
- **SAIF 6 elements**: Expand strong foundations, Extend detection and response, Automate AI security defenses, Harmonize platform-level controls, Adapt controls to AI, Contextualize AI risks for org.
- **GCP Recommended AI Controls Framework**: automated NIST AI RMF + CRI assessment via Security Command Center.
- **Knowledge Catalog MCP** (`https://dataplex.googleapis.com/mcp`): auto-harvests PHI data lineage — know exactly which datasets contain PHI at all times.

## CMS Final Rule 2024 requirements (Prior Authorization)

| Requirement | Deadline | AWS service | GCP equivalent |
|---|---|---|---|
| Prior auth decision: urgent = 72 hours | Active | Bedrock Agents orchestration | Vertex AI Agents |
| Prior auth decision: non-urgent = 7 calendar days | Active | Step Functions workflow | Cloud Workflows |
| Denial reason in machine-readable format | Active | HealthLake FHIR extension | Cloud Healthcare API FHIR R4 |
| FHIR API interoperability | Active | HealthLake FHIR R4 | Cloud Healthcare FHIR R4 |

## Cost guardrails (healthcare payer, production)

| Use case | Daily request ceiling | Monthly cost alert |
|---|---|---|
| Prior authorization automation | 5,000 req/day | $3,500/mo |
| Claims processing automation | 8,000 req/day | $2,000/mo |
| Member services chatbot | 15,000 req/day | $1,500/mo |

Set CloudWatch alarms (AWS) or Cloud Billing budget alerts (GCP) at these thresholds. Healthcare workloads have unpredictable spike patterns (open enrollment, benefit reset periods).
