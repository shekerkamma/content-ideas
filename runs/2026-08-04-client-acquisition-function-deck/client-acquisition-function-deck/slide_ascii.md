## Slide 1

PRE-SERIES A INVESTOR BRIEFING

Commercializing Vertically Integrated
Edge-AI Silicon for Non-Discretionary
Autonomy Mandates

Bypassing Western merchant silicon to deliver compliant commercial
vehicle safety at a 3x to 7x cost reduction.

INCUBATION

T-Hub Phase 2, Hyderabad

STRATEGIC FOCUS

Demystifying the Ideal Customer Profile (ICP) and executing a phased
Go-To-Market strategy with no existing customer base.

₹55 Cr

PRE-SERIES A ASK

Blended · ≈ $4.79M at ₹94/USD

3–7×

COST REDUCTION

vs. imported ADAS systems

39.3

TOPS INT8

64×512 MAC lattice, 600MHz ×2

₹1,387.95 Cr

FY32 REVENUE (MODEL)

Management projection, unaudited

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

01

## Slide 2

EXECUTIVE SUMMARY

Bridging the Valley of Death — FPGA Prototype to Custom ASIC

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

02

The technical reality

DeepGrid has validated its custom 39.3 TOPS INT8 edge-AI processor architecture on FPGAs — algorithmic efficacy proven, not simulated.

The production bottleneck

FPGA boards are physically too large, run hot, and cost ~₹35,000 (~$420) per unit — uneconomic at any commercial volume.

The silicon destination

Custom 28nm ASICs cut die cost to $3.876 at scale (<$4) and total board-level BOM to ~$30.

The GTM mandate

DeepGrid has no existing commercial automotive customers and cannot wait for 4-year OEM validation cycles. The commercial roadmap is sequenced through dual-use defense wedges (Months 0–6) and aftermarket retrofit mandates (Months 6–18) before OEM line-fit (Months 18–36) — see slides 16–18.

⚠  A correction we are making to our own materials

Earlier versions of this briefing cited a ₹25 Crore (~$3M) Pre-Series A ask. The reconciled Use-of-Funds model raises ₹45 Cr equity (CCPS) + ₹10 Cr CGTMSE-backed debt = ₹55 Cr blended (≈ $4.79M at ₹94/USD). We present the reconciled ask because it is the figure the funded plan — tape-out NRE, EDA licenses, MPW shuttle — actually builds to. See slide 22 for the matching NRE correction.

## Slide 3

THE CORE PROBLEM

The Hardware Squeeze Zone Traps Every Pure-Play AI Stack

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

03

Pure-Play AI Software

Advanced AV/ADAS perception algorithms, no owned silicon

The Squeeze Zone

Dependency on third-party merchant silicon (NVIDIA/Ambarella) drives compute BOM past $6,000

The Result

High hardware costs restrict sales to high-end logistics networks in developed economies

The power bottleneck

Flat GPU and traditional matrix processors suffer memory-bandwidth bottlenecks, leaving extremely low real-world utilization on edge ADAS workloads.

The local data failure

Global computing platforms run vision algorithms trained on structured Western highways — highly unreliable in unstructured, high-entropy Indian and GCC traffic, at right.

## Slide 4

THE SOLUTION

The Custom DGrid Alpha Combo-Die Architecture

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

04

3D Systolic Tensor Cube

A 64×512 MAC lattice, dual-issue (×2) at 600MHz — verified to deliver 39.3 TOPS INT8.

Batch dispatch firmware

Decouples host supervision from execution units — up to 200× higher real-world compute efficiency.

Combo-die integration

Eliminates multi-chip complexity — AI, sensor interfaces, and telematics on one die.

Unmatched cost advantage

Board BOM lands ~$30 at scale — absorbed into hardware, monetized via software (slide 24).

Architecture verifies: 64 × 512 × 600MHz × 2 = 39.3 TOPS INT8 (canonical chip-spec reconciliation) — vs. the source script's uncorroborated "8×8×8, 32,768 MACs," which does not arithmetically produce 39.3 TOPS.

## Slide 5

THE ARCHITECTURE

DeepGrid's Six-Chiplet Integration

Consolidating every mandatory ADAS feature onto single-die silicon

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

05

A100 — ADAS / AI Processor

39.3 TOPS INT8 running perception models (YOLOv11, VLA) at 40 fps.

R100 — Radar DSP

12-bit native ADC for 77GHz radar — eliminates external radar chips.

T100 — Thermal / LiDAR DSP

