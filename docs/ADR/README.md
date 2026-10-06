# ARCHITECTURE DECISION RECORDS (ADR)

This directory contains the historical ledger of major architectural decisions made during the RasadTwin lifecycle.

## PROPOSED ADR INDEX

- **ADR-001**: Synthetic Operational Data Policy (Defines the strict boundary separating public geographic data from fictional military logistics).
- **ADR-002**: PostgreSQL/PostGIS Core Data Architecture (Adoption of PG for spatial and relational state management).
- **ADR-003**: SQLite Edge Cache (Offline-first architecture for degraded command posts).
- **ADR-004**: Real Public Geography + Synthetic Logistics Overlay (Methodology for geospatial mapping without exposing real military infrastructure).
- **ADR-005**: Optional pgvector RAG Layer (Knowledge retrieval architecture for doctrine/SOPs).
- **ADR-006**: Offline-First Synchronization (Queue and CRDT-based reconciliation strategies).
- **ADR-007**: HITL Governance (Strict separation of `system_recommendation`, `user_action`, and `selected_scope`).
- **ADR-008**: Multi-Modal Routing Engine (Road, Heli, Mule, Drone constraints).

*Note: These ADRs are conceptually outlined and pending formal implementation in subsequent phases.*
