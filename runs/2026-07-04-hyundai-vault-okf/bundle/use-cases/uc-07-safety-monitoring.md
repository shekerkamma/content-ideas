---
type: use_case
title: 'UC-07 Safety Monitoring'
description: 'Vision AI monitors PPE compliance, unsafe movements, restricted zone access, and forklift interactions.'
source_path: 'UC-07 Safety Monitoring.md'
tags:
- uc-07
- safety-monitoring
- ppe-detection
- zone-monitoring
timestamp: '2026-07-04'
---

> Original source (local copy): [UC-07 Safety Monitoring.md](../source-vault/UC-07 Safety Monitoring.md)
> Original source (WSL): [UC-07 Safety Monitoring.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/UC-07%20Safety%20Monitoring.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/UC-07%20Safety%20Monitoring.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\UC-07 Safety Monitoring.md`
# UC-07 Safety Monitoring

Vision AI monitors PPE compliance, unsafe movements, restricted zone access, and forklift interactions.

## Problem Statement
PPE non-compliance and restricted zone violations cause workplace injuries and EHS failures. Manual safety rounds are periodic and miss real-time violations.

## Solution
[YOLOv8](../technologies/ultralytics.md) custom-trained on PPE classes (helmet, vest, goggles). [supervision](../technologies/supervision.md) polygon zone detection for restricted area intrusion with dwell-time thresholds. [ByteTrack](../technologies/bytetrack.md) multi-object tracking for person-vehicle proximity monitoring. [Hailo/Jetson](../architecture/edge-deployment.md) edge inference with privacy anonymization.

## Solution Architecture
```
Wide-FOV safety cameras → Hailo-8 / Jetson Orin → YOLOv8 PPE detector → ByteTrack tracker → supervision zone-violation engine → EHS platform → Auto-incident report → Compliance scorecard
```

## Key Repos
- [ultralytics](../technologies/ultralytics.md)
- [supervision](../technologies/supervision.md)
- [ByteTrack](../technologies/bytetrack.md)
- hailo_model_zoo

## Business Metrics
−55% safety incidents · 98% PPE compliance · <500ms alert latency · Audit-ready EHS reports

## Recommended Pilot
High-traffic areas with forklift interaction

## Related
- [Edge Deployment](../architecture/edge-deployment.md)
- [ultralytics](../technologies/ultralytics.md)
- [ByteTrack](../technologies/bytetrack.md)
- [supervision](../technologies/supervision.md)
