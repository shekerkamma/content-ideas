# Chapter 10: From Working Silicon to a Shipped Product

## Core Idea
Silicon fabrication is only the midpoint of hardware delivery. Productization requires ₹40–80 Lakhs per chip for electrical characterization and environmental qualification, ₹1.2 Cr in dedicated Automated Test Equipment (ATE) engineering, and organizational certification (ISO 9001 / AS9100) before entering customer Approved Vendor Lists (AVL).

---

## The Dual-Track Qualification Lifecycle

```
                           ┌───────────────────────────┐
                           │      SILICON IN HAND      │
                           │   (Day 180 / Day 198)     │
                           └─────────────┬─────────────┘
                                         │
             ┌───────────────────────────┴───────────────────────────┐
             ▼                                                       ▼
┌───────────────────────────────┐               ┌───────────────────────────────┐
│     COMMERCIAL / INDUSTRIAL   │               │       SCREENED DEFENCE        │
│          (6–9 Months)         │               │        (9–12 Months)          │
├───────────────────────────────┤               ├───────────────────────────────┤
│ • Electrical Characterisation │               │ • High-Temp Burn-In (168 hrs) │
│ • Multi-batch PVT Limits      │               │ • MIL-STD-883 / JSS Screening │
│ • HTOL Life Testing (125°C)   │               │ • CEMILAC Airworthiness       │
│ • ESD (HBM/CDM) & Latch-up    │               │ • Fine/Gross Package Leak Test│
│ • Automated ATE Test Vectors  │               │ • Complete Lot Traceability   │
│ • Published Datasheet         │               │ • Unit Price: 10x–100x higher │
└───────────────────────────────┘               └───────────────────────────────┘
```

---

## The Three Critical Non-Design Bottlenecks

### 1. The ATE (Automated Test Equipment) Testing Cost Line
- **The Issue**: Wafer probe cards, load boards, custom test sockets, and machine run-time are not included in foundry shuttle costs.
- **Budget Allocation**: ₹1.2 Cr dedicated testing line item explicitly provisioned in the seed round.
- **Multi-Chip Package Multiplier**: In a 6-die System-in-Package, unverified dies compound failure rates ($0.95^6 = 73.5\%$ yield). Every die must undergo Known-Good-Die (KGD) wafer-level testing prior to assembly.

### 2. Multi-Batch Material Requirements for Approval
- **The Pitfall**: A single MPW shuttle provides wafers from only one manufacturing lot. Military screening mandates samples across multiple independent fab runs to verify batch-to-batch process tolerance.
- **Round Sizing**: The ₹10 Cr round deliberately funds complete qualification for **four pathfinder chips** (Chips 1, 2, 3, 6) rather than underfunding all ten.

### 3. Organizational Approval (Auditing the Company, Not Just the Chip)
- **Customer Audit Scope**: Aerospace and defence buyers (DRDO, BEL, HAL) audit vendor quality management systems before placing component purchase orders.
- **Prerequisites**:
  - ISO 9001 / AS9100 quality certifications.
  - Documented Engineering Change Notification (ECN) procedures.
  - Strict ESD/EOS facility handling controls.
  - Guaranteed 10–20 year longevity and Last-Time-Buy (LTB) supply policies.

---

## Key Takeaways
1. Budget ₹40–80 Lakhs per SKU for characterisation and qualification; capital cannot shorten calendar test times.
2. ATE test programs and load boards are the primary operational bottleneck before volume manufacturing.
3. Defence and automotive clients approve the supplier's quality system (ISO 9001/AS9100) before approving the chip.

---

## Connects To
- **Ch 5**: The 198-day loop and post-silicon schedule buffers.
- **Ch 13**: Capital allocation for qualification (₹1.8 Cr) and ATE testing (₹1.2 Cr).
