# Peer benchmark: how semiconductor companies structure "Resources" (docs, videos, library) for investors, partners and design engineers

Research date: 2 Nov 2026. Primary sources are preferred; pages that could not be reached are listed under Gaps. Pages that could not be fetched: Andes `/en/resources/` and `/en/resources/documentation/` (crawl not found), axelera.ai/resources (crawl not found), support.axelera.ai (fetch error), the TI Hercules safety landing page, and an NXP SafeAssure training page. Where a page failed, I fell back to other primary pages from the same company.

Context checked for comparison (DeepGrid v11, fetched 2 Nov 2026):
- The landing page reads "Technical documents, decks and films" and offers three role-based entry points: the portfolio for product scope, the evidence register for maturity, and detailed documents for integration. — [DeepGrid Resources](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- The docs page says "Nine product specifications open to read; 21 more documents on request." Each document has a page count and an in-site reader, and the PDF is called "the edition of record." It labels superseded material: the whitepaper v3 is "superseded in part by the October SKU Blueprint" and carries a warning not to cite one orders figure. Datasheets are marked "preliminary." Two leftover template lines are inconsistent with an MCU portfolio: "Detailed specifications and technical documentation for all our AI accelerators" under Product Datasheets, and "ADAS Benchmarks" under Performance Benchmarks. — [DeepGrid Docs](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs/)
- The videos page lists ten part films, each 1:04 to 1:30 with a transcript, captioned "Animations illustrate; they are not simulations. Pre-silicon; every figure is a design target." Other groups on the same page have weaker framing:
  - an "Autonomous Driving" group titled "Live ADAS Demo on Hyderabad City Roads … with the DG-A100" (19:12);
  - nuScenes, Waymo and CARLA clips of 0:09 to 0:20;
  - a silicon group introduced as "Go inside our AI accelerators."

  These groups do not say what hardware ran each demo (GPU, FPGA or DeepGrid silicon), even though the parts are pre-silicon. — [DeepGrid Videos](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/videos/)

## Q1. How do 6–10 relevant peers organize resources (categories, filters, gating, public vs NDA)?

### Takeaway
Peers fall into three patterns.
- **Large MCU vendors (TI, NXP, Infineon, ST)** run per-product document tables split by document type. Datasheets, reference manuals, app notes and eval-board guides are public. Safety analysis and FMEDA material sits behind account plus NDA tiers.
- **RISC-V IP and AI-chip scale-ups (SiFive, Codasip, Axelera, Tenstorrent)** split marketing "resources" (blogs, papers, webinars, press) from an engineering docs portal organized by task: Get started, guides, reference.
- **Early-stage Indian fabless startups (Mindgrove, InCore, Netrasemi)** publish almost no technical library. They use product cards plus "contact us" or form-gated brochures.

### Cited Findings
**SiFive (RISC-V IP + boards)**
- The "Resources" page is really "Webinars & Videos": a Webinars section (e.g. "LLM Optimization and Deployment on SiFive Intelligence") and a dated Videos list ("SiFive Product Update", "RISC-V Solutions for Automotive"). — [SiFive Resources](https://www.sifive.com/resources)
- A separate Documentation page groups content by product family. Each family has a Family Brief plus per-core Product Briefs (Automotive E6-A/E7-A/S7-A, Essential, Intelligence Gen 1/Gen 2, Performance), offered in EN/ZH. There is an "Additional Resources" block of case studies (e.g. "Intelligence X280 Google Data Center Case Study") and a "Chips" block with full datasheets and manuals for its own silicon (Freedom E310/U540/U740). The HiFive Premier P550 board has a getting-started guide in 12 languages, schematics, BOMs, 3D models and a software reference manual. — [SiFive Documentation](https://www.sifive.com/documentation)
- The pattern for IP is that only briefs are public; detailed core manuals are not listed. Its own chips and boards ship full public datasheets, manuals and schematics. (Inference from the page contents above.)

**Codasip (RISC-V IP)**
- The Resources page is a content hub with three streams: Blog (tagged RISC-V, Case Study, Codasip Studio, Industry), Press releases, and "Technical papers and case studies" (posters, papers). Every item is dated. — [Codasip Resources](https://codasip.com/resources/)
- The stream mixes safety-relevant evidence, e.g. "Codasip RISC-V processors certified up to ASIL-D" (press release, 1 Oct 2025) and an ASIL motor-control case study with IAR. It also openly lists corporate events such as "Codasip board initiates an expedited process to sell the company" (1 Jul 2025). — [Codasip Resources](https://codasip.com/resources/)

**Andes Technology (RISC-V IP, ISO 26262)**
- The N25F-SE product page is the public safety-evidence unit. It covers ISO 26262:2018 parts 2, 4, 5, 8 and 9 for ASIL B, "Independent assessment and certification by SGS-TÜV Saar GmbH", a linked compliance certificate, a block diagram, a product brief, and dev tools (AndeSight IDE, ICE). It mentions DFMEA and FMEDA as supported deliverables but does not publish them. — [Andes N25F-SE](https://www.andestech.com/en/products-solutions/andescore-processors/riscv-n25f-se/)
- The Andes resources and documentation pages could not be fetched (see Gaps).

**Tenstorrent (AI silicon + open software)**
- docs.tenstorrent.com is a role- and task-led portal. It offers "No hardware yet? Get access to Tenstorrent silicon right in your browser" (Cloud Console), an AI "Ask anything" search (⌘K), "Get Started", "Learn by Building", and "Popular Destinations". It then splits Software (TT-Forge, TT-NN, TT-Metalium…) from Hardware (Blackhole, Wormhole products). — [Tenstorrent Docs](https://docs.tenstorrent.com/)

**Axelera AI (edge AI silicon, scale-up)**
- docs.axelera.ai is a "Documentation Portal" with Voyager SDK, Getting Started, Model Zoo, and Hardware Documentation ("Product datasheets, user guides, and technical references for Metis hardware"). — [Axelera Docs Portal](https://docs.axelera.ai/)
- The SDK docs explicitly follow a Diátaxis-like split: "Getting Started … User Guides … Tutorials … Model Zoo … Reference … Glossary", each with a one-line "start here if…" description. — [Voyager SDK](https://docs.axelera.ai/sdk/)
- The SDK GitHub points to a separate "Customer Portal" for technical documents and guides, and to a Community site. The SDK is under a EULA. — [voyager-sdk GitHub](https://github.com/axelera-ai-hub/voyager-sdk)

**Ambiq (ultra-low-power MCU, recently public)**
- The Resources page is one flat, reverse-chronological document list: product briefs, datasheets, errata, security advisories, app notes, compliance certificates (REACH, Prop 65), and translated briefs. Each item shows a date and file size. It links out to a "Content Portal", a "Glossary", a "Video Library" and "Whitepapers". — [Ambiq Resources](https://ambiq.com/resources/)
- Ambiq publishes silicon errata and security advisories publicly, e.g. "Apollo4 Plus Silicon Errata List", "Ambiq Security Advisory … February 23, 2026". — [Ambiq Resources](https://ambiq.com/resources/)

**Infineon AURIX (safety MCU leader)**
- The product page is organized by sub-family (TC32x…TC39x) with ASIL-D lockstep and HSM claims. — [Infineon AURIX TC3x](https://www.infineon.com/products/microcontroller/32-bit-tricore/aurix-tc3xx)
- Gating has two tiers:
  - **Public:** data sheet, delta sheets, target specs, user manuals, iLLDs, BSDL files, TriBoard manuals, app notes and training for TC2xx/TC3xx.
  - **NDA via myICP:** HSM specs, errata, "other safety documentation", and *all* TC4x documentation. Access needs a myInfineon account and then promotion to an NDA user via AURIX@infineon.com. — [Infineon myICP](https://www.infineon.com/promo/MyICP-platform-for-Microcontroller)
- An Infineon community moderator stated, "the Safety Manual is not available to the public." — [Infineon Community](https://community.infineon.com/t5/AURIX/TC3XX-Safety-Manual/td-p/754606)
- TC4xx app notes are listed publicly as an "On request" table (title, description, version/date, access link). Visitors can see what exists but need promotion to read it. — [Infineon TC4xx AN (On request)](https://documentation.infineon.com/aurixtc4xx/docs/znw1761050437240)

**NXP S32K3 (safety MCU)**
- The product page shows a public Reference Manual (Rev 12, Nov 2025, 55 MB, "Account Required"), a "How to request the safety documentation" PDF, and a software tier table (Reference / Standard / Premium software). Safety software (SAF, SCST) is "Premium". The "SafeAssure NDA group" is "Available through NXP Secure Content". — [NXP S32K3](https://www.nxp.com/products/S32K3)
- The safety manual, standardized SEooC FMEDAs, analysis reports, assessment reports and PPAPs are downloadable only from the SafeAssure NDA group or Secure Files. — [NXP blog](https://www.nxp.com/company/about-nxp/smarter-world-blog/BL-SAFETY-REQUIREMENTS-WITH-S32K3-MCUS); [NXP community](https://community.nxp.com/t5/S32K/This-is-a-request-for-FMEDA-data-related-to-S32K314NHT0VPBS-and/td-p/1628109)

**TI Hercules / TMS570 (safety MCU)**
- Safety manuals are public PDFs (e.g. SPNU620, SPNU511, SPNU540). They explicitly point to a Safety Analysis Report Summary, a Detailed Safety Analysis Report with the FMEDA, and a Safety Report with assessment results. — [TI SPNU620](https://www.ti.com/lit/pdf/spnu620); [TI SPNU540A](https://www.ti.com/lit/fs/spnu540a/spnu540a.pdf)
- TI's Hercules documentation says: "For any questions related to FMEDA tools, Safety Analysis reports and collateral covered under NDA, please access SafeTI Private." — [TI Hercules docs](https://software-dl.ti.com/hercules/hercules_docs/latest/hercules/SafeTIDiagLib/SafeTIDiagLib.html)
- TI product pages carry a "Top documentation" table (data sheet, silicon errata by revision, etc.). — [TI TMS570LS0232](https://www.ti.com/product/TMS570LS0232)

**STMicroelectronics Stellar (automotive MCU)**
- The Documentation tab is grouped by doc type: User Manual (eval/discovery boards, motor control toolkit), Technical Notes (IO definition, offline self-test, register protection), and Data Briefs per line. — [ST Stellar Documentation](https://www.st.com/en/microcontrollers-microprocessors/stellar-32-bit-automotive-mcus/documentation.html)
- The software page lists a "Safety complex device driver" data brief publicly. — [ST Stellar software docs](https://www.st.com/en/embedded-software/stellar-embedded-software/documentation.html)

**Early-stage / open-silicon / Indian startups**
- **Mindgrove** (Indian fabless): the homepage has product cards ("Secure IoT – 28nm, 700 MHz", "Vision SoC", "Edge Compute – Coming Soon!") and a contact form. No public resources library was found on the homepage. — [Mindgrove](https://www.mindgrovetech.in/)
- **InCore Semiconductors** (Indian RISC-V IP): the homepage offers brochures only via "Fill up the form to download the brochure", repeated per product. Credibility comes from customer quotes (NXP EVP, SK Hynix VP) rather than documents. — [InCore](https://incoresemi.com/)
- **Netrasemi** (Indian edge-AI SoC): the homepage lists SoCs, Chiplet & UCIe, "Netra Smart Edge Studio" and "System on Module & RDK". No document library is visible. — [Netrasemi](https://netrasemi.com/)
- **ChipFoundry** (successor ecosystem to Efabless chipIgnite on sky130):
  - It publicly shows "Shuttle Status for CI2612 : Open for Submission" and "Check out metrics from previous shuttles."
  - It prices chipIgnite at "$14,950 per tapeout". The offer includes a pre-built RISC-V SoC, "100 QFN-packaged parts or Bare Die", a dev board, and an open-source RTL-to-GDSII flow. — [ChipFoundry](https://chipfoundry.io/)

### Inferences
- **Taxonomy.** The common top-level split among credible peers is (a) a marketing/news hub (blog, press, webinars, case studies) and (b) a documentation library or portal by product and doc type. A gated tier sits on top for NDA material. DeepGrid has merged these into one "Resources" section with docs, videos and a reader. That is reasonable at its stage, but its docs page still mixes engineering specs with strategy and geopolitics papers (Three-Factory Sovereign Silicon, whitepaper). Peers keep those in "papers/whitepapers" or the news hub.
- **Filters.** The big vendors filter by product, then doc type (datasheet / reference manual / errata / app note / user guide / safety). Hubs (Codasip, Ambiq) use topic tags and dates. Portals (Tenstorrent, Axelera) use task stages. None of the startups fetched offer filters, because they have too few items to need them.
- **"Listed but gated" is a strong pattern.** Infineon's public "On request" table and DeepGrid's "21 more documents, shared on request" are the same idea. The difference is that Infineon shows version and date per gated title and a formal access path.
- **Where DeepGrid stands among Indian peers.** DeepGrid already publishes far more technical depth than Mindgrove, InCore or Netrasemi, which publish almost nothing. The investor-facing risk is not too little content. It is labeling and consistency: leftover "AI accelerators" and "ADAS" copy, and demo videos with no stated hardware.

### Gaps
- The Andes resources and documentation hub, the axelera.ai/resources marketing page, and support.axelera.ai could not be fetched, so their top-level categories and gating are unverified.
- I did not verify Mindgrove, InCore or Netrasemi subpages (e.g. a /resources or /blog path). The finding is limited to their homepages.
- I did not fetch the ST Stellar safety-manual gating page. Whether ST's Stellar safety manual/FMEDA is NDA-only is unverified, though the industry pattern suggests it.

## Q2. Standard safety-MCU document set, and what pre-silicon/pre-production companies publish vs hold back

### Takeaway
The standard set has three parts:
- **Functional docs (usually public):** product brief, datasheet, reference/technical manual, silicon errata, app notes, eval-board user guide, SDK/drivers.
- **Safety manual:** public at TI, NDA at Infineon and NXP.
- **Safety package (almost always NDA):** FMEDA (often as a configurable tool), safety analysis summary and detailed reports, safety case, assessment certificate or report.

Pre-silicon vendors publish briefs and "preliminary" or "product preview" datasheets. Pre-silicon app notes are labeled as based on simulation data, and the quantitative safety evidence is held back.

### Cited Findings
- **Infineon TC3xx "safety package" (NDA)** contains:
  - a safety case report (ISO 26262-2 cl. 6.5.4);
  - a safety manual (assumptions of use, safety mechanisms);
  - an FMEDA template ("Calculation tool to compute customized ISO 26262 random-fault-related metrics");
  - a safety analysis summary report;
  - safety package release notes.

  It is "made available to customers under non-disclosure agreement for both ISO 26262 compliance and IEC 61508." — [Infineon AN0001 FuSa in a nutshell](https://documentation.infineon.com/aurixtc3xx/docs/owq1745576218449)
- **TI Hercules set** is a public Safety Manual, plus a Safety Analysis Report Summary (failure rates, assumptions, chip-level metrics), a Detailed Safety Analysis Report (fault model plus a sub-module FMEDA), and a Safety Report (assessment results). — [TI SPNU511](https://www.ti.com/lit/pdf/spnu511)
- TI marks some of these "under NDA". — [TI Hercules docs](https://software-dl.ti.com/hercules/hercules_docs/latest/hercules/SafeTIDiagLib/SafeTIDiagLib.html); [TI/TÜV seminar](https://www.ti.com/cn/lit/ml/zhcp003/zhcp003.pdf)
- **NXP S32K3 set:**
  - public data sheet and reference manual (account required);
  - application notes such as AN14068 "S32K3/S32K1 + FS23 hardware and safety application guide" (public HTML);
  - NDA material: safety manual, SEooC standardized FMEDA, safety analysis report, assessment/confirmation reports, PPAPs;
  - safety software in a premium tier (SAF, SCST).

  Sources: [NXP S32K3](https://www.nxp.com/products/S32K3); [AN14068](https://docs.nxp.com/bundle/AN14068/page/topics/functional_safety.html); [NXP blog](https://www.nxp.com/company/about-nxp/smarter-world-blog/BL-SAFETY-REQUIREMENTS-WITH-S32K3-MCUS)
- NXP announces safety-manual and datasheet revisions through formal product change notices (e.g. Safety Manual Rev7→Rev8 alongside Data Sheet Rev11→Rev12). — [NXP PCN 202506001I via Digi-Key](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7170/202506001I.pdf)
- **IP vendors (Andes)** publish the certificate, the assessor's name and the ISO 26262 parts covered. They describe the DFMEA and FMEDA as available deliverables but do not post them. — [Andes N25F-SE](https://www.andestech.com/en/products-solutions/andescore-processors/riscv-n25f-se/)
- **Pre-silicon labeling at the incumbents:**
  - TI datasheets carry a status stamp. "PRODUCT PREVIEW information concerns products in the formative or design phase of development. Characteristic data and other specifications are design goals." Advance Information means "sampling or preproduction phase"; Production Data means "current as of publication date." — [TI AUC Data Book product stage statements](https://www.ti.com/lit/ug/sced011a/sced011a.pdf); [TI TMS320C6472 DS](https://www.ti.com/lit/ds/symlink/tms320c6472.pdf)
  - Infineon labels a pre-silicon app note directly. AN0011 "is based on TC49xA/TC4DX-silicon and TC49XN11 pre-silicon data, including chip simulation… The values will be updated based on post-silicon measurement data." — [Infineon TC4xx AN list](https://documentation.infineon.com/aurixtc4xx/docs/znw1761050437240)
- Ambiq publishes silicon errata and security advisories publicly. That is evidence that, after silicon exists, errata are expected to be visible. — [Ambiq Resources](https://ambiq.com/resources/)

### Inferences
- For a pre-silicon safety MCU, the credible public set is:
  - product brief / SKU sheet;
  - a preliminary datasheet with a TI-style status stamp ("design targets");
  - an architecture or block definition;
  - a safety-concept overview (safety mechanisms, lockstep scheme, assumed safe state), with no FMEDA numbers;
  - a list of the planned safety work products with target dates.

  Hold back FMEDA, DFA/FTA, detailed safety analysis, and anything resembling a safety case until a process assessment or certification exists. Publishing numeric diagnostic coverage pre-silicon invites challenges that cannot be answered.
- DeepGrid's "preliminary" datasheet labeling matches the TI or Infineon approach. A one-line status legend applied to every document (Product Preview / Advance / Production, or simulated / FPGA / silicon) would match incumbent practice more closely.
- An errata slot and revision history per document are expected after silicon. Before silicon, a "document revision" and "supersedes" field per item is the closest equivalent. DeepGrid already does part of this with its "supersede" notes.

### Gaps
- I did not find a primary source from a *pre-silicon startup* that publishes a safety-manual draft. No peer example was found of a startup publishing pre-silicon FMEDA material.
- I did not verify whether ST's Stellar safety manual is public or NDA.

## Q3. How startups and vendors present evidence maturity (simulation vs FPGA vs silicon) and roadmap status

### Takeaway
Incumbents use formal status vocabularies: datasheet stamps (Product Preview, Advance Information, Production Data), "pre-silicon data" notes on app notes, and Experimental / Alpha / Beta maturity labels on software. Startups mostly use availability words ("Coming Soon!", "sampling to lead customers") or third-party proof (certificates, shuttle status). They rarely use a structured evidence register. That makes DeepGrid's evidence-register approach a differentiator if it is applied consistently.

### Cited Findings
- **TI** uses three product-stage statements printed on datasheets: Product Preview (design goals), Advance Information (sampling or preproduction), and Production Data. — [TI AUC Data Book](https://www.ti.com/lit/ug/sced011a/sced011a.pdf)
- **Infineon** labels app notes built on pre-silicon data and commits to updating them with post-silicon measurements. — [Infineon TC4xx AN0011](https://documentation.infineon.com/aurixtc4xx/docs/znw1761050437240)
- **Axelera's** SDK uses explicit maturity labels: "Experimental: May change or be removed without notice … Alpha: Usable but incomplete … Beta: Feature-complete but not fully stable", alongside "production-ready release". — [voyager-sdk GitHub](https://github.com/axelera-ai-hub/voyager-sdk); [Voyager SDK docs](https://docs.axelera.ai/sdk/)
- The **Andes/Axelera** press release states availability as "currently sampling to lead customers." — [Andes press release, 1 Jun 2026](https://www.andestech.com/en/2026/06/01/axelera-ai-and-andes-technology-partner-to-power-next-generation-europa-ai-platform-with-high-performance-risc-v-ax65-cores/)
- **Mindgrove** shows maturity only through product cards ("Coming Soon!" for Edge Compute). — [Mindgrove](https://www.mindgrovetech.in/)
- **ChipFoundry** shows shuttle status publicly ("CI2612 : Open for Submission") and offers past shuttle metrics. — [ChipFoundry](https://chipfoundry.io/)
- **Investor guidance:**
  - "Distinguish between a demonstration and a product. A laboratory result…, a prototype that works when an engineer is present, a pilot unit…, and a manufactured product are four very different stages." — [Back Startups deep-tech checklist](https://backstartups.com/diligence/deeptech-diligence/)
  - Red flags include "Performance claims without reproducible measurements" and "a 2-level or larger gap between claimed TRL and observed TRL." Green flags include "Honest identification of remaining technical challenges" and "EVT/DVT/PVT milestones." — [AESTECHNO investor guide](https://www.aestechno.com/en/hardware-technical-due-diligence-investor-guide/)
  - Pre-seed evidence packs should "separate your 'best run' from your 'typical run'" and include "Test summary with conditions and baseline (include non-best runs)", "Version history (what changed between results)" and a "Milestone spec … (claim + acceptance criteria)." — [Amadeus Capital](https://www.amadeuscapital.com/pre-seed-funding-deep-tech-proof-before-revenue/)
  - Data rooms should "Start with a plain summary of what works today and what is still unproven" and "For each milestone claimed, link the data and, where possible, an external validation." — [startupdatarooms.org deep tech](https://startupdatarooms.org/use-cases/deep-tech-startups)

### Inferences
- Recommended public maturity vocabulary for DeepGrid, borrowing from TI, Infineon and Axelera. Each document, video and figure gets one evidence tag:
  - *Design target*
  - *RTL simulated*
  - *Gate-level / post-layout simulated*
  - *FPGA-validated*
  - *Taped out (shuttle X)*
  - *Silicon-measured*

  Each tag links to the evidence register entry. This mirrors TI's stamp at the asset level and answers the investor checklist directly.
- **Roadmap status.** Peers state it in plain availability terms ("sampling", "coming soon", shuttle open or closed). DeepGrid's "Nine prototypes on the ChipFoundry December 2026 shuttle" is in the same register and can be checked against ChipFoundry's public shuttle page. That is a credibility asset worth linking.
- **Video provenance.** The "Live ADAS Demo… with the DG-A100" and the dataset clips on DeepGrid's videos page have no hardware or evidence tag. Under the investor guidance above, an unlabeled demo next to "pre-silicon" products risks reading as a claimed-versus-observed maturity gap.

### Gaps
- I found no primary example of a fabless startup that publishes a formal public "evidence register". This may be a genuine white space rather than an established pattern.

## Q4. Video and learning-content patterns: types, lengths, hardware labeling

### Takeaway
Semiconductor video libraries mix four kinds of content:
- short product overviews and updates of a few minutes;
- long CTO or partner interviews and webinars of 25 to 30 minutes or more, with chapter timestamps;
- conference keynotes;
- multilingual versions.

Wistia benchmarks support 1–5 minute explainers for education and 5–30 minute walkthroughs and webinars for converting high-intent viewers. On a "Resources" page, play rates are low (6%), so the page should not depend on video alone.

### Cited Findings
- **SiFive** lists dated webinars and videos ("The Future of Compute", "SiFive Product Update", "RISC-V Solutions for Automotive", a Krste Asanović and Cliff Young AI Hardware talk). — [SiFive Resources](https://www.sifive.com/resources)
- **Ambiq** has a Video Library that includes a 28:06 CTO walkthrough of Apollo510 with detailed chapter timestamps ("00:18 Apollo510 vs Apollo4 … 24:50 Evaluation Kit … 27:35 Closing"). It is published in Japanese and Chinese versions, alongside a 2:17 SGX listing video and a 25:07 AI-lead interview. — [Ambiq Video Library](https://ambiq.com/video-library/)
- **Codasip** publishes event and demo content inside the blog stream (e.g. "Neural networks and human-to-human interfaces at Embedded World 2025"). — [Codasip Resources](https://codasip.com/resources/)
- **Axelera** homepage videos carry inline captions per clip, e.g. "Gen AI, illustration open models running locally on Axelera silicon", "Robot guided by real-time vision". — [Axelera](https://axelera.ai/)
- **Wistia 2026 State of Video** (13M+ videos):
  - Engagement by length: <1 min ~51% average; 1–3 min 46–53% across types; it falls to roughly 20–28% for 5–30 min product demos and webinars.
  - Educational videos are the most engaging type (56% <1 min, 53% 1–3 min).
  - Play rate by page: Home 24%, Video gallery 20%, Product 15%, Resources 6%.
  - Longer videos get more click-throughs (5–30 min ≈ 9%).

  — [Wistia 2026 report PDF](https://downloads.ctfassets.net/j7pfe8y48ry3/5tOf2aVNOvk9CValTgj83h/f577dc1aebb439a6904c253b9f80c23c/Wistia-2026-State-Of-Video-Report.pdf)
- **Wistia goal-to-length mapping:** awareness <1 min; "Educate or explain: 1–5 mins"; "Convert or nurture: 5–30 mins … product walkthroughs"; it also notes "an 11% drop in engagement once videos cross" 30 minutes. — [Wistia optimal length](https://wistia.com/blog/optimal-video-length)
- **Vidyard** (2022 data, 1.78M videos): 66% finish under 1 min, 56% finish 1–2 min, 50% finish 2–10 min, 39% finish 10–20 min, 22% finish over 20 min. — [MarketingProfs on Vidyard](https://www.marketingprofs.com/charts/2023/49949/business-video-benchmarks-retention-rates-by-length)

### Inferences
- DeepGrid's 1:04–1:30 part films sit in the highest-completion band and fit the "explain" goal. The 11:21 "Anatomy of our chip" fits the "nurture" band and should have chapter timestamps, as Ambiq does.
- Labeling of demo hardware is informal across peers: captions such as "running locally on Axelera silicon" rather than a structured field. A per-video "Runs on:" field (e.g. "NVIDIA Jetson / x86 GPU", "FPGA (board X)", "DG32 silicon — not yet available") plus an evidence tag would go beyond peer practice. It matters most for a pre-silicon company showing live road demos.
- Since Resources pages get about 6% play rates, the films should be linked from product/SKU pages, where play rates are 15–24%, and not live only in the Resources section.

### Gaps
- I found no primary semiconductor-specific video benchmark. The Wistia and Vidyard data are cross-industry; Wistia's "Manufacturing & engineering" row is the closest proxy.
- Typical webinar lengths for SiFive and Codasip were not visible on the fetched pages.

## Q5. Best practices: investor-facing technical resources, data-room teasers, and documentation-portal UX

### Takeaway
Investors expect the public site to carry an overview, architecture, demo and roadmap, and to separate "what works today" from "what is unproven". IP detail, test data, BOM and cost path, export-control files and source code go into a tiered data room: initial, then post-CDA, then confirmatory. Docs-portal UX best practice is the Diátaxis split (tutorials, how-to, reference, explanation), a "Start here" entry point, search, and visible versions and maturity labels. Tenstorrent and Axelera show this well.

### Cited Findings
- **Tiered access:** Level 1 "Initial, often pre-CDA: Deck, high-level architecture, public papers or grants, team"; Level 2 after the CDA: "Model, threat model, IP summary, corporate, BOM if it exists"; Level 3 confirmatory: "Full IP, source under supervision, customer contracts, export-control files." It also advises "Do not put a cloneable repo in the open room." — [Cashpian deep-tech data room](https://www.cashpian.com/what-should-be-in-a-deep-tech-fundraising-data-room)
- **Deep-tech data room index:**
  - 02 Technology overview: "plain technical summary, milestone history, readiness assessment with evidence";
  - 03 Lab and test data;
  - 04 Roadmap and capital plan;
  - 08 Export control;
  - 09 Partners: "foundry or fab access, pilot customers".

  Detailed data should be "view-only, watermarked." — [startupdatarooms.org](https://startupdatarooms.org/use-cases/deep-tech-startups)
- **Hard2beat (VC):** the Product folder should "Tell us what's already done, and what's ahead," with a technical overview and architecture. Deep-tech teams should share research papers and grants because it "will also speed up technical due diligence." — [Hard2beat](https://hard2beat.vc/insights-resources/a-guide-to-building-a-data-room-as-a-deep-tech-startup/)
- **Investor diligence checklist** for hardware: the current BOM against target and the plan between them; single-source components; "Any export controls"; "What has been demonstrated under real conditions rather than controlled ones?" — [Back Startups](https://backstartups.com/diligence/deeptech-diligence/)
- A semiconductor-specific diligence ask is "design for test (DFT) data, process node validations, and yield statistics." — [High-Tech Mag](https://www.high-tech-mag.com/hard-tech-risk-assessment-a-deep-tech-due-diligence-guide/) (secondary trade source, lower confidence)
- **Diátaxis** "identifies four distinct needs, and four corresponding forms of documentation - tutorials, how-to guides, technical reference and explanation" and proposes organizing docs "around the structures of those needs." — [Diátaxis](https://diataxis.fr/)
- **Portal UX examples:**
  - Tenstorrent: an AI search box ("Ask anything… ⌘K"), a "Get Started" path, "Popular Destinations", a hardware-free entry ("No hardware yet? … Cloud Console"), and a Software/Hardware split. — [Tenstorrent Docs](https://docs.tenstorrent.com/)
  - Axelera: "Finding your way around" explains each section and who it is for ("Start here if this is your first time…"). Tables give a one-line description per document, and the SDK carries a release compatibility matrix and release notes per version (v1.8). — [Voyager SDK](https://docs.axelera.ai/sdk/); [voyager-sdk GitHub](https://github.com/axelera-ai-hub/voyager-sdk)
- **Versioning and revision practice at incumbents:**
  - NXP shows "Rev 12, Nov 11, 2025" and file size per document, and issues change notices for revisions. — [NXP S32K3](https://www.nxp.com/products/S32K3); [NXP PCN](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7170/202506001I.pdf)
  - Infineon tables show "Version" per app note (e.g. "V1.0/2024-12-17"). — [Infineon TC4xx AN](https://documentation.infineon.com/aurixtc4xx/docs/znw1761050437240)
  - TI safety manuals end with an appendix revision history. — [TI SPNU620](https://www.ti.com/lit/pdf/spnu620)
  - Ambiq lists the date and size per file. — [Ambiq Resources](https://ambiq.com/resources/)

### Inferences
Benchmark checklist for judging DeepGrid's Resources section. A ✔/✘ applies to the current v11 where I observed it.
1. **Role-based "start here":** investor, partner/OEM and design engineer paths. ✔ partly; the landing page has portfolio / evidence / integration entry points.
2. **Public set limited to Level-1 material:** overview, architecture, preliminary datasheet, roadmap and shuttle status, with gated titles listed. ✔ ("21 more documents on request").
3. **Per-document metadata:** revision, date, status stamp (design target / simulated / FPGA / silicon), page count, "supersedes / superseded by". ✔ partly; page counts and supersede notes exist. Revision numbers, dates and a status stamp on every item were not clearly visible in the fetched text.
4. **Separate engineering specs from strategy and policy papers.** Peers keep whitepapers and press apart from datasheets. ✘ The docs page mixes the "Three-Factory Sovereign Silicon" and defence whitepaper with RTL specs.
5. **Clean template copy.** ✘ "AI accelerators" and "ADAS Benchmarks" headings on an MCU docs page; "Go inside our AI accelerators" on the videos page.
6. **Video metadata:** duration, transcript, chapters for anything over 5 minutes, "runs on" hardware, evidence tag. ✔ duration and transcripts; ✘ hardware provenance on the ADAS/E2E demos.
7. **Safety-MCU doc map:** show the planned safety work products (safety manual, FMEDA, DFA, safety case) with status and "NDA / on request" markers, following the Infineon "on request" table pattern. Not observed on v11.
8. **Search and versions.** Peers with portals (Tenstorrent, Axelera) have search and version-specific docs. For about 30 documents, a filter by SKU and doc type is likely enough; full search is optional.
9. **Data-room teaser.** Publicly name what is available after a CDA (test data, BOM and cost path, IP summary, export-control classification) and say how to request it. That turns the "on request" list into a structured Level-2 offer.

### Gaps
- I did not fetch Write the Docs guidance on versioning; Diátaxis is the only docs-framework source cited.
- No primary VC source specific to semiconductor (fabless) data rooms was found; the sources above are general deep-tech.
- I could not confirm whether any peer exposes a public "investor resources" sub-section separate from engineering docs, other than listed companies' IR sites (e.g. Ambiq, implied by its SGX listing video), which were not fetched.
