# RasadTwin Governance Pack

Use this pack to anchor Google Antigravity during long implementation sessions.

Files are intentionally separated into:
- agent constitution;
- security/data policy;
- decision boundaries;
- change control;
- persistent state;
- IDE rules and workflows;
- master operating prompt.

The pack follows the project's existing requirements for one-phase-at-a-time execution, reproducibility, synthetic data, CPU-only Windows operation, and human review.


## Usage & Setup (Windows PowerShell)

**Current Phase:** P0 — Repository Foundation, Engineering Guardrails & Reproducibility
*(Note: Application modules such as forecasting, inventory optimization, routing, re-optimization, APIs, etc., are not implemented yet.)*

Requires **Python 3.11+**.

1. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```powershell
   pip install -e ".[dev]"
   ```

3. **Run tests:**
   ```powershell
   pytest
   ```

4. **Run linter:**
   ```powershell
   ruff check .
   ```