Dense multi-sensor thermal and LiDAR point-cloud processing for low light.

D100 — Secure Enclave

Dual-core lockstep RISC-V — hardware-level keys, blocks unauthorized overrides.

S100 — SDV Telematics Gateway

Software-Defined Vehicle gateway, integrated AIS-140 real-time tracking.

H100 — Health / Bio-ADC

Drowsiness detection from steering torque and cabin-camera biometrics.

## Slide 6

ICP FRAMEWORK

The 5-Dimensional Diagnostic for Early-Stage Silicon

A common failure mode: targeting broad segments without scoring buying behavior

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

06

1 · Regulatory Compulsion

Is the purchase discretionary, or driven by immediate non-discretionary safety mandates?

2 · Integration & Certification Friction

Engineering hours and homologation cost to design our chip into the customer platform.

3 · Price Elasticity & BOM Limit

Customer's maximum budget tolerance for upfront hardware additions.

4 · Sales Cycle & Time-to-Revenue

Timeline from initial technical engagement to commercial volume purchase orders.

5 · ODD Entropy

Does the target system run in structured spaces, or chaotic, unstructured local roadways?

Why this matters

Segments scoring high across all five dimensions minimize cash-burn during the Pre-Series A runway. See the scored matrix, next.

## Slide 7

ICP FRAMEWORK

Scoring the Three Segments to Minimize Cash-Burn

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

07

DIMENSION

A · TACTICAL DEFENSE

B · AFTERMARKET FLEET

C · OEM LINE-FIT

Primary platforms

UGVs, Port AGVs, Campus AMRs

N2/N3 medium & heavy trucks

New M2/M3 buses, N2/N3 trucks

Regulatory compulsion

Moderate — defense upgrades

Extreme — transport safety deadlines

High — type approvals & certificates

Integration friction

Low–moderate — bypasses public-road standards

Moderate — mounting & power mapping

Extreme — multi-year E/E redesign

Price elasticity

Low — sovereignty over cost

High — needs rapid payback

Moderate–high — BOM pressure

Sales cycle

Short (6–12 mo) — military pilots

Moderate (12–18 mo) — direct-to-fleet

Long (24–48 mo) — engineering pipeline

ODD entropy

High — tactical / seaport terrain

Extreme — unstructured mixed traffic

Moderate–high — highways + urban

The read

Option B (aftermarket fleet retrofit) sequences first: extreme regulatory compulsion plus a 12–18 month sales cycle converts fastest into mandate-driven volume, which is why it anchors Phase 2 of the GTM roadmap (slide 17).

## Slide 8

ICP OPTION A

Tactical Defense & Constrained Robotics

The low-friction, immediate FPGA validation wedge

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

08

Target & pain point

Sovereign UGVs, border surveillance platforms, seaport AGVs. Traditional chips expose these strategic systems to foreign supply-chain threats and remote tracking.

Buying behavior & technical fit

Extremely insensitive to unit chip cost — prioritizes hardware-level cybersecurity and absolute data sovereignty. The D100 lockstep secure RISC-V enclave executes cryptographic tasks in rugged, GPS-denied environments.

The FPGA advantage

Deploys directly on currently validated FPGA boards — bypasses the wait for custom ASICs, securing immediate revenue to cushion engineering burn (₹1 Cr in defense contract revenue already received — slide 16).

## Slide 9

ICP OPTION B

Non-Discretionary Aftermarket Fleet Retrofit

The high-volume, mandate-driven volume engine

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

09

Target & pain point

Medium and heavy goods trucks (N2/N3) owned by private transport and logistics operators. Mandates require immediate ADAS integration, but razor-thin margins block new-vehicle purchases.

Buying behavior & technical fit

Highly cost-sensitive — weighs upgrade cost against non-compliance penalties and rising insurance premiums. DeepGrid's combo-die handles perception, blind-spot monitoring, and drowsiness telemetry on one board.

Commercial fit

A low-cost, homologated retrofit kit priced at ₹2–2.5 Lakh — 3–7× below premium imported systems. Full unit-economics build-up on slide 21.

## Slide 10

ICP OPTION C

OEM Factory Line-Fit Embedding

The long-term platform-locking GTM — the future scale engine

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

10

Target & pain point

Domestic Indian and emerging GCC heavy truck and passenger bus OEMs. Consolidating safety devices across multiple ECUs inflates platform BOM and creates integration bottlenecks.

Buying behavior & technical fit

Highly conservative and slow-moving — will not deal directly with pre-revenue, unproven startups. Consolidating six chiplets on one die cuts physical ECU footprint and simplifies electronics.

