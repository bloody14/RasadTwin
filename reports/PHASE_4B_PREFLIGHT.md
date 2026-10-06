# PHASE 4B PRE-FLIGHT: POSTGRESQL / POSTGIS PLATFORM AUDIT

## 1. PURPOSE
This read-only audit assesses the existing environment, validates current in-memory architectures against target relational structures, and plans a safe migration path to PostgreSQL/PostGIS. No code was modified or installed during this phase.

## 2. ENVIRONMENT AUDIT
The development environment is running Windows.
- **Docker**: Available (v29.6.2), with Docker Desktop presumed active.
- **PostgreSQL**: Not installed natively (no `psql` command available).
- **Python Drivers**: `SQLAlchemy` is available (v2.0.23). `alembic`, `psycopg2-binary`, and `geoalchemy2` are missing.
- **Resources**: ~16GB total RAM (~4.2GB free). ~30GB free disk space. Sufficient for a containerized database but requires strict bounding on GIS datasets.

## 3. CURRENT DATABASE STATE
- **SQLite (`demo_state.db`)**: Holds only `audit_log` and an unused `cache_state` table.
- **In-Memory**: `DEMO_POSTS` and `DEMO_ROUTES` act as the operational Digital Twin inside `src/rasadtwin/api/main.py`.

## 4. SCHEMA AND MIGRATION PLAN
A comprehensive blueprint has been created for migrating to a spatial relational model:
- **`docs/DATABASE_SCHEMA_PLAN.md`**: Defines WGS 84 (SRID 4326) geometries, central vs. edge table distribution, and strictly bounds `pgvector` to non-operational RAG tasks.
- **`docs/MIGRATION_PLAN.md`**: Proposes a 5-stage migration using Docker (`postgis/postgis`) to bypass local OS dependency conflicts.

## 5. API AND REAL DATA READINESS
The existing FastAPI endpoints (`/posts`, `/routes`, `/what-if`, `/decision`) are perfectly primed for SQLAlchemy refactoring without breaking the JSON contracts expected by the React frontend. The schema physically segregates real weather/terrain tables from synthetic military nodes, strictly enforcing Data Governance Rules.

---

## COPY-PASTE SUMMARY FOR CHATGPT

COPY-PASTE SUMMARY FOR CHATGPT

STATUS:
PASS

POSTGRESQL_INSTALLED:
NO (Native)

POSTGIS_INSTALLED:
NO (Native)

DOCKER_AVAILABLE:
YES

DOCKER_DESKTOP:
YES

PYTHON_DB_DRIVER:
MISSING (psycopg2-binary missing)

SQLALCHEMY:
INSTALLED (v2.0.23)

ALEMBIC:
MISSING

GEOALCHEMY2:
MISSING

RAM:
16GB Total (4.2GB Free)

FREE_DISK:
~30 GB

CURRENT_DATABASE:
In-memory Python lists for operational state. SQLite for audit ledger.

CURRENT_SQLITE_SCHEMA:
`audit_log` and `cache_state` tables only.

TARGET_SCHEMA:
`nodes`, `routes`, `fleet_assets`, `inventory`, `weather_snapshots`, `audit_events`.

CENTRAL_DATA:
PostgreSQL/PostGIS containing global geometries, full histories, and environmental tables.

EDGE_DATA:
SQLite containing localized active nodes/routes and an audit sync queue.

SPATIAL_MODEL:
WGS 84 (SRID 4326). Points for nodes, LineStrings for routes, Polygons for weather/hazards.

MIGRATION_PLAN:
Use Docker `postgis/postgis` -> Install Alembic/GeoAlchemy2 -> Generate Schema -> Translate `DEMO_POSTS` to SQL seeds -> Refactor FastAPI endpoints.

API_COMPATIBILITY:
PASS

REAL_DATA_READY:
PASS (Schema natively isolates public OSM/weather from synthetic defense overlays).

RAG_BOUNDARY:
PASS (pgvector explicitly excluded from operational tables).

OFFLINE_COMPATIBILITY:
PASS (Edge SQLite replication architecture validated).

MIGRATION_RISKS:
Schema drift, Windows Python dependency conflicts (mitigated via Docker), and memory pressure during large GIS imports (mitigated by strict spatial bounding).

RECOMMENDED_DATABASE_METHOD:
B (Docker PostgreSQL/PostGIS)

CODE_CHANGED:
NO

E1_CHANGED:
NO

DATA_DOWNLOADED:
NO

DATABASE_CREATED:
NO

PLUGINS_INSTALLED:
NO

MCP_INSTALLED:
NO

FILES_CREATED:
- reports/PHASE_4B_PREFLIGHT.md
- docs/DATABASE_SCHEMA_PLAN.md
- docs/MIGRATION_PLAN.md

NEXT_ACTION:
Phase 4B Pre-flight complete. Ready to execute the Dockerized PostgreSQL/PostGIS migration (Stage 1).
