# Reddit Fact-Check Report

- Status: draft
- Source: `/mnt/c/Users/sheke/Desktop/agent-validation-authority-deck/agent-validation-authority.pptx`
- Extraction method: `sidecar:deck.md`
- Claims extracted: 40

## Method

Reddit evidence is treated as community/operator evidence. Numeric, regulatory, market-size, funding, adoption, and date claims remain primary-source-required unless the claim only asks whether Reddit discusses the issue.

## Claim Inventory

### claim-001 - Section 2

Claim: Klarna publicly reversed its AI-first support after quality tanked.

- Evidence need: `reddit_evidence`
- Reddit query: `klarna publicly reversed ai-first support quality tanked`
- Primary source required: `false`
- Reddit evidence status: `no_reddit_evidence_found`

### claim-002 - Section 2

Claim: The blocker is the same everywhere: *nobody can prove the agent is safe to run.* That proof is a market.

- Evidence need: `reddit_evidence`
- Reddit query: `blocker same everywhere nobody prove safe run proof market`
- Primary source required: `false`
- Reddit evidence status: `supported_by_reddit_evidence`

  - Reddit post `post` score 542 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/`
    - AI AGENTS today are far more DANGEROUS that you think I know it's a long post, but I think this is something AI industry needs to talk about more. I'd love to hear the opinion from everyone. Real quick, so I built a multi-agent AI system that has root shell access to any Linux environment, this one I chose under Kal...
  - Reddit post `post` score 7 from `https://old.reddit.com/r/AI_Agents/comments/1t4gm62/ai_agent_governance_and_liability/`
    - AI Agent Governance and Liability? Working in business process automation and getting deeper into AI agent research, governance and liability kept coming up as the questions nobody had clean answers for. Not edge cases — central concerns for anyone building agents that touch real data and real outcomes. A few things...
  - Reddit comment `t1_ok2l0v3` score 1 from `https://old.reddit.com/r/AI_Agents/comments/1t4gm62/ai_agent_governance_and_liability/ok2l0v3/`
    - This is absolutely on the radar for production deployments. Key distinction being…. technical access is not the same as delegated authority. A token, role, or API permission can prove the agent was allowed to call a tool. It does not prove: - the agent had the right business context - the data was appropriate for th...

### claim-003 - Section 3

Claim: The market moved from "can we build an agent" to "can we trust one" 2023–24: the race was capability — frameworks, models, demos.

- Evidence need: `mixed`
- Reddit query: `market moved build trust one race was capability frameworks models demos`
- Primary source required: `true`
- Reddit evidence status: `reddit_signal_found_primary_source_required`

  - Reddit post `post` score 542 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/`
    - AI AGENTS today are far more DANGEROUS that you think I know it's a long post, but I think this is something AI industry needs to talk about more. I'd love to hear the opinion from everyone. Real quick, so I built a multi-agent AI system that has root shell access to any Linux environment, this one I chose under Kal...
  - Reddit comment `t1_n5zsmz8` score 4 from `https://old.reddit.com/r/ChatGPT/comments/1m9bv7d/i_tested_openais_20month_agent_so_you_dont_have/n5zsmz8/`
    - I literally built this myself. Took about a month to build the agentic model. I had to work with my brokerage firm to get the appropriate API key, and I created a new account within my profile and funded it with $2000. It operates on tight rules about what companies I accept (ie: no russian, chinese, etc), and what...
  - Reddit post `post` score 275 from `https://old.reddit.com/r/NextGenAITool/comments/1u315jd/how_to_actually_build_an_ai_agent_a_complete/`
    - How to Actually Build an AI Agent: A Complete Step-by-Step Guide for 2026 Artificial Intelligence is evolving rapidly, and AI agents are becoming one of the most transformative technologies for businesses, developers, and creators. Unlike traditional chatbots, AI agents can reason, remember, interact with tools, and...

### claim-004 - Section 3

Claim: 2026: capability is commoditized; **the model is no longer the moat.** The new question is operational: predict it, audit it, roll it back.

