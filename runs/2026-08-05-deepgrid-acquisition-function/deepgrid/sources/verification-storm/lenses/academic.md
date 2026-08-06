# ACADEMIC LENS — Technical rigour of DeepGrid Semi's silicon claims

**Verdict:** The arithmetic is clean and largely uninformative. One headline claim is
provably false as written, the architectural "moat" is textbook K-unrolling benchmarked
against DeepGrid's own prior design, and the numbers needed to judge the part — power,
on-chip SRAM, model size, sustained utilization — appear in no document.

## 1. TOPS derivation holds; area and power do not reconcile

64 × 512 = 32,768 MACs × 600e6 × 2 = **39.3 TOPS INT8**. Exact — and merely MAC count ×
clock, i.e. peak theoretical throughput, which says nothing about achievable performance.

Anchor: TPUv1 is 28nm, 65,536 INT8 MACs at 700 MHz = 92 TOPS. DeepGrid is precisely half
that array at 600/700 the clock (92 × 0.5 × 0.857 = 39.4). Buildable — but TPUv1 was
**331 mm², 40 W**, its matrix unit alone 24% of die ≈ **79 mm² for 65,536 MACs**. Half is
~40 mm² for DeepGrid's MAC array *alone*, before SRAM, LPDDR PHY, lockstep RISC-V, radar
DSP, ISP, HSM, telematics.

- IM's **57.1 mm²**: tight but arguable (~17 mm² for everything else).
- July deck's **~20 mm²** (slide 05; again in the slide 31 cost build): *below the MAC array
  alone*. Not credible.
- Load-bearing: $3.876 die cost is built on a 20 mm² wafer share ($2.180). At 57.1 mm² that
  line is ~2.85× higher and die cost lands nearer **$8–10**. The Corrections Ledger
  retracted "<$3" but never fixed the area input beneath it. **The documents disagree 2.85×
  on the parameter driving the headline cost claim.**

Power is stated **nowhere**. TPUv1 scaling implies ~17 W; a lean array plausibly 8–12 W.
Mobileye's EyeQ5 needs **7nm** for 24 TOPS at 10 W. Claiming 1.6× EyeQ5 throughput on a node
four generations older, in an M.2 module in a truck cabin, with no TDP, W/TOPS, T_j or
AEC-Q100 grade, is the largest unexamined risk in the pack.

## 2. "39.3 TOPS measured on FPGA" is false as stated

July slides 02/04/37 claim a "**measured** 39.3 TOPS INT8 on FPGA." BP-1A names the board:
**Artix-7**. The largest Artix-7 (XC7A200T) has 740 DSP48E1 slices; with standard INT8
dual-MAC packing at ~600 MHz that ceilings near **1.8 TOPS** — **~22× short**.

The June IM is the honest document, labelling 39.3 a *derivation* from ASIC MAC count and
clock. July upgraded a derivation into a measurement. What was measured, per BP-1A's own
evidence class: **40 fps YOLOv11n, 24.25 ms attention head, 0.947 sim-to-silicon**.
Respectable AD0-class results — not 39.3 TOPS.

## 3. The "3D tensor cube" is standard K-unrolling

Consuming K in one cycle rather than eight by "stacking 8 multiply layers" unrolls the
reduction dimension 8×: 8× the multipliers plus a 3-deep adder tree, finishing in 1/8 the
cycles. The IM concedes it — "same answer, different geometry." This is the primitive behind
NVIDIA tensor cores (M×N×K MACC), the TPU MXU, and systolic-array work since Kung &
Leiserson (1979). The comparison is against **SoC1.2, DeepGrid's own prior flat 8×8 unit** —
an internal generational step presented as an industry moat.

"648 MAC inputs" is self-consistent (512 accumulators + 128 operands + 8) but nonstandard,
and the register file's byte capacity is never given. More telling: weight-resident local RF
is classic **weight-stationary** dataflow, whose benefit scales with weight reuse — and
attention K/V tensors grow with sequence length and are *not* reusable weights. The
architecture is weakest precisely on the workload sold as its differentiator.

## 4. The transformer VLA claim is memory-bound; the memory spec self-contradicts

Ridge point: 39.3e12 ÷ 102.4e9 = **384 INT8 ops/byte** to stay compute-bound. Conv backbones
reach that; transformer attention in the token-streaming regime runs ~2 ops/byte. The edge
bottleneck is bandwidth, not compute, and this design is bandwidth-poor relative to its
arithmetic.