DeepGrid's approach

DeepGrid acts as a "Tier-2" chip designer, partnering with established Tier-1 automotive suppliers (Uno Minda, Spark Minda, Bosch India) who own direct OEM relations and warranties.

## Slide 11

COMPETITIVE LANDSCAPE

Strategic Playbooks of Freight Autonomy Giants

Real fleets, four different bets on where autonomy pays first

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

11

Aurora — the heavy-OEM playbook

Long-haul Class-8 on dual NVIDIA DRIVE Thor ($6,000+ BOM). Continental Tier-1 partnership; targeting 2025 pilot scale.

Kodiak Robotics — the dual-use playbook

Highway freight + DoD defense contracts on Ambarella CV3-AD685. Active US commercial freight trials.

Gatik — the constrained-route playbook

Fixed middle-mile routes on NVIDIA DRIVE AGX Orin + Isuzu box trucks. Driverless ops live for Walmart, Kroger.

DeepWay — the vertical-integration playbook

China domestic fleets on high-compute NPU + Baidu Apollo co-design. "Xingtu" L4 electric trucks in commercial ops.

The lesson for DeepGrid

Every credible playbook picks one lane — constrained ODD (Gatik), dual-use defense revenue (Kodiak — DeepGrid's Phase 1), heavy-OEM capital intensity (Aurora — DeepGrid's Phase 3), or full vertical integration (DeepWay). No incumbent runs all three phases at DeepGrid's ~$30 BOM.

## Slide 12

COMPETITIVE LANDSCAPE

Global Semiconductor & Dependency Matrix

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

12

METRIC

AURORA

KODIAK

GATIK

DEEPWAY

DEEPGRID SEMI

Primary markets

US Highway

US & Defense

US & Canada B2B

China Freight

India / GCC

Silicon partner

NVIDIA

Ambarella

NVIDIA / Intel

Baidu ecosystem

TSMC (28nm, in-house)

Compute model

Merchant silicon

Specialized merchant

Off-the-shelf (COTS)

Proprietary co-design

Custom in-house ASIC

Core processor

DRIVE Thor

CV3-AD685 (5nm)

Heterogeneous PC

High-compute NPU

DGrid Alpha combo-die

Compute capacity

~2,000 TOPS

5nm vector logic

Varies with GPUs

>500 TOPS

39.3 TOPS INT8

Chip dependency

Extreme

High

High

Moderate–high

Zero third-party dependency

Compute BOM cost

$6,000+ / board

High premium

Moderate–high

High platform cost

~$30 / board

The read

Every other player is dependent on third-party merchant silicon — DeepGrid is the only one with zero chip dependency, at roughly 1/200th the compute BOM of the US highway incumbents.

## Slide 13

COMPETITIVE LANDSCAPE

Mapping the Domestic Semiconductor Wave

As supplied in DeepGrid research materials — not independently re-verified in this pass

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

13

Netrasemi

A2000 AI SoC on TSMC 12nm. Paid evaluation trials with 3 OEMs (surveillance + automotive). Raised ₹125 Cr (incl. ₹107 Cr Series A from Zoho, Jul 2025). Targeting mid-2027 commercial launch.

Mindgrove Technologies

700MHz secure, low-power RISC-V MCU on TSMC 28nm. MoU with Bosch (Jun 2025); deal with Pinetics. Raised $10.3M total (incl. $8M Series A led by Peak XV, Dec 2024).

Agnit Semiconductors

Vertically integrated GaN devices on sapphire/SiC. Live defense radar pilots; targeting 100,000 GaN units in 24 months. $7.47M total funding (incl. $2.6M seed extension, Shastra VC, Mar 2026).

The read

India's semiconductor wave is real but young — the most advanced (Netrasemi) targets mid-2027 launch. DeepGrid's FPGA-validated architecture and live defense revenue put it ahead on commercial proof, not just design.

## Slide 14

COMPETITIVE LANDSCAPE

Mapping Software-First Autonomy Competitors

As supplied in DeepGrid research materials — not independently re-verified in this pass

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

14

Minus Zero

Vision-first stack (Nature Inspired AI, True Vision Autonomy) — eliminates LiDAR and heavy compute. L4 zPod prototype; Ashok Leyland partnership for port/campus autonomy. $1.7M seed raised.

Swaayatt Robots

L5 navigation via unsupervised/RL algorithms mapping unstructured roads without HD maps. Demonstrated map-free, LiDAR-free driving at speed. $4M post-seed (Jun 2024, $151M valuation).

