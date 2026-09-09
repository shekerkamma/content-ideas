# GTM Data Source Protocol

Use this protocol before running any workflow in this pack.

## 1. Recall durable context

If GBrain is available, run semantic recall for the named company, person, vertical, campaign, or use case before repeating research. Treat recalled material as context, not current proof. Verify time-sensitive claims against a current source.

## 2. Discover available sources

Use the best sources available in this order:

1. Connected first-party systems: intent/signal platform, CRM, marketing automation, product analytics, enrichment, calendar, or outreach system.
2. User-provided exports or tables: CSV, JSON, spreadsheet, database query results, or pasted records.
3. Current authoritative public sources for company and market context.

Clearcue is one optional intent-data adapter, not a prerequisite. Do not claim to have queried a connector that is unavailable. If essential data is missing, request the smallest useful export or input schema; otherwise continue with a clearly labeled partial result.

## 3. Normalize and preserve provenance

For each signal, retain when available: account, person, signal type, observed time and timezone, source system, source record or URL, retrieval time, and confidence. Preserve raw source values alongside normalized labels when generating an artifact.

Classify claims as:

- `VERIFIED`: directly supported by a retrieved record or cited current source.
- `INFERRED`: reasoned from verified evidence; state the reasoning and confidence.
- `UNAVAILABLE`: required evidence was not accessible.

Never present an inference, a remembered fact, or missing data as a recorded buying signal.

## 4. Separate analysis from mutation

Reading, analyzing, and drafting are non-mutating. Tagging records, updating a CRM, scheduling automation, launching outreach, sending messages, or publishing reports changes external state. Preview the exact proposed changes and obtain explicit user approval before executing them. Report whether each action was drafted, approved, executed, or failed.

## 5. Persist durable findings

When GBrain is available, write back durable cross-session findings after the run. Do not store raw private contact activity, credentials, or client deliverables unless the user has authorized that data class. Keep deliverables and evidence artifacts in the repository or configured run directory; GBrain is not the system of record.
