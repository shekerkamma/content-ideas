# Routing

## Entity Notes

- People and creators -> `People/<Full Name>.md`
- Tools, products, platforms, frameworks, languages -> `technologies/<Name>.md`
- Concepts, methods, protocols, strategy terms -> `Knowledge/<Name>.md`
- Active initiatives, offers, client pursuits, businesses -> `Projects/<Name>.md`
- Research outputs -> `content-research/<source-type>/<kebab-slug>.md`

## MOCs

Create a MOC when a topic has:
- more than 5 notes,
- repeated references across folders,
- or strategic value for TMNA, Hyundai, SAP, POC Factory, or AI agents.

MOCs belong in the folder that owns the topic:
- Enterprise and concepts -> `Knowledge/`
- Projects and initiatives -> `Projects/`
- People maps -> `People/`
- Content research maps -> `content-research/_index/`

## Task Propagation

When a cleanup produces future work:
- create a task note in `Tasks/`,
- add it to `Boards/Work.md`,
- link the related MOC or project,
- and mention the change in today's daily note.

## Stub Quality

A stub must include:
- YAML frontmatter with `title` and `tags`,
- one-sentence definition,
- `## Relevance`,
- `## Related`.

## Known Edge Cases

- `Ben AI`, `Patrick Dang`, `Chris Ashby` -> `People/`
- `n8n`, `YouTube`, `TikTok`, `Supabase`, `Shopify`, `Perplexity`, `Nano Banana`, `Skool`, `QuickBooks`, `ClickUp`, `Claude Opus`, `Meta Ads`, `Facebook`, `Windsurf` -> `technologies/`
- `wiki-links`, `content-research`, `pre-sales`, `enterprise AI`, `context engineering` -> `Knowledge/`
