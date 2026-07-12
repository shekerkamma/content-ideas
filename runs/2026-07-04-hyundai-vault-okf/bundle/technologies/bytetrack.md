---
type: technology
title: 'ByteTrack'
description: 'High-performance multi-object tracker — associates detections across video frames for person and vehicle tracking.'
source_path: 'repos/ByteTrack.md'
tags:
- repo
- uc-07
- multi-object-tracking
timestamp: '2026-07-04'
---

> Original source (local copy): [repos/ByteTrack.md](../source-vault/repos/ByteTrack.md)
> Original source (WSL): [repos/ByteTrack.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/repos/ByteTrack.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/repos/ByteTrack.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\repos\ByteTrack.md`
# ByteTrack

High-performance multi-object tracker — associates detections across video frames for person and vehicle tracking.

**GitHub:** https://github.com/ifzhang/ByteTrack
**Stars:** 4,600

## Use Cases
[UC-07 Safety Monitoring](../use-cases/uc-07-safety-monitoring.md)

## How It's Used
Uses both high and low confidence detections for association (the 'BYTE' innovation), improving tracking through occlusions. Combined with YOLOv8 detections for person-forklift proximity monitoring.

## Technologies
BYTE association, Kalman filter, IoU matching
