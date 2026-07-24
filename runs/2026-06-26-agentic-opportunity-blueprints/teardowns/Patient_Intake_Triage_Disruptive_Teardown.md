---
status: reviewed
use_case: "Patient Intake & Triage"
last_updated: "2026-06-26"
source_confidence:
  competitor: high
  pricing: medium
  workflow: high
---

# Patient Intake & Triage Disruptive Competitor Teardown

## Market Frame
- Workflow: conversational intake, symptom capture, triage, and pre-population of clinical workflow.
- Target buyer: provider access, ambulatory ops, and health-system patient-experience teams.
- Existing spend category: patient intake kiosks, portals, and engagement modules.
- Incumbent economic model: quote-based subscriptions and large EHR/portal deployments.
- Agentic wedge: conversational intake layer that bypasses clunky portal flows and routes patients intelligently.

## Incumbent Map
| Incumbent | Category | Buyer | Pricing Signal | Onboarding / Admin Friction | Strength | Weakness |
|---|---|---|---|---|---|---|
| Phreesia | Patient intake/check-in | Provider ops | Quote-based, volume/provider based | Heavy implementation and check-in configuration | Strong check-in and payment flow | Bolt-on friction and user complaints |
| Epic MyChart | Patient portal | Enterprise health systems | Embedded in large EHR deployments | Portal setup and admin burden | Deep EHR adjacency | In-basket noise and clinician burden |
| Cerner HealtheLife | Patient portal | Enterprise health systems | Enterprise deployment | Portal and workflow configuration | Portal footprint | Same manual triage issues |
| Weave / SimplePractice / athenaCommunicator | SMB engagement | SMB practices | SaaS pricing | Setup and patient adoption | Good SMB fit | Not an intelligent triage engine |

## Direct Threats
1. Phreesia and MyChart.
2. Other patient portal and intake modules.

## Pricing Friction
- Quote-based pricing and large enterprise deployments are common.
- Portal add-ons still create implementation and support burden.

## Onboarding And Workflow Friction
- Patients dislike app fatigue, pop-ups, and slow portals.
- Clinicians are overloaded by unstructured in-basket messages.

## What Not To Build
- Do not build a new patient portal app.
- Do not ship proprietary tablet hardware.

## What To Keep
- Existing EHR, scheduling, and portal systems.
- Human triage escalation points for complex or high-risk symptoms.

## Agentic Wedge
- Wedge statement: use conversational intake to gather symptoms dynamically and pre-populate clinical workflow.
- Why it wins: less friction for patients and less inbox noise for clinicians.
- Why now: portals are still clunky and patients expect a conversational experience.

## Blueprint Inputs
- Scope implication: one care setting and one intake flow.
- Architecture implication: SMS/WhatsApp-first conversation plus clinical prefill.
- Build-vs-buy implication: keep the EHR and portal; build the intake intelligence.
- ROI implication: lower staff triage time and better routing.
- QA/deployment implication: symptom redirection, escalation, and PHI controls matter.

## Source Notes
- Source teardown in `source/Patient_Intake_Triage_Competitor_Teardown.md`.
