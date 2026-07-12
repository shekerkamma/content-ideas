---
type: use_case
title: 'UC-02 Variant Confirmation'
description: 'Computer vision and VIN/barcode recognition validate vehicle model, trim, and component matching during assembly.'
source_path: 'UC-02 Variant Confirmation.md'
tags:
- uc-02
- variant-confirmation
- ocr
- object-detection
timestamp: '2026-07-04'
---

> Original source (local copy): [UC-02 Variant Confirmation.md](../source-vault/UC-02 Variant Confirmation.md)
> Original source (WSL): [UC-02 Variant Confirmation.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/UC-02%20Variant%20Confirmation.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/UC-02%20Variant%20Confirmation.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\UC-02 Variant Confirmation.md`
# UC-02 Variant Confirmation

Computer vision and VIN/barcode recognition validate vehicle model, trim, and component matching during assembly.

## Problem Statement
Wrong variant assembly — mismatched trim, components, or accessories — costs millions in rework. With 50+ variants per model on mixed lines, manual verification cannot scale.

## Solution
[PaddleOCR](../technologies/paddleocr.md) provides industrial-grade text detection for VIN plates and part labels. [YOLOv8](../technologies/ultralytics.md) custom-trained on component classes detects installed parts and matches against BOM. Combined OCR + detection pipeline runs in a single inference pass.

## Solution Architecture
```
Vision cameras + VIN/barcode scanners → PaddleOCR text detection → YOLOv8 component detection → BOM-match rules engine → SAP MES → Line controller signal
```

## Key Repos
- [PaddleOCR](../technologies/paddleocr.md)
- EasyOCR
- [ultralytics](../technologies/ultralytics.md)

## Business Metrics
−90% wrong variants · −70% rework events · 99.8% verification accuracy · <1s check latency

## Recommended Pilot
Mixed-model assembly line

## Related
- [MES Integration](../architecture/mes-integration.md)
- [PaddleOCR](../technologies/paddleocr.md)
- EasyOCR
- [ultralytics](../technologies/ultralytics.md)
- [Edge Deployment](../architecture/edge-deployment.md)
