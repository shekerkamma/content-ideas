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

## Native PowerPoint evidence

- The byte-identical 74-slide v14 source/design authority already passed Windows OfficeCLI plus
  Microsoft PowerPoint native rendering across slides 1–74.
- Its inspected native contact sheet is retained at
  `runs/2026-08-13-deepgrid-india-adas-competitor-analysis/client-package/qa/officecli/native-contact.png`
  with SHA-256 `ee5bbe5ac0851cace0c8e7a26734cb211d99ecec3c6944f21d2dac6fa5453e2f`.
- The prior review found no clipping, off-slide content, missing content, or broken analytical layouts.
- A later attempt to rerender the exact sanitized nine-slide derivative returned HRESULT `0x80048240`
  while the reviewed source deck was open. This is recorded as a derivative-session limitation, not
  as absence of prior native PowerPoint QA.
- The derivative remains `draft` pending an exact-binary native rerender; the v14 design authority
  remains `reviewed`.

## Required human review

- Inspect every slide in the contact sheets.
- Record clipping, hierarchy, missing content, evidence encoding, and render differences.
- Do not promote solely from this automated result.
