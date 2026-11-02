# DeepGrid Semi "Technical specifications" document library: audit (state as of 2026-11-02)

Scope: https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs (rendered live with Playwright/Chromium, HTTP 200, `<title>` "Documentation · DeepGrid Semi") and the read-only source clone at `/home/user/shekerkamma/deepgrid-dr-silicon-v11` (HEAD 4103fd7, 27 Oct 2026). Repo paths below are relative to that clone. "LIVE" = https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs. Reader URLs have the form `https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2F<file-stem>`.

## Q1. Full inventory: what is offered, edition, length, type, reading edition vs PDF

### Takeaway
The page offers three layers: 9 "product specification" cards that all open an in-site reading edition, 7 direct PDF downloads in four groups (5 of them duplicate cards under different titles), and 21 request-only titles (mailto). Only 1 of the 9 reading editions (the SKU Blueprint) is a faithful rendering of its PDF; the other 8 are shorter, derived "architecture specification" write-ups (7–13 KB), yet every reader page says "The source edition, unchanged."

### Cited Findings
**Page structure and counts**
- Header line on the live page: "Nine product specifications open to read; 21 more documents on request." Below it: "The October 2026 Blueprint defines the current portfolio." — [LIVE](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs)
- Card section title "Technical specifications and product evaluation guides", with the lede "The documents every figure on this site traces to. Each opens inside the site with its contents and sections; the PDF is the edition of record." Cards are generated from `groundedDocuments` with `meta: PDF · ${pdfPageCount}`, `text: first sentence of summary`, `go: 'Read on this site'`. — `app/company-pages.ts:183-186`
- The download groups come from `docGroups`. Any item without an href becomes `mailto:group@deepgrid.in?subject=Document request: …` with meta "On request". — `app/resources-data.ts:87-113`. The renderer splits these into published groups and an accordion "21 more documents, shared on request": Product Datasheets 4, SDK Documentation 4, Technical Whitepapers 3, Integration Guides 4, Performance Benchmarks 2, Software Downloads 4. — `app/company-page.tsx:280-339`; [LIVE](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs)
- Below the library the page adds: a "Contact Support"/"Videos" CTA; a BrandGallery of 3 concept illustrations, each labelled "concept illustration, not a product photograph or deployment evidence. DeepGrid silicon remains pre-silicon"; a 3-step guidance block ("Inspect document revision and evidence type"; "Keep a latency or headroom figure attached to its operating conditions"; "Resolve index shorthand against the corrective claim register and source"); and "The documents behind this page", which lists 2 docs. — [LIVE](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs); `app/resources/docs/page.tsx:9-15`

**Layer A: the 9 cards (registry `app/documents-data.ts`, in display order)**

