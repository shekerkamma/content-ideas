# Independent Citation Verification

**Verifier role:** independent re-check against primary sources. Not a review of the analysis that produced the ledger.
**Date:** 2026-08-05
**Scope:** E-01, E-02, E-03, E-04, E-05, E-08, E-14 from `outputs/evidence-ledger.csv`
**Method:** read `working/captures/*.json` (You.com Level 2 discovery + Exa fresh extractions), then re-checked each claim
against primary/authoritative sources found independently (Gazette of India text, PIB/Lok Sabha reply, Mobileye press
release, Economic Times / EE Times / The Hindu, funding-round filings coverage, live vendor pricing).

---

## Verdict table

| ID | Claim as stated in ledger | Ledger verdict | **Independent verdict** | Basis |
|---|---|---|---|---|
| E-01 | "GSR 184(E) notified March 2025; mandates AIS-162/184/186/187/188 for M2/M3/N2/N3" | CONFIRMED | **PARTIALLY CONFIRMED — materially misleading** | GSR 184(E) dated 20 Mar 2025 is a **draft** notification issued for 30-day public comment, not a notified mandate. The final rule is **G.S.R. 834(E) dated 11 Nov 2025** (Central Motor Vehicles (Sixth Amendment) Rules, 2025), amended by **G.S.R. 862(E) dated 24 Nov 2025**. The five-standard list is correct. |
| E-02 | "Mandate is phased: new models Apr 2026; existing production models Oct 2026; further systems through Jan 2028" | CONFIRMED | **CONTRADICTED** | Apr 2026 / Oct 2026 are the **superseded draft** dates. Notified dates are ~18 months later: AEBS/ESC/braking **1 Jan 2027 (new) / 1 Oct 2027 (all)**; LDWS, DDAWS, BSIS, MOIS **1 Oct 2027 (new) / 1 Jan 2028 (existing)**. |
| E-03 | "Netrasemi A2000 declared production-ready May 2026; 3 OEM trials live (surveillance + automotive)" | CONFIRMED | **PARTIALLY CONFIRMED** | Date, "production-ready" framing and "three customers in surveillance and automotive" are correctly reported (ET, 28 May 2026). But it is a **company declaration**, and EE Times (4 Jun 2026) describes the same event as silicon bring-up with **engineering samples / EVKs**, possibly needing another MPW cycle before full-mask production. "3 OEM trials" is a slight hardening of ET's "three customers". |
| E-04 | "Netrasemi raised Rs 107 Cr Series A Jul 2025 led by Zoho and Unicorn India Ventures" | CONFIRMED | **CONFIRMED** | Moneycontrol, YourStory, CNBC-TV18, Evertiq, New Indian Express, Entrackr, all 24–26 Jul 2025. ₹107 Cr ≈ $12.5M. Minor precision note: Zoho **led** (₹87 Cr / 13.83%); UIV participated as existing investor (₹16.5 Cr); Maithan Alloys also joined (₹3.45 Cr). Total raised to date ₹125 Cr. |
| E-05 | "A2000 is an edge-AI SoC for video analytics; automotive is one of several target sectors (IoT, healthcare, surveillance) — NOT a purpose-built certified ADAS combo-die" | CONFIRMED | **CONFIRMED — the caveat is fair** | The A2000 is consistently described as a **video-analytics / smart-vision edge SoC** for smart cameras, edge AI boxes, video gateways, drones, robotics, industrial automation. No AIS-162/184/186/187/188 certification, no ASIL/ISO 26262 claim, no automotive-grade qualification claim anywhere. Automotive appears as "selected automotive applications" and "in-cabin monitoring" (EE Times). One sourcing caveat below. |
| E-08 | "Mahindra selected Mobileye for ADAS across six future models" | CONFIRMED | **CONFIRMED** | Mobileye's own press release (BusinessWire via Nasdaq, 10 Feb 2026): SuperVision + Surround selected for "at least six upcoming models", production from 2027, EyeQ6 High, Mobileye as Tier 1. Corroborated by Autocar Professional, just-auto, Automotive World. |
| E-14 | "AIS-140 GPS devices retail Rs 4500-11000 in India" | CONFIRMED | **PARTIALLY CONFIRMED** | The band sits inside the real market spread but is **narrower than any source states** and rests on a **single publisher** (Fleetx blog) in the captures. Independent live listings span roughly **₹2,999–₹13,500** for hardware, higher for school-bus CCTV packages. |

