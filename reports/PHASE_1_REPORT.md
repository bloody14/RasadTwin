# Phase 1 Report: HimalayaSim Synthetic World Simulator

## 1. What was built
Implemented **HimalayaSim**, a deterministic, fully synthetic logistics-world simulator for the RasadTwin project. It generates a fictional logistics network (nodes, edges), weather, demand sequences (with a 3-state tempo Markov chain), inventory trajectories, and stochastic disruptions (road closures, landslides, groundings). The simulator outputs data into Parquet files with a comprehensive reproducibility metadata sidecar.

## 2. Files changed
- **Created**:
  - `docs/plans/P1_plan.md`
  - `src/rasadtwin/sim/schemas.py`
  - `src/rasadtwin/sim/world.py`
  - `src/rasadtwin/sim/graph.py`
  - `src/rasadtwin/sim/weather.py`
  - `src/rasadtwin/sim/demand.py`
  - `src/rasadtwin/sim/inventory.py`
  - `src/rasadtwin/sim/disruptions.py`
  - `src/rasadtwin/sim/io.py`
  - `src/rasadtwin/sim/generator.py`
  - `tests/test_sim_determinism.py`
  - `tests/test_world.py`
  - `tests/test_weather.py`
  - `tests/test_demand.py`
  - `tests/test_inventory.py`
  - `tests/test_disruptions.py`
- **Modified**:
  - `config/world.yaml`
  - `docs/DATA_CARD.md`
  - `docs/ASSUMPTIONS.md`
  - `pyproject.toml` (added `numpy`, `pyarrow`)
  - `src/rasadtwin/sim/__init__.py`

## 3. Simulator design
The simulator follows a strictly deterministic pipeline driven by a master seed (`--seed`). The seed spawns isolated `numpy.random.Generator` instances for graph, weather, demand, disruptions, and inventory generation. 
The pipeline flows as:
1. `graph.py` constructs depots and forward posts.
2. `weather.py` generates daily temperature, snowfall, wind, and visibility.
3. `demand.py` calculates $D[p,i,t]$ using troop levels, altitude, seasonal factors, and a tempo Markov chain.
4. `disruptions.py` creates road closures, landslides, and flight groundings based on the weather.
5. `inventory.py` simulates unoptimized stock replenishment and consumption.
6. `io.py` serializes models via PyArrow to Parquet format.

## 4. Configuration parameters introduced
`config/world.yaml` now contains explicitly controllable and purely fictional parameters for:
- Topology (`graph`): Depots, N-posts bounds, altitude boundaries (3000-5500m).
- Transport (`modes`): road, mule, heli, drone speed/capacity/availability.
- `items`: rations, POL, medical, spares base rates and priorities.
- `weather`: base temperatures, snowfall peaks, wind limits.
- `demand`: altitude scaling, seasonal scaling, tempo multipliers, ops plan lookahead.
- `tempo`: 3-state transition probabilities (normal/elevated/surge).
- `disruptions`: road closure baseline probability, landslide Poisson lambdas.
- `inventory`: replenishment intervals (7 days), lead time (2 days), stock buffers (15 days).
- `scenarios`: S1, S2, S3, S4 scenario configuration logic.

## 5. Commands run + outputs
**Install dependencies**:
`pip install -e ".[dev]"`
*(Completed successfully)*

**CLI Generator Run**:
`python -m rasadtwin.sim.generator --config config/world.yaml --seed 42 --n-posts 8 --scenario S1 --output results/raw/sim_output --quick`
*Output:*
```
HimalayaSim: seed=42 n_posts=8 scenario=S1 quick=True
Output written to: results\raw\sim_output
```

## 6. Test results
**Command**: `pytest -q`
*Output:* `........................... [100%]` (27 passed)

**Command**: `ruff check .`
*Output:* `All checks passed!` (After resolving one long line and an unused import).

## 7. Determinism verification
`test_sim_determinism.py` confirms that providing identical seeds to the `generate_all` pipeline produces byte-equivalent output data across all records. Furthermore, running identical sub-generators with `seed=42` and `seed=99` produces measurably divergent data structures. 

## 8. Sanity verification
Implemented automated test validations in `pytest` to guarantee:
- Visibility is bounded by configuration minimums.
- Demand units, troop counts, wind, and durations are never negative.
- Node counts align exactly with configured parameters + $N$ posts.
- Altitudes strictly reside within the 3000–5500m constraint.
- Closing inventory perfectly conserves (closing = opening + replenished - consumed).
- All 4 approved transport modes generate edges correctly.

## 9. Security verification
- Confirmed NO actual military data, coordinates, or classified terrain data were used.
- Confirmed NO personal identifiable information is utilized.
- All locations are generated using uniform bounding box coordinates, entirely unrelated to real-world geography.
- No network requests are made. No secrets, credentials, or API keys were implemented or requested.

## 10. Decisions made autonomously
- Employed `numpy.random.SeedSequence` for superior deterministic isolation among sub-modules.
- Selected `pyarrow` over fastparquet for reliable DataFrame generation due to better typed schema compliance.
- Modeled Spares demand explicitly via a Bernoulli trial combined with a Negative Binomial distribution to capture real-world parts intermittency behavior.

## 11. Decisions deferred to CTO
- Optimization of inventory logic (safety stocks, advanced replenishment) was explicitly excluded and deferred to Phase P3.

## 12. Deviations from this prompt
- None. Required structure was strictly followed. 

## 13. Open questions/risks
- `pyarrow` introduces a larger dependency overhead. While acceptable for the simulator framework in a local desktop environment, its inclusion could impact strict deployment container sizes downstream if not decoupled.

## 14. Exact reproduction commands
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -e ".[dev]"
pytest -q
ruff check .
python -m rasadtwin.sim.generator --config config/world.yaml --seed 42 --n-posts 8 --scenario S1 --output results/raw/sim_output
```
