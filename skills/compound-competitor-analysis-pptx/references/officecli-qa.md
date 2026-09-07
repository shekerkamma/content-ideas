# OfficeCLI QA and reviewed promotion

## Required checks

1. Validate the OpenXML package.
2. Run OfficeCLI `view issues`; require zero issues.
3. Run native design lint with zero unresolved errors or warnings.
4. Generate HTML contact sheets covering every slide and inspect them.
5. On Windows with Microsoft PowerPoint, generate a native-render contact sheet and inspect it.
6. Verify slide count, title sequence, notes, editability, internal-term scan, delivery checksum, and
   filename status.

## Direct OfficeCLI commands

```bash
officecli validate deck.pptx --json
officecli view deck.pptx issues --limit 5000 --json
officecli view deck.pptx screenshot --page 1-N --grid 5 --render html \
  --screenshot-width 2400 --screenshot-height 1600 -o contact-html.png --json
```

WSL must invoke the Windows binary from a Windows working directory for native rendering:

```bash
mkdir -p /mnt/c/Temp/deck-qa
cp deck.pptx /mnt/c/Temp/deck-qa/input.pptx
powershell.exe -NoProfile -Command \
  "Set-Location 'C:\Temp\deck-qa'; & '$env:LOCALAPPDATA\OfficeCLI\officecli.exe' \
   view 'C:\Temp\deck-qa\input.pptx' screenshot --page 1-N --grid 5 --render native \
   --screenshot-width 2400 --screenshot-height 1600 \
   -o 'C:\Temp\deck-qa\contact-native.png' --json"
```

Do not claim native rendering if only HTML rendering succeeded. Do not claim the absent historical
`scripts/officecli_qa.py` wrapper ran; use this skill's bundled wrapper or direct commands.

## Contact-sheet review

Inspect every slide for:

- clipping, overflow, off-slide shapes, or missing objects;
- hierarchy and five-second comprehension;
- type size, wrapping, contrast, and alignment;
- evidence-status legibility;
- meaningful whitespace and focal point;
- consistent comparable-page geometry;
- correct source/footer and slide numbering;
- native render differences versus HTML preview.

## Promotion

Write `qa/officecli/qa-summary.md` with tool version, slide count, validation/issue counts, render
paths, native/HTML status, review scope, defects fixed, and final status. Promote only when the
summary says `passed` and all contact sheets were actually inspected.
