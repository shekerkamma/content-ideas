---
title: "anomalib"
tags: [repo, uc-01, anomaly-detection]
type: repo
url: "https://github.com/openvinotoolkit/anomalib"
stars: "5,749"
---

# anomalib

Industrial anomaly detection library by OpenVINO. Implements PatchCore, FastFlow, PaDiM, and other algorithms that train on normal-only images — no labeled defect data needed.

**GitHub:** https://github.com/openvinotoolkit/anomalib
**Stars:** 5,749

## Use Cases
[[UC-01 Visual Inspection]]

## How It's Used
PatchCore extracts patch-level features from a pre-trained CNN backbone, builds a memory bank of normal features, then scores new images by distance to nearest normal patch. This means you only need images of good parts — no defect labeling required. FastFlow uses normalizing flows for the same purpose with different speed/accuracy tradeoffs.

## Technologies
PatchCore, FastFlow, PyTorch, ONNX
