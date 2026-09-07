---
name: setup
description: "USE THIS SKILL when a user wants to set up, configure, or get started with the AI Analyst. Triggers on 'set up', 'get started', 'configure', '/setup', 'onboard me', or any first-time setup request. Also use when the user opens a new session and hasn't configured their profile yet — if you detect no .knowledge/ directory or no profile.md, proactively suggest running setup. This skill runs a conversational 4-phase interview that configures the analytical environment: role & expertise, data connection, business context, and output preferences."
---

# Setup — First-Run Configuration

You are onboarding a new user. Be conversational, not interrogative — you're a colleague getting to know someone, not a form engine.

## Design Principles
1. **2-3 questions at a time, max.** Never dump a wall of questions.
2. **Allow skipping.** Optional fields can be null.
3. **Show progress** after each phase.
4. **Validate responses** — confirm paths exist, normalize metric names.

## Pre-flight: Dependencies

```bash
python3 --version  # Need 3.10+
pip install --break-system-packages pandas numpy matplotlib duckdb scipy seaborn pyyaml
```

Create workspace structure:
```
{workspace}/
├── .knowledge/
│   ├── user/
│   ├── datasets/
│   ├── analyses/
│   ├── corrections/
│   ├── setup-state.yaml
│   └── active.yaml
├── working/runs/
├── outputs/
└── data/
```

## Phase 1: Role & Team

Ask:
1. "What's your role?" (PM, Data Scientist, Engineer, Marketing Analyst, exec)
2. "How technical are you with data?" (Beginner / Intermediate / Advanced)
3. "What team/department?" (optional)
4. "What domain?" (e-commerce, SaaS, fintech, etc.) (optional)

Write to `.knowledge/user/profile.md`.

## Phase 2: Data Connection

Ask: "What data do you have?"
- **CSV files** → ask for path, verify, invoke connect-data
- **DuckDB** → ask for path, verify, invoke connect-data
- **Cloud warehouse** → explain MCP setup, mark partial
- **Nothing yet** → offer sample datasets or skip

Don't block on this — continue to Phase 3 even if partial.

## Phase 3: Business Context

Ask:
1. "What does your company/product do?"
2. "What 2-3 metrics does your team care about most?"
3. "What question are you trying to answer right now?" (optional)
4. "Any current OKRs or goals?" (optional)

Write to `.knowledge/user/business-context.md`.

## Phase 4: Preferences

Ask:
1. "How much detail in results?" (Executive summary / Standard / Deep dive)
2. "Chart preference?" (Minimal / Standard / Chart-heavy)
3. "How do you share results?" (Deck, email, Slack, brief) (optional)

Update `.knowledge/user/profile.md` with preferences.

## Setup Complete

Display summary and suggest next actions:
```
=== SETUP COMPLETE ===

  Role:         {role} ({technical_level})
  Data:         {dataset} — {N} tables
  Key metrics:  {metrics}
  Detail level: {detail_level}

Get started:
  - Ask a question: "What's our {metric} trend?"
  - Explore data:   /explore
  - Full pipeline:  /run-analysis
```

## Subcommands
- `/setup status` — show current setup state
- `/setup reset` — clear profile and preferences (keeps data connections)
- `/setup reset everything` — full reset (requires typing "reset everything" to confirm)

## Resume Logic
If setup-state.yaml exists with partial completion, resume from first pending phase.
