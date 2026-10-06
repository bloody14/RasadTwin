# ADR-006: Offline-First Synchronization

## Context
When an edge node transitions from Offline to Online, conflicting state modifications (e.g., local inventory updates vs. HQ updates) must be resolved.

## Decision
Implement a queue-based synchronization model prioritizing "Commander Override Wins" or strict timestamp-based conflict resolution.

## Rationale
Ensures local decisions made in life-or-death scenarios are not silently overwritten by delayed HQ updates.

## Consequences
- High backend engineering complexity.
- Requires transaction ledgers on both Central and Edge databases.

## Status
PROPOSED
