"""Synthetic disruption generation for HimalayaSim.

All disruption rules are fictional illustrative parameters.
No real terrain, weather, or operational data.
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np

from rasadtwin.sim.schemas import (
    DisruptionRecord,
    EdgeRecord,
    TransportMode,
    WeatherRecord,
)


def generate_disruptions(
    edges: list[EdgeRecord],
    weather_records: list[WeatherRecord],
    start_date: date,
    n_days: int,
    config: dict,
    rng: np.random.Generator,
) -> list[DisruptionRecord]:
    """Generate synthetic disruption events on transport edges.

    Disruption types:
    - road_closure: influenced by snowfall, altitude, month
    - landslide: Poisson occurrence per edge per year
    - heli_grounding: wind/visibility rule
    - drone_grounding: wind rule

    Args:
        edges: Transport edges.
        weather_records: Daily weather (for snowfall/wind/visibility).
        start_date: First simulation date.
        n_days: Number of days.
        config: The 'disruptions' section of world config.
        rng: Seeded random generator.

    Returns:
        List of DisruptionRecord.
    """
    records: list[DisruptionRecord] = []
    disruption_counter = 0

    # Index weather by (date, node_id)
    wx_idx: dict[tuple[date, str], WeatherRecord] = {}
    for wr in weather_records:
        wx_idx[(wr.date, wr.node_id)] = wr

    rc = config["road_closure"]
    ls = config["landslide"]
    hg = config["heli_grounding"]
    dg = config["drone_grounding"]

    # Track remaining closure days per edge
    active_closures: dict[str, int] = {}

    road_edges = [e for e in edges if e.mode == TransportMode.ROAD]
    heli_edges = [e for e in edges if e.mode == TransportMode.HELI]
    drone_edges = [e for e in edges if e.mode == TransportMode.DRONE]

    for day_idx in range(n_days):
        current_date = start_date + timedelta(days=day_idx)

        # Decrement active closures
        expired = []
        for eid, remaining in active_closures.items():
            if remaining <= 1:
                expired.append(eid)
            else:
                active_closures[eid] = remaining - 1
        for eid in expired:
            del active_closures[eid]

        # Road closures
        for edge in road_edges:
            if edge.edge_id in active_closures:
                disruption_counter += 1
                records.append(DisruptionRecord(
                    date=current_date,
                    disruption_id=f"D-{disruption_counter:06d}",
                    edge_id=edge.edge_id,
                    type="road_closure",
                    active=True,
                    duration_days=active_closures[edge.edge_id],
                ))
                continue

            # Check weather at destination node
            wx = wx_idx.get((current_date, edge.to_node))
            snowfall = wx.snowfall_mm if wx else 0.0
            alt_km = edge.elevation_gain_m / 1000.0

            prob = (
                rc["base_probability"]
                + rc["snowfall_factor"] * snowfall / 100.0
                + rc["altitude_factor_per_km"] * alt_km
            )
            if rng.random() < prob:
                dur = max(
                    1,
                    int(rng.lognormal(rc["duration_mu"], rc["duration_sigma"])),
                )
                active_closures[edge.edge_id] = dur
                disruption_counter += 1
                records.append(DisruptionRecord(
                    date=current_date,
                    disruption_id=f"D-{disruption_counter:06d}",
                    edge_id=edge.edge_id,
                    type="road_closure",
                    active=True,
                    duration_days=dur,
                ))

        # Landslides (Poisson per edge per year)
        daily_lambda = ls["lambda_per_edge_per_year"] / 365.0
        for edge in road_edges:
            if edge.edge_id in active_closures:
                continue
            if rng.random() < daily_lambda:
                dur = max(
                    1,
                    int(
                        rng.lognormal(ls["duration_mu"], ls["duration_sigma"])
                    ),
                )
                active_closures[edge.edge_id] = dur
                disruption_counter += 1
                records.append(DisruptionRecord(
                    date=current_date,
                    disruption_id=f"D-{disruption_counter:06d}",
                    edge_id=edge.edge_id,
                    type="landslide",
                    active=True,
                    duration_days=dur,
                ))

        # Heli grounding
        for edge in heli_edges:
            wx = wx_idx.get((current_date, edge.to_node))
            if wx and (
                wx.wind_kph > hg["wind_threshold_kph"]
                or wx.visibility_km < hg["visibility_threshold_km"]
            ):
                disruption_counter += 1
                records.append(DisruptionRecord(
                    date=current_date,
                    disruption_id=f"D-{disruption_counter:06d}",
                    edge_id=edge.edge_id,
                    type="heli_grounding",
                    active=True,
                    duration_days=1,
                ))

        # Drone grounding
        for edge in drone_edges:
            wx = wx_idx.get((current_date, edge.to_node))
            if wx and wx.wind_kph > dg["wind_threshold_kph"]:
                disruption_counter += 1
                records.append(DisruptionRecord(
                    date=current_date,
                    disruption_id=f"D-{disruption_counter:06d}",
                    edge_id=edge.edge_id,
                    type="drone_grounding",
                    active=True,
                    duration_days=1,
                ))

    return records
