# PROJECT MEMORY & AGENT GOVERNANCE

To ensure autonomous agents and future developers maintain the architectural integrity of RasadTwin, we establish a persistent Antigravity context system.

## 1. AGENT RULES SYSTEM
Rules are stored in `.agents/rules/` and dictate strict boundaries for LLM behavior.

- **`00-project-invariants.md`**: Core unbreakable rules (e.g., E1 must not be changed, prototype must remain synthetic).
- **`10-security-defence.md`**: Strict prohibitions on using real military data or PII.
- **`20-data-governance.md`**: Real vs. Synthetic boundaries.
- **`30-system-architecture.md`**: Layer boundaries (FastAPI backend, Vite frontend).
- **`40-ai-ml.md`**: E1 execution rules and forecasting boundaries.
- **`50-logistics-domain.md`**: Definitions of Fleet, Depots, and Routing constraints.
- **`60-geospatial.md`**: PostGIS standards and Map projection rules.
- **`70-offline-edge.md`**: Rules for local SQLite fallbacks and queue logic.
- **`80-frontend.md`**: Tailwind v3 requirements, offline-first UI design.
- **`90-backend-api.md`**: FastAPI contract stability and Pydantic validation.
- **`95-testing-evidence.md`**: Playwright E2E standards (must test semantics, not just DOM).
- **`99-git-change-control.md`**: Commit hygiene, branch strategy.

## 2. REUSABLE SKILLS
Antigravity skills automate complex, repetitive validation and setup routines.

- **`dataset-audit`**: Scans the repository to ensure no real military data or PII has been accidentally committed.
- **`geospatial-ingestion`**: Automates the ETL pipeline from public OSM/SRTM to synthetic overlay.
- **`database-migration`**: Safely manages PostgreSQL and SQLite schema changes.
- **`browser-e2e`**: Runs Playwright headless validations and captures screenshot evidence.
- **`offline-validation`**: Simulates network drops and verifies SQLite queue persistence.
- **`experiment-validation`**: Verifies E1 reproducibility without modifying core seeds.
- **`security-review`**: Scans for exposed API keys or `.env` leaks.

## 3. PROPOSED LONG-TERM REPOSITORY STRUCTURE

### CURRENT (Phase 3)
```text
/config
/docs
/experiments
  /e1_forecast
/frontend
  /src
  /tests
/reports
/src
  /rasadtwin
    /api
    /forecast
    /sim
/tests
```

### NEAR-TERM (Phase 4 Database & Geo)
```text
/.agents
  /rules
  /skills
/config
/db
  /migrations
  /seeds
/docs
  /ADR
/experiments
/frontend
/reports
/src
  /rasadtwin
    /api
    /db (PostgreSQL/PostGIS adapters)
    /geo (Spatial overlays)
    /forecast
    /sim
/tests
```

### FUTURE (Phase 5 RAG & Edge Sync)
```text
/edge
  /sync_client
/knowledge (pgvector/RAG pipeline)
```
