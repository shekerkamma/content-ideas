---
title: "UC-05 Predictive Quality"
tags: [uc-05, predictive-quality, machine-learning, sensor-data]
type: use-case
---

# UC-05 Predictive Quality

ML models predict defect occurrence using production line sensor data and historical trends.

## Problem Statement
Defects found at end-of-line cost 10–100x more than defects caught in process. Reactive models miss early warning signals buried in hundreds of sensor parameters.

## Solution
[[OPC-UA Integration|OPC-UA async client]] ingests real-time sensor streams into a feature store. [[XGBoost]] / [[LightGBM]] gradient boosting handles tabular sensor data with high accuracy. [[SHAP]] TreeExplainer provides per-prediction explainability — operators see which parameters drive defect risk.

## Solution Architecture
```
IoT sensors → [[OPC-UA Integration|OPC-UA async]] → AVEVA PI historian → Feature store → [[XGBoost]] / [[LightGBM]] → [[SHAP]] waterfall explainability → Early-warning dashboard → Parameter recommendations
```

## Key Repos
- [[XGBoost]]
- [[LightGBM]]
- [[SHAP]]
- [[opcua-asyncio]]

## Business Metrics
−35% scrap & rework · −25% warranty claims · +20% OEE · 3–5x measured ROI

## Recommended Pilot
Body shop or paint process with rich sensor data

## Related
- [[OPC-UA Integration]]
- [[MLOps Pipeline]]
- [[XGBoost]]
- [[LightGBM]]
- [[SHAP]]
- [[opcua-asyncio]]
