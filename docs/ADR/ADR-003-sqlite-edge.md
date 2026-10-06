# ADR-003: SQLite Edge Cache

## Context
Forward command posts experience degraded network connectivity. Relying solely on a central PostgreSQL database would render the dashboard useless offline.

## Decision
Deploy local SQLite databases on edge nodes to act as an offline cache and transactional queue.

## Rationale
SQLite is file-based, dependency-free, and handles local querying exceptionally well. It enables the UI to remain functional offline.

## Consequences
- Requires synchronization logic (e.g., CRDTs or timestamp reconciliation) when the network is restored.
- HITL decisions must be queued locally.

## Status
PROPOSED
