# DATA PLATFORM ARCHITECTURE

## 1. STORAGE ENGINES
- **PostgreSQL + PostGIS**: The central operational database. Handles all relational data (nodes, edges, fleet, inventory, audit) and complex spatial queries (radius searches, route intersections).
- **SQLite**: Edge-deployed database. Runs locally on the frontend server/client for offline-first capabilities.
- **pgvector (Optional)**: A PostgreSQL extension to store embeddings of unstructured text (SOPs, doctrines, manuals) for the RAG (Retrieval-Augmented Generation) layer.

## 2. CENTRAL vs. EDGE DATA
- **Central Data (HQ)**: Contains the global network state, historical demand series, complete audit history, and large-scale geographic geometries.
- **Edge Local Data (Forward Post)**: A synced subset of the central DB containing only the spatial slice relevant to that specific command post, current active routes, and a rolling 72-hour forecast buffer.
- **Knowledge Retrieval**: Pulled from Central on-demand (if online) or packaged into a static local vector index (if offline).

## 3. REAL vs. SYNTHETIC DATA POLICY

**REAL PUBLIC DATA (Allowed)**
- Public road networks (OSM).
- Public elevation/terrain maps (SRTM).
- Public meteorological data (Open-Meteo, NOAA).
- Public disaster/hazard alerts.

**SYNTHETIC DATA (Mandatory for Operations)**
- Military logistics network state.
- Forward-post identities, coordinates, and names.
- Troop sizes, inventory counts, and demand rates.
- Fleet availability and asset capacities.
- Fictional disruption scenarios.

**RESTRICTED / NEVER USE**
- Real operational Army positions.
- Sensitive or classified military routes.
- Targeting or weapons data.
- Live surveillance data.

## 4. DATA PIPELINE
1. **Public Data Ingest**: CRON jobs pull public weather/terrain updates.
2. **Raw Storage**: Dumped to blob storage or raw PG tables.
3. **Validate & Normalize**: Ensure schemas match, drop bad data.
4. **Process**: Overlay synthetic logistics coordinates onto the real public geospatial map.
5. **Digital Twin State**: Update the active operational tables (Current Inventory, Active Routes).
6. **AI / Optimization**: E1 Forecasting and Routing engines pull from State, pushing predictions back.
7. **Local Cache Sync**: Deltas pushed to Edge SQLite databases.
8. **UI Rendering**: Dashboard queries Edge or Central API to visualize state.
