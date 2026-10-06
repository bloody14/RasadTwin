# CURRENT ARCHITECTURE: SYNTHETIC VERTICAL SLICE

## 1. PRESENTATION / UI LAYER
- **Framework**: Vite, React 19, Tailwind CSS (v3 config).
- **Core Views**: Command Centre (Dash), Posts, Forecast, Inventory, Routing, Decisions, Audit.
- **Map Implementation**: Pure SVG auto-scaling map implementing `minX/maxX/minY/maxY` node detection, bounding-box normalization, and dynamic `viewBox` scaling with SVG `transform` for pan/zoom. Zero external map dependencies (no Google Maps, no Mapbox).

## 2. API / SERVICE LAYER
- **Framework**: FastAPI running via Uvicorn.
- **Contracts**: RESTful endpoints returning strict JSON structures.
  - `GET /health`
  - `GET /posts`, `GET /routes`, `GET /weather`
  - `GET /risk/{post_id}`, `GET /forecast/{post_id}`
  - `POST /what-if`
  - `POST /decision`
  - `GET /audit`

## 3. DATA LAYER
- **Current State Engine**: In-memory deterministic Python lists acting as the digital twin state.
- **Database**: Local SQLite (`demo_state.db`) exclusively used for persisting the `audit_log` (Hits-in-the-Loop decision tracking).
- **Synthetic Model**: 17 total nodes (2 Rear Depots, 3 Intermediate Hubs, 12 Forward Posts). Multi-modal routes (Road, Heli, Mule, Drone). 

## 4. DOMAIN LOGIC
- **Risk**: Hardcoded deterministic thresholds based on `days_of_supply` (e.g., < 7 triggers 85% risk).
- **Forecasting**: Static mock distributions injected for visual validation and E1 linkage simulation.
- **Routing**: Static graph visualization; paths are explicitly predefined per scenario.
- **What-If Engine**: Evaluates predefined string parameters (`Road Closure`, `Heavy Snow`) to return hardcoded `impact_score` and `before_after` arrays.
- **HITL (Human-in-the-Loop)**: Captures decoupled `system_recommendation`, `user_action`, and `selected_scope` to ensure immutable intent capture.

## 5. EXPERIMENT INFRASTRUCTURE
- **Forecasting (E1)**: Isolated pipeline located in `experiments/e1_forecast/` utilizing chronos, conformal prediction, and lightgbm. Fully partitioned from the runtime dashboard to prevent interference.
- **Offline Behavior**: The UI detects API unreachable states and toggles `offline=true`, rendering the "LOCAL ENGINE ACTIVE" badge, proving the conceptual framework for edge deployment.
