# DATABASE SCHEMA GAP ANALYSIS

This document compares the current Phase 3 structures (`DEMO_POSTS`, `DEMO_ROUTES`, SQLite `audit_log`) against the required Phase 4 target PostgreSQL architecture.

| DOMAIN | CURRENT TABLE / MODEL | TARGET TABLE | MISSING? | REASON | PRIORITY |
|---|---|---|---|---|---|
| **NODE** | `DEMO_POSTS` (List) | `nodes` | YES (No DB Table) | Operational state needs persistence and spatial querying. | **P0** |
| **DEPOT** | `type="rear_depot"` | `nodes` (node_type) | NO | Distinguishable via `node_type`. | **P0** |
| **INTERMEDIATE HUB** | `type="intermediate_depot"` | `nodes` (node_type) | NO | Distinguishable via `node_type`. | **P0** |
| **FORWARD POST** | `type="forward_post"` | `nodes` (node_type) | NO | Distinguishable via `node_type`. | **P0** |
| **ROUTE** | N/A (Mixed) | `routes` | YES | Needs logical abstraction above physical legs. | **P0** |
| **ROUTE LEG** | `DEMO_ROUTES` (List) | `route_legs` | YES (No DB Table) | Physical paths requiring distinct geometries and modes. | **P0** |
| **FLEET ASSET** | N/A | `fleet_assets` | YES | Explicit capabilities (capacity, weather constraints) required for realistic routing. | **P0** |
| **INVENTORY** | `dos` field in `DEMO_POSTS` | `inventory` | YES | Needs distinct snapshot decoupling from the static node definition. | **P0** |
| **DEMAND SERIES** | `get_forecast` mock | `demand_series` | YES | Crucial for integrating actual E1 LightGBM outputs securely. | **P1** |
| **WEATHER STATE** | `get_weather` mock | `weather_snapshots` | YES | Required to overlay hazard polygons on route legs. | **P1** |
| **TERRAIN STATE** | N/A | `terrain_segments` | YES | Required for SRTM elevation integration affecting route speeds. | **P1** |
| **DISRUPTION** | `WhatIfRequest` (String) | `disruptions` | YES | Must persist as a spatial geometry (e.g., Road Closure Polygon). | **P0** |
| **IMPACT ASSESSMENT** | Computed on-the-fly | `impact_assessments` | YES | Must be persisted to link recommendations to specific hazards. | **P0** |
| **RECOMMENDATION** | Computed on-the-fly | `recommendations` | YES | AI suggestion (LOCAL/GLOBAL/PRESERVE) must be saved before HITL. | **P0** |
| **DECISION** | Overloaded in `audit_log` | `decisions` | YES | Dedicated table for explicit User Action vs Selected Scope tracking. | **P0** |
| **AUDIT EVENT** | SQLite `audit_log` | `audit_events` | PARTIAL | Exists in SQLite, but must migrate to PostgreSQL for HQ central analysis. | **P0** |
| **DATA SOURCE** | N/A | `data_sources` | YES | Strict requirement for REAL vs SYNTHETIC tracking and provenance. | **P0** |
