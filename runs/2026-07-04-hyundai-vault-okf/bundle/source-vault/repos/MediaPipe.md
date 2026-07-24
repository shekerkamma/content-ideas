---
title: "MediaPipe"
tags: [repo, uc-04, pose-estimation, edge]
type: repo
url: "https://github.com/google/mediapipe"
stars: "35,252"
---

# MediaPipe

Google's lightweight ML framework for on-device pose, hand, and face tracking. Runs in real time on edge devices without GPU.

**GitHub:** https://github.com/google/mediapipe
**Stars:** 35,252

## Use Cases
[[UC-04 SOP Compliance]]

## How It's Used
Provides lightweight real-time pose estimation that runs on CPU. Used for real-time operator feedback overlays where mmpose/HRNet would be too slow without GPU.

## Technologies
BlazePose, on-device ML, TFLite
