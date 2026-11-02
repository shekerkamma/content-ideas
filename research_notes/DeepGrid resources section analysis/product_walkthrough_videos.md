# Product walkthroughs: DeepGrid Semi video library audit (as of 2026-11-02)

Scope: live page https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/videos (rendered with Playwright 2026-11-02, HTTP 200, title "Videos · DeepGrid Semi"), the read-only clone at `/home/user/shekerkamma/deepgrid-dr-silicon-v11` (HEAD 4103fd7, 2026-10-27), YouTube oEmbed for all 41 ids, YouTube watch-page descriptions/transcripts via Exa fetch, and view counts from the Return YouTube Dislike (RYD) public API. File:line refs are relative to the clone.

## Q1. Full inventory: id, title, duration, row, short/long, transcript, narration

### Takeaway
The page holds 51 items: 10 self-hosted animated "part films" plus 41 YouTube videos (28 long-form in 7 topic rows, 13 Shorts in one row). Only 11 of 41 YouTube videos carry a transcript (all 10 films do), so 21 of 51 cards show the "Transcript" badge. Most of the ADAS, mirror and D-Drive demos have no narration.

### Cited Findings
- Live page counts: "51 videos", with these chips: Part films 10, Silicon & Architecture 8, Autonomous Driving: ADAS 8, Smart Mirror: D-Mirror 3, Autonomous Mobility: D-Drive 5, Humanoid: Apexgrid 1, Company 2, Engineering tools 1, Shorts 13. There are 51 cards and 21 "Transcript" badges. Source: [live page](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/videos), Playwright DOM read 2026-11-02.
- Data model: each video has `id, title, text?, secs?, short?` (app/resources-data.ts:9). Rows come from `videoGroups` (app/resources-data.ts:68-81) and `shortGroups` (app/resources-data.ts:82-86). Films come from `explainers` (app/explainers.ts:11-22) and are prepended as "Part films" (app/video-library.tsx:234-238).
- Transcript presence: `public/transcripts/index.json` lists 11 ids: -0YJvIQHIA8, 75G6kkpDopw (hi), AOaSVtRbvRk, Bw34e4sx144, FD2xhoQYwKA, HBLdDD5Vm9k, KFQ4EHIeZnk, VYNbuuYrXSg, b4VFlC5GDzY, i_5wXj0lHmM, io4zmbFq1MM. The badge logic is at app/video-library.tsx:45 and :75-76. Without a transcript the player says "This video has no narration, so there is no transcript." (app/video-library.tsx:178).
- The transcript builder rejected some tracks on purpose. -iY2KLMsZqw (Follow-Me) is "48 scattered words in two scripts… Silero finds no speech in 654 s", and eCAw60kV01Q was also rejected (scripts/build-video-transcripts.py:32-34).

Inventory. "Tr" means a transcript exists. "Narr" is narration as heard in the transcript or YouTube's auto-text.