- Evidence need: `primary_required`
- Reddit query: `capability commoditized model longer moat new question operational predict audit roll back`
- Primary source required: `true`
- Reddit evidence status: `requires_primary_source_corroboration`

  - Reddit comment `t1_o8z5w7r` score 12 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/o8z5w7r/`
    - You're right that none of the individual techniques are new. OSINT practitioners have been doing all of this manually for years and data aggregators have been running collection algorithms for a long time What's different isn't the capability, it's the operational model What I'm describing is It's autonomous agents...
  - Reddit post `post` score 542 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/`
    - AI AGENTS today are far more DANGEROUS that you think I know it's a long post, but I think this is something AI industry needs to talk about more. I'd love to hear the opinion from everyone. Real quick, so I built a multi-agent AI system that has root shell access to any Linux environment, this one I chose under Kal...
  - Reddit comment `t1_o6yd60q` score 1 from `https://old.reddit.com/r/aiagents/comments/1qwanou/i_built_an_airgapped_agent_governance_system_in_a/o6yd60q/`
    - Invariants first means the constraints exist before any model touches the system. The model accelerates implementation inside a bounded space, not an open one. On tool approval: the audit agent handles it at the task type level, not per agent. Rules are scoped by what a tool does, not which agent calls it. The same...

### claim-005 - Section 3

Claim: *Trust is now an infrastructure problem before it is a product feature.*

- Evidence need: `reddit_evidence`
- Reddit query: `trust now infrastructure problem product feature`
- Primary source required: `false`
- Reddit evidence status: `supported_by_reddit_evidence`

  - Reddit post `post` score 4 from `https://old.reddit.com/r/aiagents/comments/1qwanou/i_built_an_airgapped_agent_governance_system_in_a/`
    - I built an airgapped agent governance system in a week by changing how I use LLMs I want to share a concrete example of what 100% AI-native workflows can accomplish. Because most discussions still treat LLMs and specialized coding tools as autocomplete for code, but without guardrails. Last week I built a production...
  - Reddit post `post` score 542 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/`
    - AI AGENTS today are far more DANGEROUS that you think I know it's a long post, but I think this is something AI industry needs to talk about more. I'd love to hear the opinion from everyone. Real quick, so I built a multi-agent AI system that has root shell access to any Linux environment, this one I chose under Kal...
  - Reddit post `post` score 5473 from `https://old.reddit.com/r/whennews/comments/1sxfm3b/the_pocketos_boss_puts_greater_blame_on_railways/`
    - The PocketOS boss puts greater blame on Railway’s architecture than on the deranged AI agent https://www.tomshardware.com/tech-industry/artificial-intelligence/claude-powered-ai-coding-agent-deletes-entire-company-database-in-9-seconds-backups-zapped-after-cursor-tool-powered-by-anthropics-claude-goes-rogue The foun...

### claim-006 - Section 4

Claim: April 17, 2026: regulators handed agentic AI back to the banks **SR 26-2** (OCC / Fed / FDIC) replaced SR 11-7 — the 15-year model-risk rulebook.

- Evidence need: `mixed`
- Reddit query: `april regulators handed back banks occ fed fdic replaced year model-risk rulebook`
- Primary source required: `true`
- Reddit evidence status: `no_reddit_evidence_found`

### claim-007 - Section 4

Claim: One sentence defines the moment: *"Generative AI and agentic AI models… are not within the scope of this guidance."* Translation: banks own agentic-AI governance with **no playbook** — and an AI rulemaking is coming.

- Evidence need: `reddit_evidence`
- Reddit query: `one sentence defines moment generative models within scope guidance translation banks own agentic-ai governance`
- Primary source required: `false`
- Reddit evidence status: `no_reddit_evidence_found`

### claim-008 - Section 4

Claim: Examiners still ask: *"What is your monitoring framework?

- Evidence need: `reddit_evidence`
- Reddit query: `examiners still ask what your monitoring framework`
- Primary source required: `false`
- Reddit evidence status: `supported_by_reddit_evidence`

  - Reddit post `post` score 911 from `https://old.reddit.com/user/ibm/comments/1pii4tg/what_are_the_real_challenges_of_automating_with/`
    - What are the real challenges of automating with AI agents? Automating with Agentic AI can get messy behind the scenes. Maybe a workflow breaks without context. Maybe tools don’t talk, or an agent takes an unexpected path. Let’s talk. What teams need to know about AI agents 🤖 Every team wants the efficiency. But let’...
  - Reddit post `post` score 275 from `https://old.reddit.com/r/NextGenAITool/comments/1u315jd/how_to_actually_build_an_ai_agent_a_complete/`
    - How to Actually Build an AI Agent: A Complete Step-by-Step Guide for 2026 Artificial Intelligence is evolving rapidly, and AI agents are becoming one of the most transformative technologies for businesses, developers, and creators. Unlike traditional chatbots, AI agents can reason, remember, interact with tools, and...
  - Reddit post `post` score 542 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/`
    - AI AGENTS today are far more DANGEROUS that you think I know it's a long post, but I think this is something AI industry needs to talk about more. I'd love to hear the opinion from everyone. Real quick, so I built a multi-agent AI system that has root shell access to any Linux environment, this one I chose under Kal...

### claim-009 - Section 4

Claim: What is your effective challenge?"* > "Can you name the person whose name should be on the examination finding?"

- Evidence need: `reddit_evidence`
- Reddit query: `what your effective challenge you name person whose examination finding`
- Primary source required: `false`
- Reddit evidence status: `supported_by_reddit_evidence`

  - Reddit post `post` score 542 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/`
    - AI AGENTS today are far more DANGEROUS that you think I know it's a long post, but I think this is something AI industry needs to talk about more. I'd love to hear the opinion from everyone. Real quick, so I built a multi-agent AI system that has root shell access to any Linux environment, this one I chose under Kal...
  - Reddit comment `t1_o8zm8oc` score 16 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/o8zm8oc/`
    - Except its mostly wrong, and glosses over the fact that most of those require authentication, rate limited, paywalled. Using writing style alone is highly subjective and prone to false positives at a high rate. Also, the person had to have doxxed themselves in someway in the first place to have that information out...
  - Reddit comment `t1_o8ytwdf` score 16 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/o8ytwdf/`
    - This person built an autonomous AI system that profiled two real people in under 25 minutes using only a name and one username. Here's what actually happened and why it matters: What they built A swarm of AI agents running in parallel on a Kali Linux machine, each with its own terminal, sharing a persistent memory d...

