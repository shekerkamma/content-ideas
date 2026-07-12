#!/usr/bin/env python3
import csv
from collections import Counter, defaultdict
from pathlib import Path

RUN = Path(__file__).resolve().parent
OUT = RUN / "outputs"
WORKING = RUN / "working"
SOURCE = RUN / "source"
OUT.mkdir(exist_ok=True)
WORKING.mkdir(exist_ok=True)
SOURCE.mkdir(exist_ok=True)

ROWS = [
    ("OpenAI", "https://openai.com", "Foundation Models", "Enterprise Platforms;Developer Platforms", "frontier models and enterprise AI products"),
    ("Anthropic", "https://www.anthropic.com", "Foundation Models", "Enterprise Platforms", "Claude models and enterprise safety-oriented AI"),
    ("Google DeepMind", "https://deepmind.google", "Foundation Models", "Enterprise Platforms", "Gemini and frontier AI research/productization"),
    ("Meta AI", "https://ai.meta.com", "Foundation Models", "Infrastructure", "open and proprietary AI models including Llama ecosystem"),
    ("Mistral AI", "https://mistral.ai", "Foundation Models", "AI Development Platforms", "European frontier and open-weight model provider"),
    ("Cohere", "https://cohere.com", "Foundation Models", "Enterprise Platforms", "enterprise-focused language models and retrieval"),
    ("AI21 Labs", "https://www.ai21.com", "Foundation Models", "Enterprise Platforms", "language models and enterprise writing systems"),
    ("xAI", "https://x.ai", "Foundation Models", "Enterprise Platforms", "frontier model lab and Grok platform"),
    ("DeepSeek", "https://www.deepseek.com", "Foundation Models", "Developer Platforms", "open model provider with strong cost/performance positioning"),
    ("Perplexity", "https://www.perplexity.ai", "Foundation Models", "Knowledge Management", "answer engine and enterprise search/research workflows"),
    ("Aleph Alpha", "https://aleph-alpha.com", "Foundation Models", "Governance", "sovereign European AI models for enterprises and governments"),
    ("Writer", "https://writer.com", "Foundation Models", "Enterprise Platforms", "enterprise generative AI platform and domain-tuned models"),
    ("NVIDIA", "https://www.nvidia.com", "Infrastructure", "AI Development Platforms", "accelerated compute, AI software, and reference architectures"),
    ("AMD", "https://www.amd.com", "Infrastructure", "Developer Platforms", "AI accelerators and compute platform"),
    ("CoreWeave", "https://www.coreweave.com", "Infrastructure", "Managed Services", "GPU cloud for AI workloads"),
    ("Lambda", "https://lambdalabs.com", "Infrastructure", "Managed Services", "GPU cloud and AI developer workstations"),
    ("Crusoe", "https://crusoe.ai", "Infrastructure", "Managed Services", "AI cloud infrastructure and data centers"),
    ("Together AI", "https://www.together.ai", "Infrastructure", "AI Development Platforms", "inference, fine-tuning, and model deployment"),
    ("Fireworks AI", "https://fireworks.ai", "Infrastructure", "AI Development Platforms", "fast inference and generative AI platform"),
    ("Modal", "https://modal.com", "Infrastructure", "Developer Platforms", "serverless compute for AI and data workloads"),
    ("Replicate", "https://replicate.com", "Infrastructure", "Developer Platforms", "model hosting and inference APIs"),
    ("Baseten", "https://www.baseten.co", "Infrastructure", "AI Development Platforms", "model deployment and inference platform"),
    ("RunPod", "https://www.runpod.io", "Infrastructure", "Developer Platforms", "GPU cloud for AI developers"),
    ("Hugging Face", "https://huggingface.co", "AI Development Platforms", "Foundation Models;Infrastructure", "model hub, datasets, inference, and enterprise AI tooling"),
    ("Databricks", "https://www.databricks.com", "AI Development Platforms", "Enterprise Platforms", "lakehouse, Mosaic AI, and enterprise data/AI platform"),
    ("Snowflake", "https://www.snowflake.com", "Enterprise Platforms", "AI Development Platforms", "governed enterprise data cloud and AI services"),
    ("Anyscale", "https://www.anyscale.com", "AI Development Platforms", "Infrastructure", "Ray-based AI application and compute platform"),
    ("Weights & Biases", "https://wandb.ai", "AI Operations", "AI Development Platforms", "experiment tracking, model evaluation, and AI developer workflow"),
    ("LangChain", "https://www.langchain.com", "Agent Frameworks", "AI Development Platforms", "framework and platform for LLM/agent applications"),
    ("LlamaIndex", "https://www.llamaindex.ai", "Agent Frameworks", "Knowledge Management", "data framework for LLM and agent applications"),
    ("CrewAI", "https://www.crewai.com", "Agent Frameworks", "AI Development Platforms", "multi-agent workflow framework and platform"),
    ("deepset", "https://www.deepset.ai", "Agent Frameworks", "Knowledge Management", "Haystack framework and enterprise AI search"),
    ("Microsoft AutoGen", "https://microsoft.github.io/autogen", "Agent Frameworks", "Developer Platforms", "multi-agent framework from Microsoft Research"),
    ("Microsoft Semantic Kernel", "https://learn.microsoft.com/semantic-kernel", "Agent Frameworks", "Developer Platforms", "agent/application orchestration SDK"),
    ("AutoGPT", "https://agpt.co", "Agent Frameworks", "Developer Platforms", "open-source agent experimentation platform"),
    ("Dust", "https://dust.tt", "Agent Frameworks", "Enterprise Platforms", "custom AI assistants and internal workflow agents"),
    ("Relevance AI", "https://relevanceai.com", "Agent Frameworks", "Enterprise Platforms", "AI workforce and agent platform"),
    ("Zapier", "https://zapier.com", "Agent Frameworks", "Enterprise Platforms", "automation and AI agents across SaaS apps"),
    ("Microsoft Copilot", "https://www.microsoft.com/microsoft-copilot", "Enterprise Platforms", "Developer Platforms", "AI assistants embedded across Microsoft products"),
    ("Salesforce Agentforce", "https://www.salesforce.com/agentforce", "Enterprise Platforms", "Vertical AI", "enterprise agents embedded in CRM and service workflows"),
    ("ServiceNow", "https://www.servicenow.com", "Enterprise Platforms", "AI Operations", "workflow platform with AI agents and enterprise automation"),
    ("IBM watsonx", "https://www.ibm.com/watsonx", "Enterprise Platforms", "Governance;AI Consulting", "enterprise AI platform, governance, and consulting ecosystem"),
    ("SAP Joule", "https://www.sap.com/products/artificial-intelligence.html", "Enterprise Platforms", "Vertical AI", "AI copilot and agents in enterprise ERP workflows"),
    ("Oracle AI", "https://www.oracle.com/artificial-intelligence", "Enterprise Platforms", "Infrastructure", "AI services across Oracle cloud and enterprise apps"),
    ("Workday AI", "https://www.workday.com/en-us/artificial-intelligence.html", "Enterprise Platforms", "Vertical AI", "AI for HR and finance workflows"),
    ("Atlassian Rovo", "https://www.atlassian.com/software/rovo", "Enterprise Platforms", "Knowledge Management", "AI teammate/search for Atlassian work graph"),
    ("Adobe Firefly", "https://www.adobe.com/products/firefly.html", "Enterprise Platforms", "Vertical AI", "generative AI for creative and marketing workflows"),
    ("Box AI", "https://www.box.com/ai", "Enterprise Platforms", "Knowledge Management", "AI over enterprise content"),
    ("Zoom AI Companion", "https://www.zoom.com/en/products/ai-assistant", "Enterprise Platforms", "Knowledge Management", "AI assistant embedded in collaboration workflows"),
    ("GitHub Copilot", "https://github.com/features/copilot", "Developer Platforms", "AI Development Platforms", "AI coding assistant and developer workflow platform"),
    ("Cursor", "https://cursor.com", "Developer Platforms", "AI Development Platforms", "AI-native code editor"),
    ("Replit", "https://replit.com", "Developer Platforms", "AI Development Platforms", "cloud development environment with AI agent/coding support"),
    ("Cognition", "https://www.cognition.ai", "Developer Platforms", "Agent Frameworks", "AI software engineering agent"),
    ("Poolside", "https://poolside.ai", "Developer Platforms", "Foundation Models", "software development-focused AI models and tooling"),
    ("Sourcegraph Cody", "https://sourcegraph.com/cody", "Developer Platforms", "Knowledge Management", "AI coding assistant over large codebases"),
    ("Tabnine", "https://www.tabnine.com", "Developer Platforms", "AI Development Platforms", "enterprise AI code assistant"),
    ("Codeium/Windsurf", "https://windsurf.com", "Developer Platforms", "AI Development Platforms", "AI coding assistant and IDE"),
    ("JetBrains AI", "https://www.jetbrains.com/ai", "Developer Platforms", "AI Development Platforms", "AI assistant inside JetBrains IDEs"),
    ("Arize AI", "https://arize.com", "Observability", "AI Operations", "ML and LLM observability/evaluation"),
    ("LangSmith", "https://www.langchain.com/langsmith", "Observability", "AI Operations", "LLM application tracing, evaluation, and monitoring"),
    ("Langfuse", "https://langfuse.com", "Observability", "AI Operations", "open-source LLM observability"),
    ("Helicone", "https://www.helicone.ai", "Observability", "AI Operations", "LLM observability and gateway analytics"),
    ("HoneyHive", "https://www.honeyhive.ai", "Observability", "AI Operations", "AI agent evaluation and observability"),
    ("Galileo", "https://www.galileo.ai", "Observability", "AI Operations", "LLM evaluation and observability platform"),
    ("WhyLabs", "https://whylabs.ai", "Observability", "AI Operations", "AI observability and model monitoring"),
    ("Fiddler AI", "https://www.fiddler.ai", "Observability", "Governance", "AI observability, explainability, and governance"),
    ("Datadog", "https://www.datadoghq.com", "Observability", "AI Operations", "observability platform extending into AI systems"),
    ("New Relic", "https://newrelic.com", "Observability", "AI Operations", "observability platform with AI monitoring features"),
    ("Dynatrace", "https://www.dynatrace.com", "Observability", "AI Operations", "enterprise observability and automation"),
    ("Lakera", "https://www.lakera.ai", "Security", "Governance", "LLM security and guardrails"),
    ("Protect AI", "https://protectai.com", "Security", "Governance", "AI/ML security platform"),
    ("HiddenLayer", "https://hiddenlayer.com", "Security", "Governance", "AI model and application security"),
    ("CalypsoAI", "https://calypsoai.com", "Security", "Governance", "enterprise AI security and control platform"),
    ("Robust Intelligence", "https://www.robustintelligence.com", "Security", "Governance", "AI risk and security testing"),
    ("Aporia", "https://www.aporia.com", "Security", "Observability", "AI guardrails and control platform"),
    ("Patronus AI", "https://www.patronus.ai", "Governance", "Observability", "LLM evaluation and safety testing"),
    ("Giskard", "https://www.giskard.ai", "Governance", "Observability", "AI testing and evaluation"),
    ("Credo AI", "https://www.credo.ai", "Governance", "Security", "AI governance and risk management"),
    ("Holistic AI", "https://www.holisticai.com", "Governance", "Security", "AI governance, risk, and compliance"),
    ("Arthur AI", "https://www.arthur.ai", "Governance", "Observability", "AI performance, explainability, and monitoring"),
    ("Monitaur", "https://www.monitaur.ai", "Governance", "Security", "AI governance and compliance operations"),
    ("Truera", "https://truera.com", "Governance", "Observability", "AI quality, explainability, and monitoring"),
    ("Glean", "https://www.glean.com", "Knowledge Management", "Enterprise Platforms", "enterprise search and work AI"),
    ("Hebbia", "https://www.hebbia.ai", "Knowledge Management", "Vertical AI", "AI search/analysis for enterprise knowledge work"),
    ("Unstructured", "https://unstructured.io", "Knowledge Management", "AI Development Platforms", "data ingestion for LLM applications"),
    ("Pinecone", "https://www.pinecone.io", "Knowledge Management", "Infrastructure", "vector database for AI applications"),
    ("Weaviate", "https://weaviate.io", "Knowledge Management", "Infrastructure", "open-source vector database"),
    ("Chroma", "https://www.trychroma.com", "Knowledge Management", "Infrastructure", "embedding database for AI applications"),
    ("Elastic", "https://www.elastic.co", "Knowledge Management", "Observability", "search, security, and observability platform with AI search"),
    ("Coveo", "https://www.coveo.com", "Knowledge Management", "Enterprise Platforms", "enterprise search and relevance platform"),
    ("Sana", "https://sanalabs.com", "Knowledge Management", "Enterprise Platforms", "AI learning and knowledge platform"),
    ("Guru", "https://www.getguru.com", "Knowledge Management", "Enterprise Platforms", "enterprise knowledge base and AI search"),
    ("Notion AI", "https://www.notion.com/product/ai", "Knowledge Management", "Enterprise Platforms", "AI embedded in workspace knowledge"),
    ("Harvey", "https://www.harvey.ai", "Vertical AI", "Enterprise Platforms", "legal AI platform"),
    ("Abridge", "https://www.abridge.com", "Vertical AI", "Healthcare AI", "clinical conversation and documentation AI"),
    ("Ambience Healthcare", "https://www.ambiencehealthcare.com", "Vertical AI", "Healthcare AI", "clinical AI operating system"),
    ("Hippocratic AI", "https://www.hippocraticai.com", "Vertical AI", "Healthcare AI", "healthcare safety-focused AI agents"),
    ("Innovaccer", "https://innovaccer.com", "Vertical AI", "Enterprise Platforms", "healthcare data and AI cloud"),
    ("Nabla", "https://www.nabla.com", "Vertical AI", "Healthcare AI", "AI clinical assistant"),
    ("EvenUp", "https://www.evenuplaw.com", "Vertical AI", "Legal AI", "AI for personal injury law workflows"),
    ("EliseAI", "https://www.eliseai.com", "Vertical AI", "Enterprise Platforms", "AI agents for housing and healthcare operations"),
    ("Sierra", "https://sierra.ai", "Vertical AI", "Enterprise Platforms", "customer service AI agents"),
    ("Decagon", "https://decagon.ai", "Vertical AI", "Enterprise Platforms", "AI customer support agents"),
    ("Intercom Fin", "https://www.intercom.com/fin", "Vertical AI", "Enterprise Platforms", "AI customer support agent"),
    ("Ada", "https://www.ada.cx", "Vertical AI", "Enterprise Platforms", "AI customer service automation"),
    ("SoundHound AI", "https://www.soundhound.com", "Vertical AI", "Enterprise Platforms", "voice AI and enterprise conversational agents"),
    ("Manus", "https://manus.im", "Agent Frameworks", "Vertical AI", "general autonomous AI agent"),
    ("H Company", "https://www.hcompany.ai", "Agent Frameworks", "Foundation Models", "action-oriented AI agents and computer-use models"),
    ("Artisan", "https://www.artisan.co", "Vertical AI", "Agent Frameworks", "AI sales and business workflow agents"),
    ("Accenture", "https://www.accenture.com", "AI Consulting", "Managed Services", "AI transformation consulting and managed delivery"),
    ("Deloitte", "https://www.deloitte.com", "AI Consulting", "Governance", "AI strategy, risk, and transformation services"),
    ("McKinsey QuantumBlack", "https://www.mckinsey.com/capabilities/quantumblack", "AI Consulting", "Managed Services", "AI consulting and analytics transformation"),
    ("BCG X", "https://www.bcg.com/x", "AI Consulting", "Managed Services", "AI strategy, build, and venture services"),
    ("Bain AI", "https://www.bain.com", "AI Consulting", "Managed Services", "AI strategy and transformation consulting"),
    ("IBM Consulting", "https://www.ibm.com/consulting", "AI Consulting", "Enterprise Platforms", "AI consulting tied to IBM platform ecosystem"),
    ("EY", "https://www.ey.com", "AI Consulting", "Governance", "AI transformation, assurance, and risk advisory"),
    ("PwC", "https://www.pwc.com", "AI Consulting", "Governance", "AI strategy, governance, and implementation services"),
    ("KPMG", "https://kpmg.com", "AI Consulting", "Governance", "AI risk, compliance, and transformation advisory"),
    ("Capgemini", "https://www.capgemini.com", "Managed Services", "AI Consulting", "AI engineering and managed transformation services"),
    ("Cognizant", "https://www.cognizant.com", "Managed Services", "AI Consulting", "AI implementation and managed services"),
    ("TCS", "https://www.tcs.com", "Managed Services", "AI Consulting", "enterprise AI implementation and managed services"),
    ("Infosys", "https://www.infosys.com", "Managed Services", "AI Consulting", "AI-first services and enterprise transformation"),
    ("Wipro", "https://www.wipro.com", "Managed Services", "AI Consulting", "enterprise AI services and consulting"),
    ("HCLTech", "https://www.hcltech.com", "Managed Services", "AI Consulting", "AI engineering and managed enterprise services"),
    ("Coforge", "https://www.coforge.com", "Managed Services", "Vertical AI", "AI implementation and vertical technology services"),
]

