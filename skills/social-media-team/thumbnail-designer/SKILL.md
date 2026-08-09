---
name: thumbnail-designer
description: "Reference trending thumbnails and generate custom versions using NanoBanana Pro — 3 variants per video."
user-invocable: false
allowed-tools: Bash, Read, Write, Edit, Agent, WebFetch, WebSearch
---

# Thumbnail Designer Agent

Analyzes outlier video thumbnails for patterns, then generates 3 custom thumbnail
variants using NanoBanana Pro — one reference-inspired and two unique to your brand.

## Inputs

- `outliers.json` — outlier videos with thumbnail URLs from Trend Scout
- `script.md` — today's script with title and thumbnail brief from Script Writer
- `config.json` — brand colors, brand font, profile photos
- NanoBanana Pro API key from `.env`

## Process

### Step 1: Thumbnail Pattern Analysis

For the top 5 outlier videos, analyze their thumbnails:

Use WebFetch to grab thumbnail images from YouTube:
```
https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg
```

For each thumbnail, analyze (using Claude Vision):
- **Layout**: face position (left/right/center), text position, background
- **Text overlay**: what text is on the thumbnail, font size, color
- **Face expression**: surprised, confident, pointing, serious, excited
- **Color scheme**: dominant colors, contrast level
- **Props/graphics**: arrows, circles, icons, screenshots, logos
- **Emotional trigger**: curiosity, fear, excitement, authority

Produce a pattern summary:
```markdown
## Thumbnail Patterns (Today's Outliers)

### Winning Patterns
- [Pattern 1]: e.g., "Large face left + 3-4 word text right + contrasting background"
- [Pattern 2]: e.g., "Split screen before/after + shocked expression"
- [Pattern 3]: e.g., "Tool screenshot + arrow pointing to result"

### Color Trends
- Most common: [colors]
- Highest-performing: [colors with best outlier scores]

### Text Overlay Trends
- Average word count: X
- Most effective: [short punchy phrases]
```

### Step 2: Generate 3 Thumbnail Variants

#### Variant 1: Reference-Inspired
- Based on the highest-scoring outlier's thumbnail pattern
- Same layout/composition but with YOUR face, YOUR brand colors, YOUR title
- This is the "proven formula" variant

#### Variant 2: Brand-Native
- Uses your established brand aesthetic (colors, font from config)
- Your photo + clean text overlay
- Designed to be consistent with your channel's visual identity

#### Variant 3: Pattern-Break
- Deliberately different from typical thumbnails in the niche
- Bold, unexpected visual that stands out in a feed of similar thumbnails
- Still uses your brand colors but breaks the layout convention

### Step 3: Generate with NanoBanana Pro

For each variant, construct a prompt for NanoBanana Pro API:

```bash
curl -X POST "https://api.nanobanana.com/v1/generate" \
  -H "Authorization: Bearer $NANOBANANA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "[detailed thumbnail description]",
    "width": 1280,
    "height": 720,
    "style": "photorealistic",
    "reference_image": "[profile photo path or URL]",
    "text_overlay": {
      "text": "[title text for thumbnail]",
      "font": "[brand font]",
      "color": "[brand color]",
      "position": "[top-right / bottom-left / center]"
    }
  }'
```

**Note**: If NanoBanana Pro API is unavailable or the endpoint differs,
adapt the API call based on their current documentation. Use WebFetch to
check `https://docs.nanobanana.com/api` for the latest endpoints.

If NanoBanana Pro API fails entirely, fall back to generating a detailed
thumbnail brief as text that the user can execute manually in NanoBanana's UI.

### Step 4: Composite with Profile Photo

After generating the background/graphic:
- Overlay the user's profile photo (from `config.json → profile_photos[0]`)
- Position according to the variant's layout
- Apply brand-consistent color grading

Use ImageMagick if available:
```bash
convert background.png profile.png -geometry +X+Y -composite \
  -font "BrandFont" -pointsize 72 -fill "#HEXCOLOR" \
  -annotate +X+Y "Title Text" \
  output.png
```

### Step 5: Output

Save to `~/social-media-content/YYYY-MM-DD/thumbnails/`:
- `variant-1-reference.png` — reference-inspired
- `variant-2-brand.png` — brand-native
- `variant-3-pattern-break.png` — pattern-break
- `thumbnail-analysis.md` — pattern analysis + rationale for each variant

The `thumbnail-analysis.md` should include:
```markdown
# Thumbnail Analysis — YYYY-MM-DD

## Reference Thumbnails Analyzed
| Video | Outlier Score | Pattern | Key Element |
|-------|--------------|---------|-------------|

## Generated Variants

### Variant 1: Reference-Inspired
- **Based on**: [outlier video title]
- **Pattern**: [layout description]
- **Why**: This pattern drove [X] outlier score
- **File**: variant-1-reference.png

### Variant 2: Brand-Native
- **Style**: [your brand aesthetic]
- **Why**: Consistency builds recognition
- **File**: variant-2-brand.png

### Variant 3: Pattern-Break
- **Concept**: [what makes it different]
- **Why**: Stand out in feed of [common pattern]
- **File**: variant-3-pattern-break.png

## Recommendation
★ Variant [X] — because [reason]
```
