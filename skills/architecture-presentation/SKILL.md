---
name: architecture-presentation
description: Use when the user wants to document, present, or teach any software architecture or system design — phrases like "document the X architecture", "create a presentation for X", "turn this architecture into slides", "run the architecture pipeline for X". Produces a draw.io diagram, a markdown explanation doc, a 10-slide pptx deck (Enterprise Consulting theme), and NotebookLM steps. Invoked as sub-task by architecture-to-everything.
---

# Architecture Presentation Pipeline Skill

Run three tools in sequence to produce a complete, professional architecture package:

| Step | Tool | Output |
|------|------|--------|
| 1 | `drawio` skill | `.drawio` diagram file |
| 2 | Markdown doc | `<name>-architecture.md` explanation doc |
| 3 | `pptx` skill | `.pptx` slide deck — Enterprise Consulting theme |
| 4 | `notebooklm` skill | NotebookLM notebook with Briefing Doc |

---

## When to use this skill

Trigger when the user says:
- "Document the X architecture"
- "Create a presentation for X"
- "Turn this architecture into slides and a notebook"
- "Run the architecture pipeline for X"

---

## Step 1 — draw.io Diagram

Invoke the `drawio` skill.

**Diagram style for architecture (component-flow style, NOT swimlanes):**
- White background, clean layout
- Labelled component boxes with light gray or colored borders
- Numbered circles on arrows to show sequence
- Hierarchical left-to-right OR top-to-bottom flow
- Group related components in light-fill zones (no heavy swimlane headers)
- File: `<working-dir>/<name>-architecture.drawio`

See `drawio` skill for full XML reference.

---

## Step 2 — Architecture Explanation Doc

Write a structured `.md` file with these sections:

```markdown
# <System Name> — Architecture Guide

## What is <System Name>?
One paragraph, plain English.

---

## Architecture Overview
Brief list of all layers/components.

---

## Component: <Name>
What it does, why it exists, key sub-components as bullet points.

[... repeat for each major component ...]

---

## Key Data Flows
### A typical <action>
Numbered 1–N steps showing how a request moves through the system.

---

## Design Decisions
- **Decision**: Why it was made this way
[3–4 key design decisions]
```

File: `<working-dir>/<name>-architecture.md`

---

## Step 3 — pptx Slide Deck

Invoke the `pptx` skill (use `pptxgenjs.md` — create from scratch).

### Theme: Enterprise Consulting + Document Standards
*Best of two reference sources: SAP/consulting deck visual impact + AI Guidelines PDF structured hierarchy*

**Color Palette:**
```
WHITE      = 'FFFFFF'   // slide background — ALL slides white, no dark backgrounds
CHARCOAL   = '1A1A1A'   // primary body text
NAVY_DEEP  = '1F3B6E'   // section headers, dominant accent (from AI Guidelines PDF)
NAVY_CARD  = '0D3B5E'   // card header bands, bottom banners (from SAP deck)
RED        = 'E31837'   // sparingly — key metrics, active/highlighted cells, CTAs
LIGHT_BG   = 'F5F7FA'   // subtle card fill, code block backgrounds
BORDER     = 'D0D5DD'   // card/table borders
MUTED      = '6B7280'   // captions, secondary text
CODE_BG    = 'F0F2F5'   // monospace code/template block background
```

**Two-accent system:**
- **NAVY_DEEP** (`1F3B6E`) = the dominant accent. Use for slide titles, section headers, numbered labels, card headers. This is the primary visual colour.
- **RED** (`E31837`) = the power accent. Use SPARINGLY — only for the single most important element per slide (a metric, the "winner" column in a comparison, a CTA button).

