---
title: A CUDA arch list is not the compatibility test — run a kernel
date: 2026-09-06
category: environment
module: torch-gpu
problem_type: bug
component: environment
severity: medium
applies_when:
  - "A torch-based tool fails with cudaErrorNoKernelImageForDevice"
  - "torch.cuda.is_available() returns True but every operation fails"
  - "Choosing a torch/CUDA wheel for an older GPU"
  - "Deciding whether GPU is worth using after making CUDA work"
tags: [cuda, torch, pascal, docling, wsl2, verification, benchmarking]
---

# A CUDA arch list is not the compatibility test — run a kernel

## Context

Installing `docling` (for `book-to-skill --mode technical`) pulled
`torch 2.14.0+cu130`. Every docling run died with:

```
CUDA error: no kernel image is available for execution on the device
```

The machine: **NVIDIA GeForce GTX 1050 Ti**, compute capability **6.1**
(Pascal, `sm_61`), driver 582.66 (CUDA 13.0 capable), WSL2 with `/dev/dxg`
passthrough.

## Guidance

**Rule 1 — `torch.cuda.is_available()` returning True says nothing about whether
a kernel can run.**

The device enumerates, memory allocates, and `is_available()` is `True`. The
failure happens at the first kernel *launch*, deep inside whatever library is
calling — so it reads as that library's bug. It is not. Diagnose with:

```python
import torch
print(torch.cuda.get_arch_list())        # ['sm_75','sm_80','sm_86','sm_90','sm_100','sm_120']
print(torch.cuda.get_device_capability(0))  # (6, 1)
```

Modern wheels have dropped Pascal: the cu130 build's floor is `sm_75` (Turing).
The wheel physically contains no kernels this card can execute. **The driver was
never the problem — the wheel was too new.**

**Rule 2 — The fix is an older CUDA wheel, not a driver change.**

```bash
uv pip install "torch==2.6.0" "torchvision==0.21.0" \
  --index-url https://download.pytorch.org/whl/cu124
```

When installing alongside a package that also depends on torch, pin it and use
`--index-strategy unsafe-best-match --extra-index-url …` so the resolver cannot
quietly restore the cu130 build.

**Rule 3 — Do not test the fix by grepping the arch list for your capability.**

The cu124 build's arch list is `sm_50, sm_60, sm_70, sm_75, sm_80, sm_86, sm_90`.
**`sm_61` is absent from the working build too.** Read literally, the fix looks
like it failed.

It works because CUDA runs a cubin built for capability `X.y` on any device
`X.z` where `z >= y` within the same major version — the `sm_60` binary executes
on a 6.1 device. Grepping for the exact capability reports a working fix as
broken and sends you hunting for a wheel that does not exist.

**Test by running a kernel, and confirm the GPU is actually busy:**

```python
a = torch.randn(512,512,device='cuda'); (a@a); torch.cuda.synchronize()
torch.nn.Conv2d(3,16,3).cuda()(torch.randn(1,3,64,64,device='cuda'))
```
```bash
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader
# during the run: 100 %, 1363 MiB   <- this is the proof, not the absent error
```

**Rule 4 — "CUDA works" and "GPU is worth using" are different questions.
Measure the second, and discard the first sample.**

Same 11-page document, same torch build, only the device varying:

| Run | GPU | CPU (12 cores) |
|---|---|---|
| 1 | 42.89 s | 35.49 s |
| 2 | 31.17 s | 33.86 s |
| 3 | 31.22 s | 32.35 s |

Steady state: **GPU 31.20 s vs CPU 33.11 s** — 5.8% faster, with **11.7 s of
one-time CUDA context warmup** on the first run. A single-sample reading said the
GPU was *21% slower* and reversed on repetition. Output was byte-identical either
way, which is the check that matters more than the clock.

**Conclusion for this machine: not worth adopting for docling.** ~2 s on a 30 s
job does not justify a 5.6 GB venv and a permanent torch 2.6.0 pin, and a one-off
conversion is genuinely faster on CPU because of the warmup. Pascal is gone from
newer wheels for good, so that pin is a dead-end branch.

## Why This Matters

Three separate false signals in one debugging session, each of which would have
ended the investigation at a wrong answer:

- `is_available: True` → "CUDA is fine, the library is broken."
- `sm_61` absent from the cu124 list → "the fix failed, find an older wheel."
- One timing sample → "the GPU is 21% slower, don't bother."

Only running a real kernel, watching `nvidia-smi`, and repeating the benchmark
produced the true picture.

## When to Apply

- Any `cudaErrorNoKernelImageForDevice`, on any torch-based tool.
- Before concluding a GPU is unsupported: check `get_arch_list()` against
  `get_device_capability()`, then remember the `X.z >= X.y` rule.
- Before adopting a GPU path: benchmark it, discard the warmup run, and confirm
  the output is unchanged.

## Workaround

`CUDA_VISIBLE_DEVICES=""` forces CPU and works with any torch build. For docling
on this machine that is also the recommended path — `book-to-skill` already falls
back to `pdftotext` or CPU automatically, so the default behaviour was correct.

## Related

- `docs/solutions/conventions/extractor-structure-counts-are-hints-not-maps.md` —
  the extraction findings from the same session.
- `CLAUDE.md` — "a check that goes green because the thing it measures moved is
  worse than no check"; the arch-list grep is exactly that shape.
