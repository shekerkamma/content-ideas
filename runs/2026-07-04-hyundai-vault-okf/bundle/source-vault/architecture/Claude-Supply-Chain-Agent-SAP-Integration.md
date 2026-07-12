---
title: Claude Supply Chain Agentic Team - SAP Integration Architecture
description: End-to-end agent orchestration for supply chain operations with SAP/ERP data connectivity
tags: [architecture, agents, supply-chain, sap, erp, integration]
---

# Claude Supply Chain Agentic Team — SAP Integration

## Overview

The Claude Supply Chain Agentic Team is a 6-agent orchestration system that reads from SAP/ERP systems of record and acts on real-time exceptions and optimization opportunities. Unlike traditional ERP modules (which are rules-based), these agents are **systems of reasoning** that factor in external signals (weather, tariffs, supplier news, carrier telemetry) and make autonomous decisions.

**Core Philosophy:**
> ERPs tell you what happened. Agents tell you what to do about it.

---

## Architecture Layers

### Layer 1: Data Ingestion (SAP Connectivity)
```
SAP ERP/MES System
    ↓
RFC/REST APIs (PyRFC, custom adapters)
    ↓
Data Lake / Real-Time Cache
    ↓
Knowledge Graph (NetworkX)
```

**SAP Connection Methods:**
- **RFC (Remote Function Call)** — Synchronous reads from SAP modules
  - Material Master (MM)
  - Sales & Operations Planning (S&OP)
  - Inventory Management (IM)
  - Purchasing (PU)
  - Production Planning (PP)
  - Quality Management (QM)

- **EDI/REST APIs** — Asynchronous data feeds
  - Purchase Orders (PO)
  - Goods Receipts (GR)
  - Invoices (IV)
  - Shipment tracking

- **Real-Time Change Data Capture (CDC)**
  - Kafka/streaming for inventory deltas
  - Supplier delivery notifications
  - QA exception flags

### Layer 2: Knowledge Graph
```
NetworkX Graph Structure:
├── Supplier Node (SKU affinity, lead times, risk profile)
├── Product Node (BOM, SKU, demand history, forecast)
├── Warehouse Node (capacity, current stock, reorder levels)
├── Edge: supplier → product → warehouse (3-second cascade traversal)
└── Attributes: cost, lead time, risk score, last-update timestamp
```

**Graph Update Frequency:**
- Inventory: Real-time (sub-second)
- Supplier performance: Hourly
- Demand history: Daily
- Product specs: On-change

### Layer 3: Six Agent Clusters

#### 1. **Demand Forecasting Agent**
```
Input:
  - SAP demand history (36 months min)
  - Point-of-sale (POS) data
  - Promotion calendar
  - Seasonality factors

Process:
  - Tournament: AutoARIMA vs AutoETS vs LightGBM
  - Winner picked by revenue-weighted wMAPE
  - P10/P50/P90 confidence intervals

Output:
  - SKU × Warehouse × Week forecast
  - Confidence scores
  - Anomaly flags (spike/drop detection)
  - Updated into SAP SNP / S&OP module
```

**SAP Integration:**
- Write forecasts to SAP `/SCWM/FORECAST` tables
- Trigger S&OP planning runs automatically
- Update safety stock recommendations in inventory module

---

#### 2. **Inventory Optimization Agent**
```
Input:
  - Current inventory levels (SAP IM)
  - Lead times by supplier (SAP PU)
  - Demand forecasts (from Agent #1)
  - Holding costs (SAP CO)
  - Stockout penalties

Process:
  - ABC/XYZ classification (volume × variability)
  - Dynamic safety stock calculation
  - Automated reorder point computation
  - Dual-flag system: stockout risk AND overstock risk

Output:
  - Reorder points per location
  - Stock transfer recommendations
  - Obsolescence alerts
  - Real-time balance sheet adjustments
```

**SAP Integration:**
- Read: `MARD` (stock), `MARC` (material control), `MBEW` (valuation)
- Write: Reorder points to `MARD-MINBE`
- Trigger stock transfers via ABAP API
- Update ABC classification in material master

---

#### 3. **Procurement Automation Agent** ⭐ (Most SAP-intensive)
```
Input:
  - Stock-out risk signals (Agent #2)
  - Supplier performance data (SAP LIS/EDI history)
  - Open POs and expected deliveries
  - Approved vendor lists (SAP PU)
  - Contract pricing (SAP MM)

Process (ReAct Loop, 14-tool chain):
  Tool 1-3: Query supplier status + lead times
  Tool 4-6: Fetch current open POs + GRs
  Tool 7-9: Check approved suppliers + pricing
  Tool 10: Decide tactic (expedite/split/absorb/substitute)
  Tool 11: Draft purchase order
  Tool 12: Generate supplier email
  Tool 13: Create internal note (audit trail)
  Tool 14: Submit to SAP (ME21N transaction)

Output:
  - New PO (auto-submitted to SAP ME22N)
  - Supplier communication (email draft)
  - Internal justification + reasoning
  - Full audit trail
  - End-to-end: 2–15 seconds

Decision Logic:
  - Expedite: if supplier in top 10% reliability + buffer stock exists
  - Split: if no single supplier can cover + risk distribution needed
  - Absorb: if cost of expedite > stockout penalty
  - Substitute: if approved alternative exists + <5% cost delta
```