---

## E-01 / E-02 — the load-bearing regulatory claim. This is wrong.

**What the capture actually supports.** The `mandate-dates.json` capture is internally consistent with the ledger only
because every extracted page traces back to the **March 2025 draft**. Two of the five extractions say "draft" explicitly:

- ARAI Technovuus (industry body, 2 Apr 2025): headline is *"Installing ADAS for Automobiles in the M2, M3, and N2 and
  N3 Categories: **Draft rule** by MoRTH"* — "the Ministry has published **draft notification** GSR 184(E) dated March
  20, 2025."
- MotorIndia (21 Apr 2025): *"MoRTH has issued a **draft notification** (G.S.R. 184(E)) **proposing** significant
  amendments … open for public comments for a period of 30 days."*

The ledger's two cited sources are the two weakest pages in the capture and both elide the draft status:
- `electraytech.com` (consultancy marketing page): *"MoRTH notification GSR 184(E) dated March 2025 **mandates** a full
  ADAS suite"* — drops "draft", asserts a mandate.
- `novushitech.com` (fleet-safety vendor blog): asserts *"AIS 184 is one of five standards issued under the **February
  2026 MoRTH notification**"* — **no such February 2026 notification exists.** I could not find one, and no other source
  references it. This is a fabricated or garbled provenance in the source the ledger relies on for E-02.

**What the primary source says.** The Gazette of India text of **G.S.R. 834(E), 11 Nov 2025** — Central Motor Vehicles
(Sixth Amendment) Rules, 2025, published 13 Nov 2025, and expressly the *final* rule made "following consideration of
public objections and suggestions to draft rules published as G.S.R 184(E) dated 20th March, 2025":

| System | Standard | New models | Existing / all models |
|---|---|---|---|
| Braking (non-ABS), Endurance Braking Type-IIA, ABS | IS 11852:2019 | 1 Jan 2027 | 1 Oct 2027 |
| Advanced Emergency Braking | AIS-162 | 1 Jan 2027 | 1 Oct 2027 |
| Vehicle Stability Function (added by G.S.R. 862(E), 24 Nov 2025) | IS 11852:2019 | 1 Jan 2027 | 1 Oct 2027 |
| Lane Departure Warning (rule 98(6)) | AIS-188 | **1 Oct 2027** | **1 Jan 2028** |
| Driver Drowsiness & Attention Warning (new rule 125Q(1)) | AIS-184 | **1 Oct 2027** | **1 Jan 2028** |
| Blind Spot Information (rule 125Q(2)) | AIS-186 | **1 Oct 2027** | **1 Jan 2028** |
| Moving-Off Information (rule 125Q(3)) | AIS-187 | **1 Oct 2027** | **1 Jan 2028** |
| School bus (rule 125C Table I, Sl. 6) | — | 1 Oct 2026 | — |

