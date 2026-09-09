# Research contract

## Source hierarchy

1. Indian regulations, Gazette notifications, standards/testing bodies, GeM/tender records, and certification issuers.
2. Official competitor/OEM/Tier-1 product documentation, filings, technical papers, homologation statements, and attributable releases.
3. Reputable trade publications quoting named parties or reproducing primary documents.
4. Distributor pages, conference materials, and databases as discovery leads.
5. Search snippets, aggregators, and unattributed reposts only as leads—never final proof.

Use primary and current sources for technical research. Record access date and publication date separately.

## Evidence states

- `VERIFIED`: supported by an authoritative record or independently inspectable artifact.
- `COMPANY_CLAIM`: asserted by the subject company without independent verification.
- `INFERRED`: analytical conclusion derived from cited evidence; include reasoning and confidence.
- `UNAVAILABLE`: required evidence was not found or accessible.
- `CONFLICTED`: credible sources disagree; preserve both and state what resolves the conflict.

## Comparison controls

- Match product scope: perception component, perception subsystem, warning-only retrofit, brake-integrated AEBS, or complete vehicle system.
- Match lifecycle: announced, sampled, qualified, orderable, shipping, or deployed.
- Match geography and program: global capability does not prove India availability or an Indian N2/N3 design win.
- Match certification scope: organization/process, component, production site, vehicle program, and type approval are distinct.
- Match economics: disclose quantity, scope, year, taxes, sensors, ECU, software, support, and qualification status. If incomparable, state so.
- Match procurement: GeM presence, Class-I status, local content, silicon origin, and tender-specific eligibility are separate facts.

## Research passes

1. Identity and corporate structure.
2. Product and shipping evidence.
3. Silicon/hardware architecture.
4. Certifications and homologation.
5. India OEM, Tier-1, channel, and service relationships.
6. Segment A procurement eligibility.
7. Segment B seven-gate readiness.
8. Segment C retrofit and field support.
9. Economics and publicly comparable BOM evidence.
10. Negative evidence, contradictions, and unresolved gaps.

## Evidence-ledger columns

`evidence_id,competitor,claim,source_url,source_title,publisher,published_date,accessed_date,status,scope,control_ids,notes`

Use stable IDs such as `ZF-001`. One row may support several controls, but do not combine unrelated claims into one row.