| # | Row (site) | id | Site title | Dur. | Long/Short | Tr | Narr / content note |
|---|---|---|---|---|---|---|---|
| 1-10 | Part films | sku-1…sku-9, d100 | e.g. "One die runs the motor loop and drives its 120 V power stage" | 1:04–1:30 | long | yes (VTT) | Narrated animated mechanism films, "Pre-silicon; every figure is a design target" (app/explainers.ts:12-21; app/video-library.tsx:197) |
| 11 | Silicon | Bw34e4sx144 | DG32-LITE, looking at the die: 3.9 × 3.9 millimetres | 2:42 | long | yes | Narrated GDS tour; ends "signed off and prepared for shuttle tape in" (transcript) |
| 12 | Silicon | b4VFlC5GDzY | Anatomy of our chip (DG32-2DOM): 13 words from a real tape-out | 11:21 | long | yes (116 lines) | Narrated explainer |
| 13 | Silicon | bJOUUJhwa9w | DG32-LITE: dual-core lockstep RISC-V safety MCU, laid out | 1:21 | long | no | none/unknown |
| 14 | Silicon | 4ZVohoOoesE | DG32-LITE: GDSII view | 2:00 | long | no | none |
| 15 | Silicon | VYNbuuYrXSg | Why the DG32-2DOM's power never reached the wrapper, and how Wrapalign fixed it | 2:44 | long | yes | Narrated failure-and-fix story |
| 16 | Silicon | HBLdDD5Vm9k | SAR guard ring latch-up | 3:21 | long | yes | Narrated; says "This chip has never been fabricated" |
| 17 | Silicon | 8Y6m7UTAZXY | DG32-LITE die (without narration) | 2:42 | long | no | silent duplicate of #11 |
| 18 | Silicon | FD2xhoQYwKA | Inside the DGRID Softmax ENGINE Accelerator | 2:48 | long | yes | Founder-style narration over the Sky130 layout |
| 19 | ADAS | qBHUWiiw4Po | Live ADAS Demo on Hyderabad City Roads | 19:12 | long | no | none |
| 20 | ADAS | Kn9Q4THjG6c | DGRID-ADAS: Lane Detection & Collision Warning | 1:49 | long | no | none |
| 21 | ADAS | 0rEnXT__B7M | Indian Road Driving Test: Scenario 2 | 3:37 | long | no | none |
| 22 | ADAS | x7pi4APnNik | Indian Driving: ADAS Test 3 | 3:42 | long | no | none |
| 23 | ADAS | 5YDEm77Tndc | Indian Driving: Model Output | 3:42 | long | no | none |
| 24 | ADAS | vjA720O8RcE | End-to-End Driving on nuScenes | 0:09 | long (9 s) | no | none |
| 25 | ADAS | UaNaELUh1JM | End-to-End Architecture on the Waymo Dataset | 0:20 | long (20 s) | no | site text calls it "narrative walkthrough", but there is no transcript |
| 26 | ADAS | aSZdrH3EerY | End-to-End Driving Trained in CARLA | 0:10 | long (10 s) | no | none |
| 27 | Mirror | JnnzI768PZ8 | AD0 AI Smart Mirror with Thermal Vision | 0:22 | long | no | none |
| 28 | Mirror | gGoUd4a-DLw | AD0 AI Smart Mirror (D-Mirror) Demo | 1:06 | long | no | none |
| 29 | Mirror | Bx9gC9iW99k | Real-Time ADAS Alerts on D-Mirror | 1:06 | long | no | none |
| 30 | D-Drive | -iY2KLMsZqw | D-Drive: Follow-Me Mode | 10:55 | long | rejected | ambient chatter only |
| 31 | D-Drive | fvz-Uhi8vhU | D-Drive: 360° Turn (Field Test 1) | 0:30 | long | no | none |
| 32 | D-Drive | knNspgTt7rM | D-Drive: BEV Perception | 0:07 | long (7 s) | no | none |
| 33 | D-Drive | pmIK4nGp5xg | D-Drive: Autonomous Steering Control | 0:13 | long | no | none |
| 34 | D-Drive | mRvephRowgc | D-Drive moving autonomously after slamming | 2:19 | long | no | none |
| 35 | Humanoid | i_5wXj0lHmM | Apexgrid doing a basic yoga exercise | 3:27 | long | yes | Hindi/English operator commentary; robot called "Paricharak/Paracharak" |
| 36 | Company | AOaSVtRbvRk | Aravind Prasad, Director, DeepGrid Semi, with T-Hub | 3:31 | long | yes | Founder interview |
| 37 | Company | -0YJvIQHIA8 | deepgridsemi.com | 1:54 | long | yes | Founder intro over the website |
| 38 | Eng. tools | CKDsqkh1eZA | Our PCB engine, live: autoroute and auto-placement | 1:15 | long | no | none |
| 39-44 | Shorts | KFQ4EHIeZnk (Tr), gevSbk7C50M, SX-Nvnv5Dhg, fI0cZ8k1fWs, eCAw60kV01Q, 75G6kkpDopw (Tr, Hindi, 1 line) | Apexgrid calibration / salute / fast salute / lawn ×2 / arms | Short | short | 2 of 6 | operator commentary |
| 45-48 | Shorts | t2EvO403h0k, hZWILGZ-mnY, Rnl7k74dVaE, io4zmbFq1MM (Tr) | D-Drive 360°, drivetrain fwd, back; D-Base Alpha v1 | Short | short | 1 of 4 | D-Base is narrated (AMR waypoint demo) |
| 49-51 | Shorts | fAoHp7WnTuY, svS1tD3uY_g, qG8XNHRXZWk | Retrofit ADAS; ADAS L1; Western vs Indian roads | Short | short | no | none |

