# POSTGRESQL MIGRATION PLAN (PHASE 4B)

This document outlines the step-by-step strategy to migrate RasadTwin from its Phase 3 in-memory/SQLite architecture to the target PostgreSQL/PostGIS environment.

## 1. MIGRATION RISKS & MITIGATIONS
- **Schema Drift Risk** (High): If the database schema evolves faster than the FastAPI endpoints.
  *Mitigation*: Use Alembic for strict migration versioning.
- **Dependency Mismatch Risk** (Medium): Missing OS-level libraries for GeoAlchemy2 or psycopg2.
  *Mitigation*: Execute via Docker (`postgis/postgis` image) to abstract host OS dependencies.
- **API Contract Breakage** (Medium): Changing from dictionary lists to SQLAlchemy objects might break Pydantic serialization.
  *Mitigation*: Update Pydantic `orm_mode = True` (or `from_attributes = True` in Pydantic v2) before cutting over.
- **Disk/RAM Pressure** (Low): Current system has 16GB RAM and ~30GB free disk, which is adequate for a Dockerized PostGIS instance, but large OSM data ingest could cause strain.
  *Mitigation*: Limit geographical data bounding boxes strictly to the designated study region.

## 2. RECOMMENDED IMPLEMENTATION METHOD
**Method B: Docker PostgreSQL/PostGIS**
*Rationale*: The host machine runs Windows, lacks native `psql`, and lacks `psycopg2`/`geoalchemy2` dependencies in the active Python environment. Using the official `postgis/postgis:15-3.3` Docker image circumvents Windows pathing issues and prevents polluting the host OS, making it the safest and fastest route.

## 3. MIGRATION STAGES

### STAGE 1: Infrastructure & Schema Generation
1. Spin up `postgis/postgis` via Docker Compose.
2. Install Python dependencies: `SQLAlchemy`, `Alembic`, `GeoAlchemy2`, `psycopg2-binary`.
3. Initialize Alembic and define the declarative base models in `src/rasadtwin/db/models.py` (matching the structures defined in `DATABASE_SCHEMA_PLAN.md`).
4. Generate and apply the initial Alembic migration.

### STAGE 2: Synthetic Seed Data
1. Write a Python seed script (`db/seeds.py`).
2. Translate the hardcoded `DEMO_POSTS` and `DEMO_ROUTES` from `main.py` into SQLAlchemy insertions.
3. Use `ST_MakePoint(lng, lat)` to populate the PostGIS geometry columns.
4. Execute the seed script against the Docker database.

### STAGE 3: API Data Access Layer Refactoring
1. Create a database session dependency (`get_db`) in FastAPI.
2. Refactor endpoints (`/posts`, `/routes`, `/audit`) to query the PostgreSQL database via SQLAlchemy instead of returning static lists.
3. Ensure Pydantic response models remain 100% identical to the current UI expectations.

### STAGE 4: Validation
1. Start the updated backend.
2. Run the frontend.
3. Execute the existing Playwright E2E test suite.
4. If tests pass (visual map renders, paths calculate, HITL works), the migration is complete.

### STAGE 5: Edge Cache Preparation (Future)
- Once Central DB is stable, replicate the SQLAlchemy models to point to local SQLite engines for the Edge architecture phase.

## 4. API COMPATIBILITY AUDIT
The current API endpoints are highly compatible with relational data:
- `GET /posts`: Will map directly to `SELECT * FROM nodes`.
- `GET /routes`: Will map to `SELECT * FROM routes`.
- `GET /risk/{id}`: Will join `nodes`, `inventory`, and `weather_snapshots`.
- `POST /what-if`: Will trigger spatial impact logic (e.g., `ST_Intersects` against a hazard polygon) instead of hardcoded string matching.
- `POST /decision` & `GET /audit`: Will map perfectly to `audit_events`.