**Typography:**
```
Slide title:     Calibri Bold, 36–40pt, left-aligned, color=NAVY_DEEP
Section header:  Calibri Bold, 20–24pt, left-aligned, color=NAVY_DEEP
Body text:       Calibri, 13–15pt, color=CHARCOAL
Caption/label:   Calibri Light, 11pt, color=MUTED
Code/template:   Courier New or Consolas, 11pt, color=CHARCOAL, bg=CODE_BG
Metric callout:  Calibri Bold, 60–80pt, color=RED
```

**Design Rules:**
- ALL slides use white background — NO dark backgrounds
- NAVY_DEEP for all titles and section headers (not black, not red)
- RED only for the single most impactful element per slide
- Left-align ALL text (never center body text — center only bottom banners)
- Card border: 1pt, BORDER color. Card header band: NAVY_CARD fill, WHITE text
- Code/template blocks: CODE_BG fill, 0.1" padding, monospace font, 1pt BORDER
- Section hierarchy on slides: Title (NAVY_DEEP, 38pt) → Section label (NAVY_DEEP, 20pt bold) → Body (CHARCOAL, 14pt) → Code block (CODE_BG)
- Never add accent lines under titles — use whitespace or a 0.06" top-margin gap
- Minimum 0.5" slide margins, 0.3" gaps between content blocks

### Standard 10-Slide Structure

| # | Slide | Layout | Key elements |
|---|-------|--------|--------------|
| 1 | **Title** | White, content left 60% + image/icon right 40% | NAVY_DEEP bold title (38pt), charcoal subtitle, small RED tagline pill |
| 2 | **What is it?** | White, 3-column icon cards | One-line NAVY summary, 3 bordered cards: NAVY_CARD header band + body text |
| 3 | **The Problem** | White, top flow diagram + 3 problem cards | Left-to-right flow boxes (light borders) + 3 cards below with bold NAVY_DEEP header |
| 4 | **Architecture Overview** | White, component diagram (65%) + numbered step list (35%) | Diagram with numbered RED circles on arrows; right panel: "N-Step Flow" numbered list, NAVY_DEEP headers |
| 5 | **Components Deep Dive** | White, 2×2 card grid | 4 cards: NAVY_CARD header band (white text) + Calibri 13pt body |
| 6 | **Comparison / Decision Matrix** | White, comparison table | Row headers in NAVY_DEEP bold; "winner" column highlighted RED fill; other columns light gray |
| 7 | **Implementation / Code View** | White, left explanation + right code block | Left: NAVY_DEEP section header + bullets. Right: CODE_BG block, monospace, template/pseudocode |
| 8 | **Key Metrics / Results** | White, left diagram + right 3 large stats | Stats: 60–80pt Calibri Bold in RED, descriptor 14pt CHARCOAL below each |
| 9 | **Key Data Flow** | White, numbered horizontal timeline | 5–7 steps as boxes in a left-to-right row; step numbers in NAVY_DEEP circles |
| 10 | **Summary / CTA** | White, 3 takeaway cards + NAVY_CARD bottom banner | Cards: NAVY_DEEP bold header + body. Banner: "Your one-sentence key message here." |

### pptxgenjs Helper Functions to Implement