Durations come from `secs` in app/resources-data.ts:18-59. Shorts carry no `secs` and display "Short" (app/video-library.tsx:21).

### Inferences
- The narrated, transcript-backed half of the library is almost entirely silicon and company content. Every ADAS, D-Mirror and D-Drive demo except D-Base is a silent screen capture. An investor gets no voiceover saying what is being shown or what it runs on.
- 7 "long-form" items run 7–30 s (#24-27, #31-33). In practice they are clips and sit oddly beside an 11-minute explainer.

### Gaps
- Narration status for non-transcript videos (#13, #14, #38) was inferred from the absence of captions. I did not watch them frame by frame.

## Q2. YouTube data: channel, views, ranking, outliers

### Takeaway
All 41 YouTube videos are on one channel, @DeepgridSemi ("Deepgrid — Semiconductors - Systems - Sentience."). Views are very low: median about 52 and mean about 133 across the 32 videos with data. The clear outliers are robotics and mirror Shorts, not silicon. The D-Drive 360° Short (1,213) and D-Base Alpha v1 (759) together hold 46% of the counted views. Subscriber count could not be obtained.

### Cited Findings
- oEmbed returns author_url `https://www.youtube.com/@DeepgridSemi` for all 41 ids. Example: [oEmbed Bw34e4sx144](https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=Bw34e4sx144&format=json). The site's own comment says the channel is UCNhzSUQYxiL7lGdzxMRwNvA and that "all 28 ids match" (app/resources-data.ts:7), which is now stale because 41 ids are listed.
- YouTube watch pages returned HTTP 302 to google.com/sorry (bot wall) from this host, so view counts, upload dates and subscriber counts could not be read from YouTube directly. The channel /about page returned empty via Exa. Upload dates are unknown. The site itself says "The channel carries no upload dates or view counts, so these are editorial picks" (app/resources-data.ts:64).
- View counts below come from the [RYD API](https://returnyoutubedislikeapi.com/votes?videoId=Bw34e4sx144), queried 2026-11-02. They are RYD's cached view counts, so they may lag YouTube. 9 ids had no RYD record (RYD returned 0 and first-seen = today), so they are unknown, not zero: 0rEnXT__B7M, x7pi4APnNik, Bx9gC9iW99k, pmIK4nGp5xg, SX-Nvnv5Dhg, 4ZVohoOoesE, VYNbuuYrXSg, HBLdDD5Vm9k, mRvephRowgc.

Ranked by views (RYD). The ×median column is views ÷ median 52.

| Rank | id | YouTube title (oEmbed) | Views | Likes | ×median |
|---|---|---|---|---|---|
| 1 | t2EvO403h0k | D-Drive 360° Movement \| DeepGrid Semi (Short) | 1,213 | 6 | 23× |
| 2 | io4zmbFq1MM | D-Base Alpha v1 (Short) | 759 | 8 | 15× |
| 3 | JnnzI768PZ8 | AD0 : AI Smart Mirror ADAS with Thermal Vision \| See Through Glare in Real-Time | 442 | 2 | 8.5× |
| 4 | fAoHp7WnTuY | "Deepgrid ADAS: LDWS, FCWS, LKAS, Over-Speeding & Traffic Sign Alerts \| Dgrid Retrofit (Short) | 174 | 0 | 3.3× |
| 5 | b4VFlC5GDzY | Anatomy of our chip (DG32-2DOM) — 13 words from a real silicon tape-out, explained! | 166 | 4 | 3.2× |
| 6 | hZWILGZ-mnY | D-Drive Drivetrain Testing Alpha Test1:Moving Forward Successful | 160 | 4 | 3.1× |
| 7 | FD2xhoQYwKA | Inside DGRID Softmax ENGINE Accelerator: 3D Chip Layout on Sky130 | 158 | 2 | 3.0× |
| 8 | fI0cZ8k1fWs | Apexgrid in lawn moving and saluting 1 | 113 | 0 | 2.2× |
| 9 | aSZdrH3EerY | End-to-End autonomous driving architecture trained in the CARLA simulator | 103 | 0 | 2.0× |
| 10 | qBHUWiiw4Po | Ad0 Live Demo on Hitech City Roads in Hyderabad \| Thermal Vision + Real-Time Driving Suggestions | 68 | 3 | 1.3× |
| 11-32 | others | gevSbk7C50M 63; UaNaELUh1JM 62; 75G6kkpDopw 62; Rnl7k74dVaE 62; qG8XNHRXZWk 55; KFQ4EHIeZnk 54; Kn9Q4THjG6c 50; AOaSVtRbvRk 49; vjA720O8RcE 45; gGoUd4a-DLw 42; eCAw60kV01Q 42; Bw34e4sx144 39; 5YDEm77Tndc 38; i_5wXj0lHmM 34; svS1tD3uY_g 33; -0YJvIQHIA8 31; -iY2KLMsZqw 27; CKDsqkh1eZA 26; bJOUUJhwa9w 25; 8Y6m7UTAZXY 24; fvz-Uhi8vhU 21; knNspgTt7rM 21 | | | |

- Sum of counted views = 4,261 across 32 videos, so the mean is about 133 and the median 52 (computed from the RYD data above).
- RYD "first seen" dates only roughly bound the upload dates: qG8XNHRXZWk 2024-12-29, fAoHp7WnTuY 2025-08-02, io4zmbFq1MM 2025-12-09, the DG32 die videos 2026-09-11/13/14/15. These are not upload dates. [RYD API](https://returnyoutubedislikeapi.com/votes?videoId=qG8XNHRXZWk)
- The YouTube titles differ from the site titles and are rougher, with typos: "Wtth Voice" (Bw34e4sx144), "agressive" (75G6kkpDopw), "Excercise" (i_5wXj0lHmM), "slaming" (mRvephRowgc), a stray leading quote on fAoHp7WnTuY, "001 Steering Control Not Driving" (pmIK4nGp5xg), and "DGRID-ADAS"/"DDRIVE-BEV" as bare codes. Source: oEmbed per id, e.g. [oEmbed 75G6kkpDopw](https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=75G6kkpDopw&format=json).

### Inferences
- The channel's outliers are physical robots moving (D-Drive carrying three people, the D-Base AMR) and a visual thermal claim ("See Through Glare"). The audience that views is drawn to tangible motion. The investor-critical silicon content sits at or below channel median, except "Anatomy…" (3.2×) and Softmax (3.0×).
- Absolute numbers are tiny. "Outlier" is a within-channel signal only and does not show traction. Do not cite these counts externally as traction.

### Gaps
- Subscriber count, true upload dates and current YouTube-side view counts were blocked by YouTube's bot wall from this host. With a logged-in browser or the YouTube Data API, the views ÷ subscribers lens could be computed.
- The 9 videos with no RYD record have unknown views.

## Q3. Evidence clarity: hardware and evidence level per demo

### Takeaway
The silicon films and the part films are honest about pre-silicon status, and some are exemplary: the latch-up narration says "This chip has never been fabricated". The road and robot demos are not. The flagship "Start here #1" says the Hitech City demo ran "with the DG-A100", a part that exists only as an "on request" datasheet. YouTube's own description says it is "Ad0" running CLRerNet + YOLOv26n "on embedded hardware", tagged "FPGA AI". No demo card names the actual compute hardware or the evidence level.

### Cited Findings
- Hitech City demo (qBHUWiiw4Po), site text: "Thermal vision and real-time perception running live on Hitech City roads with the DG-A100." (app/resources-data.ts:18). It is item 1 of "Start here" (app/resources-data.ts:66; live page "1 Live ADAS Demo on Hyderabad City Roads Autonomous Driving · 19:12").
- The same video's YouTube description says: "Ad0 combines lane detection (CLRerNet) and object detection (YOLOv26n) into a unified system ready for edge deployment… End-to-end system performance on embedded hardware". Tags include "FPGA AI". It never mentions DG-A100. [YouTube qBHUWiiw4Po](https://www.youtube.com/watch?v=qBHUWiiw4Po)
- "DG-A100 ADAS SoC" appears on the docs page only as an item without a file, which renders as "On request" (app/resources-data.ts:97, :114). The only DG-A100 mentions in app/*.ts are in resources-data.ts (grep). **Highest-risk item: an investor would read this as DeepGrid silicon running on the road.**
- The founder (T-Hub video AOaSVtRbvRk) says that in "2022 ending we first did the test in a FPGA… color conversions, motion detection, optical flow analysis, object detection", that they compared against "a 28 nanometer FPGA board", and that "we are planning to tape out using TSMC in 2025. our chipset will be out". The architecture he describes has "28 cores", which is a different design from DG32 (transcript public/transcripts/AOaSVtRbvRk.json; [YouTube](https://www.youtube.com/watch?v=AOaSVtRbvRk)). This is "Start here #4", and as of 2026-11-02 it carries a stale, unmet forward claim (TSMC 2025 tape-out) plus an unqualified Nvidia comparison.
- D-Mirror thermal (JnnzI768PZ8). The YouTube description says "Thermal + RGB sensor fusion" and names no hardware. The D-Mirror demo (gGoUd4a-DLw) says "Radar and camera sensor fusion… Edge computing for ultra-low latency alerts" with no hardware named ([YouTube JnnzI768PZ8](https://www.youtube.com/watch?v=JnnzI768PZ8), [YouTube gGoUd4a-DLw](https://www.youtube.com/watch?v=gGoUd4a-DLw)). The site row lede describes the mirror as a product ("turns the rear-view mirror into a live ADAS display") with no evidence level (app/resources-data.ts:73).
- The ADAS row lede says the end-to-end stack "powers them on CARLA, Waymo, and nuScenes" (app/resources-data.ts:71). Those three clips are 9–20 s long and are dataset or simulator results (app/resources-data.ts:23-25). The lede does not say whether the road tests ran on the same stack or on what compute.
- Retrofit Short (fAoHp7WnTuY), YouTube: "Dgrid's ADAS Retrofit Kit brings advanced safety features to existing vehicles… LKAS (Lane Keep Assist System) – Assists in steering" ([YouTube](https://www.youtube.com/watch?v=fAoHp7WnTuY)). This is product-marketing language implying a shipping kit. The site shows only the title (app/resources-data.ts:55).
- Softmax (FD2xhoQYwKA). Site text: "the silicon behind the DG-R100 accelerator" (app/resources-data.ts:26). On the docs page, DG-R100 is a "Radar SoC" (app/resources-data.ts:97), which is internally inconsistent. The narration calls it "a small layout and small tape out" with "DRC is zero and LVS is clean" ([YouTube](https://www.youtube.com/watch?v=FD2xhoQYwKA)). "Tape out" without a fab or measured-silicon qualifier can be read as fabricated.
- DG32 die (Bw34e4sx144, featured hero). The narration opens "our full 130 nanometer riskv microcontroller die running live in our proprietary GDS2 silicon inspection engine" and closes "signed off and prepared for shuttle tape in". It is correctly pre-silicon at the end, but "die running live" in the first sentence could mislead (public/transcripts/Bw34e4sx144.json).
- "Anatomy of our chip" (b4VFlC5GDzY). The title says "from a real tape-out" (site) or "a real silicon tape-out" (YouTube). The narration says "explained on a real 2.9 by 4.5 mm silicon die" and "The die is the piece of silicon we get back" (public/transcripts/b4VFlC5GDzY.json, lines at 1 s and 39 s). Together these imply fabricated silicon exists.
- Good practice. The latch-up narration says "This chip has never been fabricated. So we cannot argue that it worked before." (public/transcripts/HBLdDD5Vm9k.json). Wrapalign says "Chip Foundry caught it. Our 26 green sign-off modules had not." ([YouTube VYNbuuYrXSg](https://www.youtube.com/watch?v=VYNbuuYrXSg)). The part-film dialog shows "Animations illustrate; they are not simulations. Pre-silicon; every figure is a design target." with links to the product page and Evidence register (app/video-library.tsx:197-201). YouTube cards get only `v.text` and no such caveat or evidence link (app/video-library.tsx:195).
- The humanoid is named "Apexgrid" on the site, but the operator's narration calls it "Paricharak/Paracharak" (public/transcripts/KFQ4EHIeZnk.json, i_5wXj0lHmM.json). The page does not say what compute drives it or how it relates to DeepGrid silicon.
- D-Drive and D-Base: the descriptions cover the platform, e.g. "carrying three people on board… Built in India" ([YouTube t2EvO403h0k](https://www.youtube.com/watch?v=t2EvO403h0k)). Neither the site nor YouTube names the compute hardware.

Evidence-level classification. This is my reading of the cited text, not a DeepGrid statement.

| Video(s) | Stated hardware | Evidence level actually shown | Misleading risk |
|---|---|---|---|
| Hitech City (qBHUWiiw4Po) | Site: DG-A100. YT: "embedded hardware", FPGA tag | Third-party models (CLRerNet, YOLO) on unnamed embedded/FPGA hardware | **High** |
| T-Hub founder (AOaSVtRbvRk) | FPGA (28 nm board) | FPGA, 2022–23; stale TSMC-2025 plan | **High** (stale forward claim) |
| Anatomy (b4VFlC5GDzY) | DG32-2DOM | sky130 layout/GDS (pre-silicon) | **Medium-high** ("real silicon die… we get back") |
| Softmax (FD2xhoQYwKA) | "DG-R100" (conflicts with docs) | Sky130 block layout, DRC/LVS clean | Medium ("small tape out", wrong SKU) |
| Retrofit / ADAS L1 / Western (Shorts) | none | Unnamed hardware; product-kit language | Medium |
| D-Mirror ×3 | none | Unnamed edge hardware; sensor-fusion claims | Medium |
| ADAS scen2/test3/modelOut/DGRID-ADAS | none | Model output on recorded road footage | Medium (no hardware stated) |
| nuScenes/Waymo/CARLA | none | Dataset/simulator | Low-medium (label it "dataset/sim") |
| DG32 die tour, lockstep, GDSII | DG32-LITE | sky130 GDS, signed off for shuttle | Low (title fine; "running live" wording) |
| Latch-up, Wrapalign | DG32 analog / 2DOM | Layout verification findings | Low (exemplary) |
| Part films ×10 | design targets | Animation | Low (caveated) |
| D-Drive, D-Base, Apexgrid, PCB engine | none | Robot/platform/tool demos | Low-medium (unrelated to silicon; not said) |

### Inferences
- The library mixes three evidence universes without labelling them: (a) DG32 pre-silicon layout, (b) the earlier AI-accelerator, FPGA and third-party-model ADAS work, and (c) robotics platforms. An evidence-level badge on each card ("Layout (sky130, pre-silicon)", "FPGA / third-party SoC", "Dataset/sim", "Robot platform") would fix most of the risk at low cost. The card already supports badges (app/video-library.tsx:44-45).
- The DG-A100 claim on Start here #1 should be removed or corrected before any investor sees it.

### Gaps
- I could not confirm what hardware actually ran the road, mirror or D-Drive demos. The YouTube descriptions do not say, beyond "embedded" and "FPGA AI" tags. The founder would need to confirm.
- I did not visually inspect the frames for on-screen hardware (e.g. a Jetson or FPGA board in shot).

## Q4. Library structure, order, what plays first, purpose, calls to action

### Takeaway
The page leads with a strong evidence-oriented headline about the part films. It then features a silent-free but niche 2:42 DG32 die tour and offers a "Start here" of four legacy videos that undercut that framing: a 19-minute silent road demo, a 22-s mirror clip, an 11-minute Follow-Me video with no narration, and the stale T-Hub interview. It has no 2-minute company overview, no founder walkthrough of the current DG32 plan, and no hardware or evidence legend.

### Cited Findings
- Breadcrumb "Home / Technical references / Product walkthroughs". H1: "Ten narrated part films, plus the DG32 fault path in 1 min 26 s." Context: "The films explain the proposed jobs and mechanisms across the portfolio. Use them to build context, then use the source documents and evidence register for a decision." Source: [live page](https://shekerkamma.github.io/deepgrid-dr-silicon-v11/resources/videos); app/executive-routes.json:104-109 (decision line: "The films illustrate mechanisms; measured figures live in the evidence register."; next: /evidence).
- Featured hero = DG32-LITE die (narrated, 2:42) (app/resources-data.ts:65; app/video-library.tsx:248-261). "Start here: one film per product line" = Hitech (19:12), mirror (0:22), Follow-Me (10:55), T-Hub (3:31) (app/resources-data.ts:66; live DOM). The code comment calls these "editorial picks" (app/resources-data.ts:64).
- Row order: Part films → Silicon & Architecture → ADAS → D-Mirror → D-Drive → Humanoid → Company → Engineering tools → Shorts (live DOM; app/video-library.tsx:234-238).
- The Silicon row lede is "Go inside our AI accelerators: chip floorplanning, compute engines, and the silicon design behind ultra-low-power inference at the edge." (app/resources-data.ts:69). That is legacy AI-accelerator copy over a row that is mostly the DG32 motor-control/safety MCU.
- CTAs: "Subscribe to the DeepGrid Semi channel" (external; app/video-library.tsx:295), then a CTA block "The 104-slide portfolio, narrated end to end, and the silicon films." with "Narrated decks & films" → /resources and "Documentation" → /resources/docs (app/company-pages.ts, videos entry). Only part-film dialogs link to the Evidence register (app/video-library.tsx:200). There is no contact or "book a technical briefing" CTA on this page.
- The player keeps visitors on-site (youtube-nocookie embed, transcript beside the video, "Up next" from the same row) (app/video-library.tsx:1-5, 160-215). Search covers titles and descriptions only (app/video-library.tsx:231), not transcripts.

### Inferences
- What is missing for investors and partners:
  - a ≤2-minute company overview: problem, the DG32 wedge, evidence status and the ask
  - a founder walkthrough of the current plan, replacing the stale 2023-era T-Hub clip
  - an "evidence ladder" film or legend: layout → shuttle → measured
  - a customer or partner use-case film for one SKU
  - a "what is NOT yet proven" summary. The part films do this per SKU, but there is no library-level version.
- What is missing for engineers:
  - a narrated walkthrough of the lockstep/fault path on GDS (the film exists only as an animation)
  - a sign-off/verification flow film (the open EDA flow and the 26 sign-off modules)
  - a datasheet or pinout walkthrough
  - narration or transcripts for the silent lockstep and GDSII videos
  - transcript search
- Start here should match the H1. It should lead with a part film (e.g. SKU-4 fault path, 1:26), the DG32 die tour, Wrapalign (a candid failure-and-fix story builds credibility with technical partners) and a new overview. The legacy road and robot demos belong in a clearly labelled "Earlier platform work" section.
- The Shorts row and robotics rows dilute a semiconductor-investor page. They are the channel's best performers, so keep them on the channel, but de-emphasize or label them on the site.

### Gaps
- There is no analytics on which on-site videos get played. Site behaviour data was not available.

## Q5. Title packaging scored against the KJ Rainey lens, and sharper titles

### Takeaway
Measured against the lens (written for the viewer, a hook word such as a number, result or surprise, ≤~50 characters, thumbnail says one thing in ≤3 words), most titles are internal labels. Examples are "D-Drive: BEV Perception", "SAR guard ring latch-up" and "deepgridsemi.com". The silicon storytelling titles ("Anatomy…13 words", "Wrapalign") have hooks but run 62–79 characters. Thumbnails are YouTube's auto `hqdefault` frames, not designed thumbnails.

### Cited Findings
- Thumbnails on the site are `https://i.ytimg.com/vi/<id>/hqdefault.jpg` (or `sddefault` for the hero), so they are whatever the channel set. The site overlays duration, a topic badge and a Transcript badge (app/video-library.tsx:22, 40-45). The films use their own posters (app/explainers.ts:8).
- Site-title character counts (from app/resources-data.ts titles). Over 50: Wrapalign 79, Retrofit 73, Die (no narration) 72, Anatomy 62, Western 62, Lockstep 57, DG32 die 52, T-Hub 51. Under 25 and label-like: deepgridsemi.com 16, D-Base Alpha v1 15, ADAS L1 in action 17, Salute by Apexgrid 18, GDSII view 21, SAR guard ring latch-up 23, Follow-Me 23, BEV 23.
- The channel's top performers have a concrete physical result in the title: "360° Movement" (1,213), "See Through Glare in Real-Time" (442). "13 words… explained!" (166) is the best silicon performer (RYD data, Q2).

Scoring: V = viewer-centred, H = hook (number/result/surprise), L = ≤50 characters, C = claim-safe. One point each, 0–4.

| Title (site) | V | H | L | C | Score |
|---|---|---|---|---|---|
| Live ADAS Demo on Hyderabad City Roads | 0 | 1 | 1 | 0 (DG-A100 text) | 2 |
| AD0 AI Smart Mirror with Thermal Vision | 0 | 0 | 1 | 1 | 2 |
| Anatomy of our chip (DG32-2DOM): 13 words from a real tape-out | 1 | 1 | 0 | 0 | 2 |
| Why the DG32-2DOM's power never reached the wrapper… | 1 | 1 | 0 | 1 | 3 |
| SAR guard ring latch-up | 0 | 0 | 1 | 1 | 2 |
| DG32-LITE: GDSII view | 0 | 0 | 1 | 1 | 2 |
| DG32-LITE: dual-core lockstep RISC-V safety MCU, laid out | 0 | 0 | 0 | 1 | 1 |
| D-Drive: BEV Perception | 0 | 0 | 1 | 1 | 2 |
| D-Drive: Follow-Me Mode | 0 | 0 | 1 | 1 | 2 |
| deepgridsemi.com | 0 | 0 | 1 | 1 | 2 |
| Aravind Prasad, Director, DeepGrid Semi, with T-Hub | 0 | 0 | 0 | 0 (stale claims) | 0 |
| DGrid retrofit ADAS: LDWS, FCWS, LKAS… | 0 | 0 | 0 | 0 (kit implied) | 0 |
| Indian Driving: ADAS Test 3 / Model Output / Scenario 2 | 0 | 0/1 | 1 | 1 | 2 |
| End-to-End Driving on nuScenes / CARLA | 0 | 0 | 1 | 1 | 2 |

Proposed replacements for the weakest 8. Each is ≤50 characters, framed for the viewer, and stays inside the claims constraints. A 3-word thumbnail text is in brackets.
1. Hitech City demo → "19 minutes of Hyderabad traffic, thermal ADAS" (45) [THERMAL, LIVE TRAFFIC], with the card text changed to "Third-party models on prototype hardware; not DeepGrid silicon." Drop "DG-A100".
2. Anatomy → "13 chip words, explained on our DG32 layout" (43) [13 CHIP WORDS]. Replace "real tape-out/silicon die" with "layout".
3. Wrapalign → "The power bug our 26 sign-off checks missed" (43) [26 CHECKS MISSED]
4. SAR latch-up → "One missing via could have killed this chip" (43) [ONE MISSING VIA]. The narration already supports "never fabricated".
5. Lockstep → "Two RISC-V cores checking each other, laid out" (46) [TWO CORES, ONE ANSWER]
6. DG32 die → "A 3.9 mm safety MCU, layer by layer" (35) [3.9 MM DIE]. Change the narration or card text from "running live" to "in our layout viewer".
7. T-Hub founder → remove from Start here, or retitle "Where DeepGrid started: the 2023 FPGA work" (42) [WHERE WE STARTED] with a dated caveat. Better: replace it with a new "DeepGrid in 2 minutes" overview.
8. D-Mirror thermal → "Seeing through headlight glare with thermal" (43) [SEE THROUGH GLARE]. Card text should name the hardware and its evidence level.
- Honourable mentions: "deepgridsemi.com" → "Meet the founder in 2 minutes" (only if the content is refreshed); "D-Drive: BEV Perception" (7 s) → merge it into a single D-Drive reel rather than retitle.

### Inferences
- The lens and the claims constraint mostly align. Number hooks taken from real design data (3.9 mm, 26 checks, 13 words, one via) are both clickable and verifiable. The risk lies in result-style hooks ("works on the road") that imply silicon status.
- Investors don't search YouTube for DG32. The lens matters more for the channel, which reaches engineers and partners, than for the on-site library, where the clarity of the evidence label should take priority over the hook.

### Gaps
- I could not assess the custom thumbnails YouTube serves (maxres variants) or click-through rates. That needs YouTube Studio data.
