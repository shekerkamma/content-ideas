# PPTX Toolkit operations

## Contents

1. Inventory schema
2. Edit specification
3. Reorder and remove slides
4. OOXML unpack and repack
5. Validation and delivery
6. Boundaries

## 1. Inventory schema

```bash
python3 skills/pptx-toolkit/scripts/pptx_toolkit.py \
  inspect source.pptx --out inventory.json
```

The inventory records presentation dimensions, slide order, layout names, titles, notes,
shape IDs/names/types/positions, paragraphs, runs, and package-level comment parts. Use the
inventory as the source of truth for edit selectors.

## 2. Edit specification

Use one-based slide numbers. Select a shape with exactly one of `shape_id` or `shape_name`.
Prefer `shape_id` because names are not guaranteed to be unique.

```json
{
  "slides": [
    {
      "slide": 2,
      "replacements": [
        {"shape_id": 7, "text": "Updated action title"},
        {"shape_name": "Body Text", "text": "First line\nSecond line"}
      ],
      "notes": "Explain the decision, then transition to the implementation plan."
    }
  ]
}
```

```bash
python3 skills/pptx-toolkit/scripts/pptx_toolkit.py \
  edit source.pptx edited-draft.pptx --spec edits.json
```

Replacement is intentionally whole-shape. The first existing run supplies the retained
formatting; other runs are cleared. Do not use this operation when mixed emphasis within the
same shape must remain. In that case, rebuild the slide with the appropriate deck skill or
perform an explicitly reviewed OOXML edit.

An empty notes string clears the native speaker notes. Creating or updating notes may add a
notes-slide part to the package, which is normal PowerPoint behavior.

## 3. Reorder and remove slides

```bash
# Reorder all slides
python3 skills/pptx-toolkit/scripts/pptx_toolkit.py \
  reorder source.pptx reordered-draft.pptx --order 3,1,2

# Keep slides 1, 4, and 5; remove every omitted slide
python3 skills/pptx-toolkit/scripts/pptx_toolkit.py \
  reorder source.pptx shortened-draft.pptx --order 1,4,5
```

Each source slide can appear only once. This restriction avoids unsafe partial cloning of
charts, media, notes, and embedded relationships.

## 4. OOXML unpack and repack

Use this escape hatch only when the controlled operations cannot express the required edit.

```bash
python3 skills/pptx-toolkit/scripts/pptx_toolkit.py unpack source.pptx unpacked/
# edit files under unpacked/ with a targeted patch
python3 skills/pptx-toolkit/scripts/pptx_toolkit.py pack unpacked/ rebuilt-draft.pptx
```

Unpack rejects archive paths that escape the target directory. Pack rejects symlinks and
requires `[Content_Types].xml` plus `ppt/presentation.xml`.

## 5. Validation and delivery

```bash
python3 skills/pptx-toolkit/scripts/pptx_toolkit.py validate rebuilt-draft.pptx
python3 scripts/officecli_qa.py rebuilt-draft.pptx --out qa/officecli --required
```

Structural validation checks ZIP integrity, required package members, XML parseability, and
whether `python-pptx` can reopen the file. It does not prove visual correctness. Use the
existing branded preview and OfficeCLI render gates before assigning `reviewed` status.

## 6. Boundaries

- Supported: `.pptx` inspection, whole-shape text replacement, native notes, reorder/remove,
  safe unpack/repack, structural validation.
- Read-only discovery: comments and unsupported package parts.
- Unsupported: slide duplication, `.pptm` macros, chart workbook mutation, SmartArt editing,
  animation editing, embedded-object mutation, and fidelity claims without real render QA.
