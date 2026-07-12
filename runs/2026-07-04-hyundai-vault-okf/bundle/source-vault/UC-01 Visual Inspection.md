---
title: "UC-01 Visual Inspection"
tags: [uc-01, visual-inspection, computer-vision, quality]
type: use-case
---

# UC-01 Visual Inspection

AI-enabled cameras detect paint defects, scratches, dents, welding inconsistencies, and panel gaps in real time.

## Problem Statement
Manual inspection misses ~12% of surface defects. Inspector fatigue across shifts causes inconsistent quality. Defects that escape to downstream stages cost 10-100x more to fix.

## Solution
CNN-based anomaly detection trained on normal-only images (no labeled defect data needed). [[anomalib]] PatchCore scores surface anomalies, [[ultralytics|YOLOv8]] localizes and classifies specific defect types. Edge inference via [[Edge Deployment|TensorRT on Jetson Orin]] meets <2s line-speed constraint.

## Solution Architecture
```
Cognex / Basler cameras (pypylon) → NVIDIA Jetson Orin (TensorRT) → anomalib PatchCore / YOLOv8 → [[OPC-UA Integration|OPC-UA]] → [[MES Integration|MES line-hold]] → Quality DB → Dashboard
```

## Key Repos
- [[anomalib]]
- [[ultralytics]]
- [[jetson-inference]]
- [[pypylon]]
- [[mmdetection]]
- [[mmpretrain]]

## Business Metrics
−45% rework costs · −60% escape defects · <2s detection latency · +35% line throughput

## Recommended Pilot
IONIQ 5 / IONIQ 9 paint line at Metaplant America (HMGMA)

## Deck Assets
- [[uc-01-visual-inspection-use-case-realization]]
- [[uc-01-visual-inspection-solution-on-page]]

## Related
- [[Edge Deployment]]
- [[MES Integration]]
- [[anomalib]]
- [[ultralytics]]
- [[pypylon]]
- [[jetson-inference]]
- [[mmdetection]]