| # | Card title (registry line) | Type | Edition/date (from the file itself) | PDF behind it (pdfinfo pages / bytes) | Reading edition (.md) | Does the reading edition render the PDF? |
|---|---|---|---|---|---|---|
| 1 | "Thirty Use Cases, No Accelerator" (`:31`) | analysis / app-level whitepaper | PDF created 11 Sep 2026 (pdfinfo); PDF title "DG32-LITE Base Variant — Use Cases and Models" | deepgrid-dg32-ai-30-use-cases.pdf, 12 pp, 413,860 B | deepgrid-dg32-ai-architecture.md, 7,345 B, 91 lines | No. It is an "Edge AI & Predictive Diagnostics System Architecture" write-up, not the PDF text |
| 2 | "SKU Blueprint, October 2026 (11 SKUs + D100)" (`:63`) | strategy / portfolio | "October 2026"; cover marked "CONFIDENTIAL" | deepgrid-sku-blueprint-oct2026.pdf, 46 pp, 3,806,673 B | deepgrid-sku-blueprint-oct2026.md, 67,624 B, 1,084 lines | Yes: "Markdown rendering of `deepgrid-sku-blueprint-oct2026.pdf` (46 pages)… Text and tables are taken from the PDF unchanged", with `[pdf p.N]` markers |
| 3 | "dgrid_dshot_rx RTL Specification" (`:93`) | block / RTL spec | "Block spec for review · DG32 · 13 Sep 2026 · draft 1. Author: DG32 engineering (drafted with Claude). Reviewer: Ayaz Khan" | deepgrid-dshot-rx-block-spec.pdf, 8 pp, 353,228 B | deepgrid-dshot-rx-architecture.md, 11,311 B | Derived. Classification line "Internal Silicon Diligence Canon" |
| 4 | "DG32-2DOM Architecture & Block Definition" (`:124`) | architecture / reference | PDF created 12 Sep 2026; die "dg32_2dom (A3)", chipIgnite CI2612 | deepgrid-dg32-2dom-system-architecture.pdf, 24 pp, 78,754 B | deepgrid-2dom-architecture.md, 9,261 B | Derived. Header: "Confidential Silicon Diligence Canon" |
| 5 | "Mature-Node Silicon for India's Defence (Whitepaper v3)" (`:155`) | strategy whitepaper | "PLAIN-LANGUAGE EDITION · v3 · Angel / seed round · ₹10 Cr · September 2026"; PDF created 5 Sep 2026 | deepgrid-mature-node-silicon-master-whitepaper-v3.pdf, 71 pp, 5,620,752 B | deepgrid-mature-silicon-architecture.md, 10,713 B, 140 lines | No. A 10.7 KB summary of a 71-page PDF, headed "Confidential Diligence Whitepaper Specification" |
| 6 | "Preliminary Engineering Datasheets & Package Pinout" (`:186`) | datasheet + pinout | Undated (pypdf output); PDF title "DG32 QFN-64 Preliminary Datasheets: DG32-LITE and DG32-2DOM" | deepgrid-datasheets-qfn64.pdf, 24 pp, 78,550 B | deepgrid-datasheets-engineering-spec.md, 13,551 B | Derived. "Confidential Preliminary Datasheet Specification (CI2609 & CI2612 Releases)" |
| 7 | "D100 Tactical Drone Platform Architecture" (`:217`) | architecture concept | No date; md says "Generated Via: `/architecture-to-everything` compounded with `/deepgrid-mature-silicon`" | No own PDF. Points to the SKU Blueprint PDF, "pp. 42–44" (`:223-227`) | deepgrid-d100-architecture.md, 12,059 B | Derived, AI-generated |
| 8 | "DG SDV Software-Defined Vehicle Zonal Architecture" (`:249`) | reference-platform concept | No date; "Generated Via: `/architecture-to-everything`…" | None. `pdfFile` is the .md itself; `pdfPageCount: 'in-site document'` (`:254-258`) | deepgrid-sdv-architecture.md, 8,010 B | Derived, AI-generated |
| 9 | "Three-Factory Sovereign Silicon Architecture" (`:279`) | strategy | No date; "Generated Via: `/deepgrid-architecture` (Codified Compound Architecture Compiler)" | No own PDF. Points to the whitepaper, "Section 4" (`:285-289`) | deepgrid-three-factory-architecture.md, 9,551 B | Derived, AI-generated |

Sources for the table: `app/documents-data.ts:26-306`; `pdfinfo`/`pdftotext` of each file in `public/downloads/docs/`; first lines of each .md in `public/downloads/docs/`; live card text on [LIVE](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs).

- The page counts on the cards match pdfinfo for all 6 cards with a dedicated PDF (12, 46, 8, 24, 71, 24). — `app/documents-data.ts:41,72,103,134,165,196` vs pdfinfo
- Numbering: the badges run DOC #1, #7, #3, #4, #5, #6, then S1–S3. There is no DOC #2, and the file header still says "All 6 Core Authoritative Design Documents (Docs #1..#6) + 3 Platform Deliverables". — `app/documents-data.ts:2,29,60`
- The card meta reads "PDF · IN-SITE DOCUMENT" for SDV, which has no PDF at all. — [LIVE](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs)
- Every reader page shows the banner "The source edition, unchanged. Architecture targets, proposals and dated plans are preserved as written; they do not establish measured silicon, qualification or certification." — `app/doc-reader.tsx:131`; seen live on the reader pages for whitepaper, D100, DShot and Blueprint ([whitepaper reader](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-mature-silicon-architecture))
- The Blueprint reader's "In this document" table of contents is empty, because the .md has 0 `## ` headings (`grep -c '^## '` = 0). The reader builds its contents from H2s. — [Blueprint reader](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-sku-blueprint-oct2026); `public/downloads/docs/deepgrid-sku-blueprint-oct2026.md`

