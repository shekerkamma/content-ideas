# DeepGrid Semi Resources section: /resources landing page and /resources/read document reader

Method: I rendered the live pages with Playwright/Chromium at 1440px and 390px on 2026-11-02, extracted headings, links, text, network 4xx responses and layout metrics, and opened the "Read Spec" modal. I also used the filter search and loaded `/resources/read` with 14 `?doc=` keys: the 9 registry documents, 2 architecture guides, the SKU compendium, one bogus key and no key. Every load was checked against the read-only source at `/home/user/shekerkamma/deepgrid-dr-silicon-v11` (HEAD 4103fd7, 27 Oct 2026). File references are repo-relative `path:line`.

Live URLs: L1 = https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/ ; L2 = https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-sku-blueprint-oct2026 (other `?doc=` keys are cited inline).

## Q1. What does /resources show, in what order, and where does it send an investor vs an engineer?

### Takeaway
/resources is one long page. A 9-card document hub (with filters and search) comes first. Below it is a deck-and-film player for 5 DG32 packages, then a DG32-LITE diagram, references, a block of legacy jump buttons, an application-image gallery, a "next decision" box and related links. All of it is aimed at engineers. The only route to the investor primary action is a single "Request a discussion" link at the very bottom, plus the global header CTA. At 390px the decks and films start about 10,600px down a page that is about 21,900px long.

### Cited Findings
**Section order as rendered (1440px)**
- Breadcrumb "Home / Technical references". The single H1 is "Technical documents, decks and films." and the lead is "Start with the portfolio for product scope, the evidence register for maturity, or the detailed documents for integration. Every source has a different role in an evaluation." — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/); text from `app/executive-routes.json:92-97`.
- The page source passes its own title and copy: "The documents, decks and films behind every figure" / "Six source documents carry every number on this site…" (`app/resources/page.tsx:19-22`). `SectionHead` throws them away and uses the route story instead (`title=story.headline; copy=story.context`, `app/detail.tsx:14`). The "Six source documents" claim is dead code and does not render, which is good because 9 documents are listed.
- Heading outline: H1 → H2 "Architecture and electrical specifications" → 9 × H3 document titles → H2 "Lockstep safety on an entry-level motor chip" (deck) → H2 "DG32-LITE: system architecture and functional interfaces" → H2 "Control, sensing and integration in the customer system." → H2 "The portfolio sets scope, the evidence register sets maturity, the documents set integration detail." → H2 "Related products and references". No levels are skipped. — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)

**Section 1: document hub** (`app/documents-hub.tsx`)
- Kicker "9 product specifications", H2 "Architecture and electrical specifications". The lead says "Simulation results, timing budgets, clock partitions and pin assignments all come from these documents… check a figure against its section in Ask DeepGrid". There is also a button labelled "Explore in Ask DeepGrid". — `documents-hub.tsx:96-123`.
- There are three filter tabs: "All Documents 9", "Core Silicon Deliverables (Docs #1–#6) 6" and "Platform & System Architectures 3". The 6 "core" cards are badged DOC #1, #7, #3, #4, #5, #6. There is no DOC #2, and #7 (the SKU Blueprint) sits second, so the label "Docs #1–#6" does not match the cards. — `documents-hub.tsx:145`; `app/documents-data.ts:29,60,91,122,153,184`.
- Search box placeholder: "Search documents by parameter, standard, or title…". It filters on title, subtitle, summary, subsystem, badge and stat cards only, not on document text. In testing, "ASIL" matched only "DG SDV…", even though the DOC #1 card itself shows "ISO 26262 ASIL-D (target, not certified)". "investor" returned the empty state 'No documents found matching "investor" in this category.' with a "Reset Filters" button. — `documents-hub.tsx:24-39,256-263`; [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- The 9 cards, in order: Thirty Use Cases, No Accelerator; SKU Blueprint, October 2026 (11 SKUs + D100); dgrid_dshot_rx RTL Specification; DG32-2DOM Architecture & Block Definition; Mature-Node Silicon for India's Defence (Whitepaper v3); Preliminary Engineering Datasheets & Package Pinout; D100 Tactical Drone Platform Architecture; DG SDV Software-Defined Vehicle Zonal Architecture; Three-Factory Sovereign Silicon Architecture. — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- Every card has a badge, subsystem, subtitle, summary, 4 stat cells, a list titled "Key architectural proofs" and 4 actions: "Download PDF <size>", "Read Spec", "Spec (.md) <size>" and "Ask DeepGrid". — `documents-hub.tsx:184-253`.
- The SKU Blueprint is described as "The source of record for every SKU on this site" (`documents-data.ts:63`), but it appears second, not first.

