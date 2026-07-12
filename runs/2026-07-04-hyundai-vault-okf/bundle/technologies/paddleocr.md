---
type: technology
title: 'PaddleOCR'
description: 'Industrial-grade OCR by PaddlePaddle — text detection + recognition for VIN plates, part labels, and serial numbers in challenging industrial lighting.'
source_path: 'repos/PaddleOCR.md'
tags:
- repo
- uc-02
- ocr
timestamp: '2026-07-04'
---

> Original source (local copy): [repos/PaddleOCR.md](../source-vault/repos/PaddleOCR.md)
> Original source (WSL): [repos/PaddleOCR.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/repos/PaddleOCR.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/repos/PaddleOCR.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\repos\PaddleOCR.md`
# PaddleOCR

Industrial-grade OCR by PaddlePaddle — text detection + recognition for VIN plates, part labels, and serial numbers in challenging industrial lighting.

**GitHub:** https://github.com/PaddlePaddle/PaddleOCR
**Stars:** 78,088

## Use Cases
[UC-02 Variant Confirmation](../use-cases/uc-02-variant-confirmation.md) · [UC-08 Digital Traceability](../use-cases/uc-08-digital-traceability.md)

## How It's Used
Two-stage pipeline: DB (Differentiable Binarization) detects text regions, then CRNN recognizes characters. Handles curved text, low contrast, and partial occlusion common in factory environments.

## Technologies
DB text detection, CRNN recognition, PaddlePaddle