**SAP Integration (Deep):**
- Read RFC calls:
  - `MD04` — Material availability overview
  - `ME2M` — Vendor evaluation
  - `MDOC` — Open/confirmed POs
  - `MIGO` — Goods receipt history
  
- Write RFC calls:
  - `ME21N` — Create PO
  - `BAPI_PO_CREATE` — Direct PO creation
  - `ZVENDOR_EMAIL_LOG` — Custom table logging supplier comms
  
- Real-time data:
  - EDI 850 (purchase order) → SAP
  - EDI 856 (shipment notice) → SAP
  - EDI 997 (functional ack) from SAP

---

#### 4. **Disruption Monitoring Agent**
```
Input:
  - EDI feeds (supplier delays, ASNs)
  - Weather data (NOAA API)
  - Carrier telemetry (FedEx/DHL APIs)
  - QA rejection rates (SAP QM)
  - News feeds (supplier bankruptcies, tariffs)
  - SAP open POs with expected dates

Process:
  - Multi-source fusion (weighted scoring)
  - Revenue-at-risk prioritization
  - Auto-escalation rules (>$100K risk → immediate alert)

Output:
  - Incident severity rank (1-5)
  - Root cause hypothesis
  - Auto-trigger Procurement agent if needed
  - Dashboard alert + email

Mean Time to Detect: 42 seconds
```

**SAP Integration:**
- Real-time PO tracking via EDI 856 (ASN)
- Write alerts to custom table `ZSUPP_DISRUPTION`
- Query QM module for rejection data

---

#### 5. **Logistics & Distribution Agent**
```
Input:
  - Shipment tracking (carrier APIs)
  - Hub utilization (SAP WM)
  - ETA predictions
  - Inventory in-transit (SAP TRAN module)
  - Route optimization data

Process:
  - Identify lane-level carrier performance
  - Flag ETA risks (>12h variance)
  - Recommend consolidation or expedite
  - Calculate dwell-time costs

Output:
  - KPIs: On-time %, Cost/unit, Carrier rating
  - Hub congestion alerts
  - Carrier selection recommendations
```

**SAP Integration:**
- Read: `NAST`, `TKET` (shipment master), `MATDOC` (in-transit inventory)
- Write: Proposed route changes to planning module

---

#### 6. **Supply Chain Visibility Dashboard Agent**
```
Single Control Tower:
  - 5 KPI tiles (On-Time %, Stockout Risk, Forecast Accuracy, etc.)
  - Network Health Pulse (supplier green/yellow/red)
  - Ranked insights (highest revenue at risk first)
  - Agent recommendation queue with audit trail
  - PO export (approved recommendations)
```

**SAP Integration:**
- Live-read dashboard data every 10 seconds
- Write audit logs for every user action + agent recommendation accepted/rejected

---

## End-to-End Flow Example: Supplier Delay → Mitigation

```
Timeline: 42 seconds to fully mitigated

T+0s:   Disruption Monitoring detects delayed shipment via EDI 856
        → severity: HIGH ($420K at risk, customer deadline 3 days)

T+5s:   Agent queries SAP: current inventory, open POs, approved suppliers
        → finds stock covers 2 days, Customer A (Tier-1) affected

T+10s:  Inventory Optimization recalculates reorder points given reduced buffer
        → flags 2 alternative warehouses 500 miles away

T+15s:  Procurement Agent decides: SPLIT + EXPEDITE
        → expedite 60% from backup supplier (11h lead time, +$800 cost)
        → transfer 40% from warehouse in Atlanta (2-day ground)

T+20s:  Procurement creates 2 POs (ME21N transaction), drafts emails
        → sends to suppliers with ASN expectations

T+30s:  Inventory Agent schedules stock transfer via ABAP
        → updates warehouse replenishment schedule

T+40s:  Dashboard surfaces as #1 insight: "Mitigated $420K risk via split procurement"
        → user clicks "Accept" → POs auto-submit to SAP

T+42s:  DONE. Full reasoning trail in audit log.
```

---

## SAP Integration Patterns

### Pattern 1: Synchronous Query (Real-Time Decision)
```python
# Procurement agent needs to check approved supplier list
sap_connection.call_bapi('RFC_READ_TABLE', {
    'QUERY_TABLE': 'EORD',  # Vendor evaluation
    'OPTIONS': [
        {'SIGN': 'I', 'OPTION': 'EQ', 'LOW': vendor_id}
    ]
})
# Response: supplier risk score, on-time %, past issues
# Decision made within <200ms
```

