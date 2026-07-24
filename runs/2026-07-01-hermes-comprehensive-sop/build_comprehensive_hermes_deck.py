#!/usr/bin/env python3
"""Build a comprehensive Hermes use-case realization SOP deck."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"
QA = ROOT / "qa"
SRC = ROOT / "sources"
WATCH = ROOT / "watch-hermes-practice"

sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, Inches, PP_ALIGN  # noqa: E402


FOOTER = "Hermes Agent Use Cases + Realization SOP | Source-backed draft reviewed in PPTX QA"


def clean_vtt(path: Path) -> list[tuple[str, str]]:
    if not path.exists():
        return []
    rows: list[tuple[str, str]] = []
    last = ""
    cur_time = ""
    for raw in path.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line == "WEBVTT" or line.startswith(("Kind:", "Language:")):
            continue
        if "-->" in line:
            cur_time = line.split("-->", 1)[0].strip()[:8]
            continue
        if line.isdigit():
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        if not line or line == last:
            continue
        rows.append((cur_time, line))
        last = line
    return rows


def video_evidence(rows: list[tuple[str, str]]) -> list[tuple[str, str]]:
    keywords = [
        "Hermes", "search API", "Gbrain", "G brain", "Obsidian", "smart contacts",
        "activity dependent model", "cron jobs", "Slack", "email", "LinkedIn",
        "Twitter", "skills", "investors", "security", "Zoom", "team",
    ]
    hits: list[tuple[str, str]] = []
    seen = set()
    for t, line in rows:
        low = line.lower()
        if any(k.lower() in low for k in keywords):
            key = (t, line[:90])
            if key in seen:
                continue
            seen.add(key)
            hits.append((t, line))
    return hits[:80]


def read_json(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(errors="ignore"))
    return {}


def result_urls(data: dict, limit: int = 10) -> list[str]:
    web = data.get("results", {}).get("web", [])
    return [r.get("url", "") for r in web[:limit] if r.get("url")]


def bullets(items, size=13, color=None):
    return [{"text": x, "bullet": True, "size": size, "space_before": 5, **({"color": color} if color else {})} for x in items]


def note(slide, text: str) -> None:
    slide.notes_slide.notes_text_frame.text = text


class Builder:
    def __init__(self):
        self.d = Deck(footer=FOOTER)
        self.b = self.d.b
        self.slide_no = 0
        self.total = 1

    def _footer(self, s):
        self.slide_no += 1
        self.d.footer(s, self.slide_no, self.total, dark=False)

    def header(self, s, title, subtitle=None):
        d, b = self.d, self.b
        d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
        d.text(s, title, d.M, Inches(0.38), d.CW, Inches(0.64), size=27,
               color=b.NAVY, bold=True, font=b.FONT_H, shrink=True)
        d.rect(s, d.M, Inches(1.06), Inches(1.45), Inches(0.05), b.TEAL)
        if subtitle:
            d.text(s, subtitle, d.M, Inches(1.20), d.CW, Inches(0.52), size=12.5,
                   color=b.MUTED, shrink=True)

    def cover(self, title, subtitle, chips):
        d, b = self.d, self.b
        s = d.slide(fill=b.NAVY)
        d.rect(s, Inches(10.45), 0, Inches(2.9), d.H, b.NAVY_2)
        d.rect(s, Inches(10.45), 0, Inches(0.08), d.H, b.TEAL)
        d.text(s, "CLIENT-READY SOP DECK", d.M, Inches(0.78), Inches(6.9), Inches(0.32), size=14, color=b.TEAL, bold=True)
        d.text(s, title, d.M, Inches(1.22), Inches(8.95), Inches(1.72), size=34, color=b.WHITE, bold=True, shrink=True)
        d.rect(s, d.M, Inches(2.92), Inches(2.1), Inches(0.06), b.GOLD)
        d.text(s, subtitle, d.M, Inches(3.22), Inches(8.8), Inches(0.8), size=16, color=b.LIGHT_TEAL, shrink=True)
        x = d.M
        for chip in chips:
            d.rect(s, x, Inches(4.42), Inches(2.25), Inches(0.38), b.NAVY_2, line=b.TEAL, radius=0.12)
            d.text(s, chip, x + Inches(0.12), Inches(4.51), Inches(2.0), Inches(0.22), size=10.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
            x += Inches(2.45)
        d.text(s, "Prepared from local Hermes files, setup PDF, YouTube /watch transcript and frames, and You.com source discovery.", d.M, Inches(6.28), Inches(9.4), Inches(0.42), size=12.5, color=b.LIGHT_TEAL, shrink=True)
        self._footer(s)
        note(s, "Sources: local Hermes config/SOUL/USER/MEMORY/cron/skills, Hermes Agent Setup PDF, YouTube video Xv36Z65VPv0, You.com searches.")

    def section(self, label, title, subtitle):
        d, b = self.d, self.b
        s = d.slide(fill=b.NAVY)
        d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
        d.text(s, label, d.M, Inches(1.05), Inches(2.6), Inches(0.3), size=14, color=b.TEAL, bold=True)
        d.text(s, title, d.M, Inches(1.55), Inches(9.9), Inches(1.05), size=36, color=b.WHITE, bold=True, shrink=True)
        d.rect(s, d.M, Inches(2.86), Inches(1.8), Inches(0.06), b.GOLD)
        d.text(s, subtitle, d.M, Inches(3.25), Inches(9.4), Inches(0.72), size=16, color=b.LIGHT_TEAL, shrink=True)
        self._footer(s)
        note(s, subtitle)

    def content(self, title, subtitle, left_title, left_items, right_title=None, right_items=None, banner=None):
        d, b = self.d, self.b
        s = d.slide(fill=b.WHITE)
        self.header(s, title, subtitle)
        y = Inches(1.78)
        if banner:
            d.rect(s, d.M, y, d.CW, Inches(0.52), b.NAVY, radius=0.08)
            d.text(s, banner, d.M + Inches(0.15), y + Inches(0.12), d.CW - Inches(0.3), Inches(0.25), size=13, color=b.WHITE, bold=True, shrink=True)
            y += Inches(0.74)
        col_w = Inches(5.85)
        d.rect(s, d.M, y, col_w, Inches(4.55), b.SOFT, line=b.GRID, radius=0.08)
        d.text(s, left_title, d.M + Inches(0.22), y + Inches(0.22), col_w - Inches(0.44), Inches(0.3), size=16, color=b.NAVY, bold=True, shrink=True)
        d.text(s, bullets(left_items, size=12.8), d.M + Inches(0.28), y + Inches(0.72), col_w - Inches(0.55), Inches(3.55), shrink=True)
        if right_title:
            x2 = d.M + col_w + Inches(0.43)
            d.rect(s, x2, y, col_w, Inches(4.55), b.WHITE, line=b.GRID, radius=0.08, shadow=True)
            d.text(s, right_title, x2 + Inches(0.22), y + Inches(0.22), col_w - Inches(0.44), Inches(0.3), size=16, color=b.NAVY, bold=True, shrink=True)
            d.text(s, bullets(right_items or [], size=12.8), x2 + Inches(0.28), y + Inches(0.72), col_w - Inches(0.55), Inches(3.55), shrink=True)
        self._footer(s)
        note(s, f"{title}: {subtitle}")

    def matrix(self, title, subtitle, columns, rows):
        d, b = self.d, self.b
        s = d.slide(fill=b.WHITE)
        self.header(s, title, subtitle)
        x0, y0 = d.M, Inches(1.74)
        widths = [Inches(w) for w in [2.25, 3.15, 3.15, 3.15][: len(columns)]]
        h_head, h_row = Inches(0.42), Inches(0.46)
        x = x0
        for i, col in enumerate(columns):
            d.rect(s, x, y0, widths[i], h_head, b.NAVY if i == 0 else b.TEAL)
            d.text(s, col, x + Inches(0.08), y0 + Inches(0.1), widths[i] - Inches(0.16), Inches(0.2), size=10.5, color=b.WHITE, bold=True, shrink=True)
            x += widths[i]
        y = y0 + h_head
        for ridx, row in enumerate(rows[:10]):
            x = x0
            fill = b.SOFT if ridx % 2 == 0 else b.WHITE
            for i, cell in enumerate(row[: len(columns)]):
                d.rect(s, x, y, widths[i], h_row, fill, line=b.GRID)
                d.text(s, str(cell), x + Inches(0.08), y + Inches(0.08), widths[i] - Inches(0.16), Inches(0.28), size=9.5, color=b.INK, shrink=True)
                x += widths[i]
            y += h_row
        self._footer(s)
        note(s, f"Matrix: {title}")

    def usecase_spec(self, uc, idx):
        d, b = self.d, self.b
        s = d.slide(fill=b.WHITE)
        self.header(s, f"UC{idx:02d}. {uc['name']}", uc["so_what"])
        # left teal panel
        d.rect(s, d.M, Inches(1.74), Inches(3.05), Inches(4.78), b.TEAL, radius=0.08)
        d.text(s, "USE-CASE SPEC", d.M + Inches(0.18), Inches(1.96), Inches(2.7), Inches(0.3), size=14, color=b.NAVY, bold=True, shrink=True)
        spec = [
            f"Trigger: {uc['trigger']}",
            f"User: {uc['user']}",
            f"Output: {uc['output']}",
            f"Autonomy: {uc['autonomy']}",
        ]
        d.text(s, bullets(spec, size=11.2, color=b.NAVY), d.M + Inches(0.2), Inches(2.48), Inches(2.62), Inches(2.55), shrink=True)
        d.rect(s, d.M + Inches(0.22), Inches(5.28), Inches(2.6), Inches(0.62), b.GOLD, radius=0.08)
        d.text(s, uc["kpi"], d.M + Inches(0.35), Inches(5.43), Inches(2.35), Inches(0.26), size=12.5, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        x = d.M + Inches(3.35)
        d.rect(s, x, Inches(1.74), Inches(4.25), Inches(4.78), b.SOFT, line=b.GRID, radius=0.08)
        d.text(s, "Why This Matters", x + Inches(0.2), Inches(1.96), Inches(3.85), Inches(0.3), size=15, color=b.NAVY, bold=True)
        d.text(s, bullets(uc["why"], size=12.3), x + Inches(0.24), Inches(2.45), Inches(3.7), Inches(3.35), shrink=True)
        x2 = x + Inches(4.55)
        d.rect(s, x2, Inches(1.74), Inches(3.25), Inches(4.78), b.WHITE, line=b.GRID, radius=0.08, shadow=True)
        d.text(s, "Inputs", x2 + Inches(0.2), Inches(1.96), Inches(2.85), Inches(0.3), size=15, color=b.NAVY, bold=True)
        d.text(s, bullets(uc["inputs"], size=12.0), x2 + Inches(0.24), Inches(2.45), Inches(2.75), Inches(3.35), shrink=True)
        self._footer(s)
        note(s, f"Use case spec for {uc['name']}.")

    def usecase_arch(self, uc, idx):
        d, b = self.d, self.b
        s = d.slide(fill=b.WHITE)
        self.header(s, f"UC{idx:02d}. Realization Architecture", uc["name"])
        y = Inches(1.82)
        steps = uc["flow"]
        box_w = Inches(2.22)
        for i, step in enumerate(steps[:5]):
            x = d.M + Inches(i * 2.42)
            d.rect(s, x, y, box_w, Inches(1.05), b.NAVY if i in (0, 4) else b.SOFT, line=b.TEAL if i in (0, 4) else b.GRID, radius=0.08)
            d.text(s, step, x + Inches(0.12), y + Inches(0.18), box_w - Inches(0.24), Inches(0.62), size=11.5, color=b.WHITE if i in (0, 4) else b.INK, bold=i in (0, 4), align=PP_ALIGN.CENTER, shrink=True)
            if i < min(len(steps), 5) - 1:
                d.text(s, "->", x + box_w + Inches(0.05), y + Inches(0.34), Inches(0.25), Inches(0.2), size=14, color=b.TEAL, bold=True)
        d.rect(s, d.M, Inches(3.18), Inches(5.9), Inches(2.9), b.SOFT, line=b.GRID, radius=0.08)
        d.text(s, "Solution Components", d.M + Inches(0.2), Inches(3.4), Inches(5.4), Inches(0.3), size=15, color=b.NAVY, bold=True)
        d.text(s, bullets(uc["components"], size=12.0), d.M + Inches(0.25), Inches(3.85), Inches(5.3), Inches(1.8), shrink=True)
        x2 = d.M + Inches(6.25)
        d.rect(s, x2, Inches(3.18), Inches(5.9), Inches(2.9), b.NAVY, radius=0.08)
        d.text(s, "Integration Pattern", x2 + Inches(0.2), Inches(3.4), Inches(5.4), Inches(0.3), size=15, color=b.TEAL, bold=True)
        d.text(s, bullets(uc["integration"], size=12.0, color=b.WHITE), x2 + Inches(0.25), Inches(3.85), Inches(5.3), Inches(1.8), shrink=True)
        self._footer(s)
        note(s, f"Architecture for {uc['name']}. Components: {', '.join(uc['components'])}")

    def usecase_sop(self, uc, idx):
        d, b = self.d, self.b
        s = d.slide(fill=b.WHITE)
        self.header(s, f"UC{idx:02d}. SOP, Controls, Acceptance", uc["name"])
        cols = [
            ("SOP", uc["sop"], b.SOFT),
            ("Controls", uc["controls"], b.WHITE),
            ("Done Means", uc["acceptance"], b.SOFT),
        ]
        x = d.M
        for title, items, fill in cols:
            d.rect(s, x, Inches(1.78), Inches(3.85), Inches(4.75), fill, line=b.GRID, radius=0.08, shadow=(fill == b.WHITE))
            d.text(s, title, x + Inches(0.2), Inches(2.0), Inches(3.4), Inches(0.28), size=15, color=b.NAVY, bold=True)
            d.text(s, bullets(items, size=11.5), x + Inches(0.25), Inches(2.42), Inches(3.28), Inches(3.45), shrink=True)
            x += Inches(4.05)
        self._footer(s)
        note(s, f"SOP and controls for {uc['name']}.")


def build_use_cases() -> list[dict]:
    def uc(name, so_what, trigger, user, output, autonomy, kpi, why, inputs, components, integration, flow, sop, controls, acceptance):
        return locals()

    base_controls = [
        "Use You.com Search/Research before generic web search.",
        "Route full-page capture to livecrawl/Contents or Firecrawl only when needed.",
        "Keep approval gates for outbound send, payments, permissions, and destructive actions.",
        "Log source URLs, run ID, model route, token/cost estimate, and human decision.",
    ]
    return [
        uc("Daily Executive Brief", "One morning packet replaces scattered checking across email, calendar, Slack, news, and social feeds.", "Scheduled cron or user asks for today's brief", "Founder, executive, account lead", "Brief in chat, email, Slack, or Obsidian note", "Draft + notify; human decides actions", "Time saved per morning", ["Consolidates high-signal work before the day starts.", "Turns passive channels into a prioritized action queue.", "Creates a repeatable operating rhythm for busy professionals."], ["Calendar", "Email", "Slack/Teams", "News/social signals", "GBrain memory"], ["Cron scheduler", "You.com Search/Research", "GBrain recall", "Calendar/email connectors", "Messaging gateway"], ["One cron job builds source pack; agent synthesizes; delivery channel posts final; follow-up tasks become skills or kanban cards."], ["Cron wakes on schedule", "Collect today's meetings and unread signals", "Recall relevant people/projects", "Research external events", "Publish brief and open decisions"], ["Define brief sections and priority scoring.", "Create cron job with workdir and delivery target.", "Bind GBrain recall before synthesis.", "Add escalation rule for urgent items."], base_controls, ["Brief includes meetings, risks, asks, and sources.", "No outbound action occurs without explicit approval.", "Missed-source rate is tracked weekly."]),
        uc("Smart Contacts And Entities", "A self-updating relationship layer gives Hermes context before meetings and outreach.", "New meeting, email thread, or entity mention", "Executive, sales lead, investor relations", "Entity profile and relationship recommendations", "Autonomous enrichment; human reviews sensitive notes", "Profile freshness", ["Turns scattered emails and social mentions into durable profiles.", "Lets the agent inject relationship context at the right moment.", "Creates a practical personal CRM without manual data entry."], ["Email", "Calendar", "Zoom transcripts", "LinkedIn/Twitter", "Contacts", "You.com enrichment"], ["GBrain graph", "Obsidian", "You.com Research", "Entity extraction skill", "Dedup/fuzzy matching"], ["Ingest private context; enrich public facts; write Markdown entity notes; expose graph in Obsidian; inject relevant context during tasks."], ["Collect private touchpoints", "Extract entities", "Enrich via You.com", "Write GBrain notes", "Surface context in workflows"], ["Define entity schema.", "Schedule ingestion and enrichment.", "Add conflict flags for stale or contradictory facts.", "Create Obsidian graph view."], base_controls, ["Each profile has source provenance.", "Duplicates are merged or flagged.", "Agent can answer why a contact matters."]),
        uc("Pre-Call Account Brief", "Every meeting starts with account context, current signals, and a proposed conversation plan.", "Calendar event within next 24 hours", "Account executive, solution architect, PM", "Meeting brief and talk track", "Autonomous draft; user edits", "Prep time reduced", ["Improves meeting quality without last-minute research.", "Combines CRM-like memory with live web signals.", "Supports mixed business and technical audiences."], ["Calendar", "GBrain account notes", "LinkedIn/company pages", "Recent news", "Prior calls"], ["Calendar connector", "You.com Search", "GBrain recall", "Zoom transcript store", "Brief template"], ["Calendar trigger identifies participants; GBrain recalls history; You.com refreshes company/person facts; agent writes brief."], ["Detect meeting", "Resolve participants", "Recall history", "Research current events", "Draft agenda and asks"], ["Create participant resolver.", "Define account-brief template.", "Add 24h and 1h reminders.", "Attach source links."], base_controls, ["Brief has attendee map, account context, open asks, and risks.", "Recent external facts are dated.", "Sensitive assumptions are labeled."]),
        uc("Investor Intelligence And Outreach Tracker", "Fundraising research becomes a live investor map with thesis match, hooks, and follow-up state.", "Seed raise, pipeline refresh, investor reply", "Founder or finance lead", "Investor spreadsheet plus draft outreach", "Draft outreach; human sends", "Qualified investor coverage", ["Scales research across hundreds of investors.", "Matches thesis, portfolio, and social signals to the company story.", "Prevents generic cold outreach."], ["Investor list", "Portfolio pages", "LinkedIn/Twitter", "Email", "Public interviews", "GBrain notes"], ["You.com Research", "Finance Research", "Spreadsheet writer", "Email drafting", "Inbox monitor"], ["Source-of-truth table stores investors; research enriches rows; model drafts hooks; inbox monitor updates status."], ["Compile investor universe", "Enrich each investor", "Score thesis match", "Draft tailored hook", "Track responses"], ["Define table schema.", "Run batch enrichment with rate limits.", "Create no-auto-send policy.", "Monitor replies and update stage."], base_controls + ["Never send investor emails automatically by default."], ["Rows include source URLs and confidence.", "Drafts are personalized, not spam templates.", "Follow-up cadence respects human approval."]),
        uc("Relationship Manager And Coach", "The agent nudges relationship maintenance based on real context, not a static CRM reminder.", "No contact for N days or important public signal", "Executive, founder, sales lead", "Suggested touchpoint and context", "Suggest only by default", "Useful nudges accepted", ["Helps maintain a network without manual CRM hygiene.", "Uses news/social changes as reasons to reach out.", "Avoids awkward context gaps before outreach."], ["Smart contacts", "Public posts/news", "Email history", "Calendar history"], ["GBrain graph", "You.com Search", "Signal monitor cron", "Drafting skill"], ["Signals update entity state; relationship rules score next-best actions; user approves outreach."], ["Monitor entity signals", "Score relationship gap", "Draft note", "Ask approval", "Record outcome"], ["Set relationship tiers.", "Define do-not-contact and sensitivity rules.", "Create cadence scoring.", "Log accepted/rejected nudges."], base_controls, ["Recommendations cite the trigger.", "No message is sent without approval.", "User feedback tunes future ranking."]),
        uc("Social And News Signal Monitor", "Hermes filters the information flood into a few signals worth acting on.", "Hourly/daily cron or explicit research request", "Executive, marketer, PM, investor", "Signal digest and action queue", "Autonomous monitor; human acts", "Signal-to-noise ratio", ["Keeps professionals current without doom-scrolling.", "Finds weak signals across social, web, news, Reddit, and YouTube.", "Turns monitoring into concrete actions."], ["Twitter/X", "LinkedIn", "Reddit", "YouTube", "News/web", "Google Trends"], ["You.com Search", "Reddit skills", "YouTube watch/video skill", "Cron", "Topic taxonomy"], ["Each topic has queries and thresholds; monitor retrieves, clusters, ranks, and routes signals."], ["Run queries", "Cluster mentions", "Rank novelty", "Attach sources", "Recommend actions"], ["Define topics and ignored noise.", "Set freshness windows.", "Create scoring rubric.", "Store daily signal log."], base_controls, ["Digest separates fact, inference, and recommendation.", "Sources are current and linked.", "Repeated noise is suppressed."]),
        uc("Twitter/X Engagement Radar", "The agent identifies high-value conversations and prepares replies without consuming the user's day.", "New signal from monitored accounts/topics", "Founder, PM, marketer", "Engagement queue with reply drafts", "Draft only unless explicitly allowed", "Relevant replies shipped", ["Captures attention-market opportunities.", "Keeps posting aligned to current conversations.", "Avoids manual feed scanning."], ["X search", "Follow lists", "GBrain persona", "Campaign goals"], ["Browser/computer-use for logged-in access", "You.com Search", "Social skill", "Approval queue"], ["Use API/search where available; use browser only when platform API is unavailable; drafts wait for user approval."], ["Watch topics", "Identify threads", "Recall voice", "Draft reply", "Queue approval"], ["Create target account lists.", "Define reply criteria.", "Set browser safety rules.", "Record posted/rejected outcomes."], base_controls + ["Do not bypass platform terms or automate spam behavior."], ["Queue contains rationale per reply.", "Human can approve, edit, or reject.", "Rejected styles are learned."]),
        uc("LinkedIn Relationship And Posting Assistant", "Hermes can work around limited LinkedIn API access by using browser-based workflows carefully.", "User asks for LinkedIn prep or scheduled review", "Executive, founder, sales lead", "Draft posts, profile notes, engagement suggestions", "Draft and navigate; human clicks sensitive actions", "Approved LinkedIn actions", ["LinkedIn lacks easy API coverage for many personal workflows.", "Browser access lets the agent inspect visible context.", "Approval gates preserve reputation and account safety."], ["Logged-in browser", "Profile pages", "Posts", "GBrain contacts", "Campaign calendar"], ["Computer-use/browser", "You.com Search", "GBrain", "Content drafting skill"], ["Prefer search/docs first; use user browser for private network context; never type secrets or click sensitive prompts."], ["Capture page", "Extract context", "Draft action", "Ask approval", "Record result"], ["Define allowed LinkedIn tasks.", "Create no-auto-post default.", "Add screenshot/source capture.", "Track account risk."], base_controls + ["Stop at login, 2FA, permission, or suspicious prompts."], ["Every action is reversible or approved.", "No private data leaks into public posts.", "Drafts match user's voice."]),
        uc("Content Intelligence Blog Pipeline", "The MindStudio-style blog system turns AI-news monitoring into high-volume SEO/AEO content.", "Daily content run", "Growth, marketing, founder", "Topic list, briefs, posts, ad variants", "Human review recommended before publish", "Qualified organic traffic", ["Uses YouTube creators as a proxy for what the market wants.", "Deep research creates grounded long-form content.", "Ad variants and internal links become part of the pipeline."], ["YouTube channels", "Transcripts", "You.com Research", "Product ads", "CMS"], ["YouTube transcript skill", "You.com Search/Research", "Content writer", "Ad generator", "CMS connector"], ["Topic mining -> research -> story angle -> post -> ad variants -> publish queue."], ["Pull creator videos", "Extract topics", "Deep research", "Write posts", "Generate variants"], ["Pick source channels.", "Define editorial policy.", "Create citation requirements.", "Add publish approval gate."], base_controls, ["Posts cite research sources.", "No duplicate thin content.", "Performance feeds next topic selection."]),
        uc("YouTube Video Research Weekly Job", "A plain-English cron can turn video monitoring into recurring research briefs.", "Every Monday 9am or user-defined schedule", "Researcher, analyst, PM", "Video brief with citations and screenshots", "Autonomous draft", "Briefs produced on schedule", ["Video is a rich source of practitioner detail.", "The /watch pattern extracts transcript and frames.", "Recurring jobs make research proactive."], ["YouTube URLs/channels", "Captions", "Frames", "You.com follow-up research"], ["Watch-video skill", "Cron", "You.com Search", "Frame archive", "Research template"], ["Cron invokes watch skill, then You.com fills gaps, then a report is delivered."], ["Collect videos", "Run watch", "Extract claims", "Verify with web", "Deliver brief"], ["Set channel watchlist.", "Choose frame budget.", "Define claim-verification rules.", "Archive transcript and frames."], base_controls, ["Timestamped evidence is retained.", "Claims are verified or labeled unverified.", "Long videos are focused when needed."]),
        uc("SEO And AEO Content Variant Factory", "Hermes can generate many search-answer variants while preserving source discipline.", "New topic, product launch, or content refresh", "Growth, product marketing", "Article, FAQ, snippets, ads", "Draft queue", "Content coverage", ["AI answer engines need concise, cited, structured source material.", "Variants help test angles without manually rewriting.", "Grounding prevents generic AI output."], ["Research brief", "Keyword set", "Competitor pages", "Product positioning"], ["You.com Search", "Firecrawl/Contents", "Content skill", "AEO evidence skills", "CMS"], ["Research pack drives variant generation; each variant points back to source claims and target intent."], ["Map intent", "Collect sources", "Write variants", "QA claims", "Publish queue"], ["Define claim library.", "Set keyword and FAQ targets.", "Block unsupported stats.", "Track indexed/performance results."], base_controls, ["Each claim maps to source.", "No invented metrics.", "Variant purpose is explicit."]),
        uc("Cost And Model Spend Scan", "Daily cost inspection prevents autonomous agents from becoming expensive background noise.", "Nightly cron or threshold breach", "Operator, engineering lead", "Spend dashboard and fix plan", "Suggest fixes; user approves major changes", "Cost per useful output", ["Agent loops can drift into costly model choices.", "Model routing saves money without reducing quality.", "Daily scans find runaway jobs early."], ["Token logs", "Model route config", "Cron history", "Tool traces"], ["Cron", "Cost parser", "Activity-dependent model policy", "Config editor", "Alert delivery"], ["Scan logs, rank expensive workflows, identify wrong-model use, propose config or skill fixes."], ["Read usage", "Rank costs", "Find anomalies", "Recommend fixes", "Track savings"], ["Define budgets by job.", "Create alert thresholds.", "Audit model selection.", "Record before/after spend."], base_controls, ["Dashboard itemizes spend.", "Recommendations include risk.", "Changes are versioned."]),
        uc("Activity-Dependent Model Routing", "Hermes chooses model strength based on task type instead of running everything on the most expensive model.", "Any task start or subtask classification", "Agent operator", "Model route decision and fallback", "Autonomous within approved policy", "Quality per dollar", ["Everyday tasks do not need the strongest model.", "Code and deep reasoning can justify premium models.", "Summarization and parsing should use cheaper models where safe."], ["Task prompt", "Skill metadata", "Model catalog", "Cost/quality policy"], ["Model selector skill", "Fallback provider chain", "Config.yaml", "Cost monitor"], ["Classifier maps task to model tier; fallback chain handles provider failure; logs support audit."], ["Classify task", "Select tier", "Run task", "Log route", "Review drift"], ["Define tiers by provider.", "Map skills to model needs.", "Set fallback chain.", "Add drift scanner."], base_controls, ["Route is visible in logs.", "Premium model use has reason.", "Fallbacks are tested."]),
        uc("Security And Permissions Audit", "The agent should inspect its own risk surface before it expands capability.", "Daily cron, new integration, or profile export", "Security-conscious operator", "Risk report and remediation checklist", "Suggest and patch safe items; ask on sensitive changes", "Unreviewed exposure reduced", ["Hermes may touch email, browser, files, and secrets.", "Separate-device/profile strategies reduce blast radius.", "Cron and plugins need recurring review."], ["Config.yaml", ".env references", "MCP servers", "Cron jobs", "Browser permissions", "Skills"], ["Security audit skill", "Config parser", "Secret redaction", "Cron scanner", "MCP inventory"], ["Audit local state; flag broad permissions; patch obvious misconfigurations; escalate anything destructive."], ["Inventory access", "Rank risks", "Check secrets", "Review cron", "Patch or ask"], ["Define risk rubric.", "Create allow/deny lists.", "Schedule audit.", "Store exception decisions."], base_controls + ["Never print API keys or bearer tokens."], ["Secrets are masked.", "High-risk changes require approval.", "Audit result is dated and stored."]),
        uc("MCP And Plugin Health Monitor", "The agent watches its tool layer so workflows fail loudly instead of silently degrading.", "Scheduled healthcheck or failed tool call", "Agent operator", "Tool health report", "Autonomous diagnostics; ask before installs", "Healthy tool coverage", ["MCPs and plugins are the agent's hands.", "Broken connectors can make skills appear useless.", "Health status helps route fallback tools."], ["MCP server list", "Plugin config", "Tool discovery output", "Skill dependencies"], ["MCP health skill", "Plugin inventory", "Tool-search policy", "Alert channel"], ["Health job probes each server/plugin; results update capability map and recommend repairs."], ["Probe tools", "Record status", "Map affected skills", "Recommend repair", "Notify"], ["Create capability inventory.", "Define dependency map.", "Add health cron.", "Patch skill instructions for fallback."], base_controls, ["Report lists affected workflows.", "No install runs without approval.", "Fallback path is documented."]),
        uc("Cross-Channel Data Ingestion", "Hermes turns email, Slack, calendar, Zoom, and files into a unified context stream.", "Scheduled ingestion or new artifact", "Knowledge worker, chief of staff", "Structured notes and entity updates", "Autonomous ingest; approval for external posting", "Fresh context coverage", ["Daily work is fragmented across channels.", "Unified ingestion gives every downstream use case context.", "GBrain and skills convert raw data into reusable memory."], ["Email", "Slack", "Calendar", "Zoom", "Documents", "Browser"], ["Connectors", "Transcript processor", "Entity extractor", "GBrain write-back", "Dedup logic"], ["Ingest channels into staging; extract facts/entities; write durable notes; link to source artifacts."], ["Pull data", "Normalize", "Extract entities", "Deduplicate", "Write memory"], ["Define source boundaries.", "Create retention policy.", "Add PII handling.", "Schedule incremental ingest."], base_controls, ["Source coverage is tracked.", "Private data stays local unless approved.", "Duplicates and conflicts are flagged."]),
        uc("GBrain Dreaming And Knowledge Compaction", "Nightly memory maintenance keeps the knowledge graph clean enough to trust.", "Nightly cron or large ingestion batch", "Agent operator", "Merged, linked, cleaned memory", "Autonomous with audit log", "Contradictions resolved", ["Raw memory becomes cluttered over time.", "Dreaming deduplicates, links, and reconciles facts.", "Human-readable Markdown makes corrections practical."], ["GBrain notes", "Obsidian vault", "Session summaries", "Entity profiles"], ["GBrain service", "Git-backed Markdown", "Dream cron", "Conflict detector"], ["Dream job scans notes, merges duplicates, flags contradictions, and commits changes for audit."], ["Scan graph", "Merge duplicates", "Flag conflicts", "Link entities", "Commit changes"], ["Set dream schedule.", "Define merge rules.", "Keep git history.", "Review conflict queue weekly."], base_controls, ["Changes are inspectable.", "Conflicts are not silently overwritten.", "Graph becomes easier to query."]),
        uc("Obsidian Graph Visualization", "A visual graph helps humans inspect and correct what the agent believes.", "User opens knowledge review or entity audit", "Founder, researcher, analyst", "Obsidian vault and graph view", "Human inspection", "Graph correctness", ["Visualizing links makes memory errors obvious.", "Non-technical users can inspect the knowledge base.", "It turns agent memory into a shared artifact."], ["GBrain Markdown", "Entity links", "Project notes", "Relationship edges"], ["Obsidian", "GBrain vault", "Markdown schemas", "Graph filters"], ["GBrain stores Markdown; Obsidian renders graph; user edits notes; agent respects corrected source."], ["Open vault", "Filter graph", "Inspect entity", "Edit note", "Sync back"], ["Define vault location.", "Create note templates.", "Set graph filters.", "Document correction workflow."], base_controls, ["Graph nodes map to real notes.", "Human edits are preserved.", "Agent can cite edited notes."]),
        uc("Phone-To-App Builder", "The agent can build or modify small tools while the user is away from the workstation.", "Mobile message asks for app/tool/workflow", "Founder, operator, engineer", "Working app, script, or PR", "Build in sandbox; human reviews", "Working artifacts delivered", ["Turns idle time into implementation time.", "Hermes can use coding agents and repo tools.", "Useful for small internal apps and workflow fixes."], ["Phone gateway", "Repo", "Requirements prompt", "Existing skills"], ["Messaging gateway", "Coding agent/proxy", "GitHub skills", "Playwright/dogfood QA"], ["Mobile message creates spec; agent builds in repo; QA runs; user gets link/summary."], ["Receive request", "Clarify if needed", "Implement", "Test", "Report link"], ["Define mobile command format.", "Set repo permissions.", "Require tests before delivery.", "Block destructive operations."], base_controls, ["Artifact runs locally.", "Tests or smoke checks pass.", "Changes are summarized with file paths."]),
        uc("Code And Repo Self-Improvement", "Hermes captures repeated workflows as skills and improves its own operating procedures.", "Repeated successful task pattern", "Agent operator, developer", "New or updated skill", "Suggest/create; human can review", "Repeat work automated", ["Skills reduce repeated prompting.", "Generated procedures make agents more consistent.", "Skill QA prevents isolated skill chaining."], ["Session history", "Successful commands", "Repo conventions", "AGENTS.md"], ["Skill creator", "Curator", "Goal-loop orchestrator", "Repo skill root"], ["After repeated success, agent drafts a skill; curator prunes stale ones; orchestrator verifies chaining value."], ["Detect pattern", "Draft skill", "Test procedure", "Install locally", "Review later"], ["Define skill acceptance tests.", "Document dependencies.", "Add search-tool policy.", "Run chaining QA."], base_controls, ["Skill has trigger, dependencies, and verification.", "It consumes/produces concrete artifacts.", "It is discoverable in target hosts."]),
        uc("Back-Office Browser And Desktop Automation", "Hermes can use browser and computer-use tools when APIs are absent.", "User asks for repetitive web/native app work", "Operations, sales, analyst", "Completed workflow or evidence report", "Autonomous only within safe bounds", "Manual steps eliminated", ["Many enterprise systems have poor APIs.", "Browser and GUI control can bridge gaps.", "Safety rules keep secret/payment/permission actions human-led."], ["Browser session", "Native apps", "Files", "Screenshots"], ["Browser toolset", "Computer-use", "Dogfood QA", "OCR/document skill"], ["Use structured APIs first; use browser/computer-use for locked systems; verify after every state change."], ["Capture state", "Click/type safely", "Verify", "Extract output", "Report"], ["Document allowed apps.", "Block sensitive prompts.", "Use screenshots as evidence.", "Add retry/verification steps."], base_controls + ["Do not click password, 2FA, payment, or permission dialogs."], ["Screenshots or logs prove completion.", "No hidden irreversible action.", "User can replay SOP."]),
        uc("Spreadsheet And Document Automation", "Hermes can turn rough research or operating data into structured spreadsheets and documents.", "User requests tracker, report, or transformation", "Founder, analyst, PM", "Spreadsheet, doc, or PPT source table", "Autonomous draft", "Manual spreadsheet work reduced", ["Many workflows begin or end in spreadsheets.", "Agent-generated trackers are useful when source fields are clear.", "Document automation supports stakeholder-ready delivery."], ["CSV/XLSX", "Google Sheets", "Docs", "Research output", "Email"], ["Spreadsheet connector", "Document parser", "You.com enrichment", "Export skill"], ["Agent builds schema, populates rows, validates fields, then exports to target format."], ["Define schema", "Ingest rows", "Enrich", "Validate", "Export"], ["Set schema before filling.", "Track source per row.", "Validate formulas.", "Protect confidential fields."], base_controls, ["Rows have provenance.", "Formulas calculate correctly.", "Deck/report can consume the table."]),
        uc("Team Or Company GBrain", "A shared memory graph can support a whole team while preserving profile and permission boundaries.", "Team wants shared knowledge layer", "Startup team, enterprise practice", "Shared graph and access policy", "Admin-managed", "Knowledge reuse", ["Team agents need common context.", "A shared graph reduces repeated research.", "Profiles keep roles and credentials separate."], ["Team docs", "Meeting notes", "Slack", "Project repos", "Account data"], ["GBrain server", "Hermes profiles", "MCP auth", "Git-backed vault", "Access policy"], ["Shared memory is exposed through MCP; each profile has its own SOUL/config while reading approved shared context."], ["Define schema", "Set permissions", "Ingest docs", "Expose MCP", "Audit access"], ["Separate personal vs team memory.", "Create write-back rules.", "Use profile packaging.", "Review access logs."], base_controls, ["Shared facts have owners.", "Sensitive memories are scoped.", "Profiles can be packaged safely."]),
        uc("Multi-Profile Role Agents", "Profiles replace one giant assistant with role-specific agents that can be packaged and reused.", "Need assistant, researcher, PM, engineer, or sales profiles", "Agent operator, team lead", "Profile package with SOUL/config/skills/cron", "Admin creates; agent executes", "Profile fit to task", ["Different workflows need different personalities and tools.", "Profiles isolate config, memory, sessions, skills, cron, and gateway state.", "Role.md is not required when profile descriptions and SOUL files do the role work."], ["Profile config", "SOUL.md", "skills", "cron jobs", "MCP connections"], ["Hermes profiles", "SOUL.md", "Profile descriptions", "Skill packages", "Cron"], ["Each role gets profile home; shared packages exclude credentials/history; kanban or orchestrator routes tasks to profiles."], ["Create profile", "Write role SOUL", "Attach skills", "Add cron", "Package/share"], ["Define role boundaries.", "Avoid copying secrets.", "Document escalation rules.", "Test routing."], base_controls, ["Profile is discoverable.", "Credentials stay local.", "Role-specific behavior is observable."]),
        uc("Messaging Gateway Assistant", "Telegram, WhatsApp, Discord, or Slack can become the interface to Hermes.", "Message arrives through gateway", "Busy professional or team", "Reply, artifact, or queued task", "Depends on channel policy", "Requests handled outside terminal", ["The agent becomes available where the user already works.", "Gateway delivery supports scheduled jobs and mobile requests.", "Channel policy prevents noisy responses."], ["Telegram", "WhatsApp", "Discord", "Slack", "Files/media"], ["Gateway config", "Channel prompts", "Media handling", "Cron delivery", "Approval policy"], ["Incoming message creates a session; channel rules decide free-response vs mention-only; artifacts return through delivery channel."], ["Receive message", "Load profile", "Run task", "Deliver artifact", "Log context"], ["Configure channel scopes.", "Set mention/free-response rules.", "Add media directory policy.", "Document approval flow."], base_controls, ["No secrets typed into chat.", "Large artifacts are linked or delivered safely.", "Channel noise stays controlled."]),
        uc("Kanban And Multi-Agent Work Board", "A board can turn vague tasks into specs and route them to the right profile.", "New backlog item or triage card", "Team lead, PM, operator", "Specified task and assigned profile", "Human-in-loop for priority", "Tasks moved to done with evidence", ["Agent work needs visible state.", "Spec expansion prevents vague autonomous execution.", "Profiles can be selected by task type."], ["Kanban cards", "Profile descriptions", "Repo/docs", "Prior run artifacts"], ["Hermes dashboard/kanban", "Specifier model", "Profiles", "Goal-loop orchestrator"], ["Triage card becomes concrete spec; router selects profile; run artifacts feed back into card status."], ["Capture card", "Specify", "Route profile", "Execute", "Attach evidence"], ["Define done states.", "Require artifact links.", "Use chain QA for multi-skill tasks.", "Limit concurrent agents."], base_controls, ["Every card has acceptance criteria.", "Output artifacts are attached.", "Blocked cards show reason."]),
        uc("Finance Research And Deal Diligence", "You.com Finance Research can ground investor, company, and market questions in financial indexes.", "Investor prep, market scan, diligence question", "Founder, finance, strategy lead", "Cited finance brief", "Autonomous draft; human verifies before decisions", "Diligence cycle time", ["Financial workflows need fresher, structured data.", "Finance Research covers filings, fundamentals, market data, and news.", "Inline citations support verification."], ["Company names", "SEC filings", "Market data", "Financial news", "Investor profiles"], ["You.com Finance Research", "Spreadsheet tracker", "Citation verifier", "GBrain write-back"], ["Finance query runs specialized index; results become cited brief; key facts update deal tracker."], ["Frame question", "Run finance research", "Extract data", "Verify citations", "Write brief"], ["Use finance mode for finance claims.", "Verify material claims against citations.", "Avoid investment advice tone.", "Store assumptions."], base_controls + ["Label outputs as research, not financial advice."], ["Citations are present.", "Numbers have dates.", "Risks and uncertainties are explicit."]),
        uc("Deep Market Research Agent", "Hermes can run multi-step market research without forcing the user to manage every query.", "Strategic question or market scan", "Founder, strategist, consultant", "Research report and decision brief", "Autonomous research; human validates conclusion", "Decision confidence", ["Complex topics need multiple searches and cross-checking.", "You.com Research can carry part of the planning/search burden.", "Hermes adds user context and downstream actions."], ["Research question", "Official sources", "News", "Competitors", "Prior memory"], ["You.com Research", "Exa/Firecrawl fallback", "GBrain recall", "AI analyst validation"], ["Recall prior context; run Research API; ingest key pages; synthesize with confidence and caveats."], ["Recall context", "Run research", "Ingest pages", "Synthesize", "Recommend action"], ["Write research question precisely.", "Prefer primary sources.", "Mark unsupported claims.", "Save source pack."], base_controls, ["Report lists source URLs.", "Confidence is labeled.", "Decision options are concrete."]),
        uc("Customer And Community Signal Triage", "Community threads, support issues, and Reddit signals become a product-opportunity queue.", "Scheduled community scan", "PM, support lead, marketer", "Pain-point table and actions", "Draft opportunities", "Actionable pains found", ["Customer language is often outside official docs.", "Reddit and forums reveal switching triggers and objections.", "Fact-checking prevents overfitting to anecdotes."], ["Reddit", "Forums", "Support tickets", "Social posts", "Docs"], ["Reddit skills", "You.com Search", "Factcheck workflow", "Opportunity scorer"], ["Semantic probes find pains; factcheck filters claims; output becomes backlog/opportunity table."], ["Search communities", "Cluster pains", "Factcheck", "Score opportunity", "Route action"], ["Define target communities.", "Separate anecdote from evidence.", "Use exact thread URLs when known.", "Review before public response."], base_controls, ["Pain points include source snippets/URLs.", "Claims are fact-checked.", "Actions are assigned owners."]),
        uc("Automotive POC Factory Agent", "Hermes should be tuned to Sheker's real standard: demo on real data, architecture, cost, and business deck.", "New automotive GenAI POC request", "Enterprise solution architect", "POC package: demo, architecture, cost model, deck", "Build draft; human validates client context", "POC readiness", ["Matches the user's automotive and enterprise standards.", "Forces business value before code.", "Turns repeatable POC delivery into a governed pipeline."], ["Account context", "Realistic automotive data", "Cloud constraints", "Stakeholder goals", "Prior POCs"], ["USER.md policy", "GBrain recall", "Architecture-presentation", "Draw.io", "Branded PPTX"], ["User profile guides scope; GBrain recalls account patterns; skills build demo, architecture, cost, and deck."], ["Frame business problem", "Use real data", "Build demo", "Draw architecture", "Package deck"], ["Create account-specific POC templates.", "Require cost/latency analysis.", "Block synthetic-only demos.", "Run stakeholder-readiness QA."], base_controls, ["Live demo runs on realistic data.", "Architecture is production-aware.", "Deck explains ROI and path to scale."]),
        uc("Skill Dependency Hardening", "Search-capable skills should prefer wired search tools instead of drifting to generic web search.", "Skill creation/update or audit", "Agent operator", "Patched skill instructions", "Autonomous patch with review", "Search policy compliance", ["Research skills can silently use weak sources.", "You.com/Exa/Firecrawl/Reddit tools should be explicit dependencies.", "Goal-loop QA catches isolated skills that do not compound."], ["SKILL.md files", "Tool inventory", "Dependency map", "Run artifacts"], ["Goal-loop orchestrator", "You.com skill", "Exa/Firecrawl skills", "Reddit skills", "Skill auditor"], ["Audit skills for search language; patch routing matrix; verify each skill consumes and produces usable artifacts."], ["Inventory skills", "Find search usage", "Patch policy", "Test discovery", "Record compliance"], ["Add preferred-tool order.", "Define fallback conditions.", "State handoff artifact.", "Run chain QA after patch."], base_controls, ["Search dependencies are explicit.", "Generic search is fallback only.", "Skills produce downstream-ready artifacts."]),
        uc("Open Source Agent Evaluation Lab", "Hermes can compare OpenClaw, Hermes, NanoClaw, and custom harnesses against real workflows.", "New personal-agent framework appears", "AI operator, CTO, consultant", "Evaluation matrix and recommendation", "Research and test; human chooses", "Best-fit harness selected", ["The personal-agent space changes fast.", "Hands-on trials reveal reliability, bloat, security, and install friction.", "A repeatable test harness prevents hype-driven decisions."], ["GitHub repos", "Docs", "Install logs", "Workflow benchmarks", "Security notes"], ["You.com Search", "GitHub skill", "Dogfood tests", "Cost monitor", "Benchmark rubric"], ["Discover candidates; install in sandbox; run same use-case suite; score outcome and operational risk."], ["Discover tools", "Define tests", "Install safely", "Run benchmarks", "Recommend"], ["Use separate machine/profile.", "Record install failures.", "Score on real tasks.", "Avoid destructive tests."], base_controls, ["Matrix shows evidence.", "Recommendation includes tradeoffs.", "Tests are reproducible."]),
    ]


def build_synthesis(use_cases, evidence, hermes_urls, you_urls):
    lines = [
        "# Hermes Comprehensive Use Cases + Realization SOP",
        "",
        "## Goal Contract",
        "- Outcome: client-ready PPTX that explains Hermes architecture, integration components, persona/config files, and implementation SOPs for a comprehensive use-case catalog.",
        "- Artifacts: synthesis markdown, generated PPTX, preview QA artifacts, copied Windows Desktop deck.",
        "- Constraints: use local Hermes files, setup PDF, YouTube /watch evidence, You.com discovery, and branded PPTX workflow.",
        "- Acceptance criteria: 100+ slides; comprehensive use cases; architecture and solution components per use case; search-tool policy included; deck QA performed.",
        "- Research mode: local files first, You.com official/current docs, video transcript and frames, setup PDF.",
        "- Loop budget: 3 passes: synthesis, render, QA/fix.",
        "",
        "## Chain Contract",
        "| Step | Skill/action | Consumes | Produces | Next consumer | Value test |",
        "|---|---|---|---|---|---|",
        "| 1 | watch | YouTube URL | transcript + frames | synthesis | captures live demo setup |",
        "| 2 | you-com-search | Hermes/You API queries | source JSON | synthesis | current official docs and pricing corrections |",
        "| 3 | ai-analyst | source pack | validated synthesis | branded deck | converts raw evidence into structure |",
        "| 4 | branded-pptx-deck | synthesis | PPTX + QA | user | client-ready artifact |",
        "| 5 | goal-loop-orchestrator | chain outputs | QA decisions | final | proves skills compounded |",
        "",
        "## Source Inventory",
        "- Hermes setup PDF extracted to sources/Hermes-Agent-Setup-Google-Docs.txt.",
        "- YouTube /watch output: video.en.vtt, 80 frames, contact sheet.",
        "- Local Hermes files: config.yaml extracts, SOUL.md, USER.md, MEMORY.md, cron jobs, skills inventory.",
        "- You.com search outputs: you_search_hermes_architecture.json and you_search_you_api.json.",
        "- Official Hermes user-stories page fetched to sources/hermes_user_stories.html.",
        "",
        "## Important Correction",
        "The setup PDF says livecrawl extraction is bundled into the base You.com Search API price. Current You.com docs found during this run state that livecrawl is billed separately from the base Search API call. The deck treats pricing as current-doc dependent and avoids using the older claim unqualified.",
        "",
        "## Hermes URLs Found",
    ]
    lines += [f"- {u}" for u in hermes_urls]
    lines += ["", "## You.com URLs Found"]
    lines += [f"- {u}" for u in you_urls]
    lines += ["", "## Video Evidence Highlights"]
    lines += [f"- {t}: {txt}" for t, txt in evidence[:35]]
    lines += ["", "## Use Case Catalog"]
    for i, uc in enumerate(use_cases, 1):
        lines += [
            f"### UC{i:02d}. {uc['name']}",
            f"- Outcome: {uc['so_what']}",
            f"- Trigger: {uc['trigger']}",
            f"- Components: {', '.join(uc['components'])}",
            f"- Acceptance: {'; '.join(uc['acceptance'])}",
        ]
    path = ROOT / "hermes-comprehensive-ai-analyst-synthesis.md"
    path.write_text("\n".join(lines) + "\n")
    return path


def build():
    ART.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)

    rows = clean_vtt(WATCH / "download" / "video.en.vtt")
    evidence = video_evidence(rows)
    hermes_urls = result_urls(read_json(SRC / "you_search_hermes_architecture.json"))
    you_urls = result_urls(read_json(SRC / "you_search_you_api.json"))
    use_cases = build_use_cases()
    synth_path = build_synthesis(use_cases, evidence, hermes_urls, you_urls)

    b = Builder()
    total = 177
    b.total = total

    b.cover(
        "Hermes Agent: Use Cases, Architecture, Integration Realization SOP",
        "A spec-driven implementation guide for building a professional personal-agent operating system from Hermes, GBrain, You.com, skills, cron, profiles, and governed integrations.",
        ["100+ slides", "Source-backed", "SOP format", "Client-ready PPTX"],
    )
    b.content("Executive Answer", "Hermes is not another chat surface; it is a harness that lets a model operate your computer and tools.", "What Changes", ["The value comes from a model wrapped in tools, memory, scheduled jobs, skills, and integrations.", "The practical unit is a repeatable workflow, not an impressive one-off prompt.", "Search, memory, cron, and safe action gates decide whether the agent is useful in real work."], "Implementation Thesis", ["Start with search, memory, cost controls, and security before adding high-autonomy use cases.", "Treat every use case as a mini-product with inputs, outputs, controls, and acceptance criteria.", "Harden skills so they consume and produce artifacts for the next skill in the chain."], "BLUF: Build Hermes as an operating system for recurring professional workflows.")
    b.content("What This Deck Includes", "The deck expands the earlier version into an implementation playbook.", "Included", ["Architecture layers and component model.", "Local file guidance for SOUL.md, USER.md, MEMORY.md, project context, profiles, and role patterns.", "Integration components: You.com, GBrain, Obsidian, browser/computer-use, messaging, MCP, cron, model routing.", f"{len(use_cases)} use cases with spec, architecture, SOP, controls, and acceptance criteria."], "Explicitly Handled", ["The current You.com livecrawl pricing correction.", "The difference between Dmitry's demo setup and this local Hermes instance.", "Why ROLE.md is not a required Hermes standard file here.", "How goal-loop QA prevents isolated skills from doing nothing useful."])
    b.content("Source Pack", "The deck is grounded in concrete artifacts, not generic agent theory.", "Local Sources", ["Hermes setup PDF from Windows Desktop.", "Workshop transcript and YouTube /watch output.", "Local ~/.hermes config, SOUL, USER, MEMORY, cron, and skills.", "Existing You.com plugin and config state."], "Current Discovery", ["You.com search outputs saved as JSON artifacts.", "Official Hermes docs for config, profiles, skills, MCP, cron, and dashboard.", "Official You.com docs for Search, Contents, Research, livecrawl, pricing, and MCP.", "Video frames confirming visible setup and workflow screens."])
    b.content("Skill Chaining QA Result", "The workflow compounded because every stage handed a concrete artifact to the next one.", "Chain Status", ["watch produced transcript, frame evidence, and video-derived workflow details.", "you-com-search produced current source JSON and corrected stale pricing assumptions.", "ai-analyst synthesis converted sources into architecture and use-case specs.", "branded-pptx-deck renders an editable PPTX from the synthesis, with QA artifacts."], "Risk Controlled", ["No API keys or bearer tokens are printed.", "Current-doc pricing caveats replace older unqualified claims.", "Use-case slides separate draft actions from human-approved outbound actions.", "Search-tool dependency policy is included as a use case and governance layer."])

    b.section("SECTION 01", "Hermes Architecture", "The operating model: model + harness + tools + memory + skills + schedules + profiles + governed action.")
    arch = [
        ("Harness", "Wraps a model with tool access, terminal, browser, files, messaging, cron, and skill execution.", "Treat Hermes as the runtime, not the model."),
        ("Model Provider", "OpenRouter/local/OAuth proxy/API providers plus fallback chain and model catalog.", "Route by task cost and reasoning need."),
        ("Terminal Backend", "Local, Docker, SSH, Daytona, Singularity, Modal, or other supported environments.", "Pick by isolation, persistence, and deployment need."),
        ("Web/Search", "Configured local backend: You.com for search; Exa for extraction; You.com Research/Finance for deep tasks.", "Preferred source layer before generic web search."),
        ("Browser", "Headless/controlled browser plus CDP URL for logged-in or private workflows when APIs fail.", "Use APIs first; browser for gaps."),
        ("Computer Use", "Background GUI automation for native apps and real desktop workflows.", "Never click sensitive prompts without approval."),
        ("Memory", "SOUL.md, USER.md, MEMORY.md, state/session search, plus GBrain as graph memory.", "Stable identity plus evolving facts."),
        ("Skills", "Procedural instructions with scripts/assets/templates; agent-created and curated over time.", "Capture repeated workflows."),
        ("Cron", "Scheduled jobs with delivery, model overrides, context chaining, and retry patterns.", "Makes Hermes proactive."),
        ("MCP", "Tool servers like GBrain and ideabrowser extend action surface.", "Health monitor dependencies."),
        ("Messaging", "Telegram, WhatsApp, Discord, Slack, and gateway delivery.", "Interface lives where the user works."),
        ("Profiles", "Separate Hermes homes with config, SOUL, memories, sessions, skills, cron, and gateway state.", "Role isolation and packageability."),
        ("Dashboard/Kanban", "Admin and task surfaces for settings, profile builder, automations, and task routing.", "Turns agent work into visible operations."),
        ("Governance", "Approval, cost, security, source, and skill-chain QA gates.", "Prevents autonomous drift."),
    ]
    for comp, desc, use in arch:
        b.content(f"Architecture Layer: {comp}", use, "What It Does", [desc, "Inputs, outputs, and permissions must be explicit.", "The layer should leave artifacts or logs for audit."], "Implementation Notes", [f"Realization principle: {use}", "Bind this layer to use-case acceptance criteria.", "Add health checks and fallback behavior before relying on it in production."])

    b.section("SECTION 02", "Identity, Memory, Roles", "SOUL.md, USER.md, MEMORY.md, project context, profiles, and role design are the behavior contract.")
    identity_rows = [
        ["SOUL.md", "Identity, tone, values, boundaries", "Loaded early in prompt; stable persona", "Edit intentionally; keep concise"],
        ["USER.md", "User model and operating preferences", "Business context, delivery standards, tool defaults", "Use to guide decisions and pushback"],
        ["MEMORY.md", "Durable facts and environment notes", "Accounts, services, paths, recurrent facts", "Update after durable findings"],
        ["state.db", "Session history and full-text recall", "Past conversations and task trails", "Search, do not stuff everything into prompt"],
        ["GBrain", "Graph and semantic memory", "Entities, relationships, dream cycle", "Use before repeated strategy/research"],
        ["AGENTS.md", "Project workflow rules", "Repo-specific commands and constraints", "Treat as project contract"],
        ["Profiles", "Role/state isolation", "Separate config, keys, SOUL, memory, skills", "Use instead of a monolithic assistant"],
        ["ROLE.md", "Not found as a standard local Hermes file", "Role can be modeled through profiles/SOUL/descriptions", "Do not invent as required unless your org standardizes it"],
    ]
    b.matrix("Memory And Role File Map", "How each file or layer should be used in implementation.", ["Layer", "Purpose", "Where It Applies", "Guideline"], identity_rows)
    b.content("SOUL.md Guidance", "Use SOUL for stable agent identity, not task-specific operating procedures.", "Include", ["Communication style, values, operating boundaries.", "What the agent should refuse or escalate.", "A small number of durable behavior rules.", "Tone and writing constraints that should persist across sessions."], "Avoid", ["Stuffing project-specific SOPs into SOUL.", "Long lists that burn tokens every session.", "Contradicting project AGENTS.md.", "Secrets, API keys, account-specific private data."])
    b.content("USER.md Guidance", "Use USER for the durable user model and delivery standard.", "Local User Model", ["Enterprise solution architect for automotive GenAI POCs.", "Prefers real data, ROI, cost, latency, architecture, and stakeholder-ready decks.", "Dislikes fluff, synthetic data, and over-abstracted solutions.", "Needs mixed-audience communication: business first, technical depth second."], "Implementation Use", ["Inject into POC and deck workflows.", "Let it guide pushback and scope decisions.", "Use it to choose automotive examples.", "Keep it updated when user standards change."])
    b.content("MEMORY.md Guidance", "Use MEMORY for durable operational facts, not long transcripts.", "Good Memory Entries", ["Current accounts, active services, known paths, verified tool state.", "GBrain endpoint and token env-var name, without printing the token.", "Deliverable standards and recurring workflow constraints.", "Environment gotchas that prevent repeated mistakes."], "Bad Memory Entries", ["Raw meeting notes better stored in GBrain or files.", "Secrets or credentials.", "Speculative facts that should expire.", "One-off task details that will not matter again."])
    b.content("Project Context Guidance", "AGENTS.md and project files should carry repo-specific rules.", "Use Project Files For", ["Build commands, test commands, ports, deployment steps.", "Repo-specific skill routing and product build constraints.", "Client-facing PPTX rules and QA expectations.", "Cross-host compatibility maps."], "Keep Separate From", ["Personal style rules in SOUL.", "User identity in USER.", "Durable environment facts in MEMORY.", "Large research artifacts that belong in run folders."])
    b.content("Role Design Without ROLE.md", "No local standard ROLE.md was found; role should be expressed through profiles and SOUL variants.", "Recommended Pattern", ["Create a Hermes profile per role when tools, memory, or personality differ.", "Give each profile a clear description for routing.", "Put role behavior in profile-specific SOUL.md.", "Keep credentials and session history per-machine."], "When ROLE.md Is Useful", ["Only if your organization standardizes it as an internal overlay.", "Document it as custom convention, not required Hermes behavior.", "Do not make skills depend on ROLE.md unless the file is guaranteed."])
    b.content("Profile Packaging", "Profiles are the deployable unit for role-specific assistants.", "Package Includes", ["Config, SOUL, skills, cron jobs, plugins, and MCP connections.", "Role-specific task descriptions and default models.", "Automation blueprints and schedule definitions."], "Keep Local", ["Credentials and API keys.", "Sessions and large state history.", "Personal memories that should not travel.", "Machine-specific paths unless templated."])
    b.content("GBrain As Durable Knowledge Layer", "Use GBrain before repeated strategy, account, entity, or pipeline research.", "Read First", ["Company, person, vertical, use case, account, project, or recurring theme.", "Prior briefs and entity relationships.", "Meeting/transcript-derived facts.", "Known objections and stakeholder preferences."], "Write Back", ["Durable findings likely to matter again.", "Clean entity profiles, not raw dumps.", "Decisions and rationales.", "Source-linked summaries."])
    b.content("Obsidian As Human Inspection Layer", "Obsidian makes the agent's memory visible and editable.", "Use It For", ["Graph visualization of contacts, companies, projects, and relationships.", "Manual correction of misunderstood facts.", "Reviewing what the agent believes before high-stakes work."], "Operating Rule", ["GBrain is the durable memory engine.", "Obsidian is the human-facing inspection and edit surface.", "Every entity note should remain source-readable.", "Corrections should feed back to the agent."])
    b.content("Skills As Procedures, Not Facts", "A skill captures how to do repeatable work.", "Good Skill", ["Clear trigger and scope.", "Required tools and source order.", "Concrete handoff artifact.", "Verification steps and failure modes."], "Anti-Pattern", ["Skill does generic research with no preferred search tool.", "Skill creates a report no downstream step consumes.", "Skill duplicates another skill without added value.", "Skill works only in one host but claims to be global."])
    b.content("Cron As Proactive Work", "Cron turns Hermes from reactive chat into scheduled operations.", "Use Cron For", ["Daily briefs, ingestion, signal monitoring, cost scans, security scans, GBrain dreaming.", "Known periodic outputs with clear delivery channels.", "Jobs that can be verified after each run."], "Do Not Use Cron For", ["Ambiguous goals with no acceptance criteria.", "Actions that require sensitive approvals.", "High-cost loops without budget gates.", "Jobs with no owner or output."])
    b.content("Prompt Context Budget", "Every always-loaded file is a recurring token cost.", "Keep Always-Loaded Files Lean", ["SOUL, USER, MEMORY, and project context should be compact.", "Large evidence belongs in GBrain, run files, or source packs.", "Use skills via progressive disclosure.", "Use retrieval instead of permanent prompt stuffing."], "Review Cadence", ["Monthly memory cleanup.", "Weekly stale skill review if the agent is changing fast.", "Cost scan when adding new cron jobs.", "Security scan when adding new integrations."])
    b.content("Autonomy Ladder", "Every role and use case needs an explicit autonomy level.", "Levels", ["Inform: collect and summarize.", "Recommend: propose actions and rationale.", "Draft: prepare artifacts/messages for review.", "Execute: perform approved reversible actions.", "Operate: recurring autonomous jobs with monitoring."], "Default Stance", ["Outbound messages, purchases, permissions, secrets, destructive file operations, and public posts require approval unless explicitly governed."])

    b.section("SECTION 03", "Integration Components", "The reusable building blocks for implementing Hermes workflows.")
    integrations = [
        ("You.com Search", ["Preferred current web discovery for agent tasks.", "Use freshness, domain targeting, and structured JSON.", "Use before ordinary web search in research skills."], ["Good for source discovery, RAG grounding, current docs, web/news results.", "Save outputs as source artifacts for traceability."]),
        ("You.com Livecrawl / Contents", ["Use when snippets are not enough.", "Current docs say livecrawl is billed separately.", "Prefer Contents API for known URLs."], ["Full-page Markdown/HTML for LLM-ready ingestion.", "Do not use livecrawl blindly on broad queries."]),
        ("You.com Research", ["Use for complex multi-step research questions.", "Returns cited markdown or structured output.", "Still verify high-stakes claims."], ["Good for market scans, content briefs, competitive research, and strategy inputs."]),
        ("You.com Finance Research", ["Use for financial, investor, filings, fundamentals, market data, macro, and diligence workflows.", "Label outputs as research, not advice."], ["Good for investor intelligence and deal preparation."]),
        ("GBrain", ["Graph-like durable memory.", "Dream cycle cleans, links, and reconciles notes.", "Git-backed Markdown keeps memory inspectable."], ["Use for smart contacts, entity recall, account memory, and cross-session strategy."]),
        ("Obsidian", ["Human visual front end for GBrain notes.", "Graph review and manual corrections.", "Useful for entity relationship maps."], ["Keep notes clean and source-linked."]),
        ("Email/Calendar/Slack/Zoom", ["Core private context channels.", "Ingest into staging before writing memory.", "Respect privacy and retention boundaries."], ["Power daily briefs, smart contacts, pre-call prep, and triage."]),
        ("Browser + CDP", ["Use for web apps and logged-in surfaces when APIs are absent.", "Prefer APIs where available.", "Stop at login, 2FA, permission, and payment prompts."], ["Power LinkedIn/Twitter workflows and internal tools."]),
        ("Computer Use", ["Background native GUI automation.", "Capture, act, verify after each state change.", "Useful for desktop apps and non-web systems."], ["Bridge enterprise apps without APIs."]),
        ("Messaging Gateways", ["Telegram, WhatsApp, Discord, Slack.", "Mention-only vs free-response policy.", "Media/artifact delivery."], ["Makes Hermes available from phone and team channels."]),
        ("MCP Servers", ["Extend tool surface through GBrain, IDE, browser, and other servers.", "Health checks and secret redaction matter."], ["Dependency layer for many skills."]),
        ("Cron Scheduler", ["Plain-English schedules and cron expressions.", "Delivery to channels.", "Model and skill overrides."], ["Proactive operations layer."]),
        ("Profiles", ["Role-specific home directories.", "Package config/skills/cron without secrets/history.", "Task routing by profile description."], ["Use for researcher, operator, PM, engineer, social, and sales roles."]),
        ("Model Routing", ["Select model by task type.", "Use fallback providers.", "Monitor drift and cost."], ["Cost control layer."]),
        ("Skill Curator", ["Archive stale skills.", "Consolidate repeated procedures.", "Prevent skill clutter."], ["Keeps agent learnings useful."]),
    ]
    for name, left, right in integrations:
        b.content(f"Integration Component: {name}", "Reusable architecture block for Hermes use-case realization.", "Capabilities", left, "Design Rules", right)

    b.section("SECTION 04", "Official User-Story Catalog", "The official Hermes user-stories page widens the use-case map beyond a single demo setup.")
    b.content("Official User Stories: What They Add", "The user-provided official page is a community catalog, not only a product docs page.", "Use-Case Families", ["Developer workflow and coding automation.", "Personal assistant and life automation.", "Business operations, sales, and marketing.", "Research, content, finance, trading, and market intelligence.", "Enterprise integrations, messaging gateways, privacy, and self-hosting."], "How To Use It", ["Treat each story as a pattern candidate.", "Promote only recurring, high-value patterns into skills or cron.", "Map every story to data sources, tool dependencies, approval gates, and acceptance criteria.", "Do not copy community autonomy levels blindly; apply your own risk model."])
    b.matrix("Official Story Catalog Coverage", "Community patterns from the Hermes user-stories page grouped into build lanes.", ["Lane", "Examples", "Hermes Components", "Control Needed"], [
        ["Developer agents", "Landing page to VPS, GitHub PR flow, repo maintenance, code review", "Terminal, GitHub skills, browser, cron", "Tests, repo diff, approvals"],
        ["Personal ops", "Daily briefs, calendars, reminders, journaling, travel planning", "Memory, cron, gateway, browser", "Privacy and outbound gates"],
        ["Business ops", "Lead gen, email pipelines, investor tracking, dashboards", "You.com, spreadsheets, email, GBrain", "No-auto-send default"],
        ["Content creation", "YouTube research, blog pipeline, UGC ads, podcasts", "watch, You.com Research, CMS, media skills", "Citation and brand QA"],
        ["Research", "Deep research briefs, technical docs, market scans", "You.com Research, Firecrawl, GBrain", "Primary-source tie-out"],
        ["Finance/trading", "Market monitoring, filings, trend signals", "Finance Research, cron, alerts", "No financial-advice claims"],
        ["Enterprise", "Vertex AI, Power Platform, k8s, compliance docs", "MCP, profiles, connectors, docs", "Security review"],
        ["Messaging", "Telegram, Discord, Slack, LINE, QQ, Feishu", "Gateway, channel prompts, media handling", "Channel scope policy"],
        ["Privacy/self-hosted", "SearXNG, Raspberry Pi, local-first memory, VPS agents", "Profiles, local backend, MCP", "Isolation and backups"],
        ["Agent ops", "12 parallel Hermes, runtime monitor, approval audit", "Delegation, cron, dashboards", "Concurrency limits"],
    ])
    b.content("Community Pattern: Self-Hosted Local Agent", "Several stories point to Hermes running beyond a laptop: mini PCs, Raspberry Pi, VPS, and local-first stacks.", "Architecture", ["Profile packaged for target machine.", "Local terminal backend or container backend.", "Messaging gateway for remote access.", "GBrain or file-backed memory with backup policy."], "SOP", ["Start with read-only monitoring jobs.", "Add health and security cron.", "Test recovery after reboot.", "Keep secrets out of packaged profile."])
    b.content("Community Pattern: Developer Workflow Agent", "The official examples reinforce Hermes as a repo-aware coding operator.", "Architecture", ["Repo context files load project conventions.", "Skills capture PR review, issue triage, deployment, and test routines.", "Cron handles recurring dependency/security checks.", "Browser/dogfood validates UI flows."], "SOP", ["Define acceptance command per repo.", "Require diff summary and test output.", "Never auto-merge without policy.", "Record generated skills and stale-skill cleanup."])
    b.content("Community Pattern: Messaging-First Agent", "Many real deployments use chat channels as the front door.", "Architecture", ["Gateway receives messages and media.", "Profile/channel prompt selects scope.", "Run artifacts are stored locally and delivered as links or files.", "Cron can deliver scheduled results to the same channel."], "SOP", ["Set mention-only by default for team channels.", "Define allowed channels and media limits.", "Block secrets in chat.", "Escalate irreversible actions."])
    b.content("Community Pattern: Market And Finance Monitoring", "Trading and market stories should be implemented as research/alerting, not automatic financial action.", "Architecture", ["Finance Research for fundamentals and filings.", "Search/news/social signal monitors for freshness.", "GBrain tracks entities and hypotheses.", "Alerts route to human decision makers."], "SOP", ["Label evidence vs inference.", "Attach dates to all market data.", "Avoid trade execution by default.", "Review false positives weekly."])
    b.content("Community Pattern: Content And Media Factory", "The user-stories page supports content workflows similar to Dmitry's demo blog pipeline.", "Architecture", ["watch/video transcript ingestion.", "You.com Research for source-backed angles.", "Content skills for drafts and variants.", "QA pass for citations, brand, and publish readiness."], "SOP", ["Keep source pack per article.", "Separate ad generation from editorial claims.", "Use publish queue, not direct auto-publish initially.", "Feed performance data back into topic selection."])
    b.content("Community Pattern: Enterprise Integration Agent", "Enterprise stories need stricter architecture than personal productivity stories.", "Architecture", ["Profiles per client/account or role.", "MCP connectors for enterprise systems.", "Project AGENTS.md for account-specific delivery standards.", "Audit logs for access and generated artifacts."], "SOP", ["Start in least-privilege mode.", "Use real data only when approved.", "Keep architecture/cost/security artifacts with every POC.", "Run stakeholder-readiness QA before demos."])
    b.content("Community Pattern: Multi-Agent Operations", "Stories about parallel Hermes instances and runtime monitoring require explicit orchestration.", "Architecture", ["Parent profile routes tasks.", "Child profiles/subagents have bounded tools and depth.", "Goal-loop orchestrator verifies handoffs.", "Dashboard/kanban tracks status."], "SOP", ["Limit concurrency.", "Define consumes/produces for each child.", "Stop duplicate or isolated work.", "Use health monitor and cost monitor before scaling."])
    b.content("Official Stories To Realization Rule", "Every community story must be converted into a build spec before implementation.", "Convert Story Into", ["Business outcome and user.", "Trigger and delivery channel.", "Data sources and integration components.", "Autonomy level and approval gates.", "Acceptance criteria and verification artifacts."], "Reject Or Defer When", ["No owner or repeated need.", "No safe source/tool path.", "Output is not used by any downstream workflow.", "Cost, privacy, or account risk is not bounded."])

    b.section("SECTION 05", "Implementation SOP", "Spec-driven delivery pattern for every Hermes use case.")
    sop_slides = [
        ("Use-Case Spec Template", ["Name the business outcome, not just the automation.", "Define trigger, user, output, autonomy level, data sources, delivery channel, and KPI.", "State what the agent must never do without approval.", "List source and verification requirements."], ["Spec file", "Input inventory", "Acceptance criteria", "Owner and review cadence"]),
        ("Architecture Template", ["Draw the data path: trigger -> retrieval -> memory -> reasoning -> action -> delivery -> logging.", "Separate private data, public research, durable memory, and generated artifacts.", "Declare model route and fallback.", "Declare search-tool preference order."], ["Component diagram", "Integration list", "Trust boundaries", "Failure handling"]),
        ("Search Policy", ["You.com Search/Research/Finance first when current web or finance research matters.", "Exa/Firecrawl/Contents for discovery or full-page ingestion when appropriate.", "Reddit tools for buyer language and community evidence.", "Generic web search is fallback/source discovery only."], ["Search run JSON", "Source pack", "Citation map", "Rejected-source notes"]),
        ("Memory Policy", ["GBrain recall before recurring person/company/account/use-case research.", "Write back durable findings after strategy or pipeline work.", "Keep raw evidence in files; keep distilled facts in memory.", "Use Obsidian for human inspection."], ["Recall summary", "Write-back note", "Entity updates", "Conflict list"]),
        ("Action Gates", ["Draft before send for email, social, investor, and public posting.", "Ask before payments, permissions, destructive changes, secrets, or risky browser prompts.", "Use separate profile/device for early experiments.", "Log human approvals."], ["Approval record", "Risk label", "Rollback plan", "Audit log"]),
        ("Cost Controls", ["Route by activity and model tier.", "Budget every recurring job.", "Scan logs for runaway processes and wrong-model use.", "Prefer smaller models for parsing/summarization."], ["Budget table", "Spend dashboard", "Model route log", "Savings notes"]),
        ("Skill Chaining QA", ["Every skill must consume an artifact and produce an artifact.", "The next skill must actually use the output.", "Remove isolated or duplicate skills.", "Run pass-level chaining checks after each loop."], ["Chain contract", "Handoff file", "QA status", "Reroute decision"]),
        ("Verification", ["Decks need PPTX validation and visual QA.", "Automations need run logs and acceptance checks.", "Research needs source tie-out.", "Browser/computer tasks need screenshot or state evidence."], ["QA handoff", "Preview images", "Test output", "Known caveats"]),
        ("Rollout", ["Start with inform/recommend workflows.", "Add draft workflows after trust is established.", "Add execute/operate only with metrics, rollback, and monitoring.", "Review cron, skills, memory, and permissions monthly."], ["Pilot scope", "Metrics", "Review schedule", "Decommission rule"]),
    ]
    for title, left, right in sop_slides:
        b.content(title, "Use this gate before shipping any Hermes workflow.", "Operator Checklist", left, "Required Artifact", right)

    b.section("SECTION 06", "Use-Case Realization Catalog", "Each use case has a spec slide, architecture slide, and SOP/control slide.")
    for idx, uc in enumerate(use_cases, 1):
        b.usecase_spec(uc, idx)
        b.usecase_arch(uc, idx)
        b.usecase_sop(uc, idx)

    b.section("SECTION 07", "Rollout Roadmap", "A practical path from installed Hermes to a governed personal-agent operating system.")
    roadmap = [
        ("Day 0-7: Foundation", ["Install Hermes and verify model provider.", "Configure You.com search and extraction policy.", "Set SOUL.md, USER.md, MEMORY.md, and project context.", "Enable GBrain and Obsidian if memory graph is required."], ["Hermes launches", "Search smoke test passes", "No secrets printed", "Profile baseline saved"]),
        ("Day 8-14: Safety And Cost", ["Create activity-dependent model routing.", "Add cost scan and security audit cron jobs.", "Inventory MCP servers and plugins.", "Define approval gates."], ["Budget thresholds", "Risk report", "Health report", "Approval policy"]),
        ("Day 15-30: Core Productivity", ["Build daily brief.", "Build pre-call account brief.", "Build smart contacts ingestion.", "Create relationship nudge workflow."], ["Daily brief delivered", "Entity profiles created", "Meeting prep accepted", "Nudge feedback logged"]),
        ("Day 31-45: Research And Content", ["Add signal monitor.", "Add YouTube watch research job.", "Add deep market research workflow.", "Add content/AEO variant pipeline."], ["Source packs saved", "Citations verified", "Draft queue created", "Performance metrics planned"]),
        ("Day 46-60: Outreach And Growth", ["Add investor intelligence tracker.", "Add LinkedIn/X engagement queue.", "Add finance research mode for diligence.", "Keep no-auto-send default."], ["Tracker populated", "Drafts queued", "Human approval workflow", "Response tracking"]),
        ("Day 61-75: Team/Profiles", ["Create role profiles.", "Package shared skills and cron jobs.", "Expose shared GBrain where appropriate.", "Add kanban/task routing."], ["Role profiles tested", "Secrets local only", "Tasks route correctly", "Access policy documented"]),
        ("Day 76-90: Enterprise POC Factory", ["Specialize for automotive accounts.", "Create demo/architecture/cost/deck pipeline.", "Add draw.io and branded PPTX requirements.", "Run stakeholder readiness QA."], ["Real-data demo", "Architecture diagram", "Cost model", "Business-story deck"]),
        ("Operating Cadence", ["Daily: brief, ingest, signal scan.", "Weekly: skill curator, cost review, memory dream review.", "Monthly: security, profile, and permission review.", "Quarterly: use-case ROI review."], ["Run logs", "Savings estimate", "Skill catalog", "Decommission list"]),
    ]
    for title, left, right in roadmap:
        b.content(title, "Rollout plan with acceptance criteria.", "Actions", left, "Done Means", right)

    out = ART / "Hermes_Comprehensive_Use_Cases_Architecture_SOP-reviewed.pptx"
    b.d.save(out)
    print(f"SYNTHESIS={synth_path}")
    print(f"PPTX={out}")
    print(f"SLIDES={b.d.n}")


if __name__ == "__main__":
    build()
