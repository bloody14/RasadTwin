# DATABASE SCHEMA V2 (MVP TARGET)

This represents the minimal viable full-project PostgreSQL/PostGIS schema. 

## 1. DATA SOURCES & PROVENANCE (P0)
**Table: `data_sources`** (Reference)
- `id` (UUID, PK)
- `provider` (VARCHAR)
- `dataset_name` (VARCHAR)
- `data_class` (VARCHAR) - ENUM: 'PUBLIC_REAL', 'SYNTHETIC'
- `license` (VARCHAR)
- `source_uri` (VARCHAR)
- `version` (VARCHAR)
- `retrieved_at` (TIMESTAMP)
- `spatial_scope` (GEOMETRY(Polygon, 4326))
- `description` (TEXT)

## 2. NODES (P0)
**Table: `nodes`** (Mutable State)
- `id` (VARCHAR, PK) - e.g., 'FP-001'
- `name` (VARCHAR)
- `node_type` (VARCHAR) - ENUM: 'DEPOT', 'INTERMEDIATE_HUB', 'FORWARD_POST'
- `priority` (INTEGER)
- `status` (VARCHAR)
- `synthetic_flag` (BOOLEAN) - Must be TRUE for operational military nodes
- `data_source_id` (UUID, FK -> data_sources.id)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)
- `geometry` (GEOMETRY(Point, 4326))

## 3. ROUTES & ROUTE LEGS (P0)
**Table: `routes`** (Reference)
- `id` (VARCHAR, PK) - Logical route ID
- `name` (VARCHAR)
- `status` (VARCHAR)

**Table: `route_legs`** (Mutable State)
- `id` (VARCHAR, PK)
- `route_id` (VARCHAR, FK -> routes.id)
- `source_node` (VARCHAR, FK -> nodes.id)
- `target_node` (VARCHAR, FK -> nodes.id)
- `mode` (VARCHAR) - ENUM: 'ROAD', 'MULE', 'HELI', 'DRONE'
- `distance` (FLOAT)
- `base_eta` (FLOAT)
- `robust_eta` (FLOAT)
- `capacity` (FLOAT)
- `terrain_risk` (VARCHAR)
- `weather_risk` (VARCHAR)
- `closure_state` (BOOLEAN)
- `geometry` (GEOMETRY(LineString, 4326))

## 4. FLEET ASSETS (P0)
**Table: `fleet_assets`** (Mutable State)
- `asset_id` (UUID, PK)
- `asset_class` (VARCHAR) - ENUM: 'ROAD', 'MULE', 'HELI', 'DRONE'
- `capacity_kg` (FLOAT)
- `range_km` (FLOAT)
- `speed` (FLOAT)
- `status` (VARCHAR)
- `current_node_id` (VARCHAR, FK -> nodes.id)
- `weather_constraints` (JSONB)
- `terrain_constraints` (JSONB)
- `energy_fuel_constraints` (FLOAT)
- `maintenance_state` (VARCHAR)

## 5. INVENTORY & DEMAND (P0 / P1)
**Table: `inventory`** (Mutable State)
- `id` (UUID, PK)
- `node_id` (VARCHAR, FK -> nodes.id)
- `item_class` (VARCHAR)
- `quantity` (FLOAT)
- `unit` (VARCHAR)
- `target_quantity` (FLOAT)
- `days_of_supply` (FLOAT)
- `last_updated` (TIMESTAMP)
- `priority` (INTEGER)

**Table: `demand_series`** (Time-Series)
- `id` (UUID, PK)
- `node_id` (VARCHAR, FK -> nodes.id)
- `item_class` (VARCHAR)
- `timestamp` (TIMESTAMP)
- `observed_demand` (FLOAT)
- `forecast_demand` (FLOAT)
- `lower_bound` (FLOAT)
- `upper_bound` (FLOAT)
- `model_version` (VARCHAR)
- `confidence_level` (FLOAT)

## 6. WEATHER & TERRAIN (P1)
**Table: `weather_snapshots`** (Time-Series)
- `id` (UUID, PK)
- `timestamp` (TIMESTAMP)
- `region_geom` (GEOMETRY(Polygon, 4326))
- `temperature` (FLOAT)
- `precipitation` (FLOAT)
- `snow` (FLOAT)
- `wind` (FLOAT)
- `visibility` (FLOAT)
- `weather_risk` (VARCHAR)
- `provider` (VARCHAR)
- `source_version` (VARCHAR)

**Table: `terrain_segments`** (Reference)
- `id` (UUID, PK)
- `geometry` (GEOMETRY(Polygon, 4326))
- `elevation` (FLOAT)
- `slope` (FLOAT)
- `elevation_gain` (FLOAT)
- `terrain_class` (VARCHAR)
- `terrain_risk` (VARCHAR)
- `source` (VARCHAR)
- `source_version` (VARCHAR)

