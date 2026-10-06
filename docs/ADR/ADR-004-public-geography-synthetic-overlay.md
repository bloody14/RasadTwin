# ADR-004: Public Geography + Synthetic Overlay

## Context
Using purely fictional maps reduces the demonstrator's believability. Using real military bases violates security policies.

## Decision
Use real public geographic data (OpenStreetMap for roads, SRTM for elevation, Open-Meteo for weather) and overlay 100% synthetic logistics networks on top.

## Rationale
Demonstrates real-world environmental impact logic (e.g., snow on real elevation profiles blocking a synthetic route) without exposing any actual defense infrastructure.

## Consequences
- Requires ETL pipelines to ingest OSM/SRTM data.
- Demands strict separation of data layers.

## Status
ACCEPTED
