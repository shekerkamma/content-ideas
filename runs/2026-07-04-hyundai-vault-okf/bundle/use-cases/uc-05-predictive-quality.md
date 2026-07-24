---
type: use_case
title: 'UC-05 Predictive Quality'
description: 'ML models predict defect occurrence using production line sensor data and historical trends.'
source_path: 'UC-05 Predictive Quality.md'
tags:
- uc-05
- predictive-quality
- machine-learning
- sensor-data
timestamp: '2026-07-04'
---

> Original source (local copy): [UC-05 Predictive Quality.md](../source-vault/UC-05 Predictive Quality.md)
> Original source (WSL): [UC-05 Predictive Quality.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/UC-05%20Predictive%20Quality.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/UC-05%20Predictive%20Quality.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\UC-05 Predictive Quality.md`
# UC-05 Predictive Quality

ML models predict defect occurrence using production line sensor data and historical trends.

## Problem Statement
Defects found at end-of-line cost 10–100x more than defects caught in process. Reactive models miss early warning signals buried in hundreds of sensor parameters.

## Solution
[OPC-UA async client](../architecture/opc-ua-integration.md) ingests real-time sensor streams into a feature store. [XGBoost](../technologies/xgboost.md) / LightGBM gradient boosting handles tabular sensor data with high accuracy. SHAP TreeExplainer provides per-prediction explainability — operators see which parameters drive defect risk.

## Solution Architecture
```
IoT sensors → OPC-UA async → AVEVA PI historian → Feature store → XGBoost / LightGBM → SHAP waterfall explainability → Early-warning dashboard → Parameter recommendations
```

## Key Repos
- [XGBoost](../technologies/xgboost.md)
- LightGBM
- SHAP
- opcua-asyncio

## Business Metrics
−35% scrap & rework · −25% warranty claims · +20% OEE · 3–5x measured ROI

## Recommended Pilot
Body shop or paint process with rich sensor data

## Related
- [OPC-UA Integration](../architecture/opc-ua-integration.md)
- [MLOps Pipeline](../architecture/mlops-pipeline.md)
- [XGBoost](../technologies/xgboost.md)
- LightGBM
- SHAP
- opcua-asyncio