**Layer B: direct PDF downloads (7 links, all `download` attribute)**
- Product Datasheets: "DG32-LITE preliminary datasheet" (PDF · 12 pages; created 12 Sep 2026); "DG32-2DOM preliminary datasheet" (PDF · 12 pages; created 12 Sep 2026); "DG32 QFN-64 datasheets, both parts" (PDF · 24 pages); "Product portfolio: SKU Blueprint, October 2026" (PDF · 46 pages · 3.6 MB). — `app/resources-data.ts:92-97`
- Technical Whitepapers: "Mature-node silicon for India's defence and industrial base" (PDF · 71 pages · 5.4 MB, with the superseded note); "DG32-2DOM system architecture: block definition" (PDF · 24 pages); "DG32-LITE base variant: thirty use cases and models" (PDF · 12 pages). — `app/resources-data.ts:102-106`
- Performance Benchmarks: "ADAS Benchmarks" links to /evidence, not to a document. — `app/resources-data.ts:110`
- The two single-part datasheets (LITE, 2DOM) exist only as PDFs and have no reading edition card. The DShot block-spec PDF is not linked from the docs page at all; it is reachable only from inside its reader page. — [LIVE](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs) link dump; [DShot reader](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-dshot-rx-architecture)
- Unique PDFs offered across both layers: 8, which matches the 8 PDFs in `public/downloads/docs/`.

**Layer C: request-only (21 mailto titles)**
- Datasheets: DG-A100 ADAS SoC, DG-R100 Radar SoC, DG-S100 SDV Controller, DG-T100 Transformer NPU. SDK: Getting Started, API Reference, Code Examples, Best Practices. Whitepapers: AI Acceleration Architecture, Edge Computing Performance, Power Efficiency Studies. Integration: Hardware Integration, Software Setup, System Configuration, Troubleshooting. Benchmarks: Transformer Performance, Power Consumption Analysis. Software: DGrid SDK, Drivers & Firmware, Development Tools, Sample Projects. — `app/resources-data.ts:96-112`
- The accordion explains these as "Listed by deepgridsemi.com and not published here." — [LIVE](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs)

**Files on disk but not on the page**
- `public/downloads/docs/` also holds `deepgrid-sku-compendium-architecture.md` ("Nine Core Peripheral SKUs (SKU-1 through SKU-9)", Technical Annex v3), `deepgrid-d100-notebooklm-briefing.md`, 9 `.drawio` files and `deepgrid-qfn64-pinout-architecture.drawio`. `public/downloads/` adds `dg32-lite-architecture-guide.md`, `dg32-2dom-architecture-guide.md`, `sku-1…sku-9` guides, `.pptx` decks and `*-workflow.html`. — `ls public/downloads public/downloads/docs`

### Inferences
- The card lede promises that "the PDF is the edition of record" and the banner says "source edition, unchanged". Both are accurate only for the Blueprint. A reader of the other 8 "Read on this site" editions is reading a secondary, partly AI-generated digest. The D100/SDV/three-factory files say so themselves ("Generated Via"), and DShot says "drafted with Claude".
- Effective unique document count: 8 PDFs plus 3 PDF-less concept write-ups (D100, SDV, three-factory) = 11 distinct items. The page's two counts ("Nine…", "21 more…") hide the duplication between cards and downloads.

### Gaps
- No PDF carries a revision number or change log apart from the whitepaper ("v3") and DShot ("draft 1"). The QFN-64 combined datasheet has no creation date (pypdf strips it), so its edition cannot be dated.

## Q2. Consistency: contradictions, supersession flags, marketing-heavy summaries

### Takeaway
The September whitepaper contradicts the October Blueprint on chip count, clock, orders and funding. The site's supersession flag is visible only in one download-list note: it is cut from the cards (which show only the summary's first sentence) and missing from the reader. The whitepaper's reading edition repeats the MCEME ₹1.01 Cr "contracted" claim that `app/claims.ts` withholds as misdescribed. Several card summaries assert "proof", "guaranteed" and "validated on test silicon" beyond pre-silicon evidence.