## 7. DISRUPTIONS & IMPACTS (P0)
**Table: `disruptions`** (Mutable State)
- `id` (UUID, PK)
- `scenario_type` (VARCHAR) - ENUM: 'ROAD_CLOSURE', 'HEAVY_SNOW', 'LANDSLIDE', etc.
- `status` (VARCHAR)
- `start_time` (TIMESTAMP)
- `end_time` (TIMESTAMP)
- `geometry` (GEOMETRY(Polygon, 4326))
- `severity` (INTEGER)
- `source_type` (VARCHAR)
- `source_id` (VARCHAR)
- `description` (TEXT)

**Table: `impact_assessments`** (Mutable State)
- `id` (UUID, PK)
- `disruption_id` (UUID, FK -> disruptions.id)
- `impact_score` (INTEGER)
- `affected_nodes` (JSONB)
- `affected_legs` (JSONB)
- `delay_hours` (FLOAT)
- `service_risk` (VARCHAR)
- `inventory_impact` (FLOAT)
- `network_impact` (VARCHAR)
- `recommended_scope` (VARCHAR)
- `reason` (TEXT)
- `computed_at` (TIMESTAMP)

## 8. GOVERNANCE: DECISIONS & AUDIT (P0)
**Table: `recommendations`** (Append-Only)
- `id` (UUID, PK)
- `impact_assessment_id` (UUID, FK -> impact_assessments.id)
- `recommended_scope` (VARCHAR) - ENUM: 'PRESERVE', 'LOCAL', 'GLOBAL'
- `reason` (TEXT)
- `model_version` (VARCHAR)
- `created_at` (TIMESTAMP)

**Table: `decisions`** (Append-Only)
- `id` (UUID, PK)
- `recommendation_id` (UUID, FK -> recommendations.id)
- `scenario` (VARCHAR)
- `system_recommendation` (VARCHAR)
- `user_action` (VARCHAR) - ENUM: 'APPROVE', 'REJECT', 'OVERRIDE'
- `selected_scope` (VARCHAR)
- `actor` (VARCHAR)
- `reason` (TEXT)
- `timestamp` (TIMESTAMP)

**Table: `audit_events`** (Append-Only)
- `id` (UUID, PK)
- `timestamp` (TIMESTAMP)
- `actor` (VARCHAR) - ENUM: 'SYSTEM', 'ENGINE', 'COMMANDER'
- `event_type` (VARCHAR)
- `scenario` (VARCHAR)
- `system_recommendation` (VARCHAR)
- `user_action` (VARCHAR)
- `selected_scope` (VARCHAR)
- `reason` (TEXT)
- `entity_type` (VARCHAR)
- `entity_id` (VARCHAR)

## 9. FUTURE: KNOWLEDGE & RAG (P2 - DO NOT IMPLEMENT NOW)
- `knowledge_documents`
- `embeddings` (pgvector)

---

## CENTRAL VS EDGE MAPPING
- **Central**: `data_sources`, `nodes` (Global), `routes` (Global), `route_legs` (Global), `fleet_assets`, `inventory` (Global), `demand_series`, `weather_snapshots`, `terrain_segments`, `disruptions`, `impact_assessments`, `recommendations`, `decisions`, `audit_events` (Full Ledger).
- **Edge**: `nodes` (Local Slice), `route_legs` (Local Slice), `inventory` (Local), `demand_series` (Recent Buffer), `audit_events` (Local Queue), `decisions` (Local Queue).

## SPATIAL STRATEGY & INDEXING
- **SRID**: WGS 84 (4326).
- **Types**: Use `GEOMETRY` with explicit SRID for efficient bounding-box queries, cast to `GEOGRAPHY` for strict distance measurements when rendering robust ETAs.
- **Indexes**: 
  - GIST indexes on all `geometry` columns.
  - B-Tree indexes on FKs (`node_id`, `route_id`, `disruption_id`).
  - BRIN or B-Tree indexes on time-series `timestamp` columns.
  - Unique composite index on `(node_id, item_class)` for inventory snapshots.

## API MAPPING COMPATIBILITY
- **GET /posts**: `SELECT * FROM nodes`
- **GET /routes**: `SELECT * FROM route_legs JOIN routes`
- **GET /weather**: `SELECT * FROM weather_snapshots`
- **GET /risk/{post_id}**: Requires JOINS across `nodes`, `inventory`, `demand_series`
- **GET /forecast/{post_id}**: `SELECT * FROM demand_series`
- **POST /what-if**: Inserts to `disruptions`, generates `impact_assessments` and `recommendations`. Returns structured payload.
- **POST /decision**: Inserts to `decisions` and `audit_events`.
- **GET /audit**: `SELECT * FROM audit_events`
