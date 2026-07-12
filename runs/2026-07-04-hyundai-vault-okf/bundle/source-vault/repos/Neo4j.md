---
title: "Neo4j"
tags: [repo, uc-08, graph-database, traceability]
type: repo
url: "https://github.com/neo4j/neo4j-python-driver"
stars: "900+"
---

# Neo4j

Graph database for component-to-vehicle genealogy tracking — instant traversal queries for recall investigation and root-cause analysis.

**GitHub:** https://github.com/neo4j/neo4j-python-driver
**Stars:** 900+

## Use Cases
[[UC-08 Digital Traceability]]

## How It's Used
Models manufacturing genealogy as a native graph: Component → installed_on → Assembly → part_of → Vehicle. Cypher queries traverse the graph instantly for recall scope calculation and defect propagation analysis.

## Technologies
Cypher, graph traversal, BOLT protocol
