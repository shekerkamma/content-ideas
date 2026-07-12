---
title: "UC-04 SOP Compliance"
tags: [uc-04, sop-compliance, pose-estimation, action-recognition]
type: use-case
---

# UC-04 SOP Compliance

Vision-based monitoring ensures operators follow defined manufacturing procedures with real-time deviation alerts.

## Problem Statement
Operators skipping steps or deviating from SOPs introduce assembly defects found only at final inspection — or worse, in the field. Manual SOP audits are slow, sample-based, and subjective.

## Solution
[[mmpose|HRNet/ViTPose]] extracts human skeleton keypoints. [[SlowFast]] temporal action recognition classifies multi-step assembly sequences. [[MediaPipe]] provides lightweight on-device pose for real-time feedback. Detected actions are matched against a digital SOP step graph.

## Solution Architecture
```
Station IP cameras → [[MediaPipe]] on-device pose → [[mmpose]] HRNet/ViTPose → [[SlowFast]] action recognition → SOP sequence matcher → [[MES Integration|MES]] work-order context → Supervisor deviation feed
```

## Key Repos
- [[mmpose]]
- [[mmaction2]]
- [[MediaPipe]]
- [[SlowFast]]

## Business Metrics
−65% SOP deviations · −40% final defects · +90% compliance rate · Real-time alerts

## Recommended Pilot
Complex multi-step assembly cells

## Related
- [[Edge Deployment]]
- [[MES Integration]]
- [[mmpose]]
- [[SlowFast]]
- [[MediaPipe]]
- [[mmaction2]]
