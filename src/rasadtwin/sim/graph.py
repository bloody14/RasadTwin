"""Network topology generation for HimalayaSim.

All locations are fictional. No real military positions are used.
"""
from __future__ import annotations

import numpy as np

from rasadtwin.sim.schemas import (
    EdgeRecord,
    NodeRecord,
    NodeType,
    TransportMode,
)


def generate_nodes(
    n_posts: int,
    config: dict,
    rng: np.random.Generator,
) -> list[NodeRecord]:
    """Generate fictional depot and forward-post nodes.

    Args:
        n_posts: Number of forward posts to create.
        config: The 'graph' section of world config.
        rng: Seeded random generator.

    Returns:
        List of NodeRecord instances.
    """
    nodes: list[NodeRecord] = []
    x_min = config["x_min"]
    x_max = config["x_max"]
    y_min = config["y_min"]
    y_max = config["y_max"]

    # Rear depots
    for i in range(config["rear_depots"]):
        nodes.append(NodeRecord(
            node_id=f"RD-{i:02d}",
            node_type=NodeType.REAR_DEPOT,
            altitude_m=config["rear_depot_altitude_m"],
            x=float(rng.uniform(x_min, x_max * 0.3)),
            y=float(rng.uniform(y_min, y_max)),
        ))

    # Intermediate depots
    for i in range(config["intermediate_depots"]):
        nodes.append(NodeRecord(
            node_id=f"ID-{i:02d}",
            node_type=NodeType.INTERMEDIATE_DEPOT,
            altitude_m=config["intermediate_depot_altitude_m"],
            x=float(rng.uniform(x_max * 0.3, x_max * 0.6)),
            y=float(rng.uniform(y_min, y_max)),
        ))

    # Forward posts
    alt_min = config["forward_post_altitude_min_m"]
    alt_max = config["forward_post_altitude_max_m"]
    for i in range(n_posts):
        nodes.append(NodeRecord(
            node_id=f"FP-{i:03d}",
            node_type=NodeType.FORWARD_POST,
            altitude_m=float(rng.uniform(alt_min, alt_max)),
            x=float(rng.uniform(x_max * 0.6, x_max)),
            y=float(rng.uniform(y_min, y_max)),
        ))

    return nodes


def generate_edges(
    nodes: list[NodeRecord],
    modes_config: dict,
    rng: np.random.Generator,
) -> list[EdgeRecord]:
    """Generate transport edges between nodes.

    Connectivity rules (fictional):
    - Rear depots connect to all intermediate depots (road, heli).
    - Intermediate depots connect to forward posts (road, mule, heli, drone).
    - Some forward posts connect to nearby forward posts (mule only).

    Args:
        nodes: List of generated nodes.
        modes_config: The 'modes' section of world config.
        rng: Seeded random generator.

    Returns:
        List of EdgeRecord instances.
    """
    edges: list[EdgeRecord] = []
    edge_counter = 0

    rear = [n for n in nodes if n.node_type == NodeType.REAR_DEPOT]
    intermediate = [n for n in nodes if n.node_type == NodeType.INTERMEDIATE_DEPOT]
    forward = [n for n in nodes if n.node_type == NodeType.FORWARD_POST]

    def _dist(a: NodeRecord, b: NodeRecord) -> float:
        return float(np.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2))

    def _make_edge(
        a: NodeRecord, b: NodeRecord, mode: TransportMode,
    ) -> EdgeRecord:
        nonlocal edge_counter
        dist_km = max(1.0, _dist(a, b) * 0.5)
        elev = max(0.0, b.altitude_m - a.altitude_m)
        mc = modes_config[mode.value]
        edge_counter += 1
        return EdgeRecord(
            edge_id=f"E-{edge_counter:04d}",
            from_node=a.node_id,
            to_node=b.node_id,
            mode=mode,
            length_km=round(dist_km, 2),
            elevation_gain_m=round(elev, 1),
            base_time_h=round(dist_km / mc["speed_kmh"], 2),
            capacity=mc["capacity"],
            cost_per_km=mc["cost_per_km"],
        )

    # Rear -> Intermediate (road + heli)
    for r in rear:
        for im in intermediate:
            edges.append(_make_edge(r, im, TransportMode.ROAD))
            edges.append(_make_edge(r, im, TransportMode.HELI))

    # Intermediate -> Forward (all 4 modes)
    # Assign each FP to nearest intermediate depot
    for fp in forward:
        nearest_id = min(intermediate, key=lambda im: _dist(im, fp))
        for mode in TransportMode:
            edges.append(_make_edge(nearest_id, fp, mode))

    # Some FP-FP lateral links (mule only, ~20% pairs of nearest)
    if len(forward) > 1:
        n_lateral = max(1, int(len(forward) * 0.2))
        indices = rng.choice(
            len(forward), size=min(n_lateral, len(forward)), replace=False
        )
        for idx in indices:
            fp = forward[idx]
            others = sorted(
                [f for f in forward if f.node_id != fp.node_id],
                key=lambda f: _dist(fp, f),
            )
            if others:
                edges.append(_make_edge(fp, others[0], TransportMode.MULE))

    return edges