RoshAI

Hardware-agnostic software for control, navigation, localization, fleet tracking. Active in heavy industrial port/mining deployments. $1M seed (Aug 2024) + subsequent seed rounds (Apr 2026).

Why none of these compete on DeepGrid's axis

All three are hardware-agnostic by design — they run on third-party merchant silicon (typically NVIDIA-class) and inherit its BOM. DeepGrid competes on owned silicon economics, not perception-algorithm quality.

## Slide 15

COMPETITIVE POSITIONING

How Vertical Integration Beats Software-Only and Microcontroller Rivals

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

15

Software-first competitors are squeezed

Minus Zero, Swaayatt, RoshAI write excellent algorithms but run on expensive merchant silicon (NVIDIA-class) — hardware cost stays high for the end customer.

Microcontroller players lack compute

Mindgrove designs low-power MCUs for IoT but has no path to the 39.3 TOPS deep-learning acceleration real-time camera-radar fusion needs.

Surveillance/server players lack integration

Netrasemi targets surveillance and edge servers — no 77GHz radar (R100) or driver-biometrics (H100) path for vehicle safety.

DeepGrid's edge

The only Indian startup designing a vertically integrated, single-die ADAS combo-die purpose-built for upcoming commercial-vehicle mandates at a disruptive price point.

## Slide 16

GTM ROADMAP · PHASE 1

The Tactical & Off-Highway Wedge

Months 0–6 — FPGA deployments and immediate cash flow

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

16

PHASE 1

Tactical Wedge

Months 0–6

PHASE 2

Aftermarket Retrofit

Months 6–18

PHASE 3

OEM & Tier-1

Months 18–36

Direct FPGA field deployments

Deploy fully functional FPGA boards into enclosed port facilities and industrial campuses — bypasses slow public-road regulation to refine radar-vision fusion in real time.

Tactical defense positioning

Bid on sovereign military research contracts, highlighting the D100 RISC-V lockstep secure enclave that isolates critical software execution.

Non-dilutive cash flow

The dual-use tactical defense strategy has already generated ₹1 Cr in contract revenue — extending runway through the Pre-Series A phase.

De-risking the pitch

Real-world performance data from port and tactical deployments is the proof-of-concept evidence that closes the Pre-Series A round.

## Slide 17

GTM ROADMAP · PHASE 2

Regulatory Aftermarket Volume

Months 6–18 — launching the custom 28nm ASIC in the aftermarket sector

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

17

PHASE 1

Tactical Wedge

Months 0–6

PHASE 2

Aftermarket Retrofit

Months 6–18

PHASE 3

OEM & Tier-1

Months 18–36

Close the Pre-Series A

Secure ₹55 Cr blended (₹45 Cr equity CCPS + ₹10 Cr CGTMSE) to fund the transition to custom silicon.

Leverage government subsidies

Apply to MeitY's Design Linked Incentive scheme to offset chip design cost and secure sales-linked incentives (slide 25).

MPW tape-out

Execute a cost-efficient tape-out via TSMC's 28nm HPC+ MPW program, bypassing a dedicated mask set.

High-volume aftermarket launch

Package the ASIC into a complete retrofit kit; sell direct-to-fleet to commercial trucks facing upcoming safety mandates.

The disruptive price wedge

Price the kit at ₹2–2.5 Lakh — undercutting imported systems (company-stated ₹5–18L import bands) by 3–7×.

## Slide 18

GTM ROADMAP · PHASE 3

OEM & Tier-1 Integration

Months 18–36 — scalable Tier-1 partnerships and factory line-fit

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

18

PHASE 1

Tactical Wedge

Months 0–6

PHASE 2

Aftermarket Retrofit

Months 6–18

PHASE 3

OEM & Tier-1

Months 18–36

Tier-1 strategic alliances

Partner with domestic Tier-1 suppliers (Uno Minda, Spark Minda, Bosch India) — DeepGrid licenses the ASIC and software; the Tier-1 manages manufacturing and warranty liability.

Sovereign OEM line-fit wins

Direct-to-fleet retrofit data becomes the pitch for a cost-saving, factory-installed standard component on new vehicle models.

High-margin SaaS activation

Shift from hardware-only sales to recurring subscriptions for fleet tracking, collision alerts, and driver monitoring (slide 24).

The sovereign data moat

Every kilometer driven by fleet retrofits generates localized training data — reinforcing accuracy and raising switching costs for operators.

## Slide 19

REGULATORY MANDATE

