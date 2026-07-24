# Contact-Center Agent Assist: Competitor Teardown

## Target SaaS: CCaaS Agent-Assist & Real-time Guidance

### Overview of Incumbents
1. **NICE CXone**: Massive enterprise omnichannel contact center platform.
2. **Verint**: Legacy workforce engagement and complex contact center suite.
3. **Cresta**: Premium AI-native real-time coaching and agent assist overlay.
4. **Balto**: Real-time conversational AI guidance and coaching tool.
5. **Talkdesk / Genesys**: CCaaS platforms with bolted-on AI modules.

### Product Teardown (The Legacy Model)
*   **Top 3 Features**: Real-time transcriptions, next-best-action prompts, and post-call QA analytics.
*   **Pricing Tiers**: Very expensive. NICE CXone runs $110-$249+ per agent/month plus session fees. Cresta often starts at $150k+ annually. Verint uses complex, opaque licensing bundles.
*   **Onboarding Friction**: Reddit and G2 reviews reveal extreme complexity. Verint is described as "heavy" with a steep learning curve. Cresta requires dedicated personnel to "tune" the AI models or it suffers from transcription drift and hallucinations. Balto can take two months to implement.

### Where They Are Strong (The Moat)
*   **Telephony Integration**: Deep, entrenched integrations with legacy telephony systems (Avaya, Cisco).
*   **System of Record**: They hold the historical call recordings, QA scores, and workforce management schedules.

### Where They Are Weak (The Vulnerability)
*   **Fragile AI Rules**: Real-time prompts are often based on rigid keyword triggers rather than deep semantic understanding, leading to irrelevant pop-ups that agents ignore.
*   **Model Maintenance**: The high cost isn't just the software; it's the headcount required to continuously tune the speech analytics engine to prevent transcription drift.

## Disruptive Strategy (Our Agentic Wedge)

### 1. Direct Threats
*   **Cresta** (The premium AI-native incumbent).
*   **Verint** (The legacy giant dominating the enterprise).

### 2. Table Stakes Features
*   **Sub-second Latency**: The agent must provide answers while the customer is speaking. Delay is a dealbreaker.
*   **Existing CCaaS Integration**: Must sit cleanly on top of Genesys/NICE without requiring a telephony rip-and-replace.

### 3. What We Deliberately MUST NOT Do
*   **Do not build a CCaaS platform**: We are not competing with Twilio or Genesys for call routing. We are purely the intelligence layer augmenting the human.

### 4. The 3 Gaps Our Agentic Wedge Exploits
1.  **Zero-Shot Semantic Understanding**: Replace rigid, keyword-based trigger rules with a modern LLM that actually understands context, drastically reducing irrelevant prompts and the need for dedicated "model tuning" staff.
2.  **Automated Post-Call Toil**: Automate the ACW (After Call Work) wrap-up notes and QA scoring instantly, turning a 3-minute manual task into a 3-second automated log, showing immediate ROI on agent handle time.
3.  **Consumption vs. Per-Seat Pricing**: Disrupt the $250/agent/month model by charging purely for the compute used during active calls, making it accessible to mid-market teams previously priced out of Cresta.
