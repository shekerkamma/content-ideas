---
title: "UC-03 Component Validation"
tags: [uc-03, component-validation, keypoint-detection, fitment]
type: use-case
---

# UC-03 Component Validation

AI cameras verify seat type, orientation, mounting alignment, fastening completion, and fitment accuracy.

## Problem Statement
Incorrect seat type, orientation, or mounting errors pass undetected. Causes safety issues, costly post-delivery recalls, and customer satisfaction failures.

## Solution
[[mmpose]] keypoint detection locates mounting bolt positions and alignment markers. [[ultralytics|YOLOv8]] with keypoint head combines object detection + pose estimation in a single model. Multi-angle camera setup eliminates blind spots. ONNX export for [[Edge Deployment|Jetson Orin]] inference.

## Solution Architecture
```
Multi-angle station cameras + torque wrenches → [[mmpose]] keypoint detection → [[ultralytics|YOLOv8-pose]] → Fitment classifier → [[MES Integration|MES]] variant config → Operator tablet pass/fail
```

## Key Repos
- [[mmpose]]
- [[mmdetection]]
- [[onnxruntime]]
- [[ultralytics]]

## Business Metrics
−85% fitment errors · Zero seat recalls · +30% inspection speed · 100% vehicle coverage

## Recommended Pilot
Seat installation station

## Related
- [[Edge Deployment]]
- [[MES Integration]]
- [[mmpose]]
- [[ultralytics]]
- [[onnxruntime]]
