"""Basic inventory dynamics for HimalayaSim.

Tracks stock, consumption, replenishment, and stockout per post/item.
Does NOT implement safety-stock optimization (deferred to P3).
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np

from rasadtwin.sim.schemas import (
    DemandRecord,
    InventoryRecord,
    Item,
    NodeRecord,
    NodeType,
    Scenario,
)


def _compute_initial_stock(
    troops: int,
    rate: float,
    stock_days: int,
) -> float:
    """Compute initial stock as stock_days worth of average demand."""
    return troops * rate * stock_days


def generate_inventory(
    nodes: list[NodeRecord],
    demand_records: list[DemandRecord],
    start_date: date,
    n_days: int,
    config: dict,
    items_config: dict,
    scenario: Scenario,
    scenario_cfg: dict,
    rng: np.random.Generator,
) -> list[InventoryRecord]:
    """Generate daily inventory state for all forward posts.

    Uses simplified periodic replenishment (not optimized).
    Stockout = stock < realized demand for that day.

    Args:
        nodes: All world nodes.
        demand_records: Pre-generated demand records.
        start_date: First simulation date.
        n_days: Number of days.
        config: The 'inventory' section of world config.
        items_config: The 'items' section of world config.
        scenario: Active scenario.
        scenario_cfg: Scenario-specific parameters.
        rng: Seeded random generator.

    Returns:
        List of InventoryRecord.
    """
    posts = [n for n in nodes if n.node_type == NodeType.FORWARD_POST]
    stock_days = config["initial_stock_days"]
    replenish_interval = config["replenishment_interval_days"]
    replenish_frac = config["replenishment_fraction"]
    lead_time = config["lead_time_days"]

    # Index demand by (date, node_id, item)
    demand_idx: dict[tuple[date, str, Item], float] = {}
    for dr in demand_records:
        demand_idx[(dr.date, dr.node_id, dr.item)] = dr.demand_units

    # Initialize stock per (node, item)
    stock: dict[tuple[str, Item], float] = {}
    for post in posts:
        for item_name, item_cfg in items_config.items():
            item_enum = Item(item_name)
            if item_name == "spares":
                init = float(stock_days * 2)  # small buffer
            else:
                rate = item_cfg["base_rate_per_troop"]
                # Use midpoint troops estimate
                init = _compute_initial_stock(75, rate, stock_days)
            stock[(post.node_id, item_enum)] = init

    records: list[InventoryRecord] = []
    is_s4 = scenario == Scenario.S4
    dropout_p = scenario_cfg.get("dropout_probability", 0.0)

    for day_idx in range(n_days):
        current_date = start_date + timedelta(days=day_idx)

        for post in posts:
            for item_name, item_cfg in items_config.items():
                item_enum = Item(item_name)
                key = (post.node_id, item_enum)
                opening = stock[key]

                demand = demand_idx.get(
                    (current_date, post.node_id, item_enum), 0.0,
                )

                # Replenishment on schedule
                replenishment = 0.0
                if (
                    day_idx >= lead_time
                    and (day_idx - lead_time) % replenish_interval == 0
                ):
                    if item_name == "spares":
                        replenishment = 5.0
                    else:
                        rate = item_cfg["base_rate_per_troop"]
                        target = 75 * rate * stock_days
                        shortfall = max(0.0, target - opening)
                        replenishment = shortfall * replenish_frac

                consumed = min(demand, opening + replenishment)
                closing = opening + replenishment - consumed
                unmet = max(0.0, demand - consumed)
                stockout = opening < demand

                # S4: IoT dropout masks the observation
                reported_opening = opening
                reported_closing = closing
                if is_s4 and rng.random() < dropout_p:
                    reported_opening = float("nan")
                    reported_closing = float("nan")

                records.append(InventoryRecord(
                    date=current_date,
                    node_id=post.node_id,
                    item=item_enum,
                    opening_stock=round(reported_opening, 2),
                    demand_units=round(demand, 2),
                    replenishment_units=round(replenishment, 2),
                    closing_stock=round(reported_closing, 2),
                    unmet_demand_units=round(unmet, 2),
                    stockout=stockout,
                ))

                # Update actual stock (ground truth)
                stock[key] = closing

    return records
