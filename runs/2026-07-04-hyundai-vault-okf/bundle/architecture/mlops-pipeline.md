---
type: architecture
title: 'MLOps Pipeline'
description: 'End-to-end ML lifecycle management for industrial AI models.'
source_path: 'architecture/MLOps Pipeline.md'
tags:
- architecture
- mlops
- deployment
timestamp: '2026-07-04'
---

> Original source (local copy): [architecture/MLOps Pipeline.md](../source-vault/architecture/MLOps Pipeline.md)
> Original source (WSL): [architecture/MLOps Pipeline.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/architecture/MLOps%20Pipeline.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/architecture/MLOps%20Pipeline.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\architecture\MLOps Pipeline.md`
# MLOps Pipeline

End-to-end ML lifecycle management for industrial AI models.

## Stack
- **mlflow** — experiment tracking + model registry
- **AWS SageMaker** / **Azure ML** — managed training + serving
- **Feature Store** — centralized feature management
- **SHAP** — model explainability for regulated environments

## Pipeline Stages
1. **Data ingestion** — sensors → historian → feature store
2. **Training** — automated retraining on new data (weekly/monthly)
3. **Evaluation** — champion/challenger comparison on holdout set
4. **Registry** — promote to staging → production via MLflow
5. **Deployment** — push to [edge](../architecture/edge-deployment.md) or cloud endpoint
6. **Monitoring** — drift detection, accuracy tracking, alerting
7. **Retraining** — auto-triggered when drift exceeds threshold

## Use Cases
- [UC-05 Predictive Quality](../use-cases/uc-05-predictive-quality.md) — XGBoost retraining pipeline
- [UC-06 Predictive Maintenance](../use-cases/uc-06-predictive-maintenance.md) — survival model lifecycle

## Related
- mlflow · [XGBoost](../technologies/xgboost.md) · SHAP · [Edge Deployment](../architecture/edge-deployment.md)