```js
const C = {
  WHITE: 'FFFFFF', CHARCOAL: '1A1A1A', NAVY_DEEP: '1F3B6E',
  NAVY_CARD: '0D3B5E', RED: 'E31837', LIGHT_BG: 'F5F7FA',
  BORDER: 'D0D5DD', MUTED: '6B7280', CODE_BG: 'F0F2F5'
};

// Card with NAVY_CARD header band
function addCard(slide, x, y, w, h, header, body, opts={}) {
  slide.addShape(pptx.ShapeType.rect, {x, y, w, h,
    line: {color: C.BORDER, width: 1}, fill: {color: opts.fill || C.WHITE}});
  if (header) {
    slide.addShape(pptx.ShapeType.rect, {x, y, w, h: 0.38,
      fill: {color: C.NAVY_CARD}, line: {color: C.NAVY_CARD, width: 0}});
    slide.addText(header, {x: x+0.12, y: y+0.06, w: w-0.24, h: 0.28,
      fontSize: 12, bold: true, color: C.WHITE, fontFace: 'Calibri'});
  }
  slide.addText(body, {x: x+0.12, y: y+(header?0.44:0.12), w: w-0.24,
    h: h-(header?0.56:0.24), fontSize: 12, color: C.CHARCOAL,
    fontFace: 'Calibri', valign: 'top', wrap: true});
}

// Large RED metric callout
function addMetric(slide, x, y, w, value, label) {
  slide.addText(value, {x, y, w, h: 1.1, fontSize: 72, bold: true,
    color: C.RED, fontFace: 'Calibri', align: 'left'});
  slide.addText(label, {x, y: y+1.0, w, h: 0.5, fontSize: 13,
    color: C.CHARCOAL, fontFace: 'Calibri', align: 'left'});
}

// Code / template block (from AI Guidelines PDF style)
function addCodeBlock(slide, x, y, w, h, code) {
  slide.addShape(pptx.ShapeType.rect, {x, y, w, h,
    fill: {color: C.CODE_BG}, line: {color: C.BORDER, width: 1}});
  slide.addText(code, {x: x+0.12, y: y+0.1, w: w-0.24, h: h-0.2,
    fontSize: 11, color: C.CHARCOAL, fontFace: 'Courier New',
    valign: 'top', wrap: true});
}

// Comparison table row (highlight winner column in RED)
function addTableRow(slide, x, y, w, rowH, cols, highlightCol=null) {
  const colW = w / cols.length;
  cols.forEach((text, i) => {
    const fill = (i === highlightCol) ? 'FEE2E2' : (i===0 ? C.LIGHT_BG : C.WHITE);
    const textColor = (i === highlightCol) ? C.RED : C.CHARCOAL;
    slide.addShape(pptx.ShapeType.rect, {x: x+i*colW, y, w: colW, h: rowH,
      fill: {color: fill}, line: {color: C.BORDER, width: 0.5}});
    slide.addText(text, {x: x+i*colW+0.1, y: y+0.05, w: colW-0.2, h: rowH-0.1,
      fontSize: 12, color: textColor, fontFace: 'Calibri',
      bold: (i===0), valign: 'middle', wrap: true});
  });
}

// Bottom banner (NAVY_CARD bar)
function addBanner(slide, text) {
  slide.addShape(pptx.ShapeType.rect, {x: 0, y: 6.8, w: 17.78, h: 0.7,
    fill: {color: C.NAVY_CARD}, line: {color: C.NAVY_CARD, width: 0}});
  slide.addText(text, {x: 0.4, y: 6.85, w: 17.0, h: 0.6,
    fontSize: 15, bold: true, color: C.WHITE, fontFace: 'Calibri',
    align: 'center', valign: 'middle'});
}

// Section title (NAVY_DEEP, 38pt, left-aligned)
function addTitle(slide, text, subtitle='') {
  slide.addText(text, {x: 0.5, y: 0.25, w: 16.78, h: 0.7,
    fontSize: 38, bold: true, color: C.NAVY_DEEP, fontFace: 'Calibri'});
  if (subtitle) slide.addText(subtitle, {x: 0.5, y: 0.9, w: 16.78, h: 0.4,
    fontSize: 15, color: C.MUTED, fontFace: 'Calibri'});
}
```

File: `<working-dir>/<name>-architecture.pptx`
**After generating:** Run visual QA — convert to images and inspect for overlap, overflow, contrast.

---

## Step 4 — NotebookLM Notebook

Invoke the `notebooklm` skill.

**⚠️ Chrome MCP Domain Restriction:** The MCP cannot auto-navigate to notebooklm.google.com. Give the user these manual steps:

1. Open Chrome → **https://notebooklm.google.com**
2. Click **"New notebook"** → name it `"<System Name> Architecture"`
3. **"Add source"** → **"Upload file"** → select `<name>-architecture.md`
4. Wait for spinner (~30 sec)
5. Click **"Notebook guide"** → **"Briefing doc"**