### claim-010 - Section 5

Claim: The pain is deployed, not hypothetical — and it is failing **Wendy's FreshAI** takes drive-thru orders end-to-end; **Mercedes MBUX**, **Home Depot Magic Apron** run live.

- Evidence need: `reddit_evidence`
- Reddit query: `pain deployed hypothetical failing wendy freshai takes drive-thru orders end-to-end mercedes mbux home depot`
- Primary source required: `false`
- Reddit evidence status: `weak_reddit_support`

  - Reddit post `post` score 542 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/`
    - AI AGENTS today are far more DANGEROUS that you think I know it's a long post, but I think this is something AI industry needs to talk about more. I'd love to hear the opinion from everyone. Real quick, so I built a multi-agent AI system that has root shell access to any Linux environment, this one I chose under Kal...
  - Reddit post `post` score 911 from `https://old.reddit.com/user/ibm/comments/1pii4tg/what_are_the_real_challenges_of_automating_with/`
    - What are the real challenges of automating with AI agents? Automating with Agentic AI can get messy behind the scenes. Maybe a workflow breaks without context. Maybe tools don’t talk, or an agent takes an unexpected path. Let’s talk. What teams need to know about AI agents 🤖 Every team wants the efficiency. But let’...

### claim-011 - Section 5

Claim: Manual QA covers ~100 scenarios; real users trigger millions.

- Evidence need: `reddit_evidence`
- Reddit query: `manual covers scenarios real users trigger millions`
- Primary source required: `false`
- Reddit evidence status: `no_reddit_evidence_found`

### claim-012 - Section 5

Claim: The gap between "deployed" and "validated" is where we live.

- Evidence need: `reddit_evidence`
- Reddit query: `gap deployed where live`
- Primary source required: `false`
- Reddit evidence status: `supported_by_reddit_evidence`

  - Reddit post `post` score 542 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/`
    - AI AGENTS today are far more DANGEROUS that you think I know it's a long post, but I think this is something AI industry needs to talk about more. I'd love to hear the opinion from everyone. Real quick, so I built a multi-agent AI system that has root shell access to any Linux environment, this one I chose under Kal...
  - Reddit post `post` score 911 from `https://old.reddit.com/user/ibm/comments/1pii4tg/what_are_the_real_challenges_of_automating_with/`
    - What are the real challenges of automating with AI agents? Automating with Agentic AI can get messy behind the scenes. Maybe a workflow breaks without context. Maybe tools don’t talk, or an agent takes an unexpected path. Let’s talk. What teams need to know about AI agents 🤖 Every team wants the efficiency. But let’...
  - Reddit comment `t1_oklc3s3` score 2 from `https://old.reddit.com/r/AI_Agents/comments/1t4gm62/ai_agent_governance_and_liability/oklc3s3/`
    - The "technical authorization isn't accountability" framing is the most accurate sentence I've read on this. Most governance conversations collapse the two and pretend the audit trail is downstream paperwork rather than a load-bearing requirement. Worth separating your three questions because they live in different l...

### claim-013 - Section 6

Claim: Nobody independent can grade the agents — the labs grade themselves Foundation labs ship native guardrails — but they cannot certify their own ecosystem.

