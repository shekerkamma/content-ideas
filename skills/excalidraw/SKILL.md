---
name: excalidraw
description: Create editable Excalidraw diagrams as portable .excalidraw JSON files without requiring a live MCP canvas. Use for conceptual models, flowcharts, process maps, framework visuals, and video-frame-to-editable-diagram recreation. If live Excalidraw MCP tools are available, they may be used for screenshot iteration, but JSON-file generation is the default Codex-compatible path.
license: MIT
metadata:
  hermes:
    tags:
    - Excalidraw
    - Diagrams
    - Flowcharts
    - Architecture
    - Visualization
    - JSON
    related_skills: []
  legacy-frontmatter:
    version: 1.0.0
    author: Hermes Agent
    dependencies: []
    platforms:
    - linux
    - macos
    - windows
---

# Excalidraw Diagram Skill

Create diagrams by writing standard Excalidraw element JSON and saving as
`.excalidraw` files. These files can be drag-and-dropped onto
[excalidraw.com](https://excalidraw.com) for viewing and editing.

This is the default Codex-compatible Excalidraw workflow because it works even
when a live Excalidraw MCP server is unavailable. In this repo, a live MCP
canvas is also installed for screenshot iteration; use it when the MCP tools are
visible in the current Codex session.

## When to use

Generate `.excalidraw` files for architecture diagrams, flowcharts, sequence
diagrams, concept maps, framework visuals, and video-frame-to-editable-diagram
recreation. Files can be opened at excalidraw.com or uploaded for shareable
links.

For `video-to-deck`, use this skill by default when the video contains
conceptual models, frameworks, business workflows, mental models, process maps,
or teaching diagrams. Use captured frames as reference, but redraw the concept
in an original style rather than copying copyrighted visuals exactly.

## Workflow

1. **Load this skill**.
2. **Plan the diagram** from the user's prompt, transcript, or captured frames.
3. **Write the elements JSON** -- an array of Excalidraw element objects.
4. **Save the file** using normal file-writing tools to create a `.excalidraw`
   file.
5. **Optionally upload** for a shareable link using `scripts/upload.py` via the
   terminal.

### Saving a Diagram

Wrap your elements array in the standard `.excalidraw` envelope and save with `write_file`:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "hermes-agent",
  "elements": [ ...your elements array here... ],
  "appState": {
    "viewBackgroundColor": "#ffffff"
  }
}
```

Save to any path, e.g. `~/diagrams/my_diagram.excalidraw`.

### Uploading for a Shareable Link

Run the upload script (located in this skill's `scripts/` directory) via terminal:

```bash
python skills/diagramming/excalidraw/scripts/upload.py ~/diagrams/my_diagram.excalidraw
```

This uploads to excalidraw.com (no account needed) and prints a shareable URL.
Requires the `cryptography` pip package (`pip install cryptography`).

## Live MCP Canvas in Codex

This repo has a local Excalidraw MCP server at
`tools/mcp_excalidraw`. The Codex MCP entry is named `excalidraw` and points to:

```bash
node "$HOME/content-ideas/tools/mcp_excalidraw/dist/index.js"
```

The live canvas HTTP/WebSocket server is managed by a user systemd service:

```bash
systemctl --user status excalidraw-canvas.service --no-pager
systemctl --user restart excalidraw-canvas.service
curl -s http://127.0.0.1:3000/health
curl -s http://127.0.0.1:3000/api/sync/status
```

Screenshot/export calls also need a browser client connected to the canvas. This
repo runs a headless Chromium client as a second user service:

```bash
systemctl --user status excalidraw-canvas-client.service --no-pager
systemctl --user restart excalidraw-canvas-client.service
```

Use live MCP tools for screenshot iteration only when they are exposed in the
current Codex tool list after restart. The canvas UI can also be opened manually
at `http://127.0.0.1:3000`, but the headless service above keeps a frontend
available for visual screenshot/export tools such as `get_canvas_screenshot`.
Otherwise use `describe_scene` or export the portable `.excalidraw` file.

If live tools are missing, verify:

```bash
codex mcp get excalidraw
systemctl --user status excalidraw-canvas.service --no-pager
systemctl --user status excalidraw-canvas-client.service --no-pager
```

Then restart Codex so the MCP tool list reloads.

---

## Element Format Reference

### Required Fields (all elements)
`type`, `id` (unique string), `x`, `y`, `width`, `height`

### Defaults (skip these -- they're applied automatically)
- `strokeColor`: `"#1e1e1e"`
- `backgroundColor`: `"transparent"`
- `fillStyle`: `"solid"`
- `strokeWidth`: `2`
- `roughness`: `1` (hand-drawn look)
- `opacity`: `100`

Canvas background is white.

### Element Types

**Rectangle**:
```json
{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 100 }
```
- `roundness: { "type": 3 }` for rounded corners
- `backgroundColor: "#a5d8ff"`, `fillStyle: "solid"` for filled

**Ellipse**:
```json
{ "type": "ellipse", "id": "e1", "x": 100, "y": 100, "width": 150, "height": 150 }
```