### Cited Findings
**Whitepaper v3 (Sep 2026) vs SKU Blueprint (Oct 2026)**
- Chip count. Whitepaper: "Part Four Ten chips…", "9 Ten chips, and what each one is for", and "We cut down to the nine kinds of chip we actually build". — whitepaper PDF text, lines 41, 103, 215 (`pdftotext`, `public/downloads/docs/deepgrid-mature-node-silicon-master-whitepaper-v3.pdf`). Blueprint: "Eleven chips on SkyWater 130 nm and SCL 180 nm, plus the Track B drone SoC". — Blueprint PDF p.1. The SKU compendium md still says "Nine Core Peripheral SKUs (SKU-1 through SKU-9)". — `public/downloads/docs/deepgrid-sku-compendium-architecture.md:5`
- Clock. Whitepaper: "The product is the 130 nm chip at 200 MHz" and "Why 200 MHz is enough". — whitepaper text, lines 101, 925. Blueprint: "Product is a 130 nm chip at 100 MHz, the speed DG32-Max is built for on SKY130" (also "130 nm ∙ 100 MHz" on SKU pages). — Blueprint text, lines 404, 620. DG32 cards: "50 MHz RV32IM", "50 MHz Control · 114 MHz Attention". — `app/documents-data.ts:43,136`. The reading editions of three-factory and D100 still say "Fixed 200 MHz" / "200 MHz fixed clock". — `deepgrid-three-factory-architecture.md:52`, `deepgrid-d100-architecture.md:22,35`
- Orders. Whitepaper: "DONE ₹2.88 Cr of real revenue, before any chip exists. The Indian Army through MCEME: ₹1.01 Cr under contract…". — whitepaper text, line 371. Blueprint: "Customer evidence: this book claims no purchase orders or letters of intent; signing design partners is a tranche 2 milestone." — Blueprint text, line 253. Claim register: "₹1.01 Cr contracted, Indian Army MCEME, attached to Chip 4" is withheld because "₹23.01L delivered, ₹78.39L is L1 (lowest bidder, not an award), and it sits in Deepgrid Datacentre Pvt Ltd rather than Deepgrid Semi". — `app/claims.ts:177-181`
- Funding. Whitepaper: a single "Angel / seed round · ₹10 Cr". D100 is "a separate ₹50 Cr institutional round, gated on revenue, with first silicon targeted for early 2027". — whitepaper p.1; text line 1284. Blueprint: "Tranche 1, ₹10 Cr, takes nine chips to tape-out. Tranche 2, ₹40 Cr in May 2027". D100 "tape-out after the Rs 50 Cr institutional round, which follows mature-node revenue", at TSMC 28 nm. — Blueprint text, lines 234-235, 2764

**How supersession is flagged**
- The supersession sentence ("September 2026 edition, superseded in part by the October SKU Blueprint (chip count, clock, orders, funding). Its orders figure includes a contract this site withholds as misdescribed; do not cite it.") is stored in the whitepaper and three-factory card summaries (`app/documents-data.ts:172,296`) and in the whitepaper download note (`app/resources-data.ts:103`).
- The cards render only the summary's first sentence (`d.summary.split(/(?<=\.)\s/)[0]`, `app/company-pages.ts:185`). As a result the live whitepaper card reads only "The foundational 71-page master whitepaper establishing India's mature-node semiconductor doctrine." and the three-factory card only "Geopolitical and fab-arbitrage blueprint for Indian semiconductor sovereignty." — [LIVE](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs)
- On the live reader pages for the whitepaper and three-factory editions, the word "supersed" does not appear anywhere (Playwright text search = false). The pages say instead "The source edition, unchanged." — [whitepaper reader](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-mature-silicon-architecture); [three-factory reader](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-three-factory-architecture)
- The whitepaper PDF has no supersession stamp of its own (its pp.1 text carries none). — `pdftotext` of the whitepaper PDF

**Withheld claim republished in a reading edition**
- The whitepaper reader shows: "Live Pre-ASIC Contracted Revenue: ₹2.88 Crore (Indian Army MCEME ₹1.01 Cr, Infinis Agritech ₹1.25 Cr, Axitech Solar ₹0.62 Cr)" and a table row "Chip 4 | Lockstep Safety MCU | … | Indian Army MCEME (₹1.01 Cr Contracted); ISO 26262 ASIL-D". — `public/downloads/docs/deepgrid-mature-silicon-architecture.md:16,106`; confirmed in the live reader text ([reader](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-mature-silicon-architecture))
- The same .md is also the cited source for 3 of the 15 claims in the register (`node-130`, `loop-198`, `asil-d`). — `app/claims.ts:115-140`

