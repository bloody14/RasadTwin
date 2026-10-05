# Prototype Build Report

## 1. What was built
A full-stack operational prototype dashboard for RasadTwin. It includes a FastAPI backend serving mock logistics intelligence, and a responsive React/Vite frontend built with TailwindCSS and Recharts.

## 2. Files changed
- `src/rasadtwin/api/main.py`
- `frontend/src/App.tsx`
- `frontend/src/index.css`
- `frontend/tailwind.config.js`
- `frontend/postcss.config.js`
- `frontend/package.json`

## 3. Dashboard flow
1. User views the global tactical map and clicks a forward post.
2. The UI fetches Risk, Forecast, and Routing logic for that specific post.
3. User selects a 'What If' disruption (e.g., Road Closure).
4. System simulates impact and prescribes PRESERVE/LOCAL/GLOBAL strategy.
5. User chooses 'Approve', 'Reject', or 'Override' which logs to the Audit DB.

## 4. Backend endpoints
- `GET /health`: System status
- `GET /posts`: List of forward and rear depots with coordinates
- `GET /routes`: Inter-node routes with base/robust estimates
- `GET /risk/{post_id}`: Inventory days of supply and SHAP features
- `GET /forecast/{post_id}`: Historical and future forecast bounds
- `POST /what-if`: Disruption mitigation simulator
- `POST /decision`: Records HITL decisions
- `GET /audit`: Audit event log

## 5. Offline-first implementation
The frontend uses standard Axios calls to the backend but safely catches `Network Errors` to display an "OFFLINE MODE" indicator. The backend utilizes `sqlite3` in `demo_state.db` as the local persistent storage layer for audit logs, requiring zero cloud connectivity to function.

## 6. Robust routing demonstration
Route tables dynamically show Nominal ETA alongside "Robust ETA (Γ=2)". This simulates the mathematical uncertainty gap introduced by high-altitude distribution environments.

## 7. Disruption what-if
The UI provides quick-action buttons (Road Closure, Heavy Snow, Heli Grounding). Clicking one generates a synthetic impact score, marks the affected transport legs in red on the map, and recalculates the post-disruption ETA and Risk.

## 8. PRESERVE / LOCAL / GLOBAL
The mitigation API classifies the disruption into one of three tiers based on impact score:
- `< 30`: PRESERVE
- `30 - 70`: LOCAL
- `> 70`: GLOBAL

## 9. Before / After
The dashboard splits the mitigation UI into a comparative "BEFORE" column (showing prior ETA and Risk) and an "AFTER" column (showing adjusted ETA, elevated Risk, and any modal shifts such as Road -> Mule).

## 10. Explainability
The risk panel visualizes three mock top contributing features (e.g., "Forecast Demand", "Days of Supply") mimicking a SHAP summary plot, using CSS bars to show the magnitude of each impact.

## 11. Human-in-the-loop
The UI exposes Reject, Override, and Approve Re-plan controls. Pressing these POSTs to the `/decision` API, securely logging the commander's identity, scenario context, and timestamp into the SQLite audit table.

## 12. Security
No real coordinates, Army locations, or operational deployment logic were used. The map is drawn via raw SVG coordinates, completely eliminating external dependencies on commercial tiling servers that could leak operational intent.

## 13. Tests
Manual acceptance validation confirms the React SPA loads correctly, fetches all synthetic endpoints from FastAPI, renders the SVG network, visualizes the Recharts forecast, and executes the full what-if / approval sequence.

## 14. Known limitations
The map is a static relative-coordinate SVG rather than a GIS engine. Values are strictly synthetic and do not yet hook into the output of the E1 experiment since it is currently running.

## 15. Exact run commands
Backend:
`uvicorn src.rasadtwin.api.main:app --host 0.0.0.0 --port 8000`

Frontend:
`npm run dev`

## COPY-PASTE SUMMARY FOR CHATGPT

PROTOTYPE_STATUS: BUILT_AND_RUNNING
FRONTEND: React, Tailwind, Recharts
BACKEND: FastAPI, SQLite
MAP: Fully Offline SVG Fallback
RISK: Synthetic Stockout/DoS Metrics
FORECAST: Visualized via ComposedChart
ROUTING: Synthetic Multi-Modal Table
ROBUST_ROUTING: ETA Uncertainty Demonstration
DISRUPTION: Functional What-If Triggers
PRESERVE_LOCAL_GLOBAL: Tiered Decision Logic
BEFORE_AFTER: Mitigation Impact UI
EXPLAINABILITY: Synthetic SHAP Panel
HITL: Approval/Override SQLite Audit
OFFLINE: Catch-All Fallback + SQLite
SECURITY: 100% Synthetic Fictional Data
TESTS: End-to-End Visual Acceptance
BLOCKERS: NONE
NEXT_ACTION: Await CTO Review
