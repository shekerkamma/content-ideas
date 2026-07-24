---
type: technology
title: 'supervision'
description: "Roboflow's computer vision toolkit — polygon zone detection, tracking overlays, and annotation utilities."
source_path: 'repos/supervision.md'
tags:
- repo
- uc-07
- zone-monitoring
- tracking
timestamp: '2026-07-04'
---

> Original source (local copy): [repos/supervision.md](../source-vault/repos/supervision.md)
> Original source (WSL): [repos/supervision.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/repos/supervision.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/repos/supervision.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\repos\supervision.md`
# supervision

Roboflow's computer vision toolkit — polygon zone detection, tracking overlays, and annotation utilities.

**GitHub:** https://github.com/roboflow/supervision
**Stars:** 7,000

## Use Cases
[UC-07 Safety Monitoring](../use-cases/uc-07-safety-monitoring.md)

## How It's Used
PolygonZone defines restricted areas on camera frames. Detections (from YOLOv8) are checked against zones each frame. Configurable dwell-time thresholds prevent false alarms from brief border crossings.

## Technologies
PolygonZone, LineZone, tracking overlays
