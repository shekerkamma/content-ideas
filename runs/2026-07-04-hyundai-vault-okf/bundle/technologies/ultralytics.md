---
type: technology
title: 'ultralytics'
description: 'YOLOv8/YOLOv9 — real-time object detection, segmentation, pose estimation, and classification. The workhorse model across 4 use cases.'
source_path: 'repos/ultralytics.md'
tags:
- repo
- uc-01
- uc-02
- uc-03
- uc-07
- object-detection
timestamp: '2026-07-04'
---

> Original source (local copy): [repos/ultralytics.md](../source-vault/repos/ultralytics.md)
> Original source (WSL): [repos/ultralytics.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/repos/ultralytics.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/repos/ultralytics.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\repos\ultralytics.md`
# ultralytics

YOLOv8/YOLOv9 — real-time object detection, segmentation, pose estimation, and classification. The workhorse model across 4 use cases.

**GitHub:** https://github.com/ultralytics/ultralytics
**Stars:** 57,284

## Use Cases
[UC-01 Visual Inspection](../use-cases/uc-01-visual-inspection.md) · [UC-02 Variant Confirmation](../use-cases/uc-02-variant-confirmation.md) · [UC-03 Component Validation](../use-cases/uc-03-component-validation.md) · [UC-07 Safety Monitoring](../use-cases/uc-07-safety-monitoring.md)

## How It's Used
YOLOv8 is used for defect localization (UC-01), component detection for BOM matching (UC-02), keypoint-based fitment verification (UC-03 via YOLOv8-pose), and PPE detection (UC-07). Custom training on plant-specific classes. Exports to TensorRT for Jetson edge inference.

## Technologies
YOLOv8, YOLOv8-pose, TensorRT, ONNX
