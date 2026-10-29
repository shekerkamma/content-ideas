---
name: daily-reporter
description: "Compile daily content pipeline results into Google Sheets and send email digest summary."
user-invocable: false
allowed-tools: Bash, Read, Write, Edit, Agent, WebFetch, WebSearch
---

# Daily Reporter Agent

Aggregates all agent outputs into a structured Google Sheet and sends a
morning email digest with the day's content recommendations.

## Inputs

- `outliers.json` — from Trend Scout
- `script.md` — from Script Writer
- `thumbnail-analysis.md` — from Thumbnail Designer
- `config.json` — Google Sheet ID, email recipient, credentials
- Google Sheets API credentials + Gmail API credentials

## Process

### Step 1: Update Google Sheet

Use Google Sheets API to update the master content sheet.

```bash
# Authenticate with service account
export GOOGLE_APPLICATION_CREDENTIALS="[path from config]"
```

#### Tab 1: Daily Outliers

Append rows to the "Daily Outliers" tab:

| Date | Platform | Channel | Subs | Title | Views | Outlier Score | Engagement % | Hook Formula | URL | Thumbnail |
|------|----------|---------|------|-------|-------|---------------|-------------|--------------|-----|-----------|

One row per outlier video/post from today's `outliers.json`.

```python
# Use Google Sheets API v4
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_service_account_file(CREDS_PATH, scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

values = [[date, platform, channel, subs, title, views, score, engagement, hook, url, thumb]
          for outlier in outliers]

service.spreadsheets().values().append(
    spreadsheetId=SHEET_ID,
    range='Daily Outliers!A:K',
    valueInputOption='USER_ENTERED',
    body={'values': values}
).execute()
```

#### Tab 2: Content Calendar

Append today's content recommendation:

| Date | Topic | Title (★) | Script Status | Thumbnail Status | Video Status | Upload Status |
|------|-------|-----------|---------------|-----------------|-------------|--------------|

Mark statuses as: Draft / Ready / Approved / Published

#### Tab 3: Competitor Tracker

Update competitor channel stats (weekly, from Channel Analyst):

| Channel | Subs | Avg Views | Videos This Week | Top Video | Outlier Score |
|---------|------|-----------|-----------------|-----------|---------------|

#### Tab 4: Brand Voice Log

Track brand voice evolution and refinements:

| Date | Update Type | What Changed | Trigger |
|------|-------------|-------------|---------|

### Step 2: Generate Dashboard View

Create or update a summary dashboard tab with:
- **Today's top outlier** — title, channel, score, link
- **Recommended topic** — from Trend Scout's top recommendation
- **Script status** — draft ready / needs review
- **Thumbnail status** — 3 variants generated / pending
- **Weekly stats** — outliers found this week, scripts written, videos posted

### Step 3: Send Email Digest

Compose and send via Gmail API:

```python
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file(GMAIL_CREDS_PATH)
service = build('gmail', 'v1', credentials=creds)

msg = MIMEMultipart('alternative')
msg['Subject'] = f"🎬 AI Daily Digest — {date}"
msg['To'] = config['email_recipient']
msg['From'] = 'me'

html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
  <h1 style="color: {brand_colors[0]};">Daily Content Digest</h1>
  <p style="color: #666;">{date}</p>

  <h2>Top Outlier Videos</h2>
  <table style="width: 100%; border-collapse: collapse;">
    <tr style="background: {brand_colors[2]};">
      <th>Channel</th><th>Title</th><th>Score</th>
    </tr>
    <!-- Top 5 outliers as rows -->
  </table>

  <h2>Today's Recommended Topic</h2>
  <p><strong>{top_recommendation['topic']}</strong></p>
  <p>{top_recommendation['why']}</p>
  <p>Suggested angle: {top_recommendation['suggested_angle']}</p>

  <h2>Script Draft</h2>
  <p><strong>Title:</strong> {recommended_title}</p>
  <p><strong>Hook:</strong> {recommended_hook}</p>
  <p><a href="[google sheet link]">View full script in Google Sheet →</a></p>

  <h2>Thumbnails</h2>
  <p>3 variants generated — review in the dashboard.</p>

  <hr>
  <p style="color: #999; font-size: 12px;">
    <a href="[google sheet link]">Open Full Dashboard</a>
  </p>
</body>
</html>
"""

msg.attach(MIMEText(html_body, 'html'))

raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
service.users().messages().send(userId='me', body={'raw': raw}).execute()
```

### Step 4: Save Local Report

Write `~/social-media-content/YYYY-MM-DD/report.md`:

```markdown
# Daily Content Report — YYYY-MM-DD

## Pipeline Status
- [x] Trend Scout: X outliers found (Y YouTube, Z X)
- [x] Script Writer: draft ready for "[title]"
- [x] Thumbnail Designer: 3 variants generated
- [ ] Video Editor: awaiting footage
- [x] Google Sheet: updated
- [x] Email digest: sent to [email]

## Top 5 Outliers
| # | Channel | Title | Score | Platform |
|---|---------|-------|-------|----------|

## Recommended Content
- **Topic**: ...
- **Title**: ...
- **Why now**: ...

## Actions Needed
1. Review script draft → [link]
2. Choose thumbnail variant → [folder]
3. Record video when ready
```

## Fallbacks

- If Google Sheets API fails → save data as local CSV
- If Gmail API fails → save digest as local HTML + notify in terminal
- If partial data (e.g., no script yet) → send what's available, mark missing items
