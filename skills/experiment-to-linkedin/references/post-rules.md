# Post rules

Load the `anti-slop` skill before writing. These rules are the LinkedIn-specific layer on top.
`scripts/check_post.py` checks the mechanical ones.

## Shape of the file

```
# LinkedIn — <topic>

## Hook Options        3 first lines; mark the one used
## Draft               paste-ready post text, nothing else
## Source Notes        each number → its source and caveat (from claims.md)
## Repurpose           carousel path; X-thread outline
```

## The post

- **First line = the verdict**, gain and cost together. It must fit the first ~210 characters,
  which is all LinkedIn shows before "see more". Same words as slide 1.
- **Then the setup** in two short paragraphs: what you ran, what was held constant, the one
  thing that changed. One sentence explaining the thing tested, if readers might not know it.
- **Then the numbers**, one arm per line, same units on both:
  `Normal session: 34.4k tokens, 38 seconds.` / `Code Mode: 18k tokens, 67 seconds.`
  Then the correctness line.
- **Then other people's numbers**, only to say who measured them and that they aren't yours.
- **Then the catch**, what you lose, in one paragraph.
- **Then what you do now**, and point to the last slide for any code.
- **Close on the caveat as an instruction** ("One run on one task proves very little. Test it on
  your own work before you change your setup."). No question closer.
- Hashtags: 3, on the last line.

## Style

- 100–200 words. 1–2-sentence paragraphs with a blank line between.
- Full sentences. No outline of "2. Setup → …", no arrows as structure.
- At most one emoji; zero is fine.
- At most 1 em dash; colons only on the result lines.
- No code, backticks or shell in the body. LinkedIn shows it as a broken line.
- Order of paragraphs = order of carousel slides.

## Voice

`brand_context/voice-profile.md` in the content-ideas repo is a stock template (a web-scraping
creator persona). Use its LinkedIn format row (expertise-forward, line breaks, 100–200 words),
not its catchphrases. If the user has a real voice profile, run `review-draft` against it.
Audience default: enterprise AI architects, operators, pre-sales: direct, specific, no hype.

## Hook patterns that worked

1. "I turned on <X> and ran the same job twice. It used 48% fewer tokens. It also took 1.8 times as long."
2. "<X> halved my <metric> on a real task. It nearly doubled the wait."
3. "Everyone is quoting <big number> for <X>. None of those numbers come from <tool>, so I measured it."