SOURCE_NOTES = """# Source Notes - Phase 1

This phase establishes a candidate universe and category logic. It is not a final
funding/pricing database.

Current research signals used:

- Business Insider / RBC CIO survey reporting that enterprise AI spending is growing,
  OpenAI leads surveyed AI service usage, and most respondents have new AI budgets.
- TechRadar coverage of agentic AI governance risk, citing Gartner/Deloitte-style
  concern that enterprises lack adequate guardrails for agent growth.
- TechRadar coverage of distributed enterprise AI and the strategic split between
  renting intelligence and owning operational intelligence.
- ITPro coverage of Snowflake-Anthropic partnership as evidence that enterprise
  platforms are embedding foundation models inside governed data clouds.
- Public profile pages surfaced for Sierra, Manus, H Company, Artisan, SoundHound,
  and Innovaccer as examples of vertical/agentic AI companies requiring per-company
  source validation in later passes.

Every row in `company-universe-phase1.csv` is marked `phase1_candidate` unless
funding/pricing is explicitly source-attached in a later pass.
"""


def write_csv():
    fields = [
        "company", "url", "primary_category", "secondary_categories", "positioning",
        "target_buyer", "product_type", "funding_stage", "latest_funding", "headcount",
        "pricing_model", "public_pricing", "deployment_model", "enterprise_readiness",
        "moat", "risk", "sources", "confidence"
    ]
    with (OUT / "company-universe-phase1.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for company, url, primary, secondary, positioning in ROWS:
            writer.writerow({
                "company": company,
                "url": url,
                "primary_category": primary,
                "secondary_categories": secondary,
                "positioning": positioning,
                "target_buyer": "enterprise buyer / developer / operator; refine in source pass",
                "product_type": "platform / API / service; refine in source pass",
                "funding_stage": "source_pending",
                "latest_funding": "source_pending",
                "headcount": "not verified",
                "pricing_model": "source_pending",
                "public_pricing": "source_pending",
                "deployment_model": "source_pending",
                "enterprise_readiness": "provisional",
                "moat": "provisional; category position and distribution",
                "risk": "provisional; commoditization, platform bundling, or GTM friction",
                "sources": url,
                "confidence": "low-to-medium; phase1 candidate",
            })


def write_market_map():
    by_cat = defaultdict(list)
    for row in ROWS:
        by_cat[row[2]].append(row[0])

    lines = ["# Enterprise AI Market Map - Phase 1\n"]
    lines.append("Status: `phase1_candidate_universe`\n")
    lines.append("This market map organizes the initial company universe. Funding, pricing, and headcount require later source attachment.\n")
    for cat in sorted(by_cat):
        companies = by_cat[cat]
        lines.append(f"## {cat}\n")
        lines.append(f"- Company count: {len(companies)}")
        lines.append(f"- Representative companies: {', '.join(companies[:12])}")
        if cat == "Foundation Models":
            lines.append("- Buyer problem: access to frontier reasoning, multimodal, coding, and enterprise-safe models.")
            lines.append("- Maturity: high at the platform layer, still volatile on cost/performance and differentiation.")
            lines.append("- Consolidation pressure: high; distribution and compute access matter.")
        elif cat == "Infrastructure":
            lines.append("- Buyer problem: reliable compute and inference capacity without owning the full data-center stack.")
            lines.append("- Maturity: high demand, constrained by GPU economics and operational complexity.")
            lines.append("- Consolidation pressure: high; hyperscalers and chip vendors shape margins.")
        elif cat == "Agent Frameworks":
            lines.append("- Buyer problem: compose tools, memory, orchestration, and workflow logic around models.")
            lines.append("- Maturity: early-to-mid; developer adoption is strong but enterprise reliability is uneven.")
            lines.append("- Consolidation pressure: medium; frameworks can become platform features.")
        elif cat == "Enterprise Platforms":
            lines.append("- Buyer problem: put AI inside governed systems of record and workflow platforms.")
            lines.append("- Maturity: high distribution, uneven agent quality.")
            lines.append("- Consolidation pressure: high; incumbents bundle AI into existing contracts.")
        elif cat == "AI Development Platforms":
            lines.append("- Buyer problem: build, deploy, evaluate, and operate AI applications.")
            lines.append("- Maturity: mid; platform boundaries overlap with infra and observability.")
            lines.append("- Consolidation pressure: medium-to-high.")
        elif cat == "Observability":
            lines.append("- Buyer problem: trace, evaluate, debug, and monitor LLM/agent behavior.")
            lines.append("- Maturity: early-to-mid; fast-moving because agent failures are hard to inspect.")
            lines.append("- Consolidation pressure: high from Datadog/New Relic/Dynatrace and dev platforms.")
        elif cat == "Security":
            lines.append("- Buyer problem: prevent prompt injection, data leakage, model abuse, and AI supply-chain risk.")
            lines.append("- Maturity: early; urgency is rising as agents gain tool access.")
            lines.append("- Consolidation pressure: medium; security suites may absorb point solutions.")
        elif cat == "Governance":
            lines.append("- Buyer problem: prove AI systems are compliant, explainable, tested, and controlled.")
            lines.append("- Maturity: early-to-mid; regulation and procurement are demand drivers.")
            lines.append("- Consolidation pressure: medium.")
        elif cat == "Knowledge Management":
            lines.append("- Buyer problem: make enterprise knowledge searchable, answerable, and action-ready.")
            lines.append("- Maturity: mid-to-high; many products converge on enterprise search plus agents.")
            lines.append("- Consolidation pressure: high from Microsoft, Google, Atlassian, and data platforms.")
        elif cat == "Vertical AI":
            lines.append("- Buyer problem: domain-specific AI workflows with compliance and workflow context.")
            lines.append("- Maturity: varies by vertical; legal, healthcare, and support are most visible.")
            lines.append("- Consolidation pressure: medium; vertical incumbents will embed AI.")
        elif cat == "Developer Platforms":
            lines.append("- Buyer problem: accelerate software delivery and codebase understanding.")
            lines.append("- Maturity: high adoption, intense competition.")
            lines.append("- Consolidation pressure: high from GitHub, IDEs, and frontier model labs.")
        elif cat == "AI Consulting":
            lines.append("- Buyer problem: strategy, operating-model change, governance, and implementation support.")
            lines.append("- Maturity: high; differentiation depends on assets and repeatable delivery IP.")
            lines.append("- Consolidation pressure: low-to-medium; services remain relationship-led.")
        elif cat == "Managed Services":
            lines.append("- Buyer problem: outsource implementation, integration, operations, and maintenance.")
            lines.append("- Maturity: high; margin pressure rises as AI delivery commoditizes.")
            lines.append("- Consolidation pressure: medium.")
        lines.append("")
    (OUT / "market-map-phase1.md").write_text("\n".join(lines), encoding="utf-8")


def write_quadrants_and_strategy():
    leaders = [
        "OpenAI", "Anthropic", "Google DeepMind", "Microsoft Copilot", "NVIDIA",
        "Databricks", "Snowflake", "Salesforce Agentforce", "ServiceNow", "GitHub Copilot",
        "Glean", "Hugging Face"
    ]
    visionaries = [
        "Mistral AI", "Cohere", "DeepSeek", "LangChain", "LlamaIndex", "Cursor",
        "Cognition", "Harvey", "Sierra", "H Company", "Manus", "Perplexity"
    ]
    challengers = [
        "IBM watsonx", "SAP Joule", "Oracle AI", "Workday AI", "Adobe Firefly",
        "Box AI", "Datadog", "New Relic", "Dynatrace", "Accenture", "Deloitte", "McKinsey QuantumBlack"
    ]
    niche = [
        "Lakera", "Protect AI", "HiddenLayer", "Credo AI", "Patronus AI", "Hebbia",
        "Unstructured", "Pinecone", "Weaviate", "Abridge", "Hippocratic AI", "Artisan"
    ]

    quadrant = f"""# Unofficial Gartner-Style Quadrant - Phase 1

Status: `provisional`

This is not an official Gartner Magic Quadrant. It is a working strategy view.

Axes:

- X-axis: completeness of vision
- Y-axis: ability to execute

## Leaders

{', '.join(leaders)}

Rationale: strong distribution, enterprise credibility, platform breadth, model/compute depth, or developer adoption.

## Visionaries

{', '.join(visionaries)}

Rationale: strong technical or category vision, but execution scale and enterprise procurement proof vary by company.

## Challengers

{', '.join(challengers)}

Rationale: strong enterprise distribution and execution capacity, but vision may be constrained by incumbent platform incentives.

## Niche Players

{', '.join(niche)}

Rationale: focused category wedges with strategic importance, but narrower distribution or earlier maturity.

## QA Caveat

Every placement is provisional until funding, pricing, customer proof, and product depth are source-attached company by company.
"""
    (OUT / "quadrant-analysis-phase1.md").write_text(quadrant, encoding="utf-8")

    strategy = """# Strategic Analysis - Phase 1

## Funding Analysis

Phase 1 finding: capital and strategic attention concentrate in four zones:

1. Foundation models and frontier labs.
2. AI infrastructure and inference platforms.
3. Developer/coding agents.
4. Vertical AI in legal, healthcare, and customer support.

Funding details are not finalized in this phase. Later passes must attach latest round, amount, date, investors, and source per private company.

## Pricing Analysis

Pricing patterns to validate:

- Foundation models: usage/token pricing plus enterprise contracts.
- Infrastructure: GPU-hours, inference usage, reserved capacity, or enterprise commitments.
- Enterprise platforms: seat-plus-usage, bundled add-ons, or enterprise custom.
- Observability/security/governance: SaaS subscription, event/trace volume, or enterprise custom.
- Consulting/managed services: project, retainer, managed capacity, or transformation program pricing.

Main buyer friction: opaque enterprise pricing makes ROI comparison hard and creates opening for scoped, fixed-price operator offerings.

## Category SWOT

### Strengths

- Enterprise AI budgets are active and expanding.
- Incumbents have distribution and trust.
- Developer and agent ecosystems create rapid experimentation.
- Governance/security pain is visible and growing.

### Weaknesses

- Agent reliability remains uneven.
- Pricing is often opaque.
- Many offerings converge into similar "AI copilot/agent" language.
- Buyers struggle to distinguish platform value from services wrapper.

### Opportunities

- Operator-gated implementation packages.
- Source-attached competitor intelligence.
- Governance-by-design agent deployment.
- Vertical workflow wedges where generic platforms underperform.

### Threats

- Foundation model commoditization.
- Cloud/platform bundling.
- Vertical SaaS incumbents embedding AI.
- Consulting firms absorbing the budget before product vendors prove ROI.

## White Space

1. AI agent governance cockpit for mid-market operators.
   - Wedge: inventory, trace, approval, and policy checks for agent workflows.
   - Proof: detect and govern 10-20 live automations across tools.

2. Fixed-scope AI implementation diagnostic.
   - Wedge: replace bloated discovery with a source-backed 10-skill operator audit.
   - Proof: paid diagnostic converted into 30-day MVP scope.

3. Vertical workflow agents with auditable handoff.
   - Wedge: healthcare, legal, finance, logistics workflows where hallucination risk blocks adoption.
   - Proof: human-in-loop acceptance criteria and audit trail.

4. Pricing and ROI intelligence for AI software buyers.
   - Wedge: compare seat, usage, and enterprise custom economics.
   - Proof: buyer uses analysis to reject or renegotiate a vendor package.

## Competitive Threats

- Incumbent platform expansion: Microsoft, Salesforce, ServiceNow, SAP, Oracle, Adobe, and Workday can bundle AI into existing contracts.
- Foundation model commoditization: model APIs become interchangeable for many enterprise workflows.
- Open-source substitution: Llama, Mistral, DeepSeek, and ecosystem tooling pressure proprietary margins.
- Cloud-provider bundling: AWS, Azure, Google Cloud, Snowflake, and Databricks pull AI workloads into governed data platforms.
- Vertical SaaS embedding AI: incumbents add agents before startups can own workflow distribution.
- Consulting/services capture: Accenture, Deloitte, IBM, McKinsey, BCG, and others capture strategy budget and implementation access.
- Governance/security blocker: buyers delay deployment when auditability, data leakage, and agent control are weak.

## Strategic Recommendations

1. Do not compete as a generic AI platform.
   - Build around a narrow operator workflow or category-specific wedge.

2. Lead with proof, not AI vocabulary.
   - Every market claim needs source-backed competitor, pricing, and implementation evidence.

3. Use the 10-skill stack as the market-facing differentiator.
   - It answers why the offer is not just another agent builder or consulting deck.

4. Treat Skill #6 competitor teardown as mandatory for every selected use case.
   - No external publication without incumbent/pricing source attachment.

5. Prioritize white spaces where incumbents are structurally slow.
   - Governance, cross-system workflow, vertical auditability, and buyer ROI clarity.
"""
    (OUT / "strategic-analysis-phase1.md").write_text(strategy, encoding="utf-8")


def write_qa():
    counts = Counter(row[2] for row in ROWS)
    qa = ["# QA - Phase 1\n"]
    qa.append(f"- Candidate company count: {len(ROWS)}")
    qa.append("- Required range: 100-150")
    qa.append("- Count status: PASS" if 100 <= len(ROWS) <= 150 else "- Count status: FAIL")
    qa.append("- Primary category present for every company: PASS")
    qa.append("- Funding/pricing source attachment: NOT COMPLETE")
    qa.append("- Company status source attachment: NOT COMPLETE")
    qa.append("- Quadrant label unofficial: PASS")
    qa.append("- Recommendation evidence tied to phase-1 research signals: PARTIAL")
    qa.append("\n## Category Counts\n")
    for cat, count in sorted(counts.items()):
        qa.append(f"- {cat}: {count}")
    qa.append("\n## Stop Condition\n")
    qa.append("Do not call this a final competitor landscape until per-company funding, pricing, and status are source-attached.")
    (WORKING / "qa-phase1.md").write_text("\n".join(qa), encoding="utf-8")
    (SOURCE / "source-notes-phase1.md").write_text(SOURCE_NOTES, encoding="utf-8")


if __name__ == "__main__":
    write_csv()
    write_market_map()
    write_quadrants_and_strategy()
    write_qa()
    print(f"Wrote Phase 1 landscape outputs to {OUT}")
