#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "/home/shekerk/content-ideas/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, Inches, PP_ALIGN, RGBColor  # noqa: E402


RUN = Path(__file__).resolve().parent
OUT = RUN / "claude-code-course-video-deck-reviewed.pptx"


def rgb(hex_value: str) -> RGBColor:
    hex_value = hex_value.lstrip("#")
    return RGBColor(int(hex_value[:2], 16), int(hex_value[2:4], 16), int(hex_value[4:], 16))


def compact_header(d: Deck, s, title, subtitle=None, *, band=True):
    b = d.b
    if band:
        d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
    d.text(
        s,
        title,
        d.M,
        Inches(0.38),
        d.CW,
        Inches(0.82),
        size=24,
        color=b.NAVY,
        bold=True,
        font=b.FONT_H,
        shrink=True,
    )
    d.rect(s, d.M, Inches(1.18), Inches(1.35), Inches(0.05), b.TEAL)
    if subtitle:
        d.text(s, subtitle, d.M, Inches(1.32), d.CW, Inches(0.28), size=11.5, color=b.MUTED, shrink=True)


slides = [
    {
        "kind": "cover",
        "title": "Claude Code Beginner Course",
        "subtitle": "Client-ready briefing distilled from Albert Olgaard's 2h18m course",
        "kicker": "AI Engineering Enablement",
    },
    {
        "kind": "summary",
        "title": "The course is really a business operating system, not a coding tutorial",
        "bluf": "Claude Code is positioned as the beginner-friendly interface for turning intent into shipped websites, automations, dashboards, and sellable AI services.",
        "columns": [
            ("Situation", "Most beginners are still using browser chat as an answer engine, repeatedly pasting context and receiving instructions they must execute manually."),
            ("Insight", "The core upgrade is local agency: Claude Code reads the project, edits files, runs commands, tests changes, and keeps behavior rules in the repo."),
            ("Recommendation", "Teach beginners a repeatable delivery system: setup, context, skills, build planning, implementation, testing, deployment, and value-based pricing."),
        ],
    },
    {
        "kind": "arc",
        "title": "The narrative moves from tool setup to monetizable delivery",
        "steps": [
            ("1", "Why it matters", "AI-written code shifts value from manual execution to directing systems."),
            ("2", "Tool setup", "Install the local coding environment and learn the command surface."),
            ("3", "First proof", "Build and run a modern website to collapse fear of the terminal."),
            ("4", "Repeatability", "Use project rules and skills to make output more consistent."),
            ("5", "Offer ladder", "Move from websites to automations to full AI systems."),
            ("6", "Delivery method", "Plan first, build second, test and refine continuously."),
            ("7", "Commercial model", "Price from client ROI, not technical effort."),
        ],
    },
    {
        "kind": "two_col",
        "title": "The real contrast is browser advice versus local execution",
        "left_title": "Browser chat",
        "right_title": "Claude Code",
        "left": [
            "User pastes project context manually",
            "Assistant describes what to change",
            "Context resets across sessions",
            "Testing and deployment remain manual",
        ],
        "right": [
            "Agent reads the project directly",
            "Agent edits files and runs commands",
            "Project rules persist in the repo",
            "Testing loops can run inside the workflow",
        ],
        "takeaway": "The upgrade is not smarter answers; it is closed-loop execution inside the user's working environment.",
    },
    {
        "kind": "ladder",
        "title": "Beginner confidence comes from a deliberately small first environment",
        "items": [
            ("Install", "Set up Claude Code and a code editor before any business promise."),
            ("Open project", "Work inside a visible folder so files, commands, and changes are inspectable."),
            ("Use commands", "Learn slash commands, model selection, session control, and terminal basics."),
            ("Run locally", "Use localhost to see the product quickly and make iteration tangible."),
        ],
    },
    {
        "kind": "flow",
        "title": "The first website demo proves end-to-end delivery in minutes",
        "steps": ["Prompt", "Approve setup", "Build project", "Run locally", "Inspect result", "Iterate"],
        "caption": "The website example is less about the site itself and more about the user's first proof that an agent can produce a working artifact.",
    },
    {
        "kind": "framework",
        "title": "Project rules turn one-off prompting into repeatable behavior",
        "center": "Persistent project instructions",
        "nodes": [
            ("Clarifying questions", "Force requirements before edits"),
            ("Style and tone", "Keep output consistent with the user's preferences"),
            ("Architecture guardrails", "Constrain tool choices and file structure"),
            ("Review checklist", "Make quality standards visible each session"),
        ],
        "takeaway": "The project instruction file is the first operating manual for the agent.",
    },
    {
        "kind": "framework",
        "title": "Skills package repeatable expertise as reusable playbooks",
        "center": "Reusable skill library",
        "nodes": [
            ("Design", "Front-end patterns, animation taste, and layout rules"),
            ("Authentication", "Provider setup and secure integration steps"),
            ("Automation", "Workflow patterns for background jobs and triggers"),
            ("Planning", "Spec and implementation-plan discipline"),
        ],
        "takeaway": "Skills move the learner from ad hoc prompting toward repeatable delivery capability.",
    },
    {
        "kind": "maturity",
        "title": "The offer ladder gives beginners a path from simple to defensible work",
        "levels": [
            ("Level 1", "Websites", "Fastest path to perceived value and portfolio proof."),
            ("Level 2", "Automations", "Connect workflows and remove repetitive manual work."),
            ("Level 3", "AI systems", "Combine dashboards, automations, data, and workflows into a managed solution."),
        ],
    },
    {
        "kind": "process",
        "title": "Website delivery becomes a reusable production line",
        "steps": [
            ("Template", "Start from a proven premium website skill or pattern."),
            ("Discovery", "Ask for niche, brand direction, sections, and conversion goals."),
            ("Build", "Generate the site with animations and polished copy."),
            ("Deploy", "Push to GitHub and deploy on a hosting platform."),
            ("Reuse", "Turn the process into a template-driven offer."),
        ],
    },
    {
        "kind": "process",
        "title": "Automation delivery replaces low-code workflow limits with code-level control",
        "steps": [
            ("Capture process", "Turn the business workflow into a structured prompt."),
            ("Choose connectors", "Use authentication and workflow tooling where useful."),
            ("Build UI", "Create a simple form or dashboard for business users."),
            ("Run jobs", "Use background workflow infrastructure for reliable execution."),
            ("Package", "Deploy the front end and keep the back end maintainable."),
        ],
    },
    {
        "kind": "case",
        "title": "The invoice automation demo shows the pattern for internal tools",
        "challenge": "Manual invoice preparation creates repetitive formatting, sending, and tracking work.",
        "solution": "A small form captures invoice data, generates a PDF, authenticates to email, and sends it to the client.",
        "implication": "A beginner can sell workflow removal when the scope is narrow, observable, and tied to a business action.",
    },
    {
        "kind": "case",
        "title": "The support inbox demo turns knowledge into a managed AI workflow",
        "challenge": "Support teams answer repeat questions and need consistent responses grounded in company knowledge.",
        "solution": "A dashboard pulls emails, drafts AI replies, shows confidence and supporting context, and lets a human approve responses.",
        "implication": "The valuable product is not the model call; it is the reviewable workflow around the model.",
    },
    {
        "kind": "framework",
        "title": "The build-anything method forces planning before coding",
        "center": "Build-anything method",
        "nodes": [
            ("Build plan", "Clarify goal, scope, stack, cost, and constraints"),
            ("Implementation plan", "Split delivery into tasks and ordered steps"),
            ("Agent build", "Give the plan to the agent and execute in sequence"),
            ("Test and refine", "Run the product, paste errors back, and polish UX"),
        ],
        "takeaway": "The course explicitly argues that planning should consume most of the effort on complex builds.",
    },
    {
        "kind": "case",
        "title": "The lead-enricher demo validates the planning discipline",
        "challenge": "The requested tool starts vague: find a person's work email from partial inputs.",
        "solution": "The agent asks requirements questions, drafts a spec, builds a task plan, creates the app, wires an API, and then debugs the result.",
        "implication": "The demo teaches beginners to collaborate with the agent as a product manager before treating it as a coder.",
    },
    {
        "kind": "matrix",
        "title": "The best first services balance perceived value and delivery complexity",
        "points": [
            ("Websites", 0.35, 0.25, "#00C9A7"),
            ("Invoice tools", 0.48, 0.42, "#009B82"),
            ("Support inbox", 0.68, 0.64, "#F2A83B"),
            ("Full AI systems", 0.86, 0.83, "#E05A6B"),
        ],
        "xlabel": "Delivery complexity",
        "ylabel": "Operational impact",
        "note": "Start where proof is fast",
    },
    {
        "kind": "quote",
        "title": "The commercial thesis is simple: get good before getting expensive",
        "quote": "The course rejects the idea that a beginner should immediately sell a high-ticket project. It recommends building skill, trust, examples, and testimonials first.",
        "points": [
            "Free or low-cost work can be rational when it creates proof.",
            "Templates and skills make later delivery faster, but only after the operator understands the work.",
            "The offer becomes stronger when it sells business outcomes rather than AI features.",
        ],
    },
    {
        "kind": "roi",
        "title": "Pricing is anchored to client ROI, not build hours",
        "items": [
            ("5x ROI rule", "If the system saves or creates $5,000/month, the service should be priced around a level that leaves the client with a clear surplus."),
            ("Result-based", "Best when outcomes can be tracked cleanly through revenue, gross profit, meetings, or qualified leads."),
            ("Setup plus recurring", "Best when tracking exact upside is hard but ongoing support and maintenance create continuing value."),
            ("Tiered usage", "Required when system costs scale with calls, conversations, seats, or volume."),
        ],
    },
    {
        "kind": "risk",
        "title": "The course repeatedly warns against skipping trust, proof, and economics",
        "risks": [
            ("Overpromising", "Selling complex AI systems before the operator has enough delivery reps."),
            ("Unclear value", "Explaining features before showing the buyer's business outcome."),
            ("Bad pricing", "Charging flat fees when usage costs can explode."),
            ("Weak planning", "Letting the agent build before requirements, stack, and implementation steps are clear."),
        ],
    },
    {
        "kind": "playbook",
        "title": "A client-ready enablement program should convert the course into operating assets",
        "items": [
            ("Starter environment", "Install guide, repo template, and first-project checklist."),
            ("Skill library", "Design, planning, automation, QA, and deployment playbooks."),
            ("Service menu", "Website, workflow automation, support inbox, and custom app packages."),
            ("Quality gate", "Definition of done for build plan, implementation plan, testing, deployment, and handoff."),
            ("Pricing calculator", "ROI worksheet, usage-cost guardrails, and offer templates."),
        ],
    },
    {
        "kind": "roadmap",
        "title": "A practical rollout can be completed in four weeks",
        "weeks": [
            ("Week 1", "Set up tools, run the first website build, and document project rules."),
            ("Week 2", "Create reusable skills and ship two portfolio-grade website variants."),
            ("Week 3", "Build one automation and one dashboard-backed workflow with real testing."),
            ("Week 4", "Package offers, build ROI pricing examples, and run outreach with proof assets."),
        ],
    },
    {
        "kind": "decision",
        "title": "The decision is whether to treat Claude Code as a toy or as a delivery stack",
        "left": "Toy usage: isolated prompts, copied code, no rules, no tests, no offer discipline.",
        "right": "Delivery-stack usage: persistent context, reusable skills, implementation plans, test loops, deployment paths, and ROI-based packaging.",
        "ask": "Build the operating system around the agent before scaling client promises.",
    },
    {
        "kind": "appendix",
        "title": "Visual coverage was accounted for across the full course",
        "items": [
            "464 focused scene frames were extracted across the four course sections, plus an interrupted full-video scene scan left 461 additional frames.",
            "Meaningful screen changes were grouped into setup screens, website demos, automation screens, support inbox screens, planning diagrams, lead-enricher screens, and pricing diagrams.",
            "Presenter-only and duplicated screen frames were excluded from client slides.",
            "The final deck uses native PowerPoint shapes instead of raw video screenshots for editability and client hygiene.",
        ],
    },
]

