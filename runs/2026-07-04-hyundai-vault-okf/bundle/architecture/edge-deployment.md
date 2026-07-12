---
type: architecture
title: 'Edge Deployment'
description: 'Deploying AI models to plant-floor edge devices for line-speed inference.'
source_path: 'architecture/Edge Deployment.md'
tags:
- architecture
- edge
- deployment
timestamp: '2026-07-04'
---

> Original source (local copy): [architecture/Edge Deployment.md](../source-vault/architecture/Edge Deployment.md)
> Original source (WSL): [architecture/Edge Deployment.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/architecture/Edge%20Deployment.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/architecture/Edge%20Deployment.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\architecture\Edge Deployment.md`
# Edge Deployment

Deploying AI models to plant-floor edge devices for line-speed inference.

## Hardware Platforms
- **NVIDIA Jetson Orin** — primary edge GPU for vision inference (UC-01, UC-03, UC-04)
- **NVIDIA Jetson Orin Nano** — cost-effective option for simpler models (UC-07)
- **Hailo-8** — low-power AI accelerator for safety cameras (UC-07)
- **Intel OpenVINO** — CPU-based inference for lightweight models

## Model Optimization Pipeline
1. Train in cloud (SageMaker / Azure ML)
2. Export to ONNX (cross-platform intermediate format)
3. Convert to TensorRT (Jetson) or HEF (Hailo)
4. Quantize to FP16 or INT8 for speed
5. Deploy via OTA update framework

## Latency Targets
| Use Case | Target | Hardware |
|----------|--------|----------|
| [UC-01 Visual Inspection](../use-cases/uc-01-visual-inspection.md) | <2s | Jetson Orin |
| [UC-03 Component Validation](../use-cases/uc-03-component-validation.md) | <200ms | Jetson Orin |
| [UC-04 SOP Compliance](../use-cases/uc-04-sop-compliance.md) | Real-time | MediaPipe CPU |
| [UC-07 Safety Monitoring](../use-cases/uc-07-safety-monitoring.md) | <500ms | Hailo-8 / Jetson Nano |

## Related
- [ultralytics](../technologies/ultralytics.md) · [jetson-inference](../technologies/jetson-inference.md) · onnxruntime · [anomalib](../technologies/anomalib.md)
