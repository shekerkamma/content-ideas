---
type: architecture
title: 'OPC-UA Integration'
description: 'OPC-UA is the standard protocol for reading sensor data from PLCs and industrial controllers.'
source_path: 'architecture/OPC-UA Integration.md'
tags:
- architecture
- integration
- iot
timestamp: '2026-07-04'
---

> Original source (local copy): [architecture/OPC-UA Integration.md](../source-vault/architecture/OPC-UA Integration.md)
> Original source (WSL): [architecture/OPC-UA Integration.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/architecture/OPC-UA%20Integration.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/architecture/OPC-UA%20Integration.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\architecture\OPC-UA Integration.md`
# OPC-UA Integration

OPC-UA is the standard protocol for reading sensor data from PLCs and industrial controllers.

## How It Works
opcua-asyncio provides an async Python OPC-UA client that subscribes to data change notifications from Siemens, Beckhoff, Rockwell, and other PLC vendors.

## Data Flow
```
PLC / Sensor → OPC-UA Server → opcua-asyncio client → Kafka / Feature Store → ML Model
```

## Key Patterns
- **Subscription mode** — async callbacks on data change (vs. polling)
- **Historian bridge** — write to AVEVA PI / Aspen IP21 for retention
- **Edge pre-processing** — filter, downsample, and feature-extract before cloud send
- **Security** — OPC-UA certificate-based auth, encrypted transport

## Use Cases
- [UC-05 Predictive Quality](../use-cases/uc-05-predictive-quality.md) — sensor data for defect prediction
- [UC-06 Predictive Maintenance](../use-cases/uc-06-predictive-maintenance.md) — vibration/acoustic/thermal monitoring

## Related
- opcua-asyncio · [MES Integration](../architecture/mes-integration.md)