**Section 2: deck and film player** (`app/library.tsx`, `app/library-data.ts`)
- Two tab groups. "Product architectures" holds DG32-LITE (16 slides, 7:43 film) and DG32-2DOM (13 slides, 6:16). "Electrical specifications and first-silicon design" holds DG32-LITE Datasheet (12 slides, 5:32), DG32-2DOM Datasheet (9 slides, 4:19) and DG32-LITE Tape-in block diagram (11 slides, 5:29). That is 5 packages, 61 slides and about 29 minutes of film. — `library.tsx:13,42`; `library-data.ts:24-121`; [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- One `<video>` with an English captions track. The chapter list carries the kicker "Product functions and operating requirements", which is a generic label for chapters such as "Why lockstep" and "The control-loop budget". There is one deck download, "Download the deck (.pptx)", a slide stage with 16 numbered thumbnail buttons and "Play this slide in the film". — `library.tsx:44-56`.
- The DG32-LITE diagram block has "Open full diagram" (SVG), "Diagram source (.drawio)", "Read architecture guide" and 8 "Guide: …" deep links into `/resources/read?doc=dg32-lite-architecture-guide#…`. "Guide: Safety core" appears twice. — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- "Primary sources" lists 3 items and "7 integration and validation references", which are external TI, IEEE, RISC-V, Arm, DShot and SkyWater links. These are collapsed. — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- "Engineering references" lists the 5 source documents behind the package, then a disclaimer: "Investor-level content from Deepgrid Semi's September 2026 design documents: no register maps, memory map or board-design rules. Pre-silicon: figures are design values, process nominals or analytic estimates, labelled on each slide." The brand is spelled "Deepgrid", not "DeepGrid". — `library.tsx:67`.

**Sections 3 to 6**
- 7 unlabelled legacy jump buttons ("Overview & safety thesis", "Product family comparison", "Block architecture & 3D die", "100 kHz control-loop budget", "QFN-64 pinout & package", "Multi-spin roadmap", "Ask DeepGrid about products and applications"). They are `<button>`s calling `go('overview'|'family'|'architecture'|…)`, the old hash-router view ids, so they cannot be opened in a new tab or copied as links. — `library.tsx:69-79`; `app/routes.ts:101-110`.
- Brand gallery H2 "Control, sensing and integration in the customer system." with 4 "Review …" image links, each captioned "concept illustration, not a product photograph or deployment evidence. DeepGrid silicon remains pre-silicon." — `app/brand-imagery.tsx:23`; [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- Route-journey box: "The library spans portfolio strategy, product architecture and workload analysis." It numbers three steps: 01 "Use the SKU compendium for function and part scope.", 02 "Use DG32 architecture for safety, timing and package details.", 03 "Use the AI workload analysis for signals, features and budget limits.". Buttons: "Read the relevant architecture" → `/resources/read?doc=deepgrid-sku-compendium-architecture`, and "Continue the evaluation" → `/resources/docs`. — `app/route-journey.tsx:35`; [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- "Related products and references": Ask DeepGrid, Technology, Product validation, Products. "The documents behind this page" repeats 3 of the cards (SKU Blueprint, Whitepaper v3, Thirty Use Cases), each with a PDF and "Read in the library". "Continue your review": "Compare product architectures", "Review validation & readiness", "Request a discussion" → `/contact?intent=investor`. — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)

**Counts (main element, 1440px)**
- 25 links to `/downloads/` (PDF, .md, .pptx, .drawio), 14 links to `/resources/read`, 1 .pptx, 1 video player (5 films behind tabs), 9 document cards and 22 images (all with alt attributes). There is exactly 1 in-content contact link ("Request a discussion"). No network 4xx responses and no console errors. — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- There are at least 12 "Ask DeepGrid" controls: 9 per-card buttons, the inline lead link, the "Explore in Ask DeepGrid" CTA and a legacy button. All are `<button>`s using `go('ask')`, not anchors. — `documents-hub.tsx:104,116,242-251`.

### Inferences
- An investor arriving from the "Investors" or "Resources" menu sees an engineering document grid. The card labels are engineering vocabulary ("RTL Specification", "Key architectural proofs", "Spec (.md)"). The investor documents (SKU Blueprint, Whitepaper v3) are not singled out until the related block at the very bottom.
- An engineer is served much better: datasheets, decks, films, diagrams, guides and external standards. Even so, the most technical material (films, diagrams) comes after about 10,000px of cards on mobile.
- Having an "Ask DeepGrid" button on every card dilutes the calls to action. Ask DeepGrid gets roughly 12 entry points, while the discussion/data-room action gets 1 in-page link.

### Gaps
- I did not check analytics or real user paths. Whether investors actually land on /resources is unknown.

## Q2. How does /resources/read work: available documents, in-document navigation, provenance, version/date and evidence level?

### Takeaway
The reader is a client-side Markdown renderer at `?doc=<path>`. It gives an "In this document" table of contents built only from H2 headings, PDF and Markdown file links, and one fixed caveat banner. It has no search, no per-document version or date fields, no evidence-level labels and no document-specific page title. The flagship SKU Blueprint renders with an empty table of contents. A second, separate "Read Spec" modal on /resources shows raw Markdown in a `<pre>` block and exposes an internal file path.

### Cited Findings
**Mechanics**
- `url()` rewrites any `/downloads/*.md` link to `/resources/read?doc=<path without .md>` (`app/routes.ts:15-22`). The old generated `.html` reader pages are now meta-refresh redirects to the in-site reader (`scripts/document-readers.mjs:28-31`).
- The reader fetches `/downloads/<key>.md`. Keys must match `^[\w/-]+$`. It renders Markdown with `marked`, escapes raw HTML, converts inline LaTeX to plain text and rewrites `.md` links to the reader. — `app/doc-reader.tsx:84-95, 15-44, 62-68`.
- The table of contents collects only depth-2 headings (`if (depth === 2) headings.push(...)`) and drops the H1 (`if (depth === 1) return ''`). — `doc-reader.tsx:58-59`.
- Deep links work: headings get slugs, and after rendering the page scrolls to `location.hash`. The guide links such as `#component-safety-core` use this. — `doc-reader.tsx:99-104`.

**Documents tested (all loaded with no 4xx)**

| `?doc=` key | H1 shown | TOC entries | Words | File links |
|---|---|---|---|---|
| docs/deepgrid-dg32-ai-architecture | Thirty Use Cases, No Accelerator | 5 | 836 | PDF · 12 pages + MD |
| docs/deepgrid-sku-blueprint-oct2026 | SKU Blueprint, October 2026 (11 SKUs + D100) | **0** (143 H3, 0 H2) | 11,010 | PDF · 46 pages + MD |
| docs/deepgrid-dshot-rx-architecture | dgrid_dshot_rx RTL Specification | 7 | 1,473 | PDF · 8 pages + MD |
| docs/deepgrid-2dom-architecture | DG32-2DOM Architecture & Block Definition | 7 | 1,210 | PDF · 24 pages + MD |
| docs/deepgrid-mature-silicon-architecture | Mature-Node Silicon for India's Defence (Whitepaper v3) | 8 | 1,389 | PDF · 71 pages + MD |
| docs/deepgrid-datasheets-engineering-spec | Preliminary Engineering Datasheets & Package Pinout | 5 | 1,749 | PDF · 24 pages + MD |
| docs/deepgrid-d100-architecture | D100 Tactical Drone Platform Architecture | 6 | 1,419 | "PDF · pp. 42–44" (whole 46-page blueprint) + MD |
| docs/deepgrid-sdv-architecture | DG SDV Software-Defined Vehicle Zonal Architecture | 5 | 914 | "PDF · in-site document" → links back to the same reader page + MD |
| docs/deepgrid-three-factory-architecture | Three-Factory Sovereign Silicon Architecture | 5 | 1,000 | "PDF · Section 4" (whole 71-page whitepaper) + MD |
| dg32-lite-architecture-guide | DG32-LITE: Architecture Guide | 13 | 1,711 | MD only |
| dg32-2dom-architecture-guide | DG32-2DOM: Architecture Guide | 9 | 1,065 | MD only |
| deepgrid-sku-compendium-architecture | DeepGrid Semi: SKU Architecture Compendium Engineering Specification (Technical Annex v3) | 3 | 1,001 | MD only |

Sources: [L2](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-sku-blueprint-oct2026); [SDV](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-sdv-architecture); [D100](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-d100-architecture); [compendium](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=deepgrid-sku-compendium-architecture). The registry entries behind the PDF links are `documents-data.ts:223,227` (D100), `254,258` (SDV, `pdfFile` is the `.md`) and `285,289` (three-factory).

**Provenance, version, date and evidence level**
- For the 9 registered documents, the H1 is the curated registry title, with the raw source title shown below as a subtitle. For example, the SKU Blueprint shows "DeepGrid Semi: Product Portfolio (SKU Blueprint), October 2026". The guides and the compendium are unregistered, so they show only the raw title and no PDF link. — `doc-reader.tsx:85,123,129-130`.
- Every document gets the same banner: "The source edition, unchanged. Architecture targets, proposals and dated plans are preserved as written; they do not establish measured silicon, qualification or certification. How each figure on this site is graded" (link to /evidence). — `doc-reader.tsx:131`.
- There is no metadata block for version, date, author, status or supersession. Dates and versions appear only where the body text happens to contain them, for example "Draft 1 … Reviewer: Ayaz Khan" in DShot, "v3, Sept 2026" in the whitepaper, "Status: design complete, in physical trials." in the guides, and "October 2026" in the Blueprint. — reader pages above.
- The /resources/docs story says "older documents are marked superseded" (`app/executive-routes.json:98-103`). The reader has no superseded flag. The SKU compendium (Technical Annex v3) renders with no notice that the October 2026 Blueprint replaces it. — [compendium](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=deepgrid-sku-compendium-architecture)
- Evidence level is not tagged inline. The /read route's story text, "Every figure here is a design value, a process nominal or an analytic estimate." (`executive-routes.json:110-115`), does not render on the reader page because `DocReader` does not use `SectionHead`.
- Source text that contradicts the site's pre-silicon position is reproduced without a flag. The three-factory document shows "Status: DONE — Physical working silicon fabricated & validated" for the SkyWater sky130 tier (`/downloads/docs/deepgrid-three-factory-architecture.md` line 30). The evidence route says "No DeepGrid part has measured silicon yet; first silicon is the December 2026 shuttle." (`executive-routes.json:83`). — [three-factory reader](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-three-factory-architecture)

**Navigation and search**
- There is no in-document search, no "back to library" link in the reader body (breadcrumb only), no previous/next document, and no "related documents" list other than the generic `Related` block. — [L2](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-sku-blueprint-oct2026)
- At 390px the TOC is `position: static` above the article, 154–568px tall. On the DG32-LITE guide, 13 entries push the content about 570px down. — reader pages at 390px.
- The breadcrumb reads "Home / Technical references" on every document and does not name the document. — reader pages.

**Duplicate reader: "Read Spec" modal on /resources**
- "Read Spec" does not open /resources/read. It opens a modal that shows the raw Markdown in `<pre>`: unrendered "# …", "## …" and table pipes, with no table of contents and no caveat banner. It offers "Download PDF", "Copy Markdown", ".md", "Ask DeepGrid" and close. — `documents-hub.tsx:224-231,265-358,343`; [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- The modal footer shows an internal build path: "PDF SOURCE: scratch/deepgrid-dr-silicon/public/downloads/docs/deepgrid-dg32-ai-30-use-cases.pdf". — `documents-hub.tsx:350`; observed live.
- If the fetch fails, the modal makes up a Markdown document from card metadata, with headings such as "Executive Summary", "Key Technical Parameters" and "Core Engineering Takeaways" and the line "**Official Source Document:**". A reader could not tell this from the real source. — `documents-hub.tsx:57-73`.

### Inferences
- The in-site reader is the better of the two, but the landing page's main "Read Spec" button goes to the worse one (raw `<pre>`). Only the related-block "Read in the library" links and the guide links reach `/resources/read`.
- The SKU Blueprint is the site's source of record and the largest document (about 11k words). Its empty TOC makes it the hardest document to navigate. The cause is that the source uses H3 for each SKU and the reader only lists H2.
- The banner covers the overall boundary, but individual claims are not graded. A diligence reader cannot see from inside the reader which figures are simulation, post-route, estimate or measured.

### Gaps
- I did not open the PDFs to compare them page by page with the Markdown editions. Whether the ".md" is a faithful "source edition, unchanged" of each PDF is unverified. Several `.md` files (for example "…-architecture.md") look like derived summaries rather than the PDF itself.
- I did not test keyboard focus order or screen-reader output inside the modal.

## Q3. Broken links, empty states, duplicated content, unclear labels and label/title mismatches

### Takeaway
I found no HTTP-broken links. There are several semantic misdirections: a "PDF" that downloads Markdown, a "PDF" that links back to itself, and "PDF" links that are a whole 46- or 71-page source rather than the stated pages. The same section has at least 7 different names across nav, breadcrumb, `<title>` and H1, and some content is duplicated.

### Cited Findings
**Label and title mismatches for the same pages**
- `/resources` is called: route label / breadcrumb "Technical references" (`routes.ts:68`); mega-nav item "Architecture & electrical specifications" (`app/mega-nav.tsx:75`); `<title>` "Resources · DeepGrid Semi" (`app/resources/layout.tsx:4`); H1 "Technical documents, decks and films." (`executive-routes.json:93`); footer and investor journey "Documents, decks & films" (`app/investor-journey.tsx:85`); the reader's empty state "the document library" / "Open the document library" (`doc-reader.tsx:110-111`); and the related block "Read in the library".
- `/resources/docs` is called: route label "Technical specifications" (`routes.ts:69`); mega-nav "Technical specifications & guides" (`mega-nav.tsx:74`); `<title>` "Documentation · DeepGrid Semi" (`app/resources/docs/layout.tsx:4`); and "Continue the evaluation" on /resources.
- `/resources/videos` is called: route label "Product walkthroughs" (`routes.ts:70`); mega-nav "Product & system walkthroughs" (`mega-nav.tsx:76`); and `<title>` "Videos · DeepGrid Semi" (`app/resources/videos/layout.tsx:4`).
- `/resources/read` is called: route label "Technical reference" (singular, `routes.ts:71`); `<title>` "Source document · DeepGrid Semi" for every document (`app/resources/read/layout.tsx:3`), so browser tabs and bookmarks cannot tell documents apart; and kicker "Source document".
- The mega-nav "Resources" group contains Ask DeepGrid (`/ask`), and the active-state match list includes 'ask' (`mega-nav.tsx:72-77`). The legacy view id `library` maps to `/resources` (`routes.ts:109`).
- The mega-nav lists "Architecture & electrical specifications" (/resources) second, after "Technical specifications & guides" (/resources/docs). The /resources H2 is also "Architecture and electrical specifications", while /resources/docs is the one described as holding "Datasheets", even though the datasheet decks are on /resources. — `mega-nav.tsx:74-76`; [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)

**Misleading file links**
- DG SDV card: "Download PDF 8.0 KB" downloads `deepgrid-sdv-architecture.md`, because `pdfFile` is the `.md`. In the reader, "PDF · in-site document" links to the page you are already on. — `documents-data.ts:254-258`; [SDV reader](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-sdv-architecture)
- D100 card: "Download PDF 3.6 MB" is the whole SKU Blueprint. Three-factory card: "Download PDF 5.62 MB" is the whole 71-page whitepaper. Neither link goes to the page or section named. — `documents-data.ts:223-227,285-289`.

**Duplication**
- The SKU Blueprint, Whitepaper v3 and Thirty Use Cases appear twice on /resources: once as cards and again in "The documents behind this page". The DG32 QFN-64 datasheet PDF also appears twice: as DOC #6 and under "Primary sources". — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- "Guide: Safety core" appears twice in the diagram notes (Safety core and Supervision). — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- There are two reader implementations (the modal and /resources/read), and a third is still generated and then voided (`void html`) in `scripts/document-readers.mjs:26-27`.

**Empty states**
- Reader with no key: H1 "Choose a document from the library." Unknown key: "That document is not in the library." Both add "Every source document is listed on the Resources page with its PDF and its readable edition." and a button "Open the document library" → /resources. The unknown key still fires a 404 fetch for `/downloads/nonexistent-doc.md`. — `doc-reader.tsx:106-114`; [no-key reader](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read)
- The empty-state claim that every document has "its PDF" is false for the guides, the compendium and SDV. — `doc-reader.tsx:110`.

**Claims language that conflicts with the site rules**
- The DOC #1 card summary starts "Formal proof that high-accuracy industrial condition monitoring … do not require heavy transformer acceleration". Every card's list is headed "Key architectural proofs". — `documents-hub.tsx:205`; [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- The three-factory card highlights include "Zero-NRE open-source toolchain (OpenLane/Magic/KLayout) validated on test silicon" and "Proof of concept for India's ₹10 Cr sovereign chip initiative". Its stat cell reads "Supply Resilience: Sanction-proof multi-foundry PDKs". — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- The tab label is "Core Silicon Deliverables". `docs/site-story.md:85-88` lists "Authoritative", "Verified", "sovereign supply chain security" and "Client-ready" as language to remove because it "asserts trust instead of showing the source". The card copy has not been brought in line with that rule.
- DOC #1 card stats show "ISO 26262 ASIL-D (target, not certified)", which is correctly qualified. The reader TOC for the same document says "Safety Architecture & Advisory Boundary (ISO 26262 ASIL-D)" with no qualifier. — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/); [doc1 reader](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-dg32-ai-architecture)

**Dead or stale code visible in the source**
- `NUMW` (number words) is declared and unused (`documents-hub.tsx:13`). The `SectionHead` props on /resources are ignored (`app/detail.tsx:14`).

### Inferences
- With 7 or more names for one section, a visitor cannot tell from the menu that "Architecture & electrical specifications" is the page with the films, or that "Technical specifications & guides" is the document catalogue. The DeepGrid docs' own principle, "a route that exists in only one of those is the defect this file exists to prevent" (`routes.ts:1-3`), is not being applied to labels.
- The "Formal proof", "validated on test silicon" and "Status: DONE … validated" wording directly risks the PRODUCT.md rule not to imply measured silicon or production status.

### Gaps
- I did not crawl /resources/docs and /resources/videos in depth, which may be covered by another researcher. I only checked their labels and titles.

## Q4. Does the section lead to the primary action, and is there a "what to read first" path for each audience or goal?

### Takeaway
The primary action ("Request a discussion" → `/contact?intent=investor`) appears once in the page body, as the last of three links at the very bottom, plus the global header button. No data-room or "documents on request" path is offered here. There is only one reading-order aid: a 3-step list ("Use the SKU compendium…", "Use DG32 architecture…", "Use the AI workload analysis…"). It is the same for every audience, unranked by goal, and points at the superseded compendium rather than the October 2026 Blueprint that the site calls the source of record.

### Cited Findings
- In-body contact links on /resources: 1 ("Request a discussion" → `/deepgrid-dr-silicon-v11/contact?intent=investor`, under "Continue your review"). The header has "Request a discussion" and "Contact", and the mega-nav "Investors" group has "Request a discussion: Investment, strategic partnership or data-room enquiry". — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- The /resources route story ends with `"next": "/resources/docs"`, not `/contact`. The /read story also ends with `"next": "/resources/docs"`. The procurement route is the one whose `next` is `/contact`. — `executive-routes.json:92-97,110-115,86-91`.
- The /resources/docs story says "Nine product specifications open to read; 21 more documents on request." (`executive-routes.json:98-103`). /resources and /resources/read have no "request the other 21" or data-room link.
- The only goal-based guidance on /resources is the route-journey box: H2 "The portfolio sets scope, the evidence register sets maturity, the documents set integration detail." with steps 01–03 as quoted in Q1, then "Read the relevant architecture" → `?doc=deepgrid-sku-compendium-architecture`. — `route-journey.tsx:35`; [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- The H1 lead names three starting points ("Start with the portfolio for product scope, the evidence register for maturity, or the detailed documents for integration") but does not link any of them. — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- PRODUCT.md: "Investors and strategic partners are the primary audience (owner, 14 Oct 2026). The primary action is a discussion or data-room enquiry. Equipment-maker engineering remains supported through portfolio, market, technology and source pages." — `PRODUCT.md:8`.
- There is no investor-specific route through the documents (for example Blueprint → Whitepaper financial section → evidence register → request data room). The documents are not ranked by importance for any goal. The "core" filter splits by document family, not by reader goal. — `documents-hub.tsx:126-157`.

### Inferences
- For the stated primary audience, the section is a dead end in practice: about 21,900px of engineering material on mobile, with a single small contact link at the end.
- A goal-ranked "macro learning" path for an investor is missing entirely. The material for one exists: the Blueprint "source of record", the Whitepaper v3 financial model ("8. Financial Model, Capital Waterfall & Stop Rules" in its reader TOC), /evidence and /portfolio/brief.
- Pointing step 01 at the Technical Annex v3 compendium conflicts with the docs-page statement that "The October 2026 SKU Blueprint is the current scope; older documents are marked superseded."

### Gaps
- Contact-page handling of `intent=investor` and any data-room flow was out of scope and not checked.

## Q5. Accessibility and mobile basics

### Takeaway
The basics are sound. Both pages have one H1, a skip link and no horizontal page scroll at 390px. All 22 images on /resources have alt attributes, and the video has captions. The weak points are many navigation controls built as `<button>` instead of links, generic or duplicate link text, and the very long mobile scroll before the media.

### Cited Findings
- /resources at 390px: `scrollWidth` = 390 (no horizontal scroll). Page height is 21,906px. The document hub block is 9,942px tall, and the deck/film section starts at y ≈ 10,615px. There are no visible interactive elements under 24px tall. — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- /resources/read at 390px: `scrollWidth` = 390 for all 12 documents tested. Tables are wrapped in a focusable scroll region (`tabindex="0" role="region" aria-label="Scrollable table"`). — `doc-reader.tsx:74`; [L2](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/read?doc=docs%2Fdeepgrid-sku-blueprint-oct2026)
- One H1 per page. A skip link is present. Heading order on /resources is H1 → H2 → H3 with no skips. — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- Images: 22 in main, 0 missing `alt`. Deck slides have descriptive alt text ("DG32-LITE Architecture deck, slide n: <title>"), and thumbnails have empty alt with an `aria-label` on the button. — `library.tsx:52,55`.
- Video: one `<video>` with `<track kind="captions" … default>`. — `library.tsx:45`.
- Tabs use `role="tablist"`/`role="tab"`, `aria-selected` and roving `tabIndex`. — `documents-hub.tsx:126-157`; `library.tsx:42`.
- Navigation implemented as buttons rather than links: about 12 "Ask DeepGrid" controls, the 9 "Read Spec" buttons and the 7 legacy jump buttons. None can be opened in a new tab or bookmarked. — `documents-hub.tsx:224-251`; `library.tsx:69-79`.
- Generic or repeated link text: 9 × "Download PDF", 9 × "Read Spec", 9 × "Ask DeepGrid" and 3 × "Read in the library". Screen-reader link lists cannot tell them apart. The card `title` attributes are not reliable accessible names. — [L1](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/)
- The modal reader has `role="dialog" aria-modal="true"` and closes on Escape. It shows content in `<pre>`, which does not reflow at 390px. I did not inspect whether focus is trapped or returned. — `documents-hub.tsx:266-273,78-86`.
- The reader has no document-specific `<title>`: all documents are "Source document · DeepGrid Semi" (`read/layout.tsx:3`).

### Inferences
- Swapping the buttons for anchors on navigation controls, and adding document names to repeated link labels (for example "Download PDF: SKU Blueprint"), would fix most of the accessibility weaknesses.
- On mobile, putting a short "read first" list or a collapsible card list above the 9 full cards would cut the roughly 10,000px of scrolling before the films.

### Gaps
- I did not run axe-core or check colour contrast, so contrast and full WCAG results are unverified.
- Focus management in the modal and the keyboard behaviour of the slide strip were not exercised.
