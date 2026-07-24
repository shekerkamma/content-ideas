Translate the contents of `/raw` into durable Hyundai AI wiki notes.

Process:

1. Read each new file in `/raw`.
2. Decide whether it belongs in an existing wiki note or a new one in `/wiki`.
3. If the target wiki note already exists, read it first and merge carefully.
4. Preserve distinctive phrasing from the source when it adds signal.
5. Record uncertainty explicitly instead of inventing details.
6. Record source provenance when useful.
7. After processing a raw file, move it into `/archive` without editing its contents.

Output standard:

- Markdown only
- Clear, factual, terse
- One topic per file
- Kebab-case filenames
- No filler summaries
- Prefer durable notes about Hyundai AI strategy, operations, vendors, workflows, and implementation patterns
