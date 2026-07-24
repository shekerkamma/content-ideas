---
type: use_case
title: 'UC-03 Component Validation'
description: 'AI cameras verify seat type, orientation, mounting alignment, fastening completion, and fitment accuracy.'
source_path: 'UC-03 Component Validation.md'
tags:
- uc-03
- component-validation
- keypoint-detection
- fitment
timestamp: '2026-07-04'
---

> Original source (local copy): [UC-03 Component Validation.md](../source-vault/UC-03 Component Validation.md)
> Original source (WSL): [UC-03 Component Validation.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/UC-03%20Component%20Validation.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/UC-03%20Component%20Validation.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\UC-03 Component Validation.md`
# UC-03 Component Validation

AI cameras verify seat type, orientation, mounting alignment, fastening completion, and fitment accuracy.

## Problem Statement
Incorrect seat type, orientation, or mounting errors pass undetected. Causes safety issues, costly post-delivery recalls, and customer satisfaction failures.

## Solution
[mmpose](../technologies/mmpose.md) keypoint detection locates mounting bolt positions and alignment markers. [YOLOv8](../technologies/ultralytics.md) with keypoint head combines object detection + pose estimation in a single model. Multi-angle camera setup eliminates blind spots. ONNX export for [Jetson Orin](../architecture/edge-deployment.md) inference.

## Solution Architecture
```
Multi-angle station cameras + torque wrenches → mmpose keypoint detection → YOLOv8-pose → Fitment classifier → MES variant config → Operator tablet pass/fail
```

## Key Repos
- [mmpose](../technologies/mmpose.md)
- [mmdetection](../technologies/mmdetection.md)
- onnxruntime
- [ultralytics](../technologies/ultralytics.md)

## Business Metrics
−85% fitment errors · Zero seat recalls · +30% inspection speed · 100% vehicle coverage

## Recommended Pilot
Seat installation station

## Related
- [Edge Deployment](../architecture/edge-deployment.md)
- [MES Integration](../architecture/mes-integration.md)
- [mmpose](../technologies/mmpose.md)
- [ultralytics](../technologies/ultralytics.md)
- onnxruntime