- Evidence need: `reddit_evidence`
- Reddit query: `nobody independent grade labs themselves foundation ship native guardrails they certify own ecosystem`
- Primary source required: `false`
- Reddit evidence status: `weak_reddit_support`

  - Reddit post `post` score 577 from `https://old.reddit.com/r/AI_Agents/comments/1oajp38/most_of_you_shouldnt_build_an_ai_agent_and_heres/`
    - Most of you shouldnt build an AI agent and heres why After watching another client spend $80k on an AI agent they shut down three months later, I need to say this out loud. The vendors wont tell you this. Your CTO who just came back from a conference definitely wont tell you this. But someone needs to. Most companie...

### claim-014 - Section 6

Claim: Eval vendors (Braintrust, Arize, Patronus) sell tooling to the **builder**, not assurance to the **buyer**.

- Evidence need: `reddit_evidence`
- Reddit query: `eval vendors braintrust arize patronus sell tooling builder assurance buyer`
- Primary source required: `false`
- Reddit evidence status: `no_reddit_evidence_found`

### claim-015 - Section 6

Claim: Internal model-risk teams have no agent-native method.

- Evidence need: `reddit_evidence`
- Reddit query: `internal model-risk teams agent-native method`
- Primary source required: `false`
- Reddit evidence status: `supported_by_reddit_evidence`

  - Reddit post `post` score 542 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/`
    - AI AGENTS today are far more DANGEROUS that you think I know it's a long post, but I think this is something AI industry needs to talk about more. I'd love to hear the opinion from everyone. Real quick, so I built a multi-agent AI system that has root shell access to any Linux environment, this one I chose under Kal...
  - Reddit comment `t1_nkbloop` score 3 from `https://old.reddit.com/r/AI_Agents/comments/1oajp38/most_of_you_shouldnt_build_an_ai_agent_and_heres/nkbloop/`
    - I've got another reason for you - *you shouldn't build anything that doesn't make YOUR beer taste better*. Engineering teams notoriously have a horrible not-invented-here syndrome for every tech wave, and they're extra bad when it comes to AI. Your internal eng team shouldn't be building better accounting platforms...

### claim-016 - Section 6

Claim: *The one thing none of them can claim is independence.

- Evidence need: `reddit_evidence`
- Reddit query: `one thing none claim independence`
- Primary source required: `false`
- Reddit evidence status: `supported_by_reddit_evidence`

  - Reddit post `post` score 577 from `https://old.reddit.com/r/AI_Agents/comments/1oajp38/most_of_you_shouldnt_build_an_ai_agent_and_heres/`
    - Most of you shouldnt build an AI agent and heres why After watching another client spend $80k on an AI agent they shut down three months later, I need to say this out loud. The vendors wont tell you this. Your CTO who just came back from a conference definitely wont tell you this. But someone needs to. Most companie...
  - Reddit comment `t1_o91s4zc` score 20 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/o91s4zc/`
    - I agree, but I think it's a fake/contrived situation. I work in this field and the first thing I will say as someone who could put this together, anyone with this skill isn't writing out this manifesto. Aside from that, it is pure bullshit . Bullshit Numero Uno : A 15-minute timeline for an autonomous script to navi...
  - Reddit comment `t1_o8z5w7r` score 12 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/o8z5w7r/`
    - You're right that none of the individual techniques are new. OSINT practitioners have been doing all of this manually for years and data aggregators have been running collection algorithms for a long time What's different isn't the capability, it's the operational model What I'm describing is It's autonomous agents...

### claim-017 - Section 7

Claim: Certify the agent.** *Nobody owns it.* That is our lane: the independent referee for the other eight.

- Evidence need: `reddit_evidence`
- Reddit query: `certify nobody owns lane independent referee for other eight`
- Primary source required: `false`
- Reddit evidence status: `supported_by_reddit_evidence`

  - Reddit post `post` score 542 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/`
    - AI AGENTS today are far more DANGEROUS that you think I know it's a long post, but I think this is something AI industry needs to talk about more. I'd love to hear the opinion from everyone. Real quick, so I built a multi-agent AI system that has root shell access to any Linux environment, this one I chose under Kal...
  - Reddit comment `t1_nu6cqci` score 1 from `https://old.reddit.com/user/ibm/comments/1pii4tg/what_are_the_real_challenges_of_automating_with/nu6cqci/`
    - Nobody is going to bring AI into their workflow other than developers, and they aren’t using AI the way you think they are. They’re just using it to write code faster which allows them to create the workflows you think you can automate with AI. They reality is that business specific workflows are too niche for someo...
  - Reddit post `post` score 911 from `https://old.reddit.com/user/ibm/comments/1pii4tg/what_are_the_real_challenges_of_automating_with/`
    - What are the real challenges of automating with AI agents? Automating with Agentic AI can get messy behind the scenes. Maybe a workflow breaks without context. Maybe tools don’t talk, or an agent takes an unexpected path. Let’s talk. What teams need to know about AI agents 🤖 Every team wants the efficiency. But let’...