### Pattern 2: Asynchronous Write (PO Submission)
```python
# Procurement agent creates PO
sap_connection.call_bapi('BAPI_PO_CREATE', {
    'PO_HEADER': {...},  # vendor, date, amount
    'PO_ITEMS': [{sku, qty, price, lead_time}, ...],
    'COMMIT': True
})
# PO number returned, logged in audit trail
# Real-time visibility to SAP users
```

### Pattern 3: Real-Time Feed (EDI)
```
Supplier sends ASN (Advance Shipment Notice) via EDI 856
→ Parsed by integration layer
→ Disruption Agent fuses with weather/carrier data
→ If delay detected, auto-triggers Procurement
```

### Pattern 4: Streaming Updates (Inventory Deltas)
```
SAP CDC (Kafka topic: `sap.IM.MARD`)
  Every GR (goods receipt) → published in <1 second
  → Inventory Optimization Agent recalculates safety stock
  → Knowledge graph updated in-memory
```

---

## Technical Stack

| Component | Technology | Purpose |
|-----------|----------|---------|
| ERP Connection | SAP RFC (PyRFC) | Synchronous reads/writes |
| EDI Gateway | X12/EDIFACT parser | Async supplier comms |
| Stream Processing | Kafka | Real-time inventory deltas |
| Knowledge Graph | NetworkX | Supplier-product-warehouse relationships |
| Forecasting | AutoARIMA, AutoETS, LightGBM | Tournament-based model selection |
| Agent Framework | Claude + ReAct | Multi-tool reasoning loop |
| Persistence | PostgreSQL | Audit trail, historical data |
| Dashboard | React + WebSocket | Live KPI updates |

---

## Comparison to UC-08 Digital Traceability

Both systems integrate with SAP but serve **different layers**:

| Aspect | UC-08 Traceability | Claude Supply Chain Agent |
|--------|-------------------|--------------------------|
| **Scope** | Component genealogy (RFID/barcodes) | Supply chain decisions (demand, inventory, procure) |
| **Data Source** | Production stations (real-time tags) | SAP master data + external signals |
| **Graph Type** | Component lineage (what parts built this assembly?) | Supplier-product-warehouse network (where can we source?) |
| **SAP Integration** | RFC to MES/ERP, sync genealogy snapshots | Real-time PO creation, reorder point updates |
| **Output** | Recall investigation, traceability audit | Autonomous procurement decisions, risk alerts |
| **Time Criticality** | Historical (recall takes days) | Immediate (42s to detect + mitigate disruption) |

**Synergy:** A manufacturing plant running both systems would:
1. UC-08 tracks component genealogy for quality/safety
2. Claude Agent optimizes procurement to ensure BOM components are available
3. If disruption detected (supplier delay), Agent auto-escalates to materials planner
4. Planner views UC-08 genealogy to understand downstream impact

---

## Readiness & Deployment

**Production-Ready Components:**
- ✅ SAP RFC connectivity (PyRFC is battle-tested)
- ✅ Demand forecasting (3-model tournament well-established)
- ✅ ReAct agent framework (Claude proven at multi-tool loops)
- ✅ EDI parsing (standard X12/EDIFACT)

**Deployment Timeline:**
- **Week 1-2:** Map SAP schema to knowledge graph structure
- **Week 3-4:** Build RFC queries for each agent cluster
- **Week 5-6:** Train demand model on 36-month history
- **Week 7-8:** Parallel-run agents (dry-run POs, recommendations only)
- **Week 9:** Go-live with audit-trail validation

**Pilot Cost:** $50-150K (8-week engagement)

---

## Key Metrics

| Metric | Baseline (Manual) | With Agents |
|--------|------------------|-------------|
| Time to mitigate supplier disruption | 4-6 hours | 42 seconds |
| Forecast accuracy (wMAPE) | 18-22% | 9-12% |
| Stockout incidents/year | 12-18 | 2-4 |
| Procurement cycle time | 30-90 min | 2-15 sec |
| Safety stock excess | 22% | 8-12% |
| Spreadsheet effort (planners) | 40 hrs/week | 8 hrs/week |

---

## Security & Governance

**SAP Access Control:**
- Agents use dedicated technical user (role: `ZPLANNING_AGENT`)
- Scope: Read Material Master, Inventory, Purchasing; Write only POs
- No access to Finance (FI), Payroll (HR)
- All actions audit-logged with timestamp + reasoning

**Approval Workflows (Phase 1):**
- POs >$50K require human sign-off (e-signature)
- Procurement agent drafts, dashboard queues for approval
- User can accept, modify, or reject before submission

**Escalation to Humans:**
- Decisions with confidence <60%
- Novel scenarios (supplier not in approved list)
- Revenue at risk >$250K

---

## References

- [Claude Supply Chain Agentic Team (Full Architecture)](https://adithyan-experidium.notion.site/The-Claude-Supply-Chain-Agentic-Team-3632cd3823118136be2be80fbb1228a2)
- [[UC-08 Digital Traceability]] (Hyundai AI Vault)
- [[repos/PyRFC]] (SAP RFC library)
- [[repos/Flink]] (Stream processing for real-time inventory)