**Card vs its own reading edition**
- D100. The card says "Flight control, visual navigation and optional AI on one 28 nm chip" and summarises "Quad RV64 … Quad RV32" (`app/documents-data.ts:218,234`). The reading edition describes a "Heterogeneous Multi-Die System-in-Package", "130nm CMOS (SkyWater 130 / IHP SG13G2) + BCD 180nm + 28nm Compute", with "Dual DGridRiscV Flight Cores… at 200 MHz" on SKY130, and contains no "Quad"/"RV64". — `deepgrid-d100-architecture.md:4,6,22,35`
- Three-factory. The card subtitle and stats name "SkyWater, SCL Mohali, and Dholera 28nm fabs" / "180nm BCD · 130nm CMOS · 28nm Planar" (`app/documents-data.ts:280,291-292`). The reading edition names "SkyWater Technology (USA) · IHP Leibniz (Germany) · SCL Mohali (India)" and "130nm SiGe:C BiCMOS". — `deepgrid-three-factory-architecture.md:5-6`
- DShot. The card calls it "Complete RTL engineering specification" (`app/documents-data.ts:110`); the document calls itself "Block spec for review · … draft 1". — DShot PDF p.1

**Summaries claiming more than pre-silicon evidence supports**
- Doc 1: "Formal proof that high-accuracy industrial condition monitoring… do not require heavy transformer acceleration"; "running 50–500× faster"; "Uncovers critical 100% synthetic accuracy leakage". — `app/documents-data.ts:48,53`. The live card shows "Formal proof…" as its whole text.
- Doc 4: "control loop worst-case execution time guaranteed untouched"; "18 on-die SRAM macros… with positive timing slack". The slack is a post-route result, but the card does not label its evidence kind. — `app/documents-data.ts:143,146`
- Doc 5: "creates statutory moats" and "foundational… doctrine". — `app/documents-data.ts:172`
- Three-factory: "guaranteeing supply continuity", "Sanction-proof multi-foundry PDKs", "Zero-NRE open-source toolchain… validated on test silicon", "Proof of concept for India's ₹10 Cr sovereign chip initiative". — `app/documents-data.ts:293,296,299,301`
- D100 reading edition: "DGCA Type Certification: Compliant with Directorate General of Civil Aviation standard civil airworthiness regulations". — `deepgrid-d100-architecture.md:117`
- Counter-examples that are well labelled: SDV "ISO 26262 ASIL-D (target, not certified)" (`app/documents-data.ts:263`) and Blueprint "Volumes, prices and shares are the company's own estimates" (`:79`). The claim register itself labels kinds such as "Simulated", "Post-route", "Tool estimate". — `app/claims.ts:16`
- The whitepaper PDF itself admits an unproven point: "we should publish the exact project link, because right now we are asserting this rather than showing it." — whitepaper text, line 369-370

**Publication hygiene**
- Publicly downloadable files carry confidentiality labels: Blueprint PDF cover "CONFIDENTIAL"; 2DOM md "Confidential Silicon Diligence Canon"; datasheet md "Confidential Preliminary Datasheet Specification"; DShot md "Internal Silicon Diligence Canon". — Blueprint PDF p.1; `.md` headers in `public/downloads/docs/`
- The whitepaper reading edition prints the managing director's mobile number in its header ("Managing Director: Aravind Prasad (+91 74163 19944)"). — `deepgrid-mature-silicon-architecture.md:4`

### Inferences
- An investor who opens the whitepaper card lands on a reading edition labelled "source edition, unchanged". It states a ₹2.88 Cr contracted-revenue figure that the site's own register withholds, and nothing on that page warns against it. This is the most material integrity defect in the library.
- The clock figure varies across the documents a reader can open from one page: 50 MHz (DG32), 100 MHz (Blueprint SKUs), 200 MHz (whitepaper, D100 and three-factory editions). Nothing on the page reconciles them.

### Gaps
- I did not read every page of all 8 PDFs. The contradiction checks used text search (`pdftotext` + grep) for counts, clocks, orders and funding. Other conflicts (for example prices or market sizes per SKU) were not exhaustively compared.

