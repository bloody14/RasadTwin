# ADR-002: PostgreSQL and PostGIS Core Data Architecture

## Context
As RasadTwin scales into a full-project architecture, in-memory Python structures are insufficient for complex spatial queries, multi-modal routing, and persistent relationships.

## Decision
Adopt PostgreSQL with the PostGIS extension as the central HQ data platform.

## Rationale
PostGIS natively supports advanced geospatial indexing, coordinate math, and bounding constraints necessary for terrain and route analysis. PostgreSQL provides robust relational integrity.

## Consequences
- Requires a PostgreSQL runtime environment for production.
- Introduces database schema migration workflows.

## Status
PROPOSED
