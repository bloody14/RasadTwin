"""HimalayaSim data schemas and typed models."""
from __future__ import annotations

import enum
from datetime import date
from typing import Any

from pydantic import BaseModel, Field


class NodeType(str, enum.Enum):
    REAR_DEPOT = "rear_depot"
    INTERMEDIATE_DEPOT = "intermediate_depot"
    FORWARD_POST = "forward_post"


class TransportMode(str, enum.Enum):
    ROAD = "road"
    MULE = "mule"
    HELI = "heli"
    DRONE = "drone"


class Item(str, enum.Enum):
    RATIONS = "rations"
    POL = "POL"
    MEDICAL = "medical"
    SPARES = "spares"


ITEM_PRIORITY: dict[Item, int] = {
    Item.RATIONS: 3,
    Item.POL: 3,
    Item.MEDICAL: 4,
    Item.SPARES: 1,
}


class TempoState(str, enum.Enum):
    NORMAL = "normal"
    ELEVATED = "elevated"
    SURGE = "surge"


class Scenario(str, enum.Enum):
    S1 = "S1"  # stationary
    S2 = "S2"  # winter_surge
    S3 = "S3"  # sudden_operational_surge
    S4 = "S4"  # iot_dropout


class NodeRecord(BaseModel):
    node_id: str
    node_type: NodeType
    altitude_m: float
    x: float
    y: float


class EdgeRecord(BaseModel):
    edge_id: str
    from_node: str
    to_node: str
    mode: TransportMode
    length_km: float
    elevation_gain_m: float
    base_time_h: float
    capacity: float
    cost_per_km: float


class WeatherRecord(BaseModel):
    date: date
    node_id: str
    temperature_c: float
    snowfall_mm: float
    wind_kph: float
    visibility_km: float


class DemandRecord(BaseModel):
    date: date
    node_id: str
    item: Item
    troops: int
    demand_units: float
    tempo_state: TempoState
    ops_plan_signal: float


class InventoryRecord(BaseModel):
    date: date
    node_id: str
    item: Item
    opening_stock: float
    demand_units: float
    replenishment_units: float
    closing_stock: float
    unmet_demand_units: float
    stockout: bool


class DisruptionRecord(BaseModel):
    date: date
    disruption_id: str
    edge_id: str
    type: str
    active: bool
    duration_days: int


class SimulationMetadata(BaseModel):
    git_commit: str
    config_hash: str
    seed: int
    scenario: Scenario
    n_posts: int
    timestamp: str
    python_version: str
    config: dict[str, Any] = Field(default_factory=dict)
