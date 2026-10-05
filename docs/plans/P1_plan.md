# Phase P1 Plan: HimalayaSim Synthetic World Simulator

## Objective
Implement a deterministic, fully synthetic logistics-world simulator (HimalayaSim) under `src/rasadtwin/sim/` that generates world topology, weather, demand, inventory, and disruption data for all downstream RasadTwin experiments.

## Files to Create

### Simulator Core (`src/rasadtwin/sim/`)
- `world.py` — World config loading, node/edge graph construction
- `graph.py` — Network topology generation (depots, posts, edges, modes)
- `weather.py` — Seasonal synthetic weather generation
- `demand.py` — Demand D[p,i,t] generation with tempo Markov chain
- `inventory.py` — Daily inventory dynamics (stock, consumption, replenishment, stockout)
- `disruptions.py` — Road closure, landslide, heli/drone grounding
- `generator.py` — CLI entry point orchestrating full world generation
- `io.py` — Parquet/CSV serialization and metadata sidecar writing
- `schemas.py` — Pydantic/dataclass models for all data records

### Configuration
- `config/world.yaml` — Fully populated world parameters

### Tests (`tests/`)
- `test_sim_determinism.py`
- `test_world.py`
- `test_weather.py`
- `test_demand.py`
- `test_inventory.py`
- `test_disruptions.py`

### Documentation
- `docs/DATA_CARD.md` — Updated with simulator details
- `docs/ASSUMPTIONS.md` — Updated with simulator assumptions
- `reports/PHASE_1_REPORT.md`

### Modified
- `docs/STATE.md` — Update phase to P1
- `pyproject.toml` — Add pyarrow dependency for Parquet support

## Simulator Architecture

```
config/world.yaml
       │
       ▼
  WorldConfig (schemas.py)
       │
  ┌────┴─────┐
  │ graph.py  │ → nodes[], edges[]
  └────┬─────┘
       │
  ┌────┴──────┐
  │ weather.py│ → daily weather per node
  └────┬──────┘
       │
  ┌────┴─────┐
  │ demand.py │ → daily demand D[p,i,t]
  └────┬─────┘
       │
  ┌────┴────────────┐
  │ disruptions.py  │ → edge disruption events
  └────┬────────────┘
       │
  ┌────┴──────────┐
  │ inventory.py  │ → daily inventory state
  └────┬──────────┘
       │
  ┌────┴───┐
  │ io.py  │ → Parquet files + metadata sidecar
  └────────┘
```

## Data Schemas (column-level)
- **nodes**: node_id, node_type, altitude_m, x, y
- **edges**: edge_id, from_node, to_node, mode, length_km, elevation_gain_m, base_time_h, capacity, cost_per_km
- **weather**: date, node_id, temperature_c, snowfall_mm, wind_kph, visibility_km
- **demand**: date, node_id, item, troops, demand_units, tempo_state, ops_plan_signal
- **inventory**: date, node_id, item, opening_stock, demand_units, replenishment_units, closing_stock, unmet_demand_units, stockout
- **disruptions**: date, disruption_id, edge_id, type, active, duration_days

## Deterministic Seed Strategy
- One master seed from CLI `--seed`.
- Derive child seeds for each subsystem (graph, weather, demand, disruptions) using `numpy.random.SeedSequence`.
- Each subsystem gets its own `numpy.random.Generator` instance.
- No global `numpy.random` or `random` module state used.

## CLI
```
python -m rasadtwin.sim.generator \
  --config config/world.yaml \
  --seed 42 \
  --n-posts 8 \
  --scenario S1 \
  --output results/raw/sim_output \
  --quick
```
`--quick` reduces history to 90 days for fast test runs.

## Scenarios
- **S1** (stationary): Normal baseline, no regime changes
- **S2** (winter_surge): Extended winter with elevated demand
- **S3** (sudden_operational_surge): Mid-timeline tempo spike
- **S4** (iot_dropout): Random missing stock observations (masks, not ground-truth removal)

## Risks / Assumptions
- All parameters are synthetic and illustrative; no real Army data.
- Weather model is a simple seasonal sinusoid + noise, not a climate model.
- Demand rates are fictional illustrative values.
- Inventory replenishment uses a simplified periodic review, not an optimized policy.
- Parquet requires pyarrow; this is the only new dependency added.

## Sanity Checks
- Node counts match requested N
- Altitudes within 3000–5500 m for forward posts
- No negative demand, capacity, or stock
- Inventory conservation: closing = opening - demand + replenishment
- Disruption durations > 0
- All 4 transport modes present
- Determinism: same seed → identical output
