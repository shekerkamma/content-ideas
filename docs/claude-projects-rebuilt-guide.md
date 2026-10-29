# Claude Projects, rebuilt: setup guide

Source: [Claude Projects Just Got Rebuilt (Full Guide)](https://www.youtube.com/watch?v=MLl41Q9p3Ps),
AI Foundations (Drake). Timestamps below point into that video. Notes cross-checked
against secondary coverage of the September 2026 beta (links at the end). Anthropic's
own announcement was not reachable while writing this, so treat defaults marked
*(video)* as observed in one account, not as documented behavior.

## What changed (0:38)

A project used to be a folder: instructions, files, and a list of chats you started
yourself. Now there is one prompt bar per project. Your prompt goes to a
**coordinator agent**, which does not answer directly. It decides what work is
needed, splits it into **threads** that run in parallel (for example, channel
analytics, audience research, video outlines), passes findings between them, and
comes back with one plan.

You no longer create chats. The coordinator creates threads, and you can open any
thread to read or steer it.

## Two kinds of project (2:24)

- **Ongoing work** with no finish line: a YouTube channel, a newsletter, weekly
  numbers.
- **Finite work** with an end goal: a course launch, a website build, a 90-day
  sprint. Archive it when done.

## Creating a project (3:13)

Sidebar → `+` next to Projects. The form has three parts: name, goal, context.

**Name, icon, color.** Worth taking seriously once you have 30 projects; color-code
by area.

**Goal (4:11).** The standing job the coordinator always works toward, written like
a job description for a new manager. It is not a task; tasks are what you type into
the prompt bar later. Keep it to about one sentence. Drake's observation is that the
coordinator does better with a short goal plus good context than with a goal stuffed
with sub-tasks. His example:

> Keep the AI Foundations YouTube channel publishing multiple long-form videos every
> week by handling the research, planning, and reporting, so Drake's time goes to
> filming.

**Context (5:45).** Drake calls this more important than the goal, since most goals
can be derived from it. Add → GitHub repository, file, or folder. What he added:

- Business-wide files he attaches to every project: a business overview (what the
  company does, team, products) and current 90-day priorities, both kept up to date.
- Project-specific files: brand voice, life story, point of view, and a YouTube
  playbook (video ideas, channel strategy, title rules, video structure, positioning,
  thumbnail strategy).

Only add context specific to you. Generic material makes the help generic.

## Workspace tour (10:00)

The landing screen offers starters (set up from recent work, connect tools, make a
plan). "Connect tools" reads your goal and context and lists where the work lives
(YouTube Studio analytics, scripts, content calendar).

Right-hand panels (10:49):

| Panel | What it holds |
|---|---|
| Threads | Threads the coordinator spawned, grouped by state (working, idle/blocked, waiting on you, resolved). |
| Library | Files you uploaded and files Claude produced. Drake's account showed a 50,000-file cap *(video)*. Upload from device or link a local folder. |
| Routines | Scheduled recurring work you set up from a thread. |

Hide panels with `+`; bring the panel back with the Overview button.

## Settings (12:26)

Tabs: General, Memory, Environment, Usage, Debug access.

**General → Models.** Separate model and effort settings for the coordinator and for
threads. Defaults Drake saw: coordinator effort **low**, thread effort **medium**
*(video)*. One secondary source says threads default to Opus at high effort; the two
disagree, so check your own settings page. Drake's advice is to leave defaults alone.

**Memory → Project instructions (13:25).** Loaded at the start of every new thread.
Example he saved: "Before every business task, read my business overview document."
In the multi-thread run you can see each thread do exactly that.

**Memory → memory.md.** Claude adds notes as you work, and you can add your own
("Drake doesn't work on Sundays"). Memory is shared across every thread.

**Gotcha:** project memory silently does nothing if memory is off at the account
level. The coordinator replied "I can't save that because memory is off." Fix:
account Settings → Memory → turn both toggles on, then ask it to retry.

## Running a multi-thread task (15:22)

Prompt used:

> I just uploaded my YouTube analytics from the past year. Figure out what's
> actually working on my channel, then plan my next four weeks of videos. This is a
> big job, so split it up however you think is best.

Plus a zip of 365 days of analytics. Don't tell it how to split the work.

The coordinator made two threads: analyze the past year, then plan four weeks from
the findings. The planning thread sat idle until the analysis finished, then got a
message from the coordinator pointing to the analysis output. A small graph at the
top shows thread state. Click a thread to see it as a normal chat, with breadcrumbs
back to the overview.

Output: a four-week plan as a Claude Doc, plus two artifacts (channel findings and
in-window video metrics) in the Library.

## Claude Docs inside a project (18:16)

Opening the plan opens a Docs panel (Google Docs-style, with date pickers and an
interactive checklist) next to the thread that wrote it. You can edit or comment on
the doc, or reply in the thread to steer it, and the thread edits the doc live.

## Threads waiting on you (19:27)

When a thread needs a decision it moves to **Waiting on you** and (with the mobile
app) can notify your phone. Drake's example: "Three a week is triple last year's
pace. If three won't fit, should I cut the build slot and plan for two a week?" You
answer inside that thread, not the coordinator chat. A resolved thread has to be
reopened before you can message it again. Results stay in the threads; the
coordinator chat does not repeat them.

## Creating a routine (21:12)

A routine is a scheduled task that runs whether or not you're at your computer. Set
one up by asking the coordinator in plain language. Drake asked for:

- a monthly reminder to upload YouTube analytics, and
- on upload, an interactive dashboard in his brand colors (soft neo-brutalism, neon
  blue and pink from an uploaded brand guide) answering three questions: are videos
  getting views, are they getting clicked, are topics going to plan. He also wanted
  to be able to ask the dashboard questions.

The coordinator judged this sequential and used **one thread with four tasks**: read
the brand guide, build the dashboard, set up the reminder, explain how it works. Not
everything gets parallelized.

The dashboard artifact had interactive charts, a period-over-period comparison, and a
built-in chat box (it asked for permission because the artifact uses connectors). It
also became a **template** that future runs reuse, so each month's dashboard looks
the same but covers only that month.

The thread blocked once to ask for a time zone before finishing.

## Routine trigger and instructions (26:10)

Routines button (top center) → the routine shows:

- **Trigger:** 8:50 a.m., days 1–3 of the month, America/New_York.
- **Instructions:** written by Claude, including a link to the dashboard template.

The Library afterwards held notes, analysis, and dashboard folders, including the
template.

## Applying this to content-ideas

This repo's daily For You feed is a natural fit for a Claude Project plus a routine.
A starting setup:

**Goal**

> Keep a daily For You feed of content ideas grounded in what competitors published
> in the last 24 hours, so time goes to filming and writing instead of research.

**Context**

- `brand_context/` (voice, positioning)
- `skills/content-ideas/references/content-strategy.md`
- `vision.json`, `docs/product-vision.md`
- The repo itself via Add → GitHub repository, so threads can run the scripts.

**Project instructions**

> Before any content task, read `content-strategy.md` and the brand context. Persistent
> state lives under `$CONTENT_HOME`, never the cwd. Do not invent competitor data; if
> the scrape fails, say so.

**Routine:** daily, early morning in your time zone: run `scrape.py` then
`generate_feed.py`, and drop the feed into the Library. Ask the coordinator in plain
language and let it write the trigger and instructions, then check them on the
Routines panel, the same way Drake did.

Two things to plan for:

- `SCRAPECREATORS_API_KEY` lives in `~/.config/content/.env` on your machine. A
  project thread is a cloud session and won't see it unless you add it as an
  environment secret. The project's Settings → Environment tab is the likely place;
  the video shows the tab but doesn't open it, so confirm before relying on it.
- Threads draw on your plan's usage, and parallel threads use it faster. Check the
  Usage tab after the first few runs before adding more routines.

## Sources

- Video: <https://www.youtube.com/watch?v=MLl41Q9p3Ps>
- [DevOps.com: Anthropic adds a coordinator to Claude Projects](https://devops.com/anthropic-adds-a-coordinator-to-claude-projects-for-running-ai-work-in-parallel/)
- [MindStudio: Claude Projects agentic OS threads](https://www.mindstudio.ai/blog/claude-projects-agentic-os-threads/)
- [The AI Career Lab: parallel agent threads](https://theaicareerlab.com/blog/claude-code-projects-parallel-agents-beta-2026)
- [AI Codex: Projects redesigned with threads](https://www.aicodex.to/articles/projects-redesigned-threads)
