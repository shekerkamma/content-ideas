# SKU research — internal recall and external comparators

Route followed: local files → GBrain recall → Exa. Firecrawl not needed; Exa returned
vendor-primary pages (NVIDIA developer/product) with the specifications required.

## External: the honest comparator for the A100 compute SKUs

The right comparator is **NVIDIA Jetson Orin** (embedded edge modules), not DRIVE
(vehicle-central compute). Verified via NVIDIA product pages and two independent
2026 deployment benchmarks.

| Module | INT8 TOPS | Power | Cameras | Indicative price |
|---|---|---|---|---|
| Jetson Orin Nano 8GB | 67 | 7–25 W | up to 4 | ~$399 module |
| Jetson Orin NX 8GB | 117 | 10–40 W | up to 4 | ~$649 module |
| Jetson Orin NX 16GB | 157 | 10–40 W | up to 4 | ~$999 module (repriced up from ~$599, Jul 2026) |
| Jetson AGX Orin 64GB | 275 | 15–60 W | up to 6 | ~$1,799–2,999 module |
| Hailo-10H | detection-only, ~8 streams | low | — | ~$130 |

**Module price is not deployed price.** One production benchmark puts a fully deployed
Orin NX 16GB — module plus carrier, enclosure and cooling — at **~$1,800 per node**.
That is the like-for-like figure against a DeepGrid *box*.

### What this means per SKU, at ₹94/USD

| DeepGrid SKU | Price | ≈ USD | Nearest Jetson comparator |
|---|---|---|---|
| A100 1ch M.2 | ₹85 k | ~$904 | Orin Nano 8GB module ~$399 / NX 8GB ~$649 |
| A100 2ch | ₹1.60 L | ~$1,702 | Orin NX 16GB module ~$999 |
| A100 4ch PCIe | ₹3.00 L | ~$3,191 | AGX Orin 64GB module ~$1,799; deployed NX node ~$1,800 |

**Read this as a diligence question, not a selling point.** On published module pricing the
A100 SKUs sit at or above Jetson equivalents that carry more channels and more headroom.
The defensible positions are domestic supply, India-tuned perception, and a box-level
comparison against deployed cost — not a raw price advantage. A per-unit price claim
against a competitor should not be made without a like-for-like deployed configuration.

## External: DRIVE, for context only

DRIVE Orin is 254 INT8 TOPS; DRIVE Thor reaches up to 1,000 INT8 TOPS at 350 W with
ISO 26262 ASIL-D certifiable DriveOS. This is vehicle-central compute at a different power
and price class — relevant as the ceiling of the category, not as a SKU-level competitor.

## Internal recall

Prior DeepGrid runs in this repo carry per-SKU mentions (Seaport 49 files, thermal 43,
AD2 28, A100 27, T100 24). The richest consolidated source is
`runs/2026-08-10-deepgrid-gtm-icp-playbook/RECONCILIATION.md`.

## Claim controls carried into the deck

- No competitor per-unit India price is quoted — none is published for truck ADAS.
- The die-vs-module comparison keeps its like-for-like caveat wherever it appears.
- Jetson figures are cited as vendor-published module prices with the deployed-cost
  distinction stated, never as a head-to-head unit price.
- TOPS is not claimed for SoC2 anywhere in the deck.
