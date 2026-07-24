---
title: "MES Integration"
tags: [architecture, integration, mes, sap]
type: architecture
---

# MES Integration

Integration patterns for connecting AI systems with Manufacturing Execution Systems.

## SAP MES/ERP Integration
- **PyRFC** — Python connector for SAP RFC function calls
- **SAP MES API** — REST API for work order, BOM, and quality events
- **SAP PM** — Predictive maintenance work order auto-generation

## Integration Patterns
| Pattern | Use Case | Mechanism |
|---------|----------|-----------|
| Line Hold | [[UC-01 Visual Inspection]], [[UC-02 Variant Confirmation]] | PLC signal via OPC-UA |
| Work Order | [[UC-06 Predictive Maintenance]] | SAP PM API |
| BOM Match | [[UC-02 Variant Confirmation]] | SAP MES BOM query |
| Quality Event | [[UC-05 Predictive Quality]] | Kafka → Quality DB |
| Traceability | [[UC-08 Digital Traceability]] | PyRFC bidirectional |

## Other MES Vendors
- AVEVA MES · Siemens Opcenter · Rockwell Plex · MPDV

## Related
- [[OPC-UA Integration]] · [[Neo4j]]
