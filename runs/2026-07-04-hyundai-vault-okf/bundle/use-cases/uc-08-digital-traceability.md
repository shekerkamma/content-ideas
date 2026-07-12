---
type: use_case
title: 'UC-08 Digital Traceability'
description: 'End-to-end component and assembly traceability across production stages using RFID, barcode, IoT, and vision.'
source_path: 'UC-08 Digital Traceability.md'
tags:
- uc-08
- traceability
- graph-database
- rfid
timestamp: '2026-07-04'
---

> Original source (local copy): [UC-08 Digital Traceability.md](../source-vault/UC-08 Digital Traceability.md)
> Original source (WSL): [UC-08 Digital Traceability.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/UC-08%20Digital%20Traceability.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/UC-08%20Digital%20Traceability.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\UC-08 Digital Traceability.md`
# UC-08 Digital Traceability

End-to-end component and assembly traceability across production stages using RFID, barcode, IoT, and vision.

## Problem Statement
Fragmented component genealogy makes recall investigations take 4–6 weeks. No unified view across regional systems for defect root-cause analysis.

## Solution
[Neo4j](../technologies/neo4j.md) graph database models component-to-vehicle genealogy. RFID (UHF via sllurp) and barcode scanning track parts at every station. SAP integration (PyRFC) enables bidirectional data flow. Apache Flink handles high-throughput event ingestion.

## Solution Architecture
```
UHF RFID readers → Barcode / DataMatrix scanners → Apache Flink stream processing → Neo4j genealogy graph → SAP MES/ERP (PyRFC) → Vehicle genealogy viewer → Recall scope calculator → Auditor export
```

## Key Repos
- [Neo4j](../technologies/neo4j.md)
- sllurp
- PyRFC
- Flink

## Business Metrics
100% part traceability · −70% recall investigation time · Full audit trail · Real-time genealogy

## Recommended Pilot
Single assembly line for end-to-end pilot

## Deck Assets
- uc-08-digital-traceability-use-case-realization
- uc-08-digital-traceability-solution-on-page

## Related
- [MES Integration](../architecture/mes-integration.md)
- [Neo4j](../technologies/neo4j.md)
