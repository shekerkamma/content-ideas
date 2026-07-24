---
type: technology
title: 'MediaPipe'
description: "Google's lightweight ML framework for on-device pose, hand, and face tracking. Runs in real time on edge devices without GPU."
source_path: 'repos/MediaPipe.md'
tags:
- repo
- uc-04
- pose-estimation
- edge
timestamp: '2026-07-04'
---

> Original source (local copy): [repos/MediaPipe.md](../source-vault/repos/MediaPipe.md)
> Original source (WSL): [repos/MediaPipe.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/repos/MediaPipe.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/repos/MediaPipe.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\repos\MediaPipe.md`
# MediaPipe

Google's lightweight ML framework for on-device pose, hand, and face tracking. Runs in real time on edge devices without GPU.

**GitHub:** https://github.com/google/mediapipe
**Stars:** 35,252

## Use Cases
[UC-04 SOP Compliance](../use-cases/uc-04-sop-compliance.md)

## How It's Used
Provides lightweight real-time pose estimation that runs on CPU. Used for real-time operator feedback overlays where mmpose/HRNet would be too slow without GPU.

## Technologies
BlazePose, on-device ML, TFLite
