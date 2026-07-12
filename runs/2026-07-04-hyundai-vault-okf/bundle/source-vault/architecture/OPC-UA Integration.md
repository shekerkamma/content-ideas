---
title: "OPC-UA Integration"
tags: [architecture, integration, iot]
type: architecture
---

# OPC-UA Integration

OPC-UA is the standard protocol for reading sensor data from PLCs and industrial controllers.

## How It Works
[[opcua-asyncio]] provides an async Python OPC-UA client that subscribes to data change notifications from Siemens, Beckhoff, Rockwell, and other PLC vendors.

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
- [[UC-05 Predictive Quality]] — sensor data for defect prediction
- [[UC-06 Predictive Maintenance]] — vibration/acoustic/thermal monitoring

## Related
- [[opcua-asyncio]] · [[MES Integration]]
