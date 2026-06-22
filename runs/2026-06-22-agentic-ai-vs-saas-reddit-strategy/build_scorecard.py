#!/usr/bin/env python3
"""Agent Replacement Scorecard asset (interactive HTML + CSV) — Top 25 with expandable prose detail."""
import csv, html, pathlib

RUN = pathlib.Path("/home/shekerk/content-ideas/runs/2026-06-22-agentic-ai-vs-saas-reddit-strategy")

# Each row: dict with compact fields + prose detail (pd = proof detail, sd = SaaS detail)
R = [
 dict(n=1,at="Customer",uc="Conversational support",proof="Mercedes MBUX, Wendy's FreshAI, Home Depot Magic Apron",
   saas="Per-seat help desks (Zendesk)",vol="H",det="H",moat="L",verd="REPLACE",bvb="80 support seats → 1 agent + KB",
   pd="Mercedes-Benz routes drive-time questions through its MBUX Virtual Assistant (Gemini on Vertex AI); Wendy's FreshAI takes drive-thru orders end-to-end; Home Depot's “Magic Apron” and Macy's “Ask Macy's” resolve product and order questions in-app. These are live, branded tier-1 agents already handling the bulk of routine contacts — not pilots.",
   sd="The exposed layer is the per-seat help desk (Zendesk-class) plus QA-scoring tools and the lower tier of BPO. Once an agent resolves ~80% of volume, the buyer stops paying for ~80% of the agent seats and the remaining staff become escalation managers. The ticketing system of record can survive — the seat count is what collapses, which is why this is a clear Replace."),
 dict(n=2,at="Customer",uc="In-product owner assistant",proof="Volkswagen myVW, GM OnStar",
   saas="Manuals / FAQ / deflection tools",vol="M",det="M",moat="M",verd="RENEGOTIATE",bvb="Keep platform; drop deflection seats",
   pd="Volkswagen's myVW app lets owners ask “how do I change a flat tire?” and point a phone camera at dashboard lights for multimodal answers; GM's OnStar assistant interprets driver intent by voice. The manual and support content is embedded directly into the product experience.",
   sd="This enriches more than it replaces — the value sits in proprietary product data, so the OEM keeps the platform. What erodes is spend on standalone FAQ / knowledge-base tools and call-deflection add-ons, now folded into one in-product agent. Verdict leans Renegotiate: keep the system, drop the bolt-ons."),
 dict(n=3,at="Customer",uc="AI shopping / sales consultant",proof="Mercedes smart sales, Mobiauto, Best Buy",
   saas="Guided-selling SaaS",vol="H",det="M",moat="L",verd="REPLACE",bvb="Guided-selling seats → 1 agent",
   pd="Mercedes-Benz added a gen-AI smart sales assistant to its online storefront; Mobiauto's “Shopping Consultant” (Gemini + BigQuery) recommends the ideal car and auto-generates listings; Best Buy uses conversational agents for guided product selection. The agent does the consultative selling a human associate or a guided-selling tool used to script.",
   sd="Guided-selling and product-recommendation SaaS — the per-seat configure / quote and merchandising assistants — is the exposed layer. An agent grounded in the catalog and inventory does this natively, so the per-seat tooling compresses. The commerce platform itself stays as system of record. Replace."),
 dict(n=4,at="Customer",uc="Travel & booking planner",proof="Agoda, Priceline, LATAM Cosmos, Virgin Voyages",
   saas="Booking / itinerary tools",vol="H",det="M",moat="L",verd="REPLACE",bvb="Booking seats → agent + inventory API",
   pd="Agoda's AI Vacation Planner, Priceline's trip tools, LATAM Airlines' “Cosmos” and Virgin Voyages' “Rovey” turn a natural-language request into a built itinerary against live inventory. The agent owns the plan-and-book loop end to end.",
   sd="Standalone itinerary builders and booking-assist seats are displaced; the agent reads inventory / PMS via API and assembles the trip. The reservation system of record stays, but the human-facing booking-tool seats shrink. Replace."),
 dict(n=5,at="Customer",uc="Messaging-channel chatbot",proof="LUXGEN (LINE), Banglalink REN, DT MINDR",
   saas="Chatbot / CCaaS bots",vol="H",det="H",moat="L",verd="REPLACE",bvb="Bot-builder seats → 1 agent",
   pd="LUXGEN runs a Vertex AI agent on its official LINE account that cut human customer-service workload by ~30%; Banglalink's “REN” and Deutsche Telekom's “MINDR” handle high-volume conversational support on messaging channels. These are deterministic, high-throughput deflection agents.",
   sd="Per-seat chatbot builders and CCaaS bot modules are the target — the same flows now run on a general agent at a fraction of the per-seat cost. The contact-center platform can remain; the bot-builder licenses do not. Replace."),
 dict(n=6,at="Employee",uc="Enterprise knowledge search",proof="Geotab, Bosch AskBosch, Glean",
   saas="Enterprise search SaaS",vol="H",det="M",moat="M",verd="RENEGOTIATE",bvb="Agent over your data; trim search seats",
   pd="Geotab moved research, document summarization, and status reporting onto Google Workspace with Gemini across HR and engineering; Bosch's “AskBosch” and Glean surface answers across internal systems. The agent retrieves and synthesizes across silos on demand.",
   sd="Standalone enterprise-search SaaS is squeezed because the agent indexes your own corpus and answers directly. But the value is your proprietary data, so you keep the substrate and trim the search seats. Renegotiate — agent over your data, fewer licenses."),
 dict(n=7,at="Employee",uc="Doc summarization & drafting",proof="KPMG, PwC, Deloitte",
   saas="Doc / productivity add-ons",vol="H",det="M",moat="L",verd="REPLACE",bvb="Native LLM; drop add-on seats",
   pd="KPMG, PwC, and Deloitte deploy agents that summarize, review, and draft across engagements — collapsing a manual research-and-brief task that used to eat an hour into a usable first draft in minutes.",
   sd="This is native LLM capability, so per-seat document-productivity add-ons lose their reason to exist. The office suite stays; the bolt-on summarization / drafting seats go. Replace at the add-on layer."),
 dict(n=8,at="Employee",uc="Contact-center agent assist",proof="Humana Agent Assist, Vodafone",
   saas="CCaaS agent-assist",vol="H",det="M",moat="M",verd="RENEGOTIATE",bvb="Keep CCaaS; agent-assist replaces add-on",
   pd="Humana's Agent Assist surfaces next-best actions to live reps in real time; Vodafone uses agents to guide and automate contact-center work. The agent rides alongside the human rather than replacing them.",
   sd="This enriches the CCaaS platform rather than replacing it — but it displaces separate agent-assist and real-time-guidance add-ons. Keep the contact-center system of record; renegotiate the assist module. Renegotiate."),
 dict(n=9,at="Employee",uc="Legal research & drafting",proof="Harvey, Thomson Reuters, Deutsche Bank DB Lumina",
   saas="Westlaw, LexisNexis, CLM",vol="M",det="M",moat="L",verd="REPLACE",bvb="Per-lawyer research seats → agent",
   pd="Harvey and Legora run research, review, and drafting for AmLaw firms; Thomson Reuters embeds gen-AI research; Deutsche Bank's “DB Lumina” drafts research at scale. Firms are quietly trimming junior classes citing the productivity gain.",
   sd="Per-lawyer research platforms (Westlaw, LexisNexis) and contract-lifecycle tools are repricing fast as the agent does the lookup-and-draft loop. The proprietary case-law corpus retains value, but per-seat research licenses compress. Replace at the seat layer."),
 dict(n=10,at="Employee",uc="HR / onboarding agent",proof="Grupo Ruiz, employee-agent deployments",
   saas="HR workflow SaaS",vol="M",det="H",moat="M",verd="RENEGOTIATE",bvb="Agent runs workflow; keep record system",
   pd="Grupo Ruiz uses Gemini Enterprise to streamline team workflows; employee-agent deployments orchestrate onboarding tasks, time-off requests, and policy questions. The agent runs the repetitive HR workflow end to end.",
   sd="HR workflow SaaS keeps its system-of-record role (payroll, employee records), but the per-seat workflow and case-management modules are exposed to an agent that executes inside them. Renegotiate — keep the SoR, drop the workflow seats."),
 dict(n=11,at="Creative",uc="Ad & creative generation at scale",proof="WPP, Authentic Brands Group, PODS",
   saas="Creative production seats",vol="H",det="M",moat="L",verd="REPLACE",bvb="Production seats → gen pipeline",
   pd="WPP and Authentic Brands Group turn a single hypothesis into hundreds-to-thousands of personalized creative variations in hours; PODS built the “World's Smartest Billboard” that generated 6,000+ headlines across NYC neighborhoods in 29 hours. Creative becomes a computational process.",
   sd="Per-editor creative-production seats and the freelance long tail are displaced as generation moves from manual to computational. Brand / DAM systems stay; production seats shrink hard. Replace."),
 dict(n=12,at="Creative",uc="Video generation",proof="Veo deployments, Adobe",
   saas="Video editing SaaS",vol="M",det="M",moat="M",verd="RENEGOTIATE",bvb="Agent drafts; editors finish",
   pd="Veo deployments and Adobe's gen-video tools produce and edit footage from prompts; brands spin cinematic variations without a full production cycle. The agent drafts; editors refine the final cut.",
   sd="Video-editing SaaS is partially displaced — the agent handles first-pass generation while editors finish high-stakes work. Hybrid: agent does the volume, humans own the last mile. Renegotiate."),
 dict(n=13,at="Creative",uc="Personalized marketing content",proof="Adobe, ElevenLabs (voice)",
   saas="Marketing content tools",vol="H",det="M",moat="L",verd="REPLACE",bvb="Content-tool seats → agent",
   pd="Adobe's gen workflows and ElevenLabs' voice generation produce hyper-personalized, real-time creative; marketing teams generate variant copy, voice, and assets on demand instead of producing each by hand.",
   sd="Per-seat marketing-content and copy tools are displaced by an agent that generates on brief. The campaign / martech platform stays as orchestration; the content-tool seats go. Replace at the content layer."),
 dict(n=14,at="Creative",uc="Brand / 3D asset generation",proof="BMW Group SORDI.ai",
   saas="Asset / DAM tooling",vol="M",det="M",moat="H",verd="KEEP",bvb="DAM stays SoR; agent feeds it",
   pd="BMW Group's SORDI.ai generates large synthetic 3D datasets and brand assets for industrial and creative use. The agent feeds a managed asset pipeline rather than replacing it.",
   sd="The DAM / asset system remains the system of record and compounds in value as the agent fills it; tooling spend shifts rather than disappears. Keep — the agent enriches the moat."),
 dict(n=15,at="Code",uc="AI code assistant",proof="Valeo, Broadcom (Gemini Code Assist)",
   saas="IDE / code-review add-ons",vol="H",det="M",moat="M",verd="RENEGOTIATE",bvb="Enriches IDE; consumption not seats",
   pd="Valeo and Broadcom deploy Gemini Code Assist across engineering; developers move faster through problems they already understand. The assistant augments the IDE, not the engineer's judgment.",
   sd="This enriches the developer toolchain; the shift is from per-seat add-ons to consumption-based assistance. Architectural judgment still sits with humans. Renegotiate — consumption, not seats."),
 dict(n=16,at="Code",uc="Legacy-IT modernization (NL→SAP)",proof="Suzano, Deutsche Telekom",
   saas="Modernization consulting / tools",vol="M",det="L",moat="H",verd="KEEP",bvb="Agent unlocks legacy; keep core systems",
   pd="Suzano and Deutsche Telekom use Gemini to put natural-language interfaces over 40-year-old SAP, mainframe, and COBOL systems — letting non-technical staff query siloed data without a costly migration.",
   sd="This is pure enrichment — the agent unlocks the legacy system rather than replacing it, and the system of record becomes more valuable. Modernization consulting / tooling spend shifts to the agent layer. Keep."),
 dict(n=17,at="Code",uc="App build / migration automation",proof="Code-agent deployments",
   saas="Low-code & migration tooling",vol="M",det="M",moat="M",verd="RENEGOTIATE",bvb="Agent replaces low-code seats partially",
   pd="Code-agent deployments scaffold applications and automate migrations that used to require specialist teams; experienced engineers ship faster while the agent handles boilerplate and conversions.",
   sd="Low-code builders and migration tooling are partially displaced where the workflow is well-defined, but complex / bespoke work still needs humans. Hybrid — the agent replaces the routine slice. Renegotiate."),
 dict(n=18,at="Data",uc="NL analytics (text-to-SQL)",proof="Spotify, Etsy (BigQuery)",
   saas="BI dashboards (Looker-class)",vol="H",det="M",moat="M",verd="RENEGOTIATE",bvb="Agent over warehouse; trim BI seats",
   pd="Spotify and Etsy let teams ask questions of BigQuery in natural language instead of building dashboards; the agent writes the query and returns the answer.",
   sd="BI dashboard seats (Looker-class) are squeezed because the agent collapses the interface and answers directly — but the warehouse remains the system of record and a verification / dashboard layer stays for trust. Hybrid: trim BI seats, keep the warehouse. Renegotiate."),
 dict(n=19,at="Data",uc="Document AI / extraction",proof="Document AI deployments",
   saas="IDP / OCR SaaS",vol="H",det="H",moat="L",verd="REPLACE",bvb="IDP/OCR seats → agent + Document AI",
   pd="Document AI deployments parse invoices, forms, and contracts at scale, replacing manual keying and template-based capture. Output is structured and deterministic.",
   sd="IDP / OCR SaaS is directly displaced — the agent extracts and routes natively, absorbing the clerk role. The downstream system of record stays; the capture-tool seats go. Replace."),
 dict(n=20,at="Data",uc="Forecasting / predictive ops",proof="Honeywell, Geotab",
   saas="Predictive-analytics SaaS",vol="M",det="M",moat="H",verd="KEEP",bvb="Agent augments; data moat compounds",
   pd="Honeywell and Geotab apply agents to predictive maintenance and fleet / operations forecasting on top of proprietary sensor and telematics data. The agent augments existing models.",
   sd="Predictive-analytics SaaS is enriched, not replaced — the moat is the operational data feeding the forecast. Spend consolidates onto the platform that owns the data. Keep."),
 dict(n=21,at="Data",uc="Research & insight agent",proof="MLB Scout Insights, NotebookLM",
   saas="Market-research tooling",vol="M",det="M",moat="M",verd="RENEGOTIATE",bvb="Agent replaces research-tool seats",
   pd="MLB's “Scout Insights” and NotebookLM-style agents synthesize large corpora into briefings; teams get a usable insight package in minutes instead of days.",
   sd="Standalone market-research and insight tooling seats are displaced by an agent that synthesizes on demand, but proprietary data sources retain value. Renegotiate — fewer research-tool seats."),
 dict(n=22,at="Security",uc="Threat detection / SecOps",proof="Google Security Operations deployments",
   saas="SIEM tier-1",vol="H",det="M",moat="H",verd="KEEP",bvb="Agent rides on SIEM; keep record system",
   pd="Google Security Operations deployments correlate signals and surface threats; security teams move from manual triage to agent-surfaced detection. The agent rides on the SIEM's data.",
   sd="SIEM tier-1 work is enriched — the agent reduces toil, but the SIEM remains the system of record and the incident history is the moat. Keep the platform; the L1 seat compresses."),
 dict(n=23,at="Security",uc="Agentic auto-remediation",proof="Security-agent deployments",
   saas="SOAR / runbooks",vol="H",det="H",moat="L",verd="REPLACE",bvb="SOAR/runbook seats → agent in policy",
   pd="Security-agent deployments write detection rules, isolate compromised workloads, and deploy honeytokens autonomously — neutralizing tier-1 threats without human intervention, within a policy envelope.",
   sd="SOAR and runbook-automation seats are displaced as the agent becomes the responder. The system of record stays for audit; the playbook-authoring seats go. Replace within policy."),
 dict(n=24,at="Security",uc="Fraud & risk detection",proof="Citi, Wells Fargo, Commerzbank Bene",
   saas="Fraud / risk add-ons",vol="H",det="M",moat="H",verd="KEEP",bvb="Agent enriches; proprietary data wins",
   pd="Citi and Wells Fargo apply agents to risk and fraud analysis; Commerzbank's “Bene” assists risk workflows. The agent enriches detection on top of proprietary transaction data.",
   sd="Fraud / risk add-ons are enriched, not replaced — the bank's data and models are the moat, and being wrong is expensive, so humans stay in the loop. Keep — the agent augments, the data wins."),
 dict(n=25,at="Security",uc="Compliance & audit agent",proof="U.S. FDA, regulated deployments",
   saas="GRC tooling",vol="M",det="M",moat="H",verd="KEEP",bvb="Agent drafts; GRC stays record system",
   pd="The U.S. Food and Drug Administration and other regulated bodies use agents to draft and review compliance documentation; the agent prepares, a human signs off. Auditability is mandatory.",
   sd="GRC tooling stays the system of record because of audit and regulatory requirements; the agent drafts and accelerates rather than displacing the platform. Keep."),
]

