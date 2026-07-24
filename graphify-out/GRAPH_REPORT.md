# Graph Report - brainstorms  (2026-06-05)

## Corpus Check
- Corpus is ~1,853 words - fits in a single context window. You may not need a graph.

## Summary
- 26 nodes · 23 edges · 9 communities (6 shown, 3 thin omitted)
- Extraction: 78% EXTRACTED · 22% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Use Case & Competitive Landscape|Use Case & Competitive Landscape]]
- [[_COMMUNITY_OpenHands Data Pipeline|OpenHands Data Pipeline]]
- [[_COMMUNITY_SAP Integration Layer|SAP Integration Layer]]
- [[_COMMUNITY_Explainability Dashboard|Explainability Dashboard]]
- [[_COMMUNITY_ML Training Pipeline|ML Training Pipeline]]
- [[_COMMUNITY_Delivery & Pricing Model|Delivery & Pricing Model]]
- [[_COMMUNITY_Industrial IoT Platforms|Industrial IoT Platforms]]
- [[_COMMUNITY_SAP MII Production Context|SAP MII Production Context]]
- [[_COMMUNITY_Big Consulting Competitor|Big Consulting Competitor]]

## God Nodes (most connected - your core abstractions)
1. `OpenHands` - 5 edges
2. `UC05 Predictive Quality Use Case` - 4 edges
3. `SAP PM Agent` - 4 edges
4. `Sensor Fusion Agent` - 3 edges
5. `Model Training Agent` - 3 edges
6. `Feature Engineering Agent` - 2 edges
7. `Explainability Agent` - 2 edges
8. `SAP QM (Quality Management)` - 2 edges
9. `XGBoost Baseline Model` - 2 edges
10. `SHAP Explainability` - 2 edges

## Surprising Connections (you probably didn't know these)
- `OpenHands` --implements--> `Model Training Agent`  [EXTRACTED]
  brainstorms/2026-06-05-predictive-quality-realization.md → brainstorms/2026-06-05-predictive-quality-realization.md  _Bridges community 1 → community 4_
- `OpenHands` --implements--> `Explainability Agent`  [EXTRACTED]
  brainstorms/2026-06-05-predictive-quality-realization.md → brainstorms/2026-06-05-predictive-quality-realization.md  _Bridges community 1 → community 3_
- `OpenHands` --implements--> `SAP PM Agent`  [EXTRACTED]
  brainstorms/2026-06-05-predictive-quality-realization.md → brainstorms/2026-06-05-predictive-quality-realization.md  _Bridges community 1 → community 2_
- `XGBoost Baseline Model` --shares_data_with--> `SAP QM (Quality Management)`  [EXTRACTED]
  brainstorms/2026-06-05-predictive-quality-realization.md → brainstorms/2026-06-05-predictive-quality-realization.md  _Bridges community 2 → community 4_

## Hyperedges (group relationships)
- **OpenHands Subagent Stack for Predictive Quality** — brainstorms_2026_06_05_predictive_quality_realization_openhands, brainstorms_2026_06_05_predictive_quality_realization_sensor_fusion_agent, brainstorms_2026_06_05_predictive_quality_realization_feature_engineering_agent, brainstorms_2026_06_05_predictive_quality_realization_model_training_agent, brainstorms_2026_06_05_predictive_quality_realization_explainability_agent, brainstorms_2026_06_05_predictive_quality_realization_sap_pm_agent [EXTRACTED 1.00]
- **SAP Integration Triad (QM + PM + MII via MCP/OData)** — brainstorms_2026_06_05_predictive_quality_realization_sap_qm, brainstorms_2026_06_05_predictive_quality_realization_sap_pm, brainstorms_2026_06_05_predictive_quality_realization_sap_mii, brainstorms_2026_06_05_predictive_quality_realization_mcp_odata_integration [EXTRACTED 1.00]
- **Predictive Quality Competitive Landscape** — brainstorms_2026_06_05_predictive_quality_realization_sight_machine, brainstorms_2026_06_05_predictive_quality_realization_uptake, brainstorms_2026_06_05_predictive_quality_realization_accenture, brainstorms_2026_06_05_predictive_quality_realization_ptc_thingworx, brainstorms_2026_06_05_predictive_quality_realization_siemens_mindsphere [EXTRACTED 1.00]

## Communities (9 total, 3 thin omitted)

### Community 0 - "Use Case & Competitive Landscape"
Cohesion: 0.50
Nodes (5): Predictive Quality Realization Brainstorm, Hyundai (Reference Client Context), Sight Machine (Competitor), UC05 Predictive Quality Use Case, Uptake (Competitor)

### Community 1 - "OpenHands Data Pipeline"
Cohesion: 0.67
Nodes (4): Sensor-to-Historian Data Path, Feature Engineering Agent, OpenHands, Sensor Fusion Agent

### Community 2 - "SAP Integration Layer"
Cohesion: 0.50
Nodes (4): MCP-wrapped OData Integration Pattern, SAP PM (Plant Maintenance), SAP PM Agent, SAP QM (Quality Management)

### Community 3 - "Explainability Dashboard"
Cohesion: 0.67
Nodes (3): ADK + AG-UI Generative Dashboard, Explainability Agent, SHAP Explainability

### Community 4 - "ML Training Pipeline"
Cohesion: 0.67
Nodes (3): MLflow (Experiment Tracking), Model Training Agent, XGBoost Baseline Model

### Community 5 - "Delivery & Pricing Model"
Cohesion: 0.67
Nodes (3): 4-Week Pilot Delivery Structure, Pricing Model ($40-60K pilot, $8-12K/month retainer), Week 1 Data Discovery Gate (Risk Mitigation)

## Knowledge Gaps
- **9 isolated node(s):** `Predictive Quality Realization Brainstorm`, `SAP PM (Plant Maintenance)`, `SAP MII/ME (Manufacturing Integration)`, `ADK + AG-UI Generative Dashboard`, `Hyundai (Reference Client Context)` (+4 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `OpenHands` connect `OpenHands Data Pipeline` to `SAP Integration Layer`, `Explainability Dashboard`, `ML Training Pipeline`?**
  _High betweenness centrality (0.190) - this node is a cross-community bridge._
- **Why does `SAP PM Agent` connect `SAP Integration Layer` to `OpenHands Data Pipeline`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Why does `Explainability Agent` connect `Explainability Dashboard` to `OpenHands Data Pipeline`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Sensor Fusion Agent` (e.g. with `Sensor-to-Historian Data Path` and `Feature Engineering Agent`) actually correct?**
  _`Sensor Fusion Agent` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Predictive Quality Realization Brainstorm`, `SAP PM (Plant Maintenance)`, `SAP MII/ME (Manufacturing Integration)` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._