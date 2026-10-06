# DATABASE SCHEMA PLAN

This document details the minimum viable PostgreSQL/PostGIS schema to migrate RasadTwin from its Phase 3 in-memory state to a robust relational data platform.

## 1. SPATIAL DATA MODEL
- **Coordinate Reference Strategy**: WGS 84 (SRID 4326) for standard geographic coordinates (latitude/longitude), mapped to geography types for accurate distance calculations.
- **Node Geometry**: `POINT(lon lat)`.
- **Edge Geometry**: `LINESTRING(lon lat, lon lat)` representing route legs.
- **Hazard/Weather Geometry**: `POLYGON` or `MULTIPOLYGON` for bounding boxes representing weather fronts or disruption zones.

## 2. TABLE DEFINITIONS

### `nodes`
- **Purpose**: Unified table for all logistics locations (Depots, Hubs, Forward Posts).
- **Primary Key**: `id` (VARCHAR) e.g., 'FP-001'.
- **Fields**: `name` (VARCHAR), `node_type` (VARCHAR), `dos` (INTEGER), `base_risk` (VARCHAR), `priority` (INTEGER).
- **Spatial Column**: `geom` (GEOMETRY(Point, 4326)).
- **Placement**: Central + Edge (Filtered subset).

### `routes` (Edges)
- **Purpose**: Defines connectivity between nodes and traversal constraints.
- **Primary Key**: `id` (VARCHAR) e.g., 'R-001'.
- **Fields**: `mode` (VARCHAR), `distance_km` (FLOAT), `base_eta_hrs` (FLOAT), `status` (VARCHAR).
- **Foreign Keys**: `source_id` -> `nodes(id)`, `target_id` -> `nodes(id)`.
- **Spatial Column**: `geom` (GEOMETRY(LineString, 4326)).
- **Placement**: Central + Edge (Filtered subset).

### `fleet_assets`
- **Purpose**: Tracking specific transport assets assigned to the network.
- **Primary Key**: `id` (UUID).
- **Fields**: `asset_class` (VARCHAR: Road/Mule/Heli/Drone), `capacity_kg` (FLOAT), `range_km` (FLOAT), `status` (VARCHAR), `current_node_id` (VARCHAR).
- **Placement**: Central + Edge.

### `inventory`
- **Purpose**: Time-series or current snapshot of stock per node.
- **Primary Key**: `id` (UUID).
- **Fields**: `node_id` (VARCHAR), `item_class` (VARCHAR), `quantity` (FLOAT), `last_updated` (TIMESTAMP).
- **Foreign Keys**: `node_id` -> `nodes(id)`.
- **Placement**: Central + Edge (Local Node Only).

### `weather_snapshots`
- **Purpose**: Environmental conditions dynamically affecting routing.
- **Primary Key**: `id` (UUID).
- **Fields**: `timestamp` (TIMESTAMP), `temperature` (VARCHAR), `snow_condition` (VARCHAR), `wind` (VARCHAR), `terrain_risk` (VARCHAR).
- **Spatial Column**: `region_geom` (GEOMETRY(Polygon, 4326)).
- **Placement**: Central.

### `audit_events`
- **Purpose**: Immutable ledger of HITL and system-level actions.
- **Primary Key**: `id` (UUID).
- **Fields**: `timestamp` (TIMESTAMP), `user_id` (VARCHAR), `action` (VARCHAR), `scenario` (VARCHAR), `system_recommendation` (VARCHAR), `user_action` (VARCHAR), `selected_scope` (VARCHAR), `reason` (TEXT).
- **Placement**: Central (Master Ledger) + Edge (Sync Queue).

## 3. RAG BOUNDARY & FUTURE EXPANSION
- The `pgvector` extension will NOT be used for operational logistics tables (Nodes, Routes, Inventory).
- It is reserved exclusively for a future `knowledge_documents` table to store text chunks and vector embeddings of SOPs and military doctrine. This ensures a strict physical boundary between the operational Digital Twin state and the Generative AI retrieval layer.

## 4. CENTRAL vs. EDGE DISTRIBUTION
- **Central PostgreSQL**: Holds the complete spatial network, all historical `audit_events`, the entire `weather_snapshots` history, and global `inventory`.
- **Edge SQLite**: Holds a localized spatial slice of `nodes` and `routes`, current `inventory` for the immediate area, and acts as a local append-only queue for `audit_events` until synchronization.
