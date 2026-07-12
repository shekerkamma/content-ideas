---
title: "Edge Deployment"
tags: [architecture, edge, deployment]
type: architecture
---

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
| [[UC-01 Visual Inspection]] | <2s | Jetson Orin |
| [[UC-03 Component Validation]] | <200ms | Jetson Orin |
| [[UC-04 SOP Compliance]] | Real-time | MediaPipe CPU |
| [[UC-07 Safety Monitoring]] | <500ms | Hailo-8 / Jetson Nano |

## Related
- [[ultralytics]] · [[jetson-inference]] · [[onnxruntime]] · [[anomalib]]