### claim-018 - Section 9

Claim: Our position: certify the autonomous agent before it ships Package agent assurance as a **hiring bar for the agent**: *"passed before you deployed it."* Sell to the risk owner, not the developer — that is where pricing power lives.

- Evidence need: `reddit_evidence`
- Reddit query: `position certify autonomous ships package assurance hiring bar for passed you deployed sell risk`
- Primary source required: `false`
- Reddit evidence status: `no_reddit_evidence_found`

### claim-019 - Section 9

Claim: Output the buyer can show a regulator, a board, or a court.

- Evidence need: `reddit_evidence`
- Reddit query: `output buyer show regulator board court`
- Primary source required: `false`
- Reddit evidence status: `supported_by_reddit_evidence`

  - Reddit post `post` score 542 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/`
    - AI AGENTS today are far more DANGEROUS that you think I know it's a long post, but I think this is something AI industry needs to talk about more. I'd love to hear the opinion from everyone. Real quick, so I built a multi-agent AI system that has root shell access to any Linux environment, this one I chose under Kal...
  - Reddit post `post` score 7 from `https://old.reddit.com/r/AI_Agents/comments/1t4gm62/ai_agent_governance_and_liability/`
    - AI Agent Governance and Liability? Working in business process automation and getting deeper into AI agent research, governance and liability kept coming up as the questions nobody had clean answers for. Not edge cases — central concerns for anyone building agents that touch real data and real outcomes. A few things...
  - Reddit comment `t1_ok57gil` score 2 from `https://old.reddit.com/r/AI_Agents/comments/1t4gm62/ai_agent_governance_and_liability/ok57gil/`
    - my read: everyone reaches for observability tooling and policy engines on this, and that's the wrong layer. the only context snapshot that holds up to a regulator is one taken before the model call returns, not reconstructed from logs after. that means a gateway in front of every llm invocation and every tool call p...

### claim-020 - Section 10

Claim: What we are: the UL / SOC-2 for AI agents An **independent authority** whose stamp the market trusts.

- Evidence need: `reddit_evidence`
- Reddit query: `what soc-2 for independent whose stamp market trusts`
- Primary source required: `false`
- Reddit evidence status: `supported_by_reddit_evidence`

  - Reddit comment `t1_ok2nojd` score 1 from `https://old.reddit.com/r/AI_Agents/comments/1t4gm62/ai_agent_governance_and_liability/ok2nojd/`
    - Completely agree on designing HITL in from the start, retrofitting governance onto an existing agent stack is painful and usually incomplete. The EU AI Act deadline is real pressure. What we see in practice: organizations assume "we have logs" is sufficient for Art. 12. It isn't, inviolable means tamper-evident by d...
  - Reddit comment `t1_ok2c2h5` score 1 from `https://old.reddit.com/r/AI_Agents/comments/1t4gm62/ai_agent_governance_and_liability/ok2c2h5/`
    - Tracing mechanism in place, with all temperature set to zero. There’s no definite answer now unfortunately (see below) This is more on rag and agent tools design… I would say it’s better to design the human in the loop mechanism properly in the first place, not the other way around. I have led compliance projects /...

### claim-021 - Section 10

Claim: Independence is not a feature — it is the entire product.

- Evidence need: `reddit_evidence`
- Reddit query: `independence feature entire product`
- Primary source required: `false`
- Reddit evidence status: `weak_reddit_support`

  - Reddit post `post` score 3269 from `https://old.reddit.com/r/ChatGPT/comments/1m9bv7d/i_tested_openais_20month_agent_so_you_dont_have/`
    - I Tested OpenAI's $20/month “Agent” So You Don’t Have To. It Can’t Shop, Book, or Reserve Anything Spent my afternoon stress-testing the new “Agent” feature that’s supposed to handle shopping, travel, and reservations for you. Here’s the real-world outcome: What the Marketing Promised: AI agent that browses the web...

### claim-022 - Section 11

Claim: Deliverable: a report the buyer hands their examiner + a live assurance dashboard + a time-boxed "Validated" mark.

