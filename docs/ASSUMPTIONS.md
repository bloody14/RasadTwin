# RasadTwin Assumptions

## Phase P1 — HimalayaSim Simulator Assumptions

All assumptions below are synthetic and illustrative. They are configurable via `config/world.yaml`.

### Graph Topology
- 2 rear depots at ~1200 m altitude (fictional)
- 3 intermediate depots at ~2200 m altitude (fictional)
- N forward posts at 3000–5500 m altitude (fictional)
- Supported N values: 8, 20, 50, 100
- All coordinates are fictional, within a bounding box [0–200, 0–150]

### Transport Modes
- **road**: 25 km/h, 500 unit capacity
- **mule**: 5 km/h, 50 unit capacity
- **heli**: 150 km/h, 200 unit capacity, grounded above 50 kph wind or below 2 km visibility
- **drone**: 60 km/h, 20 unit capacity, grounded above 35 kph wind
- No monorail mode

### Items
- rations, POL (fuel), medical, spares
- Priority weights: medical=4, POL=3, rations=3, spares=1
- No weapons or ammunition

### Weather Model
- Temperature: seasonal sinusoid with altitude lapse rate (6.5 °C/km), NOT a real climate model
- Snowfall: exponential distribution during winter months, altitude-scaled
- Wind: seasonal pattern with Gaussian noise
- Visibility: degrades linearly with snowfall, clamped to minimum 0.5 km

### Demand Model
- D[p,i,t] = troops × rate × altitude_factor × seasonal_factor × tempo_mult × noise
- Spares use Bernoulli(0.15) + NegBinomial(n=2, p=0.4) mechanism
- POL demand increases by 40% during winter months
- Tempo follows a 3-state Markov chain (normal/elevated/surge)
- All rates are fictional illustrative values

### Inventory
- Initial stock: 15 days of average demand
- Replenishment: periodic (every 7 days), with 2-day lead time
- Replenishment fraction: 80% of shortfall
- Stockout = opening stock < realized demand

### Disruptions
- Road closure: probability influenced by snowfall and altitude; lognormal duration
- Landslides: Poisson occurrence (~0.3/edge/year); lognormal duration
- Heli grounding: wind > 50 kph OR visibility < 2 km
- Drone grounding: wind > 35 kph
- All parameters are fictional

### Scenarios
- S1 (stationary): no forced regime changes
- S2 (winter_surge): elevated tempo forced during Nov–Feb
- S3 (sudden_operational_surge): surge tempo forced at day 400 for 60 days
- S4 (iot_dropout): 15% probability of missing stock observations (masks only, ground truth preserved)
