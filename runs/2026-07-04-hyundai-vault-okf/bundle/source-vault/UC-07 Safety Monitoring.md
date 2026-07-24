---
title: "UC-07 Safety Monitoring"
tags: [uc-07, safety-monitoring, ppe-detection, zone-monitoring]
type: use-case
---

# UC-07 Safety Monitoring

Vision AI monitors PPE compliance, unsafe movements, restricted zone access, and forklift interactions.

## Problem Statement
PPE non-compliance and restricted zone violations cause workplace injuries and EHS failures. Manual safety rounds are periodic and miss real-time violations.

## Solution
[[ultralytics|YOLOv8]] custom-trained on PPE classes (helmet, vest, goggles). [[supervision]] polygon zone detection for restricted area intrusion with dwell-time thresholds. [[ByteTrack]] multi-object tracking for person-vehicle proximity monitoring. [[Edge Deployment|Hailo/Jetson]] edge inference with privacy anonymization.

## Solution Architecture
```
Wide-FOV safety cameras → [[Edge Deployment|Hailo-8 / Jetson Orin]] → [[ultralytics|YOLOv8]] PPE detector → [[ByteTrack]] tracker → [[supervision]] zone-violation engine → EHS platform → Auto-incident report → Compliance scorecard
```

## Key Repos
- [[ultralytics]]
- [[supervision]]
- [[ByteTrack]]
- [[hailo_model_zoo]]

## Business Metrics
−55% safety incidents · 98% PPE compliance · <500ms alert latency · Audit-ready EHS reports

## Recommended Pilot
High-traffic areas with forklift interaction

## Related
- [[Edge Deployment]]
- [[ultralytics]]
- [[ByteTrack]]
- [[supervision]]