- Evidence need: `reddit_evidence`
- Reddit query: `deliverable report buyer hands examiner live assurance dashboard time-boxed mark`
- Primary source required: `false`
- Reddit evidence status: `supported_by_reddit_evidence`

  - Reddit post `post` score 577 from `https://old.reddit.com/r/AI_Agents/comments/1oajp38/most_of_you_shouldnt_build_an_ai_agent_and_heres/`
    - Most of you shouldnt build an AI agent and heres why After watching another client spend $80k on an AI agent they shut down three months later, I need to say this out loud. The vendors wont tell you this. Your CTO who just came back from a conference definitely wont tell you this. But someone needs to. Most companie...
  - Reddit comment `t1_oklc3s3` score 2 from `https://old.reddit.com/r/AI_Agents/comments/1t4gm62/ai_agent_governance_and_liability/oklc3s3/`
    - The "technical authorization isn't accountability" framing is the most accurate sentence I've read on this. Most governance conversations collapse the two and pretend the audit trail is downstream paperwork rather than a load-bearing requirement. Worth separating your three questions because they live in different l...
  - Reddit comment `t1_nkb98p0` score 1 from `https://old.reddit.com/r/AI_Agents/comments/1oajp38/most_of_you_shouldnt_build_an_ai_agent_and_heres/nkb98p0/`
    - Yeah I just got let go after three months from a company with all of the problems you stated, all of which I shared with them about two weeks after being hired and beginning my Discovery phase. AI wasn't the quick fix the guy who hired me seemed to think it was. He hired me to be the "strategic mind" behind his AI v...

### claim-023 - Section 12

Claim: Beachhead: the SR 26-2 vacuum in financial services Banks must self-determine agentic-AI controls — and have nothing.

- Evidence need: `primary_required`
- Reddit query: `beachhead vacuum financial services banks self-determine agentic-ai controls nothing`
- Primary source required: `true`
- Reddit evidence status: `requires_primary_source_corroboration`

### claim-024 - Section 12

Claim: The buyer and budget already exist: **model risk / AI governance** is a mandated function.

- Evidence need: `reddit_evidence`
- Reddit query: `buyer budget exist model risk governance mandated function`
- Primary source required: `false`
- Reddit evidence status: `supported_by_reddit_evidence`

  - Reddit comment `t1_o3wyslg` score 1 from `https://old.reddit.com/r/aiagents/comments/1qwanou/i_built_an_airgapped_agent_governance_system_in_a/o3wyslg/`
    - That’s a really elegant way to frame it... latency as a function of risk. So you basically turn your governance layer into a high-pass filter rather than a bottleneck if Im understanding that correctly. The cheap and asynchronous proposal to execution path is the real winner here. Most people over engineer for the 1...
  - Reddit post `post` score 542 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/`
    - AI AGENTS today are far more DANGEROUS that you think I know it's a long post, but I think this is something AI industry needs to talk about more. I'd love to hear the opinion from everyone. Real quick, so I built a multi-agent AI system that has root shell access to any Linux environment, this one I chose under Kal...
  - Reddit post `post` score 4 from `https://old.reddit.com/r/aiagents/comments/1qwanou/i_built_an_airgapped_agent_governance_system_in_a/`
    - I built an airgapped agent governance system in a week by changing how I use LLMs I want to share a concrete example of what 100% AI-native workflows can accomplish. Because most discussions still treat LLMs and specialized coding tools as autocomplete for code, but without guardrails. Last week I built a production...

### claim-025 - Section 12

Claim: The regulatory vacuum is the opening; the coming AI RFI is the deadline.

- Evidence need: `reddit_evidence`
- Reddit query: `regulatory vacuum opening coming rfi deadline`
- Primary source required: `false`
- Reddit evidence status: `no_reddit_evidence_found`

### claim-026 - Section 13

Claim: We don't certify chatbots — we validate the agents MRM can't Skip the BAU: generic support bots and OCR are solved, low-stakes, vendor-benchmarked.

- Evidence need: `reddit_evidence`
- Reddit query: `don certify chatbots mrm skip bau generic support bots ocr solved low-stakes vendor-benchmarked`
- Primary source required: `false`
- Reddit evidence status: `no_reddit_evidence_found`

### claim-027 - Section 13

Claim: **AML / fraud investigation** agents → SAR quality.

- Evidence need: `reddit_evidence`
- Reddit query: `aml fraud investigation sar quality`
- Primary source required: `false`
- Reddit evidence status: `no_reddit_evidence_found`

### claim-028 - Section 13

Claim: **SecOps auto-remediation** → audit risk.

