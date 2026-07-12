---
type: technology
title: 'Neo4j'
description: 'Graph database for component-to-vehicle genealogy tracking — instant traversal queries for recall investigation and root-cause analysis.'
source_path: 'repos/Neo4j.md'
tags:
- repo
- uc-08
- graph-database
- traceability
timestamp: '2026-07-04'
---

> Original source (local copy): [repos/Neo4j.md](../source-vault/repos/Neo4j.md)
> Original source (WSL): [repos/Neo4j.md](/mnt/c/Users/sheke/Documents/hyundai-ai-vault/repos/Neo4j.md)
> Original source (Windows): [open in editor](file:///C:/Users/sheke/Documents/hyundai-ai-vault/repos/Neo4j.md)
> Windows path: `C:\Users\sheke\Documents\hyundai-ai-vault\repos\Neo4j.md`
# Neo4j

Graph database for component-to-vehicle genealogy tracking — instant traversal queries for recall investigation and root-cause analysis.

**GitHub:** https://github.com/neo4j/neo4j-python-driver
**Stars:** 900+

## Use Cases
[UC-08 Digital Traceability](../use-cases/uc-08-digital-traceability.md)

## How It's Used
Models manufacturing genealogy as a native graph: Component → installed_on → Assembly → part_of → Vehicle. Cypher queries traverse the graph instantly for recall scope calculation and defect propagation analysis.

## Technologies
Cypher, graph traversal, BOLT protocol
