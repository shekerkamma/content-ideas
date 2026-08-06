# Search log

Backends: **GBrain** (recall) · **You.com Level 2** (discovery + fresh Exa `/contents` extraction) · Exa.
Level 2 verified live before use: 5 discovery + 3 extractions on a probe query.

> Operator note: `~/.hermes/.env` (WSL) holds an `sk-…` OpenAI key under `YOU_API_KEY`, which is
> wrong and poisons the environment. The valid `ydc…` key is in the **Windows-side**
> `AppData/Local/hermes/.env`, which the skill script reads first. All calls run under
> `env -u YOU_API_KEY -u YDC_API_KEY` so the bad WSL value cannot win.

| # | Query | Slug | Discovery | Extracted |
|---|---|---|---|---|
| 1 | GSR 184(E) India ADAS mandate N2 N3 trucks effective date enforcement 2026 | mandate-dates | 5 | 5 |
| 2 | Netrasemi Mindgrove Indian ADAS automotive SoC startup shipping 2026 | indian-semi-peers | 5 | 5 |
| 3 | Minus Zero Swaayatt Robots RoshAI India autonomous driving startup funding traction 2026 | software-first-india | 5 | 3 |
| 4 | India truck fleet ADAS retrofit kit price AIS-140 compliance device cost 2026 | low-end-pricing | 5 | 5 |
| 5 | Mobileye Bosch Continental India commercial vehicle ADAS supply 2026 truck OEM | incumbent-india | 5 | 4 |

**Totals: 25 discovery results, 22 fresh page extractions, 304,574 characters.**
Per-page statuses retained in `working/captures/*.json`.

## GBrain recall status
Ran `search("DeepGrid Semi ADAS silicon competitive positioning client acquisition")`.
**Result: no prior DeepGrid pages exist.** Two unrelated hits (the dossier skill definition;
a 2026 semiconductor bottleneck map). Recall is therefore **empty for this target** — all
company facts in this run come from the four supplied documents, all market facts from Level 2.
