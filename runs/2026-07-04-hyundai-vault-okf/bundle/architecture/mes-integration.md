---
type: architecture
title: 'MES Integration'
description: 'Integration patterns for connecting AI systems with Manufacturing Execution Systems.'
source_path: 'architecture/MES Integration.md'
tags:
- architecture
- integration
- mes
- sap
timestamp: '2026-07-04'
---

> Original source (local copy): [architecture/MES Integration.md](../source-vault/architecture/MES Integration.md)
> Original source (WSL): [architecture/MES Integration.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/architecture/MES%20Integration.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/architecture/MES%20Integration.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\architecture\MES Integration.md`
# MES Integration

Integration patterns for connecting AI systems with Manufacturing Execution Systems.

## SAP MES/ERP Integration
- **PyRFC** — Python connector for SAP RFC function calls
- **SAP MES API** — REST API for work order, BOM, and quality events
- **SAP PM** — Predictive maintenance work order auto-generation

## Integration Patterns
| Pattern | Use Case | Mechanism |
|---------|----------|-----------|
| Line Hold | [UC-01 Visual Inspection](../use-cases/uc-01-visual-inspection.md), [UC-02 Variant Confirmation](../use-cases/uc-02-variant-confirmation.md) | PLC signal via OPC-UA |
| Work Order | [UC-06 Predictive Maintenance](../use-cases/uc-06-predictive-maintenance.md) | SAP PM API |
| BOM Match | [UC-02 Variant Confirmation](../use-cases/uc-02-variant-confirmation.md) | SAP MES BOM query |
| Quality Event | [UC-05 Predictive Quality](../use-cases/uc-05-predictive-quality.md) | Kafka → Quality DB |
| Traceability | [UC-08 Digital Traceability](../use-cases/uc-08-digital-traceability.md) | PyRFC bidirectional |

## Other MES Vendors
- AVEVA MES · Siemens Opcenter · Rockwell Plex · MPDV

## Related
- [OPC-UA Integration](../architecture/opc-ua-integration.md) · [Neo4j](../technologies/neo4j.md)