## Q3. Organization: grouping, filtering, ordering, audience reading paths

### Takeaway
The page has no filters, dates, audience labels or recommended order. Cards appear in raw registry order (#1, #7, #3, #4, #5, #6, S1–S3). The download groups reuse deepgridsemi.com's legacy taxonomy ("for all our AI accelerators"), which does not fit a motor-control/safety MCU portfolio. The investor journey the owner chose (PRODUCT.md) has no document path.

### Cited Findings
- Card order equals array order in `groundedDocuments`: doc1, doc7, doc3, doc4, doc5, doc6, doc-d100, doc-sdv, doc-three-factory. The registry's `group: 'core' | 'platform'` field is not shown on this page. — `app/documents-data.ts:26-306`; [LIVE](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs)
- A filterable hub (`app/documents-hub.tsx:25` filter; "All Documents" count badge `:141`) exists in the codebase, used by `app/library.tsx`. The docs route renders `CompanyPageView` instead. — `app/resources/docs/page.tsx:12`
- Group ledes copied from deepgridsemi.com: "Detailed specifications and technical documentation for all our AI accelerators"; "Complete developer guides and API references for DGrid SDK". — `app/resources-data.ts:91,99`. The page hero "Access technical documentation, datasheets, whitepapers, and development resources" and the CTA "Contact Support" are support-desk framing. — `app/company-pages.ts:181-189`
- Owner's direction: "Investors and strategic partners are the primary audience (owner, 14 Oct 2026). The primary action is a discussion or data-room enquiry." — `PRODUCT.md:8`. The docs page's in-library CTAs are "Contact Support" and "Videos". "Request a discussion" appears only in the generic "Continue your review" footer. — [LIVE](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs)
- The page's own 3-step guidance (inspect revision and evidence type; keep figures with operating conditions; resolve against the claim register) is good method advice, but the cards show no revision or evidence type to inspect. — [LIVE](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs)

### Inferences
Proposed importance-ranked paths built only from existing documents:
- **Investor / strategic partner (thesis → plan and financials → evidence → risk):**
  1. SKU Blueprint Oct 2026 PDF: the current portfolio, unit economics, tranche 1/2 use of funds, and "claims no purchase orders".
  2. /evidence page: how each figure was obtained.
  3. The DG32 QFN-64 datasheet as the single proof-point part.
  4. The whitepaper v3 PDF, for market sizing ($9B funnel), the 198-day loop and the stop rules S1–S4. Read it only with an explicit "superseded on chip count, clock, orders and funding; orders figure withheld" stamp.
  5. Three-factory / D100 / SDV, last and labelled as concept architectures.
- **Equipment-maker engineer (datasheet → reference → application):**
  1. DG32-LITE preliminary datasheet.
  2. QFN-64 combined datasheet (pinout, supply sequencing, boot ROM).
  3. DG32-LITE architecture guide (`/resources/read?doc=dg32-lite-architecture-guide`, linked only in the page footer).
  4. DG32-2DOM datasheet + 2DOM block definition.
  5. DShot RX block spec (draft 1).
  6. "Thirty use cases" as the closest thing to an application note.
- **Gap in the paths:** `dg32-lite-architecture-guide.md` is the source for 6 of the 15 register claims (39 cycles, ~100 kHz, ~300 cycles, 177 cycles, 53–58 cycles, ~8 CPI; `app/claims.ts:34-87`), yet it is not one of the 9 cards.

### Gaps
- No analytics were available to show what visitors actually open first.

## Q4. Gaps vs a semiconductor documentation set and an investor data-room index

### Takeaway
For engineers, preliminary datasheets, a pinout/package spec, block/architecture definitions and one block RTL spec exist. A safety manual (FMEDA/DFA) is the most important missing item for a lockstep part designed to an ASIL-D target. SDK, integration and evaluation-board material is listed but only "on request". Errata are appropriately absent pre-silicon. For investors, the Blueprint covers portfolio, unit economics and use of funds. There is no data-room index, financial model file, risk register, IP schedule or team/cap-table document on the page.

### Cited Findings
| Expected item | Status on page | Evidence |
|---|---|---|
| Datasheet | Present, preliminary (3 PDFs: LITE 12 pp, 2DOM 12 pp, combined 24 pp) | `app/resources-data.ts:93-95` |
| Pinout / package | Present inside the QFN-64 datasheet: "QFN-64 (9×9 mm, 0.5 mm pitch)", 44 signal pins, supply sequencing "3.3V I/O must lead 1.8V core by ≥1 ms" | `app/documents-data.ts:198-203` |
| Reference manual / register-level architecture | Partial: 2DOM block definition (24 pp); DShot block spec (draft 1). The DG32-LITE architecture guide exists but is not a card | `app/documents-data.ts:124,93`; `public/downloads/dg32-lite-architecture-guide.md` |
| Application notes | None as such. "Thirty use cases" is the closest; "Integration Guides" (4) on request | `app/resources-data.ts:107-108` |
| Evaluation-board guide | None published; "Hardware Integration" on request | `app/resources-data.ts:108` |
| Safety manual (FMEDA, DFA, assumptions of use) | Absent, and not even in the request list. The site describes ASIL-D as "The target the lockstep safety MCU is designed against. A mechanism, not a held certificate" | `app/claims.ts:133-139` |
| SDK / tools | Request-only: "DGrid SDK", "Drivers & Firmware", "Development Tools", "Sample Projects", "API Reference". A source comment notes the original site's SDK GitHub download was replaced "(no repository exists)" | `app/resources-data.ts:99-112`; `app/company-pages.ts:6-8` |
| Errata | Absent, and appropriately so pre-silicon (no silicon exists to have errata) | `PRODUCT.md:10` ("Published DG32 evidence remains pre-silicon") |
| Design-in checklist | Absent. The D100 reading edition has an "Architecture Verification & Interface Checklist" section, but it is for the concept SoC | D100 reader TOC ([reader](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-d100-architecture)) |
| Characterisation / qualification reports | Absent, and correctly so pre-silicon. "ADAS Benchmarks" redirects to /evidence | `app/resources-data.ts:110` |

- Request-only datasheets name products outside the 11-SKU Blueprint: "DG-A100 ADAS SoC", "DG-R100 Radar SoC", "DG-S100 SDV Controller", "DG-T100 Transformer NPU". — `app/resources-data.ts:96`; compare Blueprint "Eleven chips…" (Blueprint PDF p.1)
- Investor-relevant content present: market funnel, 198-day loop, stop rules and the ₹10 Cr round in the whitepaper (superseded in part). Plan line per SKU, a ₹1,000 Cr run-rate plan, "about ₹610 Cr in FY31", tranche 1 ₹10 Cr / tranche 2 ₹40 Cr, and development cost "₹41.7–91.2 Cr" for all eleven are in the Blueprint. — Blueprint text lines 87, 157, 234-235, 311
- Not present as documents: financial model workbook, cap table / term sheet, team and advisor bios, IP/patent schedule, corporate/legal pack, customer pipeline/LOI file (the Blueprint states there are none), a standalone risk register, and a data-room index or request form. — [LIVE](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs) (absence observed); `PRODUCT.md:19` ("Contact transparently composes mail; it does not submit to a backend")

### Inferences
- The most valuable additions that are honest pre-silicon: a safety concept / preliminary safety manual for DG32-LITE (assumptions of use, lockstep diagnostic coverage target, labelled as target), a design-in checklist derived from the QFN-64 sequencing and boot rules, an evidence ledger PDF exported from `app/claims.ts`, and a one-page data-room index that states what is available on request.
- Errata, characterisation and qualification reports should stay absent. The page could say explicitly that they will follow first silicon from the December 2026 shuttle (Blueprint p.1: "Nine prototypes on the ChipFoundry December 2026 shuttle").

### Gaps
- Whether the request-only items actually exist behind the mailto is unknowable from the site.

## Q5. Findability: titles, file names, link text, sizes, broken downloads

### Takeaway
All sampled downloads return HTTP 200 with correct MIME types, and the stated page counts are accurate. Findability still suffers from: the same document appearing under two different titles; reading-edition filenames that don't match their PDFs; sizes shown on only 2 of 7 downloads (and inconsistently, 5.62 MB vs 5.4 MB); no dates on cards; and the generic link text "Read on this site" repeated 9 times.

### Cited Findings
- HTTP checks on 2026-11-02 (curl), all **200**: the 8 PDFs (deepgrid-dg32-lite-preliminary-datasheet.pdf 38,751 B; deepgrid-dg32-2dom-preliminary-datasheet.pdf 41,019 B; deepgrid-datasheets-qfn64.pdf 78,550 B; deepgrid-sku-blueprint-oct2026.pdf 3,806,673 B; deepgrid-mature-node-silicon-master-whitepaper-v3.pdf 5,620,752 B; deepgrid-dg32-2dom-system-architecture.pdf 78,754 B; deepgrid-dg32-ai-30-use-cases.pdf 413,860 B; deepgrid-dshot-rx-block-spec.pdf 353,228 B), all `application/pdf`. Three .md sources returned `text/markdown`. The legacy `deepgrid-d100-architecture.html` returned 200 (a 769-byte redirect stub to the reader, per `scripts/document-readers.mjs:27-32`). `/resources/read?doc=…` returned 200. — [base](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/downloads/docs/)
- Duplicate titles for one file: "Thirty Use Cases, No Accelerator" (card) = "DG32-LITE base variant: thirty use cases and models" (download); "Preliminary Engineering Datasheets & Package Pinout" = "DG32 QFN-64 datasheets, both parts"; "DG32-2DOM Architecture & Block Definition" = "DG32-2DOM system architecture: block definition"; "Mature-Node Silicon for India's Defence (Whitepaper v3)" = "Mature-node silicon for India's defence and industrial base"; "SKU Blueprint, October 2026 (11 SKUs + D100)" = "Product portfolio: SKU Blueprint, October 2026". That is 5 of 7 downloads. — `app/documents-data.ts`; `app/resources-data.ts:92-106`
- Filename mismatches between PDF and reading edition: `deepgrid-dg32-ai-30-use-cases.pdf` ↔ `deepgrid-dg32-ai-architecture.md`; `deepgrid-mature-node-silicon-master-whitepaper-v3.pdf` ↔ `deepgrid-mature-silicon-architecture.md`; `deepgrid-datasheets-qfn64.pdf` ↔ `deepgrid-datasheets-engineering-spec.md`; `deepgrid-dshot-rx-block-spec.pdf` ↔ `deepgrid-dshot-rx-architecture.md`. Only the Blueprint shares a stem. — `app/documents-data.ts:35-38,97-100,159-162,191-192`
- Sizes. They appear only on the Blueprint ("3.6 MB") and whitepaper ("5.4 MB") download links. The registry holds "5.62 MB" for the same 5,620,752-byte file (5.62 MB decimal = 5.36 MiB), so the two figures conflict. Cards show no size. — `app/resources-data.ts:97,103`; `app/documents-data.ts:164`
- No card shows a date or version. Of the 9 titles, only the Blueprint ("October 2026") and whitepaper ("v3") carry one. — [LIVE](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs)
- Link text: every card ends in the identical "Read on this site". Card meta reads "PDF · 46 PAGES" while the link actually opens the reader, not the PDF. "PDF · PP. 42–44" and "PDF · SECTION 4" point into other documents. — [LIVE](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs)
- Breadcrumb/label drift: menu label "Technical specifications" (`app/routes.ts:69`), page `label: 'Documentation'`, hero `title: 'Resources'` (`app/company-pages.ts:180-181`), `<title>` "Documentation · DeepGrid Semi" (`app/resources/docs/layout.tsx:20`), and the reader breadcrumb "Technical references / Technical reference". — [LIVE](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/docs); reader pages

### Inferences
- A user who downloads both "Thirty Use Cases" and "DG32-LITE base variant…" gets the same file twice. A reader who saves the "Markdown source" of the whitepaper card gets a file whose name and content differ from the 71-page PDF.
- Quick wins: one canonical title per file; show date, version, evidence level and size on each card; descriptive link text ("Read the Blueprint (46 pp, Oct 2026)"); render the full summary or a dedicated "Superseded" badge on cards; and a reader banner driven by a `status` field (current / superseded-in-part / concept) instead of the blanket "source edition, unchanged".

### Gaps
- Sampled download URLs only. The 21 mailto links were not exercised, and the request flow composes email rather than submitting (`PRODUCT.md:19`).
