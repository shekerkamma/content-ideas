---
title: "MLOps Pipeline"
tags: [architecture, mlops, deployment]
type: architecture
---

# MLOps Pipeline

End-to-end ML lifecycle management for industrial AI models.

## Stack
- **[[mlflow]]** — experiment tracking + model registry
- **AWS SageMaker** / **Azure ML** — managed training + serving
- **Feature Store** — centralized feature management
- **[[SHAP]]** — model explainability for regulated environments

## Pipeline Stages
1. **Data ingestion** — sensors → historian → feature store
2. **Training** — automated retraining on new data (weekly/monthly)
3. **Evaluation** — champion/challenger comparison on holdout set
4. **Registry** — promote to staging → production via MLflow
5. **Deployment** — push to [[Edge Deployment|edge]] or cloud endpoint
6. **Monitoring** — drift detection, accuracy tracking, alerting
7. **Retraining** — auto-triggered when drift exceeds threshold

## Use Cases
- [[UC-05 Predictive Quality]] — XGBoost retraining pipeline
- [[UC-06 Predictive Maintenance]] — survival model lifecycle

## Related
- [[mlflow]] · [[XGBoost]] · [[SHAP]] · [[Edge Deployment]]