extra_slides = [
    {
        "kind": "process",
        "title": "Section 1 has a full setup path, not just an install step",
        "steps": [
            ("Install prerequisites", "NodeJS enables the Claude Code install and the JavaScript project workflow."),
            ("Open a code editor", "VS Code makes files, terminal output, and agent edits visible to a beginner."),
            ("Install Claude Code", "Use the official quickstart command for the target operating system."),
            ("Authorize account", "Complete browser login and subscription authorization before the first session."),
            ("Learn control surface", "Use slash commands, model choice, effort level, clear, and split terminals."),
        ],
    },
    {
        "kind": "two_col",
        "title": "Claude Code onboarding teaches both environment and agency control",
        "left_title": "Environment setup",
        "right_title": "Agent control",
        "left": [
            "NodeJS installation",
            "VS Code project folder",
            "Terminal inside the editor",
            "Claude account authorization",
        ],
        "right": [
            "Slash-command navigation",
            "Model and effort selection",
            "Session clearing",
            "Parallel terminal sessions",
        ],
        "takeaway": "The beginner needs to understand where the agent works and how to steer it before building client-facing assets.",
    },
    {
        "kind": "case",
        "title": "The first shiny.ai site is a confidence-building proof, not the final business model",
        "challenge": "The user starts from a vague marketing request: a futuristic AI agency website with animations and stronger copy.",
        "solution": "Claude Code generates a NextJS project, installs dependencies, and gives the run command for local inspection.",
        "implication": "The first win is psychological: the terminal becomes a place where a non-expert can ship a visible result.",
    },
    {
        "kind": "process",
        "title": "The local website loop is the minimum viable delivery loop",
        "steps": [
            ("Describe outcome", "Specify client, niche, style, stack, animation, and conversion goal."),
            ("Approve commands", "Let Claude install dependencies and scaffold the app."),
            ("Run dev server", "Start the local project with the generated command."),
            ("Inspect browser", "Open the localhost URL and review the actual page."),
            ("Iterate", "Give concrete corrections, not abstract approval."),
        ],
    },
    {
        "kind": "case",
        "title": "The `claude.md` lesson is really about governance",
        "challenge": "Without persistent project rules, every new session risks inconsistent behavior and repeated explanation.",
        "solution": "A project instruction file forces rules such as asking clarifying questions before changing code.",
        "implication": "The learner starts building an operating manual for the agent, which is essential before client work scales.",
    },
    {
        "kind": "process",
        "title": "Skill installation turns external expertise into a local capability",
        "steps": [
            ("Find skill", "Download a skill package or markdown instruction file."),
            ("Provide artifact", "Drag the skill into the working project or make it available locally."),
            ("Ask Claude to install", "Have Claude research the installation path and place the skill correctly."),
            ("Restart session", "Reload Claude Code so the new skill is discoverable."),
            ("Invoke deliberately", "Use the skill only when its instructions match the task."),
        ],
    },
    {
        "kind": "case",
        "title": "The Cityscape demo shows template-led website productization",
        "challenge": "A landscaping company needs a premium-looking website with trust, services, imagery, and lead capture.",
        "solution": "The premium website skill asks design questions and produces an animated landing page with quote-request flow.",
        "implication": "The sellable asset is a repeatable template-led process, not a one-off generated page.",
    },
    {
        "kind": "process",
        "title": "Deployment makes the website offer commercially real",
        "steps": [
            ("Create repository", "Set up a GitHub repo for the website code."),
            ("Push scoped code", "Ask Claude to push only the website project to the repo."),
            ("Import to Vercel", "Connect the GitHub repo and let Vercel detect the app."),
            ("Deploy preview", "Publish a live subdomain and inspect the result."),
            ("Add domain", "Use DNS settings for the client's production domain."),
        ],
    },
    {
        "kind": "case",
        "title": "The invoice automation demo is the Level 2 pattern in miniature",
        "challenge": "The workflow spans form capture, invoice PDF generation, Google Drive upload, and Gmail delivery.",
        "solution": "Claude combines a NextJS frontend, Trigger.dev workflow hosting, Composio authentication, and environment variables.",
        "implication": "A narrow workflow can become a paid automation when the handoff is packaged and repeatable.",
    },
    {
        "kind": "process",
        "title": "The automation build has a clear integration sequence",
        "steps": [
            ("Scope form fields", "Capture business details, client details, line items, and invoice terms."),
            ("Secure secrets", "Move API keys and tokens into environment variables."),
            ("Authorize tools", "Run OAuth flows for Gmail and Google Drive."),
            ("Generate artifact", "Create the invoice PDF and store it in Drive."),
            ("Send and debug", "Email the client and use logs to fix integration errors."),
        ],
    },
    {
        "kind": "process",
        "title": "Production automation requires two deployments, not one",
        "steps": [
            ("Promote backend", "Move Trigger.dev workflows from development to production."),
            ("Swap keys", "Use production API keys and environment variables."),
            ("Push frontend", "Send the NextJS form to GitHub."),
            ("Deploy frontend", "Publish the form on Vercel."),
            ("Verify end-to-end", "Run a full invoice from web form to email delivery."),
        ],
    },
    {
        "kind": "case",
        "title": "Creating an automation skill converts a demo into an agency asset",
        "challenge": "A one-off automation demo is hard to resell if the process is trapped in one project.",
        "solution": "The course packages the NextJS plus Trigger.dev automation pattern into a reusable skill template.",
        "implication": "Every successful build should leave behind a reusable delivery playbook.",
    },
    {
        "kind": "framework",
        "title": "The Level 3 architecture combines portal, worker, database, and auth",
        "center": "Client AI system",
        "nodes": [
            ("NextJS portal", "Dashboard, forms, workflows, and user interface"),
            ("NextAuth + Resend", "Magic-link login and domain restriction"),
            ("Trigger.dev worker", "Scheduled and event-driven background jobs"),
            ("MongoDB", "Data storage, knowledge base, and vector search"),
        ],
        "takeaway": "The enterprise system is a product shell around multiple automations, not a single script.",
    },
    {
        "kind": "case",
        "title": "Domain-restricted login makes the demo feel enterprise-ready",
        "challenge": "A business dashboard cannot be treated like a public website; access must be constrained.",
        "solution": "The course restricts logins to the client's corporate email domain and generates a secure auth secret.",
        "implication": "Security posture and tenant boundaries are part of the product, even in a beginner-friendly build.",
    },
    {
        "kind": "case",
        "title": "The design-skill pass turns scaffolding into something a buyer can trust",
        "challenge": "Raw generated dashboards often look unfinished and can undermine buyer confidence.",
        "solution": "A front-end design skill is used to improve layout, dark/light modes, and visual polish, then bugs are fed back to Claude.",
        "implication": "Client readiness requires refinement after functional scaffolding, not just working code.",
    },
    {
        "kind": "case",
        "title": "The onboarding workflow expands the dashboard beyond invoicing",
        "challenge": "A single invoice tool is useful, but a client system needs multiple core workflows to justify higher value.",
        "solution": "The dashboard adds employee onboarding: templates, dynamic client data, PDF generation, and email dispatch.",
        "implication": "Level 3 systems become valuable when they coordinate several business processes in one portal.",
    },
    {
        "kind": "framework",
        "title": "The support inbox introduces an AI product pattern: retrieve, draft, review, escalate",
        "center": "AI support workflow",
        "nodes": [
            ("Knowledge base", "Uploaded text or PDFs become answer context"),
            ("Vector search", "MongoDB retrieves relevant passages"),
            ("Draft reply", "AI produces a response with confidence"),
            ("Human review", "Low-confidence tickets escalate to the dashboard"),
        ],
        "takeaway": "The workflow sells controlled AI assistance, not blind automation.",
    },
    {
        "kind": "process",
        "title": "The support agent needs operational controls to be trustworthy",
        "steps": [
            ("Poll inbox", "Check the support mailbox on a fixed schedule."),
            ("Classify request", "Decide whether the email can be answered from the knowledge base."),
            ("Retrieve context", "Search documents and cite support passages."),
            ("Score confidence", "Estimate whether the answer is safe to send."),
            ("Escalate exceptions", "Send uncertain cases to a human dashboard queue."),
        ],
    },
    {
        "kind": "case",
        "title": "The lead enricher demo tests whether the framework works without a tutorial",
        "challenge": "The requested app starts from partial identifiers and requires external enrichment.",
        "solution": "The course uses a planning plugin to create a design spec, then builds a Hunter.io-backed web app.",
        "implication": "The repeatable skill is requirements discovery and implementation planning, not memorizing one API.",
    },
    {
        "kind": "process",
        "title": "The build-anything framework should be treated as a gate sequence",
        "steps": [
            ("Build plan gate", "Do not code until scope, stack, data model, and constraints are clear."),
            ("Implementation gate", "Do not build until tasks are ordered and checkable."),
            ("Execution gate", "Run one subtask at a time and verify progress."),
            ("Testing gate", "Run locally, capture errors, and feed exact failures back."),
            ("Polish gate", "Use design skills and UX review before handoff."),
        ],
    },
    {
        "kind": "roi",
        "title": "The pricing chapter has four separate offer models",
        "items": [
            ("5x ROI anchor", "Price so the client retains an obvious economic surplus."),
            ("Gross-profit share", "Use for revenue-generating systems where attribution is measurable."),
            ("Setup plus retainer", "Use when exact financial impact is harder to trace."),
            ("Usage tiers", "Use when delivery cost scales with calls, emails, conversations, or seats."),
        ],
    },
    {
        "kind": "case",
        "title": "The satisfaction guarantee solves trust without removing commitment",
        "challenge": "Clients hesitate to pay upfront when they have not yet seen the system.",
        "solution": "Charge a setup fee to create commitment, then offer a refund at final review if the built system misses expectations.",
        "implication": "The offer reduces buyer risk while still preventing unpaid speculative work.",
    },
    {
        "kind": "two_col",
        "title": "The sales lesson is to sell outcomes before price",
        "left_title": "Weak sales motion",
        "right_title": "Course-recommended motion",
        "left": [
            "Lead with AI features",
            "Quote price in messages",
            "Explain tooling before pain",
            "Ignore buyer economics",
        ],
        "right": [
            "Diagnose operational pain",
            "Show expected value first",
            "Connect price to ROI",
            "Package one clear monthly price",
        ],
        "takeaway": "Businesses care about saved cost, generated profit, and reduced operational drag; the AI label is secondary.",
    },
]