**Diamond**:
```json
{ "type": "diamond", "id": "d1", "x": 100, "y": 100, "width": 150, "height": 150 }
```

**Labeled shape (container binding)** -- create a text element bound to the shape:

> **WARNING:** Do NOT use `"label": { "text": "..." }` on shapes. This is NOT a valid
> Excalidraw property and will be silently ignored, producing blank shapes. You MUST
> use the container binding approach below.

The shape needs `boundElements` listing the text, and the text needs `containerId` pointing back:
```json
{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 80,
  "roundness": { "type": 3 }, "backgroundColor": "#a5d8ff", "fillStyle": "solid",
  "boundElements": [{ "id": "t_r1", "type": "text" }] },
{ "type": "text", "id": "t_r1", "x": 105, "y": 110, "width": 190, "height": 25,
  "text": "Hello", "fontSize": 20, "fontFamily": 1, "strokeColor": "#1e1e1e",
  "textAlign": "center", "verticalAlign": "middle",
  "containerId": "r1", "originalText": "Hello", "autoResize": true }
```
- Works on rectangle, ellipse, diamond
- Text is auto-centered by Excalidraw when `containerId` is set
- The text `x`/`y`/`width`/`height` are approximate -- Excalidraw recalculates them on load
- `originalText` should match `text`
- Always include `fontFamily: 1` (Virgil/hand-drawn font)

**Labeled arrow** -- same container binding approach:
```json
{ "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0,
  "points": [[0,0],[200,0]], "endArrowhead": "arrow",
  "boundElements": [{ "id": "t_a1", "type": "text" }] },
{ "type": "text", "id": "t_a1", "x": 370, "y": 130, "width": 60, "height": 20,
  "text": "connects", "fontSize": 16, "fontFamily": 1, "strokeColor": "#1e1e1e",
  "textAlign": "center", "verticalAlign": "middle",
  "containerId": "a1", "originalText": "connects", "autoResize": true }
```

**Standalone text** (titles and annotations only -- no container):
```json
{ "type": "text", "id": "t1", "x": 150, "y": 138, "text": "Hello", "fontSize": 20,
  "fontFamily": 1, "strokeColor": "#1e1e1e", "originalText": "Hello", "autoResize": true }
```
- `x` is the LEFT edge. To center at position `cx`: `x = cx - (text.length * fontSize * 0.5) / 2`
- Do NOT rely on `textAlign` or `width` for positioning

**Arrow**:
```json
{ "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0,
  "points": [[0,0],[200,0]], "endArrowhead": "arrow" }
```
- `points`: `[dx, dy]` offsets from element `x`, `y`
- `endArrowhead`: `null` | `"arrow"` | `"bar"` | `"dot"` | `"triangle"`
- `strokeStyle`: `"solid"` (default) | `"dashed"` | `"dotted"`

### Arrow Bindings (connect arrows to shapes)

```json
{
  "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 150, "height": 0,
  "points": [[0,0],[150,0]], "endArrowhead": "arrow",
  "startBinding": { "elementId": "r1", "fixedPoint": [1, 0.5] },
  "endBinding": { "elementId": "r2", "fixedPoint": [0, 0.5] }
}
```

`fixedPoint` coordinates: `top=[0.5,0]`, `bottom=[0.5,1]`, `left=[0,0.5]`, `right=[1,0.5]`

### Drawing Order (z-order)
- Array order = z-order (first = back, last = front)
- Emit progressively: background zones → shape → its bound text → its arrows → next shape
- BAD: all rectangles, then all texts, then all arrows
- GOOD: bg_zone → shape1 → text_for_shape1 → arrow1 → arrow_label_text → shape2 → text_for_shape2 → ...
- Always place the bound text element immediately after its container shape

### Sizing Guidelines

**Font sizes:**
- Minimum `fontSize`: **16** for body text, labels, descriptions
- Minimum `fontSize`: **20** for titles and headings
- Minimum `fontSize`: **14** for secondary annotations only (sparingly)
- NEVER use `fontSize` below 14

**Element sizes:**
- Minimum shape size: 120x60 for labeled rectangles/ellipses
- Leave 20-30px gaps between elements minimum
- Prefer fewer, larger elements over many tiny ones

### Color Palette

See `references/colors.md` for full color tables. Quick reference:

| Use | Fill Color | Hex |
|-----|-----------|-----|
| Primary / Input | Light Blue | `#a5d8ff` |
| Success / Output | Light Green | `#b2f2bb` |
| Warning / External | Light Orange | `#ffd8a8` |
| Processing / Special | Light Purple | `#d0bfff` |
| Error / Critical | Light Red | `#ffc9c9` |
| Notes / Decisions | Light Yellow | `#fff3bf` |
| Storage / Data | Light Teal | `#c3fae8` |

### Tips
- Use the color palette consistently across the diagram
- **Text contrast is CRITICAL** -- never use light gray on white backgrounds. Minimum text color on white: `#757575`
- Do NOT use emoji in text -- they don't render in Excalidraw's font
- For dark mode diagrams, see `references/dark-mode.md`
- For larger examples, see `references/examples.md`
