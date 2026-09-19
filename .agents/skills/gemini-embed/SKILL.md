---
name: gemini-embed
description: Multimodal embeddings for text, images, diagrams, schematics, and waveforms using Google Gemini Embedding 2 (3072 dimensions).
allowed-tools: Bash, Read, Write
metadata:
  requires:
    env:
    - GOOGLE_GENERATIVE_AI_API_KEY
    bins:
    - python3
  legacy-frontmatter:
    version: 1.0.0
    user-invocable: true
---

# gemini-embed

Generate 3,072-dimensional multimodal embeddings using Google's `models/gemini-embedding-2` via the Google AI Studio API.

Maps both text queries and visual assets (PNG, JPEG, WebP, GIF) into the **same shared vector space** for cross-modal similarity, technical schematic retrieval, and hybrid document search.

## When to Invoke
- Extract vector embeddings for technical diagrams, die floorplans, package pinouts, or waveforms.
- Compute cosine similarity between text descriptions and images.
- Batch-embed technical whitepaper chunks, code snippets, or images into vector datasets.

## CLI Usage

### 1. Embed Text
```bash
python3 scripts/gemini_embed.py --text "DeepGrid 130 nm lockstep RISC-V silicon" --out text_vec.json
```

### 2. Embed an Image (Diagram, Schematic, Waveform)
```bash
python3 scripts/gemini_embed.py --image path/to/schematic.png --out image_vec.json
```

### 3. Compute Cosine Similarity (Text-to-Text or Cross-Modal)
```bash
# Compare text against text:
python3 scripts/gemini_embed.py --text "130 nm RV32IM MCU" --compare-text "SkyWater sky130A motor silicon"

# Cross-modal comparison (Image against Text):
python3 scripts/gemini_embed.py --image path/to/die.png --compare-text "Die floorplan layout"

# Image-to-Image visual comparison:
python3 scripts/gemini_embed.py --image slide1.png --compare-image slide2.png
```

## Python Integration
```python
from scripts.gemini_embed import embed, cosine_similarity

# Text embedding
vec_text = embed(text="Lockstep safety monitor")

# Image embedding
vec_img = embed(image_path="docs/package_qfn64.png")

# Calculate cross-modal similarity
score = cosine_similarity(vec_text, vec_img)
```
