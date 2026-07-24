# Disruptive Competitor Teardown: App Build / Migration Automation (Use Case 17)

## OSINT Source Map & Methodology
- **Sources Scraped:** Reddit (r/programming, r/lowcode), G2 Reviews, GoodFirms.
- **Search Queries:** "OutSystems vs Mendix pricing", "Appian onboarding friction".
- **Methodology:** We targeted the enterprise low-code and BPM (Business Process Management) platforms that trap customers in proprietary ecosystems to automate basic workflows.

## Company Overview: Legacy Incumbents
1. **OutSystems:** Enterprise low-code application platform.
2. **Mendix:** Heavyweight low-code for industrial/enterprise.
3. **Appian:** Complex BPM and case management.
4. **Pegasystems (Pega):** Massive scale enterprise automation.
5. **Oracle APEX:** Database-centric low code.

## Product Teardown
- **Top 3 Features:** Visual workflow builders, one-click deployments, enterprise governance/RBAC.
- **Pricing Tiers:** Extremely prohibitive for mid-market. Custom enterprise licensing only. Pega starts at ~$35/user/month but enterprise scales into hundreds of thousands.
- **Onboarding Friction:** Reddit reviews consistently cite a massive learning curve. You need specialized certifications (e.g., "Pega Certified Architect") to use these "low code" tools. Severe friction from proprietary lock-in.

## Where They Are Strong
- **Scalability:** Very performant for massive, complex enterprise state machines.
- **Governance:** Deep control over who can build and deploy what.

## Where They Are Weak
- **The "Overkill" Problem:** Too heavy and expensive for 80% of agile workflows.
- **Vendor Lock-in:** Code generated is proprietary. Ejecting to standard React/Node is often impossible.
- **Developer Hate:** Traditional software engineers despise proprietary visual builders.

## Disruptive Strategy
- **Top 2 Direct Threats:** OutSystems and Appian.
- **Table Stakes:** RBAC, enterprise security, fast deployment.
- **What We Must NOT Do:** We must not build another proprietary visual flowchart language.
- **3 Specific Gaps our Agent Exploits:**
  1. **Standard Output:** Agent generates standard, ejectable code (e.g., React/Python) instead of locking the user into a proprietary runtime.
  2. **Prompt-to-App:** Replaces the complex 4-week onboarding of a visual builder with a natural language interface that scaffolds apps in seconds.
  3. **No Specialized Certs:** Eliminates the need for expensive "certified developers" to maintain the application.