The Non-Discretionary Compliance Engine in India

Mapping mandatory MoRTH and AIS deadlines to DeepGrid chiplets

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

19

MANDATE

CORE ADAS APPLICATION

CHIPLET MAPPING

AIS-184

Driver Attention Warning

H100 Bio-ADC fatigue core

AIS-186

Blind Spot Detection

R100 Radar DSP core

AIS-187

Moving-Off Detection

R100 Radar + T100 Vision DSP

AIS-188

Lane Departure Warning

A100 Edge AI vision core

AIS-162

Advanced Emergency Brake

A100 & R100 real-time logic

AIS-189/190

Secure software & hardware update mgmt.

D100 RISC-V lockstep secure enclave

⚠  A correction we are making to our own materials

Earlier DeepGrid materials cited GSR 184(E) as live from 1 April 2026 (new vehicles) / 1 October 2026 (existing fleet) — that date comes from a March-2025 draft notification. The operative dates, per the ministerial reply, are 1 October 2027 (AEBS + ESC) and 1 January 2028 (all four functions). We present the operative dates because the tape-out clock still fits inside them, and because an investor will check MoRTH's gazette directly.

## Slide 20

REGULATORY MANDATE

GCC Regional Compliance Engine — Saudi TGA & WASL

Natively meeting SASO and WASL fleet-tracking requirements

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

20

The Saudi WASL mandate & penalties

Saudi Arabia's Transport General Authority requires all commercial heavy-goods trucks, buses, and delivery vehicles to sync live location and weight metrics to the WASL platform. Unlinked vehicles face operational suspension and heavy municipal fines.

Integrated tracking & the S100 solution

Heavy trucks must run a GPS tracker paired with on-board weight sensors (>90% accuracy). Integrated WASL protocols and raw sensor interfaces on-chip let fleets run this sync directly on DeepGrid hardware — no secondary tracker unit.

## Slide 21

FINANCIAL MODEL

Hardware Unit Economics

High production yields and low manufacturing cost on TSMC 28nm

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

21

$3.876

DIE COST AT 1M CHIPS

<$4 · Muse/GSME quote, 28nm HPC+

~$30

COMPLETE BOARD BOM

ASIC + sensors + enclosure

12.9×

COST ADVANTAGE

vs. Mobileye $50 ASP (sourced)

96.7%

PREDICTED YIELD

IM figure — see workbook flag below

RETROFIT KIT VARIABLE COST BUILD-UP ($200 TOTAL)

ASIC Board  ~$30

Radar Sensor  ~$100

Visual Cameras  ~$50

Enclosure  ~$20

At a ₹2–2.5L (~$2,400–$3,000) retail ASP, this $200 variable cost implies a computed unit gross margin of roughly 92–93% at scale. We show it as a range because it is not yet reconciled to the company-level P&L model (slide 23).

⚠  A correction we are making to our own materials

Earlier materials stated die cost as "~$3 at scale." The canonical reconciliation (Muse/GSME quote) puts it at $3.876 — under $4, not under $3. We also do not repeat the source deck's "84% gross margin" figure; it is not derivable from the $200 kit-cost build-up above at the stated ASP, so we show the math instead of asserting a number.

Source: DeepGrid Business Plan v2 workbook + reviewed Pre-Series A Analysis (canonical reconciliation, 2026-07-19). Yield discrepancy flag: workbook models 94.5% (Murphy 0.1/cm²) vs. 96.7% in the IM — immaterial to die cost, both figures should not be printed together.

## Slide 22

FINANCIAL MODEL

Cost Curves & Tape-Out Break-Even

Surgical application of NRE capital

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

22

$3.17M

TAPE-OUT NRE

MPW phasing: A100+R100 MPW, full-die MPW, backend→GDSII, mask, IP, PHY

~174,908

BREAK-EVEN VOLUME

Chips, at $18.12 blended margin

FY2032

BREAK-EVEN CROSSES

Per reviewed analysis recomputation

⚠  A correction we are making to our own materials

Earlier materials showed an $8M NRE break-even of "just 3,636 retrofitted trucks" — using Break-Even = $8,000,000 ÷ ($2,400 ASP − $200 unit cost). That $8M NRE figure and the resulting 3,636-unit break-even were already investigated and superseded once, in our internal financial reconciliation (2026-07-19): the actual tape-out NRE build is $3.17M (at-risk pre-validation exposure: $370K, 11.7%), and the correctly recomputed break-even — at $18.12 blended per-unit margin, not the retail-vs-kit-cost spread alone — is ~174,908 chips, crossing profitability in FY2032. We are not repeating the earlier, smaller number.

