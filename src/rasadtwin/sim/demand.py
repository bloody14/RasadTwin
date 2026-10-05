"""Synthetic demand generation for HimalayaSim.

Demand D[p,i,t] = troops[p] * rate[i] * altitude_factor
                  * seasonal_factor * tempo_multiplier * (1 + noise).

Spares use Bernoulli + negative-binomial mechanism.
Tempo follows a 3-state Markov chain (normal/elevated/surge).

All rates are fictional. No real Army consumption data.
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np

from rasadtwin.sim.schemas import (
    DemandRecord,
    Item,
    NodeRecord,
    NodeType,
    Scenario,
    TempoState,
)


def _assign_troops(
    posts: list[NodeRecord],
    config: dict,
    rng: np.random.Generator,
) -> dict[str, int]:
    """Assign fictional troop counts to forward posts."""
    lo = config["min_per_post"]
    hi = config["max_per_post"]
    return {
        p.node_id: int(rng.integers(lo, hi + 1))
        for p in posts
    }


def _tempo_transition(
    current: TempoState,
    matrix: dict,
    rng: np.random.Generator,
) -> TempoState:
    """Advance the Markov tempo state by one step."""
    row = matrix[current.value]
    states = list(TempoState)
    probs = [row[s.value] for s in states]
    return states[int(rng.choice(len(states), p=probs))]


def _get_forced_tempo(
    current_date: date,
    scenario: Scenario,
    scenario_cfg: dict,
    start_date: date,
) -> TempoState | None:
    """Check if the scenario forces a specific tempo on this date."""
    if scenario == Scenario.S2:
        months = scenario_cfg.get("force_tempo_months", [])
        if current_date.month in months:
            return TempoState(scenario_cfg["forced_tempo"])
    elif scenario == Scenario.S3:
        day_offset = (current_date - start_date).days
        surge_start = scenario_cfg.get("surge_start_day", 400)
        surge_dur = scenario_cfg.get("surge_duration_days", 60)
        if surge_start <= day_offset < surge_start + surge_dur:
            return TempoState(scenario_cfg["forced_tempo"])
    return None


def generate_demand(
    nodes: list[NodeRecord],
    start_date: date,
    n_days: int,
    config: dict,
    tempo_config: dict,
    items_config: dict,
    troops_config: dict,
    scenario: Scenario,
    scenario_cfg: dict,
    rng: np.random.Generator,
) -> list[DemandRecord]:
    """Generate daily demand records for all forward posts and items.

    Args:
        nodes: All world nodes.
        start_date: First simulation date.
        n_days: Number of days.
        config: The 'demand' section of world config.
        tempo_config: The 'tempo' section of world config.
        items_config: The 'items' section of world config.
        troops_config: The 'troops' section of world config.
        scenario: Active scenario enum.
        scenario_cfg: Scenario-specific parameters.
        rng: Seeded random generator.

    Returns:
        List of DemandRecord.
    """
    posts = [n for n in nodes if n.node_type == NodeType.FORWARD_POST]
    troops_map = _assign_troops(posts, troops_config, rng)

    alt_factor_per_km = config["altitude_factor_per_km"]
    seasonal_amp = config["seasonal_amplitude"]
    winter_fuel = config["winter_fuel_boost"]
    noise_std = config["noise_std"]
    lookahead = config["ops_plan_lookahead_days"]
    ops_noise_std = config["ops_plan_noise_std"]

    trans_matrix = tempo_config["transition_matrix"]
    tempo_mult = tempo_config["multipliers"]

    records: list[DemandRecord] = []
    tempo_state = TempoState.NORMAL

    # Pre-generate the full tempo sequence
    tempo_seq: list[TempoState] = []
    for day_idx in range(n_days):
        current_date = start_date + timedelta(days=day_idx)
        forced = _get_forced_tempo(
            current_date, scenario, scenario_cfg, start_date,
        )
        if forced is not None:
            tempo_state = forced
        else:
            tempo_state = _tempo_transition(
                tempo_state, trans_matrix, rng,
            )
        tempo_seq.append(tempo_state)

    for day_idx in range(n_days):
        current_date = start_date + timedelta(days=day_idx)
        day_of_year = current_date.timetuple().tm_yday
        season_phase = 2.0 * np.pi * (day_of_year - 15) / 365.0
        seasonal_factor = 1.0 + seasonal_amp * np.cos(season_phase)
        is_winter = current_date.month in (11, 12, 1, 2)

        current_tempo = tempo_seq[day_idx]
        t_mult = tempo_mult[current_tempo.value]

        # Ops-plan signal: noisy lookahead of future tempo
        future_idx = min(day_idx + lookahead, n_days - 1)
        future_mult = tempo_mult[tempo_seq[future_idx].value]
        ops_signal = float(
            future_mult + rng.normal(0, ops_noise_std)
        )

        for post in posts:
            troops = troops_map[post.node_id]
            alt_km = post.altitude_m / 1000.0
            alt_mult = 1.0 + alt_factor_per_km * alt_km

            for item_name, item_cfg in items_config.items():
                item_enum = Item(item_name)

                if item_name == "spares":
                    # Bernoulli + negative-binomial
                    bp = item_cfg["bernoulli_p"]
                    occurs = rng.random() < bp
                    if occurs:
                        demand_val = float(
                            rng.negative_binomial(
                                item_cfg["nb_n"],
                                item_cfg["nb_p"],
                            )
                        )
                    else:
                        demand_val = 0.0
                    demand_val *= t_mult
                else:
                    rate = item_cfg["base_rate_per_troop"]
                    base = troops * rate * alt_mult
                    base *= seasonal_factor * t_mult
                    if item_name == "POL" and is_winter:
                        base *= 1.0 + winter_fuel
                    noise = 1.0 + rng.normal(0, noise_std)
                    demand_val = max(0.0, base * noise)

                records.append(DemandRecord(
                    date=current_date,
                    node_id=post.node_id,
                    item=item_enum,
                    troops=troops,
                    demand_units=round(demand_val, 2),
                    tempo_state=current_tempo,
                    ops_plan_signal=round(ops_signal, 4),
                ))

    return records