- Evidence need: `reddit_evidence`
- Reddit query: `secops auto-remediation audit risk`
- Primary source required: `false`
- Reddit evidence status: `supported_by_reddit_evidence`

  - Reddit post `post` score 4 from `https://old.reddit.com/r/aiagents/comments/1qwanou/i_built_an_airgapped_agent_governance_system_in_a/`
    - I built an airgapped agent governance system in a week by changing how I use LLMs I want to share a concrete example of what 100% AI-native workflows can accomplish. Because most discussions still treat LLMs and specialized coding tools as autocomplete for code, but without guardrails. Last week I built a production...
  - Reddit comment `t1_o6yd60q` score 1 from `https://old.reddit.com/r/aiagents/comments/1qwanou/i_built_an_airgapped_agent_governance_system_in_a/o6yd60q/`
    - Invariants first means the constraints exist before any model touches the system. The model accelerates implementation inside a bounded space, not an open one. On tool approval: the audit agent handles it at the task type level, not per agent. Rules are scoped by what a tool does, not which agent calls it. The same...

### claim-029 - Section 14

Claim: Sell to the CRO; the examiner is the judge **Economic buyer:** Head of Model Risk / Chief Risk Officer — holds budget and personal liability.

- Evidence need: `reddit_evidence`
- Reddit query: `sell cro examiner judge economic buyer head model risk chief officer holds budget personal`
- Primary source required: `false`
- Reddit evidence status: `supported_by_reddit_evidence`

  - Reddit post `post` score 542 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/`
    - AI AGENTS today are far more DANGEROUS that you think I know it's a long post, but I think this is something AI industry needs to talk about more. I'd love to hear the opinion from everyone. Real quick, so I built a multi-agent AI system that has root shell access to any Linux environment, this one I chose under Kal...
  - Reddit post `post` score 4 from `https://old.reddit.com/r/aiagents/comments/1qwanou/i_built_an_airgapped_agent_governance_system_in_a/`
    - I built an airgapped agent governance system in a week by changing how I use LLMs I want to share a concrete example of what 100% AI-native workflows can accomplish. Because most discussions still treat LLMs and specialized coding tools as autocomplete for code, but without guardrails. Last week I built a production...
  - Reddit post `post` score 275 from `https://old.reddit.com/r/NextGenAITool/comments/1u315jd/how_to_actually_build_an_ai_agent_a_complete/`
    - How to Actually Build an AI Agent: A Complete Step-by-Step Guide for 2026 Artificial Intelligence is evolving rapidly, and AI agents are becoming one of the most transformative technologies for businesses, developers, and creators. Unlike traditional chatbots, AI agents can reason, remember, interact with tools, and...

### claim-030 - Section 14

Claim: **Champion:** the AI-governance lead whose job is impossible without us.

- Evidence need: `reddit_evidence`
- Reddit query: `champion ai-governance lead whose job impossible`
- Primary source required: `false`
- Reddit evidence status: `no_reddit_evidence_found`

### claim-031 - Section 14

Claim: **User:** the line-of-business that must pass our gate to ship.

- Evidence need: `reddit_evidence`
- Reddit query: `user line-of-business pass gate ship`
- Primary source required: `false`
- Reddit evidence status: `no_reddit_evidence_found`

### claim-032 - Section 14

Claim: **The rejectable counterparty:** the **bank examiner** — our dossier must survive exams.

- Evidence need: `reddit_evidence`
- Reddit query: `rejectable counterparty bank examiner dossier survive exams`
- Primary source required: `false`
- Reddit evidence status: `weak_reddit_support`

  - Reddit post `post` score 542 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/`
    - AI AGENTS today are far more DANGEROUS that you think I know it's a long post, but I think this is something AI industry needs to talk about more. I'd love to hear the opinion from everyone. Real quick, so I built a multi-agent AI system that has root shell access to any Linux environment, this one I chose under Kal...

### claim-033 - Section 14

Claim: That bar is the forcing function and the moat: survive exams once, become un-switchable.

- Evidence need: `reddit_evidence`
- Reddit query: `bar forcing function moat survive exams once become un-switchable`
- Primary source required: `false`
- Reddit evidence status: `weak_reddit_support`

  - Reddit post `post` score 275 from `https://old.reddit.com/r/NextGenAITool/comments/1u315jd/how_to_actually_build_an_ai_agent_a_complete/`
    - How to Actually Build an AI Agent: A Complete Step-by-Step Guide for 2026 Artificial Intelligence is evolving rapidly, and AI agents are becoming one of the most transformative technologies for businesses, developers, and creators. Unlike traditional chatbots, AI agents can reason, remember, interact with tools, and...
  - Reddit comment `t1_oklc3s3` score 2 from `https://old.reddit.com/r/AI_Agents/comments/1t4gm62/ai_agent_governance_and_liability/oklc3s3/`
    - The "technical authorization isn't accountability" framing is the most accurate sentence I've read on this. Most governance conversations collapse the two and pretend the audit trail is downstream paperwork rather than a load-bearing requirement. Worth separating your three questions because they live in different l...

