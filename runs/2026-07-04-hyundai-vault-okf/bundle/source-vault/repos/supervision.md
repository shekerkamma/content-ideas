---
title: "supervision"
tags: [repo, uc-07, zone-monitoring, tracking]
type: repo
url: "https://github.com/roboflow/supervision"
stars: "7,000"
---

# supervision

Roboflow's computer vision toolkit — polygon zone detection, tracking overlays, and annotation utilities.

**GitHub:** https://github.com/roboflow/supervision
**Stars:** 7,000

## Use Cases
[[UC-07 Safety Monitoring]]

## How It's Used
PolygonZone defines restricted areas on camera frames. Detections (from YOLOv8) are checked against zones each frame. Configurable dwell-time thresholds prevent false alarms from brief border crossings.

## Technologies
PolygonZone, LineZone, tracking overlays
