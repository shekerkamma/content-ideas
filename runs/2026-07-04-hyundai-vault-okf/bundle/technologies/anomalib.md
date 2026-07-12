---
type: technology
title: 'anomalib'
description: 'Industrial anomaly detection library by OpenVINO. Implements PatchCore, FastFlow, PaDiM, and other algorithms that train on normal-only images — no labeled defect data needed.'
source_path: 'repos/anomalib.md'
tags:
- repo
- uc-01
- anomaly-detection
timestamp: '2026-07-04'
---

> Original source (local copy): [repos/anomalib.md](../source-vault/repos/anomalib.md)
> Original source (WSL): [repos/anomalib.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/repos/anomalib.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/repos/anomalib.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\repos\anomalib.md`
# anomalib

Industrial anomaly detection library by OpenVINO. Implements PatchCore, FastFlow, PaDiM, and other algorithms that train on normal-only images — no labeled defect data needed.

**GitHub:** https://github.com/openvinotoolkit/anomalib
**Stars:** 5,749

## Use Cases
[UC-01 Visual Inspection](../use-cases/uc-01-visual-inspection.md)

## How It's Used
PatchCore extracts patch-level features from a pre-trained CNN backbone, builds a memory bank of normal features, then scores new images by distance to nearest normal patch. This means you only need images of good parts — no defect labeling required. FastFlow uses normalizing flows for the same purpose with different speed/accuracy tradeoffs.

## Technologies
PatchCore, FastFlow, PyTorch, ONNX
