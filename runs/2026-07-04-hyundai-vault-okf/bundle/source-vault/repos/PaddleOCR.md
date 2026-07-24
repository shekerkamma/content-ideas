---
title: "PaddleOCR"
tags: [repo, uc-02, ocr]
type: repo
url: "https://github.com/PaddlePaddle/PaddleOCR"
stars: "78,088"
---

# PaddleOCR

Industrial-grade OCR by PaddlePaddle — text detection + recognition for VIN plates, part labels, and serial numbers in challenging industrial lighting.

**GitHub:** https://github.com/PaddlePaddle/PaddleOCR
**Stars:** 78,088

## Use Cases
[[UC-02 Variant Confirmation]] · [[UC-08 Digital Traceability]]

## How It's Used
Two-stage pipeline: DB (Differentiable Binarization) detects text regions, then CRNN recognizes characters. Handles curved text, low contrast, and partial occlusion common in factory environments.

## Technologies
DB text detection, CRNN recognition, PaddlePaddle
