---
type: technology
title: 'SlowFast'
description: "Facebook Research's SlowFast networks for video understanding — dual-pathway architecture that captures both spatial and temporal features."
source_path: 'repos/SlowFast.md'
tags:
- repo
- uc-04
- action-recognition
timestamp: '2026-07-04'
---

> Original source (local copy): [repos/SlowFast.md](../source-vault/repos/SlowFast.md)
> Original source (WSL): [repos/SlowFast.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/repos/SlowFast.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/repos/SlowFast.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\repos\SlowFast.md`
# SlowFast

Facebook Research's SlowFast networks for video understanding — dual-pathway architecture that captures both spatial and temporal features.

**GitHub:** https://github.com/facebookresearch/SlowFast
**Stars:** 7,362

## Use Cases
[UC-04 SOP Compliance](../use-cases/uc-04-sop-compliance.md)

## How It's Used
Slow pathway (low frame rate, high resolution) captures spatial detail. Fast pathway (high frame rate, low resolution) captures motion. Combined, they classify multi-step assembly actions for SOP matching.

## Technologies
SlowFast networks, MViT, PyTorch
