---
title: "UC-02 Variant Confirmation"
tags: [uc-02, variant-confirmation, ocr, object-detection]
type: use-case
---

# UC-02 Variant Confirmation

Computer vision and VIN/barcode recognition validate vehicle model, trim, and component matching during assembly.

## Problem Statement
Wrong variant assembly — mismatched trim, components, or accessories — costs millions in rework. With 50+ variants per model on mixed lines, manual verification cannot scale.

## Solution
[[PaddleOCR]] provides industrial-grade text detection for VIN plates and part labels. [[ultralytics|YOLOv8]] custom-trained on component classes detects installed parts and matches against BOM. Combined OCR + detection pipeline runs in a single inference pass.

## Solution Architecture
```
Vision cameras + VIN/barcode scanners → [[PaddleOCR]] text detection → [[ultralytics|YOLOv8]] component detection → BOM-match rules engine → [[MES Integration|SAP MES]] → Line controller signal
```

## Key Repos
- [[PaddleOCR]]
- [[EasyOCR]]
- [[ultralytics]]

## Business Metrics
−90% wrong variants · −70% rework events · 99.8% verification accuracy · <1s check latency

## Recommended Pilot
Mixed-model assembly line

## Related
- [[MES Integration]]
- [[PaddleOCR]]
- [[EasyOCR]]
- [[ultralytics]]
- [[Edge Deployment]]