Weight streaming settles it: OpenVLA-7B at INT8 is ~7 GB → **68 ms** at 102.4 GB/s with zero
compute, 2× over a 33.3 ms frame. A ~1B-param VLA at INT4 (~500 MB) needs ~4.9 ms of pure
DRAM traffic. "Heavy transformer VLA on-chip" is defensible *only* for aggressively
distilled sub-billion-parameter models — and **no document gives parameter count, precision,
token count or GOP/frame**, making the claim unfalsifiable.

The memory subsystem is not agreed: the IM says **LPDDR5, 102.4 GB/s** (implying 128-bit at
6400 MT/s, or LPDDR5X); July slide 05 says a "**unified LPDDR4 controller**," topping out
near 68 GB/s at 128-bit. A qualified 28nm HPC+ LPDDR5 hard macro is itself an availability
question — LPDDR5 is overwhelmingly implemented at 16nm and below. Name the PHY vendor.

"A YOLO-class edge part cannot host them" is self-refuting: DeepGrid's shipping proof is
YOLOv11n, and BP-1B lists "D-Drive / **YOLO-family INT4** network" as the licensable model
SKU. BP-1A risk #3 says it outright — *"AD2 claim outruns the silicon; today's proof is
AD0-class perception on FPGA."*

## 5. 8.6 ms / 33.3 ms: arithmetically fine, analytically empty

8.6 ÷ 33.3 = 25.8%, so 74.2% free — consistent. But 8.6 ms at 39.3 TOPS implies **338
GOP/frame at 100% MAC utilization**. Real utilization on mixed conv/attention is 20–60%; at
40% the budget affords ~135 GOP, likely under a 6-camera backbone before fusion or a VLA
head. The "~200× utilization gain" implies naive utilization was catastrophic and never
states the post-fix absolute. The measured 24.25 ms attention head is itself 73% of a 33.3 ms
frame, with no FPGA→ASIC scaling factor published to reconcile them. Finally, NPU time is not
the safety-relevant latency: BP-1A correctly pitches **photon-to-brake <100 ms**, of which
8.6 ms is one term beside exposure, ISP, fusion, planning, CAN and actuation.

## 6. ASIL-D is an unfunded aspiration, not a path

"Integer-first" buys bit-reproducibility — useful for diagnostic-coverage arguments, nowhere
near sufficient. ASIL-D requires ≥99% SPFM, ≥90% LFM, ≤10 FIT; per-block FMEDA, quantitative
FTA, dependent-failure analysis; ECC throughout, lockstep with delay and diversity,
LBIST/MBIST with defined latent-fault detection intervals, and fault-injection campaigns
*proving* the claimed coverage; ISO 26262 Part 8 cl.11 qualification of the entire EDA
toolchain; a Part 11 safety manual; an **independent** assessment; plus AEC-Q100 Grade 1/2
and IATF 16949. BP-1B's own sourced note concedes this is "a programme, not a certificate
you buy late." ASIL-D at item level is normally met by ASIL-B(D) decomposition, so "ASIL-D
chip" is imprecise on its face.

A **provisional** application is an unexamined 12-month priority placeholder with no claims
requirement and no enforceable right — "15 provisionals" is an artifact count orthogonal to
functional safety. The **$3.17M NRE phasing carries no functional-safety line item**, and
July's stop-doing list explicitly bans ISO 26262 pre-audit spend and any AEC-Q100 program:
the plan is internally consistent in *not funding* ASIL-D. Separately, **MPW shuttle silicon
cannot be AEC-Q100 qualified or PPAP'd** — shared-reticle tape-out yields characterization
die, not a saleable automotive part, leaving a mask set and qualification lot unbudgeted
between $3.17M and "ASIC swap-in 2027." To DeepGrid's credit, July retracts "mandate-ready
AD2"; the IM's ticked "✓ ASIL-D path" is the un-corrected version of that same claim.

## Missing numbers diligence must demand

Power (TDP, W/TOPS, T_j) · on-chip SRAM capacity (without it no roofline tile size, no
transformer verdict) · VLA model spec (params, precision, tokens, GOP/frame) · absolute
sustained utilization, not a 200× ratio · die area reconciled (57.1 vs 20 mm², cost build
rerun) · memory subsystem reconciled (LPDDR5 vs LPDDR4, bus width, 28nm PHY vendor).
