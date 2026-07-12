---
type: use_case
title: 'UC-04 SOP Compliance'
description: 'Vision-based monitoring ensures operators follow defined manufacturing procedures with real-time deviation alerts.'
source_path: 'UC-04 SOP Compliance.md'
tags:
- uc-04
- sop-compliance
- pose-estimation
- action-recognition
timestamp: '2026-07-04'
---

> Original source (local copy): [UC-04 SOP Compliance.md](../source-vault/UC-04 SOP Compliance.md)
> Original source (WSL): [UC-04 SOP Compliance.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/UC-04%20SOP%20Compliance.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/UC-04%20SOP%20Compliance.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\UC-04 SOP Compliance.md`
# UC-04 SOP Compliance

Vision-based monitoring ensures operators follow defined manufacturing procedures with real-time deviation alerts.

## Problem Statement
Operators skipping steps or deviating from SOPs introduce assembly defects found only at final inspection — or worse, in the field. Manual SOP audits are slow, sample-based, and subjective.

## Solution
[HRNet/ViTPose](../technologies/mmpose.md) extracts human skeleton keypoints. [SlowFast](../technologies/slowfast.md) temporal action recognition classifies multi-step assembly sequences. [MediaPipe](../technologies/mediapipe.md) provides lightweight on-device pose for real-time feedback. Detected actions are matched against a digital SOP step graph.

## Solution Architecture
```
Station IP cameras → MediaPipe on-device pose → mmpose HRNet/ViTPose → SlowFast action recognition → SOP sequence matcher → MES work-order context → Supervisor deviation feed
```

## Key Repos
- [mmpose](../technologies/mmpose.md)
- mmaction2
- [MediaPipe](../technologies/mediapipe.md)
- [SlowFast](../technologies/slowfast.md)

## Business Metrics
−65% SOP deviations · −40% final defects · +90% compliance rate · Real-time alerts

## Recommended Pilot
Complex multi-step assembly cells

## Related
- [Edge Deployment](../architecture/edge-deployment.md)
- [MES Integration](../architecture/mes-integration.md)
- [mmpose](../technologies/mmpose.md)
- [SlowFast](../technologies/slowfast.md)
- [MediaPipe](../technologies/mediapipe.md)
- mmaction2
