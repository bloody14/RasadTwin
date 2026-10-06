# ANTIGRAVITY PLUGIN / MCP STRATEGY

## OVERVIEW
The Model Context Protocol (MCP) enables the Antigravity agent to interact securely with external tools and datasets. For RasadTwin, MCP integration must respect the strict "Offline-First / Air-Gapped" ethos of defense logistics.

## POTENTIAL MCP INTEGRATIONS

### 1. PostgreSQL / PostGIS MCP
- **Benefit**: Allows the agent to query the active logistics state natively, validate schema changes, and inspect spatial queries.
- **Risk**: Potential to accidentally drop synthetic tables or leak data context if not strictly bound.
- **Recommended**: YES (Using local SQLite/PG instances).
- **Needed Now**: NO (Pending Phase 4B Database migration).

### 2. Browser Testing MCP (e.g., Playwright integration)
- **Benefit**: Permits the agent to visually inspect dashboard state via screenshots, bypassing DOM-only limitations.
- **Risk**: High overhead during rapid iteration.
- **Recommended**: YES.
- **Needed Now**: YES (Already simulated via CLI execution, but formal MCP is superior).

### 3. GitHub / Source Control MCP
- **Benefit**: Automates PR creation, code reviews, and issue tracking.
- **Risk**: Committing unstable code directly to `master`.
- **Recommended**: YES.
- **Needed Now**: NO (Standard CLI Git serves current needs).

### 4. Knowledge Base / Documentation MCP
- **Benefit**: Native search over military logistics doctrines (RAG layer preview).
- **Risk**: None, assuming data is public/synthetic.
- **Recommended**: YES (for P4G Knowledge phase).
- **Needed Now**: NO.

## API KEY POLICY

To preserve the system's ability to operate in air-gapped environments, proprietary APIs are strictly limited.

1. **Weather (Open-Meteo)**
   - **Purpose**: Environmental hazard mapping.
   - **Key Required**: NO (Free tier is keyless).
   - **Air-Gapped Feasibility**: Can be cached locally for 7-day predictions.
2. **Maps (OpenStreetMap / SRTM)**
   - **Purpose**: Terrain and road networks.
   - **Key Required**: NO (Public datasets, downloaded as raw files).
   - **Air-Gapped Feasibility**: Excellent. Vector tiles served locally.
3. **LLM APIs (OpenAI / Anthropic / Gemini)**
   - **Purpose**: Generating Explainability insights or RAG queries.
   - **Key Required**: YES (for cloud), NO (if using local models like Llama 3 on edge hardware).
   - **Air-Gapped Feasibility**: Cloud APIs are prohibited in true air-gapped deployment; local quantized models are required.

*Rule: No external API keys will be requested or integrated during the architecture bootstrap phase.*
