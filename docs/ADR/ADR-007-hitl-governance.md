# ADR-007: HITL Governance

## Context
Initial prototypes combined system recommendations and user actions into ambiguous strings, muddying the audit trail.

## Decision
Strictly decouple Human-In-The-Loop (HITL) actions into `system_recommendation` (LOCAL/GLOBAL/PRESERVE), `user_action` (APPROVE/REJECT/OVERRIDE), and `selected_scope`.

## Rationale
Establishes an immutable, unambiguous ledger separating what the AI suggested from what the human commander actually authorized.

## Consequences
- Requires slightly more complex UI payload structures.
- Significantly improves post-action forensic auditing.

## Status
ACCEPTED
