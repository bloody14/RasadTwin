"""Synthetic seasonal weather generation.

This is NOT a real climate model. All parameters are fictional.
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np

from rasadtwin.sim.schemas import NodeRecord, WeatherRecord


def generate_weather(
    nodes: list[NodeRecord],
    start_date: date,
    n_days: int,
    config: dict,
    rng: np.random.Generator,
) -> list[WeatherRecord]:
    """Generate daily synthetic weather for each node.

    Temperature follows a seasonal sinusoid with altitude lapse.
    Snowfall occurs in configured months, scaling with altitude.
    Wind follows a seasonal pattern with noise.
    Visibility degrades with snowfall.

    Args:
        nodes: List of world nodes.
        start_date: First simulation date.
        n_days: Number of days to generate.
        config: The 'weather' section of world config.
        rng: Seeded random generator.

    Returns:
        List of WeatherRecord (one per node per day).
    """
    records: list[WeatherRecord] = []
    wc = config

    base_temp = wc["base_temperature_c"]
    amp = wc["annual_amplitude_c"]
    lapse = wc["lapse_rate_c_per_km"]
    ref_alt = wc["reference_altitude_m"]
    snow_months = set(wc["snowfall_season_months"])
    snow_peak = wc["snowfall_peak_mm"]
    snow_alt_factor = wc["snowfall_altitude_factor"]
    wind_base = wc["wind_base_kph"]
    wind_amp = wc["wind_amplitude_kph"]
    wind_noise_std = wc["wind_noise_std_kph"]
    vis_clear = wc["visibility_clear_km"]
    vis_snow_red = wc["visibility_snow_reduction_km_per_mm"]
    vis_min = wc["visibility_min_km"]
    temp_noise_std = wc["temperature_noise_std_c"]

    for day_idx in range(n_days):
        current_date = start_date + timedelta(days=day_idx)
        day_of_year = current_date.timetuple().tm_yday
        # Seasonal phase: coldest around day 15 (mid-Jan)
        season_phase = 2.0 * np.pi * (day_of_year - 15) / 365.0

        for node in nodes:
            alt_km = (node.altitude_m - ref_alt) / 1000.0

            # Temperature
            temp_base = base_temp - amp * np.cos(season_phase)
            temp_lapsed = temp_base - lapse * alt_km
            temp = float(
                temp_lapsed + rng.normal(0, temp_noise_std)
            )

            # Snowfall
            snowfall = 0.0
            if current_date.month in snow_months and temp < 2.0:
                snow_intensity = snow_peak * (
                    1.0 + snow_alt_factor * node.altitude_m
                )
                snowfall = float(
                    max(0.0, rng.exponential(snow_intensity * 0.3))
                )

            # Wind
            wind_seasonal = wind_base + wind_amp * abs(
                np.sin(season_phase)
            )
            wind = float(
                max(0.0, wind_seasonal + rng.normal(0, wind_noise_std))
            )

            # Visibility
            vis = float(
                max(
                    vis_min,
                    vis_clear - vis_snow_red * snowfall,
                )
            )

            records.append(WeatherRecord(
                date=current_date,
                node_id=node.node_id,
                temperature_c=round(temp, 2),
                snowfall_mm=round(snowfall, 2),
                wind_kph=round(wind, 2),
                visibility_km=round(vis, 2),
            ))

    return records