# ---------- CSV ----------
csv_path = RUN / "agent-replacement-scorecard.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["#","Agent type","Use case","Proof (short)","SaaS affected (short)","Volume","Determinism",
                "Data moat","Verdict","Build-vs-buy","Proof — what's deployed","SaaS in the crosshairs"])
    for r in R:
        w.writerow([r["n"],r["at"],r["uc"],r["proof"],r["saas"],r["vol"],r["det"],r["moat"],r["verd"],r["bvb"],r["pd"],r["sd"]])

# ---------- HTML ----------
n_replace = sum(1 for r in R if r["verd"]=="REPLACE")
n_reneg   = sum(1 for r in R if r["verd"]=="RENEGOTIATE")
n_keep    = sum(1 for r in R if r["verd"]=="KEEP")
def e(x): return html.escape(str(x))

rows_html=[]
for r in R:
    s=(r["uc"]+" "+r["proof"]+" "+r["saas"]+" "+r["at"]+" "+r["pd"]+" "+r["sd"]).lower()
    rows_html.append(
      f'<tr class="main" data-type="{r["at"]}" data-verdict="{r["verd"]}" data-search="{e(s)}" onclick="toggleRow(this)">'
      f'<td class="num">{r["n"]}</td>'
      f'<td><span class="at">{e(r["at"])}</span></td>'
      f'<td class="uc"><span class="caret">▸</span>{e(r["uc"])}</td>'
      f'<td class="proof">{e(r["proof"])}</td>'
      f'<td class="saas">{e(r["saas"])}</td>'
      f'<td class="ctr"><span class="hml h-{r["vol"]}">{r["vol"]}</span></td>'
      f'<td class="ctr"><span class="hml h-{r["det"]}">{r["det"]}</span></td>'
      f'<td class="ctr"><span class="hml h-{r["moat"]}">{r["moat"]}</span></td>'
      f'<td class="ctr"><span class="verd v-{r["verd"]}">{e(r["verd"])}</span></td>'
      f'<td class="bvb">{e(r["bvb"])}</td></tr>')
    rows_html.append(
      f'<tr class="detail" style="display:none"><td colspan="10"><div class="dd">'
      f'<div><h4>Proof — what’s actually deployed</h4><p>{e(r["pd"])}</p></div>'
      f'<div><h4>SaaS in the crosshairs</h4><p>{e(r["sd"])}</p></div>'
      f'</div></td></tr>')
