---
type: use_case
title: 'UC-01 Visual Inspection'
description: 'AI-enabled cameras detect paint defects, scratches, dents, welding inconsistencies, and panel gaps in real time.'
source_path: 'UC-01 Visual Inspection.md'
tags:
- uc-01
- visual-inspection
- computer-vision
- quality
timestamp: '2026-07-04'
---

> Original source (local copy): [UC-01 Visual Inspection.md](../source-vault/UC-01 Visual Inspection.md)
> Original source (WSL): [UC-01 Visual Inspection.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/UC-01%20Visual%20Inspection.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/UC-01%20Visual%20Inspection.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\UC-01 Visual Inspection.md`
# UC-01 Visual Inspection

AI-enabled cameras detect paint defects, scratches, dents, welding inconsistencies, and panel gaps in real time.

## Problem Statement
Manual inspection misses ~12% of surface defects. Inspector fatigue across shifts causes inconsistent quality. Defects that escape to downstream stages cost 10-100x more to fix.

## Solution
CNN-based anomaly detection trained on normal-only images (no labeled defect data needed). [anomalib](../technologies/anomalib.md) PatchCore scores surface anomalies, [YOLOv8](../technologies/ultralytics.md) localizes and classifies specific defect types. Edge inference via [TensorRT on Jetson Orin](../architecture/edge-deployment.md) meets <2s line-speed constraint.

## Solution Architecture
```
Cognex / Basler cameras (pypylon) → NVIDIA Jetson Orin (TensorRT) → anomalib PatchCore / YOLOv8 → OPC-UA → MES line-hold → Quality DB → Dashboard
```

## Key Repos
- [anomalib](../technologies/anomalib.md)
- [ultralytics](../technologies/ultralytics.md)
- [jetson-inference](../technologies/jetson-inference.md)
- [pypylon](../technologies/pypylon.md)
- [mmdetection](../technologies/mmdetection.md)
- [mmpretrain](../technologies/mmpretrain.md)

## Business Metrics
−45% rework costs · −60% escape defects · <2s detection latency · +35% line throughput

## Recommended Pilot
IONIQ 5 / IONIQ 9 paint line at Metaplant America (HMGMA)

## Deck Assets
- uc-01-visual-inspection-use-case-realization
- uc-01-visual-inspection-solution-on-page

## Related
- [Edge Deployment](../architecture/edge-deployment.md)
- [MES Integration](../architecture/mes-integration.md)
- [anomalib](../technologies/anomalib.md)
- [ultralytics](../technologies/ultralytics.md)
- [pypylon](../technologies/pypylon.md)
- [jetson-inference](../technologies/jetson-inference.md)
- [mmdetection](../technologies/mmdetection.md)