Independently corroborated by: Times of India (5 Nov 2025, ahead of notification — "From 2027, all new models of buses
& trucks…"); teamleaseregtech summaries of both G.S.R. 834(E) and G.S.R. 862(E); Times Drive (28 Nov 2025); **Fortune
India (13 Feb 2026)** reporting Gadkari's written Lok Sabha reply of 12 Feb 2026, which cites "GSR 834(E) dated November
11, 2025" and states BSIS/MOIS/DDAWS/LDWS compulsory **from January 1, 2028**; cmv360 (13 Feb 2026) same.

**Why this matters for the strategy.** The ledger's dates make the first hard compliance wall land **1 Apr 2026 — i.e.
already past** — with the retrofit wave in Oct 2026. The notified reality is that the **first ADAS-perception wall is
1 Oct 2027** and the DDAWS/BSIS/MOIS/LDWS bulk lands **1 Jan 2028**. That is roughly an 18-month shift in the demand
curve, in the direction that *lengthens* the runway for a silicon entrant but *delays* revenue. Any slide, model, or
narrative built on "the mandate bites in April 2026" is wrong on the record and is the kind of thing an OEM or investor
in this sector will catch immediately.

**Salvageable framing.** "Phased through January 2028" is right as an endpoint, but for the wrong reason: Jan 2028 is
the *existing-model* deadline for the four perception systems, not "further systems layered on top of a 2026 rollout".

**Recommended ledger rewrite.**
- E-01 → "MoRTH notified the ADAS mandate for M2/M3/N2/N3 via G.S.R. 834(E) (11 Nov 2025), finalising draft G.S.R.
  184(E) (20 Mar 2025); covers AIS-162/184/186/187/188 plus IS 11852:2019." Verdict: CONFIRMED (primary source).
- E-02 → "Phased: AEBS/ESC/braking 1 Jan 2027 (new) / 1 Oct 2027 (all); LDWS/DDAWS/BSIS/MOIS 1 Oct 2027 (new) /
  1 Jan 2028 (existing)." Verdict: CONFIRMED (primary source).
- Source column for both should be the Gazette text, not `electraytech.com` / `novushitech.com`.

---

## E-03 — directionally right, framing is company-supplied

Confirmed facts (Economic Times, 28 May 2026, via ET/TechGig/IndiaAIPulse/Rediff/theoutpost; The Hindu 29 May 2026;
Aviation & Defence Universe 29 May 2026):
- A2000 completed **silicon bring-up** and the company declared it production-ready, announced **28 May 2026**.
- **Three customers** in **surveillance and automotive**, per CEO Jyothis Indirabhai to ET.
- TSMC **12nm**; volume production 2027; commercial launch targeted **mid-2027**.

Countervailing detail the ledger does not carry — **EE Times, 4 Jun 2026** (the most technical independent account):
- Netrasemi is "supplying **evaluation kits (EVKs) and engineering samples** to customers rather than selling production
  silicon".
- "Depending on the results, it **may undertake another multi-project wafer cycle** before entering full production."
- Full-mask production targeted mid-2027; first revenue expected end-2027. **Pre-revenue today.**
- A2000 delivers **up to 12 TOPS** — a useful, checkable number the ledger omits and which is directly comparable to the
  company-claimed DGrid Alpha figure in E-10.

Sourcing flag: the ledger cites `niftytrader.in` — a retail stock-market content site whose page reads as AI-generated
aggregation of the ET story (it is also the sole source for E-06). The underlying facts survive independent checking,
but **niftytrader should not be the citation of record**; use ET, The Hindu, or EE Times.

Suggested rewording: "Netrasemi **announced silicon bring-up and declared the A2000 production-ready in May 2026**, with
early evaluations underway with three customers in surveillance and automotive; independent trade press describes the
stage as engineering-sample/EVK distribution, with full-mask production targeted mid-2027 and the company pre-revenue."

---

## E-04 — confirmed

₹107 crore Series A, announced **24 July 2025**. Zoho Corporation led; Unicorn India Ventures (existing investor)
participated. Sources: Moneycontrol (24 Jul 2025), YourStory (24 Jul 2025), CNBC-TV18 (24 Jul 2025), Indian Startup Times
(24 Jul 2025), Evertiq (25 Jul 2025), New Indian Express (26 Jul 2025).

Filing-level detail (Entrackr 28 Aug 2025 / Financial Express 29 Aug 2025, from Tracxn-sourced RoC filings) worth
carrying if the dossier makes a valuation argument:
- Zoho ₹87 Cr ($10.2M) for **13.83%**; UIV ₹16.5 Cr ($1.94M), holds 13.56%; Maithan Alloys ₹3.45 Cr.
- Post-money ≈ **₹630 Cr / $74M**, a 6.6× step-up from ₹95 Cr / $11M at the Dec 2024 pre-Series A.
- Total funding ₹125 Cr / ~$14.6M across four rounds. FY24 operating revenue **₹1.7 Cr**.

Only nit: "led by Zoho **and** Unicorn India Ventures" reads as co-led. Zoho led at 5.3× UIV's cheque. Prefer "led by
Zoho with participation from existing investor Unicorn India Ventures".

---

## E-05 — the caveat is fair, and is the most defensible competitive claim in the set

Every independent description of the A2000 is a **video-analytics / smart-vision edge SoC**:
- netrasemi.com (live capture): "Built for diverse sectors like **surveillance, robotics, smart cities, and Industry
  4.0**." Automotive is not named on the homepage.
- The Hindu (29 May 2026): "targets applications such as **smart surveillance cameras, edge AI boxes and intelligent
  video gateways**."
- EE Times (4 Jun 2026): "initially targets **surveillance, in-cabin monitoring, selected automotive applications, and
  drone-based surveillance**"; cost/power targets "suitable for products such as surveillance cameras."
- Aviation & Defence Universe / Rediff: "surveillance through drones and CCTVs, robotics, intelligent video gateways and
  industrial automation."

Nothing in any source claims AIS-162/184/186/187/188 certification, automotive-grade (AEC-Q100) qualification, ISO 26262
/ ASIL rating, or an ADAS-specific combo-die. Grokipedia adds that Netrasemi is "**actively pursuing market entry into
the automotive IoT sector**, where its chips **can support** applications like ADAS" — forward-looking intent, not a
shipping ADAS product. **The ledger's caveat is accurate and, if anything, understated.**

Sourcing flag: "**healthcare**" as a target sector rests on **Grokipedia alone** ("customers include OEMs in the IoT,
smart sensors, edge computing, healthcare, and automotive sectors"). Grokipedia is an LLM-generated wiki and is not an
acceptable sole source. Either drop "healthcare" or replace the sector list with the ones multiple primary sources name:
**surveillance/smart cameras, robotics, smart cities, industrial automation, drones, IoT**.

---

## E-08 — confirmed against the primary source

Mobileye Global Inc. press release, **10 Feb 2026** (BusinessWire, carried on Nasdaq): SuperVision and Surround ADAS
"have been **selected by Mahindra & Mahindra Ltd. for at least six upcoming models**, with production expected to begin
in 2027." EyeQ6 High SoC; single ECU; Mobileye as **Tier 1 supplier**. SuperVision = 11 cameras + optional radars +
2× EyeQ6H; Surround = 5 cameras + multiple radars + 1× EyeQ6H. Prior collaboration on EyeQ4M and EyeQ6L.

Corroborated by Autocar Professional, just-auto/Yahoo, Automotive World, Times Drive, Indian Autos Blog, Seeking Alpha —
all 10–11 Feb 2026, all tracing to the same release.

**Strategic caveat the dossier should carry:** this is a **passenger-vehicle / SUV** programme (M1), driven by BNCAP and
consumer demand, on **hands-free L2+ SuperVision-class** systems. It is *not* evidence of Mobileye winning the
**M2/M3/N2/N3 commercial-vehicle** sockets that G.S.R. 834(E) regulates. If E-08 is used to argue "the incumbent has
already locked the Indian truck ADAS market", that inference is unsupported by the citation.

---

## E-14 — inside the range, but single-publisher and narrower than reality

What the capture supports (`low-end-pricing.json`, **both** supporting pages are Fleetx's own blog — `blog.fleetx.ai`;
Exa also surfaces the same article at `blog.fleetx.io`):
- Tiered table: basic device-only **₹3,000–6,000**; entry VLTD + SIM **₹5,500–9,000**; + platform **₹7,000–14,000**;
  advanced **₹10,000–18,000**; enterprise **₹12,000–25,000+**.
- By category: 2W/3W ₹3,500–6,000; LCV ₹5,500–9,000; MGV ₹7,000–12,000; **heavy truck/bus ₹9,000–18,000**; school bus
  (CCTV) ₹14,000–25,000+.
- Buyer's-guide headline: "hardware prices broadly run **₹3,500–₹12,000** per device."
- The source labels its own figures "indicative" and is vendor marketing content.

Independent live listings (checked 2026-08-05):
| Vendor | Price |
|---|---|
| Bada Think (device only) | ₹2,999 |
| GPSBULL via IndiaMART (New Delhi) | ₹3,500/pc |
| GeoSafe (Gujarat) | ₹4,200 / ₹6,700 |
| TraceMotor (Delhi) | ₹6,999 / ₹9,500 |
| IndiaMART (Parbatsar, eSIM 4G) | ₹7,800/pc |
| Trackster (Maharashtra) | taxis ₹7,500–9,500; buses/trucks ₹8,500–13,500 |
| WayPointGPS | ₹12,999 |

So the real hardware spread is roughly **₹3,000–₹13,500**, wider on both ends than ₹4,500–11,000, and heavy-truck/bus
units — the category that matters for a truck-ADAS thesis — cluster **₹8,500–18,000**, above the ledger's ceiling.

Two problems with the claim as written: (1) **provenance** — a single vendor blog carried as "captures" plural;
(2) **precision** — ₹4,500–11,000 is not stated verbatim by any source and appears to be an interpolation.

Suggested rewrite: "AIS-140 VLTD hardware retails in India at roughly **₹3,000–₹13,500** per unit depending on tier and
vehicle class; heavy truck/bus units typically **₹8,500–₹18,000**; school-bus packages with mandated CCTV run higher.
3-year TCO per vehicle ₹22,000–₹62,000 once SIM, platform licence and AMC are included."

---

## Cross-cutting source-quality flags

| Source used in ledger | Issue |
|---|---|
| `novushitech.com` (E-02) | Fleet-safety vendor blog. Contains a **verifiably false provenance claim** ("February 2026 MoRTH notification") and repeats the superseded draft timeline. Should not be load-bearing. |
| `electraytech.com` (E-01) | Consultancy marketing page. Describes a draft as a mandate. Should not be load-bearing. |
| `niftytrader.in` (E-03, E-06, and part of E-04) | Retail stock-content site, AI-aggregated from ET. Facts happen to hold up but citation of record should be ET / The Hindu / EE Times. |
| `grokipedia.com` (E-04, E-05) | LLM-generated wiki. Fine as a lead, not as a citation. Sole support for "healthcare" in E-05. |
| `blog.fleetx.ai` (E-14) | Single vendor publisher counted as two sources; self-labelled "indicative". |
| Primary sources **not** used but available | Gazette of India G.S.R. 834(E) / 862(E) text; PIB release 2227148 (12 Feb 2026) on the Lok Sabha reply; Mobileye/BusinessWire release (used indirectly). |

**Pattern:** the run's regulatory evidence was drawn entirely from second-hand vendor/consultancy commentary, none of
which had been reconciled against the gazette. Where the commentary was internally consistent (all five pages recycling
the March 2025 draft) the run read that consistency as corroboration. It was correlated error from a common upstream
source.

---

## Reference URLs

- G.S.R. 834(E) full text — https://gazettetracker.com/g/CG-DL-E-13112025-267610
- G.S.R. 862(E) summary — https://www.teamleaseregtech.com/updates/article/49869/morth-issued-amendments-to-the-central-motor-vehicles-sixth-amendment-/
- Sixth Amendment Rules summary — https://www.teamleaseregtech.com/updates/article/49873/central-motor-vehicles-sixth-amendment-rules-2025/
- Fortune India on Lok Sabha reply (12 Feb 2026) — https://www.fortuneindia.com/business-news/govt-mandates-advanced-safety-technologies-for-heavy-commercial-vehicles-from-2027/130378
- PIB, mandatory safety devices for HCVs (12 Feb 2026) — https://www.pib.gov.in/PressReleaseDetail.aspx?lang=1&PRID=2227148
- TOI (5 Nov 2025) — https://timesofindia.indiatimes.com/india/from-2027-all-new-models-of-buses-trucks-to-have-advanced-driver-alert-systems/articleshow/125112856.cms
- ARAI Technovuus (draft status) — https://technovuus.araiindia.com/blogs/blogDetails/MTQxNg==
- ET on A2000 — https://m.economictimes.com/tech/artificial-intelligence/zoho-backed-netrasemi-launches-its-first-ai-chip-begins-customer-trials/amp_articleshow/131362999.cms
- EE Times on A2000 — https://www.eetimes.com/netrasemi-brings-up-a2000-ai-chip-begins-customer-evaluation-phase/
- The Hindu on A2000 — https://www.thehindu.com/news/cities/Kochi/kerala-start-up-unveils-first-ai-system-on-chip/article71036794.ece
- Moneycontrol on Series A — https://www.moneycontrol.com/artificial-intelligence/semiconductor-startup-netrasemi-raises-rs-107-crore-in-series-a-from-zoho-and-unicorn-india-ventures-article-13320193.html
- Entrackr on cap table/valuation — https://entrackr.com/decoding/semiconductor-startup-netrasemis-valuation-surges-66x-in-series-a-round-9761537
- Mobileye/Mahindra release — https://www.nasdaq.com/press-release/mahindra-selects-mobileyes-supervisiontm-and-surround-adas-next-gen-models-2026-02-10
