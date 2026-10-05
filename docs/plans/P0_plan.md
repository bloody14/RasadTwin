# Phase P0 Plan: Repository Foundation, Engineering Guardrails & Reproducibility

## Objective
Establish the repository skeleton, Python environment, tooling (pytest/ruff), test and reproducibility foundations without implementing specific experimental or ML logic.

## Tasks & Target Files

1. **Workspace Skeleton**
   - Create directories: `src/rasadtwin/{sim,forecast,inventory,routing,reopt,explain,api,utils}`
   - Create directories: `experiments/{e1_forecast,e2_inventory,e3_routing,e4_reopt,e5_prepos,e6_ablation,e7_scale,e8_sensitivity}`
   - Create directories: `config/experiments`, `results/{raw,tables,figures}`
   - Create directories: `tests`, `docs/plans`, `reports`, `notebooks`, `frontend`
   - Add minimal `__init__.py` files inside Python package directories.

2. **Python Environment & Dependencies**
   - Create `pyproject.toml` (target Python 3.11+, configure `pytest`, `ruff`, and standard metadata).

3. **Tooling Configuration**
   - Configure `ruff` rules and `pytest` paths in `pyproject.toml`.

4. **Configuration Placeholders**
   - Create `config/world.yaml`, `config/forecast.yaml`, `config/routing.yaml`, `config/reopt.yaml`.
   - Create `config/experiments/e1.yaml` through `e8.yaml` (just placeholders).

5. **Reproducibility Utility**
   - Create `src/rasadtwin/utils/metadata.py` with typed, documented functions to capture git_commit, config_hash, seed, timestamp, python_version.

6. **Test Foundation**
   - Create `tests/test_imports.py`
   - Create `tests/test_config.py` (proving yaml loads)
   - Create `tests/test_metadata.py` (proving metadata fields are generated correctly and hashing works).

7. **Security / Guardrails**
   - Create/Update `.gitignore` to exclude `.env`, `*.key`, `*.pem`, `results/raw/*`, etc.

8. **Documentation updates**
   - Update `docs/STATE.md` (mark P0 as active)
   - Create `docs/DATA_CARD.md` (mark as synthetic)
   - Create `docs/ASSUMPTIONS.md`
   - Create `docs/PREREG.md`
   - Update `README.md` (add Windows PowerShell setup commands).

9. **Reporting**
   - Run `pytest` and `ruff check .`
   - Create `reports/PHASE_0_REPORT.md` with required sections.
