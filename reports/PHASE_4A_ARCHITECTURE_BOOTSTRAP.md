# PHASE 4A: LONG-TERM PROJECT GOVERNANCE & ARCHITECTURE BOOTSTRAP

## OVERVIEW
Phase 4A marks the transition of RasadTwin from a purely functional vertical-slice demonstrator into a scalable, enterprise-grade Digital Twin. This bootstrap phase is entirely read-only, establishing strict governance, data policies, and architectural boundaries without disturbing the validated E1 research or the working Phase 3 UI.

## CURRENT ARCHITECTURE
RasadTwin currently utilizes a lightweight React/Vite/Tailwind frontend communicating with a FastAPI/Uvicorn backend. State is managed deterministically via in-memory Python structures, with a local SQLite `demo_state.db` tracking HITL (Human-in-the-loop) audits. The geospatial implementation uses a responsive, dependency-free SVG canvas. E1 forecasting runs asynchronously via LightGBM and Chronos models.

## TARGET ARCHITECTURE
The future architecture encapsulates 15 distinct layers (A-O), stretching from the Presentation UI down through Forecasting (E1), Multi-Modal Routing, What-If Impact parsing, and an Optional RAG Knowledge retrieval engine. The system embraces an Offline-First philosophy, prioritizing edge resiliency.

## DATABASE ARCHITECTURE
The long-term state transitions to a hybrid model:
1. **Central HQ**: PostgreSQL + PostGIS (handles complex routing, node geometry, global inventory).
2. **Edge Node**: SQLite (handles intermittent caching, audit queues, and local state).
3. **Knowledge Retrieval**: pgvector (optional, indexes SOPs/manuals). *Note: RAG is strictly an auxiliary explainability layer, not the operational database.*

## DATA POLICY
Strictly enforced boundaries:
- **Public Data**: OS mapping, SRTM elevation, public weather APIs.
- **Synthetic Data**: ALL operational logistics data (demand, inventory, post coordinates, fleet capability).
- **Prohibited Data**: Real military coordinates, weapons data, live surveillance.

## OFFLINE MODEL
The application gracefully degrades across three states: Online (Real-time PG sync), Weak Network (API fallback to Cache, throttled sync), and Offline (Air-gapped SQLite operations appending to a local sync-queue).

## FLEET DOMAIN MODEL
The multi-modal transport network is bound by specific constraints:
- **Road**: High capacity, constrained by snow/mud.
- **Mule**: Low capacity, weather-resilient, slow.
- **Heli**: Long range, fast, constrained by wind/visibility.
- **Drone**: Fast, low payload, constrained by battery.

## COMMANDER WORKFLOW
SENSE → PREDICT → INVENTORY → ROUTE → SIMULATE → IMPACT → SYSTEM RECOMMENDS (PRESERVE/LOCAL/GLOBAL) → HITL REVIEW → UPDATED PLAN → AUDIT → DT UPDATE.

## PROJECT MEMORY & GOVERNANCE
Antigravity context is localized to `.agents/rules/` containing strict Markdown invariants (00-project-invariants.md through 99-git-change-control.md). Repetitive tasks (E2E, Security Audits) will be bound to reusable Agent Skills.

## PLUGIN & MCP STRATEGY
Cloud-dependent APIs are prohibited by design to maintain air-gapped viability. Database inspection (PG MCP) and Browser Testing MCPs are highly recommended for future phases, whereas GitHub MCPs remain secondary. No API keys are required for the MVP due to the reliance on Open-Meteo and OSM.

## ADR LEDGER
Architectural decisions (ADR-001 through ADR-008) have been bootstrapped, logging the rationale behind the PostgreSQL adoption, the HITL semantic separation, and the Synthetic Data policies.

