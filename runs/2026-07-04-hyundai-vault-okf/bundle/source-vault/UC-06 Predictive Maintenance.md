---
title: "UC-06 Predictive Maintenance"
tags: [uc-06, predictive-maintenance, survival-analysis, acoustic-ml]
type: use-case
---

# UC-06 Predictive Maintenance

AI models predict machine failures and reduce unplanned downtime using vibration, acoustic, and thermal data.

## Problem Statement
Unplanned downtime costs $22,000/minute at automotive plants. Reactive maintenance misses early failure signals on high-criticality assets like stamping presses and welding cells.

## Solution
[[lifelines]] Weibull/Cox survival models estimate time-to-failure. [[pycox|DeepSurv]] handles non-linear sensor interactions. [[librosa]] extracts mel spectrograms from acoustic sensors for bearing wear detection. [[PyWavelets]] decomposes vibration signals. [[MLOps Pipeline|MLflow]] tracks experiments and manages model registry.

## Solution Architecture
```
Vibration + acoustic + thermal sensors → [[OPC-UA Integration|IoT Edge]] → [[librosa]] mel spectrograms → [[PyWavelets]] wavelet features → [[lifelines]] Weibull / [[pycox|DeepSurv]] → [[MLOps Pipeline|MLflow]] registry → SAP PM work orders → Asset health dashboard
```

## Key Repos
- [[lifelines]]
- [[pycox]]
- [[mlflow]]
- [[librosa]]
- [[PyWavelets]]

## Business Metrics
−40% unplanned downtime · −30% maintenance cost · +25% asset lifespan · 5:1 ROI

## Recommended Pilot
Ulsan stamping presses + Asan welding cells

## Related
- [[OPC-UA Integration]]
- [[MLOps Pipeline]]
- [[lifelines]]
- [[pycox]]
- [[librosa]]
- [[PyWavelets]]
- [[mlflow]]