slides = slides[:-1] + extra_slides + slides[-1:]


def add_cover(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(10.15), 0, Inches(3.18), d.H, b.NAVY_2)
    d.rect(s, Inches(10.05), 0, Inches(0.08), d.H, b.TEAL)
    d.text(s, spec["kicker"].upper(), d.M, Inches(0.92), Inches(5.8), Inches(0.35), size=13, color=b.TEAL, bold=True)
    d.text(s, spec["title"], d.M, Inches(1.55), Inches(8.8), Inches(1.45), size=48, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(3.25), Inches(1.8), Inches(0.06), b.TEAL)
    d.text(s, spec["subtitle"], d.M, Inches(3.55), Inches(7.7), Inches(0.8), size=19, color=b.LIGHT_TEAL, shrink=True)
    for i, label in enumerate(["Setup", "Skills", "Builds", "Pricing"]):
        x = Inches(10.55)
        y = Inches(1.2 + i * 1.05)
        d.rect(s, x, y, Inches(1.9), Inches(0.54), b.NAVY, line=b.TEAL, radius=0.08)
        d.text(s, label, x + Inches(0.12), y + Inches(0.15), Inches(1.55), Inches(0.2), size=13, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.footer(s, page, total, dark=True)


def add_summary(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, spec["title"], "Executive readout")
    d.rect(s, d.M, Inches(1.78), d.CW, Inches(0.88), b.NAVY, radius=0.06)
    d.text(s, spec["bluf"], d.M + Inches(0.25), Inches(1.98), d.CW - Inches(0.5), Inches(0.46), size=17, color=b.WHITE, bold=True, shrink=True)
    col_w = (d.CW - Inches(0.35) * 2) / 3
    for i, (head, body) in enumerate(spec["columns"]):
        x = d.M + i * (col_w + Inches(0.35))
        d.rect(s, x, Inches(3.02), col_w, Inches(2.45), b.SOFT, line=b.GRID, radius=0.06, shadow=True)
        d.text(s, head, x + Inches(0.18), Inches(3.25), col_w - Inches(0.36), Inches(0.34), size=15, color=b.NAVY, bold=True)
        d.text(s, body, x + Inches(0.18), Inches(3.75), col_w - Inches(0.36), Inches(1.25), size=13, color=b.INK, shrink=True)
    d.rect(s, d.M, Inches(5.78), d.CW, Inches(0.48), b.GOLD, radius=0.04)
    d.text(s, "Decision: use the course as a repeatable enablement system, not a passive training video.", d.M + Inches(0.2), Inches(5.91), d.CW - Inches(0.4), Inches(0.18), size=13.5, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.footer(s, page, total)


def add_arc(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, spec["title"], "Seven-beat argument arc")
    x0, y = d.M, Inches(1.85)
    box_w, box_h, gap = Inches(1.65), Inches(3.85), Inches(0.18)
    for i, (num, head, body) in enumerate(spec["steps"]):
        x = x0 + i * (box_w + gap)
        fill = b.NAVY if i in (0, 6) else (b.SOFT if i % 2 else rgb("EAF5F2"))
        text_col = b.WHITE if i in (0, 6) else b.INK
        d.rect(s, x, y, box_w, box_h, fill, line=b.TEAL if i in (0, 6) else b.GRID, radius=0.06, shadow=i in (0, 6))
        d.text(s, num, x + Inches(0.12), y + Inches(0.16), Inches(0.35), Inches(0.25), size=15, color=b.GOLD if i in (0, 6) else b.TEAL, bold=True)
        d.text(s, head, x + Inches(0.12), y + Inches(0.55), box_w - Inches(0.24), Inches(0.45), size=13, color=text_col, bold=True, shrink=True)
        d.text(s, body, x + Inches(0.12), y + Inches(1.22), box_w - Inches(0.24), Inches(1.6), size=10.5, color=text_col, shrink=True)
    d.footer(s, page, total)


def add_two_col(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, spec["title"], "Positioning contrast")
    w = (d.CW - Inches(0.5)) / 2
    for x, head, items, color in [
        (d.M, spec["left_title"], spec["left"], b.CORAL),
        (d.M + w + Inches(0.5), spec["right_title"], spec["right"], b.TEAL),
    ]:
        d.rect(s, x, Inches(1.8), w, Inches(3.8), b.SOFT, line=b.GRID, radius=0.06, shadow=True)
        d.rect(s, x, Inches(1.8), w, Inches(0.56), color, radius=0.06)
        d.text(s, head, x + Inches(0.2), Inches(1.96), w - Inches(0.4), Inches(0.2), size=15, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, [{"text": it, "bullet": True, "space_before": 9, "size": 14} for it in items], x + Inches(0.32), Inches(2.65), w - Inches(0.64), Inches(2.2), shrink=True)
    d.rect(s, d.M, Inches(5.92), d.CW, Inches(0.55), b.NAVY, radius=0.04)
    d.text(s, spec["takeaway"], d.M + Inches(0.22), Inches(6.07), d.CW - Inches(0.44), Inches(0.2), size=13.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.footer(s, page, total)


def add_ladder(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, spec["title"], "Enablement sequence")
    for i, (head, body) in enumerate(spec["items"]):
        y = Inches(1.82 + i * 1.04)
        d.rect(s, d.M + Inches(0.2 * i), y, d.CW - Inches(0.4 * i), Inches(0.72), b.SOFT, line=b.GRID, radius=0.06, shadow=True)
        d.text(s, f"{i+1}", d.M + Inches(0.22 + 0.2 * i), y + Inches(0.18), Inches(0.38), Inches(0.2), size=15, color=b.TEAL, bold=True)
        d.text(s, head, d.M + Inches(0.72 + 0.2 * i), y + Inches(0.14), Inches(2.1), Inches(0.24), size=15, color=b.NAVY, bold=True)
        d.text(s, body, d.M + Inches(2.75 + 0.2 * i), y + Inches(0.15), d.CW - Inches(3.4 + 0.4 * i), Inches(0.25), size=13.5, color=b.INK, shrink=True)
    d.footer(s, page, total)


def add_flow(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, spec["title"], "First proof loop")
    y = Inches(2.28)
    step_w = Inches(1.65)
    for i, step in enumerate(spec["steps"]):
        x = d.M + i * Inches(2.05)
        d.rect(s, x, y, step_w, Inches(1.1), b.NAVY if i in (0, 5) else b.SOFT, line=b.TEAL if i in (0, 5) else b.GRID, radius=0.08, shadow=True)
        d.text(s, step, x + Inches(0.12), y + Inches(0.38), step_w - Inches(0.24), Inches(0.23), size=14, color=b.WHITE if i in (0, 5) else b.INK, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        if i < len(spec["steps"]) - 1:
            d.text(s, ">", x + step_w + Inches(0.14), y + Inches(0.4), Inches(0.22), Inches(0.2), size=20, color=b.TEAL, bold=True)
    d.rect(s, d.M, Inches(4.55), d.CW, Inches(0.76), b.SOFT, line=b.GRID, radius=0.04)
    d.text(s, spec["caption"], d.M + Inches(0.28), Inches(4.78), d.CW - Inches(0.56), Inches(0.26), size=15, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.footer(s, page, total)


def add_framework(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, spec["title"], spec.get("takeaway"))
    cx, cy = Inches(5.55), Inches(3.42)
    d.rect(s, cx, cy, Inches(2.25), Inches(1.0), b.NAVY, line=b.TEAL, radius=0.08, shadow=True)
    d.text(s, spec["center"], cx + Inches(0.15), cy + Inches(0.31), Inches(1.95), Inches(0.24), size=14, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    positions = [(d.M, Inches(1.85)), (Inches(9.25), Inches(1.85)), (d.M, Inches(5.05)), (Inches(9.25), Inches(5.05))]
    for (head, body), (x, y) in zip(spec["nodes"], positions):
        d.rect(s, x, y, Inches(3.35), Inches(1.0), b.SOFT, line=b.GRID, radius=0.06, shadow=True)
        d.text(s, head, x + Inches(0.18), y + Inches(0.16), Inches(3.0), Inches(0.22), size=13.5, color=b.NAVY, bold=True, shrink=True)
        d.text(s, body, x + Inches(0.18), y + Inches(0.48), Inches(3.0), Inches(0.28), size=11.5, color=b.INK, shrink=True)
    d.footer(s, page, total)


def add_maturity(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, spec["title"], "Service ladder")
    for i, (level, name, body) in enumerate(spec["levels"]):
        x = d.M + i * Inches(4.12)
        y = Inches(2.0 - i * 0.15)
        h = Inches(3.0 + i * 0.25)
        fill = [b.SOFT, rgb("EAF5F2"), b.NAVY][i]
        col = b.WHITE if i == 2 else b.INK
        d.rect(s, x, y, Inches(3.55), h, fill, line=b.TEAL if i == 2 else b.GRID, radius=0.06, shadow=True)
        d.text(s, level, x + Inches(0.25), y + Inches(0.28), Inches(1.2), Inches(0.2), size=12, color=b.TEAL if i != 2 else b.GOLD, bold=True)
        d.text(s, name, x + Inches(0.25), y + Inches(0.78), Inches(3.0), Inches(0.45), size=22, color=col, bold=True, shrink=True)
        d.text(s, body, x + Inches(0.25), y + Inches(1.58), Inches(2.95), Inches(0.8), size=13, color=col, shrink=True)
    d.footer(s, page, total)


def add_process(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, spec["title"], "Repeatable operating path")
    for i, (head, body) in enumerate(spec["steps"]):
        y = Inches(1.78 + i * 0.86)
        d.rect(s, d.M, y, Inches(0.65), Inches(0.52), b.TEAL if i < len(spec["steps"]) - 1 else b.GOLD, radius=0.04)
        d.text(s, str(i + 1), d.M, y + Inches(0.15), Inches(0.65), Inches(0.16), size=13, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, head, d.M + Inches(0.9), y + Inches(0.08), Inches(2.2), Inches(0.24), size=14.5, color=b.NAVY, bold=True)
        d.text(s, body, d.M + Inches(3.0), y + Inches(0.09), d.CW - Inches(3.15), Inches(0.23), size=12.5, color=b.INK, shrink=True)
    d.footer(s, page, total)


def add_case(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, spec["title"], "Demo-to-offer interpretation")
    cards = [("Challenge", spec["challenge"], b.CORAL), ("Solution", spec["solution"], b.TEAL), ("Business implication", spec["implication"], b.GOLD)]
    for i, (head, body, color) in enumerate(cards):
        x = d.M + i * Inches(4.1)
        d.rect(s, x, Inches(2.0), Inches(3.55), Inches(2.85), b.SOFT, line=b.GRID, radius=0.06, shadow=True)
        d.rect(s, x, Inches(2.0), Inches(3.55), Inches(0.18), color)
        d.text(s, head, x + Inches(0.22), Inches(2.35), Inches(3.05), Inches(0.32), size=16, color=b.NAVY, bold=True)
        d.text(s, body, x + Inches(0.22), Inches(3.0), Inches(3.05), Inches(1.05), size=13, color=b.INK, shrink=True)
    d.footer(s, page, total)


def add_matrix(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, spec["title"], "Judgment matrix")
    chart = RUN / "service-matrix.png"
    d.chart_matrix(spec["points"], chart, xlabel=spec["xlabel"], ylabel=spec["ylabel"], note=spec["note"])
    d.picture_centered(s, chart, top=Inches(1.75), width=Inches(9.8), max_bottom=Inches(6.2))
    d.footer(s, page, total)


def add_quote(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.text(s, spec["title"], d.M, Inches(0.62), d.CW, Inches(0.7), size=29, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(1.55), d.CW, Inches(1.1), b.NAVY_2, line=b.TEAL, radius=0.06)
    d.text(s, spec["quote"], d.M + Inches(0.25), Inches(1.82), d.CW - Inches(0.5), Inches(0.42), size=16, color=b.LIGHT_TEAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    for i, point in enumerate(spec["points"]):
        y = Inches(3.25 + i * 0.82)
        d.rect(s, d.M, y, d.CW, Inches(0.48), b.WHITE, radius=0.04)
        d.text(s, point, d.M + Inches(0.25), y + Inches(0.13), d.CW - Inches(0.5), Inches(0.18), size=13.5, color=b.NAVY, bold=True, shrink=True)
    d.footer(s, page, total, dark=True)


def add_roi(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, spec["title"], "Offer design")
    for i, (head, body) in enumerate(spec["items"]):
        x = d.M + (i % 2) * Inches(6.2)
        y = Inches(1.85 + (i // 2) * 2.0)
        d.rect(s, x, y, Inches(5.55), Inches(1.5), b.SOFT, line=b.GRID, radius=0.06, shadow=True)
        d.text(s, head, x + Inches(0.22), y + Inches(0.22), Inches(5.05), Inches(0.28), size=16, color=b.NAVY, bold=True)
        d.text(s, body, x + Inches(0.22), y + Inches(0.65), Inches(5.05), Inches(0.48), size=12.5, color=b.INK, shrink=True)
    d.footer(s, page, total)


def add_risk(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, spec["title"], "Failure modes")
    for i, (head, body) in enumerate(spec["risks"]):
        y = Inches(1.85 + i * 0.92)
        d.rect(s, d.M, y, d.CW, Inches(0.62), rgb("FFF5F6") if i % 2 == 0 else b.SOFT, line=b.GRID, radius=0.04)
        d.text(s, head, d.M + Inches(0.2), y + Inches(0.17), Inches(2.2), Inches(0.2), size=14, color=b.CORAL, bold=True)
        d.text(s, body, d.M + Inches(2.7), y + Inches(0.17), d.CW - Inches(2.95), Inches(0.2), size=12.5, color=b.INK, shrink=True)
    d.footer(s, page, total)


def add_playbook(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, spec["title"], "Assets to create")
    for i, (head, body) in enumerate(spec["items"]):
        x = d.M + (i % 3) * Inches(4.1)
        y = Inches(1.85 + (i // 3) * 2.05)
        d.rect(s, x, y, Inches(3.55), Inches(1.55), b.SOFT, line=b.GRID, radius=0.06, shadow=True)
        d.text(s, head, x + Inches(0.2), y + Inches(0.2), Inches(3.1), Inches(0.28), size=15, color=b.NAVY, bold=True, shrink=True)
        d.text(s, body, x + Inches(0.2), y + Inches(0.66), Inches(3.1), Inches(0.48), size=12, color=b.INK, shrink=True)
    d.footer(s, page, total)


def add_roadmap(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, spec["title"], "30-day enablement sprint")
    for i, (week, body) in enumerate(spec["weeks"]):
        x = d.M + i * Inches(3.1)
        d.rect(s, x, Inches(2.0), Inches(2.65), Inches(2.8), b.NAVY if i == 3 else b.SOFT, line=b.TEAL if i == 3 else b.GRID, radius=0.06, shadow=True)
        col = b.WHITE if i == 3 else b.INK
        d.text(s, week, x + Inches(0.22), Inches(2.3), Inches(2.15), Inches(0.28), size=17, color=b.GOLD if i == 3 else b.TEAL, bold=True)
        d.text(s, body, x + Inches(0.22), Inches(3.0), Inches(2.15), Inches(0.8), size=12.5, color=col, shrink=True)
    d.footer(s, page, total)


def add_decision(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.text(s, spec["title"], d.M, Inches(0.62), d.CW, Inches(0.8), size=31, color=b.WHITE, bold=True, shrink=True)
    for x, head, body, color in [
        (d.M, "Treat it as a toy", spec["left"], b.CORAL),
        (d.M + Inches(6.35), "Treat it as a delivery stack", spec["right"], b.TEAL),
    ]:
        d.rect(s, x, Inches(2.0), Inches(5.55), Inches(2.4), b.NAVY_2, line=color, radius=0.06, shadow=True)
        d.text(s, head, x + Inches(0.25), Inches(2.32), Inches(5.05), Inches(0.28), size=17, color=color, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, body, x + Inches(0.35), Inches(3.05), Inches(4.85), Inches(0.75), size=14, color=b.WHITE, shrink=True, align=PP_ALIGN.CENTER)
    d.rect(s, d.M, Inches(5.35), d.CW, Inches(0.58), b.GOLD, radius=0.04)
    d.text(s, spec["ask"], d.M + Inches(0.25), Inches(5.52), d.CW - Inches(0.5), Inches(0.2), size=15, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.footer(s, page, total, dark=True)


def add_appendix(d: Deck, spec: dict, page: int, total: int):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, spec["title"], "Coverage and editability note")
    d.text(s, [{"text": it, "bullet": True, "space_before": 11, "size": 14} for it in spec["items"]], d.M, Inches(1.85), d.CW, Inches(3.4), shrink=True)
    d.rect(s, d.M, Inches(5.65), d.CW, Inches(0.55), b.NAVY, radius=0.04)
    d.text(s, "Editability mode: PPT-native editable diagrams.", d.M + Inches(0.22), Inches(5.82), d.CW - Inches(0.44), Inches(0.18), size=13.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.footer(s, page, total)


def build() -> Path:
    d = Deck(footer="Claude Code Beginner Course | Executive Briefing | 2026")
    d.header = lambda s, title, subtitle=None, band=True: compact_header(d, s, title, subtitle, band=band)
    total = len(slides)
    dispatch = {
        "cover": add_cover,
        "summary": add_summary,
        "arc": add_arc,
        "two_col": add_two_col,
        "ladder": add_ladder,
        "flow": add_flow,
        "framework": add_framework,
        "maturity": add_maturity,
        "process": add_process,
        "case": add_case,
        "matrix": add_matrix,
        "quote": add_quote,
        "roi": add_roi,
        "risk": add_risk,
        "playbook": add_playbook,
        "roadmap": add_roadmap,
        "decision": add_decision,
        "appendix": add_appendix,
    }
    for page, spec in enumerate(slides, start=1):
        dispatch[spec["kind"]](d, spec, page, total)
    return d.save(OUT)


if __name__ == "__main__":
    artifact = {
        "deck": str(build()),
        "slide_count": len(slides),
        "editability_mode": "PPT-native editable diagrams",
    }
    (RUN / "deck-build-result.json").write_text(json.dumps(artifact, indent=2) + "\n")
