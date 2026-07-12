# HR & Onboarding Agent: Competitor Teardown

## Target SaaS: HRIS & Workflow SaaS

### Overview of Incumbents
1. **Workday**: The enterprise behemoth. Powerful, complex, incredibly expensive.
2. **SAP SuccessFactors**: Massive enterprise HR suite, heavily reliant on expensive consultants.
3. **UKG (Pro/Ready)**: Comprehensive HR platform with a reputation for "nickel-and-diming" add-ons.
4. **BambooHR**: Mid-market darling, but struggling with deep customization as companies scale.
5. **Rippling**: Modern HRIS, fast execution but still a rigid system of record.

### Product Teardown (The Legacy Model)
*   **Top 3 Features**: System of record for employee data, rigid workflow ticketing for onboarding/offboarding, and compliance reporting.
*   **Pricing Tiers**: Workday uses PEPM (Per Employee Per Month) and requires "insane" implementation costs. BambooHR starts around $10/employee/month but hides advanced features. UKG charges $20-$30+ per user/month plus heavy add-ons.
*   **Onboarding Friction**: Workday is famous for overwhelming complexity and configuration challenges. BambooHR users complain about navigation friction and lack of customization. UKG users suffer from clunky reporting and aggressive session timeouts. 

### Where They Are Strong (The Moat)
*   **Payroll & Compliance**: They hold the master system of record for payroll, taxes, and legal compliance. You cannot rip this out easily.
*   **Data Gravity**: They are the single source of truth for org charts and employee lifecycles.

### Where They Are Weak (The Vulnerability)
*   **Employee Experience (Friction)**: Finding a policy, requesting time off, or completing onboarding requires navigating complex portals, submitting tickets, and waiting for HR.
*   **Rigid Workflows**: "Self-service" just means the employee has to do the data entry into a clunky UI.

## Disruptive Strategy (Our Agentic Wedge)

### 1. Direct Threats
*   **Workday** (The ultimate system of record).
*   **Rippling** (The most modern, automation-forward HRIS).

### 2. Table Stakes Features
*   **Secure API Integration**: Must read/write to Workday/BambooHR seamlessly without breaking compliance.
*   **Omnichannel Access**: The agent must live where the employees live (Slack, Microsoft Teams), not in a separate HR portal.

### 3. What We Deliberately MUST NOT Do
*   **Do not build a new HRIS or Payroll system**: We will absolutely not process payroll or act as the legal system of record. We sit on top of Workday/BambooHR as the execution layer.

### 4. The 3 Gaps Our Agentic Wedge Exploits
1.  **Conversational vs. Navigational**: Replace the clunky 10-click portal navigation. Employees just type "I need to take next Friday off" in Slack, and the agent handles the API calls to Workday to log the request and notify the manager.
2.  **Proactive Onboarding Orchestration**: Instead of relying on HR to manually trigger emails and IT tickets, the agent autonomously coordinates the entire onboarding lifecycle—provisioning software, scheduling intro meetings, and answering the new hire's policy questions in real-time.
3.  **Deflect HR Support Tickets**: Eliminate the "HR Helpdesk" by having the agent instantly answer 80% of routine questions (benefits, leave policies, expensing rules) by reading the company's internal knowledge base, freeing HR from manual ticket answering.