Tell the user they can ask questions like:
- "What is the role of [component]?"
- "Explain the data flow for [action]"
- "What are the key design decisions?"

---

## Completion Checklist

- [ ] `<name>-architecture.drawio` — component-flow diagram written
- [ ] `<name>-architecture.md` — explanation doc written
- [ ] `<name>-architecture.pptx` — Enterprise Consulting theme deck generated + opened
- [ ] NotebookLM steps given to user (or notebook created if MCP allows)

---

## Example usage

```
User: "Document the Stripe payment architecture for our team"

You:
1. Run drawio skill → stripe-architecture.drawio (component-flow, left-to-right)
2. Write stripe-architecture.md (payment flow, webhook system, API layers)
3. Run pptx skill → stripe-architecture.pptx (10 slides, Enterprise Consulting theme)
4. Give NotebookLM manual steps with the .md file path
```

---

## Mistakes to avoid

- Do NOT use dark backgrounds (no Midnight Executive) — Enterprise Consulting is all white
- Do NOT use blue as the accent — RED is the single accent color
- Do NOT use swimlanes in draw.io for architecture — use component-flow boxes with arrows
- Do NOT skip the explanation `.md` doc — it feeds NotebookLM AND informs the pptx narrative
- Do NOT use Excalidraw — use draw.io (per project memory)
- Do NOT generate audio overview in NotebookLM unless user explicitly asks
- Do NOT center body text — left-align everything except banners
- Do NOT add accent lines under slide titles — use whitespace instead

---

## Skill Relationships

### Category
Business Automation

### Dependencies
- `drawio` — Stage 1 diagram generation (must be installed)
- `notebooklm` — Stage 4 notebook (manual fallback always available)

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `architecture-to-everything` | Orchestrated by | when run as Stage 2 of the full pipeline | receives system description + `.drawio` path from Stage 1 |
| `drawio` | Sequential upstream | always (Step 1) | `<name>-architecture.drawio` |
| `notebooklm` | Sequential downstream | Step 4, after `.md` doc is written | `<name>-architecture.md` (uploaded as source) |
| `workflow-visualizer` | Domain cluster | same system input, interactive HTML variant | — |
| `drawio` | Domain cluster | same diagram domain | — |

### Runtime Preamble
At invocation:
- "I'll produce 4 outputs: draw.io diagram → architecture doc (.md) → 10-slide pptx deck → NotebookLM steps."
- "Note: NotebookLM requires a manual Chrome step — I'll give you exact instructions."
- "If you already have a `.drawio` file, tell me and I'll skip Step 1."

---

## Gotchas

- **NotebookLM is not automatable via Chrome MCP:** The `mcp__Claude_in_Chrome__navigate` tool cannot reach `notebooklm.google.com`. Always fall back to the manual 5-step instructions in Step 4 — never silently skip.
- **The `.md` doc must be written before the pptx:** The pptx narrative draws directly from the markdown structure. Writing them in reverse order produces a weaker deck.
- **Enterprise Consulting theme = white backgrounds only:** No dark slides, no Midnight Executive. If a user asks for dark, decline and explain the constraint.
- **Component-flow diagrams only in draw.io:** Swimlane diagrams look wrong for architecture. Use labeled component boxes with numbered arrows — see `drawio` skill reference.
- **Run visual QA on the pptx:** After generation, convert to images and inspect for overflow, clipped text, and color contrast issues before delivering.

## Shared PPTX Visual Contract

Before building the architecture PPTX, read `pptx-visual-spec`, write and validate
`<run>/visual-spec.json`, and classify every diagram region. New architecture and data-flow
content defaults to native editable PowerPoint or deterministic Draw.io/SVG source; exact
supplied system screenshots/figures route to extraction. Architecture, labels, claims, and
technical diagrams never route to an image model.