## PHASE ROADMAP
- **P4A**: Governance (Complete)
- **P4B**: Data platform (PostgreSQL)
- **P4C**: Real geospatial study area (OSM ingest)
- **P4D**: Terrain/environment
- **P4E**: Routing
- **P4F**: Digital twin state
- **P4G**: Knowledge/RAG
- **P4H**: Offline/edge sync
- **P4I**: Full integrated dashboard
- **P4J**: Validation

---

## COPY-PASTE SUMMARY FOR CHATGPT

COPY-PASTE SUMMARY FOR CHATGPT

STATUS:
PASS

CURRENT_REPO:
c:\Users\user\OneDrive\Desktop\RasadTwin\RasadTwin_Governance_Pack\rasadtwin_governance_pack

CURRENT_ARCHITECTURE:
React/Vite SVG UI + FastAPI backend + in-memory Python state + SQLite audit + isolated E1 ML pipeline.

TARGET_ARCHITECTURE:
15-layer enterprise system integrating PostGIS spatial routing, dynamic weather overlay, multi-modal optimization, HITL governance, and robust offline sync.

DATABASE:
PostgreSQL/PostGIS (Central) + SQLite (Edge) + Optional pgvector (Knowledge)

RAG_ROLE:
Auxiliary semantic retrieval for SOPs/Doctrine ONLY. It does not replace the relational logistics database.

REAL_DATA:
Public terrain, weather, and road networks (OSM, SRTM, Open-Meteo).

SYNTHETIC_DATA:
Fictional military posts, simulated inventory, dummy fleet capacities, synthetic demand.

OFFLINE_MODEL:
Edge UI falls back to local SQLite. Disruption impacts and HITL actions are queued locally via transaction ledger and synced to HQ upon network restoral.

FLEET_MODEL:
Road, Mule, Heli, Drone (each bounded by distinct capacity, speed, and weather constraints).

LOGISTICS_MODEL:
Hierarchical flow (Depot -> Hub -> Post) bounded by Inventory Position, Demand Series, and dynamically traversable Route Legs.

COMMANDER_WORKFLOW:
Sense -> Predict -> Route -> Simulate Hazard -> Impact -> System Suggestion -> HITL Approval -> Audit Ledger.

PROJECT_MEMORY:
Governed via `.agents/rules/` enumerating strict project invariants, security thresholds, and domain logic to prevent AI hallucination.

PLUGIN_STRATEGY:
Favor air-gapped execution. Browser E2E validation plugins recommended.

MCP_STRATEGY:
PostgreSQL MCP and Playwright MCP recommended for future phases. Cloud LLM MCPs rejected for production air-gap requirements.

API_KEY_REQUIREMENTS:
None required. Open-Meteo and local models prioritized.

PROPOSED_FOLDER_STRUCTURE:
Strict separation of `/src/rasadtwin/db`, `/src/rasadtwin/geo`, and `/edge` sync clients.

ADRS:
ADR-001 through ADR-008.

PHASE_ROADMAP:
P4A (Governance) -> P4B (Data Platform) -> P4C (Geo) -> P4D (Environment) -> P4E (Routing) -> P4F (State) -> P4G (RAG) -> P4H (Offline) -> P4I (Integration) -> P4J (Validation).

CODE_CHANGED:
NO

E1_CHANGED:
NO

DATA_DOWNLOADED:
NO

PLUGINS_INSTALLED:
NO

MCP_INSTALLED:
NO

FILES_CREATED:
- docs/CURRENT_ARCHITECTURE.md
- docs/FULL_PROJECT_TARGET_ARCHITECTURE.md
- docs/DATA_PLATFORM_ARCHITECTURE.md
- docs/OFFLINE_EDGE_ARCHITECTURE.md
- docs/PROJECT_MEMORY_AND_AGENT_GOVERNANCE.md
- docs/PLUGIN_MCP_STRATEGY.md
- docs/ADR/README.md
- reports/PHASE_4A_ARCHITECTURE_BOOTSTRAP.md

NEXT_ACTION:
Phase 4A complete. Ready to proceed to Phase 4B (Data Platform Implementation).
