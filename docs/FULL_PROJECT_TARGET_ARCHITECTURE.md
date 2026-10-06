# FULL-PROJECT TARGET ARCHITECTURE

This document outlines the target architectural boundaries for the long-term RasadTwin system.

## A. PRESENTATION / UI LAYER
React/Vite dashboard providing tactical oversight. Emphasis on minimal network payload, SVG-based declarative data visualization, and immediate state-change feedback for command decisions.

## B. API / SERVICE LAYER
FastAPI bridging the UI and the Digital Twin Engine. Handles authentication, request validation, caching, and offline-sync queuing.

## C. DIGITAL TWIN STATE LAYER
The single source of truth for the active logistics network. Merges physical telemetry (synthetic) with logical states (inventory levels, active disruptions, active dispatch).

## D. FORECASTING LAYER
Statistical and ML forecasting engine (derived from E1). Subscribes to demand telemetry and produces bounded uncertainty forecasts for each node.

## E. INVENTORY OPTIMIZATION LAYER
Calculates target `Days of Supply` (DoS), safety stock, and stock-out probabilities based on the output of the Forecasting layer and current replenishment rates.

## F. ROUTING / OPTIMIZATION LAYER
Multi-modal graph traversal engine. Calculates robust ETAs and alternative paths when edge constraints change. Supports constraints per mode (e.g., Drone weight limits, Heli weather limits).

## G. DISRUPTION / IMPACT ENGINE
The core "What-If" service. Accepts environmental triggers or hypothetical hazards, overlays them on the Geospatial layer, recalculates edge traversability, and scores network-wide impact.

## H. DECISION / HITL LAYER
Asynchronous governance layer. Halts execution of autonomous execution if impact > threshold. Awaits Commander input (`APPROVE`, `REJECT`, `OVERRIDE`), applies the decision, and releases the network lock.

## I. EXPLAINABILITY LAYER
SHAP/Feature-importance extractor. Translates complex routing or forecasting deviations into human-readable narratives (e.g., "Route 1 disabled due to 45% avalanche probability").

## J. AUDIT / GOVERNANCE LAYER
Immutable append-only ledger of all state mutations, specifically tagging automated system recommendations vs. human overrides for post-action review.

## K. GEOSPATIAL LAYER
PostGIS-backed spatial engine handling coordinates, terrain traversal rules, and distance calculations.

## L. ENVIRONMENTAL / WEATHER LAYER
Time-series weather data ingest. Maps meteorological phenomenon to spatial bounds to dynamically update route risk coefficients.

## M. DATA PLATFORM
Core storage infrastructure. Centralized PostgreSQL/PostGIS database handling the global state, connected via ETL pipelines to external real-world terrain/weather APIs.

## N. OFFLINE / EDGE LAYER
SQLite-backed edge cache operating in forward command posts. Handles intermittent connectivity, queuing HITL decisions, and syncing deltas when network returns.

## O. KNOWLEDGE / RAG LAYER (Optional)
Vector-based semantic search engine containing standard operating procedures (SOPs), maintenance manuals, and military logistics doctrine to answer Commander queries. *Note: This is a retrieval system, not the core relational database.*

---

## CONCEPTUAL DOMAIN MODELS

### 1. FLEET DOMAIN MODEL
- **Road Vehicles**: High capacity, high range, moderate speed. Constrained by road network and severe weather (snow/mud).
- **Mules**: Low capacity, low range, low speed. Highly resilient to terrain and weather. Requires biological rest constraints.
- **Helicopters**: Moderate capacity, long range, high speed. Constrained strictly by visibility, high wind, and altitude ceilings.
- **Drones**: Low capacity, short range, high speed. Constrained by battery life (energy), wind shear, and payload weight.

### 2. LOGISTICS DOMAIN MODEL
- **Nodes**: `Depot` (infinite source), `Intermediate Hub` (buffer), `Forward Post` (sink).
- **Edges**: `Route`, `Route Leg`.
- **State**: `Inventory Position`, `Demand Series`, `Weather State`, `Terrain State`.
- **Workflow**: `Disruption` -> `Impact Assessment` -> `Recommendation` -> `Decision` -> `Audit Event`.

## COMMANDER WORKFLOW (E2E)
1. **SENSE**: Ingest weather and terrain updates.
2. **PREDICT**: Forecast demand dynamically.
3. **INVENTORY**: Identify low DoS thresholds.
4. **ROUTE**: Compute standard replenishment path.
5. **SIMULATE**: Detect hazard and trigger What-If.
6. **IMPACT**: Score hazard scope.
7. **PRESERVE / LOCAL / GLOBAL**: System dictates replan boundary.
8. **HUMAN APPROVAL**: Commander reviews Before/After.
9. **UPDATED PLAN**: Active routes shift to alternate modes.
10. **AUDIT**: Immutable ledger records the decision.
11. **DIGITAL TWIN UPDATE**: Current working state synchronizes to match the decision.
