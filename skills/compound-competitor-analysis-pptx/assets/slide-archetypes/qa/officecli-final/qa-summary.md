# OfficeCLI QA summary

- Status: passed
- Deck: `deepgrid-v14-native-archetypes-draft.pptx`
- SHA-256: `61fb7fff30a50643277c8b3fb0e5c8f983fad516acbb6ef4550ee2be04cf674a`
- OfficeCLI: `1.0.143`
- Slides: 9
- OpenXML validation: passed
- OfficeCLI issues: 0
- HTML contact sheet: contact-html.png
- Native PowerPoint contact sheet: not produced

## Native PowerPoint blocker

- PowerPoint 16.0 is installed, but the active application reports `Unlicensed Product`.
- New and active-session COM automation both reject `Presentations.Open` with HRESULT `0x80048240`.
- Windows OfficeCLI reports `--render native requires Windows with Microsoft PowerPoint installed`.
- The user's open v14 source deck was not closed or modified.
- Promotion remains blocked until Office activation is restored and all nine slides pass native-render inspection.

## Required human review

- Inspect every slide in the contact sheets.
- Record clipping, hierarchy, missing content, evidence encoding, and render differences.
- Do not promote solely from this automated result.