NRE PHASING (CANONICAL)

$69K A100 MPW + $69K R100 MPW + $232K full-die MPW  →  $1.0M backend→GDSII (post-MPW)  +  $1.0M mask  +  $300K PrimeSoC IP  +  $500K Terminus PHY  =  $3.17M

Source: Tapeout Expenses sheet, DeepGrid Business Plan v2 workbook (added 2026-07-19). This volume is a fraction of a percent of active commercial vehicles in India — the mandate-driven TAM is not the constraint; capital-efficient NRE phasing is.

## Slide 23

FINANCIAL MODEL

6-Year Revenue & Margin Trajectory

Management projection, unaudited — model output, not observed data

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

23

₹6 Cr

FY27

₹41.2 Cr

FY28

₹144.7 Cr

FY29

₹351.4 Cr

FY30

₹731.5 Cr

FY31

₹1,388.0 Cr

FY32

88%

FY32 GM

from 53%

39%

FY32 EBITDA

₹536.6 Cr

Net income turns positive FY2029; FY32 net income ₹381.37 Cr.

Source: DeepGrid Business Plan v2 P&L (canonical, 7 independent confirmations). Replaces the source script's unreconciled Year-1/2/3 USD ARR table, which does not tie to this P&L model. All projections are management, unaudited.

## Slide 24

MONETIZATION

Recurring Software Monetization — SaaS & the Sovereign Data Moat

Turning low-cost hardware into long-term subscription revenue

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

24

Base Compliance Tier

₹10,000 / year per vehicle. Basic safety metrics, automated drowsiness warning logs, automated compliance sync with Indian MoRTH and Saudi WASL portals.

Advanced Autonomy Tier

₹15,000 / year per vehicle. Advanced driver-fatigue tracking via the H100 bio-ADC and edge-based Vision-Language-Action video analytics.

Premium Autonomy Tier

₹25,000 / year per vehicle. Active Level 2+ collision avoidance, lane-keeping assist, adaptive speed compliance via secure OTA updates.

The data moat

Every kilometer driven acts as a Trojan Horse — generating localized training data that creates switching costs no general-purpose competitor can replicate without the same fleet footprint.

## Slide 25

CAPITAL EFFICIENCY

Leveraging Sovereign Subsidies

Maximizing India Semiconductor Mission outlays to reduce capital burn

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

25

Product Design Linked Incentive (P-DLI)

Up to 50% reimbursement of eligible chip design expenditure, capped at ₹15 Cr per application.

Deployment Linked Incentive

Financial incentives of 4–6% of net sales turnover over five years, capped at ₹30 Cr.

Shared EDA grid support

Access to the ChipIN Centre's centralized EDA platform — saves hundreds of thousands in licensing.

The VC multiplier

The ₹55 Cr blended round + these incentives fund a well-capitalized path to first-silicon.

⚠  A correction we are making to our own materials

Consistent with slide 2 and slide 17: the raise this subsidy stack is sized against is the reconciled ₹55 Cr blended figure, not the ₹25 Cr cited in earlier materials.

## Slide 26

THE CLOSE

The Defensible Pre-Series A Investment Thesis

Pillar 1 — eliminating the hardware squeeze zone

Owning the chip, sensor interfaces, and software secures high hardware margins plus high-margin recurring SaaS revenue.

Pillar 2 — de-risked technical validation

Not a concept-stage bet: the tensor-cube architecture is validated on FPGAs, generating ₹1 Cr in tactical defense contract revenue already.

Pillar 3 — non-discretionary mandate capture

MoRTH GSR 184(E) (operative Oct 2027 / Jan 2028) and GCC WASL mandates provide a guaranteed, price-sensitive TAM.

Pillar 4 — capital-efficient engineering

TSMC's mature 28nm node plus India's DLI subsidies mean the ₹55 Cr blended ask funds the journey to first-silicon and market launch.

₹55 Cr

THE ASK

Blended equity + CGTMSE debt

₹2.48 Cr

CAPITAL TO DATE

≈ $264k · angel + ARAI + HDFC

18.07%

OFFERED STAKE

⇒ implied ~₹249 Cr post (derivation)

FY2029

PROFITABLE FROM

Net income positive, model output

Join us in delivering sovereign edge-autonomy to the next billion vehicles.

DEEPGRID SEMI  ·  PRE-SERIES A INVESTOR BRIEFING  ·  JULY 2026

26
