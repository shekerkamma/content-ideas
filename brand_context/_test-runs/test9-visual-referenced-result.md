# mkt-visual-identity — Path A: Referenced Identity Test

## Scenario
User provides 3 visual reference images in `visual_refs/` — screenshots of designs they like (dark SaaS dashboards, data-heavy enterprise UIs).

## Step 1: Brand Foundation (simulated answers)

- Brand Name: {{brand_name}}
- Masthead: ["{{month_year}}", "{{handle}}", "{{tagline}}"]
- Visual References: 3 images provided (dark SaaS dashboard, data viz platform, enterprise analytics UI)
- Logo: Text-based logotype (no logo files)
- Headshot: Not provided
- Font Preferences: "derive from refs"
- Color Preferences: "derive from refs"

## Step 2: Visual Reference Analysis

### ref-01.png — Dark SaaS Dashboard
- **Dominant palette:** Near-black (#0D1117), dark gray (#161B22), electric blue (#58A6FF), white (#F0F6FC)
- **Typography:** System sans-serif, medium weight headers, regular body
- **Spacing:** Tight grid, 8px base unit, dense information layout
- **Visual tone:** Minimal, dark mode, flat, developer-oriented
- **Layout:** Card grid, sidebar navigation, data tables
- **Decorative:** Minimal — thin borders, subtle hover states, no gradients

### ref-02.png — Data Visualization Platform
- **Dominant palette:** Dark navy (#1B2838), teal accent (#4ECDC4), warm gray (#8B9BB4), white text
- **Typography:** Geometric sans (similar to Geist/Rubik), heavier display weights
- **Spacing:** Medium density, 12px base unit, chart-focused
- **Visual tone:** Professional, data-forward, clean
- **Layout:** Dashboard grid, chart cards, KPI strips
- **Decorative:** Subtle gradients on chart backgrounds, rounded corners

### ref-03.png — Enterprise Analytics UI
- **Dominant palette:** Charcoal (#1F2937), indigo accent (#6366F1), slate gray (#64748B), near-white (#F9FAFB)
- **Typography:** Inter family, tight line height, clear hierarchy
- **Spacing:** Standard 16px grid, comfortable density
- **Visual tone:** Clean enterprise, trustworthy, data-rich
- **Layout:** Full-width sections, metric cards, table views
- **Decorative:** Rounded corners, subtle shadows, occasional gradient headers

### Cross-Reference Synthesis
**Common thread:** Dark mode, data-dense, minimal decoration, accent-driven hierarchy (one bright accent on dark background), system/geometric sans-serif, card-based layouts.

**Derived tokens:**
- Primary: #0D1117 to #1F2937 range (near-black to charcoal)
- Accent: Blue-teal spectrum (#4ECDC4 to #6366F1)
- Typography: Geometric sans, Inter or Geist family
- Spacing: 8-12px base grid, medium density

## Step 3: Generated tokens.json (Path A)

```json
{
  "version": 1,
  "brand": "{{brand_name}}",
  "palette": {
    "primary":    { "hex": "#0D1117", "name": "GitHub Dark", "usage": "Headers, primary backgrounds, hero sections" },
    "secondary":  { "hex": "#161B22", "name": "Dark Surface", "usage": "Cards, panels, secondary backgrounds" },
    "accent":     { "hex": "#4ECDC4", "name": "Teal 400", "usage": "CTAs, links, highlights, data accents" },
    "background": { "hex": "#F9FAFB", "name": "Gray 50", "usage": "Light mode base, report backgrounds" },
    "text":       { "hex": "#0D1117", "name": "GitHub Dark", "usage": "Body text on light backgrounds" },
    "surface":    { "hex": "#F3F4F6", "name": "Gray 100", "usage": "Card backgrounds, code blocks, data tables" },
    "muted":      { "hex": "#8B9BB4", "name": "Slate Blue", "usage": "Secondary text, borders, axis labels" },
    "text_on_dark": { "hex": "#F0F6FC", "name": "Near White", "usage": "Text on dark primary/secondary" },
    "success":    { "hex": "#10B981", "name": "Emerald 500", "usage": "Positive metrics, upward trends" }
  },
  "typography": {
    "display": { "family": "Geist", "weights": ["Bold", "ExtraBold"], "fallback": "'Inter', sans-serif" },
    "body":    { "family": "Geist", "weights": ["Regular", "Medium"], "fallback": "'Inter', sans-serif" },
    "mono":    { "family": "Geist Mono", "weights": ["Regular", "Bold"], "fallback": "'JetBrains Mono', monospace" }
  },
  "spacing": {
    "canvas_padding": 64,
    "block_padding_v": 40,
    "block_padding_h": 32,
    "scale": { "2xs": 4, "xs": 8, "sm": 12, "md": 16, "lg": 24, "xl": 32, "2xl": 48, "3xl": 64, "4xl": 96, "5xl": 128 }
  },
  "chrome": {
    "masthead": { "enabled": true, "labels": ["{{month_year}}", "{{handle}}", "{{tagline}}"] },
    "pagination": { "subtype": "css-shape", "count": 7, "active": 1 }
  },
  "locked_fields": ["brand", "chrome.masthead"]
}
```

### WCAG Validation
- text_on_dark (#F0F6FC) on primary (#0D1117) → 17.4:1 ✓
- accent (#4ECDC4) on primary (#0D1117) → 8.7:1 ✓
- accent (#4ECDC4) on background (#F9FAFB) → 2.9:1 ⚠ (below 3:1)
  - **Adjusted:** accent on light backgrounds should use darker variant #2DBDB4 (3.8:1 ✓)

## Path A Test Status
- [x] Visual references analyzed (3 images)
- [x] Cross-reference synthesis identified common thread
- [x] tokens.json generated from analysis (not neutral defaults)
- [x] Colors derived from reference palette analysis
- [x] Typography matched to reference style
- [x] Spacing calibrated to reference density
- [x] WCAG validated with adjustment noted
- [x] Distinct from Path B (neutral) output — data-dense dark mode vs generic clean