rows_joined="\n".join(rows_html)

HTML = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Agent Replacement Scorecard — Top 25 Use Cases</title>
<style>
:root{{--navy:#0A1628;--navy2:#12243A;--teal:#00C9A7;--accent:#009B82;--gold:#FFB800;--amber:#F2A83B;
--coral:#E05A6B;--soft:#F4F7F8;--ink:#1B2B3C;--muted:#5B6B7C;--grid:#D9DFE5;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:Calibri,'Segoe UI',system-ui,Arial,sans-serif;color:var(--ink);background:#fff}}
header{{background:var(--navy);color:#fff;padding:30px 40px 26px}}
header .kicker{{color:var(--teal);font-weight:700;letter-spacing:.06em;font-size:13px}}
header h1{{margin:8px 0 6px;font-size:30px;line-height:1.1}}
header p{{margin:0;color:#E0F7F1;max-width:900px;font-size:15px}}
.bar{{height:5px;width:90px;background:var(--teal);margin:14px 0 0;border-radius:3px}}
.wrap{{padding:22px 40px 60px;max-width:1320px;margin:0 auto}}
.stats{{display:flex;gap:14px;margin:0 0 18px;flex-wrap:wrap}}
.stat{{flex:1;min-width:150px;background:var(--navy);color:#fff;border-radius:10px;padding:14px 18px}}
.stat b{{display:block;font-size:30px;color:var(--gold);line-height:1}}
.stat.replace b{{color:var(--coral)}} .stat.reneg b{{color:var(--amber)}} .stat.keep b{{color:var(--teal)}}
.stat span{{font-size:13px;color:#E0F7F1}}
.controls{{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:0 0 8px}}
.controls input{{padding:9px 12px;border:1px solid var(--grid);border-radius:8px;font-size:14px;min-width:220px}}
.chip{{border:1px solid var(--grid);background:#fff;color:var(--ink);border-radius:20px;padding:7px 14px;font-size:13px;cursor:pointer;font-weight:600}}
.chip.active{{background:var(--navy);color:#fff;border-color:var(--navy)}}
.chip.vr.active{{background:var(--coral);border-color:var(--coral)}}
.chip.vn.active{{background:var(--amber);border-color:var(--amber);color:#1B2B3C}}
.chip.vk.active{{background:var(--teal);border-color:var(--teal);color:#06281f}}
.hint{{font-size:12px;color:var(--muted);margin:0 0 12px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
thead th{{background:var(--navy);color:var(--teal);text-align:left;padding:10px 10px;font-size:12px;white-space:nowrap}}
thead th.ctr{{text-align:center}}
tbody td{{padding:9px 10px;border-bottom:1px solid var(--grid);vertical-align:middle}}
tr.main{{cursor:pointer}} tr.main:hover{{background:#eef6f4}}
tbody tr.main:nth-of-type(odd){{background:var(--soft)}}
td.num{{color:var(--muted);font-weight:700;width:30px}}
td.uc{{font-weight:700;min-width:180px}}
.caret{{display:inline-block;color:var(--teal);margin-right:6px;transition:transform .15s}}
tr.main.open .caret{{transform:rotate(90deg)}}
td.proof{{color:var(--muted);font-size:12.5px}} td.saas{{font-size:12.5px}}
td.bvb{{font-size:12.5px}} td.ctr{{text-align:center}}
.at{{font-size:11px;font-weight:700;padding:2px 8px;border-radius:10px;background:var(--navy2);color:#fff;white-space:nowrap}}
.hml{{display:inline-block;width:26px;height:26px;line-height:26px;text-align:center;border-radius:50%;font-weight:700;font-size:12px}}
.h-H{{background:var(--teal);color:#06281f}} .h-M{{background:var(--amber);color:#1B2B3C}} .h-L{{background:var(--grid);color:var(--muted)}}
.verd{{display:inline-block;padding:4px 12px;border-radius:14px;font-weight:700;font-size:11.5px;color:#fff}}
.v-REPLACE{{background:var(--coral)}} .v-RENEGOTIATE{{background:var(--amber);color:#1B2B3C}} .v-KEEP{{background:var(--teal);color:#06281f}}
tr.detail td{{background:#fbfdfd;border-bottom:2px solid var(--teal);padding:0}}
.dd{{display:flex;gap:34px;padding:14px 20px 18px 46px}}
.dd>div{{flex:1}}
.dd h4{{margin:0 0 5px;color:var(--accent);font-size:12px;text-transform:uppercase;letter-spacing:.05em}}
.dd p{{margin:0;font-size:13px;line-height:1.55;color:var(--ink)}}
.note{{margin-top:18px;background:var(--soft);border-left:4px solid var(--teal);padding:14px 18px;font-size:13px;border-radius:6px}}
.note b{{color:var(--accent)}}
.legend{{font-size:12px;color:var(--muted);margin:10px 0 0}} .legend b{{color:var(--ink)}}
footer{{color:var(--muted);font-size:12px;margin-top:18px}}
</style></head>
<body>
<header>
 <div class="kicker">PRE-SALES ASSET · AGENT REPLACEMENT SCORECARD</div>
 <h1>The Top 25 Agentic Use Cases — Keep / Renegotiate / Replace</h1>
 <p>Each use case is graded on three factors — Volume, Determinism, and Data&nbsp;moat — to produce a verdict on the SaaS it
 touches, with build-vs-buy math. <b>Click any row</b> to read what is actually deployed and which SaaS is in the crosshairs.
 Proof points are real, named deployments from Google Cloud's 1,302-use-case list.</p>
 <div class="bar"></div>
</header>
<div class="wrap">
 <div class="stats">
  <div class="stat replace"><b>{n_replace}</b><span>REPLACE — workflow-over-data, low moat</span></div>
  <div class="stat reneg"><b>{n_reneg}</b><span>RENEGOTIATE — drop seats, keep the system</span></div>
  <div class="stat keep"><b>{n_keep}</b><span>KEEP — data moat compounds; agent enriches</span></div>
  <div class="stat"><b>25</b><span>use cases · 6 agent types · 11 industries</span></div>
 </div>
 <div class="controls">
  <input id="q" type="text" placeholder="Search use case, vendor, SaaS…" oninput="apply()">
  <button class="chip active" data-f="type" onclick="setf(this,'type','all')">All types</button>
  <button class="chip" onclick="setf(this,'type','Customer')">Customer</button>
  <button class="chip" onclick="setf(this,'type','Employee')">Employee</button>
  <button class="chip" onclick="setf(this,'type','Creative')">Creative</button>
  <button class="chip" onclick="setf(this,'type','Code')">Code</button>
  <button class="chip" onclick="setf(this,'type','Data')">Data</button>
  <button class="chip" onclick="setf(this,'type','Security')">Security</button>
  <span style="width:10px"></span>
  <button class="chip vr" onclick="setf(this,'verdict','REPLACE')">Replace</button>
  <button class="chip vn" onclick="setf(this,'verdict','RENEGOTIATE')">Renegotiate</button>
  <button class="chip vk" onclick="setf(this,'verdict','KEEP')">Keep</button>
  <span style="width:10px"></span>
  <button class="chip" onclick="allRows(true)">Expand all</button>
  <button class="chip" onclick="allRows(false)">Collapse all</button>
 </div>
 <p class="hint">▸ click a row to expand the two-paragraph detail.</p>
 <table id="t">
  <thead><tr>
   <th>#</th><th>Type</th><th>Use case</th><th>Proof (summary)</th><th>SaaS affected</th>
   <th class="ctr">Vol</th><th class="ctr">Det</th><th class="ctr">Moat</th><th class="ctr">Verdict</th><th>Build-vs-buy</th>
  </tr></thead>
  <tbody id="tb">
{rows_joined}
  </tbody>
 </table>
 <p class="legend"><b>Volume</b> = task throughput · <b>Determinism</b> = how well-defined the output ·
 <b>Data moat</b> = proprietary / system-of-record strength. High volume + high determinism + low moat → Replace.
 High moat → Keep (agent enriches). Mixed → Renegotiate the seat model.</p>
 <div class="note"><b>How to use this.</b> Map your own SaaS line items onto these 25 archetypes, then act on the verdict:
 <b>Replace</b> → run the build-vs-buy math and pilot an agent in parallel for two weeks. <b>Renegotiate</b> → your renewal
 leverage just improved; move off per-seat toward consumption / outcome pricing. <b>Keep</b> → the platform is your data moat;
 let the agent ride on top via API / MCP. Deployments are real and named; the H/M/L scores and verdicts are structured
 judgment — directional guidance, not measured counts.</div>
 <footer>Agentic AI vs. SaaS · Agent Replacement Scorecard · 2026-06-22 · evidence: Google Cloud 1,302 gen-AI use cases +
 Agent Replacement Index + ITOps research (ISG / IDC / Gartner). Companion to Agentic-AI-vs-SaaS-Top25.pptx.</footer>
</div>
<script>
var F={{type:'all',verdict:null}};
function setf(btn,kind,val){{
 if(kind==='verdict'&&btn.classList.contains('active')){{btn.classList.remove('active');F.verdict=null;apply();return;}}
 document.querySelectorAll('.chip').forEach(function(c){{
   var isType=['All types','Customer','Employee','Creative','Code','Data','Security'].indexOf(c.textContent)>-1;
   var isVerd=['Replace','Renegotiate','Keep'].indexOf(c.textContent)>-1;
   if(kind==='type'&&isType)c.classList.remove('active');
   if(kind==='verdict'&&isVerd)c.classList.remove('active');
 }});
 btn.classList.add('active');F[kind]=val;apply();
}}
function apply(){{
 var q=document.getElementById('q').value.toLowerCase();
 document.querySelectorAll('#tb tr.main').forEach(function(tr){{
  var ok=(F.type==='all'||tr.dataset.type===F.type)&&(!F.verdict||tr.dataset.verdict===F.verdict)&&(!q||tr.dataset.search.indexOf(q)>-1);
  tr.style.display=ok?'':'none';
  var d=tr.nextElementSibling;
  if(d&&d.classList.contains('detail')) d.style.display=(ok&&tr.classList.contains('open'))?'':'none';
 }});
}}
function toggleRow(tr){{
 tr.classList.toggle('open');
 var d=tr.nextElementSibling;
 if(d&&d.classList.contains('detail')) d.style.display=tr.classList.contains('open')?'':'none';
}}
function allRows(open){{
 document.querySelectorAll('#tb tr.main').forEach(function(tr){{
  if(tr.style.display==='none')return;
  tr.classList.toggle('open',open);
  var d=tr.nextElementSibling;
  if(d&&d.classList.contains('detail')) d.style.display=open?'':'none';
 }});
}}
</script>
</body></html>"""

html_path = RUN / "agent-replacement-scorecard.html"
html_path.write_text(HTML, encoding="utf-8")
print("wrote", csv_path.name, "and", html_path.name)
print(f"verdicts: REPLACE={n_replace}  RENEGOTIATE={n_reneg}  KEEP={n_keep}")