### claim-034 - Section 15

Claim: The dossier maps to exactly what examiners already ask SR 26-2 keeps three validation pillars: **conceptual soundness, outcomes analysis, ongoing monitoring.** We mirror that structure — instantly legible, hard to argue with.

- Evidence need: `primary_required`
- Reddit query: `dossier maps exactly what examiners ask keeps three pillars conceptual soundness outcomes analysis ongoing`
- Primary source required: `true`
- Reddit evidence status: `requires_primary_source_corroboration`

### claim-035 - Section 15

Claim: Add the agentic layer SR 26-2 omits: tool-call safety, autonomy bounds, multi-agent error propagation.

- Evidence need: `primary_required`
- Reddit query: `add layer omits tool-call safety autonomy bounds multi-agent error propagation`
- Primary source required: `true`
- Reddit evidence status: `requires_primary_source_corroboration`

### claim-036 - Section 15

Claim: Anchor to NIST AI RMF + ISO/IEC 42001 so it reads as standard, not startup.

- Evidence need: `primary_required`
- Reddit query: `anchor nist rmf iso iec reads standard startup`
- Primary source required: `true`
- Reddit evidence status: `requires_primary_source_corroboration`

### claim-037 - Section 15

Claim: *We give examiners the artifact they're about to demand.*

- Evidence need: `reddit_evidence`
- Reddit query: `give examiners artifact they demand`
- Primary source required: `false`
- Reddit evidence status: `supported_by_reddit_evidence`

  - Reddit post `post` score 542 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/`
    - AI AGENTS today are far more DANGEROUS that you think I know it's a long post, but I think this is something AI industry needs to talk about more. I'd love to hear the opinion from everyone. Real quick, so I built a multi-agent AI system that has root shell access to any Linux environment, this one I chose under Kal...
  - Reddit comment `t1_n56qt5x` score 20 from `https://old.reddit.com/r/ChatGPT/comments/1m9bv7d/i_tested_openais_20month_agent_so_you_dont_have/n56qt5x/`
    - This is exactly the kind of “soft failure” that makes Agent risky for serious use: when asked to synthesize or summarize data (especially unstructured logs, chat transcripts, or behavioral sessions), it often “fills in the blanks” with hallucinated insights or fabricated details. This isn’t a bug it’s a direct resul...
  - Reddit comment `t1_o8zm8oc` score 16 from `https://old.reddit.com/r/ArtificialInteligence/comments/1rmdiu3/ai_agents_today_are_far_more_dangerous_that_you/o8zm8oc/`
    - Except its mostly wrong, and glosses over the fact that most of those require authentication, rate limited, paywalled. Using writing style alone is highly subjective and prone to false positives at a high rate. Also, the person had to have doxxed themselves in someway in the first place to have that information out...

### claim-038 - Section 16

Claim: **Subscription:** annual per-agent continuous assurance — drift, re-validation, exam support.

- Evidence need: `reddit_evidence`
- Reddit query: `subscription annual per-agent continuous assurance drift re-validation exam support`
- Primary source required: `false`
- Reddit evidence status: `weak_reddit_support`

  - Reddit post `post` score 275 from `https://old.reddit.com/r/NextGenAITool/comments/1u315jd/how_to_actually_build_an_ai_agent_a_complete/`
    - How to Actually Build an AI Agent: A Complete Step-by-Step Guide for 2026 Artificial Intelligence is evolving rapidly, and AI agents are becoming one of the most transformative technologies for businesses, developers, and creators. Unlike traditional chatbots, AI agents can reason, remember, interact with tools, and...

### claim-039 - Section 16

Claim: Buyer-funded, sits in the audit/MRM budget line — not a new category to justify.

- Evidence need: `reddit_evidence`
- Reddit query: `buyer-funded sits audit mrm budget line new category justify`
- Primary source required: `false`
- Reddit evidence status: `no_reddit_evidence_found`

### claim-040 - Section 16

Claim: Pilot proves demand; subscription is the annuity.

- Evidence need: `reddit_evidence`
- Reddit query: `pilot proves demand subscription annuity`
- Primary source required: `false`
- Reddit evidence status: `no_reddit_evidence_found`

## Follow-Up

- Extract or provide Reddit thread URLs for every high-priority query.
- Use official sources for all `primary_required` and `mixed` claims.
- Have the agent review evidence excerpts before marking the report reviewed.
